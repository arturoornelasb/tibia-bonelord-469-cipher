#!/usr/bin/env python3
"""
Session 20 Part 5: Decompose the biggest garbled blocks.

Target blocks:
1. WRLGTNELNRHELUIRUNNHWND (23 chars, 4x = 92 garbled chars!)
2. SIUIRUNNHWND (12 chars, 2x = 24 chars) - clearly a suffix of #1
3. RHELUIRUNNHWND (14 chars, 1x) - also a suffix
4. EOIAITOEMEEND (13 chars, 2x = 26 chars)
5. LGTNELGZ (8 chars, 2x = 16 chars)
6. THARSCR (7 chars, 2x = 14 chars)
7. HECHLLT (7 chars, 5x = 35 chars)

Strategy: anagram-DP with MHG lexicon on each block.
"""

import json, os
from collections import Counter
from itertools import combinations

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

# ================================================================
# 1. WRLGTNELNRHELUIRUNNHWND (23 chars) - THE BIG ONE
# ================================================================
print("=" * 80)
print("1. DECOMPOSING WRLGTNELNRHELUIRUNNHWND (23 chars, 4x)")
print("=" * 80)

BIG = "WRLGTNELNRHELUIRUNNHWND"
print(f"\n  Letters: {BIG}")
print(f"  Sorted:  {''.join(sorted(BIG))}")
print(f"  Letter counts: {dict(Counter(BIG))}")

# Known substructures:
# - HWND at the end (4 chars, always before FINDEN)
# - LUIRUNN or UIRUNN also seen in SIUIRUNNHWND
# So the structure might be: [prefix] + [middle] + UIRUNN + HWND
# prefix = WRLGTNE (7 chars), also appears as standalone garbled block!
# middle = LNRHE (5 chars)
# suffix = LUIRUNNHWND (11 chars)

print(f"\n  Structural decomposition:")
print(f"    WRLGTNE (7) + LNRHE (5) + LUIRUNN (7) + HWND (4) = 23")
print(f"    Also seen: WRLGTNE (7, as standalone garbled block)")
print(f"    Also seen: SIUIRUNNHWND (12) = S + IUIRUNN + HWND")
print(f"    Also seen: RHELUIRUNNHWND (14) = RHE + LUIRUNN + HWND")

# LUIRUNNHWND (11 chars) is the stable suffix
# Let's trace raw codes for the full 23-char block
print(f"\n  Raw code trace for WRLGTNELNRHELUIRUNNHWND:")
for bidx, text in enumerate(decoded_books):
    idx = text.find(BIG)
    if idx >= 0:
        pairs = book_pairs[bidx]
        if idx + 23 <= len(pairs):
            codes = pairs[idx:idx+23]
            print(f"    Book {bidx:2d}: {' '.join(codes)}")
            # Show letter-by-letter
            letters = [v7.get(c, '?') for c in codes]
            print(f"            {'  '.join(letters)}")

# Try word fragments within the block
print(f"\n  Known words hidden within WRLGTNELNRHELUIRUNNHWND:")
WORD_LIST = [
    'WELT', 'GOTT', 'RUNE', 'RUNEN', 'RUIN', 'LICHT', 'NACHT',
    'WIND', 'WAND', 'HELD', 'HERR', 'TURM', 'STERN', 'STEIN',
    'LAND', 'BERG', 'BURG', 'WALD', 'GRUFT', 'ERDE',
    'GEN', 'HIN', 'HER', 'NUN', 'NUR', 'EIN', 'ER',
    'RUHE', 'REIN', 'REHN', 'LEHRE', 'LEHR', 'WEHR',
    'LUNGE', 'HUNGER', 'SCHULD',
    # Try anagram fragments
    'ENGEL', 'LUFT', 'HEIL', 'GRUEN',
]

for word in WORD_LIST:
    if word in BIG:
        idx = BIG.index(word)
        print(f"    {word} at position {idx}")

