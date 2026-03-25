#!/usr/bin/env python3
"""
Session 21 Part 2: Deep investigation of promising leads.

Key leads from Part 1:
1. NLNDEF = FINDEN if L is actually I (5x, "DU NLNDEF SAGEN")
2. HEDDEMI segmentation issue - DP splits as HED+DEM+I (11x)
3. HIHL+NDCE+HECHLLT always appear together (repeating block)
4. UTRUNR = TUR+NUR? (7x, "ODE UTRUNR DEN")
5. SIN as MHG word (5x, "ES {S} IN" -> "ES SIN")
6. Small exact anagrams: ENG=GEN, MI=IM, NIUR=RUIN, etc.
"""

import json, os
from collections import Counter, defaultdict

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

# Reverse mapping: letter -> codes
letter_codes = defaultdict(list)
for code, letter in v7.items():
    letter_codes[letter].append(code)

# ================================================================
# 1. NLNDEF RAW CODE ANALYSIS
# ================================================================
print("=" * 80)
print("1. NLNDEF RAW CODE ANALYSIS - Is L actually I?")
print("=" * 80)

# Find NLNDEF in decoded text and get raw codes
print(f"\n  L codes: {sorted(letter_codes['L'])}")
print(f"  I codes: {sorted(letter_codes['I'])}")

for bidx, text in enumerate(decoded_books):
    pos = 0
    while True:
        idx = text.find('NLNDEF', pos)
        if idx < 0: break
        pairs = book_pairs[bidx]
        if idx + 6 <= len(pairs):
            codes = pairs[idx:idx+6]
            decoded = [v7.get(c, '?') for c in codes]
            ctx_s = max(0, idx - 5)
            ctx_e = min(len(text), idx + 11)
            print(f"  Book {bidx:2d} pos {idx:3d}: codes {' '.join(codes)} = {''.join(decoded)}")
            print(f"    Context: ...{text[ctx_s:ctx_e]}...")
            # The L is at position 1 (N-L-N-D-E-F)
            l_code = codes[1]
            print(f"    The L at pos 1: code {l_code}")
            print(f"    Code {l_code} maps to: {v7.get(l_code, '?')}")
            # What would this code be if mapped to I instead?
            if v7.get(l_code) == 'L':
                print(f"    If {l_code}=I instead of L: N+I+N+D+E+F = NINDEF")
                print(f"    NINDEF anagram of FINDEN? {sorted('NINDEF') == sorted('FINDEN')}")
        pos = idx + 1

# How many times does this specific L code appear overall?
# And in what contexts?
nlndef_l_codes = set()
for bidx, text in enumerate(decoded_books):
    idx = text.find('NLNDEF')
    if idx >= 0 and idx + 6 <= len(book_pairs[bidx]):
        nlndef_l_codes.add(book_pairs[bidx][idx + 1])

for lc in nlndef_l_codes:
    total = sum(1 for pairs in book_pairs for p in pairs if p == lc)
    print(f"\n  Code {lc} (currently {v7.get(lc, '?')}) appears {total}x total")
    print(f"  Sample contexts:")
    count = 0
    for bidx, pairs in enumerate(book_pairs):
        for pi, pair in enumerate(pairs):
            if pair == lc and count < 12:
                text = decoded_books[bidx]
                ctx_s = max(0, pi-4)
                ctx_e = min(len(text), pi+5)
                ctx = text[ctx_s:ctx_e]
                rel = pi - ctx_s
                marker = ctx[:rel] + '[' + ctx[rel] + ']' + ctx[rel+1:]
                print(f"    Book {bidx:2d} pos {pi:3d}: ...{marker}...")
                count += 1

# ================================================================
# 2. HIHL + NDCE + HECHLLT REPEATING BLOCK
# ================================================================
print(f"\n{'=' * 80}")
print("2. HIHL + NDCE + HECHLLT REPEATING BLOCK ANALYSIS")
print("=" * 80)

# These always appear together: "SAGEN AM MIN HIHL DIE NDCE FACH HECHLLT ICH"
# Let's get the raw codes for the entire sequence

