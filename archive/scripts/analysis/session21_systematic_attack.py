#!/usr/bin/env python3
"""
Session 21: Systematic attack on remaining garbled blocks.

Strategy:
1. Extract all garbled blocks with frequencies and contexts
2. For each block, test: anagram, substring decomposition, MHG words
3. Focus on high-frequency small blocks (biggest coverage gains)
4. Test context-based word completions ({X} + neighbor word)
"""

import json, os, re
from collections import Counter, defaultdict
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

all_text = ''.join(decoded_books)

# ================================================================
# 1. EXTRACT ALL GARBLED BLOCKS WITH CONTEXT
# ================================================================
# Re-run segmentation to get blocks
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
    'IEB': 'BEI', 'TNEDAS': 'STANDE', 'NSCHAT': 'NACHTS',
    'SANGE': 'SAGEN', 'GHNEE': 'GEHEN', 'THARSCR': 'SCHRAT',
}

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
                gap = text[start + len(word) - (i - start - len(word)):start]
            i = start
        else:
            j = i - 1
            while j > 0 and dp[j][1] is None:
                j -= 1
            tokens.append(('garbled', text[j:i]))
            i = j
    tokens.reverse()
    return tokens

# Collect all garbled blocks with contexts
garbled_blocks = defaultdict(list)  # block -> [(book_idx, left_word, right_word)]

for bidx, text in enumerate(decoded_books):
    # First apply anagrams
    for old, new in ANAGRAM_MAP.items():
        text = text.replace(old, new)
    tokens = dp_segment(text)
    for ti, (ttype, tval) in enumerate(tokens):
        if ttype == 'garbled':
            left = ''
            right = ''
            for j in range(ti-1, -1, -1):
                if tokens[j][0] == 'word':
                    left = tokens[j][1]
                    break
            for j in range(ti+1, len(tokens)):
                if tokens[j][0] == 'word':
                    right = tokens[j][1]
                    break
            garbled_blocks[tval].append((bidx, left, right))

print("=" * 80)
print("SESSION 21: GARBLED BLOCK CENSUS (sorted by total chars = freq x len)")
print("=" * 80)

# Sort by total garbled chars (freq * length)
ranked = sorted(garbled_blocks.items(), key=lambda x: -len(x[0]) * len(x[1]))

total_garbled_chars = sum(len(b) * len(occ) for b, occ in garbled_blocks.items())
print(f"\nTotal garbled: {total_garbled_chars} chars in {sum(len(v) for v in garbled_blocks.values())} blocks ({len(garbled_blocks)} unique)")

print(f"\nTop 40 blocks by total impact (freq x length):")
for block, occs in ranked[:40]:
    impact = len(block) * len(occs)
    contexts = set()
    for _, left, right in occs:
        contexts.add(f"{left}|...|{right}")
    ctx_str = '; '.join(list(contexts)[:3])
    print(f"  {block:30s} {len(block):2d}ch x{len(occs):2d} = {impact:4d} chars  [{ctx_str}]")

# ================================================================
# 2. SMALL BLOCK ANAGRAM ATTACK (2-5 chars)
# ================================================================
print(f"\n{'=' * 80}")
print("2. SMALL BLOCK ANAGRAM ATTACK (2-5 chars)")
print("=" * 80)

