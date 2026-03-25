#!/usr/bin/env python3
"""
Session 23: Systematic attack on remaining large garbled blocks.

Targets (by total char impact):
1. WRLGTNELNR (10x6=60) and UIRUNNHWND (10x6=60) - flanking HEL
2. UTRUNR (6x7=42) - "ODE UTRUNR DEN ENDE REDER KOENIG"
3. HIHL (4x9=36) + NDCE (4x7=28) + HECHLLT (7x5=35) - cluster unit
4. NLNDEF (6x5=30) - "DU NLNDEF SAGEN"
5. IGAA (4x5=20) - after TUT
6. RRNI (4x5=20) - after AB
7. UOD (3x7=21) - "WIR UOD IM MIN"

Strategy:
- Exhaustive German/MHG dictionary anagram matching (with +1 tolerance)
- Cross-boundary analysis (block + adjacent known word)
- Raw code fingerprinting across occurrences
"""

import json, os, itertools
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

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

ANAGRAM_MAP = {
    'LABGZERAS': 'SALZBERG', 'SCHWITEIONE': 'WEICHSTEIN',
    'SCHWITEIO': 'WEICHSTEIN', 'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'EDETOTNIURG': 'GOTTDIENER', 'EDETOTNIURGS': 'GOTTDIENERS',
    'ADTHARSC': 'SCHARDT', 'TAUTR': 'TRAUT', 'EILCH': 'LEICH',
    'HEDDEMI': 'HEIME', 'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG', 'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE', 'TEIGN': 'NEIGT', 'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER', 'SODGE': 'GODES', 'SNDTEII': 'DIENST',
    'IEB': 'BEI', 'TNEDAS': 'STANDE', 'NSCHAT': 'NACHTS',
    'SANGE': 'SAGEN', 'GHNEE': 'GEHEN', 'THARSCR': 'SCHRAT',
    'ANSD': 'SAND', 'TTU': 'TUT', 'TERLAU': 'URALTE',
    'EUN': 'NEU', 'NIUR': 'RUIN', 'RUIIN': 'RUIN',
    'CHIS': 'SICH',
}

MHG_KNOWN = {
    'HEL', 'RIT', 'EWE', 'SIN', 'MIS', 'AUE', 'EIS', 'ERE', 'TER',
    'NIT', 'SCE', 'OEL', 'ODE', 'UND', 'DER', 'DIE', 'DAS', 'IST',
    'WIR', 'ICH', 'DEN', 'ALS', 'AUS', 'AM', 'AN', 'SO', 'ER', 'ES',
    'IN', 'IM', 'DA', 'ZU', 'NU', 'AB', 'WO',
}

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    return 0 if ic_from_counts(Counter(bp0), len(bp0)) > ic_from_counts(Counter(bp1), len(bp1)) else 1

book_pairs = []
decoded_books = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)
    decoded_books.append(''.join(v7.get(p, '?') for p in pairs))

raw = ''.join(decoded_books)
processed = raw
for old in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    processed = processed.replace(old, ANAGRAM_MAP[old])

# Add MHG known words to processed
for w in sorted(MHG_KNOWN, key=len, reverse=True):
    pass  # already in word list used by DP

# ================================================================
# German/MHG word dictionary for anagram lookup
# ================================================================

