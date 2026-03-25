#!/usr/bin/env python3
"""Session 10s: Deep code 86 E→N test + compound word attacks + combinatorial search"""

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

NEG_INF = float('-inf')

# Extended word list (from 10m_fix + expansions)
german_words = [
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
    'NACH', 'IENE', 'NOCH', 'ALLE',
    'RITTER', 'MEISTER', 'GEIST', 'KRAFT', 'RECHT',
    'NACHT', 'MACHT', 'LEBEN', 'GEBEN', 'LIEBE',
    'FEUER', 'WASSER', 'LICHT', 'DUNKEL', 'GROSS',
    'KLEIN', 'OBER', 'TIEF', 'WEISE', 'KLUG',
    'ER', 'ES', 'IN', 'SO', 'AN', 'IM',
    'ABER', 'ODER', 'WENN', 'DANN', 'WEIL',
    'HIER', 'SICH', 'SIND', 'SEHR', 'WOHL',
    'VERS', 'BURG', 'BERG', 'WALD', 'FELD',
    'EDEL', 'HELD', 'HERR', 'FRAU', 'LAND',
    'NEHM', 'NEHMEN', 'GEHEN', 'SEHEN', 'STEHEN',
    'LESEN', 'HALTEN', 'KOMMEN', 'NEHMEN',
    'WARD', 'WART', 'SOLCH', 'SELB',
]
word_scores = {w: len(w) * 3 for w in german_words}
all_words = sorted(word_scores.keys(), key=len, reverse=True)

def dp_coverage(text):
    n = len(text)
    if n == 0: return 0, 0
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
    wc = 0
    while pos > 0:
        info = back[pos]
        if info is None: pos -= 1
        elif info[0] == 'unk': pos = info[1]
        elif info[0] == 'word':
            wc += len(info[2])
            pos = info[1]
    return wc, n

def total_coverage(m):
    tc = 0
    tt = 0
    for book in books:
        col = collapse(decode(book, m))
        c, t = dp_coverage(col)
        tc += c
        tt += t
    return tc * 100 / tt if tt > 0 else 0

print("=" * 80)
print("SESSION 10s: CODE 86 DEEP TEST + COMPOUND WORD ATTACKS")
print("=" * 80)

# 1. Deep analysis of code 86
print("\n1. CODE 86 DEEP ANALYSIS")
print("-" * 60)
print(f"  Current: code 86 = {mapping['86']}")
print(f"  Frequency: {all_codes['86']} occurrences")

# All N codes for reference
print(f"\n  Current N codes: {rev_map['N']}")
n_freq = sum(all_codes.get(c,0) for c in rev_map['N'])
print(f"  Total N freq: {n_freq}")
print(f"  Current E codes: {rev_map['E']}")
e_freq = sum(all_codes.get(c,0) for c in rev_map['E'])
print(f"  Total E freq: {e_freq}")

# Show ALL contexts where code 86 appears
print("\n  All code 86 contexts (collapsed):")
ctx86 = []
for bi, book in enumerate(books):
    for ci, c in enumerate(book):
        if c == '86':
            start = max(0, ci-5)
            end = min(len(book), ci+6)
            raw = decode(book[start:end])
            col = collapse(raw)
            # Mark position of code 86 in raw
            pos_in_raw = ci - start
            ctx86.append((bi, ci, col, raw, book[start:end]))

for bi, ci, col, raw, codes in ctx86:
    code_str = '-'.join(codes)
    print(f"    B{bi:02d}[{ci}]: {col:30s}  raw={raw}  codes={code_str}")

