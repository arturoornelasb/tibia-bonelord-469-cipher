"""
Decode the Knightmare NPC's 469 speech and other known 469 fragments.
Also: confirm 24=R, update mapping, test word boundary alternatives.
"""
import json
import os
from collections import Counter

data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'final_mapping_v2.json'), 'r') as f:
    base_mapping = json.load(f)

# Updated mapping with confirmed 24=R and 33=W
mapping = dict(base_mapping)
mapping['24'] = 'R'
mapping['33'] = 'W'

def decode_digits(digits, m):
    """Decode a digit string using even-offset pairs."""
    pairs = [digits[j:j+2] for j in range(0, len(digits)-1, 2)]
    return ''.join(m.get(p, f'[{p}]') for p in pairs)

def decode_digits_odd(digits, m):
    """Decode with odd offset."""
    pairs = [digits[j:j+2] for j in range(1, len(digits)-1, 2)]
    return ''.join(m.get(p, f'[{p}]') for p in pairs)

# ============================================================
# 1. KNIGHTMARE NPC DIALOGUE
# ============================================================
print("=" * 80)
print("1. KNIGHTMARE NPC 469 SPEECH DECODE")
print("=" * 80)

# Known Knightmare NPC speech: "3478 67 090871 097664 3466 00 0345!"
# Let's try various parsings:
knightmare = "347867090871097664346600034500"  # without spaces
knightmare_spaced = "3478 67 090871 097664 3466 00 0345"

print(f"\nRaw: {knightmare_spaced}")

# Parse 1: as continuous even-offset
print(f"\n  Even offset (full): {decode_digits(knightmare, mapping)}")
print(f"  Odd offset (full):  {decode_digits_odd(knightmare, mapping)}")

# Parse 2: each space-separated group independently
print(f"\n  Word-by-word (even offset each):")
for word in knightmare_spaced.split():
    dec = decode_digits(word, mapping)
    print(f"    {word} => {dec}")

# Parse 3: try with leading digit as part of alignment
print(f"\n  Word-by-word (try both offsets):")
for word in knightmare_spaced.split():
    even = decode_digits(word, mapping)
    odd = decode_digits_odd(word, mapping) if len(word) > 2 else "N/A"
    print(f"    {word}: even={even} odd={odd}")

# Parse 4: What if the spaces are just formatting and it's one sequence?
full_no_spaces = knightmare_spaced.replace(' ', '')
print(f"\n  Continuous (no spaces):")
print(f"    Even: {decode_digits(full_no_spaces, mapping)}")
print(f"    Odd:  {decode_digits_odd(full_no_spaces, mapping)}")

# ============================================================
# 2. OTHER KNOWN 469 FRAGMENTS FROM TIBIA
# ============================================================
print(f"\n\n{'='*80}")
print("2. OTHER KNOWN 469 FRAGMENTS")
print(f"{'='*80}")

# From the Bonelord Tome and other sources
fragments_469 = [
    ("Bonelord greeting (A Wrinkled Bonelord NPC)", "469"),
    ("Possible NPC phrase", "3478670908710976643466000345"),
]

for label, frag in fragments_469:
    if len(frag) >= 2:
        print(f"\n  {label}: {frag}")
        print(f"    Even: {decode_digits(frag, mapping)}")
        if len(frag) > 2:
            print(f"    Odd:  {decode_digits_odd(frag, mapping)}")

# ============================================================
# 3. TEST WORD BOUNDARY ALTERNATIVES FOR KEY UNKNOWNS
# ============================================================
print(f"\n\n{'='*80}")
print("3. WORD BOUNDARY ALTERNATIVES")
print(f"{'='*80}")

# TAUTRISTEILCH - appears 8+ times
# What if the boundary isn't TAUTRI | STEILCH but something else?
print("\n  TAUTRISTEILCH alternatives:")
phrase = "TAUTRISTEILCH"
for i in range(1, len(phrase)):
    left = phrase[:i]
    right = phrase[i:]
    print(f"    {left} | {right}")

