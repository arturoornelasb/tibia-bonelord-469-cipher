#!/usr/bin/env python3
"""
Session 19 Part 4: Narrative structure analysis and new word discovery.

Instead of matching against dictionaries, analyze the narrative STRUCTURE:
1. Map all recurring phrases and their positions
2. Identify the circular/repeating story sections
3. Use repetition to cross-validate garbled block readings
4. Look for words hiding in plain sight (German words not in KNOWN)
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

book_pairs = []
decoded_books = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        split_pos, digit = DIGIT_SPLITS[bidx]
        book = book[:split_pos] + digit + book[split_pos:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)
    text = ''.join(v7.get(p, '?') for p in pairs)
    decoded_books.append(text)

all_text = ''.join(decoded_books)

ANAGRAM_MAP = {
    'LABGZERAS': 'SALZBERG', 'SCHWITEIONE': 'WEICHSTEIN',
    'SCHWITEIO': 'WEICHSTEIN', 'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'EDETOTNIURG': 'GOTTDIENER', 'EDETOTNIURGS': 'GOTTDIENERS',
    'ADTHARSC': 'SCHARDT', 'TAUTR': 'TRAUT', 'EILCH': 'LEICH',
    'HEDEMI': 'HEIME', 'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG', 'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE', 'TEIGN': 'NEIGT', 'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER', 'SODGE': 'GODES', 'SNDTEII': 'DIENST',
    'IEB': 'BEI',
    'TNEDAS': 'STANDE', 'NSCHAT': 'NACHTS', 'SANGE': 'SAGEN',
}

resolved = all_text
for anag in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved = resolved.replace(anag, ANAGRAM_MAP[anag])

KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR', 'NU', 'STANDE', 'NACHTS',
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
    'GEIGET', 'BERUCHTIG', 'BERUCHTIGER',
    'MEERE', 'NEIGT', 'WISTEN', 'MANIER', 'HUND',
    'GODE', 'GODES', 'EIGENTUM', 'REDER',
    'THENAEUT', 'LABT', 'MORT', 'DIGE', 'WEGE', 'KOENIGS',
    'NAHE', 'NOT', 'NOTH', 'ZUR', 'OWI', 'ENGE', 'SEIDEN',
    'ALTES', 'NUT', 'NUTZ', 'HEIL', 'NEID', 'TREU', 'TREUE',
    'SUN', 'DIENST', 'SANG', 'DINC', 'HULDE', 'LANT', 'HERRE',
    'DIENEST', 'GEBOT', 'SCHWUR', 'ORDEN', 'RICHTER', 'DUNKEL',
    'EHRE', 'EDELE', 'SCHULD', 'SEGEN', 'FLUCH', 'RACHE',
    'KOENIG', 'DASS', 'EDEL', 'ADEL',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME', 'SCHARDT',
])

def dp_segment(text, wordset):
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
    return result

# ================================================================
# 1. FIND ALL UNMATCHED TEXT SEGMENTS
# ================================================================
print("=" * 80)
print("1. ALL UNMATCHED TEXT SEGMENTS (sorted by frequency)")
print("=" * 80)

tokens = dp_segment(resolved, KNOWN)

# Extract all garbled blocks and their preceding/following words
garbled_with_context = []
for i, t in enumerate(tokens):
    if t.startswith('{'):
        garbled = t[1:-1]
        prev_word = tokens[i-1] if i > 0 and not tokens[i-1].startswith('{') else ''
        next_word = tokens[i+1] if i+1 < len(tokens) and not tokens[i+1].startswith('{') else ''
        garbled_with_context.append((garbled, prev_word, next_word))

# Frequency of unmatched strings
garbled_freq = Counter(g for g, _, _ in garbled_with_context)

print(f"\n  Total garbled tokens: {len(garbled_with_context)}")
print(f"  Unique garbled strings: {len(garbled_freq)}")

# ================================================================
# 2. SCAN ALL UNMATCHED TEXT FOR HIDDEN GERMAN WORDS
# ================================================================
print(f"\n{'=' * 80}")
print("2. SCANNING UNMATCHED TEXT FOR HIDDEN WORDS")
print("=" * 80)

# German words that might appear in garbled blocks but aren't in KNOWN
GERMAN_CANDIDATES = set([
    # Common German words we might have missed
    'ACH', 'AGE', 'AHN', 'ARM', 'ART', 'BAD', 'BAU', 'BIT', 'BOT',
    'DAM', 'DEI', 'DEL', 'DIN', 'DIS', 'EIS', 'ELF', 'ERB', 'ERZ',
    'FEL', 'FIS', 'FUS', 'GAB', 'GAS', 'GEM', 'GIR', 'GIS', 'GNU',
    'GOD', 'GRA', 'HAS', 'HEI', 'HIT', 'HOF', 'HUT', 'IHM', 'IHR',
    'IRR', 'IRE', 'KAM', 'KIN', 'LAS', 'LEG', 'LOS', 'MAG', 'MAL',
    'MAT', 'MIR', 'MIT', 'MON', 'MOR', 'MUT', 'NAH', 'NET', 'NIT',
    'NOR', 'OHR', 'RAD', 'RAT', 'ROT', 'RUF', 'RUM', 'RUH', 'SAT',
    'SET', 'SIT', 'SOG', 'SUR', 'TAL', 'TOR', 'TOT', 'TUR', 'UHR',
    'WEG', 'WET', 'WIT', 'ZAL', 'ZUG',
    # 4-letter
    'BAUM', 'BEIN', 'BLUT', 'BUCH', 'BURG', 'DAME', 'DEIN', 'DING',
    'DORF', 'EDEL', 'EHER', 'EILE', 'EINS', 'ELBE', 'FALL', 'FEHL',
    'FELS', 'FORM', 'FREI', 'GABE', 'GANG', 'GLAS', 'GRAS', 'GRAU',
    'HABE', 'HALS', 'HART', 'HASS', 'HAUL', 'HAUT', 'HERZ', 'HORN',
    'HUHN', 'HUNT', 'IRRN', 'KALT', 'KERN', 'KIEL', 'KLAR', 'KNIE',
    'KOPF', 'KURZ', 'LASS', 'LAUT', 'LEHN', 'LEID', 'LIED', 'LUFT',
    'MAHL', 'MARK', 'MEIN', 'MILD', 'MOND', 'MORD', 'MEIN', 'MIST',
    'NASS', 'NEST', 'OBEN', 'OFEN', 'PEIN', 'PFAD', 'RAUB', 'REIS',
    'REST', 'RING', 'ROST', 'RUHM', 'SAAL', 'SALZ', 'SATT', 'SINN',
    'SOLD', 'SPAT', 'STAR', 'STUR', 'TIEF', 'TIER', 'TOLL', 'TORR',
    'TRUG', 'TURM', 'VOLK', 'VOLL', 'WACH', 'WAHN', 'WARM', 'WARE',
    'WEIB', 'WEIN', 'WERK', 'WILD', 'WOLF', 'WURM', 'ZAHL', 'ZART',
    'ZIEL', 'ZIER', 'ZUGE',
    # MHG specific
    'GUOT', 'MUOT', 'VUOZ', 'LIEP', 'NIHT', 'OUCH', 'SICH', 'WICH',
    'BALT', 'HOLT', 'SWER', 'TWER', 'WELT', 'GELT', 'HILT', 'SOLT',
    'GOLT', 'DOCH', 'NACH', 'SACH', 'MACH', 'WACH', 'DACH',
    'STRIT', 'GELIT', 'GESIT', 'GETOT', 'GEBOT',
    # Verb forms that might appear
    'GING', 'GALT', 'FUHR', 'LIEH', 'LITT', 'RITT', 'RISS', 'SANN',
    'TRAT', 'TRUG', 'WIES', 'WUCHS', 'ZIEHT',
    # Religious/lore words
    'ALTAR', 'BIBEL', 'ENGEL', 'GEBET', 'GOETZ', 'HEIDN', 'KREUZ',
    'OPFER', 'TAUFE', 'TEMPLE',
    # Tibia lore potential
    'THAIS', 'EDRON', 'CARLIN', 'VENORE', 'KAZORDOON',
])

# Check which of these appear in the resolved text
print("\n  German/MHG words found in text but NOT in KNOWN:")
found_new = []
for word in sorted(GERMAN_CANDIDATES, key=len, reverse=True):
    if word in KNOWN:
        continue
    count = resolved.count(word)
    if count >= 2:
        found_new.append((word, count))

for word, count in sorted(found_new, key=lambda x: -x[1]):
    # Check if adding it would improve coverage
    test_known = set(KNOWN)
    test_known.add(word)
    tokens_test = dp_segment(resolved, test_known)
    old_cov = sum(len(t) for t in dp_segment(resolved, KNOWN) if not t.startswith('{'))
    new_cov = sum(len(t) for t in tokens_test if not t.startswith('{'))
    delta = new_cov - old_cov
    if delta > 0:
        print(f"  {word}: {count}x, coverage +{delta}")
        # Show contexts
        for i in range(len(resolved)):
            if resolved[i:i+len(word)] == word:
                start = max(0, i-10)
                end = min(len(resolved), i+len(word)+10)
                ctx = resolved[start:end]
                print(f"    ...{ctx}...")
                break

# ================================================================
# 3. FIND REPEATING GARBLED SEQUENCES IN RAW DECODED TEXT
# ================================================================
print(f"\n{'=' * 80}")
print("3. REPEATING RAW LETTER SEQUENCES (not yet matched)")
print("=" * 80)

# Extract all substrings of length 4-10 that:
# 1. Appear 3+ times
# 2. Are NOT fully covered by known words
# 3. Could be unknown words or proper nouns

substring_freq = Counter()
for slen in range(4, 11):
    for i in range(len(resolved) - slen + 1):
        sub = resolved[i:i+slen]
        if '?' not in sub:
            substring_freq[sub] += 1

# Filter: must appear 3+ times, not be a known word, and not be a substring of a known word
# Also check it's not already fully covered by DP
print("\n  Frequent substrings (3+ occurrences, not in KNOWN):")
seen_subs = set()
for sub, count in substring_freq.most_common(500):
    if count < 3:
        break
    if sub in KNOWN:
        continue
    if len(sub) < 4:
        continue
    # Check if fully covered by DP
    tokens_sub = dp_segment(sub, KNOWN)
    uncovered = sum(len(t)-2 for t in tokens_sub if t.startswith('{'))
    if uncovered >= 2:  # At least 2 uncovered chars
        # Check it's not a substring of already-shown ones
        skip = False
        for prev in seen_subs:
            if sub in prev:
                skip = True
                break
        if not skip:
            seen_subs.add(sub)
            print(f"  {count:3d}x [{uncovered} unmatched]: {sub}")
            # Show DP parse
            print(f"        DP: {' '.join(tokens_sub)}")

# ================================================================
# 4. NARRATIVE SECTION MAPPING
# ================================================================
print(f"\n{'=' * 80}")
print("4. CIRCULAR NARRATIVE: Repeating Anchor Phrases")
print("=" * 80)

# Key repeating phrases that mark narrative sections
anchor_phrases = [
    'TRAUTISTLEICHANBERUCHTIG',
    'DIEUURALTESTEINEN',
    'DENENDEREDERKOENIGSALZBERG',
    'ORANGENSTRASSE',
    'WEICHSTEIN',
    'GOTTDIENER',
    'THENAEUTERALS',
    'FINDEN',
    'SAGENAMMIN',
    'ICHOELSODEN',
    'RUNEORT',
]

for phrase_nospace in anchor_phrases:
    # Count occurrences in resolved text (without spaces)
    count = resolved.count(phrase_nospace)
    if count > 0:
        positions = []
        pos = 0
        while True:
            idx = resolved.find(phrase_nospace, pos)
            if idx < 0:
                break
            positions.append(idx)
            pos = idx + 1
        print(f"\n  '{phrase_nospace}' ({count}x): positions {positions}")
        # Show spacing between occurrences
        if len(positions) > 1:
            gaps = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
            print(f"    Gaps: {gaps} (avg {sum(gaps)/len(gaps):.0f})")

# ================================================================
# 5. ORPHAN LETTER ANALYSIS: Single-char garbled blocks
# ================================================================
print(f"\n{'=' * 80}")
print("5. ORPHAN LETTERS: Where do single-char garbled blocks come from?")
print("=" * 80)

# Many single {E}, {T}, {D}, etc. These are the "+1" extra letters from anagrams
# or word boundary artifacts. Can we determine a pattern?

orphan_positions = defaultdict(list)  # letter -> [(position, before_word, after_word)]
for i, t in enumerate(tokens):
    if t.startswith('{') and len(t) == 3:  # Single letter: {X}
        letter = t[1]
        before = tokens[i-1] if i > 0 else ''
        after = tokens[i+1] if i+1 < len(tokens) else ''
        orphan_positions[letter].append((i, before, after))

for letter in sorted(orphan_positions.keys(), key=lambda x: -len(orphan_positions[x])):
    positions = orphan_positions[letter]
    if len(positions) >= 3:
        print(f"\n  {{{letter}}} ({len(positions)}x):")
        # Most common before/after words
        before_count = Counter(b for _, b, _ in positions if b)
        after_count = Counter(a for _, _, a in positions if a)
        top_before = before_count.most_common(3)
        top_after = after_count.most_common(3)
        print(f"    Most common before: {top_before}")
        print(f"    Most common after: {top_after}")

print(f"\n{'=' * 80}")
print("DONE")
print("=" * 80)
