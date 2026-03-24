#!/usr/bin/env python3
"""
Session 26: Systematic attack on ALL single-letter garbled patterns.
For each {X} single letter, try incorporating it into adjacent words to form
larger anagrammed words, testing every possibility for coverage gain.
"""
import json, os
from collections import Counter, defaultdict
from itertools import permutations

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

def dp_segment_score(text, known_set):
    n = len(text)
    dp_arr = [0] * (n + 1)
    for i in range(1, n + 1):
        dp_arr[i] = dp_arr[i-1]
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if cand in known_set:
                score = dp_arr[start] + wlen
                if score > dp_arr[i]:
                    dp_arr[i] = score
    return dp_arr[n]

# Baseline
base_resolved = all_text
for anagram in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    base_resolved = base_resolved.replace(anagram, ANAGRAM_MAP[anagram])
base_covered = dp_segment_score(base_resolved, KNOWN)
total = sum(1 for c in base_resolved if c != '?')
print(f"BASELINE: {base_covered}/{total} = {base_covered/total*100:.1f}%")

# Comprehensive German word list for testing
GERMAN_WORDS = set([
    # Existing KNOWN words (don't repeat)
    # Additional German words for testing
    'REISTEN', 'REINSTE', 'STEINER', 'DIENSTIERE', 'REIST', 'ERIST',
    'DEINER', 'DEINE', 'REISE', 'STEIN', 'MEISTER', 'GEISTER',
    'STREITE', 'SEITE', 'TEILS', 'TEILE', 'TEILEN', 'REITEN',
    'RITTER', 'BITTER', 'ENDEN', 'SENDEN', 'WENDEN', 'KENNEN',
    'RENNEN', 'NENNEN', 'DENKEN', 'SENKEN', 'LENKEN',
    'SINNE', 'INNEN', 'SINNER', 'INNER', 'STEIN', 'STEINE',
    'SEINE', 'DEINE', 'MEINE', 'FEINE', 'KEINE', 'REINE',
    'WEITE', 'SEITE', 'LEITE', 'BREITE', 'HEUTE',
    'DIENER', 'DIENEN', 'DIENERIN', 'DIENSTE',
    'RICHTET', 'DICHTER', 'LICHTER', 'SICHERT',
    'WANDERT', 'HUNDERT', 'SONDERS',
    'MINDER', 'FINDER', 'KINDER', 'HINDER', 'LINDER',
    'WUNDER', 'RUNDER', 'GESUNDER',
    'RUNDEN', 'WUNDEN', 'STUNDEN', 'KUNDEN', 'BUNDEN',
    'LAUFEN', 'KAUFEN', 'TAUFEN', 'RAUFEN',
    'NORDEN', 'MORDEN', 'WORDEN', 'ORTEN',
    'DIENEN', 'SCHIENEN', 'VERDIENEN',
    'RUHE', 'UNRUHE', 'WINDUNRUH',
    'TURNEN', 'STUERZEN', 'STUERME',
    'ERSTENS', 'DERSTES',
    'DAREIN', 'HEREIN', 'HINEIN',
    # MHG
    'VROUWE', 'DEGEN', 'RECKE', 'HELT',
    'WIGANT', 'DIENEST', 'TUGENT', 'ZUHT',
    'SAELDE', 'TRIUWE', 'STAETE', 'MILTE',
    'MINNE', 'GENIST', 'WEINEN',
])

# Find all multi-char garbled blocks between known words
# and test if incorporating adjacent single letters creates new anagram opportunities
print("\n=== SYSTEMATIC SINGLE-LETTER ABSORPTION ANALYSIS ===")
print("Testing if single garbled letters can join adjacent words to form anagrams")
print()

# Work on the resolved text - find patterns where a single letter sits between known words
import re

# Segment the resolved text and identify garbled regions
def dp_segment_full(text, known_set):
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
    tokens = []
    i = n
    while i > 0:
        if dp_arr[i][1] is not None:
            start, word = dp_arr[i][1]
            tokens.append(('W', word, start, i))
            i = start
        else:
            tokens.append(('G', text[i-1], i-1, i))
            i -= 1
    tokens.reverse()
    # Merge consecutive garbled
    result = []
    for kind, val, s, e in tokens:
        if kind == 'G' and result and result[-1][0] == 'G':
            prev = result[-1]
            result[-1] = ('G', prev[1] + val, prev[2], e)
        else:
            result.append((kind, val, s, e))
    return result

tokens = dp_segment_full(base_resolved, KNOWN)

# Find single-letter garbled surrounded by known words
# Pattern: W G(1 char) W
all_words = KNOWN | GERMAN_WORDS
gains = []

