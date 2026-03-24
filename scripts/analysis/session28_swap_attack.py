#!/usr/bin/env python3
"""Session 28: Letter-swap tolerant attack on remaining garbled blocks.
The cipher has documented I/L, E/I, E/L swaps. Test all garbled blocks
with 0-1 letter substitutions to find hidden words."""
import json, os
from collections import Counter, defaultdict
from itertools import combinations

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

KNOWN = set(['AB','AM','AN','ALS','AUF','AUS','BEI','DA','DAS','DEM','DEN','DER','DES','DIE','DU','ER','ES','IM','IN','IST','JA','MAN','OB','SO','UM','UND','VON','VOR','WO','ZU','EIN','ICH','SIE','WER','WIE','WAS','WIR','GEH','GIB','HAT','HIN','HER','NUN','NUR','SEI','TUN','TUT','SAG','WAR','NU','SIN','STANDE','NACHTS','NIT','TOT','TER','ABER','ALLE','ALLES','ALTE','ALTEN','ALTER','AUCH','BAND','BERG','BURG','DENN','DIES','DIESE','DIESER','DIESEN','DIESEM','DOCH','DORT','DREI','DURCH','EINE','EINEM','EINEN','EINER','EINES','ENDE','ERDE','ERST','ERSTE','FACH','FAND','FERN','FEST','FORT','GAR','GANZ','GEGEN','GEIST','GOTT','GOLD','GRAB','GROSS','GRUFT','GUT','HAND','HEIM','HELD','HERR','HIER','HOCH','IMMER','KANN','KLAR','KRAFT','LAND','LANG','LICHT','MACHT','MEHR','MUSS','NACH','NACHT','NAHM','NAME','NEU','NEUE','NEUEN','NICHT','NIE','NOCH','ODER','ORT','ORTEN','REDE','REDEN','REICH','RIEF','RUIN','RUNE','RUNEN','SAND','SAGT','SCHAUN','SCHON','SEHR','SEID','SEIN','SEINE','SEINEN','SEINER','SEINEM','SEINES','SICH','SIND','SOHN','SOLL','STEH','STEIN','STEINE','STEINEN','STERN','TAG','TAGE','TAGEN','TAT','TEIL','TIEF','TOD','TURM','UNTER','URALTE','VIEL','VIER','WAHR','WALD','WAND','WARD','WEIL','WELT','WENN','WERT','WESEN','WILL','WIND','WIRD','WORT','WORTE','ZEIT','ZEHN','ZORN','FINDEN','GEBEN','GEHEN','HABEN','KOMMEN','LEBEN','LESEN','NEHMEN','SAGEN','SEHEN','STEHEN','SUCHEN','WISSEN','WISSET','RUFEN','WIEDER','OEL','SCE','MINNE','MIN','HEL','ODE','SER','GEN','INS','GEIGET','BERUCHTIG','BERUCHTIGER','MEERE','NEIGT','WISTEN','MANIER','HUND','GODE','GODES','EIGENTUM','REDER','THENAEUT','LABT','MORT','DIGE','WEGE','KOENIGS','NAHE','NOT','NOTH','ZUR','OWI','ENGE','SEIDEN','ALTES','BIS','NUT','NUTZ','HEIL','NEID','TREU','TREUE','SUN','DIENST','SANG','DINC','HULDE','STEINE','LANT','HERRE','DIENEST','GEBOT','SCHWUR','ORDEN','RICHTER','DUNKEL','EHRE','EDELE','SCHULD','SEGEN','FLUCH','RACHE','KOENIG','DASS','EDEL','ADEL','SCHRAT','SALZBERG','WEICHSTEIN','ORANGENSTRASSE','GOTTDIENER','GOTTDIENERS','TRAUT','LEICH','HEIME','SCHARDT','IHM','STIER','NEST','DES','EINEN','DEGEN','REISTEN','REIST','WINDUNRUH','WINDUNRUHS','UNRUH','HEHL','HECHELT','IRREN','OEDE','ERE','NOTE','SEE','TEE','URE','GAB','GIGE','NDCE'])

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
    'UOD':'TOD','EOD':'ODE','ENG':'GEN','EODE':'OEDE',
    'EER':'ERE','WRDA':'WARD','ENOT':'NOTE','EES':'SEE',
    'ETE':'TEE','ABG':'GAB','UER':'URE',
    'GEIG':'GIGE',
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
print(f"SESSION 28 BASELINE: {base_cov}/{total} = {base_cov/total*100:.1f}%")

