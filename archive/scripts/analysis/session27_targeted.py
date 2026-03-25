#!/usr/bin/env python3
"""Session 27: Targeted attack on highest-impact remaining garbled blocks."""
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

KNOWN = set(['AB','AM','AN','ALS','AUF','AUS','BEI','DA','DAS','DEM','DEN','DER','DES','DIE','DU','ER','ES','IM','IN','IST','JA','MAN','OB','SO','UM','UND','VON','VOR','WO','ZU','EIN','ICH','SIE','WER','WIE','WAS','WIR','GEH','GIB','HAT','HIN','HER','NUN','NUR','SEI','TUN','TUT','SAG','WAR','NU','SIN','STANDE','NACHTS','NIT','TOT','TER','ABER','ALLE','ALLES','ALTE','ALTEN','ALTER','AUCH','BAND','BERG','BURG','DENN','DIES','DIESE','DIESER','DIESEN','DIESEM','DOCH','DORT','DREI','DURCH','EINE','EINEM','EINEN','EINER','EINES','ENDE','ERDE','ERST','ERSTE','FACH','FAND','FERN','FEST','FORT','GAR','GANZ','GEGEN','GEIST','GOTT','GOLD','GRAB','GROSS','GRUFT','GUT','HAND','HEIM','HELD','HERR','HIER','HOCH','IMMER','KANN','KLAR','KRAFT','LAND','LANG','LICHT','MACHT','MEHR','MUSS','NACH','NACHT','NAHM','NAME','NEU','NEUE','NEUEN','NICHT','NIE','NOCH','ODER','ORT','ORTEN','REDE','REDEN','REICH','RIEF','RUIN','RUNE','RUNEN','SAND','SAGT','SCHAUN','SCHON','SEHR','SEID','SEIN','SEINE','SEINEN','SEINER','SEINEM','SEINES','SICH','SIND','SOHN','SOLL','STEH','STEIN','STEINE','STEINEN','STERN','TAG','TAGE','TAGEN','TAT','TEIL','TIEF','TOD','TURM','UNTER','URALTE','VIEL','VIER','WAHR','WALD','WAND','WARD','WEIL','WELT','WENN','WERT','WESEN','WILL','WIND','WIRD','WORT','WORTE','ZEIT','ZEHN','ZORN','FINDEN','GEBEN','GEHEN','HABEN','KOMMEN','LEBEN','LESEN','NEHMEN','SAGEN','SEHEN','STEHEN','SUCHEN','WISSEN','WISSET','RUFEN','WIEDER','OEL','SCE','MINNE','MIN','HEL','ODE','SER','GEN','INS','GEIGET','BERUCHTIG','BERUCHTIGER','MEERE','NEIGT','WISTEN','MANIER','HUND','GODE','GODES','EIGENTUM','REDER','THENAEUT','LABT','MORT','DIGE','WEGE','KOENIGS','NAHE','NOT','NOTH','ZUR','OWI','ENGE','SEIDEN','ALTES','BIS','NUT','NUTZ','HEIL','NEID','TREU','TREUE','SUN','DIENST','SANG','DINC','HULDE','STEINE','LANT','HERRE','DIENEST','GEBOT','SCHWUR','ORDEN','RICHTER','DUNKEL','EHRE','EDELE','SCHULD','SEGEN','FLUCH','RACHE','KOENIG','DASS','EDEL','ADEL','SCHRAT','SALZBERG','WEICHSTEIN','ORANGENSTRASSE','GOTTDIENER','GOTTDIENERS','TRAUT','LEICH','HEIME','SCHARDT','IHM','STIER','NEST','DES','EINEN','DEGEN','REISTEN','REIST','WINDUNRUH','WINDUNRUHS','UNRUH','HEHL','HECHELT','IRREN','OEDE','ERE','NOTE','SEE','TEE','URE'])

