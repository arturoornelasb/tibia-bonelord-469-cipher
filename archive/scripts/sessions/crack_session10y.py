#!/usr/bin/env python3
"""Session 10y: Improved superstring assembly with lower threshold + full decode"""

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
print("SESSION 10y: IMPROVED SUPERSTRING + FULL NARRATIVE")
print("=" * 80)

# 1. Build complete overlap matrix with lower threshold
print("\n1. OVERLAP MATRIX (threshold >= 3)")
print("-" * 60)

overlaps = {}
for i in range(len(decoded_all)):
    for j in range(len(decoded_all)):
        if i == j: continue
        ti = decoded_all[i]
        tj = decoded_all[j]
        best = 0
        for k in range(min(len(ti), len(tj)), 2, -1):
            if ti[-k:] == tj[:k]:
                best = k
                break
        if best >= 3:
            overlaps[(i,j)] = best

print(f"  Pairs with >= 3 char overlap: {len(overlaps)}")

# Show distribution
ov_dist = Counter()
for ov in overlaps.values():
    if ov >= 50: ov_dist['50+'] += 1
    elif ov >= 20: ov_dist['20-49'] += 1
    elif ov >= 10: ov_dist['10-19'] += 1
    elif ov >= 5: ov_dist['5-9'] += 1
    else: ov_dist['3-4'] += 1
print(f"  Distribution: {dict(ov_dist)}")

# Top overlaps
top_ov = sorted(overlaps.items(), key=lambda x: x[1], reverse=True)[:20]
print(f"\n  Top 20 overlaps:")
for (i,j), ov in top_ov:
    print(f"    B{i:02d} -> B{j:02d}: {ov} chars")

# 2. Try greedy merge from EVERY starting book
print("\n\n2. GREEDY MERGE FROM ALL STARTS (threshold >= 3)")
print("-" * 60)

best_merged = ''
best_used = set()
best_start = -1

