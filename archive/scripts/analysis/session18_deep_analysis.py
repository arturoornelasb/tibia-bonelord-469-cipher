#!/usr/bin/env python3
"""
Session 18: Deep analysis of garbled blocks.
1. For each recurring garbled block, test if it's an anagram of known words
2. Test code corrections in full context - show what NEW text becomes readable
3. Focus on the NARRATIVE meaning to identify unknown words
"""
import json, os, re
from collections import Counter, defaultdict
from itertools import permutations

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

# MHG and German word lists for anagram matching
# Comprehensive list of German/MHG words relevant to medieval narrative
GERMAN_WORDS = set([
    # Common short words
    'AB', 'AM', 'AN', 'AUS', 'BEI', 'DA', 'DAS', 'DEM', 'DEN', 'DER',
    'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST', 'SO', 'UM',
    'UND', 'VON', 'VOR', 'WO', 'ZU',
    # 3-letter
    'ALS', 'AUF', 'BIS', 'EIN', 'GEH', 'GIB', 'GUT', 'HAT', 'HER',
    'HIN', 'ICH', 'JA', 'MAN', 'NEU', 'NIE', 'NUN', 'NUR', 'ODE',
    'ORT', 'SEI', 'SIE', 'TAG', 'TAT', 'TOD', 'TUN', 'WAR', 'WAS',
    'WER', 'WIE', 'WIR', 'ZUR', 'SUN', 'MIN', 'NOT', 'NUT', 'SAG',
    'OEL', 'SCE', 'OWI', 'GEN', 'INS',
    # 4-letter
    'ABER', 'ALLE', 'AUCH', 'BAND', 'BERG', 'BILD', 'BUCH', 'BURG',
    'DENN', 'DIES', 'DOCH', 'DORT', 'DREI', 'EDEL', 'EINE', 'ENDE',
    'ERDE', 'ERST', 'FACH', 'FAND', 'FERN', 'FEST', 'FORT', 'GANZ',
    'GOTT', 'GOLD', 'GRAB', 'HEIL', 'HEIM', 'HELD', 'HERR', 'HIER',
    'HOCH', 'HUND', 'KAUM', 'KLAR', 'LAND', 'LANG', 'LAUT', 'MEHR',
    'MUSS', 'NACH', 'NAME', 'NEID', 'NOCH', 'NOTH', 'REDE', 'RIEF',
    'RUIN', 'RUNE', 'SAND', 'SAGT', 'SEID', 'SEIN', 'SICH', 'SIND',
    'SOHN', 'SOLL', 'TAGE', 'TEIL', 'TIEF', 'TREU', 'TURM', 'VIEL',
    'VIER', 'WAHR', 'WALD', 'WAND', 'WARD', 'WEIL', 'WELT', 'WENN',
    'WERT', 'WILL', 'WIND', 'WIRD', 'WORT', 'ZEIT', 'ZEHN', 'ZORN',
    'GODE', 'LABT', 'MORT', 'DIGE', 'WEGE', 'NAHE', 'NUTZ', 'ADEL',
    'SANG', 'DINC', 'LANT', 'DASS',
    # 5-letter
    'ALLES', 'ALTEN', 'ALTER', 'ALTES', 'DURCH', 'EINEM', 'EINEN',
    'EINER', 'EINES', 'ERSTE', 'GEGEN', 'GEIST', 'GROSS', 'GRUFT',
    'IMMER', 'KRAFT', 'LICHT', 'MACHT', 'NACHT', 'NICHT', 'NEUEN',
    'ORTEN', 'REDEN', 'REICH', 'RUFEN', 'RUNEN', 'SAGEN', 'SEHEN',
    'SEINE', 'STEHE', 'STEIN', 'STERN', 'TAGEN', 'TREUE', 'UNTER',
    'WESEN', 'WISSE', 'WORTE', 'EHRE', 'GODES', 'HEIME', 'HULDE',
    'KOENIG', 'LEICH', 'MEERE', 'NEIGT', 'REDER', 'TRAUT', 'EDELE',
    'FLUCH', 'ORDEN', 'RACHE', 'SEGEN', 'HERRE', 'DIENST',
    # 6-letter
    'FINDEN', 'GEBEN', 'GEHEN', 'HABEN', 'KOMMEN', 'LEBEN', 'LESEN',
    'NEHMEN', 'SCHAUN', 'STEHEN', 'SUCHEN', 'WIEDER', 'WISSEN', 'WISSET',
    'GEIGET', 'MANIER', 'WISTEN', 'DUNKEL', 'SCHULD',
    # 7-letter
    'RICHTER', 'STEINEN', 'EIGENTUM',
    # Place names
    'SALZBERG', 'WEICHSTEIN', 'SCHARDT', 'GOTTDIENER', 'ORANGENSTRASSE',
    # Additional MHG words
    'VROUWE', 'RITTER', 'KNECHT', 'DIENEST', 'GEBOT', 'SCHWUR',
    'TUGEND', 'MINNE', 'HULDE', 'TRIUWE', 'STUNDE',
    'SUNDE', 'GNADE', 'FRIEDE', 'SEELE', 'ENGEL',
    'TEUFEL', 'HIMMEL', 'HOELLE', 'WUNDER', 'ZEICHEN',
    'STIMME', 'SPIEGEL', 'WAFFEN', 'SCHILD', 'SCHWERT',
    'KRONE', 'THRON', 'TEMPEL', 'KIRCHE', 'KLOSTER',
    'DUNKEL', 'FINSTER', 'BLEICH', 'GRAUSAM', 'HEILIG',
    'EWIG', 'MUEDE', 'STOLZ', 'KUHN', 'WEISE',
    'NORDEN', 'SUEDEN', 'WESTEN', 'OSTEN',
    'DRUIDE', 'PRIESTER', 'MEISTER', 'HERRSCHER',
    'BRUDER', 'SCHWESTER', 'TOCHTER', 'MUTTER', 'VATER',
    'REISE', 'STRASSE', 'BRUECKE', 'INSEL', 'HUEGEL',
    'FELSEN', 'HOEHLE', 'QUELLE', 'FLUSS', 'STROM',
    # More MHG-specific
    'OUCH', 'NIHT', 'HETE', 'SOLDE', 'WOLDE',
    'KUNDE', 'WISTE', 'SAGTE', 'SPRACH', 'GIENC',
    'DUHTE', 'MUOZE', 'MOHTE', 'DORFTE',
    'GERNE', 'SCHIERE', 'VASTE', 'HARTE',
    'LINDE', 'SCHOENE', 'GUOTE', 'REICHE',
    'ELLENDE', 'BERGE', 'LANDE', 'STEINE', 'WALDE',
    'MANTEL', 'HELME', 'SCHILDE', 'SWERTE',
    'HERZEN', 'SINNE', 'MUOTE', 'LIEBE',
    'STIMME', 'REDE', 'LIED', 'GESANG',
    'NACHT', 'MORGEN', 'ABEND', 'WINTER', 'SOMMER',
    # Tibia-relevant terms
    'BONELORD', 'UNTOTEN', 'SKELETT', 'NEKROMANT',
    'DAEMON', 'GEISTER', 'MONSTER', 'DRACHE',
    'MAGIER', 'KRIEGER', 'DIENER', 'WACHTER',
    'ORAKEL', 'RITUAL', 'ZAUBER', 'BESCHWOR',
    'PORTAL', 'KAMMER', 'GRUFT', 'KRYPTA',
    'INSCHRIFT', 'SCHRIFT', 'BUCHSTABE',
    'HELLGATE', 'LIBRARY',
    # Additional relevant words
    'SCHALL', 'LICHT', 'DUNST', 'NEBEL', 'FEUER',
    'WASSER', 'LUFT', 'STUHL', 'TISCH', 'THUER',
    'SCHLOSS', 'MAUER', 'TURM', 'STUFE',
    'RECHT', 'GESETZ', 'GERICHT', 'URTEIL',
    'ERBE', 'SCHULD', 'EHRE', 'MACHT', 'GEWALT',
    'FRIEDE', 'KRIEG', 'SIEG', 'FLUCHT',
    'OPFER', 'GABE', 'SEGEN', 'FLUCH',
    'QUELLE', 'KRAFT', 'WEISHEIT', 'WAHRHEIT',
    'TRAUM', 'SCHLAF', 'WACHE', 'SCHATTEN',
    'GEBEIN', 'LEICHE', 'ASCHE', 'STAUB',
    'BLUT', 'GEBET', 'GESANG', 'KLAGE',
    'GRUND', 'TIEFE', 'HOEHE', 'WEITE',
    'GRENZE', 'SCHWELLE', 'PFAD', 'WEG',
    # Hell/death-related MHG
    'HELLE', 'HELLETOR', 'HELLEN',
    'TOTEN', 'TOTER', 'GEBEIN',
    'VERDAMMT', 'VERFLUCHT', 'VERLOREN',
])

