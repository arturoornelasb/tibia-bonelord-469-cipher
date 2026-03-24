#!/usr/bin/env python3
"""
Session 21 Part 3: Test concrete coverage improvements.

Confirmed fix:
1. HEDDEMI -> HEIME (fix dead code HEDEMI entry, 11x, +2 anagram pattern)

Testing:
2. UNE -> NEU exact anagram (can't do global replace due to RUNE collision)
3. RUI -> handle contextually (SCHAUN RUI IN pattern)
4. Single-letter blocks: are any real MHG particles?
5. New MHG words to add to KNOWN
"""

import json, os, re
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

# ================================================================
# TEST 1: HEDDEMI -> HEIME fix
# ================================================================
print("=" * 80)
print("TEST 1: HEDDEMI -> HEIME (fix dead anagram entry)")
print("=" * 80)

# Current: HEDEMI -> HEIME (never fires, raw has HEDDEMI)
# Fix: HEDDEMI -> HEIME (fires 11x)

ANAGRAM_MAP_OLD = {
    'LABGZERAS': 'SALZBERG', 'SCHWITEIONE': 'WEICHSTEIN',
    'SCHWITEIO': 'WEICHSTEIN', 'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'EDETOTNIURG': 'GOTTDIENER', 'EDETOTNIURGS': 'GOTTDIENERS',
    'ADTHARSC': 'SCHARDT', 'TAUTR': 'TRAUT', 'EILCH': 'LEICH',
    'HEDEMI': 'HEIME',  # <-- DEAD CODE
    'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG', 'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE', 'TEIGN': 'NEIGT', 'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER', 'SODGE': 'GODES', 'SNDTEII': 'DIENST',
    'IEB': 'BEI', 'TNEDAS': 'STANDE', 'NSCHAT': 'NACHTS',
    'SANGE': 'SAGEN', 'GHNEE': 'GEHEN', 'THARSCR': 'SCHRAT',
}

ANAGRAM_MAP_NEW = dict(ANAGRAM_MAP_OLD)
del ANAGRAM_MAP_NEW['HEDEMI']  # Remove dead entry
ANAGRAM_MAP_NEW['HEDDEMI'] = 'HEIME'  # Add correct entry

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
            tokens.append(('word', word))
            if start < i - len(word):
                gap_text = text[i - len(word):i - len(word)]
            i = start
        else:
            j = i - 1
            while j > 0 and dp[j][1] is None:
                j -= 1
            tokens.append(('garbled', text[j:i]))
            i = j
    tokens.reverse()
    return tokens

def calc_coverage(anagram_map, known_set):
    total_known = 0
    total_chars = 0
    for bidx, text in enumerate(decoded_books):
        for old, new in anagram_map.items():
            text = text.replace(old, new)
        tokens = dp_segment(text)
        for ttype, tval in tokens:
            total_chars += len(tval)
            if ttype == 'word':
                total_known += len(tval)
    return total_known, total_chars

# Baseline
old_known, old_total = calc_coverage(ANAGRAM_MAP_OLD, KNOWN)
print(f"\n  Baseline (with dead HEDEMI entry):")
print(f"    {old_known}/{old_total} = {old_known/old_total*100:.1f}%")

# With HEDDEMI fix
new_known, new_total = calc_coverage(ANAGRAM_MAP_NEW, KNOWN)
print(f"\n  With HEDDEMI -> HEIME fix:")
print(f"    {new_known}/{new_total} = {new_known/new_total*100:.1f}%")
print(f"    Delta: +{new_known - old_known} known, {new_total - old_total} total chars")

# Verify: show what changes in the narrative
print(f"\n  Narrative changes (HEDDEMI -> HEIME):")
for bidx, text in enumerate(decoded_books):
    if 'HEDDEMI' in text:
        old_text = text
        for old, new in ANAGRAM_MAP_OLD.items():
            old_text = old_text.replace(old, new)

        new_text = text
        for old, new in ANAGRAM_MAP_NEW.items():
            new_text = new_text.replace(old, new)

        # Find where they differ
        idx = old_text.find('HEDDEMI')
        if idx >= 0:
            ctx_s = max(0, idx - 10)
            ctx_e = min(len(old_text), idx + 15)
            print(f"  Book {bidx}: OLD: ...{old_text[ctx_s:ctx_e]}...")

        idx2 = new_text.find('HEIME')
        if idx2 >= 0:
            # Find the HEIME that replaced HEDDEMI
            ctx_s2 = max(0, idx2 - 10)
            ctx_e2 = min(len(new_text), idx2 + 13)
            print(f"           NEW: ...{new_text[ctx_s2:ctx_e2]}...")

# ================================================================
# TEST 2: Additional KNOWN words scan
# ================================================================
print(f"\n{'=' * 80}")
print("TEST 2: SCAN FOR NEW KNOWN WORDS")
print("=" * 80)

# After HEDDEMI fix, what are the remaining garbled blocks?
# Test adding various MHG words

