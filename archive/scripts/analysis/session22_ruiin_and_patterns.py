#!/usr/bin/env python3
"""
Session 22: Investigate RUIIN -> RUIN (+1 anagram) and other recurring garbled blocks.

Key targets:
- {RUI} IN pattern: is it RUIIN = RUIN + I (+1)?
- {IGAA}: appears after TUT, before ER GEIGET - 5x+
- {CHN}: 8x recurring
- {UOD}: 6x recurring
- {RRNI}: 5x recurring
"""

import json, os
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

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    return 0 if ic_from_counts(Counter(bp0), len(bp0)) > ic_from_counts(Counter(bp1), len(bp1)) else 1

# Current anagram map (all confirmed)
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
    'ANSD': 'SAND',
    'TTU': 'TUT', 'TERLAU': 'URALTE', 'EUN': 'NEU', 'NIUR': 'RUIN',
}

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

# Build processed text with current anagrams
processed = ''.join(decoded_books)
for old in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    processed = processed.replace(old, ANAGRAM_MAP[old])

# ================================================================
# 1. RUIIN -> RUIN (+1) investigation
# ================================================================
print("=" * 60)
print("INVESTIGATION: RUIIN -> RUIN (+1 anagram)")
print("=" * 60)

# Find all occurrences of RUIIN in processed text
pos = 0
ruiin_count = 0
while True:
    idx = processed.find('RUIIN', pos)
    if idx < 0: break
    ruiin_count += 1
    ctx = processed[max(0,idx-15):idx+20]
    print(f"  #{ruiin_count} pos {idx}: ...{ctx}...")
    pos = idx + 1

print(f"\n  Total RUIIN occurrences: {ruiin_count}")

# Check: does RUIN appear standalone (not as part of RUIIN)?
pos = 0
ruin_count = 0
while True:
    idx = processed.find('RUIN', pos)
    if idx < 0: break
    # Check if it's part of RUIIN
    if idx + 4 < len(processed) and processed[idx+4] == 'N':
        # RUINN - not RUIIN
        pass
    if idx > 0 and processed[idx-1:idx+5] == 'RUIIN' or processed[idx:idx+5] == 'RUIIN':
        ruin_count += 1
        ctx = processed[max(0,idx-10):idx+14]
        # print(f"    RUIN inside RUIIN at {idx}: ...{ctx}...")
    else:
        ruin_count += 1
        ctx = processed[max(0,idx-10):idx+14]
        print(f"  Standalone RUIN at {idx}: ...{ctx}...")
    pos = idx + 1

# Check collision: would replacing RUIIN -> RUIN break anything?
test_text = processed.replace('RUIIN', 'RUIN')
known_words = ['SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE', 'GOTTDIENER',
               'SCHARDT', 'TRAUT', 'LEICH', 'HEIME', 'EIGENTUM',
               'BERUCHTIG', 'MEERE', 'NEIGT', 'WISTEN', 'MANIER',
               'GODES', 'DIENST', 'BEI', 'STANDE', 'NACHTS',
               'SAGEN', 'GEHEN', 'SCHRAT', 'SAND', 'RUIN', 'RUNEN',
               'RUNE', 'TUT', 'URALTE', 'NEU']
broken = []
for w in known_words:
    oc = processed.count(w)
    nc = test_text.count(w)
    if nc < oc:
        broken.append((w, oc, nc))
if broken:
    print(f"\n  COLLISIONS:")
    for w, oc, nc in broken:
        print(f"    {w}: {oc} -> {nc}")
else:
    print(f"\n  No collisions detected. RUIIN -> RUIN is SAFE.")

# What does the text look like after replacement?
print(f"\n  After RUIIN -> RUIN:")
pos = 0
while True:
    idx = processed.find('RUIIN', pos)
    if idx < 0: break
    before = processed[max(0,idx-15):idx]
    after = processed[idx+5:idx+20]
    print(f"    ...{before}[RUIN]{after}...")
    pos = idx + 1

# Also check: sorted letters match?
from itertools import permutations
ruiin_sorted = ''.join(sorted('RUIIN'))
ruin_sorted = ''.join(sorted('RUIN'))
print(f"\n  RUIIN sorted: {ruiin_sorted}")
print(f"  RUIN sorted:  {ruin_sorted}")
print(f"  Extra letter:  I (= +1 anagram pattern)")