# Session 27 anagram map (includes all new resolutions)
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
    # Session 27 new
    'UOD':'TOD','EOD':'ODE','ENG':'GEN','EODE':'OEDE',
    'EER':'ERE','WRDA':'WARD','ENOT':'NOTE','EES':'SEE',
    'ETE':'TEE','ABG':'GAB','UER':'URE',
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
print(f"SESSION 27 BASELINE: {base_cov}/{total} = {base_cov/total*100:.1f}%")

# =====================================================================
# TARGET 1: GEIG (4x, "ER GEIG TEE")
# GEIGET is in KNOWN. Could GEIG+TE = GEIGTE (past tense of geigen)?
# Or is GEIG the garbled form and TEE is separate?
# =====================================================================
print("\n" + "="*70)
print("TARGET 1: GEIG pattern (4x)")
print("="*70)

tokens = dp_segment_full(base_tr, base_known)
for i, (kind, val, s, e) in enumerate(tokens):
    if kind == 'G' and 'GEIG' in val:
        ctx_start = max(0, i-3)
        ctx_end = min(len(tokens), i+4)
        ctx = ' '.join(f"[{t[1]}]" if t[0]=='G' else t[1] for t in tokens[ctx_start:ctx_end])
        print(f"  pos {s}: ...{ctx}...")

# GEIG is 4 letters: G,E,I,G
# GIGE = fiddle (MHG) - is an anagram!
# Also: GEIGTE = played fiddle (past tense), but that's 6 chars
# Test GEIG -> GIGE
for word in ['GIGE']:
    cov, _, _, _ = apply_text({'GEIG': word}, {word})
    print(f"  GEIG -> {word}: delta={cov-base_cov:+d}")

# Try cross-boundary: GEIG+TEE (7 chars) -> ?
# Letters G,E,I,G,T,E,E = sorted: E,E,E,G,G,I,T
# GEIGET+E = GEIGET + E (geiget is already known)
# Actually: ER+GEIG+TEE = ... try ERGEIG -> ?
for combo, words in [
    ('GEIGTEE', [('GEIGET', 'E')]),  # split into GEIGET + spare E
]:
    # Test: replace GEIG+TEE -> GEIGET + E
    # But this requires complex replacement... let's try direct
    pass

# Actually ER GEIG TEE S SIN = ER GEIGET E+SSIN?
# Let me check what follows TEE
print("\n  Extended context around GEIG:")
for i, (kind, val, s, e) in enumerate(tokens):
    if kind == 'G' and 'GEIG' in val:
        ctx_start = max(0, i-2)
        ctx_end = min(len(tokens), i+6)
        ctx_tokens = tokens[ctx_start:ctx_end]
        ctx = ' '.join(f"[{t[1]}]" if t[0]=='G' else t[1] for t in ctx_tokens)
        print(f"    {ctx}")

# Try: GEIG -> part of GEIGET cross-boundary with next
# GEIG+T from TEE = GEIGT -> not a word
# GEIG+TE from TEE = GEIGTE (6 chars, "fiddled") leaving E
cov, _, _, _ = apply_text({'GEIGTEE': 'GEIGETE'}, {'GEIGET'})
print(f"  GEIGTEE -> GEIGETE (split GEIGET+E): delta={cov-base_cov:+d}")

# Actually GEIGTE would need the text to have GEIGTEE contiguously
# Check if GEIGTEE appears in base_tr
count = base_tr.count('GEIGTEE')
print(f"  'GEIGTEE' in text: {count}x")
count2 = base_tr.count('GEIG')
print(f"  'GEIG' in text: {count2}x")

# =====================================================================
# TARGET 2: IGAA (4x, "TUT IGAA ER")
# Letters: I,G,A,A -> GAAI, AAGI...
# Cross-boundary: TUT+IGAA = TUTIGAA (7) -> ?
# Or: IGAA+ER = IGAAER (6) -> ?
# =====================================================================
print("\n" + "="*70)
print("TARGET 2: IGAA pattern (4x)")
print("="*70)

