"""
Fast 2-digit pair decoder using precomputed scoring.
Key optimization: precompute pair bigram matrix, score incrementally.
"""

import json
import random
import math
from collections import Counter

with open('books.json', 'r') as f:
    books = json.load(f)

all_digits = ''.join(books)

german = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
    'Q': 0.001
}
letters_list = list(german.keys())
letter_to_idx = {l: i for i, l in enumerate(letters_list)}

german_bi = {
    'EN': 3.88, 'ER': 3.75, 'CH': 2.75, 'DE': 2.56, 'EI': 2.45,
    'ND': 2.22, 'TE': 2.09, 'IN': 2.06, 'IE': 2.02, 'GE': 1.85,
    'ES': 1.79, 'NE': 1.72, 'UN': 1.69, 'ST': 1.66, 'RE': 1.56,
    'AN': 1.55, 'HE': 1.49, 'BE': 1.39, 'SE': 1.33, 'DI': 1.30,
    'DA': 1.22, 'HA': 1.18, 'SI': 1.17, 'AU': 1.14, 'AL': 1.13
}

# Build expected bigram matrix
expected_bi = [[0.0]*26 for _ in range(26)]
for bg, pct in german_bi.items():
    i, j = letter_to_idx[bg[0]], letter_to_idx[bg[1]]
    expected_bi[i][j] = pct

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

# Build pair sequences per book
book_pairs = []
for i, book in enumerate(books):
    off = book_offsets[i]
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# All aligned pairs and precompute bigram matrix
all_pairs = []
for bp in book_pairs:
    all_pairs.extend(bp)

pair_counts = Counter(all_pairs)
all_pair_codes = sorted(pair_counts.keys())
pair_to_idx = {p: i for i, p in enumerate(all_pair_codes)}
n_pairs = len(all_pair_codes)

# Precompute pair bigram matrix
pair_bigram_matrix = [[0]*n_pairs for _ in range(n_pairs)]
for bp in book_pairs:
    for k in range(len(bp)-1):
        pi = pair_to_idx.get(bp[k])
        pj = pair_to_idx.get(bp[k+1])
        if pi is not None and pj is not None:
            pair_bigram_matrix[pi][pj] += 1

total_pairs = len(all_pairs)
total_bigrams = sum(sum(row) for row in pair_bigram_matrix)

print(f"Total pairs: {total_pairs}, unique: {n_pairs}")
print(f"Total bigrams: {total_bigrams}")
print(f"Books offset 0: {sum(1 for o in book_offsets if o==0)}, offset 1: {sum(1 for o in book_offsets if o==1)}")

# Scoring function using precomputed matrices
def full_score(mapping_arr):
    """mapping_arr[pair_idx] = letter_idx"""
    # Unigram score
    letter_freq = [0]*26
    for pi in range(n_pairs):
        letter_freq[mapping_arr[pi]] += pair_counts[all_pair_codes[pi]]

    uni_score = 0
    for li in range(26):
        obs = letter_freq[li] / total_pairs
        exp = german[letters_list[li]]
        uni_score -= (obs - exp) ** 2

    # Bigram score
    bi_freq = [[0]*26 for _ in range(26)]
    for pi in range(n_pairs):
        li = mapping_arr[pi]
        for pj in range(n_pairs):
            if pair_bigram_matrix[pi][pj] > 0:
                lj = mapping_arr[pj]
                bi_freq[li][lj] += pair_bigram_matrix[pi][pj]

    bi_score = 0
    for li in range(26):
        for lj in range(26):
            obs = bi_freq[li][lj] / total_bigrams * 100 if total_bigrams > 0 else 0
            exp = expected_bi[li][lj]
            if exp > 0:
                bi_score -= (obs - exp) ** 2

    return uni_score * 2000 + bi_score * 500

# Incremental scoring: when swapping pair p1 and p2
def delta_score_swap(mapping_arr, p1_idx, p2_idx):
    """Approximate delta score for swapping two pair assignments."""
    # For speed, just recompute full score (optimized enough with precomputation)
    old_l1, old_l2 = mapping_arr[p1_idx], mapping_arr[p2_idx]
    mapping_arr[p1_idx], mapping_arr[p2_idx] = old_l2, old_l1
    new_score = full_score(mapping_arr)
    mapping_arr[p1_idx], mapping_arr[p2_idx] = old_l1, old_l2
    return new_score

# Initial mapping: frequency-based
sorted_pair_idxs = sorted(range(n_pairs), key=lambda i: -pair_counts[all_pair_codes[i]])
letters_sorted = sorted(range(26), key=lambda i: -german[letters_list[i]])

mapping_arr = [0] * n_pairs
pidx = 0
for li in letters_sorted:
    n_codes = max(1, round(german[letters_list[li]] * 100))
    for j in range(n_codes):
        if pidx < n_pairs:
            mapping_arr[sorted_pair_idxs[pidx]] = li
            pidx += 1
while pidx < n_pairs:
    mapping_arr[sorted_pair_idxs[pidx]] = letters_sorted[-1]
    pidx += 1

print("\nRunning SA (20 restarts, 80000 iterations)...")

best_global_score = float('-inf')
best_global_mapping = None