# ================================================================
# 2. IGAA investigation (appears after TUT)
# ================================================================
print(f"\n{'='*60}")
print("INVESTIGATION: IGAA (after ES TUT)")
print(f"{'='*60}")

pos = 0
igaa_count = 0
while True:
    idx = processed.find('IGAA', pos)
    if idx < 0: break
    igaa_count += 1
    ctx = processed[max(0,idx-15):idx+19]
    print(f"  #{igaa_count} pos {idx}: ...{ctx}...")
    pos = idx + 1

print(f"\n  Total IGAA: {igaa_count}")
# Sorted: AAGI. German words: GAIA? Not standard.
# Check if IGAA could be part of a larger pattern
# Common context: "ES TUT IGAA ER GEIGET"
# What if TUT+IGAA = TUTIGAA? Or IGAA alone?
# IGAA sorted = AAGI
# Check all 4-letter anagrams
from itertools import permutations
igaa_perms = set(''.join(p) for p in permutations('IGAA'))
german_4 = {'GAIA', 'AGIA'}  # not real German words
print(f"  IGAA permutations that could be German: checking...")
# Actually check 4+5 letter words
for perm in sorted(igaa_perms):
    if perm in {'GAIA'}: print(f"    {perm} - mythological?")

# What about TUTIGAA (7 chars)? or IGAAER (6 chars)?
print(f"\n  Extended patterns:")
for ext_len in [5, 6, 7, 8]:
    pos = 0
    while True:
        idx = processed.find('IGAA', pos)
        if idx < 0: break
        start = max(0, idx - (ext_len - 4))
        chunk = processed[idx:idx+ext_len]
        chunk_before = processed[start:idx+4]
        pos = idx + 1

# Check TTUIGAA (before TTU->TUT replacement, this was the raw form)
raw_processed = ''.join(decoded_books)
for old in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    if old != 'TTU':  # skip TTU to see raw
        raw_processed = raw_processed.replace(old, ANAGRAM_MAP[old])

pos = 0
print(f"\n  Raw TTUIGAA contexts (before TTU->TUT):")
while True:
    idx = raw_processed.find('TTUIGAA', pos)
    if idx < 0: break
    ctx = raw_processed[max(0,idx-10):idx+17]
    print(f"    pos {idx}: ...{ctx}...")
    pos = idx + 1

# What about IGAA = part of a word with context?
# ES TUT IGAA ER GEIGET = "it does IGAA he fiddles"
# Could IGAA be a verb? TUT + verb = "does [verb]"?
# German: "es tut ... " often followed by a verb or adjective
# IGAA sorted = AAGI. With +1: could be GAI+A, but no German word
# What if I look at IGAAER? Sorted: AAEIGR = GEIAR? GAIER? GRAIE?
# ERGAB? no, that's ABEGR
# RAGEI? GERAI?
igaaer = 'IGAAER'
igaaer_sorted = ''.join(sorted(igaaer))
print(f"\n  IGAAER sorted: {igaaer_sorted} (6 chars)")
print(f"  Possible: REAGIE? GAIER? - no standard German word found")

# What about just IGAA -> some 3-letter word +1?
# IGAA has I,G,A,A - remove each: GAA, IAA, IGA, IGA
# GAA -> not a word. IAA -> not a word. IGA -> not a word.
# 3-letter words from {I,G,A}: GAI, GIA, AIG, AGI, IAG, IGA - none standard German
print(f"  IGAA as +1 of 3-letter word: no valid German word found")

# ================================================================
# 3. CHN investigation (8x)
# ================================================================
print(f"\n{'='*60}")
print("INVESTIGATION: CHN (8x)")
print(f"{'='*60}")

pos = 0
chn_count = 0
chn_contexts = []
while True:
    idx = processed.find('CHN', pos)
    if idx < 0: break
    # Make sure it's actually garbled CHN, not part of NACHTS etc
    # Check if it's inside a known word
    ctx = processed[max(0,idx-12):idx+15]
    chn_count += 1
    chn_contexts.append((idx, ctx))
    print(f"  #{chn_count} pos {idx}: ...{ctx}...")
    pos = idx + 1