# Extended MHG/German word list for anagram matching
MHG_WORDS = [
    # 2-letter
    'AB', 'AM', 'AN', 'AU', 'DA', 'DU', 'EI', 'ER', 'ES', 'GE', 'HE',
    'HI', 'IM', 'IN', 'IR', 'JA', 'JE', 'MI', 'NU', 'OB', 'OR', 'SO',
    'TU', 'UM', 'UN', 'UR', 'WE', 'WO', 'ZU',
    # 3-letter
    'ACH', 'ANE', 'ART', 'BIT', 'BOT', 'DAR', 'DIN', 'DOC', 'EHR', 'EIS',
    'ELF', 'FEL', 'GAB', 'GEL', 'GEN', 'GOT', 'GUT', 'HAT', 'HER', 'HIN',
    'HOF', 'ICH', 'IRE', 'IST', 'KIN', 'LAG', 'LAS', 'LID', 'LIE', 'LOT',
    'MAG', 'MAN', 'MER', 'MIN', 'MIT', 'MUO', 'NAH', 'NET', 'NIU', 'NIT',
    'NOD', 'NOT', 'NUN', 'NUR', 'NUT', 'OEL', 'ORT', 'RAT', 'RED', 'RUF',
    'SAG', 'SAH', 'SAN', 'SAT', 'SCE', 'SEI', 'SIN', 'SIT', 'SOL', 'SUN',
    'TAG', 'TAT', 'TER', 'TIR', 'TOD', 'TOT', 'TUN', 'TUR', 'UND', 'VON',
    'VOR', 'WAR', 'WEG', 'WER', 'WIE', 'WIR', 'WIS', 'WOL', 'ZIT',
    'ODE', 'SER', 'INS', 'OWI', 'BEI', 'GEH', 'DES',
    # 4-letter
    'ACHT', 'ALTE', 'AUCH', 'AUGE', 'BEIN', 'BISS', 'BLUT', 'BOTE', 'BURG',
    'DACH', 'DASS', 'DEIN', 'DICH', 'DIEN', 'DING', 'DOCH', 'DORT', 'DREI',
    'EDEL', 'EHEN', 'EIDE', 'EINE', 'ENGE', 'FACH', 'FAND', 'FERN', 'FEST',
    'FIEL', 'FORT', 'FREI', 'GABE', 'GANZ', 'GAST', 'GELD', 'GERN', 'GLAS',
    'GNAD', 'GOLD', 'GOTT', 'GRAB', 'GRAS', 'GROS', 'GRUN', 'HABE', 'HALB',
    'HALT', 'HAND', 'HAUS', 'HAUT', 'HEIL', 'HEIM', 'HELD', 'HELM', 'HERR',
    'HERS', 'HIER', 'HOCH', 'HORN', 'HORT', 'HULD', 'HUND', 'INNE', 'IURE',
    'JENE', 'KALT', 'KANN', 'KEIN', 'KIND', 'KLAR', 'KLUG', 'KNIE', 'KORE',
    'LABT', 'LAND', 'LANG', 'LAST', 'LEIT', 'LEID', 'LEUT', 'LIED', 'LIES',
    'LUST', 'MAGE', 'MEIN', 'MICH', 'MILD', 'MORT', 'MUOT', 'MUSS', 'NACH',
    'NAHE', 'NAHT', 'NAME', 'NEID', 'NEIN', 'NIDE', 'NIMM', 'NOCH', 'NOTH',
    'OBEN', 'ODER', 'REDE', 'REIN', 'RIST', 'RITE', 'ROSS', 'RUHE', 'RUIN',
    'RUNE', 'RUFT', 'SACH', 'SAGT', 'SAND', 'SANG', 'SEID', 'SEIN', 'SEIT',
    'SICH', 'SIND', 'SITE', 'SOHN', 'SOLL', 'STAR', 'STAT', 'STEH', 'TAGE',
    'TEIL', 'TIEF', 'TIER', 'TORE', 'TREU', 'TURM', 'UNER', 'VIEL', 'VIER',
    'WAHR', 'WALD', 'WAND', 'WARD', 'WART', 'WEGE', 'WEIL', 'WEIT', 'WELT',
    'WENN', 'WERT', 'WIES', 'WILL', 'WIND', 'WIRD', 'WIRT', 'WOHL', 'WORT',
    'WUND', 'ZEHN', 'ZEIT', 'ZORN', 'ZWEN', 'DIGE', 'ENDE', 'ERDE',
    'LEIB', 'DIET', 'RIET', 'TIER', 'REIS', 'REIT', 'STIR', 'RIST',
    'SIRE', 'IREN', 'REIN', 'NIRE', 'NIER', 'EINS', 'REIS', 'SEIL',
    'LEIS', 'LIES', 'LEIN', 'NEIL', 'HIRT', 'HIRN',
    # 5-letter
    'ADLER', 'ALLES', 'ALTEN', 'ALTER', 'ALTES', 'ANDRE', 'ANGEL',
    'ASCHE', 'BEGUN', 'BEIDE', 'BERGE', 'BETEN', 'BITTE', 'BLICK',
    'BODEN', 'BREIT', 'BRUST', 'DARAN', 'DARIN', 'DARUM', 'DAUER',
    'DEGEN', 'DEINE', 'DENEN', 'DERER', 'DIESE', 'DINNE', 'DIRNE',
    'DREHE', 'DUNST', 'DURCH', 'EBENE', 'EDELE', 'EHREN', 'EIGEN',
    'EILIG', 'EINIG', 'EINEN', 'EINER', 'EINES', 'ENGEL', 'ERDEN',
    'ERNST', 'ERSTE', 'ESSEN', 'ETWAS', 'EURER', 'EWIGE', 'FALLT',
    'FEIND', 'FRIED', 'GABEN', 'GEBEN', 'GEGEN', 'GEIST', 'GENUG',
    'GNADE', 'GRABE', 'GREIS', 'GRUND', 'GRUFT', 'HABEN', 'HAFEN',
    'HAUPT', 'HEIDE', 'HEILT', 'HERRE', 'HEUER', 'IHNEN', 'IMMER',
    'INDES', 'INNEN', 'JEDER', 'JENER', 'JEDEN', 'KLAGE', 'KLEIN',
    'KNABE', 'KRAFT', 'KREUZ', 'KRONE', 'LANDE', 'LAUBE', 'LEGEN',
    'LESEN', 'LEUTE', 'LICHT', 'LIEBE', 'LIEST', 'MACHT', 'MEERE',
    'MINNE', 'NACHT', 'NEIGT', 'NENNE', 'NEUE', 'NICHT', 'ORTEN',
    'RECHT', 'REDEN', 'REDET', 'REGEN', 'RUFEN', 'RUHEN', 'RUNEN',
    'SAGEN', 'SCHAR', 'SCHON', 'SEELE', 'SEGEN', 'SEHEN', 'SENDE',
    'SINNE', 'SORGE', 'STAUB', 'STEHE', 'STERN', 'STIMM', 'STOLZ',
    'SUNDE', 'TAGEN', 'TREUE', 'TUGEND', 'UNSER', 'UNTER', 'WACHE',
    'WAGEN', 'WAHRE', 'WEGEN', 'WEITE', 'WENDE', 'WESEN', 'WIDER',
    'WILLE', 'WISSE', 'WORTE', 'WUNDE', 'ZEIGT', 'ZWEIT',
    'DIENST', 'HEIME', 'LEICH', 'TRAUT', 'MEERE', 'NEIGT', 'GODES',
    'SCHARDT', 'SCHRAT', 'WISTEN', 'MANIER', 'NACHTS', 'STANDE',
    'LABT', 'DIGE', 'WEGE', 'GEIGET',
    # Extra MHG candidates
    'HELDE', 'SWERT', 'HIMEL', 'RITER', 'RICHE', 'ORDEN', 'DIENEST',
    'HULDE', 'SCHULD', 'DUNKEL', 'RICHTER', 'GEBOT', 'SCHWUR',
    'SELDEN', 'TUGENT', 'STUNDE', 'WUNDER', 'SUNNE', 'MUOTER',
    'TRIUWE', 'MINNEN', 'HERZEN', 'LIEBEN',
]

