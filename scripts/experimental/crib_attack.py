"""
Crib-based attack on the 2-digit pair cipher.
Find high-confidence word occurrences, extract underlying digit pairs,
use them as anchors to constrain the mapping.
Also analyze book overlaps to determine pair boundaries.
"""

import json
from collections import Counter

with open('books.json', 'r') as f:
    books = json.load(f)

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

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

# Per-book alignment
book_offsets = []
for book in books:
    if len(book) < 10:
        book_offsets.append(0)
        continue
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    ic0 = ic_from_counts(Counter(bp0), len(bp0))
    ic1 = ic_from_counts(Counter(bp1), len(bp1))
    book_offsets.append(0 if ic0 > ic1 else 1)


print("=" * 70)
print("1. BOOK OVERLAP ANALYSIS")
print("=" * 70)

# Find shared digit sequences between books
book_texts = [b for b in books]

# Check for containment/overlap
overlaps = []
for i in range(len(books)):
    for j in range(i+1, len(books)):
        shorter = books[i] if len(books[i]) <= len(books[j]) else books[j]
        longer = books[j] if len(books[i]) <= len(books[j]) else books[i]
        si = i if len(books[i]) <= len(books[j]) else j
        li = j if len(books[i]) <= len(books[j]) else i

        # Check if shorter is contained in longer
        pos = longer.find(shorter)
        if pos >= 0 and len(shorter) > 10:
            overlaps.append((si, li, pos, len(shorter), 'contained'))
        elif len(shorter) > 20:
            # Check for partial overlap (suffix of one = prefix of other)
            for k in range(20, min(len(shorter), len(longer))):
                if shorter[-k:] == longer[:k]:
                    overlaps.append((si, li, 0, k, 'suffix-prefix'))
                    break
                if longer[-k:] == shorter[:k]:
                    overlaps.append((li, si, 0, k, 'suffix-prefix'))
                    break

print(f"Found {len(overlaps)} overlaps:")
for si, li, pos, length, otype in overlaps[:20]:
    print(f"  Book {si} ({len(books[si])}d) {otype} in Book {li} ({len(books[li])}d) at pos {pos}")
    print(f"    Offset book {si}: {book_offsets[si]}, book {li}: {book_offsets[li]}")
    if otype == 'contained':
        # Check if the position parity matches the offset expectations
        off_si = book_offsets[si]
        off_li = book_offsets[li]
        # If book si starts at position pos within book li,
        # then pair boundary of si within li starts at pos+off_si
        # While li's pair boundary is off_li
        # For consistency: (pos + off_si) % 2 should equal off_li % 2
        # if the pair boundaries align
        parity_match = (pos + off_si) % 2 == off_li % 2
        print(f"    Parity match: {parity_match} (pos={pos}, off_si={off_si}, off_li={off_li})")


print("\n" + "=" * 70)
print("2. CRIB EXTRACTION FROM BEST MAPPING")
print("=" * 70)

# Build book pairs
book_pairs_list = []
for i, book in enumerate(books):
    off = book_offsets[i]
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs_list.append(pairs)

# Decode each book and find word occurrences
all_pairs = []
for bp in book_pairs_list:
    all_pairs.extend(bp)

decoded_full = ''.join(mapping.get(p, '?') for p in all_pairs)

# Build reverse mapping
reverse_map = {}
for code, letter in mapping.items():
    if letter not in reverse_map:
        reverse_map[letter] = []
    reverse_map[letter].append(code)

# Find STEIN occurrences
target_words = ['STEIN', 'ENDE', 'EINE', 'EINER', 'NICHT', 'AUCH', 'NACH']

