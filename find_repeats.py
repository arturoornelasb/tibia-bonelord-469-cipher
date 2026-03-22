"""Find all repeating segments in the decoded text.
This helps identify:
1. Recurring phrases (confirming the text is structured)
2. Proper nouns that appear multiple times
3. Possible sentence boundaries"""
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

# Concatenate all book texts (with separators)
all_text = []
for bpairs in book_pairs:
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    all_text.append(text)

full = '|'.join(all_text)

# Find all repeating substrings of length >= 15
print("=" * 80)
print("REPEATING SEGMENTS (length >= 15, count >= 3)")
print("=" * 80)

repeats = {}
for length in range(25, 14, -1):  # Start from longest
    for i in range(len(full) - length + 1):
        seg = full[i:i+length]
        if '|' in seg or '?' in seg:
            continue
        # Count non-overlapping occurrences
        count = 0
        pos = 0
        while True:
            pos = full.find(seg, pos)
            if pos == -1:
                break
            count += 1
            pos += length  # non-overlapping
        if count >= 3:
            # Check this isn't a substring of an already-found longer repeat
            is_sub = False
            for longer_seg in repeats:
                if seg in longer_seg and repeats[longer_seg] >= count:
                    is_sub = True
                    break
            if not is_sub:
                repeats[seg] = count

# Sort by length * count (importance)
sorted_repeats = sorted(repeats.items(), key=lambda x: -len(x[0]) * x[1])

for seg, count in sorted_repeats[:40]:
    print(f"  [{count}x] ({len(seg):2d}ch): {seg}")

# Now let's look at unique segments (the parts that DON'T repeat)
# These are likely the variable/narrative content
print(f"\n{'='*80}")
print("ANALYSIS OF REPEATING PHRASES")
print("=" * 80)

# Key repeating phrase: STUNDIESERTEINERSEINEDETOTNIURG
key_phrases = [
    'STUNDIESERTEINERSEINEDETOTNIURG',
    'WIRUNDIEMINH',
    'DIEURAL',
    'STEINEN',
    'HEARUCHTIGER',
    'KOENIGLABGZERAS',
    'AUNRSONGETRASES',
    'FINDENTEIGIDASESDERSTEIENGE',
    'THARSCISTSCHAUNRUIIIWIIS',
    'FACHHECHL',
    'LUIRUNNHWND',
]

for phrase in key_phrases:
    count = sum(1 for t in all_text if phrase in t)
    # Try manual segmentation
    print(f"\n  \"{phrase}\" ({count} books):")
    # Try splitting into German words
    words_in = []
    german = set(['ST', 'UND', 'DIES', 'DIESER', 'TEINER', 'TEIN', 'EINE', 'EINER', 'SEIN',
                  'SEINE', 'DE', 'DER', 'DIE', 'DAS', 'TEIL', 'WIR', 'ICH', 'ER', 'ES',
                  'IN', 'AN', 'UM', 'AM', 'IM', 'ORT', 'ORTE', 'IST', 'NICHT', 'RUNE',
                  'FINDEN', 'STEH', 'GUT', 'TAG', 'STEIN', 'STEINE', 'STEINEN',
                  'URALTE', 'URALTEN', 'ALTE', 'ALTEN', 'ALT',
                  'KOENIG', 'AUCH', 'NACH', 'WORT',
                  'FACH', 'HECHT', 'HECHL',
                  ])

# Manual word boundary proposals for key phrases
manual_parses = {
    'STUNDIESERTEINERSEINEDETOTNIURG':
        'ST UND DIESER T EINER SEINE DE TOTNIURG',
    'WIRUNDIEMINH':
        'WIR UND DIE MINH',
    'DIEURAL':
        'DIE URAL[TE]',
    'KOENIGLABGZERAS':
        'KOENIG LABGZERAS',
    'AUNRSONGETRASES':
        'AUNR SON GETRASES',
    'FINDENTEIGIDASESDERSTEIENGE':
        'FINDEN TEIG I DAS ES DER STEIEN GE',
    'THARSCISTSCHAUNRUIIIWIIS':
        'THARSC IST SCHAUN RU III WII S',
    'FACHHECHL':
        'FACH HECHL',
    'LUIRUNNHWND':
        'LUIRUNN HWND',
}

