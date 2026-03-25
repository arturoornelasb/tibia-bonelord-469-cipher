#!/usr/bin/env python3
"""Session 10r: D->B hypothesis + systematic code reassignment search"""

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

all_codes = Counter()
for book in books:
    for c in book:
        all_codes[c] += 1

rev_map = defaultdict(list)
for code, letter in mapping.items():
    rev_map[letter].append(code)

print("=" * 80)
print("SESSION 10r: D->B HYPOTHESIS + SYSTEMATIC REASSIGNMENT")
print("=" * 80)

# 1. D code analysis - which could be B?
print("\n1. D CODES ANALYSIS")
print("-" * 60)

d_codes = rev_map['D']
print(f"  D codes: {d_codes}")
print(f"  D frequencies:")
for c in d_codes:
    freq = all_codes.get(c, 0)
    print(f"    code {c}: {freq} occurrences")

# Which D codes are confirmed?
# Code 45 confirmed in DIESER (45-21-76-52-19-72)
# Code 42 confirmed in ADTHARSC (31-42-78-94-31-51-91-18) - the D in ADT
# Code 28 in DNRHAUNRNVMHISDIZA (first letter, but this is a proper noun)
# Need to check others

print("\n  D code confirmation status:")
confirmed_d = set()
# Check which D codes appear in known words
known_with_d = [
    ('DIESER', 'D-I-E-S-E-R'),
    ('ADTHARSC', 'A-D-T-H-A-R-S-C'),
    ('ADTHAUMR', 'A-D-T-H-A-U-M-R'),
    ('DENEN', 'D-E-N-E-N'),
    ('DORT', 'D-O-R-T'),
    ('DENN', 'D-E-N-N'),
    ('DER', 'D-E-R'),
    ('DEN', 'D-E-N'),
    ('DIE', 'D-I-E'),
    ('DAS', 'D-A-S'),
    ('HUND', 'H-U-N-D'),
    ('HWND', 'H-W-N-D'),
    ('GOLD', 'G-O-L-D'),
    ('MOND', 'M-O-N-D'),
    ('WIRD', 'W-I-R-D'),
    ('LIED', 'L-I-E-D'),
    ('REDE', 'R-E-D-E'),
    ('ERDE', 'E-R-D-E'),
    ('SEIDE', 'S-E-I-D-E'),
    ('NORDEN', 'N-O-R-D-E-N'),
    ('FINDEN', 'F-I-N-D-E-N'),
    ('ENDE', 'E-N-D-E'),
    ('RUND', 'R-U-N-D'),
    ('UNTER', 'U-N-T-E-R'),
]

for word, pattern in known_with_d:
    if 'D' not in word:
        continue
    for bi, book in enumerate(books):
        col = collapse(decode(book))
        if word in col:
            decoded = decode(book)
            for ri in range(len(decoded)):
                raw = decoded[ri:ri+len(word)*2]
                if collapse(raw).startswith(word):
                    codes = book[ri:ri+len(word)]
                    for j, ch in enumerate(word):
                        if ch == 'D' and j < len(codes):
                            confirmed_d.add(codes[j])
                    break
            break

for c in d_codes:
    status = "CONFIRMED" if c in confirmed_d else "unconfirmed"
    print(f"    code {c}: {status}")

# 2. Test each unconfirmed D code as B
print("\n" + "=" * 60)
print("2. TEST UNCONFIRMED D CODES AS B")
print("=" * 60)

unconfirmed_d = [c for c in d_codes if c not in confirmed_d]
print(f"  Unconfirmed D codes: {unconfirmed_d}")

