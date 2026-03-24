#!/usr/bin/env python3
"""
Session 18 continued: Deep MHG analysis of garbled blocks.
1. Try to identify UOD, HED, NLNDEF, UTRUNR using comprehensive MHG lexicon
2. Test word boundary realignment around garbled zones
3. Investigate UNENITGHNEE (11-letter block after SALZBERG)
4. Look for new anagram patterns with expanded word list
"""
import json, os, re
from collections import Counter, defaultdict
from itertools import combinations

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

# Comprehensive MHG lexicon for anagram matching
# Sources: Matthias Lexer's MHG dictionary, Benecke-Mueller-Zarncke
MHG_WORDS = set([
    # Common MHG words (2-4 letters)
    'AB', 'AL', 'AM', 'AN', 'DA', 'DO', 'DU', 'EI', 'ER', 'ES', 'EZ',
    'GE', 'HI', 'IM', 'IN', 'IR', 'JA', 'NU', 'OB', 'SI', 'SO', 'UF',
    'UM', 'UN', 'WE', 'WI', 'ZE', 'ZU',
    'ALS', 'BEI', 'BIN', 'DAS', 'DAZ', 'DEM', 'DEN', 'DER', 'DES',
    'DIE', 'DIR', 'DIS', 'DOC', 'EIN', 'GAR', 'GEN', 'GIB', 'GOT',
    'GUT', 'HAT', 'HER', 'HIN', 'ICH', 'IER', 'INE', 'IST', 'MAN',
    'MER', 'MIN', 'MIR', 'MIT', 'NIE', 'NIT', 'NOC', 'NUN', 'NUR',
    'ODE', 'OUC', 'SAM', 'SEI', 'SER', 'SIN', 'SIT', 'SOL', 'SUN',
    'TUN', 'UND', 'VON', 'VOR', 'WAR', 'WAS', 'WER', 'WIE', 'WIL',
    'WIR', 'WIS', 'WOL',
    'ABER', 'ALLE', 'ALSO', 'ANDE', 'BALT', 'BETE', 'BLUT', 'BOTE',
    'BURT', 'DACH', 'DANK', 'DAZU', 'DICH', 'DIEN', 'DINC', 'DISE',
    'DOCH', 'DORT', 'DRIU', 'DRUM', 'EDEL', 'EHRE', 'EINE', 'ENDE',
    'ERDE', 'GABE', 'GANZ', 'GAST', 'GELT', 'GERN', 'GOLT', 'GOTE',
    'GRAP', 'GRAS', 'GRIM', 'GROS', 'GUAT', 'GUOT', 'HABE', 'HALT',
    'HANT', 'HAUS', 'HEIL', 'HEIM', 'HEIS', 'HELT', 'HERE', 'HERR',
    'HERZ', 'HETE', 'HIEN', 'HIES', 'HOCH', 'HULD', 'HUNT', 'IEMER',
    'JUNC', 'KINT', 'KLAC', 'KLAR', 'KONE', 'KUMT', 'KUND', 'KUNEC',
    'LANT', 'LEIT', 'LIEB', 'LIET', 'LIEZ', 'LIST', 'LONE', 'MACH',
    'MAGE', 'MARC', 'MERE', 'MICH', 'MINE', 'MUOT', 'MUOZ', 'NAME',
    'NAHT', 'NEID', 'NIHT', 'NIUR', 'NOCH', 'NOTH', 'OUCH', 'REDE',
    'RICH', 'RIEF', 'RINT', 'RITE', 'RUIN', 'RUNE', 'SACH', 'SAGE',
    'SANC', 'SEGE', 'SEIL', 'SELT', 'SICH', 'SIHT', 'SINC', 'SINT',
    'SITE', 'SLAC', 'SNIT', 'SOLE', 'SOLT', 'STAT', 'STEC', 'STEIN',
    'STET', 'STIL', 'STIM', 'SULT', 'TAGE', 'TEIL', 'TIEF', 'TORT',
    'TRAT', 'TRIU', 'TROST', 'TUOT', 'UZER', 'VANT', 'VAST', 'VELT',
    'VIEL', 'VINT', 'VORN', 'VORT', 'VROU', 'VUOZ', 'WAHR', 'WALT',
    'WANT', 'WART', 'WEGE', 'WELT', 'WENE', 'WERT', 'WILT', 'WINT',
    'WIRT', 'WISE', 'WIST', 'WIZE', 'WOLT', 'WORT', 'ZAGE', 'ZEIC',
    'ZEIT', 'ZORN', 'ZUHT',
    # 5-letter MHG words
    'ADELE', 'ALLES', 'ALTEN', 'ALTER', 'ALTES', 'BEIDE', 'BLINT',
    'BOTEN', 'BUOCH', 'BURGE', 'DANKE', 'DENNE', 'DESTE', 'DINGE',
    'DURCH', 'DURFT', 'EINEN', 'EINEM', 'EINER', 'EINES', 'ELLEN',
    'ERSTE', 'FUORT', 'GABEN', 'GEGEN', 'GEIST', 'GERNE', 'GLANZ',
    'GNUOC', 'GOLDE', 'GOTER', 'GOTES', 'GRANT', 'GROZE', 'GRUNT',
    'GUOTE', 'HABET', 'HALDE', 'HARTE', 'HEIDE', 'HEILE', 'HEILT',
    'HELFE', 'HENDE', 'HERRE', 'HERZE', 'HIMEL', 'HULDE', 'JUNGE',
    'KLAGE', 'KLAGT', 'KNABE', 'KRAFT', 'KREIZ', 'KRONE', 'KUMIT',
    'KUNNE', 'KUNST', 'LANDE', 'LANGE', 'LEBEN', 'LENGE', 'LESET',
    'LIDEN', 'LIEBE', 'LIEHT', 'LIGET', 'LINDE', 'LISTE', 'LONES',
    'MACHT', 'MAGET', 'MEIDE', 'MEIEN', 'MEIRE', 'MEISE', 'MINNE',
    'MOHTE', 'MUOZE', 'NAHEN', 'NAHTE', 'NAMEN', 'NEMEN', 'NIDER',
    'NIEMEN', 'NIUWE', 'ORTEN', 'OUGEN', 'REHTE', 'REISE', 'REDEN',
    'REINE', 'REITE', 'RIEFE', 'RITER', 'RUNEN', 'SAEHE', 'SAGEN',
    'SCHAZ', 'SCHON', 'SEGEN', 'SEINE', 'SENDE', 'SINNE', 'SOLDE',
    'SPISE', 'STADE', 'STATE', 'STEGE', 'STIMM', 'STRIT', 'SUCHE',
    'SUNDE', 'SWERT', 'TAGES', 'TRIUWE', 'TUGENT', 'UNDER', 'VATER',
    'VERRE', 'VINDE', 'VOLGE', 'VREUDE', 'WALDE', 'WANDE', 'WENDE',
    'WERDE', 'WIRDE', 'WOLDE', 'WOLTE', 'WUNDE', 'ZEIGE', 'ZENDE',
    # 6+ letter MHG words
    'DIENEST', 'DUNKEL', 'EDELEN', 'FRIEDE', 'GEIGET', 'GNAEDE',
    'GROZEN', 'HEILEC', 'HELFEN', 'HERREN', 'HULDEN', 'KIRCHE',
    'KLAGEN', 'KOENEC', 'KUENEC', 'KUMBER', 'LANDEN', 'LANGEN',
    'MEISTER', 'MILTE', 'MINNEN', 'NIDERE', 'RICHES', 'RITTER',
    'SAEIDE', 'SCHATTEN', 'SCHULDE', 'SELBER', 'SENDEN', 'SOLTEN',
    'SPRACH', 'STEINE', 'STEINEN', 'STERBEN', 'STIMME', 'STRAZE',
    'SUNDEN', 'TRIUWEN', 'TUGENDEN', 'VINDEN', 'VROUWE', 'WAENEN',
    'WUNDER', 'ZEICHEN',
    # Place-name elements common in MHG
    'BURG', 'BERG', 'STEIN', 'WALD', 'FELD', 'BRUNN', 'DORF',
    'HEIM', 'HAUSEN', 'KIRCH', 'MUEHLE', 'TURM',
    # Proper nouns from the cipher
    'SALZBERG', 'WEICHSTEIN', 'SCHARDT', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME',
    'THENAEUT', 'EIGENTUM',
    # Additional words found in decoded text
    'BERUCHTIG', 'BERUCHTIGER', 'MEERE', 'NEIGT', 'WISTEN',
    'MANIER', 'GODES', 'REDER', 'LABT', 'DIGE', 'KOENIG',
    'KOENIGS', 'DIENST', 'SANG', 'OWI', 'ENGE', 'SEIDEN',
    'HEIL', 'NEID', 'TREU', 'TREUE', 'HULDE', 'HERRE',
    'EDELE', 'SCHULD', 'SEGEN', 'FLUCH', 'RACHE', 'EHRE',
    # Additional MHG/archaic
    'GENADE', 'GEWALT', 'GEZELT', 'GRUEZE', 'HERZEN',
    'KUMBER', 'LEIDEN', 'LOUGEN', 'MUOTER', 'PRIESTER',
    'SCHILDE', 'SWAERE', 'UNGEMACH', 'VRIEDEN', 'WUNNE',
    # Words potentially in the cipher
    'UNTOT', 'UNTOTE', 'UNTOTEN', 'GEBEIN', 'GEISTER',
    'NEKROMANT', 'ZAUBER', 'RITUAL', 'INSCHRIFT',
    'ORAKEL', 'PORTAL', 'KAMMER', 'KRYPTA',
    'DRUIDE', 'DIENER', 'WACHTER', 'HERRSCHER',
    'BRUDER', 'SCHWESTER', 'TOCHTER', 'MUTTER', 'VATER',
    'STIMME', 'GESANG', 'KLAGE', 'GEBET',
    'SCHATTEN', 'FINSTER', 'DUNKEL', 'BLEICH',
    'HEILIG', 'VERDAMMT', 'VERLOREN',
    'NORDEN', 'SUEDEN', 'WESTEN', 'OSTEN',
    'QUELLE', 'GRUND', 'TIEFE', 'HOEHE',
    'GRENZE', 'SCHWELLE', 'PFAD',
    'GEBEIN', 'LEICHE', 'ASCHE', 'STAUB',
    'OPFER', 'GABE', 'SCHWUR', 'ORDEN',
    'RICHTER', 'URTEIL', 'GERICHT',
])

