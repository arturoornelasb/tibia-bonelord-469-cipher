#!/usr/bin/env python3
"""
Session 19 Part 5: HWND deep investigation + narrative flow analysis.

HWND (4 chars, 8x) always appears before FINDEN.
The phrase "STEH [big garbled block] HWND FINDEN NEIGT DAS ES" repeats.
What is HWND? Can we determine its identity from code patterns?

Also: now at 68.2%, let's look at what the narrative actually says.
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

resolved = all_text
for anag in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved = resolved.replace(anag, ANAGRAM_MAP[anag])

# ================================================================
# 1. HWND: All occurrences with raw codes
# ================================================================
print("=" * 80)
print("1. HWND: Complete occurrence inventory")
print("=" * 80)

# Find all HWND in each book with raw codes
print("\nAll HWND occurrences with codes:")
all_hwnd_codes = []
for bidx, text in enumerate(decoded_books):
    pos = 0
    while True:
        idx = text.find('HWND', pos)
        if idx < 0:
            break
        pairs = book_pairs[bidx]
        if idx + 4 <= len(pairs):
            codes = pairs[idx:idx+4]
            all_hwnd_codes.append(tuple(codes))
            # Context
            ctx_start = max(0, idx-8)
            ctx_end = min(len(text), idx+12)
            ctx = text[ctx_start:ctx_end]
            marker_pos = idx - ctx_start
            print(f"  Book {bidx:2d} pos {idx:3d}: codes {' '.join(codes)} | ...{ctx}...")
        pos = idx + 1

# Check code consistency
print(f"\nHWND code patterns: {Counter(all_hwnd_codes)}")

# What letters would HWND be if codes mapped differently?
# Code 00 -> H, Code 36 -> W, Code 90 -> N, Code 42 -> D
print(f"\nHWND code analysis:")
for code, letter in [('00', 'H'), ('36', 'W'), ('90', 'N'), ('42', 'D')]:
    # How many other letters does this code produce?
    total_occ = sum(text.count(letter) for text in decoded_books)
    # What other codes also produce this letter?
    same_letter_codes = [c for c, l in v7.items() if l == letter]
    print(f"  Code {code} -> {letter} (also from codes: {same_letter_codes})")

# The key question: is code 36=W correct?
# If 36 should be U instead of W, then HWND -> HUND (dog/hound)!
# Let's check what other words use code 36
print(f"\nCode 36 (currently W) in other contexts:")
code36_positions = []
for bidx, pairs in enumerate(book_pairs):
    for pi, pair in enumerate(pairs):
        if pair == '36':
            text = decoded_books[bidx]
            ctx_start = max(0, pi-5)
            ctx_end = min(len(text), pi+6)
            ctx = text[ctx_start:ctx_end]
            rel = pi - ctx_start
            code36_positions.append((bidx, pi, ctx, rel))

print(f"  Code 36 appears {len(code36_positions)} times total")
# Show contexts that are in KNOWN words
for bidx, pi, ctx, rel in code36_positions[:15]:
    print(f"    Book {bidx:2d} pos {pi:3d}: ...{ctx}... (pos {rel})")

# Check: what words contain W in v7?
w_codes = [c for c, l in v7.items() if l == 'W']
print(f"\n  W codes: {w_codes}")

# If 36=U instead of W, what happens to all words containing code 36?
# Count how many times code 36 appears in recognized vs garbled zones
# (We'll approximate: check if the decoded letter W at that position
# is part of a matched word)

# ================================================================
# 2. NARRATIVE FLOW at 68.2%
# ================================================================
print(f"\n{'=' * 80}")
print("2. NARRATIVE SECTIONS (readable parts)")
print("=" * 80)

KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR', 'NU', 'STANDE', 'NACHTS', 'NIT', 'TOT',
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

tokens = dp_segment(resolved, KNOWN)

# Extract the core narrative by showing only long readable runs
print("\n  Longest readable runs (consecutive known words):")
runs = []
current_run = []
for t in tokens:
    if not t.startswith('{'):
        current_run.append(t)
    else:
        if len(current_run) >= 4:
            runs.append(current_run[:])
        current_run = []
if len(current_run) >= 4:
    runs.append(current_run)

runs.sort(key=len, reverse=True)
for run in runs[:20]:
    chars = sum(len(w) for w in run)
    print(f"  [{chars:3d} chars, {len(run)} words]: {' '.join(run)}")

# ================================================================
# 3. COMPLETE READABLE NARRATIVE
# ================================================================
print(f"\n{'=' * 80}")
print("3. FULL NARRATIVE (garbled blocks as [?])")
print("=" * 80)

# Compact: replace garbled blocks with [?] and show the narrative
compact = []
for t in tokens:
    if t.startswith('{'):
        content = t[1:-1]
        if len(content) <= 2:
            compact.append(f'[{content}]')
        else:
            compact.append(f'[{len(content)}?]')
    else:
        compact.append(t)

# Print in wrapped lines
line = ''
for word in compact:
    if len(line) + len(word) + 1 > 100:
        print(f"  {line}")
        line = word
    else:
        line = line + ' ' + word if line else word
if line:
    print(f"  {line}")
