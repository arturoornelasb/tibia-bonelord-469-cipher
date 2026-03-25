#!/usr/bin/env python3
"""Session 26: Find the optimal non-conflicting combination of new anagrams."""
import json, os
from collections import Counter

with open('data/mapping_v7.json') as f:
    v7 = json.load(f)
with open('data/books.json') as f:
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

book_pairs_list = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        sp, d = DIGIT_SPLITS[bidx]
        book = book[:sp] + d + book[sp:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs_list.append(pairs)

decoded_books = [''.join(v7.get(p, '?') for p in bpairs) for bpairs in book_pairs_list]
all_text = ''.join(decoded_books)

KNOWN = set(['AB','AM','AN','ALS','AUF','AUS','BEI','DA','DAS','DEM','DEN','DER','DES','DIE','DU','ER','ES','IM','IN','IST','JA','MAN','OB','SO','UM','UND','VON','VOR','WO','ZU','EIN','ICH','SIE','WER','WIE','WAS','WIR','GEH','GIB','HAT','HIN','HER','NUN','NUR','SEI','TUN','TUT','SAG','WAR','NU','SIN','STANDE','NACHTS','NIT','TOT','TER','ABER','ALLE','ALLES','ALTE','ALTEN','ALTER','AUCH','BAND','BERG','BURG','DENN','DIES','DIESE','DIESER','DIESEN','DIESEM','DOCH','DORT','DREI','DURCH','EINE','EINEM','EINEN','EINER','EINES','ENDE','ERDE','ERST','ERSTE','FACH','FAND','FERN','FEST','FORT','GAR','GANZ','GEGEN','GEIST','GOTT','GOLD','GRAB','GROSS','GRUFT','GUT','HAND','HEIM','HELD','HERR','HIER','HOCH','IMMER','KANN','KLAR','KRAFT','LAND','LANG','LICHT','MACHT','MEHR','MUSS','NACH','NACHT','NAHM','NAME','NEU','NEUE','NEUEN','NICHT','NIE','NOCH','ODER','ORT','ORTEN','REDE','REDEN','REICH','RIEF','RUIN','RUNE','RUNEN','SAND','SAGT','SCHAUN','SCHON','SEHR','SEID','SEIN','SEINE','SEINEN','SEINER','SEINEM','SEINES','SICH','SIND','SOHN','SOLL','STEH','STEIN','STEINE','STEINEN','STERN','TAG','TAGE','TAGEN','TAT','TEIL','TIEF','TOD','TURM','UNTER','URALTE','VIEL','VIER','WAHR','WALD','WAND','WARD','WEIL','WELT','WENN','WERT','WESEN','WILL','WIND','WIRD','WORT','WORTE','ZEIT','ZEHN','ZORN','FINDEN','GEBEN','GEHEN','HABEN','KOMMEN','LEBEN','LESEN','NEHMEN','SAGEN','SEHEN','STEHEN','SUCHEN','WISSEN','WISSET','RUFEN','WIEDER','OEL','SCE','MINNE','MIN','HEL','ODE','SER','GEN','INS','GEIGET','BERUCHTIG','BERUCHTIGER','MEERE','NEIGT','WISTEN','MANIER','HUND','GODE','GODES','EIGENTUM','REDER','THENAEUT','LABT','MORT','DIGE','WEGE','KOENIGS','NAHE','NOT','NOTH','ZUR','OWI','ENGE','SEIDEN','ALTES','BIS','NUT','NUTZ','HEIL','NEID','TREU','TREUE','SUN','DIENST','SANG','DINC','HULDE','STEINE','LANT','HERRE','DIENEST','GEBOT','SCHWUR','ORDEN','RICHTER','DUNKEL','EHRE','EDELE','SCHULD','SEGEN','FLUCH','RACHE','KOENIG','DASS','EDEL','ADEL','SCHRAT','SALZBERG','WEICHSTEIN','ORANGENSTRASSE','GOTTDIENER','GOTTDIENERS','TRAUT','LEICH','HEIME','SCHARDT','IHM','STIER','NEST','DES','EINEN'])

ANAGRAM_MAP = {'LABGZERAS':'SALZBERG','SCHWITEIONE':'WEICHSTEIN','SCHWITEIO':'WEICHSTEIN','AUNRSONGETRASES':'ORANGENSTRASSE','EDETOTNIURG':'GOTTDIENER','EDETOTNIURGS':'GOTTDIENERS','ADTHARSC':'SCHARDT','TAUTR':'TRAUT','EILCH':'LEICH','HEDDEMI':'HEIME','TIUMENGEMI':'EIGENTUM','HEARUCHTIG':'BERUCHTIG','HEARUCHTIGER':'BERUCHTIGER','EILCHANHEARUCHTIG':'LEICHANBERUCHTIG','EILCHANHEARUCHTIGER':'LEICHANBERUCHTIGER','EEMRE':'MEERE','TEIGN':'NEIGT','WIISETN':'WISTEN','AUIENMR':'MANIER','SODGE':'GODES','SNDTEII':'DIENST','IEB':'BEI','TNEDAS':'STANDE','NSCHAT':'NACHTS','SANGE':'SAGEN','GHNEE':'GEHEN','THARSCR':'SCHRAT','ANSD':'SAND','TTU':'TUT','TERLAU':'URALTE','EUN':'NEU','NIUR':'RUIN','RUIIN':'RUIN','CHIS':'SICH','SERTI':'STIER','ESR':'SER','NEDE':'ENDE','NTES':'NEST','HIM':'IHM','EUTR':'TREU'}

def dp_score(text, known_set):
    n = len(text)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        for wlen in range(2, min(i, 20) + 1):
            s = i - wlen
            if text[s:i] in known_set:
                dp[i] = max(dp[i], dp[s] + wlen)
    return dp[n]

def apply_and_score(anagram_map, known_set):
    tr = all_text
    for a in sorted(anagram_map.keys(), key=len, reverse=True):
        tr = tr.replace(a, anagram_map[a])
    return dp_score(tr, known_set)

# Baseline
base_cov = apply_and_score(ANAGRAM_MAP, KNOWN)
total = sum(1 for c in all_text if c != '?')
print(f"BASELINE: {base_cov}/{total} = {base_cov/total*100:.1f}%")

# All candidates to test
all_candidates = [
    ('DIESERTEIN', 'DIEREISTEN', ['REISTEN']),
    ('DENGE', 'DEGEN', ['DEGEN']),
    ('ESC', 'SCE', []),
    ('DIER', 'DREI', []),
    ('DSIE', 'DIES', []),
    ('DERSTEI', 'DEREIST', ['REIST']),
]

# Greedy: add longest first, skip if negative delta
print("\n=== GREEDY (longest first) ===")
best_map = dict(ANAGRAM_MAP)
best_known = set(KNOWN)
best_cov = base_cov

for raw, resolved, extra in sorted(all_candidates, key=lambda x: -len(x[0])):
    test_map = dict(best_map)
    test_map[raw] = resolved
    test_known = set(best_known)
    for w in extra:
        test_known.add(w)
    cov = apply_and_score(test_map, test_known)
    delta = cov - best_cov
    if delta > 0:
        best_map[raw] = resolved
        for w in extra:
            best_known.add(w)
        best_cov = cov
        print(f"  ACCEPT {raw} -> {resolved}: +{delta} (cum: {best_cov}/{total} = {best_cov/total*100:.1f}%)")
    else:
        print(f"  REJECT {raw} -> {resolved}: {delta:+d}")

print(f"\nGREEDY RESULT: {best_cov}/{total} = {best_cov/total*100:.1f}% (+{best_cov - base_cov})")

# Also try: shortest first
print("\n=== GREEDY (shortest first) ===")
best_map2 = dict(ANAGRAM_MAP)
best_known2 = set(KNOWN)
best_cov2 = base_cov

for raw, resolved, extra in sorted(all_candidates, key=lambda x: len(x[0])):
    test_map = dict(best_map2)
    test_map[raw] = resolved
    test_known = set(best_known2)
    for w in extra:
        test_known.add(w)
    cov = apply_and_score(test_map, test_known)
    delta = cov - best_cov2
    if delta > 0:
        best_map2[raw] = resolved
        for w in extra:
            best_known2.add(w)
        best_cov2 = cov
        print(f"  ACCEPT {raw} -> {resolved}: +{delta} (cum: {best_cov2}/{total} = {best_cov2/total*100:.1f}%)")
    else:
        print(f"  REJECT {raw} -> {resolved}: {delta:+d}")

print(f"\nSHORTEST-FIRST RESULT: {best_cov2}/{total} = {best_cov2/total*100:.1f}% (+{best_cov2 - base_cov})")

# Brute force: try all 2^6 = 64 combinations
print("\n=== BRUTE FORCE ALL 64 COMBINATIONS ===")
best_total = base_cov
best_combo = []
from itertools import combinations

for r in range(len(all_candidates)+1):
    for combo in combinations(range(len(all_candidates)), r):
        test_map = dict(ANAGRAM_MAP)
        test_known = set(KNOWN)
        names = []
        for idx in combo:
            raw, resolved, extra = all_candidates[idx]
            test_map[raw] = resolved
            for w in extra:
                test_known.add(w)
            names.append(f"{raw}->{resolved}")
        cov = apply_and_score(test_map, test_known)
        if cov > best_total:
            best_total = cov
            best_combo = names

print(f"BEST COMBINATION: {best_total}/{total} = {best_total/total*100:.1f}% (+{best_total - base_cov})")
print(f"  Anagrams: {best_combo}")
