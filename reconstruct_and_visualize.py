"""
Tibia 469 - Text Reconstruction + Visual/Alternative Analysis
===============================================================
1. Merge overlapping books into the minimal set of sequences
2. Visualize as grids looking for patterns
3. Try German frequency-based decoding
4. Test mathematical transformations
"""

import json
from collections import Counter, defaultdict

with open("books.json", "r") as f:
    books = json.load(f)

print("=" * 70)
print("TIBIA 469 - RECONSTRUCTION & ALTERNATIVE ANALYSIS")
print("=" * 70)

# ============================================================
# 1. FULL RECONSTRUCTION - Merge overlapping books
# ============================================================
print("\n" + "=" * 70)
print("1. FULL TEXT RECONSTRUCTION")
print("=" * 70)

def find_overlap(a, b, min_len=5):
    """Find longest suffix of a that is prefix of b."""
    max_overlap = min(len(a), len(b))
    best = 0
    for length in range(min_len, max_overlap + 1):
        if a.endswith(b[:length]):
            best = length
    return best

# Remove books that are fully contained within other books
print("\nStep 1: Removing contained books...")
contained = set()
for i in range(len(books)):
    for j in range(len(books)):
        if i != j and books[i] in books[j]:
            contained.add(i)

unique_books = [(i, books[i]) for i in range(len(books)) if i not in contained]
print(f"  Removed {len(contained)} contained books")
print(f"  Remaining: {len(unique_books)} unique books")
print(f"  Contained book indices: {sorted(contained)}")

# Build overlap graph on unique books only
print("\nStep 2: Building overlap graph...")
overlaps = []
idx_map = {orig_idx: new_idx for new_idx, (orig_idx, _) in enumerate(unique_books)}

for ni, (oi, bi) in enumerate(unique_books):
    for nj, (oj, bj) in enumerate(unique_books):
        if ni == nj:
            continue
        ov = find_overlap(bi, bj, 5)
        if ov >= 5:
            overlaps.append((ni, nj, ov, oi, oj))

overlaps.sort(key=lambda x: -x[2])

# Greedy chain building
print("\nStep 3: Greedy chain reconstruction...")
best_next = {}
for ni, nj, ov, oi, oj in overlaps:
    if ni not in best_next or ov > best_next[ni][1]:
        best_next[ni] = (nj, ov)

# Build chains
used = set()
chains = []
all_nexts = set(v[0] for v in best_next.values())
starts = [i for i in range(len(unique_books)) if i not in all_nexts]

for start in starts:
    if start in used:
        continue
    chain = [start]
    used.add(start)
    current = start
    while current in best_next:
        next_idx, ov = best_next[current]
        if next_idx in used:
            break
        chain.append(next_idx)
        used.add(next_idx)
        current = next_idx
    chains.append(chain)

# Add isolated
for i in range(len(unique_books)):
    if i not in used:
        chains.append([i])

# Merge each chain
merged_sequences = []
for chain in chains:
    merged = unique_books[chain[0]][1]
    for k in range(1, len(chain)):
        prev_text = unique_books[chain[k-1]][1]
        curr_text = unique_books[chain[k]][1]
        ov = find_overlap(prev_text, curr_text, 1)
        merged += curr_text[ov:]
    orig_indices = [unique_books[idx][0]+1 for idx in chain]
    merged_sequences.append((merged, orig_indices))

print(f"\n  Reconstructed {len(merged_sequences)} sequences:")
for i, (seq, book_nums) in enumerate(merged_sequences):
    print(f"  Sequence {i+1}: {len(seq)} digits from books {book_nums}")

# Total unique content
total_reconstructed = sum(len(s) for s, _ in merged_sequences)
print(f"\n  Total reconstructed content: {total_reconstructed} digits")
print(f"  (vs {sum(len(b) for b in books)} total across all books)")

# Show the longest sequence
longest_seq = max(merged_sequences, key=lambda x: len(x[0]))
print(f"\n--- Longest reconstructed sequence ({len(longest_seq[0])} digits) ---")
print(f"  From books: {longest_seq[1]}")
print(f"  First 200: {longest_seq[0][:200]}")
print(f"  Last 200:  {longest_seq[0][-200:]}")

# ============================================================
# 2. GRID VISUALIZATION
# ============================================================
print("\n" + "=" * 70)
print("2. GRID VISUALIZATION (looking for visual patterns)")
print("=" * 70)

text = longest_seq[0]

# Try various grid widths
for width in [5, 10, 13, 15, 20, 26, 30]:
    print(f"\n--- Width {width} ---")
    rows = [text[i:i+width] for i in range(0, min(len(text), width*15), width)]
    for row in rows:
        # Show digits with spacing for readability
        print(f"  {' '.join(row)}")

# ============================================================
# 3. BASE-5 INTERPRETATION
# ============================================================
print("\n" + "=" * 70)
print("3. BASE-5 (QUINARY) INTERPRETATION")
print("=" * 70)

# Bonelords have 5 eyes - what if digits 0-4 are one system?
# Or what if pairs of digits are base-5 numbers?