# Deduplicate
MHG_WORDS = list(set(MHG_WORDS))

# Build sorted-letter -> word mapping for fast anagram lookup
anagram_dict = defaultdict(list)
for w in MHG_WORDS:
    key = ''.join(sorted(w))
    anagram_dict[key].append(w)

print(f"\n  Testing {len([b for b in garbled_blocks if 2 <= len(b) <= 5])} small blocks (2-5 chars):")
small_hits = []
for block, occs in sorted(garbled_blocks.items(), key=lambda x: -len(x[1])):
    if len(block) < 2 or len(block) > 5:
        continue
    bsorted = ''.join(sorted(block))
    # Exact anagram
    matches = anagram_dict.get(bsorted, [])
    matches = [m for m in matches if m != block]  # exclude self
    # +1 anagram (block has one extra letter)
    plus1 = []
    if len(block) >= 3:
        for skip in range(len(block)):
            reduced = block[:skip] + block[skip+1:]
            rsorted = ''.join(sorted(reduced))
            for m in anagram_dict.get(rsorted, []):
                if m not in plus1 and m != reduced:
                    plus1.append(m)

    if matches or plus1:
        freq = len(occs)
        impact = len(block) * freq
        contexts = set()
        for _, left, right in occs:
            contexts.add(f"{left}|{block}|{right}")
        ctx_str = '; '.join(list(contexts)[:2])
        if matches:
            print(f"  {{{{%s}}}} {freq}x -> EXACT: {matches}  [{ctx_str}]" % block)
            small_hits.append((block, matches, 'exact', freq))
        if plus1:
            extra_letters = []
            for skip in range(len(block)):
                reduced = block[:skip] + block[skip+1:]
                rsorted = ''.join(sorted(reduced))
                for m in anagram_dict.get(rsorted, []):
                    extra_letters.append((block[skip], m))
            print(f"  {{{{%s}}}} {freq}x -> +1: {plus1} (extras: {extra_letters[:5]})  [{ctx_str}]" % block)
            small_hits.append((block, plus1, '+1', freq))

