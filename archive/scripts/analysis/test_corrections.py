#!/usr/bin/env python3
"""Test mapping corrections with full pipeline (anagram resolution + DP segmentation)."""
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

all_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    all_pairs.extend(pairs)

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
    'NEIGT', 'WISTEN', 'MANIER', 'HUND', 'GODE', 'GODES', 'EIGENTUM', 'REDER',
    'THENAEUT', 'LABT', 'MORT', 'DIGE', 'WEGE', 'KOENIGS', 'NAHE', 'NOT',
    'NOTH', 'ZUR', 'OWI', 'ENGE', 'SEIDEN', 'ALTES', 'DENN', 'BIS', 'NIE',
    'NUT', 'NUTZ', 'HEIL', 'NEID', 'TREU', 'TREUE', 'SUN', 'DIENST', 'SANG',
    'DINC', 'HULDE', 'STEINE', 'KOENIG', 'DASS', 'EDEL', 'ADEL',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE', 'GOTTDIENER', 'GOTTDIENERS',
    'TRAUT', 'LEICH', 'HEIME', 'SCHARDT', 'NACH', 'LANT', 'HERRE',
])

ANAGRAM_MAP = {
    'LABGZERAS': 'SALZBERG', 'SCHWITEIONE': 'WEICHSTEIN',
    'SCHWITEIO': 'WEICHSTEIN', 'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'EDETOTNIURG': 'GOTTDIENER', 'EDETOTNIURGS': 'GOTTDIENERS',
    'ADTHARSC': 'SCHARDT', 'TAUTR': 'TRAUT', 'EILCH': 'LEICH',
    'HEDEMI': 'HEIME', 'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG', 'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE', 'TEIGN': 'NEIGT', 'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER', 'AODGE': 'GODE', 'SNDTEII': 'DIENST',
}

def dp_coverage(text):
    n = len(text)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            if text[start:i] in KNOWN:
                score = dp[start] + wlen
                if score > dp[i]:
                    dp[i] = score
    return dp[n]

def full_pipeline(mapping, amap=None):
    if amap is None:
        amap = ANAGRAM_MAP
    text = ''.join(mapping.get(p, '?') for p in all_pairs)
    resolved = text
    for ana in sorted(amap.keys(), key=len, reverse=True):
        resolved = resolved.replace(ana, amap[ana])
    total_known = sum(1 for c in resolved if c != '?')
    covered = dp_coverage(resolved)
    return covered, total_known, resolved

# Baseline
baseline_cov, baseline_total, baseline_text = full_pipeline(v7)
baseline_pct = baseline_cov / baseline_total * 100
print(f"Baseline (v7): {baseline_cov}/{baseline_total} = {baseline_pct:.1f}%")

# Test single code changes
candidates = [
    ('13', 'S', 'Was 100% garbled. AODGE->SODGE=GODES'),
    ('61', 'I', 'Biggest pre-anagram gain (+75)'),
    ('88', 'S', 'Second biggest (+61)'),
    ('14', 'M', 'Third biggest (+55)'),
    ('97', 'N', 'Fourth (+53)'),
    ('80', 'I', 'Fifth (+41)'),
    ('99', 'A', '+38'),
    ('64', 'S', '+32'),
]

print(f"\nSingle code changes (with anagram resolution):")
print(f"{'Code':>5} {'Old->New':>9} {'Coverage':>12} {'Change':>8} {'Breaks':>10}  Note")
print("-" * 75)

results = []
for code, new_letter, note in candidates:
    old_letter = v7[code]
    mod = dict(v7)
    mod[code] = new_letter

    cov, total, resolved = full_pipeline(mod)
    pct = cov / total * 100
    change = cov - baseline_cov

    # Check which anagrams break
    baseline_raw = ''.join(v7.get(p, '?') for p in all_pairs)
    mod_raw = ''.join(mod.get(p, '?') for p in all_pairs)
    broken = []
    for ana in ANAGRAM_MAP:
        was_present = ana in baseline_raw
        now_present = ana in mod_raw
        if was_present and not now_present:
            broken.append(ANAGRAM_MAP[ana])

    breaks = ','.join(broken) if broken else 'none'
    marker = ' <<<' if change > 10 and not broken else ''
    print(f"{code:>5} {old_letter}->{new_letter:>5} {pct:>11.1f}% {change:>+7}  {breaks:>10}  {note}{marker}")
    results.append((code, old_letter, new_letter, change, broken))

# Test code 13: A->S with updated anagram map
print("\n--- Special: Code 13 A->S with SODGE->GODES ---")
mod13 = dict(v7)
mod13['13'] = 'S'
amap13 = dict(ANAGRAM_MAP)
del amap13['AODGE']
amap13['SODGE'] = 'GODES'
cov13, total13, res13 = full_pipeline(mod13, amap13)
print(f"  Coverage: {cov13}/{total13} = {cov13/total13*100:.1f}% ({cov13-baseline_cov:+d})")

# Find safe combinations (no broken anagrams, positive change)
safe = [(c, o, n, ch) for c, o, n, ch, br in results if not br and ch > 0]
print(f"\nSafe improvements (no broken anagrams, positive change): {len(safe)}")
for code, old, new, change in safe:
    print(f"  Code {code}: {old}->{new} ({change:+d})")

# Test all safe changes combined
if safe:
    print("\n--- Combined safe changes ---")
    mod_all = dict(v7)
    for code, old, new, change in safe:
        mod_all[code] = new
    cov_all, total_all, res_all = full_pipeline(mod_all)
    print(f"  Coverage: {cov_all}/{total_all} = {cov_all/total_all*100:.1f}% ({cov_all-baseline_cov:+d})")
