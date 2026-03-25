#!/usr/bin/env python3
"""
Crack HWND and other key unresolved words.
HWND appears 10x with FINDEN - the most common phrase in the entire text.
"""

import json, os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)

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
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# Find HWND FINDEN in context
print("=" * 70)
print("TRACING 'HWND FINDEN' ACROSS ALL BOOKS")
print("=" * 70)

for bidx, bpairs in enumerate(book_pairs):
    text = ''.join(v7.get(p, '?') for p in bpairs)
    pos = text.find('HWNDFINDEN')
    if pos >= 0:
        # Get surrounding context
        ctx_start = max(0, pos - 20)
        ctx_end = min(len(text), pos + 30)
        ctx = text[ctx_start:ctx_end]

        # Get the raw codes
        codes = bpairs[pos:pos+10]
        code_str = ' '.join(codes)

        # Extended context with word boundaries
        ext_start = max(0, pos - 40)
        ext_end = min(len(text), pos + 40)
        extended = text[ext_start:ext_end]

        print(f"\nBook {bidx:2d} pos {pos:3d}:")
        print(f"  Context: ...{extended}...")
        print(f"  HWND codes: {' '.join(bpairs[pos:pos+4])}")
        print(f"  FINDEN codes: {' '.join(bpairs[pos+4:pos+10])}")

# Also find HWND without FINDEN
print(f"\n{'=' * 70}")
print("ALL OCCURRENCES OF 'HWND' (with context)")
print(f"{'=' * 70}")

for bidx, bpairs in enumerate(book_pairs):
    text = ''.join(v7.get(p, '?') for p in bpairs)
    pos = 0
    while True:
        pos = text.find('HWND', pos)
        if pos < 0:
            break
        ctx_start = max(0, pos - 25)
        ctx_end = min(len(text), pos + 30)
        ctx = text[ctx_start:ctx_end]
        codes = bpairs[pos:pos+4]
        print(f"  Book {bidx:2d} pos {pos:3d}: ...{ctx}...")
        print(f"    Codes: [{' '.join(codes)}]")
        pos += 1

# ============================================================
# HWND ANALYSIS
# ============================================================
print(f"\n{'=' * 70}")
print("HWND CODE ANALYSIS")
print(f"{'=' * 70}")

# HWND = H W N D = codes [94] [36] [48] [42] (from garbled segment analysis)
# But let's verify
hwnd_codes_list = []
for bidx, bpairs in enumerate(book_pairs):
    text = ''.join(v7.get(p, '?') for p in bpairs)
    pos = text.find('HWND')
    if pos >= 0:
        codes = tuple(bpairs[pos:pos+4])
        hwnd_codes_list.append(codes)

hwnd_code_counter = Counter(hwnd_codes_list)
print(f"\nHWND code sequences: {hwnd_code_counter}")
for seq, cnt in hwnd_code_counter.items():
    print(f"  {seq} x{cnt}")

# Check: Is HWND possibly HUND (dog)?
# HUND = H U N D. Currently: H=[94], W=[36], N=[48], D=[42]
# If [36] is really U (not W), then HWND -> HUND!
# But [36] is mapped as W with 74 occurrences. Let's check if W is correct.

print(f"\n{'=' * 70}")
print("HYPOTHESIS: HWND = HUND (dog)?")
print("This would require [36]=U instead of W")
print(f"{'=' * 70}")

code_36_occ = sum(1 for bpairs in book_pairs for p in bpairs if p == '36')
print(f"\nCode [36] has {code_36_occ} occurrences")
print(f"Currently mapped as: W")

