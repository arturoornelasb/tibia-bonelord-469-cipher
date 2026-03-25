#!/usr/bin/env python3
"""Session 12g: Deep superstring analysis - find the FULL continuous narrative"""

import json, re
from collections import Counter, defaultdict

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

# CRITICAL: Trim odd-length books
corrected = []
for book_str in raw_books:
    if len(book_str) % 2 != 0:
        corrected.append(book_str[:-1])
    else:
        corrected.append(book_str)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]
def decode(codes, m=None):
    if m is None: m = mapping
    return ''.join(m.get(c, '?') for c in codes)
def collapse(s):
    return re.sub(r'(.)\1+', r'\1', s)

books = [parse_codes(s) for s in corrected]

print("=" * 80)
print("SESSION 12g: FULL NARRATIVE ASSEMBLY")
print("=" * 80)

# 1. Build a COMPLETE overlap graph
# Instead of just edge overlaps, find the LONGEST common suffix/prefix for ALL pairs
print("\n1. COMPLETE OVERLAP GRAPH")
print("-" * 60)

overlaps = {}  # (i,j) -> overlap length in codes
for i in range(len(books)):
    for j in range(len(books)):
        if i == j: continue
        si = corrected[i]
        sj = corrected[j]
        # Find longest k such that si ends with sj's first k digits
        for k in range(min(len(si), len(sj)), 1, -2):
            if si[-k:] == sj[:k]:
                overlaps[(i,j)] = k // 2  # in codes
                break

# Find the best successor and predecessor for each book
best_succ = {}
best_pred = {}
for (i,j), ov in overlaps.items():
    if i not in best_succ or ov > best_succ[i][1]:
        best_succ[i] = (j, ov)
    if j not in best_pred or ov > best_pred[j][1]:
        best_pred[j] = (i, ov)

print(f"  Total overlapping pairs: {len(overlaps)}")
print(f"  Books with a successor: {len(best_succ)}")
print(f"  Books with a predecessor: {len(best_pred)}")

# 2. Build chains using best successors
print("\n2. SUCCESSOR CHAINS")
print("-" * 60)

# Find chain starts (books with no predecessor or whose predecessor points elsewhere)
all_books = set(range(len(books)))
has_pred = set()
for j, (i, ov) in best_pred.items():
    # j has predecessor i, but only if i's best successor is j
    if i in best_succ and best_succ[i][0] == j:
        has_pred.add(j)

chain_starts = all_books - has_pred
print(f"  Chain starts: {len(chain_starts)}: {sorted(chain_starts)}")

chains = []
used_in_chain = set()
for start in sorted(chain_starts, key=lambda x: -len(books[x])):
    if start in used_in_chain: continue
    chain = [(start, 0)]  # (book_index, overlap_with_prev)
    used_in_chain.add(start)
    current = start
    while current in best_succ:
        nxt, ov = best_succ[current]
        if nxt in used_in_chain: break
        # Also check that nxt's best predecessor is current
        if nxt in best_pred and best_pred[nxt][0] == current:
            chain.append((nxt, ov))
            used_in_chain.add(nxt)
            current = nxt
        else:
            break
    chains.append(chain)

chains.sort(key=len, reverse=True)
print(f"\n  Top chains:")
for ci, chain in enumerate(chains[:10]):
    book_ids = [f"B{bi:02d}" for bi, _ in chain]
    overlaps_str = [str(ov) for _, ov in chain]
    total_codes = sum(len(books[bi]) for bi, _ in chain) - sum(ov for _, ov in chain)
    print(f"    Chain {ci}: {' -> '.join(book_ids)} ({len(chain)} books, ~{total_codes} unique codes)")

# 3. Assemble the longest chain
print("\n3. LONGEST CHAIN ASSEMBLY")
print("-" * 60)

main_chain = chains[0]
superstring = corrected[main_chain[0][0]]
for bi, ov in main_chain[1:]:
    superstring += corrected[bi][ov*2:]

print(f"  Chain length: {len(main_chain)} books")
print(f"  Superstring: {len(superstring)//2} codes")

# Now try to extend this superstring with remaining books
# by checking if any unassembled book overlaps
remaining = set(range(len(books))) - set(bi for bi, _ in main_chain)
print(f"  Remaining books: {len(remaining)}")

# Try to add remaining books
changed = True
while changed:
    changed = False
    best_bi = None
    best_ov = 0
    best_side = None
    best_new = ''

    for bi in list(remaining):
        text = corrected[bi]
        # Right append
        for k in range(min(len(superstring), len(text)), 3, -2):
            if superstring[-k:] == text[:k]:
                if k > best_ov:
                    best_ov = k
                    best_bi = bi
                    best_side = 'right'
                    best_new = text[k:]
                break
        # Left prepend
        for k in range(min(len(superstring), len(text)), 3, -2):
            if text[-k:] == superstring[:k]:
                if k > best_ov:
                    best_ov = k
                    best_bi = bi
                    best_side = 'left'
                    best_new = text[:-k]
                break

    if best_bi is not None and best_ov >= 4:
        remaining.remove(best_bi)
        if best_side == 'right':
            superstring += best_new
        else:
            superstring = best_new + superstring
        changed = True

