#!/usr/bin/env python3
"""Session 27: Investigate the C anomaly. Code 18 is the only C code.
C is rare in German and almost always appears as CH, SCH, CK.
Check if code 18 might be misassigned."""
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

# Find all positions of code 18 (C)
print("="*70)
print("CODE 18 (C) ANALYSIS")
print("="*70)

all_pairs = []
for bidx, bpairs in enumerate(book_pairs_list):
    for pos, pair in enumerate(bpairs):
        all_pairs.append((bidx, pos, pair))

code18_positions = []
for bidx, bpairs in enumerate(book_pairs_list):
    for pos, pair in enumerate(bpairs):
        if pair == '18':
            # Get surrounding context (decoded)
            book_decoded = ''.join(v7.get(p, '?') for p in bpairs)
            start = max(0, pos-5)
            end = min(len(bpairs), pos+6)
            ctx = book_decoded[start:end]
            marker = '.' * (pos - start) + 'C' + '.' * (end - pos - 1)
            code18_positions.append((bidx, pos, ctx, marker))

print(f"\nTotal code 18 occurrences: {len(code18_positions)}")
print(f"\nAll code 18 contexts:")
for bidx, pos, ctx, marker in code18_positions:
    # Highlight the C position
    ctx_chars = list(ctx)
    c_pos = pos - max(0, pos-5)
    print(f"  Book {bidx:2d} pos {pos:3d}: ...{ctx[:c_pos]}[C]{ctx[c_pos+1:]}...")

# Check what digrams code 18 appears in
print(f"\nC digram analysis (what comes before/after C):")
before_c = Counter()
after_c = Counter()
for bidx, bpairs in enumerate(book_pairs_list):
    book_decoded = ''.join(v7.get(p, '?') for p in bpairs)
    for pos in range(len(book_decoded)):
        if book_decoded[pos] == 'C':
            if pos > 0:
                before_c[book_decoded[pos-1]] += 1
            if pos < len(book_decoded) - 1:
                after_c[book_decoded[pos+1]] += 1

print(f"  Before C: {dict(before_c.most_common())}")
print(f"  After C:  {dict(after_c.most_common())}")

# In German, C almost always appears as:
# CH (most common), SCH, CK, CE (in loanwords)
# Check how many C's are in these patterns
ch_count = all_text.count('CH')
sch_count = all_text.count('SCH')
ck_count = all_text.count('CK')
total_c = all_text.count('C')
print(f"\n  Total C: {total_c}")
print(f"  CH: {ch_count} ({ch_count/total_c*100:.0f}%)")
print(f"  SCH: {sch_count} ({sch_count/total_c*100:.0f}%)")
print(f"  CK: {ck_count} ({ck_count/total_c*100:.0f}%)")
print(f"  Other C positions: {total_c - ch_count} ({(total_c-ch_count)/total_c*100:.0f}%)")

# Find all C positions NOT in CH or SCH patterns
print(f"\n  C positions NOT in CH/SCH/CK patterns:")
for i, ch in enumerate(all_text):
    if ch != 'C': continue
    before = all_text[i-1] if i > 0 else '^'
    after = all_text[i+1] if i < len(all_text)-1 else '$'

    is_ch = (after == 'H')
    is_sch = (before == 'S' and after == 'H')
    is_ck = (after == 'K')

    if not is_ch:
        ctx = all_text[max(0,i-5):i+6]
        print(f"    pos {i}: ...{ctx}... (before={before}, after={after})")

# What if code 18 is actually another letter?
# Test code 18 as each possible letter
print(f"\n{'='*70}")
print(f"CODE 18 REASSIGNMENT TEST")
print(f"{'='*70}")

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

