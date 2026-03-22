"""
Crib-constrained SA decoder.
Fix confirmed code assignments from word cribs, optimize the rest.
Also use trigram scoring for better discrimination.
"""

import json
import random
import math
from collections import Counter

with open('books.json', 'r') as f:
    books = json.load(f)

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
expected_bi = {}
for bg, pct in german_bi.items():
    expected_bi[(letter_to_idx[bg[0]], letter_to_idx[bg[1]])] = pct

# German trigrams (percentages)
german_tri = {
    'EIN': 0.89, 'ICH': 0.79, 'DER': 0.76, 'DIE': 0.72, 'UND': 0.69,
    'DEN': 0.64, 'SCH': 0.60, 'CHE': 0.56, 'GEN': 0.52, 'END': 0.50,
    'TEN': 0.48, 'VER': 0.44, 'BER': 0.42, 'NDE': 0.40, 'DAS': 0.38,
    'ERE': 0.36, 'AUS': 0.34, 'HAT': 0.32, 'STA': 0.30, 'NEN': 0.30,
    'HEN': 0.28, 'BEI': 0.26, 'NIC': 0.24, 'CHT': 0.24, 'EST': 0.22,
    'IND': 0.20, 'GEI': 0.20, 'IST': 0.18, 'INE': 0.18, 'STE': 0.18,
    'ERN': 0.16, 'TEI': 0.16, 'NEI': 0.16, 'TER': 0.14, 'NER': 0.14,
    'IER': 0.14, 'REN': 0.14, 'ANG': 0.12, 'GER': 0.12, 'ENS': 0.12,
}

expected_tri = {}
for tg, pct in german_tri.items():
    expected_tri[(letter_to_idx[tg[0]], letter_to_idx[tg[1]], letter_to_idx[tg[2]])] = pct

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

# Per-book alignment (standard IC: higher IC wins)
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

# Precompute pair bigram and trigram matrices
pair_bigram = {}
pair_trigram = {}
for bp in book_pairs:
    for k in range(len(bp)-1):
        pi = pair_to_idx.get(bp[k])
        pj = pair_to_idx.get(bp[k+1])
        if pi is not None and pj is not None:
            pair_bigram[(pi, pj)] = pair_bigram.get((pi, pj), 0) + 1
    for k in range(len(bp)-2):
        pi = pair_to_idx.get(bp[k])
        pj = pair_to_idx.get(bp[k+1])
        pk = pair_to_idx.get(bp[k+2])
        if pi is not None and pj is not None and pk is not None:
            pair_trigram[(pi, pj, pk)] = pair_trigram.get((pi, pj, pk), 0) + 1

total_bigrams = sum(pair_bigram.values())
total_trigrams = sum(pair_trigram.values())
pair_freq_arr = [pair_counts[all_pair_codes[i]] for i in range(n_pairs)]

print(f"Pairs: {total_pairs}, unique: {n_pairs}")
print(f"Bigrams: {total_bigrams}, Trigrams: {total_trigrams}")

# CONFIRMED CRIBS from crib_attack.py output
# All occurrences of these words use the EXACT same digit pairs
confirmed = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',  # STEIN (10 occurrences)
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',              # ENDE (28 occurrences)
    '26': 'E',                                                   # ENDE variant
    '90': 'N', '31': 'A', '18': 'C', '06': 'H',              # NACH (2 occurrences)
    '85': 'A', '61': 'U',                                       # AU in AUCH
}

# Map to indices
fixed_codes = {}  # pair_idx -> letter_idx
for code, letter in confirmed.items():
    if code in pair_to_idx:
        pi = pair_to_idx[code]
        li = letter_to_idx[letter]
        fixed_codes[pi] = li
        print(f"  Fixed: '{code}' (idx {pi}) -> {letter} (idx {li})")

print(f"\nFixed codes: {len(fixed_codes)} out of {n_pairs}")
free_codes = [pi for pi in range(n_pairs) if pi not in fixed_codes]
print(f"Free codes: {len(free_codes)}")

