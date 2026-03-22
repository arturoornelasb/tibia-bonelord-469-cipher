"""
Homophonic substitution with 2-digit pairs.
100 possible pairs -> 26 letters, ~3.85 codes per letter.
IC ratio 1.647 is close to German (1.72).

Strategy:
1. Frequency-rank all 100 pairs
2. Cluster into 26 groups matching German letter frequencies
3. Use simulated annealing to optimize the mapping
4. Verify against Knightmare crib (if applicable)
"""

import json
import random
import math
from collections import Counter

with open('books.json', 'r') as f:
    books = json.load(f)

all_digits = ''.join(books)
n_total = len(all_digits)

# German letter frequencies
german = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
    'Q': 0.001
}

# German bigram frequencies (log, most common)
german_bigrams = {
    'EN': 3.9, 'ER': 3.7, 'CH': 2.8, 'DE': 2.6, 'EI': 2.5,
    'ND': 2.2, 'TE': 2.1, 'IN': 2.1, 'IE': 2.0, 'GE': 1.9,
    'ES': 1.8, 'NE': 1.7, 'UN': 1.7, 'ST': 1.7, 'RE': 1.6,
    'AN': 1.6, 'HE': 1.5, 'BE': 1.4, 'SE': 1.3, 'DI': 1.3,
    'DA': 1.2, 'HA': 1.2, 'SI': 1.2, 'AU': 1.1, 'AL': 1.1,
    'SC': 1.1, 'LE': 1.0, 'VE': 1.0, 'OR': 1.0, 'RA': 1.0
}

# German trigrams
german_trigrams = {
    'EIN': 1.5, 'ICH': 1.4, 'DER': 1.3, 'DIE': 1.3, 'UND': 1.2,
    'DEN': 1.1, 'SCH': 1.1, 'CHE': 1.0, 'GEN': 1.0, 'END': 0.9,
    'TEN': 0.9, 'VER': 0.8, 'BER': 0.8, 'NDE': 0.8, 'DAS': 0.7,
    'ERE': 0.7, 'AUS': 0.7, 'HAT': 0.7, 'STA': 0.7, 'NEN': 0.7
}


print("=" * 70)
print("1. TWO-DIGIT PAIR FREQUENCY ANALYSIS")
print("=" * 70)

# Extract non-overlapping pairs at offset 0 and offset 1
pairs_0 = [all_digits[i:i+2] for i in range(0, n_total - 1, 2)]
pairs_1 = [all_digits[i:i+2] for i in range(1, n_total - 1, 2)]

counts_0 = Counter(pairs_0)
counts_1 = Counter(pairs_1)

# Also look at ALL overlapping pairs for comparison
pairs_all = [all_digits[i:i+2] for i in range(n_total - 1)]
counts_all = Counter(pairs_all)

print(f"\nOffset 0: {len(pairs_0)} pairs, {len(counts_0)} unique")
print(f"Offset 1: {len(pairs_1)} pairs, {len(counts_1)} unique")
print(f"All overlapping: {len(pairs_all)} pairs, {len(counts_all)} unique")

# IC at each offset
def ic_from_counts(counts, total):
    return sum(c * (c - 1) for c in counts.values()) / (total * (total - 1))

ic_0 = ic_from_counts(counts_0, len(pairs_0))
ic_1 = ic_from_counts(counts_1, len(pairs_1))
ic_all = ic_from_counts(counts_all, len(pairs_all))

print(f"\nIC offset 0: {ic_0:.6f} (ratio {ic_0 * 100:.3f})")
print(f"IC offset 1: {ic_1:.6f} (ratio {ic_1 * 100:.3f})")
print(f"IC all pairs: {ic_all:.6f} (ratio {ic_all * 100:.3f})")
print(f"German IC for 100 symbols: ~{1.72/100:.6f}")

# Show pair frequency distribution
print(f"\nTop 20 pairs (offset 0):")
for pair, count in counts_0.most_common(20):
    pct = count / len(pairs_0) * 100
    print(f"  '{pair}': {count} ({pct:.2f}%)")

# Group pairs by frequency rank into clusters
print(f"\nFrequency distribution shape:")
sorted_counts = sorted(counts_0.values(), reverse=True)
for i, c in enumerate(sorted_counts):
    pct = c / len(pairs_0) * 100
    german_rank_pct = list(german.values())[min(i, 25)] * 100 if i < 26 else 0
    bar = '#' * int(pct * 5)
    gbar = '.' * int(german_rank_pct * 5)
    print(f"  Rank {i+1:3d}: {pct:5.2f}% {bar}")
    if i < 26:
        print(f"  German:  {german_rank_pct:5.2f}% {gbar}")
    if i >= 30:
        break


