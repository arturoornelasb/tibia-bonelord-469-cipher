#!/usr/bin/env python3
"""Session 12k: DECODED-TEXT-LEVEL assembly (not raw codes!)
Key insight: homophonic substitution means same text uses different codes.
Raw code overlaps miss books that encode the same text with different code variants."""

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
print("SESSION 12k: DECODED-TEXT-LEVEL ASSEMBLY")
print("=" * 80)

# 1. Decode all books (UNCOLLAPSED - preserving doubles)
decoded_books = [decode_str(s) for s in corrected]
collapsed_books = [collapse(d) for d in decoded_books]

print("\n1. DECODED BOOK OVERLAPS (letter level)")
print("-" * 60)

# Find overlaps at the DECODED TEXT level (not raw code level)
decoded_overlaps = {}
for i in range(len(decoded_books)):
    for j in range(len(decoded_books)):
        if i == j: continue
        si = decoded_books[i]
        sj = decoded_books[j]
        for k in range(min(len(si), len(sj)), 1, -1):
            if si[-k:] == sj[:k]:
                decoded_overlaps[(i,j)] = k
                break

# Compare with raw code overlaps
raw_overlaps = {}
for i in range(len(corrected)):
    for j in range(len(corrected)):
        if i == j: continue
        si = corrected[i]
        sj = corrected[j]
        for k in range(min(len(si), len(sj)), 3, -2):
            if si[-k:] == sj[:k]:
                raw_overlaps[(i,j)] = k // 2
                break

print(f"  Raw code overlaps: {len(raw_overlaps)}")
print(f"  Decoded text overlaps: {len(decoded_overlaps)}")

# Show overlaps that exist at decoded level but NOT at code level
new_overlaps = set(decoded_overlaps.keys()) - set(raw_overlaps.keys())
print(f"  NEW overlaps (decoded only): {len(new_overlaps)}")

# Show top new overlaps
new_by_size = [(pair, decoded_overlaps[pair]) for pair in new_overlaps]
new_by_size.sort(key=lambda x: -x[1])
print(f"\n  Top new decoded-level overlaps:")
for (i,j), ov in new_by_size[:20]:
    # Show the overlapping text
    si = decoded_books[i]
    overlap_text = si[-ov:]
    overlap_collapsed = collapse(overlap_text)
    print(f"    B{i:02d} -> B{j:02d}: {ov} decoded chars ({len(overlap_collapsed)} collapsed): ...{overlap_collapsed[:40]}...")

# 2. Greedy assembly using DECODED text overlaps
print("\n2. DECODED-TEXT GREEDY ASSEMBLY")
print("-" * 60)

best_merged = ''
best_used = set()
best_start = -1
best_contained = set()

