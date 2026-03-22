"""
PARADOX TOWER BOOKS AS CIPHER KEY

The Paradox Tower was created by the same person who created the 469 language.
It contains two garbled letter books:

Book 1: 26 sections (= 26 letters in alphabet!)
Book 2: 9 rows, 11 sections

Hypothesis: These books are lookup tables for decoding 469.

Also testing: Could the Hellgate 4x4 matrix be the encoding key?
"""

import json
import sys
from collections import Counter
from itertools import product

sys.stdout.reconfigure(encoding='utf-8')

with open("books.json") as f:
    books = json.load(f)

combined = "".join(books)

# Paradox Tower Book 1 - 26 sections
paradox_1_raw = """ljkhbl nilse jfpce ojvco ld
slcld ylddiv dnolsd dd sd
sdcp cppcs cccpc cpsc
awdp cpcw cfw ce
cpvc ev vcemmev vrvf
cp fd vmfpm xcv"""

# Parse into sections (space-separated groups)
paradox_1_sections = paradox_1_raw.split()
print("=" * 70)
print("PARADOX TOWER BOOK 1 - 26 SECTIONS")
print("=" * 70)
print(f"\nSections ({len(paradox_1_sections)}):")
for i, section in enumerate(paradox_1_sections):
    letter = chr(ord('A') + i)
    print(f"  {letter} ({i:2d}): '{section}' (length {len(section)})")

# Paradox Tower Book 2
paradox_2_raw = """dtjfhg
jhfvzk
bbliiug
bkjjjjjjj
xhvuo
fffff
zkkbk h
lbhiovz
klhi igbb"""

paradox_2_lines = paradox_2_raw.strip().split('\n')
print(f"\n\nParadox Tower Book 2 ({len(paradox_2_lines)} lines):")
for i, line in enumerate(paradox_2_lines):
    print(f"  Row {i}: '{line}'")

# =====================================================================
# 1. LETTER FREQUENCY IN PARADOX BOOKS
# =====================================================================
print("\n" + "=" * 70)
print("1. LETTER FREQUENCY IN PARADOX BOOK 1")
print("=" * 70)

all_letters = ''.join(paradox_1_sections)
letter_freq = Counter(all_letters)
print(f"\nTotal letters: {len(all_letters)}")
print(f"Unique letters: {len(letter_freq)}")
print(f"\nFrequencies:")
for letter, count in letter_freq.most_common():
    pct = count / len(all_letters) * 100
    print(f"  {letter}: {count:3d} ({pct:5.1f}%)")

# Missing letters from alphabet
used = set(all_letters)
missing = set('abcdefghijklmnopqrstuvwxyz') - used
print(f"\nMissing from alphabet: {sorted(missing)}")
print(f"Letters used: {sorted(used)}")

# =====================================================================
# 2. SECTION PROPERTIES
# =====================================================================
print("\n" + "=" * 70)
print("2. SECTION PROPERTIES")
print("=" * 70)

section_lengths = [len(s) for s in paradox_1_sections]
print(f"\nSection lengths: {section_lengths}")
print(f"Sum of lengths: {sum(section_lengths)}")
print(f"Min: {min(section_lengths)}, Max: {max(section_lengths)}")

# What if each section encodes a letter and its LENGTH matters?
print(f"\nSection lengths as alphabet positions (A=1):")
for i, (section, length) in enumerate(zip(paradox_1_sections, section_lengths)):
    if 1 <= length <= 26:
        letter = chr(ord('A') + length - 1)
        print(f"  Section {i:2d} ('{section}'): length {length} -> '{letter}'")

# =====================================================================
# 3. DIGIT PAIR -> SECTION INDEX MAPPING
# =====================================================================
print("\n" + "=" * 70)
print("3. DIGIT PAIR -> SECTION INDEX (0-25) -> LETTER")
print("=" * 70)

# If digit pairs map to indices 0-25, and section i = letter i
# We need a function f(d1,d2) -> 0-25

# Test: which pair encodings give exactly 26 unique values?
print("\nTesting pair functions for exactly 26 unique values...")
good_functions = []

for a in range(1, 10):
    for b in range(0, 10):
        vals = set()
        for d1 in range(10):
            for d2 in range(10):
                val = (a * d1 + b * d2) % 26
                vals.add(val)
        if len(vals) == 26:
            # Test IC on the text
            text_vals = []
            for i in range(0, len(combined)-1, 2):
                d1, d2 = int(combined[i]), int(combined[i+1])
                text_vals.append((a * d1 + b * d2) % 26)
            vf = Counter(text_vals)
            n = len(text_vals)
            ic = sum(c*(c-1) for c in vf.values()) / (n*(n-1))
            ic_ratio = ic / (1/26)
            if ic_ratio > 1.2:
                good_functions.append((a, b, ic_ratio))

