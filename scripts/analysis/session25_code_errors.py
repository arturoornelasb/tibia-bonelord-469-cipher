#!/usr/bin/env python3
"""
Session 25: Systematic code error detection.
Test all unconfirmed codes for potential mapping corrections.
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

KNOWN = {
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN', 'TUT',
    'SAG', 'WAR', 'NU', 'SIN', 'STANDE', 'NACHTS', 'NIT', 'TOT', 'TER',
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
    'ZEHN', 'ZORN', 'FINDEN', 'GEBEN', 'GEHEN', 'HABEN', 'KOMMEN',
    'LEBEN', 'LESEN', 'NEHMEN', 'SAGEN', 'SEHEN', 'STEHEN', 'SUCHEN',
    'WISSEN', 'WISSET', 'RUFEN', 'WIEDER', 'OEL', 'SCE', 'MINNE',
    'MIN', 'HEL', 'ODE', 'SER', 'GEN', 'INS', 'GEIGET',
    'BERUCHTIG', 'BERUCHTIGER', 'MEERE', 'NEIGT', 'WISTEN', 'MANIER',
    'HUND', 'GODE', 'GODES', 'EIGENTUM', 'REDER', 'THENAEUT',
    'LABT', 'MORT', 'DIGE', 'WEGE', 'KOENIGS', 'NAHE', 'NOT', 'NOTH',
    'ZUR', 'OWI', 'ENGE', 'SEIDEN', 'ALTES', 'BIS', 'NUT', 'NUTZ',
    'HEIL', 'NEID', 'TREU', 'TREUE', 'SUN', 'DIENST', 'SANG', 'DINC',
    'HULDE', 'STEINE', 'LANT', 'HERRE', 'DIENEST', 'GEBOT', 'SCHWUR',
    'ORDEN', 'RICHTER', 'DUNKEL', 'EHRE', 'EDELE', 'SCHULD', 'SEGEN',
    'FLUCH', 'RACHE', 'KOENIG', 'DASS', 'EDEL', 'ADEL', 'SCHRAT',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE', 'GOTTDIENER',
    'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME', 'SCHARDT',
    'HEL', 'RIT', 'EWE', 'SIN', 'MIS', 'AUE', 'EIS',
}

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    return 0 if ic_from_counts(Counter(bp0), len(bp0)) > ic_from_counts(Counter(bp1), len(bp1)) else 1

def decode_with_mapping(mapping):
    decoded = []
    for bidx, book in enumerate(books):
        if bidx in DIGIT_SPLITS:
            p, d = DIGIT_SPLITS[bidx]
            book = book[:p] + d + book[p:]
        off = get_offset(book)
        pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
        decoded.append(''.join(mapping.get(p, '?') for p in pairs))
    return ''.join(decoded)

def apply_anagrams(text, amap):
    for k in sorted(amap, key=len, reverse=True):
        text = text.replace(k, amap[k])
    return text

def dp_coverage(text, vocab):
    n = len(text)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            if text[start:i] in vocab and dp[start] + wlen > dp[i]:
                dp[i] = dp[start] + wlen
    return dp[n]

def check_anagrams_intact(text, amap):
    """Check all anagram source strings still appear in pre-anagram text."""
    for src in amap:
        if src not in text:
            return False
    return True

# Baseline
print("Computing baseline...")
baseline_raw = decode_with_mapping(v7)
baseline_resolved = apply_anagrams(baseline_raw, ANAGRAM_MAP)
total_chars = sum(1 for c in baseline_resolved if c != '?')
baseline_cov = dp_coverage(baseline_resolved, KNOWN)
print(f"Baseline: {baseline_cov}/{total_chars} = {baseline_cov/total_chars*100:.1f}%")

# Step 1: Compute garbled rate per code
print("\n" + "="*60)
print("GARBLED RATE PER CODE")
print("="*60)

# For each code, find positions in raw text and check if covered
code_positions = {code: [] for code in v7}
pos = 0
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    for i, pair in enumerate(pairs):
        if pair in v7:
            code_positions[pair].append(pos + i)
    pos += len(pairs)

# DP to find covered positions
n = len(baseline_resolved)
dp = [0] * (n + 1)
dp_back = [None] * (n + 1)
for i in range(1, n + 1):
    dp[i] = dp[i-1]
    for wlen in range(2, min(i, 20) + 1):
        start = i - wlen
        if baseline_resolved[start:i] in KNOWN and dp[start] + wlen > dp[i]:
            dp[i] = dp[start] + wlen
            dp_back[i] = start

# Backtrack to find covered positions
covered_pos = set()
i = n
while i > 0:
    if dp_back[i] is not None:
        for j in range(dp_back[i], i):
            covered_pos.add(j)
        i = dp_back[i]
    else:
        i -= 1

# Compute garbled rate per code
high_garbled = []
print(f"\n{'Code':>5} {'Letter':>7} {'Total':>6} {'Garbled':>8} {'Rate':>6}")
print("-" * 40)
for code in sorted(v7.keys(), key=lambda c: int(c)):
    positions = code_positions.get(code, [])
    if not positions:
        continue
    garbled = sum(1 for p in positions if p < n and p not in covered_pos)
    total = len(positions)
    rate = garbled / total * 100 if total > 0 else 0
    if rate > 50:
        print(f"  {code:>3} -> {v7[code]:>3}   {total:>5}   {garbled:>5}   {rate:>5.1f}%")
        high_garbled.append((code, v7[code], total, rate))

high_garbled.sort(key=lambda x: -x[3])
print(f"\n{len(high_garbled)} codes with >50% garbled rate")

# Step 2: Test reassignments for high-garbled codes
print("\n" + "="*60)
print("TESTING REASSIGNMENTS FOR HIGH-GARBLED CODES")
print("="*60)

LETTERS = list('ABCDEFGHIKLMNORSTUWZ')  # German alphabet without rare J/P/Q/V/X/Y
# Add rarer letters
LETTERS += list('JPVXY')

candidates = []
for code, current_letter, total, rate in high_garbled:
    if rate < 55:  # Focus on worst offenders
        continue
    best_gain = 0
    best_letter = None
    for letter in LETTERS:
        if letter == current_letter:
            continue
        # Create modified mapping
        test_mapping = dict(v7)
        test_mapping[code] = letter
        # Decode
        test_raw = decode_with_mapping(test_mapping)
        # Check anagrams still intact
        if not check_anagrams_intact(test_raw, ANAGRAM_MAP):
            continue
        # Apply anagrams and measure coverage
        test_resolved = apply_anagrams(test_raw, ANAGRAM_MAP)
        test_cov = dp_coverage(test_resolved, KNOWN)
        gain = test_cov - baseline_cov
        if gain > best_gain:
            best_gain = gain
            best_letter = letter

    if best_gain > 0:
        print(f"  Code {code}: {current_letter} -> {best_letter} = +{best_gain} chars (garbled rate: {rate:.1f}%)")
        candidates.append((code, current_letter, best_letter, best_gain, rate))

candidates.sort(key=lambda x: -x[3])
print(f"\n{'='*60}")
print(f"TOP CANDIDATES (ranked by coverage gain)")
print(f"{'='*60}")
for i, (code, old, new, gain, rate) in enumerate(candidates[:10]):
    print(f"  #{i+1}: Code {code}: {old} -> {new} = +{gain} chars (garbled: {rate:.0f}%)")
    # Show contexts
    test_mapping = dict(v7)
    test_mapping[code] = new
    test_raw = decode_with_mapping(test_mapping)
    test_resolved = apply_anagrams(test_raw, ANAGRAM_MAP)
    # Find positions where this code appears
    for pos in code_positions[code][:3]:
        if pos < len(test_resolved):
            start = max(0, pos - 8)
            end = min(len(test_resolved), pos + 8)
            print(f"       ...{test_resolved[start:end]}...")

# Step 3: Test pairwise combinations of top candidates
if len(candidates) >= 2:
    print(f"\n{'='*60}")
    print(f"PAIRWISE COMBINATION TESTS")
    print(f"{'='*60}")
    for i in range(min(5, len(candidates))):
        for j in range(i+1, min(5, len(candidates))):
            c1 = candidates[i]
            c2 = candidates[j]
            test_mapping = dict(v7)
            test_mapping[c1[0]] = c1[2]
            test_mapping[c2[0]] = c2[2]
            test_raw = decode_with_mapping(test_mapping)
            if not check_anagrams_intact(test_raw, ANAGRAM_MAP):
                continue
            test_resolved = apply_anagrams(test_raw, ANAGRAM_MAP)
            test_cov = dp_coverage(test_resolved, KNOWN)
            gain = test_cov - baseline_cov
            print(f"  {c1[0]}:{c1[1]}->{c1[2]} + {c2[0]}:{c2[1]}->{c2[2]} = +{gain} (individual sum: +{c1[3]+c2[3]})")

print("\nDone.")
