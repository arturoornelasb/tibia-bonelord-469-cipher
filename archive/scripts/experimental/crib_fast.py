"""
Crib-constrained SA decoder - FAST version.
Fix confirmed code assignments, optimize rest with uni+bigram scoring.
Trigram scoring removed for speed. Fewer restarts, progress output.
"""
import sys
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

# Precompute bigrams
pair_bigram = {}
for bp in book_pairs:
    for k in range(len(bp)-1):
        pi = pair_to_idx.get(bp[k])
        pj = pair_to_idx.get(bp[k+1])
        if pi is not None and pj is not None:
            pair_bigram[(pi, pj)] = pair_bigram.get((pi, pj), 0) + 1

total_bigrams = sum(pair_bigram.values())
pair_freq_arr = [pair_counts[all_pair_codes[i]] for i in range(n_pairs)]

print(f"Pairs: {total_pairs}, unique: {n_pairs}", flush=True)
print(f"Bigrams: {total_bigrams}", flush=True)

# CONFIRMED CRIBS
confirmed = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',  # STEIN
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',              # ENDE
    '26': 'E',                                                   # ENDE variant
    '90': 'N', '31': 'A', '18': 'C', '06': 'H',              # NACH
    '85': 'A', '61': 'U',                                       # AU in AUCH
}

fixed_codes = {}
for code, letter in confirmed.items():
    if code in pair_to_idx:
        pi = pair_to_idx[code]
        li = letter_to_idx[letter]
        fixed_codes[pi] = li
        print(f"  Fixed: '{code}' (idx {pi}) -> {letter}", flush=True)

print(f"\nFixed: {len(fixed_codes)}, Free: {n_pairs - len(fixed_codes)}", flush=True)
free_codes = [pi for pi in range(n_pairs) if pi not in fixed_codes]

# INCREMENTAL scoring: precompute which bigrams involve each code
code_bigrams = [[] for _ in range(n_pairs)]
for (pi, pj), count in pair_bigram.items():
    code_bigrams[pi].append((pi, pj, count))
    code_bigrams[pj].append((pi, pj, count))

def score_mapping(mapping_arr):
    letter_freq = [0]*26
    for pi in range(n_pairs):
        letter_freq[mapping_arr[pi]] += pair_freq_arr[pi]

    uni_score = 0
    for li in range(26):
        obs = letter_freq[li] / total_pairs
        exp = german[letters_list[li]]
        weight = 1.0 / max(exp, 0.003)
        uni_score -= weight * (obs - exp) ** 2

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

    for key, count in bi_freq.items():
        if key not in expected_bi:
            obs_pct = count / total_bigrams * 100
            if obs_pct > 1.0:
                bi_score -= 0.3 * (obs_pct - 1.0) ** 2

    ee_idx = letter_to_idx['E']
    ee_pct = bi_freq.get((ee_idx, ee_idx), 0) / total_bigrams * 100
    bi_score -= 5 * ee_pct ** 2

    return uni_score * 500 + bi_score * 2

# Load previous best mapping as starting point
with open('best_mapping.json', 'r') as f:
    prev_mapping = json.load(f)

mapping_arr = [0] * n_pairs
for code, letter in prev_mapping.items():
    if code in pair_to_idx:
        mapping_arr[pair_to_idx[code]] = letter_to_idx[letter]

# Override with fixed codes
for pi, li in fixed_codes.items():
    mapping_arr[pi] = li

print(f"Initial score: {score_mapping(mapping_arr):.4f}", flush=True)

# SA with 8 restarts x 200k iterations
N_RESTARTS = 8
N_ITERS = 200000
print(f"\nCrib-constrained SA ({N_RESTARTS} restarts x {N_ITERS} iters)...", flush=True)

best_global_score = float('-inf')
best_global_mapping = None

