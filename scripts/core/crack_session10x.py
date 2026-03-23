#!/usr/bin/env python3
"""Session 10x: Build continuous superstring + full narrative read"""

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

decoded_all = [collapse(decode(b)) for b in books]

print("=" * 80)
print("SESSION 10x: SUPERSTRING ASSEMBLY + NARRATIVE")
print("=" * 80)

# 1. Build overlap graph
print("\n1. OVERLAP GRAPH")
print("-" * 60)

# For each pair of books, find the best suffix-prefix overlap
overlaps = {}  # (i,j) -> overlap_length
for i in range(len(decoded_all)):
    for j in range(len(decoded_all)):
        if i == j: continue
        ti = decoded_all[i]
        tj = decoded_all[j]
        best = 0
        for k in range(min(len(ti), len(tj)), 4, -1):
            if ti[-k:] == tj[:k]:
                best = k
                break
        if best >= 5:
            overlaps[(i,j)] = best

# Build adjacency: for each book, find best successor
best_succ = {}
for (i,j), ov in overlaps.items():
    if i not in best_succ or ov > best_succ[i][1]:
        best_succ[i] = (j, ov)

best_pred = {}
for (i,j), ov in overlaps.items():
    if j not in best_pred or ov > best_pred[j][1]:
        best_pred[j] = (i, ov)

# Find start nodes: books with no good predecessor
all_books = set(range(len(decoded_all)))
has_pred = set(j for (i,j) in overlaps.keys())
starts = all_books - has_pred

print(f"  Books with no predecessor: {sorted(starts)}")
print(f"  Total overlapping pairs: {len(overlaps)}")

# 2. Greedy chain building - try multiple starts
print("\n\n2. CHAIN BUILDING")
print("-" * 60)

def build_chain(start):
    chain = [start]
    used = {start}
    current = start
    while current in best_succ:
        nxt, ov = best_succ[current]
        if nxt in used:
            break
        chain.append(nxt)
        used.add(nxt)
        current = nxt
    return chain

best_chain = []
for start in list(starts) + list(range(len(decoded_all))):
    chain = build_chain(start)
    if len(chain) > len(best_chain):
        best_chain = chain

print(f"  Longest chain: {len(best_chain)} books")
print(f"  Chain: {best_chain}")

# 3. Assemble superstring from chain
print("\n\n3. SUPERSTRING ASSEMBLY")
print("-" * 60)

if best_chain:
    superstring = decoded_all[best_chain[0]]
    assembly_log = [(best_chain[0], 0, len(decoded_all[best_chain[0]]))]

    for idx in range(1, len(best_chain)):
        bi = best_chain[idx]
        prev = best_chain[idx-1]
        key = (prev, bi)
        ov = overlaps.get(key, 0)
        new_text = decoded_all[bi][ov:]
        start_pos = len(superstring)
        superstring += new_text
        assembly_log.append((bi, start_pos, len(new_text)))

    print(f"  Superstring length: {len(superstring)} chars")
    print(f"  Books used: {len(best_chain)}")
    print(f"  Books not in chain: {sorted(all_books - set(best_chain))}")

    # Show in 80-char lines
    print(f"\n  FULL SUPERSTRING:")
    for i in range(0, len(superstring), 70):
        line = superstring[i:i+70]
        print(f"  [{i:4d}] {line}")

# 4. Try alternate: merge ALL books greedily
print("\n\n4. GREEDY MERGE ALL BOOKS")
print("-" * 60)

# Start with longest book, keep merging
remaining = list(range(len(decoded_all)))
remaining.sort(key=lambda i: len(decoded_all[i]), reverse=True)
merged = decoded_all[remaining[0]]
used = {remaining[0]}

for _ in range(len(remaining)):
    best_bi = None
    best_ov = 0
    best_side = None  # 'right' or 'left'
    best_text = ''

    for bi in remaining:
        if bi in used: continue
        text = decoded_all[bi]

        # Check right append: end of merged overlaps with start of text
        for k in range(min(len(merged), len(text)), 4, -1):
            if merged[-k:] == text[:k]:
                if k > best_ov:
                    best_ov = k
                    best_bi = bi
                    best_side = 'right'
                    best_text = text[k:]
                break

        # Check left prepend: end of text overlaps with start of merged
        for k in range(min(len(merged), len(text)), 4, -1):
            if text[-k:] == merged[:k]:
                if k > best_ov:
                    best_ov = k
                    best_bi = bi
                    best_side = 'left'
                    best_text = text[:-k]
                break

    if best_bi is None:
        break

    used.add(best_bi)
    if best_side == 'right':
        merged += best_text
    else:
        merged = best_text + merged

print(f"  Merged {len(used)} of {len(remaining)} books")
print(f"  Merged text length: {len(merged)} chars")
print(f"  Not merged: {sorted(set(range(len(decoded_all))) - used)}")

# Show merged text
print(f"\n  MERGED SUPERSTRING:")
for i in range(0, len(merged), 70):
    line = merged[i:i+70]
    print(f"  [{i:4d}] {line}")

# 5. Word-level segmented reading of merged text
print("\n\n5. SEGMENTED NARRATIVE")
print("-" * 60)

NEG_INF = float('-inf')
german_words = [
    'EILCHANHEARUCHTIG', 'EDETOTNIURGS', 'WRLGTNELNRHELUIRUNN',
    'TIUMENGEMI', 'SCHWITEIONE', 'LABGZERAS', 'HEDEMI', 'TAUTR',
    'LABRNI', 'ADTHARSC', 'ENGCHD', 'KELSEI',
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
    'TER',  # MHG article variant
    'HIET',  # MHG past of heizen
    'NGETRAS',  # unknown but consistent
    'GEVMT',  # unknown but consistent
    'DGEDA',  # likely D + GEDA
    'TEMDIA',  # unknown
    'UISEMIV',  # unknown
    'TEIGN',  # between FINDEN and DAS
    'CHN',  # unknown
    'SCE',  # unknown
]

german_words = list(dict.fromkeys(german_words))
word_scores = {w: len(w) * 3 for w in german_words}
all_words = sorted(word_scores.keys(), key=len, reverse=True)

def dp_segment_full(text):
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

# Segment the merged text
parts, covered, total = dp_segment_full(merged)
print(f"  Coverage: {covered}/{total} = {covered*100/total:.1f}%")
print()

# Format as readable narrative
line = ''
line_num = 1
for ptype, ptext in parts:
    if ptype == 'W':
        word = ptext
    else:
        word = f'[{ptext}]'

    if len(line) + len(word) + 1 > 70:
        print(f"  {line_num:3d}| {line}")
        line = word + ' '
        line_num += 1
    else:
        line += word + ' '

if line.strip():
    print(f"  {line_num:3d}| {line}")

print("\n" + "=" * 80)
print("SESSION 10x COMPLETE")
print("=" * 80)
