#!/usr/bin/env python3
"""Session 26: Test cumulative addition of all validated anagrams on top of session 26 baseline."""
import json, os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json')) as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json')) as f:
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

# CURRENT SESSION 26 BASELINE (includes DIESERTEIN, DENGE, ESC, DSIE, DERSTEI)
KNOWN = set(['AB','AM','AN','ALS','AUF','AUS','BEI','DA','DAS','DEM','DEN','DER','DES','DIE','DU','ER','ES','IM','IN','IST','JA','MAN','OB','SO','UM','UND','VON','VOR','WO','ZU','EIN','ICH','SIE','WER','WIE','WAS','WIR','GEH','GIB','HAT','HIN','HER','NUN','NUR','SEI','TUN','TUT','SAG','WAR','NU','SIN','STANDE','NACHTS','NIT','TOT','TER','ABER','ALLE','ALLES','ALTE','ALTEN','ALTER','AUCH','BAND','BERG','BURG','DENN','DIES','DIESE','DIESER','DIESEN','DIESEM','DOCH','DORT','DREI','DURCH','EINE','EINEM','EINEN','EINER','EINES','ENDE','ERDE','ERST','ERSTE','FACH','FAND','FERN','FEST','FORT','GAR','GANZ','GEGEN','GEIST','GOTT','GOLD','GRAB','GROSS','GRUFT','GUT','HAND','HEIM','HELD','HERR','HIER','HOCH','IMMER','KANN','KLAR','KRAFT','LAND','LANG','LICHT','MACHT','MEHR','MUSS','NACH','NACHT','NAHM','NAME','NEU','NEUE','NEUEN','NICHT','NIE','NOCH','ODER','ORT','ORTEN','REDE','REDEN','REICH','RIEF','RUIN','RUNE','RUNEN','SAND','SAGT','SCHAUN','SCHON','SEHR','SEID','SEIN','SEINE','SEINEN','SEINER','SEINEM','SEINES','SICH','SIND','SOHN','SOLL','STEH','STEIN','STEINE','STEINEN','STERN','TAG','TAGE','TAGEN','TAT','TEIL','TIEF','TOD','TURM','UNTER','URALTE','VIEL','VIER','WAHR','WALD','WAND','WARD','WEIL','WELT','WENN','WERT','WESEN','WILL','WIND','WIRD','WORT','WORTE','ZEIT','ZEHN','ZORN','FINDEN','GEBEN','GEHEN','HABEN','KOMMEN','LEBEN','LESEN','NEHMEN','SAGEN','SEHEN','STEHEN','SUCHEN','WISSEN','WISSET','RUFEN','WIEDER','OEL','SCE','MINNE','MIN','HEL','ODE','SER','GEN','INS','GEIGET','BERUCHTIG','BERUCHTIGER','MEERE','NEIGT','WISTEN','MANIER','HUND','GODE','GODES','EIGENTUM','REDER','THENAEUT','LABT','MORT','DIGE','WEGE','KOENIGS','NAHE','NOT','NOTH','ZUR','OWI','ENGE','SEIDEN','ALTES','BIS','NUT','NUTZ','HEIL','NEID','TREU','TREUE','SUN','DIENST','SANG','DINC','HULDE','STEINE','LANT','HERRE','DIENEST','GEBOT','SCHWUR','ORDEN','RICHTER','DUNKEL','EHRE','EDELE','SCHULD','SEGEN','FLUCH','RACHE','KOENIG','DASS','EDEL','ADEL','SCHRAT','SALZBERG','WEICHSTEIN','ORANGENSTRASSE','GOTTDIENER','GOTTDIENERS','TRAUT','LEICH','HEIME','SCHARDT','IHM','STIER','NEST','DES','EINEN','DEGEN','REISTEN','REIST'])

