"""
Reconstruct the master text from book overlaps.
All 70 books appear to be fragments of one circular/continuous digit sequence.
Finding the master text gives us the correct pair boundaries.
"""

import json
from collections import Counter

with open('books.json', 'r') as f:
    books = json.load(f)

print("=" * 70)
print("MASTER TEXT RECONSTRUCTION")
print("=" * 70)

# Strategy: start with the longest book and extend by finding overlaps
books_by_length = sorted(range(len(books)), key=lambda i: -len(books[i]))
print(f"\nLongest books: {[(i, len(books[i])) for i in books_by_length[:5]]}")

# Try to build master text greedily
used = set()
master = books[books_by_length[0]]
used.add(books_by_length[0])
print(f"Starting with book {books_by_length[0]} ({len(master)} digits)")

changed = True
iterations = 0
while changed and iterations < 100:
    changed = False
    iterations += 1
    for i in range(len(books)):
        if i in used:
            continue
        book = books[i]
        if len(book) < 5:
            continue

        # Check if book is already contained in master
        pos = master.find(book)
        if pos >= 0:
            used.add(i)
            changed = True
            continue

        # Check for suffix-prefix overlaps
        best_overlap = 0
        best_type = None

        # book's suffix = master's prefix
        for k in range(min(len(book), len(master)), 4, -1):
            if book[-k:] == master[:k]:
                if k > best_overlap:
                    best_overlap = k
                    best_type = 'book-before-master'
                break

        # master's suffix = book's prefix
        for k in range(min(len(book), len(master)), 4, -1):
            if master[-k:] == book[:k]:
                if k > best_overlap:
                    best_overlap = k
                    best_type = 'master-before-book'
                break

        if best_overlap > 10:  # require significant overlap
            if best_type == 'book-before-master':
                master = book[:-best_overlap] + master
            else:
                master = master + book[best_overlap:]
            used.add(i)
            changed = True

print(f"\nAfter {iterations} iterations:")
print(f"Master text length: {len(master)} digits")
print(f"Books incorporated: {len(used)}/{len(books)}")

# Check which books are contained
contained_count = 0
not_contained = []
for i in range(len(books)):
    if master.find(books[i]) >= 0:
        contained_count += 1
    else:
        not_contained.append(i)

print(f"Books contained in master: {contained_count}/{len(books)}")
if not_contained:
    print(f"NOT contained: {not_contained}")
    for i in not_contained:
        print(f"  Book {i}: '{books[i][:40]}...' ({len(books[i])} digits)")


print("\n" + "=" * 70)
print("MASTER TEXT PROPERTIES")
print("=" * 70)

print(f"Length: {len(master)} digits")
print(f"First 100 digits: {master[:100]}")
print(f"Last 100 digits: {master[-100:]}")

