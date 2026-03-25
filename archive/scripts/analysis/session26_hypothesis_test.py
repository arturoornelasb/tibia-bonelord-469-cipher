#!/usr/bin/env python3
"""
Session 26: Hypothesis Testing with Coverage Impact
=====================================================
Tests session 24 hypotheses and additional candidates by measuring
their coverage impact using the full DP segmentation pipeline from
narrative_v3_clean.py.

Hypotheses:
  1. HIHL -> HEHL  (MHG concealment, ~8x)
  2. HECHLLT -> HECHELT  (pants/gasps, MHG, ~5x)
  3. NLNDEF -> FINDEN  (to find, freq unknown)
  4. CHN -> NCH  (common German trigram, 8x)
  5. UNR -> RUN or NUR  (only, 7x)
  6. RRNI -> NIRR or IRREN fragment  (5x)
  7. UOD -> OUD or DUO  (5x)
  + Cumulative test of all hypotheses together
"""

import json, os, copy
from collections import Counter

# ============================================================
# BOOTSTRAP: Load data exactly as narrative_v3_clean.py does
# ============================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

# Digit insertion table (from narrative_v3_clean.py)
DIGIT_SPLITS = {
    2: (45, '1'),    5: (265, '1'),   6: (12, '0'),    8: (137, '7'),
    10: (169, '0'),  11: (137, '0'),  12: (56, '1'),   13: (45, '0'),
    14: (98, '1'),   15: (98, '0'),   18: (4, '0'),    19: (52, '0'),
    20: (5, '1'),    22: (7, '1'),    23: (22, '4'),   24: (87, '8'),
    25: (0, '0'),    29: (53, '0'),   32: (137, '1'),  34: (101, '0'),
    36: (78, '0'),   39: (44, '0'),   42: (91, '2'),   43: (122, '0'),
    45: (15, '0'),   46: (0, '2'),    48: (126, '0'),  49: (97, '1'),
    50: (16, '6'),   52: (1, '0'),    53: (257, '1'),  54: (49, '1'),
    60: (73, '9'),   61: (93, '7'),   64: (60, '0'),   65: (114, '2'),
    68: (54, '0'),
}

# Current ANAGRAM_MAP from narrative_v3_clean.py (including session 25)
ANAGRAM_MAP_BASELINE = {
    'LABGZERAS': 'SALZBERG',
    'SCHWITEIONE': 'WEICHSTEIN',
    'SCHWITEIO': 'WEICHSTEIN',
    'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'EDETOTNIURG': 'GOTTDIENER',
    'EDETOTNIURGS': 'GOTTDIENERS',
    'ADTHARSC': 'SCHARDT',
    'TAUTR': 'TRAUT',
    'EILCH': 'LEICH',
    'HEDDEMI': 'HEIME',
    'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG',
    'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE',
    'TEIGN': 'NEIGT',
    'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER',
    'SODGE': 'GODES',
    'SNDTEII': 'DIENST',
    'IEB': 'BEI',
    'TNEDAS': 'STANDE',
    'NSCHAT': 'NACHTS',
    'SANGE': 'SAGEN',
    'GHNEE': 'GEHEN',
    'THARSCR': 'SCHRAT',
    'ANSD': 'SAND',
    'TTU': 'TUT',
    'TERLAU': 'URALTE',
    'EUN': 'NEU',
    'NIUR': 'RUIN',
    'RUIIN': 'RUIN',
    'CHIS': 'SICH',
    # Session 25 cross-boundary anagrams
    'SERTI': 'STIER',
    'ESR': 'SER',
    'NEDE': 'ENDE',
    'NTES': 'NEST',
    'HIM': 'IHM',
    'EUTR': 'TREU',
}

