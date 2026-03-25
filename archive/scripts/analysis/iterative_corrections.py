#!/usr/bin/env python3
"""
Iterative mapping corrections: apply one correction, then search for the next.
Each round: test all possible single-code changes, pick the best that doesn't
break any anagram, apply it, repeat.
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

def full_pipeline(mapping, amap):
    text = ''.join(mapping.get(p, '?') for p in all_pairs)
    resolved = text
    for ana in sorted(amap.keys(), key=len, reverse=True):
        resolved = resolved.replace(ana, amap[ana])
    total_known = sum(1 for c in resolved if c != '?')
    covered = dp_coverage(resolved)
    return covered, total_known

def check_anagram_breaks(old_mapping, new_mapping, amap):
    old_raw = ''.join(old_mapping.get(p, '?') for p in all_pairs)
    new_raw = ''.join(new_mapping.get(p, '?') for p in all_pairs)
    broken = []
    for ana in amap:
        if ana in old_raw and ana not in new_raw:
            broken.append(ana)
    return broken

# Start with the confirmed correction: 13: A->S, AODGE->GODE becomes SODGE->GODES
current_mapping = dict(v7)
current_mapping['13'] = 'S'

current_amap = dict({
    'LABGZERAS': 'SALZBERG', 'SCHWITEIONE': 'WEICHSTEIN',
    'SCHWITEIO': 'WEICHSTEIN', 'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'EDETOTNIURG': 'GOTTDIENER', 'EDETOTNIURGS': 'GOTTDIENERS',
    'ADTHARSC': 'SCHARDT', 'TAUTR': 'TRAUT', 'EILCH': 'LEICH',
    'HEDEMI': 'HEIME', 'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG', 'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE', 'TEIGN': 'NEIGT', 'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER', 'SODGE': 'GODES', 'SNDTEII': 'DIENST',
})

cov, total = full_pipeline(current_mapping, current_amap)
print(f"After 13:A->S + SODGE->GODES: {cov}/{total} = {cov/total*100:.1f}%")

letters = 'ABCDEFGHIKLMNORSTUWZ'

# Iterative improvement
for round_num in range(5):
    print(f"\n--- Round {round_num + 1}: Searching for best safe single-code change ---")

    best = None
    best_change = 0

    for code in sorted(current_mapping.keys(), key=lambda c: int(c)):
        total_occurrences = sum(1 for p in all_pairs if p == code)
        if total_occurrences < 3:
            continue

        current_letter = current_mapping[code]

        for new_letter in letters:
            if new_letter == current_letter:
                continue

            mod = dict(current_mapping)
            mod[code] = new_letter

            # Check anagram breaks
            broken = check_anagram_breaks(current_mapping, mod, current_amap)
            if broken:
                continue  # Skip if any anagram breaks

            new_cov, new_total = full_pipeline(mod, current_amap)
            change = new_cov - cov

            if change > best_change:
                best = (code, current_letter, new_letter, new_cov, new_total, change)
                best_change = change

    if best is None or best_change <= 0:
        print("  No further safe improvements found.")
        break

    code, old, new, new_cov, new_total, change = best
    pct = new_cov / new_total * 100
    print(f"  Best: Code {code}: {old}->{new} (+{change} chars, {pct:.1f}%)")

    # Apply
    current_mapping[code] = new
    cov = new_cov

    # Show what new text appears
    text = ''.join(current_mapping.get(p, '?') for p in all_pairs)
    resolved = text
    for ana in sorted(current_amap.keys(), key=len, reverse=True):
        resolved = resolved.replace(ana, current_amap[ana])

    # Find newly recognized words around changed positions
    # (skip this for speed — just print total)

print(f"\nFinal mapping changes from v7:")
changes = []
for code in sorted(v7.keys(), key=lambda c: int(c)):
    if current_mapping.get(code) != v7[code]:
        changes.append(f"  {code}: {v7[code]} -> {current_mapping[code]}")
if changes:
    for c in changes:
        print(c)
else:
    print("  (none besides 13:A->S)")

final_cov, final_total = full_pipeline(current_mapping, current_amap)
print(f"\nFinal coverage: {final_cov}/{final_total} = {final_cov/final_total*100:.1f}%")
