"""
Tibia 469 Bonelord Language - Comprehensive Analysis
=====================================================
Analyzing the 71 Hellgate Library books to find patterns
that might help decode the mysterious numerical cipher.
"""

import json
import math
from collections import Counter, defaultdict
from itertools import product as iter_product

# Load books
with open("books.json", "r") as f:
    books = json.load(f)

print("=" * 70)
print("TIBIA 469 BONELORD LANGUAGE - ANALYSIS REPORT")
print("=" * 70)

# ============================================================
# 1. BASIC STATISTICS
# ============================================================
print("\n" + "=" * 70)
print("1. BASIC STATISTICS")
print("=" * 70)

all_digits = "".join(books)
total_digits = len(all_digits)
print(f"\nTotal books: {len(books)}")
print(f"Total digits: {total_digits}")
print(f"Shortest book: {min(len(b) for b in books)} digits (Book {min(range(len(books)), key=lambda i: len(books[i]))+1})")
print(f"Longest book: {max(len(b) for b in books)} digits (Book {max(range(len(books)), key=lambda i: len(books[i]))+1})")
print(f"Average book length: {total_digits/len(books):.1f} digits")

# Digit frequency analysis
print("\n--- Global Digit Frequency ---")
digit_counts = Counter(all_digits)
for d in "0123456789":
    count = digit_counts[d]
    pct = count / total_digits * 100
    bar = "#" * int(pct * 2)
    print(f"  {d}: {count:5d} ({pct:5.2f}%) {bar}")

# Global average
digit_sum = sum(int(d) for d in all_digits)
global_avg = digit_sum / total_digits
print(f"\nGlobal digit sum: {digit_sum}")
print(f"Global average: {global_avg:.6f}")

# Per-book averages
print("\n--- Per-Book Averages ---")
book_avgs = []
for i, book in enumerate(books):
    avg = sum(int(d) for d in book) / len(book)
    book_avgs.append(avg)

book_avgs_sorted = sorted(enumerate(book_avgs), key=lambda x: x[1])
print(f"Min avg: Book {book_avgs_sorted[0][0]+1} = {book_avgs_sorted[0][1]:.6f}")
print(f"Max avg: Book {book_avgs_sorted[-1][0]+1} = {book_avgs_sorted[-1][1]:.6f}")
print(f"All start with 4.xxxx: {all(str(a).startswith('4.') for a in book_avgs)}")

# Find book pairs with same average
print("\n--- Book Pairs with Identical Averages ---")
avg_groups = defaultdict(list)
for i, avg in enumerate(book_avgs):
    avg_groups[f"{avg:.10f}"].append(i + 1)
for avg_str, book_nums in avg_groups.items():
    if len(book_nums) > 1:
        print(f"  Average {avg_str}: Books {book_nums}")

# ============================================================
# 2. N-GRAM ANALYSIS (pairs, triplets, quads)
# ============================================================
print("\n" + "=" * 70)
print("2. N-GRAM FREQUENCY ANALYSIS")
print("=" * 70)

for n in [2, 3, 4, 5]:
    ngrams = Counter()
    for book in books:
        for i in range(len(book) - n + 1):
            ngrams[book[i:i+n]] += 1

    print(f"\n--- {n}-gram: Top 20 most frequent ---")
    for gram, count in ngrams.most_common(20):
        print(f"  '{gram}': {count}")

    # How many unique n-grams
    total_possible = 10 ** n
    print(f"  Unique {n}-grams found: {len(ngrams)} / {total_possible} possible ({len(ngrams)/total_possible*100:.1f}%)")

# ============================================================
# 3. SEARCH FOR KEY SEQUENCES
# ============================================================
print("\n" + "=" * 70)
print("3. KEY SEQUENCE SEARCH")
print("=" * 70)

key_sequences = {
    "469": "The language name",
    "3478": "Recurring key (Knightmare NPC, Honeminas)",
    "4315": "Honeminas vector 1 prefix",
    "43153": "Honeminas vector (4,3,1,5,3)",
    "34784": "Honeminas vector (3,4,7,8,4)",
    "486486": "Wrinkled Bonelord's name",
    "486": "Bonelord name fragment",
    "1234": "Sequential test",
    "0000": "Quad zeros",
    "9999": "Quad nines",
    "666": "Devil number",
    "1111": "Quad ones",
}

for seq, desc in key_sequences.items():
    occurrences = []
    for i, book in enumerate(books):
        pos = 0
        while True:
            pos = book.find(seq, pos)
            if pos == -1:
                break
            occurrences.append((i + 1, pos))
            pos += 1
    print(f"  '{seq}' ({desc}): {len(occurrences)} occurrences")
    if occurrences and len(occurrences) <= 10:
        for book_num, pos in occurrences:
            print(f"    Book {book_num}, position {pos}")

