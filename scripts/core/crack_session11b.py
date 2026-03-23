#!/usr/bin/env python3
"""Session 11b: Wrong code detection via impossible consonant clusters"""

import json, re
from collections import Counter, defaultdict
from itertools import product

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

# Known confirmed codes (from session 10r analysis)
# Unconfirmed: A(66), B(62), D(02,63), E(09,37,39,69,86), H(94), I(15),
#              L(96), M(04,40), N(13,71), O(79), R(10), S(05), W(33)
unconfirmed = {
    '66': 'A', '62': 'B', '02': 'D', '63': 'D',
    '09': 'E', '37': 'E', '39': 'E', '69': 'E', '86': 'E',
    '94': 'H', '15': 'I', '96': 'L', '04': 'M', '40': 'M',
    '13': 'N', '71': 'N', '79': 'O', '10': 'R', '05': 'S', '33': 'W'
}
all_codes_freq = Counter()
for book in books:
    for c in book:
        all_codes_freq[c] += 1

print("=" * 80)
print("SESSION 11b: WRONG CODE DETECTION VIA CONSONANT ANALYSIS")
print("=" * 80)

# 1. Find the raw codes in impossible regions
print("\n1. RAW CODES IN IMPOSSIBLE REGIONS")
print("-" * 60)

all_collapsed = [collapse(decode(b)) for b in books]

# Target regions and their contexts
targets = [
    ('LRSZTHK', 'IST', 'WIR'),
    ('VMTEGE', 'IST', 'VIEL'),
    ('URIHWNRS', 'WIR', 'IST'),
    ('GELNMH', 'IR', 'SO'),
    ('WRLGTNELNRHELU', 'STEH', 'IR'),
    ('DNRHAUNRNVMHISDIZA', 'DEN', 'RUNE'),
    ('AMNEUD', 'TER', 'ES'),
    ('NTENTUIGA', 'ENDE', 'ER'),
]

for region, before, after in targets:
    print(f"\n  [{region}] (between {before}...{after}):")
    # Find the raw codes
    search = before + region
    found = False
    for bi, book in enumerate(books):
        col = collapse(decode(book))
        if search in col:
            idx = col.index(search)
            # Map collapsed position to raw code position
            decoded_raw = decode(book)
            for ri in range(len(decoded_raw)):
                sub = decoded_raw[ri:ri+50]
                col_sub = collapse(sub)
                if col_sub.startswith(search):
                    # Find where the region starts in raw codes
                    # Skip past 'before' text
                    col_pos = 0
                    region_start = None
                    for k in range(ri, min(ri+50, len(book))):
                        if k == ri or decoded_raw[k] != decoded_raw[k-1]:
                            if col_pos == len(before):
                                region_start = k
                                break
                            col_pos += 1

                    if region_start is not None:
                        # Get codes for the region
                        region_len = len(region)
                        col_count = 0
                        region_codes = []
                        for k in range(region_start, min(region_start + region_len * 2, len(book))):
                            if k == region_start or decoded_raw[k] != decoded_raw[k-1]:
                                if col_count >= region_len:
                                    break
                                code = book[k]
                                letter = mapping.get(code, '?')
                                is_unc = '*' if code in unconfirmed else ' '
                                region_codes.append((code, letter, is_unc))
                                col_count += 1

                        print(f"    B{bi:02d} raw codes:")
                        for code, letter, unc in region_codes:
                            freq = all_codes_freq.get(code, 0)
                            print(f"      {code}={letter}{unc} (freq={freq})")
                        found = True
                        break
            if found:
                break

    if not found:
        print(f"    NOT FOUND in corpus")

    # Vowel/consonant analysis
    vowels = sum(1 for c in region if c in 'AEIOU')
    consonants = len(region) - vowels
    ratio = vowels / len(region) if len(region) > 0 else 0
    print(f"    V/C ratio: {vowels}V/{consonants}C = {ratio:.2f} (German avg ~0.40)")

