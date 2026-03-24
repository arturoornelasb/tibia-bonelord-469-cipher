#!/usr/bin/env python3
"""
Anagram Resolution
===================
Key insight: CipSoft uses TWO anagram patterns:
  1. Proper nouns (place names): ANAGRAM + 1 extra letter
     LABGZERAS = SALZBERG + A
     SCHWITEIONE = WEICHSTEIN + O
     AUNRSONGETRASES = ORANGENSTRASSE + U
  2. Common words: EXACT anagram (no extra letter)
     Hypothesis: TAUTR = TRAUT, EILCH = LEICH

Test ALL unresolved words against comprehensive German+MHG dictionaries.
"""

import json, os
from collections import Counter
from itertools import permutations

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

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

decoded_books = []
for bpairs in book_pairs:
    text = ''.join(v7.get(p, '?') for p in bpairs)
    decoded_books.append(text)

# ============================================================
# COMPREHENSIVE GERMAN + MHG WORD LIST
# ============================================================
# This list focuses on words that could plausibly appear in a
# medieval German text about kings, ruins, stones, and quests.

WORD_LIST = [
    # Common short words
    'AB', 'AN', 'AUF', 'AUS', 'BEI', 'DA', 'DU', 'ER', 'ES', 'IN',
    'JA', 'OB', 'SO', 'UM', 'WO', 'ZU',
    # 3-letter
    'ALT', 'ART', 'DAS', 'DEM', 'DEN', 'DER', 'DIE', 'DIS', 'EIN',
    'END', 'FEL', 'GAR', 'GEH', 'GUT', 'HAT', 'HER', 'HIN', 'ICH',
    'IHR', 'IST', 'MAN', 'MAL', 'MUT', 'NEU', 'NIE', 'NUN', 'NUR',
    'ODE', 'ORT', 'RAT', 'ROT', 'RUF', 'SAG', 'SEI', 'TAG', 'TAT',
    'TOD', 'TOT', 'TUN', 'UND', 'VOR', 'WAR', 'WAS', 'WEG', 'WER',
    'WIE', 'WIR',
    # 4-letter
    'ABER', 'ACHT', 'ALLE', 'ALSO', 'AUCH', 'BAND', 'BAUM', 'BERG',
    'BILD', 'BLUT', 'BOTE', 'BUCH', 'BURG', 'DANK', 'DANN', 'DENN',
    'DIES', 'DOCH', 'DORF', 'DORT', 'DREI', 'EDLE', 'EHRE', 'EICH',
    'EINE', 'ENDE', 'ERDE', 'FACH', 'FAND', 'FERN', 'FEST', 'FIEL',
    'FREI', 'GANZ', 'GEBT', 'GELD', 'GERN', 'GING', 'GOLD', 'GOTT',
    'GRAB', 'GRAL', 'HEIL', 'HEIM', 'HELD', 'HERR', 'HIER', 'HOCH',
    'HOLZ', 'HUND', 'INNS', 'KALT', 'KANN', 'KEIN', 'KIND', 'KLAR',
    'KOPF', 'LAND', 'LANG', 'LAUT', 'LEER', 'LEIB', 'LEID', 'LIEB',
    'LIED', 'LUFT', 'MAHL', 'MEHR', 'MOND', 'MUSS', 'NACH', 'NAHM',
    'NAME', 'NOCH', 'OBEN', 'ODER', 'PAKT', 'REDE', 'REIN', 'RIEF',
    'RING', 'RUIN', 'RUNE', 'RUHE', 'RUHM', 'RUND', 'SAGT', 'SAND',
    'SANG', 'SEID', 'SEIN', 'SEHR', 'SICH', 'SIND', 'SOHN', 'SOLL',
    'TAGE', 'HAUS', 'TEIL', 'TIEF', 'TURM', 'VIEL', 'VIER', 'VOLK',
    'VOLL', 'WAHL', 'WAHR', 'WALD', 'WAND', 'WARD', 'WEIL', 'WEIT',
    'WELT', 'WENN', 'WERK', 'WERT', 'WILL', 'WIND', 'WIRD', 'WOHL',
    'WORT', 'ZAHL', 'ZEHN', 'ZEIT', 'ZORN', 'ZWEI',
    # 5-letter
    'ABEND', 'ADLER', 'ALLES', 'ALTER', 'ANGST', 'ARBEI', 'BAUEN',
    'BETEN', 'BLICK', 'BREIT', 'DARIN', 'DURCH', 'DUNKE', 'EDLER',
    'EIGEN', 'ENGEL', 'ERNST', 'ERSTE', 'EWIGE', 'FEIND', 'FEUER',
    'FLUCH', 'FLUSS', 'FRAGE', 'FRIEE', 'FRONT', 'GEGEN', 'GEIST',
    'GLAUB', 'GLANZ', 'GLEIC', 'GNADE', 'GOLDE', 'GRENZ', 'GROSS',
    'GRUBE', 'GRUFT', 'GRUND', 'HABEN', 'HALTEN', 'HEIME', 'KRAFT',
    'LICHT', 'LINIE', 'MAUER', 'NACHT', 'NEUEN', 'NICHT', 'OPFER',
    'ORTE', 'PFEIL', 'PLATZ', 'PREIS', 'RECHT', 'REDEN', 'REISE',
    'RUFEN', 'RUNEN', 'SCHON', 'SEGEN', 'SEINE', 'STAMM', 'STEIN',
    'STERN', 'STOLZ', 'SUCHE', 'TATEN', 'TIEFE', 'TRAGE', 'TRAUT',
    'TREUE', 'UNTER', 'VATER', 'VIELE', 'WACHE', 'WAFFE', 'WAGEN',
    'WESEN', 'WISSE',
    # 6-letter
    'ABENDS', 'ANFANG', 'BISHER', 'BRUDER', 'DIENER', 'DUNKEL',
    'EHRBAR', 'EICHEN', 'FELDEN', 'FINDEN', 'FREUND', 'FRIEDE',
    'FUERST', 'FURCHT', 'GARTEN', 'GEDING', 'GEIGEN', 'GELEIT',
    'GOTTES', 'GRABEN', 'GRIECH', 'HAUPTS', 'HERBST', 'HIMMEL',
    'KOENIG', 'KINDER', 'KIRCHE', 'KNECHT', 'KRIEGE', 'KUENDE',
    'MAIDEN', 'MAUERN', 'MUTTER', 'NICHTS', 'OPFERN', 'ORDNEN',
    'RITTER', 'SCHAUN', 'SCHATZ', 'SCHILD', 'SEELEN', 'SIEBEN',
    'SOLLEN', 'SOMMER', 'SPRACH', 'STEINE', 'STRAFE', 'SUENDE',
    'URALTE', 'VIERTE', 'WAENDE', 'WEISEN', 'WINTER', 'WISSET',
    'WORAUF', 'ZAUBER',
    # 7-letter
    'ANDEREN', 'BRUEDER', 'DUNKLEN', 'EIGENEN', 'FRIEDEN', 'GEHEIME',
    'HEILIGE', 'KOENIGL', 'MEISTER', 'MEINUNG', 'RITTERS', 'RUINENS',
    'SCHWERT', 'SCHWERE', 'STEINEN', 'STIMMEN', 'STRASSE', 'TOCHTER',
    'UMGEBEN', 'WAHRHE', 'WANDERN', 'ZEICHEN',
    # 8+ letter
    'EIGENTUM', 'FREIHEIT', 'GEMEINSCHAFT', 'GERECHTIGKEIT',
    'GESCHLECHT', 'GEWEIHTE', 'HEILIGEN', 'KOENIGIN', 'KOENIGLICH',
    'MEISTERIN', 'PRIESTERIN', 'RITTERTUM',
    'HEILIGTUM', 'ALTERTUM', 'PRIESTERTUM', 'KAISERTUM',
    'KOENIGTUM', 'HERZOGTUM', 'FUERSTENTUM', 'CHRISTENTUM',
    # MHG-specific words
    'MINNE', 'RECKE', 'RECKEN', 'SWERT', 'RICHE', 'RITTER',
    'VROUWE', 'EDELE', 'HERRE', 'LEICH', 'LEICHE',
    'TUGEND', 'HULDE', 'BUSSE', 'SUEHNE', 'FREVEL',
    'RUCHTIG', 'BERUCHTIG', 'BERUCHTIGT',
    'GRIMME', 'KUEHNE', 'TAPFER', 'WACKER',
    'GESELLE', 'KNAPPE', 'MAGD', 'MUOTER',
    'VERDERBEN', 'ERWACHEN', 'ERLOESEN',
    'GEWALTIG', 'MAECHTIG', 'PRAECHTIG',
    'EHRFUERCHTIG', 'ANDAECHTIG', 'NACHDENKLICH',
    # Place-related compound words
    'BACHSTADT', 'BERGSTADT', 'BURGSTADT', 'DRACHSTADT',
    'FELSENBURG', 'GOLDSTADT', 'MARKTSTADT',
    'STEINBRUCH', 'STEINBURG', 'STEINMAUER',
    'RUNDTURM', 'BURGTURM', 'KIRCHTURM', 'WACHTURM',
    'GRENZSTEIN', 'GRABSTEIN', 'GRUNDSTEIN', 'ECKSTEIN',
    'FLUSSSTEIN', 'KALKSTEIN', 'SANDSTEIN',
    # Tibia context
    'BONELORD', 'HELLGATE', 'LIBRARY', 'ANCIENT',
    'FORBIDDEN', 'DREAMER', 'CHALICE',
    # More German words
    'ERBE', 'ERBEN', 'SIEGEL', 'KRONE', 'THRON',
    'KELCH', 'GRAIL', 'BECHER', 'KRUG',
    'LANZE', 'SPEER', 'DOLCH', 'AMULETT',
    'TALISMAN', 'RELIQUIE', 'ARTEFAKT',
    'PROPHET', 'SEHER', 'DRUIDE', 'SCHAMANE',
    'ORAKEL', 'VISION', 'TRAUM', 'TRAEUME',
    'SCHATTEN', 'GEISTER', 'DAEMONEN', 'UNTOTE',
    'SKELETT', 'ZOMBIE', 'VAMPIR', 'WERWOLF',
    'DRACHE', 'DRACHEN', 'GREIF', 'SPHINX',
    'SCHLANGE', 'WURM', 'MOLCH', 'KROTE',
    'EINHORN', 'PHOENIX', 'BASILISK',
]