# Scoring function
def score_mapping(mapping_arr):
    # Unigram
    letter_freq = [0]*26
    for pi in range(n_pairs):
        letter_freq[mapping_arr[pi]] += pair_freq_arr[pi]

    uni_score = 0
    for li in range(26):
        obs = letter_freq[li] / total_pairs
        exp = german[letters_list[li]]
        weight = 1.0 / max(exp, 0.003)
        uni_score -= weight * (obs - exp) ** 2

    # Bigram
    bi_freq = {}
    for (pi, pj), count in pair_bigram.items():
        li = mapping_arr[pi]
        lj = mapping_arr[pj]
        key = (li, lj)
        bi_freq[key] = bi_freq.get(key, 0) + count

    bi_score = 0
    for key, exp_pct in expected_bi.items():
        obs_pct = bi_freq.get(key, 0) / total_bigrams * 100
        bi_score -= (obs_pct - exp_pct) ** 2

    # Penalize non-German high bigrams
    for key, count in bi_freq.items():
        if key not in expected_bi:
            obs_pct = count / total_bigrams * 100
            if obs_pct > 1.0:
                bi_score -= 0.3 * (obs_pct - 1.0) ** 2

    # Trigram
    tri_freq = {}
    for (pi, pj, pk), count in pair_trigram.items():
        li = mapping_arr[pi]
        lj = mapping_arr[pj]
        lk = mapping_arr[pk]
        key = (li, lj, lk)
        tri_freq[key] = tri_freq.get(key, 0) + count

    tri_score = 0
    for key, exp_pct in expected_tri.items():
        obs_pct = tri_freq.get(key, 0) / total_trigrams * 100
        tri_score -= (obs_pct - exp_pct) ** 2

    # EE penalty
    ee_idx = letter_to_idx['E']
    ee_pct = bi_freq.get((ee_idx, ee_idx), 0) / total_bigrams * 100
    bi_score -= 5 * ee_pct ** 2

    return uni_score * 500 + bi_score * 2 + tri_score * 3

# Load best mapping as starting point
with open('best_mapping.json', 'r') as f:
    prev_mapping = json.load(f)

# Convert to array
mapping_arr = [0] * n_pairs
for code, letter in prev_mapping.items():
    if code in pair_to_idx:
        mapping_arr[pair_to_idx[code]] = letter_to_idx[letter]

# Override with fixed codes
for pi, li in fixed_codes.items():
    mapping_arr[pi] = li

print(f"\nInitial score: {score_mapping(mapping_arr):.4f}")

# SA: only swap FREE codes
print(f"\nCrib-constrained SA (15 restarts x 500k iterations)...")
best_global_score = float('-inf')
best_global_mapping = None

for restart in range(15):
    if restart == 0:
        current = list(mapping_arr)
    elif best_global_mapping is not None:
        current = list(best_global_mapping)
        # Perturb
        for _ in range(25):
            p1 = random.choice(free_codes)
            p2 = random.choice(free_codes)
            if current[p1] != current[p2]:
                current[p1], current[p2] = current[p2], current[p1]
    else:
        current = list(mapping_arr)
        # Random shuffle of free codes
        free_letters = [current[pi] for pi in free_codes]
        random.shuffle(free_letters)
        for idx, pi in enumerate(free_codes):
            current[pi] = free_letters[idx]

    current_score = score_mapping(current)
    best_score = current_score
    best_local = list(current)

    T = 6.0
    cooling = 0.999988

    for iteration in range(500000):
        # Swap two free codes
        p1 = random.choice(free_codes)
        p2 = random.choice(free_codes)
        if current[p1] == current[p2]:
            continue

        current[p1], current[p2] = current[p2], current[p1]
        new_score = score_mapping(current)
        delta = new_score - current_score

        if delta > 0 or random.random() < math.exp(min(delta / max(T, 0.001), 500)):
            current_score = new_score
            if current_score > best_score:
                best_score = current_score
                best_local = list(current)
        else:
            current[p1], current[p2] = current[p2], current[p1]

        T *= cooling

    if best_score > best_global_score:
        best_global_score = best_score
        best_global_mapping = list(best_local)

    print(f"  Restart {restart}: score = {best_score:.4f}")

print(f"\nBest score: {best_global_score:.4f}")

