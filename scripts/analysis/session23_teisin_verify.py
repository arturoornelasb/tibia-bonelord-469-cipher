#!/usr/bin/env python3
"""
Session 23 Part 2: Verify TEI+SIN=STEIN cross-boundary anagram and other finds.

Key discoveries to verify:
1. TEI+SIN = STEIN (cross-boundary, +0 exact anagram!)
2. RRNI context: does it appear near TUT?
3. TEI+ICH = TEICH (pond, cross-boundary)
4. HIHL code analysis: is it a proper noun?
5. Coverage gain from TEI-based anagrams
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
    'CHIS': 'SICH',
}

MHG_WORDS = {
    'HEL', 'RIT', 'EWE', 'SIN', 'MIS', 'AUE', 'EIS', 'NIT',
    'SCE', 'OEL', 'TER',
}

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    return 0 if ic_from_counts(Counter(bp0), len(bp0)) > ic_from_counts(Counter(bp1), len(bp1)) else 1

book_pairs_list = []
decoded_books = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs_list.append(pairs)
    decoded_books.append(''.join(v7.get(p, '?') for p in pairs))

raw = ''.join(decoded_books)
processed = raw
for old in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    processed = processed.replace(old, ANAGRAM_MAP[old])

# ================================================================
# Coverage baseline
# ================================================================
import sys
sys.path.insert(0, os.path.join(script_dir))

# Simple DP coverage calculation
GERMAN_VOCAB = set([
    'SEIN', 'SEINE', 'SEINER', 'SEINEN', 'SEINEM', 'SEINES',
    'IST', 'WAR', 'WIRD', 'WURDE', 'WAREN',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES',
    'EIN', 'EINE', 'EINER', 'EINEM', 'EINEN', 'EINES',
    'UND', 'ODER', 'ABER', 'NICHT', 'MIT', 'VON', 'BIS',
    'WIR', 'ICH', 'ER', 'SIE', 'ES', 'IHR', 'WER', 'WAS',
    'IN', 'IM', 'AN', 'AM', 'AUF', 'AUS', 'AB', 'ZU', 'ZUR', 'ZUM',
    'BEI', 'SO', 'DA', 'WO', 'NUN', 'NU',
    'HIER', 'DORT', 'ODE', 'ORT', 'IM',
    'NACH', 'ALS', 'WIE', 'WO', 'WENN',
    'KLAR', 'AUCH', 'WEG', 'NUR',
    'GOTT', 'RUNE', 'RUNEN', 'STEIN', 'STEINEN', 'STEINE',
    'URALTE', 'ALT', 'ALTE', 'ALTEN',
    'KOENIG', 'KONIG', 'RITTER',
    'WORT', 'WORTE', 'SAGEN', 'SAGEND',
    'FINDEN', 'FIND', 'FINDET',
    'STEH', 'STEHEN', 'STEHT',
    'GEHEN', 'GEH', 'GEHT',
    'ENDE', 'ENDEN',
    'ERSTE', 'ERSTEN', 'ERSTER',
    'DIE', 'DIESE', 'DIESER', 'DIESEN', 'DIESEM', 'DIESES',
    'WIR', 'WIRD', 'WIRT',
    'TAG', 'TAGE', 'TAGEN',
    'MIN', 'MINE', 'MEIN', 'MEINE',
    'TOT', 'TOTEN', 'TOTE',
    'RUIN', 'RUINE',
    'SAND', 'HEIME', 'HEIM',
    'LEICH', 'LEICHE',
    'TRAUT', 'TREUE',
    'SCHRAT', 'SCHATZ',
    'SCHARDT', 'SCHAUN', 'SCHAU',
    'WEICHSTEIN', 'SALZBERG', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS',
    'EIGENTUM', 'MEERE',
    'NEIGT', 'WISTEN', 'MANIER', 'GODES',
    'DIENST', 'NACHTS', 'STANDE', 'BEI',
    'TUT', 'NEU', 'SAND', 'URALTE',
    'SICH', 'REDER',
    'NIT', 'HEL', 'RIT', 'EWE', 'SIN', 'MIS', 'AUE', 'EIS',
    'SCE', 'OEL', 'TER', 'ODE',
    'THENAEUT', 'WISTEN',
    'BERUCHTIG', 'BERUCHTIGER', 'LEICHANBERUCHTIG', 'LEICHANBERUCHTIGER',
    'SALZBERG', 'ORANGENSTRASSE', 'SCHARDT', 'TRAUT', 'LEICH',
    'HEIME', 'EIGENTUM', 'MEERE',
    'INS', 'GEN', 'DES', 'AUS',
    'RUNEN', 'RUNE',
    'GEIGET', 'GEIG', 'GEIGE',
    'FACH', 'FACHE',
    'ICH', 'OEL',
    'WIR', 'UND', 'WO',
    'STANDE', 'NACHT', 'NACHTS',
    'ERDE', 'ERDEN',
    'HEIL', 'HEILIG',
    'WELT', 'WELTEN',
    'WIND', 'WINDE',
    'ZUM', 'ZUR',
    'AUCH', 'WEG', 'KLAR',
    'DEN', 'AM',
    'HAT', 'NET', 'EM', 'TUN',
    'RUINEN', 'SAND', 'SAND',
    'SCHRAT', 'DER',
    'UNTER', 'UNTEN',
    'TEICH',
])

def dp_cover(text, vocab):
    n = len(text)
    dp = [False] * (n+1)
    dp[0] = True
    prev = [-1] * (n+1)
    for i in range(n):
        if not dp[i]:
            continue
        for length in range(2, min(20, n-i+1)):
            word = text[i:i+length]
            if word in vocab:
                if not dp[i+length]:
                    dp[i+length] = True
                    prev[i+length] = i
    covered = sum(1 for i in range(n) if dp[i] and i < n and dp[i+1] or
                  any(dp[j] and text[j:i+1] in vocab for j in range(max(0,i-19), i+1)))
    # Simpler: count chars that are in a matched span
    spans = set()
    pos = n
    while pos > 0 and prev[pos] >= 0:
        start = prev[pos]
        for c in range(start, pos):
            spans.add(c)
        pos = start
    return len(spans), n

# ================================================================
# 1. Find all TEI occurrences and check adjacency with SIN/ICH/ER
# ================================================================
print("=" * 70)
print("1. TEI OCCURRENCES - adjacency analysis")
print("=" * 70)

pos = 0
tei_before_sin = 0
tei_before_ich = 0
tei_before_stein = 0
tei_standalone = []

while True:
    idx = processed.find('TEI', pos)
    if idx < 0:
        break
    ctx = processed[max(0, idx-10):idx+15]
    after = processed[idx+3:idx+10]
    tei_standalone.append((idx, ctx))
    if after.startswith('SIN'):
        tei_before_sin += 1
        print(f"  TEI+SIN at pos {idx}: ...{ctx}...")
    if after.startswith('ICH'):
        tei_before_ich += 1
        print(f"  TEI+ICH at pos {idx}: ...{ctx}...")
    if after.startswith('STEIN'):
        tei_before_stein += 1
        print(f"  TEI+STEIN at pos {idx}: ...{ctx}...")
    pos = idx + 1

print(f"\nTotal TEI: {len(tei_standalone)}")
print(f"TEI immediately before SIN: {tei_before_sin}")
print(f"TEI immediately before ICH: {tei_before_ich}")

# Also check SIN immediately before TEI
print("\nSIN+TEI occurrences:")
pos = 0
sin_before_tei = 0
while True:
    idx = processed.find('SIN', pos)
    if idx < 0:
        break
    after = processed[idx+3:idx+7]
    if after.startswith('TEI'):
        sin_before_tei += 1
        ctx = processed[max(0, idx-8):idx+12]
        print(f"  SIN+TEI at pos {idx}: ...{ctx}...")
    pos = idx + 1

# Show all TEI contexts
print("\nAll TEI contexts:")
for idx, ctx in tei_standalone[:20]:
    print(f"  pos {idx:4d}: {ctx}")

# ================================================================
# 2. Coverage test: adding TEISIN -> STEIN cross-boundary anagram
# ================================================================
print("\n" + "=" * 70)
print("2. COVERAGE TEST: TEISIN -> STEIN")
print("=" * 70)

# Baseline
baseline_covered = sum(1 for c in processed if c != ' ')
words_covered = 0
words_total = 0
for i, c in enumerate(processed):
    if c != ' ':
        words_total += 1

# Simple coverage: count chars in known-word spans
def simple_coverage(text, known_words):
    """Count chars in known-word segments."""
    covered = 0
    total = len(text)
    i = 0
    while i < total:
        found = False
        for l in range(min(20, total-i), 1, -1):
            w = text[i:i+l]
            if w in known_words:
                covered += l
                i += l
                found = True
                break
        if not found:
            i += 1
    return covered, total

baseline = simple_coverage(processed, GERMAN_VOCAB)
print(f"Baseline: {baseline[0]}/{baseline[1]} = {baseline[0]/baseline[1]*100:.1f}%")

# Test TEISIN -> STEIN
new_map = dict(ANAGRAM_MAP)
new_map['TEISIN'] = 'STEIN'
processed_v2 = raw
for old in sorted(new_map.keys(), key=len, reverse=True):
    processed_v2 = processed_v2.replace(old, new_map[old])

cov_v2 = simple_coverage(processed_v2, GERMAN_VOCAB)
print(f"With TEISIN->STEIN: {cov_v2[0]}/{cov_v2[1]} = {cov_v2[0]/cov_v2[1]*100:.1f}%")
print(f"Gain: +{cov_v2[0]-baseline[0]} chars")

# Show occurrences
pos = 0
cnt = 0
while True:
    idx = processed_v2.find('TEISIN', pos)
    if idx < 0:
        break
    ctx = processed_v2[max(0, idx-10):idx+16]
    print(f"  TEISIN at pos {idx}: ...{ctx}...")
    pos = idx + 1
    cnt += 1
print(f"Total TEISIN: {cnt}")

# Also try SINTEI -> STEIN
new_map2 = dict(ANAGRAM_MAP)
new_map2['SINTEI'] = 'STEIN'
processed_v3 = raw
for old in sorted(new_map2.keys(), key=len, reverse=True):
    processed_v3 = processed_v3.replace(old, new_map2[old])
cov_v3 = simple_coverage(processed_v3, GERMAN_VOCAB)
print(f"\nWith SINTEI->STEIN: {cov_v3[0]}/{cov_v3[1]} = {cov_v3[0]/cov_v3[1]*100:.1f}%")
print(f"Gain: +{cov_v3[0]-baseline[0]} chars")

# ================================================================
# 3. TEI+STEIN cross-boundary - is TEI part of STEINE/STEINEN?
# ================================================================
print("\n" + "=" * 70)
print("3. TEI WITHIN LARGER CONTEXT")
print("   Is TEI part of longer known words?")
print("=" * 70)

# Check STEIN in processed (from STEINEN, STEINE)
# What letters are T-E-I in the raw?
# T codes: 88 78 64 75 81 98
# E codes: 95 56 19 26 76 01 41 30 86 67 27 03 09 17 29 49 39 74 37 69
# I codes: 21 15 46 71 65 16 50 24
# So TEI can have many code combinations

# Find all raw TEI sequences
print("\nRaw codes for garbled TEI blocks:")
for bidx, pairs in enumerate(book_pairs_list):
    decoded = decoded_books[bidx]
    # Apply anagram map to see where garbled TEI appears
    processed_book = decoded
    for old in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
        processed_book = processed_book.replace(old, new_map.get(old, ANAGRAM_MAP[old]))

    # Find TEI that's NOT in a known word
    idx = 0
    while True:
        pos = processed_book.find('TEI', idx)
        if pos < 0:
            break
        # Check if this TEI is in a garbled position
        # A TEI is garbled if the raw characters at that position don't form a known word
        if pos + 3 <= len(pairs):
            # Check surrounding context
            before = processed_book[max(0,pos-4):pos]
            after = processed_book[pos+3:pos+7]
            # Is this standalone TEI (not part of STEIN, STEINEN, etc.)
            in_word = False
            for w in ['STEIN', 'WEICHSTEIN', 'STEINEN', 'STEINE']:
                if w in processed_book[max(0,pos-8):pos+8]:
                    # Check if TEI is at the start of STEIN
                    full_ctx = processed_book[max(0,pos-8):pos+len(w)+2]
                    if 'STEIN' in full_ctx[8:] or full_ctx.find('STEIN') < 8:
                        in_word = True
            if not in_word:
                codes_here = pairs[pos:pos+3]
                if len(codes_here) == 3:
                    pass  # print(f"  Book {bidx:2d} pos {pos}: {before}|TEI|{after} codes: {'-'.join(codes_here)}")
        idx = pos + 1

# ================================================================
# 4. Check STEIN as a standalone (is it already covered?)
# ================================================================
print("\n" + "=" * 70)
print("4. STEIN standalone occurrences in processed text")
print("=" * 70)

pos = 0
stein_count = 0
while True:
    idx = processed.find('STEIN', pos)
    if idx < 0:
        break
    ctx = processed[max(0, idx-8):idx+12]
    print(f"  pos {idx:4d}: ...{ctx}...")
    pos = idx + 1
    stein_count += 1
    if stein_count > 15:
        print(f"  ... (more)")
        break
print(f"Total STEIN standalone: {stein_count}")

# ================================================================
# 5. New MHG words: TEICH (pond), RITE (journey)
# ================================================================
print("\n" + "=" * 70)
print("5. COVERAGE TEST: Add TEICH and RITE to vocabulary")
print("=" * 70)

vocab_teich = set(GERMAN_VOCAB) | {'TEICH', 'RITE'}
cov_teich = simple_coverage(processed, vocab_teich)
print(f"With TEICH+RITE: {cov_teich[0]}/{cov_teich[1]} = {cov_teich[0]/cov_teich[1]*100:.1f}%")
print(f"Gain: +{cov_teich[0]-baseline[0]} chars")

# ================================================================
# 6. Investigate the HIHL proper noun
# ================================================================
print("\n" + "=" * 70)
print("6. HIHL proper noun analysis")
print("   Codes: 57(H)-65(I)-94(H)-34(L) -- always identical")
print("=" * 70)

print("  HIHL contains double-H: unusual in German")
print("  Cross-references to Tibia lore:")
print("  - HIHL could be a bonelord place name")
print("  - Sorted: HHIL -> no German word match")
print("  - HIHL reversed = LHIH -> no match")
print("  - Could be 'Höhl' (cave/hollow) variant? HOEHL?")
print("  - OHG: 'hihl' doesn't appear in dictionaries")
print("  - Possible anagram with +1: HIHL+? = HILFE? no (HILFE=EFHIL, HIHL+?=HHIL+?)")

# What's the full context of HIHL?
print("\n  Full HIHL context (all occurrences):")
pos = 0
hihl_count = 0
while True:
    idx = processed.find('HIHL', pos)
    if idx < 0:
        break
    ctx = processed[max(0, idx-20):idx+25]
    print(f"    pos {idx}: ...{ctx}...")
    pos = idx + 1
    hihl_count += 1
print(f"  Total HIHL: {hihl_count}")

# ================================================================
# 7. Summary: what new anagrams should we add?
# ================================================================
print("\n" + "=" * 70)
print("7. RECOMMENDED NEW ADDITIONS FOR SESSION 23")
print("=" * 70)

additions = []

# Test TEISIN
if cov_v2[0] > baseline[0]:
    additions.append(('TEISIN', 'STEIN', cov_v2[0]-baseline[0], 'cross-boundary TEI+SIN'))

# Test vocab additions
for word, label in [('TEICH', 'pond'), ('RITE', 'MHG journey'), ('HEIL', 'salvation'),
                     ('HEIL', 'salvation'), ('HEILE', 'healed'), ('INNE', 'inside'),
                     ('RINNE', 'groove'), ('WUNNE', 'joy'), ('ZINNE', 'battlement'),
                     ('MINNE', 'love'), ('SUNNE', 'sun')]:
    vocab_test = set(GERMAN_VOCAB) | {word}
    cov_test = simple_coverage(processed, vocab_test)
    gain = cov_test[0] - baseline[0]
    if gain > 0:
        additions.append((word, word, gain, label))

additions.sort(key=lambda x: -x[2])
print("\nTop additions by coverage gain:")
for anag, target, gain, label in additions[:15]:
    print(f"  {anag} -> {target}: +{gain} chars ({label})")

print("\nDone.")