# 2. Systematic: for each unconfirmed code, test ALL possible letters
print("\n\n2. SYSTEMATIC CODE REASSIGNMENT TEST")
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
]
german_words = list(dict.fromkeys(german_words))
word_scores = {w: len(w) * 3 for w in german_words}
all_words = sorted(word_scores.keys(), key=len, reverse=True)

def dp_coverage(m):
    """Total DP coverage percentage with given mapping"""
    tc = 0
    tt = 0
    for book in books:
        col = collapse(decode(book, m))
        n = len(col)
        if n == 0: continue
        dp = [NEG_INF] * (n + 1)
        dp[0] = 0
        for i in range(n):
            if dp[i] == NEG_INF: continue
            ns = dp[i] - 1
            if ns > dp[i+1]:
                dp[i+1] = ns
            for word in all_words:
                wl = len(word)
                if i + wl <= n and col[i:i+wl] == word:
                    ns = dp[i] + word_scores.get(word, wl)
                    if ns > dp[i+wl]:
                        dp[i+wl] = ns
        pos = n
        wc = 0
        back_dp = [None] * (n + 1)
        # Recompute with backtracking
        dp2 = [NEG_INF] * (n + 1)
        dp2[0] = 0
        for i in range(n):
            if dp2[i] == NEG_INF: continue
            ns = dp2[i] - 1
            if ns > dp2[i+1]:
                dp2[i+1] = ns
                back_dp[i+1] = ('u', i)
            for word in all_words:
                wl = len(word)
                if i + wl <= n and col[i:i+wl] == word:
                    ns = dp2[i] + word_scores.get(word, wl)
                    if ns > dp2[i+wl]:
                        dp2[i+wl] = ns
                        back_dp[i+wl] = ('w', i, wl)
        pos = n
        while pos > 0:
            info = back_dp[pos]
            if info is None: pos -= 1
            elif info[0] == 'u': pos = info[1]
            elif info[0] == 'w':
                wc += info[2]
                pos = info[1]
        tc += wc
        tt += n
    return tc * 100 / tt if tt > 0 else 0

# Baseline
base_cov = dp_coverage(mapping)
print(f"  Baseline coverage: {base_cov:.1f}%")

# Test each unconfirmed code with all 22 possible letters
letters = sorted(set(mapping.values()))
print(f"  Testing {len(unconfirmed)} unconfirmed codes x {len(letters)} letters...")

improvements = []
for code, current_letter in sorted(unconfirmed.items(), key=lambda x: all_codes_freq.get(x[0], 0), reverse=True):
    freq = all_codes_freq.get(code, 0)
    best_letter = current_letter
    best_cov = base_cov
    for letter in letters:
        if letter == current_letter:
            continue
        mod = dict(mapping)
        mod[code] = letter
        cov = dp_coverage(mod)
        if cov > best_cov:
            best_cov = cov
            best_letter = letter
    if best_letter != current_letter:
        delta = best_cov - base_cov
        improvements.append((code, current_letter, best_letter, delta, freq))
        print(f"  ** Code {code}: {current_letter}->{best_letter} = +{delta:.1f}% (freq={freq})")
    else:
        print(f"     Code {code}: {current_letter} is optimal (freq={freq})")

# 3. Check if any improvements don't break confirmed words
print("\n\n3. IMPROVEMENT VALIDATION")
print("-" * 60)

