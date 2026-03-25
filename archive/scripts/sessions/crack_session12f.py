#!/usr/bin/env python3
"""Session 12f: Full re-analysis with correctly trimmed books + massive assembly"""

import json, re
from collections import Counter, defaultdict

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

print("=" * 80)
print("SESSION 12f: CORRECTED BOOKS + FULL ASSEMBLY")
print("=" * 80)

# CRITICAL FIX: Trim odd-length books (drop trailing digit)
corrected = []
for bi, book_str in enumerate(raw_books):
    if len(book_str) % 2 != 0:
        corrected.append(book_str[:-1])
    else:
        corrected.append(book_str)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]

books = [parse_codes(s) for s in corrected]

def decode(book, m=None):
    if m is None: m = mapping
    return ''.join(m.get(c, '?') for c in book)
def collapse(s):
    return re.sub(r'(.)\1+', r'\1', s)

# Verify: no unknowns now
total_q = sum(decode(b).count('?') for b in books)
print(f"\n  Unknown characters after trimming: {total_q} (should be 0)")

# 1. Full overlap matrix at code level
print("\n1. CODE-LEVEL OVERLAPS")
print("-" * 60)

code_strings = [c for c in corrected]
overlaps = {}
for i in range(len(books)):
    for j in range(len(books)):
        if i == j: continue
        si = code_strings[i]
        sj = code_strings[j]
        for k in range(min(len(si), len(sj)), 3, -2):
            if si[-k:] == sj[:k]:
                overlaps[(i,j)] = k // 2
                break

print(f"  Total overlapping pairs: {len(overlaps)}")

# 2. Greedy assembly with corrected books
print("\n2. GREEDY ASSEMBLY (BEST START)")
print("-" * 60)

best_merged = ''
best_used = set()
best_start = -1
best_order = []

