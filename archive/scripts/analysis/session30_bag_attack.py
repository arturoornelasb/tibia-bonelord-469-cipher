#!/usr/bin/env python3
"""Session 30: Bag-of-letters attack on remaining 3+ char garbled blocks.

For each garbled block, find optimal partition into known German words
allowing I<->E and I<->L letter swaps.
"""
import json, os
from collections import Counter
from itertools import combinations

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json')) as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json')) as f:
    books = json.load(f)

src = open(os.path.join(script_dir, '..', 'core', 'narrative_v3_clean.py')).read()
code_end = src.index("\n# ============================================================\n# RECONSTRUCT")
exec(src[:code_end])

all_text = ''.join(decoded_books)
resolved_text = all_text
for anagram in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved_text = resolved_text.replace(anagram, ANAGRAM_MAP[anagram])

tokens, covered = dp_segment(resolved_text)
total_known = sum(1 for c in resolved_text if c != '?')
print(f"Baseline: {covered}/{total_known} = {covered/total_known*100:.1f}%\n")

# Collect garbled blocks (3+ chars)
garbled_blocks = {}
for i, tok in enumerate(tokens):
    if not tok.startswith('{'):
        continue
    block = tok[1:-1]
    if len(block) < 3:
        continue
    prev = tokens[i-1] if i > 0 else '^'
    nxt = tokens[i+1] if i < len(tokens)-1 else '$'
    if block not in garbled_blocks:
        garbled_blocks[block] = []
    garbled_blocks[block].append((prev, nxt))

def can_form_with_swaps(word_letters, bag_letters, max_swaps=3):
    """Check if word_letters can be formed from bag_letters with I<->E, I<->L swaps."""
    if len(word_letters) != len(bag_letters):
        return False, 0

    wl = sorted(word_letters)
    bl = sorted(bag_letters)

    if wl == bl:
        return True, 0

    # Try swaps
    for n_swaps in range(1, max_swaps + 1):
        for positions in combinations(range(len(wl)), n_swaps):
            for swap_combo in range(2**n_swaps):
                test = list(wl)
                valid = True
                for idx, pos in enumerate(positions):
                    if swap_combo & (1 << idx):
                        if test[pos] == 'I': test[pos] = 'E'
                        elif test[pos] == 'E': test[pos] = 'I'
                        elif test[pos] == 'L': test[pos] = 'I'
                        elif test[pos] == 'I': test[pos] = 'L'
                        else: valid = False
                    else:
                        if test[pos] == 'I': test[pos] = 'L'
                        elif test[pos] == 'L': test[pos] = 'I'
                        elif test[pos] == 'I': test[pos] = 'E'
                        elif test[pos] == 'E': test[pos] = 'I'
                        else: valid = False
                if sorted(test) == bl:
                    return True, n_swaps
    return False, 0

def find_word_partitions(letters, known_set, max_depth=4):
    """Find all ways to partition letter bag into known words."""
    results = []
    bag = sorted(letters)

    def search(remaining, words, depth):
        if not remaining:
            results.append(list(words))
            return
        if depth >= max_depth:
            return
        if len(results) > 100:
            return

        remaining_sorted = sorted(remaining)

        for word in known_set:
            wlen = len(word)
            if wlen < 2 or wlen > len(remaining):
                continue

            # Check if word can be formed from remaining letters (with swaps)
            word_letters = list(word)

            # Try to match word letters against remaining
            # Direct match first
            rem_copy = list(remaining_sorted)
            matched = True
            for c in sorted(word_letters):
                if c in rem_copy:
                    rem_copy.remove(c)
                else:
                    matched = False
                    break

            if matched:
                search(rem_copy, words + [word], depth + 1)

            # Try with I<->E swaps on word
            for swap_from, swap_to in [('I', 'E'), ('E', 'I'), ('I', 'L'), ('L', 'I')]:
                swapped_word = list(word)
                for si in range(len(swapped_word)):
                    if swapped_word[si] == swap_from:
                        swapped_word[si] = swap_to
                        rem_copy = list(remaining_sorted)
                        matched = True
                        for c in sorted(swapped_word):
                            if c in rem_copy:
                                rem_copy.remove(c)
                            else:
                                matched = False
                                break
                        if matched:
                            search(rem_copy, words + [word + f'({swap_from}->{swap_to}@{si})'], depth + 1)
                        swapped_word[si] = swap_from  # restore

    search(list(bag), [], 0)
    return results

print("=" * 70)
print("BAG-OF-LETTERS ATTACK ON 3+ CHAR BLOCKS")
print("=" * 70)

# Sort blocks by impact
scored = []
for block, contexts in garbled_blocks.items():
    impact = len(block) * len(contexts)
    scored.append((impact, block, contexts))
scored.sort(key=lambda x: -x[0])

total_found = 0
new_entries = []

for impact, block, contexts in scored:
    letters = list(block)
    count = len(contexts)

    # Skip blocks that are proper nouns (already in KNOWN)
    if block in KNOWN:
        continue

    partitions = find_word_partitions(letters, KNOWN, max_depth=4)

    # Score partitions by coverage
    best_partition = None
    best_coverage = 0
    for partition in partitions:
        # Calculate coverage: sum of word lengths that are recognized
        cov = sum(len(w.split('(')[0]) for w in partition)  # strip swap notation
        leftover = len(block) - cov
        if cov > best_coverage:
            best_coverage = cov
            best_partition = partition

    # Show results
    ctx_str = f"{contexts[0][0]}|{block}|{contexts[0][1]}"
    if best_partition and best_coverage > 0:
        pct = best_coverage / len(block) * 100
        print(f"\n  {block!r} ({count}x, {impact} chars)")
        print(f"    context: {ctx_str}")
        print(f"    letters: {''.join(sorted(letters))}")
        print(f"    best: {' + '.join(best_partition)} ({best_coverage}/{len(block)} = {pct:.0f}%)")
        if best_coverage == len(block):
            print(f"    ** 100% COVERAGE - CANDIDATE FOR ANAGRAM_MAP **")
            total_found += impact
            # Build the replacement string
            repl_letters = []
            for word in best_partition:
                clean = word.split('(')[0]
                repl_letters.extend(list(clean))
            new_entries.append((block, ''.join(repl_letters), best_partition, count))
        elif pct >= 60:
            print(f"    ** {pct:.0f}% COVERAGE - partial match **")
    elif len(block) >= 5:
        print(f"\n  {block!r} ({count}x, {impact} chars) - NO PARTITION FOUND")
        print(f"    context: {ctx_str}")
        print(f"    letters: {''.join(sorted(letters))}")

print(f"\n{'='*70}")
print(f"SUMMARY")
print(f"{'='*70}")
print(f"100% coverage blocks found: {len(new_entries)}")
print(f"Total recoverable chars: {total_found}")
for block, repl, partition, count in new_entries:
    print(f"  '{block}' -> '{repl}'  # {' + '.join(partition)}, {count}x")
