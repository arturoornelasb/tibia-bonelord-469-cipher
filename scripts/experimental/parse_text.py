"""Parse decoded text into German words using greedy longest-first matching."""
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
    '79': 'O', '10': 'R',
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# German word list for parsing
german = {
    'GESCHRIEBEN', 'VERSCHIEDENE', 'RUNENSTEIN', 'INSCHRIFT',
    'GESCHAFFEN', 'VERSPRECHEN', 'VERSTEHEN',
    'GEHEIMNIS', 'BIBLIOTHEK', 'TAUSEND',
    'ZWISCHEN', 'STEINEN', 'STEINE',
    'DIESER', 'DIESES', 'DIESEM', 'DIESEN', 'DIESE',
    'EINEN', 'EINER', 'EINEM',
    'ANDEREN', 'ANDERE',
    'WERDEN', 'WURDE',
    'HABEN', 'HATTE',
    'KOENIG', 'KRIEGER',
    'FINDEN', 'KENNEN', 'SEHEN', 'WISSEN',
    'GEGEN', 'UNTER', 'DURCH', 'HINTER',
    'IMMER', 'WIEDER',
    'MACHT', 'KRAFT', 'GEIST', 'NACHT', 'LICHT',
    'ERSTE', 'ERSTEN', 'STEIN',
    'RUNEN', 'URALTE', 'URALTEN',
    'SEINE', 'SEINER', 'SEINEN', 'SEINES',
    'VIELE', 'WENIG',
    'KEINE', 'KEINEN',
    'ORTEN', 'ORTE',
    'HERREN', 'MEISTER',
    'SCHON', 'NOCH', 'AUCH', 'ABER', 'ODER', 'WENN', 'DANN', 'DENN',
    'HIER', 'DORT', 'WELT', 'TEIL', 'TEILE', 'ZEIT', 'WORT', 'NAME',
    'ALLES', 'ALLEN', 'ALLE', 'KLAR',
    'SICH', 'SIND', 'SEIN',
    'DASS', 'NICHT', 'NICHTS',
    'GANZ', 'SEHR', 'VIEL', 'FORT', 'DOCH', 'HOCH',
    'EINE', 'ERDE', 'ERDEN',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES',
    'UND', 'IST', 'EIN', 'WIR', 'ICH', 'SIE',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI',
    'NUR', 'WAS', 'MAN', 'WER', 'WIE', 'GUT',
    'TAG', 'ORT', 'TOD', 'OFT',
    'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER',
    'NACH', 'VOR',
    'GEBOREN', 'GESEHEN', 'GEFUNDEN',
    'NORDEN', 'SUEDEN', 'OSTEN', 'WESTEN',
    'BERG', 'BURG', 'GOLD', 'SOHN', 'HELD',
    'HERR', 'GOTT', 'KRIEG',
    'RUNE', 'KOMMEN', 'GEHEN',
    'GROSS', 'ALT', 'NEU',
    'ORT', 'ORTE', 'ORTEN',
    'WORT', 'WORTE', 'WORTEN',
    'RUNEORT', 'ANTWORT',
    'SOFORT', 'DORT',
}

max_word_len = max(len(w) for w in german)

# Parse each long book
print("=" * 70)
print("WORD-PARSED DECODED BOOKS")
print("=" * 70)

for idx, bpairs in enumerate(book_pairs):
    if len(bpairs) < 80:
        continue

    text = ""
    for p in bpairs:
        if p in all_codes:
            text += all_codes[p]
        else:
            text += "?"

    # Greedy longest-first word matching
    tokens = []
    i = 0
    while i < len(text):
        if text[i] == "?":
            # Collect unknown stretch
            j = i
            while j < len(text) and text[j] == "?":
                j += 1
            tokens.append("[?]" * (j - i))
            i = j
            continue

        found = False
        for wlen in range(min(max_word_len, len(text) - i), 1, -1):
            candidate = text[i:i+wlen]
            if "?" in candidate:
                break
            if candidate in german:
                tokens.append(candidate)
                i += wlen
                found = True
                break
        if not found:
            tokens.append(text[i].lower())
            i += 1

    parsed = " ".join(tokens)
    print(f"\nBook {idx} ({len(bpairs)} pairs):")
    for j in range(0, len(parsed), 110):
        print(f"  {parsed[j:j+110]}")
