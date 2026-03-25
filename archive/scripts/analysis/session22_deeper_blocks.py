#!/usr/bin/env python3
"""
Session 22 Part 2: Deeper investigation of remaining garbled blocks.

Focus:
1. UNE standalone vs inside RUNE/RUNEN
2. ENG standalone vs inside words
3. NDCE pattern (DEN+C?)
4. HISS, EOR, TEI patterns
5. {DE} between SEINE and TOT (20x)
6. {S} IN pattern (12x)
"""

import json, os
from collections import Counter
from itertools import permutations

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

processed = ''.join(decoded_books)
for old in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    processed = processed.replace(old, ANAGRAM_MAP[old])

# ================================================================
# 1. UNE: is it ever standalone (not inside RUNE/RUNEN)?
# ================================================================
print("=" * 60)
print("1. UNE occurrences - standalone vs inside RUNE/RUNEN")
print("=" * 60)

pos = 0
une_standalone = 0
une_inside = 0
while True:
    idx = processed.find('UNE', pos)
    if idx < 0: break
    ctx = processed[max(0,idx-6):idx+9]
    # Check if inside RUNE or RUNEN
    in_rune = False
    if idx >= 1 and processed[idx-1:idx+3] == 'RUNE':
        in_rune = True
    if idx >= 1 and processed[idx-1:idx+4] == 'RUNEN':
        in_rune = True
    if in_rune:
        une_inside += 1
        print(f"  INSIDE RUNE: pos {idx}: ...{ctx}...")
    else:
        une_standalone += 1
        print(f"  STANDALONE:  pos {idx}: ...{ctx}...")
    pos = idx + 1

print(f"\n  Standalone UNE: {une_standalone}")
print(f"  Inside RUNE/RUNEN: {une_inside}")
print(f"  If standalone > 0, could selectively replace only non-RUNE contexts")

# ================================================================
# 2. ENG: standalone vs inside words
# ================================================================
print(f"\n{'='*60}")
print("2. ENG occurrences - contexts")
print(f"{'='*60}")

pos = 0
eng_count = 0
while True:
    idx = processed.find('ENG', pos)
    if idx < 0: break
    eng_count += 1
    ctx = processed[max(0,idx-10):idx+13]
    # Check if inside ENGE
    in_enge = processed[idx:idx+4] == 'ENGE'
    label = "INSIDE ENGE" if in_enge else "STANDALONE"
    print(f"  {label}: pos {idx}: ...{ctx}...")
    pos = idx + 1
print(f"  Total: {eng_count} (most likely inside ENGE)")

# ================================================================
# 3. {DE} pattern - SEINE {DE} TOT
# ================================================================
print(f"\n{'='*60}")
print("3. {DE} pattern analysis")
print(f"{'='*60}")

# Find all places where DE appears as garbled
# In the DP output, {DE} appears between SEINE and TOT
# Context: "SEINE {DE} TOT" - could this be SEINEDETOT?
# SEINEDETOT -> SEINE DE TOT -> "his the dead"
# Or: SEINED+ETOT? Or: SEINEN + DETOT?

# Check: does SEINEN appear if we merge SEINE+D?
# SEINE is known, D is garbled. So the DP sees SEINE + {DE} + TOT
# What if SEINEDETOT has a different segmentation?
# SEINED = not a word
# SEINEDE = not a word
# But what about: SEINER + DETOT? No, SEINER would need R.
# What about DE alone: "of the" in German (from/of)
# "SEINE DE TOT" = "his of-the dead" - not great German
# "SEINED E TOT" = not a word

# More likely: the D is garbled and E belongs to something else
# Let's check the full context
pos = 0
while True:
    idx = processed.find('SEINEDETOT', pos)
    if idx < 0: break
    ctx = processed[max(0,idx-5):idx+25]
    print(f"  SEINEDETOT at {idx}: ...{ctx}...")
    # What comes after TOT?
    after = processed[idx+10:idx+20]
    print(f"    After: '{after}'")
    pos = idx + 1

# Alternative: what about SEINEN + D + E + TOT?
# SEINEN is a known word!
pos = 0
print(f"\n  Checking SEINEN match:")
while True:
    idx = processed.find('SEINEN', pos)
    if idx < 0: break
    ctx = processed[max(0,idx-5):idx+20]
    print(f"    pos {idx}: ...{ctx}...")
    pos = idx + 1

