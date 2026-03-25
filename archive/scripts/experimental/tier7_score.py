"""
Comprehensive scoring: for each remaining unknown code, compute the best letter
based on bigram compatibility + word evidence + frequency needs.
"""
import json
from collections import Counter, defaultdict

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

# Tier 1-6 mapping (62 codes)
fixed = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U',
    '00': 'H', '14': 'N', '72': 'R', '91': 'S', '15': 'I',
    '76': 'E', '52': 'S', '42': 'D', '46': 'I', '48': 'N',
    '57': 'H', '04': 'M', '12': 'S', '58': 'N',
    '78': 'T', '51': 'R', '35': 'A', '34': 'L',
    '01': 'E', '59': 'S', '41': 'E', '30': 'E',
    '94': 'H',
    '47': 'D', '13': 'N', '71': 'I', '79': 'H', '63': 'D',
    '93': 'N', '28': 'D', '86': 'E', '43': 'U',
    '70': 'U', '65': 'I', '16': 'I', '36': 'W',
    '64': 'T', '89': 'A', '80': 'G', '97': 'G', '75': 'T',
    '08': 'R', '20': 'F', '96': 'L', '99': 'O', '55': 'R',
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

pair_counts = Counter()
for pairs in book_pairs:
    pair_counts.update(pairs)
total_pairs = sum(pair_counts.values())

# German bigram frequencies (relative, top pairs)
german_bigrams = {
    'EN': 3.88, 'ER': 3.75, 'CH': 2.75, 'DE': 2.00, 'EI': 1.88,
    'ND': 1.88, 'TE': 1.67, 'IN': 1.65, 'IE': 1.64, 'GE': 1.43,
    'ES': 1.36, 'NE': 1.26, 'SE': 1.20, 'RE': 1.18, 'HE': 1.16,
    'AN': 1.14, 'UN': 1.14, 'ST': 1.13, 'BE': 1.06, 'DI': 0.98,
    'EL': 0.92, 'AU': 0.87, 'IC': 0.86, 'NG': 0.82, 'SI': 0.77,
    'IT': 0.75, 'NI': 0.75, 'SC': 0.75, 'AL': 0.73, 'ET': 0.73,
    'LI': 0.73, 'RA': 0.72, 'RI': 0.72, 'HI': 0.69, 'IS': 0.69,
    'IG': 0.68, 'DA': 0.66, 'UE': 0.66, 'WI': 0.65, 'WE': 0.64,
    'TI': 0.63, 'ME': 0.63, 'HA': 0.62, 'NT': 0.62, 'EC': 0.61,
    'LE': 0.58, 'NS': 0.57, 'ED': 0.56, 'MI': 0.54, 'AS': 0.53,
    'ON': 0.51, 'RD': 0.50, 'EM': 0.48, 'SS': 0.48, 'US': 0.47,
    'EU': 0.46, 'DU': 0.46, 'UF': 0.45, 'AB': 0.44, 'UR': 0.44,
    'RN': 0.44, 'WA': 0.43, 'OL': 0.43, 'AR': 0.42, 'SO': 0.42,
    'EH': 0.41, 'OC': 0.40, 'HT': 0.40, 'BI': 0.38, 'OR': 0.38,
    'VO': 0.38, 'ZU': 0.38, 'OD': 0.37, 'MA': 0.37, 'AT': 0.37,
    'AH': 0.36, 'SU': 0.35, 'EG': 0.35, 'TO': 0.35, 'NO': 0.35,
    'DO': 0.34, 'TR': 0.34, 'OT': 0.33, 'UG': 0.33, 'UT': 0.32,
    'TA': 0.32, 'IL': 0.32, 'AE': 0.31, 'HN': 0.31, 'FE': 0.31,
    'RU': 0.30, 'TU': 0.30, 'KE': 0.30, 'LT': 0.30, 'ZE': 0.30,
    'OE': 0.29, 'FO': 0.28, 'AG': 0.28, 'EW': 0.28, 'LA': 0.27,
}

