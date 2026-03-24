#!/usr/bin/env python3
"""
Session 19: Cross-boundary anagram application and systematic garbled block attack.

Key discovery from S18: TNEDAS = STANDE (MHG subjunctive of 'stan')
The DP segments this as {TNE} DAS, but the real word spans the boundary.

Strategy:
1. Verify TNEDAS in raw text, apply as anagram
2. Systematically scan ALL garbled+word boundaries for hidden anagrams
3. Attack remaining garbled blocks with context-aware MHG matching
4. Measure coverage impact of each change
"""

import json, os, re
from collections import Counter, defaultdict
from itertools import combinations

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

# Digit insertion table
DIGIT_SPLITS = {
    2: (45, '1'),    5: (265, '1'),   6: (12, '0'),    8: (137, '7'),
    10: (169, '0'),  11: (137, '0'),  12: (56, '1'),   13: (45, '0'),
    14: (98, '1'),   15: (98, '0'),   18: (4, '0'),    19: (52, '0'),
    20: (5, '1'),    22: (7, '1'),    23: (22, '4'),   24: (87, '8'),
    25: (0, '0'),    29: (53, '0'),   32: (137, '1'),  34: (101, '0'),
    36: (78, '0'),   39: (44, '0'),   42: (91, '2'),   43: (122, '0'),
    45: (15, '0'),   46: (0, '2'),    48: (126, '0'),  49: (97, '1'),
    50: (16, '6'),   52: (1, '0'),    53: (257, '1'),  54: (49, '1'),
    60: (73, '9'),   61: (93, '7'),   64: (60, '0'),   65: (114, '2'),
    68: (54, '0'),
}

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

