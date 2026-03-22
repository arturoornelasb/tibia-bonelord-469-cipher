"""Tier 14 decoder: 92 codes assigned. Adds 39=E and 87=W to tier 13."""
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

# TIER 14 MAPPING: 92 codes
all_codes = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U', '00': 'H', '14': 'N', '72': 'R',
    '91': 'S', '15': 'I', '76': 'E', '52': 'S', '42': 'D',
    '46': 'I', '48': 'N', '57': 'H', '04': 'M', '12': 'S',
    '58': 'N', '78': 'T', '51': 'R', '35': 'A', '34': 'L',
    '01': 'E', '59': 'S', '41': 'E', '30': 'E', '94': 'H',
    '47': 'D', '13': 'N', '71': 'I', '63': 'D', '93': 'N',
    '28': 'D', '86': 'E', '43': 'U', '70': 'U', '65': 'I',
    '16': 'I', '36': 'W', '64': 'T', '89': 'A', '80': 'G',
    '97': 'G', '75': 'T', '08': 'R', '20': 'F', '96': 'L',
    '99': 'O', '55': 'R', '67': 'E', '27': 'E', '03': 'E',
    '09': 'E', '05': 'C', '53': 'N', '44': 'U', '62': 'B',
    '68': 'R', '23': 'S', '17': 'E', '29': 'E', '66': 'A',
    '49': 'E', '38': 'K', '77': 'Z', '22': 'K', '82': 'O',
    '73': 'N', '50': 'I', '84': 'G', '25': 'O', '83': 'V',
    '81': 'T', '24': 'I', '79': 'O', '10': 'R', '54': 'M',
    '98': 'T',
    # Tier 14 additions:
    '39': 'E',  # ORTE in 2/2 contexts
    '87': 'W',  # WIR in 2/2 contexts
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# Decode and report
print("=" * 80)
print(f"TIER 14 DECODER: {len(all_codes)} codes assigned")
print("=" * 80)

total_pairs = 0
decoded_pairs = 0
letter_counts = Counter()
unknown_codes = Counter()
all_text = []

for idx, bpairs in enumerate(book_pairs):
    text = ''
    for p in bpairs:
        total_pairs += 1
        letter = all_codes.get(p)
        if letter:
            decoded_pairs += 1
            letter_counts[letter] += 1
            text += letter
        else:
            unknown_codes[p] += 1
            text += '?'
    all_text.append(text)

print(f"\nCoverage: {decoded_pairs}/{total_pairs} = {decoded_pairs/total_pairs*100:.1f}%")
print(f"Unknown codes: {len(unknown_codes)} unique, {sum(unknown_codes.values())} total occurrences")

# Unknown codes
print("\nUnknown code frequencies:")
for code, cnt in unknown_codes.most_common():
    print(f"  {code}: {cnt}")

# Letter frequencies
german_freq = {
    'E': 16.93, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
    'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
    'L': 3.44, 'C': 3.06, 'G': 3.01, 'M': 2.53, 'O': 2.51,
    'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
    'P': 0.79, 'V': 0.67,
}

total_letters = sum(letter_counts.values())
print(f"\nLetter frequencies ({total_letters} total):")
for letter in sorted(german_freq.keys(), key=lambda l: -german_freq[l]):
    count = letter_counts.get(letter, 0)
    pct = count / total_letters * 100
    exp = german_freq[letter]
    delta = pct - exp
    flag = " !!!" if abs(delta) > 2.0 else " !" if abs(delta) > 1.0 else ""
    n_codes = sum(1 for c, l in all_codes.items() if l == letter)
    print(f"  {letter}: {count:4d} ({pct:5.1f}%) exp={exp:5.2f}% delta={delta:+5.1f}% codes={n_codes}{flag}")

# Word counting
german_words = [
    'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO', 'DU', 'OB', 'AM', 'IM',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST',
    'WIR', 'ICH', 'SIE', 'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI', 'VOR', 'FUR', 'BIS', 'ALS',
    'TAG', 'ORT', 'TOD', 'OFT', 'NIE', 'ALT', 'NEU', 'NUN', 'HIN',
    'NACH', 'AUCH', 'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN',
    'DASS', 'WENN', 'DANN', 'DENN', 'ABER', 'ODER', 'WEIL',
    'EINE', 'DIES', 'HIER', 'DORT', 'WELT', 'ZEIT', 'TEIL',
    'ERDE', 'GOTT', 'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN',
    'HELD', 'MACHT', 'KRAFT', 'GEIST', 'NACHT', 'LICHT',
    'HABEN', 'WERDEN', 'KOMMEN', 'GEHEN', 'SEHEN', 'FINDEN',
    'ALLE', 'ALLES', 'ALLEN', 'KEINE', 'VIELE',
    'ERSTE', 'ANDEREN', 'SEINE', 'SEINER', 'SEINEN',
    'EINEN', 'EINER', 'EINEM', 'EINES',
    'NICHT', 'NICHTS', 'IMMER', 'WIEDER',
    'RUNE', 'RUNEN', 'STEIN', 'STEINE', 'STEINEN',
    'ORTE', 'ORTEN', 'KOENIG', 'URALTE', 'URALTEN',
    'ENDE', 'TEILE', 'TEILEN', 'FINDEN',
    'TAGE', 'TAGEN', 'NACHT', 'LAND', 'LEBEN',
    'DIESE', 'DIESER', 'DIESES',
]
word_set = set(german_words)

# Scan for words
word_counts = Counter()
full = ''.join(all_text)
for w in word_set:
    start = 0
    while True:
        pos = full.find(w, start)
        if pos == -1:
            break
        word_counts[w] += 1
        start = pos + 1

print(f"\nTop 25 German words found (substring match):")
for w, cnt in word_counts.most_common(25):
    print(f"  {w}: {cnt}")

# Show decoded text for longer books
print(f"\n{'='*80}")
print("DECODED TEXT (books with 60+ pairs)")
print("=" * 80)
for idx, text in enumerate(all_text):
    if len(book_pairs[idx]) >= 60:
        print(f"\nBk{idx:2d} ({len(book_pairs[idx])}p): {text}")
