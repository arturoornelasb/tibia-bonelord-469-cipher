#!/usr/bin/env python3
"""
Session 25: Brute-force ALL code reassignments.
For each of the 98 codes, test every possible letter and measure coverage change.
Only accept changes that don't break any confirmed anagram.
"""
import json, os, sys
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
    'RIT', 'EWE', 'MIS', 'AUE', 'EIS',
}

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    return 0 if ic_from_counts(Counter(bp0), len(bp0)) > ic_from_counts(Counter(bp1), len(bp1)) else 1

# Pre-compute book data (pairs per book) to avoid recomputing
book_data = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_data.append(pairs)

def decode_fast(mapping):
    parts = []
    for pairs in book_data:
        parts.append(''.join(mapping.get(p, '?') for p in pairs))
    return ''.join(parts)

def apply_anagrams(text):
    for k in sorted(ANAGRAM_MAP, key=len, reverse=True):
        text = text.replace(k, ANAGRAM_MAP[k])
    return text

def dp_coverage(text):
    n = len(text)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            if text[start:i] in KNOWN and dp[start] + wlen > dp[i]:
                dp[i] = dp[start] + wlen
    return dp[n]

def check_anagrams(raw_text):
    for src in ANAGRAM_MAP:
        if src not in raw_text:
            return False
    return True

# Count code frequencies
code_freq = Counter()
for pairs in book_data:
    for p in pairs:
        code_freq[p] += 1

# Baseline
print("Computing baseline...")
baseline_raw = decode_fast(v7)
baseline_resolved = apply_anagrams(baseline_raw)
total_chars = sum(1 for c in baseline_resolved if c != '?')
baseline_cov = dp_coverage(baseline_resolved)
print(f"Baseline: {baseline_cov}/{total_chars} = {baseline_cov/total_chars*100:.1f}%")

# Unconfirmed codes from FINDINGS.md 10.14 + 10.23
UNCONFIRMED = {
    '35', '66',  # A
    '62',        # B (only B code)
    '02', '63',  # D
    '09', '37', '39', '41', '69', '74', '95',  # E
    '00', '06',  # H
    '38',        # K
    '54',        # M
    '58', '60', '90', '93',  # N (removed 13, already corrected)
    '79',        # O
    '10', '68',  # R
    '92',        # S
    '75', '98',  # T
    '70',        # U
    '77',        # Z
    # From 10.23: also unconfirmed
    '15', '16', '65',  # I
    '33', '36', '87',  # W
}

LETTERS = 'ABCDEFGHIKLMNORSTUWZ'

print(f"\n{'='*60}")
print(f"BRUTE-FORCE ALL {len(UNCONFIRMED)} UNCONFIRMED CODES x {len(LETTERS)} LETTERS")
print(f"{'='*60}")

all_candidates = []
tested = 0
total_tests = len(UNCONFIRMED) * len(LETTERS)

for code in sorted(UNCONFIRMED, key=lambda c: -code_freq.get(c, 0)):
    current = v7.get(code, '?')
    freq = code_freq.get(code, 0)
    best_gain = 0
    best_letter = None

    for letter in LETTERS:
        if letter == current:
            continue
        tested += 1
        if tested % 100 == 0:
            print(f"  Progress: {tested}/{total_tests} ({tested/total_tests*100:.0f}%)", file=sys.stderr)

        test_mapping = dict(v7)
        test_mapping[code] = letter
        test_raw = decode_fast(test_mapping)

        if not check_anagrams(test_raw):
            continue

        test_resolved = apply_anagrams(test_raw)
        test_cov = dp_coverage(test_resolved)
        gain = test_cov - baseline_cov

        if gain > best_gain:
            best_gain = gain
            best_letter = letter

    if best_gain > 0:
        print(f"  Code {code} ({current}, {freq}x): best = {best_letter} (+{best_gain})")
        all_candidates.append((code, current, best_letter, best_gain, freq))
    elif best_gain == 0:
        # Check if any letter gives same coverage (neutral change)
        pass

all_candidates.sort(key=lambda x: -x[3])

print(f"\n{'='*60}")
print(f"RESULTS: {len(all_candidates)} codes with positive gain")
print(f"{'='*60}")

for i, (code, old, new, gain, freq) in enumerate(all_candidates):
    print(f"\n  #{i+1}: Code {code}: {old} -> {new} = +{gain} chars ({freq} occurrences)")
    # Show sample contexts
    test_mapping = dict(v7)
    test_mapping[code] = new
    test_raw = decode_fast(test_mapping)
    test_resolved = apply_anagrams(test_raw)

    # Find where this code appears and show context
    shown = 0
    pos = 0
    for pairs in book_data:
        text_start = pos
        for j, p in enumerate(pairs):
            if p == code and shown < 3:
                char_pos = text_start + j
                if char_pos < len(test_resolved):
                    s = max(0, char_pos - 10)
                    e = min(len(test_resolved), char_pos + 10)
                    old_ctx = baseline_resolved[s:e] if s < len(baseline_resolved) else ''
                    new_ctx = test_resolved[s:e]
                    print(f"       OLD: ...{old_ctx}...")
                    print(f"       NEW: ...{new_ctx}...")
                    shown += 1
        pos += len(pairs)

# Pairwise combinations
if len(all_candidates) >= 2:
    print(f"\n{'='*60}")
    print(f"PAIRWISE COMBINATIONS (top 5)")
    print(f"{'='*60}")

    for i in range(min(5, len(all_candidates))):
        for j in range(i+1, min(5, len(all_candidates))):
            c1 = all_candidates[i]
            c2 = all_candidates[j]
            test_mapping = dict(v7)
            test_mapping[c1[0]] = c1[2]
            test_mapping[c2[0]] = c2[2]
            test_raw = decode_fast(test_mapping)
            if not check_anagrams(test_raw):
                print(f"  {c1[0]}:{c1[1]}->{c1[2]} + {c2[0]}:{c2[1]}->{c2[2]} = BREAKS ANAGRAMS")
                continue
            test_resolved = apply_anagrams(test_raw)
            test_cov = dp_coverage(test_resolved)
            gain = test_cov - baseline_cov
            synergy = gain - c1[3] - c2[3]
            print(f"  {c1[0]}:{c1[1]}->{c1[2]} + {c2[0]}:{c2[1]}->{c2[2]} = +{gain} (synergy: {synergy:+d})")

print("\nDone.")