for restart in range(N_RESTARTS):
    if restart == 0:
        current = list(mapping_arr)
    elif best_global_mapping is not None:
        current = list(best_global_mapping)
        for _ in range(20):
            p1 = random.choice(free_codes)
            p2 = random.choice(free_codes)
            if current[p1] != current[p2]:
                current[p1], current[p2] = current[p2], current[p1]
    else:
        current = list(mapping_arr)
        free_letters = [current[pi] for pi in free_codes]
        random.shuffle(free_letters)
        for idx, pi in enumerate(free_codes):
            current[pi] = free_letters[idx]

    current_score = score_mapping(current)
    best_score = current_score
    best_local = list(current)

    T = 5.0
    cooling = 0.99997  # for 200k iters

    for iteration in range(N_ITERS):
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

    print(f"  Restart {restart}: score = {best_score:.4f}", flush=True)

print(f"\nBest score: {best_global_score:.4f}", flush=True)

# Convert to dict
mapping = {}
for pi in range(n_pairs):
    mapping[all_pair_codes[pi]] = letters_list[best_global_mapping[pi]]


print("\n" + "=" * 70, flush=True)
print("MAPPING", flush=True)
print("=" * 70, flush=True)

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
    print(f"  {letter} ({exp:.1f}% exp, {pct:.1f}% obs): {codes} [fixed: {fixed_mark}]", flush=True)


print("\n" + "=" * 70, flush=True)
print("DECODED BOOKS (first 15)", flush=True)
print("=" * 70, flush=True)

for i, bp in enumerate(book_pairs[:15]):
    decoded = ''.join(mapping.get(p, '?') for p in bp)
    print(f"\n  Book {i:2d} (off={book_offsets[i]}, {len(decoded)} letters):", flush=True)
    for j in range(0, len(decoded), 70):
        print(f"    {decoded[j:j+70]}", flush=True)


print("\n" + "=" * 70, flush=True)
print("LONGEST BOOKS", flush=True)
print("=" * 70, flush=True)

book_decoded = []
for i, bp in enumerate(book_pairs):
    decoded = ''.join(mapping.get(p, '?') for p in bp)
    book_decoded.append((i, decoded, len(decoded)))

book_decoded.sort(key=lambda x: -x[2])
for idx, decoded, length in book_decoded[:8]:
    print(f"\n  Book {idx} ({length} letters, off={book_offsets[idx]}):", flush=True)
    for j in range(0, len(decoded), 70):
        print(f"    {decoded[j:j+70]}", flush=True)


print("\n" + "=" * 70, flush=True)
print("WORD SEARCH", flush=True)
print("=" * 70, flush=True)

decoded_full = ''.join(mapping.get(p, '?') for p in all_pairs)
n = len(decoded_full)

german_words = [
    'DER', 'DIE', 'DAS', 'UND', 'IST', 'EIN', 'EINE', 'EINEN', 'EINER',
    'DEN', 'DEM', 'VON', 'HAT', 'AUF', 'MIT', 'DES', 'SIE', 'ICH',
    'SIND', 'AUS', 'BEI', 'RUNE', 'RUNEN', 'STEIN', 'STEINEN',
    'ABER', 'AUCH', 'DASS', 'NACH', 'WIR', 'KANN', 'NOCH', 'DIESE',
    'NICHT', 'WIRD', 'SEIN', 'WENN', 'NUR', 'ALLE', 'WELT', 'ENDE',
    'FEUER', 'WASSER', 'ERDE', 'LICHT', 'LEBEN',
    'BONELORD', 'TIBIA', 'MAGIE', 'RUNENSTEIN',
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
    print(f"  '{word}': {count} times ({ratio:.1f}x expected)", flush=True)


# Save
with open('best_mapping.json', 'w') as f:
    json.dump(mapping, f, indent=2)
print("\nSaved updated mapping to best_mapping.json", flush=True)

print("\n" + "=" * 70, flush=True)
print("DONE", flush=True)
print("=" * 70, flush=True)
