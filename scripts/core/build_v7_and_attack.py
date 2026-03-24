#!/usr/bin/env python3
"""
Build mapping v7: comprehensive mapping + multi-pronged attack
===============================================================
1. Start from v6 (best confirmed)
2. Add back missing codes from v4 (02,33,37,39,40,54,69,74,87,98)
3. Test each addition's impact on global coverage
4. Test [91] S->A hypothesis (NSCHA -> NACH)
5. Exhaustive sweep: for EVERY code, test all 26 letters
6. Find the global optimum mapping
"""

import json, os, sys
from collections import Counter
from itertools import combinations

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

# V6 mapping (our best so far)
V6 = {
    "00": "H", "01": "E", "03": "E", "04": "M", "05": "S",
    "06": "H", "08": "R", "09": "E", "10": "R", "11": "N",
    "12": "S", "13": "N", "14": "N", "15": "I", "16": "I",
    "17": "E", "18": "C", "19": "E", "20": "F", "21": "I",
    "22": "K", "23": "S", "24": "R", "25": "O", "26": "E",
    "27": "E", "28": "D", "29": "E", "30": "E", "31": "A",
    "34": "L", "35": "A", "36": "W", "38": "K", "41": "E",
    "42": "D", "43": "U", "44": "U", "45": "D", "46": "I",
    "47": "D", "48": "N", "49": "E", "50": "I", "51": "R",
    "52": "S", "53": "N", "55": "R", "56": "E", "57": "H",
    "58": "N", "59": "S", "60": "N", "61": "U", "62": "B",
    "63": "D", "64": "T", "65": "I", "66": "A", "67": "E",
    "68": "R", "70": "U", "71": "N", "72": "R", "73": "N",
    "75": "T", "76": "E", "77": "Z", "78": "T", "79": "O",
    "80": "G", "81": "T", "82": "O", "83": "N", "84": "G",
    "85": "A", "86": "E", "88": "T", "89": "A", "90": "N",
    "91": "S", "92": "S", "93": "N", "94": "H", "95": "E",
    "96": "L", "97": "G", "99": "O",
}

# Codes in v4 but missing from v6
V4_EXTRAS = {
    "02": "D", "33": "W", "37": "E", "39": "E",
    "40": "M", "54": "M", "69": "E", "74": "E",
    "87": "W", "98": "T",
}

