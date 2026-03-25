#!/usr/bin/env python3
"""Session 12c: Raw code-level assembly + internal overlap detection"""

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

print("=" * 80)
print("SESSION 12c: RAW CODE-LEVEL ASSEMBLY")
print("=" * 80)

# 1. Work at RAW code level - find overlaps in code sequences, not text
print("\n1. RAW CODE OVERLAPS")
print("-" * 60)

# Convert books to code strings for easier comparison
code_strings = [''.join(b) for b in books]

# Find all edge overlaps at code level
raw_overlaps = {}
for i in range(len(books)):
    for j in range(len(books)):
        if i == j: continue
        si = code_strings[i]
        sj = code_strings[j]
        # si suffix matches sj prefix (in increments of 2 for code pairs)
        for k in range(min(len(si), len(sj)), 3, -2):  # step by 2 for code pairs
            if si[-k:] == sj[:k]:
                raw_overlaps[(i,j)] = k // 2  # in number of codes
                break

print(f"  Raw code overlaps found: {len(raw_overlaps)}")

# Show top overlaps
top_raw = sorted(raw_overlaps.items(), key=lambda x: x[1], reverse=True)[:20]
print(f"\n  Top 20 raw code overlaps:")
for (i,j), ov in top_raw:
    print(f"    B{i:02d} -> B{j:02d}: {ov} codes ({ov*2} digits)")

# 2. Greedy merge at RAW code level
print(f"\n2. RAW CODE GREEDY MERGE")
print("-" * 60)

best_merged_codes = ''
best_used_raw = set()
best_start_raw = -1
best_order_raw = []