for i, (kind, val, s, e) in enumerate(tokens):
    if kind == 'G' and 'IGAA' in val:
        ctx_start = max(0, i-3)
        ctx_end = min(len(tokens), i+4)
        ctx = ' '.join(f"[{t[1]}]" if t[0]=='G' else t[1] for t in tokens[ctx_start:ctx_end])
        print(f"  pos {s}: ...{ctx}...")

# IGAA: I,G,A,A -> possible: GAAI (no), let me check via anagram
# Cross-boundary right: IGAA+ER = IGAAER (6 chars): I,G,A,A,E,R
# Sorted: A,A,E,G,I,R -> GAAEIR -> possible: GRAIE? No
# What about: IGAAER -> anagram of GAAIER -> REAGIA? No clear word
# Cross-boundary left: TUT+IGAA = TUTIGAA (7): A,A,G,I,T,T,U
# GATTIUA? No

# Maybe IGAA is part of the GEIGET pattern?
# Let me check: ER GEIG TEE S SIN ... TUT IGAA ER
# These might be in the same book sequence

# Check book-level context for IGAA
print("\n  IGAA in per-book context:")
for bidx, bpairs in enumerate(book_pairs_list):
    book_text = ''.join(v7.get(p, '?') for p in bpairs)
    for a in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
        book_text = book_text.replace(a, ANAGRAM_MAP[a])
    if 'IGAA' in book_text:
        toks = dp_segment_full(book_text, base_known)
        display = ' '.join(f"{{{t[1]}}}" if t[0]=='G' else t[1] for t in toks)
        print(f"  Book {bidx}: {display}")

# =====================================================================
# TARGET 3: HISS (3x, "DEN HISS TUN")
# Letters: H,I,S,S -> no clear anagram
# Cross-boundary: DEN+HISS = DENHISS (7): D,E,H,I,N,S,S
# Sorted: D,E,H,I,N,S,S -> SCHIENDS? HINDES? SEINDS?
# HISS+TUN = HISSTUN (7): H,I,N,S,S,T,U
# =====================================================================
print("\n" + "="*70)
print("TARGET 3: HISS pattern (3x)")
print("="*70)

for i, (kind, val, s, e) in enumerate(tokens):
    if kind == 'G' and val == 'HISS':
        ctx_start = max(0, i-3)
        ctx_end = min(len(tokens), i+4)
        ctx = ' '.join(f"[{t[1]}]" if t[0]=='G' else t[1] for t in tokens[ctx_start:ctx_end])
        print(f"  pos {s}: ...{ctx}...")

# HISS -> SCHI? No... SHIS? Let me think MHG
# In MHG: "hiez" = was called, "his" = commanded
# Cross: DEN + HISS + TUN = "the HISS do"
# HISSTUN sorted: H,I,N,S,S,T,U -> SINSTUH? No
# DENHISS sorted: D,E,H,I,N,S,S -> HINDES+S? SINDHES?
# Actually DENHISS -> HINDES+S? or is it SCHINDEN -> no, too many letters
# HISS could be HISS (hiss/command, MHG)? Leave as is.

# =====================================================================
# TARGET 4: ND (9x, multiple contexts)
# ND is just 2 chars: N,D -> DN
# Contexts: ORT ND TER, GEH ND FINDEN
# =====================================================================
print("\n" + "="*70)
print("TARGET 4: ND pattern (9x)")
print("="*70)

nd_contexts = []
for i, (kind, val, s, e) in enumerate(tokens):
    if kind == 'G' and val == 'ND':
        ctx_start = max(0, i-2)
        ctx_end = min(len(tokens), i+3)
        ctx = ' '.join(f"[{t[1]}]" if t[0]=='G' else t[1] for t in tokens[ctx_start:ctx_end])
        nd_contexts.append(ctx)
        print(f"  pos {s}: ...{ctx}...")