print("\n" + "=" * 70)
print("2. CLUSTER PAIRS INTO 26 LETTERS")
print("=" * 70)

# Strategy: sort pairs by frequency, assign to letters in frequency order
# Each letter gets ceil(100/26) ≈ 4 codes, but adjusted by frequency

# First, let's see if there are natural frequency gaps
sorted_pairs_0 = sorted(counts_0.items(), key=lambda x: -x[1])
print("\nLooking for frequency gaps (natural clusters):")
prev_count = sorted_pairs_0[0][1]
for i, (pair, count) in enumerate(sorted_pairs_0):
    gap = prev_count - count
    if gap > 5:
        print(f"  GAP of {gap} between rank {i} ({prev_count}) and rank {i+1} ({count})")
    prev_count = count

# Compute expected number of codes per letter
print(f"\nExpected codes per letter (100 codes / 26 letters):")
total_pairs = len(pairs_0)
for letter, freq in german.items():
    expected_codes = max(1, round(100 * freq / sum(german.values())))
    expected_count = freq * total_pairs
    print(f"  {letter}: freq={freq:.3f}, expected_count={expected_count:.0f}, approx_codes={expected_codes}")


print("\n" + "=" * 70)
print("3. SIMULATED ANNEALING DECODER")
print("=" * 70)

# Assign each of the 100 two-digit pairs to one of 26 letters
# Optimize the assignment using simulated annealing to maximize:
# 1. German unigram frequency fit
# 2. German bigram frequency fit

def decode_text(pairs, mapping):
    """Decode pairs using mapping dict."""
    return ''.join(mapping.get(p, '?') for p in pairs)

def score_mapping(pairs, mapping, total):
    """Score a mapping based on frequency fit to German."""
    decoded = decode_text(pairs, mapping)

    # Unigram score
    letter_counts = Counter(decoded)
    n = len(decoded)
    uni_score = 0
    for letter, expected_freq in german.items():
        observed_freq = letter_counts.get(letter, 0) / n
        uni_score -= (observed_freq - expected_freq) ** 2

    # Bigram score
    bigram_counts = Counter()
    for i in range(len(decoded) - 1):
        bigram_counts[decoded[i:i+2]] += 1
    n_bi = n - 1
    bi_score = 0
    for bigram, expected_pct in german_bigrams.items():
        observed_pct = bigram_counts.get(bigram, 0) / n_bi * 100
        bi_score -= (observed_pct - expected_pct) ** 2

    return uni_score * 1000 + bi_score * 100

def create_initial_mapping():
    """Create initial mapping: frequency-rank assignment."""
    sorted_pairs = [p for p, c in sorted(counts_0.items(), key=lambda x: -x[1])]
    letters_sorted = [l for l, f in sorted(german.items(), key=lambda x: -x[1])]

    mapping = {}
    # Assign most common pairs to most common letters
    # Each letter gets approximately freq * 100 codes
    pair_idx = 0
    for letter in letters_sorted:
        n_codes = max(1, round(german[letter] * 100))
        for j in range(n_codes):
            if pair_idx < len(sorted_pairs):
                mapping[sorted_pairs[pair_idx]] = letter
                pair_idx += 1

    # Assign remaining pairs
    while pair_idx < len(sorted_pairs):
        # Assign to least-assigned letter
        letter_code_counts = Counter(mapping.values())
        least_letter = min(letters_sorted, key=lambda l: letter_code_counts.get(l, 0))
        mapping[sorted_pairs[pair_idx]] = least_letter
        pair_idx += 1

    return mapping

# Run simulated annealing
print("\nRunning simulated annealing (10 restarts, 50000 iterations each)...")

best_global_score = float('-inf')
best_global_mapping = None

