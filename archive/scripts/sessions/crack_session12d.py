#!/usr/bin/env python3
"""Session 12d: Investigate code alignment + code 33 mystery + assembly improvement"""

import json, re
from collections import Counter, defaultdict

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]

print("=" * 80)
print("SESSION 12d: CODE ALIGNMENT INVESTIGATION")
print("=" * 80)

# 1. Check book digit string lengths
print("\n1. BOOK DIGIT STRING LENGTHS")
print("-" * 60)

odd_books = []
for bi, book_str in enumerate(raw_books):
    if len(book_str) % 2 != 0:
        odd_books.append((bi, len(book_str)))
        print(f"  B{bi:02d}: {len(book_str)} digits (ODD!)")
        print(f"    Last 10 digits: ...{book_str[-10:]}")
        print(f"    Codes: {parse_codes(book_str[-10:])}")

if not odd_books:
    print("  All books have even number of digits")
else:
    print(f"\n  {len(odd_books)} books with odd digit count!")

# 2. Find ALL unique codes across all books
print("\n2. ALL UNIQUE CODES IN CORPUS")
print("-" * 60)

all_codes_set = set()
all_codes_list = []
for bi, book_str in enumerate(raw_books):
    codes = parse_codes(book_str)
    for c in codes:
        all_codes_set.add(c)
        all_codes_list.append(c)

print(f"  Unique codes: {len(all_codes_set)}")
print(f"  Sorted: {sorted(all_codes_set)}")

# Check which codes are NOT in the mapping
unmapped = sorted(all_codes_set - set(mapping.keys()))
print(f"\n  Codes in text but NOT in mapping ({len(unmapped)}): {unmapped}")

for code in unmapped:
    count = all_codes_list.count(code)
    # Show which books contain this code
    books_with = []
    for bi, book_str in enumerate(raw_books):
        codes = parse_codes(book_str)
        if code in codes:
            books_with.append(bi)
    print(f"    Code {code}: {count}x, in books: {books_with[:10]}")

# Codes in mapping but NOT in text
unused_mapped = sorted(set(mapping.keys()) - all_codes_set)
print(f"\n  Codes in mapping but NOT in text ({len(unused_mapped)}): {unused_mapped}")
for code in unused_mapped:
    print(f"    Code {code} -> {mapping[code]}")

# 3. Code 33 investigation - it's mapped to W but never appears
print("\n3. CODE 33 (W) INVESTIGATION")
print("-" * 60)

# How does W appear in decoded text if code 33 never appears?
w_codes = [c for c, l in mapping.items() if l == 'W']
print(f"  W codes in mapping: {w_codes}")
for wc in w_codes:
    count = all_codes_list.count(wc)
    print(f"    Code {wc}: {count}x")

# Check code 33 as digits - maybe it appears split across code boundaries
for bi, book_str in enumerate(raw_books):
    idx = book_str.find('33')
    if idx >= 0:
        # Check if it's at an even boundary (actual code) vs odd boundary (split)
        if idx % 2 == 0:
            # This IS a valid code 33 position
            print(f"  B{bi:02d}: '33' at pos {idx} (VALID code boundary)")
        else:
            pass  # split across boundaries, not an actual code 33

# 4. The unmapped codes - are they single-digit artifacts or real codes?
print("\n4. UNMAPPED CODE ANALYSIS")
print("-" * 60)

for code in unmapped:
    # Find context in books
    for bi, book_str in enumerate(raw_books):
        codes = parse_codes(book_str)
        for ci, c in enumerate(codes):
            if c == code:
                # Show surrounding codes
                start = max(0, ci-3)
                end = min(len(codes), ci+4)
                context = codes[start:end]
                decoded_context = ''.join(mapping.get(cc, f'[{cc}]') for cc in context)
                print(f"  B{bi:02d} pos {ci}: ...{' '.join(context)}... = {decoded_context}")
                break
        else:
            continue
        break

# 5. Check if these unmapped codes could be additional letters
print("\n5. UNMAPPED CODES AS POTENTIAL LETTERS")
print("-" * 60)

# For each unmapped code, analyze what letter it might represent
# by looking at surrounding code context
for code in unmapped:
    contexts = []
    for bi, book_str in enumerate(raw_books):
        codes = parse_codes(book_str)
        for ci, c in enumerate(codes):
            if c == code:
                before = codes[max(0,ci-5):ci]
                after = codes[ci+1:ci+6]
                before_text = ''.join(mapping.get(cc, '?') for cc in before)
                after_text = ''.join(mapping.get(cc, '?') for cc in after)
                contexts.append((bi, ci, before_text, after_text))

    if contexts:
        print(f"\n  Code {code} ({len(contexts)} occurrences):")
        for bi, ci, before, after in contexts[:5]:
            print(f"    B{bi:02d}:{ci}: ...{before}[?]{after}...")