target_seq = 'HIHLDIENDC'  # Just HIHL + DIE + NDCE part
for bidx, text in enumerate(decoded_books):
    idx = text.find('HIHL')
    if idx >= 0:
        # Get extended context with codes
        ctx_s = max(0, idx - 8)
        ctx_e = min(len(text), idx + 25)
        pairs = book_pairs[bidx]
        if ctx_e <= len(pairs):
            codes = pairs[ctx_s:ctx_e]
            decoded = text[ctx_s:ctx_e]
            print(f"\n  Book {bidx:2d}: {decoded}")
            print(f"  Codes:   {' '.join(codes)}")
            # Label each position
            for i, (c, d) in enumerate(zip(codes, decoded)):
                pos_label = f"pos {ctx_s+i:3d}"
                print(f"    [{i:2d}] {pos_label}: code {c} = {d}", end='')
                if d in 'HIHL' and i >= (idx - ctx_s) and i < (idx - ctx_s + 4):
                    print(f"  <-- HIHL[{i-(idx-ctx_s)}]", end='')
                print()
        break  # Just show first occurrence

# Now check: what is HIHL in codes?
print(f"\n  HIHL code patterns across all occurrences:")
for bidx, text in enumerate(decoded_books):
    idx = text.find('HIHL')
    if idx >= 0 and idx + 4 <= len(book_pairs[bidx]):
        codes = book_pairs[bidx][idx:idx+4]
        print(f"    Book {bidx:2d}: {' '.join(codes)} = H({codes[0]}) I({codes[1]}) H({codes[2]}) L({codes[3]})")

# NDCE code patterns
print(f"\n  NDCE code patterns:")
for bidx, text in enumerate(decoded_books):
    idx = text.find('NDCE')
    if idx >= 0 and idx + 4 <= len(book_pairs[bidx]):
        codes = book_pairs[bidx][idx:idx+4]
        print(f"    Book {bidx:2d}: {' '.join(codes)} = N({codes[0]}) D({codes[1]}) C({codes[2]}) E({codes[3]})")

# HECHLLT code patterns
print(f"\n  HECHLLT code patterns:")
for bidx, text in enumerate(decoded_books):
    idx = text.find('HECHLLT')
    if idx >= 0 and idx + 7 <= len(book_pairs[bidx]):
        codes = book_pairs[bidx][idx:idx+7]
        decoded_chars = [v7.get(c, '?') for c in codes]
        print(f"    Book {bidx:2d}: {' '.join(codes)} = {''.join(decoded_chars)}")

# The full repeated phrase
print(f"\n  Full repeated phrase pattern:")
print(f"  'SAGEN AM MIN HIHL DIE NDCE FACH HECHLLT ICH OEL'")
print(f"\n  Reading as continuous text (ignoring segmentation):")
print(f"  SAGENAMMINIHIHLDIENNDCEFACHHECHLLTICHOEL")
print(f"\n  What if we re-read the raw codes differently?")

# Get the FULL raw code sequence from MIN to ICH
for bidx, text in enumerate(decoded_books):
    hihl_idx = text.find('HIHL')
    if hihl_idx >= 0:
        # Find MIN before HIHL
        min_start = text.rfind('MIN', max(0, hihl_idx-10), hihl_idx)
        # Find ICH or OEL after HECHLLT
        hechllt_idx = text.find('HECHLLT', hihl_idx)
        if hechllt_idx >= 0:
            end_idx = hechllt_idx + 7 + 6  # +ICH+OEL
            if min_start >= 0 and end_idx <= len(book_pairs[bidx]):
                full_codes = book_pairs[bidx][min_start:end_idx]
                full_text = text[min_start:end_idx]
                print(f"\n  Book {bidx}: '{full_text}'")
                print(f"  Full codes: {' '.join(full_codes)}")
                print(f"  Length: {len(full_codes)} code pairs = {len(full_text)} letters")
                break

# ================================================================
# 3. UTRUNR RAW CODE CHECK
# ================================================================
print(f"\n{'=' * 80}")
print("3. UTRUNR (7x) RAW CODE ANALYSIS")
print("=" * 80)

