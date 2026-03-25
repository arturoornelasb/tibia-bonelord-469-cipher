#!/usr/bin/env python3
"""
Trace garbled blocks back to their raw digit codes.
For each recurring garbled segment, find what codes produced it
and check if a single code correction could fix it.
"""
import json, os, re
from collections import Counter, defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
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

DIGIT_SPLITS = {
    2: (45, '1'), 5: (265, '1'), 6: (12, '0'), 8: (137, '7'),
    10: (169, '0'), 11: (137, '0'), 12: (56, '1'), 13: (45, '0'),
    14: (98, '1'), 15: (98, '0'), 18: (4, '0'), 19: (52, '0'),
    20: (5, '1'), 22: (7, '1'), 23: (22, '4'), 24: (87, '8'),
    25: (0, '0'), 29: (53, '0'), 32: (137, '1'), 34: (101, '0'),
    36: (78, '0'), 39: (44, '0'), 42: (91, '2'), 43: (122, '0'),
    45: (15, '0'), 46: (0, '2'), 48: (126, '0'), 49: (97, '1'),
    50: (16, '6'), 52: (1, '0'), 53: (257, '1'), 54: (49, '1'),
    60: (73, '9'), 61: (93, '7'), 64: (60, '0'), 65: (114, '2'),
    68: (54, '0'),
}