# Get neighbor profiles for each unknown code
unknown_codes = sorted(set(pair_counts.keys()) - set(fixed.keys()),
                       key=lambda c: -pair_counts.get(c, 0))

german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
}

# Current letter counts
letter_counts = Counter()
for c, l in fixed.items():
    letter_counts[l] += pair_counts.get(c, 0)

print("=" * 70)
print("COMPREHENSIVE UNKNOWN CODE SCORING")
print("=" * 70)

# For each unknown code, score against each plausible letter
results = {}

for code in unknown_codes:
    freq = pair_counts.get(code, 0)
    if freq < 5:
        continue

    # Get neighbor distributions
    left = Counter()
    right = Counter()
    for bpairs in book_pairs:
        for j, p in enumerate(bpairs):
            if p != code:
                continue
            if j > 0 and bpairs[j-1] in fixed:
                left[fixed[bpairs[j-1]]] += 1
            if j < len(bpairs)-1 and bpairs[j+1] in fixed:
                right[fixed[bpairs[j+1]]] += 1

    # Score each letter
    scores = {}
    for letter in 'ENOABFMCKLZGWIRDSHTU':
        score = 0
        # Bigram compatibility
        for left_letter, ct in left.items():
            bigram = left_letter + letter
            if bigram in german_bigrams:
                score += ct * german_bigrams[bigram]
            else:
                score -= ct * 0.1  # small penalty for uncommon bigrams

        for right_letter, ct in right.items():
            bigram = letter + right_letter
            if bigram in german_bigrams:
                score += ct * german_bigrams[bigram]
            else:
                score -= ct * 0.1

        # Frequency need bonus: letters with bigger deficits get a boost
        current_pct = letter_counts.get(letter, 0) / total_pairs
        expected_pct = german_freq.get(letter, 0)
        deficit = expected_pct - current_pct
        if deficit > 0:
            score += deficit * 100 * freq / total_pairs * 50  # bonus for filling deficit

        scores[letter] = score

    # Sort by score
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    results[code] = {
        'freq': freq,
        'left': dict(left.most_common(5)),
        'right': dict(right.most_common(5)),
        'ranked': ranked[:5],
    }

# Display results
for code in sorted(results.keys(), key=lambda c: -results[c]['freq']):
    r = results[code]
    if r['freq'] < 5:
        continue
    ranked_str = ', '.join(f"{l}:{s:.1f}" for l, s in r['ranked'])
    best = r['ranked'][0]
    second = r['ranked'][1]
    confidence = "HIGH" if best[1] > second[1] * 1.5 else "MED" if best[1] > second[1] * 1.2 else "LOW"

    print(f"\n  {code} (freq={r['freq']}) [{confidence}]")
    print(f"    Best: {ranked_str}")
    print(f"    L={r['left']}  R={r['right']}")


# Now group by best letter assignment
print(f"\n{'='*70}")
print("PROPOSED ASSIGNMENTS (grouped by letter)")
print("=" * 70)

assignments = defaultdict(list)
for code, r in sorted(results.items(), key=lambda x: -x[1]['freq']):
    if r['freq'] < 5:
        continue
    best_letter = r['ranked'][0][0]
    best_score = r['ranked'][0][1]
    second_score = r['ranked'][1][1]
    confidence = best_score / max(second_score, 0.1)
    assignments[best_letter].append((code, r['freq'], best_score, confidence))

for letter in sorted(assignments.keys(), key=lambda l: -german_freq.get(l, 0)):
    codes = assignments[letter]
    total_freq = sum(f for _, f, _, _ in codes)
    current_pct = letter_counts.get(letter, 0) / total_pairs * 100
    expected_pct = german_freq.get(letter, 0) * 100
    new_pct = (letter_counts.get(letter, 0) + total_freq) / total_pairs * 100

    print(f"\n  {letter}: current={current_pct:.1f}% expected={expected_pct:.1f}% "
          f"-> with all: {new_pct:.1f}% ({len(codes)} codes)")
    for code, freq, score, conf in sorted(codes, key=lambda x: -x[1]):
        marker = "***" if conf > 1.5 else "**" if conf > 1.2 else "*"
        print(f"    {code} (freq={freq}, score={score:.1f}, conf={conf:.1f}) {marker}")