# Key question: is "CH" the start of CHAN or the end of EILCH?
# In German CH never starts a word. So CH must end the previous word.
# STEILCH -> STEIL + CH doesn't work
# EILCH -> not a word
# What if we need to go further back?
# TAUTRISTEILCHANHEARUCHTIGER
# Possible: TAUTR | ISTEILCH | AN | HEARUCHTIGER
# Or: TAUT | RISTEILCHAN | HEARUCHTIGER
# Or: TAU | TRI | STEIL | CHAN | HEARUCHTIGER (CHAN is not German)
# Best: TAUTR | IST | EILCH | AN or TAUTRI | STEIL | CH | AN

# Actually: what if IST is "is" and the boundary is:
# [TAUTR] IST [EILCH] AN HEARUCHTIGER
# "[tautr] is [eilch] at Hearuchtiger"
print("\n  Most likely reading: '[TAUTR] IST [EILCH] AN HEARUCHTIGER'")
print("  = '[tautr] is [eilch] at Hearuchtiger'")

# But wait - Book 2 starts with "EIETAUTRISTEILCH"
# = EIE + TAUTRISTEILCH
# What if it's "EIE TAUTR IST EILCH" where EIE = "his" (archaic)?

# Let's check the codes for TAUTRI
print("\n  Checking TAUTRI codes:")
for i, book in enumerate(books):
    dec = decode_digits(book, mapping) if i == 0 else ''  # skip for speed
    # Use proper IC offset
    from collections import Counter as Ctr
    def get_off(b):
        if len(b) < 10: return 0
        bp0 = [b[j:j+2] for j in range(0, len(b)-1, 2)]
        bp1 = [b[j:j+2] for j in range(1, len(b)-1, 2)]
        def ic(counts, total):
            if total <= 1: return 0
            return sum(c*(c-1) for c in counts.values()) / (total*(total-1))
        ic0 = ic(Ctr(bp0), len(bp0))
        ic1 = ic(Ctr(bp1), len(bp1))
        return 0 if ic0 > ic1 else 1

    off = get_off(books[i])
    pairs = [books[i][j:j+2] for j in range(off, len(books[i])-1, 2)]
    decoded = ''.join(mapping.get(p, '?') for p in pairs)

    if 'TAUTRI' in decoded:
        pos = decoded.find('TAUTRI')
        tautri_codes = pairs[pos:pos+6]
        ctx_codes = pairs[max(0,pos-3):pos+12]
        ctx_decoded = decoded[max(0,pos-3):pos+12]
        print(f"  Book {i}: TAUTRI codes = {' '.join(tautri_codes)}")
        print(f"    Context: {ctx_decoded}")
        print(f"    Codes:   {' '.join(ctx_codes)}")
        break

# ============================================================
# 4. WHAT IF SOME UNKNOWN SEGMENTS ARE GERMAN WITH P?
# ============================================================
print(f"\n\n{'='*80}")
print("4. TESTING IF UNKNOWNS CONTAIN MISSING LETTER P")
print(f"{'='*80}")

# Key unknowns that might contain P:
# TAUTRI - TAUPT RI? No.
# UTRUNR - if one letter is P: UPTRUNR, UTPRUNR, UTRUPNR...
# EILCH - EILPH? PILCH?
# HECHLLT - if H is wrong: PECHLLT?
# HIHLDI - PIHLDI?
# GEVM - GEPM?

# Actually, let's think differently. We have:
# - 20 E codes (a lot!)
# - 8 I codes (too many)
# What if one of the less-frequent E codes is actually P?
# Expected P: ~37 occurrences

# E codes and their frequencies:
e_codes = ['95', '56', '19', '26', '76', '01', '41', '30', '86', '67',
           '27', '03', '09', '17', '29', '49', '39', '74', '37', '69']