# Words to test adding:
TEST_WORDS = [
    # MHG particles and short words
    'LAB',   # rennet/stomach (MHG lab)
    'SIN',   # MHG: his/its (possessive)
    'ERL',   # alder tree
    'DAZ',   # MHG: that/so that (variant of das)
    'WIS',   # MHG: know! (imperative)
    'SAT',   # MHG: satiated/enough
    'HIE',   # MHG: here (variant of hier)
    'DIT',   # MHG: this
    'DAT',   # MHG: that (dialectal)
    'DIS',   # MHG: this (genitive)
    'OUZ',   # MHG: out
    'OUF',   # MHG: up
    'ERE',   # MHG: honor (variant of ehre)
    'MUO',   # MHG: must (variant)
    'ANE',   # MHG: without
    'UME',   # MHG: around
    'MAGET', # MHG: maiden/virgin
    'RISE',  # MHG: giant
    'IEMER', # MHG: always
    'NIEMEN', # MHG: no one
    'GUOT',  # MHG: good
    'TUOT',  # MHG: does
    'MUOT',  # MHG: courage/spirit
    'HUOTE', # MHG: guard
    'DIET',  # MHG: people/nation
    'DEGEN', # MHG: warrior
    'REIN',  # pure/clean
    'LEIT',  # MHG: people (Leute)
    'EIGEN', # own/property
    'STEIN', # stone (already have STEINE/STEINEN)
    'STEIN',
]

# Remove duplicates and already-known words
TEST_WORDS = [w for w in set(TEST_WORDS) if w not in KNOWN]

for word in sorted(TEST_WORDS):
    # Test impact of adding this word
    KNOWN_TEST = KNOWN | {word}
    test_known, test_total = calc_coverage(ANAGRAM_MAP_NEW, KNOWN_TEST)
    delta = test_known - new_known
    if delta > 0:
        print(f"  +{word}: +{delta} chars ({test_known}/{test_total} = {test_known/test_total*100:.1f}%)")

# ================================================================
# TEST 3: Compound anagram patterns (UNE context-specific)
# ================================================================
print(f"\n{'=' * 80}")
print("TEST 3: CONTEXT-SPECIFIC ANAGRAM PATTERNS")
print("=" * 80)

# Test UNE-related compound replacements
# SALZBERGUNE -> SALZBERGNEU? Need to check if this substring exists
test_text_sample = decoded_books[1]  # Book 1 has SALZBERG UNE NIT
for old, new in ANAGRAM_MAP_NEW.items():
    test_text_sample = test_text_sample.replace(old, new)
print(f"  Sample text (Book 1 after anagrams): ...{test_text_sample}...")

# Check if UNENITMGEHEN exists
for bidx, text in enumerate(decoded_books):
    processed = text
    for old, new in ANAGRAM_MAP_NEW.items():
        processed = processed.replace(old, new)
    if 'UNE' in processed:
        idx = processed.find('UNE')
        if idx >= 0:
            ctx = processed[max(0,idx-10):idx+15]
            # Check if it's inside RUNE/RUNEN
            before = processed[max(0,idx-1):idx]
            if before not in ['R']:  # Not part of RUNE
                print(f"  Book {bidx}: standalone UNE at: ...{ctx}...")

# ================================================================
# TEST 4: Scan for cross-boundary anagrams
# ================================================================
print(f"\n{'=' * 80}")
print("TEST 4: CROSS-BOUNDARY ANAGRAM SCAN")
print("=" * 80)

# Some garbled blocks might form words when combined with adjacent known words
# E.g., {SD} + IM = SDIM -> MIDS? No...
# {ND} + TER = NDTER -> ?
# ER + {L} + AB = ERLAB or ELAB or LAB

# Let me check if AB appears right after {L} consistently
# Pattern: "ER L AB" -> what if L+AB = LAB (MHG: refresh/rennet)?
# LAB is a real MHG word! Let me test adding it.

KNOWN_TEST2 = KNOWN | {'LAB'}
test_known2, test_total2 = calc_coverage(ANAGRAM_MAP_NEW, KNOWN_TEST2)
delta2 = test_known2 - new_known
print(f"  Adding LAB: delta = {delta2}")

# What about RUIN as a word variant?
# {RUI} appears 7x in "SCHAUN RUI IN"
# What if RUIIN gets found? Or if we handle RUI differently?
# Actually RUIN is already in KNOWN. The issue is the text has RUI not RUIN.
# RUI is 3 chars. What if we add RUI as a variant/word?
# RUI isn't a real German word though.

# Test: what if RUI is an exact anagram? RUI -> IRU? UIR? No, these aren't words.
# What about: RUIINWISTEN... could RUIIN be a word?
# No. The text is "SCHAUNRUIINWISTEN..." and DP finds SCHAUN+{RUI}+IN+WISTEN
# {RUI} is stuck as garbled.

# ================================================================
# TEST 5: Broader MHG word scan with impact measurement
# ================================================================
print(f"\n{'=' * 80}")
print("TEST 5: BROAD MHG WORD SCAN")
print("=" * 80)