# ================================================================
# 3. MEDIUM BLOCK ATTACK (6-10 chars)
# ================================================================
print(f"\n{'=' * 80}")
print("3. MEDIUM BLOCK ANAGRAM ATTACK (6-10 chars)")
print("=" * 80)

# For medium blocks, try splitting into 2 words
medium_hits = []
for block, occs in sorted(garbled_blocks.items(), key=lambda x: -len(x[1])):
    if len(block) < 6 or len(block) > 10:
        continue
    freq = len(occs)
    if freq < 2:  # skip singletons for now
        continue

    # Try splitting into 2 parts and anagram each
    found = []
    for split in range(2, len(block) - 1):
        left_part = block[:split]
        right_part = block[split:]
        ls = ''.join(sorted(left_part))
        rs = ''.join(sorted(right_part))
        lmatches = anagram_dict.get(ls, [])
        rmatches = anagram_dict.get(rs, [])
        if lmatches and rmatches:
            for lm in lmatches:
                for rm in rmatches:
                    found.append(f"{lm}+{rm}")

    # Also try: full block anagram of a longer word
    bsorted = ''.join(sorted(block))
    full_matches = anagram_dict.get(bsorted, [])
    full_matches = [m for m in full_matches if m != block]

    if found or full_matches:
        contexts = set()
        for _, left, right in occs:
            contexts.add(f"{left}|...|{right}")
        ctx_str = '; '.join(list(contexts)[:2])
        if full_matches:
            print(f"  {{{{%s}}}} {freq}x -> FULL: {full_matches}  [{ctx_str}]" % block)
        if found:
            print(f"  {{{{%s}}}} {freq}x -> SPLIT: {found[:8]}  [{ctx_str}]" % block)
        medium_hits.append((block, found + full_matches, freq))

# ================================================================
# 4. CONTEXT ANALYSIS: {single-letter} + neighbor
# ================================================================
print(f"\n{'=' * 80}")
print("4. SINGLE-LETTER GARBLED + NEIGHBOR WORD ANALYSIS")
print("=" * 80)

# When we have {X} WORD or WORD {X}, what if X is actually part of the word?
single_letter_blocks = {b: o for b, o in garbled_blocks.items() if len(b) == 1}
print(f"\n  Single-letter garbled blocks: {len(single_letter_blocks)}")

for letter, occs in sorted(single_letter_blocks.items(), key=lambda x: -len(x[1])):
    freq = len(occs)
    if freq < 3:
        continue

    # Collect what words appear before/after
    before_combos = Counter()  # letter + right_word
    after_combos = Counter()   # left_word + letter

    for bidx, left, right in occs:
        if right:
            combo = letter + right
            if combo in KNOWN or combo in [w for ws in anagram_dict.values() for w in ws]:
                before_combos[combo] += 1
        if left:
            combo = left + letter
            if combo in KNOWN or combo in [w for ws in anagram_dict.values() for w in ws]:
                after_combos[combo] += 1

    contexts = Counter()
    for bidx, left, right in occs:
        contexts[f"{left}|{{{letter}}}|{right}"] += 1

    top_ctx = contexts.most_common(5)
    ctx_str = ', '.join(f"{c}x {ctx}" for ctx, c in top_ctx)
    print(f"\n  {{{{{letter}}}}} {freq}x: {ctx_str}")
    if before_combos:
        print(f"    -> could prefix: {dict(before_combos)}")
    if after_combos:
        print(f"    -> could suffix: {dict(after_combos)}")

