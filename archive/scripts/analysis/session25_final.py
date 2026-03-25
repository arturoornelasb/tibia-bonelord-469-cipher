#!/usr/bin/env python3
"""
Session 25 Part 3: Final refined cross-boundary anagram candidates.

KEY FINDING from verification:
- ERT->TER LOSES coverage (-11) and destroys SERTI->STIER
  REJECT ERT->TER

- ESD->DES gains +0 with this vocab set
  RE-EXAMINE: DES is already in vocab. The issue is the string replacement
  pattern - we need to apply it to RAW text, but ESD doesn't appear in raw
  text (it's created by anagram resolution). REJECT ESD->DES

- NEDE->ENDE: net +16 alone, but NEDE appears after anagram resolution
  (SEINE -> SEI + NEDE). This is a proper cross-boundary.

Final safe candidates to validate:
  SERTI -> STIER (5-6x, +10-12 chars, bull)
  EUTR  -> TREU  (7x, +21 chars, faithful)
  NEDE  -> ENDE  (7x, +14-16 chars, end)
  HIM   -> IHM   (8x, +8 chars, to him)
  HHE   -> HEH   (11x, +11 chars, concealment)
  NTES  -> NEST  (4x, +8 chars, nest)
  ESR   -> SER   (11x, +11 chars, very/MHG)

Apply in longest-first order and check for interference.
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
    'EUN': 'NEU', 'NIUR': 'RUIN', 'RUIIN': 'RUIN', 'CHIS': 'SICH',
}

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    return 0 if ic_from_counts(Counter(bp0), len(bp0)) > ic_from_counts(Counter(bp1), len(bp1)) else 1

decoded_books = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    decoded_books.append(''.join(v7.get(p, '?') for p in pairs))

raw_concat = ''.join(decoded_books)

# Session 22 vocabulary (canonical)
KNOWN_WORDS = {
    'SEIN', 'SEINE', 'SEINER', 'SEINEN', 'SEINEM', 'SEINES',
    'IST', 'WAR', 'WIRD', 'WAREN', 'SEID',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES',
    'EIN', 'EINE', 'EINER', 'EINEM', 'EINEN', 'EINES',
    'UND', 'ODER', 'ABER', 'NICHT', 'MIT', 'VON', 'BIS',
    'WIR', 'ICH', 'ER', 'SIE', 'ES', 'IHR', 'WER', 'WAS',
    'IN', 'IM', 'AN', 'AM', 'AUF', 'AUS', 'AB', 'ZU', 'ZUR', 'ZUM',
    'BEI', 'SO', 'DA', 'WO', 'NUN', 'NU', 'INS', 'GEN', 'AUS',
    'HIER', 'ODE', 'ORT', 'NACH', 'ALS', 'WIE', 'WENN',
    'KLAR', 'AUCH', 'WEG', 'NUR', 'NIT',
    'GOTT', 'RUNE', 'RUNEN', 'STEIN', 'STEINEN', 'STEINE',
    'URALTE', 'ALT', 'ALTE', 'ALTEN',
    'KOENIG', 'RITTER', 'WORT', 'SAGEN', 'FINDEN',
    'STEH', 'GEHEN', 'GEH', 'ENDE', 'ENDEN',
    'ERSTE', 'ERSTEN',
    'DIESE', 'DIESER', 'DIESEN', 'DIESEM', 'DIESES',
    'TAG', 'MIN', 'TOT', 'RUIN', 'RUINE', 'SAND', 'HEIME', 'HEIM',
    'LEICH', 'LEICHE', 'TRAUT', 'SCHRAT', 'SCHARDT', 'SCHAUN',
    'WEICHSTEIN', 'SALZBERG', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'EIGENTUM', 'MEERE',
    'NEIGT', 'WISTEN', 'MANIER', 'GODES', 'DIENST', 'NACHTS',
    'STANDE', 'BEI', 'TUT', 'NEU', 'SICH', 'REDER',
    'HEL', 'RIT', 'EWE', 'SIN', 'MIS', 'AUE', 'EIS',
    'SCE', 'OEL', 'TER', 'THENAEUT',
    'BERUCHTIG', 'BERUCHTIGER', 'LEICHANBERUCHTIG', 'LEICHANBERUCHTIGER',
    'HAT', 'NET', 'EM', 'TUN',
    'RUINEN', 'HUND', 'GRUND', 'RECHT', 'NACHT',
    'BURG', 'BERG', 'WALD', 'LICHT', 'KNECHT',
    'HEHL', 'HEHLE', 'HEIL', 'HELD', 'SCHLECHT', 'ECHT',
    'WIRT', 'WIRTE', 'TURM', 'TEICH',
    'ELCH', 'DURCH', 'WUNDER', 'WUNDE',
    'UNTER', 'HOLT', 'SER',
}

def count_coverage(text, vocab):
    n = len(text)
    covered = 0
    i = 0
    while i < n:
        best_len = 0
        for l in range(min(20, n-i), 1, -1):
            if text[i:i+l] in vocab:
                best_len = l
                break
        if best_len > 0:
            covered += best_len
            i += best_len
        else:
            i += 1
    return covered

def apply_map(raw, anagram_map):
    text = raw
    for k in sorted(anagram_map, key=len, reverse=True):
        text = text.replace(k, anagram_map[k])
    return text

# ============================================================
# BASELINE
# ============================================================

baseline_text = apply_map(raw_concat, ANAGRAM_MAP)
baseline_cov = count_coverage(baseline_text, KNOWN_WORDS)
print(f"BASELINE: {baseline_cov}/{len(baseline_text)} = {baseline_cov/len(baseline_text)*100:.1f}%")
print()

# ============================================================
# TEST EACH CANDIDATE INDIVIDUALLY
# ============================================================

CANDIDATES = [
    ('SERTI', 'STIER', 'bull'),
    ('EUTR', 'TREU', 'faithful/loyal'),
    ('NEDE', 'ENDE', 'end'),
    ('NTES', 'NEST', 'nest'),
    ('HIM', 'IHM', 'to him (dat)'),
    ('HHE', 'HEH', 'concealment (MHG)'),
    ('ESR', 'SER', 'very (MHG)'),
    ('ESD', 'DES', 'of the (genitive)'),
    ('ERT', 'TER', '3-letter word TER'),
]

print("=" * 80)
print("INDIVIDUAL CANDIDATE TESTING")
print("=" * 80)
print(f"{'Combo':>10} -> {'Match':<10} {'Count':>6} {'Cov':>6} {'Gain':>6} {'GainPct':>8} {'Status':>8}")
print("-" * 70)

individual_gains = {}
for combo, match, meaning in CANDIDATES:
    test_map = dict(ANAGRAM_MAP)
    test_map[combo] = match
    test_text = apply_map(raw_concat, test_map)

    test_vocab = KNOWN_WORDS | {match}
    test_cov = count_coverage(test_text, test_vocab)
    gain = test_cov - baseline_cov
    gain_pct = gain / len(baseline_text) * 100

    # Count occurrences in raw
    raw_count = raw_concat.count(combo)

    status = "ACCEPT" if gain > 0 else ("NEUTRAL" if gain == 0 else "REJECT")
    print(f"{combo:>10} -> {match:<10} {raw_count:>6} {test_cov:>6} {gain:>+6} {gain_pct:>+7.2f}% {status:>8}")
    individual_gains[combo] = (gain, match, meaning)

# ============================================================
# BUILD OPTIMAL SET (greedy, longest-first, no interference)
# ============================================================

print("\n" + "=" * 80)
print("GREEDY OPTIMAL SET CONSTRUCTION")
print("=" * 80)

# Sort by individual gain, descending
sorted_cands = sorted(
    [(c, m, individual_gains[c][0], meaning) for c, m, meaning in CANDIDATES if individual_gains[c][0] > 0],
    key=lambda x: -x[2]
)

print(f"\nCandidates with positive individual gain: {len(sorted_cands)}")
for c, m, g, meaning in sorted_cands:
    print(f"  {c} -> {m} (+{g}, {meaning})")

# Greedy construction: add one at a time, check for interference
optimal_map = dict(ANAGRAM_MAP)
optimal_vocab = set(KNOWN_WORDS)
current_cov = baseline_cov
accepted = []
rejected = []

# Try longest combos first to avoid substring issues
sorted_cands_by_len = sorted(sorted_cands, key=lambda x: -len(x[0]))

print(f"\nGreedy application (longest first):")
for combo, match, indiv_gain, meaning in sorted_cands_by_len:
    test_map = dict(optimal_map)
    test_map[combo] = match
    test_text = apply_map(raw_concat, test_map)
    test_vocab = optimal_vocab | {match}
    test_cov = count_coverage(test_text, test_vocab)
    gain = test_cov - current_cov

    # Check if adding this creates unwanted side effects
    # (combo appears inside other map keys/values after resolution)
    status = 'ACCEPT' if gain > 0 else 'SKIP'

    print(f"  + {combo:>10} -> {match:<10} cov={test_cov} gain={gain:+d} {status}")

    if gain > 0:
        optimal_map[combo] = match
        optimal_vocab.add(match)
        current_cov = test_cov
        accepted.append((combo, match, gain, meaning))
    else:
        rejected.append((combo, match, gain, meaning))

# ============================================================
# FINAL RESULTS
# ============================================================

print("\n" + "=" * 80)
print("FINAL RESULTS - SESSION 25 NEW CROSS-BOUNDARY ANAGRAMS")
print("=" * 80)

new_anagrams = {k: v for k, v in optimal_map.items() if k not in ANAGRAM_MAP}
print(f"\nACCEPTED ({len(accepted)}):")
total_gain = 0
for combo, match, gain, meaning in accepted:
    raw_count = raw_concat.count(combo)
    total_gain += gain
    print(f"  '{combo}' -> '{match}' ({meaning}) : {raw_count}x in raw text, +{gain} coverage chars")

print(f"\nREJECTED:")
for combo, match, gain, meaning in rejected:
    print(f"  '{combo}' -> '{match}' ({meaning}) : gain={gain:+d} when applied incrementally")

# Also show those that were individually negative
for combo, match, meaning in CANDIDATES:
    if individual_gains[combo][0] <= 0 and combo not in [c for c, _, _, _ in rejected]:
        print(f"  '{combo}' -> '{match}' ({meaning}) : individual gain={individual_gains[combo][0]:+d}")

final_text = apply_map(raw_concat, optimal_map)
final_cov = count_coverage(final_text, optimal_vocab)

print(f"\nBefore session 25: {baseline_cov}/{len(baseline_text)} = {baseline_cov/len(baseline_text)*100:.1f}%")
print(f"After session 25:  {final_cov}/{len(final_text)} = {final_cov/len(final_text)*100:.1f}%")
print(f"Total gain: +{total_gain} chars (+{total_gain/len(final_text)*100:.2f}%)")

# ============================================================
# SHOW RESOLVED TEXT SAMPLE
# ============================================================

print("\n" + "=" * 80)
print("SAMPLE OF RESOLVED TEXT (first 600 chars)")
print("=" * 80)

# Show with word boundaries
from collections import defaultdict

# Rough segmentation to show words
sample = final_text[:600]
i = 0
segments = []
while i < len(sample):
    best_len = 0
    best_word = ''
    for l in range(min(20, len(sample)-i), 1, -1):
        if sample[i:i+l] in optimal_vocab:
            best_len = l
            best_word = sample[i:i+l]
            break
    if best_len > 0:
        segments.append(best_word)
        i += best_len
    else:
        segments.append('{' + sample[i] + '}')
        i += 1

print(' '.join(segments))

# ============================================================
# RECOMMENDED UPDATES TO ANAGRAM_MAP
# ============================================================

print("\n" + "=" * 80)
print("RECOMMENDED ANAGRAM_MAP ADDITIONS (copy-paste ready)")
print("=" * 80)

print("# Session 25: Cross-boundary anagram resolutions")
for combo, match, gain, meaning in accepted:
    print(f"    '{combo}': '{match}',  # {meaning}, +{gain} chars")

print("\n# Corresponding vocabulary additions:")
for combo, match, gain, meaning in accepted:
    print(f"    '{match}',  # {meaning}")

print("\nDone.")
