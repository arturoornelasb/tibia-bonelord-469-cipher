#!/usr/bin/env python3
"""
Session 20 Part 3: Deep investigation of two breakthrough candidates.

1. TER as MHG article "of the" (+15 chars, 9x in STEINEN TER SCHARDT)
2. Code 96: L->I reassignment (+13 chars, 45 occurrences)
3. HEDDEMI mystery: what codes produce it? Why extra D?
4. Combined impact assessment
"""

import json, os
from collections import Counter, defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

DIGIT_SPLITS = {
    2: (45, '1'), 5: (265, '1'), 6: (12, '0'), 8: (137, '7'),
    10: (169, '0'), 11: (137, '0'), 12: (56, '1'), 13: (45, '0'),
    14: (98, '1'), 15: (98, '0'), 18: (4, '0'), 19: (52, '0'),
    20: (5, '1'), 22: (7, '1'), 23: (22, '4'), 24: (87, '8'),
    25: (0, '0'), 29: (53, '0'), 32: (137, '1'), 34: (101, '0'),
    36: (78, '0'), 39: (44, '0'), 42: (91, '2'), 43: (122, '0'),
    45: (15, '0'), 46: (0, '2'), 48: (126, '0'), 49: (97, '1'),
    50: (16, '6'), 52: (1, '0'), 53: (257, '1'), 54: (49, '1'),
    60: (73, '9'), 61: (93, '7'), 64: (60, '0'), 65: (114, '2'),
    68: (54, '0'),
}

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    return 0 if ic_from_counts(Counter(bp0), len(bp0)) > ic_from_counts(Counter(bp1), len(bp1)) else 1

book_pairs = []
decoded_books = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)
    decoded_books.append(''.join(v7.get(p, '?') for p in pairs))

all_text = ''.join(decoded_books)

ANAGRAM_MAP = {
    'LABGZERAS': 'SALZBERG', 'SCHWITEIONE': 'WEICHSTEIN',
    'SCHWITEIO': 'WEICHSTEIN', 'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'EDETOTNIURG': 'GOTTDIENER', 'EDETOTNIURGS': 'GOTTDIENERS',
    'ADTHARSC': 'SCHARDT', 'TAUTR': 'TRAUT', 'EILCH': 'LEICH',
    'HEDEMI': 'HEIME', 'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG', 'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE', 'TEIGN': 'NEIGT', 'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER', 'SODGE': 'GODES', 'SNDTEII': 'DIENST',
    'IEB': 'BEI', 'TNEDAS': 'STANDE', 'NSCHAT': 'NACHTS',
    'SANGE': 'SAGEN', 'GHNEE': 'GEHEN',
}

KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR', 'NU', 'STANDE', 'NACHTS', 'NIT', 'TOT',
    'ABER', 'ALLE', 'ALLES', 'ALTE', 'ALTEN', 'ALTER', 'AUCH', 'BAND',
    'BERG', 'BURG', 'DENN', 'DIES', 'DIESE', 'DIESER', 'DIESEN',
    'DIESEM', 'DOCH', 'DORT', 'DREI', 'DURCH', 'EINE', 'EINEM',
    'EINEN', 'EINER', 'EINES', 'ENDE', 'ERDE', 'ERST', 'ERSTE',
    'FACH', 'FAND', 'FERN', 'FEST', 'FORT', 'GAR', 'GANZ', 'GEGEN',
    'GEIST', 'GOTT', 'GOLD', 'GRAB', 'GROSS', 'GRUFT', 'GUT',
    'HAND', 'HEIM', 'HELD', 'HERR', 'HIER', 'HOCH', 'IMMER',
    'KANN', 'KLAR', 'KRAFT', 'LAND', 'LANG', 'LICHT', 'MACHT',
    'MEHR', 'MUSS', 'NACH', 'NACHT', 'NAHM', 'NAME', 'NEU', 'NEUE',
    'NEUEN', 'NICHT', 'NIE', 'NOCH', 'ODER', 'ORT', 'ORTEN',
    'REDE', 'REDEN', 'REICH', 'RIEF', 'RUIN', 'RUNE', 'RUNEN',
    'SAND', 'SAGT', 'SCHAUN', 'SCHON', 'SEHR', 'SEID', 'SEIN',
    'SEINE', 'SEINEN', 'SEINER', 'SEINEM', 'SEINES',
    'SICH', 'SIND', 'SOHN', 'SOLL', 'STEH', 'STEIN', 'STEINE',
    'STEINEN', 'STERN', 'TAG', 'TAGE', 'TAGEN', 'TAT', 'TEIL',
    'TIEF', 'TOD', 'TURM', 'UNTER', 'URALTE', 'VIEL', 'VIER',
    'WAHR', 'WALD', 'WAND', 'WARD', 'WEIL', 'WELT', 'WENN', 'WERT',
    'WESEN', 'WILL', 'WIND', 'WIRD', 'WORT', 'WORTE', 'ZEIT',
    'ZEHN', 'ZORN',
    'FINDEN', 'GEBEN', 'GEHEN', 'HABEN', 'KOMMEN', 'LEBEN', 'LESEN',
    'NEHMEN', 'SAGEN', 'SEHEN', 'STEHEN', 'SUCHEN', 'WISSEN',
    'WISSET', 'RUFEN', 'WIEDER',
    'OEL', 'SCE', 'MINNE', 'MIN', 'ODE', 'SER', 'GEN', 'INS',
    'GEIGET', 'BERUCHTIG', 'BERUCHTIGER',
    'MEERE', 'NEIGT', 'WISTEN', 'MANIER', 'HUND',
    'GODE', 'GODES', 'EIGENTUM', 'REDER',
    'THENAEUT', 'LABT', 'MORT', 'DIGE', 'WEGE', 'KOENIGS',
    'NAHE', 'NOT', 'NOTH', 'ZUR', 'OWI', 'ENGE', 'SEIDEN',
    'ALTES', 'NUT', 'NUTZ', 'HEIL', 'NEID', 'TREU', 'TREUE',
    'SUN', 'DIENST', 'SANG', 'DINC', 'HULDE', 'LANT', 'HERRE',
    'DIENEST', 'GEBOT', 'SCHWUR', 'ORDEN', 'RICHTER', 'DUNKEL',
    'EHRE', 'EDELE', 'SCHULD', 'SEGEN', 'FLUCH', 'RACHE',
    'KOENIG', 'DASS', 'EDEL', 'ADEL',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME', 'SCHARDT',
])

def dp_count(text, wordset):
    n = len(text)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            if text[start:i] in wordset:
                dp[i] = max(dp[i], dp[start] + wlen)
    return dp[n]

def apply_anagrams(text, amap):
    for anag in sorted(amap.keys(), key=len, reverse=True):
        text = text.replace(anag, amap[anag])
    return text

resolved = apply_anagrams(all_text, ANAGRAM_MAP)
total = sum(1 for c in resolved if c != '?')
baseline = dp_count(resolved, KNOWN)
print(f"Baseline: {baseline}/{total} = {baseline/total*100:.1f}%")

# ================================================================
# 1. HEDDEMI: trace the raw codes
# ================================================================
print(f"\n{'=' * 80}")
print("1. HEDDEMI RAW CODE ANALYSIS")
print("=" * 80)

# Find HEDDEMI in decoded text (before anagram replacement)
print(f"\n  Finding HEDDEMI in raw decoded text:")
heddemi_positions = []
for bidx, text in enumerate(decoded_books):
    pos = 0
    while True:
        idx = text.find('HEDDEMI', pos)
        if idx < 0:
            # Try HEDEMI too
            idx2 = text.find('HEDEMI', pos)
            if idx2 >= 0 and text[idx2:idx2+7] != 'HEDDEMI':
                pairs = book_pairs[bidx]
                if idx2 + 6 <= len(pairs):
                    codes = pairs[idx2:idx2+6]
                    ctx_s = max(0, idx2-5)
                    ctx_e = min(len(text), idx2+12)
                    print(f"  Book {bidx:2d} pos {idx2}: HEDEMI codes={' '.join(codes)} ctx=...{text[ctx_s:ctx_e]}...")
                pos = idx2 + 1
            else:
                break
        else:
            pairs = book_pairs[bidx]
            if idx + 7 <= len(pairs):
                codes = pairs[idx:idx+7]
                heddemi_positions.append((bidx, idx, codes))
                ctx_s = max(0, idx-5)
                ctx_e = min(len(text), idx+15)
                print(f"  Book {bidx:2d} pos {idx}: HEDDEMI codes={' '.join(codes)} ctx=...{text[ctx_s:ctx_e]}...")
            pos = idx + 1

