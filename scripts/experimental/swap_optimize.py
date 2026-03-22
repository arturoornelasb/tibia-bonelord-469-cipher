"""
Swap-based hill climbing for code-to-letter mapping.
Instead of trying all 26 letters for each code, swap letters between two codes.
This preserves overall frequency distribution.

Fix confirmed codes + high-confidence bigram-derived codes.
Use word-matching + frequency scoring.
"""
import json
import random
from collections import Counter

with open('books.json', 'r') as f:
    books = json.load(f)

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    ic0 = ic_from_counts(Counter(bp0), len(bp0))
    ic1 = ic_from_counts(Counter(bp1), len(bp1))
    return 0 if ic0 > ic1 else 1

book_data = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_data.append(pairs)

all_pairs = []
for pairs in book_data:
    all_pairs.extend(pairs)
pair_counts = Counter(all_pairs)
all_pair_codes = sorted(pair_counts.keys())
pair_to_idx = {p: i for i, p in enumerate(all_pair_codes)}
n_pairs = len(all_pair_codes)
total_pairs = sum(pair_counts.values())

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Fixed assignments (confirmed + tier 1 bigram)
fixed = {
    # Confirmed from cribs
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U',
    # Tier 1 bigram (overwhelming evidence)
    '00': 'H',  # C->00 x56 (CH digraph)
    '14': 'N',  # U->14 x59 (UN bigram)
    '72': 'R',  # E->72 x40, 72->U x41 (ER, RU)
    '91': 'S',  # 91->C x51 (SCH), E->91 x26 (ES)
    '15': 'I',  # D->15 x12 + 15->E x31 (DIE, IE)
}

fixed_idxs = {}
for code, letter in fixed.items():
    if code in pair_to_idx:
        fixed_idxs[pair_to_idx[code]] = letters.index(letter)

free_codes = [pi for pi in range(n_pairs) if pi not in fixed_idxs]

# German frequency targets
german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
    'Q': 0.001
}

# Initialize: assign remaining codes to letters based on frequency matching
# Sort free codes by frequency (descending)
pair_freq_arr = [pair_counts[all_pair_codes[i]] for i in range(n_pairs)]
free_sorted = sorted(free_codes, key=lambda pi: -pair_freq_arr[pi])

# Target: distribute free codes proportionally to expected frequencies
# First calculate how much frequency each letter already has from fixed codes
letter_fixed_freq = [0.0] * 26
for pi, li in fixed_idxs.items():
    letter_fixed_freq[li] += pair_freq_arr[pi] / total_pairs

# Calculate remaining needed frequency for each letter
letter_remaining = {}
for li in range(26):
    exp = german_freq.get(letters[li], 0.001)
    remaining = exp - letter_fixed_freq[li]
    letter_remaining[li] = max(remaining, 0.0)

# Assign free codes greedily to letters that need more frequency
mapping_arr = [0] * n_pairs
for pi, li in fixed_idxs.items():
    mapping_arr[pi] = li

# Sort letters by remaining need (descending)
for pi in free_sorted:
    freq_contribution = pair_freq_arr[pi] / total_pairs
    # Find letter with most remaining need
    best_li = max(range(26), key=lambda li: letter_remaining[li])
    mapping_arr[pi] = best_li
    letter_remaining[best_li] -= freq_contribution