def sorted_letters(s):
    return ''.join(sorted(s))

# Build anagram index
anagram_index = defaultdict(list)
for word in GERMAN_WORDS:
    key = sorted_letters(word)
    anagram_index[key].append(word)

# Recurring garbled blocks to analyze
garbled_blocks = [
    ('UTRUNR', 7, 'ODE {UTRUNR} DEN ENDE REDER KOENIG'),
    ('HIHL', 9, 'AM MIN {HIHL} DIE NDCE'),
    ('NDCE', 9, 'DIE {NDCE} FACH HECHLLT'),
    ('HECHLLT', 5, 'FACH {HECHLLT} ICH OEL'),
    ('NLNDEF', 7, 'DU {NLNDEF} SANG E AM MIN'),
    ('UOD', 8, 'WIR {UOD} IM MIN'),
    ('HED', 12, 'MIN {HED} DEM'),
    ('LGTNELGZ', 2, 'NOT ER {LGTNELGZ} ER'),
    ('TIURIT', 3, 'SER {TIURIT} ORANGENSTRASSE'),
    ('GCHD', 4, 'EIGENTUM ORTEN {GCHD}'),
    ('THARSCR', 2, 'DER {THARSCR} SCE AUS'),
    ('RRNI', 6, 'AB {RRNI} WIR'),
    ('RUI', 8, 'SCHAUN {RUI} IN'),
    ('LABRRNI', 1, 'ER L AB RRNI = LABRRNI?'),
    ('SD', 10, 'AN {SD} IM'),
    ('EO', 12, 'GAR {EO} RUNE'),
    ('NDT', 9, 'ORT {NDT} ER'),
    ('WRLGTNELNRHELUIRUNNHWND', 1, 'STEH {WRLGTNE...HWND} FINDEN'),
    ('UNENITGH', 1, 'KOENIG SALZBERG {UNENITGH}'),
]

