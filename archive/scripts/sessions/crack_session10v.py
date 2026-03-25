#!/usr/bin/env python3
"""Session 10v: Code 57 H->N hypothesis (MINHE->MINNE) + narrative reading"""

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

print("=" * 80)
print("SESSION 10v: CODE 57 (H->N?) + NARRATIVE READING")
print("=" * 80)

# 1. Code 57 current status
print("\n1. CODE 57 ANALYSIS")
print("-" * 60)
print(f"  Code 57 currently: {mapping['57']}")
print(f"  Frequency: {all_codes['57']} occurrences")
print(f"  H codes: {rev_map['H']}")
h_freqs = [(c, all_codes.get(c,0)) for c in rev_map['H']]
print(f"  H code freqs: {h_freqs}")
print(f"  Total H freq: {sum(f for _,f in h_freqs)}")
print(f"  N codes: {rev_map['N']}")
n_freqs = [(c, all_codes.get(c,0)) for c in rev_map['N']]
print(f"  Total N freq: {sum(f for _,f in n_freqs)}")

# Expected frequencies
total_chars = sum(len(collapse(decode(b))) for b in books)
print(f"\n  Total collapsed text chars: {total_chars}")
h_expected = total_chars * 0.048  # H ~4.8% in German
n_expected = total_chars * 0.098  # N ~9.8% in German
print(f"  Expected H count: ~{h_expected:.0f} ({100*sum(f for _,f in h_freqs)/total_chars:.1f}% actual)")
print(f"  Expected N count: ~{n_expected:.0f} ({100*sum(f for _,f in n_freqs)/total_chars:.1f}% actual)")

# If code 57 moves from H to N:
h_new = sum(f for _,f in h_freqs) - all_codes['57']
n_new = sum(f for _,f in n_freqs) + all_codes['57']
print(f"\n  If code 57 = N:")
print(f"    H would be: {h_new} ({100*h_new/total_chars:.1f}%)")
print(f"    N would be: {n_new} ({100*n_new/total_chars:.1f}%)")
print(f"    H expected: {h_expected:.0f} ({4.8}%)")
print(f"    N expected: {n_expected:.0f} ({9.8}%)")

# 2. ALL contexts of code 57
print("\n\n2. ALL CODE 57 CONTEXTS")
print("-" * 60)

ctx57 = []
for bi, book in enumerate(books):
    for ci, c in enumerate(book):
        if c == '57':
            start = max(0, ci-5)
            end = min(len(book), ci+6)
            raw = decode(book[start:end])
            col = collapse(raw)
            # Also show with N
            mod = dict(mapping)
            mod['57'] = 'N'
            raw_n = decode(book[start:end], mod)
            col_n = collapse(raw_n)
            ctx57.append((bi, ci, col, col_n))

seen_pairs = set()
for bi, ci, col, col_n in ctx57:
    key = (col, col_n)
    if key not in seen_pairs:
        seen_pairs.add(key)
        print(f"  B{bi:02d}[{ci}]: H={col:25s}  N={col_n}")

# 3. Check if code 57=H is confirmed in any known words
print("\n\n3. CODE 57 CONFIRMATION CHECK")
print("-" * 60)

# Words with H
h_words = ['HIER', 'HIN', 'HER', 'HUND', 'HWND', 'HEIT',
           'SCHAUN', 'STEH', 'GEH', 'NICHT', 'HEDEMI']

print("  Checking which H words use code 57:")
for word in h_words:
    found = False
    for bi, book in enumerate(books):
        col = collapse(decode(book))
        if word in col:
            decoded = decode(book)
            for ri in range(len(decoded)):
                sub = decoded[ri:ri+len(word)+3]
                if collapse(sub).startswith(word):
                    # Find H positions in word and check codes
                    col_pos = 0
                    for k in range(ri, min(ri+len(word)*2, len(book))):
                        if k == ri or decoded[k] != decoded[k-1]:
                            if col_pos < len(word):
                                if word[col_pos] == 'H':
                                    code_used = book[k]
                                    is57 = "***57***" if code_used == '57' else f"code {code_used}"
                                    print(f"    {word}: H at pos {col_pos} uses {is57} (B{bi:02d})")
                                    if code_used == '57':
                                        found = True
                                col_pos += 1
                            if col_pos >= len(word):
                                break
                    break
            if found:
                break

