"""
Tier 8b: 77 + 3 strong new assignments.
82=I (DIE pattern), 38=K (KLAR:2), 77=Z (ZU:5)
Total: 80 codes.
"""
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

# All 77 tier 8a codes + 3 tier 8b
all_codes = {
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
    '67': 'E', '27': 'E', '03': 'E', '09': 'E',
    '05': 'C', '53': 'N',
    '44': 'U', '62': 'B', '68': 'R',
    '23': 'S', '17': 'E', '29': 'E', '66': 'A', '22': 'D', '49': 'E',
    # Tier 8b
    '82': 'I',  # D[82]E=11 -> DIE; DI(0.98)+IE(1.64) top bigrams
    '38': 'K',  # KLAR:2 word hits; KL bigram; fills K deficit
    '77': 'Z',  # ZU:5 word hits; fills Z deficit from 0%
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

german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
}

letter_freq = Counter()
for c, l in all_codes.items():
    letter_freq[l] += pair_counts.get(c, 0)

known_total = sum(pair_counts[c] for c in all_codes)
unknown_total = total_pairs - known_total

print("=" * 70)
print(f"TIER 8b DECODER: {len(all_codes)} fixed codes")
print("=" * 70)

print(f"\nKnown: {known_total}/{total_pairs} ({known_total/total_pairs*100:.1f}%)")
print(f"Unknown: {unknown_total}/{total_pairs} ({unknown_total/total_pairs*100:.1f}%)")

print(f"\nLetter frequencies:")
for l in sorted(german_freq, key=lambda x: -german_freq[x]):
    obs = letter_freq.get(l, 0) / total_pairs * 100
    exp = german_freq[l] * 100
    diff = obs - exp
    n_codes = sum(1 for c in all_codes if all_codes[c] == l)
    marker = " !!" if abs(diff) > 2 else " !" if abs(diff) > 1.5 else ""
    print(f"  {l}: {obs:.1f}% (exp {exp:.1f}%, diff {diff:+.1f}%, {n_codes} codes){marker}")

# Decode
full_text = ''
for bpairs in book_pairs:
    full_text += ''.join(all_codes.get(p, '?') for p in bpairs)

known_pct = sum(1 for c in full_text if c != '?') / len(full_text) * 100
print(f"\nText known: {known_pct:.1f}%")

# Books
print(f"\n{'='*70}")
print("DECODED BOOKS (longest)")
print("=" * 70)

book_decoded = []
for i, bpairs in enumerate(book_pairs):
    decoded = ''.join(all_codes.get(p, f'[{p}]') for p in bpairs)
    book_decoded.append((i, decoded, len(bpairs)))

book_decoded.sort(key=lambda x: -x[2])

for idx, decoded, length in book_decoded[:15]:
    print(f"\n  Book {idx} ({length} pairs):")
    for j in range(0, len(decoded), 90):
        print(f"    {decoded[j:j+90]}")

# Word hits
print(f"\n{'='*70}")
print("WORD HITS")
print("=" * 70)

german_words = [
    'RUNENSTEIN', 'INSCHRIFT', 'INSCHRIFTEN',
    'URALTE', 'URALTEN', 'VERSCHIEDENE',
    'GESCHRIEBEN', 'SCHREIBEN', 'SCHRIFT',
    'VERSTEHEN', 'GEHEIMNIS', 'GEHEIME',
    'BIBLIOTHEK', 'ZWISCHEN',
    'STEINEN', 'STEINE', 'STEIN',
    'RUNEN', 'RUNE',
    'DIESER', 'DIESES', 'DIESEM', 'DIESEN', 'DIESE',
    'NICHT', 'NICHTS',
    'EINEN', 'EINER', 'EINE', 'EINEM',
    'ANDEREN', 'ANDERE', 'ANDERER',
    'WERDEN', 'WURDE', 'WORDEN',
    'HABEN', 'HATTE', 'HATTEN',
    'KONNTE', 'KOENNEN', 'KANN',
    'MUSSTE', 'SOLLTE', 'WOLLTE',
    'DURCH', 'GEGEN', 'UNTER', 'HINTER',
    'IMMER', 'WIEDER', 'SCHON', 'NOCH',
    'MACHT', 'KRAFT', 'GEIST',
    'LICHT', 'DUNKEL', 'NACHT',
    'WISSEN', 'KENNEN', 'SEHEN', 'FINDEN',
    'ALLE', 'JEDER', 'JEDES', 'JEDE',
    'AUCH', 'ABER', 'ODER', 'WENN', 'DANN', 'DENN',
    'GANZ', 'SEHR', 'VIEL', 'WENIG',
    'SICH', 'SIND', 'SEIN', 'SEINE',
    'DASS', 'HIER', 'DORT', 'WELT',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES',
    'UND', 'IST', 'EIN', 'WIR', 'ICH', 'SIE',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI',
    'NUR', 'WAS', 'MAN', 'WER', 'WIE', 'GUT',
    'TAG', 'TEIL', 'ZEIT', 'WORT', 'NAME',
    'OFT', 'DOCH', 'HOCH', 'SOLCH', 'WELCH',
    'FORT', 'MILCH', 'VOLK', 'GOLD', 'SOHN',
    'ERSTE', 'ERSTEN', 'ERSTER', 'ERSTES',
    'ERDE', 'ERDEN',
    'TAUSEND',
    'ALLES', 'ALLEN',
    'KLAR',
    'ZU', 'ZURUECK', 'ZUSAMMEN', 'ZEIT',
    'ZEICHEN', 'ZWEI', 'ZWISCHEN',
    'DIESEN', 'DESSEN', 'JEDEN', 'JEDES',
    'IHREN', 'SEINEN', 'SEINES',
    'HELFEN', 'HELD', 'STELLEN', 'SCHNELL',
    'DAZU', 'HIERZULANDE',
]