def check_anagram(word, target, max_extra=1):
    """Check if word is anagram of target + 0-max_extra letters."""
    wc = Counter(word.upper())
    tc = Counter(target.upper())

    # Extra letters in word not in target
    extra = []
    for c in wc:
        diff = wc[c] - tc.get(c, 0)
        if diff > 0:
            extra.extend([c] * diff)

    # Missing letters in word that target needs
    missing = []
    for c in tc:
        diff = tc[c] - wc.get(c, 0)
        if diff > 0:
            missing.extend([c] * diff)

    if len(missing) == 0 and len(extra) <= max_extra:
        return ''.join(extra) if extra else "(exact)"
    return None

# ============================================================
# TEST ALL UNRESOLVED WORDS
# ============================================================
unresolved = {
    # Proper nouns
    'EDETOTNIURG': 'title/place, "SEIN EDETOTNIURGS"',
    'TIUMENGEMI': 'place, near ORTEN',
    'UTRUNR': 'place/title, before "DEN ENDE REDE KOENIG"',
    'HIHL': 'place, with RUNE and DIE NDCE',
    'EILCH': 'word, before AN HEARUCHTIG',
    'TAUTR': 'word, before IST EILCH',
    'HEDEMI': 'place, with DIE URALTE STEINEN',
    'ADTHARSC': 'place, "IST SCHAUN RUIN"',
    'ENGCHD': 'unknown, after TIUMENGEMI ORT',
    'KELSEI': 'unknown, in text',
    'LABRNI': 'place, with WIR',
    'HEARUCHTIG': 'adjective, after AN, MHG word',
    # Garbled segments
    'HECHLLT': 'after FACH, 5x',
    'NDCE': '8x in DIE NDCE',
    'RHEIUIRUNN': 'with HWND, 6x',
    'LAUNRLRUNR': 'near NACH, 2x',
    'TEHWRIGTN': 'before EIN, 9 letters',
    'NTEUTTUIG': 'various, 9 letters',
    'UNENITGH': 'after LABGZERAS, 8 letters',
    'GEIGET': 'various, 6 letters',
    'HWND': 'most common with FINDEN, 4 letters',
}