print(f"  After extension: {len(superstring)//2} codes")
print(f"  Books remaining: {len(remaining)}")

# Check containment
contained = set()
for bi in range(len(books)):
    if corrected[bi] in superstring:
        contained.add(bi)
print(f"  Books contained in superstring: {len(contained)}/{len(books)}")
still_missing = sorted(set(range(len(books))) - contained)
print(f"  Still missing: {still_missing}")

# 4. Decode the superstring
print("\n4. DECODED SUPERSTRING")
print("-" * 60)

super_codes = parse_codes(superstring)
decoded_super = decode(super_codes)
collapsed_super = collapse(decoded_super)
print(f"  Codes: {len(super_codes)}")
print(f"  Decoded: {len(decoded_super)} chars")
print(f"  Collapsed: {len(collapsed_super)} chars")
print()
for i in range(0, len(collapsed_super), 70):
    print(f"  [{i:4d}] {collapsed_super[i:i+70]}")

# 5. For missing books, check what text they contain
print("\n5. MISSING BOOKS ANALYSIS")
print("-" * 60)

for bi in still_missing[:20]:
    text = collapse(decode(books[bi]))
    # Check how much of this text is in the collapsed superstring
    in_super = 0
    for k in range(len(text), 0, -1):
        if text[:k] in collapsed_super:
            in_super = k
            break
    print(f"  B{bi:02d} ({len(text)} chars): prefix in super = {in_super}")
    print(f"    Text: {text[:70]}...")

# 6. Are the missing books from a DIFFERENT part of the narrative?
# Check if they overlap with each other
print("\n6. OVERLAPS AMONG MISSING BOOKS")
print("-" * 60)

missing_overlaps = {}
for i in still_missing:
    for j in still_missing:
        if i == j: continue
        si = corrected[i]
        sj = corrected[j]
        for k in range(min(len(si), len(sj)), 3, -2):
            if si[-k:] == sj[:k]:
                missing_overlaps[(i,j)] = k // 2
                break

if missing_overlaps:
    print(f"  Overlaps among missing books: {len(missing_overlaps)}")
    for (i,j), ov in sorted(missing_overlaps.items(), key=lambda x: -x[1])[:10]:
        print(f"    B{i:02d} -> B{j:02d}: {ov} codes")

    # Try to assemble missing books into their own superstring
    missing_best = ''
    missing_used = set()
    for start in still_missing:
        merged = corrected[start]
        used = {start}
        changed = True
        while changed:
            changed = False
            bst_bi = None
            bst_ov = 0
            bst_side = None
            bst_new = ''
            for bi in still_missing:
                if bi in used: continue
                text = corrected[bi]
                for k in range(min(len(merged), len(text)), 3, -2):
                    if merged[-k:] == text[:k]:
                        if k > bst_ov:
                            bst_ov = k
                            bst_bi = bi
                            bst_side = 'right'
                            bst_new = text[k:]
                        break
                for k in range(min(len(merged), len(text)), 3, -2):
                    if text[-k:] == merged[:k]:
                        if k > bst_ov:
                            bst_ov = k
                            bst_bi = bi
                            bst_side = 'left'
                            bst_new = text[:-k]
                        break
            if bst_bi is not None and bst_ov >= 4:
                used.add(bst_bi)
                if bst_side == 'right':
                    merged += bst_new
                else:
                    merged = bst_new + merged
                changed = True
        if len(used) > len(missing_used):
            missing_best = merged
            missing_used = set(used)

    print(f"\n  Missing books assembled: {len(missing_used)} of {len(still_missing)}")
    if missing_best:
        mc = parse_codes(missing_best)
        md = decode(mc)
        mc_col = collapse(md)
        print(f"  Missing superstring: {len(mc_col)} chars collapsed")
        for i in range(0, min(350, len(mc_col)), 70):
            print(f"    [{i:4d}] {mc_col[i:i+70]}")
else:
    print("  No overlaps among missing books")

# 7. Check if the narrative is CIRCULAR
print("\n7. CIRCULAR CHECK")
print("-" * 60)

# Check if the superstring's end overlaps with its beginning
for k in range(min(200, len(superstring)//2), 3, -2):
    if superstring[-k:] == superstring[:k]:
        print(f"  CIRCULAR! Overlap of {k//2} codes at ends")
        print(f"  Overlap text: {collapse(decode(parse_codes(superstring[:k])))}")
        break
else:
    # Check at collapsed text level
    for k in range(min(100, len(collapsed_super)), 3, -1):
        if collapsed_super[-k:] == collapsed_super[:k]:
            print(f"  Circular at TEXT level! Overlap of {k} chars")
            print(f"  Overlap: {collapsed_super[:k]}")
            break
    else:
        print("  Not circular")

print("\n" + "=" * 80)
print("SESSION 12g COMPLETE")
print("=" * 80)