GERMAN_WORDS = set([
    'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO',
    'DU', 'OB', 'AM', 'IM', 'AB',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST',
    'WIR', 'ICH', 'SIE', 'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI', 'VOR', 'FUR', 'VOM',
    'ZUM', 'ZUR', 'BIS', 'ALS', 'NUN', 'HIN', 'TAG', 'ORT', 'TOD',
    'OFT', 'NIE', 'ALT', 'NEU', 'GAR', 'NET', 'ODE', 'SEI', 'TUN',
    'MAL', 'RAT', 'RUF', 'MUT', 'HUT', 'NOT', 'ROT', 'TAT',
    'ENDE', 'REDE', 'RUNE', 'WORT', 'NACH', 'AUCH',
    'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN', 'WARD', 'DASS', 'WENN',
    'DANN', 'DENN', 'ABER', 'ODER', 'WEIL', 'WIRD', 'EINE', 'DIES',
    'HIER', 'DORT', 'WELT', 'ZEIT', 'TEIL', 'SEID', 'WORT', 'NAME',
    'GANZ', 'SEHR', 'VIEL', 'FORT', 'HOCH', 'KLAR', 'ERDE', 'GOTT',
    'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN', 'WAHR', 'HELD', 'FACH',
    'WIND', 'FAND', 'GING', 'NAHM', 'SAGT', 'KANN', 'SOLL', 'WILL',
    'MUSS', 'GIBT', 'RIEF', 'LAND', 'HAND', 'BAND', 'SAND', 'WAND',
    'MACHT', 'KRAFT', 'GEIST', 'NACHT', 'LICHT', 'KRIEG', 'REICH',
    'UNTER', 'DURCH', 'GEGEN', 'IMMER', 'NICHT', 'SCHON',
    'DIESE', 'SEINE', 'EINEN', 'EINER', 'EINEM', 'EINES',
    'URALTE', 'STEINEN', 'STEINE', 'STEIN', 'RUNEN', 'FINDEN',
    'STEHEN', 'GEHEN', 'KOMMEN', 'SAGEN', 'WISSEN',
    'ERSTE', 'ANDEREN', 'KOENIG', 'SCHAUN', 'RUIN',
    'ORTE', 'ORTEN', 'WORTE', 'STEH', 'GEH',
    'ALLE', 'ALLES', 'VIELE', 'WIEDER', 'WISSET',
    'SPRACH', 'GESCHAH', 'GEFUNDEN', 'GEBOREN', 'GESTORBEN',
    'ZWISCHEN', 'HEILIG', 'DUNKEL', 'SCHWERT',
    'STIMME', 'ZEICHEN', 'HIMMEL', 'SEELE', 'GEHEIMNIS',
    'MIN', 'SER', 'GEN', 'WEG', 'INS', 'HER',
    'SEI', 'LIES', 'SAG', 'GIB', 'WAR', 'GAR',
    'REDE', 'REDEN', 'WESEN', 'EHRE', 'TREUE', 'GRAB', 'GRUFT',
    'ALTE', 'ALTEN', 'ALTER', 'NEUE', 'NEUEN',
    'DUNKLE', 'DUNKLEN',
    'HWND', 'OEL', 'SCE', 'MINNE', 'RUCHTIG',
    'HEARUCHTIG', 'HEARUCHTIGER',
    'LABGZERAS', 'HEDEMI', 'ADTHARSC', 'TAUTR',
    'TOTNIURG', 'TOTNIURGS', 'EDETOTNIURG', 'EDETOTNIURGS',
    'SCHWITEIONE', 'SCHWITEIO', 'ENGCHD', 'KELSEI',
    'TIUMENGEMI', 'LABRNI', 'UTRUNR', 'GEVMT',
    'AUNRSONGETRASES', 'EILCH', 'EILCHANHEARUCHTIG',
    'DIESEN', 'DIESEM', 'DIESER', 'DIESES',
    'SEINER', 'SEINEN', 'SEINES', 'SEINEM',
    'NORDEN', 'SUEDEN', 'OSTEN', 'WESTEN',
    'RUNEORT', 'RUNENSTEIN',
    'EDEL', 'ADEL', 'HARSCH', 'SCHAR',
    'HIHL', 'SANG', 'SANG',
    # Additional common German words for better coverage
    'TEIL', 'TEILE', 'TEILEN', 'SEITE', 'SEITEN',
    'GROSSE', 'GROSSEN', 'GROSS', 'KLEINE', 'KLEINEN', 'KLEIN',
    'TAGE', 'TAGEN', 'NEBEN', 'HINEIN', 'HINAUS',
    'LIESS', 'SAGTE', 'WURDE', 'WAREN', 'HATTE',
    'HABEN', 'LEBEN', 'SEHEN', 'NEHMEN', 'GEBEN',
    'HALTEN', 'LASSEN', 'FALLEN', 'TRAGEN', 'SCHLAGEN',
    'BRINGEN', 'DENKEN', 'KENNEN', 'NENNEN', 'BRENNEN',
    'IHRER', 'IHREN', 'IHREM', 'IHRES',
    'MEINER', 'MEINEN', 'MEINEM', 'MEINES',
    'UNSER', 'UNSERE', 'UNSEREN', 'UNSEREM', 'UNSERES',
    'WELCHE', 'WELCHEN', 'WELCHEM', 'WELCHER', 'WELCHES',
    'JEDER', 'JEDE', 'JEDEN', 'JEDEM', 'JEDES',
    'KEIN', 'KEINE', 'KEINEN', 'KEINEM', 'KEINES',
    'MEHR', 'WENIG', 'WENIGE', 'BEIDE', 'BEIDEN',
    'SOLCH', 'SOLCHE', 'SOLCHEN', 'SOLCHEM', 'SOLCHER',
    'WIE', 'ODER', 'SONDERN', 'WEDER', 'NOCH',
    'ERST', 'SCHON', 'NOCH', 'EBEN', 'WOHL',
    'RECHT', 'SCHLECHT', 'SCHNELL', 'STARK', 'SCHWACH',
    'OBEN', 'UNTEN', 'RECHTS', 'LINKS', 'VORN',
    'INNEN', 'AUSSEN',
    'FEUER', 'WASSER', 'STEIN', 'HOLZ', 'EISEN',
    'STERN', 'STERNE', 'STERNEN', 'MOND', 'SONNE',
    'BLUT', 'BEIN', 'HERZ', 'LEIB', 'HAUPT',
    'HELM', 'SCHILD', 'PFEIL', 'BOGEN',
    'FLUCHT', 'FURCHT', 'ZORN', 'STOLZ', 'SCHULD',
    'FRIEDE', 'FRIEDEN', 'FREUND', 'FEIND',
    'WAFFE', 'WAFFEN', 'KLINGE', 'KLINGEN',
    'DRACHE', 'DRACHEN', 'RIESE', 'RIESEN',
    'ZAUBER', 'FLUCH', 'SEGEN', 'BANN',
    'GEBET', 'OPFER', 'ALTAR',
    'GRAB', 'GRUFT', 'GROTTE', 'HOEHLE',
    'TURM', 'MAUER', 'BRUCKE', 'STRASSE',
    'DORF', 'STADT', 'SCHLOSS', 'TEMPEL',
    'WALD', 'WIESE', 'FLUSS', 'MEER', 'INSEL',
    'KNECHT', 'KRIEGER', 'PRIESTER', 'MAGIER',
    'TOCHTER', 'BRUDER', 'SCHWESTER', 'MUTTER', 'VATER',
    'VOLKE', 'VOELKER', 'STAMM',
    'THRONE', 'KRONE', 'SCEPTER',
    'RITTER', 'GRAF', 'FUERST', 'HERZOG',
    'SAGE', 'SAGEN', 'LEGENDE', 'MYTHOS',
    'RUHE', 'STILLE', 'SCHWEIGEN',
    'MACHT', 'OHNMACHT', 'GEWALT',
    'DIENST', 'TREUE', 'PFLICHT',
    'GRENZE', 'GRENZEN', 'GEBIET',
    'WACHE', 'WACHT', 'HUETER',
    'ZEICHEN', 'SCHRIFT', 'SIEGEL',
    'ACHT', 'NEUN', 'ZEHN', 'DREI', 'VIER', 'FUENF',
    'SECHS', 'SIEBEN', 'ZWEI', 'EINS',
    'HUNDERT', 'TAUSEND',
])

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

