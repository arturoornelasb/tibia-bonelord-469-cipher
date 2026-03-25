#!/usr/bin/env python3
"""Session 11a: Smart boundary segmentation + persistent unknown region attack"""

import json, re
from collections import Counter, defaultdict

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]
books = [parse_codes(b) for b in raw_books]
def decode(book, m=None):
    if m is None: m = mapping
    return ''.join(m.get(c, '?') for c in book)
def collapse(s):
    return re.sub(r'(.)\1+', r'\1', s)

rev_map = defaultdict(list)
for code, letter in mapping.items():
    rev_map[letter].append(code)

print("=" * 80)
print("SESSION 11a: BOUNDARY-AWARE SEGMENTATION")
print("=" * 80)

# 1. Smart decode that inserts | at cross-code double boundaries
def smart_decode_book(book):
    """Returns list of (letter, is_boundary) tuples"""
    result = []
    for ci in range(len(book)):
        letter = mapping.get(book[ci], '?')
        if ci > 0:
            prev_letter = mapping.get(book[ci-1], '?')
            if letter == prev_letter:
                if book[ci] != book[ci-1]:
                    # Cross-code boundary - mark it
                    result.append(('|', True))
                    result.append((letter, False))
                # else: same code double, skip (collapse)
            else:
                result.append((letter, False))
        else:
            result.append((letter, False))
    return result

def smart_text(book):
    """Get text with | boundary markers, then segment around them"""
    parts = smart_decode_book(book)
    return ''.join(ch for ch, _ in parts)

# 2. Segment text treating | as forced word boundaries
NEG_INF = float('-inf')

# Comprehensive word list
german_words = [
    # Known proper nouns (treat as whole words)
    'EILCHANHEARUCHTIG', 'EDETOTNIURGS', 'WRLGTNELNRHELUIRUNN',
    'TIUMENGEMI', 'SCHWITEIONE', 'LABGZERAS', 'HEDEMI', 'TAUTR',
    'LABRNI', 'ADTHARSC', 'ENGCHD', 'KELSEI',
    # Known unknowns (consistent patterns)
    'NGETRAS', 'GEVMT', 'DGEDA', 'TEMDIA', 'UISEMIV',
    'TEIGN', 'CHN', 'SCE',
    # Common MHG/German words
    'KOENIG', 'GEIGET', 'SCHAUN', 'URALTE', 'FINDEN', 'DIESER',
    'NORDEN', 'SONNE', 'UNTER', 'NICHT', 'WERDE',
    'STEINEN', 'STEIN', 'DENEN', 'ERDE', 'VIEL', 'RUNE',
    'STEH', 'LIED', 'SEGEN', 'DORT', 'DENN',
    'GOLD', 'MOND', 'WELT', 'ENDE', 'REDE',
    'HUND', 'SEIN', 'WIRD', 'KLAR', 'ERST',
    'HWND', 'WISET', 'OWI', 'MINHE',
    'EINEN', 'EINER', 'SEINE', 'SEIDE',
    'GROZ', 'SOLCH', 'DOCH', 'WOHL',
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
]
german_words = list(dict.fromkeys(german_words))
word_scores = {w: len(w) * 3 for w in german_words}
all_words_sorted = sorted(word_scores.keys(), key=len, reverse=True)

def dp_segment(text):
    """DP segmentation that respects | boundaries"""
    n = len(text)
    if n == 0: return [], 0, 0
    dp = [NEG_INF] * (n + 1)
    back = [None] * (n + 1)
    dp[0] = 0

    for i in range(n):
        if dp[i] == NEG_INF: continue
        if text[i] == '|':
            # Must advance past |, it's a forced boundary
            if dp[i] > dp[i+1]:
                dp[i+1] = dp[i]
                back[i+1] = ('boundary', i)
            continue

        # Unknown char
        ns = dp[i] - 1
        if ns > dp[i+1]:
            dp[i+1] = ns
            back[i+1] = ('unk', i)

        # Try all words, but they cannot cross a |
        for word in all_words_sorted:
            wl = len(word)
            end = i + wl
            if end > n: continue
            # Check no | in the span
            span = text[i:end]
            if '|' in span: continue
            if span == word:
                ns = dp[i] + word_scores.get(word, wl)
                if ns > dp[end]:
                    dp[end] = ns
                    back[end] = ('word', i, word)

    pos = n
    parts = []
    covered = 0
    while pos > 0:
        info = back[pos]
        if info is None:
            parts.append(('?', text[pos-1:pos]))
            pos -= 1
        elif info[0] == 'boundary':
            parts.append(('|', '|'))
            pos = info[1]
        elif info[0] == 'unk':
            parts.append(('?', text[info[1]:pos]))
            pos = info[1]
        elif info[0] == 'word':
            parts.append(('W', info[2]))
            covered += len(info[2])
            pos = info[1]
    parts.reverse()
    return parts, covered, n