def sorted_letters(s):
    return ''.join(sorted(s))

# Build comprehensive anagram index
anagram_idx = defaultdict(list)
for w in MHG_WORDS:
    anagram_idx[sorted_letters(w)].append(w)

# ================================================================
# 1. DEEP ANALYSIS OF UNENITGHNEE
# ================================================================
print("=" * 80)
print("ANALYSIS: UNENITGHNEE (11 letters, after KOENIG SALZBERG)")
print("=" * 80)

block = 'UNENITGHNEE'
letters = sorted_letters(block)
print(f"Letters: {block} -> sorted: {letters}")
print(f"Letter counts: {dict(Counter(block))}")

# Exact anagram
exact = anagram_idx.get(letters, [])
if exact:
    print(f"EXACT: {exact}")

# +1 pattern (drop one letter)
print(f"\n+1 anagram candidates (drop one letter from {block}):")
seen = set()
for i in range(len(block)):
    reduced = block[:i] + block[i+1:]
    key = sorted_letters(reduced)
    for match in anagram_idx.get(key, []):
        if match not in seen:
            print(f"  {block} = {match} + '{block[i]}'")
            seen.add(match)

# +2 pattern (drop two letters)
print(f"\n+2 anagram candidates (drop two letters):")
seen2 = set()
for i in range(len(block)):
    for j in range(i+1, len(block)):
        reduced = block[:i] + block[i+1:j] + block[j+1:]
        key = sorted_letters(reduced)
        for match in anagram_idx.get(key, []):
            if match not in seen2 and len(match) >= 5:
                print(f"  {block} = {match} + '{block[i]}','{block[j]}'")
                seen2.add(match)