for restart in range(10):
    if restart == 0:
        mapping = create_initial_mapping()
    else:
        # Random restart
        all_pair_codes = list(counts_0.keys())
        letters = list(german.keys())
        mapping = {p: random.choice(letters) for p in all_pair_codes}

    current_score = score_mapping(pairs_0[:2000], mapping, len(pairs_0[:2000]))
    best_score = current_score
    best_mapping = dict(mapping)

    T = 10.0
    for iteration in range(50000):
        # Pick two random pairs and swap their letter assignments
        p1, p2 = random.sample(list(mapping.keys()), 2)
        mapping[p1], mapping[p2] = mapping[p2], mapping[p1]

        new_score = score_mapping(pairs_0[:2000], mapping, len(pairs_0[:2000]))

        # Accept or reject
        delta = new_score - current_score
        if delta > 0 or random.random() < math.exp(delta / T):
            current_score = new_score
            if current_score > best_score:
                best_score = current_score
                best_mapping = dict(mapping)
        else:
            # Revert
            mapping[p1], mapping[p2] = mapping[p2], mapping[p1]

        T *= 0.99995

    if best_score > best_global_score:
        best_global_score = best_score
        best_global_mapping = dict(best_mapping)

    if restart % 3 == 0:
        print(f"  Restart {restart}: best score = {best_score:.2f}")

print(f"\nBest global score: {best_global_score:.2f}")

# Show the best mapping
print(f"\nBest mapping:")
mapping_by_letter = {}
for pair, letter in sorted(best_global_mapping.items()):
    if letter not in mapping_by_letter:
        mapping_by_letter[letter] = []
    mapping_by_letter[letter].append(pair)

for letter in sorted(mapping_by_letter.keys()):
    codes = mapping_by_letter[letter]
    total_count = sum(counts_0[c] for c in codes)
    pct = total_count / len(pairs_0) * 100
    print(f"  {letter} ({german[letter]*100:.1f}%): {codes} -> {pct:.1f}%")

# Decode first part of text
decoded = decode_text(pairs_0[:200], best_global_mapping)
print(f"\nDecoded text (first 400 digits / 200 pairs):")
print(f"  {decoded}")

# Check for German words
print(f"\nGerman word search in decoded text:")
decoded_full = decode_text(pairs_0, best_global_mapping)
common_words = ['DER', 'DIE', 'DAS', 'UND', 'IST', 'EIN', 'DEN', 'VON',
                'HAT', 'FUR', 'AUF', 'MIT', 'DEM', 'SIE', 'ICH', 'SIND',
                'AUS', 'BEI', 'TOD', 'HAT', 'RUNE', 'STEIN', 'MAGIE']

for word in common_words:
    count = decoded_full.count(word)
    expected = len(decoded_full) * (1/26) ** len(word)
    ratio = count / expected if expected > 0 else 0
    if count > 0:
        print(f"  '{word}': {count} times (expected {expected:.1f}, ratio {ratio:.1f}x)")


print("\n" + "=" * 70)
print("4. OFFSET SENSITIVITY TEST")
print("=" * 70)

# The key question: does the encoding start at offset 0 or offset 1?
# Test both and compare scores

# Re-run SA for offset 1
mapping_1 = create_initial_mapping()  # Reuse frequency-based initial mapping
# But remap to offset 1 counts
sorted_pairs_1 = [p for p, c in sorted(counts_1.items(), key=lambda x: -x[1])]
letters_sorted = [l for l, f in sorted(german.items(), key=lambda x: -x[1])]

mapping_1 = {}
pair_idx = 0
for letter in letters_sorted:
    n_codes = max(1, round(german[letter] * 100))
    for j in range(n_codes):
        if pair_idx < len(sorted_pairs_1):
            mapping_1[sorted_pairs_1[pair_idx]] = letter
            pair_idx += 1
while pair_idx < len(sorted_pairs_1):
    letter_code_counts = Counter(mapping_1.values())
    least_letter = min(letters_sorted, key=lambda l: letter_code_counts.get(l, 0))
    mapping_1[sorted_pairs_1[pair_idx]] = least_letter
    pair_idx += 1

score_0 = score_mapping(pairs_0[:2000], best_global_mapping, 2000)
score_1 = score_mapping(pairs_1[:2000], mapping_1, 2000)

print(f"Score at offset 0: {score_0:.2f}")
print(f"Score at offset 1: {score_1:.2f}")

decoded_1 = decode_text(pairs_1[:200], mapping_1)
print(f"\nDecoded at offset 1 (first 200 pairs):")
print(f"  {decoded_1}")


print("\n" + "=" * 70)
print("5. EACH BOOK SEPARATELY - ALIGNMENT TEST")
print("=" * 70)

# If books start at different offsets, the pair alignment varies per book
# Test: does decoding quality differ by book?