GERMAN_WORDS = [
    # Common German words
    'GOTT', 'RUNE', 'RUNEN', 'STEIN', 'STEINEN', 'ALT', 'ALTE', 'ALTEN',
    'URALTE', 'BURG', 'BERG', 'STRASSE', 'HAUS', 'WALD', 'LAND', 'ERDE',
    'HIMMEL', 'TEUFEL', 'KONIG', 'KOENIG', 'RITTER', 'SCHRAT', 'SCHATZ',
    'GRUND', 'GRUNDE', 'RUHE', 'RUHEN', 'STEHEN', 'STEH', 'GEHEN', 'GEH',
    'FINDEN', 'WARTEN', 'STUNDE', 'NACHT', 'NACHTS', 'DUNKEL', 'DUNKEL',
    'RECHT', 'MACHT', 'KRAFT', 'GEIST', 'WELT', 'SEELE', 'LEBEN',
    'STERBEN', 'TOT', 'LEICH', 'LEICHE', 'LEICHEN', 'BLUT', 'FEUER',
    'WASSER', 'WIND', 'STEIN', 'GOLD', 'SILBER', 'EISEN', 'HOLZ',
    # MHG words
    'HEL', 'HEL', 'HELHEIM', 'NIFL', 'NIFLHEIM',
    'RIT', 'RITE', 'RITTER',
    'EWE', 'EWIG', 'EWIGE',
    'SIN', 'SINT', 'SINDE',
    'MIS', 'MIST', 'MIT',
    'AUE', 'AUEN',
    'EIS', 'EISE',
    'NIT', 'NIHT', 'NICHT',
    'WALT', 'WALTE', 'GEWALT',
    'HEIL', 'HEILE', 'HEILIG',
    'WIRT', 'WIRTE',
    'BURG', 'BURGE',
    'HEIM', 'HEIME',
    'TURM', 'TURNE',
    'HUND', 'HUNDE',
    'WUND', 'WUNDE',
    'RUND', 'RUNDE',
    'BUND', 'BUNDE',
    'FUND', 'FUNDE',
    'GRUND', 'GRUNDE',
    'MUND', 'MUNDE',
    'WUNDR', 'WUNDER',
    'HUNNE', 'HUNNEN',
    'RUINE', 'RUINEN',
    'TURNIER', 'TURNIR',
    'UNWIRT', 'UNWIRTE',
    'RUNDUM', 'RINGUM',
    # Place name elements
    'BURG', 'BERG', 'DORF', 'FELD', 'FORST', 'GARTEN',
    'HAIN', 'HALDE', 'HANG', 'HORN', 'HUEGEL',
    'INSEL', 'KLIPPE', 'MOOR', 'MURE',
    'PASS', 'PFAD', 'RAIN', 'RAND',
    'SCHLUCHT', 'SENKE', 'SUMPF',
    'TAL', 'TEICH', 'TRIFT',
    'UFER', 'WALD', 'WASSER', 'WIESE',
    # Mythological
    'DRACHE', 'DRACHEN', 'RIESE', 'RIESEN',
    'TROLL', 'TROLLE', 'ZWERG', 'ZWERGE',
    'HEXE', 'HEXEN', 'GEIST', 'GEISTER',
    'DAEMON', 'TEUFEL', 'ENGEL',
    # Additional MHG/OHG
    'NAHT', 'NAHTE', 'NAHTEN',
    'WUNN', 'WUNNE', 'WUNNEN',
    'LICHT', 'LICHTE',
    'DICHT', 'NICHT', 'ICHT',
    'GLUECK', 'GLUECKE',
    'FLUCHT', 'FLUECHTE',
    'SCHLACHT', 'SCHLACHTEN',
    'KNECHT', 'KNECHTE',
    'RECHT', 'RECHTE',
    'NACHT', 'NACHTE',
    'WACHT', 'WACHTE',
    'RACHT', 'RACHEN',
    'DACHT', 'GEDACHT',
    'TACHT', 'BETRACHT',
    'RUNNE', 'RINNEN',
    'BRUNE', 'BRUNNEN',
    'DUNNE', 'DUNNER',
    'TUNNE', 'TUNNEL',
    'WUNNE', 'WONNE',
    'ZINNE', 'ZINNEN',
    'RINNE', 'RINNEN',
    'INNE', 'INNEN',
    'SUNNE', 'SONNE',
    'HUNNE', 'HUNNEN',
    'GUNNE', 'GONNEN',
    'MUNNE', 'MUNNEN',
    'WINNE', 'WANNEN',
    'INNE', 'HINNEN',
    'DINNE', 'DUNNER',
    'LINNE', 'LINNEN',
    'MINNE', 'MINNER',
    'NINNE', 'NENNEN',
    'RINNE', 'RINNEN',
    # Additional attack targets
    'WIRT', 'WIRTIN', 'UNRUH', 'UNRUHE',
    'TURNIR', 'TURNIER',
    'HINTRUM', 'HINDURCH',
    'WINTERUNG', 'WANDERUNG',
    'WINDHUND', 'WINDHUNDE',
    'WUNDHORN', 'WUNDERHORN',
]
GERMAN_WORDS = sorted(set(GERMAN_WORDS), key=len, reverse=True)