for word in target_words:
    positions = []
    start = 0
    while True:
        pos = decoded_full.find(word, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1

    if positions:
        print(f"\n  '{word}' found {len(positions)} times:")
        for pos in positions:
            # Extract the underlying digit pairs
            pair_sequence = all_pairs[pos:pos+len(word)]
            print(f"    Position {pos}: pairs={pair_sequence}")
            # Show surrounding context
            ctx_start = max(0, pos-3)
            ctx_end = min(len(decoded_full), pos+len(word)+3)
            context = decoded_full[ctx_start:ctx_end]
            highlight = '.' * (pos - ctx_start) + word + '.' * (ctx_end - pos - len(word))
            print(f"    Context: '{context}'")
            print(f"             '{highlight}'")


print("\n" + "=" * 70)
print("3. CODE CONSISTENCY CHECK")
print("=" * 70)

# For each letter, check which codes map to it and their frequencies
pair_counts = Counter(all_pairs)
for letter in sorted(german.keys(), key=lambda l: -german[l]):
    codes = sorted(reverse_map.get(letter, []))
    if codes:
        freqs = [(c, pair_counts.get(c, 0)) for c in codes]
        total = sum(f for _, f in freqs)
        pct = total / len(all_pairs) * 100
        exp = german[letter] * 100
        print(f"  {letter} ({exp:.1f}% exp, {pct:.1f}% obs): {freqs}")


print("\n" + "=" * 70)
print("4. DIGIT PAIR FREQUENCY DISTRIBUTION")
print("=" * 70)

# Show all 98 pairs sorted by frequency
sorted_codes = sorted(pair_counts.items(), key=lambda x: -x[1])
print(f"Total pairs: {len(all_pairs)}, unique: {len(pair_counts)}")
print(f"\nCode frequencies (top 30):")
for code, count in sorted_codes[:30]:
    pct = count / len(all_pairs) * 100
    letter = mapping.get(code, '?')
    print(f"  '{code}' -> {letter}: {count} ({pct:.2f}%)")

print(f"\nCode frequencies (bottom 30):")
for code, count in sorted_codes[-30:]:
    pct = count / len(all_pairs) * 100
    letter = mapping.get(code, '?')
    print(f"  '{code}' -> {letter}: {count} ({pct:.2f}%)")

# Check if any pair is missing
all_possible = set(f"{i:02d}" for i in range(100))
present = set(pair_counts.keys())
missing = all_possible - present
print(f"\nMissing pairs: {sorted(missing)}")


print("\n" + "=" * 70)
print("5. BOOK STRUCTURE: CIRCULAR/REPEATING PATTERN")
print("=" * 70)

# Check if books are fragments of a longer circular text
# Concatenate longest books and look for repetition
longest_books = sorted(range(len(books)), key=lambda i: -len(books[i]))

# Check if the concatenated digit sequence of all books contains
# a single repeated cycle
all_digits = ''.join(books)
print(f"Total digits across all books: {len(all_digits)}")
print(f"Unique digits: {len(set(all_digits))}")

# Check for a master text that all books are fragments of
# Try building it from overlaps
master_candidates = []
for li in longest_books[:5]:
    master = books[li]
    extended = True
    while extended:
        extended = False
        for i in range(len(books)):
            if i == li:
                continue
            # Check if book i overlaps with current master
            for k in range(min(len(books[i]), len(master)), 10, -1):
                # book i's suffix = master's prefix
                if books[i][-k:] == master[:k]:
                    master = books[i][:-k] + master
                    extended = True
                    break
                # master's suffix = book i's prefix
                if master[-k:] == books[i][:k]:
                    master = master + books[i][k:]
                    extended = True
                    break

    master_candidates.append((li, len(master), master))
    if len(master) > 500:
        break

for li, mlen, master in master_candidates[:3]:
    print(f"\n  Starting from book {li}: master length = {mlen} digits")
    # Check how many books are contained in this master
    contained = 0
    for i in range(len(books)):
        if master.find(books[i]) >= 0:
            contained += 1
    print(f"  Books contained: {contained}/{len(books)}")

    if contained > 50:
        print(f"  Master text (first 200 digits): {master[:200]}")
        # Decode master with offset 0
        mpairs0 = [master[j:j+2] for j in range(0, len(master)-1, 2)]
        decoded0 = ''.join(mapping.get(p, '?') for p in mpairs0)
        print(f"  Decoded (off=0, first 200): {decoded0[:200]}")
        # And offset 1
        mpairs1 = [master[j:j+2] for j in range(1, len(master)-1, 2)]
        decoded1 = ''.join(mapping.get(p, '?') for p in mpairs1)
        print(f"  Decoded (off=1, first 200): {decoded1[:200]}")


print("\n" + "=" * 70)
print("6. ALTERNATIVE: TRY SINGLE GLOBAL OFFSET")
print("=" * 70)

# What if ALL books use the same offset?
# Try offset 0 for all
for global_off in [0, 1]:
    all_p = []
    for book in books:
        pairs = [book[j:j+2] for j in range(global_off, len(book)-1, 2)]
        all_p.extend(pairs)

    pc = Counter(all_p)
    ic = ic_from_counts(pc, len(all_p))

    decoded = ''.join(mapping.get(p, '?') for p in all_p)

    # Count German words
    n_german = 0
    for word in ['DER', 'DIE', 'DAS', 'UND', 'IST', 'EIN', 'DEN', 'DES', 'SIE', 'ICH']:
        n_german += decoded.count(word)

    print(f"\n  Global offset {global_off}: IC={ic*100:.3f}, German words={n_german}")
    print(f"    First 200 decoded: {decoded[:200]}")


print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