# Full KNOWN set from narrative_v3_clean.py (session 25)
KNOWN = {
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN', 'TUT',
    'SAG', 'WAR',
    'NU', 'SIN', 'STANDE', 'NACHTS', 'NIT', 'TOT', 'TER',
    'ABER', 'ALLE', 'ALLES', 'ALTE', 'ALTEN', 'ALTER', 'AUCH', 'BAND',
    'BERG', 'BURG', 'DENN', 'DIES', 'DIESE', 'DIESER', 'DIESEN',
    'DIESEM', 'DOCH', 'DORT', 'DREI', 'DURCH', 'EINE', 'EINEM',
    'EINEN', 'EINER', 'EINES', 'ENDE', 'ERDE', 'ERST', 'ERSTE',
    'FACH', 'FAND', 'FERN', 'FEST', 'FORT', 'GAR', 'GANZ', 'GEGEN',
    'GEIST', 'GOTT', 'GOLD', 'GRAB', 'GROSS', 'GRUFT', 'GUT',
    'HAND', 'HEIM', 'HELD', 'HERR', 'HIER', 'HOCH', 'IMMER',
    'KANN', 'KLAR', 'KRAFT', 'LAND', 'LANG', 'LICHT', 'MACHT',
    'MEHR', 'MUSS', 'NACH', 'NACHT', 'NAHM', 'NAME', 'NEU', 'NEUE',
    'NEUEN', 'NICHT', 'NIE', 'NOCH', 'ODER', 'ORT', 'ORTEN',
    'REDE', 'REDEN', 'REICH', 'RIEF', 'RUIN', 'RUNE', 'RUNEN',
    'SAND', 'SAGT', 'SCHAUN', 'SCHON', 'SEHR', 'SEID', 'SEIN',
    'SEINE', 'SEINEN', 'SEINER', 'SEINEM', 'SEINES',
    'SICH', 'SIND', 'SOHN', 'SOLL', 'STEH', 'STEIN', 'STEINE',
    'STEINEN', 'STERN', 'TAG', 'TAGE', 'TAGEN', 'TAT', 'TEIL',
    'TIEF', 'TOD', 'TURM', 'UNTER', 'URALTE', 'VIEL', 'VIER',
    'WAHR', 'WALD', 'WAND', 'WARD', 'WEIL', 'WELT', 'WENN', 'WERT',
    'WESEN', 'WILL', 'WIND', 'WIRD', 'WORT', 'WORTE', 'ZEIT',
    'ZEHN', 'ZORN',
    'FINDEN', 'GEBEN', 'GEHEN', 'HABEN', 'KOMMEN', 'LEBEN', 'LESEN',
    'NEHMEN', 'SAGEN', 'SEHEN', 'STEHEN', 'SUCHEN', 'WISSEN',
    'WISSET', 'RUFEN', 'WIEDER',
    'OEL', 'SCE', 'MINNE', 'MIN', 'HEL', 'ODE', 'SER', 'GEN', 'INS',
    'GEIGET', 'BERUCHTIG', 'BERUCHTIGER', 'MEERE', 'NEIGT', 'WISTEN',
    'MANIER', 'HUND', 'GODE', 'GODES', 'EIGENTUM', 'REDER', 'THENAEUT',
    'LABT', 'MORT', 'DIGE', 'WEGE', 'KOENIGS', 'NAHE', 'NOT', 'NOTH',
    'ZUR', 'OWI', 'ENGE', 'SEIDEN', 'ALTES', 'BIS', 'NUT', 'NUTZ',
    'HEIL', 'NEID', 'TREU', 'TREUE', 'SUN', 'DIENST', 'SANG', 'DINC',
    'HULDE', 'LANT', 'HERRE', 'DIENEST', 'GEBOT', 'SCHWUR', 'ORDEN',
    'RICHTER', 'DUNKEL', 'EHRE', 'EDELE', 'SCHULD', 'SEGEN', 'FLUCH',
    'RACHE', 'KOENIG', 'DASS', 'EDEL', 'ADEL', 'SCHRAT',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME', 'SCHARDT',
    # Session 25
    'IHM', 'STIER', 'NEST', 'DES',
}

# ============================================================
# DECODE PIPELINE (exact copy from narrative_v3_clean.py)
# ============================================================
def ic_from_counts(counts, total):
    if total <= 1:
        return 0
    return sum(c * (c - 1) for c in counts.values()) / (total * (total - 1))

def get_offset(book):
    if len(book) < 10:
        return 0
    bp0 = [book[j:j+2] for j in range(0, len(book) - 1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book) - 1, 2)]
    ic0 = ic_from_counts(Counter(bp0), len(bp0))
    ic1 = ic_from_counts(Counter(bp1), len(bp1))
    return 0 if ic0 > ic1 else 1