for start_idx in range(len(books)):
    merged = code_strings[start_idx]
    used = {start_idx}
    order = [start_idx]

    changed = True
    while changed:
        changed = False
        best_bi = None
        best_ov = 0
        best_side = None
        best_new_text = ''

        for bi in range(len(books)):
            if bi in used: continue
            text = code_strings[bi]

            # Right append (must align on 2-char code boundaries)
            for k in range(min(len(merged), len(text)), 3, -2):
                if merged[-k:] == text[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'right'
                        best_new_text = text[k:]
                    break

            # Left prepend
            for k in range(min(len(merged), len(text)), 3, -2):
                if text[-k:] == merged[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'left'
                        best_new_text = text[:-k]
                    break

        if best_bi is not None and best_ov >= 4:  # at least 2 codes
            used.add(best_bi)
            order.append(best_bi)
            if best_side == 'right':
                merged += best_new_text
            else:
                merged = best_new_text + merged
            changed = True

    if len(used) > len(best_used_raw):
        best_merged_codes = merged
        best_used_raw = set(used)
        best_start_raw = start_idx
        best_order_raw = list(order)

print(f"  Best start: B{best_start_raw:02d}")
print(f"  Books merged: {len(best_used_raw)}/{len(books)}")
print(f"  Total codes in merged: {len(best_merged_codes)//2}")
print(f"  Merge order: {best_order_raw[:20]}...")
print(f"  NOT merged: {sorted(set(range(len(books))) - best_used_raw)}")

# 3. Check if unmerged books are SUBSTRINGS of merged
print(f"\n3. SUBSTRING CHECK")
print("-" * 60)

contained = 0
not_contained = []
for bi in range(len(books)):
    if code_strings[bi] in best_merged_codes:
        contained += 1
    else:
        not_contained.append(bi)

print(f"  Books contained in merged: {contained}/{len(books)}")
if not_contained:
    print(f"  NOT contained ({len(not_contained)}): {not_contained[:20]}...")

# 4. For uncontained books, find best internal alignment
print(f"\n4. INTERNAL ALIGNMENT OF UNCONTAINED BOOKS")
print("-" * 60)

for bi in not_contained[:10]:
    bk = code_strings[bi]
    # Find longest matching substring
    best_match_len = 0
    best_match_pos = -1
    for start in range(0, len(best_merged_codes) - 3, 2):
        match_len = 0
        for k in range(0, min(len(bk), len(best_merged_codes) - start), 2):
            if bk[k:k+2] == best_merged_codes[start+k:start+k+2]:
                match_len += 2
            else:
                break
        if match_len > best_match_len:
            best_match_len = match_len
            best_match_pos = start

    print(f"  B{bi:02d}: {len(bk)//2} codes, best prefix match = {best_match_len//2} codes at pos {best_match_pos//2}")

# 5. Decode and collapse the full merged raw codes
print(f"\n5. DECODED MERGED TEXT")
print("-" * 60)

merged_codes = parse_codes(best_merged_codes)
decoded_merged = decode(merged_codes)
collapsed_merged = collapse(decoded_merged)
print(f"  Raw codes: {len(merged_codes)}")
print(f"  Decoded: {len(decoded_merged)} chars")
print(f"  Collapsed: {len(collapsed_merged)} chars")
print()
for i in range(0, len(collapsed_merged), 70):
    print(f"  [{i:4d}] {collapsed_merged[i:i+70]}")

# 6. Try MUCH lower threshold for merge
print(f"\n6. AGGRESSIVE MERGE (threshold >= 2 codes)")
print("-" * 60)

best_merged2 = ''
best_used2 = set()
best_start2 = -1

for start_idx in range(len(books)):
    merged = code_strings[start_idx]
    used = {start_idx}

    changed = True
    while changed:
        changed = False
        best_bi = None
        best_ov = 0
        best_side = None
        best_new = ''

        for bi in range(len(books)):
            if bi in used: continue
            text = code_strings[bi]

            for k in range(min(len(merged), len(text)), 3, -2):
                if merged[-k:] == text[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'right'
                        best_new = text[k:]
                    break

            for k in range(min(len(merged), len(text)), 3, -2):
                if text[-k:] == merged[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'left'
                        best_new = text[:-k]
                    break

        if best_bi is not None and best_ov >= 4:
            used.add(best_bi)
            if best_side == 'right':
                merged += best_new
            else:
                merged = best_new + merged
            changed = True

    if len(used) > len(best_used2):
        best_merged2 = merged
        best_used2 = set(used)
        best_start2 = start_idx

print(f"  Best start: B{best_start2:02d}")
print(f"  Books merged: {len(best_used2)}/{len(books)}")
print(f"  Total codes: {len(best_merged2)//2}")

# 7. Try finding a CIRCULAR text
# If the narrative wraps around, the last book's end matches the first book's start
print(f"\n7. CIRCULAR TEXT CHECK")
print("-" * 60)

# Check if any book's end matches any other book's start at high overlap
# suggesting a cycle
for (i,j), ov in sorted(raw_overlaps.items(), key=lambda x: -x[1])[:5]:
    print(f"  B{i:02d}->B{j:02d}: {ov} codes")
    # Show the overlapping codes
    overlap_codes = code_strings[i][-ov*2:]
    overlap_decoded = collapse(decode(parse_codes(overlap_codes)))
    print(f"    Overlap text: ...{overlap_decoded}...")

# 8. Alternative: find ALL pairwise overlaps including internal matches
# This looks for where one book is a substring of another
print(f"\n8. CONTAINMENT RELATIONSHIPS")
print("-" * 60)

containers = defaultdict(list)  # book -> list of books it contains
for i in range(len(books)):
    for j in range(len(books)):
        if i == j: continue
        if code_strings[j] in code_strings[i]:
            containers[i].append(j)

if containers:
    for container, contained_books in sorted(containers.items(), key=lambda x: -len(x[1])):
        if len(contained_books) >= 1:
            print(f"  B{container:02d} ({len(books[container])} codes) contains: {['B'+str(b).zfill(2) for b in contained_books]}")
else:
    print("  No containment found at raw code level")

# 9. Check book lengths distribution
print(f"\n9. BOOK LENGTH DISTRIBUTION")
print("-" * 60)

lengths = [(bi, len(books[bi])) for bi in range(len(books))]
lengths.sort(key=lambda x: -x[1])
for bi, ln in lengths[:10]:
    print(f"  B{bi:02d}: {ln} codes = {ln*2} digits")
print(f"  ...")
for bi, ln in lengths[-5:]:
    print(f"  B{bi:02d}: {ln} codes = {ln*2} digits")
print(f"\n  Mean: {sum(l for _,l in lengths)/len(lengths):.1f} codes")
print(f"  Total unique codes: {len(set(c for b in books for c in b))}")

# 10. Unique codes analysis
print(f"\n10. UNIQUE CODE ANALYSIS")
print("-" * 60)
all_codes = [c for b in books for c in b]
code_freq = Counter(all_codes)
print(f"  Total code occurrences: {len(all_codes)}")
print(f"  Unique codes: {len(code_freq)}")
print(f"\n  Code frequency (top 20):")
for code, freq in code_freq.most_common(20):
    letter = mapping.get(code, '?')
    print(f"    {code}={letter}: {freq}x")

# Check for code 32 or any missing codes
all_possible = set(f"{i:02d}" for i in range(100))
used_codes = set(code_freq.keys())
unused = all_possible - used_codes - set(mapping.keys())
never_appears = set(mapping.keys()) - used_codes
print(f"\n  Mapped but never appears in text: {sorted(never_appears)}")
print(f"  Unmapped and unused: {sorted(unused)}")

print("\n" + "=" * 80)
print("SESSION 12c COMPLETE")
print("=" * 80)