print(f"\n  UTRUNR code patterns:")
for bidx, text in enumerate(decoded_books):
    idx = text.find('UTRUNR')
    if idx >= 0 and idx + 6 <= len(book_pairs[bidx]):
        codes = book_pairs[bidx][idx:idx+6]
        # Extended context with codes
        ctx_s = max(0, idx - 4)
        ctx_e = min(len(text), idx + 10)
        if ctx_e <= len(book_pairs[bidx]):
            full_codes = book_pairs[bidx][ctx_s:ctx_e]
            full_text = text[ctx_s:ctx_e]
            print(f"  Book {bidx:2d}: '{full_text}' codes: {' '.join(full_codes)}")

# UTRUNR = U,T,R,U,N,R
# ODE UTRUNR DEN ENDE REDER KOENIG
# "or [UTRUNR] the end speaker king"
# What if UTRUNR is two words? TUR + NUR = "door only"
# Or UNTER + RU? = "under RU"?
# Or UNTUR + R? = NATUR - R? (nature)
# Or reversed: RNURTU -> ????

# Let's check if the codes are always identical
utrunr_code_sets = []
for bidx, text in enumerate(decoded_books):
    idx = text.find('UTRUNR')
    if idx >= 0 and idx + 6 <= len(book_pairs[bidx]):
        codes = tuple(book_pairs[bidx][idx:idx+6])
        utrunr_code_sets.append((bidx, codes))

print(f"\n  Code consistency check:")
if utrunr_code_sets:
    ref = utrunr_code_sets[0][1]
    all_same = all(c == ref for _, c in utrunr_code_sets)
    print(f"  All {len(utrunr_code_sets)} occurrences identical: {all_same}")
    if all_same:
        print(f"  Codes: {' '.join(ref)}")
        for i, (code, letter) in enumerate(zip(ref, 'UTRUNR')):
            all_codes = sorted(letter_codes[letter])
            print(f"    [{i}] code {code} = {letter} (all {letter} codes: {all_codes})")

# ================================================================
# 4. HEDDEMI = HEMD + EID HYPOTHESIS
# ================================================================
print(f"\n{'=' * 80}")
print("4. HEDDEMI HYPOTHESIS: HEMD + EID")
print("=" * 80)

# Current behavior: HEDDEMI -> DP splits as HED + DEM + I
# This means the anagram map HEDEMI->HEIME never fires (raw has HEDDEMI)
# And DEM is being falsely matched from inside the garbled block!
# The actual garbled text is HEDDEMI as one unit.

# If HEDDEMI = HEMD (garment) + EID (oath), this would be a 2-word anagram
# Let's verify: HEMD+EID sorted = HEDDEMI sorted
print(f"  HEMD+EID sorted: {sorted('HEMDEID')}")
print(f"  HEDDEMI sorted:  {sorted('HEDDEMI')}")
print(f"  Match: {sorted('HEMDEID') == sorted('HEDDEMI')}")

# Context: "IM MIN HEDDEMI DIE URALTE" = "in love/my HEMD+EID the ancient"
# HEMD = garment, shirt
# EID = oath
# "in my garment-oath" ? Doesn't make great narrative sense.

# Alternative: what about DIEHEIME (using D as connector)?
# HEDDEMI + D = HEDDEMID -> no
# What if HEDDEMI is actually HEIMEDD or similar?
# HEDDEMI = HEIME + DD -> homes + extra DD? (+2 pattern)
# Or: is there a 7-letter MHG word?

# GEHEIMDE? No wrong letters
# MEDIZIN? Wrong letters
# Let's try: what words can be made from D,D,E,E,H,I,M ?

# Actually, the more important question: can we fix the segmentation?
# The garbled report shows {HED} 11x and {I} 17x (some from HEDDEMI)
# If we add HEDDEMI to the anagram map mapping to... what?

# Let me check how many of the 11 {HED} occurrences come from HEDDEMI
print(f"\n  Checking {'{'}HED{'}'} origins:")
for bidx, text in enumerate(decoded_books):
    idx = text.find('HEDDEMI')
    if idx >= 0:
        # Show context
        ctx_s = max(0, idx - 8)
        ctx_e = min(len(text), idx + 12)
        print(f"    Book {bidx:2d} pos {idx:3d}: ...{text[ctx_s:ctx_e]}...")