if improvements:
    improvements.sort(key=lambda x: x[3], reverse=True)
    print(f"  Top improvements:")
    for code, old, new, delta, freq in improvements:
        print(f"    Code {code}: {old}->{new} = +{delta:.1f}% (freq={freq})")

        # Check what words this BREAKS
        mod = dict(mapping)
        mod[code] = new
        broken = []
        confirmed_words = [
            'DAS', 'DER', 'DEN', 'DIE', 'UND', 'IST', 'EIN', 'SIE', 'WIR',
            'HIER', 'TAUTR', 'SEIN', 'DIESER', 'EINER', 'ERDE', 'VIEL',
            'URALTE', 'STEINEN', 'SCHAUN', 'KOENIG', 'WISET', 'RUNE',
            'HUND', 'HWND', 'STEH', 'GEH', 'FINDEN', 'TAG', 'WEG',
            'SEI', 'WIE', 'TUN', 'AUS', 'ORT', 'MIT', 'VON', 'ACH',
            'DENEN', 'SEGEN', 'DORT', 'DENN', 'GOLD', 'MOND', 'WELT',
            'ENDE', 'REDE', 'WIRD', 'KLAR', 'ERST', 'AUCH', 'UNTER',
            'NICHT', 'SUN', 'NUR', 'HIN', 'HER', 'ALS', 'NACH',
            'NOCH', 'ALLE', 'WOHL', 'SICH', 'SIND', 'SEHR', 'OWI',
            'MINHE', 'HEDEMI', 'ADTHARSC', 'LABRNI',
        ]
        for bi, book in enumerate(books):
            col_old = collapse(decode(book))
            col_new = collapse(decode(book, mod))
            for word in confirmed_words:
                if word in col_old and word not in col_new:
                    broken.append(word)
        broken = list(set(broken))
        if broken:
            print(f"      BREAKS: {broken}")
        else:
            print(f"      No confirmed words broken!")

        # Show sample text change
        for bi in range(len(books)):
            col_old = collapse(decode(books[bi]))
            col_new = collapse(decode(books[bi], mod))
            if col_old != col_new:
                # Find first difference
                for pos in range(min(len(col_old), len(col_new))):
                    if pos < len(col_old) and pos < len(col_new) and col_old[pos] != col_new[pos]:
                        start = max(0, pos-10)
                        end = min(len(col_old), pos+10)
                        print(f"      B{bi:02d} old: ...{col_old[start:end]}...")
                        end = min(len(col_new), pos+10)
                        print(f"      B{bi:02d} new: ...{col_new[start:end]}...")
                        break
                break
else:
    print("  No improvements found")

# 4. What if we apply ALL non-breaking improvements?
print("\n\n4. COMBINED NON-BREAKING IMPROVEMENTS")
print("-" * 60)

confirmed_words = [
    'DAS', 'DER', 'DEN', 'DIE', 'UND', 'IST', 'EIN', 'SIE', 'WIR',
    'HIER', 'TAUTR', 'SEIN', 'DIESER', 'EINER', 'ERDE', 'VIEL',
    'URALTE', 'STEINEN', 'SCHAUN', 'KOENIG', 'WISET', 'RUNE',
    'HUND', 'HWND', 'STEH', 'GEH', 'FINDEN', 'TAG', 'WEG',
    'SEI', 'WIE', 'TUN', 'AUS', 'ORT', 'MIT', 'VON', 'ACH',
    'DENEN', 'SEGEN', 'DORT', 'DENN', 'GOLD', 'MOND', 'WELT',
    'ENDE', 'REDE', 'WIRD', 'KLAR', 'ERST', 'AUCH', 'UNTER',
    'NICHT', 'SUN', 'NUR', 'HIN', 'HER', 'ALS', 'NACH',
    'NOCH', 'ALLE', 'WOHL', 'SICH', 'SIND', 'SEHR', 'OWI',
    'MINHE', 'HEDEMI', 'ADTHARSC', 'LABRNI', 'GEIGET', 'KLAR',
    'SONNE', 'NORDEN', 'WERDE', 'SEIDE', 'SEINE',
]

combined = dict(mapping)
applied = []
for code, old, new, delta, freq in improvements:
    test = dict(combined)
    test[code] = new
    broken = []
    for bi, book in enumerate(books):
        col_old = collapse(decode(book, combined))
        col_new = collapse(decode(book, test))
        for word in confirmed_words:
            if word in col_old and word not in col_new:
                broken.append(word)
    broken = list(set(broken))
    if not broken:
        combined[code] = new
        applied.append((code, old, new, delta))

if applied:
    combined_cov = dp_coverage(combined)
    print(f"  Applied {len(applied)} changes:")
    for code, old, new, delta in applied:
        print(f"    Code {code}: {old}->{new}")
    print(f"  Combined coverage: {combined_cov:.1f}% (baseline: {base_cov:.1f}%)")
    print(f"  Total improvement: {combined_cov - base_cov:+.1f}%")

    # Show best book with combined changes
    print(f"\n  B05 with combined changes:")
    col_old = collapse(decode(books[5]))
    col_new = collapse(decode(books[5], combined))
    print(f"    Old: {col_old}")
    print(f"    New: {col_new}")