# ================================================================
# 4. The {S} IN pattern
# ================================================================
print(f"\n{'='*60}")
print("4. {S} IN pattern")
print(f"{'='*60}")

# Context: "ES {S} IN" - the S is a single garbled letter
# Could this be: ESSIN? ESSIN sorted = EINSS
# SINNE (senses/mind)? No, different letters.
# What about SEIN? ES SEIN = "it [to] be"?
# But SEIN is already matched. The issue is the garbled S.
# Looking at it: E-S-S-I-N -> DP matches ES(2) + {S}(garbled) + IN(2)
# Alternative: ESSIN = not a word
# What if it's ESSEN (to eat)? E-S-S-E-N sorted EENSS ≠ EINSS
# No.

# What about SIND? ES + S + IN + D? Or ES SIND (they are)?
# Check if SINД follows: ES S IN -> ES SIND?
pos = 0
print("  Checking 'ESSIN' contexts:")
while True:
    idx = processed.find('ESSIN', pos)
    if idx < 0: break
    ctx = processed[max(0,idx-5):idx+15]
    print(f"    pos {idx}: ...{ctx}...")
    after = processed[idx+5:idx+10]
    # Check if next is D -> ESSIND
    if after and after[0] in 'DE':
        print(f"      -> Could be ES SIND {'(they are)' if after[0]=='D' else ''}")
    pos = idx + 1

# ================================================================
# 5. What about {OE} -> OE is valid German (Ö)
# ================================================================
print(f"\n{'='*60}")
print("5. {OE} pattern - could be standalone Ö-word fragment")
print(f"{'='*60}")

pos = 0
oe_count = 0
while True:
    idx = processed.find('OE', pos)
    if idx < 0: break
    # Skip if inside OEL (already known)
    if processed[idx:idx+3] == 'OEL':
        pos = idx + 1
        continue
    oe_count += 1
    ctx = processed[max(0,idx-8):idx+10]
    if oe_count <= 15:
        print(f"  #{oe_count} pos {idx}: ...{ctx}...")
    pos = idx + 1

# ================================================================
# 6. The repeating NLNDEF block
# ================================================================
print(f"\n{'='*60}")
print("6. NLNDEF pattern (would be FINDEN if L=I)")
print(f"{'='*60}")

pos = 0
while True:
    idx = processed.find('NLNDEF', pos)
    if idx < 0: break
    ctx = processed[max(0,idx-10):idx+16]
    print(f"  pos {idx}: ...{ctx}...")
    pos = idx + 1

# Check: "DU NLNDEF SAGEN" -> "DU FINDEN SAGEN" = "you find legends"
# If NLNDEF = FINDEN with L->I swap, every L position would use code 96
# But code 96 is confirmed L. Unless there's a special context.
# What if NLNDEF is an anagram? Sorted: DEFLNN
# 6-letter words from DEFLNN: FINDEN? F-I-N-D-E-N sorted = DEFINN ≠ DEFLNN
# The L ≠ I. DEFLNN has L, DEFINN has I. So it's NOT an anagram of FINDEN.
# NLNDEF sorted = DEFLNN. What word has letters D,E,F,L,N,N?
# FLNDEN? FLENDN? None are German words.

# What if it's a +1 anagram? NLNDEF (6 chars) = some 5-char word + extra letter
# Remove each: LNDEF, NNDEF, NLNEF, NLNDF, NLNDE
# LNDEF sorted = DEFLN
# NNDEF sorted = DEFNN -> FINDEN without I? no
# None match German words easily

print(f"\n  NLNDEF sorted: {''.join(sorted('NLNDEF'))}")
print(f"  FINDEN sorted: {''.join(sorted('FINDEN'))}")
print(f"  Difference: L vs I - confirmed code 96=L, so NOT an anagram of FINDEN")

# ================================================================
# 7. Look at raw codes for {T} in ER{T}EIN pattern
# ================================================================
print(f"\n{'='*60}")
print("7. Raw codes analysis for single-letter garbled blocks")
print(f"{'='*60}")

# Build code-level view
all_pairs = []
for bpairs in book_pairs:
    all_pairs.extend(bpairs)

all_decoded = ''.join(v7.get(p, '?') for p in all_pairs)