# Check if it's circular (end overlaps with beginning)
for k in range(min(100, len(master)//2), 4, -1):
    if master[-k:] == master[:k]:
        print(f"\nCIRCULAR! Overlap of {k} digits at start/end")
        print(f"  Start: {master[:k+10]}")
        print(f"  End:   {master[-(k+10):]}")
        break

# IC for both offsets
def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

for off in [0, 1]:
    pairs = [master[j:j+2] for j in range(off, len(master)-1, 2)]
    pc = Counter(pairs)
    ic = ic_from_counts(pc, len(pairs))
    print(f"\nOffset {off}: {len(pairs)} pairs, IC = {ic*100:.4f}")
    print(f"  Unique pairs: {len(pc)}")
    print(f"  Top 10: {pc.most_common(10)}")


print("\n" + "=" * 70)
print("DECODE MASTER TEXT")
print("=" * 70)

with open('best_mapping.json', 'r') as f:
    mapping = json.load(f)

german = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
    'Q': 0.001
}

for off in [0, 1]:
    pairs = [master[j:j+2] for j in range(off, len(master)-1, 2)]
    decoded = ''.join(mapping.get(p, '?') for p in pairs)

    # Count German words
    german_words = [
        'DER', 'DIE', 'DAS', 'UND', 'IST', 'EIN', 'EINE', 'EINEN', 'EINER',
        'DEN', 'DEM', 'VON', 'HAT', 'AUF', 'MIT', 'DES', 'SIE', 'ICH',
        'SIND', 'AUS', 'BEI', 'RUNE', 'RUNEN', 'STEIN', 'NICHT',
        'ABER', 'AUCH', 'NACH', 'NOCH', 'KANN', 'WIRD', 'SEIN',
        'ENDE', 'FEUER', 'WASSER', 'ERDE', 'LICHT',
    ]

    word_counts = {}
    for word in german_words:
        c = decoded.count(word)
        if c > 0:
            word_counts[word] = c

    total_word_hits = sum(word_counts.values())

    print(f"\n  Offset {off}: {len(decoded)} letters, {total_word_hits} German word hits")
    print(f"  Words: {sorted(word_counts.items(), key=lambda x: -x[1])[:20]}")
    print(f"\n  Decoded text:")
    for j in range(0, min(len(decoded), 500), 70):
        print(f"    {decoded[j:j+70]}")
    if len(decoded) > 500:
        print(f"    ...")
        print(f"    [... total {len(decoded)} letters ...]")


print("\n" + "=" * 70)
print("BOOK POSITIONS IN MASTER")
print("=" * 70)

# For each book, find its position in master text
book_positions = []
for i in range(len(books)):
    pos = master.find(books[i])
    if pos >= 0:
        book_positions.append((i, pos, len(books[i])))
    else:
        book_positions.append((i, -1, len(books[i])))

# Sort by position
book_positions.sort(key=lambda x: x[1])
for bi, pos, blen in book_positions:
    if pos >= 0:
        # The correct pair offset for this book depends on its position in master
        # If master offset is 0, book at even pos has offset 0, odd pos has offset 1
        correct_off = pos % 2
        ic_off = 0  # will compute below
        bp0 = [books[bi][j:j+2] for j in range(0, len(books[bi])-1, 2)]
        bp1 = [books[bi][j:j+2] for j in range(1, len(books[bi])-1, 2)]
        ic0 = ic_from_counts(Counter(bp0), len(bp0))
        ic1 = ic_from_counts(Counter(bp1), len(bp1))
        ic_off = 0 if ic0 > ic1 else 1
        match = "OK" if correct_off == ic_off else "MISMATCH"
        print(f"  Book {bi:2d} at pos {pos:4d} ({blen:3d}d): master_off={correct_off} ic_off={ic_off} [{match}]")
    else:
        print(f"  Book {bi:2d} NOT FOUND ({blen:3d}d)")


print("\n" + "=" * 70)
print("DECODE WITH MASTER OFFSET")
print("=" * 70)

# Use the master text's best offset
# First determine which offset is better for master
best_off = 0
best_word_count = 0
for off in [0, 1]:
    pairs = [master[j:j+2] for j in range(off, len(master)-1, 2)]
    decoded = ''.join(mapping.get(p, '?') for p in pairs)
    wc = sum(decoded.count(w) for w in german_words)
    if wc > best_word_count:
        best_word_count = wc
        best_off = off

print(f"Best master offset: {best_off} ({best_word_count} word hits)")

# Now decode each book using its correct offset derived from master position
print(f"\nBooks decoded with correct master-derived offsets:")
for bi, pos, blen in book_positions[:20]:
    if pos >= 0:
        correct_off = (pos + best_off) % 2
        pairs = [books[bi][j:j+2] for j in range(correct_off, len(books[bi])-1, 2)]
        decoded = ''.join(mapping.get(p, '?') for p in pairs)
        print(f"\n  Book {bi:2d} (pos={pos}, off={correct_off}, {len(decoded)} letters):")
        for j in range(0, len(decoded), 70):
            print(f"    {decoded[j:j+70]}")


print("\n" + "=" * 70)
print("SAVE MASTER TEXT")
print("=" * 70)

with open('master_text.txt', 'w') as f:
    f.write(master)
print(f"Saved master text ({len(master)} digits) to master_text.txt")

# Save book positions
with open('book_positions.json', 'w') as f:
    json.dump(book_positions, f, indent=2)
print("Saved book positions to book_positions.json")

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