# Analyze the codes
if heddemi_positions:
    print(f"\n  HEDDEMI code pattern analysis ({len(heddemi_positions)} occurrences):")
    code_patterns = Counter()
    for bidx, idx, codes in heddemi_positions:
        code_patterns[tuple(codes)] += 1
    for pattern, cnt in code_patterns.most_common():
        print(f"    {cnt}x: {' '.join(pattern)}")
        # What each code maps to
        for i, code in enumerate(pattern):
            letter = v7.get(code, '?')
            other_letters = set()
            # What other codes also map to this letter?
            same_letter_codes = [c for c, l in v7.items() if l == letter]
            print(f"      [{i}] code {code} -> {letter} (all {letter} codes: {same_letter_codes})")

    # KEY QUESTION: is the 4th code (D) correct?
    # If code at position 3 should be something else, what would HEDDEMI become?
    print(f"\n  Testing alternative for the D position (index 3):")
    sample = heddemi_positions[0]
    bidx, idx, codes = sample
    d_code = codes[3]
    print(f"  D code at position 3: {d_code}")
    print(f"  Currently maps to: {v7.get(d_code, '?')}")

    # What if this code mapped to E instead?
    for alt in 'ENISRATULCGMOBWFKZH':
        alt_word = 'HED' + alt + 'EMI'
        # Would removing one letter give us a known anagram?
        for skip_pos in range(7):
            reduced = alt_word[:skip_pos] + alt_word[skip_pos+1:]
            reduced_sorted = ''.join(sorted(reduced))
            # Check against HEIME sorted
            heime_sorted = ''.join(sorted('HEIME'))
            if reduced_sorted == heime_sorted:
                print(f"    D->{alt}: {alt_word}, skip pos {skip_pos} -> {''.join(sorted(reduced))} = HEIME anagram!")

# ================================================================
# 2. CODE 96 DEEP ANALYSIS: L vs I
# ================================================================
print(f"\n{'=' * 80}")
print("2. CODE 96: L vs I - DEEP ANALYSIS")
print("=" * 80)

# Show all contexts where code 96 appears
print(f"\n  Code 96 currently maps to: {v7.get('96', '?')}")
print(f"  All L codes: {sorted([c for c, l in v7.items() if l == 'L'])}")
print(f"  All I codes: {sorted([c for c, l in v7.items() if l == 'I'])}")

# Count total I vs L occurrences
i_total = sum(1 for pairs in book_pairs for p in pairs if v7.get(p) == 'I')
l_total = sum(1 for pairs in book_pairs for p in pairs if v7.get(p) == 'L')
all_pairs_total = sum(len(pairs) for pairs in book_pairs)

print(f"\n  Current frequencies:")
print(f"    I: {i_total} ({i_total/all_pairs_total*100:.2f}%) [German expected: 7.55%]")
print(f"    L: {l_total} ({l_total/all_pairs_total*100:.2f}%) [German expected: 3.44%]")

# If 96 moves from L to I:
new_i = i_total + 45
new_l = l_total - 45
print(f"\n  If code 96 becomes I:")
print(f"    I: {new_i} ({new_i/all_pairs_total*100:.2f}%) [expected: 7.55%]")
print(f"    L: {new_l} ({new_l/all_pairs_total*100:.2f}%) [expected: 3.44%]")

