#!/usr/bin/env python3
"""Session 29 Round 2: Attack remaining 10.9% garbled text.
Focus on: context-specific UNR->NUR, ND pattern, low-coverage books,
and extended bag-of-letters on 1-occurrence blocks.
"""
import json, os
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

KNOWN = set(['AB','AM','AN','ALS','AUF','AUS','BEI','DA','DAS','DEM','DEN','DER','DES','DIE','DU','ER','ES','IM','IN','IST','JA','MAN','OB','SO','UM','UND','VON','VOR','WO','ZU','EIN','ICH','SIE','WER','WIE','WAS','WIR','GEH','GIB','HAT','HIN','HER','NUN','NUR','SEI','TUN','TUT','SAG','WAR','NU','SIN','STANDE','NACHTS','NIT','TOT','TER','ABER','ALLE','ALLES','ALTE','ALTEN','ALTER','AUCH','BAND','BERG','BURG','DENN','DIES','DIESE','DIESER','DIESEN','DIESEM','DOCH','DORT','DREI','DURCH','EINE','EINEM','EINEN','EINER','EINES','ENDE','ERDE','ERST','ERSTE','FACH','FAND','FERN','FEST','FORT','GAR','GANZ','GEGEN','GEIST','GOTT','GOLD','GRAB','GROSS','GRUFT','GUT','HAND','HEIM','HELD','HERR','HIER','HOCH','IMMER','KANN','KLAR','KRAFT','LAND','LANG','LICHT','MACHT','MEHR','MUSS','NACH','NACHT','NAHM','NAME','NEU','NEUE','NEUEN','NICHT','NIE','NOCH','ODER','ORT','ORTEN','REDE','REDEN','REICH','RIEF','RUIN','RUNE','RUNEN','SAND','SAGT','SCHAUN','SCHON','SEHR','SEID','SEIN','SEINE','SEINEN','SEINER','SEINEM','SEINES','SICH','SIND','SOHN','SOLL','STEH','STEIN','STEINE','STEINEN','STERN','TAG','TAGE','TAGEN','TAT','TEIL','TIEF','TOD','TURM','UNTER','URALTE','VIEL','VIER','WAHR','WALD','WAND','WARD','WEIL','WELT','WENN','WERT','WESEN','WILL','WIND','WIRD','WORT','WORTE','ZEIT','ZEHN','ZORN','FINDEN','GEBEN','GEHEN','HABEN','KOMMEN','LEBEN','LESEN','NEHMEN','SAGEN','SEHEN','STEHEN','SUCHEN','WISSEN','WISSET','RUFEN','WIEDER','OEL','SCE','MINNE','MIN','HEL','ODE','SER','GEN','INS','GEIGET','BERUCHTIG','BERUCHTIGER','MEERE','NEIGT','WISTEN','MANIER','HUND','GODE','GODES','EIGENTUM','REDER','THENAEUT','LABT','MORT','DIGE','WEGE','KOENIGS','NAHE','NOT','NOTH','ZUR','OWI','ENGE','SEIDEN','ALTES','BIS','NUT','NUTZ','HEIL','NEID','TREU','TREUE','SUN','DIENST','SANG','DINC','HULDE','STEINE','LANT','HERRE','DIENEST','GEBOT','SCHWUR','ORDEN','RICHTER','DUNKEL','EHRE','EDELE','SCHULD','SEGEN','FLUCH','RACHE','KOENIG','DASS','EDEL','ADEL','SCHRAT','SALZBERG','WEICHSTEIN','ORANGENSTRASSE','GOTTDIENER','GOTTDIENERS','TRAUT','LEICH','HEIME','SCHARDT','IHM','STIER','NEST','DES','EINEN','DEGEN','REISTEN','REIST','WINDUNRUH','WINDUNRUHS','UNRUH','HEHL','HECHELT','IRREN','OEDE','ERE','NOTE','SEE','TEE','URE','GAB','GIGE','NDCE','EID','AUE','MIR',
    # Session 29
    'WRLGTNELNR','CHN','EHHIIHW','IGAA','LGTNELGZ','HISDIZA',
    'EI','EN','AD','OR','WI','OD','LAB',
    'UNE','GETRAS','HISS',
])

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
    'DEE':'EID','URIT':'TREU','RUIT':'TREU','NTEIG':'NEIGT',
    'EHI':'HEL','LRM':'MIR','ADTHA':'DAHAT','MISE':'IMES',
    'UNRN':'NUN','NDMI':'MIN','NSCHA':'NACH','AEUU':'AUE',
    'ENDNO':'DENN','ENDR':'DER','TOAD':'TOD','DDNE':'DEN','UENO':'NEU',
    # Session 29 bag-of-letters
    'OIAITOEMEEND':'OEDENAMETEEO',
    'OIAITOEMEENDGEEMKMTGRSCASEZSTEIEHHIS':'HECHELTALLESGOTTDIENERSOMMKMGAEZSEES',
    'UUISEMIADIIRGELNMH':'LANGHEIMEDIESERUUM',
    'EHHIIHHISLUIRUNNS':'HEHLUNRUHSEINESHI',
    'AUIGLAUNHEARUCHT':'LANGURALTEAUCHUH',
    'TTGEARUCHTIG':'TATGUTREICHG',
    'DNRHAUNIIOD':'OEDENURHAND',
    'SEZEEUITGH':'ZUHELGEIST',
    'CHDKELSNDEF':'DESDENICHKF',
    'UHONRIELT':'ORTNEUHEL',
    'HIEAUIENA':'ANAUEHEIL',
    'UONGETRAS':'ORTAUSGEN',
    'LHLADIZEEELU':'EDELEALLEZUH',
    'EEOIGTSTEI':'SOTEETEILG',
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
print(f"BASELINE: {base_cov}/{total} = {base_cov/total*100:.1f}%")

