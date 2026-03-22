"""
Tibia 469 - Homophonic Cipher Cracker
======================================
Attempts to crack the 469 language assuming it's a homophonic
substitution cipher where digit pairs map to English letters.

Strategy:
1. Analyze pair frequency distribution
2. Use hill-climbing with English language scoring
3. Try multiple key sizes and pair alignments
"""

import json
import math
import random
import string
from collections import Counter
from itertools import combinations

# Load books
with open("books.json", "r") as f:
    books = json.load(f)

all_text = "".join(books)

# English letter frequencies (for scoring)
ENGLISH_FREQ = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974,
    'Z': 0.074
}

# English bigram frequencies (log probabilities)
# Top English bigrams for scoring decoded text
COMMON_BIGRAMS = {
    'TH': 3.56, 'HE': 3.07, 'IN': 2.43, 'ER': 2.05, 'AN': 1.99,
    'RE': 1.85, 'ON': 1.76, 'AT': 1.49, 'EN': 1.45, 'ND': 1.35,
    'TI': 1.34, 'ES': 1.34, 'OR': 1.28, 'TE': 1.27, 'OF': 1.17,
    'ED': 1.17, 'IS': 1.13, 'IT': 1.12, 'AL': 1.09, 'AR': 1.07,
    'ST': 1.05, 'TO': 1.05, 'NT': 1.04, 'NG': 0.95, 'SE': 0.93,
    'HA': 0.93, 'AS': 0.87, 'OU': 0.87, 'IO': 0.83, 'LE': 0.83,
    'VE': 0.83, 'CO': 0.79, 'ME': 0.79, 'DE': 0.76, 'HI': 0.76,
    'RI': 0.73, 'RO': 0.73, 'IC': 0.70, 'NE': 0.69, 'EA': 0.69,
    'RA': 0.69, 'CE': 0.65, 'LI': 0.62, 'CH': 0.60, 'LL': 0.58,
    'BE': 0.58, 'MA': 0.57, 'SI': 0.55, 'OM': 0.55, 'UR': 0.54,
}

# Common English trigrams
COMMON_TRIGRAMS = {
    'THE': 3.51, 'AND': 1.59, 'ING': 1.15, 'HER': 0.82, 'HAT': 0.65,
    'HIS': 0.60, 'THA': 0.59, 'ERE': 0.56, 'FOR': 0.55, 'ENT': 0.53,
    'ION': 0.51, 'TER': 0.46, 'WAS': 0.46, 'YOU': 0.44, 'ITH': 0.43,
    'VER': 0.43, 'ALL': 0.42, 'WIT': 0.40, 'THI': 0.39, 'TIO': 0.38,
}

# Common English words for bonus scoring
COMMON_WORDS_3 = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'HIS', 'HAS', 'HIM', 'HOW', 'ITS', 'LET', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'WAY', 'WHO', 'DID', 'GET', 'HAS', 'HIM', 'HIS', 'HOW', 'MAN', 'OUR', 'SAY', 'SHE', 'TWO', 'USE'}
COMMON_WORDS_4 = {'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM', 'THEY', 'BEEN', 'CALL', 'COME', 'EACH', 'MAKE', 'LIKE', 'LONG', 'LOOK', 'MANY', 'SOME', 'TIME', 'VERY', 'WHEN', 'WORD', 'THEM', 'THEN', 'WERE', 'WHAT', 'THERE', 'BONE', 'LORD', 'DEAD', 'EVIL', 'DARK', 'FIRE', 'BOOK', 'FIVE', 'EYES'}


def score_text(text):
    """Score decoded text by how 'English-like' it is."""
    text = text.upper()
    score = 0.0

    # 1. Letter frequency matching
    if len(text) == 0:
        return -999999
    letter_counts = Counter(c for c in text if c.isalpha())
    total_letters = sum(letter_counts.values())
    if total_letters == 0:
        return -999999

    for letter, expected_pct in ENGLISH_FREQ.items():
        observed_pct = letter_counts.get(letter, 0) / total_letters * 100
        score -= abs(observed_pct - expected_pct) * 2

    # 2. Bigram scoring
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        if bigram in COMMON_BIGRAMS:
            score += COMMON_BIGRAMS[bigram] * 5

    # 3. Trigram scoring
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        if trigram in COMMON_TRIGRAMS:
            score += COMMON_TRIGRAMS[trigram] * 10

    # 4. Word bonus (sliding window)
    for w in COMMON_WORDS_3:
        score += text.count(w) * 15
    for w in COMMON_WORDS_4:
        score += text.count(w) * 25

    return score


def extract_pairs(text, offset=0):
    """Extract digit pairs from text starting at given offset."""
    pairs = []
    for i in range(offset, len(text) - 1, 2):
        pairs.append(text[i:i+2])
    return pairs


def decode_with_key(pairs, key):
    """Decode pairs using a key mapping pairs -> letters."""
    return "".join(key.get(p, '?') for p in pairs)


