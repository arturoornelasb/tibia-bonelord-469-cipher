#!/usr/bin/env python3
"""
Session 20 Part 7: Deeper analysis of the 23-char block and its variants.

WRLGTNELNRHELUIRUNNHWND (23 chars, 4x)
Also: SIUIRUNNHWND (12 chars, 2x), RHELUIRUNNHWND (14 chars, 1x)

Key insight: these all share the suffix UIRUNNHWND.
The 23-char block = WR + LGTNE + LNRHE + L + UIRUNN + HWND

What if we look at this from the KNOWN block boundaries?
Context: "STEH {WRLGTNELNRHELUIRUNNHWND} FINDEN NEIGT DAS ES"
The block is between STEH (stand) and FINDEN (find).

New approach: treat HWND as a word (it always precedes FINDEN).
Then we have WRLGTNELNRHELUIRUNN (19 chars) to decompose.
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
# 1. All variants of the *UIRUNNHWND suffix
# ================================================================
print("=" * 80)
print("1. ALL VARIANTS ENDING IN UIRUNNHWND")
print("=" * 80)

# Find all occurrences of UIRUNNHWND
print(f"\n  UIRUNNHWND in decoded text:")
for bidx, text in enumerate(decoded_books):
    pos = 0
    while True:
        idx = text.find('UIRUNNHWND', pos)
        if idx < 0: break
        # Get extended context before
        ctx_s = max(0, idx - 20)
        ctx_e = min(len(text), idx + 15)
        prefix = text[ctx_s:idx]
        suffix = text[idx:ctx_e]
        print(f"  Book {bidx:2d} pos {idx:3d}: ...{prefix}|{suffix}...")

        # Get the raw codes for the full block
        block_start = idx
        while block_start > 0 and text[block_start-1:block_start+10] not in ['STEHUIRUNNHWND']:
            # Go back to find where the garbled block starts
            block_start -= 1
            if block_start <= idx - 25:
                break

        pairs = book_pairs[bidx]
        if idx + 10 <= len(pairs):
            uirunn_codes = pairs[idx:idx+10]
            print(f"           UIRUNNHWND codes: {' '.join(uirunn_codes)}")
        pos = idx + 1

# ================================================================
# 2. HWND as a standalone entity
# ================================================================
print(f"\n{'=' * 80}")
print("2. HWND STANDALONE ANALYSIS")
print("=" * 80)

# HWND always appears before FINDEN. What if HWND is a word?
# In the narrative: "STEH [block] HWND FINDEN NEIGT DAS ES"
# = "stand ... HWND find inclines that it..."
# HWND FINDEN = "HWND find" = find the HWND
# What could HWND be?

# Codes are always 00-36-90-42
# 00=H, 36=W, 90=N, 42=D
# If these codes are correct: HWND
# H-W-N-D doesn't spell a German word.

# What if HWND is actually an abbreviation or acronym?
# Or a proper noun that we can't decode further?
# HUND (dog) would need W=U, but code 36=W is confirmed by
# its appearance in WISTEN, WEICHSTEIN, WIR etc.

# Alternative: what if the block structure is different?
# What if the last word before FINDEN is not HWND but something longer?
# E.g., NNHWND or UNNHWND or RUNNHWND?

# Let's check: what always comes right before HWND?
print(f"\n  Characters immediately before HWND in decoded text:")
for bidx, text in enumerate(decoded_books):
    pos = 0
    while True:
        idx = text.find('HWND', pos)
        if idx < 0: break
        if idx >= 2:
            before = text[max(0,idx-6):idx]
            after = text[idx:min(len(text),idx+10)]
            print(f"    Book {bidx:2d}: ...{before}|{after}...")
        pos = idx + 1

# ================================================================
# 3. What is WRLGTNE?
# ================================================================
print(f"\n{'=' * 80}")
print("3. WRLGTNE (7 chars, appears as prefix and standalone)")
print("=" * 80)

# WRLGTNE appears:
# 1. As prefix of 23-char block (WRLGTNE + LNRHELUIRUNNHWND)
# 2. As standalone garbled block (context: STEH {WRLGTNE} ES)

wrlgtne_count = all_text.count('WRLGTNE')
print(f"\n  WRLGTNE in decoded text: {wrlgtne_count}x")

for bidx, text in enumerate(decoded_books):
    pos = 0
    while True:
        idx = text.find('WRLGTNE', pos)
        if idx < 0: break
        ctx_s = max(0, idx - 10)
        ctx_e = min(len(text), idx + 20)
        # Check codes
        pairs = book_pairs[bidx]
        if idx + 7 <= len(pairs):
            codes = pairs[idx:idx+7]
            print(f"    Book {bidx:2d}: ...{text[ctx_s:ctx_e]}... codes: {' '.join(codes)}")
        pos = idx + 1

# Letters: W,R,L,G,T,N,E (7 unique letters, all different)
# This is a 7-letter sequence with no repeated letters!
# Possible anagrams (7 letters, all distinct):
# WERGELT? W,E,R,G,E,L,T - has 2 E's, we have 1. No.
# ENGWELT? Not a word.
# GENWELT? Not standard.
# NETZWRGL? Too long.
# GERTNEL? No.
# WENGLER? W,E,N,G,L,E,R - 2 E's. No.
# WERGENT? No.

# What about partial matches?
# ELTNER? WENGT? GLENT?
# MHG words with these letters?
# GELTEN (to be worth) = G,E,L,T,E,N - 6 letters, needs 2 E's
# GARTEN (garden) = G,A,R,T,E,N - has A, we don't
# WINTER = W,I,N,T,E,R - has I, we have L,G instead
# WRANGLE = W,R,A,N,G,L,E - has A, not G,T. Close!
# GELTNER = not a word
# WELTRNG? No.

print(f"\n  WRLGTNE anagram candidates:")
letters = sorted('WRLGTNE')
# Try all 6-letter subsets (+1 pattern)
for skip in range(7):
    reduced = 'WRLGTNE'[:skip] + 'WRLGTNE'[skip+1:]
    rs = ''.join(sorted(reduced))
    # Check common 6-letter words
    candidates = [
        'ENGELT', 'GELTEN', 'GARTEN', 'WINTER', 'RETTEN',
        'WERTEN', 'GLUENT', 'WENIGE', 'ZWERGE', 'LANGER',
        'LENKER', 'WINGER', 'RENNET', 'TRAGEN',
    ]
    for cand in candidates:
        if len(cand) == 6 and ''.join(sorted(cand)) == rs:
            print(f"    WRLGTNE - '{WRLGTNE[skip]}' = {reduced} -> {cand}")

# ================================================================
# 4. COMPARE BLOCK VARIANTS
# ================================================================
print(f"\n{'=' * 80}")
print("4. BLOCK VARIANT COMPARISON")
print("=" * 80)

# Full block: WRLGTNELNRHELUIRUNNHWND (23)
# Variant 1: SIUIRUNNHWND (12) - appears 2x
# Variant 2: RHELUIRUNNHWND (14) - appears 1x
# Variant 3: HECHLLNRHELUIRUNNHWND (21) - appears 1x (!)

# Check variant 3
hech_variant = 'HECHLLNRHELUIRUNNHWND'
hech_count = all_text.count(hech_variant)
print(f"\n  HECHLLNRHELUIRUNNHWND in text: {hech_count}x")
# Wait, this would be HECHLLT + ... Let me search more carefully

# Actually let me look at all *HWND occurrences and what precedes them
print(f"\n  All *HWND blocks with prefix context:")
for bidx, text in enumerate(decoded_books):
    pos = 0
    while True:
        idx = text.find('HWND', pos)
        if idx < 0: break
        # Get full garbled block
        start = idx
        # Go backward to find the start of the garbled block
        # (where a known word boundary is)
        block = text[max(0,idx-25):idx+4]
        pairs = book_pairs[bidx]
        if idx + 4 <= len(pairs):
            hwnd_codes = pairs[idx:idx+4]
            full_prefix = text[max(0,idx-20):idx]
            print(f"    Book {bidx:2d}: ...{full_prefix}HWND... (HWND codes: {' '.join(hwnd_codes)})")
        pos = idx + 1

# ================================================================
# 5. Frequency of each code pair in the 23-char block
# ================================================================
print(f"\n{'=' * 80}")
print("5. CODE FREQUENCY ANALYSIS FOR THE 23-CHAR BLOCK")
print("=" * 80)

block_codes = ['36', '24', '96', '84', '75', '60', '19', '96', '58', '55',
               '06', '49', '96', '70', '46', '72', '61', '14', '58', '00',
               '36', '90', '42']

# For each code, what letter it maps to and how many total occurrences
print(f"\n  Code-by-code breakdown:")
for i, code in enumerate(block_codes):
    letter = v7.get(code, '?')
    # Count total occurrences of this code in all books
    total_occ = sum(1 for pairs in book_pairs for p in pairs if p == code)
    # How many other codes map to the same letter?
    same_letter = sorted([c for c, l in v7.items() if l == letter])
    print(f"    [{i:2d}] code {code} -> {letter} ({total_occ}x total, {letter} has codes: {same_letter})")

# ================================================================
# 6. Test: what if code 84 is not G?
# ================================================================
print(f"\n{'=' * 80}")
print("6. CODE 84 (G) ALTERNATIVE TEST")
print("=" * 80)

# Code 84 appears at position 3 of the 23-char block -> G
# G codes: check
g_codes = sorted([c for c, l in v7.items() if l == 'G'])
print(f"  G codes: {g_codes}")

# Count code 84 occurrences
code84_count = sum(1 for pairs in book_pairs for p in pairs if p == '84')
print(f"  Code 84 total: {code84_count}x")

# Contexts of code 84
print(f"\n  Code 84 contexts (first 10):")
count = 0
for bidx, pairs in enumerate(book_pairs):
    for pi, pair in enumerate(pairs):
        if pair == '84' and count < 10:
            text = decoded_books[bidx]
            ctx_s = max(0, pi-4)
            ctx_e = min(len(text), pi+5)
            ctx = text[ctx_s:ctx_e]
            rel = pi - ctx_s
            print(f"    Book {bidx:2d} pos {pi:3d}: ...{ctx[:rel]}[{ctx[rel]}]{ctx[rel+1:]}...")
            count += 1

print(f"\n  Done.")