print("=" * 80)
print("ANAGRAM ANALYSIS OF GARBLED BLOCKS")
print("=" * 80)

for block, freq, context in garbled_blocks:
    print(f"\n{'─' * 60}")
    print(f"  {block} ({freq}x) | Context: {context}")
    print(f"{'─' * 60}")

    letters = sorted_letters(block)

    # Exact anagram
    exact = anagram_index.get(letters, [])
    if exact:
        print(f"  EXACT ANAGRAM: {', '.join(exact)}")

    # +1 pattern: block has N letters, word has N-1 (drop one letter from block)
    plus1 = []
    for i in range(len(block)):
        reduced = block[:i] + block[i+1:]
        key = sorted_letters(reduced)
        matches = anagram_index.get(key, [])
        for m in matches:
            plus1.append((block[i], m))
    if plus1:
        seen = set()
        print(f"  +1 ANAGRAM (block = word + extra letter):")
        for extra, word in plus1:
            if word not in seen:
                print(f"    {block} = {word} + '{extra}'")
                seen.add(word)

    # -1 pattern: block has N letters, word has N+1 (block is missing one letter)
    minus1 = []
    alphabet = 'ABCDEFGHIKLMNORSTUWZ'
    for pos in range(len(block) + 1):
        for letter in alphabet:
            expanded = block[:pos] + letter + block[pos:]
            key = sorted_letters(expanded)
            matches = anagram_index.get(key, [])
            for m in matches:
                minus1.append((pos, letter, m))
    if minus1:
        seen = set()
        print(f"  -1 ANAGRAM (block is missing a letter):")
        for pos, letter, word in minus1:
            if word not in seen and word != block:
                print(f"    {block} + '{letter}' = {word}")
                seen.add(word)

    if not exact and not plus1 and not minus1:
        print(f"  No anagram matches found")
        # Try 2-word split
        for split in range(2, len(block)-1):
            part1 = block[:split]
            part2 = block[split:]
            k1 = sorted_letters(part1)
            k2 = sorted_letters(part2)
            w1 = anagram_index.get(k1, [])
            w2 = anagram_index.get(k2, [])
            if w1 and w2:
                for a in w1[:3]:
                    for b in w2[:3]:
                        print(f"    Split {split}: {part1}={a} + {part2}={b}")

