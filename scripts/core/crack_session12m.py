#!/usr/bin/env python3
"""Session 12m: CONSENSUS ASSEMBLY via voting-based alignment.

Key insight: 70 books are ~10x overlapping windows into the same ~500 char narrative.
Homophonic substitution means same text → different codes.
Instead of code-level overlap, align decoded books using sliding window correlation
and build a consensus sequence by voting across all aligned books.
"""

import json, re
from collections import Counter, defaultdict

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

corrected = []
for book_str in raw_books:
    if len(book_str) % 2 != 0:
        corrected.append(book_str[:-1])
    else:
        corrected.append(book_str)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]
def decode_str(s, m=None):
    if m is None: m = mapping
    codes = parse_codes(s)
    return ''.join(m.get(c, '?') for c in codes)
def collapse(s):
    return re.sub(r'(.)\1+', r'\1', s)

print("=" * 80)
print("SESSION 12m: CONSENSUS ASSEMBLY VIA VOTING")
print("=" * 80)

# 1. Decode all books
decoded_books = [decode_str(s) for s in corrected]
collapsed_books = [collapse(d) for d in decoded_books]

print(f"\n1. BOOK STATS")
print("-" * 60)
print(f"  Total books: {len(decoded_books)}")
print(f"  Decoded lengths: {min(len(d) for d in decoded_books)}-{max(len(d) for d in decoded_books)}")
print(f"  Collapsed lengths: {min(len(c) for c in collapsed_books)}-{max(len(c) for c in collapsed_books)}")

# 2. Build seed from the raw-code assembly (best known approach: 25 books)
# Use greedy raw-code assembly as seed
overlaps = {}
for i in range(len(corrected)):
    for j in range(len(corrected)):
        if i == j: continue
        si = corrected[i]
        sj = corrected[j]
        for k in range(min(len(si), len(sj)), 3, -2):
            if si[-k:] == sj[:k]:
                overlaps[(i,j)] = k // 2
                break

best_merged = ''
best_used = set()
best_start = -1
best_contained = set()

