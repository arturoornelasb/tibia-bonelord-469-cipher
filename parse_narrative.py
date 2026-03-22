"""Parse the full superstring as a narrative.
Try manual word segmentation on repeating segments to understand the story."""
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

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# Build the superstring by finding overlaps
# First get all decoded texts
texts = []
for bpairs in book_pairs:
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    texts.append(text)

# Find all unique segments (some books are identical substrings of others)
# Sort by length descending, keep the longest
long_texts = sorted(enumerate(texts), key=lambda x: -len(x[1]))

# ============================================================
# DETAILED CONTEXT FOR CODES 37, 40, 02
# ============================================================
print("=" * 80)
print("CODE 37 (8 occurrences) — DETAILED RAW CONTEXT")
print("=" * 80)

for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p != '37':
            continue
        start = max(0, j - 12)
        end = min(len(bpairs), j + 13)
        decoded = []
        raw = []
        for k in range(start, end):
            letter = all_codes.get(bpairs[k], f'[{bpairs[k]}]')
            if k == j:
                decoded.append(f'>>{letter}<<')
            else:
                decoded.append(letter)
            raw.append(bpairs[k])
        print(f"  Bk{idx:2d}: {''.join(decoded)}")
        print(f"         {' '.join(raw)}")

print(f"\n{'='*80}")
print("CODE 40 (7 occurrences) — DETAILED RAW CONTEXT")
print("=" * 80)

for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p != '40':
            continue
        start = max(0, j - 12)
        end = min(len(bpairs), j + 13)
        decoded = []
        raw = []
        for k in range(start, end):
            letter = all_codes.get(bpairs[k], f'[{bpairs[k]}]')
            if k == j:
                decoded.append(f'>>{letter}<<')
            else:
                decoded.append(letter)
            raw.append(bpairs[k])
        print(f"  Bk{idx:2d}: {''.join(decoded)}")
        print(f"         {' '.join(raw)}")

print(f"\n{'='*80}")
print("CODE 02 (4 occurrences) — DETAILED RAW CONTEXT")
print("=" * 80)

for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p != '02':
            continue
        start = max(0, j - 12)
        end = min(len(bpairs), j + 13)
        decoded = []
        raw = []
        for k in range(start, end):
            letter = all_codes.get(bpairs[k], f'[{bpairs[k]}]')
            if k == j:
                decoded.append(f'>>{letter}<<')
            else:
                decoded.append(letter)
            raw.append(bpairs[k])
        print(f"  Bk{idx:2d}: {''.join(decoded)}")
        print(f"         {' '.join(raw)}")

# ============================================================
# EXTENDED WORD LIST TEST for codes 37, 40, 02
# ============================================================
print(f"\n{'='*80}")
print("EXTENDED WORD TEST for 37, 40, 02")
print("=" * 80)

# Much bigger German dictionary
big_dict = set([
    'AB', 'AM', 'AN', 'DA', 'DU', 'ER', 'ES', 'IM', 'IN', 'JA', 'OB', 'SO', 'UM', 'WO', 'ZU',
    'ALS', 'AUF', 'AUS', 'BEI', 'BIS', 'DAS', 'DEN', 'DER', 'DES', 'DIE', 'EIN', 'FUR',
    'HAT', 'HIN', 'ICH', 'IHM', 'IHN', 'IST', 'MAN', 'MIT', 'NEU', 'NIE', 'NUN', 'NUR',
    'ORT', 'SIE', 'TAG', 'TOD', 'UND', 'VOM', 'VON', 'VOR', 'WAR', 'WAS', 'WER', 'WIE',
    'WIR', 'ZUM', 'ZUR',
    'ABER', 'ALLE', 'AUCH', 'DASS', 'DENN', 'DIES', 'DOCH', 'DORT', 'EINE', 'ENDE',
    'ERDE', 'ERST', 'FAND', 'GANZ', 'GING', 'GOTT', 'GANZ', 'HALB', 'HAUS', 'HERR',
    'HIER', 'HOCH', 'KAUM', 'KEIN', 'LAND', 'MEHR', 'NACH', 'NAME', 'NOCH', 'ODER',
    'OHNE', 'RUNE', 'SAGT', 'SEHR', 'SEIN', 'SICH', 'SIND', 'TEIL', 'UEBER', 'VIEL',
    'VOLK', 'WEIL', 'WELT', 'WENN', 'WORT', 'ZEIT', 'ZWEI',
    'ALLES', 'ALTEN', 'ANDER', 'BEIDE', 'BERGE', 'BRINGT', 'DIESE', 'DURCH', 'EIGEN',
    'EINEN', 'EINER', 'EINEM', 'EINES', 'ERSTE', 'ETWAS', 'FINDET', 'GEGEN', 'GEHEN',
    'GEIST', 'GROSS', 'HABEN', 'HEISST', 'IMMER', 'JEDER', 'JENEN', 'KEINE', 'KENNT',
    'KOENIG', 'KOMMT', 'KRAFT', 'LICHT', 'MACHT', 'NACHT', 'NEBEN', 'NICHT', 'OSTEN',
    'ORTE', 'ORTEN', 'RUNEN', 'SAGEN', 'SAGTE', 'SEHEN', 'SEINE', 'SETZT', 'STEHT',
    'STEIN', 'TAGEN', 'TEILE', 'UNTER', 'VIELE', 'WAGEN', 'WEDER', 'WELCH', 'WERDE',
    'WESEN', 'WIEDER', 'WISSEN', 'ZEICHEN',
    'FINDEN', 'FINDEN', 'GEBEN', 'KOENIG', 'ANDERE', 'ANFANG', 'DIESER', 'DIESES',
    'DUNKEL', 'EIGENE', 'ERSTEN', 'EWIGEN', 'GEFAHR', 'GEHEIM', 'GROSSE', 'GRUPPE',
    'HELFEN', 'HIMMEL', 'KOMMEN', 'KONNTE', 'LANGEN', 'MACHEN', 'MENSCHEN',
    'NORDEN', 'NICHTS', 'SCHAFFEN', 'SEINES', 'SEINER', 'SEINEM', 'SEINEN',
    'SPRACHE', 'STEINE', 'STEINEN', 'SUEDEN', 'TEMPEL',
    'URALTE', 'URALTEN', 'VOELKER', 'WAHRHEIT', 'WANDERN', 'WESTEN',
    'ZEITEN',
    # Game-specific
    'LABGZERAS', 'MINH', 'TOTNIURG', 'RUNEORT',
    # Verbs/forms
    'GIBT', 'GEHT', 'SAGT', 'SIEHT', 'STEHT', 'TRAEGT', 'WIRD',
    'WURDEN', 'HATTEN', 'WAREN', 'SOLLTE', 'SOLLTEN', 'WOLLTE',
    # Adjective forms
    'ALTEN', 'ALTES', 'ALTE', 'GUTEN', 'GUTES', 'GUTE',
    'GROSSEN', 'GROSSER', 'KLEINEN', 'LETZTEN',
    # Common patterns
    'TAUSEND', 'HUNDERT', 'ZUSAMMEN', 'ZWISCHEN',
    'ERSTER', 'ZWEITER', 'DRITTER',
    'PLATZ', 'PFAD', 'PFORTE', 'PRIESTER', 'PROPHET',
    'PALAST', 'PILGER',  # P words that might appear in this text
])