# ================================================================
# CONTEXT-BASED WORD IDENTIFICATION
# ================================================================
print(f"\n{'=' * 80}")
print("CONTEXT-BASED ANALYSIS: What words make sense in context?")
print("=" * 80)

print("""
KEY RECURRING PHRASE: "IM MIN {HED} DEM {I} DIE URALTE STEINEN"
  Codes: 57-74-45 = H-E-D
  Context requires: a noun or adjective between MIN and DEM
  MHG candidates:
    - HEID = heath, moor (Heide)
    - HET = had (past tense of haben)
    - Actually HED could be valid MHG for 'Heide' (heath/pagan)

  Full reading: "IM MINNE HEID DEM I DIE URALTE STEINEN"
  = "In the love/beloved heath of the [I] ancient stones"

  BUT: what if {HED}{DEM}{I} = HEDDEMI?
  HEDEMI is in our anagram map -> HEIME (homes)!
  The raw text has HEDDEMI (extra D) not HEDEMI.
  This suggests the D in DEM is being double-counted.
  What if the word is actually HEDEM + I?

KEY PHRASE: "ODE {UTRUNR} DEN ENDE REDER KOENIG"
  UTRUNR = codes 44-64-72-61-14-51 = U-T-R-U-N-R
  Rearranged: N-R-R-T-U-U
  Could be: UNTRUE? No...
  Could be: RUNDTUR (round tour)? Letters: D-N-R-R-T-U-U. Too many letters.
  UNTRU? TURNU? NURTR?

  Context: "[at] UTRUNR, the final speech of King Salzberg"
  This is a PLACE NAME where the king gives a speech.

  +1 anagram: UTRUNR = 6 letters. Word is 5:
    UTRUN+R: U-T-R-U-N = UNTUR? TURNU? RUNT?
    Remove first U: TRUNR = N-R-R-T-U
    Remove T: URUNR = N-R-R-U-U
    Remove second U: TRUNR = N-R-R-T-U
    Remove N: UTRUR = R-R-T-U-U
    Remove first R: UTUNR = N-R-T-U-U  = RUUNT? UNTUR?
    Remove second R: UTRUN = N-R-T-U-U = same

KEY PHRASE: "DU {NLNDEF} SANG E AM MIN HIHL"
  NLNDEF = codes 90-96-73-47-09-20 = N-L-N-D-E-F
  Context: "you NLNDEF sang at/in love HIHL"
  NLNDEF should be a VERB (subject DU = you) or a noun
  Letters: D-E-F-L-N-N

  POSSIBLE: If this is a +1 anagram of FINDEN (F-I-N-D-E-N):
    NLNDEF letters: D-E-F-L-N-N
    FINDEN letters: D-E-F-I-N-N
    Difference: L vs I
    Code 96=L. If 96 should be I...
    BUT code 96=L was confirmed by EILCH->LEICH anagram!
    So 96=L is locked.

  What about LNNDEF = anagram of FENDELN (to bargain)?
  FENDELN = D-E-F-L-N-N-E. Has 7 letters, we have 6. Doesn't match.

  What about FLNDEN? Not a word.
  NLNFED? FENNDL? LENDNF?

  None work. This may have a code error.

KEY PHRASE: "SCHAUN {RUI} IN WISTEN"
  RUI = codes 72-61-16 = R-U-I
  Always followed by "IN" (I-N)
  Could be: RUIN + extra I?
  The raw text is: SCHAUN-R-U-I-I-N-W-I-I-S-E-T-N
  RUIIN... the double I suggests code 16 and the next code both give I.
  Code 16=I, and the 'I' at start of 'IN' comes from code 50 or 15...

  Actually "RUIN" = R-U-I-N, and the raw gives R-U-I-I-N.
  The extra I comes from code 16=I appearing, then code 50 or 15 also giving I.

  What if code 16 should be N? Then RUI becomes RUN, and "RUN IN" doesn't help.
  What if the pairing is shifted? SCHAUN + RUIN + ...
  R-U-I-N would need the N, but the N is currently being read as start of IN.

  WAIT - the DP SHOULD match RUIN since it's in the KNOWN set!
  Let me check: the raw chars are R-U-I-I-N. RUIN needs R-U-I-N (4 chars).
  But we have R-U-I-I-N (5 chars). The extra I prevents RUIN from matching!

  Unless... RUIIN has RUIN at positions 0-3 (R-U-I-I) or 0-4 (R-U-I-I-N)?
  RUIN = R-U-I-N. In RUIIN: positions 0-3 = RUII (not RUIN), position 1-4 = UIIN (not RUIN).
  So RUIN doesn't match in RUIIN. The double I breaks it.
""")