# Test as N: does it break any known E words?
print("\n  Code 86 as N - checking impact on known E words:")
mod86n = dict(mapping)
mod86n['86'] = 'N'
breaks = []
for bi, book in enumerate(books):
    for ci, c in enumerate(book):
        if c == '86':
            # Check surrounding known words in original
            start = max(0, ci-4)
            end = min(len(book), ci+5)
            orig = collapse(decode(book[start:end]))
            modif = collapse(decode(book[start:end], mod86n))
            for w in ['DER', 'DEN', 'DIE', 'DAS', 'EIN', 'ERDE', 'ENDE',
                       'REDE', 'DENN', 'EINER', 'EINEN', 'SEINE', 'SEIDE',
                       'DIESER', 'SEGEN', 'VIEL', 'WELT', 'WERDE', 'STEH',
                       'FINDEN', 'SONNE', 'NICHT', 'IST', 'EST', 'ERST',
                       'WIE', 'GEH', 'SEI', 'HER']:
                if w in orig and w not in modif:
                    breaks.append((bi, ci, w, orig, modif))

if breaks:
    print("  ** BREAKS FOUND:")
    for bi, ci, w, orig, modif in breaks:
        print(f"    B{bi:02d}[{ci}]: breaks {w}: {orig} -> {modif}")
else:
    print("  ** No known words broken! **")

# New words enabled by N assignment
print("\n  Code 86 as N - new words enabled:")
new_words_found = []
for bi, book in enumerate(books):
    col_n = collapse(decode(book, mod86n))
    col_e = collapse(decode(book))
    for w in all_words:
        if len(w) >= 3 and w in col_n and w not in col_e:
            new_words_found.append((bi, w, col_n[max(0, col_n.index(w)-5):col_n.index(w)+len(w)+5]))

seen_w = set()
for bi, w, ctx in new_words_found:
    if w not in seen_w:
        seen_w.add(w)
        print(f"    New word: {w} in B{bi:02d}: ...{ctx}...")

# Coverage comparison
print("\n  Coverage comparison:")
base = total_coverage(mapping)
print(f"    Baseline (86=E): {base:.1f}%")
cov_n = total_coverage(mod86n)
print(f"    Modified (86=N): {cov_n:.1f}%")
print(f"    Delta: {cov_n - base:+.1f}%")

# 2. Test code 86 as other letters too
print("\n" + "=" * 60)
print("2. CODE 86 - ALL LETTER OPTIONS")
print("=" * 60)
for letter in 'ABCDEFGHIKLMNOPRSTUVWZ':
    mod = dict(mapping)
    mod['86'] = letter
    cov = total_coverage(mod)
    if cov > base:
        print(f"  86={letter}: {cov:.1f}% ({cov-base:+.1f}%) ***")
    elif cov == base:
        pass  # skip no change
    else:
        pass  # skip worse

# 3. Broader combinatorial search: top unconfirmed codes
print("\n" + "=" * 60)
print("3. TOP UNCONFIRMED CODES - ALL LETTER OPTIONS")
print("=" * 60)

# From 10r results: unconfirmed codes
unconfirmed = {
    '66': 'A', '62': 'B', '02': 'D', '63': 'D',
    '09': 'E', '37': 'E', '39': 'E', '69': 'E', '86': 'E',
    '94': 'H', '15': 'I', '96': 'L',
    '04': 'M', '40': 'M', '13': 'N', '71': 'N',
    '79': 'O', '10': 'R', '05': 'S', '33': 'W',
}

# Sort by frequency
unconf_sorted = sorted(unconfirmed.items(), key=lambda x: all_codes.get(x[0], 0), reverse=True)

improvements = []
print(f"  Baseline: {base:.1f}%")
for code, cur_letter in unconf_sorted[:12]:
    freq = all_codes.get(code, 0)
    if freq < 5: continue
    print(f"\n  Code {code} (cur={cur_letter}, {freq}x):")
    for letter in 'ABCDEFGHIKLMNOPRSTUVWZ':
        if letter == cur_letter: continue
        mod = dict(mapping)
        mod[code] = letter
        cov = total_coverage(mod)
        if cov > base + 0.1:
            print(f"    {code}={letter}: {cov:.1f}% ({cov-base:+.1f}%)")
            improvements.append((code, cur_letter, letter, cov - base, freq))

if improvements:
    print(f"\n  All improvements found:")
    improvements.sort(key=lambda x: x[3], reverse=True)
    for code, cur, new, delta, freq in improvements:
        print(f"    code {code} ({cur}->{new}, {freq}x): +{delta:.1f}%")