# CHN sorted = CHN. Anagram of NCH? German: "noch"? But that's 4 letters.
# Actually CHN has only 3 chars. Permutations: CHN, CNH, HCN, HNC, NCH, NHC
# NCH could be part of "noch" but it's only 3 chars
print(f"\n  CHN permutations: CHN, CNH, HCN, HNC, NCH, NHC")
print(f"  None are standalone German words (too short/unusual)")

# ================================================================
# 4. UOD investigation (6x)
# ================================================================
print(f"\n{'='*60}")
print("INVESTIGATION: UOD (6x)")
print(f"{'='*60}")

pos = 0
uod_count = 0
while True:
    idx = processed.find('UOD', pos)
    if idx < 0: break
    uod_count += 1
    ctx = processed[max(0,idx-12):idx+15]
    print(f"  #{uod_count} pos {idx}: ...{ctx}...")
    pos = idx + 1

# UOD sorted = DOU. Anagram: DOU, OUD, UDO (name?), DUO!
print(f"\n  UOD sorted: DOU")
print(f"  Possible: DUO (pair/duet)? UDO (name)? OD/OUD?")
print(f"  DUO is a real word! Check context: 'WIR UOD IM MIN HEIME'")
print(f"  'WIR DUO IM MIN HEIME' = 'we duo/pair in my/love home'")

# Check collision for UOD -> DUO
test2 = processed.replace('UOD', 'DUO')
broken2 = []
for w in known_words:
    oc = processed.count(w)
    nc = test2.count(w)
    if nc < oc:
        broken2.append((w, oc, nc))
if broken2:
    print(f"  UOD->DUO COLLISIONS: {broken2}")
else:
    print(f"  UOD->DUO: No collisions")

# But wait - context is "WIR {UOD} IM" - could UOD be part of cross-boundary?
# Check R+UOD or UOD+I
print(f"\n  Cross-boundary check:")
for ext in ['RUOD', 'UODI', 'UODIM', 'WIRUOD']:
    pos = 0
    while True:
        idx = processed.find(ext, pos)
        if idx < 0: break
        print(f"    '{ext}' at {idx}: sorted = {''.join(sorted(ext))}")
        pos = idx + 1

# ================================================================
# 5. RRNI investigation (5x)
# ================================================================
print(f"\n{'='*60}")
print("INVESTIGATION: RRNI (5x)")
print(f"{'='*60}")

pos = 0
rrni_count = 0
while True:
    idx = processed.find('RRNI', pos)
    if idx < 0: break
    rrni_count += 1
    ctx = processed[max(0,idx-12):idx+16]
    print(f"  #{rrni_count} pos {idx}: ...{ctx}...")
    pos = idx + 1

# RRNI sorted = INRR. Anagram: INRR? NIRR? RRIN?
# With +1: RRNI = IRR+N? IRREN has 5 letters...
# IRR = astray (German: in die Irre). IRRN? Not standard.
# What about cross-boundary? Context: "AB {RRNI} WIR"
# AB+RRNI = ABRRNI sorted = ABINRR. No 6-letter German word.
# RRNI+W = RRNIW sorted = INRRW. No.
# What if just RRNI -> IRRN? Not a word. NIRR? No.
print(f"\n  RRNI sorted: INRR")
print(f"  No clear anagram found. Could be garbled code issue.")

# ================================================================
# 6. Check all remaining 3-4 letter garbled blocks for anagrams
# ================================================================
print(f"\n{'='*60}")
print("SYSTEMATIC: All 3-4 char garbled blocks, check for anagrams")
print(f"{'='*60}")

# Use DP to find garbled blocks
KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN', 'TUT',
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
    'GEIGET', 'BERUCHTIG', 'BERUCHTIGER', 'MEERE', 'NEIGT', 'WISTEN',
    'MANIER', 'HUND', 'GODE', 'GODES', 'EIGENTUM', 'REDER',
    'THENAEUT', 'LABT', 'MORT', 'DIGE', 'WEGE', 'KOENIGS',
    'NAHE', 'NOT', 'NOTH', 'ZUR', 'OWI', 'ENGE', 'SEIDEN',
    'ALTES', 'DENN', 'BIS', 'NIE', 'NUT', 'NUTZ', 'HEIL', 'NEID',
    'TREU', 'TREUE', 'SUN', 'DIENST', 'SANG', 'DINC', 'HULDE',
    'NACH', 'STEINE', 'LANT', 'HERRE', 'DIENEST', 'GEBOT',
    'SCHWUR', 'ORDEN', 'RICHTER', 'DUNKEL', 'EHRE', 'EDELE',
    'SCHULD', 'SEGEN', 'FLUCH', 'RACHE', 'KOENIG', 'DASS',
    'EDEL', 'ADEL', 'SCHRAT', 'SALZBERG', 'WEICHSTEIN',
    'ORANGENSTRASSE', 'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH',
    'HEIME', 'SCHARDT',
])

