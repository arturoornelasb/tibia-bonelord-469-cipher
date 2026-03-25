#!/usr/bin/env python3
"""Session 12b: Deep narrative analysis + word boundary re-segmentation"""

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

# Word list from session 12a
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
    'DU', 'HAT', 'BIS', 'SINE',
    'STEINE', 'RUNEN', 'EHRE',
    'UM', 'AM', 'AB', 'ZU', 'BI',
    'ALT', 'NEU', 'DIR', 'MAN',
    # Add more based on 12a analysis
    'NIDEN',  # MHG "niden" = below/beneath
]
german_words = list(dict.fromkeys(german_words))
word_scores = {w: len(w) * 3 for w in german_words}
all_words = sorted(word_scores.keys(), key=len, reverse=True)

all_collapsed = [collapse(decode(b)) for b in books]

print("=" * 80)
print("SESSION 12b: DEEP NARRATIVE ANALYSIS")
print("=" * 80)

# 1. Build the full narrative by finding the reading order
# Using the overlap data to chain books together
print("\n1. FINDING READING ORDER")
print("-" * 60)

# Build overlap matrix
overlaps = {}
for i in range(len(all_collapsed)):
    for j in range(len(all_collapsed)):
        if i == j: continue
        ti = all_collapsed[i]
        tj = all_collapsed[j]
        for k in range(min(len(ti), len(tj)), 2, -1):
            if ti[-k:] == tj[:k]:
                overlaps[(i,j)] = k
                break

# For each book, find best predecessor and best successor
best_pred = {}
best_succ = {}
for (i,j), ov in overlaps.items():
    if j not in best_pred or ov > best_pred[j][1]:
        best_pred[j] = (i, ov)
    if i not in best_succ or ov > best_succ[i][1]:
        best_succ[i] = (j, ov)

# Find books that start chains (no predecessor)
chain_starts = []
for bi in range(len(all_collapsed)):
    if bi not in best_pred:
        chain_starts.append(bi)

# Build chains from each start
chains = []
for start in chain_starts:
    chain = [start]
    visited = {start}
    current = start
    while current in best_succ:
        nxt, ov = best_succ[current]
        if nxt in visited: break
        chain.append(nxt)
        visited.add(nxt)
        current = nxt
    chains.append(chain)

chains.sort(key=len, reverse=True)

print(f"  Chain starts (no predecessor): {len(chain_starts)}")
print(f"  Books with overlaps: {len(set(i for i,j in overlaps.keys()) | set(j for i,j in overlaps.keys()))}")
print(f"  Books WITHOUT any overlap: {70 - len(set(i for i,j in overlaps.keys()) | set(j for i,j in overlaps.keys()))}")
print(f"  Longest chains: {[len(c) for c in chains[:10]]}")

# 2. Show the full narrative text from longest chain
if chains:
    main_chain = chains[0]
    print(f"\n  Main chain ({len(main_chain)} books): {main_chain}")

    # Build narrative from chain
    narrative = all_collapsed[main_chain[0]]
    for idx in range(1, len(main_chain)):
        bi = main_chain[idx]
        prev = main_chain[idx-1]
        key = (prev, bi)
        ov = overlaps.get(key, 0)
        narrative += all_collapsed[bi][ov:]

    print(f"  Narrative length: {len(narrative)} chars")

# 3. Show ALL books as text, position them in the narrative
print(f"\n2. ALL BOOKS AS DECODED TEXT")
print("-" * 60)

# Sort books by content to find natural reading order
# Use first 20 chars as sort key to group similar starts
for bi in range(len(all_collapsed)):
    text = all_collapsed[bi]
    print(f"  B{bi:02d} ({len(text):3d}): {text[:80]}")

# 4. Find the FULL continuous text
# Since books are windows, find the unique text by overlap merging
print(f"\n3. GREEDY MERGE - ALL STARTING POINTS")
print("-" * 60)

best_merged = ''
best_used = set()
best_start = -1
best_order = []