# Decode all books
book_pairs = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        split_pos, digit = DIGIT_SPLITS[bidx]
        book = book[:split_pos] + digit + book[split_pos:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

decoded_books = []
for bpairs in book_pairs:
    text = ''.join(v7.get(p, '?') for p in bpairs)
    decoded_books.append(text)

all_text = ''.join(decoded_books)

# Current anagram map
ANAGRAM_MAP = {
    'LABGZERAS': 'SALZBERG',
    'SCHWITEIONE': 'WEICHSTEIN',
    'SCHWITEIO': 'WEICHSTEIN',
    'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'EDETOTNIURG': 'GOTTDIENER',
    'EDETOTNIURGS': 'GOTTDIENERS',
    'ADTHARSC': 'SCHARDT',
    'TAUTR': 'TRAUT',
    'EILCH': 'LEICH',
    'HEDEMI': 'HEIME',
    'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG',
    'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE',
    'TEIGN': 'NEIGT',
    'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER',
    'SODGE': 'GODES',
    'SNDTEII': 'DIENST',
    'IEB': 'BEI',
}

def sorted_letters(s):
    return ''.join(sorted(s))

# ================================================================
# 1. VERIFY TNEDAS IN RAW TEXT
# ================================================================
print("=" * 80)
print("1. TNEDAS -> STANDE CROSS-BOUNDARY VERIFICATION")
print("=" * 80)

# Apply current anagrams first
resolved = all_text
for anag in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved = resolved.replace(anag, ANAGRAM_MAP[anag])

# Find TNEDAS in resolved text
count_tnedas = resolved.count('TNEDAS')
print(f"\n  'TNEDAS' in resolved text: {count_tnedas} occurrences")

# Also find 'TNE' near 'DAS'
# Show context around each TNEDAS
for i in range(len(resolved)):
    if resolved[i:i+6] == 'TNEDAS':
        start = max(0, i-20)
        end = min(len(resolved), i+26)
        context = resolved[start:end]
        pos_marker = ' ' * (i - start) + '^^^^^^'
        print(f"\n  ...{context}...")
        print(f"     {pos_marker}")

# Also check: TNED alone (appears in "ALS TNED ENDE")
count_tned = resolved.count('TNED')
print(f"\n  'TNED' in resolved text: {count_tned} occurrences")
for i in range(len(resolved)):
    if resolved[i:i+4] == 'TNED':
        start = max(0, i-15)
        end = min(len(resolved), i+20)
        context = resolved[start:end]
        print(f"    ...{context}...")

# Check: STANDE sorted = ADENST, TNEDAS sorted = ADENST
print(f"\n  TNEDAS sorted: {sorted_letters('TNEDAS')}")
print(f"  STANDE sorted: {sorted_letters('STANDE')}")
print(f"  Match: {sorted_letters('TNEDAS') == sorted_letters('STANDE')}")

# What about TNED? Is it part of STANDE minus AS?
# TNED sorted = DENT. Not a great word.
# But TNED appears in "ALS TNED ENDE" - could this be "ALS STANDE ENDE"
# with the last two letters absorbed by ENDE? No - TNED only has 4 letters.
# TNEDE = TNED + E from ENDE = 5 letters = DENET? TENDE? EENDT?
# STENDE? No, that's 6 letters. TNED is only 4.
# Actually: TNED + E (first char of ENDE) = TNEDE = sorted DEENT
# TENDE sorted = DEENT. Is TENDE a word? No standard German.
# What about just TNED = DENT? TEND? Not MHG.
# Let's check TNEDENDE = TNED + ENDE = 8 letters
tnedende = 'TNEDENDE'
print(f"\n  TNEDENDE (TNED+ENDE) sorted: {sorted_letters(tnedende)}")
# DDEENNTT? ENTDENDE? STENDENDE? Nope, too many letters.
# Actually TNEDENDE has letters: D,D,E,E,N,N,T,T (wait no)
# T,N,E,D,E,N,D,E = D,D,E,E,E,N,N,T
print(f"  Letters: {dict(Counter(tnedende))}")

# ================================================================
# 2. SYSTEMATIC CROSS-BOUNDARY SCAN
# ================================================================
print(f"\n{'=' * 80}")
print("2. SYSTEMATIC CROSS-BOUNDARY ANAGRAM SCAN")
print("=" * 80)

# Build comprehensive word list for matching
KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR', 'NU',
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
    'OEL', 'SCE', 'MINNE', 'MIN',
    'ODE', 'SER', 'GEN', 'INS',
    'GEIGET', 'BERUCHTIG', 'BERUCHTIGER',
    'MEERE', 'NEIGT', 'WISTEN', 'MANIER', 'HUND',
    'GODE', 'GODES', 'EIGENTUM', 'REDER',
    'THENAEUT', 'LABT', 'MORT', 'DIGE', 'WEGE',
    'KOENIGS', 'NAHE', 'NOT', 'NOTH', 'ZUR', 'OWI',
    'ENGE', 'SEIDEN', 'ALTES', 'DENN', 'BIS', 'NIE',
    'NUT', 'NUTZ', 'HEIL', 'NEID', 'TREU', 'TREUE',
    'SUN', 'DIENST', 'SANG', 'DINC', 'HULDE', 'NACH',
    'STEINE', 'LANT', 'HERRE', 'DIENEST',
    'GEBOT', 'SCHWUR', 'ORDEN', 'RICHTER', 'DUNKEL',
    'EHRE', 'EDELE', 'SCHULD', 'SEGEN', 'FLUCH', 'RACHE',
    'KOENIG', 'DASS', 'EDEL', 'ADEL',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME',
    'SCHARDT',
])