# Are ALL 11 {HED} from HEDDEMI?
hed_from_heddemi = 0
hed_standalone = 0
for bidx, text in enumerate(decoded_books):
    pos = 0
    while True:
        idx = text.find('HED', pos)
        if idx < 0: break
        # Check if this is part of HEDDEMI
        if text[idx:idx+7] == 'HEDDEMI':
            hed_from_heddemi += 1
        else:
            hed_standalone += 1
            ctx_s = max(0, idx - 5)
            ctx_e = min(len(text), idx + 8)
        pos = idx + 1

print(f"\n  HED from HEDDEMI: {hed_from_heddemi}x")
print(f"  HED standalone: {hed_standalone}x")

# ================================================================
# 5. SIN (MHG "his") TEST
# ================================================================
print(f"\n{'=' * 80}")
print("5. SIN (MHG 'his/its') - WOULD ADDING TO KNOWN HELP?")
print("=" * 80)

# {S} IN pattern appears 5x: "ES {S} IN"
# If SIN is a word, text "ESSIN" -> E+S+SIN (SIN=3, vs S(0)+IN(2) = less coverage)
# Wait, ES is also matched. So it's ES + SIN vs ES + {S} + IN

# Let's count occurrences of "SIN" in decoded text that aren't part of longer words
sin_count = 0
for bidx, text in enumerate(decoded_books):
    pos = 0
    while True:
        idx = text.find('SIN', pos)
        if idx < 0: break
        # Check it's not part of SIND, SINNE, WISTEN, etc.
        ctx_s = max(0, idx - 3)
        ctx_e = min(len(text), idx + 6)
        ctx = text[ctx_s:ctx_e]
        # Check if SIN is standalone (not part of longer known word)
        before = text[idx-1:idx] if idx > 0 else ''
        after = text[idx+3:idx+4] if idx+3 < len(text) else ''
        print(f"  Book {bidx:2d} pos {idx:3d}: ...{ctx}... (before='{before}', after='{after}')")
        sin_count += 1
        pos = idx + 1

print(f"\n  Total SIN in text: {sin_count}x")

# Test: what if we add SIN to KNOWN?
# The issue is SIN appears inside WISTEN, SINDEN, etc.
# DP should handle this correctly since it maximizes coverage

# ================================================================
# 6. THE {S} {D} {I} {H} {L} PATTERNS - ARE THEY WORD FRAGMENTS?
# ================================================================
print(f"\n{'=' * 80}")
print("6. HIGH-FREQUENCY SINGLE LETTER PATTERNS")
print("=" * 80)

# {T} 23x: 13x as ER|T|EIN -> "ER T EIN ER SEIN GOTTDIENER"
# This is part of the repeating phrase! What word is between ER and EIN?
# "ER [T] EIN" = he [T] a = he [takes?] a
# German: TEIN? TEILT? No, just one letter T.
# What if it's: ER T+EIN = ERTEIN? Or E+R+T+E+I+N?
# TUT (does)? Only 3 letters but we see just T.
# Actually, "ER {T} EIN ER SEIN GOTTDIENER" repeats 13x
# The T is always between ER and EIN.
# What if the text is actually "ERT EIN" = ? Or "ER TEIN"?
# TEIN is not a standard word.
# What about: the raw text has a two-code sequence that decodes to just "T"
# meaning it's a single letter. This single T could be:
# - A garbled preposition or particle
# - Part of a word that got split

print(f"\n  Pattern: ER {{T}} EIN ER SEIN GOTTDIENER (13x)")
print(f"  Raw codes for the T:")
for bidx, text in enumerate(decoded_books):
    # Find pattern: ER + T + EIN
    idx = text.find('TEINERSEIN')  # TEINERSEINGOTTDIENER
    if idx < 0:
        idx = text.find('TEINERSEI')
    if idx >= 0:
        # T is at idx, ER before it
        t_pos = idx
        if t_pos > 0 and text[t_pos-2:t_pos] == 'ER':
            code = book_pairs[bidx][t_pos]
            print(f"  Book {bidx:2d}: code {code} = T (T codes: {sorted(letter_codes['T'])})")
            # What are the surrounding codes?
            ctx_codes = book_pairs[bidx][max(0,t_pos-3):t_pos+4]
            ctx_text = text[max(0,t_pos-3):t_pos+4]
            print(f"    Context: {ctx_text} = {' '.join(ctx_codes)}")