good_functions.sort(key=lambda x: -x[2])
print(f"\nTop functions with 26 values and IC > 1.2:")
for a, b, ic_ratio in good_functions[:10]:
    print(f"  ({a}*d1 + {b}*d2) mod 26: IC ratio = {ic_ratio:.4f}")

# =====================================================================
# 4. HELLGATE 4x4 MATRIX AS KEY
# =====================================================================
print("\n" + "=" * 70)
print("4. HELLGATE 4x4 MATRIX AS ENCODING KEY")
print("=" * 70)

matrix = [
    [1, 1, 1, 1],
    [1, 3, 6, 1],
    [1, 1, 4, 1],
    [4, 6, 1, 1]
]

print("\nMatrix:")
for row in matrix:
    print(f"  {row}")

# What if pairs of digits index into this matrix?
# d1 (row 0-3, 4-7, 8-9 -> wrap), d2 (col 0-3, 4-7, 8-9 -> wrap)
print("\n--- Matrix lookup: row = d1 mod 4, col = d2 mod 4 ---")
lookup_vals = []
for i in range(0, len(combined)-1, 2):
    d1, d2 = int(combined[i]), int(combined[i+1])
    row = d1 % 4
    col = d2 % 4
    val = matrix[row][col]
    lookup_vals.append(val)

lf = Counter(lookup_vals)
print(f"Values: {dict(sorted(lf.items()))}")
print(f"Only {len(lf)} unique values - too few for alphabet")

# What if the matrix is used for Hill cipher (groups of 4)?
print("\n--- Hill cipher with 4x4 matrix (mod 26) ---")
import numpy as np

M = np.array(matrix)
det = int(np.round(np.linalg.det(M)))
print(f"Determinant: {det}")
print(f"Det mod 26: {det % 26}")

# For Hill cipher, need gcd(det, 26) = 1
from math import gcd
g = gcd(abs(det) % 26, 26)
print(f"gcd(|det| mod 26, 26) = {g}")
if g != 1:
    print(f"  Matrix NOT invertible mod 26 (gcd != 1)")
    print(f"  Hill cipher with mod 26 is not directly possible")

# Try mod 29 (for 29-symbol alphabet)
print(f"\nDet mod 29: {det % 29}")
g29 = gcd(abs(det) % 29, 29)
print(f"gcd(|det| mod 29, 29) = {g29}")
if g29 == 1:
    print(f"  Matrix IS invertible mod 29!")

    # Apply Hill cipher mod 29
    hill_vals = []
    for i in range(0, len(combined)-3, 4):
        vec = np.array([int(combined[i+j]) for j in range(4)])
        result = M @ vec
        result_mod = result % 29
        hill_vals.extend(result_mod.tolist())

    hf = Counter(hill_vals)
    n = len(hill_vals)
    ic = sum(c*(c-1) for c in hf.values()) / (n*(n-1))
    ic_ratio = ic / (1/29)
    print(f"  IC ratio (mod 29): {ic_ratio:.4f}")
    print(f"  Unique values: {len(hf)}")

    # Try inverse
    M_inv29 = np.round(np.linalg.inv(M) * det).astype(int)
    det_inv = pow(det % 29, -1, 29) if gcd(det % 29, 29) == 1 else None
    if det_inv:
        M_adj = np.round(np.linalg.inv(M) * det).astype(int) % 29
        M_inv_mod29 = (det_inv * M_adj) % 29
        print(f"\n  Inverse matrix mod 29:")
        for row in M_inv_mod29:
            print(f"    {list(row)}")

        inv_vals = []
        for i in range(0, len(combined)-3, 4):
            vec = np.array([int(combined[i+j]) for j in range(4)])
            result = M_inv_mod29 @ vec
            result_mod = result % 29
            inv_vals.extend([int(x) for x in result_mod])

        ivf = Counter(inv_vals)
        n_inv = len(inv_vals)
        ic_inv = sum(c*(c-1) for c in ivf.values()) / (n_inv*(n_inv-1))
        ic_ratio_inv = ic_inv / (1/29)
        print(f"\n  IC ratio (inverse, mod 29): {ic_ratio_inv:.4f}")

# =====================================================================
# 5. SECTION AS CIPHER ALPHABET
# =====================================================================
print("\n" + "=" * 70)
print("5. PARADOX SECTIONS AS CIPHER ALPHABET")
print("=" * 70)

# What if we need to find which section each pair of digits references?
# The sections have different lengths, so maybe the pair gives a
# position within the concatenated sections

all_sections_concat = ''.join(paradox_1_sections)
print(f"\nAll sections concatenated: '{all_sections_concat}' ({len(all_sections_concat)} chars)")