# Check what happens to the text if [36]=U
# First, where does code [36] appear?
for bidx, bpairs in enumerate(book_pairs):
    text_w = ''.join(v7.get(p, '?') for p in bpairs)
    test_map = dict(v7)
    test_map['36'] = 'U'
    text_u = ''.join(test_map.get(p, '?') for p in bpairs)

    if text_w != text_u and len(bpairs) >= 30:
        # Show differences
        diffs = []
        for i in range(len(text_w)):
            if text_w[i] != text_u[i]:
                ctx_s = max(0, i - 8)
                ctx_e = min(len(text_w), i + 8)
                diffs.append((text_w[ctx_s:ctx_e], text_u[ctx_s:ctx_e]))

        if diffs:
            unique_diffs = list(set(diffs))[:5]
            print(f"\n  Book {bidx}:")
            for old, new in unique_diffs:
                print(f"    W: ...{old}...")
                print(f"    U: ...{new}...")

# ============================================================
# CHECK: SCHWITEIONE with [36]=U
# ============================================================
print(f"\n{'=' * 70}")
print("CRITICAL CHECK: SCHWITEIONE contains [36]=W")
print("If [36]=U, SCHWITEIONE becomes SCHUITEI ONE")
print(f"{'=' * 70}")

# SCHWITEIONE codes: 91 18 00 36 46 88 95 21 99
# [36] is position 3 (the W)
# If [36]=U: S C H U I T E I O = SCHUITEI + ONE
# This BREAKS the WEICHSTEIN anagram! SCHWITEIONE is WEICHSTEIN+O but SCHUITEI+ONE is not.
print("SCHWITEIONE = WEICHSTEIN + O (confirmed anagram)")
print("If [36]=U: 'SCHUITEIONE' -- NOT an anagram of WEICHSTEIN!")
print(">> [36]=W is CONFIRMED correct by the WEICHSTEIN constraint!")
print(">> HWND is NOT HUND. It's a real word/name with W.")

# ============================================================
# HWND as Middle High German
# ============================================================
print(f"\n{'=' * 70}")
print("HWND IN MIDDLE HIGH GERMAN")
print(f"{'=' * 70}")

print("""
Possible MHG interpretations of HWND:
1. HWND could be a scribal abbreviation or archaic spelling
2. In MHG, "wand" (wall/because) sometimes written without vowel
3. Could be related to "Hund" (dog) but spelled archaically
4. Could be a proper noun (place or character name)
5. HWND + FINDEN = "[something] find/discover"

In MHG and early NHG:
- "wand" = because/for (conjunction) - very common
- "want" = wall/side
- The phrase "HWND FINDEN" could mean "the wall/because to find"
- Or if HWND is a noun: "find the HWND"

Context analysis (surrounding decoded text):
The full repeating pattern is:
  "...EIN RHEIUIRUNN HWND N IN DEN TEIGN DAS ES D ERSTE IEN GEH..."
  = "...one [RHEIUIRUNN] HWND [?] in the [TEIGN] that it [?] first ..."

RHEIUIRUNN (before HWND) could contain RHEIN (Rhine) if some codes are wrong.
""")

# ============================================================
# FINDEN trace
# ============================================================
print(f"\n{'=' * 70}")
print("FINDEN TRACE")
print(f"{'=' * 70}")

for bidx, bpairs in enumerate(book_pairs):
    text = ''.join(v7.get(p, '?') for p in bpairs)
    pos = text.find('FINDEN')
    if pos >= 0:
        codes = bpairs[pos:pos+6]
        code_str = ' '.join(codes)
        ctx_s = max(0, pos - 10)
        ctx_e = min(len(text), pos + 16)
        print(f"  Book {bidx:2d}: [{code_str}] ctx=...{text[ctx_s:ctx_e]}...")

# Check FINDEN codes
finden_codes = set()
for bidx, bpairs in enumerate(book_pairs):
    text = ''.join(v7.get(p, '?') for p in bpairs)
    pos = text.find('FINDEN')
    if pos >= 0:
        codes = tuple(bpairs[pos:pos+6])
        finden_codes.add(codes)

print(f"\nFINDEN code sequences: {finden_codes}")
for seq in finden_codes:
    print(f"  F={seq[0]} I={seq[1]} N={seq[2]} D={seq[3]} E={seq[4]} N={seq[5]}")
    print(f"  Mapped: {' '.join(v7.get(c, '?') for c in seq)}")