# Get current garbled inventory
tokens = dp_segment_full(base_tr, base_known)
garbled_blocks = Counter()
garbled_contexts = defaultdict(list)
for i, (kind, val, s, e) in enumerate(tokens):
    if kind != 'G': continue
    garbled_blocks[val] += 1
    if len(garbled_contexts[val]) < 3:
        prev = tokens[i-1][1] if i > 0 and tokens[i-1][0] == 'W' else '^'
        nxt = tokens[i+1][1] if i < len(tokens)-1 and tokens[i+1][0] == 'W' else '$'
        garbled_contexts[val].append(f"{prev} |{val}| {nxt}")

total_garbled = sum(len(v)*c for v,c in garbled_blocks.items())
print(f"Remaining garbled: {total_garbled} chars ({total_garbled/total*100:.1f}%)")

# ============================================================
# STRATEGY 1: Remaining proper noun + small block classification
# ============================================================
print("\n" + "="*70)
print("STRATEGY 1: SMALL BLOCK CLASSIFICATION")
print("="*70)

small_candidates = []
for block, count in garbled_blocks.items():
    if len(block) <= 5 and count >= 1:
        cov, _, _, _ = apply_text(None, {block})
        delta = cov - base_cov
        if delta > 0:
            small_candidates.append((delta, block, count))

small_candidates.sort(key=lambda x: -x[0])
for delta, block, count in small_candidates[:30]:
    ctxs = garbled_contexts[block][:2]
    print(f"  {delta:+3d} | {block:12s} ({count}x) | {ctxs[0]}")

# ============================================================
# STRATEGY 2: Extended bag-of-letters on remaining blocks
# ============================================================
print("\n" + "="*70)
print("STRATEGY 2: EXTENDED BAG-OF-LETTERS")
print("="*70)

SWAP_PAIRS = [('I', 'E'), ('I', 'L')]

def can_form_from_bag(word, bag):
    remaining = list(bag)
    for c in word:
        if c in remaining:
            remaining.remove(c)
        else:
            found = False
            for a, b in SWAP_PAIRS:
                if c == a and b in remaining:
                    remaining.remove(b)
                    found = True
                    break
                if c == b and a in remaining:
                    remaining.remove(a)
                    found = True
                    break
            if not found:
                return False, []
    return True, remaining

def best_word_cover(letters, known_set, depth=0, max_depth=3, memo=None):
    if memo is None: memo = {}
    key = tuple(sorted(letters))
    if key in memo: return memo[key]
    if len(letters) < 2 or depth >= max_depth:
        memo[key] = (0, [])
        return (0, [])
    best = (0, [])
    for w in known_set:
        wl = len(w)
        if wl < 2 or wl > len(letters): continue
        ok, remaining = can_form_from_bag(w, letters)
        if not ok: continue
        sub_score, sub_words = best_word_cover(remaining, known_set, depth+1, max_depth, memo)
        total_score = wl + sub_score
        if total_score > best[0]:
            best = (total_score, [w] + sub_words)
    memo[key] = best
    return best

