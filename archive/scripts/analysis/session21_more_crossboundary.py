#!/usr/bin/env python3
"""
Session 21 Part 6: More cross-boundary anagram search.

ANSD -> SAND worked (+14 chars). Search for more patterns like this.

Two-letter garbled blocks to investigate:
- {DE} 10x: NEU|DE|DIENST (5x), SEINE|DE|TOT (3x)
- {ND} 9x: ORT|ND|TER (6x)
- {NT} 4x: ENDE|NT|ES
- {DR} 3x: RUNEN|DR|THENAEUT
- {TD} 3x: IM|TD|ENDE
- {HH} 3x: ENGE|HH|EIN
- {TI} 3x: SER|TI|UM
- {EO} 5x: GAR|EO|RUNE (3x)

Also try three-letter garbled blocks with neighbors.
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

# Apply current anagram map
ANAGRAM_MAP = {
    'LABGZERAS': 'SALZBERG', 'SCHWITEIONE': 'WEICHSTEIN',
    'SCHWITEIO': 'WEICHSTEIN', 'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'EDETOTNIURG': 'GOTTDIENER', 'EDETOTNIURGS': 'GOTTDIENERS',
    'ADTHARSC': 'SCHARDT', 'TAUTR': 'TRAUT', 'EILCH': 'LEICH',
    'HEDDEMI': 'HEIME',
    'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG', 'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE', 'TEIGN': 'NEIGT', 'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER', 'SODGE': 'GODES', 'SNDTEII': 'DIENST',
    'IEB': 'BEI', 'TNEDAS': 'STANDE', 'NSCHAT': 'NACHTS',
    'SANGE': 'SAGEN', 'GHNEE': 'GEHEN', 'THARSCR': 'SCHRAT',
    'ANSD': 'SAND',
}

# Get processed text
processed_books = []
for text in decoded_books:
    for old, new in ANAGRAM_MAP.items():
        text = text.replace(old, new)
    processed_books.append(text)

all_processed = ''.join(processed_books)

# ================================================================
# Comprehensive search: garbled+known word combinations
# ================================================================
print("=" * 80)
print("CROSS-BOUNDARY ANAGRAM SEARCH (extended)")
print("=" * 80)

# Large German word list for matching
WORDS = set([
    # 2-letter
    'AB', 'AM', 'AN', 'DA', 'DU', 'EI', 'ER', 'ES', 'GE', 'IM', 'IN',
    'JA', 'JE', 'MI', 'NU', 'OB', 'SO', 'TU', 'UM', 'UN', 'UR', 'WO', 'ZU',
    # 3-letter
    'ACH', 'ART', 'BIS', 'DAR', 'DAS', 'DEM', 'DEN', 'DER', 'DES', 'DIE',
    'DIR', 'EIN', 'GAR', 'GEN', 'GOT', 'GUT', 'HAT', 'HER', 'HIN', 'ICH',
    'IHR', 'IST', 'MAN', 'MIR', 'MIT', 'NUN', 'NUR', 'ODE', 'ORT', 'RAT',
    'SAG', 'SEI', 'SER', 'SIE', 'TAG', 'TAT', 'TER', 'TOD', 'TOT', 'TUN',
    'TUT', 'UND', 'VON', 'VOR', 'WAR', 'WAS', 'WEG', 'WER', 'WIE', 'WIR',
    'OEL', 'OWI', 'MIN', 'SUN', 'NIT', 'NOT', 'GEH', 'SCE', 'INS', 'NEU',
    'NIE', 'NUT', 'BEI',
    # 4-letter
    'ABER', 'ACHT', 'ALLE', 'ALSO', 'ALTE', 'AUCH', 'BALD', 'BAND', 'BERG',
    'BILD', 'BOTE', 'BURG', 'DANK', 'DASS', 'DEIN', 'DENN', 'DICH', 'DIES',
    'DOCH', 'DORT', 'DREI', 'EDEL', 'EGAL', 'EHRE', 'EIDE', 'EINE', 'ENDE',
    'ERDE', 'ERST', 'EUCH', 'FACH', 'FAND', 'FERN', 'FEST', 'FIEL', 'FORT',
    'FREI', 'GABE', 'GALT', 'GANZ', 'GAST', 'GELD', 'GERN', 'GIBT', 'GLAS',
    'GOTT', 'GRAB', 'GRAS', 'GROS', 'GRUN', 'HALF', 'HALT', 'HAND', 'HAUS',
    'HEIL', 'HEIM', 'HELD', 'HERR', 'HIER', 'HOCH', 'HORN', 'HORT', 'HULD',
    'HUND', 'INNE', 'JEDE', 'KALT', 'KANN', 'KEIN', 'KIND', 'KLAR', 'KLUG',
    'KNIE', 'LABT', 'LAND', 'LANG', 'LEID', 'LIED', 'LUST', 'MEHR', 'MEIN',
    'MILD', 'MORT', 'MUSS', 'NACH', 'NAHE', 'NAHT', 'NAME', 'NEID', 'NEIN',
    'NOCH', 'ODER', 'REDE', 'REIN', 'RIEF', 'RUIN', 'RUNE', 'SAGT', 'SAND',
    'SANG', 'SEID', 'SEIN', 'SICH', 'SIND', 'SOHN', 'SOLL', 'STEH', 'TEIL',
    'TIEF', 'TIER', 'TORE', 'TREU', 'TURM', 'UFER', 'VIEL', 'VIER', 'WALD',
    'WAND', 'WARD', 'WART', 'WEGE', 'WEIL', 'WEIT', 'WELT', 'WENN', 'WERT',
    'WILL', 'WIND', 'WIRD', 'WIRT', 'WOHL', 'WORT', 'WUND', 'ZEHN', 'ZEIT',
    'ZORN', 'DIGE', 'ENGE',
    # 5-letter
    'ADLER', 'ALLES', 'ALTEN', 'ALTER', 'ALTES', 'BEIDE', 'BERGE', 'BREIT',
    'DARAN', 'DARIN', 'DARUM', 'DEINE', 'DENEN', 'DERER', 'DIESE', 'DURCH',
    'EIGEN', 'EINEN', 'EINER', 'EINES', 'ENGEL', 'ERDEN', 'ERNST', 'ERSTE',
    'ETWAS', 'FEIND', 'GABEN', 'GEBEN', 'GEGEN', 'GEIST', 'GNADE', 'GRABE',
    'GREIS', 'GRUND', 'GRUFT', 'HABEN', 'HAUPT', 'HEIDE', 'HERRE', 'IMMER',
    'JEDER', 'JEDEN', 'KLAGE', 'KLEIN', 'KRAFT', 'KREUZ', 'KRONE', 'LANDE',
    'LEGEN', 'LESEN', 'LEUTE', 'LICHT', 'LIEBE', 'MACHT', 'MEERE', 'MINNE',
    'NACHT', 'NEIGT', 'NICHT', 'ORTEN', 'RECHT', 'REDEN', 'RUFEN', 'RUHEN',
    'RUNEN', 'SAGEN', 'SCHON', 'SEELE', 'SEGEN', 'SEHEN', 'SENDE', 'SORGE',
    'STAUB', 'STEHE', 'STERN', 'STOLZ', 'UNTER', 'WACHE', 'WAGEN', 'WEGEN',
    'WENDE', 'WESEN', 'WILLE', 'WISSE', 'WORTE', 'WUNDE',
    'DIENST', 'FINDEN', 'GEIGET', 'SCHAUN', 'STANDE', 'NACHTS', 'WISTEN',
    'MANIER', 'STEINEN', 'URALTE', 'RICHTER', 'DUNKEL', 'KOENIG',
    'REDER', 'HEIME', 'SALZBERG', 'TRAUT', 'LEICH',
    # MHG extras
    'DINC', 'HULDE', 'LANT', 'HERRE', 'DIENEST', 'GEBOT', 'SCHWUR',
    'ORDEN', 'EDELE', 'SCHULD', 'FLUCH', 'RACHE', 'SEGEN',
    'SCHRAT', 'SCHARDT',
    'GODES', 'BERUCHTIG', 'EIGENTUM', 'GOTTDIENER', 'WEICHSTEIN',
    'ORANGENSTRASSE',
    # Additional MHG
    'SIN', 'WOL', 'MER', 'DAR', 'SOL', 'HIE', 'ANE',
    'DIET', 'RIET', 'MUOT', 'GUOT', 'TUOT', 'MAGE',
    'SWERT', 'RICHE', 'HELDE', 'MINNEN',
    'SELDE', 'TUGENT', 'TRIUWE',
])

# Build sorted lookup
word_lookup = defaultdict(list)
for w in WORDS:
    word_lookup[''.join(sorted(w))].append(w)

# For each 2-letter garbled block, try combining with left and right neighbor
# Parse the processed text to find garbled blocks with context

KNOWN = set([w for w in WORDS if len(w) >= 2])

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
            i = start
        else:
            j = i - 1
            while j > 0 and dp[j][1] is None:
                j -= 1
            tokens.append(('garbled', text[j:i]))
            i = j
    tokens.reverse()
    return tokens

# Find all garbled+word combos
results = []
for bidx, text in enumerate(processed_books):
    tokens = dp_segment(text)
    for ti, (ttype, tval) in enumerate(tokens):
        if ttype == 'garbled' and 1 <= len(tval) <= 4:
            # Get left and right words
            left_word = None
            right_word = None
            for j in range(ti-1, -1, -1):
                if tokens[j][0] == 'word':
                    left_word = tokens[j][1]
                    break
            for j in range(ti+1, len(tokens)):
                if tokens[j][0] == 'word':
                    right_word = tokens[j][1]
                    break

            # Try: left_word + garbled
            if left_word:
                combo = left_word + tval
                cs = ''.join(sorted(combo))
                matches = word_lookup.get(cs, [])
                matches = [m for m in matches if m != combo]
                if matches:
                    results.append((f"{left_word}+{tval}", combo, matches, 'exact', bidx))

                # +1 pattern
                for skip in range(len(combo)):
                    reduced = combo[:skip] + combo[skip+1:]
                    rs = ''.join(sorted(reduced))
                    rmatches = word_lookup.get(rs, [])
                    rmatches = [m for m in rmatches if m != reduced]
                    if rmatches:
                        results.append((f"{left_word}+{tval}", combo, rmatches, f"+1(extra {combo[skip]})", bidx))
                        break

            # Try: garbled + right_word
            if right_word:
                combo = tval + right_word
                cs = ''.join(sorted(combo))
                matches = word_lookup.get(cs, [])
                matches = [m for m in matches if m != combo]
                if matches:
                    results.append((f"{tval}+{right_word}", combo, matches, 'exact', bidx))

                # +1 pattern
                for skip in range(len(combo)):
                    reduced = combo[:skip] + combo[skip+1:]
                    rs = ''.join(sorted(reduced))
                    rmatches = word_lookup.get(rs, [])
                    rmatches = [m for m in rmatches if m != reduced]
                    if rmatches:
                        results.append((f"{tval}+{right_word}", combo, rmatches, f"+1(extra {combo[skip]})", bidx))
                        break

# Deduplicate and count
combo_counts = Counter()
combo_info = {}
for desc, combo, matches, pattern, bidx in results:
    key = (desc, combo, tuple(matches), pattern)
    combo_counts[key] += 1
    if key not in combo_info:
        combo_info[key] = []
    combo_info[key].append(bidx)

# Sort by frequency
print(f"\n  Found {len(combo_counts)} unique cross-boundary patterns:")
for (desc, combo, matches, pattern), count in combo_counts.most_common(30):
    if count >= 2:
        books_str = ','.join(str(b) for b in combo_info[(desc, combo, matches, pattern)][:5])
        print(f"  {count:2d}x {desc:20s} = {combo:15s} -> {list(matches)} ({pattern}) [books: {books_str}]")

print(f"\n  All exact matches with freq >= 2:")
for (desc, combo, matches, pattern), count in combo_counts.most_common():
    if count >= 2 and pattern == 'exact':
        books_str = ','.join(str(b) for b in combo_info[(desc, combo, matches, pattern)][:5])
        print(f"  {count:2d}x {desc:20s} = {combo:15s} -> {list(matches)} [books: {books_str}]")

        # Check for collision: does this combo appear inside other words?
        collision = False
        for w in WORDS:
            if combo in w and w != combo:
                collision = True
                print(f"       COLLISION: {combo} is inside {w}")
                break
        # Also check in anagram map outputs
        for old, new in ANAGRAM_MAP.items():
            if combo in new:
                collision = True
                print(f"       COLLISION: {combo} is inside anagram output {new}")
                break
        if not collision:
            print(f"       No collision detected - SAFE to add")

print(f"\nDone.")
