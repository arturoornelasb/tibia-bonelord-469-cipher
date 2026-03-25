#!/usr/bin/env python3
"""Session 26 Round 2: Test UOD->TOD, HELLICHT cross-boundary, and scan for more gains."""
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

# Current KNOWN + ANAGRAM_MAP from session 26 pipeline
KNOWN = set(['AB','AM','AN','ALS','AUF','AUS','BEI','DA','DAS','DEM','DEN','DER','DES','DIE','DU','ER','ES','IM','IN','IST','JA','MAN','OB','SO','UM','UND','VON','VOR','WO','ZU','EIN','ICH','SIE','WER','WIE','WAS','WIR','GEH','GIB','HAT','HIN','HER','NUN','NUR','SEI','TUN','TUT','SAG','WAR','NU','SIN','STANDE','NACHTS','NIT','TOT','TER','ABER','ALLE','ALLES','ALTE','ALTEN','ALTER','AUCH','BAND','BERG','BURG','DENN','DIES','DIESE','DIESER','DIESEN','DIESEM','DOCH','DORT','DREI','DURCH','EINE','EINEM','EINEN','EINER','EINES','ENDE','ERDE','ERST','ERSTE','FACH','FAND','FERN','FEST','FORT','GAR','GANZ','GEGEN','GEIST','GOTT','GOLD','GRAB','GROSS','GRUFT','GUT','HAND','HEIM','HELD','HERR','HIER','HOCH','IMMER','KANN','KLAR','KRAFT','LAND','LANG','LICHT','MACHT','MEHR','MUSS','NACH','NACHT','NAHM','NAME','NEU','NEUE','NEUEN','NICHT','NIE','NOCH','ODER','ORT','ORTEN','REDE','REDEN','REICH','RIEF','RUIN','RUNE','RUNEN','SAND','SAGT','SCHAUN','SCHON','SEHR','SEID','SEIN','SEINE','SEINEN','SEINER','SEINEM','SEINES','SICH','SIND','SOHN','SOLL','STEH','STEIN','STEINE','STEINEN','STERN','TAG','TAGE','TAGEN','TAT','TEIL','TIEF','TOD','TURM','UNTER','URALTE','VIEL','VIER','WAHR','WALD','WAND','WARD','WEIL','WELT','WENN','WERT','WESEN','WILL','WIND','WIRD','WORT','WORTE','ZEIT','ZEHN','ZORN','FINDEN','GEBEN','GEHEN','HABEN','KOMMEN','LEBEN','LESEN','NEHMEN','SAGEN','SEHEN','STEHEN','SUCHEN','WISSEN','WISSET','RUFEN','WIEDER','OEL','SCE','MINNE','MIN','HEL','ODE','SER','GEN','INS','GEIGET','BERUCHTIG','BERUCHTIGER','MEERE','NEIGT','WISTEN','MANIER','HUND','GODE','GODES','EIGENTUM','REDER','THENAEUT','LABT','MORT','DIGE','WEGE','KOENIGS','NAHE','NOT','NOTH','ZUR','OWI','ENGE','SEIDEN','ALTES','BIS','NUT','NUTZ','HEIL','NEID','TREU','TREUE','SUN','DIENST','SANG','DINC','HULDE','STEINE','LANT','HERRE','DIENEST','GEBOT','SCHWUR','ORDEN','RICHTER','DUNKEL','EHRE','EDELE','SCHULD','SEGEN','FLUCH','RACHE','KOENIG','DASS','EDEL','ADEL','SCHRAT','SALZBERG','WEICHSTEIN','ORANGENSTRASSE','GOTTDIENER','GOTTDIENERS','TRAUT','LEICH','HEIME','SCHARDT','IHM','STIER','NEST','DES','EINEN','DEGEN','REISTEN','REIST','WINDUNRUH','WINDUNRUHS','UNRUH','HEHL','HECHELT','IRREN'])

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
    'DIESERTEIN':'DIEREISTEN','DERSTEI':'DEREIST',
    'DENGE':'DEGEN','ESC':'SCE','DSIE':'DIES',
    'UIRUNNHWND':'WINDUNRUH','SIUIRUNNHWND':'WINDUNRUHS',
    'HIHL':'HEHL','HECHLLT':'HECHELT','NLNDEF':'FINDEN','RRNI':'IRREN',
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
    result = []
    for kind, val, s, e in tokens:
        if kind == 'G' and result and result[-1][0] == 'G':
            prev = result[-1]
            result[-1] = ('G', prev[1] + val, prev[2], e)
        else:
            result.append((kind, val, s, e))
    return result

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
print(f"CURRENT BASELINE: {base_cov}/{total} = {base_cov/total*100:.1f}%")