# Also check: is UNENITGHNEE = ENTEIGNUNG + H - G + E?
# ENTEIGNUNG: E-E-G-G-I-N-N-N-T-U (10 letters)
# UNENITGHNEE: E-E-E-G-H-I-N-N-N-T-U (11 letters)
# Diff: UNENITGHNEE has extra E and H, missing G
print(f"\nComparison with ENTEIGNUNG (expropriation):")
print(f"  ENTEIGNUNG sorted: {''.join(sorted('ENTEIGNUNG'))}")
print(f"  UNENITGHNEE sorted: {letters}")
enteignung_letters = Counter('ENTEIGNUNG')
block_letters = Counter(block)
diff_extra = block_letters - enteignung_letters
diff_missing = enteignung_letters - block_letters
print(f"  UNENITGHNEE has extra: {dict(diff_extra)}")
print(f"  UNENITGHNEE missing: {dict(diff_missing)}")

# Check EINHEITUNG, EINHEGUNG, etc.
german_candidates_11 = [
    'ENTEIGNUNG', 'EINHEITENG', 'GENEIGTNEH', 'EINGEHTNEU',
    'UNEINIGTHE', 'GEHEIMTUNE',
]
for cand in german_candidates_11:
    if sorted_letters(cand) == letters:
        print(f"  MATCH: {cand}")

