"""
Word-matching optimization for code-to-letter mapping.
Instead of n-gram statistics, score by how many German words appear.
Greedy hill-climbing: for each free code, try all 26 letters.
"""
import json
import random
from collections import Counter

with open('books.json', 'r') as f:
    books = json.load(f)

with open('best_mapping.json', 'r') as f:
    mapping = json.load(f)

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

# German words for scoring - weighted by informativeness
german_words_weighted = {
    # Long words worth more (more constraining)
    'RUNENSTEIN': 50, 'RUNENSTEINEN': 60, 'STEINEN': 30,
    'NICHT': 20, 'EINER': 15, 'EINEN': 15, 'DIESE': 15, 'DIESER': 20,
    'WERDEN': 15, 'WURDE': 15, 'WAREN': 15, 'HABEN': 15,
    'STEINE': 25, 'STEINER': 25,
    # Medium words
    'STEIN': 10, 'RUNE': 8, 'RUNEN': 12, 'AUCH': 8,
    'NACH': 8, 'NOCH': 8, 'WENN': 8, 'DANN': 8,
    'ABER': 8, 'ODER': 8, 'ALLE': 8, 'WELT': 8,
    'SICH': 10, 'SIND': 8, 'DASS': 8,
    'ENDE': 5, 'HABE': 8, 'KANN': 8, 'WIRD': 8,
    # Short common words
    'DER': 3, 'DIE': 3, 'DAS': 3, 'UND': 3,
    'IST': 3, 'EIN': 2, 'DEN': 2, 'DEM': 2,
    'VON': 3, 'HAT': 3, 'AUF': 3, 'MIT': 3,
    'DES': 2, 'SIE': 2, 'ICH': 3, 'AUS': 3,
    'BEI': 2, 'WIR': 3, 'NUR': 3,
    'EINE': 5,
    # Penalize impossible German patterns
}

# German frequency data for unigram scoring
german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
    'Q': 0.001
}

confirmed = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U',
}
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

fixed_codes = {}
for code, letter in confirmed.items():
    if code in pair_to_idx:
        fixed_codes[pair_to_idx[code]] = letters.index(letter)

free_codes = [pi for pi in range(n_pairs) if pi not in fixed_codes]

# Build pair index array from current mapping
pair_freq_arr = [pair_counts[all_pair_codes[i]] for i in range(n_pairs)]
mapping_arr = [0] * n_pairs
for code, letter in mapping.items():
    if code in pair_to_idx:
        mapping_arr[pair_to_idx[code]] = letters.index(letter)
for pi, li in fixed_codes.items():
    mapping_arr[pi] = li

def decode_text(marr):
    """Decode all pairs to text."""
    return ''.join(letters[marr[pair_to_idx[p]]] for p in all_pairs)

def word_score(text):
    """Score based on German word occurrences."""
    score = 0
    for word, weight in german_words_weighted.items():
        count = text.count(word)
        score += count * weight
    return score

def freq_score(marr):
    """Penalize deviation from German frequencies."""
    letter_freq = [0]*26
    total = 0
    for pi in range(n_pairs):
        letter_freq[marr[pi]] += pair_freq_arr[pi]
        total += pair_freq_arr[pi]
    score = 0
    for li in range(26):
        obs = letter_freq[li] / total
        exp = german_freq.get(letters[li], 0.001)
        weight = 1.0 / max(exp, 0.003)
        score -= weight * (obs - exp) ** 2 * 100
    return score

def total_score(marr, text=None):
    if text is None:
        text = decode_text(marr)
    return word_score(text) + freq_score(marr)

current_text = decode_text(mapping_arr)
current_score = total_score(mapping_arr, current_text)
print(f"Initial score: {current_score:.2f} (words: {word_score(current_text)}, freq: {freq_score(mapping_arr):.2f})", flush=True)
print(f"Initial word hits:", flush=True)
for word, weight in sorted(german_words_weighted.items(), key=lambda x: -x[1]):
    c = current_text.count(word)
    if c > 0:
        print(f"  '{word}': {c} times (weight {weight})", flush=True)

print(f"\n{'='*70}", flush=True)
print("GREEDY HILL CLIMBING", flush=True)
print(f"{'='*70}", flush=True)

best_mapping = list(mapping_arr)
best_score = current_score

for iteration in range(50):
    improved = False
    random.shuffle(free_codes)

    for pi in free_codes:
        old_letter = best_mapping[pi]
        best_letter = old_letter
        best_local_score = best_score

        for li in range(26):
            if li == old_letter:
                continue
            best_mapping[pi] = li
            text = decode_text(best_mapping)
            s = total_score(best_mapping, text)
            if s > best_local_score:
                best_local_score = s
                best_letter = li

        best_mapping[pi] = best_letter
        if best_letter != old_letter:
            improved = True
            best_score = best_local_score

    text = decode_text(best_mapping)
    ws = word_score(text)
    fs = freq_score(best_mapping)
    print(f"  Iteration {iteration}: score={best_score:.2f} (words={ws}, freq={fs:.2f})", flush=True)

    if not improved:
        print("  No improvement, stopping.", flush=True)
        break

# Show final results
print(f"\n{'='*70}", flush=True)
print("FINAL MAPPING", flush=True)
print(f"{'='*70}", flush=True)

final_mapping = {}
for pi in range(n_pairs):
    final_mapping[all_pair_codes[pi]] = letters[best_mapping[pi]]

mapping_by_letter = {}
for pair, letter in sorted(final_mapping.items()):
    if letter not in mapping_by_letter:
        mapping_by_letter[letter] = []
    mapping_by_letter[letter].append(pair)

for letter in sorted(mapping_by_letter.keys(), key=lambda l: -german_freq.get(l, 0)):
    codes = sorted(mapping_by_letter[letter])
    tc = sum(pair_counts.get(c, 0) for c in codes)
    pct = tc / len(all_pairs) * 100
    exp = german_freq.get(letter, 0) * 100
    fixed_mark = [c for c in codes if pair_to_idx.get(c) in fixed_codes]
    print(f"  {letter} ({exp:.1f}% exp, {pct:.1f}% obs): {codes} [fixed: {fixed_mark}]", flush=True)

# Decode and show
print(f"\n{'='*70}", flush=True)
print("DECODED BOOKS", flush=True)
print(f"{'='*70}", flush=True)

final_text = decode_text(best_mapping)
ws = word_score(final_text)
print(f"Total word score: {ws}", flush=True)
for word, weight in sorted(german_words_weighted.items(), key=lambda x: -x[1]):
    c = final_text.count(word)
    if c > 0:
        print(f"  '{word}': {c} times", flush=True)

# Show longest books
book_decoded = []
for i, bp in enumerate(book_pairs):
    decoded = ''.join(final_mapping.get(p, '?') for p in bp)
    book_decoded.append((i, decoded, len(decoded)))

book_decoded.sort(key=lambda x: -x[2])
for idx, decoded, length in book_decoded[:10]:
    print(f"\n  Book {idx} ({length} letters, off={book_offsets[idx]}):", flush=True)
    for j in range(0, len(decoded), 80):
        print(f"    {decoded[j:j+80]}", flush=True)

# Save
with open('best_mapping.json', 'w') as f:
    json.dump(final_mapping, f, indent=2)
print(f"\nSaved mapping to best_mapping.json", flush=True)

print(f"\n{'='*70}", flush=True)
print("DONE", flush=True)
print(f"{'='*70}", flush=True)