def anagram_match(block, word, plus=1):
    """Check if block is an anagram of word (within +plus extra chars)."""
    bc = Counter(block)
    wc = Counter(word)
    # word letters must all be present in block
    for ch, cnt in wc.items():
        if bc.get(ch, 0) < cnt:
            return False
    extra = sum(bc.values()) - sum(wc.values())
    return 0 <= extra <= plus

def find_german_matches(block, words, plus=1):
    results = []
    bs = sorted(block)
    for w in words:
        if abs(len(w) - len(block)) > plus:
            continue
        if anagram_match(block, w, plus):
            results.append(w)
    return results

# ================================================================
# 1. WRLGTNELNR analysis (10 chars, 6x)
# ================================================================
print("=" * 70)
print("1. WRLGTNELNR (10 chars, 6x) - LEFT side of big block")
print("   Context: STEH {WRLGTNELNR} HEL {UIRUNNHWND} FINDEN")
print("=" * 70)
block1 = 'WRLGTNELNR'
print(f"  Sorted: {''.join(sorted(block1))}")
matches = find_german_matches(block1, GERMAN_WORDS, plus=2)
print(f"  German word matches (+2): {matches}")

# Check cross-boundary with STEH
combined_steh = 'STEH' + block1
print(f"\n  Cross-boundary STEH+block: {combined_steh}")
print(f"  Sorted: {''.join(sorted(combined_steh))}")
matches_cb = find_german_matches(combined_steh, GERMAN_WORDS, plus=2)
print(f"  German matches: {matches_cb}")

# Split analysis
print(f"\n  Split possibilities:")
for i in range(2, len(block1)-1):
    left = block1[:i]
    right = block1[i:]
    lm = find_german_matches(left, GERMAN_WORDS, plus=1)
    rm = find_german_matches(right, GERMAN_WORDS, plus=1)
    if lm or rm:
        print(f"    {left}|{right}: left={lm}, right={rm}")

# ================================================================
# 2. UIRUNNHWND analysis (10 chars, 6x)
# ================================================================
print("\n" + "=" * 70)
print("2. UIRUNNHWND (10 chars, 6x) - RIGHT side of big block")
print("   Context: HEL {UIRUNNHWND} FINDEN NEIGT DAS ES")
print("=" * 70)
block2 = 'UIRUNNHWND'
print(f"  Sorted: {''.join(sorted(block2))}")
matches = find_german_matches(block2, GERMAN_WORDS, plus=2)
print(f"  German word matches (+2): {matches}")

# Cross-boundary with FINDEN
combined_finden = block2 + 'FINDEN'
print(f"\n  Cross-boundary block+FINDEN: {combined_finden}")
print(f"  Sorted: {''.join(sorted(combined_finden))}")
matches_cb = find_german_matches(combined_finden, GERMAN_WORDS, plus=2)
print(f"  German matches: {matches_cb}")

# Split analysis
print(f"\n  Split possibilities:")
for i in range(2, len(block2)-1):
    left = block2[:i]
    right = block2[i:]
    lm = find_german_matches(left, GERMAN_WORDS, plus=1)
    rm = find_german_matches(right, GERMAN_WORDS, plus=1)
    if lm or rm:
        print(f"    {left}|{right}: left={lm}, right={rm}")

# ================================================================
# 3. UTRUNR analysis (6 chars, 7x)
# ================================================================
print("\n" + "=" * 70)
print("3. UTRUNR (6 chars, 7x)")
print("   Context: ODE {UTRUNR} DEN ENDE REDER KOENIG SALZBERG")
print("=" * 70)
block3 = 'UTRUNR'
print(f"  Sorted: {''.join(sorted(block3))}")
matches = find_german_matches(block3, GERMAN_WORDS, plus=2)
print(f"  German word matches (+2): {matches}")

