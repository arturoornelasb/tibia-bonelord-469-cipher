#!/usr/bin/env python3
"""Session 27: Comprehensive attack on remaining 23% garbled text.
Tests all round 2 candidates + new pattern scans."""
import json, os, re
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

def apply_text(extra_map=None, extra_known=None):
    test_map = dict(ANAGRAM_MAP)
    if extra_map: test_map.update(extra_map)
    test_known = set(KNOWN)
    if extra_known: test_known.update(extra_known)
    tr = all_text
    for a in sorted(test_map.keys(), key=len, reverse=True):
        tr = tr.replace(a, test_map[a])
    total = sum(1 for c in tr if c != '?')
    cov = dp_score(tr, test_known)
    return cov, total, tr, test_known

base_cov, total, base_tr, base_known = apply_text()
print(f"SESSION 26 BASELINE: {base_cov}/{total} = {base_cov/total*100:.1f}%")

# =====================================================================
# PART 1: Test confirmed candidates from round 2
# =====================================================================
print("\n" + "="*70)
print("PART 1: INDIVIDUAL CANDIDATE TESTS")
print("="*70)

candidates = [
    ("UOD -> TOD", {'UOD': 'TOD'}, set()),
    ("EODE -> OEDE", {'EODE': 'OEDE'}, {'OEDE'}),
    ("ODEE -> OEDE", {'ODEE': 'OEDE'}, {'OEDE'}),
    ("UNE -> NEU", {'UNE': 'NEU'}, set()),  # NEU already in KNOWN
    ("EOD -> ODE", {'EOD': 'ODE'}, set()),   # ODE already in KNOWN
]

for label, extra_map, extra_known in candidates:
    cov, _, _, _ = apply_text(extra_map, extra_known)
    delta = cov - base_cov
    print(f"  {label}: {cov}/{total} = {cov/total*100:.1f}% (delta: {delta:+d})")

# =====================================================================
# PART 2: Systematic 2-3 letter garbled block resolution
# =====================================================================
print("\n" + "="*70)
print("PART 2: SYSTEMATIC GARBLED BLOCK ATTACK")
print("="*70)

# Big German/MHG word list for matching
GERMAN_WORDS = set(KNOWN)
GERMAN_WORDS.update([
    # Common 2-letter
    'OB', 'OH', 'EI', 'AU', 'JE',
    # Common 3-letter
    'TAG', 'RAT', 'TAT', 'MAL', 'TAL', 'ART', 'ARM', 'ALT', 'ORT',
    'RUH', 'TOR', 'ROT', 'NOT', 'LOT', 'GOT', 'HOF', 'RAD', 'BAD',
    'MAG', 'LAG', 'SAH', 'GAB', 'BAT', 'LOG', 'BOG', 'ZOG', 'LOG',
    'FEL', 'GEL', 'REH', 'SEE', 'FEE', 'TEE', 'WEH', 'RUF', 'TUG',
    'OHR', 'DOM', 'ION', 'IRR', 'IRE', 'ERZ', 'ESS', 'UHR',
    # Common 4-letter
    'WEHR', 'HEER', 'MEER', 'LEER', 'HERZ', 'GIER', 'TIER', 'ZIER',
    'ARME', 'ERDE', 'EHRE', 'RUHE', 'NOTE', 'TORE', 'DAME', 'SAGE',
    'EIDE', 'LEIB', 'REIF', 'HEIL', 'WEIL', 'FEIL', 'TEIL',
    'RAUM', 'BAUM', 'DAUM', 'HELM', 'KELM', 'REIS', 'WEIS', 'HEIM',
    'WEIN', 'REIN', 'FEIN', 'MEIN', 'DEIN', 'KEIN', 'SEIN', 'BEIN',
    'LEID', 'NEID', 'SEID', 'HERD', 'WERD', 'HORT', 'WORT', 'SORT',
    'HULD', 'MUND', 'BUND', 'FUND', 'RUND', 'KUND', 'WUND',
    'SUCH', 'FLUG', 'ZAHL', 'WAHL', 'STAB', 'GRAB', 'GRAU',
    # MHG forms
    'WIP', 'LIP', 'TUO', 'WUO', 'ZUO', 'HAN', 'TAN', 'GAN',
    'LIT', 'RIT', 'BIT', 'SIT',
    'ERE', 'IRE', 'URE',
])