# {I} 17x: 10x as DEM|I|DIE -> "DEM I DIE"
# These are from HEDDEMI! The I at the end of HEDDEMI after DP eats DEM
# Let's verify
print(f"\n  Pattern: DEM {{I}} DIE (10x)")
print(f"  These are likely the tail of HEDDEMI after DP extracts DEM")

# {H} 9x: 7x as IN|H|IM -> "IN H IM"
# What if this is INHIM or IN+HIM?
# HIM is not standard German. HEIM (home) needs E.
# Or: IN + H + IM = the H is a garbled fragment
print(f"\n  Pattern: IN {{H}} IM (7x)")
print(f"  Raw codes for H between IN and IM:")
h_between_count = 0
for bidx, text in enumerate(decoded_books):
    pos = 0
    while True:
        idx = text.find('INHIM', pos)
        if idx < 0: break
        h_pos = idx + 2  # The H
        if h_pos < len(book_pairs[bidx]):
            code = book_pairs[bidx][h_pos]
            ctx_codes = book_pairs[bidx][max(0,h_pos-3):h_pos+4]
            ctx_text = text[max(0,h_pos-3):h_pos+4]
            print(f"  Book {bidx:2d}: code {code} = H  ctx: {ctx_text} = {' '.join(ctx_codes)}")
            h_between_count += 1
        pos = idx + 1

# {L} 11x: 4x as ER|L|AB -> "ER L AB"
# L + AB = LAB? LABT (refreshes) is already known...
# But the text has ER + L + AB, not ERLAB.
# What if this is ER + LAB? LAB = rennet/stomach (MHG)
# Or: ERL + AB? ERL = alder tree
print(f"\n  Pattern: ER {{L}} AB (4x)")
print(f"  Could be: ER LAB (he stomach/rennet) or ERL AB (alder from)")

# {N} 12x: 3x as DU|N|TER
# DU N TER = you N of-the
# What if N+TER = NTER? Or DU+N = DUN?
# UNTER (under)? Would need the text to have UNTER not DUNTER
print(f"\n  Pattern: DU {{N}} TER (3x)")

# ================================================================
# 7. THE REPEATING STRUCTURAL FORMULA
# ================================================================
print(f"\n{'=' * 80}")
print("7. REPEATING STRUCTURAL FORMULA")
print("=" * 80)

# The narrative has a clear repeating structure. Let me map it.
# Looking at the full decoded text, these phrases repeat ~8x:
# "TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIES ER {T} EIN ER SEIN GOTTDIENER"
# "DIE URALTE STEINEN TER SCHARDT IST SCHAUN"
# "DEN ENDE REDER KOENIG SALZBERG {UNE} NIT GEHEN ORANGENSTRASSE"
# "IM MIN {HED} DEM {I} DIE URALTE"
# "ER {L} AB {RRNI} WIR/DIE"

# Let's count exact repeating phrases
phrases_to_check = [
    "TRAUT IST LEICH AN BERUCHTIG ER SO DASS TUN DIES ER",
    "DIE URALTE STEINEN TER SCHARDT IST SCHAUN",
    "DEN ENDE REDER KOENIG",
    "SAGEN AM MIN",
    "ODE UTRUNR DEN",
    "DIE NDCE FACH",
    "IM MIN HED",
    "ER L AB",
]

