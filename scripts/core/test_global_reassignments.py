#!/usr/bin/env python3
"""
Test Global Code Reassignments
===============================
Tests the most promising code reassignments from the crib attack,
measuring their GLOBAL impact on word coverage across all 70 books.

Focus on:
1. Code [97] G -> ? (17% word rate, 58 occ)
2. Code [24] I -> ? (17% word rate, 47 occ)
3. Code [04] M -> ? (19% word rate, 58 occ)
4. Code [83] V -> ? (11% word rate, 28 occ)
5. Code [05] C -> ? (0% word rate, 34 occ)
6. Fix I over-representation by testing I-codes as B, F, P, M
"""

import json, os, sys
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

MAPPING = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U',
    '00': 'H', '14': 'N', '72': 'R', '91': 'S', '15': 'I',
    '76': 'E', '52': 'S', '42': 'D', '46': 'I', '48': 'N',
    '57': 'H', '04': 'M', '12': 'S', '58': 'N',
    '78': 'T', '51': 'R', '35': 'A', '34': 'L',
    '01': 'E', '59': 'S', '41': 'E', '30': 'E',
    '94': 'H',
    '47': 'D', '13': 'N', '71': 'I', '63': 'D',
    '93': 'N', '28': 'D', '86': 'E', '43': 'U',
    '70': 'U', '65': 'I', '16': 'I', '36': 'W',
    '64': 'T', '89': 'A', '80': 'G', '97': 'G', '75': 'T',
    '08': 'R', '20': 'F', '96': 'L', '99': 'O', '55': 'R',
    '67': 'E', '27': 'E', '03': 'E', '09': 'E', '05': 'C', '53': 'N',
    '44': 'U', '62': 'B', '68': 'R',
    '23': 'S', '17': 'E', '29': 'E', '66': 'A', '49': 'E',
    '38': 'K', '77': 'Z',
    '22': 'K', '82': 'O', '73': 'N', '50': 'I', '84': 'G',
    '25': 'O', '83': 'V', '81': 'T', '24': 'I',
    '79': 'O', '10': 'R',
}