# German words for scoring
german_words_weighted = {
    'RUNENSTEIN': 50, 'RUNENSTEINEN': 60, 'STEINEN': 30,
    'NICHT': 20, 'EINER': 15, 'EINEN': 15, 'DIESE': 15, 'DIESER': 20,
    'WERDEN': 15, 'WURDE': 15, 'WAREN': 15, 'HABEN': 15,
    'STEINE': 25, 'STEINER': 25,
    'STEIN': 10, 'RUNE': 8, 'RUNEN': 12, 'AUCH': 8,
    'NACH': 8, 'NOCH': 8, 'WENN': 8, 'DANN': 8,
    'ABER': 8, 'ODER': 8, 'ALLE': 8, 'WELT': 8,
    'SICH': 10, 'SIND': 8, 'DASS': 8,
    'ENDE': 5, 'HABE': 8, 'KANN': 8, 'WIRD': 8,
    'DER': 3, 'DIE': 3, 'DAS': 3, 'UND': 3,
    'IST': 3, 'EIN': 2, 'DEN': 2, 'DEM': 2,
    'VON': 3, 'HAT': 3, 'AUF': 3, 'MIT': 3,
    'DES': 2, 'SIE': 2, 'ICH': 3, 'AUS': 3,
    'BEI': 2, 'WIR': 3, 'NUR': 3, 'EINE': 5,
    'SEIN': 5, 'HIER': 5, 'IHRE': 5, 'JEDE': 5,
    'DURCH': 10, 'GEGEN': 10, 'UNTER': 10,
    'SCHRIFT': 15, 'SPRACHE': 15, 'ZEICHEN': 15,
    'AUGE': 8, 'AUGEN': 10, 'FEUER': 10,
    'DUNKEL': 10, 'LICHT': 10, 'LEBEN': 10,
    'MACHT': 10, 'KRAFT': 10, 'GEIST': 10,
    'NICHTS': 12, 'SEINE': 10, 'DIESEN': 10,
    'ZWISCHEN': 20, 'ANDERE': 12, 'ANDEREN': 15,
    'KONNTE': 12, 'MUSSTE': 12, 'SOLLTE': 12,
    'SCHON': 8, 'IMMER': 10, 'WIEDER': 10,
    'UEBER': 8, 'UNTER': 8, 'HINTER': 10,
}

# Common German bigrams with weights
german_bigrams = {
    'EN': 3.88, 'ER': 3.75, 'CH': 2.75, 'DE': 2.00, 'EI': 1.88,
    'ND': 1.88, 'TE': 1.67, 'IN': 1.65, 'IE': 1.64, 'GE': 1.43,
    'ES': 1.36, 'NE': 1.26, 'SE': 1.20, 'RE': 1.18, 'HE': 1.16,
    'AN': 1.14, 'UN': 1.14, 'ST': 1.13, 'BE': 1.06, 'DI': 0.98,
    'EM': 0.93, 'AU': 0.93, 'SC': 0.86, 'DA': 0.86, 'SI': 0.82,
    'LE': 0.82, 'IC': 0.81, 'TI': 0.73, 'AL': 0.71, 'HA': 0.71,
    'NG': 0.67, 'WE': 0.65, 'EL': 0.65, 'HI': 0.58, 'NS': 0.57,
    'NT': 0.56, 'IS': 0.55, 'HT': 0.54, 'MI': 0.52, 'IT': 0.50,
}

def decode_text(marr):
    return ''.join(letters[marr[pair_to_idx[p]]] for p in all_pairs)

def word_score(text):
    score = 0
    for word, weight in german_words_weighted.items():
        count = text.count(word)
        score += count * weight
    return score

def bigram_score(text):
    score = 0
    for i in range(len(text) - 1):
        bg = text[i:i+2]
        if bg in german_bigrams:
            score += german_bigrams[bg]
    return score

def freq_score(marr):
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
        score -= weight * (obs - exp) ** 2 * 1000
    return score

def total_score(marr, text=None):
    if text is None:
        text = decode_text(marr)
    return word_score(text) + bigram_score(text) * 0.5 + freq_score(marr)

current_text = decode_text(mapping_arr)
current_score = total_score(mapping_arr, current_text)
print(f"Initial score: {current_score:.2f}", flush=True)
print(f"  words={word_score(current_text)}, bigrams={bigram_score(current_text):.1f}, freq={freq_score(mapping_arr):.2f}", flush=True)

# SWAP-BASED HILL CLIMBING
print(f"\n{'='*70}", flush=True)
print("SWAP HILL CLIMBING", flush=True)
print(f"{'='*70}", flush=True)

best_mapping = list(mapping_arr)
best_score = current_score

