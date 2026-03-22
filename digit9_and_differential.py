"""
Tibia 469 - Digit 9 Special Role + Differential Encoding
==========================================================
Key finding: Digit 9 has extreme transition asymmetry (0.583).
What comes BEFORE 9 is very constrained; what follows 9 is diverse.
This suggests 9 may function as a structural element.

Also testing: differential encoding (digit - previous digit, mod 10)
"""

import json
from collections import Counter, defaultdict
import math

with open("books.json", "r") as f:
    books = json.load(f)

all_text = "".join(books)

print("=" * 70)
print("DIGIT 9 SPECIAL ROLE + DIFFERENTIAL ENCODING ANALYSIS")
print("=" * 70)

# ============================================================
# 1. DIGIT 9 IN DEPTH
# ============================================================
print("\n" + "=" * 70)
print("1. DIGIT 9 - WHAT COMES BEFORE AND AFTER?")
print("=" * 70)

for focus_digit in ['9', '3', '0']:
    print(f"\n--- Focus digit: {focus_digit} ---")

    before = Counter()
    after = Counter()
    for i in range(len(all_text)):
        if all_text[i] == focus_digit:
            if i > 0:
                before[all_text[i-1]] += 1
            if i < len(all_text) - 1:
                after[all_text[i+1]] += 1

    print(f"  What comes BEFORE {focus_digit}:")
    total_b = sum(before.values())
    for d in "0123456789":
        count = before.get(d, 0)
        pct = count / total_b * 100 if total_b > 0 else 0
        bar = '#' * int(pct / 2)
        print(f"    {d}: {count:4d} ({pct:5.1f}%) {bar}")

    print(f"  What comes AFTER {focus_digit}:")
    total_a = sum(after.values())
    for d in "0123456789":
        count = after.get(d, 0)
        pct = count / total_a * 100 if total_a > 0 else 0
        bar = '#' * int(pct / 2)
        print(f"    {d}: {count:4d} ({pct:5.1f}%) {bar}")

# ============================================================
# 2. DIGIT ROLES: WHICH DIGITS PREFER CERTAIN POSITIONS?
# ============================================================
print("\n" + "=" * 70)
print("2. DIGIT ROLE ANALYSIS")
print("=" * 70)

# For each digit, what's its preferred context?
# Group digits by their transition behavior
print("\n--- Clustering digits by transition behavior ---")

# Create feature vectors for each digit based on transitions
for d in "0123456789":
    # What follows this digit?
    after_vec = []
    total = 0
    for d2 in "0123456789":
        c = 0
        for i in range(len(all_text) - 1):
            if all_text[i] == d and all_text[i+1] == d2:
                c += 1
        after_vec.append(c)
        total += c

    if total > 0:
        after_pct = [v/total*100 for v in after_vec]
    else:
        after_pct = [0]*10

    # Dominant follower
    max_follower = "0123456789"[after_pct.index(max(after_pct))]
    print(f"  Digit {d}: most common follower={max_follower} ({max(after_pct):.1f}%), "
          f"self-follow={after_pct[int(d)]:.1f}%")

# ============================================================
# 3. DIFFERENTIAL ENCODING
# ============================================================
print("\n" + "=" * 70)
print("3. DIFFERENTIAL ENCODING (digit[i] - digit[i-1] mod 10)")
print("=" * 70)

# Compute the difference sequence
diffs = []
for i in range(1, len(all_text)):
    d = (int(all_text[i]) - int(all_text[i-1])) % 10
    diffs.append(str(d))

diff_text = "".join(diffs)

# Frequency of differences
diff_freq = Counter(diff_text)
total_diffs = len(diff_text)
print("\nDifference frequency:")
for d in "0123456789":
    count = diff_freq.get(d, 0)
    pct = count / total_diffs * 100
    bar = '#' * int(pct * 2)
    print(f"  +{d} (mod 10): {count:5d} ({pct:5.1f}%) {bar}")

# Entropy of differences
def entropy(counter):
    total = sum(counter.values())
    if total == 0:
        return 0
    ent = 0
    for count in counter.values():
        if count > 0:
            p = count / total
            ent -= p * math.log2(p)
    return ent

e_orig = entropy(Counter(all_text))
e_diff = entropy(diff_freq)
print(f"\n  Original text entropy: {e_orig:.4f} bits")
print(f"  Difference entropy:   {e_diff:.4f} bits")
print(f"  {'LOWER' if e_diff < e_orig else 'HIGHER'} entropy in differences")