KNOWN = set(['AB','AM','AN','ALS','AUF','AUS','BEI','DA','DAS','DEM','DEN','DER','DES','DIE','DU','ER','ES','IM','IN','IST','JA','MAN','OB','SO','UM','UND','VON','VOR','WO','ZU','EIN','ICH','SIE','WER','WIE','WAS','WIR','GEH','GIB','HAT','HIN','HER','NUN','NUR','SEI','TUN','TUT','SAG','WAR','NU','SIN','STANDE','NACHTS','NIT','TOT','TER','ABER','ALLE','ALLES','ALTE','ALTEN','ALTER','AUCH','BAND','BERG','BURG','DENN','DIES','DIESE','DIESER','DIESEN','DIESEM','DOCH','DORT','DREI','DURCH','EINE','EINEM','EINEN','EINER','EINES','ENDE','ERDE','ERST','ERSTE','FACH','FAND','FERN','FEST','FORT','GAR','GANZ','GEGEN','GEIST','GOTT','GOLD','GRAB','GROSS','GRUFT','GUT','HAND','HEIM','HELD','HERR','HIER','HOCH','IMMER','KANN','KLAR','KRAFT','LAND','LANG','LICHT','MACHT','MEHR','MUSS','NACH','NACHT','NAHM','NAME','NEU','NEUE','NEUEN','NICHT','NIE','NOCH','ODER','ORT','ORTEN','REDE','REDEN','REICH','RIEF','RUIN','RUNE','RUNEN','SAND','SAGT','SCHAUN','SCHON','SEHR','SEID','SEIN','SEINE','SEINEN','SEINER','SEINEM','SEINES','SICH','SIND','SOHN','SOLL','STEH','STEIN','STEINE','STEINEN','STERN','TAG','TAGE','TAGEN','TAT','TEIL','TIEF','TOD','TURM','UNTER','URALTE','VIEL','VIER','WAHR','WALD','WAND','WARD','WEIL','WELT','WENN','WERT','WESEN','WILL','WIND','WIRD','WORT','WORTE','ZEIT','ZEHN','ZORN','FINDEN','GEBEN','GEHEN','HABEN','KOMMEN','LEBEN','LESEN','NEHMEN','SAGEN','SEHEN','STEHEN','SUCHEN','WISSEN','WISSET','RUFEN','WIEDER','OEL','SCE','MINNE','MIN','HEL','ODE','SER','GEN','INS','GEIGET','BERUCHTIG','BERUCHTIGER','MEERE','NEIGT','WISTEN','MANIER','HUND','GODE','GODES','EIGENTUM','REDER','THENAEUT','LABT','MORT','DIGE','WEGE','KOENIGS','NAHE','NOT','NOTH','ZUR','OWI','ENGE','SEIDEN','ALTES','BIS','NUT','NUTZ','HEIL','NEID','TREU','TREUE','SUN','DIENST','SANG','DINC','HULDE','STEINE','LANT','HERRE','DIENEST','GEBOT','SCHWUR','ORDEN','RICHTER','DUNKEL','EHRE','EDELE','SCHULD','SEGEN','FLUCH','RACHE','KOENIG','DASS','EDEL','ADEL','SCHRAT','SALZBERG','WEICHSTEIN','ORANGENSTRASSE','GOTTDIENER','GOTTDIENERS','TRAUT','LEICH','HEIME','SCHARDT','IHM','STIER','NEST','DES','EINEN','DEGEN','REISTEN','REIST','WINDUNRUH','WINDUNRUHS','UNRUH','HEHL','HECHELT','IRREN','OEDE','ERE','NOTE','SEE','TEE','URE','GAB','GIGE','NDCE'])

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

# Baseline with C
tr_base = all_text
for a in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    tr_base = tr_base.replace(a, ANAGRAM_MAP[a])
total = sum(1 for c in tr_base if c != '?')
base_cov = dp_score(tr_base, KNOWN)
print(f"\nBaseline (18=C): {base_cov}/{total} = {base_cov/total*100:.1f}%")

# Test each alternative letter for code 18
for test_letter in 'ABDEFGHIKLMNOPRSTUWZ':
    if test_letter == 'C': continue
    # Create modified v7
    mod_v7 = dict(v7)
    mod_v7['18'] = test_letter
    # Decode with modified mapping
    mod_text = ''.join(''.join(mod_v7.get(p, '?') for p in bpairs) for bpairs in book_pairs_list)
    # Apply anagram map (some anagrams may no longer match)
    for a in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
        mod_text = mod_text.replace(a, ANAGRAM_MAP[a])
    mod_total = sum(1 for c in mod_text if c != '?')
    mod_cov = dp_score(mod_text, KNOWN)
    delta = mod_cov - base_cov
    if delta != 0:
        print(f"  18={test_letter}: {mod_cov}/{mod_total} = {mod_cov/mod_total*100:.1f}% (delta: {delta:+d})")
        # Show what NDCE and CHN become
        # Find NDCE equivalent in modified text
        ndce_new = 'ND' + test_letter + 'E'
        chn_new = test_letter + 'HN'
        sch_new = 'S' + test_letter + 'H'
        print(f"    NDCE -> {ndce_new}, CHN -> {chn_new}, SCH -> {sch_new}")
