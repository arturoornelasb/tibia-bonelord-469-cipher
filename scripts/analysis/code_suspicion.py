#!/usr/bin/env python3
"""
Analyze which digit codes appear most often in garbled (unrecognized) text.
High garbled ratio = possible mapping error.
"""
import json, os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

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

KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR', 'ODE', 'SER', 'GEN', 'INS', 'MIN', 'OEL', 'SCE',
    'ABER', 'ALLE', 'ALLES', 'ALTE', 'ALTEN', 'ALTER', 'AUCH', 'BAND',
    'BERG', 'BURG', 'DENN', 'DIES', 'DOCH', 'DORT', 'DREI', 'DURCH',
    'EINE', 'EINEM', 'EINEN', 'EINER', 'EINES', 'ENDE', 'ERDE', 'ERST',
    'ERSTE', 'FACH', 'FAND', 'FERN', 'FEST', 'FORT', 'GAR', 'GANZ',
    'GEGEN', 'GEIST', 'GOTT', 'GOLD', 'GRAB', 'GROSS', 'GRUFT', 'GUT',
    'HAND', 'HEIM', 'HELD', 'HERR', 'HIER', 'HOCH', 'IMMER', 'KANN', 'KLAR',
    'KRAFT', 'LAND', 'LANG', 'LICHT', 'MACHT', 'MEHR', 'MUSS', 'NACH',
    'NACHT', 'NAHM', 'NAME', 'NEU', 'NEUE', 'NEUEN', 'NICHT', 'NIE', 'NOCH',
    'ODER', 'ORT', 'ORTEN', 'REDE', 'REDEN', 'REICH', 'RIEF', 'RUIN', 'RUNE',
    'RUNEN', 'SAND', 'SAGT', 'SCHAUN', 'SCHON', 'SEHR', 'SEID', 'SEIN',
    'SEINE', 'SEINEN', 'SEINER', 'SEINEM', 'SEINES', 'SICH', 'SIND', 'SOHN',
    'SOLL', 'STEH', 'STEIN', 'STEINE', 'STEINEN', 'STERN', 'TAG', 'TAGE',
    'TAT', 'TEIL', 'TIEF', 'TOD', 'TURM', 'UNTER', 'URALTE', 'VIEL', 'VIER',
    'WAHR', 'WALD', 'WAND', 'WARD', 'WEIL', 'WELT', 'WENN', 'WERT',
    'WESEN', 'WILL', 'WIND', 'WIRD', 'WORT', 'WORTE', 'ZEIT', 'ZEHN', 'ZORN',
    'FINDEN', 'GEBEN', 'GEHEN', 'HABEN', 'KOMMEN', 'LEBEN', 'LESEN',
    'NEHMEN', 'SAGEN', 'SEHEN', 'STEHEN', 'SUCHEN', 'WISSEN', 'WISSET',
    'RUFEN', 'WIEDER', 'GEIGET', 'BERUCHTIG', 'BERUCHTIGER', 'MEERE',
    'NEIGT', 'WISTEN', 'MANIER', 'HUND', 'GODE', 'EIGENTUM', 'REDER',
    'THENAEUT', 'LABT', 'MORT', 'DIGE', 'WEGE', 'KOENIGS', 'NAHE', 'NOT',
    'NOTH', 'ZUR', 'OWI', 'ENGE', 'SEIDEN', 'ALTES', 'DENN', 'BIS', 'NIE',
    'NUT', 'NUTZ', 'HEIL', 'NEID', 'TREU', 'TREUE', 'SUN', 'DIENST', 'SANG',
    'DINC', 'HULDE', 'STEINE', 'KOENIG', 'DASS', 'EDEL', 'ADEL',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE', 'GOTTDIENER', 'GOTTDIENERS',
    'TRAUT', 'LEICH', 'HEIME', 'SCHARDT', 'NACH', 'LANT', 'HERRE',
])

