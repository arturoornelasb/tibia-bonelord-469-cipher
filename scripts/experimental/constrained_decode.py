"""
Constrained 2-digit pair decoder.
Fix: maintain target code counts per letter, only swap codes between letters.
This guarantees German-like frequency distribution while optimizing assignment.
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

# Precompute pair bigram matrix (sparse dict for speed)
pair_bigram = {}
for bp in book_pairs:
    for k in range(len(bp)-1):
        pi = pair_to_idx.get(bp[k])
        pj = pair_to_idx.get(bp[k+1])
        if pi is not None and pj is not None:
            pair_bigram[(pi, pj)] = pair_bigram.get((pi, pj), 0) + 1

total_bigrams = sum(pair_bigram.values())

print(f"Pairs: {total_pairs}, unique: {n_pairs}")
print(f"Bigrams: {total_bigrams}")

# Target codes per letter
target_codes = {}
total_assigned = 0
for letter in letters_list:
    n = max(1, round(german[letter] * n_pairs))
    target_codes[letter] = n
    total_assigned += n

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

# Precompute pair frequency array for fast unigram scoring
pair_freq_arr = [pair_counts[all_pair_codes[i]] for i in range(n_pairs)]

# Scoring: unigram + bigram
def score_mapping(mapping_arr):
    # Unigram: penalize deviation from German frequencies
    letter_freq = [0]*26
    for pi in range(n_pairs):
        letter_freq[mapping_arr[pi]] += pair_freq_arr[pi]

    uni_score = 0
    for li in range(26):
        obs = letter_freq[li] / total_pairs
        exp = german[letters_list[li]]
        # Weight inversely by expected frequency so rare letters matter
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

    # Penalize unexpected high bigrams
    for key, count in bi_freq.items():
        if key not in expected_bi:
            obs_pct = count / total_bigrams * 100
            if obs_pct > 1.0:
                bi_score -= 0.3 * (obs_pct - 1.0) ** 2

    # Penalize EE (very rare in German)
    ee_idx = letter_to_idx['E']
    ee_pct = bi_freq.get((ee_idx, ee_idx), 0) / total_bigrams * 100
    bi_score -= 5 * ee_pct ** 2

    return uni_score * 500 + bi_score

# Build initial mapping: assign codes by frequency rank
sorted_pair_idxs = sorted(range(n_pairs), key=lambda i: -pair_counts[all_pair_codes[i]])
letters_sorted = sorted(range(26), key=lambda i: -german[letters_list[i]])

mapping_arr = [0] * n_pairs
pidx = 0
for li in letters_sorted:
    letter = letters_list[li]
    for j in range(target_codes[letter]):
        if pidx < n_pairs:
            mapping_arr[sorted_pair_idxs[pidx]] = li
            pidx += 1

# Build letter-to-codes index for constrained swaps
def build_letter_codes(mapping_arr):
    lc = [[] for _ in range(26)]
    for pi in range(n_pairs):
        lc[mapping_arr[pi]].append(pi)
    return lc

print(f"\nConstrained SA (swap codes between letters, 10 restarts x 500k iterations)...")

best_global_score = float('-inf')
best_global_mapping = None

for restart in range(10):
    if restart == 0:
        current = list(mapping_arr)
    elif best_global_mapping is not None:
        current = list(best_global_mapping)
        # Random swaps to perturb
        lc = build_letter_codes(current)
        for _ in range(30):
            l1, l2 = random.sample(range(26), 2)
            if lc[l1] and lc[l2]:
                p1 = random.choice(lc[l1])
                p2 = random.choice(lc[l2])
                current[p1], current[p2] = current[p2], current[p1]
                lc[l1].remove(p1)
                lc[l2].remove(p2)
                lc[l1].append(p2)
                lc[l2].append(p1)
    else:
        current = list(mapping_arr)
        # Shuffle within constraint
        all_idxs = list(range(n_pairs))
        random.shuffle(all_idxs)
        pidx = 0
        for li in letters_sorted:
            letter = letters_list[li]
            for j in range(target_codes[letter]):
                if pidx < n_pairs:
                    current[all_idxs[pidx]] = li
                    pidx += 1

    current_score = score_mapping(current)
    best_score = current_score
    best_local = list(current)

    T = 8.0
    cooling = 0.999988  # slow cooling for 500k iterations

    for iteration in range(500000):
        # Swap two codes belonging to different letters
        p1 = random.randint(0, n_pairs-1)
        p2 = random.randint(0, n_pairs-1)
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
    print(f"  {letter} (exp {exp:.1f}%, obs {pct:.1f}%, diff {diff:+.1f}%): {codes}")


print("\n" + "=" * 70)
print("FREQUENCY CHECK")
print("=" * 70)

decoded_full = ''.join(mapping.get(p, '?') for p in all_pairs)
n = len(decoded_full)

letter_counts = Counter(decoded_full)
print(f"Total decoded letters: {n}")
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

print(f"Top 30 bigrams:")
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
    'STRASSE', 'WEG',
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
print("DECODED BOOKS (first 20)")
print("=" * 70)

for i, bp in enumerate(book_pairs[:20]):
    decoded = ''.join(mapping.get(p, '?') for p in bp)
    print(f"\n  Book {i:2d} (off={book_offsets[i]}): [{len(decoded)} letters]")
    for j in range(0, len(decoded), 70):
        print(f"    {decoded[j:j+70]}")


print("\n" + "=" * 70)
print("LONGEST BOOKS (full text)")
print("=" * 70)

book_decoded = []
for i, bp in enumerate(book_pairs):
    decoded = ''.join(mapping.get(p, '?') for p in bp)
    book_decoded.append((i, decoded, len(decoded)))

book_decoded.sort(key=lambda x: -x[2])
for idx, decoded, length in book_decoded[:8]:
    print(f"\n  Book {idx} ({length} letters, off={book_offsets[idx]}):")
    for j in range(0, len(decoded), 70):
        print(f"    {decoded[j:j+70]}")


print("\n" + "=" * 70)
print("SAVE MAPPING")
print("=" * 70)

with open('best_mapping.json', 'w') as f:
    json.dump(mapping, f, indent=2)
print("Saved mapping to best_mapping.json")

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
