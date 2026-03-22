"""Tier 13 decoder — 90 codes, 99.2% coverage.
Includes 54=M and 98=T from tier 13 analysis."""
import json
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

# TIER 13 MAPPING — 90 codes
all_codes = {
    # Tier 1-3: Frequency + IC (36 codes)
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U',
    '00': 'H', '14': 'N', '72': 'R', '91': 'S', '15': 'I',
    '76': 'E', '52': 'S', '42': 'D', '46': 'I', '48': 'N',
    '57': 'H', '04': 'M', '12': 'S', '58': 'N',
    '78': 'T', '51': 'R', '35': 'A', '34': 'L',
    '01': 'E', '59': 'S', '41': 'E', '30': 'E',
    # Tier 4-6: Frequency expansion (26 codes)
    '94': 'H',
    '47': 'D', '13': 'N', '71': 'I', '63': 'D',
    '93': 'N', '28': 'D', '86': 'E', '43': 'U',
    '70': 'U', '65': 'I', '16': 'I', '36': 'W',
    '64': 'T', '89': 'A', '80': 'G', '97': 'G', '75': 'T',
    '08': 'R', '20': 'F', '96': 'L', '99': 'O', '55': 'R',
    '67': 'E', '27': 'E', '03': 'E',
    # Tier 7-8: Context + frequency (16 codes)
    '09': 'E', '05': 'C', '53': 'N',
    '44': 'U', '62': 'B', '68': 'R',
    '23': 'S', '17': 'E', '29': 'E', '66': 'A', '49': 'E',
    '38': 'K', '77': 'Z',
    # Tier 9: KOENIG resolution (5 codes)
    '22': 'K', '82': 'O', '73': 'N', '50': 'I', '84': 'G',
    # Tier 10: Differential word test (4 codes)
    '25': 'O', '83': 'V', '81': 'T', '24': 'I',
    # Tier 12: Bigram audit (2 codes)
    '79': 'O', '10': 'R',
    # Tier 13: Mystery term analysis (2 codes)
    '54': 'M', '98': 'T',
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# Decode all books
print("=" * 80)
print("TIER 13 DECODER — 90 codes, includes 54=M and 98=T")
print("=" * 80)

total_pairs = 0
total_known = 0
all_decoded = []
letter_counts = Counter()
unknown_counts = Counter()

for idx, bpairs in enumerate(book_pairs):
    decoded = ''
    for p in bpairs:
        if p in all_codes:
            decoded += all_codes[p]
            letter_counts[all_codes[p]] += 1
            total_known += 1
        else:
            decoded += '?'
            unknown_counts[p] += 1
        total_pairs += 1
    all_decoded.append(decoded)

print(f"\nCoverage: {total_known}/{total_pairs} = {total_known/total_pairs*100:.1f}%")
print(f"Unknown pairs: {total_pairs - total_known}")

# Show remaining unknowns
print(f"\nRemaining unknown codes:")
for code, cnt in unknown_counts.most_common():
    print(f"  {code}: {cnt} occurrences")

# Letter frequency analysis
total_letters = sum(letter_counts.values())
german_freq = {
    'E': 16.93, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
    'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
    'L': 3.44, 'C': 3.06, 'G': 3.01, 'M': 2.53, 'O': 2.51,
    'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
    'P': 0.79, 'V': 0.67, 'J': 0.27, 'Y': 0.04, 'X': 0.03, 'Q': 0.02,
}

print(f"\nLetter frequency (sorted by deviation):")
deviations = []
for letter in sorted(german_freq.keys(), key=lambda x: -german_freq[x]):
    count = letter_counts.get(letter, 0)
    pct = count / total_letters * 100
    expected = german_freq[letter]
    delta = pct - expected
    deviations.append((letter, pct, expected, delta, count))

for letter, pct, expected, delta, count in sorted(deviations, key=lambda x: -abs(x[3])):
    n_codes = sum(1 for v in all_codes.values() if v == letter)
    flag = " !!!" if abs(delta) > 2 else (" *" if abs(delta) > 1 else "")
    print(f"  {letter}: {pct:5.1f}% (exp {expected:4.1f}%, {delta:+5.1f}%) [{n_codes} codes, {count} pairs]{flag}")

# Word count
german_words = set([
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES',
    'EIN', 'EINE', 'EINEN', 'EINER', 'EINEM', 'EINES',
    'UND', 'IST', 'WIR', 'ICH', 'SIE', 'MAN', 'WER',
    'NICHT', 'NICHTS', 'SEIN', 'SEINE', 'SEINER', 'SEINEN',
    'DIESE', 'DIESER', 'DIESES', 'DIESEM', 'DIESEN',
    'RUNE', 'RUNEN', 'STEIN', 'STEINE', 'STEINEN',
    'KOENIG', 'ORT', 'ORTE', 'ORTEN', 'RUNEORT',
    'URALTE', 'URALTEN', 'FINDEN', 'TEIL', 'TEILE',
    'DASS', 'WENN', 'DANN', 'ABER', 'ODER',
    'HIER', 'DORT', 'ENDE', 'ERSTE', 'ERSTEN',
    'GOTT', 'HERR', 'HELD', 'MACHT', 'KRAFT',
    'TAG', 'TAGE', 'NACHT', 'WELT', 'ERDE',
    'AM', 'UM', 'IM', 'ZUM', 'VOM',
    'NACH', 'AUCH', 'NOCH', 'DOCH', 'SCHON',
])

full_text = ''.join(all_decoded)
print(f"\nKey word counts:")
for word in sorted(german_words, key=lambda w: -full_text.count(w)):
    cnt = full_text.count(word)
    if cnt >= 3:
        print(f"  {word}: {cnt}")

# Show decoded books (longest ones)
print(f"\n{'='*80}")
print("DECODED BOOKS (longest)")
print("=" * 80)

for idx, (bpairs, decoded) in enumerate(zip(book_pairs, all_decoded)):
    if len(bpairs) >= 80:
        print(f"\nBook {idx} ({len(bpairs)} pairs):")
        for j in range(0, len(decoded), 80):
            print(f"  {j:4d}: {decoded[j:j+80]}")