for start_idx in range(len(corrected)):
    merged = corrected[start_idx]
    used = {start_idx}
    changed = True
    while changed:
        changed = False
        best_bi = None
        best_ov = 0
        best_side = None
        best_new = ''
        for bi in range(len(corrected)):
            if bi in used: continue
            text = corrected[bi]
            for k in range(min(len(merged), len(text)), 3, -2):
                if merged[-k:] == text[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'right'
                        best_new = text[k:]
                    break
            for k in range(min(len(merged), len(text)), 3, -2):
                if text[-k:] == merged[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'left'
                        best_new = text[:-k]
                    break
        if best_bi is not None and best_ov >= 4:
            used.add(best_bi)
            if best_side == 'right':
                merged += best_new
            else:
                merged = best_new + merged
            changed = True

    contained = set()
    for bi in range(len(corrected)):
        if corrected[bi] in merged:
            contained.add(bi)

    if len(contained) > len(best_contained):
        best_merged = merged
        best_used = set(used)
        best_start = start_idx
        best_contained = set(contained)

seed_raw = best_merged
seed_decoded = decode_str(seed_raw)
seed_collapsed = collapse(seed_decoded)

print(f"\n2. SEED SUPERSTRING (raw-code assembly)")
print("-" * 60)
print(f"  Start: B{best_start:02d}, Books used: {len(best_used)}, Contained: {len(best_contained)}")
print(f"  Raw codes: {len(seed_raw)//2}, Decoded: {len(seed_decoded)}, Collapsed: {len(seed_collapsed)}")

# 3. For each uncontained book, find best alignment against seed at COLLAPSED level
print(f"\n3. ALIGNING REMAINING BOOKS TO SEED")
print("-" * 60)

missing = sorted(set(range(len(decoded_books))) - best_contained)
print(f"  Missing books: {len(missing)}")

def best_alignment(ref, query, min_match=5):
    """Find best position to align query against ref using sliding window.
    Returns (position, score, direction) where position is in ref coordinates."""
    best_pos = -1
    best_score = 0
    best_dir = None

    ref_len = len(ref)
    q_len = len(query)

    # Slide query along ref
    for offset in range(-q_len + min_match, ref_len - min_match + 1):
        # overlap region
        r_start = max(0, offset)
        r_end = min(ref_len, offset + q_len)
        q_start = max(0, -offset)
        q_end = q_start + (r_end - r_start)

        if r_end - r_start < min_match:
            continue

        matches = 0
        total = r_end - r_start
        for i in range(total):
            if ref[r_start + i] == query[q_start + i]:
                matches += 1

        score = matches / total if total > 0 else 0
        if matches > best_score and score >= 0.5:
            best_score = matches
            best_pos = offset

    return best_pos, best_score

# Align each missing book to the collapsed seed
alignments = []
for bi in missing:
    book_col = collapsed_books[bi]
    pos, score = best_alignment(seed_collapsed, book_col, min_match=5)
    if pos != -1:
        overlap_len = min(len(seed_collapsed) - max(0, pos), len(book_col) - max(0, -pos))
        match_pct = score / overlap_len * 100 if overlap_len > 0 else 0
        alignments.append((bi, pos, score, overlap_len, match_pct))

alignments.sort(key=lambda x: -x[2])
print(f"  Books aligned: {len(alignments)}/{len(missing)}")
for bi, pos, score, ov_len, pct in alignments[:20]:
    book_col = collapsed_books[bi]
    print(f"    B{bi:02d} ({len(book_col)} chars): pos={pos}, matches={score}/{ov_len} ({score/ov_len*100:.0f}%)")

# 4. Build position-based voting matrix
print(f"\n4. CONSENSUS BUILDING")
print("-" * 60)

# Map each contained book to its position in the seed
book_positions = {}  # bi -> start position in seed_collapsed

# Books from the raw-code assembly are embedded in seed_raw
for bi in best_contained:
    # Find position of this book's decoded text in the seed decoded text
    book_decoded = decoded_books[bi]
    book_collapsed = collapsed_books[bi]

    # Search in collapsed seed
    idx = seed_collapsed.find(book_collapsed)
    if idx >= 0:
        book_positions[bi] = idx

# Add aligned missing books
for bi, pos, score, ov_len, pct in alignments:
    if score / ov_len >= 0.5:  # At least 50% match
        book_positions[bi] = max(0, pos)

print(f"  Books with positions: {len(book_positions)}")

# Build voting matrix: for each position in narrative, count letter votes
max_pos = max(pos + len(collapsed_books[bi]) for bi, pos in book_positions.items())
# Extend beyond seed if books extend further
max_pos = max(max_pos, len(seed_collapsed) + 50)

votes = defaultdict(Counter)  # position -> Counter of letters

for bi, start_pos in book_positions.items():
    book_col = collapsed_books[bi]
    for i, ch in enumerate(book_col):
        pos = start_pos + i
        votes[pos][ch] += 1

# Build consensus from votes
consensus = []
vote_details = []
for pos in range(max_pos):
    if pos in votes and votes[pos]:
        top = votes[pos].most_common(1)[0]
        letter = top[0]
        count = top[1]
        total = sum(votes[pos].values())
        consensus.append(letter)
        vote_details.append((letter, count, total))
    else:
        consensus.append('.')
        vote_details.append(('.', 0, 0))

consensus_text = ''.join(consensus).strip('.')
# Remove trailing dots
while consensus_text.endswith('.'):
    consensus_text = consensus_text[:-1]

print(f"  Consensus length: {len(consensus_text)}")
print(f"  Seed length: {len(seed_collapsed)}")

# Show consensus with confidence
print(f"\n  CONSENSUS TEXT:")
for i in range(0, len(consensus_text), 70):
    line = consensus_text[i:i+70]
    # Mark low-confidence positions
    conf_line = ''
    for j, ch in enumerate(line):
        pos = i + j
        if pos < len(vote_details):
            letter, count, total = vote_details[pos]
            if total > 0 and count / total < 0.7:
                conf_line += '?'
            elif total >= 3:
                conf_line += '#'
            elif total >= 1:
                conf_line += '.'
            else:
                conf_line += ' '
        else:
            conf_line += ' '
    print(f"  [{i:4d}] {line}")
    print(f"         {conf_line}")

# 5. Show positions with disagreement (potential mapping errors!)
print(f"\n5. POSITION DISAGREEMENTS (potential mapping errors)")
print("-" * 60)

disagreements = []
for pos in range(len(consensus_text)):
    if pos in votes and len(votes[pos]) > 1:
        total = sum(votes[pos].values())
        top = votes[pos].most_common(1)[0]
        if top[1] / total < 0.9 and total >= 3:
            disagreements.append((pos, votes[pos], total))

print(f"  Positions with <90% agreement (3+ votes): {len(disagreements)}")
for pos, vote_counter, total in disagreements[:30]:
    vote_str = ', '.join(f"{ch}:{cnt}" for ch, cnt in vote_counter.most_common())
    context = consensus_text[max(0,pos-5):pos+6]
    print(f"    pos {pos:3d}: [{vote_str}] total={total} context='...{context}...'")

# 6. DP segmentation of consensus
print(f"\n6. DP SEGMENTED CONSENSUS")
print("-" * 60)

NEG_INF = float('-inf')
german_words = [
    'EILCHANHEARUCHTIG', 'EDETOTNIURGS', 'WRLGTNELNRHELUIRUN',
    'TIUMENGEMI', 'SCHWITEIONE', 'LABGZERAS', 'HEDEMI', 'TAUTR',
    'LABRNI', 'ADTHARSC', 'ENGCHD', 'KELSEI',
    'NGETRAS', 'GEVMT', 'DGEDA', 'TEMDIA', 'UISEMIV',
    'TEIGN', 'CHN', 'SCE',
    'KOENIG', 'GEIGET', 'SCHAUN', 'URALTE', 'FINDEN', 'DIESER',
    'NORDEN', 'SONNE', 'UNTER', 'NICHT', 'WERDE',
    'STEINEN', 'STEIN', 'STEINE', 'DENEN', 'ERDE', 'VIEL', 'RUNE', 'RUNEN',
    'STEH', 'LIED', 'SEGEN', 'DORT', 'DENN',
    'GOLD', 'MOND', 'WELT', 'ENDE', 'REDE',
    'HUND', 'SEIN', 'WIRD', 'KLAR', 'ERST',
    'HWND', 'WISET',
    'EINEN', 'EINER', 'SEINE', 'SEIDE',
    'TAG', 'WEG', 'DER', 'DEN', 'DIE', 'DAS',
    'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON',
    'MIT', 'WIE', 'SEI', 'AUS', 'ORT', 'TUN',
    'NUR', 'SUN', 'TOT', 'GAR', 'ACH', 'ZUM',
    'HIN', 'HER', 'ALS', 'AUCH', 'RUND', 'GEH',
    'NACH', 'NOCH', 'ALLE', 'WOHL',
    'HIER', 'SICH', 'SIND', 'SEHR',
    'ABER', 'ODER', 'WENN', 'DANN',
    'ALTE', 'EDEL', 'HELD', 'LAND',
    'WARD', 'WART',
    'ER', 'ES', 'IN', 'SO', 'AN', 'IM',
    'DA', 'NU', 'IR', 'EZ', 'DO', 'OB', 'IE',
    'TER', 'HIET', 'DU', 'HAT', 'BIS', 'SINE',
    'EHRE', 'NIDEN',
    'UM', 'AM', 'AB', 'ZU', 'BI', 'ALT', 'NEU', 'DIR', 'MAN',
]
german_words = list(dict.fromkeys(german_words))
word_scores = {w: len(w) * 3 for w in german_words}
all_words = sorted(word_scores.keys(), key=len, reverse=True)

def dp_segment(text):
    n = len(text)
    if n == 0: return [], 0, 0
    dp = [NEG_INF] * (n + 1)
    back = [None] * (n + 1)
    dp[0] = 0
    for i in range(n):
        if dp[i] == NEG_INF: continue
        ns = dp[i] - 1
        if ns > dp[i+1]:
            dp[i+1] = ns
            back[i+1] = ('unk', i)
        for word in all_words:
            wl = len(word)
            if i + wl <= n and text[i:i+wl] == word:
                ns = dp[i] + word_scores.get(word, wl)
                if ns > dp[i+wl]:
                    dp[i+wl] = ns
                    back[i+wl] = ('word', i, word)
    pos = n
    parts = []
    covered = 0
    while pos > 0:
        info = back[pos]
        if info is None:
            parts.append(('?', text[pos-1:pos]))
            pos -= 1
        elif info[0] == 'unk':
            parts.append(('?', text[info[1]:pos]))
            pos = info[1]
        elif info[0] == 'word':
            parts.append(('W', info[2]))
            covered += len(info[2])
            pos = info[1]
    parts.reverse()
    return parts, covered, n

parts, covered, total = dp_segment(consensus_text)
print(f"  Coverage: {covered}/{total} = {covered*100/total:.1f}%\n")

line = ''
line_num = 1
for ptype, ptext in parts:
    if ptype == 'W':
        word = ptext
    else:
        word = f'[{ptext}]'
    if len(line) + len(word) + 1 > 75:
        print(f"    {line_num:3d}| {line}")
        line = word + ' '
        line_num += 1
    else:
        line += word + ' '
if line.strip():
    print(f"    {line_num:3d}| {line}")

# 7. Cross-check: which books are NOT well-aligned?
print(f"\n7. UNALIGNED BOOKS ANALYSIS")
print("-" * 60)

unaligned = sorted(set(range(len(decoded_books))) - set(book_positions.keys()))
print(f"  Unaligned books: {len(unaligned)}")
for bi in unaligned:
    book_col = collapsed_books[bi]
    # Find longest common substring with consensus
    best_sub = ''
    for k in range(len(book_col), 2, -1):
        found = False
        for start in range(len(book_col) - k + 1):
            sub = book_col[start:start+k]
            if sub in consensus_text:
                best_sub = sub
                found = True
                break
        if found:
            break
    print(f"  B{bi:02d} ({len(book_col)} chars): best common substr={len(best_sub)} chars")
    if best_sub:
        print(f"       '{best_sub[:50]}...' at consensus pos {consensus_text.find(best_sub)}")

# 8. Try extending consensus with unaligned book content
print(f"\n8. EXTENDING CONSENSUS WITH UNALIGNED BOOKS")
print("-" * 60)

extended = consensus_text
for bi in unaligned:
    book_col = collapsed_books[bi]
    # Try suffix/prefix overlaps
    for k in range(min(len(extended), len(book_col)), 2, -1):
        if extended[-k:] == book_col[:k]:
            new_part = book_col[k:]
            if len(new_part) > 0:
                extended += new_part
                print(f"  Extended right with B{bi:02d}: +{len(new_part)} chars (overlap {k})")
            break
    for k in range(min(len(extended), len(book_col)), 2, -1):
        if book_col[-k:] == extended[:k]:
            new_part = book_col[:-k]
            if len(new_part) > 0:
                extended = new_part + extended
                print(f"  Extended left with B{bi:02d}: +{len(new_part)} chars (overlap {k})")
            break

if len(extended) > len(consensus_text):
    print(f"\n  Extended consensus: {len(extended)} chars (was {len(consensus_text)})")
    parts2, covered2, total2 = dp_segment(extended)
    print(f"  Extended coverage: {covered2}/{total2} = {covered2*100/total2:.1f}%")
else:
    print(f"  No extension possible with suffix/prefix overlaps")

# 9. Final narrative
print(f"\n9. FINAL NARRATIVE")
print("-" * 60)
final = extended if len(extended) > len(consensus_text) else consensus_text
print(f"  Length: {len(final)} chars")
print()
for i in range(0, len(final), 70):
    print(f"  [{i:4d}] {final[i:i+70]}")

# 10. Letter frequency in consensus vs expected German
print(f"\n10. CONSENSUS LETTER FREQUENCIES")
print("-" * 60)
letter_counts = Counter(final)
total_letters = sum(letter_counts.values())
expected = {
    'E': 17.4, 'N': 9.8, 'I': 7.6, 'S': 7.3, 'R': 7.0,
    'A': 6.5, 'T': 6.2, 'D': 5.1, 'H': 4.8, 'U': 4.4,
    'L': 3.4, 'C': 2.7, 'G': 3.0, 'M': 2.5, 'O': 2.5,
    'B': 1.9, 'W': 1.9, 'F': 1.7, 'K': 1.2, 'Z': 1.1,
    'V': 0.7, 'P': 0.8
}
for ch, cnt in sorted(letter_counts.items(), key=lambda x: -x[1]):
    pct = cnt * 100 / total_letters
    exp = expected.get(ch, 0)
    diff = pct - exp
    flag = ' !!!' if abs(diff) > 2.0 else ''
    print(f"  {ch}: {cnt:4d} ({pct:5.1f}%) expected {exp:4.1f}% diff {diff:+5.1f}%{flag}")

print("\n" + "=" * 80)
print("SESSION 12m COMPLETE")
print("=" * 80)