# ================================================================
# TEST CANDIDATE CORRECTIONS IN FULL CONTEXT
# ================================================================
print(f"\n{'=' * 80}")
print("TESTING CANDIDATE CODE CORRECTIONS IN CONTEXT")
print("=" * 80)

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

ANAGRAM_MAP = {
    'LABGZERAS': 'SALZBERG', 'SCHWITEIONE': 'WEICHSTEIN',
    'SCHWITEIO': 'WEICHSTEIN', 'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'EDETOTNIURG': 'GOTTDIENER', 'EDETOTNIURGS': 'GOTTDIENERS',
    'ADTHARSC': 'SCHARDT', 'TAUTR': 'TRAUT', 'EILCH': 'LEICH',
    'HEDEMI': 'HEIME', 'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG', 'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE', 'TEIGN': 'NEIGT', 'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER', 'SODGE': 'GODES', 'SNDTEII': 'DIENST',
}

KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR', 'ODE', 'SER', 'GEN', 'INS', 'MIN', 'OEL', 'SCE',
    'ABER', 'ALLE', 'ALLES', 'ALTE', 'ALTEN', 'ALTER', 'AUCH', 'BAND',
    'BERG', 'BURG', 'DENN', 'DIES', 'DOCH', 'DORT', 'DREI', 'DURCH',
    'EINE', 'EINEM', 'EINEN', 'EINER', 'EINES', 'ENDE', 'ERDE', 'ERST',
    'ERSTE', 'FACH', 'FAND', 'FERN', 'FEST', 'FORT', 'GAR', 'GANZ',
    'GEGEN', 'GEIST', 'GOTT', 'GOLD', 'GRAB', 'GROSS', 'GRUFT', 'GUT',
    'HAND', 'HEIM', 'HELD', 'HERR', 'HIER', 'HOCH', 'IMMER',
    'KANN', 'KLAR', 'KRAFT', 'LAND', 'LANG', 'LICHT', 'MACHT',
    'MEHR', 'MUSS', 'NACH', 'NACHT', 'NAHM', 'NAME', 'NEU', 'NEUE',
    'NEUEN', 'NICHT', 'NIE', 'NOCH', 'ODER', 'ORT', 'ORTEN',
    'REDE', 'REDEN', 'REICH', 'RIEF', 'RUIN', 'RUNE', 'RUNEN',
    'SAND', 'SAGT', 'SCHAUN', 'SCHON', 'SEHR', 'SEID', 'SEIN',
    'SEINE', 'SEINEN', 'SEINER', 'SEINEM', 'SEINES',
    'SICH', 'SIND', 'SOHN', 'SOLL', 'STEH', 'STEIN', 'STEINE',
    'STEINEN', 'STERN', 'TAG', 'TAGE', 'TAGEN', 'TAT', 'TEIL',
    'TIEF', 'TOD', 'TURM', 'UNTER', 'URALTE', 'VIEL', 'VIER',
    'WAHR', 'WALD', 'WAND', 'WARD', 'WEIL', 'WELT', 'WENN', 'WERT',
    'WESEN', 'WILL', 'WIND', 'WIRD', 'WORT', 'WORTE', 'ZEIT',
    'ZEHN', 'ZORN', 'FINDEN', 'GEBEN', 'GEHEN', 'HABEN', 'KOMMEN',
    'LEBEN', 'LESEN', 'NEHMEN', 'SAGEN', 'SEHEN', 'STEHEN', 'SUCHEN',
    'WISSEN', 'WISSET', 'RUFEN', 'WIEDER', 'GEIGET', 'BERUCHTIG',
    'BERUCHTIGER', 'MEERE', 'NEIGT', 'WISTEN', 'MANIER', 'HUND',
    'GODE', 'GODES', 'EIGENTUM', 'REDER', 'THENAEUT', 'LABT', 'MORT',
    'DIGE', 'WEGE', 'KOENIGS', 'NAHE', 'NOT', 'NOTH', 'ZUR', 'OWI',
    'ENGE', 'SEIDEN', 'ALTES', 'BIS', 'NUT', 'NUTZ', 'HEIL', 'NEID',
    'TREU', 'TREUE', 'SUN', 'DIENST', 'SANG', 'DINC', 'HULDE',
    'LANT', 'HERRE', 'DIENEST', 'GEBOT', 'SCHWUR', 'ORDEN',
    'RICHTER', 'DUNKEL', 'EHRE', 'EDELE', 'SCHULD', 'SEGEN',
    'FLUCH', 'RACHE', 'KOENIG', 'DASS', 'EDEL', 'ADEL',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME', 'SCHARDT',
])