# Need the full segmented narrative - let me reconstruct it
KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR', 'NU', 'STANDE', 'NACHTS', 'NIT', 'TOT', 'TER',
    'ABER', 'ALLE', 'ALLES', 'ALTE', 'ALTEN', 'ALTER', 'AUCH', 'BAND',
    'BERG', 'BURG', 'DENN', 'DIES', 'DIESE', 'DIESER', 'DIESEN',
    'DIESEM', 'DOCH', 'DORT', 'DREI', 'DURCH', 'EINE', 'EINEM',
    'EINEN', 'EINER', 'EINES', 'ENDE', 'ERDE', 'ERST', 'ERSTE',
    'FACH', 'FAND', 'FERN', 'FEST', 'FORT', 'GAR', 'GANZ', 'GEGEN',
    'GEIST', 'GOTT', 'GOLD', 'GRAB', 'GROSS', 'GRUFT', 'GUT',
    'HAND', 'HEIM', 'HELD', 'HERR', 'HIER', 'HOCH', 'IMMER',
    'KANN', 'KLAR', 'KRAFT', 'LAND', 'LANG', 'LICHT', 'MACHT',
    'MEHR', 'MUSS', 'NACH', 'NACHT', 'NAHM', 'NAME', 'NEU', 'NEUE',
    'NEUEN', 'NICHT', 'NIE', 'NOCH', 'ODER', 'ORT', 'ORTEN',
    'REDE', 'REDEN', 'REICH', 'RIEF', 'RUIN', 'RUNE', 'RUNEN',
    'SAND', 'SAGT', 'SCHAUN', 'SCHON', 'SEHR', 'SEID', 'SEIN',
    'SEINE', 'SEINEN', 'SEINER', 'SEINEM', 'SEINES',
    'SICH', 'SIND', 'SOHN', 'SOLL', 'STEH', 'STEIN', 'STEINE',
    'STEINEN', 'STERN', 'TAG', 'TAGE', 'TAGEN', 'TAT', 'TEIL',
    'TIEF', 'TOD', 'TURM', 'UNTER', 'URALTE', 'VIEL', 'VIER',
    'WAHR', 'WALD', 'WAND', 'WARD', 'WEIL', 'WELT', 'WENN', 'WERT',
    'WESEN', 'WILL', 'WIND', 'WIRD', 'WORT', 'WORTE', 'ZEIT',
    'ZEHN', 'ZORN',
    'FINDEN', 'GEBEN', 'GEHEN', 'HABEN', 'KOMMEN', 'LEBEN', 'LESEN',
    'NEHMEN', 'SAGEN', 'SEHEN', 'STEHEN', 'SUCHEN', 'WISSEN',
    'WISSET', 'RUFEN', 'WIEDER',
    'OEL', 'SCE', 'MINNE', 'MIN', 'ODE', 'SER', 'GEN', 'INS',
    'GEIGET', 'BERUCHTIG', 'BERUCHTIGER', 'MEERE', 'NEIGT',
    'WISTEN', 'MANIER', 'HUND', 'GODE', 'GODES', 'EIGENTUM',
    'REDER', 'THENAEUT', 'LABT', 'MORT', 'DIGE', 'WEGE',
    'KOENIGS', 'NAHE', 'NOT', 'NOTH', 'ZUR', 'OWI', 'ENGE',
    'SEIDEN', 'ALTES', 'DENN', 'BIS', 'NIE', 'NUT', 'NUTZ',
    'HEIL', 'NEID', 'TREU', 'TREUE', 'SUN', 'DIENST', 'SANG',
    'DINC', 'HULDE', 'NACH', 'STEINE', 'LANT', 'HERRE', 'DIENEST',
    'GEBOT', 'SCHWUR', 'ORDEN', 'RICHTER', 'DUNKEL', 'EHRE',
    'EDELE', 'SCHULD', 'SEGEN', 'FLUCH', 'RACHE',
    'KOENIG', 'DASS', 'EDEL', 'ADEL', 'SCHRAT',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME', 'SCHARDT',
])

for phrase in phrases_to_check:
    count = 0
    for text in decoded_books:
        count += text.count(phrase.replace(' ', ''))
    print(f"  {phrase}: {count}x in decoded text")

# ================================================================
# 8. UNE (4x, "SALZBERG UNE NIT") - IS THIS A WORD?
# ================================================================
print(f"\n{'=' * 80}")
print("8. UNE (4x) ANALYSIS")
print("=" * 80)

# Context: SALZBERG UNE NIT GEHEN ORANGENSTRASSE
# = "Salzberg UNE not go Orangenstrasse"
# UNE could be:
# - UND (and) with wrong last letter? But D is a common code
# - MHG "une" = without (archaic form of "ohne")!
# - ANE = MHG for "without" (more common MHG form)
# If UNE = "without": "Salzberg without not go Orangenstrasse"
# Double negative: "Salzberg without not going" = "must go via"?