# If 100 possible pairs (00-99) map to positions 0-99 in this string...
print(f"\n--- Pairs as positions in concatenated sections ---")
if len(all_sections_concat) >= 26:
    # Map position to which section it's in
    pos_to_section = {}
    pos = 0
    for i, section in enumerate(paradox_1_sections):
        for j in range(len(section)):
            pos_to_section[pos] = (i, chr(ord('A') + i), section[j])
            pos += 1

    # Test: read first 20 pairs from combined text
    print(f"\nFirst 20 digit pairs -> position -> section -> letter:")
    for i in range(0, 40, 2):
        d1, d2 = int(combined[i]), int(combined[i+1])
        pair_val = d1 * 10 + d2
        if pair_val < len(all_sections_concat):
            sec_idx, sec_letter, char = pos_to_section[pair_val]
            print(f"  Pair '{combined[i:i+2]}' = {pair_val} -> section {sec_idx} ({sec_letter}), char '{char}'")
        else:
            print(f"  Pair '{combined[i:i+2]}' = {pair_val} -> OUT OF RANGE")

# =====================================================================
# 6. SECTION FIRST LETTERS
# =====================================================================
print("\n" + "=" * 70)
print("6. SECTION FIRST LETTERS AND PATTERNS")
print("=" * 70)

first_letters = ''.join(s[0] for s in paradox_1_sections)
print(f"First letters of each section: {first_letters}")

last_letters = ''.join(s[-1] for s in paradox_1_sections)
print(f"Last letters of each section:  {last_letters}")

# Check if first letters spell something when rearranged
print(f"\nFirst letters sorted: {''.join(sorted(first_letters))}")
print(f"Contains: {Counter(first_letters)}")

# =====================================================================
# 7. SECTION LENGTHS AS CODE
# =====================================================================
print("\n" + "=" * 70)
print("7. SECTION LENGTHS AND NUMERICAL PROPERTIES")
print("=" * 70)

print(f"\nLengths: {section_lengths}")
print(f"As string: {''.join(str(l) for l in section_lengths)}")

# What if lengths encode a permutation?
# Lengths: [6,5,5,5,2, 5,6,6,2,2, 4,5,5,4, 4,5,4,3,2, 4,2,7,4, 2,2,5,3]
# Wait, I counted 26 sections but let me recount
print(f"\n  Number of sections: {len(paradox_1_sections)}")

# =====================================================================
# 8. CONNECT PARADOX BOOK TO DIGIT TRANSITIONS
# =====================================================================
print("\n" + "=" * 70)
print("8. PARADOX LETTERS vs DIGIT FREQUENCIES")
print("=" * 70)

# The letters in the paradox book might map to specific digits
# Check if any letter-to-digit mapping makes the paradox book
# read as a valid sequence of book digits

print(f"\nParadox Book 1 unique letters: {sorted(set(all_letters))}")
print(f"Count: {len(set(all_letters))}")
print(f"\nIf each letter maps to a digit (10 digits, {len(set(all_letters))} letters):")
print(f"  Multiple letters must share digits (homophonic in reverse)")

# What's the letter frequency in the paradox book?
print(f"\nParadox letter frequencies:")
for l, c in letter_freq.most_common():
    pct = c / len(all_letters) * 100
    print(f"  '{l}': {c:3d} ({pct:.1f}%)")

# Compare to cipher digit frequencies
print(f"\nCipher digit frequencies:")
digit_freq = Counter(combined)
for d in '0123456789':
    c = digit_freq[d]
    pct = c / len(combined) * 100
    print(f"  '{d}': {c:4d} ({pct:.1f}%)")

# =====================================================================
# 9. STRADDLING CHECKERBOARD
# =====================================================================
print("\n" + "=" * 70)
print("9. STRADDLING CHECKERBOARD HYPOTHESIS")
print("=" * 70)

# A straddling checkerboard uses a keyword to arrange letters
# 8 common letters get single-digit codes
# 18 remaining letters get two-digit codes (using 2 unused digits as row markers)

# In 469: digit 1 is most common (16.6%), which could mean:
# - 1 encodes a single letter, OR
# - 1 is a row marker for two-digit codes

# Digit frequencies suggest: 1,5,4,6,8,9,7,2 are common (>7.5%)
# 0 (7.6%) and 3 (5.8%) are less common

# What if 0 and 3 are the ROW MARKERS?
# Then: single-digit codes: 1,2,4,5,6,7,8,9 (8 letters)
# Two-digit codes: 0X and 3X (20 more letters, for total 28)

# This would explain:
# - 0 being "obscene" (it's a special marker, not a letter)
# - 3 being rare (it's a special marker)
# - 0->7 and 3->2, 3->3 being forbidden (specific 2-digit codes that don't exist)