for restart in range(20):
    if restart == 0:
        # Use frequency-based initial
        current = list(mapping_arr)
    else:
        current = [random.randint(0, 25) for _ in range(n_pairs)]

    current_score = full_score(current)
    best_score = current_score
    best_local = list(current)

    T = 12.0
    cooling = 0.99994

    for iteration in range(80000):
        i1 = random.randint(0, n_pairs-1)
        i2 = random.randint(0, n_pairs-1)
        if i1 == i2:
            continue

        old_l1, old_l2 = current[i1], current[i2]
        current[i1], current[i2] = old_l2, old_l1

        # Only recompute full score every 100 iterations for speed
        if iteration % 50 == 0:
            new_score = full_score(current)
        else:
            new_score = full_score(current)

        delta = new_score - current_score
        if delta > 0 or random.random() < math.exp(min(delta / max(T, 0.01), 500)):
            current_score = new_score
            if current_score > best_score:
                best_score = current_score
                best_local = list(current)
        else:
            current[i1], current[i2] = old_l1, old_l2

        T *= cooling

    if best_score > best_global_score:
        best_global_score = best_score
        best_global_mapping = list(best_local)

    if restart % 5 == 0:
        print(f"  Restart {restart}: score = {best_score:.2f}")

print(f"\nBest score: {best_global_score:.2f}")

# Convert to dict mapping
mapping = {}
for pi in range(n_pairs):
    mapping[all_pair_codes[pi]] = letters_list[best_global_mapping[pi]]


print("\n" + "=" * 70)
print("MAPPING")
print("=" * 70)

mapping_by_letter = {}
for pair, letter in sorted(mapping.items()):
    if letter not in mapping_by_letter:
        mapping_by_letter[letter] = []
    mapping_by_letter[letter].append(pair)

for letter in sorted(mapping_by_letter.keys()):
    codes = sorted(mapping_by_letter[letter])
    tc = sum(pair_counts.get(c, 0) for c in codes)
    pct = tc / total_pairs * 100
    exp = german[letter] * 100
    print(f"  {letter} (exp {exp:.1f}%, obs {pct:.1f}%): {codes}")


print("\n" + "=" * 70)
print("DECODED BOOKS")
print("=" * 70)

for i, bp in enumerate(book_pairs):
    decoded = ''.join(mapping.get(p, '?') for p in bp)
    print(f"\n  Book {i:2d} (off={book_offsets[i]}, {len(books[i])} dig -> {len(decoded)} let):")
    for j in range(0, len(decoded), 70):
        print(f"    {decoded[j:j+70]}")


print("\n" + "=" * 70)
print("GERMAN WORD SEARCH")
print("=" * 70)

decoded_full = ''.join(mapping.get(p, '?') for p in all_pairs)

german_words = [
    'DER', 'DIE', 'DAS', 'UND', 'IST', 'EIN', 'EINE', 'EINEN', 'EINER',
    'DEN', 'DEM', 'VON', 'HAT', 'AUF', 'MIT', 'DES', 'SIE', 'ICH',
    'SIND', 'AUS', 'BEI', 'TOD', 'RUNE', 'RUNEN', 'STEIN',
    'ABER', 'AUCH', 'DASS', 'NACH', 'WIR', 'KANN', 'NOCH', 'DIESE',
    'NICHT', 'WIRD', 'SEIN', 'WENN', 'NUR', 'ALLE', 'WELT',
    'FEUER', 'WASSER', 'ERDE', 'LUFT', 'LICHT', 'LEBEN',
    'MACHT', 'KRAFT', 'KRIEG', 'GOLD', 'SCHWERT', 'RING',
    'LAND', 'BERG', 'MEER', 'WALD', 'TURM', 'BURG',
    'BUCH', 'WORT', 'AUGE', 'NARR', 'WEISE', 'KLUG',
    'EINS', 'ZWEI', 'DREI', 'VIER', 'ACHT', 'NEUN', 'ZEHN'
]

found = []
for word in german_words:
    count = decoded_full.count(word)
    expected = len(decoded_full) * (1/26) ** len(word)
    ratio = count / expected if expected > 0 else 0
    if count > 0:
        found.append((word, count, ratio))

found.sort(key=lambda x: -x[2])
print(f"\nGerman words (sorted by significance):")
for word, count, ratio in found[:40]:
    print(f"  '{word}': {count} times ({ratio:.1f}x expected)")


print("\n" + "=" * 70)
print("FREQUENCY AND BIGRAM CHECK")
print("=" * 70)

letter_counts = Counter(decoded_full)
n = len(decoded_full)
print(f"Decoded letters: {n}")

for letter in sorted(german.keys(), key=lambda l: -german[l]):
    obs = letter_counts.get(letter, 0) / n * 100
    exp = german[letter] * 100
    diff = obs - exp
    print(f"  {letter}: obs={obs:5.1f}% exp={exp:5.1f}% ({diff:+.1f}%)")

bi_counts = Counter()
for i in range(n-1):
    bi_counts[decoded_full[i:i+2]] += 1

print(f"\nTop 25 bigrams:")
for bg, count in bi_counts.most_common(25):
    pct = count / (n-1) * 100
    exp = german_bi.get(bg, 0)
    marker = " <-- German!" if exp > 1.0 else ""
    print(f"  '{bg}': {pct:.2f}% (exp: {exp:.2f}%){marker}")


print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
