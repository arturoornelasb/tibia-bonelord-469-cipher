#!/usr/bin/env python3
"""
Session 19 Part 3b: Fast garbled block deep analysis.
Focus: decompose big block, investigate HWND/UTRUNR/HIHL, code reliability.
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

def sorted_letters(s):
    return ''.join(sorted(s))

# Extended word list for anagram matching
ALL_WORDS = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR', 'NU', 'STANDE', 'NACHTS',
    'ABER', 'ALLE', 'ALLES', 'ALTE', 'ALTEN', 'ALTER', 'AUCH',
    'BERG', 'BURG', 'DENN', 'DIES', 'DOCH', 'DORT', 'DREI', 'DURCH',
    'EINE', 'EINEM', 'EINEN', 'EINER', 'EINES', 'ENDE', 'ERDE',
    'ERST', 'ERSTE', 'FACH', 'FAND', 'FERN', 'FEST', 'FORT', 'GAR',
    'GANZ', 'GEGEN', 'GEIST', 'GOTT', 'GOLD', 'GRAB', 'GROSS',
    'GRUFT', 'GUT', 'HAND', 'HEIM', 'HELD', 'HERR', 'HIER', 'HOCH',
    'IMMER', 'KANN', 'KLAR', 'KRAFT', 'LAND', 'LANG', 'LICHT',
    'MACHT', 'MEHR', 'MUSS', 'NACH', 'NACHT', 'NAHM', 'NAME', 'NEU',
    'NEUE', 'NEUEN', 'NICHT', 'NIE', 'NOCH', 'ODER', 'ORT', 'ORTEN',
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
    'THENAEUT', 'LABT', 'DIGE', 'WEGE', 'KOENIGS',
    'NAHE', 'NOT', 'NOTH', 'OWI', 'ENGE', 'SEIDEN',
    'ALTES', 'NUT', 'NUTZ', 'HEIL', 'NEID', 'TREU', 'TREUE',
    'SUN', 'DIENST', 'SANG', 'DINC', 'HULDE', 'LANT', 'HERRE',
    'DIENEST', 'GEBOT', 'SCHWUR', 'ORDEN', 'RICHTER', 'DUNKEL',
    'EHRE', 'EDELE', 'SCHULD', 'SEGEN', 'FLUCH', 'RACHE',
    'KOENIG', 'DASS', 'EDEL', 'ADEL',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME', 'SCHARDT',
    # Additional for matching
    'RITTER', 'KNECHT', 'HELFEN', 'WUNDER', 'GEWALT',
    'BRUNNEN', 'LINDEN', 'KIRCHE', 'STIMME', 'KLAGE',
    'GEBEIN', 'SCHWERT', 'SCHILD', 'KREUZ', 'KRONE',
    'FEUER', 'WASSER', 'LUFT', 'HUNGER', 'RUHE',
    'HERREN', 'HULDEN', 'EWIGE', 'EWIGEN',
    'NORDEN', 'SUEDEN', 'WESTEN', 'OSTEN',
    'BRUDER', 'VATER', 'MUTTER',
    'GENADE', 'FRIEDE', 'TUGENT', 'STERBEN',
    'UNTOT', 'UNTOTE', 'LEICHE', 'INSCHRIFT',
])

anagram_idx = defaultdict(list)
for w in ALL_WORDS:
    anagram_idx[sorted_letters(w)].append(w)

# ================================================================
# 1. DECOMPOSE BIG BLOCK WITH ANAGRAM-DP
# ================================================================
print("=" * 80)
print("1. DECOMPOSING: WRLGTNELNRHELUIRUNNHWND (23 chars)")
print("=" * 80)

block = 'WRLGTNELNRHELUIRUNNHWND'
print(f"  Letters: {dict(Counter(block))}")

# DP: find best segmentation using anagram matches
n = len(block)
dp = [(0, None)] * (n + 1)
for i in range(2, n + 1):
    dp[i] = (dp[i-1][0], None)
    for wlen in range(2, min(i, 16) + 1):
        start = i - wlen
        sub = block[start:i]
        key = sorted_letters(sub)
        matches = anagram_idx.get(key, [])
        if matches:
            score = dp[start][0] + wlen
            if score > dp[i][0]:
                dp[i] = (score, (start, matches[0], sub))
        # +1 pattern
        for ci in range(len(sub)):
            reduced = sub[:ci] + sub[ci+1:]
            k2 = sorted_letters(reduced)
            for m in anagram_idx.get(k2, []):
                if len(m) >= 3:
                    score = dp[start][0] + len(m)
                    if score > dp[i][0]:
                        dp[i] = (score, (start, f'{m}+{sub[ci]}', sub))
                    break

words = []
i = n
while i > 0:
    if dp[i][1] is not None:
        start, word, raw = dp[i][1]
        words.append((start, i, word, raw))
        i = start
    else:
        i -= 1
words.reverse()

print(f"\n  Best anagram-DP segmentation ({dp[n][0]}/{n} matched):")
pos = 0
for start, end, word, raw in words:
    if start > pos:
        print(f"    [{pos}:{start}] GARBLED: {block[pos:start]}")
    print(f"    [{start}:{end}] {raw} -> {word}")
    pos = end
if pos < n:
    print(f"    [{pos}:{n}] GARBLED: {block[pos:]}")

# Try manual splits based on known patterns
print(f"\n  Manual split attempts:")
# The block ends with HWND which always precedes FINDEN
# So: [something 19 chars] + HWND
prefix = block[:-4]
print(f"    Prefix without HWND: {prefix} ({len(prefix)} chars)")

# Shorter variant of same block: WRLGTNE (7 chars)
# This appears in "IM NU STEH {WRLGTNE} ES"
# WRLGTNE vs WRLGTNELNRHELUIRUNNHWND
# They share the prefix WRLGTNE
# So the 23-char block = WRLGTNE + LNRHELUIRUNNHWND
# The 7-char version is a truncated form!

short_block = 'WRLGTNE'
print(f"\n  Short variant: {short_block} (7 chars, in 'STEH {{WRLGTNE}} ES')")
print(f"    Shared prefix with big block: {block[:7]}")
print(f"    Extension: {block[7:]}")
extension = block[7:]  # LNRHELUIRUNNHWND (16 chars)
print(f"    Extension: {extension} ({len(extension)} chars)")
print(f"    Extension letters: {dict(Counter(extension))}")

# Could WRLGTNE be an anagram?
key = sorted_letters(short_block)
print(f"\n    WRLGTNE sorted: {key}")
print(f"    Matches: {anagram_idx.get(key, [])}")
# +1
for i in range(len(short_block)):
    reduced = short_block[:i] + short_block[i+1:]
    k = sorted_letters(reduced)
    for m in anagram_idx.get(k, []):
        if len(m) >= 4:
            print(f"    WRLGTNE = {m} + '{short_block[i]}' (+1)")

# ================================================================
# 2. RAW CODES IN BIG BLOCK
# ================================================================
print(f"\n{'=' * 80}")
print("2. RAW CODES IN BIG BLOCK")
print("=" * 80)

# Find in each book
for bidx, text in enumerate(decoded_books):
    pos = text.find(block)
    if pos >= 0:
        pairs = book_pairs[bidx]
        raw_codes = pairs[pos:pos+len(block)]
        print(f"\n  Book {bidx}, position {pos}:")
        for j in range(len(block)):
            code = raw_codes[j] if j < len(raw_codes) else '??'
            letter = block[j]
            print(f"    {j:2d}: code {code} -> {letter}")
        break

# Also find HWND raw codes
print(f"\n  HWND raw code trace:")
for bidx, text in enumerate(decoded_books):
    pos = text.find('HWND')
    if pos >= 0:
        pairs = book_pairs[bidx]
        raw_codes = pairs[pos:pos+4]
        print(f"    Book {bidx}: codes {' '.join(raw_codes)} -> HWND")
        # only show first 3 books
        if sum(1 for t in decoded_books[:bidx+1] if 'HWND' in t) >= 3:
            break

# ================================================================
# 3. UTRUNR PLACE NAME
# ================================================================
print(f"\n{'=' * 80}")
print("3. UTRUNR: Place Name Analysis")
print("=" * 80)

utrunr = 'UTRUNR'
print(f"  Letters: {dict(Counter(utrunr))}")
print(f"  Sorted: {sorted_letters(utrunr)}")
print(f"  Context: ODE {{UTRUNR}} DEN ENDE REDER KOENIG")

# Exact anagram
key = sorted_letters(utrunr)
print(f"  Exact matches: {anagram_idx.get(key, [])}")

# +1 pattern
print("  +1 patterns:")
for i in range(len(utrunr)):
    reduced = utrunr[:i] + utrunr[i+1:]
    k = sorted_letters(reduced)
    for m in anagram_idx.get(k, []):
        if len(m) >= 4:
            print(f"    {utrunr} = {m} + '{utrunr[i]}' (+1)")

# -1 pattern
print("  -1 patterns:")
for letter in 'ABCDEFGHIKLMNORSTUWZ':
    expanded = utrunr + letter
    k = sorted_letters(expanded)
    for m in anagram_idx.get(k, []):
        if len(m) >= 5:
            print(f"    {utrunr} + {letter} = {m}")

# German place names with R,R,U,U,N,T:
# TURNUR? RUNTUN? These are not real places.
# But consider: the narrative mentions SALZBERG and WEICHSTEIN as places.
# UTRUNR could be another fictional Tibia location.
# In the Tibia world: THAIS, CARLIN, VENORE, EDRON, DARASHIA, ANKRAHMUN
# UTRUNR doesn't anagram to any of these.

# Check with KTRUNR variant (appears once)
ktrunr = 'KTRUNR'
print(f"\n  KTRUNR variant (1x):")
print(f"    Sorted: {sorted_letters(ktrunr)}")
print(f"    Matches: {anagram_idx.get(sorted_letters(ktrunr), [])}")
# If UTRUNR and KTRUNR are the same place, code substitution differs:
# U vs K at position 0. That means the first code is different.
# In v7: which codes map to U? And which to K?
u_codes = [c for c, l in v7.items() if l == 'U']
k_codes = [c for c, l in v7.items() if l == 'K']
print(f"    U codes: {u_codes}")
print(f"    K codes: {k_codes}")

# ================================================================
# 4. HIHL: Place Name
# ================================================================
print(f"\n{'=' * 80}")
print("4. HIHL: Place Name Analysis")
print("=" * 80)

hihl = 'HIHL'
print(f"  Letters: {dict(Counter(hihl))}")
print(f"  Sorted: {sorted_letters(hihl)}")
print(f"  Context: SAGEN AM MIN {{HIHL}} DIE {{NDCE}} FACH {{HECHLLT}}")

# -1 pattern (add a letter to find 5-letter words)
print("  -1 patterns:")
for letter in 'ABCDEFGHIKLMNORSTUWZ':
    expanded = hihl + letter
    k = sorted_letters(expanded)
    for m in anagram_idx.get(k, []):
        print(f"    {hihl} + {letter} = {m}")

# HIHL has H,H,I,L - double H is rare in German
# Could be a compound: HI + HL, or H + IHL
# In MHG: "hel" = bright, "hil" = help root
# HIHL might be a place name based on "hell" (bright/Hellgate?)

# ================================================================
# 5. RRNI Investigation
# ================================================================
print(f"\n{'=' * 80}")
print("5. RRNI Investigation")
print("=" * 80)

rrni = 'RRNI'
print(f"  Context: ER {{L}} AB {{RRNI}} WIR/DIE")
print(f"  Sorted: {sorted_letters(rrni)}")

# Exact
print(f"  Exact: {anagram_idx.get(sorted_letters(rrni), [])}")

# +1
print("  +1:")
for i in range(len(rrni)):
    reduced = rrni[:i] + rrni[i+1:]
    k = sorted_letters(reduced)
    for m in anagram_idx.get(k, []):
        print(f"    {rrni} = {m} + '{rrni[i]}' (+1)")

# -1
print("  -1:")
for letter in 'ABCDEFGHIKLMNORSTUWZ':
    expanded = rrni + letter
    k = sorted_letters(expanded)
    for m in anagram_idx.get(k, []):
        print(f"    {rrni} + {letter} = {m}")

# What about L+AB+RRNI combined? = LABRRNI (7 chars)
labrrni = 'LABRRNI'
print(f"\n  LABRRNI (L+AB+RRNI combined):")
print(f"    Sorted: {sorted_letters(labrrni)}")
print(f"    Matches: {anagram_idx.get(sorted_letters(labrrni), [])}")

# E+ER+L+AB+RRNI = EERLABRRNI (10 chars)
# Nah, too many letters

# ABRRNI (6 chars)
abrrni = 'ABRRNI'
print(f"  ABRRNI:")
for letter in 'ABCDEFGHIKLMNORSTUWZ':
    expanded = abrrni + letter
    k = sorted_letters(expanded)
    for m in anagram_idx.get(k, []):
        if len(m) >= 5:
            print(f"    {abrrni} + {letter} = {m}")

# ================================================================
# 6. NDCE Investigation
# ================================================================
print(f"\n{'=' * 80}")
print("6. NDCE: After 'DIE'")
print("=" * 80)

ndce = 'NDCE'
print(f"  Context: DIE {{NDCE}} FACH {{HECHLLT}} ICH OEL")
print(f"  Sorted: {sorted_letters(ndce)}")

# With DIE: DIENDCE = 7 chars
diendce = 'DIENDCE'
print(f"  DIENDCE sorted: {sorted_letters(diendce)}")
print(f"  Matches: {anagram_idx.get(sorted_letters(diendce), [])}")

# Just NDCE
print(f"  NDCE exact: {anagram_idx.get(sorted_letters(ndce), [])}")

# -1
print("  NDCE -1:")
for letter in 'ABCDEFGHIKLMNORSTUWZ':
    expanded = ndce + letter
    k = sorted_letters(expanded)
    for m in anagram_idx.get(k, []):
        print(f"    {ndce} + {letter} = {m}")

# NDCE+FACH = NDCEFACH (8 chars)
ndcefach = 'NDCEFACH'
print(f"\n  NDCEFACH sorted: {sorted_letters(ndcefach)}")
# Any word?
matches = anagram_idx.get(sorted_letters(ndcefach), [])
print(f"  Matches: {matches}")

# ================================================================
# 7. HECHLLT Investigation
# ================================================================
print(f"\n{'=' * 80}")
print("7. HECHLLT Investigation")
print("=" * 80)

hechllt = 'HECHLLT'
print(f"  Context: FACH {{HECHLLT}} ICH OEL")
print(f"  Letters: {dict(Counter(hechllt))}")
print(f"  Sorted: {sorted_letters(hechllt)}")

# Exact
print(f"  Exact: {anagram_idx.get(sorted_letters(hechllt), [])}")

# +1
print("  +1:")
for i in range(len(hechllt)):
    reduced = hechllt[:i] + hechllt[i+1:]
    k = sorted_letters(reduced)
    for m in anagram_idx.get(k, []):
        if len(m) >= 4:
            print(f"    {hechllt} = {m} + '{hechllt[i]}' (+1)")

# +2
print("  +2:")
for i in range(len(hechllt)):
    for j in range(i+1, len(hechllt)):
        reduced = hechllt[:i] + hechllt[i+1:j] + hechllt[j+1:]
        k = sorted_letters(reduced)
        for m in anagram_idx.get(k, []):
            if len(m) >= 4:
                print(f"    {hechllt} = {m} + '{hechllt[i]}','{hechllt[j]}' (+2)")

# ================================================================
# 8. PHRASE: NLNDEF before SAGEN
# ================================================================
print(f"\n{'=' * 80}")
print("8. NLNDEF Investigation")
print("=" * 80)

nlndef = 'NLNDEF'
print(f"  Context: DU {{NLNDEF}} SAGEN AM MIN {{HIHL}}")
print(f"  Sorted: {sorted_letters(nlndef)}")

# This appears after DU (you) and before SAGEN (tell/say)
# "Du [NLNDEF] sagen am min [HIHL]"
# = "You [?] tell/say at my [?]"
# NLNDEF could be a verb or adverb

print(f"  Exact: {anagram_idx.get(sorted_letters(nlndef), [])}")

# +1
print("  +1:")
for i in range(len(nlndef)):
    reduced = nlndef[:i] + nlndef[i+1:]
    k = sorted_letters(reduced)
    for m in anagram_idx.get(k, []):
        if len(m) >= 4:
            print(f"    {nlndef} = {m} + '{nlndef[i]}' (+1)")

# -1
print("  -1:")
for letter in 'ABCDEFGHIKLMNORSTUWZ':
    expanded = nlndef + letter
    k = sorted_letters(expanded)
    for m in anagram_idx.get(k, []):
        if len(m) >= 5:
            print(f"    {nlndef} + {letter} = {m}")

# NLNDEF sorted = DEFLNN. FINDEN sorted = DEFINN.
# Diff: NLNDEF has L,N,N vs FINDEN has I,N,N
# So NLNDEF is like FINDEN but L instead of I
# If code for I is wrong and should be L... or vice versa
# This is suspicious. Check which codes produce NLNDEF
print(f"\n  NLNDEF raw codes:")
for bidx, text in enumerate(decoded_books):
    pos = text.find('NLNDEF')
    if pos >= 0:
        pairs = book_pairs[bidx]
        raw_codes = pairs[pos:pos+6]
        finden_comparison = []
        for j, (code, letter) in enumerate(zip(raw_codes, 'NLNDEF')):
            finden_letter = 'FINDEN'[j]
            match = '=' if letter == finden_letter else f'!={finden_letter}'
            finden_comparison.append(f'{code}->{letter}({match})')
        print(f"    Book {bidx}: {' '.join(finden_comparison)}")
        break

# Check FINDEN codes for comparison
print(f"  FINDEN raw codes:")
for bidx, text in enumerate(decoded_books):
    pos = text.find('FINDEN')
    if pos >= 0:
        pairs = book_pairs[bidx]
        raw_codes = pairs[pos:pos+6]
        print(f"    Book {bidx}: {' '.join(f'{c}->{v7[c]}' for c in raw_codes)}")
        break

# ================================================================
# 9. TTUIGAA / TTUIGGWI - recurring pattern
# ================================================================
print(f"\n{'=' * 80}")
print("9. TTUIGAA / TTUIGGWI Patterns")
print("=" * 80)

for block_name in ['TTUIGAA', 'TTUIGGWI', 'TIURIT']:
    key = sorted_letters(block_name)
    print(f"\n  {block_name}:")
    print(f"    Sorted: {key}")
    print(f"    Exact: {anagram_idx.get(key, [])}")
    # +1
    for i in range(len(block_name)):
        reduced = block_name[:i] + block_name[i+1:]
        k = sorted_letters(reduced)
        for m in anagram_idx.get(k, []):
            if len(m) >= 4:
                print(f"    +{block_name[i]}: {m}")
                break

print(f"\n{'=' * 80}")
print("SESSION 19 DEEP ANALYSIS COMPLETE")
print("=" * 80)
