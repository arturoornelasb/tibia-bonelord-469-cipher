#!/usr/bin/env python3
"""Validate THARSCR -> SCHRAT (+1 anagram, R extra) and measure coverage."""

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
    'SANGE': 'SAGEN', 'GHNEE': 'GEHEN',
}

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

def dp_count(text, wordset):
    n = len(text)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            if text[start:i] in wordset:
                dp[i] = max(dp[i], dp[start] + wlen)
    return dp[n]

# Baseline with TER
resolved = all_text
for anag in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved = resolved.replace(anag, ANAGRAM_MAP[anag])
total = sum(1 for c in resolved if c != '?')
baseline = dp_count(resolved, KNOWN)
print(f"Baseline (with TER): {baseline}/{total} = {baseline/total*100:.1f}%")

# 1. Verify THARSCR -> SCHRAT
print(f"\n{'=' * 60}")
print("THARSCR -> SCHRAT VALIDATION")
print("=" * 60)

# Verify anagram
print(f"  THARSCR sorted: {''.join(sorted('THARSCR'))}")
print(f"  SCHRAT sorted:  {''.join(sorted('SCHRAT'))}")
print(f"  SCHRAT + R = SCHRATR sorted: {''.join(sorted('SCHRATR'))}")
print(f"  Match: {''.join(sorted('THARSCR'))} == {''.join(sorted('SCHRATR'))}: {''.join(sorted('THARSCR')) == ''.join(sorted('SCHRATR'))}")

# Count occurrences
tharscr_count = all_text.count('THARSCR')
print(f"\n  THARSCR in raw text: {tharscr_count}x")

# Show all contexts
pos = 0
while True:
    idx = resolved.find('THARSCR', pos)
    if idx < 0: break
    ctx_s = max(0, idx-20)
    ctx_e = min(len(resolved), idx+25)
    print(f"    pos {idx}: ...{resolved[ctx_s:ctx_e]}...")
    pos = idx + 1

# But wait: ADTHARSC is already in the anagram map -> SCHARDT
# Does THARSCR overlap with ADTHARSC?
print(f"\n  ADTHARSC in raw text: {all_text.count('ADTHARSC')}x")
print(f"  After ADTHARSC->SCHARDT replacement, THARSCR count: {resolved.count('THARSCR')}x")

# Apply THARSCR -> SCHRAT
new_map = dict(ANAGRAM_MAP)
new_map['THARSCR'] = 'SCHRAT'
new_resolved = all_text
for anag in sorted(new_map.keys(), key=len, reverse=True):
    new_resolved = new_resolved.replace(anag, new_map[anag])
new_total = sum(1 for c in new_resolved if c != '?')

# Add SCHRAT to known
new_known = set(KNOWN)
new_known.add('SCHRAT')
new_cov = dp_count(new_resolved, new_known)
delta = new_cov - baseline
# Adjust for text length change (THARSCR=7 -> SCHRAT=6, saves 1 char each)
print(f"\n  +SCHRAT anagram: {new_cov}/{new_total} = {new_cov/new_total*100:.1f}% ({delta:+d} chars coverage)")

# Show contexts after replacement
print(f"\n  Contexts after THARSCR->SCHRAT:")
pos = 0
while True:
    idx = new_resolved.find('SCHRAT', pos)
    if idx < 0: break
    ctx_s = max(0, idx-20)
    ctx_e = min(len(new_resolved), idx+20)
    print(f"    ...{new_resolved[ctx_s:ctx_e]}...")
    pos = idx + 1

# 2. Also look at ADTHA (5 chars, 2x) - is this a fragment of ADTHARSC?
print(f"\n{'=' * 60}")
print("ADTHA CHECK (appears as garbled block)")
print("=" * 60)
# ADTHA appears where ADTHARSC doesn't match
adtha_count = resolved.count('ADTHA')
print(f"  ADTHA in resolved text: {adtha_count}x")
# Context
pos = 0
while True:
    idx = resolved.find('ADTHA', pos)
    if idx < 0: break
    ctx_s = max(0, idx-15)
    ctx_e = min(len(resolved), idx+20)
    print(f"    pos {idx}: ...{resolved[ctx_s:ctx_e]}...")
    pos = idx + 1

# In raw text?
adtha_raw = all_text.count('ADTHA')
print(f"  ADTHA in raw text: {adtha_raw}x")
# What comes after ADTHA in raw text?
pos = 0
while True:
    idx = all_text.find('ADTHA', pos)
    if idx < 0: break
    after = all_text[idx:idx+15]
    print(f"    raw pos {idx}: {after}")
    pos = idx + 1

# ADTHA might be a truncated ADTHARSC that didn't get the full match
# because of digit split boundary issues

# 3. Also test: does ADTHARSCR exist? (ADTHARSC + R)
print(f"\n  ADTHARSCR in raw text: {all_text.count('ADTHARSCR')}x")

# 4. What about the SCHARDT name appearing directly?
print(f"  SCHARDT in resolved text: {resolved.count('SCHARDT')}x")

print(f"\nDone.")