code_freqs = Counter()
for book in books:
    off = get_off(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    for p in pairs:
        code_freqs[p] += 1

print("\nE-code frequencies:")
for code in sorted(e_codes, key=lambda c: code_freqs[c]):
    print(f"  Code {code}: {code_freqs[code]}x (currently E)")

# The lowest-frequency E codes:
# code 69: 1x - too rare for P
# code 37: 12x - tentative E, could be something else
# code 74: 19x - confirmed E, but close to P frequency
# code 41: 16x
# code 39: 14x

# Let's test 37=P (was tentatively E, creates "SEE" in TOTNIURG context)
print("\n\nTesting code 37 as P instead of E:")
m37p = dict(mapping)
m37p['37'] = 'P'
for i, book in enumerate(books):
    off = get_off(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    decoded = ''.join(m37p.get(p, '?') for p in pairs)
    if '37' in [p for p in pairs]:
        # Find contexts where 37 appears
        for k, p in enumerate(pairs):
            if p == '37':
                ctx = decoded[max(0,k-4):min(len(decoded),k+5)]
                ctx_base = ''.join(mapping.get(pairs[j], '?') for j in range(max(0,k-4), min(len(pairs),k+5)))
                if i < 15 or True:
                    pass  # collect all
        break

# Show specific contexts for code 37
print("Code 37 contexts (first 10 books with it):")
shown = 0
for i, book in enumerate(books):
    off = get_off(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    for k, p in enumerate(pairs):
        if p == '37':
            ctx_e = ''.join(mapping.get(pairs[j], '?') for j in range(max(0,k-4), min(len(pairs),k+5)))
            ctx_p = ''.join(m37p.get(pairs[j], '?') for j in range(max(0,k-4), min(len(pairs),k+5)))
            print(f"  Book {i} pos {k}: E={ctx_e}  P={ctx_p}")
            shown += 1
            if shown >= 12:
                break
    if shown >= 12:
        break

# ============================================================
# 5. COMPREHENSIVE LOOK AT TAUTRI/EILCH WITH ALL BOOKS
# ============================================================
print(f"\n\n{'='*80}")
print("5. ALL TAUTRISTEILCH CONTEXTS")
print(f"{'='*80}")

for i, book in enumerate(books):
    off = get_off(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    decoded = ''.join(mapping.get(p, '?') for p in pairs)

    if 'TAUTR' in decoded:
        pos = decoded.find('TAUTR')
        ctx = decoded[max(0,pos-10):min(len(decoded),pos+25)]
        ctx_codes = pairs[max(0,pos-10):min(len(pairs),pos+25)]
        print(f"  Book {i}: ...{ctx}...")
        print(f"    Codes: {' '.join(ctx_codes)}")

# ============================================================
# 6. SAVE UPDATED MAPPING
# ============================================================
print(f"\n\n{'='*80}")
print("6. SAVING UPDATED MAPPING (v3: +24=R, +33=W)")
print(f"{'='*80}")

output_path = os.path.join(data_dir, 'final_mapping_v3.json')
with open(output_path, 'w') as f:
    json.dump(mapping, f, indent=2, sort_keys=True)
print(f"Saved to {output_path}")

# Print the mapping summary
letter_codes = {}
for code, letter in sorted(mapping.items()):
    letter_codes.setdefault(letter, []).append(code)

print("\nMapping v3 summary:")
for letter in 'ENISRTADHUGOLMCWFKZBV':
    codes = letter_codes.get(letter, [])
    code_with_freq = [(c, code_freqs.get(c, 0)) for c in codes]
    total_freq = sum(f for _, f in code_with_freq)
    codes_str = ', '.join(f'{c}({f})' for c, f in sorted(code_with_freq, key=lambda x: -x[1]))
    print(f"  {letter} ({len(codes):2d} codes, {total_freq:4d}x): {codes_str}")

# Changes from v2:
print("\nChanges from v2:")
print("  24: I -> R (confirmed: +39 chars, creates UNTER/ER ALS/ER AM NEU)")
print("  33: [unmapped] -> W (confirmed: positional overlap evidence)")
