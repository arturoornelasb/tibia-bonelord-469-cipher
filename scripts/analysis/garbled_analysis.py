#!/usr/bin/env python3
"""
Systematic analysis of garbled (unresolved) segments in the decoded bonelord text.
For each garbled block, try: exact anagrams, +1/-1 anagrams against German/MHG words.
Also look at context to constrain possibilities.
"""
import json, os, re
from collections import Counter
from itertools import combinations

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)

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

# Decode all books
decoded_books = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    text = ''.join(v7.get(p, '?') for p in pairs)
    decoded_books.append(text)

# Concatenate with anagram resolution
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
    'AUIENMR': 'MANIER', 'AODGE': 'GODE',
}

all_text = ''.join(decoded_books)
resolved = all_text
for ana in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved = resolved.replace(ana, ANAGRAM_MAP[ana])

# DP segmentation (simplified KNOWN set for identifying garbled blocks)
KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR',
    'ABER', 'ALLE', 'ALLES', 'ALTE', 'ALTEN', 'ALTER', 'AUCH', 'BAND',
    'BERG', 'BURG', 'DENN', 'DIES', 'DIESE', 'DIESER', 'DIESEN', 'DIESEM',
    'DOCH', 'DORT', 'DREI', 'DURCH', 'EINE', 'EINEM', 'EINEN', 'EINER',
    'EINES', 'ENDE', 'ERDE', 'ERST', 'ERSTE', 'FACH', 'FAND', 'FERN',
    'FEST', 'FORT', 'GAR', 'GANZ', 'GEGEN', 'GEIST', 'GOTT', 'GOLD',
    'GRAB', 'GROSS', 'GRUFT', 'GUT', 'HAND', 'HEIM', 'HELD', 'HERR',
    'HIER', 'HOCH', 'IMMER', 'KANN', 'KLAR', 'KRAFT', 'LAND', 'LANG',
    'LICHT', 'MACHT', 'MEHR', 'MUSS', 'NACH', 'NACHT', 'NAHM', 'NAME',
    'NEU', 'NEUE', 'NEUEN', 'NICHT', 'NIE', 'NOCH', 'ODER', 'ORT', 'ORTEN',
    'REDE', 'REDEN', 'REICH', 'RIEF', 'RUIN', 'RUNE', 'RUNEN',
    'SAND', 'SAGT', 'SCHAUN', 'SCHON', 'SEHR', 'SEID', 'SEIN',
    'SEINE', 'SEINEN', 'SEINER', 'SEINEM', 'SEINES',
    'SICH', 'SIND', 'SOHN', 'SOLL', 'STEH', 'STEIN', 'STEINE',
    'STEINEN', 'STERN', 'TAG', 'TAGE', 'TAGEN', 'TAT', 'TEIL',
    'TIEF', 'TOD', 'TURM', 'UNTER', 'URALTE', 'VIEL', 'VIER',
    'WAHR', 'WALD', 'WAND', 'WARD', 'WEIL', 'WELT', 'WENN', 'WERT',
    'WESEN', 'WILL', 'WIND', 'WIRD', 'WORT', 'WORTE', 'ZEIT', 'ZEHN', 'ZORN',
    'FINDEN', 'GEBEN', 'GEHEN', 'HABEN', 'KOMMEN', 'LEBEN', 'LESEN',
    'NEHMEN', 'SAGEN', 'SEHEN', 'STEHEN', 'SUCHEN', 'WISSEN', 'WISSET',
    'RUFEN', 'WIEDER',
    'OEL', 'SCE', 'MINNE', 'MIN', 'ODE', 'SER', 'GEN', 'INS',
    'GEIGET', 'BERUCHTIG', 'BERUCHTIGER', 'MEERE', 'NEIGT', 'WISTEN',
    'MANIER', 'HUND', 'GODE', 'EIGENTUM', 'REDER', 'THENAEUT', 'LABT',
    'MORT', 'DIGE', 'WEGE', 'KOENIGS', 'NAHE', 'NOT', 'NOTH', 'ZUR',
    'OWI', 'ENGE', 'SEIDEN', 'ALTES', 'DENN', 'BIS', 'NIE', 'NUT', 'NUTZ',
    'HEIL', 'NEID', 'TREU', 'TREUE',
    'KOENIG', 'DASS', 'EDEL', 'ADEL',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME', 'SCHARDT',
])

