#!/usr/bin/env python3
"""Session 30: Inventory of remaining garbled blocks after DIGIT_SPLIT optimization."""
import json, os, re
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json')) as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json')) as f:
    books = json.load(f)

# Load pipeline components from narrative_v3_clean.py
src = open(os.path.join(script_dir, '..', 'core', 'narrative_v3_clean.py')).read()

# Extract all data structures and functions
# Extract DIGIT_SPLITS, ic, get_offset, book decoding, KNOWN, dp_segment, ANAGRAM_MAP
# Split at the section that starts the output (after ANAGRAM_MAP closing brace)
code_end = src.index("\n# ============================================================\n# RECONSTRUCT")
exec(src[:code_end])

# Concatenate and resolve
all_text = ''.join(decoded_books)
resolved_text = all_text
for anagram in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved_text = resolved_text.replace(anagram, ANAGRAM_MAP[anagram])

tokens, covered = dp_segment(resolved_text)
total_known = sum(1 for c in resolved_text if c != '?')
print(f"Coverage: {covered}/{total_known} = {covered/total_known*100:.1f}%")

# Extract garbled blocks with context
garbled = []
for i, tok in enumerate(tokens):
    if tok.startswith('{'):
        block = tok[1:-1]
        prev = tokens[i-1] if i > 0 else '^'
        nxt = tokens[i+1] if i < len(tokens)-1 else '$'
        garbled.append((block, prev, nxt))

# Count and categorize
block_counts = Counter(b for b, _, _ in garbled)
total_garbled = sum(len(v)*c for v, c in block_counts.items())
print(f"Total garbled: {total_garbled} chars in {len(garbled)} blocks ({len(block_counts)} unique)")

# By length category
for maxlen, label in [(1, '1-char'), (2, '2-char'), (99, '3+ char')]:
    minlen = {1: 1, 2: 2, 99: 3}[maxlen]
    chars = sum(len(v)*c for v, c in block_counts.items() if minlen <= len(v) <= maxlen)
    instances = sum(c for v, c in block_counts.items() if minlen <= len(v) <= maxlen)
    print(f"  {label}: {instances} instances, {chars} chars")

# All blocks sorted by impact
print(f"\nAll garbled blocks (by total char impact):")
scored = [(len(v)*c, v, c) for v, c in block_counts.items()]
scored.sort(key=lambda x: -x[0])
for impact, block, count in scored:
    # Get all contexts
    contexts = [(p, n) for b, p, n in garbled if b == block]
    ctx_strs = [f"{p}|{block}|{n}" for p, n in contexts[:3]]
    print(f"  {impact:3d} chars: {block!r:20s} ({count}x)  {' // '.join(ctx_strs)}")

# Focus: multi-char blocks that could be words
print(f"\n{'='*70}")
print("ACTIONABLE BLOCKS (3+ chars, potential words)")
print(f"{'='*70}")
for impact, block, count in scored:
    if len(block) < 3:
        continue
    contexts = [(p, n) for b, p, n in garbled if b == block]
    # Try simple anagram check
    from itertools import permutations
    letters = sorted(block)
    print(f"\n  {block!r} ({count}x, {impact} chars, letters: {''.join(letters)})")
    for p, n in contexts:
        print(f"    context: {p} |{block}| {n}")

    # Check if any known word can be formed from these letters (with I<->E, I<->L swaps)
    matches = []
    for word in KNOWN:
        if len(word) != len(block):
            continue
        wl = sorted(word)
        bl = list(letters)
        # Try direct match
        if wl == bl:
            matches.append(('exact', word))
            continue
        # Try with I<->E swaps
        for swaps in range(1, 4):
            found = False
            from itertools import combinations
            for swap_positions in combinations(range(len(wl)), swaps):
                test_wl = list(wl)
                for sp in swap_positions:
                    if test_wl[sp] == 'I':
                        test_wl[sp] = 'E'
                    elif test_wl[sp] == 'E':
                        test_wl[sp] = 'I'
                    elif test_wl[sp] == 'L':
                        test_wl[sp] = 'I'
                if sorted(test_wl) == bl:
                    matches.append((f'{swaps}-swap', word))
                    found = True
                    break
            if found:
                break

    if matches:
        print(f"    MATCHES: {matches}")