# ================================================================
# 2. WORD BOUNDARY REALIGNMENT
# ================================================================
print(f"\n{'=' * 80}")
print("WORD BOUNDARY REALIGNMENT: Testing alternative word splits")
print("=" * 80)

# The phrase "IM MIN HED DEM I DIE URALTE STEINEN T ER SCHARDT"
# currently parses as: IM MIN {HED} DEM {I} DIE URALTE STEINEN {T} ER SCHARDT
#
# What if we read it differently?
# Option 1: IM MINNE DEM I DIE... (HED absorbed into MINNE somehow?)
# Option 2: IM MIN HEDDEMI = IM MIN HEIME + extra D?
# Option 3: The T before ER is part of STEINENT (a verb form?)

alternatives = [
    ("Current", "IM MIN HED DEM I DIE URALTE STEINEN T ER SCHARDT"),
    ("Alt 1: HEDDEMI as one block", "IM MIN HEDDEMI DIE URALTE STEINEN TER SCHARDT"),
    ("Alt 2: MINHEDDEMI", "I MINHEDDEMI DIE URALTE STEINEN TER SCHARDT"),
    ("Alt 3: STEINENT ER", "IM MIN HED DEM I DIE URALTE STEINENT ER SCHARDT"),
    ("Alt 4: STEINENTER", "IM MIN HED DEM I DIE URALTE STEINENTER SCHARDT"),
]

for name, phrase in alternatives:
    print(f"\n  {name}:")
    print(f"    {phrase}")

# Check: is HEDDEMI an anagram?
heddemi = 'HEDDEMI'
key = sorted_letters(heddemi)
print(f"\n  HEDDEMI sorted: {key}")
matches = anagram_idx.get(key, [])
if matches:
    print(f"  HEDDEMI exact anagram: {matches}")

# +1 pattern for HEDDEMI
for i in range(len(heddemi)):
    reduced = heddemi[:i] + heddemi[i+1:]
    key = sorted_letters(reduced)
    for match in anagram_idx.get(key, []):
        print(f"  HEDDEMI = {match} + '{heddemi[i]}' (+1)")

