"""
Test if any of the 8 I-codes might actually be a different letter.
The I frequency is 11.1% vs expected 7.5% — 204 excess I's.
If one high-frequency I-code is misassigned, fixing it could unlock new words.
"""
import json
import os
from collections import Counter

data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

# Full mapping
base_mapping = {
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
    '09': 'E', '05': 'S', '53': 'N', '44': 'U', '62': 'B',
    '68': 'R', '23': 'S', '17': 'E', '29': 'E', '66': 'A',
    '49': 'E', '38': 'K', '77': 'Z', '22': 'K', '82': 'O',
    '73': 'N', '50': 'I', '84': 'G', '25': 'O', '83': 'V',
    '81': 'T', '24': 'I', '79': 'O', '10': 'R', '54': 'M',
    '98': 'T', '39': 'E', '87': 'W',
    '74': 'E', '37': 'E', '40': 'M', '02': 'D', '69': 'E',
}

WORDS = set("""
ab aber alle allem allen aller alles als also alt alte altem alten alter altes am an andere
ans auch auf aus bei beim bis da dabei damit dann das dass dem den denen denn
der deren des die dies diese diesem diesen dieser dir doch dort durch
ein eine einem einen einer einige em en ende er erde erst erste es
fach fand fest finden ganz gar geh geheim gegen geben gibt ging
hab haben hat her herr hier hin ich ihm ihn ihr ihre ihrem ihren im in ins ist
ja jede jeden klar koenig koenige kommen kam
nach nacht nah neu neue neuen nicht noch nun nur ob oder ohne ort orte orten
rede reden ruin rune runen runeort see sehr sei seid sein seine seinem seinen seiner
sie sind so soll steil stein steine steinen teil teile teilen tod tot tun
ueber um und uns unter uralte uralten viel vom von vor wahr war was weg weil
wir wird wo wohl wort zeichen zeit zu zum zur zwei
schwiteio tharsc totniurg hearuchtiger aunrsongetrases labgzeras labge
finden dass dieser dieses nach aus tun ab des geh erde enden nu
min gem steil koenigs tag tage nacht orte erste schau
fach rede teil ab des geh erde enden drei vier land lande
""".split())

i_codes = [('21', 165), ('46', 158), ('15', 77), ('65', 71),
           ('24', 47), ('16', 38), ('50', 35), ('71', 33)]

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

def decode_book(book, m):
    offset = get_offset(book)
    pairs = [book[j:j+2] for j in range(offset, len(book)-1, 2)]
    return ''.join(m.get(p, '?') for p in pairs)

def measure_coverage(text):
    covered = 0
    text_lower = text.lower()
    used = [False] * len(text_lower)
    for length in range(max(len(w) for w in WORDS), 1, -1):
        for word in WORDS:
            if len(word) != length:
                continue
            pos = 0
            while True:
                p = text_lower.find(word, pos)
                if p == -1:
                    break
                # Check not already used
                if not any(used[p:p+len(word)]):
                    for k in range(p, p+len(word)):
                        used[k] = True
                    covered += len(word)
                pos = p + 1
    return covered

# Baseline coverage
base_total = 0
for book in books:
    dec = decode_book(book, base_mapping)
    base_total += measure_coverage(dec)
print(f"Baseline coverage (all I): {base_total} chars")

# Test reassigning each I-code to every other common letter
candidates = 'IENSRADTHUGOMWCLFBZV'

print(f"\n{'='*80}")
print("TESTING I-CODE REASSIGNMENTS")
print(f"{'='*80}")

for code, freq in i_codes:
    print(f"\n--- Code {code} (I, {freq}x) ---")

    # Get contexts for this code
    contexts = []
    for book in books:
        dec_pairs = []
        offset = get_offset(book)
        pairs = [book[j:j+2] for j in range(offset, len(book)-1, 2)]
        for k, p in enumerate(pairs):
            if p == code:
                before = ''.join(base_mapping.get(pairs[j], '?') for j in range(max(0,k-3), k))
                after = ''.join(base_mapping.get(pairs[j], '?') for j in range(k+1, min(len(pairs), k+4)))
                contexts.append(f"{before}__{after}")

    # Show unique contexts (up to 5)
    unique_ctx = list(set(contexts))[:5]
    for ctx in unique_ctx:
        print(f"  Context: ...{ctx}...")

    # Test each letter
    results = []
    for letter in candidates:
        test_mapping = dict(base_mapping)
        test_mapping[code] = letter
        total = 0
        for book in books:
            dec = decode_book(book, test_mapping)
            total += measure_coverage(dec)
        diff = total - base_total
        results.append((letter, total, diff))

    results.sort(key=lambda x: -x[1])
    print(f"  Top 5 assignments:")
    for letter, total, diff in results[:5]:
        marker = " <-- BETTER!" if diff > 5 else ""
        print(f"    {code}={letter}: {total} chars (diff: {diff:+d}){marker}")

    # Also show I assignment for comparison
    i_result = next(r for r in results if r[0] == 'I')
    print(f"    {code}=I: {i_result[1]} chars (current)")