for start_idx in range(len(decoded_books)):
    merged = decoded_books[start_idx]
    used = {start_idx}

    changed = True
    while changed:
        changed = False
        best_bi = None
        best_ov = 0
        best_side = None
        best_new = ''

        for bi in range(len(decoded_books)):
            if bi in used: continue
            text = decoded_books[bi]

            # Right overlap
            for k in range(min(len(merged), len(text)), 1, -1):
                if merged[-k:] == text[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'right'
                        best_new = text[k:]
                    break
            # Left overlap
            for k in range(min(len(merged), len(text)), 1, -1):
                if text[-k:] == merged[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'left'
                        best_new = text[:-k]
                    break

        if best_bi is not None and best_ov >= 3:
            used.add(best_bi)
            if best_side == 'right':
                merged += best_new
            else:
                merged = best_new + merged
            changed = True

    # Check containment
    contained = set()
    for bi in range(len(decoded_books)):
        if decoded_books[bi] in merged:
            contained.add(bi)

    if len(contained) > len(best_contained):
        best_merged = merged
        best_used = set(used)
        best_start = start_idx
        best_contained = set(contained)

print(f"  Best start: B{best_start:02d}")
print(f"  Books merged: {len(best_used)}/{len(decoded_books)}")
print(f"  Books contained: {len(best_contained)}/{len(decoded_books)}")
missing = sorted(set(range(len(decoded_books))) - best_contained)
print(f"  Missing: {missing}")

# 3. Collapse and display
print("\n3. FULL NARRATIVE (decoded-level assembly)")
print("-" * 60)

collapsed_merged = collapse(best_merged)
print(f"  Decoded chars: {len(best_merged)}")
print(f"  Collapsed chars: {len(collapsed_merged)}")
print()
for i in range(0, len(collapsed_merged), 70):
    print(f"  [{i:4d}] {collapsed_merged[i:i+70]}")

# 4. Also try COLLAPSED text overlaps
print("\n4. COLLAPSED-TEXT ASSEMBLY")
print("-" * 60)

best_merged_c = ''
best_contained_c = set()

for start_idx in range(len(collapsed_books)):
    merged = collapsed_books[start_idx]
    used = {start_idx}

    changed = True
    while changed:
        changed = False
        best_bi = None
        best_ov = 0
        best_side = None
        best_new = ''

        for bi in range(len(collapsed_books)):
            if bi in used: continue
            text = collapsed_books[bi]

            for k in range(min(len(merged), len(text)), 2, -1):
                if merged[-k:] == text[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'right'
                        best_new = text[k:]
                    break
            for k in range(min(len(merged), len(text)), 2, -1):
                if text[-k:] == merged[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'left'
                        best_new = text[:-k]
                    break

        if best_bi is not None and best_ov >= 3:
            used.add(best_bi)
            if best_side == 'right':
                merged += best_new
            else:
                merged = best_new + merged
            changed = True

    contained = set()
    for bi in range(len(collapsed_books)):
        if collapsed_books[bi] in merged:
            contained.add(bi)

    if len(contained) > len(best_contained_c):
        best_merged_c = merged
        best_contained_c = set(contained)

print(f"  Books contained (collapsed): {len(best_contained_c)}/{len(collapsed_books)}")
c_missing = sorted(set(range(len(collapsed_books))) - best_contained_c)
print(f"  Missing: {c_missing}")

if len(best_contained_c) > len(best_contained):
    print(f"\n  Collapsed assembly is BETTER!")
    print(f"  Collapsed chars: {len(best_merged_c)}")
    print()
    for i in range(0, len(best_merged_c), 70):
        print(f"  [{i:4d}] {best_merged_c[i:i+70]}")
    final_text = best_merged_c
    final_contained = best_contained_c
else:
    print(f"\n  Decoded assembly is better (or equal)")
    final_text = collapsed_merged
    final_contained = best_contained

# 5. DP Segmentation of the best result
print("\n5. DP SEGMENTED NARRATIVE")
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

parts, covered, total = dp_segment(final_text)
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

# 6. How many books are IDENTICAL at decoded level vs code level?
print("\n6. BOOK RELATIONSHIP ANALYSIS")
print("-" * 60)

# Find book pairs that decode to the same text
for i in range(len(decoded_books)):
    for j in range(i+1, len(decoded_books)):
        if decoded_books[i] == decoded_books[j]:
            print(f"  B{i:02d} and B{j:02d}: IDENTICAL decoded text!")
        elif collapsed_books[i] == collapsed_books[j]:
            print(f"  B{i:02d} and B{j:02d}: identical COLLAPSED text (different uncollapsed)")

# Check if any book is a substring of another at decoded level
substr_pairs = []
for i in range(len(decoded_books)):
    for j in range(len(decoded_books)):
        if i == j: continue
        if decoded_books[i] in decoded_books[j]:
            substr_pairs.append((i, j))

print(f"\n  Decoded-text containment pairs: {len(substr_pairs)}")
for i, j in substr_pairs[:15]:
    print(f"    B{i:02d} ({len(decoded_books[i])} chars) is contained in B{j:02d} ({len(decoded_books[j])} chars)")

# Check at collapsed level
csubstr_pairs = []
for i in range(len(collapsed_books)):
    for j in range(len(collapsed_books)):
        if i == j: continue
        if collapsed_books[i] in collapsed_books[j]:
            csubstr_pairs.append((i, j))

print(f"\n  Collapsed-text containment pairs: {len(csubstr_pairs)}")
for i, j in csubstr_pairs[:15]:
    print(f"    B{i:02d} ({len(collapsed_books[i])} chars) is contained in B{j:02d} ({len(collapsed_books[j])} chars)")

# 7. What's the TOTAL unique text if we merge everything?
print("\n7. TOTAL UNIQUE TEXT (all books)")
print("-" * 60)

# Simple union of all collapsed text
all_text = set()
for bi, text in enumerate(collapsed_books):
    for i in range(len(text)):
        for j in range(i+3, min(i+50, len(text)+1)):
            all_text.add(text[i:j])

# Count unique 3-grams across all books
all_trigrams = set()
for text in collapsed_books:
    for i in range(len(text)-2):
        all_trigrams.add(text[i:i+3])

print(f"  Unique 3-grams: {len(all_trigrams)}")
print(f"  Total collapsed chars (sum): {sum(len(t) for t in collapsed_books)}")
print(f"  Average book length (collapsed): {sum(len(t) for t in collapsed_books)/len(collapsed_books):.0f}")

# 8. For still-missing books, show their collapsed text
print("\n8. MISSING BOOKS TEXT")
print("-" * 60)

final_missing = sorted(set(range(len(decoded_books))) - final_contained)
for bi in final_missing[:10]:
    text = collapsed_books[bi]
    print(f"  B{bi:02d} ({len(text)} chars): {text[:80]}...")
    # Check best substring match in final_text
    best_match = ''
    for k in range(len(text), 2, -1):
        for start in range(len(text) - k + 1):
            sub = text[start:start+k]
            if sub in final_text:
                best_match = sub
                break
        if best_match:
            break
    if best_match:
        print(f"       Best common substring ({len(best_match)} chars): {best_match[:50]}...")

print("\n" + "=" * 80)
print("SESSION 12k COMPLETE")
print("=" * 80)