print("\n--- Digits 0-4 frequency vs 5-9 frequency ---")
all_text = "".join(books)
low = sum(1 for d in all_text if d in '01234')
high = sum(1 for d in all_text if d in '56789')
print(f"  Digits 0-4: {low} ({low/len(all_text)*100:.1f}%)")
print(f"  Digits 5-9: {high} ({high/len(all_text)*100:.1f}%)")

# What if each digit is base-5 and pairs form base-25 numbers (0-24)?
print("\n--- If pairs of digits are base-5 -> base-25 (A-Y or A-Z) ---")
# Digit X in range 0-4 is valid base-5
# But our digits go 0-9... unless we map them somehow

# Alternative: what if the 5 eyes each blink 0 or 1 (binary)?
# 5 bits = 32 values, enough for 26 letters + 6 extra
# But each digit is 0-9, not 0-1...

# What if digits 0-4 map to binary 0, and 5-9 map to binary 1?
print("\n--- Binary interpretation (0-4=low, 5-9=high) ---")
binary_str = ""
for d in text[:200]:
    if d in '01234':
        binary_str += '0'
    else:
        binary_str += '1'

# Group into 5-bit chunks (for 5 eyes)
print("  First 200 digits as 5-bit groups:")
for i in range(0, min(len(binary_str), 100), 5):
    bits = binary_str[i:i+5]
    if len(bits) == 5:
        val = int(bits, 2)
        if 1 <= val <= 26:
            letter = chr(64 + val)
        else:
            letter = '?'
        print(f"    {text[i:i+5]} -> {bits} -> {val:2d} -> {letter}", end="  ")
        if (i // 5 + 1) % 5 == 0:
            print()
print()

# ============================================================
# 4. DIGIT TRANSITION MATRIX
# ============================================================
print("\n" + "=" * 70)
print("4. DIGIT TRANSITION MATRIX")
print("=" * 70)

# What digit follows what digit? If it's a cipher, certain transitions
# should be more/less common based on letter combinations

transitions = Counter()
for i in range(len(all_text) - 1):
    transitions[(all_text[i], all_text[i+1])] += 1

total_trans = sum(transitions.values())
print("\n  Transition probabilities (row=from, col=to, values in %):")
print("      ", end="")
for to_d in "0123456789":
    print(f"  {to_d:>5}", end="")
print()

for from_d in "0123456789":
    print(f"  {from_d}:", end="")
    row_total = sum(transitions.get((from_d, to_d), 0) for to_d in "0123456789")
    for to_d in "0123456789":
        count = transitions.get((from_d, to_d), 0)
        pct = count / max(row_total, 1) * 100
        print(f"  {pct:5.1f}", end="")
    print()

# Highlight unusual transitions
print("\n  Most common transitions:")
for (f, t), count in transitions.most_common(10):
    print(f"    {f}->{t}: {count} ({count/total_trans*100:.2f}%)")

print("\n  Least common transitions:")
for (f, t), count in transitions.most_common()[-10:]:
    print(f"    {f}->{t}: {count} ({count/total_trans*100:.2f}%)")

# ============================================================
# 5. GERMAN FREQUENCY HILL CLIMB (2-digit pairs)
# ============================================================
print("\n" + "=" * 70)
print("5. GERMAN FREQUENCY-BASED PAIR MAPPING")
print("=" * 70)

GERMAN_FREQ = {
    'E': 16.4, 'N': 9.8, 'I': 7.6, 'S': 7.3, 'R': 7.0,
    'A': 6.5, 'T': 6.2, 'D': 5.1, 'H': 4.8, 'U': 4.3,
    'L': 3.4, 'C': 3.1, 'G': 3.0, 'M': 2.5, 'O': 2.5,
    'B': 1.9, 'W': 1.9, 'F': 1.7, 'K': 1.4, 'Z': 1.1,
    'P': 0.8, 'V': 0.7, 'J': 0.3, 'Y': 0.04, 'X': 0.03,
    'Q': 0.02
}

# Map pairs to German letters proportionally by frequency
pairs = [all_text[i:i+2] for i in range(0, len(all_text)-1, 2)]
pair_freq = Counter(pairs)
sorted_pairs = sorted(pair_freq.items(), key=lambda x: -x[1])

ger_sorted = sorted(GERMAN_FREQ.items(), key=lambda x: -x[1])
total_pairs_count = sum(c for _, c in sorted_pairs)

german_key = {}
pair_idx = 0
print("\nGerman frequency mapping:")
for letter, freq in ger_sorted:
    num_pairs = max(1, round(freq / 100 * len(pair_freq)))
    assigned = []
    for j in range(num_pairs):
        if pair_idx < len(sorted_pairs):
            p = sorted_pairs[pair_idx][0]
            german_key[p] = letter
            assigned.append(p)
            pair_idx += 1
    print(f"  {letter} ({freq:4.1f}%): {', '.join(assigned)}")

# Decode with German mapping
print("\n--- German-decoded books (first 80 chars) ---")
for i in range(min(10, len(books))):
    book_pairs = [books[i][j:j+2] for j in range(0, len(books[i])-1, 2)]
    decoded = "".join(german_key.get(p, '?') for p in book_pairs)
    print(f"  Book {i+1}: {decoded[:80]}")

# Decode NPC dialogues
print("\n--- German-decoded NPC dialogues ---")
npc_texts = {
    "Knightmare": "347867090871097664346600345",
    "Greeting 1": "485611800364197",
    "Greeting 2": "78572611857643646724",
    "Chayenne": "114514519485611451908304576512282177",
    "Elder Bonelord": "65997854764",
}
for name, text in npc_texts.items():
    d_pairs = [text[j:j+2] for j in range(0, len(text)-1, 2)]
    decoded = "".join(german_key.get(p, '?') for p in d_pairs)
    print(f"  {name:>16}: {decoded}")

# ============================================================
# 6. WORD-LENGTH ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("6. LOOKING FOR WORD BOUNDARIES")
print("=" * 70)

# In English text, certain patterns repeat that correspond to common words
# THE, AND, TO, OF, etc. If pairs are the unit, these would be specific
# 4-6 digit sequences

# Find the most frequent fixed-length sequences that could be "words"
print("\n--- Most frequent potential 'words' (assuming 2-digit pairs) ---")
for word_len_pairs in [2, 3, 4, 5]:
    digit_len = word_len_pairs * 2
    print(f"\n  {word_len_pairs}-letter words ({digit_len} digits):")
    seqs = Counter()
    for book in books:
        for i in range(0, len(book) - digit_len + 1, 2):
            seqs[book[i:i+digit_len]] += 1
    for seq, count in seqs.most_common(5):
        # Decode with both mappings
        pairs_list = [seq[j:j+2] for j in range(0, len(seq), 2)]
        decoded = "".join(german_key.get(p, '?') for p in pairs_list)
        print(f"    '{seq}' ({count}x) -> '{decoded}'")

# ============================================================
# 7. PRIME NUMBER / MATHEMATICAL ENCODING TEST
# ============================================================
print("\n" + "=" * 70)
print("7. MATHEMATICAL ENCODING TESTS")
print("=" * 70)

# What if the digits, read as numbers in some way, encode
# ASCII values or other number->letter conversions?

sample = longest_seq[0][:300]

# Test: sliding window of 2 digits as ASCII-related values
print("\n--- 2-digit numbers + 64 = ASCII uppercase ---")
decoded = ""
for i in range(0, min(len(sample), 100), 2):
    n = int(sample[i:i+2])
    # A=65, Z=90 -> need values 65-90, so n+64 or n+65
    if 1 <= n <= 26:
        decoded += chr(n + 64)
    elif n == 0:
        decoded += ' '
    else:
        decoded += '?'
print(f"  Result: {decoded}")

# Test: every 3 digits as a number, mod 26 + 65 = letter
print("\n--- 3-digit numbers mod 26 = letter ---")
decoded = ""
for i in range(0, min(len(sample), 150), 3):
    n = int(sample[i:i+3])
    letter = chr(n % 26 + 65)
    decoded += letter
print(f"  Result: {decoded}")

# Test: Honeminas dot product transformation
print("\n--- Honeminas dot product sliding window ---")
v1 = [4, 3, 1, 5, 3]
v2 = [3, 4, 7, 8, 4]

# Apply dot product to groups of 5 digits
decoded = ""
for i in range(0, min(len(sample), 100), 5):
    group = [int(d) for d in sample[i:i+5]]
    if len(group) == 5:
        # Dot with v1
        dot1 = sum(a*b for a, b in zip(group, v1))
        # Dot with v2
        dot2 = sum(a*b for a, b in zip(group, v2))
        letter1 = chr(dot1 % 26 + 65)
        letter2 = chr(dot2 % 26 + 65)
        decoded += f"({letter1}/{letter2})"
print(f"  Result: {decoded}")

# ============================================================
# 8. VISUAL PATTERN - DIGIT HEAT MAP
# ============================================================
print("\n" + "=" * 70)
print("8. DIGIT DISTRIBUTION HEAT MAP (per position mod N)")
print("=" * 70)

# If there's a repeating structure, digit frequencies should vary by position
for period in [5, 10, 13, 26]:
    print(f"\n--- Period {period} ---")
    pos_counts = [Counter() for _ in range(period)]
    for i, d in enumerate(all_text):
        pos_counts[i % period][d] += 1

    print(f"  Pos:", end="")
    for d in "0123456789":
        print(f"  {d:>4}", end="")
    print()

    for pos in range(period):
        total = sum(pos_counts[pos].values())
        print(f"  {pos:3d}:", end="")
        for d in "0123456789":
            pct = pos_counts[pos].get(d, 0) / max(total, 1) * 100
            # Mark significant deviations
            marker = "*" if abs(pct - 10) > 5 else " "
            print(f" {pct:4.1f}{marker}", end="")
        print()

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