# Try all splits
print(f"\n  Split possibilities:")
for i in range(2, len(block3)-1):
    left = block3[:i]
    right = block3[i:]
    lm = find_german_matches(left, GERMAN_WORDS, plus=1)
    rm = find_german_matches(right, GERMAN_WORDS, plus=1)
    if lm or rm:
        print(f"    {left}|{right}: left={lm}, right={rm}")

# Cross-boundary ODE + UTRUNR
combined_ode = 'ODE' + block3
print(f"\n  ODE+UTRUNR: {combined_ode}")
print(f"  Sorted: {''.join(sorted(combined_ode))}")
matches_cb = find_german_matches(combined_ode, GERMAN_WORDS, plus=2)
print(f"  German matches: {matches_cb}")

# Cross-boundary UTRUNR + DEN
combined_den = block3 + 'DEN'
print(f"\n  UTRUNR+DEN: {combined_den}")
print(f"  Sorted: {''.join(sorted(combined_den))}")
matches_cb = find_german_matches(combined_den, GERMAN_WORDS, plus=2)
print(f"  German matches: {matches_cb}")

# Raw codes for UTRUNR
print(f"\n  Raw code analysis for UTRUNR:")
print(f"  Codes: 44=U, 64=T, 72=R, 61=U, 14=N, 51=R")
print(f"  Fixed sequence, always identical -> proper noun likely")
print(f"  Anagram with TURM (tower): UTRUNR vs TURM (need 4 chars, block has 6)")
print(f"  Possible: TURM + UR = TURMUR? UNTURR? TURNU+R?")
# Check TURM derivatives
print(f"  TURMUR: {''.join(sorted('TURMUR'))} vs UTRUNR: {''.join(sorted('UTRUNR'))}")

# ================================================================
# 4. HIHL, NDCE, HECHLLT cluster
# ================================================================
print("\n" + "=" * 70)
print("4. HIHL (4 chars, 9x) + NDCE (4 chars, 7x) + HECHLLT (7 chars, 5x)")
print("   Context: SAGEN AM MIN {HIHL} DIE {NDCE} FACH {HECHLLT} ICH OEL")
print("=" * 70)

for block, freq in [('HIHL', 9), ('NDCE', 7), ('HECHLLT', 5)]:
    print(f"\n  Block: {block} ({freq}x)")
    print(f"  Sorted: {''.join(sorted(block))}")
    matches = find_german_matches(block, GERMAN_WORDS, plus=2)
    print(f"  German matches (+2): {matches}")

# Combined cluster analysis
cluster = 'HIHL' + 'DIE' + 'NDCE' + 'FACH' + 'HECHLLT'
print(f"\n  Full cluster: {cluster}")
# Does HIHL + MIN = something?
hihl_min = 'MIN' + 'HIHL'
print(f"  MIN+HIHL: {hihl_min}, sorted: {''.join(sorted(hihl_min))}")
matches = find_german_matches(hihl_min, GERMAN_WORDS, plus=2)
print(f"  German matches: {matches}")

# NDCE cross-boundary
ndce_die = 'DIE' + 'NDCE'
print(f"\n  DIE+NDCE: {ndce_die}, sorted: {''.join(sorted(ndce_die))}")
matches = find_german_matches(ndce_die, GERMAN_WORDS, plus=2)
print(f"  German matches: {matches}")

ndce_fach = 'NDCE' + 'FACH'
print(f"  NDCE+FACH: {ndce_fach}, sorted: {''.join(sorted(ndce_fach))}")
matches = find_german_matches(ndce_fach, GERMAN_WORDS, plus=2)
print(f"  German matches: {matches}")

# ================================================================
# 5. NLNDEF analysis (6 chars, 5x)
# ================================================================
print("\n" + "=" * 70)
print("5. NLNDEF (6 chars, 5x)")
print("   Context: DU {NLNDEF} SAGEN AM MIN {HIHL}...")
print("=" * 70)
block5 = 'NLNDEF'
print(f"  Sorted: {''.join(sorted(block5))}")
matches = find_german_matches(block5, GERMAN_WORDS, plus=2)
print(f"  German word matches (+2): {matches}")