# ND = N,D -> DN (no word)
# Cross-boundary: ORT+ND = ORTND (5): D,N,O,R,T -> TRONDN? No
# ND+TER = NDTER (5): D,E,N,R,T -> TREND! Or RNDET
# Or: ND+FINDEN = NDFINDEN (8) -> too long
# Test NDTER -> TREND
print("\n  Testing ND cross-boundary resolutions:")
for word in ['TREND', 'RNDET', 'DRENT', 'INDER', 'UNTER']:
    if sorted(word) == sorted('NDTER'):
        cov, _, _, _ = apply_text({'NDTER': word}, {word})
        print(f"    NDTER -> {word}: delta={cov-base_cov:+d}")

# Also test: ORTND -> anagram?
for word in ['TRONDN', 'DORNT', 'NORDT', 'FRONT']:
    if len(word) == 5 and sorted(word) == sorted('ORTND'):
        cov, _, _, _ = apply_text({'ORTND': word}, {word})
        print(f"    ORTND -> {word}: delta={cov-base_cov:+d}")

# GEH+ND -> GEHND (5): D,E,G,H,N -> HENGD? NEHGD?
# ND+FINDEN -> NDFINDEN: too long.
# Actually: GEH ND FINDEN could be GEHEND FINDEN (going to find)
# GEHND -> GEHEND needs 6 chars but GEHND is only 5
# Unless ND absorbs the F? NDFINDEN -> ND+FINDEN (2+6=8)
# What if it's: GEH + UND + FINDEN where U was consumed?

# =====================================================================
# TARGET 5: EHHIIHW (3x, "GEN EHHIIHW IN")
# 7 chars: E,H,H,I,I,H,W = E,H,H,H,I,I,W
# =====================================================================
print("\n" + "="*70)
print("TARGET 5: EHHIIHW pattern (3x)")
print("="*70)

for i, (kind, val, s, e) in enumerate(tokens):
    if kind == 'G' and 'EHHIIHW' in val:
        ctx_start = max(0, i-3)
        ctx_end = min(len(tokens), i+4)
        ctx = ' '.join(f"[{t[1]}]" if t[0]=='G' else t[1] for t in tokens[ctx_start:ctx_end])
        print(f"  pos {s}: ...{ctx}...")

# EHHIIHW: E,H,H,H,I,I,W
# Possible anagrams with 3 H's... unusual
# WEIHHI + H? No
# Cross-boundary: GEN+EHHIIHW = GENEHHIIHW (10): E,E,G,H,H,H,I,I,N,W
# Hmm... EINWEIHUNG has E,E,G,H,I,I,N,N,U,W - close but not matching
# EHHIIHW+IN = EHHIIHWIN (9): E,H,H,H,I,I,I,N,W
# WEIHHINNI? No

# Could be a proper noun?
# In Tibia: HIWHIEH? No...
# What if one H is actually a different letter? Mapping issue?

# Let me check the raw code pairs for EHHIIHW
print("\n  Checking raw code pairs for EHHIIHW blocks:")
for bidx, bpairs in enumerate(book_pairs_list):
    book_text = ''.join(v7.get(p, '?') for p in bpairs)
    # Don't apply anagram map, look at raw
    pos = 0
    while True:
        p = book_text.find('EHHIIHW', pos)
        if p == -1: break
        # Find the code pairs that produced this
        raw_codes = bpairs[p:p+7]
        print(f"  Book {bidx} pos {p}: codes={raw_codes}")
        print(f"    Each code: {[(c, v7.get(c,'?')) for c in raw_codes]}")
        pos = p + 1

# =====================================================================
# TARGET 6: WRLGTNELNR (4x, "STEH WRLGTNELNR HEL")
# 10 chars: always followed by HEL then WINDUNRUH
# Full fixed sequence: STEH + WRLGTNELNR + HEL + WINDUNRUH
# =====================================================================
print("\n" + "="*70)
print("TARGET 6: WRLGTNELNR context analysis (4x)")
print("="*70)