def dp_segment(text):
    n = len(text)
    dp = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], None)
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if cand in KNOWN:
                score = dp[start][0] + wlen
                if score > dp[i][0]:
                    dp[i] = (score, (start, cand))
    tokens = []
    i = n
    while i > 0:
        if dp[i][1] is not None:
            start, word = dp[i][1]
            tokens.append(('W', word))
            i = start
        else:
            tokens.append(('C', text[i-1]))
            i -= 1
    tokens.reverse()
    result = []
    for kind, val in tokens:
        if kind == 'W':
            result.append(val)
        else:
            if result and result[-1].startswith('{'):
                result[-1] = result[-1][:-1] + val + '}'
            else:
                result.append('{' + val + '}')
    return result, dp[n][0]

tokens, covered = dp_segment(processed)

# Extract garbled blocks
garbled_blocks = Counter()
for t in tokens:
    if t.startswith('{'):
        block = t[1:-1]
        garbled_blocks[block] += 1

# Focus on 3-4 char blocks
print(f"\nAll 3-4 char garbled blocks (freq >= 2):")
small_blocks = {b: c for b, c in garbled_blocks.items() if 3 <= len(b) <= 4 and c >= 2}
for block, count in sorted(small_blocks.items(), key=lambda x: -x[1]):
    sorted_b = ''.join(sorted(block))
    # Check if any permutation is a known German word
    matches = []
    if len(block) <= 4:
        for perm in set(''.join(p) for p in permutations(block)):
            if perm in KNOWN:
                matches.append(perm)
    # Also check +1 (removing each letter)
    plus1 = []
    for i in range(len(block)):
        reduced = block[:i] + block[i+1:]
        for perm in set(''.join(p) for p in permutations(reduced)):
            if perm in KNOWN and len(perm) >= 2:
                plus1.append(f"{perm}+{block[i]}")

    match_str = f" -> EXACT: {matches}" if matches else ""
    plus1_str = f" -> +1: {plus1}" if plus1 else ""
    print(f"  {block:6s} {count}x (sorted: {sorted_b}){match_str}{plus1_str}")

# ================================================================
# 7. Deeper: EO pattern (5x)
# ================================================================
print(f"\n{'='*60}")
print("INVESTIGATION: EO (5x)")
print(f"{'='*60}")

pos = 0
eo_count = 0
while True:
    idx = processed.find('EO', pos)
    if idx < 0: break
    # Check if inside a known word or garbled
    ctx = processed[max(0,idx-8):idx+10]
    # Simple heuristic: check surrounding
    eo_count += 1
    if eo_count <= 10:
        print(f"  #{eo_count} pos {idx}: ...{ctx}...")
    pos = idx + 1

# Context: "ODE GAR {EO} RUNE ORT" - always same pattern
# EO could be part of cross-boundary: GAR+EO or EO+RUNE
# GAREO sorted = AEGOR -> ORAGE? no. ERGO+A? ERGO!
# EO+R = EOR sorted = EOR -> ORE, OER?
# Actually check GAREO: sorted AEGOR
# REGAL? no. ORAGE? no. ERGO = "therefore" (Latin, used in German)!
# But ERGO = ERGO, and GAREO sorted is AEGOR. That's ERGO+A.
# Not quite. Let me check: GAR = known word, EO = garbled.
# What if it's not GAR+{EO} but GA+{REO}? Let me check the DP.
print(f"\n  Checking if GAREO is actually GA+{'{REO}'} or GAR+{'{EO}'}...")
print(f"  GAR is a known word (3 chars), so DP prefers GAR + {{EO}}")
print(f"  But GAREO sorted = {''.join(sorted('GAREO'))}")
print(f"  Could be: ORAGE? ERGO+A? None are standard German.")
print(f"  EO alone: no 2-letter German word. Cross-boundary with RUNE: EORUNE sorted = {''.join(sorted('EORUNE'))}")