for start_idx in range(len(all_collapsed)):
    merged = all_collapsed[start_idx]
    used = {start_idx}
    order = [start_idx]

    changed = True
    while changed:
        changed = False
        best_bi = None
        best_ov = 0
        best_side = None
        best_new_text = ''

        for bi in range(len(all_collapsed)):
            if bi in used: continue
            text = all_collapsed[bi]

            # Right append
            for k in range(min(len(merged), len(text)), 2, -1):
                if merged[-k:] == text[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'right'
                        best_new_text = text[k:]
                    break

            # Left prepend
            for k in range(min(len(merged), len(text)), 2, -1):
                if text[-k:] == merged[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'left'
                        best_new_text = text[:-k]
                    break

        if best_bi is not None and best_ov >= 3:
            used.add(best_bi)
            order.append(best_bi)
            if best_side == 'right':
                merged += best_new_text
            else:
                merged = best_new_text + merged
            changed = True

    if len(used) > len(best_used):
        best_merged = merged
        best_used = set(used)
        best_start = start_idx
        best_order = list(order)

print(f"  Best start: B{best_start:02d}")
print(f"  Books merged: {len(best_used)}/{len(all_collapsed)}")
print(f"  Merge order: {best_order}")
print(f"  Merged text length: {len(best_merged)} chars")
print(f"  NOT merged: {sorted(set(range(len(all_collapsed))) - best_used)}")

# 5. Show full merged text with line breaks
print(f"\n4. FULL MERGED TEXT")
print("-" * 60)
for i in range(0, len(best_merged), 70):
    line = best_merged[i:i+70]
    print(f"  [{i:4d}] {line}")

# 6. DP segment the full merged text
print(f"\n5. SEGMENTED FULL TEXT")
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

parts, covered, total = dp_segment(best_merged)
print(f"  Coverage: {covered}/{total} = {covered*100/total:.1f}%")

# Format as readable narrative with numbered lines
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

# 7. Try to read each unknown segment with context
print(f"\n6. UNKNOWN SEGMENTS IN CONTEXT")
print("-" * 60)

# Merge consecutive unknowns for context analysis
merged_parts = []
for ptype, ptext in parts:
    if ptype == '?' and merged_parts and merged_parts[-1][0] == '?':
        merged_parts[-1] = ('?', merged_parts[-1][1] + ptext)
    else:
        merged_parts.append((ptype, ptext))

# Show each unknown with surrounding words
for idx, (ptype, ptext) in enumerate(merged_parts):
    if ptype == '?' and len(ptext) >= 2:
        # Get surrounding context
        before_words = []
        for j in range(idx-1, max(-1, idx-4), -1):
            if merged_parts[j][0] == 'W':
                before_words.insert(0, merged_parts[j][1])
            else:
                before_words.insert(0, f'[{merged_parts[j][1]}]')
        after_words = []
        for j in range(idx+1, min(len(merged_parts), idx+4)):
            if merged_parts[j][0] == 'W':
                after_words.append(merged_parts[j][1])
            else:
                after_words.append(f'[{merged_parts[j][1]}]')

        before = ' '.join(before_words)
        after = ' '.join(after_words)
        print(f"  ...{before} [{ptext}] {after}...")

# 8. Analyze the narrative structure - find clauses
print(f"\n7. CLAUSE STRUCTURE")
print("-" * 60)

# The text seems to repeat - find the period/cycle
# Look for "HIER TAUTR" as a clear narrative marker
marker = 'HIERTAUTR'
positions = []
for i in range(len(best_merged)):
    if best_merged[i:i+len(marker)] == marker:
        positions.append(i)

print(f"  '{marker}' appears at positions: {positions}")
if len(positions) >= 2:
    print(f"  Cycle length estimate: {positions[1] - positions[0]}")

# Find all instances of key phrases in full merged text
key_phrases = ['HIERTAUTR', 'SEIGEVMT', 'DGEDASIE', 'SONGETRAS',
               'INHEDEMI', 'ERLABRNIWIR', 'DIEURALTE',
               'ORTENGCHD', 'KOENIGLABGZERAS', 'OWIRUNE',
               'STEIENGEH']
for phrase in key_phrases:
    positions = []
    pos = 0
    while True:
        idx = best_merged.find(phrase, pos)
        if idx < 0: break
        positions.append(idx)
        pos = idx + 1
    if positions:
        print(f"  {phrase}: at {positions}")

# 9. Extract the UNIQUE narrative (one cycle if it repeats)
print(f"\n8. UNIQUE NARRATIVE CONTENT")
print("-" * 60)

# Check if the text is cyclic
text = best_merged
for cycle_len in range(50, len(text)//2 + 1):
    matches = 0
    for i in range(min(cycle_len, len(text) - cycle_len)):
        if text[i] == text[i + cycle_len]:
            matches += 1
    match_pct = matches * 100 / cycle_len if cycle_len > 0 else 0
    if match_pct > 90:
        print(f"  CYCLIC! Period ~{cycle_len} chars ({match_pct:.1f}% match)")
        # Show the core cycle
        core = text[:cycle_len]
        print(f"  Core text ({len(core)} chars):")
        for i in range(0, len(core), 70):
            print(f"    [{i:4d}] {core[i:i+70]}")
        break
else:
    print(f"  Text does not appear cyclic (tested up to {len(text)//2})")
    print(f"  Full unique text: {len(text)} chars")

print("\n" + "=" * 80)
print("SESSION 12b COMPLETE")
print("=" * 80)