# Find code for {T} in context ERTEIN
# After anagram resolution, ERTEIN appears. In raw decoded text, what codes produce T?
t_codes = set()
for i, p in enumerate(all_pairs):
    if v7.get(p) == 'T':
        t_codes.add(p)

print(f"  All T codes: {sorted(t_codes)}")

# Now find the specific T codes that appear as garbled {T}
# In the DP output, {T} appears in "ER {T} EIN" context
# The raw decoded text has "...SERTEINERSEIN..." where the T is single-garbled
# Find all ERTEIN in raw decoded (before anagram resolution)
# Actually, after anagram resolution the text changes. Let me find in processed text.

# Count each T code in garbled vs known context
# First, map each position in processed text back to its code
# This is complex because anagram replacements change positions.
# Let me instead count T codes in known words vs garbled:

# Build raw decoded text (no anagram) and segment it
raw_decoded = ''.join(decoded_books)
# Apply anagrams to get processed
proc = raw_decoded
for old in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    proc = proc.replace(old, ANAGRAM_MAP[old])

# Find which T code is at position of garbled T
# Simpler approach: just count T codes overall
t_code_counts = Counter()
for p in all_pairs:
    if v7.get(p) == 'T':
        t_code_counts[p] += 1

print(f"  T code frequencies:")
for code, count in t_code_counts.most_common():
    print(f"    code {code}: {count}x")

# ================================================================
# 8. Look for SEIT (since) and WEG (way/path)
# ================================================================
print(f"\n{'='*60}")
print("8. Checking for missing common German words")
print(f"{'='*60}")

common_missing = [
    'SEIT', 'WEG', 'WEGE', 'IHR', 'MIR', 'DIR', 'IHN', 'IHM',
    'AUS', 'UBER', 'OHNE', 'GEGEN', 'NEBEN', 'VOM', 'JEDER',
    'VOLK', 'HELD', 'NEBEN', 'TRUG', 'SCHWERT', 'MACHT',
    'FEUER', 'WASSER', 'LUFT', 'LIED', 'SANG', 'BLUT',
    'FLEISCH', 'BEIN', 'SEELE', 'GEBET', 'ALTAR', 'TEMPEL',
    'PRIESTER', 'OPFER', 'HEILIG', 'DUNKEL', 'LICHT',
    'GRABEN', 'HOEHLE', 'TIEFE', 'OBEN', 'UNTEN',
    'SKELETT', 'KNOCHEN', 'SCHAEDEL', 'AUGE', 'AUGEN',
    'DEMON', 'DAEMON', 'GEIST', 'FLUCH', 'BANN',
    'BESCHWOR', 'RITUAL', 'ZAUBER', 'SPRUCH',
]

for word in common_missing:
    count = proc.count(word)
    if count > 0:
        print(f"  {word}: {count}x")
        # Show first context
        idx = proc.find(word)
        ctx = proc[max(0,idx-8):idx+len(word)+8]
        print(f"    context: ...{ctx}...")

# ================================================================
# 9. What about the {ADTHA} fragment?
# ================================================================
print(f"\n{'='*60}")
print("9. ADTHA fragment (appears where SCHARDT expected)")
print(f"{'='*60}")

pos = 0
while True:
    idx = processed.find('ADTHA', pos)
    if idx < 0: break
    ctx = processed[max(0,idx-10):idx+20]
    print(f"  pos {idx}: ...{ctx}...")
    pos = idx + 1

# ADTHARSC -> SCHARDT. But ADTHA appears alone sometimes.
# ADTHA sorted = AADHT. Is this SCHARDT truncated?
# Or is ADTHA + next chars = ADTHARSC?
# Check what follows ADTHA
pos = 0
while True:
    idx = processed.find('ADTHA', pos)
    if idx < 0: break
    after = processed[idx+5:idx+10]
    print(f"  After ADTHA: '{after}'")
    # If next chars are RSC, it would be ADTHARSC -> SCHARDT
    # But the anagram replacement should have caught ADTHARSC already
    pos = idx + 1

# It seems ADTHARSC is sometimes truncated to ADTHA
# This could mean the book boundary cuts in the middle
print(f"\n  ADTHA sorted: {''.join(sorted('ADTHA'))}")
print(f"  SCHARDT minus RSC: ADTHA = first 5 chars of ADTHARSC")
print(f"  This is likely SCHARDT with the RSC part in next book or garbled")

