"""Audit II and HH bigrams to find likely misassigned codes."""
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
    '67': 'E', '27': 'E', '03': 'E', '09': 'E', '05': 'C', '53': 'N',
    '44': 'U', '62': 'B', '68': 'R',
    '23': 'S', '17': 'E', '29': 'E', '66': 'A', '49': 'E',
    '38': 'K', '77': 'Z',
    '22': 'K', '82': 'O', '73': 'N', '50': 'I', '84': 'G',
    '25': 'O', '83': 'V', '81': 'T', '24': 'I',
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# Find which CODE PAIRS produce II and HH bigrams
ii_pairs = Counter()  # (code1, code2) -> count
hh_pairs = Counter()
ee_pairs = Counter()
dd_pairs = Counter()

for bpairs in book_pairs:
    for j in range(len(bpairs) - 1):
        c1, c2 = bpairs[j], bpairs[j+1]
        if c1 in all_codes and c2 in all_codes:
            l1, l2 = all_codes[c1], all_codes[c2]
            if l1 == 'I' and l2 == 'I':
                ii_pairs[(c1, c2)] += 1
            elif l1 == 'H' and l2 == 'H':
                hh_pairs[(c1, c2)] += 1
            elif l1 == 'E' and l2 == 'E':
                ee_pairs[(c1, c2)] += 1
            elif l1 == 'D' and l2 == 'D':
                dd_pairs[(c1, c2)] += 1

print("=" * 70)
print("II BIGRAM SOURCES (51 total)")
print("=" * 70)
for (c1, c2), ct in ii_pairs.most_common():
    print(f"  {c1}(I) + {c2}(I): {ct}")

print(f"\n{'='*70}")
print("HH BIGRAM SOURCES (22 total)")
print("=" * 70)
for (c1, c2), ct in hh_pairs.most_common():
    print(f"  {c1}(H) + {c2}(H): {ct}")

print(f"\n{'='*70}")
print("DD BIGRAM SOURCES (14 total)")
print("=" * 70)
for (c1, c2), ct in dd_pairs.most_common():
    print(f"  {c1}(D) + {c2}(D): {ct}")

print(f"\n{'='*70}")
print("EE BIGRAM SOURCES (54 total)")
print("=" * 70)
for (c1, c2), ct in ee_pairs.most_common(20):
    print(f"  {c1}(E) + {c2}(E): {ct}")

# Now: for each I-code, count how many II bigrams it participates in
print(f"\n{'='*70}")
print("I-CODE II-PARTICIPATION")
print("=" * 70)

i_codes = [c for c, l in all_codes.items() if l == 'I']
h_codes = [c for c, l in all_codes.items() if l == 'H']

pair_counts = Counter()
for bpairs in book_pairs:
    pair_counts.update(bpairs)

for code in sorted(i_codes, key=lambda c: -pair_counts.get(c, 0)):
    freq = pair_counts.get(code, 0)
    ii_count = sum(ct for (c1, c2), ct in ii_pairs.items() if c1 == code or c2 == code)
    ii_rate = ii_count / freq * 100 if freq > 0 else 0
    print(f"  {code}=I (freq={freq}): II involvement={ii_count} ({ii_rate:.1f}%)")

print(f"\n{'='*70}")
print("H-CODE HH-PARTICIPATION")
print("=" * 70)

for code in sorted(h_codes, key=lambda c: -pair_counts.get(c, 0)):
    freq = pair_counts.get(code, 0)
    hh_count = sum(ct for (c1, c2), ct in hh_pairs.items() if c1 == code or c2 == code)
    hh_rate = hh_count / freq * 100 if freq > 0 else 0
    print(f"  {code}=H (freq={freq}): HH involvement={hh_count} ({hh_rate:.1f}%)")

# Test: what if we swap the worst II offender to deficit letters?
print(f"\n{'='*70}")
print("SWAP TESTS: WORST II/HH OFFENDERS -> DEFICIT LETTERS")
print("=" * 70)