# Pre-compute book pairs
book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# Count code occurrences
code_counts = Counter()
for bpairs in book_pairs:
    code_counts.update(bpairs)

def dp_coverage(m, word_set=GERMAN_WORDS):
    total_chars = 0
    total_covered = 0
    for bpairs in book_pairs:
        text = ''.join(m.get(p, '?') for p in bpairs)
        n = len(text)
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i-1]
            for wlen in range(2, min(i, 20) + 1):
                start = i - wlen
                cand = text[start:i]
                if '?' not in cand and cand in word_set:
                    dp[i] = max(dp[i], dp[start] + wlen)
        known = sum(1 for c in text if c != '?')
        total_chars += known
        total_covered += dp[n]
    return total_covered, total_chars

print("=" * 70)
print("MAPPING V7 CONSTRUCTION")
print("=" * 70)

# ============================================================
# PHASE 1: Baseline with v6
# ============================================================
base_cov, base_total = dp_coverage(V6)
base_pct = base_cov / base_total * 100
print(f"\nV6 baseline: {base_cov}/{base_total} = {base_pct:.2f}%")

# ============================================================
# PHASE 2: Test adding each v4 extra code
# ============================================================
print(f"\n{'=' * 70}")
print("PHASE 2: ADDING BACK V4 CODES")
print(f"{'=' * 70}")

v4_improvements = []
for code, letter in sorted(V4_EXTRAS.items()):
    occ = code_counts.get(code, 0)
    test_map = dict(V6)
    test_map[code] = letter
    cov, total = dp_coverage(test_map)
    pct = cov / total * 100
    delta = pct - base_pct
    marker = " *** IMPROVES" if delta > 0.01 else ""
    print(f"  [{code}]={letter} ({occ} occ): {pct:.2f}% ({delta:+.3f}%){marker}")
    if delta > 0.01:
        v4_improvements.append((code, letter, delta, occ))

# Add all v4 codes at once
v6_plus = dict(V6)
v6_plus.update(V4_EXTRAS)
cov, total = dp_coverage(v6_plus)
pct = cov / total * 100
delta = pct - base_pct
print(f"\n  ALL v4 codes added: {pct:.2f}% ({delta:+.3f}%)")