# Extended list of MHG and early NHG words to try
BROAD_WORDS = [
    # 2-letter
    'OD', 'OU', 'HI', 'MI', 'WE', 'GE', 'RE', 'EI', 'HE', 'IR',
    'OR', 'TU', 'AU', 'UR',
    # 3-letter
    'LAB', 'SIN', 'ERL', 'HIE', 'MUO', 'ANE', 'UME', 'ZIT',
    'BOT', 'GAB', 'SAH', 'LAS', 'NAM', 'BAT', 'RIT',
    'WOL', 'MER', 'DAR', 'SOL', 'MOT', 'LOS', 'ROT',
    'GIE', 'VIL', 'ZUO', 'LIE', 'HIR', 'TIR', 'KUR',
    'HEL', 'REI', 'LEI', 'SEL', 'WEL', 'FEL', 'GEL',
    'TEL', 'BEL', 'MEL', 'NEL', 'DEL', 'OLE', 'ULE',
    # 4-letter
    'DIET', 'REIN', 'LEIT', 'DEIN', 'MEIN', 'KEIN', 'FEIN',
    'RIET', 'LIED', 'BEIN', 'WEIS', 'REIS', 'RITT', 'SITZ',
    'MILD', 'MUOT', 'TUOT', 'GUOT', 'SITE', 'RITE', 'HIRN',
    'HIRT', 'HULD', 'GELT', 'LANT', 'GERN', 'OBEN', 'SEIT',
    'MORD', 'WUND', 'RUFT', 'DANK', 'DREH', 'LEHN', 'ZAHL',
    'NAHT', 'SINN', 'BALD', 'GENS', 'IREN', 'NEIN',
    # 5-letter
    'DEGEN', 'EIGEN', 'ENGEL', 'ERDEN', 'ERNST', 'GREIS',
    'HEIDE', 'KLAGE', 'LEGEN', 'LEUTE', 'MINNE', 'SEELE',
    'SORGE', 'STOLZ', 'WACHE', 'WILLE', 'WUNDE',
    'DIENE', 'REDET', 'SENDE', 'WENDE',
    # 6-letter
    'LIEDER', 'MEINER', 'SEINER', 'DEINER', 'KEINER',
    'UNSERE', 'KINDER', 'LEIDER', 'LIEBEN', 'STEHEN',
    'HERZEN', 'DULDEN', 'SENDEN', 'STERBE',
]

BROAD_WORDS = [w for w in set(BROAD_WORDS) if w not in KNOWN]

print(f"  Testing {len(BROAD_WORDS)} additional words...")
gains = []
for word in sorted(BROAD_WORDS):
    KNOWN_TEST = KNOWN | {word}
    test_known, test_total = calc_coverage(ANAGRAM_MAP_NEW, KNOWN_TEST)
    delta = test_known - new_known
    if delta > 0:
        gains.append((word, delta, test_known, test_total))

gains.sort(key=lambda x: -x[1])
for word, delta, tk, tt in gains:
    print(f"  +{word}: +{delta} chars ({tk}/{tt} = {tk/tt*100:.1f}%)")

# ================================================================
# TEST 6: Cumulative test
# ================================================================
print(f"\n{'=' * 80}")
print("TEST 6: CUMULATIVE IMPACT")
print("=" * 80)

# Add all gains >= 3 chars
good_words = [word for word, delta, _, _ in gains if delta >= 3]
print(f"  Words with >= 3 char gain: {good_words}")

if good_words:
    KNOWN_CUMUL = KNOWN | set(good_words)
    cum_known, cum_total = calc_coverage(ANAGRAM_MAP_NEW, KNOWN_CUMUL)
    print(f"\n  HEDDEMI fix + new words:")
    print(f"    {cum_known}/{cum_total} = {cum_known/cum_total*100:.1f}%")
    print(f"    vs baseline {old_known}/{old_total} = {old_known/old_total*100:.1f}%")
    print(f"    Total gain: +{cum_known - old_known} known, {cum_total - old_total} total chars")

# ================================================================
# TEST 7: What does the narrative look like after fixes?
# ================================================================
print(f"\n{'=' * 80}")
print("TEST 7: SAMPLE NARRATIVE AFTER ALL FIXES")
print("=" * 80)

if good_words:
    FINAL_KNOWN = KNOWN | set(good_words)
else:
    FINAL_KNOWN = KNOWN

FINAL_MAP = ANAGRAM_MAP_NEW

# Show a few books with the new segmentation
for bidx in [5, 9, 17, 33, 45]:
    if bidx >= len(decoded_books):
        continue
    text = decoded_books[bidx]
    for old, new in FINAL_MAP.items():
        text = text.replace(old, new)
    tokens = dp_segment(text)

    parts = []
    for ttype, tval in tokens:
        if ttype == 'word':
            parts.append(tval)
        else:
            parts.append('{' + tval + '}')
    segmented = ' '.join(parts)

    total_c = sum(len(v) for _, v in tokens)
    known_c = sum(len(v) for t, v in tokens if t == 'word')
    pct = known_c / total_c * 100 if total_c > 0 else 0
    print(f"\n  Book {bidx} ({pct:.0f}%):")
    print(f"    {segmented}")

print(f"\nDone.")