german_words = [
    'RUNENSTEIN', 'INSCHRIFT', 'VERSCHIEDENE',
    'GESCHRIEBEN', 'SCHREIBEN', 'SCHRIFT',
    'VERSTEHEN', 'GEHEIMNIS', 'GEHEIME', 'GEHEIM',
    'BIBLIOTHEK', 'ZWISCHEN',
    'STEINEN', 'STEINE', 'STEIN',
    'RUNEN', 'RUNE',
    'DIESER', 'DIESES', 'DIESEM', 'DIESEN', 'DIESE',
    'NICHT', 'NICHTS',
    'EINEN', 'EINER', 'EINE', 'EINEM',
    'ANDEREN', 'ANDERE',
    'WERDEN', 'WURDE', 'WORDEN',
    'HABEN', 'HATTE',
    'DURCH', 'GEGEN', 'UNTER', 'HINTER',
    'IMMER', 'WIEDER', 'SCHON', 'NOCH',
    'MACHT', 'KRAFT', 'GEIST',
    'LICHT', 'NACHT',
    'WISSEN', 'KENNEN', 'SEHEN', 'FINDEN',
    'AUCH', 'ABER', 'ODER', 'WENN', 'DANN', 'DENN',
    'SICH', 'SIND', 'SEIN', 'SEINE',
    'DASS', 'HIER', 'DORT', 'WELT',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES',
    'UND', 'IST', 'EIN', 'WIR', 'ICH', 'SIE',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI',
    'NUR', 'WAS', 'MAN', 'WER', 'WIE', 'GUT',
    'TAG', 'TEIL', 'ZEIT', 'WORT', 'NAME',
    'DOCH', 'HOCH', 'FORT', 'VOLK', 'GOLD', 'SOHN',
    'ERSTE', 'ERSTEN', 'ERDE', 'ERDEN', 'TAUSEND',
    'ALLES', 'ALLEN', 'KLAR', 'ZU',
    'KOENIG', 'ORT', 'ORTE', 'ORTEN', 'VIEL',
    'GEBOREN', 'GESCHAFFEN', 'VERSPRECHEN',
    'KOMMEN', 'GEHEN', 'NEHMEN',
    'KRIEGER', 'KRIEG', 'HERR', 'HERREN', 'MEISTER',
    'NORDEN', 'SUEDEN', 'BERG', 'BURG',
    'TOD', 'HELD', 'GOTT',
    'SPRECHEN', 'KEINE', 'KEINEN',
    'STIMME', 'STIMMEN', 'BRUDER', 'BLUT',
    'MORGEN', 'ABEND', 'HIMMEL',
    'MACHEN', 'GEMACHT', 'SOMMER',
    'FALLEN', 'HELFEN', 'SCHNELL',
    'ZUSAMMEN', 'ZURUECK',
    'PLATZ', 'PERSON', 'BEISPIEL',
    'GROSS', 'ALT', 'NEU',
    'BEREITS', 'BEIDE', 'NEBEN', 'OBEN',
    'UEBER', 'OPFER', 'NICHT',
]

# Build baseline text
base_text = ''
for bpairs in book_pairs:
    base_text += ''.join(all_codes.get(p, '?') for p in bpairs)

base_word_counts = {}
for w in german_words:
    base_word_counts[w] = base_text.count(w)

# Count baseline bad bigrams
base_bad = {}
for bg in ['II', 'HH', 'DD', 'EE']:
    base_bad[bg] = base_text.count(bg)

# Test swapping each I-code and H-code to deficit letters
deficit_letters = ['M', 'B', 'F', 'P', 'A', 'L', 'O', 'W']

for code in sorted(i_codes + h_codes, key=lambda c: -pair_counts.get(c, 0)):
    orig = all_codes[code]
    freq = pair_counts.get(code, 0)
    if freq < 15:
        continue

    print(f"\n--- Swap {code}={orig} (freq={freq}) ---")
    for new_letter in deficit_letters:
        test_codes = {**all_codes, code: new_letter}
        test_text = ''
        for bpairs in book_pairs:
            test_text += ''.join(test_codes.get(p, '?') for p in bpairs)

        # Word differential
        new_words = []
        lost_words = []
        for w in german_words:
            old = base_word_counts[w]
            new = test_text.count(w)
            if new > old:
                new_words.append((w, new - old))
            elif new < old:
                lost_words.append((w, old - new))

        # Bigram change
        bigram_delta = {}
        for bg in ['II', 'HH', 'DD', 'EE']:
            delta = test_text.count(bg) - base_bad[bg]
            if delta != 0:
                bigram_delta[bg] = delta

        word_gain = sum(d * len(w) for w, d in new_words)
        word_loss = sum(d * len(w) for w, d in lost_words)
        net = word_gain - word_loss

        if net > 0 or any(v < -3 for v in bigram_delta.values()):
            gains = ', '.join(f"{w}:+{d}" for w, d in sorted(new_words, key=lambda x: -x[1]*len(x[0]))[:4])
            losses = ', '.join(f"{w}:-{d}" for w, d in sorted(lost_words, key=lambda x: -x[1]*len(x[0]))[:3])
            bg_str = ' '.join(f"{k}:{v:+d}" for k, v in bigram_delta.items())
            print(f"  -> {new_letter}: net={net:+d} gain=[{gains}] loss=[{losses}] bigrams=[{bg_str}]")