# Build per-book pairs with their raw codes
book_data = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        split_pos, digit = DIGIT_SPLITS[bidx]
        book = book[:split_pos] + digit + book[split_pos:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    letters = [v7.get(p, '?') for p in pairs]
    text = ''.join(letters)
    book_data.append({'pairs': pairs, 'letters': letters, 'text': text})

# Target garbled patterns to trace
# These appear frequently in the decoded output between known words
targets = [
    # (pattern, description, context)
    ('T', 'single T before ER SCHARDT/etc', 'appears as {T} ER many times'),
    ('RUI', 'before IN - could be RUIN?', 'IST SCHAUN {RUI} IN'),
    ('UOD', 'after WIR - MHG word?', 'WIR {UOD} IM MIN'),
    ('HED', 'before DEM - recurring', 'MIN {HED} DEM'),
    ('RRNI', 'after AB - recurring', 'AB {RRNI} WIR'),
    ('SD', 'after AN - recurring', 'ORT AN {SD} IM MIN'),
    ('UTRUNR', 'place name 8x', 'ODE {UTRUNR} DEN ENDE'),
    ('HIHL', 'place name 7x', 'AM MIN {HIHL} DIE'),
    ('NDCE', 'after DIE 7x', 'DIE {NDCE} FACH'),
    ('HECHLLT', 'after FACH 5x', 'FACH {HECHLLT} ICH'),
    ('LGTNELGZ', 'after ER 3x', 'NOT ER {LGTNELGZ} ER'),
    ('TIURIT', 'before ORANGENSTRASSE', 'SER {TIURIT} ORANGENSTRASSE'),
    ('EO', 'GAR {EO} RUNE', 'ODE GAR {EO} RUNE ORT'),
    ('NDT', 'before ER AM NEU', 'RUNE ORT {NDT} ER AM NEU'),
    ('DE', 'AM NEU {DE} DIENST', 'NEU {DE} DIENST'),
    ('NLNDEF', 'DU {NLNDEF} SANG', 'ODE DU {NLNDEF} SANG'),
    ('CHN', 'ES IN {CHN} ES', 'ES IN {CHN} ES'),
    ('GCHD', 'ORTEN {GCHD}', 'EIGENTUM ORTEN {GCHD}'),
    ('THARSCR', 'DER {THARSCR} SCE', 'RUNEN DER {THARSCR} SCE'),
]

print("=" * 80)
print("GARBLED BLOCK TRACE: Raw codes behind recurring garbled segments")
print("=" * 80)

for target, desc, context in targets:
    print(f"\n{'─' * 60}")
    print(f"Target: {target} ({desc})")
    print(f"Context: {context}")
    print(f"{'─' * 60}")

    # Find all occurrences across all books
    occurrences = []
    for bidx, bd in enumerate(book_data):
        text = bd['text']
        start = 0
        while True:
            pos = text.find(target, start)
            if pos == -1:
                break
            # Get the raw codes for this position
            codes = bd['pairs'][pos:pos+len(target)]
            # Get surrounding context (5 chars each side)
            ctx_start = max(0, pos-8)
            ctx_end = min(len(text), pos+len(target)+8)
            ctx_text = text[ctx_start:ctx_end]
            ctx_codes = bd['pairs'][ctx_start:ctx_end]

            occurrences.append({
                'book': bidx,
                'pos': pos,
                'codes': codes,
                'context_text': ctx_text,
                'context_codes': ctx_codes,
                'target_start_in_ctx': pos - ctx_start,
            })
            start = pos + 1

    print(f"  Found {len(occurrences)} occurrences:")
    # Show up to 8 occurrences with their codes
    for occ in occurrences[:8]:
        code_str = '-'.join(occ['codes'])
        t_start = occ['target_start_in_ctx']
        t_end = t_start + len(target)
        ctx = occ['context_text']
        # Mark target in context
        marked = ctx[:t_start] + '[' + ctx[t_start:t_end] + ']' + ctx[t_end:]
        print(f"    Book {occ['book']:2d} pos {occ['pos']:3d}: codes={code_str}  ctx={marked}")

    if len(occurrences) > 8:
        print(f"    ... and {len(occurrences)-8} more")

    # Check code consistency
    if occurrences:
        code_sets = [tuple(o['codes']) for o in occurrences]
        code_counter = Counter(code_sets)
        if len(code_counter) == 1:
            print(f"  >> CONSISTENT: always codes {'-'.join(code_sets[0])}")
        else:
            print(f"  >> VARIABLE codes:")
            for codes, count in code_counter.most_common(5):
                print(f"       {count}x: {'-'.join(codes)}")

# Now check: what if {T} before ER is actually DER?
# That means the T-producing code should be D
print(f"\n{'=' * 80}")
print("HYPOTHESIS: {T} ER = 'DER' (code producing T should be D)")
print("=" * 80)

# Find all "{T} ER" patterns - the T is a single decoded letter
# followed by decoded ER
for bidx, bd in enumerate(book_data):
    text = bd['text']
    # Look for T followed by ER where T is isolated
    for pos in range(len(text)-2):
        if text[pos] == 'T' and text[pos+1:pos+3] == 'ER':
            code_t = bd['pairs'][pos]
            code_e = bd['pairs'][pos+1]
            code_r = bd['pairs'][pos+2]
            # Check if this T is in a garbled zone (not part of any known word)
            ctx_start = max(0, pos-5)
            ctx_end = min(len(text), pos+8)
            ctx = text[ctx_start:ctx_end]
            # Only care about cases where T is likely isolated
            if pos > 0 and text[pos-1] in 'ENIS':  # common word endings
                continue  # Skip - T could be part of previous word
            break  # Just check first

# Better approach: look at what specific codes produce the {T} blocks
print("\nCodes that map to T in v7:")
t_codes = [c for c, l in v7.items() if l == 'T']
print(f"  {t_codes}")
print(f"\nCodes that map to D in v7:")
d_codes = [c for c, l in v7.items() if l == 'D']
print(f"  {d_codes}")

# Check the recurring "{T} ER SCHARDT" pattern
print(f"\n{'=' * 80}")
print("Tracing '{T} ER SCHARDT' pattern back to codes")
print("=" * 80)
target_seq = 'TERSCHARDT'
# Actually search for the anagram-resolved form
# SCHARDT comes from ADTHARSC anagram. Before resolution, it's ADTHARSC
# So look for T + ER + ADTHARSC in raw decoded text

for bidx, bd in enumerate(book_data):
    text = bd['text']
    # Look for the raw pattern before anagram resolution
    idx = text.find('TERADTHARSC')
    if idx >= 0:
        codes = bd['pairs'][idx:idx+11]
        ctx_start = max(0, idx-3)
        ctx_end = min(len(text), idx+14)
        print(f"  Book {bidx}: codes for T-ER-ADTHARSC: {'-'.join(codes)}")
        print(f"    T={codes[0]}({v7.get(codes[0],'?')}), E={codes[1]}, R={codes[2]}")
        print(f"    Context codes: {'-'.join(bd['pairs'][ctx_start:ctx_end])}")

# Now the big question: is there a CONSISTENT single code that produces
# the isolated T in "T ER SCHARDT"? If so, should it be D?
print(f"\n{'=' * 80}")
print("All isolated single-letter garbled blocks and their codes")
print("=" * 80)

# Collect all single-letter garbled positions
# These are letters that appear between known words but don't attach to any word
KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR', 'ODE', 'SER', 'GEN', 'INS', 'MIN', 'OEL', 'SCE',
    'ABER', 'ALLE', 'ALLES', 'ALTE', 'ALTEN', 'ALTER', 'AUCH', 'BAND',
    'BERG', 'BURG', 'DENN', 'DIES', 'DOCH', 'DORT', 'DREI', 'DURCH',
    'EINE', 'EINEM', 'EINEN', 'EINER', 'EINES', 'ENDE', 'ERDE', 'ERST',
    'ERSTE', 'FACH', 'FAND', 'FERN', 'FEST', 'FORT', 'GAR', 'GANZ',
    'GEGEN', 'GEIST', 'GOTT', 'GOLD', 'GRAB', 'GROSS', 'GRUFT', 'GUT',
    'HAND', 'HEIM', 'HELD', 'HERR', 'HIER', 'HOCH', 'IMMER', 'KANN', 'KLAR',
    'KRAFT', 'LAND', 'LANG', 'LICHT', 'MACHT', 'MEHR', 'MUSS', 'NACH',
    'NACHT', 'NAHM', 'NAME', 'NEU', 'NEUE', 'NEUEN', 'NICHT', 'NIE', 'NOCH',
    'ODER', 'ORT', 'ORTEN', 'REDE', 'REDEN', 'REICH', 'RIEF', 'RUIN', 'RUNE',
    'RUNEN', 'SAND', 'SAGT', 'SCHAUN', 'SCHON', 'SEHR', 'SEID', 'SEIN',
    'SEINE', 'SEINEN', 'SEINER', 'SEINEM', 'SEINES',
    'SICH', 'SIND', 'SOHN', 'SOLL', 'STEH', 'STEIN', 'STEINE',
    'STEINEN', 'STERN', 'TAG', 'TAGE', 'TAGEN', 'TAT', 'TEIL',
    'TIEF', 'TOD', 'TURM', 'UNTER', 'URALTE', 'VIEL', 'VIER',
    'WAHR', 'WALD', 'WAND', 'WARD', 'WEIL', 'WELT', 'WENN', 'WERT',
    'WESEN', 'WILL', 'WIND', 'WIRD', 'WORT', 'WORTE', 'ZEIT',
    'ZEHN', 'ZORN', 'FINDEN', 'GEBEN', 'GEHEN', 'HABEN', 'KOMMEN',
    'LEBEN', 'LESEN', 'NEHMEN', 'SAGEN', 'SEHEN', 'STEHEN', 'SUCHEN',
    'WISSEN', 'WISSET', 'RUFEN', 'WIEDER', 'GEIGET', 'BERUCHTIG',
    'BERUCHTIGER', 'MEERE', 'NEIGT', 'WISTEN', 'MANIER', 'HUND',
    'GODE', 'GODES', 'EIGENTUM', 'REDER', 'THENAEUT', 'LABT', 'MORT',
    'DIGE', 'WEGE', 'KOENIGS', 'NAHE', 'NOT', 'NOTH', 'ZUR', 'OWI',
    'ENGE', 'SEIDEN', 'ALTES', 'BIS', 'NUT', 'NUTZ', 'HEIL', 'NEID',
    'TREU', 'TREUE', 'SUN', 'DIENST', 'SANG', 'DINC', 'HULDE',
    'LANT', 'HERRE', 'DIENEST', 'GEBOT', 'SCHWUR', 'ORDEN',
    'RICHTER', 'DUNKEL', 'EHRE', 'EDELE', 'SCHULD', 'SEGEN',
    'FLUCH', 'RACHE', 'KOENIG', 'DASS', 'EDEL', 'ADEL',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME', 'SCHARDT',
])