print("\nStraddling Checkerboard with row markers 0 and 3:")
print("  Single-digit: 1,2,4,5,6,7,8,9 -> 8 most common letters")
print("  Two-digit: 0X (X=0-9) -> 10 letters")
print("  Two-digit: 3X (X=0-9) -> 10 letters")
print("  Total: 8 + 10 + 10 = 28 symbols")
print()

# Apply this encoding to the text
# First, tokenize: if digit is 0 or 3, take two digits; else one digit
tokens = []
i = 0
while i < len(combined):
    d = int(combined[i])
    if d in (0, 3) and i + 1 < len(combined):
        tokens.append(combined[i:i+2])
        i += 2
    else:
        tokens.append(combined[i])
        i += 1

print(f"Tokenized: {len(tokens)} tokens from {len(combined)} digits")
print(f"Average digits/token: {len(combined)/len(tokens):.3f}")
print(f"Unique tokens: {len(set(tokens))}")
print(f"\nToken frequency (top 30):")
tf = Counter(tokens)
for tok, cnt in tf.most_common(30):
    pct = cnt / len(tokens) * 100
    print(f"  '{tok}': {cnt:4d} ({pct:.1f}%)")

# Calculate IC of this tokenization
n = len(tokens)
ic = sum(c*(c-1) for c in tf.values()) / (n*(n-1))
ic_ratio = ic / (1/len(tf))
print(f"\nIC = {ic:.6f}")
print(f"IC ratio = {ic_ratio:.4f} (need ~1.72 for German)")

# English/German freq comparison
german_freq_ordered = [
    ('E', 16.4), ('N', 9.8), ('I', 7.6), ('S', 7.3), ('R', 7.0),
    ('A', 6.5), ('T', 6.2), ('D', 5.1), ('H', 4.8), ('U', 4.2),
    ('L', 3.4), ('C', 3.1), ('G', 3.0), ('M', 2.5), ('O', 2.5),
    ('B', 1.9), ('W', 1.9), ('F', 1.7), ('K', 1.2), ('Z', 1.1),
    ('P', 0.8), ('V', 0.7), ('J', 0.3), ('Y', 0.04), ('X', 0.03), ('Q', 0.02)
]

print(f"\nComparing token frequencies to German letters:")
sorted_tokens = [tok for tok, cnt in tf.most_common()]
for i in range(min(26, len(sorted_tokens))):
    tok = sorted_tokens[i]
    tok_pct = tf[tok] / len(tokens) * 100
    if i < len(german_freq_ordered):
        letter, ger_pct = german_freq_ordered[i]
        print(f"  Rank {i+1:2d}: '{tok:2s}' ({tok_pct:5.1f}%) vs '{letter}' ({ger_pct:.1f}%)")

# =====================================================================
# 10. TEST CHECKERBOARD ON KNIGHTMARE CRIB
# =====================================================================
print("\n" + "=" * 70)
print("10. STRADDLING CHECKERBOARD ON KNIGHTMARE")
print("=" * 70)

knightmare = "347867908719766434660345"
# Tokenize with 0 and 3 as row markers
km_tokens = []
i = 0
while i < len(knightmare):
    d = int(knightmare[i])
    if d in (0, 3) and i + 1 < len(knightmare):
        km_tokens.append(knightmare[i:i+2])
        i += 2
    else:
        km_tokens.append(knightmare[i])
        i += 1

print(f"\nKnightmare: {knightmare}")
print(f"Tokens: {km_tokens}")
print(f"Number of tokens: {len(km_tokens)}")
print(f"Plaintext: BEAWITTHANBEAFOOL ({len('BEAWITTHANBEAFOOL')} letters)")
print(f"\nTokens match letters? {len(km_tokens)} tokens vs 17 letters: {'YES!' if len(km_tokens) == 17 else 'NO'}")

if len(km_tokens) == len("BEAWITTHANBEAFOOL"):
    print("\n  TOKEN -> LETTER MAPPING:")
    plain = "BEAWITTHANBEAFOOL"
    token_to_letter = {}
    consistent = True
    for tok, letter in zip(km_tokens, plain):
        if tok in token_to_letter:
            if token_to_letter[tok] != letter:
                print(f"  CONFLICT: '{tok}' -> '{token_to_letter[tok]}' AND '{letter}'")
                consistent = False
        else:
            token_to_letter[tok] = letter
        print(f"  '{tok}' -> '{letter}'")

    print(f"\n  Consistent mapping: {consistent}")
    if consistent:
        print(f"\n  MAPPING TABLE:")
        for tok, letter in sorted(token_to_letter.items()):
            print(f"    '{tok}' = '{letter}'")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