# Show how code 96 is used in KNOWN vs GARBLED words
print(f"\n  Code 96 in context (first 20 occurrences):")
count96 = 0
for bidx, pairs in enumerate(book_pairs):
    for pi, pair in enumerate(pairs):
        if pair == '96':
            text = decoded_books[bidx]
            ctx_s = max(0, pi-5)
            ctx_e = min(len(text), pi+6)
            ctx = text[ctx_s:ctx_e]
            rel = pi - ctx_s
            # Show what it would be with I instead
            alt_ctx = ctx[:rel] + 'I' + ctx[rel+1:]
            if count96 < 20:
                print(f"    Book {bidx:2d} pos {pi:3d}: L: ...{ctx}... | I: ...{alt_ctx}...")
            count96 += 1

# Does changing 96 to I break any existing anagram matches?
print(f"\n  Checking anagram compatibility with 96=I:")
alt_v7 = dict(v7)
alt_v7['96'] = 'I'
alt_decoded = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    alt_decoded.append(''.join(alt_v7.get(p, '?') for p in pairs))

alt_all = ''.join(alt_decoded)

# Check each anagram still works
for anag, target in sorted(ANAGRAM_MAP.items()):
    old_count = all_text.count(anag)
    new_count = alt_all.count(anag)
    if old_count != new_count:
        print(f"  CHANGED: {anag}->{target}: {old_count}x -> {new_count}x")

# Check specific important words: NLNDEF
print(f"\n  NLNDEF with 96=L: {all_text.count('NLNDEF')}x")
# What does NLNDEF become with 96=I?
nlndef_alt = alt_all.count('NINDEF')
nlndef_old = alt_all.count('NLNDEF')
print(f"  With 96=I: NLNDEF->{nlndef_old}x, NINDEF->{nlndef_alt}x")

# Actually find what NLNDEF codes are
print(f"\n  NLNDEF raw code trace:")
for bidx, text in enumerate(decoded_books):
    idx = text.find('NLNDEF')
    if idx >= 0:
        pairs = book_pairs[bidx]
        if idx + 6 <= len(pairs):
            codes = pairs[idx:idx+6]
            # Check which one is the L
            for ci, code in enumerate(codes):
                if v7.get(code) == 'L':
                    print(f"    Book {bidx}: NLNDEF codes={' '.join(codes)}, L at position {ci} (code {code})")

# ================================================================
# 3. TER VALIDATION
# ================================================================
print(f"\n{'=' * 80}")
print("3. TER VALIDATION")
print("=" * 80)

# Does TER appear only in STEINEN TER or in other contexts too?
ter_count = resolved.count('TER')
print(f"\n  TER in resolved text: {ter_count}x total")

# Find all TER with context
pos = 0
while True:
    idx = resolved.find('TER', pos)
    if idx < 0: break
    ctx_s = max(0, idx-10)
    ctx_e = min(len(resolved), idx+15)
    print(f"    pos {idx:4d}: ...{resolved[ctx_s:ctx_e]}...")
    pos = idx + 1

# In MHG, TER = "der/the/of the" (dialectal)
# Check: would adding TER conflict with existing words?
print(f"\n  Existing words containing TER:")
for w in sorted(KNOWN):
    if 'TER' in w:
        print(f"    {w}")

# Test: add TER and measure
test_known = set(KNOWN)
test_known.add('TER')
ter_cov = dp_count(resolved, test_known)
print(f"\n  +TER: {ter_cov}/{total} = {ter_cov/total*100:.1f}% ({ter_cov-baseline:+d})")

# Check it doesn't break longer words
print(f"\n  Verify TER doesn't break UNTER, RICHTER, etc.:")
# DP should prefer longer words over TER
for word in ['UNTER', 'RICHTER', 'ORTEN', 'STEINEN']:
    if 'TER' in word:
        print(f"    {word}: contains TER but is longer, DP should prefer it")

# ================================================================
# 4. COMBINED IMPACT: TER + code96=I
# ================================================================
print(f"\n{'=' * 80}")
print("4. COMBINED IMPACT")
print("=" * 80)

# Test TER alone
test1 = set(KNOWN)
test1.add('TER')
cov1 = dp_count(resolved, test1)
print(f"  +TER only: {cov1}/{total} = {cov1/total*100:.1f}% ({cov1-baseline:+d})")