def dp_segment(text):
    n = len(text)
    dp = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], None)
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if cand in KNOWN:
                score = dp[start][0] + wlen
                if score > dp[i][0]:
                    dp[i] = (score, (start, cand))
    tokens = []
    i = n
    while i > 0:
        if dp[i][1] is not None:
            start, word = dp[i][1]
            tokens.append(('W', word))
            i = start
        else:
            tokens.append(('C', text[i-1]))
            i -= 1
    tokens.reverse()
    result = []
    for kind, val in tokens:
        if kind == 'W':
            result.append(val)
        else:
            if result and result[-1].startswith('{'):
                result[-1] = result[-1][:-1] + val + '}'
            else:
                result.append('{' + val + '}')
    return result, dp[n][0]

tokens, _ = dp_segment(resolved)

# Extract all garbled blocks and count occurrences
garbled = Counter()
garbled_contexts = {}
for i, tok in enumerate(tokens):
    if tok.startswith('{'):
        block = tok[1:-1]
        if len(block) >= 3:  # Skip single/double char noise
            garbled[block] += 1
            # Get context (2 tokens before and after)
            ctx_before = ' '.join(tokens[max(0,i-2):i])
            ctx_after = ' '.join(tokens[i+1:min(len(tokens),i+3)])
            if block not in garbled_contexts:
                garbled_contexts[block] = []
            garbled_contexts[block].append(f"...{ctx_before} [{block}] {ctx_after}...")

print("=" * 70)
print("GARBLED BLOCKS (3+ chars, sorted by frequency)")
print("=" * 70)
for block, count in garbled.most_common(50):
    print(f"\n  {block} ({count}x) - letters: {sorted(Counter(block).items())}")
    for ctx in garbled_contexts[block][:2]:
        print(f"    Context: {ctx}")