print("=" * 70)
print("COMPREHENSIVE ANAGRAM RESOLUTION")
print("=" * 70)

for word, desc in sorted(unresolved.items(), key=lambda x: -len(x[0])):
    # Test against word list: exact anagram and +1 extra
    exact = []
    plus1 = []

    for target in WORD_LIST:
        result = check_anagram(word, target, max_extra=1)
        if result == "(exact)":
            exact.append(target)
        elif result is not None:
            plus1.append((target, result))

    if exact or plus1:
        print(f"\n  {word} ({desc}):")
        if exact:
            print(f"    EXACT anagrams: {', '.join(exact)}")
        if plus1:
            for target, extra in sorted(plus1, key=lambda x: len(x[1])):
                print(f"    {target} + {extra}")

# ============================================================
# VERIFY KEY DISCOVERIES
# ============================================================
print(f"\n{'=' * 70}")
print("VERIFICATION OF KEY ANAGRAM DISCOVERIES")
print(f"{'=' * 70}")

verifications = [
    ('TAUTR', 'TRAUT', 'trusted/dear (MHG)'),
    ('EILCH', 'LEICH', 'corpse/song (MHG)'),
    ('EILCH', 'EICH', 'oak (river Lech+I also possible)'),
    ('LABGZERAS', 'SALZBERG', 'Salt Mountain'),
    ('SCHWITEIONE', 'WEICHSTEIN', 'Soft Stone'),
    ('AUNRSONGETRASES', 'ORANGENSTRASSE', 'Orange Street'),
    ('EDETOTNIURG', 'GOTTDIENER', 'God\'s Servant (compound)'),
    ('TIUMENGEMI', 'EIGENTUM', 'Property/Possession'),
    ('HEDEMI', 'HEIME', 'homes (plural of Heim)'),
    ('LABRNI', 'BRLAN', 'test - BERLIN?'),
]

