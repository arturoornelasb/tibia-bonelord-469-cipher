"""
Tier 4 decoder: 39 tier 1-3 codes + new word-pattern derived codes.
Focus on codes with 100% word ratio or strong combined evidence.
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

# Tiers 1-3 (39 codes) + Tier 4 (word-pattern derived)
fixed = {
    # Confirmed (16)
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U',
    # Tier 1 (5)
    '00': 'H', '14': 'N', '72': 'R', '91': 'S', '15': 'I',
    # Tier 2 (9)
    '76': 'E', '52': 'S', '42': 'D', '46': 'I', '48': 'N',
    '57': 'H', '04': 'M', '12': 'S', '58': 'N',
    # Tier 3 - URALTE (8) + CH pattern
    '78': 'T', '51': 'R', '35': 'A', '34': 'L',
    '01': 'E', '59': 'S', '41': 'E', '30': 'E',
    '94': 'H',
    # Tier 4A - 100% word ratio
    '47': 'D',   # 11 hits 100% - DEN
    '13': 'N',   # 12 hits 100% - EIN, SEIN
    '71': 'I',   # 8 hits 100% - ICH
    '79': 'H',   # 8 hits 100% - IHR
    '63': 'D',   # 6 hits 100% - DEN
    # Tier 4B - strong combined evidence
    '93': 'N',   # 16 hits 67% - STEINEN + joint analysis
    '28': 'D',   # 8 hits 89% - DEN
    '86': 'E',   # 11 hits 65% - DIE + bigram E:81.9
    '43': 'U',   # 11 hits - UND, RUNEN (STR43NEN = ST RUNEN!)
    '70': 'U',   # 12 hits - UND
    '65': 'I',   # 23 hits 52% - IST, ICH, HIER (H->I context)
    '16': 'I',   # 8 hits 89% - SIE
    '36': 'W',   # 25 hits - WIR (strongest word signal)
}

fixed_idxs = {}
for code, letter in fixed.items():
    if code in pair_to_idx:
        fixed_idxs[pair_to_idx[code]] = letters.index(letter)

free_codes = [pi for pi in range(n_pairs) if pi not in fixed_idxs]
print(f"Fixed: {len(fixed_idxs)} codes, Free: {len(free_codes)} codes")

# German frequencies
german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
    'Q': 0.001
}

pair_freq_arr = [pair_counts[all_pair_codes[i]] for i in range(n_pairs)]

# Check distribution
letter_fixed_count = Counter()
letter_fixed_freq = [0.0] * 26
for pi, li in fixed_idxs.items():
    letter_fixed_freq[li] += pair_freq_arr[pi] / total_pairs
    letter_fixed_count[letters[li]] += 1

print(f"\nFixed code distribution:")
for li in range(26):
    l = letters[li]
    exp = german_freq.get(l, 0.001)
    obs = letter_fixed_freq[li]
    if letter_fixed_count[l] > 0 or exp > 0.01:
        diff = obs - exp
        marker = "!!" if abs(diff) > 0.03 else ("!" if abs(diff) > 0.02 else "")
        print(f"  {l}: {letter_fixed_count[l]:2d} codes, {obs*100:5.1f}% obs (exp {exp*100:.1f}%, diff {diff*100:+.1f}%) {marker}")

# Frequency-based initialization for free codes
mapping_arr = [0] * n_pairs
for pi, li in fixed_idxs.items():
    mapping_arr[pi] = li

letter_remaining = {}
for li in range(26):
    exp = german_freq.get(letters[li], 0.001)
    remaining = exp - letter_fixed_freq[li]
    letter_remaining[li] = max(remaining, 0.0)

free_sorted = sorted(free_codes, key=lambda pi: -pair_freq_arr[pi])
for pi in free_sorted:
    freq_contribution = pair_freq_arr[pi] / total_pairs
    best_li = max(range(26), key=lambda li: letter_remaining[li])
    mapping_arr[pi] = best_li
    letter_remaining[best_li] -= freq_contribution

# Scoring
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
    'URALTE': 20, 'URALTEN': 25,
    'MACHT': 10, 'KRAFT': 10, 'GEIST': 10,
    'NICHTS': 12, 'SEINE': 10, 'DIESEN': 10,
    'ZWISCHEN': 20, 'ANDERE': 12, 'ANDEREN': 15,
    'KONNTE': 12, 'MUSSTE': 12, 'SOLLTE': 12,
    'SCHON': 8, 'IMMER': 10, 'WIEDER': 10,
    'UEBER': 8, 'HINTER': 10,
    'KLEINE': 10, 'KLEINEN': 12,
    'ALTEN': 8, 'ALTE': 5,
    'JEDER': 8, 'JEDES': 8,
    'NACHT': 8, 'LICHT': 8,
    'WISSEN': 10, 'LESEN': 8,
}

german_bigrams = {
    'EN': 3.88, 'ER': 3.75, 'CH': 2.75, 'DE': 2.00, 'EI': 1.88,
    'ND': 1.88, 'TE': 1.67, 'IN': 1.65, 'IE': 1.64, 'GE': 1.43,
    'ES': 1.36, 'NE': 1.26, 'SE': 1.20, 'RE': 1.18, 'HE': 1.16,
    'AN': 1.14, 'UN': 1.14, 'ST': 1.13, 'BE': 1.06, 'DI': 0.98,
    'EM': 0.93, 'AU': 0.93, 'SC': 0.86, 'DA': 0.86, 'SI': 0.82,
    'LE': 0.82, 'IC': 0.81, 'TI': 0.73, 'AL': 0.71, 'HA': 0.71,
    'NG': 0.67, 'WE': 0.65, 'EL': 0.65, 'HI': 0.58, 'NS': 0.57,
    'NT': 0.56, 'IS': 0.55, 'HT': 0.54, 'MI': 0.52, 'IT': 0.50,
    'RI': 0.41, 'AB': 0.38, 'LI': 0.35, 'ED': 0.35, 'EG': 0.34,
    'NI': 0.33, 'ET': 0.33, 'IG': 0.32, 'AR': 0.31, 'RU': 0.30,
    'WI': 0.28, 'LA': 0.29, 'BI': 0.27, 'FE': 0.26, 'ZU': 0.25,
}

def decode_text(marr):
    return ''.join(letters[marr[pair_to_idx[p]]] for p in all_pairs)

def word_score(text):
    return sum(text.count(word) * weight for word, weight in german_words_weighted.items())

def bigram_score(text):
    return sum(german_bigrams.get(text[i:i+2], 0) for i in range(len(text) - 1))

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
        score -= weight * (obs - exp) ** 2 * 3000  # Even stronger penalty
    return score

def total_score(marr, text=None):
    if text is None:
        text = decode_text(marr)
    return word_score(text) + bigram_score(text) * 0.3 + freq_score(marr)

current_text = decode_text(mapping_arr)
current_score = total_score(mapping_arr, current_text)
print(f"\nInitial score: {current_score:.2f}")

# HILL CLIMBING
print(f"\n{'='*70}")
print("HILL CLIMBING")
print(f"{'='*70}")

best_mapping = list(mapping_arr)
best_score = current_score

for iteration in range(80):
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

    # Random swaps
    for _ in range(400):
        i = random.choice(free_codes)
        j = random.choice(free_codes)
        if i == j or best_mapping[i] == best_mapping[j]:
            continue
        best_mapping[i], best_mapping[j] = best_mapping[j], best_mapping[i]
        text = decode_text(best_mapping)
        s = total_score(best_mapping, text)
        if s > best_score:
            best_score = s
            improved = True
        else:
            best_mapping[i], best_mapping[j] = best_mapping[j], best_mapping[i]

    if iteration < 10 or iteration % 5 == 0 or not improved:
        text = decode_text(best_mapping)
        ws = word_score(text)
        bs = bigram_score(text)
        fs = freq_score(best_mapping)
        print(f"  Iter {iteration}: score={best_score:.1f} (words={ws}, bigrams={bs:.0f}, freq={fs:.1f})")

    if not improved:
        print("  No improvement, stopping.")
        break

# Results
print(f"\n{'='*70}")
print("FINAL MAPPING")
print(f"{'='*70}")

final_mapping = {}
for pi in range(n_pairs):
    final_mapping[all_pair_codes[pi]] = letters[best_mapping[pi]]

letter_codes = {}
for code, letter in final_mapping.items():
    letter_codes.setdefault(letter, []).append(code)

for letter in sorted(letter_codes, key=lambda l: -german_freq.get(l, 0)):
    codes = sorted(letter_codes[letter])
    tc = sum(pair_counts.get(c, 0) for c in codes)
    pct = tc / total_pairs * 100
    exp = german_freq.get(letter, 0) * 100
    fixed_list = [c for c in codes if c in fixed]
    free_list = [c for c in codes if c not in fixed]
    print(f"  {letter} ({exp:.1f}% exp, {pct:.1f}% obs, {len(codes)} codes): fixed={fixed_list} free={free_list}")

# Decode books
print(f"\n{'='*70}")
print("DECODED BOOKS")
print(f"{'='*70}")

final_text = decode_text(best_mapping)
ws = word_score(final_text)
bs = bigram_score(final_text)
print(f"Total word score: {ws}, bigram score: {bs:.0f}")

# Show word hits
for word in sorted(german_words_weighted, key=lambda w: -german_words_weighted[w]):
    c = final_text.count(word)
    if c > 0:
        print(f"  '{word}': {c} times")

book_decoded = []
for i, pairs in enumerate(book_data):
    decoded = ''.join(final_mapping.get(p, '?') for p in pairs)
    book_decoded.append((i, decoded))

book_decoded.sort(key=lambda x: -len(x[1]))
for idx, decoded in book_decoded[:10]:
    print(f"\n  Book {idx} ({len(decoded)} letters):")
    for j in range(0, len(decoded), 80):
        print(f"    {decoded[j:j+80]}")

# Key patterns
target_codes = ['45','21','76','52','19','72','78','30','46','48','76','51','59','56','46','11','41','45','19']
decoded_pattern = ''.join(final_mapping.get(c, '?') for c in target_codes)
print(f"\n  19-pair pattern: {decoded_pattern}")

far_context = ['74','45','45','19','04','50','42','15','95','61','51','35','34','78','01','92','88','95','21','60','19','93','64','67','24','31','42','78','94','31','51','91','18','65','12']
far_decoded = ''.join(final_mapping.get(c, '?') for c in far_context)
print(f"  Extended STEIN context: {far_decoded}")

# Save
with open('best_mapping.json', 'w') as f:
    json.dump(final_mapping, f, indent=2)

print(f"\n{'='*70}")
print("DONE")
print(f"{'='*70}")