# ============================================================
# German word list for anagram checking
# ============================================================
# Extended word list for anagram checking - common German/MHG words
GERMAN_WORDS = set([
    # Common nouns
    'ACHT', 'ANGST', 'ARBEIT', 'BAUER', 'BLUT', 'BOTE', 'BRUDER',
    'DIENST', 'DING', 'EHRE', 'FEIND', 'FEUER', 'FISCH', 'FLUCH',
    'FLUCHT', 'FREUND', 'FRIEDE', 'FUERST', 'GARTEN', 'GEBIET',
    'GEBOT', 'GEFAHR', 'GEHEIMNIS', 'GEMAHL', 'GERICHT', 'GESCHLECHT',
    'GESETZ', 'GEWALT', 'GLAUBE', 'GLUECK', 'GRAB', 'GRAF', 'GRENZE',
    'GRUND', 'HAFEN', 'HAUS', 'HEILIG', 'HERRSCHER', 'HERZ', 'HIMMEL',
    'HUETER', 'INSEL', 'JUNGFRAU', 'KAMPF', 'KIRCHE', 'KLOSTER',
    'KNECHT', 'KOENIG', 'KOENIGIN', 'KOENIGLICH', 'KOENIGREICH',
    'KREUZ', 'KRIEG', 'KRIEGER', 'KRONE', 'LEIB', 'LEUTE',
    'MACHT', 'MEISTER', 'MOENCH', 'MORD', 'MUTTER', 'NORDEN',
    'OSTEN', 'PRIESTER', 'RACHE', 'RITTER', 'SCHLACHT', 'SCHLOSS',
    'SCHMERZ', 'SCHRIFT', 'SCHULD', 'SCHUTZ', 'SCHWERT', 'SEELE',
    'SIEG', 'SITTE', 'SOHN', 'STRAFE', 'STRASSE', 'SUEDEN',
    'TEMPEL', 'THRON', 'TREUE', 'TUGEND', 'TURM', 'VATER',
    'VOLK', 'WAFFE', 'WAHRHEIT', 'WESTEN', 'ZEICHEN', 'ZORN',
    # MHG words
    'BURC', 'DINC', 'HERRE', 'MINNE', 'MUOT', 'RECKE', 'STRIT',
    'SWAERE', 'TRIUWE', 'TUGENT', 'VROUWE', 'WALT', 'WUNDER',
    'RITTER', 'DIENEST', 'MEIDE', 'MAGD', 'HULDE', 'ORDEN',
    'GEIST', 'DUNKEL', 'DUNKELHEIT', 'FINSTER', 'FINSTERNISS',
    'HEILIG', 'HEILIGTUM', 'ALTAR', 'INSCHRIFT', 'SCHRIFT',
    'CHRONIK', 'SAGE', 'LEGENDE', 'MYTHOS', 'ORAKEL',
    'SCHREIN', 'GRUFT', 'KAMMER', 'KERKER', 'TURM',
    # Verbs
    'STERBEN', 'HERRSCHEN', 'KAEMPFEN', 'GLAUBEN', 'BETEN',
    'FLUCHEN', 'RICHTEN', 'STRAFEN', 'SCHUETZEN', 'DIENEN',
    'KENNEN', 'DULDEN', 'ERBEN', 'LEHREN', 'LERNEN',
    'STUERZEN', 'EROBERN', 'VERNICHTEN', 'ZERSTOEREN',
    # Adjectives
    'DUNKEL', 'HEILIG', 'EDEL', 'TREU', 'TAPFER', 'FROMM',
    'GERECHT', 'FINSTER', 'MAECHTIG', 'GRAUSAM', 'EINSAM',
    # Place/geography
    'HALLE', 'BRUECKE', 'GRABEN', 'MAUER', 'BURG', 'SCHLOSS',
    'KAPELLE', 'KLOSTER', 'FRIEDHOF', 'QUELLE', 'HOEHLE',
    # More nouns
    'NACHRICHT', 'BOTSCHAFT', 'ZEUGNIS', 'BEWEIS', 'FLUCH',
    'SEGEN', 'SCHWUR', 'BUND', 'VERRAT', 'UNTREU', 'UNTREUE',
    'SCHULDEN', 'SCHULDIG', 'UNSCHULD',
    # Specifically for our cipher context
    'TRACHT', 'SCHLECHT', 'RECHT', 'NECHSTE', 'NAECHSTE',
    'RICHTER', 'DICHTER', 'HENKER', 'RUINE', 'RUINEN',
    'SCHATZ', 'KELCH', 'THRONHALL', 'NISCHE', 'GRABMAL',
    'DENKMAL', 'STANDBILD', 'INSCHRIFT',
    'LICHT', 'NACHT', 'MACHT', 'WACHT', 'PRACHT', 'RACHT',
    'ANDACHT', 'EINTRACHT', 'SCHLACHT',
    'LEHR', 'KEHR', 'MEHR', 'WEHR', 'ZEHR', 'SEHR',
    'HEER', 'HERR', 'STERN', 'HERRN',
    # Common word endings
    'HEIT', 'KEIT', 'SCHAFT', 'TUNG', 'LING', 'LICH',
    # Numbers
    'EINS', 'ZWEI', 'DREI', 'VIER', 'FUENF', 'SECHS', 'SIEBEN',
    'ACHT', 'NEUN', 'ZEHN', 'ELF', 'ZWOELF',
    'HUNDERT', 'TAUSEND',
    # Tibia-specific proper nouns (anagram candidates)
    'MINTWALLIN', 'THAIS', 'KAZORDOON', 'CARLIN', 'EDRON',
    'VENORE', 'ANKRAHMUN', 'DARASHIA', 'DREFIA', 'MINTWALLIN',
    'FERUMBRAS', 'EXCALIBUG', 'BANOR', 'ZATHROTH', 'UMAN',
    'FARDOS', 'URGITH', 'TIBIASULA', 'BORETH', 'CRUNOR',
    'SUON', 'KIROK', 'THAIAN', 'HELLGATE',
    # More possible matches for our blocks
    'TURNIER', 'TURNIERE', 'RICHTIG', 'ZURUECK',
    'LETZTE', 'LETZT', 'GERICHT', 'BERICHT', 'ERRICHT',
    'ENTDECKT', 'ENTRICHT', 'VERNICHTET',
    'UNRECHT', 'ZURECHT', 'GERECHT',
    'SPRUCH', 'EINSPRUCH', 'ANSPRUCH', 'ZUSPRUCH',
    'VERTUN', 'NURTUN', 'RUNDTUR', 'RUNDTURM',
    # For UTRUNR specifically
    'UNRUHT', 'UNTREU', 'UNTREUE', 'UNRUH', 'UNRECHT',
    'NURTUR', 'RUNTUR', 'TURNUR',
    # For LGTNELGZ specifically
    'GLANZTEL', 'LANGSTELZ', 'GLANZTEIL',
    # For HECHLLT
    'SCHLECHT', 'HELLTCH', 'THELLCH',
    # For NDCE
    'DENC', 'CEND',
    # For HIHL
    'HILL', 'HEIL',
    # More MHG
    'SWERT', 'STRIC', 'BURC', 'KUNIC', 'RICHE',
    'LANT', 'LIUT', 'VUOZ', 'ANDER', 'NIUWE',
    'NIHT', 'WOLD', 'MUOZE', 'HEIZE', 'ZIERE',
    'SNELL', 'ELLENDE', 'ELLENTHAFT', 'EDELE',
])

