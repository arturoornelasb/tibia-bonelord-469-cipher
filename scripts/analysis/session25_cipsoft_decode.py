#!/usr/bin/env python3
"""
Session 25: Decode CipSoft developer texts with v7 mapping.
CRITICAL known-plaintext attack opportunities.
"""
import json, os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def decode_text(text, mapping, try_both_offsets=True):
    """Decode a digit string using pair mapping."""
    results = []
    for off in ([0, 1] if try_both_offsets else [0]):
        pairs = [text[j:j+2] for j in range(off, len(text)-1, 2)]
        decoded = ''.join(mapping.get(p, '?') for p in pairs)
        # Count unknowns
        unknowns = decoded.count('?')
        results.append((off, decoded, unknowns, pairs))
    return results

print("="*70)
print("DECODING CIPSOFT DEVELOPER TEXTS WITH V7 MAPPING")
print("="*70)

# 1. Chayenne's reply (CipSoft Content Team Leader, 2009)
# "114514519485611451908304576512282177 :) 6612527570584 xD"
print("\n1. CHAYENNE'S REPLY (2009)")
print("-" * 40)
chayenne_parts = ["114514519485611451908304576512282177", "6612527570584"]
for i, text in enumerate(chayenne_parts):
    print(f"\n  Part {i+1}: {text} (length: {len(text)})")
    results = decode_text(text, v7)
    for off, decoded, unknowns, pairs in results:
        print(f"    Offset {off}: {decoded} ({unknowns} unknowns)")
        print(f"    Pairs: {' '.join(pairs[:15])}...")

# 2. Wrinkled Bonelord voice lines
print("\n\n2. WRINKLED BONELORD VOICE LINES")
print("-" * 40)
voice1 = "485611800364197"
voice2 = "78572611857643646724"
for label, text in [("Voice 1", voice1), ("Voice 2", voice2)]:
    print(f"\n  {label}: {text} (length: {len(text)})")
    results = decode_text(text, v7)
    for off, decoded, unknowns, pairs in results:
        print(f"    Offset {off}: {decoded} ({unknowns} unknowns)")

# 3. Kharos Library book
print("\n\n3. KHAROS LIBRARY BOOK")
print("-" * 40)
kharos = "51595646114145190584521765219727830464879636612527578967212778894388727857261185764217614588952196180031651288899751121615127215196805970"
print(f"  Length: {len(kharos)}")
results = decode_text(kharos, v7)
for off, decoded, unknowns, pairs in results:
    print(f"    Offset {off}: {decoded} ({unknowns} unknowns)")

# 4. Elder Bonelord and Evil Eye (NPC word-level codes, NOT pair encoding)
print("\n\n4. NPC WORD-LEVEL CODES (for reference)")
print("-" * 40)
print("  Elder Bonelord: 659978 54764! 653768764!")
print("  Evil Eye: 653768764!")
print("  Knightmare: 3478 67 90871 97664 3466 0 345")
print("  These use WORD-LEVEL encoding (different system from books)")

# 5. Facebook poll answer in 469
print("\n\n5. CIPSOFT FACEBOOK POLL (469 answer)")
print("-" * 40)
fb = "663 902073 7223 67538 467 80097"
print(f"  '{fb}' -- space-separated = WORD-LEVEL encoding")
print("  Individual codes: 663, 902073, 7223, 67538, 467, 80097")

# 6. Honeminas formula vectors
print("\n\n6. HONEMINAS FORMULA ANALYSIS")
print("-" * 40)
print("  (4,3,1,5,3).(3,4,7,8,4) = 4*3 + 3*4 + 1*7 + 5*8 + 3*4 = 12+12+7+40+12 = 83")
print("  Five components per vector = 5 bonelord eyes?")
# Check if 3478 and 4315 appear in books
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
count_3478 = sum(b.count('3478') for b in books)
count_4315 = sum(b.count('4315') for b in books)
print(f"  '3478' appears in books: {count_3478} times")
print(f"  '4315' appears in books: {count_4315} times")
print(f"  In v7: 34->L, 78->T (LT); 43->U, 15->I (UI)")

# 7. Cross-validate: Does Chayenne's text appear in books?
print("\n\n7. CROSS-VALIDATION: CHAYENNE TEXT IN BOOKS?")
print("-" * 40)
for part in chayenne_parts:
    for book_idx, book in enumerate(books):
        if part[:20] in book:
            print(f"  First 20 digits of '{part[:20]}...' found in Book {book_idx}!")
            # Find position
            pos = book.index(part[:20])
            print(f"    Position: {pos}")
            break
    else:
        # Try shorter substrings
        found = False
        for slen in [16, 12, 10, 8]:
            substr = part[:slen]
            for book_idx, book in enumerate(books):
                if substr in book:
                    print(f"  First {slen} digits '{substr}' found in Book {book_idx} at pos {book.index(substr)}")
                    found = True
                    break
            if found:
                break
        if not found:
            print(f"  '{part[:20]}...' NOT found in any book (even 8-digit substr)")

# 8. Voice line cross-validation
print("\n\n8. VOICE LINES IN BOOKS?")
print("-" * 40)
for label, text in [("Voice 1", voice1), ("Voice 2", voice2)]:
    for book_idx, book in enumerate(books):
        if text in book:
            print(f"  {label} found in Book {book_idx}!")
            break
    else:
        # Try substrings
        for slen in [14, 12, 10, 8]:
            substr = text[:slen]
            for book_idx, book in enumerate(books):
                if substr in book:
                    print(f"  {label} first {slen} digits found in Book {book_idx}")
                    break
            else:
                continue
            break
        else:
            print(f"  {label} NOT found in any book")

# 9. Hex decode from tibia.org hidden HTML
print("\n\n9. TIBIA.ORG HIDDEN HTML HEX DECODE")
print("-" * 40)
hex_str = "62792068657272657261"
ascii_result = bytes.fromhex(hex_str).decode('ascii', errors='replace')
print(f"  Hex: {hex_str}")
print(f"  ASCII: '{ascii_result}'")
print(f"  This replaced '63378129' in Avar Tar's poem")
print(f"  Pair decode of 63378129:")
for off in [0, 1]:
    pairs = [hex_str[j:j+2] for j in range(off, len(hex_str)-1, 2)]
    # These are hex values, but let's also try as v7 pairs
    avtar = "63378129"
    avtar_pairs = [avtar[j:j+2] for j in range(off, len(avtar)-1, 2)]
    avtar_decoded = ''.join(v7.get(p, '?') for p in avtar_pairs)
    print(f"    Avar Tar '63378129' offset {off}: {avtar_decoded}")

print("\n" + "="*70)
print("SUMMARY OF KEY FINDINGS")
print("="*70)
print("""
1. Chayenne's reply decodes with v7 — check if it produces German text
2. Wrinkled Bonelord voice lines should match book content
3. Voice line 2 (78572611857643646724) was confirmed = THENAEUTER in session 16
4. Honeminas formula: 3478 appears 24x in books, 4315 appears many times
5. The NPC word-level encoding (Knightmare, Avar Tar) is SEPARATE from book pairs
6. Facebook hex "by herrrera" is in a DIFFERENT encoding system (ASCII hex)
""")
print("Done.")
