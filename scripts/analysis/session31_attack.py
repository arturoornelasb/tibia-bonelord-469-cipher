#!/usr/bin/env python3
"""
Session 31: Attack remaining garbled blocks
Goal: Push beyond 94.4% coverage by finding new anagram resolutions
"""

import json, os, sys
from collections import Counter, defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)

# === Replicate the pipeline from narrative_v3_clean.py ===
def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    ic0 = ic_from_counts(Counter(bp0), len(bp0))
    ic1 = ic_from_counts(Counter(bp1), len(bp1))
    return 0 if ic0 > ic1 else 1

DIGIT_SPLITS = {
    2: (34, '0'),    5: (265, '1'),   6: (20, '0'),    8: (137, '7'),
    10: (277, '2'),  11: (137, '0'),  12: (0, '0'),    13: (55, '0'),
    14: (98, '1'),   15: (98, '0'),   18: (4, '0'),    19: (52, '0'),
    20: (5, '1'),    22: (7, '1'),    23: (14, '0'),   24: (47, '8'),
    25: (0, '0'),    29: (151, '1'),  32: (137, '1'),  34: (101, '0'),
    36: (78, '0'),   39: (44, '0'),   42: (91, '2'),   43: (26, '1'),
    45: (23, '7'),   46: (0, '2'),    48: (127, '0'),  49: (97, '1'),
    50: (136, '2'),  52: (0, '4'),    53: (248, '2'),  54: (49, '1'),
    60: (73, '9'),   61: (93, '7'),   64: (58, '4'),   65: (94, '0'),
    68: (4, '0'),
}

# Decode all books
book_pairs = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        split_pos, digit = DIGIT_SPLITS[bidx]
        book = book[:split_pos] + digit + book[split_pos:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

decoded_books = []
for bpairs in book_pairs:
    text = ''.join(v7.get(p, '?') for p in bpairs)
    decoded_books.append(text)

# Import KNOWN and ANAGRAM_MAP by reading and exec-ing just those sections
core_path = os.path.join(script_dir, '..', 'core', 'narrative_v3_clean.py')
with open(core_path, 'r') as f:
    core_source = f.read()

# Extract KNOWN set
known_start = core_source.index("KNOWN = set([")
known_end = core_source.index("])", known_start) + 2
exec(core_source[known_start:known_end])

# Extract ANAGRAM_MAP
map_start = core_source.index("ANAGRAM_MAP = {")
map_end = core_source.index("\n}", map_start) + 2
exec(core_source[map_start:map_end])

# DP word segmentation
def dp_segment(text):
    n = len(text)
    dp = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], None)
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if cand in KNOWN:
                score = dp[start][0] + wlen
                if score > dp[i][0]:
                    dp[i] = (score, (start, cand))
    tokens = []
    i = n
    while i > 0:
        if dp[i][1] is not None:
            start, word = dp[i][1]
            tokens.append(('W', word))
            i = start
        else:
            tokens.append(('C', text[i-1]))
            i -= 1
    tokens.reverse()
    result = []
    for kind, val in tokens:
        if kind == 'W':
            result.append(val)
        else:
            if result and result[-1].startswith('{'):
                result[-1] = result[-1][:-1] + val + '}'
            else:
                result.append('{' + val + '}')
    return result, dp[n][0]

# Build resolved text
all_text = ''.join(decoded_books)
resolved_text = all_text
for anagram in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved_text = resolved_text.replace(anagram, ANAGRAM_MAP[anagram])
resolved_text = resolved_text.replace('TREUUNR', 'TREUNUR')

tokens, covered = dp_segment(resolved_text)
total_known = sum(1 for c in resolved_text if c != '?')

print("=" * 70)
print("SESSION 31: GARBLED BLOCK ANALYSIS")
print("=" * 70)
print(f"Current coverage: {covered}/{total_known} = {covered/total_known*100:.1f}%")

# === Extract garbled blocks with context ===
garbled_blocks = []
for i, tok in enumerate(tokens):
    if tok.startswith('{') and tok.endswith('}'):
        block = tok[1:-1]
        left_ctx = ' '.join(tokens[max(0,i-3):i])
        right_ctx = ' '.join(tokens[i+1:min(len(tokens),i+4)])
        garbled_blocks.append((block, left_ctx, right_ctx, i))

block_contexts = defaultdict(list)
for block, left, right, idx in garbled_blocks:
    block_contexts[block].append((left, right))

# === BoLWP ===
GERMAN_WORDS = set()
GERMAN_WORDS.update(KNOWN)
# Add more MHG/German candidates
GERMAN_WORDS.update([
    'WIRT', 'STAT', 'STETE', 'LEIT', 'RECHT', 'STERN', 'NACHT',
    'GAST', 'STILL', 'LISTE', 'RITTER', 'HERZE', 'KLAGE', 'MUOT',
    'SCHULD', 'SEGEN', 'FLUCH', 'RACHE', 'HALTE', 'STEIN', 'HALTEN',
    'STELLE', 'STARK', 'EWIGE', 'EWIG', 'LEID', 'GEBOT', 'SCHWUR',
    'RICHTER', 'HELDIN', 'SCHAR', 'STATT', 'GRAB', 'GRABEN',
    'TROST', 'GERECHT', 'TREUE', 'EHREN', 'EIGEN', 'SCHLAG',
    'SCHLECHT', 'SONDER', 'WENIG', 'EDELE',
    # Short MHG
    'LE', 'RE', 'GE', 'ST', 'EL', 'TS', 'RS', 'CH', 'TR',
    'DO', 'GO', 'LO', 'RO', 'TO',
    # Potential new resolutions
    'ORTS', 'TROST', 'SORGE', 'SORGEN', 'STOLZ',
    'SCHAR', 'RECHT', 'SCHLOSS', 'GARTEN',
])