# 4. Try combining top improvements
print("\n" + "=" * 60)
print("4. COMBINATORIAL: TOP IMPROVEMENTS TOGETHER")
print("=" * 60)

if improvements:
    # Try top 3 improvements together
    top3 = improvements[:min(3, len(improvements))]
    print(f"  Testing top improvements combined:")
    mod_combo = dict(mapping)
    for code, cur, new, delta, freq in top3:
        mod_combo[code] = new
        print(f"    {code}: {cur}->{new}")
    combo_cov = total_coverage(mod_combo)
    print(f"  Combined coverage: {combo_cov:.1f}% (baseline {base:.1f}%, delta {combo_cov-base:+.1f}%)")

    # Also try all improvements
    if len(improvements) > 3:
        mod_all = dict(mapping)
        for code, cur, new, delta, freq in improvements:
            mod_all[code] = new
        all_cov = total_coverage(mod_all)
        print(f"  All improvements: {all_cov:.1f}% (delta {all_cov-base:+.1f}%)")

# 5. COMPOUND WORD ATTACKS with modified mapping
print("\n" + "=" * 60)
print("5. COMPOUND WORD ATTACKS")
print("=" * 60)

# Build best mapping so far
best_map = dict(mapping)
if improvements:
    for code, cur, new, delta, freq in improvements[:3]:
        if delta > 0.3:
            best_map[code] = new

# TIUMENGEMI analysis
print("\n  --- TIUMENGEMI ---")
print("  Always appears before ORT ENGCHD")
print("  Could be GEMEINDE (community) rearranged?")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'TIUMENGEMI' in col:
        idx = col.index('TIUMENGEMI')
        ctx = col[max(0,idx-15):idx+25]
        # Get raw codes
        decoded = decode(book)
        for ri in range(len(decoded)):
            rcol = collapse(decoded[:ri+1])
            if len(rcol) >= idx + 1:
                raw_start = ri - (len(rcol) - idx) + 1
                if raw_start >= 0:
                    break
        # Get the raw codes for TIUMENGEMI
        print(f"    B{bi:02d}: ...{ctx}...")