tokens = dp_segment_full(base_tr, base_known)

# Documented letter swaps in this cipher
SWAP_PAIRS = [('I', 'L'), ('E', 'I'), ('E', 'L'), ('I', 'E')]

# Extended German word list
GERMAN_WORDS = set(KNOWN)
EXTRA = [
    # 2-3 letter
    'OHN', 'IHN', 'IHR', 'MIR', 'DIR', 'WEM', 'DOM', 'RUH', 'RAT', 'TAL',
    'HOF', 'TOR', 'RAD', 'MAG', 'SAH', 'GAB', 'ZOG', 'BOG', 'IRR',
    'ERZ', 'OHR', 'UHR', 'RUF', 'EID', 'OEL', 'AUE', 'ARG',
    # 4 letter
    'WEHR', 'HEER', 'MEER', 'LEER', 'HERZ', 'GIER', 'TIER', 'ZIER',
    'ARME', 'EHRE', 'RUHE', 'TORE', 'SAGE', 'EIDE', 'LEIB', 'REIF',
    'RAUM', 'HELM', 'REIS', 'WEIN', 'REIN', 'FEIN', 'MEIN', 'DEIN',
    'KEIN', 'BEIN', 'LEID', 'HERD', 'HORT', 'HULD', 'MUND', 'BUND',
    'FUND', 'RUND', 'KUND', 'WUND', 'SUCH', 'FLUG', 'ZAHL', 'WAHL',
    'RAST', 'LAST', 'MAST', 'FAST', 'HAST', 'GAST', 'LIST', 'MIST',
    'FIST', 'ROST', 'MOST', 'KOST', 'LUST', 'JUST', 'RUST', 'DUST',
    'SALZ', 'HOLZ', 'STOLZ', 'WURM', 'STURM', 'TURM', 'FORM', 'NORM',
    'BORN', 'HORN', 'DORN', 'KORN', 'ZORN', 'KERN', 'FERN', 'GERN',
    'STERN', 'HERR', 'NARR', 'STARR', 'WIRR', 'KNIRR',
    'TRUG', 'KLUG', 'FLUG', 'PFLUG', 'BEUG', 'ZEUG',
    'HIEB', 'LIEB', 'DIEB', 'TRIEB', 'SIEB',
    'HASS', 'MASS', 'NASS', 'FASS', 'LASS', 'GRUSS',
    'GRAB', 'STAB', 'RAUB', 'LAUB', 'STAUB', 'TRAUB',
    'ZIEL', 'SPIEL', 'VIEL', 'WIEL',
    'KLEID', 'STREIT', 'BREIT', 'BEREIT', 'GELEIT',
    # 5 letter
    'NACHT', 'MACHT', 'WACHT', 'TRACHT', 'SCHLACHT',
    'KRAFT', 'SCHAR', 'SCHEIN', 'STEIN', 'KLEIN',
    'ALLEIN', 'VEREIN', 'GEBEIN',
    'FEIND', 'FREUND', 'SCHWERT', 'PFERD',
    'RECHT', 'KNECHT', 'SCHLECHT',
    'KAMPF', 'KRAMPF', 'DAMPF', 'SUMPF',
    'ANGST', 'GUNST', 'KUNST', 'DUNST', 'BRUNST',
    'GRUFT', 'KLUFT', 'LUFT', 'DUFT',
    'GNADE', 'EHREN', 'ADELN', 'EDLEN', 'ORDEN',
    'WUNDER', 'UNTER', 'HINTER', 'WINTER', 'DONNER',
    'HAUPT', 'MEISTER', 'GEISTER',
    'NEBEL', 'DUNKEL', 'FINSTER',
    'SCHILD', 'BILD', 'WILD', 'MILD', 'GILD',
    'SCHULD', 'UNSCHULD', 'HULD',
    'TREUE', 'REUE', 'FREUDE', 'BEUTE',
    # 6+ letter
    'GEHEIMNIS', 'ERKENNTNIS', 'FINSTERNIS',
    'SCHICKSAL', 'URSPRUNG', 'UNTERGANG',
    'WAHRHEIT', 'WEISHEIT', 'FREIHEIT', 'DUNKELHEIT',
    'EWIGKEIT', 'EINIGKEIT', 'TAPFERKEIT',
    'GEWALTIG', 'MAECHTIG', 'PRAECHTIG',
    'VERGESSEN', 'VERLOREN', 'GEFALLEN', 'ZERBROCHEN',
    'VERBORGEN', 'VERGANGEN', 'VERWUNSCHEN',
    # MHG specific
    'VROUWE', 'RECKE', 'GENIST', 'STAETE', 'MILTE',
    'SAELDE', 'TUGENT', 'ZUHT', 'WIGANT', 'DEGEN',
    'MINNE', 'TRIUWE', 'ELLEN', 'SEGEN',
    'HEHL', 'HEHLEN', 'OEDE', 'WUESTE',
    'TODE', 'TODES', 'TOTEN', 'GNADE',
    'SCHAR', 'SCHAREN', 'EDLEN',
    'HAUPT', 'HAUFE', 'HAUSE',
    'MEIDE', 'HEIDE', 'WEIDE', 'SEIDE', 'SCHNEIDE',
    'WACHE', 'RACHE', 'SACHE', 'DRACHE',
    'ZEICHEN', 'LEICHEN', 'REICHEN', 'WEICHEN', 'GLEICHEN',
    'SCHATTEN', 'KLAFFEN', 'WAFFEN', 'SCHAFFEN',
    'GRABEN', 'RABEN', 'HABEN', 'GABEN', 'KLAGEN',
    'SAGEN', 'TRAGEN', 'WAGEN', 'FRAGEN', 'JAGEN',
]
GERMAN_WORDS.update(EXTRA)