def is_anagram(s1, s2):
    return sorted(s1) == sorted(s2)

def check_plus_one(block, words):
    """Check if block is an anagram of word + 1 extra letter"""
    matches = []
    for word in words:
        if len(word) == len(block) - 1:
            bc = Counter(block)
            wc = Counter(word)
            diff = bc - wc
            if sum(diff.values()) == 1:
                extra = list(diff.elements())[0]
                matches.append((word, extra))
    return matches

def check_minus_one(block, words):
    """Check if block is an anagram of word - 1 letter (block is missing one)"""
    matches = []
    for word in words:
        if len(word) == len(block) + 1:
            bc = Counter(block)
            wc = Counter(word)
            diff = wc - bc
            if sum(diff.values()) == 1:
                missing = list(diff.elements())[0]
                matches.append((word, missing))
    return matches

print(f"\n{'='*70}")
print("ANAGRAM ANALYSIS OF GARBLED BLOCKS")
print(f"{'='*70}")

# Focus on blocks that appear 2+ times or are 4-8 chars (likely words)
target_blocks = set()
for block, count in garbled.most_common():
    if count >= 2 or (3 <= len(block) <= 10):
        target_blocks.add(block)

# Also add specifically known unresolved blocks
target_blocks.update(['UTRUNR', 'LGTNELGZ', 'TIURIT', 'RRNI', 'HECHLLT',
                       'NDCE', 'HIHL', 'GCHDE', 'HWND', 'LABRRNI',
                       'UOD', 'UNENITGH', 'NTEATTUIGAA'])

for block in sorted(target_blocks, key=lambda b: (-garbled.get(b, 0), len(b))):
    if len(block) < 3 or len(block) > 15:
        continue

    count = garbled.get(block, 0)
    exact = [w for w in GERMAN_WORDS if is_anagram(block, w)]
    plus1 = check_plus_one(block, GERMAN_WORDS)
    minus1 = check_minus_one(block, GERMAN_WORDS)

    if exact or plus1 or minus1:
        print(f"\n  {block} ({count}x, {len(block)} chars):")
        if exact:
            print(f"    EXACT anagram: {exact}")
        if plus1:
            print(f"    +1 anagram: {[(w, f'+{e}') for w, e in plus1]}")
        if minus1:
            print(f"    -1 anagram (missing letter): {[(w, f'-{m}') for w, m in minus1]}")

# ============================================================
# Check UTRUNR specifically with all 6-letter German words
# ============================================================
print(f"\n{'='*70}")
print("DEEP ANALYSIS: UTRUNR (U,T,R,U,N,R)")
print(f"{'='*70}")
print(f"Letters: {sorted(Counter('UTRUNR').items())}")
print(f"Always in context: 'ODE UTRUNR DEN ENDE REDER KOENIG'")
print(f"This is: 'Or/And UTRUNR the end/final speech/er King'")
print(f"Likely a place name or title.")
print()

# Could UTRUNR be a +1 anagram?
utrunr_letters = Counter('UTRUNR')
print("Testing +1 (remove one letter from UTRUNR and check 5-letter German words):")
for remove_letter in set('UTRUNR'):
    remaining = utrunr_letters.copy()
    remaining[remove_letter] -= 1
    if remaining[remove_letter] == 0:
        del remaining[remove_letter]
    remaining_str = ''.join(sorted(remaining.elements()))
    # Check common 5-letter German words
    five_letter = [w for w in GERMAN_WORDS if len(w) == 5 and sorted(w) == sorted(remaining_str)]
    if five_letter:
        print(f"  Remove {remove_letter}: {remaining_str} → {five_letter}")