# Now try: can WRLGTNE be an anagram of anything?
wrlgtne_sorted = ''.join(sorted('WRLGTNE'))
print(f"\n  WRLGTNE sorted: {wrlgtne_sorted} (7 letters: E,G,L,N,R,T,W)")
# German 7-letter words with these letters: WERGELT? GELTNER? WENGLTR?
# GELTNER is not a word. WERGELT = Wergeld (blood money)?
# WERGELT has E,E,G,L,R,T,W - but we have E,G,L,N,R,T,W (N vs E)
# So not WERGELT.

# What about 6-letter + 1 extra?
for skip in range(7):
    reduced = 'WRLGTNE'[:skip] + 'WRLGTNE'[skip+1:]
    reduced_sorted = ''.join(sorted(reduced))
    # Check some candidates
    candidates_6 = ['GARTEN', 'WINTER', 'WENIGE', 'ENGELT', 'GELTEN',
                     'LANGER', 'RETTEN', 'WARTEN', 'GLUTEN', 'NUTZER']
    for cand in candidates_6:
        if ''.join(sorted(cand)) == reduced_sorted:
            print(f"    WRLGTNE - '{WRLGTNE[skip]}' = {reduced} -> anagram of {cand}!")

# Try: LNRHE (5 chars in the middle)
lnrhe_sorted = ''.join(sorted('LNRHE'))
print(f"\n  LNRHE sorted: {lnrhe_sorted} (5 letters: E,H,L,N,R)")
# LEHREN? No, that's 6. LERNE? L,E,R,N,E - needs 2 Es. We have 1 E.
# HERNE? Not a word. NEHRL? No.

# LUIRUNN (7 chars)
luirunn_sorted = ''.join(sorted('LUIRUNN'))
print(f"\n  LUIRUNN sorted: {luirunn_sorted} (7 letters: I,L,N,N,R,U,U)")
# Words: LINNUR? RUNNIL? No common German words.

# SIUIRUNN (from SIUIRUNNHWND minus HWND)
siuirunn_sorted = ''.join(sorted('SIUIRUNN'))
print(f"\n  SIUIRUNN sorted: {siuirunn_sorted} (8 letters: I,I,N,N,R,S,U,U)")
# RUINNS? No. INSRUUN? No.

# Full block minus HWND = WRLGTNELNRHELUIRUNN (19 chars)
without_hwnd = 'WRLGTNELNRHELUIRUNN'
wh_sorted = ''.join(sorted(without_hwnd))
print(f"\n  Without HWND: {without_hwnd} ({len(without_hwnd)} chars)")
print(f"  Sorted: {wh_sorted}")
print(f"  Counts: {dict(Counter(without_hwnd))}")

# ================================================================
# 2. APPROACH: Try splitting into 2-3 word-sized pieces via anagram
# ================================================================
print(f"\n{'=' * 80}")
print("2. ANAGRAM-DP ON WRLGTNELNRHELUIRUNNHWND")
print("=" * 80)

