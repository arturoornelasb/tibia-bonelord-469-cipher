#!/usr/bin/env python3
"""
Parse the Hellgate Library bookcase data and match to books.json.
Create complete physical arrangement mapping.
"""
import json, os, re

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')
docs_dir = os.path.join(script_dir, '..', '..', 'docs')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

# Parse the Hellgate Library file
with open(os.path.join(docs_dir, 'Hellgate_Library.txt'), 'r') as f:
    raw = f.read()

# Parse bookcases and books
bookcase_name = None
library_books = []
current_book = None

for line in raw.split('\n'):
    line = line.rstrip()

    # Check for bookcase header
    bc_match = re.match(r'^(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|'
                        r'Eleventh|Twelfth|Thirteenth|Fourteenth|Fifteenth|Sixteenth|'
                        r'Seventeenth|Eighteenth|Nineteenth|Twentieth|Twenty-First|'
                        r'Twenty-Second|Twenty-Third|Twenty-Fourth|Twenty-Fifth|'
                        r'Twenty-Sixth|Twenty-Seventh|Twenty-Eighth|Twenty-Ninth|'
                        r'Thirtieth|Thirty-First|Thirty-Second|Thirty-Third|'
                        r'Thirty-Fourth|Thirty-Fifth|Thirty-Sixth|Thirty-Seventh|'
                        r'Thirty-Eighth|Thirty-Ninth|Fortieth)\s+Bookcase', line)
    if bc_match:
        bookcase_name = bc_match.group(0)
        continue

    # Check for book entry
    book_match = re.match(r'^#\s*(\d+)\s+(\d+)\s+\(Book\)\s+([\d\s]+)', line)
    if book_match:
        if current_book:
            library_books.append(current_book)
        book_num = int(book_match.group(1))
        label = book_match.group(2)
        content = book_match.group(3).strip().replace(' ', '')
        current_book = {
            'num': book_num,
            'label': label,
            'bookcase': bookcase_name,
            'content': content,
        }
        continue

    # Continuation line (indented digits)
    if current_book and line.strip() and re.match(r'^[\d\s]+$', line.strip()):
        current_book['content'] += line.strip().replace(' ', '')

if current_book:
    library_books.append(current_book)

print(f"Parsed {len(library_books)} books from Hellgate Library file")
print(f"Books in books.json: {len(books)}")

# Match each library book to books.json by content
matches = []
unmatched_lib = []
matched_json_indices = set()

for lb in library_books:
    content = lb['content']
    best_match = None
    best_overlap = 0

    for idx, book in enumerate(books):
        # Check if the content matches (could be slightly different due to copy errors)
        # Try exact match first
        if content == book:
            best_match = idx
            best_overlap = len(book)
            break
        # Try prefix match (at least 20 chars)
        common_len = 0
        for i in range(min(len(content), len(book))):
            if content[i] == book[i]:
                common_len += 1
            else:
                break
        if common_len > best_overlap and common_len >= 20:
            best_match = idx
            best_overlap = common_len

    if best_match is not None:
        matches.append({
            'lib_num': lb['num'],
            'json_idx': best_match,
            'bookcase': lb['bookcase'],
            'label': lb['label'],
            'overlap': best_overlap,
            'lib_len': len(lb['content']),
            'json_len': len(books[best_match]),
            'exact': lb['content'] == books[best_match],
        })
        matched_json_indices.add(best_match)
    else:
        unmatched_lib.append(lb)

# Report
print(f"\nMatched: {len(matches)} books")
print(f"Unmatched library books: {len(unmatched_lib)}")
print(f"Unmatched books.json indices: {set(range(len(books))) - matched_json_indices}")

print(f"\n{'=' * 90}")
print(f"COMPLETE BOOKCASE MAPPING")
print(f"{'=' * 90}")
print(f"{'Bookcase':<30} {'Lib#':>4} {'JSON#':>5} {'Len':>5} {'Match':>6} {'Label':<12}")
print(f"{'-' * 90}")

current_bc = None
for m in sorted(matches, key=lambda x: (x['bookcase'] or '', x['lib_num'])):
    bc = m['bookcase']
    if bc != current_bc:
        if current_bc:
            print()
        current_bc = bc
    match_str = 'EXACT' if m['exact'] else f"{m['overlap']}/{m['lib_len']}"
    print(f"  {bc:<28} #{m['lib_num']:>3}  idx{m['json_idx']:>3}  {m['json_len']:>5}  {match_str:>6}  {m['label']}")

# Check for duplicate JSON indices (same book appearing in multiple shelves)
json_idx_counts = {}
for m in matches:
    idx = m['json_idx']
    if idx not in json_idx_counts:
        json_idx_counts[idx] = []
    json_idx_counts[idx].append(m['lib_num'])

print(f"\n{'=' * 90}")
print(f"DUPLICATE DETECTION (same book on multiple shelves)")
print(f"{'=' * 90}")
duplicates = {k: v for k, v in json_idx_counts.items() if len(v) > 1}
if duplicates:
    for idx, nums in sorted(duplicates.items()):
        print(f"  books.json[{idx}] appears as library books: {nums}")
else:
    print("  No duplicates found")

# Books in books.json not found in library
missing = sorted(set(range(len(books))) - matched_json_indices)
if missing:
    print(f"\n{'=' * 90}")
    print(f"BOOKS IN books.json NOT FOUND IN LIBRARY ({len(missing)} books)")
    print(f"{'=' * 90}")
    for idx in missing:
        print(f"  books.json[{idx}]: len={len(books[idx])}, starts with {books[idx][:20]}...")

# Save the mapping
bookcase_map = []
for m in sorted(matches, key=lambda x: x['lib_num']):
    bookcase_map.append({
        'library_number': m['lib_num'],
        'books_json_index': m['json_idx'],
        'bookcase': m['bookcase'],
        'label_10digit': m['label'],
        'exact_match': m['exact'],
        'content_length': m['json_len'],
    })

output_path = os.path.join(data_dir, 'bookcase_mapping.json')
with open(output_path, 'w') as f:
    json.dump(bookcase_map, f, indent=2)
print(f"\nSaved bookcase mapping to {output_path}")

# Show bookcase order for narrative reading
print(f"\n{'=' * 90}")
print(f"NARRATIVE READING ORDER (by bookcase, then by shelf position)")
print(f"{'=' * 90}")

# Group by bookcase
from collections import OrderedDict
bc_order = OrderedDict()
for m in matches:
    bc = m['bookcase']
    if bc not in bc_order:
        bc_order[bc] = []
    bc_order[bc].append(m)

bookcase_reading_order = []
for bc, bks in bc_order.items():
    bks_sorted = sorted(bks, key=lambda x: x['lib_num'])
    for bk in bks_sorted:
        bookcase_reading_order.append(bk['json_idx'])
    print(f"  {bc}: {[b['json_idx'] for b in bks_sorted]}")

print(f"\nFull reading order: {bookcase_reading_order}")
print(f"Total books in order: {len(bookcase_reading_order)}")
