#!/usr/bin/env python3
"""Session 26: Analyze the fixed DIESERTEIN pattern and find coverage-improving anagrams."""
import json, os, sys
from collections import Counter, defaultdict

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

# Build decoded books
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

# Define KNOWN set
KNOWN = set([
    'AB','AM','AN','ALS','AUF','AUS','BEI','DA','DAS','DEM','DEN','DER','DES','DIE','DU','ER','ES',
    'IM','IN','IST','JA','MAN','OB','SO','UM','UND','VON','VOR','WO','ZU','EIN','ICH','SIE','WER',
    'WIE','WAS','WIR','GEH','GIB','HAT','HIN','HER','NUN','NUR','SEI','TUN','TUT','SAG','WAR',
    'NU','SIN','STANDE','NACHTS','NIT','TOT','TER',
    'ABER','ALLE','ALLES','ALTE','ALTEN','ALTER','AUCH','BAND','BERG','BURG','DENN','DIES',
    'DIESE','DIESER','DIESEN','DIESEM','DOCH','DORT','DREI','DURCH','EINE','EINEM','EINEN',
    'EINER','EINES','ENDE','ERDE','ERST','ERSTE','FACH','FAND','FERN','FEST','FORT','GAR',
    'GANZ','GEGEN','GEIST','GOTT','GOLD','GRAB','GROSS','GRUFT','GUT','HAND','HEIM','HELD',
    'HERR','HIER','HOCH','IMMER','KANN','KLAR','KRAFT','LAND','LANG','LICHT','MACHT','MEHR',
    'MUSS','NACH','NACHT','NAHM','NAME','NEU','NEUE','NEUEN','NICHT','NIE','NOCH','ODER',
    'ORT','ORTEN','REDE','REDEN','REICH','RIEF','RUIN','RUNE','RUNEN','SAND','SAGT','SCHAUN',
    'SCHON','SEHR','SEID','SEIN','SEINE','SEINEN','SEINER','SEINEM','SEINES','SICH','SIND',
    'SOHN','SOLL','STEH','STEIN','STEINE','STEINEN','STERN','TAG','TAGE','TAGEN','TAT','TEIL',
    'TIEF','TOD','TURM','UNTER','URALTE','VIEL','VIER','WAHR','WALD','WAND','WARD','WEIL',
    'WELT','WENN','WERT','WESEN','WILL','WIND','WIRD','WORT','WORTE','ZEIT','ZEHN','ZORN',
    'FINDEN','GEBEN','GEHEN','HABEN','KOMMEN','LEBEN','LESEN','NEHMEN','SAGEN','SEHEN',
    'STEHEN','SUCHEN','WISSEN','WISSET','RUFEN','WIEDER',
    'OEL','SCE','MINNE','MIN','HEL','ODE','SER','GEN','INS','GEIGET','BERUCHTIG','BERUCHTIGER',
    'MEERE','NEIGT','WISTEN','MANIER','HUND','GODE','GODES','EIGENTUM','REDER','THENAEUT',
    'LABT','MORT','DIGE','WEGE','KOENIGS','NAHE','NOT','NOTH','ZUR','OWI','ENGE','SEIDEN',
    'ALTES','BIS','NUT','NUTZ','HEIL','NEID','TREU','TREUE','SUN','DIENST','SANG','DINC',
    'HULDE','STEINE','LANT','HERRE','DIENEST','GEBOT','SCHWUR','ORDEN','RICHTER','DUNKEL',
    'EHRE','EDELE','SCHULD','SEGEN','FLUCH','RACHE','KOENIG','DASS','EDEL','ADEL','SCHRAT',
    'SALZBERG','WEICHSTEIN','ORANGENSTRASSE','GOTTDIENER','GOTTDIENERS','TRAUT','LEICH','HEIME',
    'SCHARDT','IHM','STIER','NEST','DES','EINEN',
])

ANAGRAM_MAP = {
    'LABGZERAS': 'SALZBERG', 'SCHWITEIONE': 'WEICHSTEIN', 'SCHWITEIO': 'WEICHSTEIN',
    'AUNRSONGETRASES': 'ORANGENSTRASSE', 'EDETOTNIURG': 'GOTTDIENER',
    'EDETOTNIURGS': 'GOTTDIENERS', 'ADTHARSC': 'SCHARDT', 'TAUTR': 'TRAUT',
    'EILCH': 'LEICH', 'HEDDEMI': 'HEIME', 'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG', 'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG', 'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE', 'TEIGN': 'NEIGT', 'WIISETN': 'WISTEN', 'AUIENMR': 'MANIER',
    'SODGE': 'GODES', 'SNDTEII': 'DIENST', 'IEB': 'BEI',
    'TNEDAS': 'STANDE', 'NSCHAT': 'NACHTS', 'SANGE': 'SAGEN', 'GHNEE': 'GEHEN',
    'THARSCR': 'SCHRAT', 'ANSD': 'SAND', 'TTU': 'TUT', 'TERLAU': 'URALTE',
    'EUN': 'NEU', 'NIUR': 'RUIN', 'RUIIN': 'RUIN', 'CHIS': 'SICH',
    'SERTI': 'STIER', 'ESR': 'SER', 'NEDE': 'ENDE', 'NTES': 'NEST',
    'HIM': 'IHM', 'EUTR': 'TREU',
}

def dp_segment(text, known_set):
    n = len(text)
    dp_arr = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp_arr[i] = (dp_arr[i-1][0], None)
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if cand in known_set:
                score = dp_arr[start][0] + wlen
                if score > dp_arr[i][0]:
                    dp_arr[i] = (score, (start, cand))
    return dp_arr[n][0]