# Extended word list for anagram matching
ANAGRAM_WORDS = set([
    # Common German/MHG words (3-8 letters)
    'DER', 'DIE', 'DAS', 'EIN', 'UND', 'IST', 'VON', 'MIT', 'AUF',
    'AUS', 'FUR', 'BEI', 'DURCH', 'GEGEN', 'HINTER', 'NEBEN',
    'WELT', 'GOTT', 'RUNE', 'RUNEN', 'RUIN', 'LICHT', 'NACHT',
    'WIND', 'WAND', 'HELD', 'HERR', 'TURM', 'STERN', 'STEIN',
    'LAND', 'BERG', 'BURG', 'WALD', 'GRUFT', 'ERDE', 'STEH',
    'GEN', 'HIN', 'HER', 'NUN', 'NUR', 'EIN', 'ER', 'TER', 'WIR',
    'RUHE', 'REIN', 'LEHRE', 'LEHR', 'WEHR', 'RINGEN', 'RING',
    'ENGEL', 'LUFT', 'HEIL', 'GRUEN', 'TREUE', 'TREU',
    'NEID', 'HULDE', 'EHRE', 'HEIDE', 'WURM', 'WURZEL',
    'THRON', 'KOENIG', 'RITTER', 'KRIEGER', 'HUNGER',
    'GERICHT', 'RICHTER', 'GERICHT', 'RECHT',
    'NEBEL', 'DUNKEL', 'WINTER', 'SOMMER',
    'TIEFE', 'HOEHE', 'WEITE', 'ENGE', 'STILLE',
    'EWIGEN', 'EWIG', 'HEILIG', 'SCHULD',
    'UNTER', 'UNTEN', 'UEBER', 'INNER', 'INNERE',
    'UNRUH', 'UNRUHE', 'UNHEIL', 'UNGLUECK',
    'RUHIG', 'RUHIGER', 'GELTEN', 'GELTUNG',
    'IRREN', 'IRRE', 'WIRREN', 'WIRR', 'WIRREN',
    'GRUEN', 'GRUENE', 'BRUENNE', 'BRUNNE', 'BRUNNEN',
    'WUERDE', 'TUGEND', 'TAUGEN',
    'STEIN', 'STEINE', 'STEINEN', 'HUND', 'FINDEN',
    'NEIGT', 'HEIDE', 'WEIDE',
    # MHG words
    'SWERT', 'LIUTE', 'VOLKE', 'STRIT', 'GUOTE', 'MAGET',
    'MEIDE', 'LEIT', 'LEIT', 'MINNE', 'MUOT', 'SINNE',
    'TUGENT', 'WUNNE', 'HULDE',
    # Place-related
    'STRASSE', 'GASSE', 'TURM', 'TREPPE', 'GROTTE',
    'TEMPEL', 'KIRCHE', 'KAPELLE',
    # Tibia monsters/concepts
    'WURM', 'DRACHE', 'GEIST', 'WESEN',
])

# For each block, try all ways to split it into 2-3 pieces where
# each piece is an anagram (possibly +1) of a known word
def find_anagram_splits(block, word_list, max_pieces=3):
    """Find ways to split block into pieces that are anagrams of words."""
    results = []
    n = len(block)

    # Try 2-piece splits
    for split1 in range(2, n-1):
        part1 = block[:split1]
        part2 = block[split1:]
        s1 = ''.join(sorted(part1))
        s2 = ''.join(sorted(part2))
        for w1 in word_list:
            if len(w1) == len(part1) and ''.join(sorted(w1)) == s1:
                for w2 in word_list:
                    if len(w2) == len(part2) and ''.join(sorted(w2)) == s2:
                        results.append(((w1, w2), (part1, part2)))

    # Try 3-piece splits (limit range for speed)
    if max_pieces >= 3:
        for split1 in range(2, min(n-3, 12)):
            for split2 in range(split1+2, min(n-1, split1+12)):
                part1 = block[:split1]
                part2 = block[split1:split2]
                part3 = block[split2:]
                s1 = ''.join(sorted(part1))
                s2 = ''.join(sorted(part2))
                s3 = ''.join(sorted(part3))
                match1 = [w for w in word_list if len(w) == len(part1) and ''.join(sorted(w)) == s1]
                if not match1: continue
                match2 = [w for w in word_list if len(w) == len(part2) and ''.join(sorted(w)) == s2]
                if not match2: continue
                match3 = [w for w in word_list if len(w) == len(part3) and ''.join(sorted(w)) == s3]
                if not match3: continue
                for w1 in match1:
                    for w2 in match2:
                        for w3 in match3:
                            results.append(((w1, w2, w3), (part1, part2, part3)))

    return results

# Test on the big block
print(f"\n  Trying 2-3 piece anagram splits of WRLGTNELNRHELUIRUNNHWND:")
splits = find_anagram_splits(BIG, ANAGRAM_WORDS)
if splits:
    for words, parts in splits[:20]:
        print(f"    {' + '.join(words)} <- {' + '.join(parts)}")
else:
    print(f"    No exact anagram splits found")