# Transition matrix of differences
print("\n--- Difference transition matrix ---")
diff_trans = Counter()
for i in range(len(diff_text) - 1):
    diff_trans[(diff_text[i], diff_text[i+1])] += 1

# Most/least common diff transitions
print("\nMost common difference transitions:")
for (f, t), count in diff_trans.most_common(10):
    print(f"  +{f} -> +{t}: {count}")

print("\nLeast common difference transitions:")
for (f, t), count in diff_trans.most_common()[-10:]:
    print(f"  +{f} -> +{t}: {count}")

# ============================================================
# 4. LOOKING FOR THE ENCODING UNIT SIZE
# ============================================================
print("\n" + "=" * 70)
print("4. MUTUAL INFORMATION AT DIFFERENT DISTANCES")
print("=" * 70)

# If the encoding unit is K digits, then digits K apart should have
# LOW mutual information (they're in different code units)
# while digits < K apart should have HIGH MI

def mutual_information(text, distance):
    """Compute MI between digit[i] and digit[i+distance]."""
    joint = Counter()
    marginal_a = Counter()
    marginal_b = Counter()
    for i in range(len(text) - distance):
        a, b = text[i], text[i + distance]
        joint[(a, b)] += 1
        marginal_a[a] += 1
        marginal_b[b] += 1

    total = sum(joint.values())
    mi = 0
    for (a, b), count_ab in joint.items():
        p_ab = count_ab / total
        p_a = marginal_a[a] / total
        p_b = marginal_b[b] / total
        if p_ab > 0 and p_a > 0 and p_b > 0:
            mi += p_ab * math.log2(p_ab / (p_a * p_b))
    return mi

print("\nMutual information between digit[i] and digit[i+k]:")
for k in range(1, 21):
    mi = mutual_information(all_text, k)
    bar = '#' * int(mi * 200)
    print(f"  k={k:2d}: MI={mi:.5f} {bar}")

# ============================================================
# 5. DIGIT PAIR ANALYSIS (SLIDING VS NON-OVERLAPPING)
# ============================================================
print("\n" + "=" * 70)
print("5. ODD vs EVEN POSITION ANALYSIS")
print("=" * 70)

# If the encoding uses 2-digit codes, the statistical properties
# should differ between odd-aligned and even-aligned pairs

even_pairs = Counter()  # positions 0,2,4,...
odd_pairs = Counter()   # positions 1,3,5,...

for book in books:
    for i in range(0, len(book) - 1, 2):
        even_pairs[book[i:i+2]] += 1
    for i in range(1, len(book) - 1, 2):
        odd_pairs[book[i:i+2]] += 1

e_even = entropy(even_pairs)
e_odd = entropy(odd_pairs)

print(f"\n  Even-aligned pair entropy: {e_even:.4f} bits (out of max {math.log2(100):.4f})")
print(f"  Odd-aligned pair entropy:  {e_odd:.4f} bits")
print(f"  Difference: {abs(e_even - e_odd):.4f} bits")

# If even-aligned and odd-aligned have DIFFERENT properties,
# the alignment matters -> the encoding unit starts at even positions
# If they're similar -> either the unit isn't 2 digits, or alignment doesn't matter

print(f"\n  {'Alignment matters!' if abs(e_even - e_odd) > 0.1 else 'No alignment preference -> encoding unit is NOT fixed 2-digit pairs'}")

# Try the same for 3-digit alignment
for offset in range(3):
    trips = Counter()
    for book in books:
        for i in range(offset, len(book) - 2, 3):
            trips[book[i:i+3]] += 1
    e = entropy(trips)
    print(f"  3-digit alignment offset {offset}: entropy = {e:.4f}")

# ============================================================
# 6. LOOKING FOR DIGIT 9 AS A SEPARATOR
# ============================================================
print("\n" + "=" * 70)
print("6. DIGIT 9 AS POTENTIAL SEPARATOR/PREFIX")
print("=" * 70)

# Split at every '9' and analyze the segments
segments_9 = all_text.split('9')
non_empty_9 = [s for s in segments_9 if s]