# Convert to dict
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

for letter in sorted(mapping_by_letter.keys(), key=lambda l: -german[l]):
    codes = sorted(mapping_by_letter[letter])
    tc = sum(pair_counts.get(c, 0) for c in codes)
    pct = tc / total_pairs * 100
    exp = german[letter] * 100
    diff = pct - exp
    fixed_mark = [c for c in codes if pair_to_idx.get(c) in fixed_codes]
    print(f"  {letter} ({exp:.1f}% exp, {pct:.1f}% obs, {diff:+.1f}%): {codes} [fixed: {fixed_mark}]")


print("\n" + "=" * 70)
print("FREQUENCY CHECK")
print("=" * 70)

decoded_full = ''.join(mapping.get(p, '?') for p in all_pairs)
n = len(decoded_full)

letter_counts = Counter(decoded_full)
for letter in sorted(german.keys(), key=lambda l: -german[l]):
    obs = letter_counts.get(letter, 0) / n * 100
    exp = german[letter] * 100
    print(f"  {letter}: obs={obs:5.1f}% exp={exp:5.1f}% ({obs-exp:+.1f}%)")


print("\n" + "=" * 70)
print("BIGRAM CHECK")
print("=" * 70)

bi_counts = Counter()
for i in range(n-1):
    bi_counts[decoded_full[i:i+2]] += 1

for bg, count in bi_counts.most_common(30):
    pct = count / (n-1) * 100
    exp = german_bi.get(bg, 0)
    marker = " <-- GERMAN" if exp > 1.0 else ""
    print(f"  '{bg}': {pct:.2f}% (exp: {exp:.2f}%){marker}")


print("\n" + "=" * 70)
print("WORD SEARCH")
print("=" * 70)

german_words = [
    'DER', 'DIE', 'DAS', 'UND', 'IST', 'EIN', 'EINE', 'EINEN', 'EINER',
    'DEN', 'DEM', 'VON', 'HAT', 'AUF', 'MIT', 'DES', 'SIE', 'ICH',
    'SIND', 'AUS', 'BEI', 'RUNE', 'RUNEN', 'STEIN', 'STEINEN',
    'ABER', 'AUCH', 'DASS', 'NACH', 'WIR', 'KANN', 'NOCH', 'DIESE',
    'NICHT', 'WIRD', 'SEIN', 'WENN', 'NUR', 'ALLE', 'WELT',
    'STEIN', 'STEINE', 'STEINEN',
    'FEUER', 'WASSER', 'ERDE', 'LICHT', 'LEBEN', 'ENDE',
]

found = []
for word in set(german_words):
    count = decoded_full.count(word)
    expected = n * (1/26) ** len(word)
    ratio = count / expected if expected > 0 else 0
    if count > 0:
        found.append((word, count, ratio))

found.sort(key=lambda x: -x[2])
for word, count, ratio in found[:30]:
    print(f"  '{word}': {count} times ({ratio:.1f}x expected)")


print("\n" + "=" * 70)
print("DECODED BOOKS")
print("=" * 70)

for i, bp in enumerate(book_pairs[:15]):
    decoded = ''.join(mapping.get(p, '?') for p in bp)
    print(f"\n  Book {i:2d} (off={book_offsets[i]}, {len(decoded)} letters):")
    for j in range(0, len(decoded), 70):
        print(f"    {decoded[j:j+70]}")


print("\n" + "=" * 70)
print("LONGEST BOOKS")
print("=" * 70)

book_decoded = []
for i, bp in enumerate(book_pairs):
    decoded = ''.join(mapping.get(p, '?') for p in bp)
    book_decoded.append((i, decoded, len(decoded)))

book_decoded.sort(key=lambda x: -x[2])
for idx, decoded, length in book_decoded[:5]:
    print(f"\n  Book {idx} ({length} letters, off={book_offsets[idx]}):")
    for j in range(0, len(decoded), 70):
        print(f"    {decoded[j:j+70]}")


# Save
with open('best_mapping.json', 'w') as f:
    json.dump(mapping, f, indent=2)
print("\nSaved updated mapping to best_mapping.json")

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