# Note: NLNDEF sorted = DEFLNN, FINDEN sorted = DDEFIINN (no match)
# But if we allow code 96 = I temporarily...
nlndef_as_i = block5.replace('L', 'I')
print(f"\n  If L->I substitution: NLNDEF = {nlndef_as_i}")
print(f"  Sorted: {''.join(sorted(nlndef_as_i))}")
matches_i = find_german_matches(nlndef_as_i, GERMAN_WORDS, plus=1)
print(f"  German matches: {matches_i}")

# Cross-boundary DU + NLNDEF + SAGEN
du_nl = 'DU' + block5
nl_sagen = block5 + 'SAGEN'
print(f"\n  DU+NLNDEF: {''.join(sorted(du_nl))}")
print(f"  NLNDEF+SAGEN: {''.join(sorted(nl_sagen))}")

# ================================================================
# 6. IGAA analysis (4 chars, 5x)
# ================================================================
print("\n" + "=" * 70)
print("6. IGAA (4 chars, 5x)")
print("   Context: ES TUT {IGAA} ER GEIGET ES IN {CHN} ES")
print("=" * 70)
block6 = 'IGAA'
print(f"  Sorted: {''.join(sorted(block6))}")
matches = find_german_matches(block6, GERMAN_WORDS, plus=2)
print(f"  German word matches (+2): {matches}")

# TUT + IGAA cross-boundary
tut_igaa = 'TUT' + block6
igaa_er = block6 + 'ER'
print(f"  TUT+IGAA: {tut_igaa}, sorted: {''.join(sorted(tut_igaa))}")
print(f"  IGAA+ER: {igaa_er}, sorted: {''.join(sorted(igaa_er))}")
matches_tut = find_german_matches(tut_igaa, GERMAN_WORDS, plus=2)
matches_er = find_german_matches(igaa_er, GERMAN_WORDS, plus=2)
print(f"  TUT+IGAA matches: {matches_tut}")
print(f"  IGAA+ER matches: {matches_er}")

# ================================================================
# 7. RRNI analysis (4 chars, 5x)
# ================================================================
print("\n" + "=" * 70)
print("7. RRNI (4 chars, 5x)")
print("   Context: ER {L} AB {RRNI} WIR {UOD} IM MIN HEIME")
print("=" * 70)
block7 = 'RRNI'
print(f"  Sorted: {''.join(sorted(block7))}")
matches = find_german_matches(block7, GERMAN_WORDS, plus=2)
print(f"  German word matches (+2): {matches}")

# AB + RRNI cross-boundary
ab_rrni = 'AB' + block7
print(f"  AB+RRNI: {ab_rrni}, sorted: {''.join(sorted(ab_rrni))}")
matches_ab = find_german_matches(ab_rrni, GERMAN_WORDS, plus=2)
print(f"  AB+RRNI matches: {matches_ab}")
# Check LABRNI (original cipher name!)
labrni = 'L' + 'AB' + 'RRNI'
print(f"  L+AB+RRNI = {labrni}: could 'LABRNI' be a proper noun?")
print(f"  Sorted LABRNI: {''.join(sorted(labrni))}")
labrni_matches = find_german_matches(labrni, GERMAN_WORDS, plus=2)
print(f"  LABRNI matches: {labrni_matches}")

# ================================================================
# 8. UOD analysis (3 chars, 7x)
# ================================================================
print("\n" + "=" * 70)
print("8. UOD (3 chars, 7x)")
print("   Context: WIR {UOD} IM MIN HEIME")
print("=" * 70)
block8 = 'UOD'
print(f"  Sorted: {''.join(sorted(block8))}")
matches = find_german_matches(block8, GERMAN_WORDS, plus=1)
print(f"  German word matches (+1): {matches}")
# UOD sorted = DOU -> DUO? no German word. OUD?
# Cross-boundary WIR+UOD
wir_uod = 'WIR' + block8
print(f"  WIR+UOD: {wir_uod}, sorted: {''.join(sorted(wir_uod))}")
matches_wir = find_german_matches(wir_uod, GERMAN_WORDS, plus=2)
print(f"  WIR+UOD matches: {matches_wir}")