# Check: is MINHEDDEMI something?
mhd = 'MINHEDDEMI'
for i in range(2, len(mhd)-2):
    p1 = mhd[:i]
    p2 = mhd[i:]
    k1 = sorted_letters(p1)
    k2 = sorted_letters(p2)
    m1 = anagram_idx.get(k1, [])
    m2 = anagram_idx.get(k2, [])
    if m1 and m2:
        for a in m1[:2]:
            for b in m2[:2]:
                if len(a) >= 3 and len(b) >= 3:
                    print(f"  MINHEDDEMI split {i}: {p1}={a} + {p2}={b}")

# ================================================================
# 3. COMPREHENSIVE GARBLED BLOCK ANALYSIS WITH EXPANDED LEXICON
# ================================================================
print(f"\n{'=' * 80}")
print("EXPANDED ANAGRAM SEARCH (comprehensive MHG lexicon)")
print("=" * 80)

targets = [
    ('UTRUNR', 'place name 7x'),
    ('HIHL', 'place name 9x'),
    ('NDCE', 'after DIE 9x'),
    ('HECHLLT', 'after FACH 5x'),
    ('NLNDEF', 'before SANG 7x'),
    ('UOD', 'after WIR 8x'),
    ('HED', 'before DEM 12x'),
    ('LGTNELGZ', 'after ER 2x'),
    ('TIURIT', 'before ORANGENSTRASSE 3x'),
    ('GCHD', 'after ORTEN 4x'),
    ('RRNI', 'after AB 6x'),
    ('TTUIGAA', 'after ES 3x'),
    ('HISS', 'SO DEN HISS TUN 3x'),
    ('CHN', 'IN CHN ES 10x'),
    ('TNE', 'ALS TNE DAS 4x'),
    ('THARSCR', 'DER THARSCR SCE 2x'),
    ('DETOTNIUR', 'SEINE DETOTNIUR 2x'),
    ('ADTHA', 'ER ADTHA 2x'),
    ('NSCHA', 'WIR NSCHA ER 2x'),
]

for block, desc in targets:
    letters = sorted_letters(block)

    results = []

    # Exact
    for m in anagram_idx.get(letters, []):
        results.append(('exact', m))

    # +1 (block has extra letter)
    for i in range(len(block)):
        reduced = block[:i] + block[i+1:]
        key = sorted_letters(reduced)
        for m in anagram_idx.get(key, []):
            results.append((f'+{block[i]}', m))

    # -1 (block missing a letter)
    for letter in 'ABCDEFGHIKLMNORSTUWZ':
        expanded = block + letter
        key = sorted_letters(expanded)
        for m in anagram_idx.get(key, []):
            results.append((f'-{letter}', m))

    # Deduplicate
    seen = set()
    unique = []
    for typ, word in results:
        if word not in seen:
            seen.add(word)
            unique.append((typ, word))

    if unique:
        print(f"\n  {block} ({desc}):")
        for typ, word in unique[:10]:
            print(f"    [{typ:>6}] {word}")

# ================================================================
# 4. INVESTIGATE RECURRING PHRASE: "THENAEUT ER ALS TNE DAS E NOT"
# ================================================================
print(f"\n{'=' * 80}")
print("PHRASE ANALYSIS: THENAEUT ER ALS TNE DAS E NOT")
print("=" * 80)

# THENAEUT is a proper noun (appears in both books and NPC dialogue)
# TNE = 3 letters: T, N, E
# What if TNE is part of the surrounding text?
# "ALS TNE DAS" = "as TNE that"
# Could be: "ALS EINE DAS" with wrong letter? Or "ALS NET DAS"?