# ================================================================
# 8. Single-letter {T} between ER and EIN (13x)
# ================================================================
print(f"\n{'='*60}")
print("INVESTIGATION: ER {T} EIN pattern (13x)")
print(f"{'='*60}")

# This is "SERTEIN" in raw text - ER + T + EIN
# Could this be SERTI + EIN? Or ER + TEIN?
# ERTEIN = 6 chars sorted EEINRT
# REITEN (to ride)? sorted EEINRT = match!
# ERTEIN sorted = EEINRT, REITEN sorted = EEINRT. YES!
ertein_sorted = ''.join(sorted('ERTEIN'))
reiten_sorted = ''.join(sorted('REITEN'))
print(f"  ERTEIN sorted: {ertein_sorted}")
print(f"  REITEN sorted: {reiten_sorted}")
print(f"  MATCH! ERTEIN = REITEN (to ride) - exact anagram!")

# But wait - DP sees "ER {T} EIN" = ER(2) + EIN(3) = 5 chars covered
# If ERTEIN -> REITEN: REITEN(6) = 6 chars covered = +1 gain per occurrence
# Need to check: does ERTEIN always appear in this context?
pos = 0
ertein_count = 0
while True:
    idx = processed.find('ERTEIN', pos)
    if idx < 0: break
    ertein_count += 1
    ctx = processed[max(0,idx-10):idx+16]
    print(f"  #{ertein_count} pos {idx}: ...{ctx}...")
    pos = idx + 1

print(f"\n  Total ERTEIN: {ertein_count}")

# But ERTEIN is very common as ER+TEIN or ERT+EIN substrings
# Need to check collisions carefully
test3 = processed.replace('ERTEIN', 'REITEN')
broken3 = []
for w in known_words + ['GOTTDIENER', 'GOTTDIENERS', 'ORANGENSTRASSE', 'EIGENTUM']:
    oc = processed.count(w)
    nc = test3.count(w)
    if nc < oc:
        broken3.append((w, oc, nc))
if broken3:
    print(f"  ERTEIN->REITEN COLLISIONS: {broken3}")
else:
    print(f"  No collisions detected.")

# Actually wait - ERTEIN appears inside GOTTDIENER!
# GOTTDIENER = G-O-T-T-D-I-E-N-E-R. Does it contain ERTEIN?
# Let me check: DIENERTEIN? No. GOTTDIENER doesn't contain ERTEIN.
# But after anagram resolution, EDETOTNIURG -> GOTTDIENER.
# So in the resolved text, GOTTDIENER is there. Does GOTTDIENER contain ERTEIN?
# G-O-T-T-D-I-E-N-E-R: no ERTEIN substring.
print(f"\n  GOTTDIENER contains ERTEIN? {'ERTEIN' in 'GOTTDIENER'}")
print(f"  GOTTDIENERS contains ERTEIN? {'ERTEIN' in 'GOTTDIENERS'}")

# Check the broader context: what comes before and after ERTEIN?
# "DIES ER {T} EIN ER SEIN GOTTDIENER" -> "DIES ERTEIN ER SEIN GOTTDIENER"
# If replaced: "DIES REITEN ER SEIN GOTTDIENER" = "this ride/riding his God's Servant"
# Hmm, REITEN doesn't make great narrative sense here.
# But the pattern is "DIES ER {T} EIN ER" = "this he [T] one/a he"
# Actually in German: "dies er tut, ein er sein Gottdiener" = "this he does, a/one his God's servant"
# Wait - the {T} might actually be TUT split differently!
# Let me reconsider: DIES ER T EIN -> "dies er t ein"
# If T = tut (does), context = "dies er tut, einer sein Gottdiener"
# But we already have TUT from TTU replacement in other places.
# Here the T is a single garbled letter, code 78.
# What if we ignore ERTEIN and look at the T differently?

print(f"\n  Context analysis: 'DIES ER {{T}} EIN ER SEIN GOTTDIENER'")
print(f"  German reading: 'dies er [tut] ein er sein Gottdiener'")
print(f"  = 'this he does, one/a, he [is] God's servant'")
print(f"  The {{T}} is likely a single garbled letter, not part of ERTEIN")
print(f"  ERTEIN->REITEN would break the narrative structure")

print(f"\nDone.")