# =====================================================================
# APPROACH 1: Letter-swap tolerant anagram matching
# =====================================================================
print("\n" + "="*70)
print("APPROACH 1: LETTER-SWAP TOLERANT ANAGRAM MATCHING")
print("="*70)

# Collect unique garbled blocks with frequency
garbled_blocks = Counter()
garbled_contexts = defaultdict(list)
for i, (kind, val, s, e) in enumerate(tokens):
    if kind != 'G': continue
    garbled_blocks[val] += 1
    if len(garbled_contexts[val]) < 2:
        prev = tokens[i-1][1] if i > 0 and tokens[i-1][0] == 'W' else '^'
        nxt = tokens[i+1][1] if i < len(tokens)-1 and tokens[i+1][0] == 'W' else '$'
        garbled_contexts[val].append(f"{prev} |{val}| {nxt}")

print(f"\nUnique garbled blocks: {len(garbled_blocks)}")

# For blocks 3-8 chars, try anagram with 0-1 letter swap
print("\n--- Testing 3-8 char blocks with 0-1 letter swaps ---")
swap_results = []
for block, count in garbled_blocks.most_common():
    if len(block) < 3 or len(block) > 8: continue
    block_letters = list(block)

    # Try exact anagram first
    sorted_block = sorted(block)
    for word in GERMAN_WORDS:
        if len(word) == len(block) and sorted(word) == sorted_block and word != block:
            cov, _, _, _ = apply_text({block: word}, {word})
            delta = cov - base_cov
            if delta > 0:
                swap_results.append((delta, block, word, count, 'exact', garbled_contexts[block]))

    # Try with 1 letter swap (replace each position with swap partner)
    for pos in range(len(block_letters)):
        orig_letter = block_letters[pos]
        for a, b in SWAP_PAIRS:
            if orig_letter == a:
                new_letter = b
            elif orig_letter == b:
                new_letter = a
            else:
                continue
            modified = list(block_letters)
            modified[pos] = new_letter
            sorted_mod = sorted(modified)
            for word in GERMAN_WORDS:
                if len(word) == len(block) and sorted(word) == sorted_mod and word != ''.join(modified):
                    cov, _, _, _ = apply_text({block: word}, {word})
                    delta = cov - base_cov
                    if delta > 0:
                        swap_desc = f"swap {orig_letter}->{new_letter} at pos {pos}"
                        swap_results.append((delta, block, word, count, swap_desc, garbled_contexts[block]))

swap_results.sort(key=lambda x: -x[0])
seen = set()
print(f"\nPositive-delta results (with letter swaps):")
for delta, block, word, count, desc, ctxs in swap_results:
    key = (block, word)
    if key in seen: continue
    seen.add(key)
    print(f"  +{delta:3d}: {block} -> {word} ({count}x, {desc})")
    for ctx in ctxs[:1]:
        print(f"         {ctx}")