word_hits = {}
for word in sorted(set(german_words), key=lambda w: -len(w)):
    ct = full_text.count(word)
    if ct > 0:
        word_hits[word] = ct

for word, ct in sorted(word_hits.items(), key=lambda x: (-len(x[0]) * x[1], -len(x[0]))):
    if ct >= 2 or len(word) >= 5:
        print(f"  {word}: {ct}")

# New tier 8b specific word tests
print(f"\n--- Tier 8b new words ---")
new_words = ['DIE', 'DIES', 'DIESE', 'KLAR', 'KLARE',
             'ZU', 'ZURUECK', 'ZWEI', 'DAZU',
             'ZEICHEN', 'ZEIT', 'ZWISCHEN',
             'KIRCHE', 'KOENIG', 'KLEIN',
             'KEIN', 'KEINE', 'KEINEN']
for word in sorted(set(new_words), key=lambda w: -len(w)):
    ct = full_text.count(word)
    if ct > 0:
        print(f"  {word}: {ct}")


# Bigram check
print(f"\n{'='*70}")
print("BIGRAM CHECK")
print("=" * 70)

bigram_counts = Counter()
for i in range(len(full_text) - 1):
    if full_text[i] != '?' and full_text[i+1] != '?':
        bigram_counts[full_text[i:i+2]] += 1

print("New bigrams from 8b codes:")
for bg in ['DI', 'ID', 'IE', 'II', 'ZU', 'UZ', 'ZE', 'EZ',
           'KL', 'KE', 'EK', 'KO', 'HK', 'NK', 'LK',
           'IZ', 'ZI', 'SZ', 'ZS', 'AZ', 'ZA',
           'IK', 'KI']:
    ct = bigram_counts.get(bg, 0)
    if ct > 0:
        print(f"  {bg}: {ct}")

print("\nUnusual (should be low):")
for bg in ['EE', 'II', 'HH', 'DD', 'NN', 'SS', 'AA', 'RR', 'UU',
           'KK', 'ZZ', 'IZ', 'ZI', 'IK', 'KI']:
    ct = bigram_counts.get(bg, 0)
    if ct > 0:
        print(f"  {bg}: {ct}")


# Remaining
print(f"\n{'='*70}")
print("REMAINING DEFICITS")
print("=" * 70)

for l in sorted(german_freq, key=lambda l: german_freq[l] - letter_freq.get(l,0)/total_pairs):
    obs = letter_freq.get(l, 0) / total_pairs * 100
    exp = german_freq[l] * 100
    diff = exp - obs
    if diff > 0.3:
        need = diff / 100 * total_pairs
        print(f"  {l}: obs={obs:.1f}% exp={exp:.1f}% deficit={diff:.1f}% (need ~{need:.0f} pairs)")

print(f"\nRemaining unknown codes (freq>=3):")
unknown_codes = sorted(set(pair_counts.keys()) - set(all_codes.keys()),
                       key=lambda c: -pair_counts.get(c, 0))
for c in unknown_codes:
    freq = pair_counts[c]
    if freq >= 3:
        left = Counter()
        right = Counter()
        for bpairs in book_pairs:
            for j, p in enumerate(bpairs):
                if p != c: continue
                if j > 0 and bpairs[j-1] in all_codes:
                    left[all_codes[bpairs[j-1]]] += 1
                if j < len(bpairs)-1 and bpairs[j+1] in all_codes:
                    right[all_codes[bpairs[j+1]]] += 1
        print(f"  {c} (freq={freq}): L={dict(left.most_common(5))} R={dict(right.most_common(5))}")


print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