# ============================================================
# 4. DIGIT PAIR FREQUENCY (potential homophonic cipher)
# ============================================================
print("\n" + "=" * 70)
print("4. HOMOPHONIC CIPHER ANALYSIS (digit pairs)")
print("=" * 70)

# English letter frequency (approximate)
english_freq = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0,
    'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3,
    'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4, 'W': 2.4,
    'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5,
    'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
    'Z': 0.07
}

# Analyze all digit pairs (assuming text is read as consecutive pairs)
# Try both even-aligned and odd-aligned pairing
for offset_name, offset in [("even-aligned (0,2,4...)", 0), ("odd-aligned (1,3,5...)", 1)]:
    print(f"\n--- Digit pairs, {offset_name} ---")
    pair_counts = Counter()
    for book in books:
        for i in range(offset, len(book) - 1, 2):
            pair_counts[book[i:i+2]] += 1

    total_pairs = sum(pair_counts.values())
    print(f"  Total pairs: {total_pairs}")
    print(f"  Unique pairs: {len(pair_counts)} / 100 possible")

    # Top pairs
    print(f"  Top 15 pairs:")
    for pair, count in pair_counts.most_common(15):
        pct = count / total_pairs * 100
        print(f"    '{pair}': {count} ({pct:.2f}%)")

    # Bottom pairs (least frequent)
    print(f"  Bottom 10 pairs:")
    for pair, count in pair_counts.most_common()[-10:]:
        pct = count / total_pairs * 100
        print(f"    '{pair}': {count} ({pct:.2f}%)")

# ============================================================
# 5. ENTROPY ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("5. ENTROPY ANALYSIS")
print("=" * 70)

def shannon_entropy(text, n=1):
    """Calculate Shannon entropy for n-grams."""
    ngrams = [text[i:i+n] for i in range(len(text) - n + 1)]
    counts = Counter(ngrams)
    total = len(ngrams)
    entropy = -sum((c/total) * math.log2(c/total) for c in counts.values())
    return entropy

# Global entropy
print(f"\nGlobal single-digit entropy: {shannon_entropy(all_digits, 1):.4f} bits (max for 10 symbols = {math.log2(10):.4f})")
print(f"Global digram entropy: {shannon_entropy(all_digits, 2):.4f} bits (max for 100 symbols = {math.log2(100):.4f})")
print(f"Global trigram entropy: {shannon_entropy(all_digits, 3):.4f} bits (max for 1000 symbols = {math.log2(1000):.4f})")

# Per-book entropy
print("\n--- Per-Book Single-Digit Entropy ---")
for i, book in enumerate(books):
    if len(book) > 20:  # need enough data
        ent = shannon_entropy(book, 1)
        print(f"  Book {i+1:2d} ({len(book):3d} digits): entropy = {ent:.4f}")

# ============================================================
# 6. SHARED SUBSEQUENCES BETWEEN BOOKS
# ============================================================
print("\n" + "=" * 70)
print("6. LONGEST SHARED SUBSEQUENCES (between books)")
print("=" * 70)

def longest_common_substring(s1, s2):
    """Find longest common substring between two strings."""
    m, n = len(s1), len(s2)
    longest = 0
    end_pos = 0
    # Use rolling approach to save memory
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                curr[j] = prev[j-1] + 1
                if curr[j] > longest:
                    longest = curr[j]
                    end_pos = i
            else:
                curr[j] = 0
        prev, curr = curr, [0] * (n + 1)
    return s1[end_pos - longest:end_pos], longest

# Find top overlaps (sample - doing all pairs would be slow)
print("\nComputing longest common substrings between all book pairs...")
print("(showing pairs with overlap >= 20 digits)\n")

overlaps = []
for i in range(len(books)):
    for j in range(i + 1, len(books)):
        substr, length = longest_common_substring(books[i], books[j])
        if length >= 20:
            overlaps.append((i+1, j+1, length, substr))

overlaps.sort(key=lambda x: -x[2])
for book_a, book_b, length, substr in overlaps[:30]:
    print(f"  Books {book_a:2d} & {book_b:2d}: {length} digits - '{substr[:50]}{'...' if len(substr) > 50 else ''}'")

print(f"\nTotal pairs with overlap >= 20: {len(overlaps)}")

# ============================================================
# 7. HONEMINAS FORMULA ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("7. HONEMINAS FORMULA ANALYSIS")
print("=" * 70)