# Show full context in each book
for bidx, bpairs in enumerate(book_pairs_list):
    book_text = ''.join(v7.get(p, '?') for p in bpairs)
    if 'WRLGTNELNR' in book_text:
        for a in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
            book_text = book_text.replace(a, ANAGRAM_MAP[a])
        toks = dp_segment_full(book_text, base_known)
        display = ' '.join(f"{{{t[1]}}}" if t[0]=='G' else t[1] for t in toks)
        print(f"  Book {bidx}: {display}")

# The full decoded sequence around WRLGTNELNR:
# NU STEH WRLGTNELNR HEL WINDUNRUH FINDEN NEIGT DAS ES DER...
# = "Now stand [PLACE] HEL wind-unrest find inclines that it the..."
# WRLGTNELNR = 10 chars: E,G,L,L,N,N,R,R,T,W
# Possible place name anagrams:
print("\n  WRLGTNELNR letter frequency: ", sorted('WRLGTNELNR'))
# E,G,L,L,N,N,R,R,T,W
# WELLRINGTN? GRENTWELL? WELLINGTON? (W,E,L,L,I,N,G,T,O,N) - has I and O, we have R,R,N
# What about: ERNTLINGEN? E,R,N,T,L,I,N,G,E,N - has I,E extra
# GELTENNRWR? No
# TRENNWELLGR? Too many letters
# Let me try: what German place names have these letters?
# E,G,L,L,N,N,R,R,T,W
# RENNWELTGL? No...

# Check if it could be a compound:
# WELT (4) + remaining RLGNN+R = ?
# RING (4) + remaining WLLTNE+R = WELLTNER?
# STERN (5) + remaining WLGLN+R = ?

# Tibia places with similar letters:
# "ERNTLINGEN" type pattern?
# What about NELLERGTWRN?
print("  Possible Tibia-related anagrams of WRLGTNELNR (E,G,L,L,N,N,R,R,T,W):")
tibia_places = [
    'MINTWALLIN', 'GREENSHORE', 'TROLLENBERG', 'GREENWALL',
    'WELLSPRING', 'NIGHTWELL', 'TROLL', 'GREENLAND',
    'TRENNWALL', 'RINGWALL', 'WELLENGRAT', 'GRENTWALL',
    'NELLERTWRG', 'WRLGTNELNR',
    # German compound words
    'WETTRENNEN', 'ENTGELLNRW', 'WELTRENNGL',
]
for tp in tibia_places:
    if sorted(tp) == sorted('WRLGTNELNR'):
        print(f"    MATCH: {tp}")

# =====================================================================
# TARGET 7: NDCE (7x, "DIE NDCE FACH")
# 4 chars: C,D,E,N
# =====================================================================
print("\n" + "="*70)
print("TARGET 7: NDCE analysis (7x)")
print("="*70)

# NDCE: C,D,E,N -> anagrams: DENC, CEND, CDEN, NCED, EDCN
# Cross-boundary: DIE+NDCE = DIENDCE (7): C,D,D,E,E,I,N
# NDCE+FACH = NDCEFACH (8): A,C,C,D,E,F,H,N
# "DIE NDCE FACH" = "the NDCE compartment"
# Could NDCE be a proper noun? A German abbreviation?

# Check raw codes
print("  Raw codes for NDCE:")
for bidx, bpairs in enumerate(book_pairs_list):
    book_text = ''.join(v7.get(p, '?') for p in bpairs)
    pos = 0
    while True:
        p = book_text.find('NDCE', pos)
        if p == -1: break
        raw_codes = bpairs[p:p+4]
        print(f"    Book {bidx} pos {p}: codes={raw_codes} -> {[v7.get(c,'?') for c in raw_codes]}")
        pos = p + 1
        break  # Just first occurrence per book