def decode_books():
    """Decode all books using v7 mapping + digit splits."""
    decoded = []
    for bidx, book in enumerate(books):
        if bidx in DIGIT_SPLITS:
            split_pos, digit = DIGIT_SPLITS[bidx]
            book = book[:split_pos] + digit + book[split_pos:]
        off = get_offset(book)
        pairs = [book[j:j+2] for j in range(off, len(book) - 1, 2)]
        decoded.append(''.join(v7.get(p, '?') for p in pairs))
    return decoded

def apply_anagram_map(text, amap):
    """Apply anagram map to text, longest-first."""
    result = text
    for anagram in sorted(amap.keys(), key=len, reverse=True):
        result = result.replace(anagram, amap[anagram])
    return result

def dp_segment(text, known_set):
    """DP word segmentation -- exact copy from narrative_v3_clean.py."""
    n = len(text)
    dp = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], None)
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if cand in known_set:
                score = dp[start][0] + wlen
                if score > dp[i][0]:
                    dp[i] = (score, (start, cand))
    return dp[n][0]

def measure_coverage(anagram_map, known_set, decoded_books):
    """Compute global and per-book coverage with given anagram map + known set."""
    global_covered = 0
    global_total = 0
    per_book = []
    for bidx, text in enumerate(decoded_books):
        rt = apply_anagram_map(text, anagram_map)
        known_chars = sum(1 for c in rt if c != '?')
        covered = dp_segment(rt, known_set)
        global_covered += covered
        global_total += known_chars
        pct = covered / max(known_chars, 1) * 100
        per_book.append((bidx, covered, known_chars, pct))
    global_pct = global_covered / max(global_total, 1) * 100
    return global_covered, global_total, global_pct, per_book

def find_occurrences(text, pattern, context=15):
    """Find all occurrences of pattern in text with surrounding context."""
    results = []
    pos = 0
    while True:
        idx = text.find(pattern, pos)
        if idx < 0:
            break
        left = max(0, idx - context)
        right = min(len(text), idx + len(pattern) + context)
        ctx = text[left:right]
        results.append((idx, ctx))
        pos = idx + 1
    return results


# ============================================================
# MAIN
# ============================================================
print("=" * 70)
print("SESSION 26: HYPOTHESIS TESTING WITH COVERAGE IMPACT")
print("=" * 70)

decoded = decode_books()

# Baseline coverage
base_covered, base_total, base_pct, base_per_book = measure_coverage(
    ANAGRAM_MAP_BASELINE, KNOWN, decoded
)
print(f"\nBASELINE: {base_covered}/{base_total} = {base_pct:.2f}%")
print(f"  (Using session 25 ANAGRAM_MAP + KNOWN set)")

# Build the resolved baseline text for occurrence counting
all_decoded = ''.join(decoded)
baseline_resolved = apply_anagram_map(all_decoded, ANAGRAM_MAP_BASELINE)

# ============================================================
# INDIVIDUAL HYPOTHESIS TESTS
# ============================================================
print(f"\n{'=' * 70}")
print("INDIVIDUAL HYPOTHESIS TESTS")
print("=" * 70)