# Baseline
base_resolved = all_text
for anagram in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    base_resolved = base_resolved.replace(anagram, ANAGRAM_MAP[anagram])
base_covered = dp_segment(base_resolved, KNOWN)
total = sum(1 for c in base_resolved if c != '?')
print(f"BASELINE: {base_covered}/{total} = {base_covered/total*100:.1f}%")
print(f"DIESERTEIN count in resolved: {base_resolved.count('DIESERTEIN')}")
print(f"TEINERSEIN count in resolved: {base_resolved.count('TEINERSEIN')}")

# Test candidates for DIESERTEIN
candidates = [
    ('DIESERTEIN', 'DIEREISTEN', ['REISTEN']),
    ('DIESERTEIN', 'REINSTEDIE', ['REINSTE']),
    ('DIESERTEIN', 'DIENSTIERE', ['DIENSTIERE']),
    ('DIESERTEIN', 'STEINERDIE', ['STEINER']),
]

# Also test TEINERSEIN
candidates += [
    ('TEINERSEIN', 'SEINERITEN', ['RITEN']),
    ('TEINERSEIN', 'REISTENSEIN', []),  # wrong length
]

print("\n=== TESTING ANAGRAM CANDIDATES ===")
for raw, resolved, extra_words in candidates:
    if sorted(raw) != sorted(resolved):
        print(f"  {raw} -> {resolved}: LETTER MISMATCH, skipping")
        continue
    if base_resolved.count(raw) == 0:
        print(f"  {raw} -> {resolved}: NOT FOUND in resolved text, skipping")
        continue

    test_map = dict(ANAGRAM_MAP)
    test_map[raw] = resolved
    test_known = set(KNOWN)
    for w in extra_words:
        test_known.add(w)

    tr = all_text
    for anagram in sorted(test_map.keys(), key=len, reverse=True):
        tr = tr.replace(anagram, test_map[anagram])
    tc = dp_segment(tr, test_known)
    delta = tc - base_covered
    new_words_str = ', '.join(extra_words) if extra_words else 'no new words'
    print(f"  {raw} -> {resolved}: {tc}/{total} delta={delta:+d} ({new_words_str})")

# Find ALL fixed code sequences (10+ pairs, 3+ occurrences)
print("\n=== MOST REPEATED 10-PAIR CODE SEQUENCES ===")
all_pairs = []
for bpairs in book_pairs_list:
    all_pairs.extend(bpairs)

seq_count = defaultdict(int)
for i in range(len(all_pairs) - 9):
    seq = tuple(all_pairs[i:i+10])
    seq_count[seq] += 1

print("Top repeated 10-pair sequences (3+ times):")
for seq, count in sorted(seq_count.items(), key=lambda x: -x[1])[:20]:
    if count >= 3:
        decoded = ''.join(v7.get(p, '?') for p in seq)
        print(f"  {count}x: {decoded}  [{' '.join(seq)}]")

# Find repeated 5-pair sequences too
print("\nTop repeated 5-pair sequences (8+ times):")
seq5 = defaultdict(int)
for i in range(len(all_pairs) - 4):
    seq = tuple(all_pairs[i:i+5])
    seq5[seq] += 1

for seq, count in sorted(seq5.items(), key=lambda x: -x[1])[:25]:
    if count >= 8:
        decoded = ''.join(v7.get(p, '?') for p in seq)
        print(f"  {count}x: {decoded}  [{' '.join(seq)}]")

# Additional: check what ERSODASSTUN maps to - is it also fixed?
print("\n=== FULL REPEATING PHRASE ANALYSIS ===")
search = 'ERSODASSTUNDIESERTEINERSEINGOTTDIENER'
count = base_resolved.count(search)
print(f"Full phrase 'ERSODASSTUNDIESERTEINERSEINGOTTDIENER': {count}x")
# Try shorter
for slen in [30, 25, 20, 15]:
    substr = search[:slen]
    c = base_resolved.count(substr)
    if c > count:
        print(f"  First {slen} chars '{substr}': {c}x")

# Check the {D} ERSTE pattern too
print("\n=== {D} ERSTE PATTERN ===")
print(f"DERSTEI count: {base_resolved.count('DERSTEI')}")
print(f"DERSTE count: {base_resolved.count('DERSTE')}")
# What could DERSTEI be?
# D,E,R,S,T,E,I = 7 letters
# STERIDE? REITEST? STEIGER?
test_d = [
    ('DERSTEI', 'STEIDER', []),  # nonsense
    ('DERSTEI', 'DEREIST', ['REIST']),  # he/she travels
    ('DERSTEI', 'STEIERD', []),
]
print("Testing {D}ERSTE{I} = DERSTEI anagrams:")
for raw, resolved, extra in test_d:
    if sorted(raw) != sorted(resolved):
        print(f"  {raw} -> {resolved}: LETTER MISMATCH")
        continue
    c = base_resolved.count(raw)
    if c == 0: continue
    test_map = dict(ANAGRAM_MAP)
    test_map[raw] = resolved
    test_known = set(KNOWN)
    for w in extra:
        test_known.add(w)
    tr = all_text
    for a in sorted(test_map.keys(), key=len, reverse=True):
        tr = tr.replace(a, test_map[a])
    tc = dp_segment(tr, test_known)
    print(f"  {raw} -> {resolved} ({c}x): delta={tc-base_covered:+d}")

print("\nDone.")
