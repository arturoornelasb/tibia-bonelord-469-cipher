"""
Differential word test: count ONLY new word instances created by each assignment.
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
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# Baseline text
base_text = ''
for bpairs in book_pairs:
    base_text += ''.join(all_codes.get(p, '?') for p in bpairs)

# Test words
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
    'ANDEREN', 'ANDERE', 'ANDERER',
    'WERDEN', 'WURDE', 'WORDEN',
    'HABEN', 'HATTE', 'HATTEN',
    'KONNTE', 'KOENNEN', 'KANN',
    'MUSSTE', 'SOLLTE', 'WOLLTE',
    'DURCH', 'GEGEN', 'UNTER', 'HINTER',
    'IMMER', 'WIEDER', 'SCHON', 'NOCH',
    'MACHT', 'KRAFT', 'GEIST', 'GEISTER',
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
    'ERSTE', 'ERSTEN', 'ERDE', 'ERDEN', 'TAUSEND',
    'ALLES', 'ALLEN', 'KLAR', 'ZU',
    'KOENIG', 'DERKOENIG',
    'DIESEN', 'DESSEN', 'SEINEN', 'SEINES',
    'HELFEN', 'HELD', 'SCHNELL',
    'ORT', 'ORTE', 'ORTEN', 'DORT',
    'VIEL', 'VIELE', 'VIELEN',
    'VOLK', 'VOELKER',
    'IMMER', 'NIMMER',
    'GEHEIM', 'GEHEIMNIS',
    'BORN', 'GEBOREN',
    'OBEN', 'NEBEN',
    'BEIDE', 'BEREITS',
    'ABER', 'UEBER',
    'KOERPER', 'OPFER',
    'SPRECHEN', 'VERSPRECHEN',
    'PLATZ', 'BEISPIEL',
    'PERSON', 'PERSONEN',
    'NAME', 'NAMEN',
    'STIMME', 'STIMMEN',
    'KOMMEN', 'BEKOMMEN', 'ANKOMMEN',
    'NEHMEN', 'ANNEHMEN',
    'FLAMME', 'ZUSAMMEN',
    'STAMM',
    'SOMMER', 'HAMMER', 'ZIMMER', 'NUMMER',
    'AMMER', 'KAMMER',
    'HIMMEL',
    'BRAUCHEN', 'BRAUCHTE',
    'MACHEN', 'GEMACHT',
    'ANDER', 'ANDERS',
    'BLUT', 'BRUDER',
    'FALLEN', 'GEFALLEN',
    'LAUFEN', 'VERLAUFEN',
    'RUFEN', 'GERUFEN',
    'SCHAFFEN', 'GESCHAFFEN',
    'TREFFEN', 'GETROFFEN',
    'HOFFEN', 'GEHOFFT',
    'WOHNEN', 'GEWOHNT',
    'SOHN', 'SOEHNE',
    'MORGEN', 'MORGENS',
    'ABEND', 'ABENDS',
    'NORDEN', 'SUEDEN', 'OSTEN', 'WESTEN',
    'BERG', 'BERGE', 'BERGEN',
    'BURG', 'BURGEN',
    'KRIEG', 'KRIEGER',
    'TOD', 'TODE', 'TOTEN',
    'GOTT', 'GOETTER',
    'HERR', 'HERREN',
    'MEISTER',
]

# Compute base word counts
base_counts = {}
for w in german_words:
    base_counts[w] = base_text.count(w)

# For each unknown code x each candidate letter, compute differential
unknowns = ['24', '81', '83', '74', '54', '25', '10', '40']
candidates = 'ABCDEFGHIKLMNOPRSTUVWZ'

print("=" * 70)
print("DIFFERENTIAL WORD HITS (new instances only)")
print("=" * 70)

for code in unknowns:
    print(f"\n--- Code {code} ---")
    best_total = 0
    best_letter = ''
    results = []

    for letter in candidates:
        test_codes = {**all_codes, code: letter}
        test_text = ''
        for bpairs in book_pairs:
            test_text += ''.join(test_codes.get(p, '?') for p in bpairs)

        # Count differential word hits
        new_hits = []
        total_new = 0
        for w in german_words:
            old = base_counts[w]
            new = test_text.count(w)
            diff = new - old
            if diff > 0:
                new_hits.append((w, diff))
                total_new += diff * len(w)  # weight by word length

        # Count new bad bigrams (doubled letters)
        bad_bigrams = 0
        for bg in ['EE', 'II', 'HH', 'DD', 'NN', 'SS', 'AA', 'RR', 'UU', 'KK', 'ZZ', 'GG']:
            old_bg = base_text.count(bg)
            new_bg = test_text.count(bg)
            bad_bigrams += max(0, new_bg - old_bg)

        if new_hits:
            results.append((letter, total_new, new_hits, bad_bigrams))

    # Sort by weighted total
    results.sort(key=lambda x: -x[1])

    for letter, total, hits, bad in results[:6]:
        hit_str = ', '.join(f"{w}:+{d}" for w, d in sorted(hits, key=lambda x: -x[1]*len(x[0]))[:5])
        bad_str = f" (BAD: +{bad} doubled)" if bad > 0 else ""
        print(f"  {letter}: score={total:>4}  {hit_str}{bad_str}")

print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