# MHG extended word list for anagram matching
MHG_EXTENDED = set([
    'STANDE', 'STUONT', 'GESINDE', 'VROUWE', 'RITTER', 'MEISTER',
    'TUGENT', 'TRIUWE', 'MINNEN', 'HERZEN', 'LIEBE', 'VREUDE',
    'SWAERE', 'KUMBER', 'LEIDEN', 'SCHULDE', 'HEILEC', 'GENADE',
    'GEWALT', 'FRIEDE', 'WUNDER', 'ZEICHEN', 'STIMME', 'GESANG',
    'KLAGE', 'GEBET', 'SCHATTEN', 'FINSTER', 'BLEICH',
    'HEILIG', 'VERLOREN', 'NORDEN', 'SUEDEN', 'WESTEN', 'OSTEN',
    'QUELLE', 'GRUND', 'TIEFE', 'GRENZE', 'SCHWELLE',
    'GEBEIN', 'LEICHE', 'ASCHE', 'STAUB', 'OPFER', 'GABE',
    'UNTOT', 'UNTOTE', 'UNTOTEN', 'ZAUBER', 'RITUAL',
    'INSCHRIFT', 'ORAKEL', 'PORTAL', 'KAMMER', 'KRYPTA',
    'DRUIDE', 'DIENER', 'WACHTER', 'HERRSCHER',
    'BRUDER', 'SCHWESTER', 'TOCHTER', 'MUTTER', 'VATER',
    'DUNKEL', 'STERBEN', 'STRAZE',
    # Common MHG verbs/forms
    'MOHTE', 'SOLDE', 'WOLDE', 'WOLTE', 'KUNDE', 'DORFTE',
    'SPRACH', 'GESACH', 'GEBOT', 'GESCHACH',
    'STUNDE', 'STUNDEN', 'STANDEN',
    # Additional MHG nouns
    'KIRCHE', 'KLOSTER', 'TEMPEL', 'ALTAR', 'THRON',
    'LINDE', 'EICHE', 'BIRKE', 'TANNE',
    'FLUSS', 'STROM', 'BRUECKE', 'BRUCKE',
    'TURNIER', 'SCHILD', 'SCHWERT', 'LANZE',
    'KNECHT', 'BAUER', 'BUERGER', 'FUERST', 'GRAF',
    'STERNE', 'FEUER', 'WASSER', 'LUFT',
    'KREUZ', 'KETTE', 'RING', 'KRONE',
    'NACHT', 'MORGEN', 'ABEND', 'MITTAG',
    # Place-name elements
    'BURG', 'BERG', 'STEIN', 'WALD', 'FELD', 'BRUNN', 'DORF',
    'HEIM', 'HAUSEN', 'KIRCH', 'MUEHLE', 'TURM',
    'LUTHER', 'RUNTHE', 'RUTHE', 'TURNHEL', 'HILDEN',
    'LINDEN', 'BRUNNEN', 'THURNE', 'THURM',
])

ALL_WORDS = KNOWN | MHG_EXTENDED

# Build anagram index
anagram_idx = defaultdict(list)
for w in ALL_WORDS:
    anagram_idx[sorted_letters(w)].append(w)

# DP segmentation
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

# Find all garbled-word boundaries in segmented text
tokens, _ = dp_segment(resolved)

print("\n  Scanning all garbled+known word boundaries for hidden anagrams...")
print("  (looking for cases where garbled{X} + WORD or WORD + garbled{X}")
print("   forms a valid anagram of a known MHG word)")

boundary_hits = []
for i in range(len(tokens) - 1):
    t1, t2 = tokens[i], tokens[i+1]

    # Case 1: garbled + known word
    if t1.startswith('{') and not t2.startswith('{'):
        garbled = t1[1:-1]  # strip braces
        combined = garbled + t2
        key = sorted_letters(combined)
        for m in anagram_idx.get(key, []):
            if m != t2:  # don't match the word itself
                boundary_hits.append((i, f"{t1} {t2}", combined, 'exact', m))
        # +1 pattern
        for ci in range(len(combined)):
            reduced = combined[:ci] + combined[ci+1:]
            k = sorted_letters(reduced)
            for m in anagram_idx.get(k, []):
                if len(m) >= 4 and m != t2:
                    boundary_hits.append((i, f"{t1} {t2}", combined, f'+{combined[ci]}', m))

    # Case 2: known word + garbled
    if not t1.startswith('{') and t2.startswith('{'):
        garbled = t2[1:-1]
        combined = t1 + garbled
        key = sorted_letters(combined)
        for m in anagram_idx.get(key, []):
            if m != t1:
                boundary_hits.append((i, f"{t1} {t2}", combined, 'exact', m))
        # +1 pattern
        for ci in range(len(combined)):
            reduced = combined[:ci] + combined[ci+1:]
            k = sorted_letters(reduced)
            for m in anagram_idx.get(k, []):
                if len(m) >= 4 and m != t1:
                    boundary_hits.append((i, f"{t1} {t2}", combined, f'+{combined[ci]}', m))

    # Case 3: garbled + known word + garbled (3-token span)
    if i + 2 < len(tokens):
        t3 = tokens[i+2]
        if t1.startswith('{') and not t2.startswith('{') and t3.startswith('{'):
            garbled = t1[1:-1] + t2 + t3[1:-1]
            key = sorted_letters(garbled)
            for m in anagram_idx.get(key, []):
                if len(m) >= 5:
                    boundary_hits.append((i, f"{t1} {t2} {t3}", garbled, 'exact-3span', m))