print("""
Context: "THENAEUT ER ALS {TNE} DAS {E} NOT"
Translation attempt: "THENAEUT he as [?] that [?] need/distress"

TNE possibilities:
  - If exact word: no common German/MHG word "TNE"
  - If anagram: T-N-E -> ENT (prefix, "de-/un-"), NET (net), TEN (MHG?)
  - If part of ALSTNE: A-E-L-N-S-T -> STALEN? LANSET? SALENT?
  - If part of TNEDAS: A-D-E-N-S-T -> STANDE (stand), SANDEL, DANTES

  Key insight: TNEDAS rearranged = STANDE (stood/stand) or DANTES!
  ALS TNEDAS = ALS STANDE? = "as [he] stood"?

  In MHG: "stuont" = stood (past tense of "stan")
  But STANDE is valid MHG present participle/subjunctive!

  Or: TNED = DENT? TEND?
  "ALS TNED ENDE" appears once. If TNED = DENT? Not MHG.

  What about reading it as: ALSTNEDAS = ALS + [word]?
  TNEDAS = 6 letters: A,D,E,N,S,T
  STANDE (MHG: would stand) - PERFECT FIT!

  So: "THENAEUT ER ALS STANDE DAS E NOT"
  = "THENAEUT he as standing/stood that [E] need"
  = "THENAEUT, he who stood as... that... need/distress"
""")

# Verify: is TNEDAS an anagram of STANDE?
tnedas = 'TNEDAS'
stande = 'STANDE'
print(f"  TNEDAS sorted: {sorted_letters(tnedas)}")
print(f"  STANDE sorted: {sorted_letters(stande)}")
print(f"  Match: {sorted_letters(tnedas) == sorted_letters(stande)}")

# But wait - the DP segments it as "{TNE} DAS" not "TNEDAS"
# The word DAS is matched by the DP. So we'd need to NOT match DAS
# and instead match STANDE across the boundary.
# This is a word-boundary issue! The DP greedily matches DAS but
# the real word might be STANDE spanning TNE+DAS.

# Check other splits of the garbled text around TNE
print(f"\n  Checking if STANDE is a valid new KNOWN word...")
print(f"  STANDE = MHG subjunctive of 'stan' (to stand)")
print(f"  'er stande' = 'he would stand' or 'he stood'")

# Similarly check ALSTNE
alstne = 'ALSTNE'
key = sorted_letters(alstne)
matches = anagram_idx.get(key, [])
print(f"\n  ALSTNE anagrams: {matches}")

# Check TNEDASE (TNE + DAS + E)
tnedase = 'TNEDASE'
key = sorted_letters(tnedase)
matches = anagram_idx.get(key, [])
print(f"  TNEDASE anagrams: {matches}")

# ================================================================
# 5. LOOK FOR CROSS-BOUNDARY ANAGRAMS
# ================================================================
print(f"\n{'=' * 80}")
print("CROSS-BOUNDARY ANAGRAM SEARCH")
print("(garbled blocks that span DP word boundaries)")
print("=" * 80)

# Key cases where the DP might be splitting a word incorrectly:
cross_boundary = [
    ('TNEDAS', '{TNE} DAS', 'ALS [?] E NOT'),
    ('EODE', '{E} ODE', '[?] UTRUNR'),
    ('SDIM', '{SD} IM', 'AN [?] MIN'),
    ('RUIIN', '{RUI} IN', 'SCHAUN [?] WISTEN'),
    ('NUOD', 'NU {OD}', 'ENDE [?] IM'),
    ('DEENDE', '{DE} ENDE', 'NEU [?] E WEICHSTEIN'),
    ('EERLAB', '{E} ER {L} AB', 'GOTTDIENERS [?] RRNI WIR'),
    ('NDTERAM', '{NDT} ER AM', 'ORT [?] NEU'),
    ('EORUNEORT', '{EO} RUNE ORT', 'GAR [?] NDT'),
]

for block, current_parse, context in cross_boundary:
    key = sorted_letters(block)
    matches = anagram_idx.get(key, [])
    if matches:
        print(f"  {current_parse} -> {block} = {matches}")
    # Also +1/-1
    for i in range(len(block)):
        reduced = block[:i] + block[i+1:]
        k = sorted_letters(reduced)
        for m in anagram_idx.get(k, []):
            if len(m) >= 3:
                print(f"  {current_parse} -> {block} = {m} + '{block[i]}' (+1)")
                break