for test_code in unconfirmed_d:
    freq = all_codes.get(test_code, 0)
    print(f"\n  --- Testing code {test_code} ({freq}x) as B ---")

    mod = dict(mapping)
    mod[test_code] = 'B'

    # Show contexts
    contexts = []
    for bi, book in enumerate(books):
        for ci, c in enumerate(book):
            if c == test_code:
                start = max(0, ci-3)
                end = min(len(book), ci+4)
                raw_d = ''.join(mapping.get(x, '?') for x in book[start:end])
                raw_b = ''.join(mod.get(x, '?') for x in book[start:end])
                col_d = collapse(raw_d)
                col_b = collapse(raw_b)
                contexts.append((bi, col_d, col_b))
                if len(contexts) >= 8:
                    break
        if len(contexts) >= 8:
            break

    seen = set()
    good_count = 0
    bad_count = 0
    for bi, cd, cb in contexts:
        key = (cd, cb)
        if key not in seen:
            seen.add(key)
            # Check if B makes good German words
            b_good = ""
            for w in ['BER', 'AUB', 'ABE', 'ABER', 'BIS', 'BUCH',
                       'BERG', 'BURG', 'BALD', 'BRIEF', 'BRUDER',
                       'BEI', 'BEIDE', 'BETEN', 'GEBEN', 'LEBEN',
                       'LIEB', 'LEIB', 'GRAB', 'HERB', 'HALB']:
                if w in cb:
                    b_good = f" -> {w}"
                    good_count += 1
            d_good = ""
            for w in ['DER', 'DEN', 'DIE', 'DAS', 'UND', 'WIRD',
                       'ERDE', 'DORT', 'DENN', 'FINDEN', 'HUND',
                       'GOLD', 'MOND', 'LIED', 'REDE', 'ENDE',
                       'RUND', 'NORDEN', 'SEIDE']:
                if w in cd:
                    d_good = f" (breaks {w})"
                    bad_count += 1
            print(f"    {cd:15s} -> {cb:15s}{b_good}{d_good}")

    if bad_count == 0 and good_count > 0:
        print(f"  *** CODE {test_code} = B LOOKS PROMISING! ***")

# 3. All confirmed vs unconfirmed codes summary
print("\n" + "=" * 60)
print("3. CONFIRMED VS UNCONFIRMED CODES SUMMARY")
print("=" * 60)

# Build confirmed set from all known words
confirmed_codes = {}  # code -> (letter, word)
all_known = [
    'DIESER', 'FINDEN', 'SCHAUN', 'URALTE', 'KOENIG', 'GEIGET',
    'STEIN', 'RUNE', 'ERDE', 'SEGEN', 'SEIN', 'DAS', 'DIE',
    'DER', 'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON', 'MIT',
    'AUS', 'ORT', 'TUN', 'NUR', 'SUN', 'TOT', 'GAR', 'ACH',
    'ZUM', 'HIN', 'HER', 'ALS', 'AUCH', 'TAG', 'WEG', 'DENN',
    'ERST', 'KLAR', 'WIRD', 'STEH', 'DORT', 'GOLD', 'MOND',
    'WELT', 'ENDE', 'REDE', 'HUND', 'HWND', 'LIED', 'NORDEN',
    'SONNE', 'UNTER', 'NICHT', 'WERDE', 'DENEN', 'VIEL', 'RUND',
    'SEIDE', 'EINEN', 'EINER', 'SEINE', 'WIE', 'SEI', 'DEN',
    'GEH', 'WISET',
]

for word in all_known:
    for bi, book in enumerate(books):
        col = collapse(decode(book))
        if word in col:
            decoded = decode(book)
            for ri in range(len(decoded)):
                raw = decoded[ri:ri+len(word)*3]
                if collapse(raw).startswith(word):
                    # Map collapsed positions to raw positions
                    col_pos = 0
                    raw_idx = 0
                    word_codes = []
                    for ri2 in range(ri, min(ri + len(word)*2, len(book))):
                        letter = mapping.get(book[ri2], '?')
                        # Is this a new collapsed character?
                        if ri2 == ri or decoded[ri2] != decoded[ri2-1]:
                            if col_pos < len(word):
                                if letter == word[col_pos]:
                                    confirmed_codes[book[ri2]] = (letter, word)
                                col_pos += 1
                        if col_pos >= len(word):
                            break
                    break
            break

