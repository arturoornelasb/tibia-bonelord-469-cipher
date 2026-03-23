#!/usr/bin/env python3
"""Session 12e: Investigate odd-length books - are they truncated or do they use 1-digit codes?"""

import json, re
from collections import Counter, defaultdict

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

print("=" * 80)
print("SESSION 12e: ODD-LENGTH BOOK INVESTIGATION")
print("=" * 80)

# Key question: 37 of 70 books have ODD digit counts
# This means parse_codes() misaligns the last digit
# Two hypotheses:
# A) The last digit is a truncated/incomplete code (data extraction error)
# B) The last digit is significant (maybe a 1-digit code, or different encoding)

# 1. Compare even vs odd books
print("\n1. EVEN vs ODD LENGTH BOOKS")
print("-" * 60)

even_books = []
odd_books = []
for bi, book_str in enumerate(raw_books):
    if len(book_str) % 2 == 0:
        even_books.append(bi)
    else:
        odd_books.append(bi)

print(f"  Even-length books: {len(even_books)}: {even_books}")
print(f"  Odd-length books:  {len(odd_books)}: {odd_books}")

# 2. For odd books, what is the LAST digit?
print("\n2. TRAILING DIGITS OF ODD-LENGTH BOOKS")
print("-" * 60)

trailing = Counter()
for bi in odd_books:
    last_digit = raw_books[bi][-1]
    trailing[last_digit] += 1

print(f"  Trailing digit distribution:")
for digit, count in sorted(trailing.items()):
    print(f"    '{digit}': {count}x")

# 3. If we DROP the last digit of odd books, do overlaps improve?
print("\n3. OVERLAPS WITH TRIMMED ODD BOOKS")
print("-" * 60)

# Trim odd books (drop last digit)
trimmed = {}
for bi in range(len(raw_books)):
    s = raw_books[bi]
    if len(s) % 2 != 0:
        trimmed[bi] = s[:-1]  # drop last digit
    else:
        trimmed[bi] = s

# Now find overlaps at code level with all even-aligned
def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]

trimmed_codes = {bi: parse_codes(trimmed[bi]) for bi in range(len(raw_books))}
trimmed_strings = {bi: trimmed[bi] for bi in range(len(raw_books))}

# Find overlaps
raw_overlaps_trimmed = {}
for i in range(len(raw_books)):
    for j in range(len(raw_books)):
        if i == j: continue
        si = trimmed_strings[i]
        sj = trimmed_strings[j]
        for k in range(min(len(si), len(sj)), 3, -2):
            if si[-k:] == sj[:k]:
                raw_overlaps_trimmed[(i,j)] = k // 2
                break

print(f"  Overlaps with trimmed books: {len(raw_overlaps_trimmed)}")

# Compare to untrimmed
untrimmed_codes = {bi: parse_codes(raw_books[bi]) for bi in range(len(raw_books))}
untrimmed_strings = {bi: raw_books[bi] for bi in range(len(raw_books))}
raw_overlaps_untrimmed = {}
for i in range(len(raw_books)):
    for j in range(len(raw_books)):
        if i == j: continue
        si = untrimmed_strings[i]
        sj = untrimmed_strings[j]
        for k in range(min(len(si), len(sj)), 3, -2):
            if si[-k:] == sj[:k]:
                raw_overlaps_untrimmed[(i,j)] = k // 2
                break

print(f"  Overlaps with untrimmed books: {len(raw_overlaps_untrimmed)}")

# 4. Try SHIFTED parsing - what if some books start at digit 1 instead of digit 0?
print("\n4. SHIFTED PARSING TEST")
print("-" * 60)

# For odd-length books, try parsing from position 1 instead of 0
for bi in odd_books[:5]:
    s = raw_books[bi]
    normal = parse_codes(s)  # [s[0:2], s[2:4], ...]
    shifted = parse_codes(s[1:])  # [s[1:3], s[3:5], ...]

    normal_decoded = ''.join(mapping.get(c, '?') for c in normal)
    shifted_decoded = ''.join(mapping.get(c, '?') for c in shifted)

    normal_q = normal_decoded.count('?')
    shifted_q = shifted_decoded.count('?')

    print(f"  B{bi:02d} ({len(s)} digits):")
    print(f"    Normal parse ({len(normal)} codes, {normal_q} unknown): {re.sub(r'(.)+', r'\\1', normal_decoded[:50])}...")
    print(f"    Shifted parse ({len(shifted)} codes, {shifted_q} unknown): {re.sub(r'(.)+', r'\\1', shifted_decoded[:50])}...")

# 5. Greedy merge with trimmed books
print("\n5. GREEDY MERGE WITH TRIMMED BOOKS")
print("-" * 60)

best_merged = ''
best_used = set()
best_start = -1

for start_idx in range(len(raw_books)):
    merged = trimmed_strings[start_idx]
    used = {start_idx}

    changed = True
    while changed:
        changed = False
        best_bi = None
        best_ov = 0
        best_side = None
        best_new = ''

        for bi in range(len(raw_books)):
            if bi in used: continue
            text = trimmed_strings[bi]

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

    if len(used) > len(best_used):
        best_merged = merged
        best_used = set(used)
        best_start = start_idx

print(f"  Best start: B{best_start:02d}")
print(f"  Books merged: {len(best_used)}/{len(raw_books)}")
print(f"  Superstring length: {len(best_merged)//2} codes")
print(f"  NOT merged: {sorted(set(range(len(raw_books))) - best_used)}")

