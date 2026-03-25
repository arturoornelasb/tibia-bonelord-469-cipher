#!/usr/bin/env python3
"""
Session 20 Part 6: NPC response analysis + H overrepresentation investigation.

NPC Noodles response pattern:
- BARK (Woof!): gottdiener, "God's Servant", godes -> GOD-RELATED
- SNIFF: THENAEUT, "The trusted one", "The ancient stones of SCHARDT"
- WIGGLE: bone, bonelord, book, "are to behold as ruin"

H analysis: 62% of H is in garbled zones (vs 32% average).
Which H codes appear most in garbled zones? Are any misassigned?
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

# ================================================================
# H CODE DEEP ANALYSIS
# ================================================================
print("=" * 80)
print("H CODE DEEP ANALYSIS")
print("=" * 80)

h_codes = sorted([c for c, l in v7.items() if l == 'H'])
print(f"\n  H codes: {h_codes}")

# For each H code, show contexts and determine if it's genuinely H
for hc in h_codes:
    occurrences = []
    for bidx, pairs in enumerate(book_pairs):
        for pi, pair in enumerate(pairs):
            if pair == hc:
                text = decoded_books[bidx]
                ctx_s = max(0, pi-4)
                ctx_e = min(len(text), pi+5)
                ctx = text[ctx_s:ctx_e]
                rel = pi - ctx_s
                occurrences.append((bidx, pi, ctx, rel))

    total_occ = len(occurrences)
    print(f"\n  Code {hc} -> H ({total_occ}x):")

    # Show a sample of contexts
    for bidx, pi, ctx, rel in occurrences[:8]:
        marker = ctx[:rel] + '[' + ctx[rel] + ']' + ctx[rel+1:]
        print(f"    Book {bidx:2d} pos {pi:3d}: ...{marker}...")

    # Check: in how many of these does H appear in a known word?
    # (Approximate: check if the H is adjacent to letters that form known patterns)
    in_known_patterns = 0
    known_h_words = ['HIER', 'HOCH', 'HEIM', 'HELD', 'HERR', 'HAND', 'HEIL',
                     'HULDE', 'HERRE', 'HEIME', 'HAT', 'HIN', 'HER',
                     'HUND', 'SCHARDT', 'SCHAUN', 'NICHT', 'NACH', 'STEH',
                     'NACHT', 'NACHTS', 'HECHLLT', 'HWND', 'HIHL',
                     'SCHWUR', 'ICH', 'EHRE', 'RUHE', 'SCH', 'CHN', 'CH']
    for bidx, pi, ctx, rel in occurrences:
        for w in known_h_words:
            if w in ctx:
                in_known_patterns += 1
                break

    print(f"    In known H-patterns: {in_known_patterns}/{total_occ} ({in_known_patterns/total_occ*100:.0f}%)")

# ================================================================
# Check specific hypothesis: is code 06 correct as H?
# Code 06 appears 34x. If it's actually something else?
# ================================================================
print(f"\n{'=' * 80}")
print("CODE 06 (H, 34x) - ALTERNATIVE TESTING")
print("=" * 80)

# Code 06 contexts
for bidx, pairs in enumerate(book_pairs):
    for pi, pair in enumerate(pairs):
        if pair == '06':
            text = decoded_books[bidx]
            ctx_s = max(0, pi-5)
            ctx_e = min(len(text), pi+6)
            ctx = text[ctx_s:ctx_e]
            rel = pi - ctx_s
            # In WRLGTNELNRHELUIRUNNHWND, code 06 is at position 10 (the first H)
            # What word/block is this in?
            break  # Just check first occurrence per book to see distribution
    else:
        continue
    break  # Got one example

# Where does code 06 appear in the big block?
print(f"\n  Code 06 in big block WRLGTNELNRHELUIRUNNHWND:")
big_codes = ['36', '24', '96', '84', '75', '60', '19', '96', '58', '55',
             '06', '49', '96', '70', '46', '72', '61', '14', '58', '00',
             '36', '90', '42']
for i, code in enumerate(big_codes):
    if code == '06':
        print(f"    Position {i}: code 06 = H in ...{decoded_books[3][i-2:i+3]}...")

# Code 94 (H, 42x)
print(f"\n  Code 94 in HECHLLT block:")
hech_codes = ['57', '19', '18', '94', '34', '34', '64']
for i, code in enumerate(hech_codes):
    if code == '94':
        print(f"    Position {i}: code 94 = H, gives 'HECHLLT'")

# ================================================================
# NPC NOODLES PATTERN ANALYSIS
# ================================================================
print(f"\n{'=' * 80}")
print("NPC NOODLES RESPONSE PATTERN")
print("=" * 80)

print("""
  Response categories based on testing:

  BARK ("Woof! Woof!") - God-related words:
    - "gottdiener" (God's Servant in German)
    - "God's Servant" (English translation)
    - "godes" (MHG genitive "of God")
    - "are to behold as ruin" (Woof! - contains narrative?)

  SNIFF - Proper nouns/cipher concepts:
    - "THENAEUT" (bonelord concept, bridges books/NPC)
    - "The trusted one" (reference to TRAUT?)
    - "The ancient stones of SCHARDT" (narrative phrase)

  WIGGLE - Bone/book generic:
    - "bone"
    - "bonelord"
    - "book"

  NO RESPONSE:
    - HWND, FINDEN, UTRUNR, HIHL, leich, reder
    - ritual, TRAUT, BERUCHTIG, rune, magic
    - SALZBERG, WEICHSTEIN, ORANGENSTRASSE, oil
    - distress, need, code, 36=w

  Key observations:
  1. Noodles recognizes GOD-related cipher content -> BARK
  2. Noodles recognizes NARRATIVE PHRASES -> SNIFF
  3. Generic bone/book keywords -> WIGGLE
  4. Individual decoded WORDS (TRAUT, BERUCHTIG, etc.) -> NO RESPONSE
  5. This suggests the GOD connection is a KEY THEME

  The narrative contains:
    - GOTTDIENER (God's Servant) -> central character
    - GODES (of God) -> genitive reference
    - THENAEUT -> appears 6x near STANDE (stood) and NOT (distress)

  THENAEUT as God-related? "THENAEUT ER ALS STANDE E NOT" =
    "Thenaeut he as stood/when distress"
    = "Thenaeut, when he stood in distress"

  NPC keywords to test next:
    - "schrat" (forest demon - just discovered!)
    - "distress" / "not" / "noth"
    - "anointed" / "oil" / "oel"
    - "ancient stones"
    - "runen der schrat" (runes of the forest-demon)
    - "death" / "corpse" / "leiche"
    - "beruechtigt" (notorious - modern German spelling)
    - specific sentences from the narrative
""")

# What narrative phrases could trigger Noodles?
print("  Suggested phrases to test on Noodles:")
print("    1. 'schrat' (new MHG word: forest demon)")
print("    2. 'runes of the schrat' / 'runen der schrat'")
print("    3. 'forest demon' / 'waldschrat'")
print("    4. 'thenaeut stood in distress'")
print("    5. 'anointed with oil'")
print("    6. 'king salzberg not go orange street'")
print("    7. 'Zathroth' (evil god mentioned by King Tibianus)")
print("    8. 'death' / 'corpse' / 'leiche'")
print("    9. 'notorious' / 'beruechtigt'")
print("   10. 'the trusted one is a corpse'")