# Word evidence for top candidates
print(f"\n{'='*70}")
print("WORD EVIDENCE FOR TOP CANDIDATES")
print("=" * 70)

def test_word(word, target_code, target_pos):
    count = 0
    for bpairs in book_pairs:
        for j in range(len(bpairs) - len(word) + 1):
            window = bpairs[j:j+len(word)]
            match = True
            for k in range(len(word)):
                if k == target_pos:
                    if window[k] != target_code:
                        match = False
                        break
                else:
                    if window[k] not in fixed or fixed[window[k]] != word[k]:
                        match = False
                        break
            if match:
                count += 1
    return count

# Test specific assignments
tests = {
    '67': {'E': ['EINE', 'DIESE', 'SEINER', 'WERDEN', 'ANDERE', 'JEDER', 'HIER'],
           'R': ['DER', 'ODER', 'JEDER', 'RUNE', 'RUNEN', 'DURCH'],
           'O': ['NOCH', 'ODER', 'DORT', 'WORT', 'GROSS', 'GOTT']},
    '27': {'O': ['NOCH', 'ODER', 'DORT', 'WORT', 'VON', 'OFT', 'GROSS', 'DOCH', 'HOCH'],
           'E': ['EINE', 'DIESE', 'SEINE', 'ANDERE', 'WERDEN', 'JEDER'],
           'B': ['ABER', 'BUCH', 'HABEN', 'GEBEN', 'BERG']},
    '03': {'E': ['EINE', 'DIESE', 'SEINE', 'ANDERE', 'WERDEN', 'GEBEN', 'ALLE'],
           'B': ['ABER', 'BEI', 'BIS', 'BUCH', 'BERG'],
           'K': ['KEIN', 'KANN', 'KONNTE', 'KRAFT']},
    '53': {'N': ['UND', 'SIND', 'SEIN', 'EINE', 'EINEN', 'RUNEN', 'STEINEN'],
           'E': ['EINE', 'DIESE', 'SEINE', 'WERDEN']},
    '84': {'E': ['EINE', 'DIESE', 'SEINE', 'ANDERE', 'WERDEN'],
           'A': ['DAS', 'EINE', 'SEINE', 'ANDERE', 'HABE']},
    '24': {'E': ['EINE', 'DIESE', 'SEINE', 'ANDERE', 'WERDEN', 'JEDER'],
           'A': ['DAS', 'EINE', 'ALLE', 'ANDERE']},
    '09': {'E': ['EINE', 'DIESE', 'SEINE', 'ANDERE', 'WERDEN'],
           'K': ['KEIN', 'KANN', 'KONNTE', 'KRAFT']},
    '68': {'E': ['EINE', 'DIESE', 'SEINE', 'ANDERE', 'TEIL'],
           'A': ['DAS', 'EINE', 'SEINE', 'ALLE']},
    '50': {'E': ['EINE', 'DIESE', 'SEINE', 'WERDEN'],
           'B': ['ABER', 'BUCH', 'BIS', 'HABEN']},
    '05': {'E': ['EINE', 'DIESE', 'SEINE', 'WERDEN'],
           'C': ['NOCH', 'DOCH', 'NICHT', 'ICH']},
}

for code, letter_words in tests.items():
    freq = pair_counts.get(code, 0)
    print(f"\n  Code {code} (freq={freq}):")
    for letter, words in letter_words.items():
        hits = []
        for word in words:
            for pos in range(len(word)):
                if word[pos] == letter:
                    ct = test_word(word, code, pos)
                    if ct > 0:
                        hits.append(f"{word}:{ct}")
        total = sum(int(h.split(':')[1]) for h in hits)
        if hits:
            print(f"    {letter}: {total} hits [{', '.join(hits)}]")
        else:
            print(f"    {letter}: 0 hits")


print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