# 3. Compare coverage: normal vs smart
print("\n1. COVERAGE COMPARISON: NORMAL vs SMART")
print("-" * 60)

total_cov_normal = 0
total_chars_normal = 0
total_cov_smart = 0
total_chars_smart = 0

for bi in range(len(books)):
    normal_text = collapse(decode(books[bi]))
    smart = smart_text(books[bi])

    # Normal segmentation
    _, cov_n, tot_n = dp_segment(normal_text)
    total_cov_normal += cov_n
    total_chars_normal += tot_n

    # Smart segmentation
    _, cov_s, tot_s = dp_segment(smart)
    # Subtract | chars from total
    pipe_count = smart.count('|')
    adj_tot = tot_s - pipe_count
    total_cov_smart += cov_s
    total_chars_smart += adj_tot

pct_normal = total_cov_normal * 100 / total_chars_normal
pct_smart = total_cov_smart * 100 / total_chars_smart
print(f"  Normal collapse: {total_cov_normal}/{total_chars_normal} = {pct_normal:.1f}%")
print(f"  Smart boundary:  {total_cov_smart}/{total_chars_smart} = {pct_smart:.1f}%")
print(f"  Delta: {pct_smart - pct_normal:+.1f}%")

# 4. Show the best and worst books with smart decode
print("\n\n2. PER-BOOK SMART SEGMENTATION")
print("-" * 60)

book_results = []
for bi in range(len(books)):
    smart = smart_text(books[bi])
    parts, cov, tot = dp_segment(smart)
    pipe_count = smart.count('|')
    adj_tot = tot - pipe_count
    pct = cov * 100 / adj_tot if adj_tot > 0 else 0
    book_results.append((bi, pct, parts, smart))

book_results.sort(key=lambda x: x[1], reverse=True)

print("  TOP 10:")
for bi, pct, parts, smart in book_results[:10]:
    formatted = ''
    for ptype, ptext in parts:
        if ptype == 'W': formatted += ptext + ' '
        elif ptype == '|': formatted += '| '
        else: formatted += f'[{ptext}]'
    print(f"  B{bi:02d} ({pct:4.1f}%): {formatted[:100]}")

print("\n  BOTTOM 10:")
for bi, pct, parts, smart in book_results[-10:]:
    formatted = ''
    for ptype, ptext in parts:
        if ptype == 'W': formatted += ptext + ' '
        elif ptype == '|': formatted += '| '
        else: formatted += f'[{ptext}]'
    print(f"  B{bi:02d} ({pct:4.1f}%): {formatted[:100]}")

# 5. Attack persistent unknown regions using smart text
print("\n\n3. PERSISTENT UNKNOWN REGIONS (SMART)")
print("-" * 60)

# Collect unknown runs from smart-segmented text
unk_runs_smart = Counter()
for bi in range(len(books)):
    smart = smart_text(books[bi])
    parts, _, _ = dp_segment(smart)

    i = 0
    while i < len(parts):
        if parts[i][0] == '?' or parts[i][0] == '|':
            unk_str = ''
            j = i
            while j < len(parts) and (parts[j][0] == '?' or parts[j][0] == '|'):
                unk_str += parts[j][1]
                j += 1
            unk_clean = unk_str.replace('|', ' ')
            if len(unk_clean.replace(' ', '')) >= 3:
                # Get surrounding words
                before = ''
                if i > 0 and parts[i-1][0] == 'W':
                    before = parts[i-1][1]
                after = ''
                if j < len(parts) and parts[j][0] == 'W':
                    after = parts[j][1]
                key = f"{before}[{unk_clean}]{after}"
                unk_runs_smart[key] += 1
            i = j
        else:
            i += 1

print(f"  Unique unknown runs: {len(unk_runs_smart)}")
print(f"\n  Most common (smart-segmented):")
for run, count in unk_runs_smart.most_common(25):
    print(f"    x{count}: {run}")