def dp_covered_positions(text):
    """Returns set of positions covered by known words."""
    n = len(text)
    dp = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], None)
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if cand in KNOWN:
                score = dp[start][0] + wlen
                if score > dp[i][0]:
                    dp[i] = (score, (start, cand))
    covered = set()
    i = n
    while i > 0:
        if dp[i][1] is not None:
            start, word = dp[i][1]
            for p in range(start, i):
                covered.add(p)
            i = start
        else:
            i -= 1
    return covered

# Build pair-to-position mapping
all_pairs = []
pair_positions = []  # (pair_code, position_in_decoded_text)

for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    all_pairs.extend(pairs)

full_text = ''.join(v7.get(p, '?') for p in all_pairs)
covered_positions = dp_covered_positions(full_text)

# Count per-code coverage
code_covered = Counter()
code_uncovered = Counter()
code_total = Counter()

for i, pair in enumerate(all_pairs):
    code_total[pair] += 1
    if i in covered_positions:
        code_covered[pair] += 1
    else:
        code_uncovered[pair] += 1

print("CODE GARBLED RATIO (sorted by garbled ratio, descending)")
print(f"{'Code':>5} {'Letter':>7} {'Total':>6} {'Garbled':>8} {'Covered':>8} {'Ratio':>7}")
print("-" * 50)

suspicious = []
for code in sorted(v7.keys(), key=lambda c: code_uncovered.get(c,0)/max(code_total.get(c,1),1), reverse=True):
    total = code_total.get(code, 0)
    if total < 3: continue
    garbled = code_uncovered.get(code, 0)
    covered = code_covered.get(code, 0)
    ratio = garbled / total if total > 0 else 0
    letter = v7[code]
    flag = " ***" if ratio > 0.65 and total >= 10 else " **" if ratio > 0.55 and total >= 10 else ""
    print(f"{code:>5} {letter:>7} {total:>6} {garbled:>8} {covered:>8} {ratio:>6.1%}{flag}")
    if ratio > 0.65 and total >= 10:
        suspicious.append((code, letter, total, garbled, ratio))

if suspicious:
    print(f"\nHIGHLY SUSPICIOUS CODES (>65% garbled, 10+ occurrences):")
    for code, letter, total, garbled, ratio in suspicious:
        print(f"  Code {code} -> {letter}: {garbled}/{total} garbled ({ratio:.0%})")
        # Show what letter would improve coverage most
        print(f"    Testing alternative mappings...")

# Test swapping suspicious codes
print("\n" + "=" * 70)
print("BRUTE-FORCE MAPPING CORRECTIONS")
print("Testing if changing any single code improves coverage")
print("=" * 70)

baseline_covered = len(covered_positions)
baseline_total = sum(1 for c in full_text if c != '?')
baseline_pct = baseline_covered / baseline_total * 100

print(f"Baseline: {baseline_covered}/{baseline_total} = {baseline_pct:.1f}%")

# For each code that appears 10+ times, try changing to each letter
improvements = []
letters = 'ABCDEFGHIKLMNORSTUWZ'

for code in sorted(v7.keys(), key=lambda c: int(c)):
    total = code_total.get(code, 0)
    if total < 5: continue
    current_letter = v7[code]

    for new_letter in letters:
        if new_letter == current_letter: continue

        # Build modified text
        mod_text = list(full_text)
        for i, pair in enumerate(all_pairs):
            if pair == code:
                mod_text[i] = new_letter
        mod_text = ''.join(mod_text)

        # Check coverage
        mod_covered = dp_covered_positions(mod_text)
        mod_count = len(mod_covered)

        if mod_count > baseline_covered + 5:  # At least 5 chars improvement
            improvement = mod_count - baseline_covered
            improvements.append((code, current_letter, new_letter, improvement, total))

# Sort by improvement
improvements.sort(key=lambda x: -x[3])
print(f"\nTop improvements from single code changes:")
for code, old, new, imp, total in improvements[:20]:
    new_pct = (baseline_covered + imp) / baseline_total * 100
    print(f"  Code {code}: {old}->{new} (+{imp} chars, {new_pct:.1f}%) [{total} occurrences]")