hypotheses = [
    # (name, anagram_additions, vocab_additions, description)
    (
        "H1: HIHL -> HEHL",
        {'HIHL': 'HEHL'},
        {'HEHL'},
        "MHG concealment/hiding, E<->I vowel alternation, ~8x"
    ),
    (
        "H2: HECHLLT -> HECHELT",
        {'HECHLLT': 'HECHELT'},
        {'HECHELT'},
        "MHG pants/gasps (hecheln), L<->E swap, ~5x"
    ),
    (
        "H3: NLNDEF -> FINDEN",
        {'NLNDEF': 'FINDEN'},
        set(),  # FINDEN already in KNOWN
        "to find, letter reorder (I<->L substitution?), freq unknown"
    ),
    (
        "H4: CHN -> NCH",
        {'CHN': 'NCH'},
        set(),  # NCH is not a word, but enables NACH, NICHT, etc.
        "Common German trigram, fix transposition, ~8x"
    ),
    (
        "H5a: UNR -> RUN",
        {'UNR': 'RUN'},
        {'RUN'},
        "English/MHG 'run', or part of compounds, ~7x"
    ),
    (
        "H5b: UNR -> NUR",
        {'UNR': 'NUR'},
        set(),  # NUR already in KNOWN
        "'only' (German), cross-boundary reorder, ~7x"
    ),
    (
        "H6a: RRNI -> NIRR",
        {'RRNI': 'NIRR'},
        {'NIRR'},
        "MHG form, possibly related to IRREN (to err), ~5x"
    ),
    (
        "H6b: RRNI -> IRREN (fragment)",
        {'RRNI': 'IRRE'},
        {'IRRE'},
        "Crazy/astray (German), reduced anagram, ~5x"
    ),
    (
        "H7a: UOD -> OUD",
        {'UOD': 'OUD'},
        {'OUD'},
        "MHG/Dutch form, ~5x"
    ),
    (
        "H7b: UOD -> DUO",
        {'UOD': 'DUO'},
        {'DUO'},
        "Latin/German 'duo', ~5x"
    ),
    (
        "H7c: UOD -> TOD (U->T error?)",
        {'UOD': 'TOD'},
        set(),  # TOD already in KNOWN
        "Death (if code error U->T), ~5x"
    ),
]

results = []

for name, anagram_adds, vocab_adds, description in hypotheses:
    test_map = dict(ANAGRAM_MAP_BASELINE)
    test_map.update(anagram_adds)
    test_known = KNOWN | vocab_adds

    cov, tot, pct, per_book = measure_coverage(test_map, test_known, decoded)
    gain = cov - base_covered
    results.append((name, gain, pct, anagram_adds, vocab_adds))

    print(f"\n--- {name} ---")
    print(f"  Description: {description}")
    for old, new in anagram_adds.items():
        print(f"  Anagram: {old} -> {new}")
    if vocab_adds:
        print(f"  New vocab: {vocab_adds}")
    print(f"  Coverage: {cov}/{tot} = {pct:.2f}%  (delta: {'+' if gain >= 0 else ''}{gain} chars)")

    # Show occurrence count and context
    test_resolved = apply_anagram_map(all_decoded, test_map)
    for old, new in anagram_adds.items():
        # Count how many times the pattern appears in the raw decoded text
        raw_count = all_decoded.count(old)
        # Count how many times the resolution appears after applying the new map
        new_count = test_resolved.count(new)
        base_count = baseline_resolved.count(new)
        net_new = new_count - base_count
        print(f"  '{old}' found {raw_count}x in decoded text")
        print(f"  '{new}' appears {new_count}x after resolution ({net_new} new from this hypothesis)")

        # Show up to 5 occurrences with context
        occurrences = find_occurrences(all_decoded, old, context=12)
        for i, (idx, ctx) in enumerate(occurrences[:5]):
            print(f"    [{i+1}] pos {idx}: ...{ctx}...")
        if len(occurrences) > 5:
            print(f"    ... and {len(occurrences) - 5} more")

    # Show per-book impact (only books that changed)
    changed_books = []
    for bidx, c, t, p in per_book:
        bc, bt, bp = base_per_book[bidx][1], base_per_book[bidx][2], base_per_book[bidx][3]
        if c != bc:
            changed_books.append((bidx, c - bc, p, bp))
    if changed_books:
        print(f"  Per-book changes:")
        for bidx, delta, new_pct, old_pct in sorted(changed_books, key=lambda x: -x[1]):
            print(f"    Book {bidx:2d}: {old_pct:.1f}% -> {new_pct:.1f}% ({'+' if delta >= 0 else ''}{delta} chars)")

# ============================================================
# RANKING
# ============================================================
print(f"\n{'=' * 70}")
print("HYPOTHESIS RANKING BY COVERAGE GAIN")
print("=" * 70)

results.sort(key=lambda x: -x[1])
for rank, (name, gain, pct, _, _) in enumerate(results, 1):
    marker = " ***" if gain > 5 else (" **" if gain > 0 else "")
    print(f"  {rank:2d}. {gain:+4d} chars | {pct:.2f}% | {name}{marker}")

