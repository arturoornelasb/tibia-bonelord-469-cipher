"""
Refined 2-digit pair homophonic decoder.
- Per-book alignment detection
- Quadgram scoring for SA
- More iterations
- Full decoded output
"""

import json
import random
import math
from collections import Counter

with open('books.json', 'r') as f:
    books = json.load(f)

all_digits = ''.join(books)

# German frequencies
german = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
    'Q': 0.001
}

# German bigrams (relative frequency %)
german_bi = {
    'EN': 3.88, 'ER': 3.75, 'CH': 2.75, 'DE': 2.56, 'EI': 2.45,
    'ND': 2.22, 'TE': 2.09, 'IN': 2.06, 'IE': 2.02, 'GE': 1.85,
    'ES': 1.79, 'NE': 1.72, 'UN': 1.69, 'ST': 1.66, 'RE': 1.56,
    'AN': 1.55, 'HE': 1.49, 'BE': 1.39, 'SE': 1.33, 'DI': 1.30,
    'DA': 1.22, 'HA': 1.18, 'SI': 1.17, 'AU': 1.14, 'AL': 1.13
}

# German quadgrams (log probabilities for scoring)
# We'll compute these from bigrams as a proxy
german_trigrams = {
    'EIN': 1.5, 'ICH': 1.4, 'DER': 1.3, 'DIE': 1.3, 'UND': 1.2,
    'DEN': 1.1, 'SCH': 1.1, 'CHE': 1.0, 'GEN': 1.0, 'END': 0.9,
    'TEN': 0.9, 'VER': 0.8, 'BER': 0.8, 'NDE': 0.8, 'DAS': 0.7,
    'ERE': 0.7, 'AUS': 0.7, 'HAT': 0.7, 'STA': 0.7, 'NEN': 0.7,
    'HEN': 0.6, 'BEI': 0.6, 'RUN': 0.5, 'UNE': 0.5, 'IST': 0.5
}


def ic_from_counts(counts, total):
    if total <= 1:
        return 0
    return sum(c * (c - 1) for c in counts.values()) / (total * (total - 1))


print("=" * 70)
print("1. PER-BOOK ALIGNMENT DETECTION")
print("=" * 70)

book_offsets = []
for i, book in enumerate(books):
    if len(book) < 10:
        book_offsets.append(0)
        continue

    bp0 = [book[j:j+2] for j in range(0, len(book) - 1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book) - 1, 2)]

    ic0 = ic_from_counts(Counter(bp0), len(bp0))
    ic1 = ic_from_counts(Counter(bp1), len(bp1))

    book_offsets.append(0 if ic0 > ic1 else 1)

offset_counts = Counter(book_offsets)
print(f"Books preferring offset 0: {offset_counts[0]}")
print(f"Books preferring offset 1: {offset_counts[1]}")

# Build aligned pair sequence using per-book offsets
aligned_pairs = []
for i, book in enumerate(books):
    offset = book_offsets[i]
    pairs = [book[j:j+2] for j in range(offset, len(book) - 1, 2)]
    aligned_pairs.extend(pairs)

print(f"Total aligned pairs: {len(aligned_pairs)}")
aligned_counts = Counter(aligned_pairs)
aligned_ic = ic_from_counts(aligned_counts, len(aligned_pairs))
print(f"Aligned IC ratio: {aligned_ic * 100:.3f} (German ~1.72)")

# Also try all offset 0
all_off0_pairs = []
for book in books:
    pairs = [book[j:j+2] for j in range(0, len(book) - 1, 2)]
    all_off0_pairs.extend(pairs)

off0_ic = ic_from_counts(Counter(all_off0_pairs), len(all_off0_pairs))
print(f"All-offset-0 IC ratio: {off0_ic * 100:.3f}")


print("\n" + "=" * 70)
print("2. ENHANCED SIMULATED ANNEALING")
print("=" * 70)

# Use aligned pairs for decoding
pairs = aligned_pairs
pair_counts = aligned_counts
total = len(pairs)

# Precompute bigram counts of pairs
pair_bigrams = Counter()
for i in range(len(pairs) - 1):
    pair_bigrams[(pairs[i], pairs[i+1])] += 1