# What if UTRUNR is part of a compound? Like UN+TRUNR or UT+RUNR?
print("\nCompound analysis:")
print(f"  UN + TRUNR: 'UN' (un-) + TRUNR (anagram of TRUNK? = drink)")
trunk_letters = sorted('TRUNR')
trunk_match = sorted('TRUNK')
print(f"    TRUNR sorted: {trunk_letters}, TRUNK sorted: {trunk_match}")
if trunk_letters == trunk_match:
    print(f"    *** MATCH: UTRUNR = U + TRUNK (drink/potion)!")
else:
    # Check: TRUNR has T,R,U,N,R but TRUNK has K,N,R,T,U
    print(f"    No match (TRUNR has R×2, TRUNK has K×1)")

# ============================================================
# Check LGTNELGZ specifically
# ============================================================
print(f"\n{'='*70}")
print("DEEP ANALYSIS: LGTNELGZ (L,G,T,N,E,L,G,Z)")
print(f"{'='*70}")
lgtnelgz = Counter('LGTNELGZ')
print(f"Letters: {sorted(lgtnelgz.items())}")
print(f"Context: 'NOT ER LGTNELGZ ER A SER TIURIT ORANGENSTRASSE'")
print(f"This is: 'need/distress he LGTNELGZ he [a] very TIURIT Orange-Street'")

# +1 analysis
print("\nTesting +1 (remove one letter):")
for remove_letter in set('LGTNELGZ'):
    remaining = lgtnelgz.copy()
    remaining[remove_letter] -= 1
    if remaining[remove_letter] == 0:
        del remaining[remove_letter]
    remaining_str = ''.join(sorted(remaining.elements()))
    seven_letter = [w for w in GERMAN_WORDS if len(w) == 7 and sorted(w) == sorted(remaining_str)]
    if seven_letter:
        print(f"  Remove {remove_letter}: → {seven_letter}")

# ============================================================
# HECHLLT deep analysis
# ============================================================
print(f"\n{'='*70}")
print("DEEP ANALYSIS: HECHLLT (H,E,C,H,L,L,T)")
print(f"{'='*70}")
hechllt = Counter('HECHLLT')
print(f"Letters: {sorted(hechllt.items())}")
print(f"Context: 'DIE NDCE FACH HECHLLT ICH OEL SO DEN HIER'")

# Could HECHLLT be SCHLECHT with mapping errors?
# SCHLECHT = S,C,H,L,E,C,H,T (8 letters, needs S and 2nd C)
# HECHLLT has H,E,C,H,L,L,T (7 letters)
print(f"\nCompare to SCHLECHT: S,C,H,L,E,C,H,T")
print(f"  HECHLLT has:  {sorted(hechllt.items())}")
print(f"  SCHLECHT has: {sorted(Counter('SCHLECHT').items())}")
diff1 = Counter('SCHLECHT') - hechllt
diff2 = hechllt - Counter('SCHLECHT')
print(f"  SCHLECHT needs extra: {dict(diff1)}")
print(f"  HECHLLT has extra:    {dict(diff2)}")

# What about HELLICHT (bright)?
print(f"\nCompare to HELLICHT (bright light):")
hellicht = Counter('HELLICHT')
print(f"  HELLICHT: {sorted(hellicht.items())}")
diff1 = hellicht - hechllt
diff2 = hechllt - hellicht
print(f"  HELLICHT needs extra: {dict(diff1)}")
print(f"  HECHLLT has extra:    {dict(diff2)}")

# ============================================================
# TIURIT deep analysis
# ============================================================
print(f"\n{'='*70}")
print("DEEP ANALYSIS: TIURIT (T,I,U,R,I,T)")
print(f"{'='*70}")
tiurit = Counter('TIURIT')
print(f"Letters: {sorted(tiurit.items())}")
print(f"Context: 'SER TIURIT ORANGENSTRASSE'")
print(f"This is: 'very TIURIT Orange-Street'")

# Could be RITTUI? TRIUIT?
# +1 analysis
print("\nTesting +1 (remove one letter from TIURIT):")
for remove_letter in set('TIURIT'):
    remaining = tiurit.copy()
    remaining[remove_letter] -= 1
    if remaining[remove_letter] == 0:
        del remaining[remove_letter]
    remaining_str = ''.join(sorted(remaining.elements()))
    five_letter = [w for w in GERMAN_WORDS if len(w) == 5 and sorted(w) == sorted(remaining_str)]
    if five_letter:
        print(f"  Remove {remove_letter}: → {five_letter}")