# ================================================================
# 10. The {MISE} pattern and other 4-char blocks
# ================================================================
print(f"\n{'='*60}")
print("10. Unique 4-char garbled blocks analysis")
print(f"{'='*60}")

# Get DP segments
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

# Check all 4-5 char garbled blocks for German word anagrams
german_words_4_5 = [
    'ACHT', 'BALD', 'BEIM', 'BLUT', 'BROT', 'BURG', 'DANK', 'DEIN',
    'EILE', 'FELD', 'FELS', 'FEST', 'FORM', 'FREI', 'GABE', 'GAST',
    'GEHT', 'GELD', 'GIER', 'GIFT', 'GLAS', 'GNAD', 'GRAM', 'GRAS',
    'GRAU', 'HAUS', 'HEER', 'HILF', 'HOLZ', 'HORN', 'HUET', 'IRRE',
    'KERN', 'KLUG', 'KNIE', 'KOPF', 'LAGE', 'LEER', 'LEID', 'LEIS',
    'LIST', 'LOHN', 'LUFT', 'LUST', 'MAID', 'MASS', 'MILCH', 'MILD',
    'MOND', 'MORD', 'MUET', 'NAHT', 'NARR', 'NEID', 'NEST', 'NIMM',
    'OBEN', 'PEIN', 'PFAD', 'QUAL', 'RAUB', 'RAST', 'RAUM', 'RECHT',
    'REIF', 'REIN', 'REST', 'RING', 'ROSS', 'RUHE', 'RUHM', 'SAGE',
    'SARG', 'SATT', 'SEIL', 'SEHN', 'SINN', 'SPUR', 'STAB', 'TANZ',
    'TIEF', 'TIER', 'TORE', 'TURM', 'WACH', 'WAHN', 'WEIN', 'WEISE',
    'WERK', 'WURM', 'ZAHL', 'ZAUN', 'ZIEL',
    # MHG additions
    'MINNE', 'MUOT', 'GUOT', 'VROUWE', 'RITTER', 'SWERT', 'STRIT',
    'HERRE', 'LANT', 'DINC', 'WORT', 'BEIN', 'LEIP', 'SELE',
    'TUGENT', 'TRIUWE', 'HULDE', 'GEWALT', 'ORDEN', 'GEBOT',
]

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

# Extract garbled blocks of size 4-5
garbled_45 = Counter()
for t in tokens:
    if t.startswith('{'):
        block = t[1:-1]
        if 4 <= len(block) <= 5:
            garbled_45[block] += 1

print(f"\n  4-5 char garbled blocks (checking against German word list):")
for block, count in sorted(garbled_45.items(), key=lambda x: -x[1]):
    if count < 1: continue
    sorted_block = ''.join(sorted(block))
    # Check exact anagram against word list
    matches = []
    for word in german_words_4_5:
        if ''.join(sorted(word)) == sorted_block:
            matches.append(word)
    # Also check against KNOWN set
    for word in KNOWN:
        if len(word) == len(block) and ''.join(sorted(word)) == sorted_block:
            if word not in matches:
                matches.append(word)
    if matches:
        print(f"  {block:8s} {count}x -> ANAGRAM OF: {matches}")
    elif count >= 2:
        print(f"  {block:8s} {count}x (sorted: {sorted_block}) - no match")

# ================================================================
# 11. Look for SEINEDETOT -> SEINEN + DE + TOT or SEINE + DETOT
# ================================================================
print(f"\n{'='*60}")
print("11. SEINEDETOT deep analysis")
print(f"{'='*60}")

# The DP currently segments as: SEINE {DE} TOT
# What if D belongs to SAND or other words?
# What if E belongs to the next word?
# Actually, let's check: what are ALL the suffixes after SEINE in the text?
pos = 0
print("  All SEINE+next contexts:")
while True:
    idx = processed.find('SEINE', pos)
    if idx < 0: break
    after = processed[idx+5:idx+15]
    # Check it's not SEINEN
    if idx + 5 < len(processed) and processed[idx+5] == 'N':
        pos = idx + 1
        continue  # This is SEINEN, skip
    print(f"    pos {idx}: SEINE + '{after}'")
    pos = idx + 1

print(f"\nDone.")