# Test code96=I alone
alt_resolved = apply_anagrams(alt_all, ANAGRAM_MAP)
cov2 = dp_count(alt_resolved, KNOWN)
print(f"  code96=I only: {cov2}/{total} = {cov2/total*100:.1f}% ({cov2-baseline:+d})")

# Test code96=I + TER
test3 = set(KNOWN)
test3.add('TER')
cov3 = dp_count(alt_resolved, test3)
print(f"  TER + code96=I: {cov3}/{total} = {cov3/total*100:.1f}% ({cov3-baseline:+d})")

# Test with SIN, SET too
test4 = set(test3)
test4.add('SIN')  # MHG: his (possessive)
test4.add('SET')  # SET?
cov4 = dp_count(alt_resolved, test4)
print(f"  +TER+SIN+SET+96=I: {cov4}/{total} = {cov4/total*100:.1f}% ({cov4-baseline:+d})")

# ================================================================
# 5. WHAT DOES THE TEXT LOOK LIKE WITH CODE 96=I?
# ================================================================
print(f"\n{'=' * 80}")
print("5. TEXT COMPARISON: 96=L vs 96=I (first 500 chars)")
print("=" * 80)

print(f"\n  96=L (current):")
print(f"    {resolved[:300]}...")
print(f"\n  96=I:")
print(f"    {alt_resolved[:300]}...")

# Show the differences
print(f"\n  Positions where 96=I differs:")
diff_count = 0
for i in range(min(len(resolved), len(alt_resolved))):
    if resolved[i] != alt_resolved[i]:
        diff_count += 1
        if diff_count <= 20:
            ctx_old = resolved[max(0,i-5):i+6]
            ctx_new = alt_resolved[max(0,i-5):i+6]
            print(f"    pos {i:4d}: L: ...{ctx_old}... -> I: ...{ctx_new}...")
print(f"  Total different positions: {diff_count}")

# ================================================================
# 6. FULL CODE FREQUENCY AUDIT
# ================================================================
print(f"\n{'=' * 80}")
print("6. FREQUENCY AUDIT: actual vs expected for each letter")
print("=" * 80)

GERMAN_FREQ = {
    'E': 17.40, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
    'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
    'L': 3.44, 'C': 3.06, 'G': 3.01, 'M': 2.53, 'O': 2.51,
    'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
}

letter_counts = Counter()
for pairs in book_pairs:
    for p in pairs:
        letter = v7.get(p, '?')
        if letter != '?':
            letter_counts[letter] += 1

total_mapped = sum(letter_counts.values())
print(f"\n  {'Letter':>6} {'Codes':>5} {'Count':>6} {'Actual%':>8} {'Expected%':>10} {'Diff':>7}")
print(f"  {'-'*50}")
for letter in sorted(GERMAN_FREQ.keys(), key=lambda x: -GERMAN_FREQ[x]):
    codes = sorted([c for c, l in v7.items() if l == letter])
    count = letter_counts.get(letter, 0)
    actual = count / total_mapped * 100
    expected = GERMAN_FREQ[letter]
    diff = actual - expected
    marker = ' **' if abs(diff) > 2 else ''
    print(f"  {letter:>6} {len(codes):>5} {count:>6} {actual:>7.2f}% {expected:>9.2f}% {diff:>+6.2f}{marker}")

# Now with 96=I
print(f"\n  With code 96 = I:")
alt_counts = Counter()
for pairs in book_pairs:
    for p in pairs:
        letter = alt_v7.get(p, '?')
        if letter != '?':
            alt_counts[letter] += 1

for letter in ['I', 'L']:
    codes = sorted([c for c, l in alt_v7.items() if l == letter])
    count = alt_counts.get(letter, 0)
    actual = count / total_mapped * 100
    expected = GERMAN_FREQ[letter]
    diff = actual - expected
    print(f"    {letter}: {len(codes)} codes, {count} ({actual:.2f}%) vs expected {expected:.2f}% ({diff:+.2f})")

print(f"\n  Done.")