# ================================================================
# 5. TWO-LETTER GARBLED ANALYSIS
# ================================================================
print(f"\n{'=' * 80}")
print("5. TWO-LETTER GARBLED BLOCK ANALYSIS")
print("=" * 80)

two_letter_blocks = {b: o for b, o in garbled_blocks.items() if len(b) == 2}
for block, occs in sorted(two_letter_blocks.items(), key=lambda x: -len(x[1])):
    freq = len(occs)
    if freq < 2:
        continue
    contexts = Counter()
    for bidx, left, right in occs:
        contexts[f"{left}|{{{block}}}|{right}"] += 1
    top_ctx = contexts.most_common(3)
    ctx_str = ', '.join(f"{c}x {ctx}" for ctx, c in top_ctx)

    # Check if block+neighbor or neighbor+block forms a word
    combos = set()
    for bidx, left, right in occs:
        if right:
            c = block + right
            if c in KNOWN:
                combos.add(f"{block}+{right}={c}")
        if left:
            c = left + block
            if c in KNOWN:
                combos.add(f"{left}+{block}={c}")

    combo_str = f" COMBOS: {combos}" if combos else ""
    print(f"  {{{{{block}}}}} {freq}x: {ctx_str}{combo_str}")

# ================================================================
# 6. RECURRING SUBSTRING PATTERNS IN GARBLED
# ================================================================
print(f"\n{'=' * 80}")
print("6. RECURRING SUBSTRINGS IN GARBLED BLOCKS (len >= 3)")
print("=" * 80)

# Collect all garbled text
all_garbled = []
for block in garbled_blocks:
    all_garbled.append(block)
garbled_concat = ' '.join(all_garbled)

# Count substrings of length 3-6 across all garbled blocks
substr_counts = Counter()
for block in garbled_blocks:
    for slen in range(3, min(len(block)+1, 7)):
        for i in range(len(block) - slen + 1):
            sub = block[i:i+slen]
            # Count in how many DIFFERENT blocks this appears
            substr_counts[sub] += garbled_blocks[block].__len__()

# Show substrings appearing in multiple blocks
print(f"\n  Substrings appearing across multiple garbled blocks:")
seen_substrings = set()
for sub, count in substr_counts.most_common(50):
    if count >= 3 and sub not in seen_substrings:
        # How many unique blocks contain this?
        containing = [b for b in garbled_blocks if sub in b]
        if len(containing) >= 2:
            print(f"  '{sub}' in {len(containing)} blocks ({count} total occ): {containing[:5]}")
            seen_substrings.add(sub)

# ================================================================
# 7. HEDDEMI DEEP DIVE
# ================================================================
print(f"\n{'=' * 80}")
print("7. HEDDEMI (11x) DEEP DIVE")
print("=" * 80)

# HEDDEMI has 7 letters including double-D
# The anagram map entry HEDEMI->HEIME never fires because raw has HEDDEMI
# What 6 or 7 letter words can we make from H,E,D,D,E,M,I?
heddemi_letters = sorted('HEDDEMI')
print(f"  Letters: {heddemi_letters} (7 letters, D appears 2x)")

# Check all 6-letter subsets (remove one letter)
print(f"  6-letter subsets (remove one):")
for skip in range(7):
    reduced = 'HEDDEMI'[:skip] + 'HEDDEMI'[skip+1:]
    rs = ''.join(sorted(reduced))
    matches = anagram_dict.get(rs, [])
    if matches:
        print(f"    Remove '{heddemi_letters[skip]}' at pos {skip}: {reduced} -> {matches}")

# What about treating DD as a single phoneme?
# In MHG, double consonants are common
# HEDDEMI -> HE + DD + EMI or HEDD + EMI
# Could DD represent a different letter?
print(f"\n  What if DD (code 45 45) is actually a different character?")
print(f"  Code 45 currently maps to: {v7.get('45', '?')}")

# Let's check what code 45 maps to and if double-45 could mean something else
code45_letter = v7.get('45', '?')
print(f"  Code 45 = '{code45_letter}'")
print(f"  In HEDDEMI: H E {code45_letter}{code45_letter} E M I")
print(f"  = HE{code45_letter}{code45_letter}EMI")

