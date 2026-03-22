"""Decode all superstring fragments and produce the full narrative text."""
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
    '98': 'T', '39': 'E', '87': 'W',
}

# Build superstring from raw digits using overlaps
book_texts = []
for book in books:
    off = get_offset(book)
    book_texts.append(book[off:])

# Greedy assembly: find overlaps between raw digit strings
fragments = list(range(len(book_texts)))
texts = [book_texts[i] for i in range(len(book_texts))]

# Keep merging until no more overlaps
while True:
    best_ov = 0
    best_i = -1
    best_j = -1
    for i in range(len(texts)):
        for j in range(len(texts)):
            if i == j:
                continue
            # Check if end of texts[i] overlaps start of texts[j]
            ti = texts[i]
            tj = texts[j]
            max_ov = min(len(ti), len(tj))
            for ov in range(max_ov, 7, -1):  # min overlap 8 digits = 4 pairs
                if ti[-ov:] == tj[:ov]:
                    if ov > best_ov:
                        best_ov = ov
                        best_i = i
                        best_j = j
                    break
    if best_ov <= 7:
        break
    # Merge best_i and best_j
    merged = texts[best_i] + texts[best_j][best_ov:]
    # Replace best_i with merged, remove best_j
    texts[best_i] = merged
    texts.pop(best_j)

# Decode each fragment
print("=" * 80)
print(f"FULL DECODED TEXT — {len(texts)} fragment(s)")
print("=" * 80)

for frag_idx, raw in enumerate(sorted(texts, key=lambda x: -len(x))):
    # Decode: take pairs
    pairs = [raw[j:j+2] for j in range(0, len(raw)-1, 2)]
    decoded = ''.join(all_codes.get(p, '?') for p in pairs)

    if len(decoded) < 20:
        continue

    print(f"\n--- Fragment {frag_idx+1} ({len(decoded)} chars) ---")
    for i in range(0, len(decoded), 80):
        print(f"  {i:4d}: {decoded[i:i+80]}")

    # DP word segmentation on this fragment
    word_dict = set([
        'AB', 'AM', 'AN', 'DA', 'DU', 'ER', 'ES', 'IM', 'IN', 'JA', 'OB', 'SO',
        'UM', 'WO', 'ZU',
        'ALS', 'AUF', 'AUS', 'BEI', 'BIS', 'DAS', 'DEM', 'DEN', 'DER', 'DES',
        'DIE', 'EIN', 'FUR', 'GAB', 'GUT', 'HAT', 'HIN', 'ICH', 'IHM', 'IHN',
        'IST', 'KAM', 'MAN', 'MIT', 'NEU', 'NIE', 'NUN', 'NUR', 'ORT', 'SIE',
        'TAG', 'TOD', 'UND', 'VOM', 'VON', 'VOR', 'WAR', 'WAS', 'WER', 'WIE',
        'WIR', 'ZUM', 'ZUR',
        'ABER', 'ALLE', 'AUCH', 'DANN', 'DASS', 'DEIN', 'DENN', 'DIES', 'DOCH',
        'DORT', 'DREI', 'EINE', 'ENDE', 'ERDE', 'ERST', 'FAND', 'GANZ', 'GING',
        'GOLD', 'GOTT', 'HERR', 'HIER', 'KEIN', 'LAND', 'MEHR', 'NACH', 'NAME',
        'NOCH', 'ODER', 'OHNE', 'ORTE', 'RUNE', 'SAGT', 'SEHR', 'SEIN', 'SICH',
        'SIND', 'TEIL', 'VIEL', 'VOLK', 'WEIL', 'WELT', 'WENN', 'WORT', 'ZEIT',
        'ALLES', 'ALTEN', 'BEIDE', 'DIESE', 'DURCH', 'EINEN', 'EINER', 'EINEM',
        'EINES', 'ERSTE', 'ETWAS', 'GEGEN', 'GEHEN', 'GEIST', 'GROSS', 'HABEN',
        'JEDER', 'KEINE', 'KRAFT', 'LICHT', 'MACHT', 'NACHT', 'NEBEN', 'NICHT',
        'ORTEN', 'RUNEN', 'SAGEN', 'SAGTE', 'SEHEN', 'SEINE', 'STEIN', 'TAGEN',
        'TEILE', 'UNTER', 'VIELE', 'WERDE', 'WESEN', 'IMMER', 'WIEDER',
        'ANDERE', 'DIESER', 'DIESES', 'DIESEM', 'DIESEN', 'DUNKEL', 'EIGENE',
        'ERSTEN', 'FINDEN', 'GROSSE', 'KOENIG', 'KOMMEN', 'KONNTE', 'NICHTS',
        'NORDEN', 'SEINES', 'SEINER', 'SEINEM', 'SEINEN', 'STEINE', 'TEMPEL',
        'URALTE', 'WISSEN',
        'ANDEREN', 'STEINEN', 'URALTEN', 'STIMMEN',
        'LABGZERAS', 'TOTNIURG', 'RUNEORT', 'HEARUCHTIGER',
    ])

    n = len(decoded)
    dp = [(0, -1, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], i-1, None)
        for wlen in range(2, min(20, i + 1)):
            start = i - wlen
            candidate = decoded[start:i]
            if '?' not in candidate and candidate in word_dict:
                new_covered = dp[start][0] + wlen
                if new_covered > dp[i][0]:
                    dp[i] = (new_covered, start, candidate)

    # Traceback
    words_found = []
    pos = n
    while pos > 0:
        _, prev, word = dp[pos]
        if word:
            words_found.append((prev, word))
            pos = prev
        else:
            pos = prev
    words_found.reverse()

    total_covered = dp[n][0]
    print(f"  Word coverage: {total_covered}/{n} = {total_covered/n*100:.1f}%")

    # Show segmented text
    covered = [False] * n
    for start, word in words_found:
        for j in range(start, start + len(word)):
            covered[j] = True

    result = []
    i = 0
    while i < n:
        if covered[i]:
            for start, word in words_found:
                if start == i:
                    result.append(f' {word} ')
                    i += len(word)
                    break
            else:
                result.append(decoded[i])
                i += 1
        else:
            result.append(decoded[i].lower())
            i += 1

    annotated = ''.join(result)
    # Clean up double spaces
    while '  ' in annotated:
        annotated = annotated.replace('  ', ' ')

    print(f"  Segmented:")
    for i in range(0, len(annotated), 100):
        print(f"    {annotated[i:i+100]}")