print(f"  Total confirmed codes: {len(confirmed_codes)}")
print(f"  Total mapped codes: {len(mapping)}")
print(f"  Unconfirmed: {len(mapping) - len(confirmed_codes)}")

# Show unconfirmed codes by letter
print("\n  Unconfirmed codes by letter:")
for letter in sorted(rev_map.keys()):
    codes = rev_map[letter]
    unconf = [c for c in codes if c not in confirmed_codes]
    if unconf:
        total_freq = sum(all_codes.get(c, 0) for c in unconf)
        print(f"    {letter}: {unconf} ({total_freq} total occurrences)")

# 4. Test all viable code reassignments
print("\n" + "=" * 60)
print("4. SYSTEMATIC REASSIGNMENT SEARCH")
print("=" * 60)

# For each unconfirmed code, test if changing its letter improves coverage
NEG_INF = float('-inf')

word_scores = {}
definite = [
    'EILCHANHEARUCHTIG', 'EDETOTNIURGS', 'WRLGTNELNRHELUIRUNN',
    'TIUMENGEMI', 'SCHWITEIONE', 'LABGZERAS', 'HEDEMI', 'TAUTR',
    'LABRNI', 'ADTHARSC', 'ENGCHD', 'KELSEI',
    'KOENIG', 'GEIGET', 'SCHAUN', 'URALTE', 'FINDEN', 'DIESER',
    'NORDEN', 'SONNE', 'UNTER', 'NICHT', 'WERDE',
    'STEIN', 'DENEN', 'ERDE', 'VIEL', 'RUNE',
    'STEH', 'LIED', 'SEGEN', 'DORT', 'DENN',
    'GOLD', 'MOND', 'WELT', 'ENDE', 'REDE',
    'HUND', 'SEIN', 'WIRD', 'KLAR', 'ERST',
    'HWND', 'VMTEGE', 'STEIEN', 'WISET', 'OWI',
    'EINEN', 'EINER', 'SEINE', 'SEIDE',
    'TAG', 'WEG', 'DER', 'DEN', 'DIE', 'DAS',
    'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON',
    'MIT', 'WIE', 'SEI', 'AUS', 'ORT', 'TUN',
    'NUR', 'SUN', 'TOT', 'GAR', 'ACH', 'ZUM',
    'HIN', 'HER', 'ALS', 'AUCH', 'RUND', 'GEH',
    'ER', 'ES', 'IN', 'SO',
]

for w in definite:
    word_scores[w] = len(w) * 3
all_words = sorted(word_scores.keys(), key=len, reverse=True)

def dp_segment(text, words, scores):
    n = len(text)
    dp = [NEG_INF] * (n + 1)
    back = [None] * (n + 1)
    dp[0] = 0
    for i in range(n):
        if dp[i] == NEG_INF: continue
        ns = dp[i] - 1
        if ns > dp[i+1]:
            dp[i+1] = ns
            back[i+1] = ('unk', i)
        for word in words:
            wl = len(word)
            if i + wl <= n and text[i:i+wl] == word:
                ns = dp[i] + scores.get(word, wl)
                if ns > dp[i+wl]:
                    dp[i+wl] = ns
                    back[i+wl] = ('word', i, word)
    return dp[n]

def coverage(m):
    total = 0
    covered = 0
    for bi, book in enumerate(books):
        col = collapse(decode(book, m))
        total += len(col)
        result = dp_segment(col, all_words, word_scores)
        # Need to run full backtrack for coverage
        n = len(col)
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
                if i + wl <= n and col[i:i+wl] == word:
                    ns = dp[i] + word_scores.get(word, wl)
                    if ns > dp[i+wl]:
                        dp[i+wl] = ns
                        back[i+wl] = ('word', i, word)
        # Backtrack to count word chars
        pos = n
        wc = 0
        while pos > 0:
            info = back[pos]
            if info is None:
                pos -= 1
            elif info[0] == 'unk':
                pos = info[1]
            elif info[0] == 'word':
                wc += len(info[2])
                pos = info[1]
        covered += wc
    return covered * 100 / total if total > 0 else 0