def hill_climb(pairs, iterations=50000, restarts=5):
    """Hill climbing attack on homophonic cipher."""
    best_score = -999999
    best_key = None
    best_text = None

    # Get unique pairs and their frequencies
    pair_counts = Counter(pairs)
    unique_pairs = sorted(pair_counts.keys(), key=lambda p: -pair_counts[p])

    print(f"  Unique pairs: {len(unique_pairs)}")
    print(f"  Total pairs: {len(pairs)}")

    for restart in range(restarts):
        # Initialize with frequency-based assignment
        # Sort pairs by frequency, assign to letters by English frequency
        sorted_letters = sorted(ENGLISH_FREQ.keys(), key=lambda l: -ENGLISH_FREQ[l])

        # Assign multiple pairs per letter based on frequency
        key = {}
        # Simple initial assignment: distribute pairs across letters proportionally
        pairs_per_letter = max(1, len(unique_pairs) // 26)
        for i, pair in enumerate(unique_pairs):
            letter_idx = min(i // max(1, pairs_per_letter), 25)
            key[pair] = sorted_letters[letter_idx]

        # Randomize a bit for diversity across restarts
        if restart > 0:
            keys_list = list(key.keys())
            for _ in range(len(keys_list) // 2):
                i, j = random.sample(range(len(keys_list)), 2)
                key[keys_list[i]], key[keys_list[j]] = key[keys_list[j]], key[keys_list[i]]

        current_text = decode_with_key(pairs, key)
        current_score = score_text(current_text)

        no_improve = 0
        for iteration in range(iterations):
            # Random swap: change what letter a pair maps to
            pair_to_change = random.choice(unique_pairs)
            old_letter = key[pair_to_change]

            # Either swap with another pair's letter or assign random letter
            if random.random() < 0.5:
                other_pair = random.choice(unique_pairs)
                new_letter = key[other_pair]
                key[pair_to_change] = new_letter
                key[other_pair] = old_letter
            else:
                new_letter = random.choice(string.ascii_uppercase)
                key[pair_to_change] = new_letter

            new_text = decode_with_key(pairs, key)
            new_score = score_text(new_text)

            if new_score > current_score:
                current_score = new_score
                current_text = new_text
                no_improve = 0
            else:
                # Revert
                if random.random() < 0.5:
                    key[pair_to_change] = old_letter
                    if 'other_pair' in dir():
                        pass  # swap back handled below
                else:
                    key[pair_to_change] = old_letter
                no_improve += 1

            # Simulated annealing: accept worse solutions early
            if no_improve > 5000:
                break

        if current_score > best_score:
            best_score = current_score
            best_key = dict(key)
            best_text = current_text

        print(f"  Restart {restart+1}/{restarts}: score = {current_score:.1f}")

    return best_key, best_score, best_text


def try_known_mappings():
    """Try decoding with known/proposed mappings from the community."""
    print("\n" + "=" * 70)
    print("TESTING KNOWN COMMUNITY MAPPINGS")
    print("=" * 70)

    # Community theory: 3478 = "BE" or similar common word
    # Knightmare's dialogue decoded as "BE A WIT THAN BE A FOOL!"
    # 3478 67 090871 097664 3466 00 0345!

    # If 34=B, 78=E (from "BE" theory)
    # If 67=A (from spacing)
    # Test these partial mappings

    partial_key = {
        '34': 'B', '78': 'E',  # BE theory
        '67': 'A',  # From NPC dialogue spacing
    }

    print("\nPartial mapping test (34=B, 78=E, 67=A):")
    pairs = extract_pairs(all_text[:200], 0)
    partial_decode = ""
    for p in pairs:
        if p in partial_key:
            partial_decode += partial_key[p]
        else:
            partial_decode += f"[{p}]"
    print(f"  First 100 pairs: {partial_decode[:300]}")


def analyze_pair_distribution():
    """Detailed analysis of pair frequency distribution."""
    print("\n" + "=" * 70)
    print("PAIR DISTRIBUTION ANALYSIS")
    print("=" * 70)

    for offset in [0, 1]:
        pairs = extract_pairs(all_text, offset)
        pair_counts = Counter(pairs)
        total = len(pairs)

        freqs = sorted(pair_counts.values(), reverse=True)

        print(f"\nOffset {offset}:")
        print(f"  Unique pairs: {len(pair_counts)}")
        print(f"  Max frequency: {freqs[0]} ({freqs[0]/total*100:.2f}%)")
        print(f"  Min frequency: {freqs[-1]} ({freqs[-1]/total*100:.2f}%)")
        print(f"  Frequency ratio (max/min): {freqs[0]/max(freqs[-1],1):.1f}")

        # Compare to English: in a homophonic cipher with ~4 pairs per letter,
        # we'd expect frequency clusters
        # Group by frequency ranges
        ranges = [(0, 10), (10, 30), (30, 60), (60, 100), (100, 150), (150, 300)]
        print(f"  Frequency distribution:")
        for lo, hi in ranges:
            count = sum(1 for f in freqs if lo <= f < hi)
            print(f"    {lo:3d}-{hi:3d}: {count} pairs")


def try_fixed_width_decode():
    """Try interpreting as fixed-width number-to-letter (various widths)."""
    print("\n" + "=" * 70)
    print("FIXED-WIDTH DECODE ATTEMPTS")
    print("=" * 70)

    # Try 1-digit, 2-digit, 3-digit groupings
    sample = books[0][:100]  # First book, first 100 chars

    # 1-digit: 0=space?, 1-26 = A-Z (but we have 0-9 only)
    print("\n--- 1-digit mapping (1=A...9=I, 0=space/J) ---")
    mapping_1 = {str(i): chr(64+i) if i > 0 else ' ' for i in range(10)}
    decoded_1 = "".join(mapping_1[d] for d in sample)
    print(f"  Book 1: {decoded_1}")

    # 2-digit: 01-26 = A-Z
    print("\n--- 2-digit mapping (01=A...26=Z, others=?) ---")
    pairs = extract_pairs(sample, 0)
    decoded_2 = ""
    for p in pairs:
        n = int(p)
        if 1 <= n <= 26:
            decoded_2 += chr(64 + n)
        elif n == 0:
            decoded_2 += " "
        else:
            decoded_2 += "?"
    print(f"  Book 1 (offset 0): {decoded_2}")

    pairs = extract_pairs(sample, 1)
    decoded_2b = ""
    for p in pairs:
        n = int(p)
        if 1 <= n <= 26:
            decoded_2b += chr(64 + n)
        elif n == 0:
            decoded_2b += " "
        else:
            decoded_2b += "?"
    print(f"  Book 1 (offset 1): {decoded_2b}")


def try_mirror_theory():
    """Test the mirror number theory: if AB maps to X, then BA also maps to X."""
    print("\n" + "=" * 70)
    print("MIRROR NUMBER THEORY TEST")
    print("=" * 70)

    pairs = extract_pairs(all_text, 0)
    pair_counts = Counter(pairs)

    # For each pair AB, compare frequency with BA
    print("\nComparing pair AB vs BA frequencies:")
    print(f"{'AB':>4} {'freq':>5} | {'BA':>4} {'freq':>5} | {'ratio':>6} | {'similar?':>8}")
    print("-" * 55)

    similar_count = 0
    total_pairs_checked = 0
    for a in range(10):
        for b in range(a+1, 10):
            ab = f"{a}{b}"
            ba = f"{b}{a}"
            f_ab = pair_counts.get(ab, 0)
            f_ba = pair_counts.get(ba, 0)
            if f_ab > 0 and f_ba > 0:
                ratio = max(f_ab, f_ba) / min(f_ab, f_ba)
                similar = ratio < 1.5
                if similar:
                    similar_count += 1
                total_pairs_checked += 1
                if ratio < 2.0:  # Show pairs that are somewhat close
                    print(f"  {ab}  {f_ab:5d} | {ba}  {f_ba:5d} | {ratio:6.2f} | {'YES' if similar else 'no'}")

    print(f"\nPairs where AB ~ BA (ratio < 1.5): {similar_count}/{total_pairs_checked}")


# ============================================================
# RUN ALL ANALYSES
# ============================================================
print("=" * 70)
print("TIBIA 469 - CIPHER CRACKING ATTEMPTS")
print("=" * 70)

# 1. Pair distribution
analyze_pair_distribution()

# 2. Fixed-width decode attempts
try_fixed_width_decode()

# 3. Mirror theory
try_mirror_theory()

# 4. Community mappings
try_known_mappings()

# 5. Hill climbing attack (the main event)
print("\n" + "=" * 70)
print("HILL CLIMBING ATTACK")
print("=" * 70)

for offset in [0]:
    print(f"\n--- Offset {offset} ---")
    pairs = extract_pairs(all_text, offset)

    best_key, best_score, best_text = hill_climb(
        pairs,
        iterations=80000,
        restarts=8
    )

    print(f"\nBest score: {best_score:.1f}")
    print(f"\nKey mapping (pair -> letter):")
    # Sort by letter
    by_letter = {}
    for pair, letter in sorted(best_key.items()):
        if letter not in by_letter:
            by_letter[letter] = []
        by_letter[letter].append(pair)
    for letter in sorted(by_letter.keys()):
        pairs_list = by_letter[letter]
        print(f"  {letter}: {', '.join(pairs_list)}")

    print(f"\nDecoded text (first 500 chars):")
    print(f"  {best_text[:500]}")

    print(f"\nDecoded text (last 500 chars):")
    print(f"  {best_text[-500:]}")

    # Show per-book decoded samples
    print(f"\n--- Per-book samples (first 80 chars each) ---")
    for i, book in enumerate(books[:10]):
        book_pairs = extract_pairs(book, offset)
        decoded = decode_with_key(book_pairs, best_key)
        print(f"  Book {i+1}: {decoded[:80]}")

print("\n" + "=" * 70)
print("CRACKING COMPLETE")
print("=" * 70)
