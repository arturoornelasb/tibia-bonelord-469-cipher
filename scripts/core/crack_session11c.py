#!/usr/bin/env python3
"""Session 11c: Combined code reassignment + narrative assembly"""

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
    tc = 0; tt = 0
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
                back[i+1] = ('u', i)
            for word in all_words:
                wl = len(word)
                if i + wl <= n and col[i:i+wl] == word:
                    ns = dp[i] + word_scores.get(word, wl)
                    if ns > dp[i+wl]:
                        dp[i+wl] = ns
                        back[i+wl] = ('w', i, wl)
        pos = n
        wc = 0
        while pos > 0:
            info = back[pos]
            if info is None: pos -= 1
            elif info[0] == 'u': pos = info[1]
            elif info[0] == 'w':
                wc += info[2]
                pos = info[1]
        tc += wc; tt += n
    return tc * 100 / tt if tt > 0 else 0

base = dp_coverage(mapping)
print("=" * 80)
print("SESSION 11c: COMBINED CODE REASSIGNMENT + NARRATIVE")
print("=" * 80)
print(f"\nBaseline coverage: {base:.1f}%")

# 1. Test PAIRS of code changes
print("\n1. COMBINED CODE PAIR TESTS")
print("-" * 60)

# Focus on highest-impact unconfirmed codes
# I(10.0%) is most over-rep, code 15(I, freq=85) is unconfirmed
# B(0.4%) and F(0.3%) are most under-rep
# Also test: 96(L,52), 94(H,50), 04(M,80)

# Key hypothesis: code 15(I) + code 96(L) might be wrong
targets = [
    ('15', 'I', 85),  # most frequent unconfirmed I
    ('96', 'L', 52),  # unconfirmed L, appears in consonant clusters
    ('94', 'H', 50),  # unconfirmed H, appears in consonant clusters
    ('04', 'M', 80),  # unconfirmed M
]

letters = 'ABCDEFGHIKLMNORSTUVWZ'
best_pair = None
best_pair_cov = base

# Test all pairs from targets x letters
print("  Testing pair combinations...")
for i in range(len(targets)):
    for j in range(i+1, len(targets)):
        code_i, curr_i, _ = targets[i]
        code_j, curr_j, _ = targets[j]
        for li in letters:
            if li == curr_i: continue
            for lj in letters:
                if lj == curr_j: continue
                mod = dict(mapping)
                mod[code_i] = li
                mod[code_j] = lj
                cov = dp_coverage(mod)
                if cov > best_pair_cov + 0.3:  # Only report significant improvements
                    print(f"  {code_i}:{curr_i}->{li} + {code_j}:{curr_j}->{lj} = {cov:.1f}% (+{cov-base:.1f}%)")
                    best_pair_cov = cov
                    best_pair = (code_i, li, code_j, lj)

if best_pair:
    print(f"\n  Best pair: code {best_pair[0]}->{best_pair[1]}, code {best_pair[2]}->{best_pair[3]} = {best_pair_cov:.1f}%")
else:
    print("\n  No significant pair improvements found")

# 2. Test code 15 specifically: I->B, I->F, I->P (missing letters)
print("\n\n2. CODE 15 DEEP TEST (I -> missing letters)")
print("-" * 60)

for target_letter in ['B', 'F', 'P', 'A', 'O']:
    mod = dict(mapping)
    mod['15'] = target_letter
    cov = dp_coverage(mod)

    # Check what changes in text
    changes = 0
    sample = None
    for bi, book in enumerate(books):
        col_old = collapse(decode(book))
        col_new = collapse(decode(book, mod))
        if col_old != col_new:
            changes += 1
            if sample is None:
                for pos in range(min(len(col_old), len(col_new))):
                    if pos < len(col_old) and pos < len(col_new) and col_old[pos] != col_new[pos]:
                        s = max(0, pos-15)
                        e = min(len(col_old), pos+15)
                        sample = (bi, col_old[s:e], col_new[s:e])
                        break

    print(f"  15: I->{target_letter}: {cov:.1f}% ({cov-base:+.1f}%), {changes} books changed")
    if sample:
        bi, old, new = sample
        print(f"    B{bi:02d} old: ...{old}...")
        print(f"    B{bi:02d} new: ...{new}...")

# 3. Test code 96 specifically: L -> vowels
print("\n\n3. CODE 96 DEEP TEST (L -> vowels/other)")
print("-" * 60)

for target_letter in ['A', 'E', 'O', 'B', 'F', 'P']:
    mod = dict(mapping)
    mod['96'] = target_letter
    cov = dp_coverage(mod)

    changes = 0
    sample = None
    for bi, book in enumerate(books):
        col_old = collapse(decode(book))
        col_new = collapse(decode(book, mod))
        if col_old != col_new:
            changes += 1
            if sample is None:
                for pos in range(min(len(col_old), len(col_new))):
                    if col_old[pos] != col_new[pos]:
                        s = max(0, pos-15)
                        e = min(len(col_old), pos+15)
                        sample = (bi, col_old[s:e], col_new[s:e])
                        break

    print(f"  96: L->{target_letter}: {cov:.1f}% ({cov-base:+.1f}%), {changes} books changed")
    if sample:
        bi, old, new = sample
        print(f"    B{bi:02d} old: ...{old}...")
        print(f"    B{bi:02d} new: ...{new}...")
    # Show what known words are affected
    if target_letter in ['A', 'E', 'O']:
        # Show WRLGTNELNRHELU with the change
        mod_text = collapse(''.join(mod.get(c, '?') for c in ['36','24','96','84','75','60','19','96','58','55','06','49','96','70']))
        print(f"    WRLGTNELNRHELU becomes: {mod_text}")