# Deduplicate and show
seen = set()
print(f"\n  Found {len(boundary_hits)} raw hits, deduplicating...")
for idx, parse, combined, pattern, match in boundary_hits:
    sig = (combined, match)
    if sig in seen:
        continue
    seen.add(sig)
    # Count occurrences
    occ = resolved.count(combined)
    if occ >= 2 or (occ >= 1 and len(match) >= 5):
        context_start = max(0, resolved.find(combined) - 10)
        context_end = min(len(resolved), resolved.find(combined) + len(combined) + 10)
        ctx = resolved[context_start:context_end]
        print(f"\n  [{pattern}] {parse}")
        print(f"    {combined} ({occ}x) -> {match}")
        print(f"    Context: ...{ctx}...")

# ================================================================
# 3. FOCUSED: What does TNEDAS resolution give us?
# ================================================================
print(f"\n{'=' * 80}")
print("3. IMPACT: TNEDAS -> STANDE")
print("=" * 80)

# Test adding TNEDAS->STANDE and STANDE to KNOWN
test_anagram = dict(ANAGRAM_MAP)
test_anagram['TNEDAS'] = 'STANDE'

test_resolved = all_text
for anag in sorted(test_anagram.keys(), key=len, reverse=True):
    test_resolved = test_resolved.replace(anag, test_anagram[anag])

test_known = set(KNOWN)
test_known.add('STANDE')

# DP with new word
def dp_count(text, wordset):
    n = len(text)
    dp = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], None)
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if cand in wordset:
                score = dp[start][0] + wlen
                if score > dp[i][0]:
                    dp[i] = (score, (start, cand))
    return dp[n][0]

baseline_cov = dp_count(resolved, KNOWN)
test_cov = dp_count(test_resolved, test_known)
total = sum(1 for c in resolved if c != '?')

print(f"  Baseline: {baseline_cov}/{total} = {baseline_cov/total*100:.1f}%")
print(f"  +STANDE:  {test_cov}/{total} = {test_cov/total*100:.1f}%")
print(f"  Delta: {test_cov - baseline_cov:+d} chars")

# Show the resolved STANDE in context
for i in range(len(test_resolved)):
    if test_resolved[i:i+6] == 'STANDE':
        start = max(0, i-20)
        end = min(len(test_resolved), i+26)
        ctx = test_resolved[start:end]
        print(f"    ...{ctx}...")

# ================================================================
# 4. TEST MORE CROSS-BOUNDARY CANDIDATES
# ================================================================
print(f"\n{'=' * 80}")
print("4. ADDITIONAL CROSS-BOUNDARY CANDIDATES")
print("=" * 80)

# From S18: RUIIN=RUIN+I, NUOD=UND+O
# Let's test each systematically

candidates = [
    # (raw_block, target_word, extra_letter, description)
    ('TNEDAS', 'STANDE', None, 'MHG subjunctive of stan - cross boundary'),
    # Check if TNED (without AS) could be something
]

# Look for all recurring short garbled blocks adjacent to known words
# that could form longer words
print("\n  Checking specific cross-boundary patterns:")

patterns_to_check = [
    # garbled, adjacent_word, combined, direction
    ('RUI', 'IN', 'RUIIN', 'garbled+word'),
    ('UOD', 'IM', 'UODIM', 'garbled+word'),
    ('HED', 'DEM', 'HEDDEM', 'garbled+word'),  # or HEDDEMI
    ('CHN', 'ES', 'CHNES', 'garbled+word'),
    ('T', 'ER', 'TER', 'garbled+word'),
    ('T', 'EIN', 'TEIN', 'garbled+word'),
    ('E', 'NOT', 'ENOT', 'garbled+word'),
    ('RRNI', 'WIR', 'RRNIWIR', 'garbled+word'),
    ('NSC', 'HAT', 'NSCHAT', 'garbled+word'),  # SCHANT? NACHTS?
    ('NDCE', 'FACH', 'NDCEFACH', 'garbled+word'),
    ('NT', 'ES', 'NTES', 'garbled+word'),
    ('HISS', 'TUN', 'HISSTUN', 'garbled+word'),
    # word + garbled
    ('ER', 'L', 'ERL', 'word+garbled'),
    ('ORTEN', 'GCHD', 'ORTENGCHD', 'word+garbled'),
    ('ODE', 'UTRUNR', 'ODEUTRUNR', 'word+garbled'),
    ('AB', 'RRNI', 'ABRRNI', 'word+garbled'),
    ('DA', 'EI', 'DAEI', 'word+garbled'),  # EIDA? AIDE? IDEE?
    ('DAS', 'E', 'DASE', 'word+garbled'),
    ('SO', 'ETE', 'SOETE', 'word+garbled'),
    ('WISTEN', 'HIER', 'WISTENTHIER', 'word+garbled+word'),  # just the garbled between
]