tokens = dp_segment_full(base_tr, base_known)

# Collect all garbled blocks
garbled_analysis = []
for i, (kind, val, s, e) in enumerate(tokens):
    if kind != 'G': continue
    prev = tokens[i-1][1] if i > 0 and tokens[i-1][0] == 'W' else None
    nxt = tokens[i+1][1] if i < len(tokens)-1 and tokens[i+1][0] == 'W' else None
    garbled_analysis.append((val, prev, nxt, s, e))

# Count garbled blocks
garbled_counter = Counter()
for val, prev, nxt, s, e in garbled_analysis:
    garbled_counter[val] += 1

print(f"\nTotal garbled positions: {len(garbled_analysis)}")
print(f"Unique garbled blocks: {len(garbled_counter)}")
print(f"Total garbled chars: {sum(len(v)*c for v,c in garbled_counter.items())}")

# For each garbled block, try all anagram permutations against word list
print("\n--- Anagram matches for garbled blocks (2-5 chars) ---")
resolution_candidates = []
for block, count in garbled_counter.most_common():
    if len(block) < 2 or len(block) > 5: continue
    sorted_block = sorted(block)
    matches = []
    for word in GERMAN_WORDS:
        if len(word) == len(block) and sorted(word) == sorted_block and word != block:
            matches.append(word)
    if matches:
        # Test each match
        for word in matches:
            cov, _, _, _ = apply_text({block: word}, {word})
            delta = cov - base_cov
            if delta > 0:
                resolution_candidates.append((delta, block, word, count))

resolution_candidates.sort(key=lambda x: -x[0])
print(f"\nPositive-delta anagram resolutions:")
seen = set()
for delta, block, word, count in resolution_candidates:
    key = (block, word)
    if key in seen: continue
    seen.add(key)
    print(f"  +{delta:3d}: {block} -> {word} ({count}x)")

# =====================================================================
# PART 3: Cross-boundary absorption (garbled + known word or known word + garbled)
# =====================================================================
print("\n" + "="*70)
print("PART 3: CROSS-BOUNDARY WORD FORMATION")
print("="*70)

# Look at garbled chars adjacent to known words
cross_candidates = []
for i, (kind, val, s, e) in enumerate(tokens):
    if kind != 'G': continue
    if len(val) > 4: continue  # Only short garbled blocks

    # Try merging with previous word
    if i > 0 and tokens[i-1][0] == 'W':
        merged = tokens[i-1][1] + val
        sorted_merged = sorted(merged)
        for word in GERMAN_WORDS:
            if len(word) == len(merged) and sorted(word) == sorted_merged and word != merged:
                cov, _, _, _ = apply_text({merged: word}, {word})
                delta = cov - base_cov
                if delta > 0:
                    cross_candidates.append((delta, merged, word, f"left: {tokens[i-1][1]}+{val}"))

    # Try merging with next word
    if i < len(tokens)-1 and tokens[i+1][0] == 'W':
        merged = val + tokens[i+1][1]
        sorted_merged = sorted(merged)
        for word in GERMAN_WORDS:
            if len(word) == len(merged) and sorted(word) == sorted_merged and word != merged:
                cov, _, _, _ = apply_text({merged: word}, {word})
                delta = cov - base_cov
                if delta > 0:
                    cross_candidates.append((delta, merged, word, f"right: {val}+{tokens[i+1][1]}"))

cross_candidates.sort(key=lambda x: -x[0])
seen = set()
print(f"\nPositive-delta cross-boundary resolutions:")
for delta, raw, word, desc in cross_candidates[:20]:
    key = (raw, word)
    if key in seen: continue
    seen.add(key)
    print(f"  +{delta:3d}: {raw} -> {word} ({desc})")

# =====================================================================
# PART 4: Greedy cumulative application of all positive candidates
# =====================================================================
print("\n" + "="*70)
print("PART 4: GREEDY CUMULATIVE APPLICATION")
print("="*70)

# Gather all positive candidates
all_cands = []

# Round 2 confirmed
all_cands.append(("UOD->TOD", {'UOD': 'TOD'}, set()))
all_cands.append(("EODE->OEDE", {'EODE': 'OEDE'}, {'OEDE'}))