# The Honeminas formula: g[a_,x_] := a g[3,2] + (4,3,1,5,3).(3,4,7,8,4)
# Dot product of (4,3,1,5,3) and (3,4,7,8,4) = 4*3 + 3*4 + 1*7 + 5*8 + 3*4 = 12+12+7+40+12 = 83
v1 = [4, 3, 1, 5, 3]
v2 = [3, 4, 7, 8, 4]
dot_product = sum(a*b for a, b in zip(v1, v2))
print(f"\nVector 1: {v1}")
print(f"Vector 2: {v2}")
print(f"Dot product: {dot_product}")

# Search for these vectors as subsequences
v1_str = "".join(str(x) for x in v1)  # "43153"
v2_str = "".join(str(x) for x in v2)  # "34784"
print(f"\nVector 1 as string '{v1_str}' occurrences in books:")
for i, book in enumerate(books):
    count = book.count(v1_str)
    if count > 0:
        print(f"  Book {i+1}: {count} times")

print(f"\nVector 2 as string '{v2_str}' occurrences in books:")
for i, book in enumerate(books):
    count = book.count(v2_str)
    if count > 0:
        print(f"  Book {i+1}: {count} times")

# ============================================================
# 8. MODULAR ARITHMETIC PATTERNS
# ============================================================
print("\n" + "=" * 70)
print("8. MODULAR ARITHMETIC PATTERNS")
print("=" * 70)

# Check if digit sums mod various numbers reveal patterns
for mod in [5, 7, 10, 13, 26]:
    print(f"\n--- Book digit sums mod {mod} ---")
    mod_values = []
    for i, book in enumerate(books):
        s = sum(int(d) for d in book)
        mod_val = s % mod
        mod_values.append(mod_val)

    mod_freq = Counter(mod_values)
    print(f"  Distribution: {dict(sorted(mod_freq.items()))}")

# ============================================================
# 9. ATTEMPT: SIMPLE PAIR-TO-LETTER MAPPING
# ============================================================
print("\n" + "=" * 70)
print("9. BRUTE FORCE: IF PAIRS MAP TO LETTERS, WHAT'S THE DISTRIBUTION?")
print("=" * 70)

# If the text is a homophonic cipher with digit pairs -> letters,
# we expect roughly 26 distinct "frequency levels"
# Let's see how the 100 possible pairs distribute

all_text = "".join(books)
# Try reading as pairs from start
pair_freq = Counter()
for i in range(0, len(all_text) - 1, 2):
    pair_freq[all_text[i:i+2]] += 1

# Sort by frequency
sorted_pairs = pair_freq.most_common()
total = sum(c for _, c in sorted_pairs)

print(f"\nAll 100 possible pairs, sorted by frequency:")
print(f"{'Pair':>4} {'Count':>6} {'%':>7}  Bar")
print("-" * 50)
for pair, count in sorted_pairs:
    pct = count / total * 100
    bar = "#" * int(pct * 3)
    print(f"  {pair}  {count:5d}  {pct:5.2f}%  {bar}")

# Group pairs into frequency clusters (potential letter groups)
print(f"\nUnique pairs used: {len(pair_freq)}")
print(f"Pairs NOT used: {[f'{a}{b}' for a in '0123456789' for b in '0123456789' if f'{a}{b}' not in pair_freq]}")

# ============================================================
# 10. INDEX OF COINCIDENCE
# ============================================================
print("\n" + "=" * 70)
print("10. INDEX OF COINCIDENCE (cipher type indicator)")
print("=" * 70)

def index_of_coincidence(text, n=1):
    """Calculate IC for n-grams."""
    ngrams = [text[i:i+n] for i in range(len(text) - n + 1)]
    counts = Counter(ngrams)
    N = len(ngrams)
    if N <= 1:
        return 0
    ic = sum(c * (c-1) for c in counts.values()) / (N * (N-1))
    return ic

ic_1 = index_of_coincidence(all_text, 1)
ic_2 = index_of_coincidence(all_text, 2)
print(f"\nIC (single digits): {ic_1:.6f}")
print(f"  Random (10 symbols): {1/10:.6f}")
print(f"  Ratio to random: {ic_1 / (1/10):.4f}")
print(f"\nIC (digit pairs): {ic_2:.6f}")
print(f"  Random (100 symbols): {1/100:.6f}")
print(f"  Ratio to random: {ic_2 / (1/100):.4f}")

# English text IC for comparison
print(f"\n  (English text IC ≈ 0.0667 for single letters)")
print(f"  (Random text IC ≈ 0.0385 for 26 letters)")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