# ============================================================
# CUMULATIVE TEST: Best variant per group (non-conflicting)
# ============================================================
print(f"\n{'=' * 70}")
print("CUMULATIVE TEST: BEST VARIANT PER GROUP (NON-CONFLICTING)")
print("=" * 70)

# Group hypotheses and pick the best variant for each
# H1 has only one variant, H2 has only one, H3 has only one, H4 has only one
# H5 has a/b, H6 has a/b, H7 has a/b/c
groups = {
    'H1': [(n, g, a, v) for n, g, _, a, v in results if n.startswith('H1')],
    'H2': [(n, g, a, v) for n, g, _, a, v in results if n.startswith('H2')],
    'H3': [(n, g, a, v) for n, g, _, a, v in results if n.startswith('H3')],
    'H4': [(n, g, a, v) for n, g, _, a, v in results if n.startswith('H4')],
    'H5': [(n, g, a, v) for n, g, _, a, v in results if n.startswith('H5')],
    'H6': [(n, g, a, v) for n, g, _, a, v in results if n.startswith('H6')],
    'H7': [(n, g, a, v) for n, g, _, a, v in results if n.startswith('H7')],
}

cumul_map = dict(ANAGRAM_MAP_BASELINE)
cumul_known = set(KNOWN)
applied = []
skipped = []

for group_name, variants in sorted(groups.items()):
    best = max(variants, key=lambda x: x[1])
    name, gain, anagram_adds, vocab_adds = best
    if gain > 0:
        cumul_map.update(anagram_adds)
        cumul_known |= vocab_adds
        applied.append((name, gain))
    else:
        skipped.append((name, gain))

cumul_cov, cumul_tot, cumul_pct, cumul_per_book = measure_coverage(
    cumul_map, cumul_known, decoded
)
cumul_gain = cumul_cov - base_covered

print(f"\n  Applied (best per group, positive gain only): {len(applied)}")
for h, g in applied:
    print(f"    + {h} ({g:+d} chars individually)")
if skipped:
    print(f"  Skipped (non-positive gain):")
    for h, g in skipped:
        print(f"    - {h} ({g:+d} chars individually)")

print(f"\n  Cumulative coverage: {cumul_cov}/{cumul_tot} = {cumul_pct:.2f}%")
print(f"  Net gain over baseline: +{cumul_gain} chars")
print(f"  Baseline was: {base_pct:.2f}%")

# Check for regressions
regressions = 0
improvements = 0
print(f"\n  Per-book impact (changed books only):")
for bidx, c, t, p in cumul_per_book:
    bc = base_per_book[bidx][1]
    bp = base_per_book[bidx][3]
    if c != bc:
        delta = c - bc
        if delta < 0:
            regressions += 1
        else:
            improvements += 1
        print(f"    Book {bidx:2d}: {bp:.1f}% -> {p:.1f}% ({'+' if delta >= 0 else ''}{delta} chars)")
print(f"\n  Summary: {improvements} books improved, {regressions} books regressed")

# ============================================================
# FULL CUMULATIVE: ALL hypotheses (including zero/negative gain)
# ============================================================
print(f"\n{'=' * 70}")
print("FULL CUMULATIVE TEST: ALL SESSION 24 HYPOTHESES")
print("=" * 70)

# Pick the best variant for each hypothesis group
# H1: HIHL->HEHL, H2: HECHLLT->HECHELT, H3: NLNDEF->FINDEN
# H4: CHN->NCH, H5: best of UNR->RUN vs UNR->NUR
# H6: best of RRNI variants, H7: best of UOD variants
best_h5 = max(
    [(g, a, v) for n, g, _, a, v in results if 'H5' in n],
    key=lambda x: x[0], default=None
)
best_h6 = max(
    [(g, a, v) for n, g, _, a, v in results if 'H6' in n],
    key=lambda x: x[0], default=None
)
best_h7 = max(
    [(g, a, v) for n, g, _, a, v in results if 'H7' in n],
    key=lambda x: x[0], default=None
)

full_map = dict(ANAGRAM_MAP_BASELINE)
full_known = set(KNOWN)

