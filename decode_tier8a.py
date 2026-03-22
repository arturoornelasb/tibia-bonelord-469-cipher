"""
Tier 8a: 71 + strong new assignments.
23=S (ERSTE:8), 17=E (RE/ER conf=4.74), 29=E (USEND), 66=A (DAS/DASS)
Also test: 22=D (ERD pattern), 49=E (HEL pattern)
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

# All 71 tier 7b codes
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
    '67': 'E', '27': 'E', '03': 'E', '09': 'E',
    '05': 'C', '53': 'N',
    '44': 'U', '62': 'B', '68': 'R',
}

# Tier 8a: strong evidence
tier8a = {
    '23': 'S',  # R={T:11} 100% -> ST; ER23TE=ERSTE:8
    '17': 'E',  # L={R:10} R={R:9} -> RE+ER; conf=4.74
    '29': 'E',  # US29ND -> USEND (TAUSEND); conf=2.76
    '66': 'A',  # L={D:9} R={S:10} -> DAS/DASS; HD_SS:9
    '22': 'D',  # L={R:11} -> RD (0.50); ERD pattern -> ERDE
    '49': 'E',  # L={H:9} R={L:8} -> HEL; conf=2.08
}

all_codes = {**fixed, **tier8a}

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
print(f"TIER 8a DECODER: {len(all_codes)} fixed codes")
print("=" * 70)

print(f"\nKnown: {known_total}/{total_pairs} ({known_total/total_pairs*100:.1f}%)")
print(f"Unknown: {unknown_total}/{total_pairs} ({unknown_total/total_pairs*100:.1f}%)")

print(f"\nLetter frequencies ({len(all_codes)} codes):")
for l in sorted(german_freq, key=lambda x: -german_freq[x])[:20]:
    obs = letter_freq.get(l, 0) / total_pairs * 100
    exp = german_freq[l] * 100
    diff = obs - exp
    n_codes = sum(1 for c in all_codes if all_codes[c] == l)
    marker = " !!" if abs(diff) > 2 else ""
    print(f"  {l}: {obs:.1f}% (exp {exp:.1f}%, diff {diff:+.1f}%, {n_codes} codes){marker}")

# Decode
full_text = ''
for bpairs in book_pairs:
    full_text += ''.join(all_codes.get(p, '?') for p in bpairs)

known_pct = sum(1 for c in full_text if c != '?') / len(full_text) * 100
print(f"\nText known: {known_pct:.1f}%")

# Decode books
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
    'BESCHRIEBEN', 'BESONDERE', 'BESTIMMTE',
    'GEMACHT', 'GESEHEN', 'GEWESEN', 'GEFUNDEN',
    'GELESEN', 'GEGEBEN', 'GESCHRIEBEN',
    'GEHEIMEN', 'GEHEIMNISSE',
    'ENTDECKEN', 'ENTDECKT',
    'BRAUCHEN', 'BRAUCHTE', 'GEBRAUCHT',
    'ABER', 'OBEN', 'NEBEN',
    'HABEN', 'GEBEN', 'LEBEN',
    # New words enabled by tier 8a
    'ERSTE', 'ERSTEN', 'ERSTER', 'ERSTES',
    'ERDE', 'ERDEN',
    'DASS',
    'TAUSEND',
    'ANDERES', 'ANDERER',
    'NEUES', 'NEUEN', 'NEUE', 'NEUER',
    'ALLES', 'ALLEN',
    'IHREN', 'IHRES', 'IHREM',
    'SEINEN', 'SEINER', 'SEINES',
    'DIESEN', 'DESSEN',
    'JEDES', 'JEDEM', 'JEDEN',
]

word_hits = {}
for word in sorted(set(german_words), key=lambda w: -len(w)):
    ct = full_text.count(word)
    if ct > 0:
        word_hits[word] = ct

for word, ct in sorted(word_hits.items(), key=lambda x: -len(x[0]) * x[1]):
    if ct >= 2 or len(word) >= 5:
        print(f"  {word}: {ct}")


# Bigram validation
print(f"\n{'='*70}")
print("BIGRAM CHECK")
print("=" * 70)

bigram_counts = Counter()
for i in range(len(full_text) - 1):
    if full_text[i] != '?' and full_text[i+1] != '?':
        bigram_counts[full_text[i:i+2]] += 1

print("New bigrams from 8a codes:")
for bg in ['ST', 'TS', 'SE', 'ES', 'SS', 'DS', 'SD',
           'RE', 'ER', 'EE', 'DE', 'ED', 'DA', 'AD', 'AS', 'SA',
           'RD', 'DR', 'DD', 'HE', 'EH', 'HL', 'EL', 'LE']:
    ct = bigram_counts.get(bg, 0)
    if ct > 0:
        print(f"  {bg}: {ct}")

print("\nUnusual (should be low):")
for bg in ['EE', 'II', 'HH', 'DD', 'NN', 'SS', 'AA', 'RR', 'UU']:
    ct = bigram_counts.get(bg, 0)
    if ct > 0:
        print(f"  {bg}: {ct}")


# ERSTE validation
print(f"\n{'='*70}")
print("NEUE WORDS VALIDATION")
print("=" * 70)

new_tests = ['ERSTE', 'ERSTEN', 'ERSTER', 'ERDE', 'ERDEN',
             'DASS', 'TAUSEND', 'ANDERES',
             'DESSEN', 'IHREN', 'SEINES', 'SEINEN',
             'NEUEN', 'NEUE', 'ALLES', 'ALLEN',
             'DIESEN', 'JEDES', 'JEDEN',
             'HELFEN', 'HELD', 'STELLEN', 'SCHNELL']
for word in new_tests:
    ct = full_text.count(word)
    if ct > 0:
        print(f"  {word}: {ct}")


# Remaining unknowns
print(f"\n{'='*70}")
print("REMAINING UNKNOWN CODES")
print("=" * 70)

print(f"\nDeficits:")
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