print(f"  Context: 'SALZBERG UNE NIT GEHEN ORANGENSTRASSE'")
print(f"  UNE sorted = {sorted('UNE')}")
print(f"  Possible words:")
print(f"    - MHG 'une' = without (variant of 'ane/ohne')")
print(f"    - Anagram of NEU (new)? sorted NEU = {sorted('NEU')} = match!")
print(f"  UNE = NEU (new)? 'Salzberg new/again not go Orangenstrasse'")

# Check raw codes
for bidx, text in enumerate(decoded_books):
    idx = text.find('UNE')
    if idx >= 0 and idx + 3 <= len(book_pairs[bidx]):
        codes = book_pairs[bidx][idx:idx+3]
        ctx_s = max(0, idx - 10)
        ctx_e = min(len(text), idx + 15)
        print(f"  Book {bidx:2d}: codes {' '.join(codes)} = UNE  ctx: {text[ctx_s:ctx_e]}")

# ================================================================
# 9. RRNI (5x, "AB RRNI WIR/DIE")
# ================================================================
print(f"\n{'=' * 80}")
print("9. RRNI (5x) - DEEPER ANALYSIS")
print("=" * 80)

# Context: always "ER {L} AB {RRNI} WIR" or "ER {L} AB {RRNI} DIE"
# Full pattern: "ER L AB RRNI WIR/DIE UOD IM MIN HED DEM I DIE URALTE"
#
# What if "L AB RRNI" is actually one block? LABRRNI?
# LABRRNI -> IRRN + AB + L?
# Or: AB + RRNI = ABRRIN -> NARRIB? No...
# RRNI = IRREN (to err) without E?
# IRRE (mad) = I,R,R,E not I,R,R,N

# Let me check codes
print(f"  RRNI code patterns:")
for bidx, text in enumerate(decoded_books):
    idx = text.find('RRNI')
    if idx >= 0 and idx + 4 <= len(book_pairs[bidx]):
        codes = book_pairs[bidx][idx:idx+4]
        # Extended context
        ctx_s = max(0, idx - 6)
        ctx_e = min(len(text), idx + 10)
        if ctx_e <= len(book_pairs[bidx]):
            full_codes = book_pairs[bidx][ctx_s:ctx_e]
            full_text = text[ctx_s:ctx_e]
            print(f"  Book {bidx:2d}: '{full_text}' = {' '.join(full_codes)}")

# ================================================================
# 10. RUI (7x, "SCHAUN RUI IN") - VIEW/BEHOLD?
# ================================================================
print(f"\n{'=' * 80}")
print("10. RUI (7x) - SCHAUN RUI IN")
print("=" * 80)

# Context: always "IST SCHAUN RUI IN WISTEN"
# SCHAUN = look/behold
# RUI = RUIN minus N? Or related to RUHE (rest)?
# "is to behold RUI in" = "is to behold ruin in"?
# Actually RUIN is already a known word, and RUI is not RUIN (missing N)
# But +1 analysis showed: RUI -> UR (removing I) or IR (removing U)
# Could RUI be an anagram of something with context?

# "SCHAUN RUI IN" vs "SCHAUN RUIN IN" - just missing an N?
# Let me check: does the raw text actually have RUIN or RUI?
print(f"  RUI code patterns:")
for bidx, text in enumerate(decoded_books):
    idx = text.find('RUI')
    if idx >= 0 and text[idx:idx+4] != 'RUIN':
        if idx + 3 <= len(book_pairs[bidx]):
            codes = book_pairs[bidx][idx:idx+3]
            ctx_s = max(0, idx - 6)
            ctx_e = min(len(text), idx + 8)
            print(f"  Book {bidx:2d}: codes {' '.join(codes)} ctx: {text[ctx_s:ctx_e]}")

# What if RUI is just RUIN without N? Or an abbreviation?
# In MHG, there are words like:
# RIUWE = regret, sorrow
# But RUI doesn't match standard MHG patterns
# SCHAUN RUIN = "behold ruin" makes narrative sense with the story

print(f"\n  If RUI + following I/N forms RUIN:")
for bidx, text in enumerate(decoded_books):
    idx = text.find('RUI')
    if idx >= 0 and text[idx:idx+4] != 'RUIN':
        after = text[idx+3:idx+6] if idx+3 < len(text) else ''
        print(f"  Book {bidx:2d}: RUI + '{after}'...")

print(f"\nDone with deep investigation.")