GERMAN_WORDS = set([
    'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO',
    'DU', 'OB', 'AM', 'IM', 'AB',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST',
    'WIR', 'ICH', 'SIE', 'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI', 'VOR', 'FUR', 'VOM',
    'ZUM', 'ZUR', 'BIS', 'ALS', 'NUN', 'HIN', 'TAG', 'ORT', 'TOD',
    'OFT', 'NIE', 'ALT', 'NEU', 'GAR', 'NET', 'ODE', 'SEI', 'TUN',
    'MAL', 'RAT', 'ENDE', 'REDE', 'RUNE', 'WORT', 'NACH', 'AUCH',
    'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN', 'WARD', 'DASS', 'WENN',
    'DANN', 'DENN', 'ABER', 'ODER', 'WEIL', 'WIRD', 'EINE', 'DIES',
    'HIER', 'DORT', 'WELT', 'ZEIT', 'TEIL', 'SEID', 'WORT', 'NAME',
    'GANZ', 'SEHR', 'VIEL', 'FORT', 'HOCH', 'KLAR', 'ERDE', 'GOTT',
    'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN', 'WAHR', 'HELD', 'FACH',
    'WIND', 'FAND', 'GING', 'NAHM', 'SAGT', 'KANN', 'SOLL', 'WILL',
    'MUSS', 'GIBT', 'RIEF',
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
    'HIHL',
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

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

def dp_coverage(m, word_set=GERMAN_WORDS):
    """Calculate total word coverage across all books."""
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

# ============================================================
# BASELINE
# ============================================================

print("=" * 70)
print("GLOBAL REASSIGNMENT TESTING")
print("=" * 70)

baseline_cov, baseline_total = dp_coverage(MAPPING)
baseline_pct = baseline_cov / baseline_total * 100
print(f"\nBaseline: {baseline_cov}/{baseline_total} = {baseline_pct:.2f}%")

# ============================================================
# TEST EACH SUSPICIOUS CODE WITH ALL 26 LETTERS
# ============================================================

suspicious_codes = [
    ('97', 'G', 58, "17% word rate, crib: +20 as N"),
    ('24', 'I', 47, "17% word rate, was R in v4"),
    ('04', 'M', 58, "19% word rate, M under-represented"),
    ('83', 'V', 28, "11% word rate"),
    ('05', 'C', 34, "0% word rate, gap-only"),
    ('71', 'I', 33, "was N in v4, I over-represented"),
    ('50', 'I', 35, "I over-represented"),
    ('65', 'I', 71, "I over-represented"),
    ('16', 'I', 38, "I over-represented"),
]

all_improvements = []

for code, current, occ, reason in suspicious_codes:
    print(f"\n{'=' * 70}")
    print(f"Testing code [{code}] = {current} ({occ} occ) - {reason}")
    print(f"{'=' * 70}")

    results = []
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        test_map = dict(MAPPING)
        test_map[code] = letter
        cov, total = dp_coverage(test_map)
        pct = cov / total * 100
        delta = pct - baseline_pct
        results.append((letter, pct, delta))

    results.sort(key=lambda x: -x[1])

    print(f"\n  Top 10 assignments (current = {current}):")
    for letter, pct, delta in results[:10]:
        marker = " <-- CURRENT" if letter == current else ""
        marker = " *** BEST" if delta > 0 and results[0][0] == letter else marker
        print(f"    {letter}: {pct:.2f}% ({delta:+.2f}%){marker}")

    # Record if there's an improvement
    best_letter, best_pct, best_delta = results[0]
    if best_letter != current and best_delta > 0.05:
        all_improvements.append({
            'code': code,
            'current': current,
            'best': best_letter,
            'delta': best_delta,
            'occ': occ,
        })

# ============================================================
# SUMMARY OF IMPROVEMENTS
# ============================================================

print(f"\n{'=' * 70}")
print("SUMMARY: CODES THAT IMPROVE COVERAGE WHEN CHANGED")
print(f"{'=' * 70}")

all_improvements.sort(key=lambda x: -x['delta'])

if not all_improvements:
    print("\n  No individual code change improves coverage by >0.05%")
else:
    for imp in all_improvements:
        print(f"\n  [{imp['code']}] {imp['current']} -> {imp['best']}: "
              f"+{imp['delta']:.2f}% ({imp['occ']} occurrences)")

# ============================================================
# TEST COMBINATIONS OF TOP IMPROVEMENTS
# ============================================================

if len(all_improvements) >= 2:
    print(f"\n{'=' * 70}")
    print("COMBINATION TESTS")
    print(f"{'=' * 70}")

    # Try all pairs
    for i in range(len(all_improvements)):
        for j in range(i + 1, len(all_improvements)):
            a = all_improvements[i]
            b = all_improvements[j]
            test_map = dict(MAPPING)
            test_map[a['code']] = a['best']
            test_map[b['code']] = b['best']
            cov, total = dp_coverage(test_map)
            pct = cov / total * 100
            delta = pct - baseline_pct
            print(f"  [{a['code']}]{a['current']}->{a['best']} + "
                  f"[{b['code']}]{b['current']}->{b['best']}: "
                  f"{pct:.2f}% ({delta:+.2f}%)")

    # Try all at once
    if len(all_improvements) >= 3:
        test_map = dict(MAPPING)
        for imp in all_improvements:
            test_map[imp['code']] = imp['best']
        cov, total = dp_coverage(test_map)
        pct = cov / total * 100
        delta = pct - baseline_pct
        changes = ' + '.join(f"[{i['code']}]{i['current']}->{i['best']}" for i in all_improvements)
        print(f"\n  ALL: {changes}")
        print(f"  Result: {pct:.2f}% ({delta:+.2f}%)")

# ============================================================
# SHOW TEXT IMPACT FOR BEST CHANGES
# ============================================================

if all_improvements:
    print(f"\n{'=' * 70}")
    print("TEXT COMPARISON FOR BEST CHANGE")
    print(f"{'=' * 70}")

    best = all_improvements[0]
    test_map = dict(MAPPING)
    test_map[best['code']] = best['best']

    for bidx in [0, 2, 5, 9, 31, 46, 53]:
        bpairs = book_pairs[bidx]
        old = ''.join(MAPPING.get(p, '?') for p in bpairs)
        new = ''.join(test_map.get(p, '?') for p in bpairs)

        if old != new:
            print(f"\n  Book {bidx}:")
            # Find differences
            for i in range(len(old)):
                if old[i] != new[i]:
                    ctx_s = max(0, i - 12)
                    ctx_e = min(len(old), i + 12)
                    print(f"    old: ...{old[ctx_s:ctx_e]}...")
                    print(f"    new: ...{new[ctx_s:ctx_e]}...")
                    break