core_hypotheses = [
    ('H1: HIHL->HEHL', {'HIHL': 'HEHL'}, {'HEHL'}),
    ('H2: HECHLLT->HECHELT', {'HECHLLT': 'HECHELT'}, {'HECHELT'}),
    ('H3: NLNDEF->FINDEN', {'NLNDEF': 'FINDEN'}, set()),
    ('H4: CHN->NCH', {'CHN': 'NCH'}, set()),
]

if best_h5:
    core_hypotheses.append(('H5 (best)', best_h5[1], best_h5[2]))
if best_h6:
    core_hypotheses.append(('H6 (best)', best_h6[1], best_h6[2]))
if best_h7:
    core_hypotheses.append(('H7 (best)', best_h7[1], best_h7[2]))

for name, a, v in core_hypotheses:
    full_map.update(a)
    full_known |= v

full_cov, full_tot, full_pct, full_per_book = measure_coverage(
    full_map, full_known, decoded
)
full_gain = full_cov - base_covered

print(f"\n  All hypotheses combined (best variant per group):")
for name, a, v in core_hypotheses:
    for old, new in a.items():
        print(f"    {name}: {old} -> {new}")
print(f"\n  Full coverage: {full_cov}/{full_tot} = {full_pct:.2f}%")
print(f"  Net gain over baseline: +{full_gain} chars")
print(f"  Baseline was: {base_pct:.2f}%")

# ============================================================
# COLLISION/INTERFERENCE ANALYSIS
# ============================================================
print(f"\n{'=' * 70}")
print("COLLISION/INTERFERENCE ANALYSIS")
print("=" * 70)
print("  Checking if any hypotheses interfere with existing anagram entries...")
print("  NOTE: Anagram map applies longest-first, so a short pattern inside")
print("  a longer key is safe -- the longer key fires first.\n")

# Check if any hypothesis pattern overlaps with existing anagram keys/values
collision_found = False
for name, anagram_adds, vocab_adds, description in hypotheses:
    for old_h, new_h in anagram_adds.items():
        for existing_key, existing_val in ANAGRAM_MAP_BASELINE.items():
            if old_h in existing_key and old_h != existing_key:
                print(f"  INFO: '{old_h}' ({name}) is substring of existing key '{existing_key}'")
                print(f"         -> SAFE: '{existing_key}' ({len(existing_key)} chars) resolves before '{old_h}' ({len(old_h)} chars)")
                collision_found = True
            if old_h in existing_val:
                print(f"  WARNING: '{old_h}' ({name}) appears in existing resolved value '{existing_val}'")
                print(f"           -> DANGER: could corrupt already-resolved text!")
                collision_found = True
            if existing_key in old_h and existing_key != old_h:
                print(f"  INFO: Existing key '{existing_key}' is substring of '{old_h}' ({name})")
                print(f"         -> SAFE: '{old_h}' ({len(old_h)} chars) resolves before '{existing_key}' ({len(existing_key)} chars)")
                collision_found = True
if not collision_found:
    print("  No collisions detected.")

# ============================================================
# CONTEXT DUMP: Show surrounding text for each hypothesis pattern
# ============================================================
print(f"\n{'=' * 70}")
print("CONTEXT DUMP: Where each pattern appears in narrative")
print("=" * 70)

patterns_to_trace = [
    ('HIHL', 'H1'),
    ('HECHLLT', 'H2'),
    ('NLNDEF', 'H3'),
    ('CHN', 'H4'),
    ('UNR', 'H5'),
    ('RRNI', 'H6'),
    ('UOD', 'H7'),
]

for pattern, label in patterns_to_trace:
    occurrences = find_occurrences(baseline_resolved, pattern, context=20)
    print(f"\n  {label}: '{pattern}' ({len(occurrences)} occurrences in resolved text)")
    for i, (idx, ctx) in enumerate(occurrences[:8]):
        print(f"    [{i+1}] pos {idx:5d}: ...{ctx}...")
    if len(occurrences) > 8:
        print(f"    ... and {len(occurrences) - 8} more")

print(f"\n{'=' * 70}")
print("DONE")
print("=" * 70)
