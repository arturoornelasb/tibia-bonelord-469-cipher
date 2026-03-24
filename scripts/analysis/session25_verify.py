#!/usr/bin/env python3
"""
Session 25 Part 2: Verify and deep-analyze cross-boundary anagram candidates.

From session25_cross_boundary.py, the accepted candidates are:
  'EUTR' -> 'TREU' (7x, +21 chars) [split_left: ODE|E+{UTR}]
  'ERT' -> 'TER' (16x, +16 chars)
  'SERTI' -> 'STIER' (5x, +10 chars)
  'ESD' -> 'DES' (8x, +8 chars)
  'ESR' -> 'SER' (8x, +8 chars)
  'NTES' -> 'NEST' (4x, +8 chars)
  'NEDE' -> 'ENDE' (4x, +8 chars)
  'HIM' -> 'IHM' (6x, +6 chars)
  'HHE' -> 'HEH' (3x, +3 chars)

For each candidate, we need to check:
1. Is it truly a cross-boundary (garbled touching a known word)?
2. Does the resolved form make linguistic sense in context?
3. Does it appear in the RAW decoded text (pre-anagram-map)?
4. Could it conflict with any future resolution?
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

# Apply anagram map
processed_books = []
for text in decoded_books:
    for old in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
        text = text.replace(old, ANAGRAM_MAP[old])
    processed_books.append(text)

raw_concat = ''.join(decoded_books)
processed_concat = ''.join(processed_books)

# ============================================================
# CANDIDATE VERIFICATION
# ============================================================

NEW_CANDIDATES = [
    ('EUTR', 'TREU', 'split_left: ODE|{E}+{UTR} -> ODE TREU', 'ODE + TREU (faithful/loyal)'),
    ('ERT', 'TER', 'exact: ER+{T}', 'single chars, very common'),
    ('SERTI', 'STIER', 'exact: SER+{TI}', 'SER = very (MHG), STIER = bull'),
    ('ESD', 'DES', 'exact: ES+{D}', 'ES + DES (of the)'),
    ('ESR', 'SER', 'exact: ES+{R}', 'ES + SER (very)'),
    ('NTES', 'NEST', 'exact: {NT}+ES', 'NEST (nest/hideout) + ES'),
    ('NEDE', 'ENDE', 'split_left: SEINE|{NE}+{DE}', 'SEI ENDE (be end)'),
    ('HIM', 'IHM', 'exact: HI+{M}', 'IHM (to him, dative)'),
    ('HHE', 'HEH', 'split_right: {H}+HE|IN', 'HEH + EIN/IN'),
]

print("=" * 80)
print("SESSION 25 CANDIDATE VERIFICATION")
print("=" * 80)

for combo, match, desc, meaning in NEW_CANDIDATES:
    print(f"\n{'='*70}")
    print(f"CANDIDATE: '{combo}' -> '{match}' ({desc})")
    print(f"Meaning: {meaning}")
    print(f"{'='*70}")

    # Find in raw text
    raw_count = raw_concat.count(combo)
    proc_count = processed_concat.count(combo)
    print(f"  In raw decoded text: {raw_count}x")
    print(f"  In processed text:   {proc_count}x")

    # Show all contexts in processed text
    pos = 0
    ctx_list = []
    while True:
        idx = processed_concat.find(combo, pos)
        if idx < 0:
            break
        ctx_start = max(0, idx - 20)
        ctx_end = min(len(processed_concat), idx + len(combo) + 20)
        ctx = processed_concat[ctx_start:ctx_end]
        # Mark the combo
        rel_start = idx - ctx_start
        rel_end = rel_start + len(combo)
        marked = ctx[:rel_start] + '[' + ctx[rel_start:rel_end] + ']' + ctx[rel_end:]
        ctx_list.append(marked)
        pos = idx + 1

    print(f"\n  All occurrences in processed text:")
    for i, ctx in enumerate(ctx_list):
        print(f"    {i+1:2d}. ...{ctx}...")

    # Show what it would look like after resolution
    print(f"\n  After replacing '{combo}' -> '{match}':")
    test_text = processed_concat.replace(combo, match)
    pos = 0
    while True:
        idx = test_text.find(match, pos)
        if idx < 0:
            break
        ctx_start = max(0, idx - 20)
        ctx_end = min(len(test_text), idx + len(match) + 20)
        ctx = test_text[ctx_start:ctx_end]
        rel_start = idx - ctx_start
        rel_end = rel_start + len(match)
        marked = ctx[:rel_start] + '[' + ctx[rel_start:rel_end] + ']' + ctx[rel_end:]
        print(f"    ...{marked}...")
        pos = idx + 1

    # Check if combo appears inside any existing anagram I/O
    for old, new in ANAGRAM_MAP.items():
        if combo in old:
            print(f"  WARNING: '{combo}' is substring of anagram input '{old}' -> '{new}'")
        if combo in new:
            print(f"  WARNING: '{combo}' is substring of anagram output '{old}' -> '{new}'")

# ============================================================
# IMPORTANT: Check for interference patterns
# ============================================================

print("\n" + "=" * 80)
print("INTERFERENCE CHECK: Do any new candidates overlap/conflict?")
print("=" * 80)

for i, (c1, m1, _, _) in enumerate(NEW_CANDIDATES):
    for j, (c2, m2, _, _) in enumerate(NEW_CANDIDATES):
        if i >= j:
            continue
        # Check if resolving c1->m1 creates or destroys c2
        test = processed_concat.replace(c1, m1)
        c2_before = processed_concat.count(c2)
        c2_after = test.count(c2)
        if c2_before != c2_after:
            print(f"  INTERFERENCE: '{c1}'->' {m1}' changes '{c2}' count from {c2_before} to {c2_after}")

# ============================================================
# APPLICATION ORDER MATTERS - test sequential application
# ============================================================

print("\n" + "=" * 80)
print("SEQUENTIAL APPLICATION TEST")
print("=" * 80)

# Build full map from raw to final
full_map = dict(ANAGRAM_MAP)
# Add candidates in order of combo length (longest first to avoid substring issues)
ordered_candidates = sorted(NEW_CANDIDATES, key=lambda x: -len(x[0]))

for combo, match, desc, meaning in ordered_candidates:
    full_map[combo] = match

# Apply
final_text = raw_concat
for k in sorted(full_map, key=len, reverse=True):
    final_text = final_text.replace(k, full_map[k])

# Count coverage
KNOWN_WORDS = {
    'SEIN', 'SEINE', 'SEINER', 'SEINEN', 'SEINEM', 'SEINES',
    'IST', 'WAR', 'WIRD', 'WAREN', 'SEID',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES',
    'EIN', 'EINE', 'EINER', 'EINEM', 'EINEN', 'EINES',
    'UND', 'ODER', 'ABER', 'NICHT', 'MIT', 'VON', 'BIS',
    'WIR', 'ICH', 'ER', 'SIE', 'ES', 'IHR', 'WER', 'WAS',
    'IN', 'IM', 'AN', 'AM', 'AUF', 'AUS', 'AB', 'ZU', 'ZUR', 'ZUM',
    'BEI', 'SO', 'DA', 'WO', 'NUN', 'NU', 'INS', 'GEN', 'DES', 'AUS',
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
    # NEW from session 25
    'TREU', 'STIER', 'NEST', 'IHM', 'HEH',
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

# Baseline (existing anagram map only)
baseline_text = raw_concat
for k in sorted(ANAGRAM_MAP, key=len, reverse=True):
    baseline_text = baseline_text.replace(k, ANAGRAM_MAP[k])

base_vocab = KNOWN_WORDS - {'TREU', 'STIER', 'NEST', 'IHM', 'HEH'}
base_cov = count_coverage(baseline_text, base_vocab)
print(f"Baseline coverage (before session 25): {base_cov}/{len(baseline_text)} = {base_cov/len(baseline_text)*100:.1f}%")

# One-by-one application
print(f"\nOne-by-one application (longest first):")
current_map = dict(ANAGRAM_MAP)
current_vocab = set(base_vocab)

for combo, match, desc, meaning in ordered_candidates:
    current_map[combo] = match
    current_vocab.add(match)

    t = raw_concat
    for k in sorted(current_map, key=len, reverse=True):
        t = t.replace(k, current_map[k])

    cov = count_coverage(t, current_vocab)
    gain = cov - base_cov
    print(f"  + '{combo}' -> '{match}': coverage = {cov}/{len(t)} = {cov/len(t)*100:.1f}% (net +{gain} from baseline)")

# Final combined
final_cov = count_coverage(final_text, KNOWN_WORDS)
print(f"\nFinal combined coverage: {final_cov}/{len(final_text)} = {final_cov/len(final_text)*100:.1f}%")
print(f"Net gain from all session 25 candidates: +{final_cov - base_cov}")

# ============================================================
# INTERESTING UNSOLVED PATTERNS
# ============================================================

print("\n" + "=" * 80)
print("UNSOLVED HIGH-FREQUENCY PATTERNS TO INVESTIGATE NEXT")
print("=" * 80)

# Apply full map
final_text_v2 = raw_concat
for k in sorted(full_map, key=len, reverse=True):
    final_text_v2 = final_text_v2.replace(k, full_map[k])

# Show remaining garbled zones
print("Remaining text after all resolutions (first 500 chars):")
print(final_text_v2[:500])
print("...")

# Count remaining uncovered chars
uncov_chars = Counter()
n = len(final_text_v2)
i = 0
while i < n:
    best_len = 0
    for l in range(min(20, n-i), 1, -1):
        if final_text_v2[i:i+l] in KNOWN_WORDS:
            best_len = l
            break
    if best_len > 0:
        i += best_len
    else:
        uncov_chars[final_text_v2[i]] += 1
        i += 1

print(f"\nRemaining uncovered char frequencies:")
for ch, cnt in uncov_chars.most_common():
    print(f"  {ch}: {cnt}x")

print("\nDone.")