print(f"\nSplitting at '9': {len(non_empty_9)} segments")
seg_lengths_9 = [len(s) for s in non_empty_9]
print(f"  Length distribution: min={min(seg_lengths_9)}, max={max(seg_lengths_9)}, "
      f"avg={sum(seg_lengths_9)/len(seg_lengths_9):.1f}")

seg_len_dist = Counter(seg_lengths_9)
print(f"\n  Length distribution (count):")
for length in sorted(seg_len_dist.keys()):
    if seg_len_dist[length] >= 3:
        bar = '*' * min(seg_len_dist[length], 50)
        print(f"    {length:3d}: {seg_len_dist[length]:4d} {bar}")

# Most common segments
seg_freq_9 = Counter(non_empty_9)
print(f"\n  Most common segments (between 9s):")
for seg, count in seg_freq_9.most_common(20):
    if count >= 5:
        print(f"    '{seg}' ({len(seg)} digits): {count}x")

# What if 9 is NOT a separator but a PREFIX?
# Then codes would be: 9X, 9XX, etc.
print("\n--- If '9' is a prefix (9X codes) ---")
codes_9x = Counter()
for i in range(len(all_text) - 1):
    if all_text[i] == '9':
        codes_9x[all_text[i:i+2]] += 1

print(f"  9X codes and their frequencies:")
for code in sorted(codes_9x.keys()):
    count = codes_9x[code]
    pct = count / sum(codes_9x.values()) * 100
    print(f"    '{code}': {count:4d} ({pct:5.1f}%)")

# ============================================================
# 7. CONSECUTIVE DIGIT RUNS
# ============================================================
print("\n" + "=" * 70)
print("7. CONSECUTIVE DIGIT RUNS (same digit repeated)")
print("=" * 70)

# Find runs of the same digit
runs = []
current_digit = all_text[0]
run_length = 1
for i in range(1, len(all_text)):
    if all_text[i] == current_digit:
        run_length += 1
    else:
        if run_length >= 2:
            runs.append((current_digit, run_length, i - run_length))
        current_digit = all_text[i]
        run_length = 1

if run_length >= 2:
    runs.append((current_digit, run_length, len(all_text) - run_length))

print(f"\nRuns of repeated digits (length >= 2): {len(runs)}")

run_by_digit = defaultdict(list)
for digit, length, pos in runs:
    run_by_digit[digit].append(length)

for digit in "0123456789":
    if digit in run_by_digit:
        lengths = run_by_digit[digit]
        max_len = max(lengths)
        print(f"  Digit {digit}: {len(lengths):3d} runs, max length {max_len}, "
              f"avg {sum(lengths)/len(lengths):.1f}")
    else:
        print(f"  Digit {digit}:   0 runs")

# The fact that 3->3 appears only ONCE means '33' almost never occurs
# and '333' NEVER occurs. This is very unusual.

# ============================================================
# 8. XOR / ADDITION BASED TRANSFORMATIONS
# ============================================================
print("\n" + "=" * 70)
print("8. ADDITIVE TRANSFORMATIONS")
print("=" * 70)

# What if each digit encodes: (plaintext_value + key_digit) mod 10?
# With a repeating key, this would be a Vigenere-like cipher in mod 10

# Test: for each possible key length, try to find the key
# by frequency analysis on each position

for key_len in [3, 4, 5, 6, 7, 8, 10, 13]:
    # For each position mod key_len, find the most frequent digit
    position_freqs = [Counter() for _ in range(key_len)]
    for i, d in enumerate(all_text):
        position_freqs[i % key_len][d] += 1

    # If this is additive cipher, the most frequent digit at each position
    # should correspond to the most frequent plaintext letter (E in English = ?)
    # In a mod-10 system with 26 letters, we'd need a digit-to-letter mapping first

    # Instead, just check if positional distributions are DIFFERENT
    entropies = [entropy(pf) for pf in position_freqs]
    avg_e = sum(entropies) / len(entropies)
    var_e = sum((e - avg_e)**2 for e in entropies) / len(entropies)

    print(f"  Key length {key_len:2d}: avg entropy={avg_e:.4f}, variance={var_e:.6f}")

# ============================================================
# 9. MODULAR ARITHMETIC PATTERNS
# ============================================================
print("\n" + "=" * 70)
print("9. MODULAR ARITHMETIC PATTERNS")
print("=" * 70)