else:
    print("  No non-breaking improvements applicable")

# 5. Focus: what letters are missing from the text?
print("\n\n5. LETTER FREQUENCY ANALYSIS")
print("-" * 60)

# Get letter frequencies from collapsed text
all_text = ''.join(collapse(decode(b)) for b in books)
letter_freq = Counter(all_text)
total = len(all_text)

# Expected German frequencies
german_freq = {
    'E': 17.4, 'N': 9.8, 'I': 7.6, 'S': 7.3, 'R': 7.0,
    'A': 6.5, 'T': 6.2, 'D': 5.1, 'H': 4.8, 'U': 4.3,
    'L': 3.4, 'G': 3.0, 'C': 3.1, 'O': 2.5, 'M': 2.5,
    'W': 1.9, 'B': 1.9, 'F': 1.7, 'K': 1.2, 'Z': 1.1,
    'V': 0.8, 'P': 0.8,
}

print(f"  {'Letter':>6} {'Actual%':>8} {'Expected%':>10} {'Delta':>8} {'Status':>12}")
print(f"  {'-'*6} {'-'*8} {'-'*10} {'-'*8} {'-'*12}")

overrep = []
underrep = []
for letter in sorted(german_freq.keys(), key=lambda l: german_freq[l], reverse=True):
    actual = letter_freq.get(letter, 0) * 100 / total
    expected = german_freq[letter]
    delta = actual - expected
    status = ''
    if delta > 2.0: status = 'OVER +++'
    elif delta > 1.0: status = 'OVER +'
    elif delta < -1.5: status = 'UNDER ---'
    elif delta < -0.8: status = 'UNDER -'
    if delta > 1.5: overrep.append(letter)
    if delta < -1.0: underrep.append(letter)
    print(f"  {letter:>6} {actual:>7.1f}% {expected:>9.1f}% {delta:>+7.1f}% {status:>12}")

# Missing P
print(f"\n  P: 0.0% actual vs 0.8% expected - MISSING")

if overrep:
    print(f"\n  Over-represented: {overrep}")
    print(f"  These letters may have codes that should map elsewhere")
if underrep:
    print(f"  Under-represented: {underrep}")
    print(f"  These letters may need codes reassigned to them")

# 6. Specific hypothesis: move codes from over-rep to under-rep
print("\n\n6. TARGETED REASSIGNMENT HYPOTHESES")
print("-" * 60)

# For each overrep letter, check which codes are unconfirmed
for letter in overrep:
    codes = rev_map[letter]
    unc_codes = [c for c in codes if c in unconfirmed]
    conf_codes = [c for c in codes if c not in unconfirmed]
    if unc_codes:
        print(f"\n  {letter} (over): codes={codes}")
        print(f"    Unconfirmed: {unc_codes} (could be reassigned)")
        print(f"    Confirmed: {conf_codes}")

        # For each unconfirmed code, which under-rep letters benefit?
        for uc in unc_codes:
            freq = all_codes_freq.get(uc, 0)
            print(f"\n    Testing code {uc} ({letter}, freq={freq}):")
            for target in underrep:
                mod = dict(mapping)
                mod[uc] = target
                cov = dp_coverage(mod)
                delta = cov - base_cov
                if delta != 0:
                    # Check breaks
                    broken = []
                    for bi, book in enumerate(books):
                        col_old = collapse(decode(book))
                        col_new = collapse(decode(book, mod))
                        for word in confirmed_words:
                            if word in col_old and word not in col_new:
                                broken.append(word)
                    broken = list(set(broken))
                    break_str = f" BREAKS:{broken}" if broken else " (safe)"
                    if delta > 0:
                        print(f"      {letter}->{target}: {delta:+.1f}%{break_str}")

print("\n" + "=" * 80)
print("SESSION 11b COMPLETE")
print("=" * 80)