# 6. Investigate: is code 33 actually in the data but parsed as something else?
print("\n6. DIGIT SEQUENCE '33' IN RAW DATA")
print("-" * 60)

total_33 = 0
for bi, book_str in enumerate(raw_books):
    # Count all occurrences of '33' in the raw string
    count = book_str.count('33')
    if count > 0:
        total_33 += count
        positions = []
        pos = 0
        while True:
            idx = book_str.find('33', pos)
            if idx < 0: break
            alignment = "EVEN (=code)" if idx % 2 == 0 else "ODD (split)"
            positions.append((idx, alignment))
            pos = idx + 1
        print(f"  B{bi:02d}: '33' x{count}: {positions}")

print(f"\n  Total '33' occurrences: {total_33}")
print(f"  But code 33 never appears at even boundary")

# 7. This means: code 33 is mapped to W but never actually used!
# W only appears via codes 36 and 87
# Check W frequency
w_count = sum(1 for c in all_codes_list if mapping.get(c) == 'W')
print(f"\n7. W LETTER STATISTICS")
print(f"  Total W occurrences: {w_count}")
print(f"  W codes actually used: {[c for c in w_codes if c in all_codes_set]}")
print(f"  W codes never used: {[c for c in w_codes if c not in all_codes_set]}")

# 8. Full code-to-letter frequency table
print(f"\n8. COMPLETE CODE FREQUENCY TABLE")
print("-" * 60)

code_freq = Counter(all_codes_list)
by_letter = defaultdict(list)
for code, letter in mapping.items():
    freq = code_freq.get(code, 0)
    by_letter[letter].append((code, freq))

for letter in sorted(by_letter.keys()):
    codes_info = by_letter[letter]
    total = sum(f for _, f in codes_info)
    detail = ', '.join(f'{c}:{f}' for c, f in sorted(codes_info, key=lambda x: -x[1]))
    pct = total * 100 / len(all_codes_list)
    print(f"  {letter}: {total:4d} ({pct:5.1f}%) <- [{detail}]")

# Show unmapped codes
print(f"\n  UNMAPPED:")
for code in sorted(unmapped):
    freq = code_freq.get(code, 0)
    print(f"  ?{code}?: {freq:4d} occurrences")

# 9. Build better superstring using longest-first assembly
print(f"\n9. LONGEST-FIRST ASSEMBLY")
print("-" * 60)

# Sort books by length (longest first)
books_parsed = [(bi, parse_codes(raw_books[bi])) for bi in range(len(raw_books))]
books_by_length = sorted(books_parsed, key=lambda x: -len(x[1]))

# Start with longest book
superstring = list(books_by_length[0][1])
used = {books_by_length[0][0]}
print(f"  Starting with B{books_by_length[0][0]:02d} ({len(superstring)} codes)")

# Iteratively add books
for bi, book_codes in books_by_length[1:]:
    # Check if this book is already contained
    book_str = ''.join(book_codes)
    super_str = ''.join(superstring)
    if book_str in super_str:
        used.add(bi)
        continue

    # Check right append
    best_right = 0
    for k in range(min(len(superstring), len(book_codes)), 0, -1):
        if superstring[-k:] == book_codes[:k]:
            best_right = k
            break

    # Check left prepend
    best_left = 0
    for k in range(min(len(superstring), len(book_codes)), 0, -1):
        if book_codes[-k:] == superstring[:k]:
            best_left = k
            break

    if best_right >= 2 or best_left >= 2:
        if best_right >= best_left:
            superstring.extend(book_codes[best_right:])
        else:
            superstring = book_codes[:-best_left] + superstring
        used.add(bi)

print(f"  Books assembled: {len(used)}/{len(raw_books)}")
print(f"  Superstring length: {len(superstring)} codes")
print(f"  Not assembled: {sorted(set(range(len(raw_books))) - used)}")

# Decode and display
from collections import Counter
def decode_codes(codes, m=None):
    if m is None: m = mapping
    return ''.join(m.get(c, '?') for c in codes)

decoded = decode_codes(superstring)
collapsed = re.sub(r'(.)\1+', r'\1', decoded)
print(f"  Decoded length: {len(decoded)}")
print(f"  Collapsed length: {len(collapsed)}")
print(f"\n  First 500 chars of collapsed superstring:")
for i in range(0, min(500, len(collapsed)), 70):
    print(f"    [{i:4d}] {collapsed[i:i+70]}")

print("\n" + "=" * 80)
print("SESSION 12d COMPLETE")
print("=" * 80)