for word, target, meaning in verifications:
    result = check_anagram(word, target, max_extra=2)
    word_sorted = ''.join(sorted(word.upper()))
    target_sorted = ''.join(sorted(target.upper()))
    print(f"\n  {word} vs {target} ({meaning}):")
    print(f"    {word} sorted: {word_sorted}")
    print(f"    {target} sorted: {target_sorted}")
    if result:
        print(f"    MATCH: extra = {result}")
    else:
        # Show what's different
        wc = Counter(word.upper())
        tc = Counter(target.upper())
        extra_w = []
        missing_w = []
        for c in set(list(wc.keys()) + list(tc.keys())):
            diff = wc.get(c, 0) - tc.get(c, 0)
            if diff > 0:
                extra_w.extend([c] * diff)
            elif diff < 0:
                missing_w.extend([c] * (-diff))
        print(f"    NO MATCH: word has extra {extra_w}, missing {missing_w}")

# ============================================================
# LABRNI = BERLIN hypothesis
# ============================================================
print(f"\n{'=' * 70}")
print("LABRNI vs BERLIN")
print(f"{'=' * 70}")
result = check_anagram('LABRNI', 'BERLIN', max_extra=1)
labrni_sorted = ''.join(sorted('LABRNI'))
berlin_sorted = ''.join(sorted('BERLIN'))
print(f"  LABRNI sorted: {labrni_sorted}")
print(f"  BERLIN sorted: {berlin_sorted}")
if result:
    print(f"  MATCH: extra = {result}")
else:
    wc = Counter('LABRNI')
    tc = Counter('BERLIN')
    print(f"  LABRNI: {dict(wc)}")
    print(f"  BERLIN: {dict(tc)}")
    extra = []
    missing = []
    for c in set(list(wc.keys()) + list(tc.keys())):
        diff = wc.get(c, 0) - tc.get(c, 0)
        if diff > 0: extra.extend([c] * diff)
        elif diff < 0: missing.extend([c] * (-diff))
    print(f"  Extra in LABRNI: {extra}, Missing: {missing}")
    # LABRNI: A,B,I,L,N,R  BERLIN: B,E,I,L,N,R
    # LABRNI has A, BERLIN has E. If one code maps A when it should be E (or vice versa),
    # LABRNI could be BERLIN.
    print(f"  >> If A were E: LEBRNI. Sorted: {sorted('LEBRNI')} vs BERLIN sorted: {sorted('BERLIN')}")

# ============================================================
# NARRATIVE READING with resolved anagrams
# ============================================================
print(f"\n{'=' * 70}")
print("NARRATIVE READING WITH RESOLVED ANAGRAMS")
print("=" * 70)

# Anagram resolutions
RESOLVED = {
    'LABGZERAS': 'SALZBERG',
    'SCHWITEIONE': 'WEICHSTEIN',
    'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'TAUTR': 'TRAUT',
    'EILCH': 'LEICH',
    'EDETOTNIURG': 'GOTTDIENER',
    'TIUMENGEMI': 'EIGENTUM',
    'HEDEMI': 'HEIME',
    'HEARUCHTIG': 'BERUCHTIG',
}

# Read the highest-coverage books and apply resolutions
for bidx in range(min(70, len(decoded_books))):
    text = decoded_books[bidx]
    if len(text) < 30:
        continue

    # Apply anagram resolutions
    resolved_text = text
    for anagram, real in RESOLVED.items():
        resolved_text = resolved_text.replace(anagram, f'[{real}]')

    # Only show if resolutions were applied
    if resolved_text != text and len(text) > 50:
        print(f"\n  Book {bidx:2d} ({len(text)} chars):")
        # Show a manageable chunk
        if len(resolved_text) > 120:
            print(f"    {resolved_text[:120]}...")
        else:
            print(f"    {resolved_text}")

# ============================================================
# FULL NARRATIVE with word boundaries
# ============================================================
print(f"\n{'=' * 70}")
print("SAMPLE NARRATIVE WITH WORD BOUNDARIES")
print(f"{'=' * 70}")

# Take a few high-coverage books and try to manually segment
sample_books = [0, 1, 2, 5, 9, 10, 46]
for bidx in sample_books:
    if bidx >= len(decoded_books):
        continue
    text = decoded_books[bidx]
    # Apply resolutions
    for anagram, real in RESOLVED.items():
        text = text.replace(anagram, f'{real}')

    # Simple word boundary guess: insert spaces at known word boundaries
    # This is approximate but helps readability
    print(f"\n  Book {bidx}: {text}")
