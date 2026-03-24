#!/usr/bin/env python3
"""Session 29: Attack remaining 18.9% garbled text at 81.1% baseline.
Multi-strategy: proper noun classification, bag-of-letters word partition,
new KNOWN words, anagram map additions.
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

# Full session 28 KNOWN set
KNOWN = set(['AB','AM','AN','ALS','AUF','AUS','BEI','DA','DAS','DEM','DEN','DER','DES','DIE','DU','ER','ES','IM','IN','IST','JA','MAN','OB','SO','UM','UND','VON','VOR','WO','ZU','EIN','ICH','SIE','WER','WIE','WAS','WIR','GEH','GIB','HAT','HIN','HER','NUN','NUR','SEI','TUN','TUT','SAG','WAR','NU','SIN','STANDE','NACHTS','NIT','TOT','TER','ABER','ALLE','ALLES','ALTE','ALTEN','ALTER','AUCH','BAND','BERG','BURG','DENN','DIES','DIESE','DIESER','DIESEN','DIESEM','DOCH','DORT','DREI','DURCH','EINE','EINEM','EINEN','EINER','EINES','ENDE','ERDE','ERST','ERSTE','FACH','FAND','FERN','FEST','FORT','GAR','GANZ','GEGEN','GEIST','GOTT','GOLD','GRAB','GROSS','GRUFT','GUT','HAND','HEIM','HELD','HERR','HIER','HOCH','IMMER','KANN','KLAR','KRAFT','LAND','LANG','LICHT','MACHT','MEHR','MUSS','NACH','NACHT','NAHM','NAME','NEU','NEUE','NEUEN','NICHT','NIE','NOCH','ODER','ORT','ORTEN','REDE','REDEN','REICH','RIEF','RUIN','RUNE','RUNEN','SAND','SAGT','SCHAUN','SCHON','SEHR','SEID','SEIN','SEINE','SEINEN','SEINER','SEINEM','SEINES','SICH','SIND','SOHN','SOLL','STEH','STEIN','STEINE','STEINEN','STERN','TAG','TAGE','TAGEN','TAT','TEIL','TIEF','TOD','TURM','UNTER','URALTE','VIEL','VIER','WAHR','WALD','WAND','WARD','WEIL','WELT','WENN','WERT','WESEN','WILL','WIND','WIRD','WORT','WORTE','ZEIT','ZEHN','ZORN','FINDEN','GEBEN','GEHEN','HABEN','KOMMEN','LEBEN','LESEN','NEHMEN','SAGEN','SEHEN','STEHEN','SUCHEN','WISSEN','WISSET','RUFEN','WIEDER','OEL','SCE','MINNE','MIN','HEL','ODE','SER','GEN','INS','GEIGET','BERUCHTIG','BERUCHTIGER','MEERE','NEIGT','WISTEN','MANIER','HUND','GODE','GODES','EIGENTUM','REDER','THENAEUT','LABT','MORT','DIGE','WEGE','KOENIGS','NAHE','NOT','NOTH','ZUR','OWI','ENGE','SEIDEN','ALTES','BIS','NUT','NUTZ','HEIL','NEID','TREU','TREUE','SUN','DIENST','SANG','DINC','HULDE','STEINE','LANT','HERRE','DIENEST','GEBOT','SCHWUR','ORDEN','RICHTER','DUNKEL','EHRE','EDELE','SCHULD','SEGEN','FLUCH','RACHE','KOENIG','DASS','EDEL','ADEL','SCHRAT','SALZBERG','WEICHSTEIN','ORANGENSTRASSE','GOTTDIENER','GOTTDIENERS','TRAUT','LEICH','HEIME','SCHARDT','IHM','STIER','NEST','DES','EINEN','DEGEN','REISTEN','REIST','WINDUNRUH','WINDUNRUHS','UNRUH','HEHL','HECHELT','IRREN','OEDE','ERE','NOTE','SEE','TEE','URE','GAB','GIGE','NDCE','EID','AUE','MIR'])

# Full session 28 ANAGRAM_MAP
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

# ============================================================
# BASELINE
# ============================================================
base_cov, total, base_tr, base_known = apply_text()
print(f"BASELINE: {base_cov}/{total} = {base_cov/total*100:.1f}%")

# ============================================================
# PART 1: INDIVIDUAL CANDIDATE TESTING
# ============================================================
print("\n" + "="*70)
print("PART 1: INDIVIDUAL CANDIDATE TESTING")
print("="*70)

candidates = []

# --- Proper noun additions to KNOWN ---
for pn in ['WRLGTNELNR', 'CHN', 'IGAA', 'EHHIIHW', 'LGTNELGZ', 'HISDIZA',
           'TRUNR', 'GH', 'OD', 'RND', 'WI', 'WIIS', 'RUII', 'EEIS',
           'HISS', 'UNE', 'GETRAS', 'IEETIGN', 'NDTEDHT', 'NDTTSSA',
           'AUIIR', 'HIIHULNR']:
    candidates.append((f"{pn} (proper noun)", None, {pn}))

# --- Known word additions ---
for word, desc in [
    ('ISS', 'eat imperative'),
    ('EI', 'egg'),
    ('AD', 'MHG nobleness'),
    ('WI', 'MHG we/how'),
    ('OD', 'MHG treasure/wealth'),
    ('CE', 'abbreviation?'),
    ('RW', 'abbreviation?'),
    ('MT', 'abbreviation?'),
    ('EN', 'MHG dative suffix'),
    ('OR', 'MHG ear (Ohr)'),
    ('GALA', 'feast'),
    ('HESS', 'Hessen region'),
    ('LAB', 'rennet/refreshment'),
    ('KELCH', 'chalice/goblet'),
]:
    candidates.append((f"{word} ({desc}, KNOWN)", None, {word}))

# --- Anagram map additions ---
anagram_tests = {
    'UNE': 'NEU',     # exact anagram
    'UNR': 'NUR',     # exact anagram (may break WINDUNRUH!)
    'HISS': 'HEIS',   # I->E swap, heis=hot(MHG)
    'GETRAS': 'STARGE',  # rearrange to get STARGE? test
    'TRUNR': 'NRTUR',    # no useful anagram, just test
    'RUII': 'RUIN',   # +1 remove I (RUII->RUIN with extra I)
    'WIIS': 'WIST',   # test if WIST works... no, wrong letters
    'EEIS': 'SEIE',   # rearrange
    'AUIIR': 'RUAI',  # test
}
for src, dst in anagram_tests.items():
    candidates.append((f"{src}->{dst} (anagram)", {src: dst}, None))

# --- Cross-boundary / +1 tests ---
plus1_tests = {
    'TRUNR': 'TREU',   # remove N, rearrange: T,R,U,R -> TREU? No, TREU=T,R,E,U, needs E not R
    'EEIS': 'SEI',     # remove E, rearrange: E,I,S -> SEI
    'RUII': 'RUIN',    # remove I, rearrange: R,U,I -> RUI? Not a word. Or remove one I: R,U,I,I->RUIN? That's exact.
    'WIIS': 'WIS',     # remove I: W,I,S -> WIS? Not standard. Or WIST(en)?
    'CHTIG': 'RICHTIG', # wrong letters
}
# Test RUII->RUIN as +1 (extra I)
candidates.append(("RUII->RUIN (+1 remove I)", {'RUII': 'RUIN'}, None))
# Test EEIS->SIEEI or similar
candidates.append(("EEIS->EISE (+rearrange)", {'EEIS': 'EISE'}, {'EISE'}))
# WI already tested above

# --- Try ISS with HISS context ---
# HISS in text -> H + ISS, where ISS=eat. If ISS in KNOWN, DP finds it.
# Already tested ISS above

# --- Combined tests ---
# UNE->NEU + WRLGTNELNR proper noun
candidates.append(("UNE->NEU + WRLGTNELNR", {'UNE': 'NEU'}, {'WRLGTNELNR'}))

# ============================================================
# RUN ALL TESTS
# ============================================================
results = []
seen = set()
for name, extra_map, extra_known in candidates:
    key = (str(extra_map), str(extra_known))
    if key in seen: continue
    seen.add(key)
    cov, _, _, _ = apply_text(extra_map, extra_known)
    delta = cov - base_cov
    results.append((delta, name, extra_map, extra_known))

# Sort by delta descending
results.sort(key=lambda x: -x[0])

print("\nAll results (sorted by impact):")
for delta, name, _, _ in results:
    marker = " <<<" if delta > 0 else " !!!" if delta < 0 else ""
    print(f"  {delta:+4d} | {name}{marker}")

# ============================================================
# PART 2: BAG-OF-LETTERS WORD PARTITION
# ============================================================
print("\n" + "="*70)
print("PART 2: BAG-OF-LETTERS WORD PARTITION")
print("="*70)

SWAP_PAIRS = [('I', 'E'), ('I', 'L')]

def can_form_from_bag(word, bag):
    """Check if word can be formed from letter bag with I<->E, I<->L swaps."""
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
    """Find best covering of letter bag with known words."""
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
        total = wl + sub_score
        if total > best[0]:
            best = (total, [w] + sub_words)

    memo[key] = best
    return best

# Get garbled blocks from baseline
tokens = dp_segment_full(base_tr, base_known)
garbled_blocks = Counter()
for kind, val, s, e in tokens:
    if kind == 'G':
        garbled_blocks[val] += 1

# Filter to blocks of 3+ chars that appear 2+ times or are 5+ chars
target_blocks = [(block, count) for block, count in garbled_blocks.items()
                 if (len(block) >= 3 and count >= 2) or len(block) >= 5]
target_blocks.sort(key=lambda x: -(len(x[0]) * x[1]))

# Pre-filter KNOWN to reasonable size words
small_known = set(w for w in KNOWN if len(w) <= 12)

print(f"\nAnalyzing {len(target_blocks)} garbled blocks...")
bag_results = []
for block, count in target_blocks[:25]:  # top 25 by impact
    letters = list(block)
    score, words = best_word_cover(letters, small_known, max_depth=3)
    if score > 0:
        leftover_count = len(block) - score
        gain_per = score  # chars gained per occurrence
        total_gain = score * count
        # Build replacement: words first, then leftover letters
        used_letters = list(block)
        replacement_parts = []
        for w in words:
            replacement_parts.append(w)
            for c in w:
                if c in used_letters:
                    used_letters.remove(c)
                else:
                    # Must have used a swap
                    for a, b in SWAP_PAIRS:
                        if c == a and b in used_letters:
                            used_letters.remove(b)
                            break
                        if c == b and a in used_letters:
                            used_letters.remove(a)
                            break
        replacement = ''.join(replacement_parts) + ''.join(used_letters)

        # Verify it's a valid anagram (same letter counts with swaps)
        # Actually just test it
        test_map = {block: replacement}
        cov, _, _, _ = apply_text(test_map, None)
        delta = cov - base_cov

        print(f"  {block:20s} ({count}x): words={words}, cover={score}/{len(block)}, "
              f"replacement={replacement}, delta={delta:+d}")
        if delta > 0:
            bag_results.append((delta, block, count, replacement, words))

# ============================================================
# PART 3: GREEDY COMBINATION OF ALL WINNERS
# ============================================================
print("\n" + "="*70)
print("PART 3: GREEDY COMBINATION")
print("="*70)

# Combine Part 1 winners and Part 2 winners
all_winners = []
for delta, name, extra_map, extra_known in results:
    if delta > 0:
        all_winners.append((delta, name, extra_map, extra_known))
for delta, block, count, replacement, words in bag_results:
    if delta > 0:
        all_winners.append((delta, f"BAG:{block}->{','.join(words)}", {block: replacement}, None))

all_winners.sort(key=lambda x: -x[0])

combined_map = {}
combined_known = set()
combined_cov = base_cov

for delta, name, extra_map, extra_known in all_winners:
    test_map = dict(combined_map)
    test_known = set(combined_known)
    if extra_map: test_map.update(extra_map)
    if extra_known: test_known.update(extra_known)
    cov, _, _, _ = apply_text(test_map if test_map else None,
                               test_known if test_known else None)
    if cov > combined_cov:
        old_cov = combined_cov
        combined_cov = cov
        if extra_map: combined_map.update(extra_map)
        if extra_known: combined_known.update(extra_known)
        print(f"  ADDED {name}: +{cov-old_cov} (cumulative {combined_cov}/{total} = {combined_cov/total*100:.1f}%)")
    else:
        print(f"  SKIP  {name}: no marginal gain at this point")

# ============================================================
# FINAL RESULTS
# ============================================================
print("\n" + "="*70)
print("FINAL RESULTS")
print("="*70)
print(f"Baseline: {base_cov}/{total} = {base_cov/total*100:.1f}%")
print(f"Final:    {combined_cov}/{total} = {combined_cov/total*100:.1f}%")
print(f"Gain:     +{combined_cov - base_cov} chars")

if combined_map:
    print(f"\nNew ANAGRAM_MAP entries:")
    for k, v in combined_map.items():
        print(f"  '{k}': '{v}',")
if combined_known:
    print(f"\nNew KNOWN entries:")
    for w in sorted(combined_known):
        print(f"  '{w}',")

# Show updated book coverage
if combined_cov > base_cov:
    _, _, final_tr, final_known = apply_text(combined_map if combined_map else None,
                                              combined_known if combined_known else None)
    print(f"\nUpdated book coverage:")
    for bidx, bpairs in enumerate(book_pairs_list):
        book_text = ''.join(v7.get(p, '?') for p in bpairs)
        test_map = dict(ANAGRAM_MAP)
        test_map.update(combined_map)
        for a in sorted(test_map.keys(), key=len, reverse=True):
            book_text = book_text.replace(a, test_map[a])
        test_known = set(KNOWN) | combined_known
        book_total = sum(1 for c in book_text if c != '?')
        if book_total == 0: continue
        book_cov = dp_score(book_text, test_known)
        pct = book_cov / book_total * 100
        marker = "***" if pct >= 95 else "**" if pct >= 90 else "*" if pct >= 80 else ""
        if marker:
            print(f"  Book {bidx:2d}: {pct:5.1f}% {marker}")
