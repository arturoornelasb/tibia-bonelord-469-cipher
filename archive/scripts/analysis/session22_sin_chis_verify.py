#!/usr/bin/env python3
"""
Session 22 Part 3: Verify CHIS->SICH and SIN (MHG) additions.
Also test adding more MHG words to KNOWN set.
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

decoded_books = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    decoded_books.append(''.join(v7.get(p, '?') for p in pairs))

processed = ''.join(decoded_books)
for old in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    processed = processed.replace(old, ANAGRAM_MAP[old])

# Current KNOWN set (baseline)
KNOWN_BASE = set([
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

def dp_segment(text, known_set):
    n = len(text)
    dp = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], None)
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if cand in known_set:
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

# Baseline coverage
_, base_covered = dp_segment(processed, KNOWN_BASE)
total = sum(1 for c in processed if c != '?')
print(f"Baseline coverage: {base_covered}/{total} = {base_covered/total*100:.1f}%")

# ================================================================
# 1. Test CHIS->SICH anagram
# ================================================================
print(f"\n{'='*60}")
print("1. CHIS -> SICH (exact anagram)")
print(f"{'='*60}")

# Find CHIS in processed text
pos = 0
while True:
    idx = processed.find('CHIS', pos)
    if idx < 0: break
    ctx = processed[max(0,idx-12):idx+16]
    print(f"  pos {idx}: ...{ctx}...")
    pos = idx + 1

# Check collision
test = processed.replace('CHIS', 'SICH')
for w in ['NACHTS', 'BERUCHTIG', 'BERUCHTIGER', 'LEICHANBERUCHTIG',
          'LEICHANBERUCHTIGER', 'SCHRAT', 'SCHARDT', 'ORANGENSTRASSE',
          'WEICHSTEIN']:
    oc = processed.count(w)
    nc = test.count(w)
    if nc < oc:
        print(f"  COLLISION: {w}: {oc} -> {nc}")

# Add CHIS->SICH and check gain
test_map = dict(ANAGRAM_MAP)
test_map['CHIS'] = 'SICH'
test_proc = ''.join(decoded_books)
for old in sorted(test_map.keys(), key=len, reverse=True):
    test_proc = test_proc.replace(old, test_map[old])
_, chis_covered = dp_segment(test_proc, KNOWN_BASE)
print(f"  With CHIS->SICH: {chis_covered}/{total} ({chis_covered/total*100:.1f}%), gain: +{chis_covered-base_covered}")

# ================================================================
# 2. Test SIN as KNOWN word
# ================================================================
print(f"\n{'='*60}")
print("2. SIN as MHG word (to be / his)")
print(f"{'='*60}")

known_sin = KNOWN_BASE | {'SIN'}
_, sin_covered = dp_segment(processed, known_sin)
print(f"  With SIN added: {sin_covered}/{total} ({sin_covered/total*100:.1f}%), gain: +{sin_covered-base_covered}")

# Where does SIN appear?
tokens_sin, _ = dp_segment(processed, known_sin)
for i, t in enumerate(tokens_sin):
    if t == 'SIN':
        ctx = ' '.join(tokens_sin[max(0,i-3):i+4])
        print(f"    SIN context: {ctx}")

# ================================================================
# 3. Test batch of MHG words
# ================================================================
print(f"\n{'='*60}")
print("3. Batch MHG word testing")
print(f"{'='*60}")

# Test each word individually
mhg_candidates = [
    'SIN',   # to be (MHG sîn)
    'MIS',   # MHG: wrong, miss
    'WIS',   # MHG: wise, knowing
    'IHR',   # her/their
    'AUE',   # meadow (MHG ouwe)
    'AAL',   # eel
    'EIS',   # ice
    'ERE',   # honor (MHG êre)
    'IRE',   # anger (MHG)
    'IRR',   # astray
    'RIS',   # MHG: twig
    'TOR',   # gate/fool
    'OEN',   # MHG: to harrow
    'ARM',   # poor/arm
    'ANE',   # MHG: without (ohne)
    'EWE',   # MHG: eternity
    'HEL',   # MHG: hell/bright
    'MEI',   # MHG: May
    'MES',   # MHG: knife
    'TIE',   # MHG: deep (tief)
    'RIT',   # MHG: ride (Ritt)
    'WIS',   # MHG: wise
    'GAB',   # gave
    'GIE',   # MHG: went
    'LIT',   # MHG: suffered
    'SAH',   # saw
    'HEIM',  # home (already in KNOWN)
    'OEDE',  # desolate
    'STEINE', # stones (already in)
    'WELT',  # world (already in)
    'MERE',  # MHG: sea, lake
    'SITE',  # MHG: custom, manner
    'HEIL',  # salvation (already in)
    'REIN',  # pure
    'EDEL',  # noble (already in)
    'STEIN', # stone (already in)
    'MEIN',  # my
    'DEIN',  # your
    'GIER',  # greed
    'LEID',  # suffering
    'DRITTE', # third
    'ORTEN',  # places (already in)
    'HORT',  # treasure
    'TRUGEN', # carried/deceived
    'GREIS',  # old man
    'SITTE',  # custom
    'KLAGE',  # lament
    'SCHAR',  # host/troop
    'STREITEN', # to fight
]

gains = []
for word in mhg_candidates:
    if word in KNOWN_BASE:
        continue
    test_known = KNOWN_BASE | {word}
    _, test_cov = dp_segment(processed, test_known)
    gain = test_cov - base_covered
    if gain > 0:
        gains.append((word, gain))

gains.sort(key=lambda x: -x[1])
print(f"\n  Words with positive gain:")
for word, gain in gains:
    print(f"    {word:12s} +{gain} chars")

# ================================================================
# 4. Test combined: all positive gains together
# ================================================================
print(f"\n{'='*60}")
print("4. Combined gains")
print(f"{'='*60}")

# Add all words with gain > 0
combined_known = KNOWN_BASE.copy()
for word, gain in gains:
    combined_known.add(word)

_, combined_covered = dp_segment(processed, combined_known)
print(f"  Combined: {combined_covered}/{total} ({combined_covered/total*100:.1f}%)")
print(f"  Total gain: +{combined_covered-base_covered} chars")

# Also test with CHIS->SICH anagram
combined_map = dict(ANAGRAM_MAP)
combined_map['CHIS'] = 'SICH'
combined_proc = ''.join(decoded_books)
for old in sorted(combined_map.keys(), key=len, reverse=True):
    combined_proc = combined_proc.replace(old, combined_map[old])
_, full_covered = dp_segment(combined_proc, combined_known)
print(f"  Combined + CHIS->SICH: {full_covered}/{total} ({full_covered/total*100:.1f}%)")
print(f"  Total gain: +{full_covered-base_covered} chars")

# Show the words that gained and their contexts
print(f"\n  Contexts for new words:")
tokens_combined, _ = dp_segment(combined_proc, combined_known)
for word, gain in gains:
    contexts = []
    for i, t in enumerate(tokens_combined):
        if t == word:
            ctx = ' '.join(tokens_combined[max(0,i-2):i+3])
            contexts.append(ctx)
    if contexts:
        print(f"\n  {word} (+{gain}):")
        for ctx in contexts[:5]:
            print(f"    {ctx}")

print(f"\nDone.")