# Baseline coverage
base_cov = coverage(mapping)
print(f"  Baseline coverage: {base_cov:.1f}%")

# Test reassigning each unconfirmed code
print("\n  Testing all unconfirmed code reassignments:")
improvements = []
unconfirmed = [c for c in mapping if c not in confirmed_codes]

# Only test high-frequency unconfirmed codes with plausible target letters
for code in sorted(unconfirmed, key=lambda c: -all_codes.get(c, 0))[:15]:
    current_letter = mapping[code]
    freq = all_codes.get(code, 0)
    if freq < 10:
        continue

    # Test plausible alternative letters
    # Skip letters the code is already assigned to
    for target in 'ABCDEFGHIKLMNORSTUV':
        if target == current_letter:
            continue
        mod = dict(mapping)
        mod[code] = target
        new_cov = coverage(mod)
        if new_cov > base_cov + 0.3:
            improvements.append((code, current_letter, target, freq, new_cov))
            print(f"    code {code} ({current_letter}->{target}, {freq}x): "
                  f"coverage {base_cov:.1f}% -> {new_cov:.1f}% (+{new_cov-base_cov:.1f}%)")

if not improvements:
    print("  No significant improvements found via single-code reassignment.")
else:
    print(f"\n  Found {len(improvements)} improvements!")
    best = max(improvements, key=lambda x: x[4])
    print(f"  Best: code {best[0]} ({best[1]}->{best[2]}): +{best[4]-base_cov:.1f}%")

# 5. Top unknown words - can they be German with letter swaps?
print("\n" + "=" * 60)
print("5. UNKNOWN WORDS - POSSIBLE GERMAN READINGS")
print("=" * 60)

# EILCHANHEARUCHTIG - compound adjective ending in -IG
print("\n  EILCHANHEARUCHTIG:")
print("    Split: EIL-CH-AN-HE-A-RUCH-T-IG")
print("    -RUCHTIG could be from BERUCHTIG(T) = famous")
print("    Or: EIL = haste + CHANHE = ? + ARUCHTIG = ?")
print("    Try: ELICH (=ehelich, legitimate) + AN + HEA + RUCHTIG?")
print("    Try: EI + LCHANHE + ARUCHTIG?")
# Get raw codes
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'EILCHANHEARUCHTIG' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if 'EILCHAN' in collapse(decoded[ri:ri+20]):
                codes = book[ri:ri+17]
                raw = decoded[ri:ri+20]
                print(f"    B{bi:02d} raw: {raw[:20]}")
                print(f"    codes: {' '.join(codes[:17])}")
                break
        break

# EDETOTNIURGS - contains TOT (dead)
print("\n  EDETOTNIURGS:")
print("    Contains TOT = dead")
print("    Possible: EDE + TOT + NIURGS")
print("    EDE could be: eid (oath) in OHG")
print("    NIURGS = ? (could contain a name)")
# Get raw codes
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'EDETOTNIURGS' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if 'EDETOT' in collapse(decoded[ri:ri+16]):
                codes = book[ri:ri+12]
                raw = decoded[ri:ri+14]
                print(f"    B{bi:02d} raw: {raw}")
                print(f"    codes: {' '.join(codes)}")
                break
        break

# TIUMENGEMI
print("\n  TIUMENGEMI:")
print("    Context: always before ORT ENGCHD")
print("    GEMEIND(E) = community? UMENGEMIN = ?")
print("    TI + UMEN + GEMI? Or TIUM + EN + GEMI?")
print("    Reversed: IMEGNEMUIT")
print("    Could be cipher for GEMEINDE (community)?")

# SCHWITEIONE
print("\n  SCHWITEIONE:")
print("    SCH is German digraph")
print("    SCHWIT + EIONE? Or SCHWI + TEIONE?")
print("    SCHWEI(GEN) = to be silent?")
print("    SCHWI could be from SCHWI(NDEN) = disappear")
print("    TEION(E) = ?")

print("\n" + "=" * 80)
print("SESSION 10r COMPLETE")
print("=" * 80)
