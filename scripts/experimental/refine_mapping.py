"""
Refine the 2-digit pair mapping.
Problem: E is 26.6% but should be 16.4%. Letters M,O,W,F,K,Z near 0%.
Solution: Constrained SA where E gets max 10 codes (not 16).
Also try: hill climbing with per-pair reassignment.
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

expected_bi = {}
for bg, pct in german_bi.items():
    expected_bi[(letter_to_idx[bg[0]], letter_to_idx[bg[1]])] = pct

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

book_pairs = []
for i, book in enumerate(books):
    off = book_offsets[i]
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

all_pairs = []
for bp in book_pairs:
    all_pairs.extend(bp)

pair_counts = Counter(all_pairs)
all_pair_codes = sorted(pair_counts.keys())
pair_to_idx = {p: i for i, p in enumerate(all_pair_codes)}
n_pairs = len(all_pair_codes)
total_pairs = len(all_pairs)

# Precompute pair bigram matrix
pair_bigram_matrix = {}
for bp in book_pairs:
    for k in range(len(bp)-1):
        key = (pair_to_idx.get(bp[k]), pair_to_idx.get(bp[k+1]))
        if key[0] is not None and key[1] is not None:
            pair_bigram_matrix[key] = pair_bigram_matrix.get(key, 0) + 1

total_bigrams = sum(pair_bigram_matrix.values())

print(f"Pairs: {total_pairs}, unique: {n_pairs}")

# Better scoring: use log-likelihood instead of chi-squared
def score_mapping(mapping_arr):
    # Unigram
    letter_freq = [0]*26
    for pi in range(n_pairs):
        letter_freq[mapping_arr[pi]] += pair_counts[all_pair_codes[pi]]

    uni_score = 0
    for li in range(26):
        obs = letter_freq[li] / total_pairs
        exp = german[letters_list[li]]
        # Penalize deviation quadratically with higher weight on low-freq letters
        weight = 1.0 / max(exp, 0.005)
        uni_score -= weight * (obs - exp) ** 2

    # Bigram
    bi_freq = [[0]*26 for _ in range(26)]
    for (pi, pj), count in pair_bigram_matrix.items():
        li = mapping_arr[pi]
        lj = mapping_arr[pj]
        bi_freq[li][lj] += count

    bi_score = 0
    for key, exp_pct in expected_bi.items():
        li, lj = key
        obs_pct = bi_freq[li][lj] / total_bigrams * 100
        bi_score -= (obs_pct - exp_pct) ** 2

    # Penalty for 'EE' (should be very rare in German)
    ee_idx = letter_to_idx['E']
    ee_pct = bi_freq[ee_idx][ee_idx] / total_bigrams * 100
    bi_score -= 10 * ee_pct ** 2  # Heavy penalty for EE

    return uni_score * 1000 + bi_score * 500

# Hill climbing with single-pair reassignment
def hill_climb(mapping_arr, n_iter=200000):
    current = list(mapping_arr)
    current_score = score_mapping(current)
    best = list(current)
    best_score = current_score

    for i in range(n_iter):
        # Pick random pair, try reassigning to random letter
        pi = random.randint(0, n_pairs-1)
        old_letter = current[pi]
        new_letter = random.randint(0, 25)
        if new_letter == old_letter:
            continue

        current[pi] = new_letter
        new_score = score_mapping(current)

        if new_score > current_score:
            current_score = new_score
            if current_score > best_score:
                best_score = current_score
                best = list(current)
        else:
            current[pi] = old_letter

    return best, best_score


# Create good initial mapping
sorted_pair_idxs = sorted(range(n_pairs), key=lambda i: -pair_counts[all_pair_codes[i]])
letters_sorted = sorted(range(26), key=lambda i: -german[letters_list[i]])

# Target codes per letter based on frequency * 100
target_codes = {}
total_assigned = 0
for letter in letters_list:
    n = max(1, round(german[letter] * n_pairs))
    target_codes[letter] = n
    total_assigned += n

# Adjust to match total
while total_assigned > n_pairs:
    max_letter = max(target_codes, key=target_codes.get)
    target_codes[max_letter] -= 1
    total_assigned -= 1
while total_assigned < n_pairs:
    min_letter = min(target_codes, key=lambda l: target_codes[l] / max(german[l], 0.001))
    target_codes[min_letter] += 1
    total_assigned += 1

print(f"\nTarget codes per letter:")
for l in sorted(target_codes.keys(), key=lambda l: -german[l]):
    print(f"  {l}: {target_codes[l]} codes (freq {german[l]*100:.1f}%)")

# Assign pairs to letters by frequency rank
mapping_arr = [0] * n_pairs
pidx = 0
for li in letters_sorted:
    letter = letters_list[li]
    for j in range(target_codes[letter]):
        if pidx < n_pairs:
            mapping_arr[sorted_pair_idxs[pidx]] = li
            pidx += 1

print(f"\nRunning hill climbing (5 rounds x 200k iterations)...")
best_score = float('-inf')
best_mapping = None

for round_num in range(5):
    if round_num == 0:
        init = list(mapping_arr)
    else:
        # Perturb best mapping
        init = list(best_mapping) if best_mapping else list(mapping_arr)
        for _ in range(20):
            pi = random.randint(0, n_pairs-1)
            init[pi] = random.randint(0, 25)

    result, score = hill_climb(init, 200000)
    print(f"  Round {round_num}: score = {score:.2f}")

    if score > best_score:
        best_score = score
        best_mapping = list(result)

print(f"\nBest score: {best_score:.2f}")

# SA refinement on top of hill climbing result
print(f"\nSA refinement (300k iterations)...")
current = list(best_mapping)
current_score = score_mapping(current)

T = 5.0
for i in range(300000):
    # Try single reassignment
    pi = random.randint(0, n_pairs-1)
    old = current[pi]
    current[pi] = random.randint(0, 25)

    new_score = score_mapping(current)
    delta = new_score - current_score

    if delta > 0 or random.random() < math.exp(min(delta / max(T, 0.001), 500)):
        current_score = new_score
        if current_score > best_score:
            best_score = current_score
            best_mapping = list(current)
    else:
        current[pi] = old

    T *= 0.999985

print(f"Final score: {best_score:.2f}")

# Convert to dict
mapping = {}
for pi in range(n_pairs):
    mapping[all_pair_codes[pi]] = letters_list[best_mapping[pi]]


print("\n" + "=" * 70)
print("REFINED MAPPING")
print("=" * 70)

mapping_by_letter = {}
for pair, letter in sorted(mapping.items()):
    if letter not in mapping_by_letter:
        mapping_by_letter[letter] = []
    mapping_by_letter[letter].append(pair)

for letter in sorted(mapping_by_letter.keys(), key=lambda l: -german[l]):
    codes = sorted(mapping_by_letter[letter])
    tc = sum(pair_counts.get(c, 0) for c in codes)
    pct = tc / total_pairs * 100
    exp = german[letter] * 100
    diff = pct - exp
    print(f"  {letter} (exp {exp:.1f}%, obs {pct:.1f}%, diff {diff:+.1f}%): {codes}")


print("\n" + "=" * 70)
print("DECODED BOOKS (first 15)")
print("=" * 70)

for i, bp in enumerate(book_pairs[:15]):
    decoded = ''.join(mapping.get(p, '?') for p in bp)
    print(f"\n  Book {i:2d} (off={book_offsets[i]}):")
    for j in range(0, len(decoded), 70):
        print(f"    {decoded[j:j+70]}")


print("\n" + "=" * 70)
print("FREQUENCY AND BIGRAM CHECK")
print("=" * 70)

decoded_full = ''.join(mapping.get(p, '?') for p in all_pairs)
n = len(decoded_full)

letter_counts = Counter(decoded_full)
for letter in sorted(german.keys(), key=lambda l: -german[l]):
    obs = letter_counts.get(letter, 0) / n * 100
    exp = german[letter] * 100
    print(f"  {letter}: obs={obs:5.1f}% exp={exp:5.1f}% ({obs-exp:+.1f}%)")

bi_counts = Counter()
for i in range(n-1):
    bi_counts[decoded_full[i:i+2]] += 1

print(f"\nTop 30 bigrams:")
for bg, count in bi_counts.most_common(30):
    pct = count / (n-1) * 100
    exp = german_bi.get(bg, 0)
    marker = " <-- GERMAN" if exp > 1.0 else ""
    print(f"  '{bg}': {pct:.2f}% (exp: {exp:.2f}%){marker}")


print("\n" + "=" * 70)
print("GERMAN WORD SEARCH")
print("=" * 70)

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
    'EINS', 'ZWEI', 'DREI', 'VIER', 'ACHT', 'NEUN', 'ZEHN',
    'TIER', 'MENSCH', 'GOTT', 'GEIST',
    'NACHT', 'TAG', 'ENDE', 'ANFANG',
    'SCHRIFT', 'ZEICHEN', 'SPRACHE',
    'DUNKEL', 'HELL', 'KALT', 'HEISS',
    'BLUT', 'SEELE', 'HERZ', 'HAND', 'KOPF',
    'STEIN', 'STEIN', 'STRASSE', 'WEG',
    'STARK', 'GROSS', 'KLEIN', 'ALT', 'NEU',
    'FINDEN', 'SUCHEN', 'GEHEN', 'KOMMEN',
    'SAGEN', 'LESEN', 'SCHREIBEN',
    'BONELORD', 'TIBIA', 'MAGIC', 'MAGIE'
]

found = []
for word in set(german_words):
    count = decoded_full.count(word)
    expected = n * (1/26) ** len(word)
    ratio = count / expected if expected > 0 else 0
    if count > 0:
        found.append((word, count, ratio))

found.sort(key=lambda x: -x[2])
for word, count, ratio in found[:50]:
    print(f"  '{word}': {count} times ({ratio:.1f}x expected)")


print("\n" + "=" * 70)
print("RECONSTRUCTED TEXT (longest books)")
print("=" * 70)

# Sort books by length, show longest
book_decoded = []
for i, bp in enumerate(book_pairs):
    decoded = ''.join(mapping.get(p, '?') for p in bp)
    book_decoded.append((i, decoded, len(decoded)))

book_decoded.sort(key=lambda x: -x[2])
for idx, decoded, length in book_decoded[:5]:
    print(f"\n  Book {idx} ({length} letters):")
    for j in range(0, len(decoded), 70):
        print(f"    {decoded[j:j+70]}")


print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