# What if one D is actually part of a different pair?
# Raw codes for HEDDEMI: 57-74-45-45-19-04-50
# What if 45-45 should actually be read differently?
# This is a digit split issue! What if there's an extra/missing digit?
print(f"\n  HEDDEMI raw codes: 57-74-45-45-19-04-50")
print(f"  Decoded: H-E-D-D-E-M-I")
print(f"  What if this is actually a misaligned read?")
print(f"  If we shift: 5-74-54-51-90-45-0 -> ???")
# Check what these would decode to
alt_pairs_1 = ['74', '54', '51', '90', '45']
alt_decode_1 = ''.join(v7.get(p, '?') for p in alt_pairs_1)
print(f"  Alt read (shift right): {alt_pairs_1} -> {alt_decode_1}")

alt_pairs_2 = ['57', '44', '54', '51', '90', '45', '0']
# 44 and single 0 aren't valid pairs, skip this

# Actually, the issue is: could HEDDEMI be HEIME + DD (extra DD)?
# Like SCHRAT from THARSCR has extra R
# HEDDEMI sorted = D,D,E,E,H,I,M
# HEIME sorted = E,E,H,I,M (5 letters)
# HEDDEMI = HEIME + D,D (two extra D's)
# That's a +2 pattern, not +1. Unusual but possible?
print(f"\n  HEDDEMI = HEIME + DD? (+2 pattern)")
print(f"    HEIME sorted: {sorted('HEIME')}")
print(f"    HEDDEMI sorted: {sorted('HEDDEMI')}")
print(f"    Extra letters: D, D")
print(f"    This would be a +2 anagram pattern (unprecedented)")

# What about MEDIZIN? No, wrong letters
# DIEMEN? D,I,E,M,E,N - needs N, we have H and extra D
# DIEHEIM? Not a word
# HEMD (shirt) = H,E,M,D - 4 letters, would leave E,D,I
# HEMD + EID (oath) = 7 letters, H,E,M,D,E,I,D = match!
hmatch = sorted('HEMDEID')
hcheck = sorted('HEDDEMI')
print(f"\n  HEMD + EID = HEMDEID -> sorted: {hmatch}")
print(f"  HEDDEMI sorted: {hcheck}")
print(f"  Match: {hmatch == hcheck}")
if hmatch == hcheck:
    print(f"  *** HEMD (shirt/garment) + EID (oath) = match! ***")
    print(f"  Context: 'IM MIN {{HED}} DEM {{I}} DIE URALTE'")
    print(f"  Currently split as {{HED}} DEM {{I}}")
    print(f"  Full garbled would be: HEDDEMI = HEMD+EID")
    print(f"  But segmentation splits it as HED + DEM + I")
    print(f"  Need to check: is DEM being matched from inside HEDDEMI?")

# Check the actual segmentation
print(f"\n  Testing segmentation of HEDDEMI:")
test_seg = dp_segment('HEDDEMI')
print(f"    DP result: {test_seg}")

# ================================================================
# 8. UTRUNR (7x) ATTACK
# ================================================================
print(f"\n{'=' * 80}")
print("8. UTRUNR (7x, 6 chars) ATTACK")
print("=" * 80)

utrunr = 'UTRUNR'
us = sorted(utrunr)
print(f"  Letters: {us} (N,R,R,T,U,U)")

# Exact anagram
matches = anagram_dict.get(''.join(us), [])
print(f"  Exact anagram matches: {matches}")

# +1 patterns
print(f"  +1 patterns (remove one letter):")
for skip in range(len(utrunr)):
    reduced = utrunr[:skip] + utrunr[skip+1:]
    rs = ''.join(sorted(reduced))
    matches = anagram_dict.get(rs, [])
    if matches:
        print(f"    Remove '{utrunr[skip]}': {reduced} -> {matches}")

# What about NATUR (nature)? N,A,T,U,R - needs A, we have extra U,R
# TURM (tower)? T,U,R,M - needs M
# RUND (round)? R,U,N,D - needs D, not T
# TRUNK (drink)? T,R,U,N,K - needs K
# UNRUT? Not a word. UNRUH (unrest)? U,N,R,U,H - needs H not T,R
# RUTUR? RETUR? NURTRU?
# MHG: TURNE (tournament)? T,U,R,N,E - needs E
# RUNTER (down)? R,U,N,T,E,R - needs E not U