def can_form_with_swaps(bag_remaining, word, max_swaps):
    needed = Counter(word)
    swaps = 0
    temp_bag = Counter(bag_remaining)
    for letter, count in needed.items():
        have = temp_bag.get(letter, 0)
        if have >= count:
            temp_bag[letter] -= count
            continue
        deficit = count - have
        if letter == 'E' and temp_bag.get('I', 0) >= deficit:
            temp_bag['I'] -= deficit
            swaps += deficit
        elif letter == 'I' and temp_bag.get('E', 0) >= deficit:
            temp_bag['E'] -= deficit
            swaps += deficit
        elif letter == 'L' and temp_bag.get('I', 0) >= deficit:
            temp_bag['I'] -= deficit
            swaps += deficit
        elif letter == 'I' and temp_bag.get('L', 0) >= deficit:
            temp_bag['L'] -= deficit
            swaps += deficit
        else:
            return False, 0, {}
    if swaps > max_swaps:
        return False, 0, {}
    return True, swaps, dict(temp_bag)

def bolwp(garbled, dictionary, max_swaps=3):
    bag = Counter(garbled)
    n = len(garbled)
    best = {'coverage': 0, 'words': [], 'swaps': 0}
    candidates = sorted([w for w in dictionary if 2 <= len(w) <= n], key=len, reverse=True)

    def search(remaining_bag, remaining_len, words, swaps_used, depth=0):
        cov = sum(len(w) for w in words)
        if cov > best['coverage']:
            best['coverage'] = cov
            best['words'] = words[:]
            best['swaps'] = swaps_used
        if remaining_len == 0 or depth > 4:
            return
        for w in candidates:
            if len(w) > remaining_len:
                continue
            ok, sw, new_bag = can_form_with_swaps(remaining_bag, w, max_swaps - swaps_used)
            if ok:
                search(new_bag, remaining_len - len(w), words + [w], swaps_used + sw, depth + 1)

    search(bag, n, [], 0)
    return best

# === Analyze multi-char blocks ===
print(f"\n{'=' * 70}")
print("BOLWP ON MULTI-CHAR GARBLED BLOCKS (>= 2 chars)")
print(f"{'=' * 70}")

sorted_blocks = sorted(block_contexts.items(),
                       key=lambda x: len(x[0]) * len(x[1]), reverse=True)

total_potential = 0
new_resolutions = []

for block, contexts in sorted_blocks:
    if len(block) < 2 or '?' in block:
        continue
    freq = len(contexts)

    result = bolwp(block, GERMAN_WORDS, max_swaps=3)

    if result['coverage'] > 0 and result['coverage'] >= max(len(block) * 0.5, 2):
        new_chars = result['coverage']
        # Only count chars that aren't already covered by KNOWN matches
        # The garbled block means these chars are ALL uncovered
        gain = new_chars * freq
        total_potential += gain

        print(f"\n  {{{block}}} ({len(block)} chars, {freq}x)")
        ctx = contexts[0]
        print(f"    ...{ctx[0][-35:]} [{block}] {ctx[1][:35]}...")
        print(f"    -> {'+'.join(result['words'])} ({result['coverage']}/{len(block)}, {result['swaps']} swaps)")
        print(f"    Gain: +{gain}")
        new_resolutions.append((block, result, freq))

# === Look for cross-boundary absorptions ===
print(f"\n{'=' * 70}")
print("CROSS-BOUNDARY PATTERN ANALYSIS")
print(f"{'=' * 70}")

# Find {X}WORD or WORD{X} where X+WORD or WORD+X forms a known word
cross_boundary = []
for i, tok in enumerate(tokens):
    if not tok.startswith('{'):
        continue
    block = tok[1:-1]
    if len(block) > 3:
        continue

    # Try block + next_word
    if i + 1 < len(tokens) and not tokens[i+1].startswith('{'):
        combo = block + tokens[i+1]
        if combo in GERMAN_WORDS:
            cross_boundary.append(('prepend', block, tokens[i+1], combo, i))
        # Also try anagram of combo
        for w in GERMAN_WORDS:
            if len(w) == len(combo) and Counter(w) == Counter(combo):
                if w != combo:
                    cross_boundary.append(('prepend+anagram', block, tokens[i+1], w, i))
                    break

    # Try prev_word + block
    if i - 1 >= 0 and not tokens[i-1].startswith('{'):
        combo = tokens[i-1] + block
        if combo in GERMAN_WORDS:
            cross_boundary.append(('append', tokens[i-1], block, combo, i))

seen = set()
for kind, a, b, result, idx in cross_boundary:
    key = (kind, a, b, result)
    if key not in seen:
        seen.add(key)
        left = ' '.join(tokens[max(0,idx-2):idx])
        right = ' '.join(tokens[idx+1:min(len(tokens),idx+3)])
        print(f"  {kind}: {a} + {b} = {result}   (ctx: ...{left} [{a}+{b}] {right}...)")

# === Summary ===
print(f"\n{'=' * 70}")
print("SUMMARY")
print(f"{'=' * 70}")
print(f"Current:   {covered}/{total_known} = {covered/total_known*100:.1f}%")
print(f"Potential: +{total_potential} chars from BoLWP resolutions")
proj = covered + total_potential
print(f"Projected: {proj}/{total_known} = {proj/total_known*100:.1f}%")
print(f"\nNew resolution candidates: {len(new_resolutions)}")
for block, result, freq in new_resolutions:
    print(f"  {block} -> {'+'.join(result['words'])} ({freq}x, +{result['coverage']*freq})")
