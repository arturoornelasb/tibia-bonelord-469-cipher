#!/usr/bin/env python3
"""
Session 21 Part 5: Focused attack on the two biggest unsolved patterns.

1. WRLGTNELNRHELUIRUNNHWND (23 chars, 4x = 92 garbled chars)
   - The single biggest source of garbled text
   - Has variants: SIUIRUNNHWND (12, 2x), RHELUIRUNNHWND (14, 1x)
   - All share suffix UIRUNNHWND (10 chars)

2. HIHL+NDCE+HECHLLT repeating block (15 chars, 5-9x)
   - Always: "SAGEN AM MIN HIHL DIE NDCE FACH HECHLLT ICH OEL"
   - Full raw codes: 57 65 94 34 | 42 15 95 60 42 18 30 | 20 31 18 06 57 19 18 94 34 34 64

New approach: try re-reading codes with different pair boundaries.
What if the digit split is wrong for some of these books?
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
raw_books = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    raw_books.append(book)
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)
    decoded_books.append(''.join(v7.get(p, '?') for p in pairs))

# ================================================================
# 1. THE BIG BLOCK: WRLGTNELNRHELUIRUNNHWND
# ================================================================
print("=" * 80)
print("1. WRLGTNELNRHELUIRUNNHWND (23 chars, 4x)")
print("=" * 80)

# Full codes: 36 24 96 84 75 60 19 96 58 55 06 49 96 70 46 72 61 14 58 00 36 90 42
# = W R L G T N E L N R H E L U I R U N N H W N D

# Let me look at this as raw digits
big_block_codes = ['36', '24', '96', '84', '75', '60', '19', '96', '58', '55',
                   '06', '49', '96', '70', '46', '72', '61', '14', '58', '00',
                   '36', '90', '42']

print(f"\n  Codes: {' '.join(big_block_codes)}")
print(f"  Decoded: {''.join(v7.get(c, '?') for c in big_block_codes)}")

# As raw digit string: 362496847560199658550649967046726114580036904 2
raw_digits = ''.join(big_block_codes)
print(f"  Raw digits: {raw_digits}")
print(f"  Digit length: {len(raw_digits)}")

# What if we read these digits differently? Shift by 1 position?
print(f"\n  Alternative readings (shifted):")
for shift in range(1, 3):
    alt_digits = raw_digits[shift:]
    alt_pairs = [alt_digits[j:j+2] for j in range(0, len(alt_digits)-1, 2)]
    alt_decode = ''.join(v7.get(p, '?') for p in alt_pairs)
    print(f"    Shift +{shift}: {alt_decode} (pairs: {' '.join(alt_pairs[:12])}...)")

# What if we split differently within the block?
# The block sits in the middle of a book. Before it: STEH (known), after it: FINDEN (known).
# STEH codes: could verify

# Let me look at the raw digit sequence of a full book containing this block
for bidx, text in enumerate(decoded_books):
    idx = text.find('WRLGTNELNRHELUIRUNNHWND')
    if idx >= 0:
        # Get the raw book digits around this position
        book = raw_books[bidx]
        off = get_offset(book)
        # Each decoded letter = 2 raw digits (starting from offset)
        raw_start = off + idx * 2
        raw_end = off + (idx + 23) * 2
        raw_context = book[max(0, raw_start-8):raw_end+8]
        decoded_context = text[max(0, idx-4):idx+27]
        print(f"\n  Book {bidx}: '{decoded_context}'")
        print(f"  Raw digits: ...{raw_context}...")
        print(f"  STEH codes before block:")
        steh_start = idx - 4
        if steh_start >= 0:
            steh_codes = book_pairs[bidx][steh_start:idx]
            steh_decoded = [v7.get(c, '?') for c in steh_codes]
            print(f"    {' '.join(steh_codes)} = {''.join(steh_decoded)}")
        print(f"  FINDEN codes after block:")
        find_start = idx + 23
        if find_start + 6 <= len(book_pairs[bidx]):
            find_codes = book_pairs[bidx][find_start:find_start+6]
            find_decoded = [v7.get(c, '?') for c in find_codes]
            print(f"    {' '.join(find_codes)} = {''.join(find_decoded)}")
        break

# ================================================================
# 2. DECOMPOSITION ATTEMPTS
# ================================================================
print(f"\n{'=' * 80}")
print("2. WRLGTNELNRHELUIRUNNHWND DECOMPOSITION")
print("=" * 80)

block = 'WRLGTNELNRHELUIRUNNHWND'
letters = sorted(block)
print(f"  Letters: {letters}")
print(f"  Frequency: {Counter(block).most_common()}")

# The suffix UIRUNNHWND appears in all variants.
# Let's focus on decomposing UIRUNNHWND (10 chars)
suffix = 'UIRUNNHWND'
print(f"\n  Suffix UIRUNNHWND = {Counter(suffix).most_common()}")
print(f"  Suffix sorted: {sorted(suffix)}")

# What words contain HWND?
# HUND (dog) with W: could HWND = HUND where W is mapped wrong? No, W=36 confirmed.
# But in the cipher, the anagram scrambles letters. So HWND could be:
# WNDH anagram = DHWN = not a word
# WNHD, HDNW, etc. - all nonsensical
# Unless it's part of a longer word where HWND are scattered letters

# What about: split UIRUNNHWND as UIRUNN + HWND
# UIRUNN sorted: I, N, N, R, U, U -> NNIRRUU? No obvious word.
# Could be RUIN + extra U, N, N?
# RUIN (4) + UNN (leftover) = ?

# Or: UIRU + NNHWND
# NNHWND sorted: D, H, N, N, W -> not helpful

# What about: WRLGTNE (first 7 chars, all unique letters)
prefix = 'WRLGTNE'
print(f"\n  Prefix WRLGTNE = {Counter(prefix).most_common()}")
print(f"  7 unique letters: W, R, L, G, T, N, E")

# Try all meaningful 7-letter German words:
# GELTNER? WELTRNG? WENGLER?
# 6-letter subsets:
import itertools
six_letter_words = [
    'GELTEN', 'GARTEN', 'WINTER', 'WERTEN', 'ENGELT', 'LANGER',
    'WENIGE', 'ERGING', 'RENNTE', 'TRAGEN', 'RETTEN', 'LENKER',
    'GLUTEN', 'TRENNE', 'ELTERN', 'LERNEN', 'WARTEN', 'LAGERN',
    'LIEGEN', 'REGELN', 'WETTERN', 'REGNETE', 'LERNTEN',
]

print(f"\n  6-letter words from 7 letters of WRLGTNE:")
for word in six_letter_words:
    if len(word) > 7: continue
    word_counter = Counter(word)
    prefix_counter = Counter(prefix)
    if all(prefix_counter.get(c, 0) >= n for c, n in word_counter.items()):
        remaining = list(prefix)
        for c in word:
            remaining.remove(c)
        print(f"    {word} + {''.join(remaining)} (leftover)")

# ================================================================
# 3. HIHL+NDCE+HECHLLT as one unit
# ================================================================
print(f"\n{'=' * 80}")
print("3. HIHL+NDCE+HECHLLT AS ONE UNIT")
print("=" * 80)

# Combined garbled letters (ignoring DIE and FACH which DP matched):
# HIHL + NDCE + HECHLLT = H,I,H,L + N,D,C,E + H,E,C,H,L,L,T
# Total: 15 letters
# Frequency: C(2), D(1), E(2), H(4), I(1), L(3), N(1), T(1)

combined = 'HIHLNDCEHECHLLT'
print(f"  Combined: {combined} ({len(combined)} chars)")
print(f"  Letter frequency: {Counter(combined).most_common()}")

# That's a LOT of H (4x) and L (3x). Suspicious.
# In German, what words have many H's?
# HOCHHEILIG (most holy), NACHHALL (echo)...
# But these have other letters too.

# What if we include the known words DIE and FACH?
# Full sequence: HIHL + DIE + NDCE + FACH + HECHLLT
# = HIHLDIENDC EFACHHECHLLT
# As one string: HIHLDIENDC EFACHHECHLLT
full_seq = 'HIHLDIENDCEFACHHECHLLT'
print(f"\n  Full sequence (with DIE and FACH): {full_seq} ({len(full_seq)} chars)")
print(f"  Letter frequency: {Counter(full_seq).most_common()}")

# Maybe the word boundaries are wrong. What if DIE and FACH are not real words
# but happen to be inside a longer block?
# Full: H I H L D I E N D C E F A C H H E C H L L T
# That's 22 letters.
# What words could hide in there?

# LICHTFENENDE? NACHTHELDIN? Let me try decomposition.
# Split into words:
# HILD (MHG: battle, as in Brynhild) = H,I,L,D = 4 letters -> present!
# HILD appears at positions 0-3: H-I-H-L-D... wait, it's HIHL not HILD.
# But if it's anagrammed: HIHL -> HILD? Sorted: H,H,I,L = no match (HILD sorted = D,H,I,L)
# HIHL has 2 H's, HILD has 1 H and 1 D. Not a match.

# What about the context before and after?
# Full phrase: "SAGEN AM MIN HIHL DIE NDCE FACH HECHLLT ICH OEL"
# SAGEN(say) AM(at) MIN(love/my) [block] ICH(I) OEL(oil)
# = "say at my [????] I oil"

# What if MIN+HIHL = MINIHIHL -> MINNE + IHL? MINNE is "love" in MHG
# But MINHIHL has 7 letters and MINNE has 5. Not a clean match.

# What about: the raw codes might decode differently if there's a code mapping error
# HIHL = H(57) I(65) H(94) L(34)
# What if code 65 is not I? Let me check.
print(f"\n  Code 65 currently maps to: {v7.get('65', '?')}")
print(f"  I codes: {sorted([c for c, l in v7.items() if l == 'I'])}")
print(f"  Code 65 total occurrences: {sum(1 for pairs in book_pairs for p in pairs if p == '65')}")

# Count code 65 in known vs garbled contexts
code65_in_known = 0
code65_in_garbled = 0
for bidx, pairs in enumerate(book_pairs):
    text = decoded_books[bidx]
    for pi, pair in enumerate(pairs):
        if pair == '65':
            # Check surrounding context for known words
            ctx = text[max(0,pi-3):min(len(text),pi+4)]
            # Simple heuristic: if the I is adjacent to common word patterns
            known_patterns = ['DIE', 'DIES', 'IN', 'IST', 'ICH', 'IM', 'SIE',
                            'EIN', 'SEIN', 'DIENST', 'FINDEN', 'HIER', 'NIE',
                            'MIN', 'NIT', 'SEID']
            found = False
            for kp in known_patterns:
                if kp in ctx:
                    code65_in_known += 1
                    found = True
                    break
            if not found:
                code65_in_garbled += 1

total_65 = code65_in_known + code65_in_garbled
print(f"  Code 65 in known patterns: {code65_in_known}/{total_65} ({code65_in_known/total_65*100:.0f}%)")
print(f"  Code 65 in garbled: {code65_in_garbled}/{total_65} ({code65_in_garbled/total_65*100:.0f}%)")

# ================================================================
# 4. What if HECHLLT contains LICHT (light)?
# ================================================================
print(f"\n{'=' * 80}")
print("4. HECHLLT WORD SEARCH")
print("=" * 80)

# HECHLLT sorted = C,E,H,H,L,L,T
# LICHT = C,H,I,L,T (5) -- needs I, we have E and extra H,L
# SCHLECHT = C,C,E,H,H,L,S,T -- needs S and extra C
# HELLICHT = E,H,H,I,L,L,C,T -- needs I, we have all others!
# Wait: HELLICHT sorted = C,E,H,H,I,L,L,T (8 letters, needs I)
# HECHLLT sorted = C,E,H,H,L,L,T (7 letters, no I)

# What about HECHEL (hackle, comb) = C,E,E,H,H,L (6) - needs 2 E's
# HECHT (pike fish) = C,E,H,H,T (5) - leaves L,L
# LECHZT? HECHELT?

# MHG words with these letters:
# HELLE (bright/hell) = E,H,L,L,E (needs 2 E's)
# CHLEIT? No standard word
# HECHEL (teasel/hackle) = needs 2 E's

# What if HECHLLT is actually multiple words?
# HE + CHLLT? HEC + HLLT? HECH + LLT?
# HECH is not a word. LLT is not a word.
# What about HELL + CHT? HELL = H,E,L,L (bright/hell in German)
# CHT = not a word, but -CHT is a common suffix (NICHT, RECHT, LICHT, NACHT)
# HELL + remaining: HECHLLT - HELL = C,H,T = CHT
# So HECHLLT = HELL + CHT? But CHT alone isn't a word.

# What if it's HECHT + LL? HECHT (pike, the fish) = H,E,C,H,T
# HECHT sorted = C,E,H,H,T, remaining LL
# "FACH HECHT LL ICH" = "compartment pike LL I" -- doesn't make sense

# What about KNECHT (servant)? K,N,E,C,H,T - we don't have K or N...
# wait, we DO have N from NDCE! If we combine: NDCE + HECHLLT = N,D,C,E,H,E,C,H,L,L,T
# From these: KNECHT needs K,N,E,C,H,T -- no K.

# SCHLICHT (simple) = S,C,H,L,I,C,H,T -- needs S and I and 2 C's
# NACHTLICH? = N,A,C,H,T,L,I,C,H -- needs A and 2 C's

# Let's try: HIHLDIENDC EFACHHECHLLT = combined 22 letters
# What multi-word German phrase uses these letters?
# C(3), D(2), E(3), F(1), A(1), H(4), I(2), L(2), N(1), T(1)
# That's a lot of variety. Hard to anagram manually.

# Let me try automated 2-word split on HECHLLT
hechllt = 'HECHLLT'
print(f"\n  Trying 2-word splits for HECHLLT:")
# Simple word list for matching
word_list = {}
for w in ['HE', 'EH', 'EL', 'CH', 'HELL', 'HECHT', 'ECHT', 'LECH', 'TELL',
          'HELLE', 'TEICH', 'LEICHT', 'LICHT', 'RECHT', 'HECHEL',
          'TELLER', 'HELLET', 'STELLT', 'ECHTE', 'NACHT',
          'HEHL', 'HALT', 'HELLT']:
    word_list[''.join(sorted(w))] = word_list.get(''.join(sorted(w)), []) + [w]

for split in range(2, len(hechllt) - 1):
    left = hechllt[:split]
    right = hechllt[split:]
    ls = ''.join(sorted(left))
    rs = ''.join(sorted(right))
    lm = word_list.get(ls, [])
    rm = word_list.get(rs, [])
    if lm or rm:
        print(f"    {left}|{right}: left({ls})={lm}, right({rs})={rm}")
    # Also try: anagram of full left or right
    for skip_l in range(len(left)):
        reduced_l = left[:skip_l] + left[skip_l+1:]
        rls = ''.join(sorted(reduced_l))
        rlm = word_list.get(rls, [])
        if rlm and rm:
            print(f"    {left}(-{left[skip_l]})|{right}: left={rlm} +1, right={rm}")

# ================================================================
# 5. FREQUENCY OF H IN GARBLED - IS THERE A SYSTEMATIC ERROR?
# ================================================================
print(f"\n{'=' * 80}")
print("5. H FREQUENCY IN GARBLED ZONES - SYSTEMATIC ERROR CHECK")
print("=" * 80)

# H is 4x in HIHLNDCEHECHLLT combined block
# H is massively overrepresented in garbled zones (62.3%)
# What if one H code is actually something else?

# H codes and their garbled %:
h_codes_data = {}
for hc in [c for c, l in v7.items() if l == 'H']:
    total = 0
    in_garbled = 0
    for bidx, pairs in enumerate(book_pairs):
        text = decoded_books[bidx]
        for pi, pair in enumerate(pairs):
            if pair == hc:
                total += 1
                ctx = text[max(0,pi-3):min(len(text),pi+4)]
                # Check if in known pattern
                known_h = ['HIER', 'HOCH', 'HEIM', 'STEH', 'HAT', 'EHRE',
                           'NACH', 'NACHT', 'NICHT', 'ICH', 'SCH', 'SCHAUN',
                           'SCHARDT', 'SCHWUR', 'RUHE', 'SCHULD', 'HULDE',
                           'HERRE', 'HELD', 'HEIME', 'HAND', 'SCHRAT',
                           'DIENST', 'GOTTDIENER', 'THENA', 'HEARUCHTIG']
                is_known = any(k in text[max(0,pi-6):min(len(text),pi+7)] for k in known_h)
                if not is_known:
                    in_garbled += 1
    h_codes_data[hc] = (total, in_garbled)
    pct = in_garbled/total*100 if total > 0 else 0
    print(f"  Code {hc} -> H: {total}x total, {in_garbled}x garbled ({pct:.0f}%)")

# The most suspicious H code with highest garbled % might be wrong
# If we could test: what if code XX is actually B (or another rare letter)?
# B only has 1 code (62). Very underrepresented.
# F only has 1 code (20). Also underrepresented.
# What if code 06 or 94 is actually B or F?

print(f"\n  B codes: {[c for c, l in v7.items() if l == 'B']}")
print(f"  F codes: {[c for c, l in v7.items() if l == 'F']}")
print(f"  K codes: {[c for c, l in v7.items() if l == 'K']}")
print(f"  Z codes: {[c for c, l in v7.items() if l == 'Z']}")

# These rare letters are suspiciously underrepresented.
# German expects: B ~1.89%, F ~1.66%, K ~1.21%, Z ~1.13%
# Currently: B 0.52%, F 0.50%, K 0.38%, Z 0.38%
# All about 1/3 of expected! This suggests MORE codes should map to B, F, K, Z.

# What if one H code is actually B?
# H has 4 codes: 00, 06, 57, 94
# German H = ~4.76%, we have ~4.62% (slightly under, close to expected)
# If we remove one H code, H would be underrepresented.
# But H is overrepresented in garbled zones, suggesting some H codes are wrong.

# Let me test: what if code 06 (34x, 68% garbled) = B instead of H?
print(f"\n  Test: what if code 06 = B (instead of H)?")
code06_contexts = []
for bidx, pairs in enumerate(book_pairs):
    text = decoded_books[bidx]
    for pi, pair in enumerate(pairs):
        if pair == '06':
            ctx = text[max(0,pi-4):min(len(text),pi+5)]
            rel = pi - max(0, pi-4)
            code06_contexts.append((bidx, pi, ctx, rel))

for bidx, pi, ctx, rel in code06_contexts[:15]:
    marker = ctx[:rel] + '[' + ctx[rel] + '->' + 'B' + ']' + ctx[rel+1:]
    print(f"    Book {bidx:2d}: ...{marker}...")

# Does changing 06 to B improve any garbled blocks?
# HECHLLT with 06 at position FACH+H -> FACH+B = FACHB?
# In the HIHL+NDCE+HECHLLT block, code 06 appears at position FACH[06]HECHLLT
# If 06=B: FACH B ECHLLT -> FACH BECHLLT?
# Or: FACHB + ECHLLT
# ECHLLT sorted = C,E,H,L,L,T (without the H from code 06)
# That changes HECHLLT to BECHLLT = B,C,E,H,L,L,T

print(f"\n  With code 06=B, HECHLLT block becomes:")
print(f"  Current: ...FACH + H(06) + ECHLLT... = FACH HECHLLT")
print(f"  With B:  ...FACH + B(06) + ECHLLT... = FACH BECHLLT?")
print(f"  Or rearranged: FACHB = not a word, BECHLLT = not obvious")

# Actually, let me check WHERE exactly code 06 appears in the block
# Full codes: MIN(04 21 58) HIHL(57 65 94 34) DIE(42 15 95) NDCE(60 42 18 30)
#             FACH(20 31 18 06) HECHLLT(57 19 18 94 34 34 64) ICH(65 18 00)
# Code 06 is the LAST code of FACH = F(20) A(31) C(18) H(06)
# So code 06 = the H in FACH. If it's B instead: F(20) A(31) C(18) B(06) = FACB
# FACB is not a word. FACH (compartment) is. So code 06 = H is correct HERE.

# But what about the H at position 22 in the full sequence?
# Wait, looking at the raw code output again:
# Position 21 (FACH): 18=C, 06=H -> making FACH. Code 06 is correct as H here.

# What about in the big block WRLGTNELNRHELUIRUNNHWND?
# Code 06 appears at position 10: code 06 = H (the first H after LNRHE)
# If 06=B: WRLGTNELNRBELUIRUNNHWND
# Doesn't help.

print(f"\n  Code 06 = H is likely correct (appears in FACH 5x as the H).")
print(f"  The H overrepresentation in garbled is from genuinely unsolved blocks.")

print(f"\nDone.")