for p1, p2, combined, direction in patterns_to_check:
    key = sorted_letters(combined)
    matches = anagram_idx.get(key, [])
    occ = resolved.count(combined)

    # Also +1
    plus1 = []
    for ci in range(len(combined)):
        reduced = combined[:ci] + combined[ci+1:]
        k = sorted_letters(reduced)
        for m in anagram_idx.get(k, []):
            if len(m) >= 3:
                plus1.append((combined[ci], m))

    if matches or plus1:
        print(f"\n  {p1}+{p2} = {combined} ({occ}x)")
        if matches:
            print(f"    Exact: {matches}")
        for extra, m in plus1[:5]:
            print(f"    +{extra}: {m}")

# ================================================================
# 5. ATTACK: RECURRING GARBLED WITH CONTEXT
# ================================================================
print(f"\n{'=' * 80}")
print("5. CONTEXT-AWARE GARBLED BLOCK ANALYSIS")
print("=" * 80)

# For each major garbled block, look at ALL its contexts
# and try to determine identity from surrounding words

# First get the segmented tokens with positions
tokens_pos = []  # (token_text, start_pos, end_pos)
pos = 0
for t in tokens:
    if t.startswith('{'):
        tlen = len(t) - 2  # minus braces
    else:
        tlen = len(t)
    tokens_pos.append((t, pos, pos + tlen))
    pos += tlen

# Find recurring garbled blocks
garbled_blocks = Counter()
garbled_contexts = defaultdict(list)
for i, (t, s, e) in enumerate(tokens_pos):
    if t.startswith('{'):
        garbled = t[1:-1]
        garbled_blocks[garbled] += 1
        # Get context: 3 tokens before and after
        before = [tokens_pos[j][0] for j in range(max(0,i-3), i)]
        after = [tokens_pos[j][0] for j in range(i+1, min(len(tokens_pos), i+4))]
        garbled_contexts[garbled].append((' '.join(before), ' '.join(after)))

print("\n  Top garbled blocks with all contexts:")
for garbled, count in garbled_blocks.most_common(25):
    if count >= 2 and len(garbled) >= 2:
        print(f"\n  {{{garbled}}} ({count}x, {len(garbled)} chars)")
        for before, after in garbled_contexts[garbled][:4]:
            print(f"    [{before}] _ [{after}]")

# ================================================================
# 6. INVESTIGATE {T} ER PATTERN
# ================================================================
print(f"\n{'=' * 80}")
print("6. THE {T} PATTERN: Single-letter garbled blocks")
print("=" * 80)

# {T} appears very often (before ER, before EIN, before ES, etc.)
# This is code 64 which maps to T.
# But T alone isn't a German word, so DP marks it garbled.
# However, T could be:
# - Part of the previous word (STEINEN+T = STEINENTERN?)
# - Article/prefix (archaic)
# - Just cipher noise from word boundaries

single_garbled = Counter()
for i, (t, s, e) in enumerate(tokens_pos):
    if t.startswith('{') and len(t) == 3:  # {X}
        letter = t[1]
        single_garbled[letter] += 1

print("  Single-letter garbled frequency:")
for letter, count in single_garbled.most_common(15):
    print(f"    {{{letter}}}: {count}x")
    # Show first few contexts
    for i, (t, s, e) in enumerate(tokens_pos):
        if t == f'{{{letter}}}':
            before = [tokens_pos[j][0] for j in range(max(0,i-2), i)]
            after = [tokens_pos[j][0] for j in range(i+1, min(len(tokens_pos), i+3))]
            print(f"      [{' '.join(before)}] {{{letter}}} [{' '.join(after)}]")
            if sum(1 for j, (t2,_,_) in enumerate(tokens_pos[:i+1]) if t2 == f'{{{letter}}}') >= 3:
                break