# Check containment with trimmed
contained_trimmed = 0
for bi in range(len(raw_books)):
    if trimmed_strings[bi] in best_merged:
        contained_trimmed += 1
print(f"  Books contained in merged: {contained_trimmed}/{len(raw_books)}")

# Decode merged
merged_codes = parse_codes(best_merged)
decoded = ''.join(mapping.get(c, '?') for c in merged_codes)
collapsed = re.sub(r'(.)\1+', r'\1', decoded)
print(f"  Collapsed text: {len(collapsed)} chars")

# 6. What if the trailing digit of odd books is the FIRST digit of the next book?
# In Tibia, books might wrap around in a scroll
print("\n6. CROSS-BOOK DIGIT BRIDGING")
print("-" * 60)

# For each odd book, check if its last digit + first digit of another book
# forms a valid code
bridge_matches = []
for bi in odd_books:
    last_digit = raw_books[bi][-1]
    for bj in range(len(raw_books)):
        if bi == bj: continue
        first_digit = raw_books[bj][0]
        bridge_code = last_digit + first_digit
        if bridge_code in mapping:
            # Check if the rest of bi and bj overlap
            bi_trimmed = raw_books[bi][:-1]  # remove last digit
            bj_shifted = raw_books[bj][1:]   # remove first digit
            # Form the bridge: bi_trimmed + bridge_code + bj_shifted
            # Or simply: does bi (without last digit) overlap with bj?
            bridge_matches.append((bi, bj, bridge_code, mapping[bridge_code]))

# Count how many unique bridges
bridge_pairs = set((bi, bj) for bi, bj, _, _ in bridge_matches)
print(f"  Potential bridges (odd end + even start = valid code): {len(bridge_matches)}")
print(f"  Unique book pairs: {len(bridge_pairs)}")

# Show some examples
for bi, bj, code, letter in bridge_matches[:10]:
    bi_end = raw_books[bi][-5:]
    bj_start = raw_books[bj][:5]
    print(f"  B{bi:02d}[...{bi_end}] + B{bj:02d}[{bj_start}...] -> bridge code {code}={letter}")

# 7. Analyze the ACTUAL text encoding
# Are these Bonelord library books or are they from somewhere else?
print("\n7. BOOK STRUCTURE ANALYSIS")
print("-" * 60)

# Check if books could use a DIFFERENT encoding
# What if some digits are literal (representing themselves)?
# Tibia's Bonelord language uses digits 0-9 displayed as symbols
# The 469 cipher = base-10 digits represented as Bonelord characters

# Show first 20 digits of each book
for bi in range(min(10, len(raw_books))):
    s = raw_books[bi]
    print(f"  B{bi:02d} ({len(s):3d} digits): {s[:40]}...")

# 8. Statistical test: do odd books decode worse than even books?
print("\n8. DECODE QUALITY: EVEN vs ODD BOOKS")
print("-" * 60)

def collapse(s):
    return re.sub(r'(.)\1+', r'\1', s)

for group_name, group in [("EVEN", even_books), ("ODD", odd_books)]:
    total_q = 0
    total_chars = 0
    for bi in group:
        codes = parse_codes(raw_books[bi])
        decoded = ''.join(mapping.get(c, '?') for c in codes)
        total_q += decoded.count('?')
        total_chars += len(decoded)
    print(f"  {group_name}: {total_q}/{total_chars} unknown = {total_q*100/total_chars:.1f}%")

# For odd books, compare normal vs trimmed
print(f"\n  Odd books: normal parse vs trimmed:")
total_q_normal = 0
total_q_trimmed = 0
total_chars_normal = 0
total_chars_trimmed = 0
for bi in odd_books:
    # Normal (includes misaligned last code)
    codes_n = parse_codes(raw_books[bi])
    decoded_n = ''.join(mapping.get(c, '?') for c in codes_n)
    total_q_normal += decoded_n.count('?')
    total_chars_normal += len(decoded_n)

    # Trimmed (drop last digit)
    codes_t = parse_codes(raw_books[bi][:-1])
    decoded_t = ''.join(mapping.get(c, '?') for c in codes_t)
    total_q_trimmed += decoded_t.count('?')
    total_chars_trimmed += len(decoded_t)

print(f"    Normal: {total_q_normal}/{total_chars_normal} unknown = {total_q_normal*100/total_chars_normal:.1f}%")
print(f"    Trimmed: {total_q_trimmed}/{total_chars_trimmed} unknown = {total_q_trimmed*100/total_chars_trimmed:.1f}%")

# 9. Does trimming affect the decoded text?
print(f"\n9. TRIMMED vs NORMAL DECODE COMPARISON")
print("-" * 60)

for bi in odd_books[:5]:
    codes_n = parse_codes(raw_books[bi])
    codes_t = parse_codes(raw_books[bi][:-1])

    decoded_n = ''.join(mapping.get(c, '?') for c in codes_n)
    decoded_t = ''.join(mapping.get(c, '?') for c in codes_t)

    collapsed_n = collapse(decoded_n)
    collapsed_t = collapse(decoded_t)

    # The difference is only at the end
    print(f"  B{bi:02d}:")
    print(f"    Normal end:  ...{collapsed_n[-30:]}")
    print(f"    Trimmed end: ...{collapsed_t[-30:]}")

print("\n" + "=" * 80)
print("SESSION 12e COMPLETE")
print("=" * 80)