# Exact 6-letter anagram
six_letter = [w for w in GERMAN_WORDS if len(w) == 6 and is_anagram(w, 'TIURIT')]
print(f"\nExact 6-letter anagrams: {six_letter}")

# What about RITTUI -> TURM+II? Or RITUAL-AL+I?
# RITUS (Latin, used in German) = R,I,T,U,S (5 letters - no S in TIURIT)
# TRIBUT = T,R,I,B,U,T (6 letters - has B, TIURIT has I instead)
print(f"\nCompare TRIBUT: {sorted(Counter('TRIBUT').items())}")
print(f"         TIURIT: {sorted(tiurit.items())}")

# ============================================================
# Look for the phrase "LABRRNI" or "L AB RRNI"
# ============================================================
print(f"\n{'='*70}")
print("DEEP ANALYSIS: The AB/RRNI pattern")
print(f"{'='*70}")
# In context: "ER {L} AB {RRNI} WIR {UOD} IM MIN"
# What if the boundaries are wrong? What if it's LABRRNI (7 chars)?
labrrni = Counter('LABRRNI')
print(f"LABRRNI letters: {sorted(labrrni.items())}")
print(f"Context: 'ER LABRRNI WIR UOD IM MINNE'")
print(f"= 'He LABRRNI we [?] in love/courtly-love'")

# +1 analysis for 6-letter word
print("\nTesting if LABRRNI is a 6-letter word + 1:")
for remove_letter in set('LABRRNI'):
    remaining = labrrni.copy()
    remaining[remove_letter] -= 1
    if remaining[remove_letter] == 0:
        del remaining[remove_letter]
    remaining_str = ''.join(sorted(remaining.elements()))
    matches = [w for w in GERMAN_WORDS if len(w) == 6 and sorted(w) == sorted(remaining_str)]
    if matches:
        print(f"  Remove {remove_letter}: → {matches}")

# What about BERLIN+R?
berlin = Counter('BERLIN')
print(f"\nBERLIN: {sorted(berlin.items())}")
print(f"LABRRNI: {sorted(labrrni.items())}")
diff = labrrni - berlin
print(f"Extra in LABRRNI: {dict(diff)} (need E→A and extra R)")

# ============================================================
# NPC "mathemagic" connection: check for mathematical ops
# ============================================================
print(f"\n{'='*70}")
print("MATHEMATICAL PROPERTIES OF 469 AND MAPPING")
print(f"{'='*70}")
print(f"469 = 7 × 67 (both prime)")
print(f"486486 (bonelord name) = 2 × 3^5 × 7 × 11 × 13")
print(f"486486 / 7 = {486486 / 7}")
print(f"486486 / 469 = {486486 / 469:.4f}")
print(f"486486 mod 469 = {486486 % 469}")
print(f"486486 mod 100 = {486486 % 100}")

# Check if 469 appears anywhere in the books
for bidx, book in enumerate(books):
    pos = book.find('469')
    if pos >= 0:
        print(f"\n'469' found in Book {bidx} at position {pos}: ...{book[max(0,pos-5):pos+8]}...")

# ============================================================
# Check code pairs that map to same letter - mathematical relationship?
# ============================================================
print(f"\n{'='*70}")
print("HOMOPHONIC CODE GROUPINGS")
print(f"{'='*70}")
letter_codes = {}
for code, letter in v7.items():
    if letter not in letter_codes:
        letter_codes[letter] = []
    letter_codes[letter].append(int(code))

for letter in sorted(letter_codes.keys()):
    codes = sorted(letter_codes[letter])
    if len(codes) > 1:
        diffs = [codes[i+1] - codes[i] for i in range(len(codes)-1)]
        print(f"  {letter}: codes={codes}, diffs={diffs}")

# Check: do codes for same letter have common mod values?
print(f"\nMod-7 analysis (469 = 7 × 67):")
for letter in sorted(letter_codes.keys()):
    codes = sorted(letter_codes[letter])
    mods = [c % 7 for c in codes]
    print(f"  {letter}: codes mod 7 = {mods}")

print(f"\nMod-67 analysis:")
for letter in sorted(letter_codes.keys()):
    codes = sorted(letter_codes[letter])
    mods = [c % 67 for c in codes]
    print(f"  {letter}: codes mod 67 = {mods}")