# ================================================================
# 7. COMBINED IMPROVEMENTS TEST
# ================================================================
print(f"\n{'=' * 80}")
print("7. COMBINED COVERAGE TEST")
print("=" * 80)

# Test all confirmed changes together
new_anagrams = dict(ANAGRAM_MAP)
new_anagrams['TNEDAS'] = 'STANDE'

new_known = set(KNOWN)
new_known.add('STANDE')

# Also test: what if we add common MHG short words that appear as garbled?
# E.g., single-letter blocks that could be particles
# TER could be a MHG word: "ter" = der (the) in some dialects
# DER appears often, but {T} ER could be TER
# Wait - {T} ER is code64+next_word. The T is actually there in the text.

# Let me check: is "TER" a valid word we should add?
# In MHG, "ter" isn't standard. But "tër" could be a dialectal "der"
# More likely: the T is a trailing letter from the previous word

# Test: what about adding STANDE + checking NSCHAT
# NSCHAT sorted = ACHNST. NACHTS (nights) sorted = ACHNST. MATCH!
nschat = 'NSCHAT'
nachts = 'NACHTS'
print(f"\n  NSCHAT sorted: {sorted_letters(nschat)}")
print(f"  NACHTS sorted: {sorted_letters(nachts)}")
print(f"  Match: {sorted_letters(nschat) == sorted_letters(nachts)}")

# Where does NSCHAT appear?
nschat_count = resolved.count('NSCHAT')
print(f"  'NSCHAT' in text: {nschat_count}x")

# Actually the DP segments as {NSC} HAT, so NSCHAT appears in the raw text
# Let me check the raw resolved text around NSC
for i in range(len(resolved)):
    if resolved[i:i+3] == 'NSC':
        start = max(0, i-10)
        end = min(len(resolved), i+15)
        ctx = resolved[start:end]
        print(f"    ...{ctx}...")

# Check if {NSC} HAT could be NACHTS
# NSC+HAT = NSCHAT. NACHTS sorted = ACHNST. NSCHAT sorted = ACHNST.
# But wait: HAT is a real word (has). Could "hat" be correct here?
# "WIR {NSC} HAT {EMNET}" -> "WIR NACHTS {EMNET}" = "we at night..."?
# OR: "WIR ... hat ..." = "we ... has ..."
# NACHTS makes more narrative sense than "NSC" + "hat"

# Final combined test
print(f"\n  Combined test with STANDE:")

new_resolved = all_text
for anag in sorted(new_anagrams.keys(), key=len, reverse=True):
    new_resolved = new_resolved.replace(anag, new_anagrams[anag])

new_cov = dp_count(new_resolved, new_known)
print(f"  Baseline:   {baseline_cov}/{total} = {baseline_cov/total*100:.1f}%")
print(f"  +STANDE:    {new_cov}/{total} = {new_cov/total*100:.1f}%")
print(f"  Delta: {new_cov - baseline_cov:+d} chars")

# Also test NACHTS
test_known2 = set(new_known)
test_known2.add('NACHTS')
new_anagrams2 = dict(new_anagrams)
# But NSCHAT needs to be in the text... let me check
# Actually the DP doesn't need an anagram map entry if NACHTS appears naturally
# The issue is: the raw text has NSCHAT, which is an anagram of NACHTS
# So we need NSCHAT -> NACHTS in the anagram map
new_anagrams2['NSCHAT'] = 'NACHTS'
new_resolved2 = all_text
for anag in sorted(new_anagrams2.keys(), key=len, reverse=True):
    new_resolved2 = new_resolved2.replace(anag, new_anagrams2[anag])

new_cov2 = dp_count(new_resolved2, test_known2)
print(f"  +NACHTS:    {new_cov2}/{total} = {new_cov2/total*100:.1f}%")
print(f"  Delta from baseline: {new_cov2 - baseline_cov:+d} chars")

# Show context of NACHTS resolution
for i in range(len(new_resolved2)):
    if new_resolved2[i:i+6] == 'NACHTS':
        start = max(0, i-15)
        end = min(len(new_resolved2), i+21)
        ctx = new_resolved2[start:end]
        print(f"    ...{ctx}...")

print(f"\n{'=' * 80}")
print("SESSION 19 SUMMARY")
print("=" * 80)