# NDCE sorted = C,D,E,N
# CENDE? DECN? What about DENC? Or NCED?
# In MHG: ENCE? EDENC?
# "DIE NDCE FACH" might be "DIE [CEND/DENC] FACH"
# Or it could be that NDCE is actually 2 words: ND + CE
# ND = 2 chars, CE = 2 chars
# If we split: DIE + ND + CE + FACH -> cross-boundary: DIEND = DIEN+D? CEFACH?

# Test NDCE -> CEND, DENC, EDCN, NCED
for word in ['CEND', 'DENC', 'NCED']:
    cov, _, _, _ = apply_text({'NDCE': word}, {word})
    print(f"  NDCE -> {word}: delta={cov-base_cov:+d}")

# Test cross-boundary: DIENDCE -> ? (7 chars C,D,D,E,E,I,N)
# DICEEND? DECIDEN?
# NDCEFACH -> ? (8 chars A,C,C,D,E,F,H,N)
# HANDCEF+C? FACHEND+C?
# What about: NDCE is part of UNSCHULD or similar?

# =====================================================================
# TARGET 8: CHN (8x, "IN CHN SER")
# =====================================================================
print("\n" + "="*70)
print("TARGET 8: CHN analysis (8x)")
print("="*70)

for i, (kind, val, s, e) in enumerate(tokens):
    if kind == 'G' and val == 'CHN':
        ctx_start = max(0, i-3)
        ctx_end = min(len(tokens), i+4)
        ctx = ' '.join(f"[{t[1]}]" if t[0]=='G' else t[1] for t in tokens[ctx_start:ctx_end])
        print(f"  pos {s}: ...{ctx}...")

# CHN: C,H,N -> NCH (nach? but nach is 4 chars)
# Cross: IN+CHN = INCHN (5): C,H,I,N,N -> CHINN? NNCIH?
# CHN+SER = CHNSER (6): C,E,H,N,R,S -> SCHNRE? RENSCH? SCHENR?
# Actually: SCHER! Wait CHNSER = C,E,H,N,R,S sorted = C,E,H,N,R,S
# SCHENR? SCHNRE? RENSCH?
# What about: HERRSCHEN? No, too many letters
# CHNSER -> SCHNRE -> hmm
# INCHN: C,H,I,N,N -> NCHNI? CHINN?

# Actually "IN CHN SER" in the narrative...
# Could be "IN [?] SEHR" (in [?] very)
# SER is an accepted word already (very, MHG form of SEHR)
# So the reading is "IN [place/thing] VERY/MUCH"
# CHN could be a proper noun abbreviation

# =====================================================================
# SUMMARY
# =====================================================================
print("\n" + "="*70)
print("SUMMARY: Session 27 targeted analysis")
print("="*70)
print(f"""
Current coverage: {base_cov}/{total} = {base_cov/total*100:.1f}%
Remaining garbled: ~22%

Highest-impact unsolved blocks:
  1. WRLGTNELNR (40 chars) - proper noun, letters E,G,L,L,N,N,R,R,T,W
  2. NDCE (28 chars) - proper noun or unknown word, always "DIE NDCE FACH"
  3. CHN (24 chars) - proper noun fragment, always "IN CHN SER"
  4. UNR (21 chars) - =NUR causes regressions, needs context-specific fix
  5. EHHIIHW (21 chars) - unknown, 3 H's unusual
  6. ND (18 chars) - short garbled, various contexts
  7. GEIG (16 chars) - related to GEIGET?
  8. IGAA (16 chars) - unknown pattern

Blocks classified as proper nouns (untranslatable without lore):
  - WRLGTNELNR, NDCE, CHN, THENAEUT, UTRUNR

Blocks needing more analysis:
  - EHHIIHW, IGAA, GEIG, HISS, LGTNELGZ
""")