for iteration in range(100):
    improved = False
    random.shuffle(free_codes)

    # Try single-code changes
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

    # Try swaps between pairs of free codes
    swap_improved = False
    for attempt in range(min(500, len(free_codes) * 5)):
        i = random.choice(free_codes)
        j = random.choice(free_codes)
        if i == j or best_mapping[i] == best_mapping[j]:
            continue

        # Swap
        best_mapping[i], best_mapping[j] = best_mapping[j], best_mapping[i]
        text = decode_text(best_mapping)
        s = total_score(best_mapping, text)
        if s > best_score:
            best_score = s
            swap_improved = True
            improved = True
        else:
            # Undo swap
            best_mapping[i], best_mapping[j] = best_mapping[j], best_mapping[i]

    text = decode_text(best_mapping)
    ws = word_score(text)
    bs = bigram_score(text)
    fs = freq_score(best_mapping)

    if iteration < 10 or iteration % 5 == 0 or not improved:
        print(f"  Iter {iteration}: score={best_score:.2f} (words={ws}, bigrams={bs:.0f}, freq={fs:.2f})", flush=True)

    if not improved:
        print("  No improvement, stopping.", flush=True)
        break

# Results
print(f"\n{'='*70}", flush=True)
print("FINAL MAPPING", flush=True)
print(f"{'='*70}", flush=True)

final_mapping = {}
for pi in range(n_pairs):
    final_mapping[all_pair_codes[pi]] = letters[best_mapping[pi]]

# Show letter distribution
letter_codes = {}
for code, letter in final_mapping.items():
    letter_codes.setdefault(letter, []).append(code)

for letter in sorted(letter_codes, key=lambda l: -german_freq.get(l, 0)):
    codes = sorted(letter_codes[letter])
    tc = sum(pair_counts.get(c, 0) for c in codes)
    pct = tc / total_pairs * 100
    exp = german_freq.get(letter, 0) * 100
    fixed_list = [c for c in codes if c in fixed]
    print(f"  {letter} ({exp:.1f}% exp, {pct:.1f}% obs, {len(codes)} codes): {codes} [fixed: {fixed_list}]", flush=True)

# Decode key books
print(f"\n{'='*70}", flush=True)
print("DECODED BOOKS", flush=True)
print(f"{'='*70}", flush=True)

final_text = decode_text(best_mapping)
ws = word_score(final_text)
bs = bigram_score(final_text)
print(f"Total word score: {ws}, bigram score: {bs:.0f}", flush=True)

for word in sorted(german_words_weighted, key=lambda w: -german_words_weighted[w]):
    c = final_text.count(word)
    if c > 0:
        print(f"  '{word}': {c} times", flush=True)

book_decoded = []
for i, pairs in enumerate(book_data):
    decoded = ''.join(final_mapping.get(p, '?') for p in pairs)
    book_decoded.append((i, decoded))

book_decoded.sort(key=lambda x: -len(x[1]))
for idx, decoded in book_decoded[:10]:
    print(f"\n  Book {idx} ({len(decoded)} letters):", flush=True)
    for j in range(0, len(decoded), 80):
        print(f"    {decoded[j:j+80]}", flush=True)

# Show the 19-pair pattern
target_codes = ['45','21','76','52','19','72','78','30','46','48','76','51','59','56','46','11','41','45','19']
decoded_pattern = ''.join(final_mapping.get(c, '?') for c in target_codes)
print(f"\n  19-pair pattern: {decoded_pattern}", flush=True)

# Pre-STEIN context
far_context = ['74','45','45','19','04','50','42','15','95','61','51','35','34','78','01','92','88','95','21','60','19','93','64','67','24','31','42','78','94','31','51','91','18','65','12']
far_decoded = ''.join(final_mapping.get(c, '?') for c in far_context)
print(f"  Extended STEIN context: {far_decoded}", flush=True)

# Save
with open('best_mapping.json', 'w') as f:
    json.dump(final_mapping, f, indent=2)
print(f"\nSaved mapping to best_mapping.json", flush=True)

print(f"\n{'='*70}", flush=True)
print("DONE", flush=True)
print(f"{'='*70}", flush=True)