# 1. Test UOD -> TOD
print("\n=== TEST: UOD -> TOD ===")
for word, label in [('TOD', 'death'), ('OUD', 'old-Dutch'), ('DUO', 'pair')]:
    cov, _ = apply_and_score({'UOD': word}, {word} if word not in KNOWN else set())
    print(f"  UOD -> {word} ({label}): {cov}/{total} delta={cov-base_cov:+d}")

# Show UOD contexts in current text
tr = all_text
for a in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    tr = tr.replace(a, ANAGRAM_MAP[a])
tokens = dp_segment_full(tr, KNOWN)
for i, (kind, val, s, e) in enumerate(tokens):
    if kind == 'G' and 'UOD' in val:
        prev = tokens[i-1][1] if i > 0 else ''
        nxt = tokens[i+1][1] if i < len(tokens)-1 else ''
        print(f"  Context: ...{prev} |{val}| {nxt}...")

# 2. Test HELLICHT cross-boundary
print("\n=== TEST: HECHLLT+ICH -> HELLICHT (cross-boundary) ===")
# Current: HECHLLT -> HECHELT already in map
# Alternative: HECHLLTICCH -> HELLICHT + extra C,H
# Actually, the text is HECHLLTICH (after anagram map, HECHLLT becomes HECHELT, then ICH follows)
# Let me check what the raw text looks like around HECHLLT
for i, (kind, val, s, e) in enumerate(tokens):
    if kind == 'W' and val == 'HECHELT':
        ctx_before = tokens[i-1][1] if i > 0 else ''
        ctx_after = tokens[i+1][1] if i < len(tokens)-1 else ''
        ctx_after2 = tokens[i+2][1] if i < len(tokens)-2 else ''
        print(f"  HECHELT context: ...{ctx_before} HECHELT {ctx_after} {ctx_after2}...")

# Test removing HECHLLT->HECHELT and trying HECHLLTICCH -> HELLICHT instead
# First check the raw text
raw_tr = all_text
for a in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    if a != 'HECHLLT':
        raw_tr = raw_tr.replace(a, ANAGRAM_MAP[a])
# Now find HECHLLT in raw_tr
idx = 0
while True:
    pos = raw_tr.find('HECHLLT', idx)
    if pos == -1: break
    ctx = raw_tr[max(0,pos-10):pos+20]
    print(f"  Raw HECHLLT at {pos}: ...{ctx}...")
    idx = pos + 1

# Try HECHLLTICHOELS -> HELLICHT + OEL + S? No, let's try direct
test_map = dict(ANAGRAM_MAP)
del test_map['HECHLLT']
test_map['HECHLLTICHOELSO'] = 'HELLICHTOELANSO'  # too complex, skip
# Actually: "HECHLLTICHOELSO DEN HIER" - the ICH OEL SO DEN HIER part follows HECHLLT
# HECHLLT ICH = 10 chars. HELLICHT = 8 chars. So +2 extra (C, remaining letters...)
# This is complex. Let me test simpler alternatives.