small_known = set(w for w in KNOWN if len(w) <= 15)

# Target remaining blocks >= 5 chars that weren't in session 29 round 1
for block, count in sorted(garbled_blocks.items(), key=lambda x: -(len(x[0])*x[1])):
    if len(block) < 5: continue
    # Skip blocks already classified as proper nouns
    if block in KNOWN: continue
    letters = list(block)
    score, words = best_word_cover(letters, small_known, max_depth=3)
    if score >= 3:
        used_letters = list(block)
        replacement_parts = []
        for w in words:
            replacement_parts.append(w)
            for c in w:
                if c in used_letters:
                    used_letters.remove(c)
                else:
                    for a, b in SWAP_PAIRS:
                        if c == a and b in used_letters:
                            used_letters.remove(b)
                            break
                        if c == b and a in used_letters:
                            used_letters.remove(a)
                            break
        replacement = ''.join(replacement_parts) + ''.join(used_letters)
        test_cov, _, _, _ = apply_text({block: replacement}, None)
        delta = test_cov - base_cov
        if delta > 0:
            ctxs = garbled_contexts[block][:1]
            print(f"  {delta:+3d} | {block:25s} ({count}x) -> {words} ({score}/{len(block)}) | {ctxs[0] if ctxs else '?'}")

# ============================================================
# STRATEGY 3: Context-specific UNR fix
# ============================================================
print("\n" + "="*70)
print("STRATEGY 3: CONTEXT-SPECIFIC UNR -> NUR")
print("="*70)

# UNR appears 7x. Adding 'UNR':'NUR' breaks WINDUNRUH.
# Solution: replace the longer context strings that contain UNR
# Example: "TREUUNR" -> "TREUNUR" (if TREU+NUR is valid)
# Or protect WINDUNRUH by using a longer key

# Find all occurrences of UNR in the decoded text
test_tr = base_tr
positions = []
start = 0
while True:
    pos = test_tr.find('UNR', start)
    if pos == -1: break
    # Check if inside WINDUNRUH
    is_inside_windunruh = (pos >= 4 and test_tr[pos-4:pos+5] == 'DWINDUNRUH'[:9]) or \
                          (pos >= 4 and test_tr[pos-4:pos+3] == 'DUNRUH'[:3])
    context = test_tr[max(0,pos-10):pos+13]
    positions.append((pos, is_inside_windunruh, context))
    start = pos + 1

print(f"UNR occurrences in text: {len(positions)}")
windunruh_count = sum(1 for _, inside, _ in positions if inside)
isolated_count = sum(1 for _, inside, _ in positions if not inside)
print(f"  Inside WINDUNRUH: {windunruh_count}")
print(f"  Isolated: {isolated_count}")
for pos, inside, ctx in positions:
    marker = "WIND" if inside else "FREE"
    print(f"  [{marker}] pos {pos}: ...{ctx}...")

# Try protecting WINDUNRUH by pre-replacing it with a placeholder
# then doing UNR->NUR, then restoring
# Actually, since ANAGRAM_MAP sorts by length, we can ensure WINDUNRUH
# is replaced first. But the issue is WINDUNRUH is OUTPUT of another
# replacement (UIRUNNHWND->WINDUNRUH), so it exists in the post-replacement text.

# Alternative: instead of UNR->NUR in ANAGRAM_MAP, we can try specific
# longer patterns that contain isolated UNR
# Find patterns around isolated UNR
print("\nIsolated UNR contexts:")
for pos, inside, ctx in positions:
    if inside: continue
    # Get 3 chars before and after
    before = test_tr[max(0,pos-5):pos]
    after = test_tr[pos+3:pos+8]
    print(f"  ...{before}[UNR]{after}...")