for phrase, parse in manual_parses.items():
    print(f"  {phrase}")
    print(f"    -> {parse}")

# ============================================================
# Try to read the LONGEST coherent segment as a story
# ============================================================
print(f"\n{'='*80}")
print("NARRATIVE READING — Longest Coherent Fragment")
print("=" * 80)

# The longest fragment from full_decode.py was 451 chars
# Let me reconstruct it properly using Bk5 (136 pairs) which contains the core narrative

bk5 = ''.join(all_codes.get(p, '?') for p in book_pairs[5])
bk10 = ''.join(all_codes.get(p, '?') for p in book_pairs[10])
bk17 = ''.join(all_codes.get(p, '?') for p in book_pairs[17])

print("Book 5 (core narrative segment):")
print(bk5)
print()

# Manual word boundary attempt
manual = """
EN HIER TAUT RI S TEIL CH AN HEARUCHTIGER
CO DASS T UND DIESER T EINER SEINE DE TOTNIURG
CE ?I LABRR NI WIR UND DIE MINH?DDE
MIDI E URALTE STEINEN TEIAD THARSC
IST SCHAUN RU III WII SET N HIER SERTIUM
"""

print("Proposed reading:")
print(manual)

# Let me try the most natural German parsing
print("\nBest-effort German translation:")
lines = [
    "EN HIER TAUTRISTEILCHAN HEARUCHTIGER",
    "  -> (EN HIER [proper noun] HEARUCHTIGER)",
    "  -> '...here [something] HEARUCHTIGER'",
    "",
    "CODASS T UND DIESER TEINER SEINE DE TOTNIURG",
    "  -> CO DASS ... UND DIESER ... EINER SEINE DE TOTNIURG",
    "  -> '...that...and this...one's his/the TOTNIURG'",
    "",
    "CE?ILABRRNI WIR UND DIE MINH?DDE",
    "  -> CE?I LABRRNI WIR UND DIE MINH?DDE",
    "  -> '[name] we and the MINH?DDE'",
    "",
    "MIDI E URALTE STEINEN",
    "  -> MIDI DIE URALTE STEINEN",
    "  -> 'with the ancient stones'",
    "",
    "TEIAD THARSC IST SCHAUN RU",
    "  -> [unknown] THARSC IST SCHAUN RU[NE]",
    "  -> '[something] is [looking/showing] rune'",
]
for line in lines:
    print(f"  {line}")

# Look at Book 10 (the longest with few unknowns)
print(f"\nBook 10 (140 pairs, few unknowns):")
print(bk10)

manual10 = """
MI SEIN ND GE DAS IE O WIR UNE AU I ENER DEN GE ENDEN
TENT TUIGAA ER GEIGE TECI ICH NES R ER SCE AUS ENDE
UTRUNR DEN ENDE RE DER KOENIG LABGZERAS UNE NIT GH
NEE AUNR SON GETRASES RW
"""
print("Proposed reading:")
print(manual10)

# ============================================================
# Check if IIIWII could be a number or code
# ============================================================
print(f"\n{'='*80}")
print("IIIWII — Could this be a cipher-within-cipher?")
print("=" * 80)

# If we assign numbers: I=1, W=5 (Roman-ish), then IIIWII = 111511 or 3+5+2=10
# Or if I=1 and W=5 in a positional system
# Or: III = 3, W = separator, II = 2 -> "3-2"?
# Or: IIIWII is a bonelord number (bonelords use 469 cipher)

# In Tibia, bonelords have a "language" using the 469 cipher
# The 469 system: 4, 6, 9 are the three symbols
# Could IIIWII map to something in the 469 system?

# Actually, let me check if the raw codes for IIIWII have any pattern:
for idx, bpairs in enumerate(book_pairs):
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    pos = text.find('IIIWII')
    if pos == -1:
        continue
    raw_codes = bpairs[pos:pos+6]
    print(f"  Bk{idx:2d}: IIIWII raw codes = {raw_codes}")
    print(f"         Numeric: {' '.join(raw_codes)} = {'-'.join(raw_codes)}")
    # Sum of code numbers?
    nums = [int(c) for c in raw_codes]
    print(f"         Sum: {sum(nums)}, codes as ints: {nums}")
    break
