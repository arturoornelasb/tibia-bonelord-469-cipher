#!/usr/bin/env python3
"""Session 12h: Multi-chain assembly - merge all chains into one superstring"""

import json, re
from collections import Counter, defaultdict

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

# Trim odd-length books
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
print("SESSION 12h: MULTI-CHAIN ASSEMBLY")
print("=" * 80)

# Strategy: instead of greedy from one book, assemble ALL chains first,
# then merge the chain-superstrings together

# 1. Build overlap graph
overlaps = {}
for i in range(len(corrected)):
    for j in range(len(corrected)):
        if i == j: continue
        si = corrected[i]
        sj = corrected[j]
        for k in range(min(len(si), len(sj)), 3, -2):
            if si[-k:] == sj[:k]:
                overlaps[(i,j)] = k // 2
                break

# 2. Build chains by following best successors
# Use MUTUAL best: i's best successor must have i as best predecessor
best_succ = {}
best_pred = {}
for (i,j), ov in overlaps.items():
    if i not in best_succ or ov > best_succ[i][1]:
        best_succ[i] = (j, ov)
    if j not in best_pred or ov > best_pred[j][1]:
        best_pred[j] = (i, ov)

# Build mutual chains
used = set()
chains = []
for start in range(len(corrected)):
    if start in used: continue
    # Walk backward to find actual start
    current = start
    while current in best_pred:
        pred, ov = best_pred[current]
        if pred in used: break
        if pred in best_succ and best_succ[pred][0] == current:
            current = pred
        else:
            break
        if current == start: break  # cycle

    # Now walk forward building chain
    if current in used: continue
    chain = [current]
    used.add(current)
    while current in best_succ:
        nxt, ov = best_succ[current]
        if nxt in used: break
        if nxt in best_pred and best_pred[nxt][0] == current:
            chain.append(nxt)
            used.add(nxt)
            current = nxt
        else:
            break

    chains.append(chain)

chains.sort(key=len, reverse=True)
print(f"\n1. CHAINS FOUND: {len(chains)}")
print("-" * 60)
for ci, chain in enumerate(chains[:15]):
    ids = [f"B{bi:02d}" for bi in chain]
    print(f"  Chain {ci} ({len(chain)} books): {' -> '.join(ids)}")

# 3. Assemble each chain into its own superstring
print(f"\n2. ASSEMBLING CHAINS")
print("-" * 60)

chain_strings = []
for ci, chain in enumerate(chains):
    super_s = corrected[chain[0]]
    for idx in range(1, len(chain)):
        bi = chain[idx]
        prev = chain[idx-1]
        ov = overlaps.get((prev, bi), 0) * 2  # in digits
        super_s += corrected[bi][ov:]
    chain_strings.append(super_s)
    decoded = collapse(decode_str(super_s))
    if len(chain) > 1:
        print(f"  Chain {ci}: {len(chain)} books, {len(super_s)//2} codes, {len(decoded)} collapsed chars")

# 4. Now merge chain-superstrings together
print(f"\n3. MERGING CHAINS")
print("-" * 60)

# Start with longest chain-superstring and greedily add others
merged = chain_strings[0]
used_chains = {0}

changed = True
iterations = 0
while changed:
    changed = False
    iterations += 1
    best_ci = None
    best_ov = 0
    best_side = None
    best_new = ''

    for ci in range(len(chain_strings)):
        if ci in used_chains: continue
        text = chain_strings[ci]

        # Right
        for k in range(min(len(merged), len(text)), 3, -2):
            if merged[-k:] == text[:k]:
                if k > best_ov:
                    best_ov = k
                    best_ci = ci
                    best_side = 'right'
                    best_new = text[k:]
                break
        # Left
        for k in range(min(len(merged), len(text)), 3, -2):
            if text[-k:] == merged[:k]:
                if k > best_ov:
                    best_ov = k
                    best_ci = ci
                    best_side = 'left'
                    best_new = text[:-k]
                break

    if best_ci is not None and best_ov >= 4:
        used_chains.add(best_ci)
        if best_side == 'right':
            merged += best_new
        else:
            merged = best_new + merged
        print(f"  Merged chain {best_ci} ({best_side}, {best_ov//2} codes overlap)")
        changed = True

print(f"\n  Total chains merged: {len(used_chains)}/{len(chains)}")
print(f"  Final superstring: {len(merged)//2} codes")

# Check containment
contained = set()
for bi in range(len(corrected)):
    if corrected[bi] in merged:
        contained.add(bi)
print(f"  Books contained: {len(contained)}/{len(corrected)}")
missing = sorted(set(range(len(corrected))) - contained)
print(f"  Still missing: {missing}")

# 5. Full decoded text
decoded = collapse(decode_str(merged))
print(f"\n4. FULL NARRATIVE ({len(decoded)} chars)")
print("-" * 60)
for i in range(0, len(decoded), 70):
    print(f"  [{i:4d}] {decoded[i:i+70]}")

# 6. DP Segment the full narrative
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
    'TER', 'HIET', 'DU', 'HAT', 'BIS', 'SINE',
    'STEINE', 'RUNEN', 'EHRE', 'NIDEN',
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

parts, covered, total = dp_segment(decoded)
print(f"\n5. SEGMENTED NARRATIVE")
print("-" * 60)
print(f"  Coverage: {covered}/{total} = {covered*100/total:.1f}%\n")

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

# 7. Try a TRANSLATION of the readable parts
print(f"\n6. NARRATIVE TRANSLATION ATTEMPT")
print("-" * 60)

# Extract just the readable words in sequence
readable = []
for ptype, ptext in parts:
    if ptype == 'W':
        readable.append(ptext)
    else:
        readable.append(f'_{ptext}_')

# Group into sentences (split at proper nouns or major markers)
sentences = ' '.join(readable)
print(f"  Full readable text:")
for i in range(0, len(sentences), 70):
    print(f"    {sentences[i:i+70]}")

print("\n" + "=" * 80)
print("SESSION 12h COMPLETE")
print("=" * 80)