# ============================================================
# PHASE 3: For v4 extras, test all 26 letters (maybe v4 was wrong)
# ============================================================
print(f"\n{'=' * 70}")
print("PHASE 3: OPTIMIZE V4 EXTRA CODES (test all 26 letters)")
print(f"{'=' * 70}")

# Use v6+v4 as new baseline
new_base = dict(v6_plus)
new_base_cov, new_base_total = dp_coverage(new_base)
new_base_pct = new_base_cov / new_base_total * 100

optimized_changes = {}
for code, v4_letter in sorted(V4_EXTRAS.items()):
    occ = code_counts.get(code, 0)
    if occ < 3:
        print(f"\n  [{code}] skipped ({occ} occ, too rare)")
        continue

    results = []
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        test_map = dict(new_base)
        test_map[code] = letter
        cov, total = dp_coverage(test_map)
        pct = cov / total * 100
        results.append((letter, pct))

    results.sort(key=lambda x: -x[1])
    best_letter, best_pct = results[0]
    v4_pct = next(p for l, p in results if l == v4_letter)

    print(f"\n  [{code}] ({occ} occ) v4={v4_letter} ({v4_pct:.2f}%), best={best_letter} ({best_pct:.2f}%)")
    print(f"    Top 5: {', '.join(f'{l}={p:.2f}%' for l, p in results[:5])}")

    if best_letter != v4_letter:
        optimized_changes[code] = best_letter

# ============================================================
# PHASE 4: Test [91] S->A hypothesis (NSCHA -> NACH)
# ============================================================
print(f"\n{'=' * 70}")
print("PHASE 4: TESTING [91] S->A HYPOTHESIS")
print(f"{'=' * 70}")

test_map = dict(new_base)
occ_91 = code_counts.get('91', 0)
print(f"  Code [91] has {occ_91} occurrences")

results_91 = []
for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    test_map_91 = dict(new_base)
    test_map_91['91'] = letter
    cov, total = dp_coverage(test_map_91)
    pct = cov / total * 100
    results_91.append((letter, pct))

results_91.sort(key=lambda x: -x[1])
print(f"  Current S: {next(p for l, p in results_91 if l == 'S'):.2f}%")
print(f"  Top 5: {', '.join(f'{l}={p:.2f}%' for l, p in results_91[:5])}")

# ============================================================
# PHASE 5: Full exhaustive sweep of ALL codes
# ============================================================
print(f"\n{'=' * 70}")
print("PHASE 5: EXHAUSTIVE SWEEP - ALL CODES")
print(f"{'=' * 70}")

all_codes_in_data = set()
for bpairs in book_pairs:
    all_codes_in_data.update(bpairs)

print(f"  Total unique codes in data: {len(all_codes_in_data)}")
print(f"  Codes in v6+v4 mapping: {len(new_base)}")
print(f"  Unmapped codes: {sorted(all_codes_in_data - set(new_base.keys()))}")

# For each currently mapped code, check if a different letter would be better
improvements = []
for code in sorted(new_base.keys()):
    occ = code_counts.get(code, 0)
    if occ < 5:
        continue

    current = new_base[code]
    best_letter = current
    best_pct = new_base_pct

    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if letter == current:
            continue
        test_map = dict(new_base)
        test_map[code] = letter
        cov, total = dp_coverage(test_map)
        pct = cov / total * 100
        if pct > best_pct + 0.05:
            best_pct = pct
            best_letter = letter

    if best_letter != current:
        delta = best_pct - new_base_pct
        improvements.append((code, current, best_letter, delta, occ))

improvements.sort(key=lambda x: -x[3])
print(f"\n  Codes where a different letter improves coverage >0.05%:")
for code, current, best, delta, occ in improvements:
    print(f"    [{code}] {current} -> {best}: +{delta:.2f}% ({occ} occ)")

# ============================================================
# PHASE 6: Build v7 with all improvements
# ============================================================
print(f"\n{'=' * 70}")
print("PHASE 6: BUILDING MAPPING V7")
print(f"{'=' * 70}")

v7 = dict(new_base)
# Apply optimized changes for v4 extras
for code, letter in optimized_changes.items():
    if code_counts.get(code, 0) >= 5:
        v7[code] = letter

# Apply improvements from exhaustive sweep
for code, current, best, delta, occ in improvements:
    v7[code] = best