# 6. Analyze the most persistent unknowns for possible words
print("\n\n4. DEEP ANALYSIS OF TOP UNKNOWN REGIONS")
print("-" * 60)

# Focus on the most common unknown regions
target_regions = [
    ('DNRHAUNRNVMHISDIZA', 'between DEN...RUNE'),
    ('EUGENDRTHENAEDEULGHLWUOEHSG', 'between DAS...SEI'),
    ('NTENTUIGA', 'between ENDE...ER'),
    ('WRLGTNELNRHELU', 'after STEH'),
    ('OIAITOEMENDGEMKMTGRSCAS', 'between ERDE...EZ'),
    ('VMTEGE', 'between IST...VIEL'),
    ('URIHWNRS', 'between WIR...IST'),
    ('AMNEUD', 'between TER...ES'),
    ('ELUSED', 'between EZ...HER'),
    ('GELNMH', 'between IR...SO'),
    ('LRSZTHK', 'between IST...WIR'),
]

# For each region, try to find German words or word combinations
for region, desc in target_regions:
    print(f"\n  [{region}] ({desc}):")

    # Try all possible splits and word matches
    best_split = None
    best_coverage = 0

    # Exhaustive 2-split search
    for i in range(1, len(region)):
        left = region[:i]
        right = region[i:]
        left_score = len(left) if left in word_scores else 0
        right_score = len(right) if right in word_scores else 0
        score = left_score + right_score
        if score > best_coverage:
            best_coverage = score
            best_split = (left, right)

    # Exhaustive 3-split search
    for i in range(1, len(region)):
        for j in range(i+1, len(region)):
            p1 = region[:i]
            p2 = region[i:j]
            p3 = region[j:]
            s1 = len(p1) if p1 in word_scores else 0
            s2 = len(p2) if p2 in word_scores else 0
            s3 = len(p3) if p3 in word_scores else 0
            score = s1 + s2 + s3
            if score > best_coverage:
                best_coverage = score
                best_split = (p1, p2, p3)

    # Also check for known common German words
    found_words = []
    for word in all_words_sorted:
        if word in region:
            pos = region.index(word)
            found_words.append((word, pos))

    if found_words:
        print(f"    Known words found: {found_words}")
    if best_split and best_coverage > 0:
        marked = ' + '.join(f'[{p}]' if p not in word_scores else p for p in best_split)
        print(f"    Best split ({best_coverage} chars covered): {marked}")
    else:
        print(f"    No known words found")

    # Check if this could be a run-length encoded word
    # (letter frequencies suggest German patterns)
    vowels = sum(1 for c in region if c in 'AEIOU')
    consonants = len(region) - vowels
    print(f"    Length: {len(region)}, vowels: {vowels}, consonants: {consonants}")

    # MHG word candidates based on pattern
    if len(region) <= 8:
        # Short region - might be a single word
        print(f"    Could be MHG word: {region}")
    else:
        # Long region - likely multiple words
        # Try to identify syllable boundaries
        syllables = []
        current = ''
        for ch in region:
            current += ch
            if ch in 'AEIOU' and len(current) >= 2:
                syllables.append(current)
                current = ''
        if current:
            syllables.append(current)
        print(f"    Syllable attempt: {'-'.join(syllables)}")

# 7. Cross-reference: what do the BEST books tell us about reading order?
print("\n\n5. NARRATIVE RECONSTRUCTION (BEST BOOKS)")
print("-" * 60)