for start_idx in range(len(decoded_all)):
    remaining = list(range(len(decoded_all)))
    merged = decoded_all[start_idx]
    used = {start_idx}

    changed = True
    while changed:
        changed = False
        best_bi = None
        best_ov = 0
        best_side = None
        best_text = ''

        for bi in remaining:
            if bi in used: continue
            text = decoded_all[bi]

            # Right append
            for k in range(min(len(merged), len(text)), 2, -1):
                if merged[-k:] == text[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'right'
                        best_text = text[k:]
                    break

            # Left prepend
            for k in range(min(len(merged), len(text)), 2, -1):
                if text[-k:] == merged[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'left'
                        best_text = text[:-k]
                    break

        if best_bi is not None and best_ov >= 3:
            used.add(best_bi)
            if best_side == 'right':
                merged += best_text
            else:
                merged = best_text + merged
            changed = True

    if len(used) > len(best_used):
        best_merged = merged
        best_used = set(used)
        best_start = start_idx

print(f"  Best start: B{best_start:02d}")
print(f"  Books merged: {len(best_used)} of {len(decoded_all)}")
print(f"  Merged text length: {len(best_merged)} chars")
print(f"  Not merged: {sorted(set(range(len(decoded_all))) - best_used)}")

# 3. Try with threshold 4 (less aggressive)
print("\n\n3. GREEDY MERGE (threshold >= 4)")
print("-" * 60)

best_merged4 = ''
best_used4 = set()
best_start4 = -1

for start_idx in range(len(decoded_all)):
    remaining = list(range(len(decoded_all)))
    merged = decoded_all[start_idx]
    used = {start_idx}

    changed = True
    while changed:
        changed = False
        best_bi = None
        best_ov = 0
        best_side = None
        best_text = ''

        for bi in remaining:
            if bi in used: continue
            text = decoded_all[bi]

            for k in range(min(len(merged), len(text)), 3, -1):
                if merged[-k:] == text[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'right'
                        best_text = text[k:]
                    break

            for k in range(min(len(merged), len(text)), 3, -1):
                if text[-k:] == merged[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'left'
                        best_text = text[:-k]
                    break

        if best_bi is not None:
            used.add(best_bi)
            if best_side == 'right':
                merged += best_text
            else:
                merged = best_text + merged
            changed = True

    if len(used) > len(best_used4):
        best_merged4 = merged
        best_used4 = set(used)
        best_start4 = start_idx

print(f"  Best start: B{best_start4:02d}")
print(f"  Books merged: {len(best_used4)} of {len(decoded_all)}")
print(f"  Merged text length: {len(best_merged4)} chars")
print(f"  Not merged: {sorted(set(range(len(decoded_all))) - best_used4)}")

# 4. Show the best merged text
merged = best_merged if len(best_used) >= len(best_used4) else best_merged4
used = best_used if len(best_used) >= len(best_used4) else best_used4

print(f"\n\n4. FULL MERGED TEXT ({len(used)} books, {len(merged)} chars)")
print("-" * 60)
for i in range(0, len(merged), 70):
    line = merged[i:i+70]
    print(f"  [{i:4d}] {line}")

# 5. Are ALL books identical text (different windows)?
print("\n\n5. BOOK IDENTITY CHECK")
print("-" * 60)

# Check if all books are substrings of the merged text
contained = 0
not_contained = []
for bi in range(len(decoded_all)):
    if decoded_all[bi] in merged:
        contained += 1
    else:
        not_contained.append(bi)

print(f"  Books contained in merged text: {contained}/{len(decoded_all)}")
if not_contained:
    print(f"  NOT contained: {not_contained}")
    for bi in not_contained[:5]:
        print(f"    B{bi:02d}: {decoded_all[bi][:60]}...")
        # Find best partial match
        best_pos = -1
        best_match = 0
        for start in range(len(merged)):
            match_len = 0
            for k in range(min(len(decoded_all[bi]), len(merged) - start)):
                if decoded_all[bi][k] == merged[start + k]:
                    match_len += 1
                else:
                    break
            if match_len > best_match:
                best_match = match_len
                best_pos = start
        print(f"         Best prefix match: {best_match} chars at pos {best_pos}")

# 6. DP Segmentation of the full merged text
print("\n\n6. SEGMENTED NARRATIVE")
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
    'TER',
    'HIET',
    'NGETRAS',
    'GEVMT',
    'DGEDA',
    'TEMDIA',
    'UISEMIV',
    'TEIGN',
    'CHN',
    'SCE',
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

# 7. Each book individually decoded
print("\n\n7. ALL BOOKS DECODED WITH WORD BOUNDARIES")
print("-" * 60)

for bi in range(len(decoded_all)):
    text = decoded_all[bi]
    parts_b, cov_b, tot_b = dp_segment_full(text)
    pct = cov_b * 100 / tot_b if tot_b > 0 else 0

    formatted = ''
    for ptype, ptext in parts_b:
        if ptype == 'W':
            formatted += ptext + ' '
        else:
            formatted += f'[{ptext}]'

    # Only show first line
    print(f"  B{bi:02d} ({pct:4.1f}%): {formatted[:100]}")

# 8. Summary stats
print("\n\n8. UNKNOWN WORD FREQUENCY IN FULL CORPUS")
print("-" * 60)

all_unknowns = Counter()
for bi in range(len(decoded_all)):
    text = decoded_all[bi]
    parts_b, _, _ = dp_segment_full(text)
    for ptype, ptext in parts_b:
        if ptype == '?':
            all_unknowns[ptext] += 1

print(f"  Total unique unknowns: {len(all_unknowns)}")
print(f"\n  Most common unknowns:")
for unk, count in all_unknowns.most_common(30):
    print(f"    '{unk}' x{count}")

print("\n" + "=" * 80)
print("SESSION 10y COMPLETE")
print("=" * 80)