print(f"\nPer-book IC at offset 0 vs offset 1:")
for i, book in enumerate(books[:20]):
    bp0 = [book[j:j+2] for j in range(0, len(book) - 1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book) - 1, 2)]

    if len(bp0) < 5 or len(bp1) < 5:
        continue

    ic0 = ic_from_counts(Counter(bp0), len(bp0))
    ic1 = ic_from_counts(Counter(bp1), len(bp1))

    better = "OFF0" if ic0 > ic1 else "OFF1"
    print(f"  Book {i:2d} ({len(book):3d} digits): IC0={ic0:.5f} IC1={ic1:.5f} [{better}]")


print("\n" + "=" * 70)
print("6. KNIGHTMARE CRIB WITH 2-DIGIT PAIRS")
print("=" * 70)

# If the encoding is 2-digit pairs, the 24-digit Knightmare splits into 12 pairs
# But plaintext is 17 letters. 12 != 17, so fixed 2-digit pairs DON'T work for Knightmare!

km = "347867908719766434660345"
km_pairs_0 = [km[i:i+2] for i in range(0, len(km) - 1, 2)]
km_pairs_1 = [km[i:i+2] for i in range(1, len(km) - 1, 2)]

print(f"\nKnightmare at offset 0: {km_pairs_0} ({len(km_pairs_0)} pairs vs 17 letters)")
print(f"Knightmare at offset 1: {km_pairs_1} ({len(km_pairs_1)} pairs vs 17 letters)")

# 12 pairs for 17 letters is impossible for fixed-length 2-digit encoding
# Unless the Knightmare uses a DIFFERENT encoding format

# BUT: what about the 27-digit version?
km27 = "347867090871097664346600345"
km27_pairs_0 = [km27[i:i+2] for i in range(0, len(km27) - 1, 2)]
# 27 digits -> 13 pairs (with 1 leftover) at offset 0
print(f"\nKnightmare-27 at offset 0: {km27_pairs_0} ({len(km27_pairs_0)} pairs)")
# Still only 13, not 17

# What if SOME digits are standalone (like digit 0)?
# That's back to variable-length encoding

# Actually, the 27/24 digit versions give 13.5/12 pairs, neither is 17
# The only way to get 17 from 24 is variable-length (avg 1.41 digits/letter)
# The only way to get 17 from 27 is variable-length (avg 1.59 digits/letter)
print(f"\n24 digits / 17 letters = {24/17:.3f} digits per letter")
print(f"27 digits / 17 letters = {27/17:.3f} digits per letter")
print(f"If all 2-digit: need {17*2} = 34 digits (have 24/27)")
print(f"Conclusion: fixed 2-digit pairs CANNOT encode the Knightmare crib")

# However! Maybe the Knightmare NPC text is formatted differently from the books
# The books might use 2-digit pairs while the NPC adds word separators/padding
print(f"\nBut the books might use 2-digit pairs even if NPC text is different!")
print(f"Corpus avg: {n_total} digits / ({n_total}//2) = {n_total//2} pairs")
print(f"If each pair = 1 letter: {n_total//2} letters")
print(f"Avg German word length: ~5.5 letters, so ~{n_total//2/5.5:.0f} words")


print("\n" + "=" * 70)
print("7. TRIGRAM AND QUADGRAM ANALYSIS OF DECODED TEXT")
print("=" * 70)

# Use the best mapping to decode and analyze n-gram structure
decoded_full = decode_text(pairs_0, best_global_mapping)

# Trigram frequency
tri_counts = Counter()
for i in range(len(decoded_full) - 2):
    tri_counts[decoded_full[i:i+3]] += 1

print(f"\nTop 20 decoded trigrams:")
for tri, count in tri_counts.most_common(20):
    in_german = tri in german_trigrams
    print(f"  '{tri}': {count} {'<-- German trigram!' if in_german else ''}")

# Letter frequency of decoded text
letter_counts = Counter(decoded_full)
print(f"\nDecoded letter frequencies vs German:")
for letter, freq in sorted(german.items(), key=lambda x: -x[1]):
    obs_pct = letter_counts.get(letter, 0) / len(decoded_full) * 100
    exp_pct = freq * 100
    diff = obs_pct - exp_pct
    bar = '#' * int(obs_pct * 3)
    print(f"  {letter}: obs={obs_pct:5.1f}% exp={exp_pct:5.1f}% (diff={diff:+5.1f}%) {bar}")


print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