# 3. More single-letter absorptions on current resolved text
print("\n=== NEW SINGLE-LETTER ABSORPTIONS (Round 2) ===")
tokens = dp_segment_full(tr, KNOWN)
all_test_words = set(KNOWN)
extra_german = ['WEIT', 'WEITE', 'SEITE', 'REISE', 'GEISTE', 'MEISTE', 'WEISE',
    'LEISTE', 'HEISSE', 'REICHE', 'GLEICH', 'FLEISCH', 'GERECHT', 'SCHEIN',
    'LEGEN', 'REGEN', 'GEGEN', 'WEGEN', 'SEGEN', 'DEGEN', 'HEGEN',
    'OBEN', 'UNTEN', 'NEBEN', 'INNEN', 'AUSSEN',
    'KLEIN', 'REIN', 'FEIN', 'MEIN', 'DEIN', 'KEIN', 'ALLEIN',
    'GENUG', 'DARAUF', 'DARIN', 'DARUM', 'DARAN', 'DABEI', 'DAHIN',
    'DUNST', 'KUNST', 'GUNST', 'BRUNST', 'FEIND',
    'HERRN', 'HERREN', 'ERDEN', 'ORDEN', 'MORDEN', 'WORDEN',
    'DIENER', 'DIENEN', 'MEINEN', 'DEINEN', 'SEINEN', 'KEINEN',
    'STEHEN', 'DREHEN', 'SEHEN', 'GEHEN', 'NEHMEN',
    'SCHULDEN', 'HALTEN', 'WALTEN', 'GELTEN', 'SELTEN',
    'WUNDER', 'UNTER', 'HINTER', 'WINTER', 'DONNER',
    'FEIND', 'FREUND', 'BRUDER', 'SCHWESTER', 'MUTTER', 'VATER',
    'TUGEND', 'JUGEND', 'GEGEND', 'LEGEND',
    'STIER', 'TIER', 'HIER', 'ZIER', 'BIER',
    'OEL', 'ANOEL', 'SOEL',
    # MHG
    'VROUWE', 'DEGEN', 'RECKE', 'GENIST', 'STAETE', 'MILTE',
    'SAELDE', 'TUGENT', 'ZUHT', 'WIGANT',
    'HERRE', 'MINNE', 'TRIUWE', 'ELLEN', 'SEGEN',
    'HEHL', 'HEHLEN', 'OEDE', 'WUESTE',
    'TOD', 'TODE', 'TODES', 'TOTEN',
    'GNADE', 'EHREN', 'ADELN',
    'AUE', 'GAUE', 'BAUE',
    'EID', 'LEID', 'NEID', 'SEID', 'KLEID',
    'NOT', 'NOTH', 'BROT', 'ROT', 'GRAU',
    'SCHAR', 'SCHAREN', 'EDLEN',
    'HAUPT', 'HAUFE', 'HAUSE',
]
all_test_words.update(extra_german)

gains = []
for i in range(1, len(tokens) - 1):
    kind, val, start, end = tokens[i]
    if kind != 'G' or len(val) != 1:
        continue
    prev_kind, prev_val, _, _ = tokens[i-1]
    next_kind, next_val, _, _ = tokens[i+1]
    if prev_kind != 'W' or next_kind != 'W':
        continue

    letter = val
    # Left absorption
    left_raw = prev_val + letter
    left_sorted = sorted(left_raw)
    for word in all_test_words:
        if len(word) == len(left_raw) and sorted(word) == left_sorted and word != left_raw:
            # Check if it's in the resolved text
            count = tr.count(left_raw)
            if count > 0:
                cov, _ = apply_and_score({left_raw: word}, {word})
                delta = cov - base_cov
                if delta > 0:
                    gains.append((delta, left_raw, word, 'left', count, prev_val, letter, next_val))

    # Right absorption
    right_raw = letter + next_val
    right_sorted = sorted(right_raw)
    for word in all_test_words:
        if len(word) == len(right_raw) and sorted(word) == right_sorted and word != right_raw:
            count = tr.count(right_raw)
            if count > 0:
                cov, _ = apply_and_score({right_raw: word}, {word})
                delta = cov - base_cov
                if delta > 0:
                    gains.append((delta, right_raw, word, 'right', count, prev_val, letter, next_val))

gains.sort(key=lambda x: -x[0])
seen = set()
print(f"Found {len(gains)} candidates (showing unique, positive-delta):")
for delta, raw, word, direction, count, prev, letter, nxt in gains[:20]:
    key = (raw, word)
    if key in seen: continue
    seen.add(key)
    print(f"  +{delta:3d}: {raw} -> {word} ({direction}, {prev}|{letter}|{nxt}, {count}x)")

# 4. Multi-letter garbled block scan - find 2-3 letter blocks between known words
print("\n=== SHORT GARBLED BLOCKS (2-3 chars) ===")
short_blocks = Counter()
for i, (kind, val, s, e) in enumerate(tokens):
    if kind == 'G' and 2 <= len(val) <= 3:
        prev = tokens[i-1][1] if i > 0 and tokens[i-1][0] == 'W' else '?'
        nxt = tokens[i+1][1] if i < len(tokens)-1 and tokens[i+1][0] == 'W' else '?'
        short_blocks[(val, prev, nxt)] += 1

print("Most common 2-3 char garbled blocks between known words:")
for (block, prev, nxt), count in short_blocks.most_common(25):
    if prev != '?' and nxt != '?':
        # Try anagram
        anagram_options = []
        for word in all_test_words:
            if len(word) == len(block) and sorted(word) == sorted(block):
                anagram_options.append(word)
        label = f" -> could be: {', '.join(anagram_options)}" if anagram_options else ""
        print(f"  {count}x: {prev} |{block}| {nxt}{label}")