def build_all_pairs(mapping):
    all_pairs = []
    for bidx, book in enumerate(books):
        if bidx in DIGIT_SPLITS:
            split_pos, digit = DIGIT_SPLITS[bidx]
            book = book[:split_pos] + digit + book[split_pos:]
        off = get_offset(book)
        pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
        all_pairs.extend(pairs)
    return all_pairs

def dp_coverage(text, known=KNOWN):
    n = len(text)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            if text[start:i] in known:
                score = dp[start] + wlen
                if score > dp[i]:
                    dp[i] = score
    return dp[n]

def full_text(mapping, amap=ANAGRAM_MAP):
    all_pairs = build_all_pairs(mapping)
    text = ''.join(mapping.get(p, '?') for p in all_pairs)
    for ana in sorted(amap.keys(), key=len, reverse=True):
        text = text.replace(ana, amap[ana])
    return text

# Current baseline
current = dict(v7)
baseline_text = full_text(current)
baseline_total = sum(1 for c in baseline_text if c != '?')
baseline_cov = dp_coverage(baseline_text)
print(f"\nBaseline: {baseline_cov}/{baseline_total} = {baseline_cov/baseline_total*100:.1f}%")

# Test each candidate correction and show WHAT CHANGES in the text
candidates = [
    ('90', 'N', 'O', '+8 from iterative'),
    ('20', 'F', 'N', '+7 from iterative'),
    ('02', 'D', 'B', '+4 from iterative'),
    ('94', 'H', 'I', 'garbled HIHL->HIIL, HECHLLT->HECILLT'),
    ('94', 'H', 'E', 'garbled HIHL->HIEL, HECHLLT->HECELTT??'),
    ('94', 'H', 'A', 'garbled HIHL->HIAL, HECHLLT->HECALLT'),
]