# Try with HWND separated
print(f"\n  Trying splits of WRLGTNELNRHELUIRUNN (without HWND):")
splits2 = find_anagram_splits(without_hwnd, ANAGRAM_WORDS)
if splits2:
    for words, parts in splits2[:20]:
        print(f"    {' + '.join(words)} + HWND <- {' + '.join(parts)} + HWND")
else:
    print(f"    No exact anagram splits found")

# ================================================================
# 3. HECHLLT (7 chars, 5x = 35 chars)
# ================================================================
print(f"\n{'=' * 80}")
print("3. HECHLLT ANALYSIS (7 chars, 5x)")
print("=" * 80)

block = "HECHLLT"
print(f"  Letters: {block}")
print(f"  Sorted: {''.join(sorted(block))}")
print(f"  Counts: {dict(Counter(block))}")

# Always after FACH: "FACH HECHLLT ICH"
# FACH = compartment/subject/field
# Could FACHHECHLLT be one block?
combined_fach = "FACH" + block
print(f"\n  FACH+HECHLLT = {combined_fach} (11 chars)")
print(f"  Sorted: {''.join(sorted(combined_fach))}")

# What about just HECHLLT?
# HECHLLT sorted: CEHHLT (C,E,H,H,L,L,T)
# 7 letters: SCHLECHT? S,C,H,L,E,C,H,T = 8 letters with 2 C's. No.
# LEUCHTE? L,E,U,C,H,T,E = 7 letters, sorted CEEHLT (only 1 H). No.
# What has C,E,H,H,L,L,T?
# HELL: H,E,L,L = 4 letters. Remaining: C,H,T
# HELL + CHT = "HELLCHT"? HELLICHT (bright)? HELLICHT = 8 letters.
# Actually LICHT = L,I,C,H,T - we have L,not I. Hmm.

# With +1 pattern (one extra letter):
for skip in range(7):
    reduced = block[:skip] + block[skip+1:]
    rs = ''.join(sorted(reduced))
    # 6-letter candidates
    for cand in ['LEICHT', 'SCHLECHT', 'LECHZT', 'NICHTS', 'HELLET']:
        if len(cand) == 6 and ''.join(sorted(cand)) == rs:
            print(f"  {block} - '{block[skip]}' = {reduced} -> {cand} (+1)")

# Raw codes
print(f"\n  HECHLLT raw codes:")
for bidx, text in enumerate(decoded_books):
    idx = text.find('HECHLLT')
    if idx >= 0:
        pairs = book_pairs[bidx]
        if idx + 7 <= len(pairs):
            codes = pairs[idx:idx+7]
            print(f"    Book {bidx:2d}: {' '.join(codes)} -> {''.join(v7.get(c,'?') for c in codes)}")

# ================================================================
# 4. LGTNELGZ (8 chars, 2x = 16 chars)
# ================================================================
print(f"\n{'=' * 80}")
print("4. LGTNELGZ ANALYSIS (8 chars, 2x)")
print("=" * 80)

block = "LGTNELGZ"
print(f"  Letters: {block}")
print(f"  Sorted: {''.join(sorted(block))}")
# E,G,G,L,L,N,T,Z
# Context: "NOT ER {LGTNELGZ} ER {A} SER {TIURIT} ORANGENSTRASSE"
# So it's between NOT ER and ER A SER

# Could this be GELTENGELZ -> GELTENZ? GELTEN (to be valid) = G,E,L,T,E,N
# LGTNELGZ sorted: EGGLNTZ (missing second E). Not GELTEN.
# GELTUNG = G,E,L,T,U,N,G = 7 letters. We have 8 letters without U: EGGLNTZ.
# No match.

# GLANZ (splendor) = G,L,A,N,Z = 5 letters.
# LGTNELGZ has no A. Not GLANZ.

# With +1:
for skip in range(8):
    reduced = block[:skip] + block[skip+1:]
    rs = ''.join(sorted(reduced))
    for cand in ['GELTEN', 'GELTNE', 'ENGELT', 'GELTUNG']:
        if len(cand) == 7 and ''.join(sorted(cand)) == rs:
            print(f"  {block} - '{block[skip]}' = {reduced} -> {cand} (+1)")