# 4. Test the N assignment - check for broken H words
print("\n\n4. CODE 57 AS N - IMPACT ON KNOWN WORDS")
print("-" * 60)

mod57n = dict(mapping)
mod57n['57'] = 'N'

broken = []
improved = []

for bi, book in enumerate(books):
    col_h = collapse(decode(book))
    col_n = collapse(decode(book, mod57n))

    # Check known words
    for word in ['HIER', 'HIN', 'HER', 'HUND', 'HWND', 'NICHT', 'SCHAUN',
                 'STEH', 'GEH', 'HEDEMI', 'ADTHARSC', 'STEIN', 'AUCH',
                 'MINHE', 'DENEN', 'SEGEN', 'KOENIG']:
        if word in col_h and word not in col_n:
            broken.append((bi, word, col_h, col_n))

    # Check for new words with N
    for word in ['MINNE', 'SINNE', 'SONNE', 'WONNE', 'KENNE', 'RENNE',
                 'NENNE', 'BRENNE', 'INNE', 'BEGINNE', 'SPINNE',
                 'UND', 'KIND', 'HAND', 'BAND', 'LAND',
                 'NAHMEN', 'NUN', 'DENKEN']:
        if word in col_n and word not in col_h:
            improved.append((bi, word, col_n))

if broken:
    print("  BROKEN words:")
    seen = set()
    for bi, word, _, _ in broken:
        if word not in seen:
            seen.add(word)
            print(f"    BREAKS: {word}")
else:
    print("  ** No known words broken! **")

if improved:
    print("\n  NEW words found with N:")
    seen = set()
    for bi, word, col_n in improved:
        if word not in seen:
            seen.add(word)
            idx = col_n.index(word)
            ctx = col_n[max(0,idx-8):idx+len(word)+8]
            print(f"    NEW: {word} in B{bi:02d}: ...{ctx}...")

# 5. DP Coverage comparison
print("\n\n5. COVERAGE COMPARISON")
print("-" * 60)

# Extended word list with MINNE
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
    'HWND', 'WISET', 'OWI', 'MINHE', 'MINNE',
    'EINEN', 'EINER', 'SEINE', 'SEIDE',
    'TAG', 'WEG', 'DER', 'DEN', 'DIE', 'DAS',
    'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON',
    'MIT', 'WIE', 'SEI', 'AUS', 'ORT', 'TUN',
    'NUR', 'SUN', 'TOT', 'GAR', 'ACH', 'ZUM',
    'HIN', 'HER', 'ALS', 'AUCH', 'RUND', 'GEH',
    'NACH', 'IENE', 'NOCH', 'ALLE', 'WOHL',
    'HIER', 'SICH', 'SIND', 'SEHR',
    'ABER', 'ODER', 'WENN', 'DANN',
    'ALTE', 'EDEL', 'HELD', 'LAND', 'BURG', 'WALD',
    'WARD', 'WART', 'SOLCH', 'SELB',
    'ER', 'ES', 'IN', 'SO', 'AN', 'IM',
    'DA', 'NU', 'IR', 'EZ', 'DO', 'OB', 'IE',
]
german_words = list(dict.fromkeys(german_words))
word_scores = {w: len(w) * 3 for w in german_words}
all_words = sorted(word_scores.keys(), key=len, reverse=True)

def dp_coverage_total(m):
    tc = 0
    tt = 0
    for book in books:
        col = collapse(decode(book, m))
        n = len(col)
        if n == 0: continue
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
        pos = n
        wc = 0
        while pos > 0:
            info = back[pos]
            if info is None: pos -= 1
            elif info[0] == 'unk': pos = info[1]
            elif info[0] == 'word':
                wc += len(info[2])
                pos = info[1]
        tc += wc
        tt += n
    return tc * 100 / tt if tt > 0 else 0