# Split into two words
print(f"\n  Two-word splits:")
for split in range(2, len(utrunr) - 1):
    left = utrunr[:split]
    right = utrunr[split:]
    ls = ''.join(sorted(left))
    rs = ''.join(sorted(right))
    lm = anagram_dict.get(ls, [])
    rm = anagram_dict.get(rs, [])
    if lm and rm:
        for l in lm:
            for r in rm:
                print(f"    {left}|{right} -> {l} + {r}")
    # Also try +1 on each part
    for lskip in range(len(left)):
        lred = left[:lskip] + left[lskip+1:]
        lrs = ''.join(sorted(lred))
        lrm = anagram_dict.get(lrs, [])
        if lrm and rm:
            for l in lrm:
                for r in rm:
                    print(f"    {left}(-{left[lskip]})|{right} -> {l} + {r}")

# Context
print(f"\n  UTRUNR contexts:")
for bidx, left, right in garbled_blocks.get('UTRUNR', []):
    print(f"    Book {bidx}: {left} | UTRUNR | {right}")

# ================================================================
# 9. RRNI (5x) ATTACK
# ================================================================
print(f"\n{'=' * 80}")
print("9. RRNI (5x, 4 chars) ATTACK")
print("=" * 80)

rrni = 'RRNI'
rs = sorted(rrni)
print(f"  Letters: {rs}")
# IRRE? I,R,R,E - needs E not N. Close!
# HIRN (brain)? H,I,R,N - needs H not R
# NIRR? Not standard
# IRR + N? IN + RR?
# What MHG words have I,N,R,R?
# RINN (flow/run)? R,I,N,N - needs 2 N's, we have 2 R's
# What about IRREN (to err)? Too long
# NARR (fool)? N,A,R,R - needs A not I

matches = anagram_dict.get(''.join(sorted(rrni)), [])
print(f"  Exact anagram: {matches}")

for skip in range(len(rrni)):
    reduced = rrni[:skip] + rrni[skip+1:]
    rrs = ''.join(sorted(reduced))
    matches = anagram_dict.get(rrs, [])
    if matches:
        print(f"  +1 remove '{rrni[skip]}': {reduced} -> {matches}")

# Context
print(f"\n  RRNI contexts:")
for bidx, left, right in garbled_blocks.get('RRNI', []):
    print(f"    Book {bidx}: {left} | RRNI | {right}")

# ================================================================
# 10. HIHL (8x) and NDCE (7x) ATTACK
# ================================================================
print(f"\n{'=' * 80}")
print("10. HIHL (8x) and NDCE (7x) ATTACK")
print("=" * 80)

for target in ['HIHL', 'NDCE']:
    occs = garbled_blocks.get(target, [])
    ts = sorted(target)
    print(f"\n  {{{target}}} {len(occs)}x, letters: {ts}")

    matches = anagram_dict.get(''.join(ts), [])
    if matches:
        print(f"    Exact anagram: {matches}")

    for skip in range(len(target)):
        reduced = target[:skip] + target[skip+1:]
        rrs = ''.join(sorted(reduced))
        matches = anagram_dict.get(rrs, [])
        if matches:
            print(f"    +1 remove '{target[skip]}': -> {matches}")

    # Context
    print(f"    Contexts:")
    for bidx, left, right in occs[:3]:
        print(f"      Book {bidx}: {left} | {target} | {right}")

# ================================================================
# 11. NLNDEF (5x) ATTACK
# ================================================================
print(f"\n{'=' * 80}")
print("11. NLNDEF (5x, 6 chars) ATTACK")
print("=" * 80)

nlndef = 'NLNDEF'
ns = sorted(nlndef)
print(f"  Letters: {ns} (D,E,F,L,N,N)")

matches = anagram_dict.get(''.join(ns), [])
print(f"  Exact anagram: {matches}")

# +1
for skip in range(len(nlndef)):
    reduced = nlndef[:skip] + nlndef[skip+1:]
    rrs = ''.join(sorted(reduced))
    matches = anagram_dict.get(rrs, [])
    if matches:
        print(f"  +1 remove '{nlndef[skip]}': -> {matches}")