# Test v7
v7_cov, v7_total = dp_coverage(v7)
v7_pct = v7_cov / v7_total * 100
print(f"\n  V6 baseline:  {base_pct:.2f}%")
print(f"  V6+v4 codes:  {new_base_pct:.2f}%")
print(f"  V7 optimized: {v7_pct:.2f}%")

# List all changes from v6
print(f"\n  Changes from v6:")
all_keys = sorted(set(list(V6.keys()) + list(v7.keys())))
for code in all_keys:
    v6_val = V6.get(code, '-')
    v7_val = v7.get(code, '-')
    if v6_val != v7_val:
        occ = code_counts.get(code, 0)
        print(f"    [{code}] {v6_val} -> {v7_val} ({occ} occ)")

# ============================================================
# PHASE 7: Letter frequency analysis of v7
# ============================================================
print(f"\n{'=' * 70}")
print("PHASE 7: LETTER FREQUENCY ANALYSIS (V7)")
print(f"{'=' * 70}")

# German letter frequencies (approximate)
GERMAN_FREQ = {
    'E': 16.93, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
    'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
    'L': 3.44, 'C': 3.06, 'G': 3.01, 'M': 2.53, 'O': 2.51,
    'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
    'P': 0.79, 'V': 0.67, 'J': 0.27, 'Y': 0.04, 'X': 0.03,
    'Q': 0.02,
}

# Count letters in v7 decoded text
letter_counts = Counter()
total_letters = 0
for bpairs in book_pairs:
    for p in bpairs:
        if p in v7:
            letter_counts[v7[p]] += 1
            total_letters += 1

print(f"\n  {'Letter':>6} {'Count':>6} {'Actual%':>8} {'German%':>8} {'Delta':>8} {'Codes':>6}")
print(f"  {'-'*6:>6} {'-'*6:>6} {'-'*8:>8} {'-'*8:>8} {'-'*8:>8} {'-'*6:>6}")

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    count = letter_counts.get(letter, 0)
    actual_pct = count / total_letters * 100 if total_letters > 0 else 0
    german_pct = GERMAN_FREQ.get(letter, 0)
    delta = actual_pct - german_pct
    num_codes = sum(1 for v in v7.values() if v == letter)
    flag = " <<<" if abs(delta) > 2.0 else ""
    if actual_pct > 0 or german_pct > 0.5:
        print(f"  {letter:>6} {count:>6} {actual_pct:>7.2f}% {german_pct:>7.2f}% {delta:>+7.2f}% {num_codes:>6}{flag}")

# ============================================================
# PHASE 8: Show decoded text samples with v7
# ============================================================
print(f"\n{'=' * 70}")
print("PHASE 8: DECODED TEXT SAMPLES (V7)")
print(f"{'=' * 70}")

def dp_parse(text, word_set=GERMAN_WORDS):
    n = len(text)
    dp = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], None)
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if '?' not in cand and cand in word_set:
                score = dp[start][0] + wlen
                if score > dp[i][0]:
                    dp[i] = (score, (start, cand))
    tokens = []
    i = n
    while i > 0:
        if dp[i][1] is not None:
            start, word = dp[i][1]
            tokens.append(('WORD', word))
            i = start
        else:
            tokens.append(('CHAR', text[i-1]))
            i -= 1
    tokens.reverse()
    merged = []
    for kind, val in tokens:
        if kind == 'WORD':
            merged.append(val)
        else:
            if merged and merged[-1].startswith('['):
                merged[-1] = merged[-1][:-1] + val + ']'
            else:
                merged.append('[' + val + ']')
    return merged, dp[n][0]

for idx, bpairs in enumerate(book_pairs):
    if len(bpairs) < 30:
        continue
    text = ''.join(v7.get(p, '?') for p in bpairs)
    tokens, covered = dp_parse(text)
    known = sum(1 for c in text if c != '?')
    pct = covered / max(known, 1) * 100
    parsed = ' '.join(tokens)
    print(f"\nBook {idx:2d} ({pct:2.0f}%): {parsed[:300]}")

# Save v7
v7_path = os.path.join(data_dir, 'mapping_v7.json')
with open(v7_path, 'w') as f:
    json.dump(v7, f, indent=2, sort_keys=True)
print(f"\n\nMapping v7 saved to {v7_path}")
print(f"Total codes mapped: {len(v7)}")