# Use B05 and B09 (identical high-coverage) as the core
# Then follow the overlap chain
print("  Core narrative (B05, 94.7%):")
text = collapse(decode(books[5]))
parts, _, _ = dp_segment(text)
trans = {
    'HIER': 'here', 'TAUTR': 'Tautr', 'IST': 'is',
    'EILCHANHEARUCHTIG': '[renowned]',
    'ER': 'he', 'SO': 'thus', 'DAS': 'that', 'TUN': 'does',
    'DIESER': 'this', 'EINER': 'one', 'SEIN': 'his',
    'EDETOTNIURGS': 'Edetotniurgs',
    'LABRNI': 'Labrni', 'WIR': 'we', 'UND': 'and',
    'IE': 'ever', 'IN': 'in', 'HEDEMI': 'Hedemi',
    'DIE': 'the', 'URALTE': 'ancient', 'STEINEN': 'stones',
    'TER': 'the', 'ADTHARSC': 'Adtharsc',
    'SCHAUN': 'behold', 'WISET': 'know(ye)',
    'TIUMENGEMI': 'Tiumengemi', 'ORT': 'place',
    'ENGCHD': 'Engchd', 'KELSEI': 'Kelsei',
    'DEN': 'the', 'RUNE': 'rune(s)', 'UNTER': 'under',
    'AUS': 'from', 'HIET': 'was-called',
    'ENDE': 'end', 'SCHWITEIONE': 'Schwiteione',
    'WIRD': 'becomes', 'SEI': 'be!', 'GEVMT': '[word]',
    'WIE': 'as', 'TAG': 'day', 'SICH': 'self',
    'MINHE': 'Minhe', 'AUCH': 'also', 'GEIGET': 'shows',
    'CHN': '[CHN]', 'SCE': '[SCE]', 'LABGZERAS': 'Labgzeras',
    'KOENIG': 'king', 'DENEN': 'to-whom', 'VIEL': 'much',
    'STEH': 'stand', 'HWND': 'hound', 'FINDEN': 'find',
    'TEIGN': '[TEIGN]', 'ERST': 'first',
    'GEH': 'go', 'EIN': 'a', 'NGETRAS': '[NGETRAS]',
    'ERDE': 'earth', 'SIE': 'they', 'OWI': 'alas',
    'DENN': 'for', 'DORT': 'there', 'SEGEN': 'blessing',
    'GOLD': 'gold', 'MOND': 'moon', 'WELT': 'world',
    'SONNE': 'sun', 'NORDEN': 'north',
    'DGEDA': '[DGEDA]', 'TEMDIA': '[TEMDIA]',
    'UISEMIV': '[UISEMIV]', 'NUR': 'only', 'SUN': 'sun',
    'TOT': 'dead', 'GAR': 'very', 'ZUM': 'to-the',
    'HIN': 'away', 'HER': 'here', 'ALS': 'as/when',
    'RUND': 'round', 'NACH': 'after',
    'NOCH': 'still', 'ALLE': 'all', 'WOHL': 'well',
    'SIND': 'are', 'SEHR': 'very',
    'ABER': 'but', 'ODER': 'or', 'WENN': 'when',
    'DANN': 'then', 'ALTE': 'old', 'EDEL': 'noble',
    'HELD': 'hero', 'LAND': 'land', 'WARD': 'became',
    'ES': 'it', 'AN': 'at', 'IM': 'in-the',
    'DA': 'there', 'NU': 'now', 'IR': 'you(pl)',
    'EZ': 'it(MHG)', 'DO': 'then(MHG)', 'OB': 'whether',
    'MIT': 'with', 'WIE': 'as/how', 'VON': 'from',
    'NICHT': 'not', 'WERDE': 'become', 'STEIN': 'stone',
    'SEIDE': 'silk', 'EINE': 'a',
}

# Print word-by-word
line = ''
for ptype, ptext in parts:
    if ptype == 'W':
        t = trans.get(ptext, ptext)
        word = f'{ptext}({t})'
    else:
        word = f'[{ptext}]'
    if len(line) + len(word) + 1 > 80:
        print(f"    {line}")
        line = word + ' '
    else:
        line += word + ' '
if line.strip():
    print(f"    {line}")

# 8. What's the full narrative? Collect ALL unique text segments
print("\n\n6. UNIQUE NARRATIVE SEGMENTS")
print("-" * 60)

# Sort books by their position in the narrative
# Use overlap to find reading order
all_collapsed = [collapse(decode(b)) for b in books]

# Collect all unique decoded segments
unique_segments = set()
for text in all_collapsed:
    unique_segments.add(text)

print(f"  Total books: {len(all_collapsed)}")
print(f"  Unique texts: {len(unique_segments)}")

# Check for exact duplicates
dupes = defaultdict(list)
for bi, text in enumerate(all_collapsed):
    dupes[text].append(bi)

print(f"\n  Duplicate groups:")
for text, bis in sorted(dupes.items(), key=lambda x: len(x[1]), reverse=True):
    if len(bis) > 1:
        print(f"    Books {bis}: {text[:50]}...")

print("\n" + "=" * 80)
print("SESSION 11a COMPLETE")
print("=" * 80)