for start_idx in range(len(books)):
    merged = code_strings[start_idx]
    used = {start_idx}
    order = [start_idx]

    changed = True
    while changed:
        changed = False
        best_bi = None
        best_ov = 0
        best_side = None
        best_new = ''

        for bi in range(len(books)):
            if bi in used: continue
            text = code_strings[bi]

            # Right
            for k in range(min(len(merged), len(text)), 3, -2):
                if merged[-k:] == text[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'right'
                        best_new = text[k:]
                    break
            # Left
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
            order.append(best_bi)
            if best_side == 'right':
                merged += best_new
            else:
                merged = best_new + merged
            changed = True

    if len(used) > len(best_used):
        best_merged = merged
        best_used = set(used)
        best_start = start_idx
        best_order = list(order)

print(f"  Best start: B{best_start:02d}")
print(f"  Books merged: {len(best_used)}/{len(books)}")
print(f"  Merge order: {best_order}")

# Check containment
contained = set()
for bi in range(len(books)):
    if code_strings[bi] in best_merged:
        contained.add(bi)
print(f"  Books contained: {len(contained)}/{len(books)}")
not_in = sorted(set(range(len(books))) - contained)
print(f"  NOT contained: {not_in}")

# 3. Try iterative assembly: after initial merge, try to add uncontained books
# by finding their position in the superstring (allowing internal matching)
print("\n3. ITERATIVE POSITION FINDING")
print("-" * 60)

# For books not contained, find where they best align
for bi in not_in[:15]:
    bk = code_strings[bi]
    # Find longest common substring
    best_match = 0
    best_pos = -1
    for start in range(0, len(best_merged) - 3, 2):
        match_len = 0
        for k in range(0, min(len(bk), len(best_merged) - start), 2):
            if bk[k:k+2] == best_merged[start+k:start+k+2]:
                match_len += 2
            else:
                break
        if match_len > best_match:
            best_match = match_len
            best_pos = start

    pct = best_match * 100 / len(bk) if len(bk) > 0 else 0
    print(f"  B{bi:02d}: {len(bk)//2} codes, best PREFIX match = {best_match//2} codes ({pct:.0f}%) at superstring pos {best_pos//2}")

# 4. Full decoded superstring
print("\n4. FULL DECODED SUPERSTRING")
print("-" * 60)

merged_codes = parse_codes(best_merged)
decoded = decode(merged_codes)
collapsed = collapse(decoded)
print(f"  Total codes: {len(merged_codes)}")
print(f"  Decoded chars: {len(decoded)}")
print(f"  Collapsed chars: {len(collapsed)}")
print()
for i in range(0, len(collapsed), 70):
    print(f"  [{i:4d}] {collapsed[i:i+70]}")

# 5. DP Segmentation with expanded word list
print("\n5. DP SEGMENTED NARRATIVE")
print("-" * 60)

NEG_INF = float('-inf')
german_words = [
    'EILCHANHEARUCHTIG', 'EDETOTNIURGS', 'WRLGTNELNRHELUIRUNN',
    'TIUMENGEMI', 'SCHWITEIONE', 'LABGZERAS', 'HEDEMI', 'TAUTR',
    'LABRNI', 'ADTHARSC', 'ENGCHD', 'KELSEI',
    'NGETRAS', 'GEVMT', 'DGEDA', 'TEMDIA', 'UISEMIV',
    'TEIGN', 'CHN', 'SCE',
    'KOENIG', 'GEIGET', 'SCHAUN', 'URALTE', 'FINDEN', 'DIESER',
    'NORDEN', 'SONNE', 'UNTER', 'NICHT', 'WERDE',
    'STEINEN', 'STEIN', 'DENEN', 'ERDE', 'VIEL', 'RUNE',
    'STEH', 'LIED', 'SEGEN', 'DORT', 'DENN',
    'GOLD', 'MOND', 'WELT', 'ENDE', 'REDE',
    'HUND', 'SEIN', 'WIRD', 'KLAR', 'ERST',
    'HWND', 'WISET', 'OWI', 'MINHE',
    'EINEN', 'EINER', 'SEINE', 'SEIDE',
    'TAG', 'WEG', 'DER', 'DEN', 'DIE', 'DAS',
    'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON',
    'MIT', 'WIE', 'SEI', 'AUS', 'ORT', 'TUN',
    'NUR', 'SUN', 'TOT', 'GAR', 'ACH', 'ZUM',
    'HIN', 'HER', 'ALS', 'AUCH', 'RUND', 'GEH',
    'NACH', 'IENE', 'NOCH', 'ALLE', 'WOHL',
    'HIER', 'SICH', 'SIND', 'SEHR',
    'ABER', 'ODER', 'WENN', 'DANN',
    'ALTE', 'EDEL', 'HELD', 'LAND',
    'WARD', 'WART',
    'ER', 'ES', 'IN', 'SO', 'AN', 'IM',
    'DA', 'NU', 'IR', 'EZ', 'DO', 'OB', 'IE',
    'TER', 'HIET',
    'DU', 'HAT', 'BIS', 'SINE',
    'STEINE', 'RUNEN', 'EHRE', 'NIDEN',
    'UM', 'AM', 'AB', 'ZU', 'BI',
    'ALT', 'NEU', 'DIR', 'MAN',
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

parts, covered, total = dp_segment(collapsed)
print(f"  Coverage: {covered}/{total} = {covered*100/total:.1f}%\n")

line = ''
line_num = 1
for ptype, ptext in parts:
    if ptype == 'W':
        word = ptext
    else:
        word = f'[{ptext}]'
    if len(line) + len(word) + 1 > 70:
        print(f"    {line_num:3d}| {line}")
        line = word + ' '
        line_num += 1
    else:
        line += word + ' '
if line.strip():
    print(f"    {line_num:3d}| {line}")

# 6. Per-book coverage with corrected parsing
print(f"\n6. PER-BOOK COVERAGE (CORRECTED)")
print("-" * 60)

all_collapsed = [collapse(decode(b)) for b in books]
total_corpus_chars = sum(len(t) for t in all_collapsed)
total_corpus_cov = 0
book_cov = []
for bi in range(len(books)):
    p, c, t = dp_segment(all_collapsed[bi])
    pct = c * 100 / t if t > 0 else 0
    total_corpus_cov += c
    book_cov.append((bi, pct, t))

book_cov.sort(key=lambda x: -x[1])
for bi, pct, tot in book_cov[:15]:
    bar = '#' * int(pct / 5) + '.' * (20 - int(pct / 5))
    print(f"  B{bi:02d} [{bar}] {pct:5.1f}% ({tot} chars)")

corpus_pct = total_corpus_cov * 100 / total_corpus_chars
print(f"\n  TOTAL CORPUS: {total_corpus_cov}/{total_corpus_chars} = {corpus_pct:.1f}%")
print(f"  Books >90%: {sum(1 for _,p,_ in book_cov if p >= 90)}")
print(f"  Books >80%: {sum(1 for _,p,_ in book_cov if p >= 80)}")
print(f"  Books >70%: {sum(1 for _,p,_ in book_cov if p >= 70)}")
print(f"  Books >50%: {sum(1 for _,p,_ in book_cov if p >= 50)}")

# 7. Check: does trimming odd books change the overall mapping quality?
print(f"\n7. LETTER FREQUENCY WITH CORRECTED BOOKS")
print("-" * 60)

all_codes_corrected = [c for b in books for c in b]
code_freq = Counter(all_codes_corrected)
by_letter = defaultdict(int)
for c in all_codes_corrected:
    by_letter[mapping.get(c, '?')] += 1

total_letters = sum(by_letter.values())
# Expected German letter frequencies
expected = {
    'E': 17.4, 'N': 9.8, 'I': 7.6, 'S': 7.3, 'R': 7.0,
    'A': 6.5, 'T': 6.2, 'D': 5.1, 'H': 4.8, 'U': 4.3,
    'L': 3.4, 'C': 3.1, 'G': 3.0, 'M': 2.5, 'O': 2.5,
    'B': 1.9, 'W': 1.9, 'F': 1.7, 'K': 1.2, 'Z': 1.1,
    'V': 0.9, 'P': 0.8
}

print(f"  Letter frequencies (corrected books):")
for letter in sorted(by_letter.keys()):
    actual_pct = by_letter[letter] * 100 / total_letters
    exp = expected.get(letter, 0)
    diff = actual_pct - exp
    flag = ' <-- ANOMALY' if abs(diff) > 2.0 else ''
    print(f"    {letter}: {actual_pct:5.1f}% (exp {exp:.1f}%, diff {diff:+.1f}%){flag}")

print("\n" + "=" * 80)
print("SESSION 12f COMPLETE")
print("=" * 80)