base_cov = dp_coverage_total(mapping)
n_cov = dp_coverage_total(mod57n)
print(f"  Baseline (57=H): {base_cov:.1f}%")
print(f"  Modified (57=N): {n_cov:.1f}%")
print(f"  Delta: {n_cov - base_cov:+.1f}%")

# 6. If 57=N works, what does MINNE context look like?
print("\n\n6. TEXT WITH CODE 57=N (MINNE)")
print("-" * 60)

if n_cov >= base_cov:
    print("  Books where code 57 appears (showing N version):")
    for bi, book in enumerate(books):
        has57 = any(c == '57' for c in book)
        if has57:
            col_n = collapse(decode(book, mod57n))
            col_h = collapse(decode(book))
            print(f"\n  B{bi:02d} (H): {col_h}")
            print(f"  B{bi:02d} (N): {col_n}")

# 7. Deeper: what if BOTH code 57=N AND code 04=A?
print("\n\n7. COMBINED: 57=N + 04=A TEST")
print("-" * 60)
mod_both = dict(mapping)
mod_both['57'] = 'N'
mod_both['04'] = 'A'
both_cov = dp_coverage_total(mod_both)
print(f"  Combined (57=N, 04=A): {both_cov:.1f}%")
print(f"  Delta from baseline: {both_cov - base_cov:+.1f}%")

# Show sample text
print("\n  B05 with combined changes:")
col_orig = collapse(decode(books[5]))
col_mod = collapse(decode(books[5], mod_both))
print(f"    Original: {col_orig}")
print(f"    Modified: {col_mod}")

# 8. Pattern analysis: what does HEDEMI become with 57=N?
print("\n\n8. HEDEMI WITH 57=N")
print("-" * 60)
# HEDEMI raw codes: check
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'HEDEMI' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            sub = decoded[ri:ri+10]
            if collapse(sub).startswith('HEDEMI'):
                raw_codes = book[ri:ri+8]
                raw = [f"{c}={mapping.get(c,'?')}" for c in raw_codes[:8]]
                col_n_txt = collapse(decode(book[ri:ri+8], mod57n))
                print(f"  B{bi:02d}: HEDEMI codes: {' '.join(raw)}")
                print(f"         With 57=N: {col_n_txt}")
                break
        break

# Does HEDEMI use code 57?
print("\n  Does HEDEMI contain code 57?")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'HEDEMI' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            sub = decoded[ri:ri+10]
            if collapse(sub).startswith('HEDEMI'):
                codes_used = book[ri:ri+8]
                has57 = '57' in codes_used[:6]
                print(f"  B{bi:02d}: codes={codes_used[:6]}, contains 57: {has57}")
                break
        break

# 9. Summary of all findings
print("\n\n" + "=" * 60)
print("9. SESSION 10v SUMMARY")
print("=" * 60)
print(f"  Code 57 current: H ({all_codes['57']}x)")
print(f"  Hypothesis: Code 57 = N")
print(f"  Key evidence: MINHE(H) -> MINNE(N) = MHG love")
print(f"  Coverage impact: {n_cov - base_cov:+.1f}%")
if not broken:
    print("  No confirmed words broken")
else:
    print(f"  Words broken: {len(set(w for _,w,_,_ in broken))}")
print(f"  Frequency analysis:")
print(f"    H {4.8}% expected, currently {100*sum(f for _,f in h_freqs)/total_chars:.1f}%")
print(f"    N {9.8}% expected, currently {100*sum(f for _,f in n_freqs)/total_chars:.1f}%")
if n_cov > base_cov:
    print(f"  VERDICT: Code 57=N improves text - APPLY CHANGE")
elif n_cov == base_cov and not broken:
    print(f"  VERDICT: Neutral change, linguistic evidence supports N (MINNE)")
else:
    print(f"  VERDICT: Change may not be beneficial")

print("\n" + "=" * 80)
print("SESSION 10v COMPLETE")
print("=" * 80)