# FINDEN (find) = F,I,N,D,E,N - needs I not L!
# But we have L. What if code mapping is wrong here?
# FLENDE? LENDEN (loins)? L,E,N,D,E,N - needs 2 E's
# FELDEN? Not standard. FINDEN with L=I?
print(f"\n  FINDEN = F,I,N,D,E,N vs NLNDEF = D,E,F,L,N,N")
print(f"  If L were I: NINDEF -> sorted: {sorted('NINDEF')} vs FINDEN: {sorted('FINDEN')}")
print(f"  Match: {sorted('NINDEF') == sorted('FINDEN')}")
# No, NINDEF sorted = D,E,F,I,N,N and FINDEN sorted = D,E,F,I,N,N
# Wait, let me check
nlndef_if_L_is_I = 'NINDEF'
print(f"  NLNDEF with L->I: NINDEF sorted = {sorted('NINDEF')}")
print(f"  FINDEN sorted = {sorted('FINDEN')}")
print(f"  Match: {sorted('NINDEF') == sorted('FINDEN')}")

# Context
print(f"\n  NLNDEF contexts:")
for bidx, left, right in garbled_blocks.get('NLNDEF', []):
    print(f"    Book {bidx}: {left} | NLNDEF | {right}")

# ================================================================
# 12. HECHLLT (5x) ATTACK
# ================================================================
print(f"\n{'=' * 80}")
print("12. HECHLLT (5x, 7 chars) ATTACK")
print("=" * 80)

hechllt = 'HECHLLT'
hs = sorted(hechllt)
print(f"  Letters: {hs} (C,E,H,H,L,L,T)")

# LACHELT? (smiles) = L,A,C,H,E,L,T - needs A, we have H
# HECHELT? Not standard
# SCHLECHT (bad) = S,C,H,L,E,C,H,T - needs S and 2 C's
# What about splitting?
print(f"  Two-word splits:")
for split in range(2, len(hechllt) - 1):
    left = hechllt[:split]
    right = hechllt[split:]
    ls = ''.join(sorted(left))
    rs = ''.join(sorted(right))
    lm = anagram_dict.get(ls, [])
    rm = anagram_dict.get(rs, [])
    if lm or rm:
        print(f"    {left}|{right}: left={lm if lm else '-'}, right={rm if rm else '-'}")

# HECHT (pike fish) = H,E,C,H,T - 5 letters, would leave L,L
# LICHT (light) = L,I,C,H,T - needs I not E,H,L
# LECHTE? Not standard
# MHG: HELLE (hell/bright) = H,E,L,L,E - needs 2 E's
# STELLEN? Too many letters
# HECHEL (hackle/comb) = H,E,C,H,E,L - 6 letters, needs 2 E's

print(f"\n  Checking HECHT (pike) + LL:")
print(f"    HECHT sorted = {sorted('HECHT')}")
print(f"    remaining = LL")
print(f"    HECHT is a real German word (pike fish)")

# Context
print(f"\n  HECHLLT contexts:")
for bidx, left, right in garbled_blocks.get('HECHLLT', []):
    print(f"    Book {bidx}: {left} | HECHLLT | {right}")

# ================================================================
# 13. {CHN} (8x) ATTACK
# ================================================================
print(f"\n{'=' * 80}")
print("13. CHN (8x, 3 chars) ATTACK")
print("=" * 80)

chn_occs = garbled_blocks.get('CHN', [])
print(f"  {{CHN}} {len(chn_occs) if chn_occs else 0}x")
if chn_occs:
    print(f"  Contexts:")
    for bidx, left, right in chn_occs[:5]:
        print(f"    Book {bidx}: {left} | CHN | {right}")

# CHN -> anagram?
matches = anagram_dict.get(''.join(sorted('CHN')), [])
print(f"  Exact anagram: {matches}")

# Always appears as: ...IN {{CHN}} ES...
# What if this is actually INCH? or part of NICHT?
# NICHT = N,I,C,H,T
# IN + CHN -> INCHN... not helpful
# What about: ...IN CHN ES... = INCHNES?
# Or: the segmentation is wrong and it should be: ...I NCHNE S...
# NCHEN? Like -NCHEN suffix (diminutive)?

print(f"\n  Pattern: 'IN {{CHN}} ES' -- could CHN be part of a word?")
print(f"  Testing: INCHNES, NCHNES, etc.")

print(f"\nDone.")
