#!/usr/bin/env python3
"""
Session 19 Part 3: Deep attack on remaining garbled blocks.

Focus areas:
1. The huge WRLGTNELNRHELUIRUNNHWND block (23 chars, 4x)
2. HWND always before FINDEN - what is it?
3. RRNI pattern (5x, after "ER L AB")
4. UTRUNR identity (7x place name)
5. HIHL identity (8x place name)
6. Pattern analysis: do garbled blocks form a consistent sub-narrative?
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

# Decode
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

# Apply current anagrams
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

# ================================================================
# 1. DECOMPOSE THE BIG BLOCK
# ================================================================
print("=" * 80)
print("1. BIG BLOCK: WRLGTNELNRHELUIRUNNHWND (23 chars)")
print("=" * 80)

block = 'WRLGTNELNRHELUIRUNNHWND'
print(f"  Context: IM NU STEH [{block}] FINDEN NEIGT DAS")
print(f"  Letters: {dict(Counter(block))}")
print(f"  Total: {len(block)} chars")

# The block appears between STEH and FINDEN
# In the narrative: "in now stand [???] find inclines/bows that it..."
# What words could be hiding?

# Strategy: try to split into 2-4 words
# HWND is always at the end, always before FINDEN
# So: [prefix] + HWND + FINDEN
# HWND has 4 chars: H,W,N,D

# What's the prefix? WRLGTNELNRHELUIRUNN (19 chars)
prefix = block[:-4]  # WRLGTNELNRHELUIRUNN
suffix = block[-4:]  # HWND
print(f"\n  Split: [{prefix}] + [{suffix}]")
print(f"  Prefix letters: {dict(Counter(prefix))}")
print(f"  Suffix letters: {dict(Counter(suffix))}")

# HWND: could be a garbled proper noun
# Or: could include first letter of FINDEN
# HWNDF sorted = DFHNW. No obvious match.

# Try splitting prefix into words
# Look for known word substrings from the right side
from itertools import combinations

# Build word lookup
KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR', 'NU',
    'STANDE', 'NACHTS',
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
    'THENAEUT', 'LABT', 'MORT', 'DIGE', 'WEGE',
    'KOENIGS', 'NAHE', 'NOT', 'NOTH', 'ZUR', 'OWI',
    'ENGE', 'SEIDEN', 'ALTES', 'BIS',
    'NUT', 'NUTZ', 'HEIL', 'NEID', 'TREU', 'TREUE',
    'SUN', 'DIENST', 'SANG', 'DINC', 'HULDE',
    'LANT', 'HERRE', 'DIENEST',
    'GEBOT', 'SCHWUR', 'ORDEN', 'RICHTER', 'DUNKEL',
    'EHRE', 'EDELE', 'SCHULD', 'SEGEN', 'FLUCH', 'RACHE',
    'KOENIG', 'DASS', 'EDEL', 'ADEL',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME',
    'SCHARDT',
])

def sorted_letters(s):
    return ''.join(sorted(s))

anagram_idx = defaultdict(list)
for w in KNOWN:
    anagram_idx[sorted_letters(w)].append(w)

# Try: is any prefix of the block an anagram of a known word?
print(f"\n  Prefix anagram matches (block[:n]):")
for n in range(3, len(block)):
    sub = block[:n]
    key = sorted_letters(sub)
    matches = anagram_idx.get(key, [])
    if matches:
        rest = block[n:]
        print(f"    [{sub}] = {matches}, rest = [{rest}]")

# Try: is any suffix of the block an anagram?
print(f"\n  Suffix anagram matches (block[n:]):")
for n in range(1, len(block)-2):
    sub = block[n:]
    key = sorted_letters(sub)
    matches = anagram_idx.get(key, [])
    if matches:
        print(f"    [{block[:n]}] + [{sub}] = {matches}")

# DP on the block treating anagram matches as valid words
# Find all possible anagram matches at each position
print(f"\n  DP anagram segmentation of the block:")
n = len(block)
# For each position, find all anagram matches ending there
dp = [(0, None)] * (n + 1)
for i in range(3, n + 1):
    dp[i] = (dp[i-1][0], None)
    for wlen in range(2, min(i, 15) + 1):
        start = i - wlen
        sub = block[start:i]
        key = sorted_letters(sub)
        matches = anagram_idx.get(key, [])
        if matches:
            # Use longest match
            score = dp[start][0] + wlen
            if score > dp[i][0]:
                dp[i] = (score, (start, matches[0], sub))

# Backtrack
words_found = []
i = n
while i > 0:
    if dp[i][1] is not None:
        start, word, raw = dp[i][1]
        words_found.append((start, i, word, raw))
        i = start
    else:
        i -= 1
words_found.reverse()
print(f"    Best segmentation ({dp[n][0]}/{n} chars matched):")
pos = 0
for start, end, word, raw in words_found:
    if start > pos:
        print(f"      [{pos}:{start}] garbled: {block[pos:start]}")
    print(f"      [{start}:{end}] {raw} -> {word}")
    pos = end
if pos < n:
    print(f"      [{pos}:{n}] garbled: {block[pos:]}")

# ================================================================
# 2. CODE-LEVEL ANALYSIS OF BIG BLOCK
# ================================================================
print(f"\n{'=' * 80}")
print("2. RAW CODES IN BIG BLOCK")
print("=" * 80)

# Find which book/position the block comes from and get raw codes
# Search in each decoded book
for bidx, text in enumerate(decoded_books):
    pos = text.find(block)
    if pos >= 0:
        # Get the raw pairs for this region
        pairs = book_pairs[bidx]
        # pos in decoded text = pair index
        raw_codes = pairs[pos:pos+len(block)]
        print(f"\n  Book {bidx}, position {pos}:")
        print(f"    Codes: {' '.join(raw_codes)}")
        print(f"    Letters: {' '.join(v7.get(c,'?') for c in raw_codes)}")
        # Show code->letter mapping for each
        for j, (code, letter) in enumerate(zip(raw_codes, block)):
            other_uses = sum(1 for bk in decoded_books for i, c in enumerate(bk) if c == letter)
            print(f"      [{j:2d}] code {code} -> {letter}")
        break  # Just show first occurrence

# ================================================================
# 3. HWND INVESTIGATION
# ================================================================
print(f"\n{'=' * 80}")
print("3. HWND INVESTIGATION")
print("=" * 80)

print("  HWND always precedes FINDEN (to find)")
print("  Letters: H, W, N, D")
print("  Sorted: DHNW")
print()

# What 4-letter German words have these letters?
candidates = ['HUND', 'WAND', 'WAHN', 'HAND', 'WEND', 'WIND']
for c in candidates:
    match = sorted_letters(c) == sorted_letters('HWND')
    if match:
        print(f"  HWND = {c}? sorted match: YES")
    else:
        diff = set(c) - set('HWND')
        missing = set('HWND') - set(c)
        if len(diff) <= 1:
            print(f"  HWND ~ {c}? diff: +{diff} -{missing}")

# HWND sorted = DHNW
# HUND sorted = DHNU -> W vs U mismatch
# WAND sorted = ADNW -> H vs A mismatch
# None match exactly. HWND is likely a proper noun or a garbled word.

# Check if HWND could be part of a longer word with FINDEN
hwndfinden = 'HWNDFINDEN'
key = sorted_letters(hwndfinden)
matches = anagram_idx.get(key, [])
print(f"\n  HWNDFINDEN sorted: {key}")
print(f"  Anagram matches: {matches}")

# What about just HWND as a place name from the Tibia world?
# In Tibia, there are places like: Edron, Thais, Carlin, Ab'Dendriel
# HWND doesn't match any obvious Tibia location

# ================================================================
# 4. RRNI INVESTIGATION
# ================================================================
print(f"\n{'=' * 80}")
print("4. RRNI INVESTIGATION")
print("=" * 80)

# RRNI appears 5x, always after "ER L AB"
# Context: "ER {L} AB {RRNI} WIR/DIE"
# "ER L AB RRNI WIR" = "he L from RRNI we"
# L is also garbled here

# Could L+AB+RRNI be one word? LABRRNI = 7 chars
labrrni = 'LABRRNI'
key = sorted_letters(labrrni)
matches = anagram_idx.get(key, [])
print(f"  LABRRNI sorted: {key}, matches: {matches}")

# Could ERLAB be something?
erlab = 'ERLAB'
key = sorted_letters(erlab)
matches = anagram_idx.get(key, [])
print(f"  ERLAB sorted: {key}, matches: {matches}")

# Or LABR? ABRRNI?
for combo in ['RRNI', 'ABRRNI', 'LABRRNI', 'RRNIWIR']:
    key = sorted_letters(combo)
    matches = anagram_idx.get(key, [])
    if matches:
        print(f"  {combo} -> {matches}")
    # +1/-1
    for i in range(len(combo)):
        reduced = combo[:i] + combo[i+1:]
        k = sorted_letters(reduced)
        for m in anagram_idx.get(k, []):
            if len(m) >= 3:
                print(f"  {combo} = {m} + '{combo[i]}' (+1)")
                break

# RRNI has letters I, N, R, R.
# With double R: could be part of HERRIN (mistress), IRREN (to err)?
# IRREN sorted = EINRR. RRNI sorted = INRR. Missing E.
# RRNI + E = RRNEI sorted = EINRR. But where does the E come from?
# The garbled block after RRNI is usually just WIR...
# What about: ELAB RRNI = ERLAB + RRNI = ELABRRNI
# or the whole phrase: ER L AB RRNI = ERLABRRNI (9 chars)
erlabrrni = 'ERLABRRNI'
key = sorted_letters(erlabrrni)
matches = anagram_idx.get(key, [])
print(f"\n  ERLABRRNI sorted: {key}, matches: {matches}")

# What about: "E ER L AB RRNI WIR"
# The {E} before ER is also garbled. So the full garbled zone is:
# {E} ER {L} AB {RRNI} WIR
# The recognized words are: ER, AB, WIR
# Garbled letters: E, L, RRNI = E + L + R + R + N + I = 6 garbled letters
# Could ELRRNI = IRRE? No, that's only 4. LINER? No.
# E+L+R+R+N+I sorted = EILNRR
# +1 patterns:
for i in range(6):
    test = 'ELRRNI'
    reduced = test[:i] + test[i+1:]
    k = sorted_letters(reduced)
    for m in anagram_idx.get(k, []):
        if len(m) >= 4:
            print(f"  ELRRNI = {m} + '{test[i]}' (+1)")

# ================================================================
# 5. UTRUNR: PLACE NAME CANDIDATE
# ================================================================
print(f"\n{'=' * 80}")
print("5. UTRUNR PLACE NAME ANALYSIS")
print("=" * 80)

# UTRUNR (6 chars) appears 7x, always in "ODE UTRUNR DEN ENDE REDER KOENIG"
# Context: "or UTRUNR the end speech/reder of king SALZBERG"
# This is a place name where the king gave a speech

print("  Context: ODE {UTRUNR} DEN ENDE REDER KOENIG [SALZBERG/LABT]")
print("  Letters: U, T, R, U, N, R")
print(f"  Sorted: {sorted_letters('UTRUNR')}")
print(f"  Letter counts: {dict(Counter('UTRUNR'))}")

# German place names with these letters (R×2, U×2, N, T):
# TURM + NR? RUNTUR? UNRUH?
# Historical German places: NURNBERG -> but that has B,E,G extra
# RUHNT? TURNU? RUNTUR?
# MHG: TURNE (tournament), TURNIER
# Could be: UNTRUE -> not German
# RUTUN? UNTUR? TURNU?

# Check anagram:
key = sorted_letters('UTRUNR')
print(f"  Exact anagram matches: {anagram_idx.get(key, [])}")

# +1 pattern
for i in range(6):
    reduced = 'UTRUNR'[:i] + 'UTRUNR'[i+1:]
    k = sorted_letters(reduced)
    for m in anagram_idx.get(k, []):
        if len(m) >= 4:
            print(f"  UTRUNR = {m} + '{('UTRUNR')[i]}' (+1)")

# -1 pattern (add a letter)
print(f"\n  -1 patterns (UTRUNR + letter):")
for letter in 'ABCDEFGHIKLMNORSTUWZ':
    expanded = 'UTRUNR' + letter
    k = sorted_letters(expanded)
    for m in anagram_idx.get(k, []):
        if len(m) >= 5:
            print(f"    UTRUNR + {letter} = {m}")

# ================================================================
# 6. HIHL: PLACE NAME
# ================================================================
print(f"\n{'=' * 80}")
print("6. HIHL PLACE NAME ANALYSIS")
print("=" * 80)

# HIHL (4 chars) appears 8x, always in "AM MIN HIHL DIE NDCE FACH"
# Context: "at my HIHL the [?] compartment [?]"
# HIHL is a location associated with DIE NDCE FACH (a compartment/section)
print("  Context: SAGEN AM MIN {HIHL} DIE {NDCE} FACH {HECHLLT}")
print("  Letters: H, I, H, L")
print(f"  Sorted: {sorted_letters('HIHL')}")
print(f"  Letter counts: {dict(Counter('HIHL'))}")

# German words: HEIL? No, that's H,E,I,L. HIHL has H,H,I,L
# No common German word has two H's and I,L
# HIHL is likely a proper noun / place name
# In Tibia: could relate to the Hellgate (Holl-/Hell- prefix)

# -1 patterns
print(f"  -1 patterns (HIHL + letter):")
for letter in 'ABCDEFGHIKLMNORSTUWZ':
    expanded = 'HIHL' + letter
    k = sorted_letters(expanded)
    for m in anagram_idx.get(k, []):
        print(f"    HIHL + {letter} = {m}")

# ================================================================
# 7. COMPREHENSIVE: Code-to-letter reliability check
# ================================================================
print(f"\n{'=' * 80}")
print("7. CODE RELIABILITY: Which codes appear most in garbled zones?")
print("=" * 80)

# For each decoded letter position, determine if it's in a garbled zone
# by checking the DP segmentation

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
    # Build coverage mask
    covered = [False] * n
    i = n
    while i > 0:
        if dp[i][1] is not None:
            start, word = dp[i][1]
            for j in range(start, i):
                covered[j] = True
            i = start
        else:
            i -= 1
    return covered

covered = dp_segment(resolved, KNOWN)

# Now trace back to raw codes
# We need position-to-code mapping
all_pairs = []
for bidx, pairs in enumerate(book_pairs):
    all_pairs.extend(pairs)

# Count garbled ratio per code
code_garbled = Counter()
code_total = Counter()
for i, (pair, is_covered) in enumerate(zip(all_pairs, covered[:len(all_pairs)])):
    code_total[pair] += 1
    if not is_covered:
        code_garbled[pair] += 1

# Show codes with highest garbled ratio
print(f"\n  Codes with >50% garbled ratio (min 5 occurrences):")
suspicious = []
for code in sorted(code_total.keys()):
    total = code_total[code]
    garbled = code_garbled[code]
    ratio = garbled / total if total > 0 else 0
    if ratio > 0.5 and total >= 5:
        letter = v7.get(code, '?')
        suspicious.append((code, letter, garbled, total, ratio))

for code, letter, garbled, total, ratio in sorted(suspicious, key=lambda x: -x[4]):
    print(f"    Code {code} -> {letter}: {garbled}/{total} = {ratio:.0%} garbled")

# Also show codes that are NEVER garbled (most reliable)
print(f"\n  Codes with 0% garbled ratio (min 10 occurrences):")
for code in sorted(code_total.keys()):
    total = code_total[code]
    garbled = code_garbled[code]
    if garbled == 0 and total >= 10:
        letter = v7.get(code, '?')
        print(f"    Code {code} -> {letter}: 0/{total} always in known words")

# ================================================================
# 8. TEST: What if some high-garbled codes are WRONG?
# ================================================================
print(f"\n{'=' * 80}")
print("8. SUSPICIOUS CODE ANALYSIS")
print("=" * 80)

# For the most suspicious codes (high garbled ratio), test alternative letters
# and see if coverage improves
print("\n  Testing top-3 most suspicious codes with alternative letters:")

for code, letter, garbled, total, ratio in sorted(suspicious, key=lambda x: -x[4])[:3]:
    print(f"\n  Code {code}: currently {letter} ({garbled}/{total} = {ratio:.0%} garbled)")

    # Get all contexts where this code appears in garbled zones
    contexts = []
    for i, (pair, is_covered) in enumerate(zip(all_pairs, covered[:len(all_pairs)])):
        if pair == code and not is_covered:
            start = max(0, i-5)
            end = min(len(all_pairs), i+6)
            ctx_pairs = all_pairs[start:end]
            ctx_letters = [v7.get(p, '?') for p in ctx_pairs]
            ctx_str = ''.join(ctx_letters)
            rel_pos = i - start
            contexts.append((ctx_str, rel_pos))
    if contexts:
        print(f"  Sample garbled contexts:")
        for ctx, pos in contexts[:3]:
            marker = ' ' * pos + '^'
            print(f"    {ctx}")
            print(f"    {marker}")

    # Test each alternative letter
    best_alt = None
    best_delta = 0
    for alt_letter in 'ABCDEFGHIKLMNORSTUWZ':
        if alt_letter == letter:
            continue
        # Create modified mapping
        alt_v7 = dict(v7)
        alt_v7[code] = alt_letter
        # Redecode
        alt_decoded = []
        for bpairs in book_pairs:
            text = ''.join(alt_v7.get(p, '?') for p in bpairs)
            alt_decoded.append(text)
        alt_all = ''.join(alt_decoded)
        # Apply anagrams
        alt_resolved = alt_all
        for anag in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
            alt_resolved = alt_resolved.replace(anag, ANAGRAM_MAP[anag])
        # Measure coverage
        alt_cov = sum(1 for j in range(len(alt_resolved))
                      if dp_segment(alt_resolved, KNOWN)[j])
        # Actually this is too slow for full text. Use dp_count instead.
    # Skip full alternative testing (too slow), just show contexts
    print(f"  (Full alternative testing skipped - use targeted approach)")

print(f"\n{'=' * 80}")
print("SESSION 19 DEEP ANALYSIS COMPLETE")
print("=" * 80)
