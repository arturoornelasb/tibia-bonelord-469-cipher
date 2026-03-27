#!/usr/bin/env python3
"""
Generate a clean per-book catalog: raw digits, decoded German, and book number.
Output goes to stdout for review.
"""

import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)

def decode(digits, mapping):
    """Decode a digit string, returning decoded text and per-char status."""
    result = []
    i = 0
    while i < len(digits) - 1:
        code = digits[i:i+2]
        if code in mapping:
            result.append(mapping[code])
        else:
            result.append('?')
        i += 2
    return ''.join(result)

# Decode each book
print(f"Total books: {len(books)}")
print(f"Mapping: v7 (98 codes -> 22 German letters)")
print()

for i, book in enumerate(books):
    decoded = decode(book, v7)
    digit_count = len(book)
    char_count = len(decoded)
    odd = " [ODD LENGTH - 1 digit lost]" if digit_count % 2 != 0 else ""

    print(f"=== BOOK {i+1:02d} ({digit_count} digits -> {char_count} letters{odd}) ===")
    print(f"RAW:     {decoded}")
    print()