# 4. Full narrative with best current mapping
print("\n\n4. FULL NARRATIVE RECONSTRUCTION")
print("-" * 60)

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

# Group books by overlap to find reading order
all_collapsed = [collapse(decode(b)) for b in books]

# Find all overlapping chains
overlaps = {}
for i in range(len(all_collapsed)):
    for j in range(len(all_collapsed)):
        if i == j: continue
        ti = all_collapsed[i]
        tj = all_collapsed[j]
        for k in range(min(len(ti), len(tj)), 4, -1):
            if ti[-k:] == tj[:k]:
                overlaps[(i,j)] = k
                break

# Build best successor for each book
best_succ = {}
for (i,j), ov in overlaps.items():
    if i not in best_succ or ov > best_succ[i][1]:
        best_succ[i] = (j, ov)

# Group connected books
visited = set()
groups = []
for start in range(len(all_collapsed)):
    if start in visited: continue
    group = [start]
    visited.add(start)
    current = start
    while current in best_succ:
        nxt, ov = best_succ[current]
        if nxt in visited: break
        group.append(nxt)
        visited.add(nxt)
        current = nxt
    groups.append(group)

# Sort groups by size
groups.sort(key=len, reverse=True)

print(f"  {len(groups)} groups of overlapping books")
print(f"  Largest groups: {[len(g) for g in groups[:5]]}")

# Show the largest group's narrative
if groups:
    main_group = groups[0]
    print(f"\n  Largest group ({len(main_group)} books): {main_group[:20]}")

    # Assemble the group into a superstring
    if len(main_group) > 1:
        superstring = all_collapsed[main_group[0]]
        for idx in range(1, len(main_group)):
            bi = main_group[idx]
            prev = main_group[idx-1]
            key = (prev, bi)
            ov = overlaps.get(key, 0)
            superstring += all_collapsed[bi][ov:]

        print(f"  Superstring length: {len(superstring)}")
        parts, cov, tot = dp_segment(superstring)
        print(f"  Coverage: {cov}/{tot} = {cov*100/tot:.1f}%")

        # Format narrative
        print(f"\n  NARRATIVE:")
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

# 5. Show ALL 70 books sorted by coverage
print("\n\n5. ALL BOOKS BY COVERAGE")
print("-" * 60)

book_cov = []
for bi in range(len(all_collapsed)):
    parts, cov, tot = dp_segment(all_collapsed[bi])
    pct = cov * 100 / tot if tot > 0 else 0
    book_cov.append((bi, pct, tot))

book_cov.sort(key=lambda x: x[1], reverse=True)

for bi, pct, length in book_cov:
    bar = '#' * int(pct / 5) + '.' * (20 - int(pct / 5))
    print(f"  B{bi:02d} [{bar}] {pct:5.1f}% ({length} chars)")

# 6. Summary statistics
print("\n\n6. SUMMARY")
print("-" * 60)
total_chars = sum(len(all_collapsed[bi]) for bi in range(len(all_collapsed)))
total_cov = sum(dp_segment(all_collapsed[bi])[1] for bi in range(len(all_collapsed)))
print(f"  Total text: {total_chars} chars across {len(books)} books")
print(f"  Total coverage: {total_cov}/{total_chars} = {total_cov*100/total_chars:.1f}%")
print(f"  Books > 90%: {sum(1 for _,p,_ in book_cov if p >= 90)}")
print(f"  Books > 70%: {sum(1 for _,p,_ in book_cov if p >= 70)}")
print(f"  Books > 50%: {sum(1 for _,p,_ in book_cov if p >= 50)}")
print(f"  Books < 30%: {sum(1 for _,p,_ in book_cov if p < 30)}")

# Confirmed proper nouns in the narrative
print(f"\n  Identified proper nouns:")
nouns = {
    'TAUTR': 'person/deity',
    'EILCHANHEARUCHTIG': 'adjective (renowned)',
    'EDETOTNIURGS': "TAUTR's attribute/title",
    'HEDEMI': 'place (has ancient stones)',
    'ADTHARSC': 'entity (at the stones)',
    'LABRNI': 'person/place',
    'ENGCHD': 'place',
    'KELSEI': 'person/thing',
    'TIUMENGEMI': 'person/thing',
    'LABGZERAS': 'king (KOENIG)',
    'SCHWITEIONE': 'attribute/state',
}
for name, desc in nouns.items():
    count = sum(1 for t in all_collapsed if name in t)
    print(f"    {name}: {desc} ({count} books)")

print("\n" + "=" * 80)
print("SESSION 11c COMPLETE")
print("=" * 80)