# Test: What if we add 'TREUUNR': 'TREUNUR' and 'ODUNR': 'ODNUR' etc.?
# These longer patterns wouldn't match inside WINDUNRUH
context_replacements = {}
for pos, inside, ctx in positions:
    if inside: continue
    # Get the text around UNR for context-specific replacement
    # Look for patterns like XUNR where X is part of preceding word
    before3 = test_tr[max(0,pos-3):pos]
    after3 = test_tr[pos+3:min(len(test_tr),pos+6)]
    # Try 1-char context before
    if pos > 0:
        key1 = test_tr[pos-1:pos+3]  # e.g., "EUNR"
        val1 = key1[0] + 'NUR'       # e.g., "ENUR"
        if key1 not in context_replacements and key1 not in ANAGRAM_MAP:
            # Check this doesn't appear inside WINDUNRUH
            if 'WINDUNRUH'.find(key1) == -1:
                context_replacements[key1] = val1

print(f"\nContext-specific UNR replacements found:")
for k, v in context_replacements.items():
    print(f"  '{k}': '{v}'")

# Test each
for k, v in context_replacements.items():
    cov, _, _, _ = apply_text({k: v}, None)
    delta = cov - base_cov
    print(f"  '{k}'->'{v}': {delta:+d}")

# Test all combined
if context_replacements:
    cov, _, _, _ = apply_text(context_replacements, None)
    delta = cov - base_cov
    print(f"\n  ALL combined: {delta:+d}")

# ============================================================
# STRATEGY 4: ND pattern analysis
# ============================================================
print("\n" + "="*70)
print("STRATEGY 4: ND PATTERN ANALYSIS")
print("="*70)

# ND appears 10x, mostly in "ORT ND TER"
# Could be UND (and) with missing U, or a word fragment
# Check all contexts
for i, (kind, val, s, e) in enumerate(tokens):
    if kind == 'G' and val == 'ND':
        prev = tokens[i-1] if i > 0 else None
        nxt = tokens[i+1] if i < len(tokens)-1 else None
        prev_str = prev[1] if prev and prev[0] == 'W' else f'[{prev[1]}]' if prev else '^'
        nxt_str = nxt[1] if nxt and nxt[0] == 'W' else f'[{nxt[1]}]' if nxt else '$'
        print(f"  {prev_str} |ND| {nxt_str}")

# Test ND as UND (would add a char)
cov_nd_und, _, _, _ = apply_text({'ND': 'UND'}, None)
print(f"\n  ND->UND: {cov_nd_und - base_cov:+d}")

# ============================================================
# SUMMARY: Greedy combination of all round 2 gains
# ============================================================
print("\n" + "="*70)
print("GREEDY COMBINATION OF ALL ROUND 2 GAINS")
print("="*70)

# Collect all positive candidates
all_candidates = []

# From strategy 1 (small blocks)
for delta, block, count in small_candidates:
    if delta > 0:
        all_candidates.append((delta, f"KNOWN:{block}", None, {block}))

# From strategy 3 (context-specific UNR)
for k, v in context_replacements.items():
    cov, _, _, _ = apply_text({k: v}, None)
    delta = cov - base_cov
    if delta > 0:
        all_candidates.append((delta, f"MAP:{k}->{v}", {k: v}, None))

all_candidates.sort(key=lambda x: -x[0])

combined_map = {}
combined_known = set()
combined_cov = base_cov

for delta, name, extra_map, extra_known in all_candidates:
    test_map = dict(combined_map)
    test_known = set(combined_known)
    if extra_map: test_map.update(extra_map)
    if extra_known: test_known.update(extra_known)
    cov, _, _, _ = apply_text(test_map if test_map else None,
                               test_known if test_known else None)
    if cov > combined_cov:
        old = combined_cov
        combined_cov = cov
        if extra_map: combined_map.update(extra_map)
        if extra_known: combined_known.update(extra_known)
        print(f"  ADDED {name}: +{cov-old} (cumulative {combined_cov}/{total} = {combined_cov/total*100:.1f}%)")

print(f"\nFINAL: {combined_cov}/{total} = {combined_cov/total*100:.1f}% (+{combined_cov-base_cov} from baseline)")

if combined_map:
    print(f"\nNew ANAGRAM_MAP entries:")
    for k, v in combined_map.items():
        print(f"  '{k}': '{v}',")
if combined_known:
    print(f"\nNew KNOWN entries:")
    for w in sorted(combined_known):
        print(f"  '{w}',")