# Now check: what words would we gain by adding common short words?
print("\nTesting what happens if common garbled fragments are actually words:")
test_words = [
    'TER',   # Middle High German: of the (genitive article)
    'DER',   # the (already in KNOWN, but check context)
    'NE',    # MHG: not, no
    'SE',    # MHG: sie (she/they)
    'EN',    # suffix
    'TE',    # suffix
    'RE',    # suffix
    'UOD',   # unknown
    'HED',   # unknown
    'RUINE', # ruin (feminine)
    'RUINEN', # ruins (plural)
]

for word in test_words:
    if word not in KNOWN:
        # Count how many times it appears in the full decoded text
        full_text = ''.join(bd['text'] for bd in book_data)
        count = full_text.count(word)
        print(f"  '{word}' appears {count}x in decoded text")

# Key insight: check if 'TER' is a valid MHG word
print(f"\n{'=' * 80}")
print("DEEP ANALYSIS: What is the {T} before ER?")
print("=" * 80)
print("""
In Middle High German, 'ter' is not a standard word.
But 'der' (the/of the) is extremely common.
If the garbled {T} is actually a D, it would create 'DER SCHARDT' = 'of Schardt'.

However, in v7 mapping:
  T codes: 64, 75, 78, 81, 88, 98
  D codes: 02, 28, 42, 45, 47, 63

For the {T} to really be D, the specific code at that position would need
to be reassigned from T to D. Let's check what code it actually is.
""")

