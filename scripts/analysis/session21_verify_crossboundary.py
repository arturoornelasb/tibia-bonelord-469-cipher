#!/usr/bin/env python3
"""
Session 21 Part 7: Verify cross-boundary anagram candidates.

Must verify each candidate won't collide with existing text.
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
    'ANSD': 'SAND',
}

# Build processed text
processed = ''.join(decoded_books)
for old, new in ANAGRAM_MAP.items():
    processed = processed.replace(old, new)

# Test each candidate
candidates = [
    ('ESD', 'DES', 'of the (genitive)'),
    ('TTU', 'TUT', 'does (3rd person tun)'),
    ('TERLAU', 'URALTE', 'ancient'),
    ('EUN', 'NEU', 'new'),
    ('NIUR', 'RUIN', 'ruin'),
    ('SDA', 'DAS', 'the/that'),
]

for old, new, meaning in candidates:
    print(f"\n{'='*60}")
    print(f"Testing: {old} -> {new} ({meaning})")
    print(f"{'='*60}")

    # Count occurrences in processed text
    count = processed.count(old)
    print(f"  Total occurrences of '{old}' in processed text: {count}x")

    # Show all contexts
    pos = 0
    contexts = []
    while True:
        idx = processed.find(old, pos)
        if idx < 0: break
        ctx_s = max(0, idx - 12)
        ctx_e = min(len(processed), idx + len(old) + 12)
        ctx = processed[ctx_s:ctx_e]
        highlight = ctx[:idx-ctx_s] + '[' + old + ']' + ctx[idx-ctx_s+len(old):]
        contexts.append(highlight)
        print(f"    pos {idx}: ...{highlight}...")
        pos = idx + 1

    # Check collisions: would this replacement break existing known words?
    # Test by doing the replacement and checking if coverage changes positively
    test_text = processed.replace(old, new)

    # Check if any known words got broken
    known_words_to_check = ['SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE', 'GOTTDIENER',
                           'SCHARDT', 'TRAUT', 'LEICH', 'HEIME', 'EIGENTUM',
                           'BERUCHTIG', 'MEERE', 'NEIGT', 'WISTEN', 'MANIER',
                           'GODES', 'DIENST', 'BEI', 'STANDE', 'NACHTS',
                           'SAGEN', 'GEHEN', 'SCHRAT', 'SAND', 'STEINEN',
                           'URALTE', 'THENAEUT', 'SCHAUN', 'REDER', 'KOENIG',
                           'FINDEN', 'RUNEN', 'RUNE', 'WISTEN']
    broken = []
    for w in known_words_to_check:
        old_count = processed.count(w)
        new_count = test_text.count(w)
        if new_count < old_count:
            broken.append((w, old_count, new_count))

    if broken:
        print(f"\n  COLLISIONS DETECTED:")
        for w, oc, nc in broken:
            print(f"    {w}: {oc} -> {nc} (LOST {oc-nc})")
    else:
        print(f"\n  No known word collisions detected.")

    # Show what the replacement would look like
    print(f"\n  After replacement, contexts become:")
    for ctx in contexts[:5]:
        replaced = ctx.replace('[' + old + ']', '[' + new + ']')
        print(f"    ...{replaced}...")

# ================================================================
# Special check: TERLAU -> URALTE
# ================================================================
print(f"\n{'='*60}")
print("DEEP CHECK: TERLAU -> URALTE")
print(f"{'='*60}")

# Find where TERLAU appears and what comes after
pos = 0
while True:
    idx = processed.find('TERLAU', pos)
    if idx < 0: break
    # Extended context
    ctx = processed[max(0,idx-15):idx+21]
    after = processed[idx+6:idx+20]
    print(f"  pos {idx}: ...{ctx}...")
    print(f"    After TERLAU: '{after}'")
    # If TERLAU -> URALTE, what would the text look like?
    new_ctx = processed[max(0,idx-15):idx] + 'URALTE' + processed[idx+6:idx+21]
    print(f"    Replaced: ...{new_ctx}...")
    pos = idx + 1

# ================================================================
# Special check: ESD -> DES
# ================================================================
print(f"\n{'='*60}")
print("DEEP CHECK: ESD -> DES")
print(f"{'='*60}")

# Check all ESD contexts
pos = 0
while True:
    idx = processed.find('ESD', pos)
    if idx < 0: break
    ctx = processed[max(0,idx-10):idx+13]
    print(f"  pos {idx}: ...{ctx}...")
    # What comes after?
    after_word = processed[idx+3:idx+10]
    print(f"    After DES: '{after_word}'")
    pos = idx + 1

print(f"\nDone.")