# Sum of consecutive pairs mod N
for N in [5, 7, 10, 13, 26]:
    sums = []
    for i in range(0, len(all_text) - 1, 2):
        s = (int(all_text[i]) + int(all_text[i+1])) % N
        sums.append(s)

    sum_freq = Counter(sums)
    e = entropy(sum_freq)
    max_e = math.log2(N) if N > 0 else 0
    ratio = e / max_e if max_e > 0 else 0

    print(f"\n  Pair sums mod {N}: entropy={e:.4f} (max={max_e:.4f}, ratio={ratio:.3f})")
    if N <= 10:
        for v in range(N):
            count = sum_freq.get(v, 0)
            pct = count / len(sums) * 100
            print(f"    {v}: {count:4d} ({pct:.1f}%)")

# Product of pairs mod N
for N in [5, 7, 11, 13, 26]:
    prods = []
    for i in range(0, len(all_text) - 1, 2):
        p = (int(all_text[i]) * int(all_text[i+1])) % N
        prods.append(p)

    prod_freq = Counter(prods)
    e = entropy(prod_freq)
    max_e = math.log2(N) if N > 0 else 0
    ratio = e / max_e if max_e > 0 else 0

    print(f"\n  Pair products mod {N}: entropy={e:.4f} (max={max_e:.4f}, ratio={ratio:.3f})")

# ============================================================
# 10. TWO-SYMBOL HYPOTHESIS
# ============================================================
print("\n" + "=" * 70)
print("10. TWO-SYMBOL REDUCTION (high entropy digits = 1, low = 0)")
print("=" * 70)

# What if the digits encode binary through a mapping
# where some digits represent 1 and others 0?

# Find the natural binary split that maximizes structure
from itertools import combinations

best_ic = 0
best_split = None

for n_ones in range(1, 10):
    for ones in combinations("0123456789", n_ones):
        ones_set = set(ones)
        binary = "".join('1' if d in ones_set else '0' for d in all_text)

        # Compute IC of the binary sequence
        ones_count = binary.count('1')
        zeros_count = binary.count('0')
        total = len(binary)
        ic = (ones_count * (ones_count-1) + zeros_count * (zeros_count-1)) / (total * (total-1))

        if ic > best_ic:
            best_ic = ic
            best_split = (ones, binary[:100])

print(f"\nBest binary split (max IC): digits {''.join(best_split[0])} = 1, rest = 0")
print(f"IC = {best_ic:.6f}")
print(f"First 100: {best_split[1]}")

# Try the most natural split: digits above median
# Digit 1 is the most frequent at 16.59%
# If we split at {1,4,5} = most frequent as one group
high_freq_digits = set('145')  # top 3 by frequency
binary_hf = "".join('1' if d in high_freq_digits else '0' for d in all_text)
ones_hf = binary_hf.count('1')
ic_hf = (ones_hf * (ones_hf-1) + (len(binary_hf)-ones_hf) * (len(binary_hf)-ones_hf-1)) / (len(binary_hf) * (len(binary_hf)-1))
print(f"\nHigh-freq split (1,4,5 = 1): IC = {ic_hf:.6f}")
print(f"  1s: {ones_hf} ({ones_hf/len(binary_hf)*100:.1f}%)")

# What about viewing as ternary (0-3=A, 4-6=B, 7-9=C)?
print("\n--- Ternary split (0-3/4-6/7-9) ---")
ternary = []
for d in all_text:
    n = int(d)
    if n <= 3:
        ternary.append('A')
    elif n <= 6:
        ternary.append('B')
    else:
        ternary.append('C')

ternary_text = "".join(ternary)
ternary_freq = Counter(ternary_text)
print(f"  A (0-3): {ternary_freq['A']} ({ternary_freq['A']/len(ternary_text)*100:.1f}%)")
print(f"  B (4-6): {ternary_freq['B']} ({ternary_freq['B']/len(ternary_text)*100:.1f}%)")
print(f"  C (7-9): {ternary_freq['C']} ({ternary_freq['C']/len(ternary_text)*100:.1f}%)")

# IC of ternary
ternary_ic_pairs = Counter()
for i in range(0, len(ternary_text) - 1, 2):
    ternary_ic_pairs[ternary_text[i:i+2]] += 1

e_ternary = entropy(ternary_ic_pairs)
print(f"  Pair entropy: {e_ternary:.4f} (max {math.log2(9):.4f})")
print(f"  Pair frequencies: {dict(ternary_ic_pairs.most_common())}")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