def score_mapping(mapping):
    """Score using unigram + bigram fit to German."""
    # Unigram score
    letter_counts = Counter()
    for pair, count in pair_counts.items():
        letter = mapping.get(pair, '?')
        letter_counts[letter] += count

    n = total
    uni_score = 0
    for letter, exp_freq in german.items():
        obs_freq = letter_counts.get(letter, 0) / n
        uni_score -= (obs_freq - exp_freq) ** 2

    # Bigram score using precomputed pair bigrams
    decoded_bigrams = Counter()
    for (p1, p2), count in pair_bigrams.items():
        l1 = mapping.get(p1, '?')
        l2 = mapping.get(p2, '?')
        decoded_bigrams[l1 + l2] += count

    n_bi = total - 1
    bi_score = 0
    for bigram, exp_pct in german_bi.items():
        obs_pct = decoded_bigrams.get(bigram, 0) / n_bi * 100
        bi_score -= (obs_pct - exp_pct) ** 2

    # Trigram score (sampled)
    tri_score = 0
    decoded_trigrams = Counter()
    for i in range(len(pairs) - 2):
        l1 = mapping.get(pairs[i], '?')
        l2 = mapping.get(pairs[i+1], '?')
        l3 = mapping.get(pairs[i+2], '?')
        decoded_trigrams[l1 + l2 + l3] += 1

    n_tri = total - 2
    for trigram, exp_pct in german_trigrams.items():
        obs_pct = decoded_trigrams.get(trigram, 0) / n_tri * 100
        tri_score -= (obs_pct - exp_pct) ** 2

    return uni_score * 2000 + bi_score * 500 + tri_score * 200

def create_freq_mapping():
    """Frequency-based initial mapping."""
    sorted_pairs = [p for p, c in sorted(pair_counts.items(), key=lambda x: -x[1])]
    letters_sorted = [l for l, f in sorted(german.items(), key=lambda x: -x[1])]

    mapping = {}
    pair_idx = 0
    for letter in letters_sorted:
        n_codes = max(1, round(german[letter] * 100))
        for j in range(n_codes):
            if pair_idx < len(sorted_pairs):
                mapping[sorted_pairs[pair_idx]] = letter
                pair_idx += 1
    while pair_idx < len(sorted_pairs):
        letter_code_counts = Counter(mapping.values())
        least = min(letters_sorted, key=lambda l: letter_code_counts.get(l, 0))
        mapping[sorted_pairs[pair_idx]] = least
        pair_idx += 1
    return mapping

print("Running enhanced SA (15 restarts, 100000 iterations each)...")

best_global_score = float('-inf')
best_global_mapping = None

for restart in range(15):
    if restart == 0:
        mapping = create_freq_mapping()
    else:
        all_pair_codes = list(pair_counts.keys())
        letters = list(german.keys())
        mapping = {p: random.choice(letters) for p in all_pair_codes}

    current_score = score_mapping(mapping)
    best_score = current_score
    best_mapping = dict(mapping)

    T = 15.0
    cooling = 0.99997

    for iteration in range(100000):
        # Mutation: swap two pair assignments
        p1, p2 = random.sample(list(mapping.keys()), 2)
        mapping[p1], mapping[p2] = mapping[p2], mapping[p1]

        new_score = score_mapping(mapping)
        delta = new_score - current_score

        if delta > 0 or random.random() < math.exp(min(delta / max(T, 0.001), 500)):
            current_score = new_score
            if current_score > best_score:
                best_score = current_score
                best_mapping = dict(mapping)
        else:
            mapping[p1], mapping[p2] = mapping[p2], mapping[p1]

        T *= cooling

    if best_score > best_global_score:
        best_global_score = best_score
        best_global_mapping = dict(best_mapping)

    if restart % 3 == 0:
        print(f"  Restart {restart}: score = {best_score:.2f}")

print(f"\nBest score: {best_global_score:.2f}")


print("\n" + "=" * 70)
print("3. DECODED TEXT")
print("=" * 70)

mapping = best_global_mapping

# Show mapping
mapping_by_letter = {}
for pair, letter in sorted(mapping.items()):
    if letter not in mapping_by_letter:
        mapping_by_letter[letter] = []
    mapping_by_letter[letter].append(pair)

print("\nMapping (pair -> letter):")
for letter in sorted(mapping_by_letter.keys()):
    codes = sorted(mapping_by_letter[letter])
    total_count = sum(pair_counts.get(c, 0) for c in codes)
    pct = total_count / total * 100
    exp = german[letter] * 100
    print(f"  {letter} (exp {exp:.1f}%, obs {pct:.1f}%): {codes}")

# Decode each book
print("\nDecoded books (first 10):")
for i, book in enumerate(books[:10]):
    offset = book_offsets[i]
    bpairs = [book[j:j+2] for j in range(offset, len(book) - 1, 2)]
    decoded = ''.join(mapping.get(p, '?') for p in bpairs)
    print(f"\n  Book {i} (offset {offset}, {len(book)} digits -> {len(decoded)} letters):")
    # Print in chunks of 60
    for j in range(0, len(decoded), 60):
        print(f"    {decoded[j:j+60]}")