# =====================================================================
# APPROACH 2: Split garbled blocks into 2 known words
# =====================================================================
print("\n" + "="*70)
print("APPROACH 2: SPLIT GARBLED BLOCKS INTO 2 KNOWN WORDS")
print("="*70)

split_results = []
for block, count in garbled_blocks.most_common():
    if len(block) < 4 or len(block) > 12: continue

    # Try splitting at every position
    for split_pos in range(2, len(block) - 1):
        left = block[:split_pos]
        right = block[split_pos:]

        # Check if both halves are anagrams of known words
        sorted_left = sorted(left)
        sorted_right = sorted(right)

        for w1 in GERMAN_WORDS:
            if len(w1) != len(left) or sorted(w1) != sorted_left: continue
            for w2 in GERMAN_WORDS:
                if len(w2) != len(right) or sorted(w2) != sorted_right: continue
                combined = w1 + w2
                cov, _, _, _ = apply_text({block: combined}, {w1, w2})
                delta = cov - base_cov
                if delta > 0:
                    split_results.append((delta, block, w1, w2, count, garbled_contexts[block]))

split_results.sort(key=lambda x: -x[0])
seen = set()
print(f"\nPositive-delta block splits:")
for delta, block, w1, w2, count, ctxs in split_results[:20]:
    key = (block, w1, w2)
    if key in seen: continue
    seen.add(key)
    print(f"  +{delta:3d}: {block} -> {w1}+{w2} ({count}x)")
    for ctx in ctxs[:1]:
        print(f"         {ctx}")

# =====================================================================
# APPROACH 3: +1 pattern (block has 1 extra letter, remove it)
# =====================================================================
print("\n" + "="*70)
print("APPROACH 3: +1 PATTERN (remove 1 extra letter)")
print("="*70)

plus1_results = []
for block, count in garbled_blocks.most_common():
    if len(block) < 4 or len(block) > 10: continue

    # Try removing each position
    for skip_pos in range(len(block)):
        reduced = block[:skip_pos] + block[skip_pos+1:]
        sorted_reduced = sorted(reduced)
        for word in GERMAN_WORDS:
            if len(word) == len(reduced) and sorted(word) == sorted_reduced:
                cov, _, _, _ = apply_text({block: word}, {word})
                delta = cov - base_cov
                if delta > 0:
                    removed = block[skip_pos]
                    plus1_results.append((delta, block, word, count, f"remove {removed} at pos {skip_pos}", garbled_contexts[block]))

plus1_results.sort(key=lambda x: -x[0])
seen = set()
print(f"\nPositive-delta +1 removals:")
for delta, block, word, count, desc, ctxs in plus1_results[:20]:
    key = (block, word)
    if key in seen: continue
    seen.add(key)
    print(f"  +{delta:3d}: {block} -> {word} ({count}x, {desc})")
    for ctx in ctxs[:1]:
        print(f"         {ctx}")

# =====================================================================
# APPROACH 4: Greedy cumulative of all positive results
# =====================================================================
print("\n" + "="*70)
print("APPROACH 4: GREEDY CUMULATIVE APPLICATION")
print("="*70)

all_cands = []
seen_labels = set()

for delta, block, word, count, desc, ctxs in swap_results + plus1_results:
    label = f"{block}->{word}"
    if label in seen_labels: continue
    if delta > 0:
        seen_labels.add(label)
        all_cands.append((label, {block: word}, {word}))

for delta, block, w1, w2, count, ctxs in split_results:
    label = f"{block}->{w1}+{w2}"
    if label in seen_labels: continue
    if delta > 0:
        seen_labels.add(label)
        all_cands.append((label, {block: w1+w2}, {w1, w2}))

cum_map = {}
cum_known = set()
cum_cov = base_cov

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
    print(f"  APPLIED: {label} = +{best_delta} (cumulative: {cum_cov}/{total} = {cum_cov/total*100:.1f}%)")

print(f"\nSESSION 28 RESULT: {cum_cov}/{total} = {cum_cov/total*100:.1f}%")
print(f"GAIN: +{cum_cov - base_cov} chars (+{(cum_cov - base_cov)/total*100:.1f}%)")