for i in range(1, len(tokens) - 1):
    kind, val, start, end = tokens[i]
    if kind != 'G' or len(val) != 1:
        continue

    prev_kind, prev_val, prev_start, prev_end = tokens[i-1]
    next_kind, next_val, next_start, next_end = tokens[i+1]

    if prev_kind != 'W' or next_kind != 'W':
        continue

    letter = val
    # Try: prev_word + letter + next_word = big_raw
    big_raw = prev_val + letter + next_val

    # Try all anagrams that form word combinations
    # For efficiency, try: sorted letters match any known word combinations
    raw_sorted = tuple(sorted(big_raw))

    # Quick test: does incorporating the letter into either adjacent word help?
    # Left absorption: (prev_word + letter) -> find anagram that's a known word
    left_raw = prev_val + letter
    left_sorted = sorted(left_raw)

    # Right absorption: (letter + next_word) -> find anagram
    right_raw = letter + next_val
    right_sorted = sorted(right_raw)

    # Check left absorption
    for word in all_words:
        if len(word) == len(left_raw) and sorted(word) == left_sorted:
            # Found a match! Test coverage
            test_map = dict(ANAGRAM_MAP)
            test_map[left_raw] = word
            test_known = set(KNOWN)
            test_known.add(word)
            tr = all_text
            for a in sorted(test_map.keys(), key=len, reverse=True):
                tr = tr.replace(a, test_map[a])
            tc = dp_segment_score(tr, test_known)
            delta = tc - base_covered
            if delta > 0:
                count = base_resolved.count(left_raw)
                gains.append((delta, left_raw, word, 'left', count, prev_val, letter, next_val))

    # Check right absorption
    for word in all_words:
        if len(word) == len(right_raw) and sorted(word) == right_sorted:
            test_map = dict(ANAGRAM_MAP)
            test_map[right_raw] = word
            test_known = set(KNOWN)
            test_known.add(word)
            tr = all_text
            for a in sorted(test_map.keys(), key=len, reverse=True):
                tr = tr.replace(a, test_map[a])
            tc = dp_segment_score(tr, test_known)
            delta = tc - base_covered
            if delta > 0:
                count = base_resolved.count(right_raw)
                gains.append((delta, right_raw, word, 'right', count, prev_val, letter, next_val))

# Sort by delta descending
gains.sort(key=lambda x: -x[0])

# Remove duplicates (same raw -> word)
seen = set()
unique_gains = []
for g in gains:
    key = (g[1], g[2])
    if key not in seen:
        seen.add(key)
        unique_gains.append(g)

print(f"Found {len(unique_gains)} positive-delta candidates:")
for delta, raw, word, direction, count, prev, letter, nxt in unique_gains[:30]:
    print(f"  +{delta:3d}: {raw} -> {word} ({direction} absorption of '{letter}', "
          f"context: {prev}|{letter}|{nxt}, {count}x in text)")

# Now test cumulative application of top candidates
print("\n=== CUMULATIVE APPLICATION (best non-conflicting) ===")
cumulative_map = dict(ANAGRAM_MAP)
cumulative_known = set(KNOWN)
cum_covered = base_covered
applied = []

for delta, raw, word, direction, count, prev, letter, nxt in unique_gains:
    # Skip if this raw string is already mapped
    if raw in cumulative_map:
        continue

    test_map = dict(cumulative_map)
    test_map[raw] = word
    test_known = set(cumulative_known)
    test_known.add(word)

    tr = all_text
    for a in sorted(test_map.keys(), key=len, reverse=True):
        tr = tr.replace(a, test_map[a])
    tc = dp_segment_score(tr, test_known)
    actual_delta = tc - cum_covered

    if actual_delta > 0:
        cumulative_map[raw] = word
        cumulative_known.add(word)
        cum_covered = tc
        applied.append((raw, word, actual_delta, cum_covered))
        print(f"  APPLIED: {raw} -> {word} = +{actual_delta} (cumulative: {cum_covered}/{total} = {cum_covered/total*100:.1f}%)")

print(f"\nTOTAL GAIN: +{cum_covered - base_covered} chars")
print(f"FINAL: {cum_covered}/{total} = {cum_covered/total*100:.1f}%")

# Also test the confirmed DIESERTEIN
print("\n=== ADDING DIESERTEIN ===")
cumulative_map['DIESERTEIN'] = 'DIEREISTEN'  # or any other valid anagram
cumulative_known.add('REISTEN')
tr = all_text
for a in sorted(cumulative_map.keys(), key=len, reverse=True):
    tr = tr.replace(a, cumulative_map[a])
tc = dp_segment_score(tr, cumulative_known)
print(f"  +DIESERTEIN -> DIEREISTEN: {tc}/{total} = {tc/total*100:.1f}% (delta from cumulative: +{tc - cum_covered})")

# And DERSTEI
cumulative_map['DERSTEI'] = 'DEREIST'
cumulative_known.add('REIST')
tr = all_text
for a in sorted(cumulative_map.keys(), key=len, reverse=True):
    tr = tr.replace(a, cumulative_map[a])
tc2 = dp_segment_score(tr, cumulative_known)
print(f"  +DERSTEI -> DEREIST: {tc2}/{total} = {tc2/total*100:.1f}% (delta: +{tc2 - tc})")
print(f"\nGRAND TOTAL with all changes: {tc2}/{total} = {tc2/total*100:.1f}% (+{tc2 - base_covered} from baseline)")