# Try 2-piece split
print(f"\n  2-piece splits:")
splits_lg = find_anagram_splits(block, ANAGRAM_WORDS, max_pieces=2)
for words, parts in splits_lg[:10]:
    print(f"    {' + '.join(words)} <- {' + '.join(parts)}")

# ================================================================
# 5. THARSCR (7 chars, 2x = 14 chars)
# ================================================================
print(f"\n{'=' * 80}")
print("5. THARSCR ANALYSIS (7 chars, 2x)")
print("=" * 80)

block = "THARSCR"
print(f"  Letters: {block}")
print(f"  Sorted: {''.join(sorted(block))}")
# A,C,H,R,R,S,T
# Context: "RUNEN DER {THARSCR} SCE AUS ER" and "DES ER {THARSCR} SCE AUS ER"
# SCHARDT sorted: A,C,D,H,R,S,T
# THARSCR sorted: A,C,H,R,R,S,T
# Difference: THARSCR has extra R, missing D
# THARSCR could be SCHARDT with R instead of D?
# Or: THARSCR is an anagram of something with A,C,H,R,R,S,T
# SCHART + R? SCHRAT + R?
# SCHRAT = MHG demon/wood sprite! S,C,H,R,A,T = 6 letters
# THARSCR = 7 letters = SCHRAT + R (extra R)

schart_sorted = ''.join(sorted('SCHRAT'))
print(f"  SCHRAT sorted: {schart_sorted}")
for skip in range(7):
    reduced = block[:skip] + block[skip+1:]
    rs = ''.join(sorted(reduced))
    if rs == schart_sorted:
        print(f"  THARSCR - '{block[skip]}' = {reduced} -> SCHRAT (+1, skip R)")

# Also check SCHARDT relation
print(f"\n  SCHARDT sorted: {''.join(sorted('SCHARDT'))}")
print(f"  THARSCR sorted: {''.join(sorted('THARSCR'))}")
print(f"  Difference: SCHARDT has D, THARSCR has extra R")

# Could THARSCR be a variant of the SCHARDT name?
# Context "DER THARSCR SCE AUS ER" = "the THARSCR ... out of him"
# vs "STEINEN TER SCHARDT IST SCHAUN" = "stones of Schardt is to behold"

# ================================================================
# 6. EOIAITOEMEEND (13 chars, 2x = 26 chars)
# ================================================================
print(f"\n{'=' * 80}")
print("6. EOIAITOEMEEND ANALYSIS (13 chars, 2x)")
print("=" * 80)

block = "EOIAITOEMEEND"
print(f"  Letters: {block}")
print(f"  Sorted: {''.join(sorted(block))}")
print(f"  Counts: {dict(Counter(block))}")
# D,E,E,E,I,I,M,N,O,O,T,A
# Context: "DA BEI ERDE {EOIAITOEMEEND} GEH ND FINDEN"
# 13 letters. What could this be?

# Try 2-piece:
print(f"\n  2-piece splits:")
splits_eo = find_anagram_splits(block, ANAGRAM_WORDS, max_pieces=2)
for words, parts in splits_eo[:10]:
    print(f"    {' + '.join(words)} <- {' + '.join(parts)}")

# Try with extended list including compound concepts
# What if it contains TOTEM or GEOMANTIE?
# EOIAITOEMEEND contains: E(3), O(2), I(2), A(1), T(1), M(1), N(1), D(1)
# That's 13 letters total

# GOTTESDIENER? G,O,T,T,E,S,D,I,E,N,E,R = 12 letters. Missing G,S,R. No.
# MEDITATION? M,E,D,I,T,A,T,I,O,N = 10 letters. Sorted: ADEIIMNNOTT
# Our 13 letters sorted: ADEEEIIMNOOTT
# Different.

print(f"\n  Done.")