for code in ['37', '40', '02']:
    windows = []
    for idx, bpairs in enumerate(book_pairs):
        for j, p in enumerate(bpairs):
            if p == code:
                start = max(0, j - 8)
                end = min(len(bpairs), j + 9)
                windows.append((idx, j, bpairs[start:end], j - start))

    count = len(windows)
    print(f"\nCode {code} ({count} occ):")
    results = []
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        test = {**all_codes, code: letter}
        hits = Counter()
        for idx, j, window, rel_pos in windows:
            text = ''.join(test.get(p, '?') for p in window)
            if '?' in text:
                continue
            for wlen in range(2, min(16, len(text) + 1)):
                for ws in range(len(text) - wlen + 1):
                    cand = text[ws:ws + wlen]
                    if cand in big_dict and ws <= rel_pos < ws + wlen:
                        hits[cand] += 1
        total = sum(hits.values())
        if total > 0:
            word_str = ', '.join(f"{w}:{c}" for w, c in hits.most_common(8))
            results.append((letter, total, word_str))

    results.sort(key=lambda x: -x[1])
    for letter, total, word_str in results[:10]:
        print(f"  {code}={letter}: hits={total:2d}  {word_str}")

# ============================================================
# MANUAL NARRATIVE PARSE of the longest book (Bk9, 147 pairs)
# ============================================================
print(f"\n{'='*80}")
print("NARRATIVE PARSE — Book 9 (longest)")
print("=" * 80)

bk9 = book_pairs[9]
text9 = ''.join(all_codes.get(p, '?') for p in bk9)
print(f"Full: {text9}")
print(f"Len:  {len(text9)}")

# Known word positions in the text
# Try to manually identify word boundaries
segments = [
    # Attempt to parse the text
    "N HIER TAUT RI STEILCHAN HEARUCHTIGER CODAS ST UND IESER TEINER SEINE DE TOTNIURG",
    "CE?ILABRR NI WIR UND DIE MINH?DDE MIDI E URALTE STEINEN",
    "TEIAD THARSC IST SCHAUN RU IIIWII SET EIS",
]

# Let me try a greedy forward parse
print(f"\nGreedy parse attempt:")
i = 0
words_found = []
word_list = sorted(big_dict, key=lambda w: -len(w))  # longest first
while i < len(text9):
    found = False
    for w in word_list:
        if text9[i:i+len(w)] == w:
            words_found.append((i, w))
            found = True
            i += len(w)
            break
    if not found:
        i += 1

print(f"Words found: {len(words_found)}")
for pos, w in words_found:
    print(f"  pos {pos:3d}: {w}")

# ============================================================
# SUPERSTRING RECONSTRUCTION (simplified)
# ============================================================
print(f"\n{'='*80}")
print("SUPERSTRING — full decoded text from longest books, non-overlapping")
print("=" * 80)

# Find the longest contiguous text by chaining books
# Use Bk10 (140p) as it's the longest with few unknowns
for bk_idx in [10, 17, 35, 31]:
    btext = ''.join(all_codes.get(p, '?') for p in book_pairs[bk_idx])
    print(f"\nBk{bk_idx} ({len(book_pairs[bk_idx])}p):")
    # Print in chunks of 60 chars
    for i in range(0, len(btext), 60):
        chunk = btext[i:i+60]
        print(f"  {i:4d}: {chunk}")