for code, old_letter, new_letter, reason in candidates:
    print(f"\n{'─' * 60}")
    print(f"  Testing: code {code}: {old_letter} -> {new_letter} ({reason})")
    print(f"{'─' * 60}")

    mod = dict(current)
    mod[code] = new_letter
    mod_text = full_text(mod)
    mod_total = sum(1 for c in mod_text if c != '?')
    mod_cov = dp_coverage(mod_text)
    change = mod_cov - baseline_cov
    print(f"  Coverage: {mod_cov}/{mod_total} = {mod_cov/mod_total*100:.1f}% (change: {change:+d})")

    # Find text differences
    # Show snippets where the text changed and the new text is readable
    diffs = []
    for i in range(len(baseline_text)):
        if i < len(mod_text) and baseline_text[i] != mod_text[i]:
            # Get context around the change
            ctx_start = max(0, i-15)
            ctx_end = min(len(mod_text), i+16)
            old_ctx = baseline_text[ctx_start:ctx_end]
            new_ctx = mod_text[ctx_start:ctx_end]
            pos_in_ctx = i - ctx_start
            diffs.append((i, old_ctx, new_ctx, pos_in_ctx))

    # Show unique diff contexts
    shown = set()
    for i, old_ctx, new_ctx, pos in diffs[:20]:
        key = new_ctx
        if key not in shown:
            shown.add(key)
            print(f"    pos {i:4d}: ...{old_ctx}... -> ...{new_ctx}...")

    # Check which anagrams break
    old_raw = ''.join(current.get(p, '?') for p in build_all_pairs(current))
    new_raw = ''.join(mod.get(p, '?') for p in build_all_pairs(mod))
    broken = []
    for ana in ANAGRAM_MAP:
        if ana in old_raw and ana not in new_raw:
            broken.append(f"{ana}->{ANAGRAM_MAP[ana]}")
    if broken:
        print(f"  BREAKS ANAGRAMS: {', '.join(broken)}")
    else:
        print(f"  No anagrams broken")

# ================================================================
# NEW WORD DISCOVERY
# ================================================================
print(f"\n{'=' * 80}")
print("POTENTIAL NEW WORDS TO ADD TO KNOWN SET")
print("=" * 80)

# Scan the decoded text for 3-5 letter sequences between known words
# that could be valid German words
text = baseline_text

# Simple DP to find gaps
n = len(text)
dp = [0] * (n + 1)
bt = [None] * (n + 1)
for i in range(1, n + 1):
    dp[i] = dp[i-1]
    for wlen in range(2, min(i, 20) + 1):
        start = i - wlen
        if text[start:i] in KNOWN:
            score = dp[start] + wlen
            if score > dp[i]:
                dp[i] = score
                bt[i] = (start, text[start:i])

# Extract unmatched segments
segments = []
i = n
matched = set()
while i > 0:
    if bt[i] is not None:
        start, word = bt[i]
        for j in range(start, i):
            matched.add(j)
        i = start
    else:
        i -= 1

# Find unmatched runs
current_gap = []
gap_list = []
for i in range(n):
    if i not in matched and text[i] != '?':
        current_gap.append(text[i])
    else:
        if current_gap:
            gap_text = ''.join(current_gap)
            gap_list.append((i - len(current_gap), gap_text))
            current_gap = []
if current_gap:
    gap_text = ''.join(current_gap)
    gap_list.append((n - len(current_gap), gap_text))

# Count gap frequencies
gap_counter = Counter(g[1] for g in gap_list)
print("\nMost frequent unmatched text segments (potential words):")
for gap, count in gap_counter.most_common(40):
    if len(gap) >= 2 and count >= 2:
        # Check if it could be a German word
        notes = []
        key = sorted_letters(gap)
        anagram_matches = anagram_index.get(key, [])
        if anagram_matches:
            notes.append(f"anagram of: {', '.join(anagram_matches[:3])}")
        print(f"  {count:3d}x '{gap}' (len={len(gap)}){' - ' + '; '.join(notes) if notes else ''}")