# Find the specific code producing T in "T ER ADTHARSC"
t_in_teradtharsc = []
for bidx, bd in enumerate(book_data):
    text = bd['text']
    # Search for TERADTHARSC (before anagram resolution)
    idx = text.find('TERADTHARSC')
    if idx >= 0:
        the_code = bd['pairs'][idx]
        t_in_teradtharsc.append((bidx, the_code))
        print(f"  Book {bidx}: code at T position = '{the_code}' (maps to '{v7.get(the_code, '?')}')")

if t_in_teradtharsc:
    codes_found = Counter(c for _, c in t_in_teradtharsc)
    print(f"\n  Code distribution: {dict(codes_found)}")
    main_code = codes_found.most_common(1)[0][0]
    print(f"  Main code: '{main_code}' (currently maps to '{v7[main_code]}')")
    # What are all the contexts where this code appears?
    all_ctx = []
    for bidx, bd in enumerate(book_data):
        for pos, pair in enumerate(bd['pairs']):
            if pair == main_code:
                ctx_start = max(0, pos-3)
                ctx_end = min(len(bd['text']), pos+4)
                ctx = bd['text'][ctx_start:ctx_end]
                t_pos = pos - ctx_start
                marked = ctx[:t_pos] + '[' + ctx[t_pos] + ']' + ctx[t_pos+1:]
                all_ctx.append((bidx, pos, marked))
    print(f"\n  All occurrences of code '{main_code}' ({len(all_ctx)} total):")
    for bidx, pos, ctx in all_ctx[:20]:
        print(f"    Book {bidx:2d} pos {pos:3d}: ...{ctx}...")

# Also trace: what code produces the garbled E at the start?
print(f"\n{'=' * 80}")
print("Tracing common small garbled blocks to their codes")
print("=" * 80)

small_targets = {
    'RUI': 'before IN (RUIN?)',
    'UOD': 'WIR {UOD} IM',
    'HED': 'MIN {HED} DEM',
    'SD': 'AN {SD} IM',
    'EO': 'GAR {EO} RUNE',
    'NDT': 'ORT {NDT} ER',
    'DE': 'NEU {DE} DIENST',
    'MTD': '{MTD} ENDE',
    'NK': 'WEICHSTEIN {NK}',
    'RW': 'ORANGENSTRASSE {RW}',
}

for target, desc in small_targets.items():
    print(f"\n  {target} ({desc}):")
    found = []
    for bidx, bd in enumerate(book_data):
        text = bd['text']
        start = 0
        while True:
            pos = text.find(target, start)
            if pos == -1:
                break
            codes = bd['pairs'][pos:pos+len(target)]
            ctx_start = max(0, pos-5)
            ctx_end = min(len(text), pos+len(target)+5)
            ctx = text[ctx_start:ctx_end]
            found.append((bidx, codes, ctx))
            start = pos + 1

    # Show unique code combinations
    code_combos = Counter(tuple(f['codes'] if isinstance(f, dict) else f[1]) for f in found)
    for codes, count in code_combos.most_common(5):
        if count >= 2:
            print(f"    {count}x: codes {'-'.join(codes)}")
    if not found:
        print(f"    (not found in raw text - may only appear after anagram resolution)")