ANAGRAM_MAP = {
    'LABGZERAS':'SALZBERG','SCHWITEIONE':'WEICHSTEIN','SCHWITEIO':'WEICHSTEIN',
    'AUNRSONGETRASES':'ORANGENSTRASSE','EDETOTNIURG':'GOTTDIENER',
    'EDETOTNIURGS':'GOTTDIENERS','ADTHARSC':'SCHARDT','TAUTR':'TRAUT',
    'EILCH':'LEICH','HEDDEMI':'HEIME','TIUMENGEMI':'EIGENTUM',
    'HEARUCHTIG':'BERUCHTIG','HEARUCHTIGER':'BERUCHTIGER',
    'EILCHANHEARUCHTIG':'LEICHANBERUCHTIG','EILCHANHEARUCHTIGER':'LEICHANBERUCHTIGER',
    'EEMRE':'MEERE','TEIGN':'NEIGT','WIISETN':'WISTEN','AUIENMR':'MANIER',
    'SODGE':'GODES','SNDTEII':'DIENST','IEB':'BEI',
    'TNEDAS':'STANDE','NSCHAT':'NACHTS','SANGE':'SAGEN','GHNEE':'GEHEN',
    'THARSCR':'SCHRAT','ANSD':'SAND','TTU':'TUT','TERLAU':'URALTE',
    'EUN':'NEU','NIUR':'RUIN','RUIIN':'RUIN','CHIS':'SICH',
    'SERTI':'STIER','ESR':'SER','NEDE':'ENDE','NTES':'NEST',
    'HIM':'IHM','EUTR':'TREU',
    # Session 26 (already applied)
    'DIESERTEIN':'DIEREISTEN','DERSTEI':'DEREIST',
    'DENGE':'DEGEN','ESC':'SCE','DSIE':'DIES',
}

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

def apply_and_score(extra_map, extra_known):
    test_map = dict(ANAGRAM_MAP)
    test_map.update(extra_map)
    test_known = set(KNOWN)
    test_known.update(extra_known)
    tr = all_text
    for a in sorted(test_map.keys(), key=len, reverse=True):
        tr = tr.replace(a, test_map[a])
    total = sum(1 for c in tr if c != '?')
    cov = dp_score(tr, test_known)
    return cov, total

base_cov, total = apply_and_score({}, set())
print(f"SESSION 26 BASELINE: {base_cov}/{total} = {base_cov/total*100:.1f}%")

# Test new hypotheses individually
candidates = [
    ("UIRUNNHWND -> WINDUNRUH", {'UIRUNNHWND': 'WINDUNRUH'}, {'WINDUNRUH', 'UNRUH'}),
    ("SIUIRUNNHWND -> WINDUNRUH (S-prefix variant)", {'SIUIRUNNHWND': 'WINDUNRUHS', 'UIRUNNHWND': 'WINDUNRUH'}, {'WINDUNRUH', 'WINDUNRUHS', 'UNRUH'}),
    ("HIHL -> HEHL", {'HIHL': 'HEHL'}, {'HEHL'}),
    ("HECHLLT -> HECHELT", {'HECHLLT': 'HECHELT'}, {'HECHELT'}),
    ("NLNDEF -> FINDEN (L->I required)", {'NLNDEF': 'FINDEN'}, set()),
    ("UNR -> NUR", {'UNR': 'NUR'}, set()),
    ("RRNI -> IRREN (fragment)", {'RRNI': 'IRREN'}, {'IRREN'}),
    ("UOD -> OUD", {'UOD': 'OUD'}, {'OUD'}),
]

print("\n=== INDIVIDUAL TESTS (on top of session 26 baseline) ===")
for label, extra_map, extra_known in candidates:
    cov, _ = apply_and_score(extra_map, extra_known)
    delta = cov - base_cov
    print(f"  {label}: {cov}/{total} = {cov/total*100:.1f}% (delta: {delta:+d})")

# Greedy cumulative (add largest positive delta first)
print("\n=== GREEDY CUMULATIVE APPLICATION ===")
remaining = list(candidates)
cum_map = {}
cum_known = set()
cum_cov = base_cov

while remaining:
    best_idx = -1
    best_delta = 0
    best_cov_val = 0
    for idx, (label, extra_map, extra_known) in enumerate(remaining):
        test_extra = dict(cum_map)
        test_extra.update(extra_map)
        test_k = set(cum_known)
        test_k.update(extra_known)
        cov, _ = apply_and_score(test_extra, test_k)
        delta = cov - cum_cov
        if delta > best_delta:
            best_delta = delta
            best_idx = idx
            best_cov_val = cov
    if best_idx < 0:
        break
    label, extra_map, extra_known = remaining.pop(best_idx)
    cum_map.update(extra_map)
    cum_known.update(extra_known)
    cum_cov = best_cov_val
    print(f"  APPLIED: {label} = +{best_delta} (cumulative: {cum_cov}/{total} = {cum_cov/total*100:.1f}%)")

print(f"\nFINAL: {cum_cov}/{total} = {cum_cov/total*100:.1f}% (+{cum_cov - base_cov} from session 26 baseline)")
print(f"TOTAL GAIN FROM SESSION 25: +{cum_cov - 3999} chars (from 72.3% baseline)")