# Full decoded text with word detection
print("\nSearching decoded text for German words...")
decoded_full = ''.join(mapping.get(p, '?') for p in aligned_pairs)

words_found = {}
german_words = [
    'DER', 'DIE', 'DAS', 'UND', 'IST', 'EIN', 'EINE', 'EINEN', 'EINER',
    'DEN', 'DEM', 'VON', 'HAT', 'FUR', 'AUF', 'MIT', 'DES', 'SIE', 'ICH',
    'SIND', 'AUS', 'BEI', 'TOD', 'RUNE', 'RUNEN', 'STEIN', 'MAGIE',
    'ABER', 'AUCH', 'DASS', 'NACH', 'WIR', 'KANN', 'NOCH', 'DIESE',
    'HABEN', 'WERDEN', 'NICHT', 'WIRD', 'SEIN', 'WENN', 'NUR', 'ALLE',
    'WELT', 'FEUER', 'WASSER', 'ERDE', 'LUFT', 'LICHT', 'DUNKEL',
    'LEBEN', 'STERBEN', 'MACHT', 'KRAFT', 'KRIEG', 'FRIEDEN',
    'GOLD', 'SILBER', 'SCHWERT', 'SCHILD', 'HELM', 'RING',
    'DRACHE', 'TIER', 'MENSCH', 'GOTT', 'DEMON', 'GEIST',
    'LAND', 'BERG', 'MEER', 'WALD', 'TURM', 'BURG',
    'BUCH', 'SCHRIFT', 'ZEICHEN', 'SPRACHE', 'WORT',
    'AUGE', 'BLICK', 'SEHEN', 'WISSEN', 'KENNEN',
    'ACHT', 'NEUN', 'ZEHN', 'HUNDERT', 'TAUSEND',
    'EINS', 'ZWEI', 'DREI', 'VIER', 'FUNF',
    'NARR', 'DUMMKOPF', 'WEISE', 'KLUG'
]

for word in german_words:
    count = decoded_full.count(word)
    expected = len(decoded_full) * (1/26) ** len(word)
    ratio = count / expected if expected > 0 else 0
    if ratio > 5 or count > 3:
        words_found[word] = (count, ratio)

print(f"\nGerman words found (sorted by significance):")
for word, (count, ratio) in sorted(words_found.items(), key=lambda x: -x[1][1]):
    print(f"  '{word}': {count} times ({ratio:.1f}x expected)")


print("\n" + "=" * 70)
print("4. LETTER FREQUENCY COMPARISON")
print("=" * 70)

letter_counts = Counter(decoded_full)
n = len(decoded_full)
print(f"Total decoded letters: {n}")

chi2 = 0
for letter in sorted(german.keys()):
    obs = letter_counts.get(letter, 0) / n
    exp = german[letter]
    chi2 += (obs - exp) ** 2 / max(exp, 0.001)
    match = "OK" if abs(obs - exp) < 0.02 else "CLOSE" if abs(obs - exp) < 0.04 else "OFF"
    print(f"  {letter}: obs={obs*100:5.1f}% exp={exp*100:5.1f}% [{match}]")

print(f"\nChi-squared: {chi2:.4f}")


print("\n" + "=" * 70)
print("5. BIGRAM ANALYSIS")
print("=" * 70)

bi_counts = Counter()
for i in range(len(decoded_full) - 1):
    bi_counts[decoded_full[i:i+2]] += 1

n_bi = n - 1
print(f"\nTop 30 bigrams vs German:")
top_obs = bi_counts.most_common(30)
for bigram, count in top_obs:
    obs_pct = count / n_bi * 100
    exp_pct = german_bi.get(bigram, 0)
    marker = "<<< German top bigram!" if exp_pct > 0 else ""
    print(f"  '{bigram}': {obs_pct:.2f}% (German: {exp_pct:.2f}%) {marker}")


print("\n" + "=" * 70)
print("6. DECODED BOOK SAMPLES (ALL BOOKS)")
print("=" * 70)

for i, book in enumerate(books):
    offset = book_offsets[i]
    bpairs = [book[j:j+2] for j in range(offset, len(book) - 1, 2)]
    decoded = ''.join(mapping.get(p, '?') for p in bpairs)
    # Just show first 80 chars
    print(f"  Book {i:2d} (off={offset}): {decoded[:80]}{'...' if len(decoded)>80 else ''}")


print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