# Analyze TIUMENGEMI raw codes
print("\n  TIUMENGEMI raw code analysis:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'TIUMENGEMI' not in col: continue
    decoded = decode(book)
    # Find the start position in raw
    target = 'TIUMENGEMI'
    col_pos = 0
    raw_pos = 0
    found = False
    for ri in range(len(decoded)):
        if ri == 0 or decoded[ri] != decoded[ri-1]:
            # New collapsed character
            test = collapse(decoded[:ri+1])
            if test.endswith(target[0]) and len(test) >= col.index(target) + 1:
                # Now find exact start
                break
    # Brute force: try all positions
    for ri in range(len(decoded)):
        sub = decoded[ri:ri+20]
        if collapse(sub).startswith(target):
            raw_codes = book[ri:ri+20]
            raw_letters = [mapping.get(c, '?') for c in raw_codes[:15]]
            print(f"    B{bi:02d} raw pos {ri}: codes={raw_codes[:15]}")
            print(f"    Letters: {' '.join(f'{c}={l}' for c, l in zip(raw_codes[:15], raw_letters))}")
            # Try to find how many codes make up TIUMENGEMI
            col_so_far = ''
            for k in range(15):
                col_so_far = collapse(decoded[ri:ri+k+1])
                if len(col_so_far) >= len(target):
                    print(f"    {len(target)} collapsed chars from {k+1} raw codes")
                    tiu_codes = raw_codes[:k+1]
                    print(f"    TIUMENGEMI codes: {tiu_codes}")
                    break
            break
    break

# SCHWITEIONE analysis
print("\n  --- SCHWITEIONE ---")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'SCHWITEIONE' in col:
        idx = col.index('SCHWITEIONE')
        ctx = col[max(0,idx-10):idx+20]
        print(f"    B{bi:02d}: ...{ctx}...")

# Raw code analysis for SCHWITEIONE
print("\n  SCHWITEIONE raw code analysis:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'SCHWITEIONE' not in col: continue
    decoded = decode(book)
    for ri in range(len(decoded)):
        sub = decoded[ri:ri+25]
        if collapse(sub).startswith('SCHWITEIONE'):
            raw_codes = book[ri:ri+20]
            raw_letters = [mapping.get(c, '?') for c in raw_codes[:16]]
            print(f"    B{bi:02d} raw pos {ri}: codes={raw_codes[:16]}")
            print(f"    Letters: {' '.join(f'{c}={l}' for c, l in zip(raw_codes[:16], raw_letters))}")
            col_so_far = ''
            for k in range(20):
                col_so_far = collapse(decoded[ri:ri+k+1])
                if len(col_so_far) >= len('SCHWITEIONE'):
                    sch_codes = raw_codes[:k+1]
                    print(f"    SCHWITEIONE codes: {sch_codes}")
                    break
            break
    break

# 6. Code 86 as N: full decoded text comparison
print("\n" + "=" * 60)
print("6. CODE 86=N FULL TEXT SAMPLE")
print("=" * 60)
mod86n = dict(mapping)
mod86n['86'] = 'N'

# Show first 10 books with both decodings side by side
for bi in range(min(10, len(books))):
    col_e = collapse(decode(books[bi]))
    col_n = collapse(decode(books[bi], mod86n))
    if col_e != col_n:
        print(f"\n  B{bi:02d} (E): {col_e}")
        print(f"  B{bi:02d} (N): {col_n}")
        # Highlight differences
        diffs = []
        for i in range(min(len(col_e), len(col_n))):
            if col_e[i] != col_n[i]:
                diffs.append(i)
        if diffs:
            print(f"  Diffs at positions: {diffs}")

# 7. Look for P in the cipher (still missing letter)
print("\n" + "=" * 60)
print("7. SEARCH FOR MISSING P")
print("=" * 60)
print("  P expected frequency: ~0.8% in German text")
print("  Total text length: ~5650 chars")
print("  Expected ~45 P occurrences")
print("  Testing all unconfirmed codes as P:")

for code, cur_letter in unconf_sorted:
    freq = all_codes.get(code, 0)
    if freq < 10 or freq > 100: continue
    mod = dict(mapping)
    mod[code] = 'P'
    cov = total_coverage(mod)
    if cov >= base:
        print(f"    code {code} ({cur_letter}->{code}, {freq}x) as P: {cov:.1f}% ({cov-base:+.1f}%)")

# 8. Unknown segment deep attack - the most common unknown runs
print("\n" + "=" * 60)
print("8. MOST COMMON UNKNOWN SEGMENTS")
print("=" * 60)

# Decode all books and find runs of characters not in known words
unknown_segments = Counter()
for bi, book in enumerate(books):
    col = collapse(decode(book))
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
    # Extract unknown runs
    pos = n
    segments = []
    while pos > 0:
        info = back[pos]
        if info is None:
            pos -= 1
        elif info[0] == 'unk':
            segments.append(('unk', info[1], pos))
            pos = info[1]
        elif info[0] == 'word':
            segments.append(('word', info[1], pos, info[2]))
            pos = info[1]

    # Merge consecutive unknown chars into segments
    segments.reverse()
    unk_run = ''
    for seg in segments:
        if seg[0] == 'unk':
            unk_run += col[seg[1]:seg[2]]
        else:
            if unk_run and len(unk_run) >= 2:
                unknown_segments[unk_run] += 1
            unk_run = ''
    if unk_run and len(unk_run) >= 2:
        unknown_segments[unk_run] += 1

print("  Top unknown segments (3+ occurrences):")
for seg, count in unknown_segments.most_common(30):
    if count >= 3:
        print(f"    {seg:25s} x{count}")

print("\n" + "=" * 80)
print("SESSION 10s COMPLETE")
print("=" * 80)