# ================================================================
# 9. New cross-boundary discovery scan
# ================================================================
print("\n" + "=" * 70)
print("9. SYSTEMATIC CROSS-BOUNDARY SCAN")
print("   Looking for new garbled+known or known+garbled anagrams")
print("=" * 70)

# Target high-frequency garbled blocks
TARGET_BLOCKS = [
    'WRLGTNELNR', 'UIRUNNHWND', 'UTRUNR', 'HIHL', 'NDCE',
    'HECHLLT', 'NLNDEF', 'IGAA', 'RRNI', 'UOD', 'GAREO',
    'SNHI', 'EOR', 'HHIS', 'TEI', 'MIURIT',
]

KNOWN_WORDS = [
    'STEH', 'FINDEN', 'RUNE', 'RUNEN', 'ODE', 'DEN', 'ENDE',
    'REDER', 'KOENIG', 'SALZBERG', 'AM', 'MIN', 'HEIME',
    'DIE', 'DAS', 'ER', 'ES', 'WIR', 'ICH', 'IN', 'IM',
    'TUT', 'GEIGET', 'SAGEN', 'DU', 'FACH', 'WO', 'AB',
    'HEL', 'NIT', 'SICH', 'SIN', 'MIS', 'AUE',
]

print("\nChecking block+word and word+block combinations:")
for block in TARGET_BLOCKS:
    if len(block) > 8:
        continue  # skip huge blocks
    for word in KNOWN_WORDS:
        combined = block + word
        matches = find_german_matches(combined, GERMAN_WORDS, plus=1)
        if matches:
            print(f"  {block}+{word} = {combined} -> {matches}")
        combined2 = word + block
        matches2 = find_german_matches(combined2, GERMAN_WORDS, plus=1)
        if matches2:
            print(f"  {word}+{block} = {combined2} -> {matches2}")

# ================================================================
# 10. Frequency fingerprint: which codes appear in each block?
# ================================================================
print("\n" + "=" * 70)
print("10. CODE FINGERPRINT FOR KEY BLOCKS")
print("    (All books must use identical codes for same garbled block)")
print("=" * 70)

def get_book_raw_pairs(bidx):
    book = books[bidx]
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    return [book[j:j+2] for j in range(off, len(book)-1, 2)]

# Find raw codes for UTRUNR in each book
print("\nUTRUNR raw codes (expected: 44-64-72-61-14-51):")
utrunr_letter_seq = list('UTRUNR')
for bidx in range(len(books)):
    raw_pairs = get_book_raw_pairs(bidx)
    decoded = ''.join(v7.get(p, '?') for p in raw_pairs)
    idx = 0
    while True:
        pos = decoded.find('UTRUNR', idx)
        if pos < 0:
            break
        if pos + 6 <= len(raw_pairs):
            codes = raw_pairs[pos:pos+6]
            print(f"  Book {bidx:2d} pos {pos}: {'-'.join(codes)}")
        idx = pos + 1

print("\nHIHL raw codes:")
for bidx in range(len(books)):
    raw_pairs = get_book_raw_pairs(bidx)
    decoded = ''.join(v7.get(p, '?') for p in raw_pairs)
    idx = 0
    while True:
        pos = decoded.find('HIHL', idx)
        if pos < 0:
            break
        if pos + 4 <= len(raw_pairs):
            codes = raw_pairs[pos:pos+4]
            print(f"  Book {bidx:2d} pos {pos}: {'-'.join(codes)}")
        idx = pos + 1

print("\nNDCE raw codes:")
for bidx in range(len(books)):
    raw_pairs = get_book_raw_pairs(bidx)
    decoded = ''.join(v7.get(p, '?') for p in raw_pairs)
    idx = 0
    while True:
        pos = decoded.find('NDCE', idx)
        if pos < 0:
            break
        if pos + 4 <= len(raw_pairs):
            codes = raw_pairs[pos:pos+4]
            print(f"  Book {bidx:2d} pos {pos}: {'-'.join(codes)}")
        idx = pos + 1

print("\nDone.")
