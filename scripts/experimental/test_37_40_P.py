"""Test codes 37 and 40 as P (completely missing letter) and other candidates."""
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
    '47': 'D', '13': 'N', '71': 'I', '63': 'D',
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
    '79': 'O', '10': 'R',
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# Show all contexts for codes 37 and 40
for code in ['37', '40', '39', '87', '54']:
    print(f"\n{'='*70}")
    print(f"CODE {code} — ALL CONTEXTS")
    print("=" * 70)
    for idx, bpairs in enumerate(book_pairs):
        for j, p in enumerate(bpairs):
            if p != code:
                continue
            ctx_start = max(0, j - 6)
            ctx_end = min(len(bpairs), j + 7)
            parts = []
            codes = []
            for k in range(ctx_start, ctx_end):
                letter = all_codes.get(bpairs[k], f'[{bpairs[k]}]')
                if k == j:
                    parts.append(f'>{letter}<')
                    codes.append(f'>>>{bpairs[k]}<<<')
                else:
                    parts.append(letter)
                    codes.append(f'{bpairs[k]}={letter}')
            print(f"  Bk{idx:2d}: {''.join(parts):<35s} | {' '.join(codes)}")

# Test specific words with 37 and 40
print(f"\n{'='*70}")
print("TESTING 37 AND 40 AS VARIOUS LETTERS")
print("=" * 70)

base_text = ''
for bpairs in book_pairs:
    base_text += ''.join(all_codes.get(p, '?') for p in bpairs)

german_words = [
    'NICHT', 'NICHTS', 'BEISPIEL', 'PLATZ', 'PERSON',
    'OPFER', 'SPRECHEN', 'VERSPRECHEN', 'KOENIG',
    'ABER', 'ODER', 'WERDEN', 'DURCH', 'SICH',
    'PILGER', 'TEMPEL', 'KAMPF', 'KOPF',
    'PUNKT', 'SPIEL', 'SPINNE', 'SPRICHT',
    'HAUPT', 'HAUFEN', 'HAUCHER',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM',
    'HIER', 'DORT', 'WELT', 'KLAR',
    'ORT', 'ORTEN', 'WORT', 'RUNEORT',
    'INSCHRIFT', 'SCHRIFT', 'SCHREIBEN',
    'ZUSAMMEN', 'MACHEN', 'GEMACHT',
    'HIMMEL', 'STIMME', 'STIMMEN',
    'FALLEN', 'HELFEN', 'SCHNELL',
    'TEMPEL', 'EMPEL',
    'KAPITEL', 'PAPIER', 'PAAR',
    'ALPHA', 'EPSILON',
]

for code in ['37', '40']:
    print(f"\n--- Code {code} ---")
    for letter in 'PABMFWLOJ':
        test_codes = {**all_codes, code: letter}
        test_text = ''
        for bpairs in book_pairs:
            test_text += ''.join(test_codes.get(p, '?') for p in bpairs)

        hits = []
        for w in german_words:
            old = base_text.count(w)
            new = test_text.count(w)
            if new > old:
                hits.append((w, new - old))

        bad_new = 0
        for bg in ['PP', 'AA', 'BB', 'MM', 'FF', 'WW', 'LL', 'JJ', 'OO']:
            bad_new += max(0, test_text.count(bg) - base_text.count(bg))

        if hits or letter == 'P':
            hit_str = ', '.join(f"{w}:+{d}" for w, d in sorted(hits, key=lambda x: -x[1]*len(x[0]))[:5])
            bad_str = f" BAD:+{bad_new}" if bad_new > 0 else ""
            print(f"  {letter}: {hit_str}{bad_str}")

# Also check: what trigrams/quadgrams does code 37 create?
print(f"\n{'='*70}")
print("TRIGRAMS AROUND CODE 37 (E?I pattern)")
print("=" * 70)

for letter in 'PHNTSRGWBMFLK':
    trigrams = Counter()
    test_codes = {**all_codes, '37': letter}
    for bpairs in book_pairs:
        decoded = [test_codes.get(p, '?') for p in bpairs]
        for j in range(len(decoded) - 2):
            if '?' not in decoded[j:j+3]:
                trigrams[decoded[j] + decoded[j+1] + decoded[j+2]] += 1

    # Get the trigrams involving position of code 37
    relevant = Counter()
    for bpairs in book_pairs:
        for j, p in enumerate(bpairs):
            if p != '37':
                continue
            # Trigrams centered on 37
            if j > 0 and j < len(bpairs) - 1:
                left = all_codes.get(bpairs[j-1], '?')
                right = all_codes.get(bpairs[j+1], '?')
                if left != '?' and right != '?':
                    relevant[left + letter + right] += 1
            if j > 1:
                ll = all_codes.get(bpairs[j-2], '?')
                left = all_codes.get(bpairs[j-1], '?')
                if ll != '?' and left != '?':
                    relevant[ll + left + letter] += 1
            if j < len(bpairs) - 2:
                right = all_codes.get(bpairs[j+1], '?')
                rr = all_codes.get(bpairs[j+2], '?')
                if right != '?' and rr != '?':
                    relevant[letter + right + rr] += 1

    top = relevant.most_common(5)
    top_str = ', '.join(f"{k}:{v}" for k, v in top)
    print(f"  37={letter}: {top_str}")