# Add positive resolution candidates
seen_blocks = set()
for delta, block, word, count in resolution_candidates:
    if block in seen_blocks: continue
    if delta > 0:
        seen_blocks.add(block)
        all_cands.append((f"{block}->{word}", {block: word}, {word}))

# Add positive cross-boundary candidates
seen_cross = set()
for delta, raw, word, desc in cross_candidates:
    if raw in seen_cross: continue
    if delta > 0:
        seen_cross.add(raw)
        all_cands.append((f"{raw}->{word} ({desc})", {raw: word}, {word}))

# Greedy application
cum_map = {}
cum_known = set()
cum_cov = base_cov
applied = []

remaining = list(all_cands)
while remaining:
    best_idx = -1
    best_delta = 0
    best_cov_val = 0
    for idx, (label, extra_map, extra_known) in enumerate(remaining):
        test_map = dict(cum_map)
        test_map.update(extra_map)
        test_k = set(cum_known)
        test_k.update(extra_known)
        cov, _, _, _ = apply_text(test_map, test_k)
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
    applied.append((label, best_delta))
    print(f"  APPLIED: {label} = +{best_delta} (cumulative: {cum_cov}/{total} = {cum_cov/total*100:.1f}%)")

print(f"\nSESSION 27 RESULT: {cum_cov}/{total} = {cum_cov/total*100:.1f}%")
print(f"GAIN FROM SESSION 26: +{cum_cov - base_cov} chars (+{(cum_cov - base_cov)/total*100:.1f}%)")

# =====================================================================
# PART 5: Show full decoded text for top books
# =====================================================================
print("\n" + "="*70)
print("PART 5: TOP DECODED BOOKS (after all session 27 gains)")
print("="*70)

final_map = dict(ANAGRAM_MAP)
final_map.update(cum_map)
final_known = set(KNOWN)
final_known.update(cum_known)

# Decode per-book
for bidx, bpairs in enumerate(book_pairs_list):
    book_text = ''.join(v7.get(p, '?') for p in bpairs)
    for a in sorted(final_map.keys(), key=len, reverse=True):
        book_text = book_text.replace(a, final_map[a])
    book_total = sum(1 for c in book_text if c != '?')
    if book_total == 0: continue
    book_cov = dp_score(book_text, final_known)
    pct = book_cov / book_total * 100
    if pct >= 90:
        tokens = dp_segment_full(book_text, final_known)
        display = ' '.join(f"{{{v}}}" if k == 'G' else v for k, v, s, e in tokens)
        print(f"\n  Book {bidx} ({pct:.0f}%, {book_cov}/{book_total}):")
        print(f"    {display}")

# =====================================================================
# PART 6: Remaining garbled inventory
# =====================================================================
print("\n" + "="*70)
print("PART 6: REMAINING GARBLED INVENTORY")
print("="*70)

final_tr = all_text
for a in sorted(final_map.keys(), key=len, reverse=True):
    final_tr = final_tr.replace(a, final_map[a])
final_tokens = dp_segment_full(final_tr, final_known)

remaining_garbled = Counter()
remaining_contexts = defaultdict(list)
for i, (kind, val, s, e) in enumerate(final_tokens):
    if kind != 'G':
        continue
    remaining_garbled[val] += 1
    prev = final_tokens[i-1][1] if i > 0 else '^'
    nxt = final_tokens[i+1][1] if i < len(final_tokens)-1 else '$'
    if len(remaining_contexts[val]) < 3:
        remaining_contexts[val].append(f"{prev} |{val}| {nxt}")

total_garbled = sum(len(v)*c for v,c in remaining_garbled.items())
print(f"\nRemaining garbled: {total_garbled} chars ({total_garbled/total*100:.1f}%)")
print(f"\nTop garbled blocks by frequency * length:")
scored = [(len(v)*c, v, c) for v,c in remaining_garbled.items()]
scored.sort(key=lambda x: -x[0])
for impact, block, count in scored[:25]:
    ctxs = remaining_contexts[block]
    print(f"  {impact:4d} chars: {block!r:20s} ({count}x)")
    for ctx in ctxs:
        print(f"         {ctx}")
