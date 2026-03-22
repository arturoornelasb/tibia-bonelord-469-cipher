"""Test 79=O and 10=R assignments together — do they reinforce each other?"""
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

# Show all contexts where code 79 appears
print("=" * 70)
print("ALL CODE 79 CONTEXTS (currently H, testing O)")
print("=" * 70)

for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p != '79':
            continue
        ctx_start = max(0, j - 4)
        ctx_end = min(len(bpairs), j + 5)

        # Decode with 79=H (current)
        parts_h = []
        for k in range(ctx_start, ctx_end):
            if k == j:
                parts_h.append('[H]')
            else:
                parts_h.append(all_codes.get(bpairs[k], f'[{bpairs[k]}]'))

        # Decode with 79=O (test)
        parts_o = []
        for k in range(ctx_start, ctx_end):
            if k == j:
                parts_o.append('[O]')
            else:
                parts_o.append(all_codes.get(bpairs[k], f'[{bpairs[k]}]'))

        codes_str = ' '.join(bpairs[ctx_start:ctx_end])
        print(f"  Bk{idx:2d} pos{j:3d}: H={''.join(parts_h):<25s} O={''.join(parts_o):<25s} | {codes_str}")

# Now test combined: 79=O + 10=R
print(f"\n{'='*70}")
print("COMBINED TEST: 79=O + 10=R")
print("=" * 70)

german_words = [
    'RUNENSTEIN', 'INSCHRIFT', 'VERSCHIEDENE', 'GESCHRIEBEN',
    'VERSTEHEN', 'GEHEIMNIS', 'BIBLIOTHEK', 'ZWISCHEN',
    'STEINEN', 'STEINE', 'STEIN', 'RUNEN', 'RUNE',
    'DIESER', 'DIESES', 'DIESEM', 'DIESEN', 'DIESE',
    'NICHT', 'NICHTS', 'EINEN', 'EINER', 'EINE', 'EINEM',
    'ANDEREN', 'ANDERE', 'WERDEN', 'WURDE', 'WORDEN',
    'HABEN', 'HATTE', 'DURCH', 'GEGEN', 'UNTER', 'HINTER',
    'IMMER', 'WIEDER', 'SCHON', 'NOCH', 'MACHT', 'KRAFT',
    'GEIST', 'LICHT', 'NACHT', 'WISSEN', 'KENNEN', 'SEHEN',
    'FINDEN', 'AUCH', 'ABER', 'ODER', 'WENN', 'DANN', 'DENN',
    'SICH', 'SIND', 'SEIN', 'SEINE', 'DASS', 'HIER', 'DORT',
    'WELT', 'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES',
    'UND', 'IST', 'EIN', 'WIR', 'ICH', 'SIE',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI',
    'NUR', 'WAS', 'MAN', 'WER', 'WIE', 'GUT',
    'TAG', 'TEIL', 'ZEIT', 'WORT', 'NAME', 'DOCH', 'HOCH',
    'FORT', 'VOLK', 'GOLD', 'SOHN', 'ERSTE', 'ERSTEN',
    'ERDE', 'ERDEN', 'TAUSEND', 'ALLES', 'ALLEN', 'KLAR', 'ZU',
    'KOENIG', 'ORT', 'ORTE', 'ORTEN', 'VIEL',
    'GEBOREN', 'GESCHAFFEN', 'VERSPRECHEN',
    'KOMMEN', 'GEHEN', 'KRIEGER', 'KRIEG',
    'HERR', 'HERREN', 'MEISTER', 'NORDEN', 'SUEDEN',
    'BERG', 'BURG', 'TOD', 'HELD', 'GOTT',
    'KEINE', 'KEINEN', 'STIMME', 'BRUDER', 'BLUT',
    'MORGEN', 'ABEND', 'GROSS', 'ALT', 'NEU',
    'OBEN', 'NEBEN', 'UEBER', 'OPFER',
    'BEREITS', 'BEIDE', 'ZUSAMMEN',
    'WORT', 'WORTE', 'WORTEN',
    'DORT', 'DORTEN',
    'NORDEN', 'SUEDEN', 'OSTEN', 'WESTEN',
    'ANTWORT',
    'SOFORT',
]

configs = {
    'baseline': dict(all_codes),
    '79=O only': {**all_codes, '79': 'O'},
    '10=R only': {**all_codes, '10': 'R'},
    '79=O + 10=R': {**all_codes, '79': 'O', '10': 'R'},
}

for name, codes in configs.items():
    text = ''
    for bpairs in book_pairs:
        text += ''.join(codes.get(p, '?') for p in bpairs)

    hits = {}
    for w in sorted(set(german_words), key=lambda w: -len(w)):
        ct = text.count(w)
        if ct > 0:
            hits[w] = ct

    # Bad bigrams
    bad = sum(text.count(bg) for bg in ['II', 'HH', 'DD'])

    # New words compared to baseline
    if name == 'baseline':
        base_hits = hits.copy()
        base_bad = bad
        print(f"\n{name}: bad_bigrams={bad}")
    else:
        new = {w: hits.get(w, 0) - base_hits.get(w, 0) for w in set(list(hits.keys()) + list(base_hits.keys()))}
        gains = {w: d for w, d in new.items() if d > 0}
        losses = {w: -d for w, d in new.items() if d < 0}
        gain_str = ', '.join(f"{w}:+{d}" for w, d in sorted(gains.items(), key=lambda x: -x[1]*len(x[0]))[:8])
        loss_str = ', '.join(f"{w}:-{d}" for w, d in sorted(losses.items(), key=lambda x: -x[1]*len(x[0]))[:5])
        print(f"\n{name}: bad_bigrams={bad} (delta={bad-base_bad:+d})")
        print(f"  Gains: {gain_str}")
        print(f"  Losses: {loss_str}")

# Frequency impact
print(f"\n{'='*70}")
print("FREQUENCY IMPACT OF 79=O + 10=R")
print("=" * 70)

pair_counts = Counter()
for bpairs in book_pairs:
    pair_counts.update(bpairs)
total = sum(pair_counts.values())

test_codes = {**all_codes, '79': 'O', '10': 'R'}

german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007,
}

letter_freq = Counter()
for c, l in test_codes.items():
    letter_freq[l] += pair_counts.get(c, 0)

print(f"\nH and O changes with 79=O, 10=R:")
for l in ['H', 'O', 'R']:
    old_count = sum(pair_counts.get(c, 0) for c in all_codes if all_codes[c] == l)
    new_count = letter_freq[l]
    old_pct = old_count / total * 100
    new_pct = new_count / total * 100
    exp_pct = german_freq[l] * 100
    print(f"  {l}: {old_pct:.1f}% -> {new_pct:.1f}% (expected {exp_pct:.1f}%)")
