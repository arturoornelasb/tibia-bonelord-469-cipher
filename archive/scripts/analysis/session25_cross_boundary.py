#!/usr/bin/env python3
"""
Session 25: Systematic cross-boundary anagram discovery.

Strategy:
1. Decode all books with v7 mapping + DIGIT_SPLITS
2. Apply existing ANAGRAM_MAP
3. DP-segment to find garbled blocks (chars not covered by known words)
4. For each garbled block of length 1-6 chars, combine with adjacent known words
5. Check if any combination is an anagram of a German/MHG word
6. Validate: the anagram must appear consistently across MULTIPLE books
7. Rank by (frequency x chars_gained)

Focus on single-letter garbled blocks ({T}, {E}, {D}, {H}, {I}, {C}) and
short blocks ({RU}, {UN}, {SC}, {CH}, {NG}, {CHN}, {RUI}, {UOD}, {SCE}).
"""

import json, os, sys
from collections import Counter, defaultdict
from itertools import permutations

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

# ============================================================
# CONSTANTS
# ============================================================

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
    'HEDDEMI': 'HEIME', 'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG', 'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE', 'TEIGN': 'NEIGT', 'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER', 'SODGE': 'GODES', 'SNDTEII': 'DIENST',
    'IEB': 'BEI', 'TNEDAS': 'STANDE', 'NSCHAT': 'NACHTS',
    'SANGE': 'SAGEN', 'GHNEE': 'GEHEN', 'THARSCR': 'SCHRAT',
    'ANSD': 'SAND', 'TTU': 'TUT', 'TERLAU': 'URALTE',
    'EUN': 'NEU', 'NIUR': 'RUIN', 'RUIIN': 'RUIN', 'CHIS': 'SICH',
}

EXISTING_ANAGRAM_OUTPUTS = set(ANAGRAM_MAP.values())
EXISTING_ANAGRAM_INPUTS = set(ANAGRAM_MAP.keys())

# ============================================================
# COMPREHENSIVE GERMAN + MHG WORD LIST
# ============================================================

GERMAN_WORDS = set()

# --- 2-letter ---
for w in ['AB', 'AM', 'AN', 'DA', 'DU', 'EI', 'ER', 'ES', 'GE', 'IM', 'IN',
          'JA', 'JE', 'MI', 'NU', 'OB', 'SO', 'TU', 'UM', 'UN', 'UR', 'WO', 'ZU',
          'OD', 'AH', 'OH', 'EH', 'HI', 'AU', 'OS']:
    GERMAN_WORDS.add(w)

# --- 3-letter ---
for w in ['ACH', 'ALS', 'ALT', 'ART', 'AUE', 'AUS', 'BEI', 'BIS', 'DAR', 'DAS',
          'DEM', 'DEN', 'DER', 'DES', 'DIE', 'DIR', 'EIN', 'EIS', 'GAR', 'GEH',
          'GEN', 'GOT', 'GUT', 'HAT', 'HEL', 'HER', 'HIN', 'ICH', 'IHM', 'IHN',
          'IHR', 'INS', 'IST', 'MAN', 'MIR', 'MIN', 'MIT', 'MUT', 'NIT', 'NUN',
          'NUR', 'NUT', 'ODE', 'OEL', 'OFT', 'ORT', 'RAT', 'RIT', 'ROT', 'SAG',
          'SCE', 'SEI', 'SER', 'SIE', 'SIN', 'TAG', 'TAT', 'TER', 'TOD', 'TOT',
          'TUN', 'TUT', 'UND', 'VON', 'VOR', 'WAR', 'WAS', 'WEG', 'WER', 'WIE',
          'WIR', 'WOL', 'ZUM', 'ZUR', 'NEU', 'NIE', 'NET', 'HEI', 'MIS', 'MAG',
          'TAL', 'TOR', 'HUT', 'RUH', 'RUF', 'SAH', 'GAB', 'KAM', 'LOS', 'MAL',
          'RAD', 'RAN', 'SAT', 'TAU', 'TUE', 'WEH', 'ARM', 'BAD', 'BAU', 'BOG',
          'ERZ', 'FEL', 'GOD', 'HAS', 'HOF', 'IRR', 'LAG', 'LAS',
          'NAH', 'OHR', 'RAB', 'RIS', 'SEE', 'SOG', 'ZOG',
          'EWE', 'ANE', 'SOL', 'HIE', 'DAZ', 'GIB', 'REB', 'MER', 'SUN',
          'AUF', 'NOT', 'BOT', 'RED', 'BEG', 'HEH', 'REH', 'RUE', 'TUE',
          'HOL', 'MET', 'SIT', 'ENT', 'VER', 'AGE',
          'DEI', 'REI', 'SUE']:
    GERMAN_WORDS.add(w)

# --- 4-letter ---
for w in ['ABER', 'ACHT', 'ADEL', 'ALLE', 'ALSO', 'ALTE', 'AUCH', 'BALD', 'BAND',
          'BERG', 'BILD', 'BLUT', 'BOTE', 'BUCH', 'BURG', 'DANK', 'DASS', 'DEIN',
          'DENN', 'DICH', 'DIES', 'DOCH', 'DORT', 'DREI', 'EDEL', 'EGAL', 'EHRE',
          'EIDE', 'EINE', 'ENDE', 'ERDE', 'ERST', 'EUCH', 'EWIG', 'FACH', 'FAND',
          'FERN', 'FEST', 'FIEL', 'FORT', 'FREI', 'GABE', 'GALT', 'GANZ', 'GAST',
          'GELD', 'GERN', 'GIBT', 'GLAS', 'GOTT', 'GRAB', 'GRAS', 'GRUN', 'GRAF',
          'HALF', 'HALT', 'HAND', 'HAUS', 'HEER', 'HEIL', 'HEIM', 'HELD', 'HELL',
          'HERR', 'HIER', 'HOCH', 'HOLZ', 'HORN', 'HORT', 'HULD', 'HUND', 'INNE',
          'JEDE', 'KALT', 'KANN', 'KEIN', 'KIND', 'KLAR', 'KLUG', 'KNIE', 'LABT',
          'LAND', 'LANG', 'LAUT', 'LEID', 'LIED', 'LUST', 'MEHR', 'MEIN', 'MILD',
          'MORT', 'MUSS', 'NACH', 'NAHE', 'NAHT', 'NAME', 'NEID', 'NEIN', 'NOCH',
          'ODER', 'OBEN', 'RAST', 'REDE', 'REIN', 'RIEF', 'RISS', 'RUIN', 'RUNE',
          'RUHE', 'SAGT', 'SAND', 'SANG', 'SEID', 'SEIN', 'SICH', 'SIND', 'SOHN',
          'SOLL', 'STEH', 'TEIL', 'TIEF', 'TIER', 'TORE', 'TREU', 'TURM', 'UFER',
          'VIEL', 'VIER', 'WALD', 'WAND', 'WARD', 'WART', 'WEGE', 'WEIL', 'WEIT',
          'WELT', 'WENN', 'WERT', 'WILL', 'WIND', 'WIRD', 'WIRT', 'WOHL', 'WORT',
          'WUND', 'ZEHN', 'ZEIT', 'ZORN', 'HEHL', 'ECHT', 'HOHL', 'WAHR', 'GOLD',
          'RANG', 'TRUG', 'NAHM', 'LIEB', 'ZEIG', 'FELL', 'FELS', 'FELD', 'LEER',
          'MORD', 'FLUG', 'GANG', 'GING', 'HAUT', 'SAGE', 'BEIN', 'WOGE', 'TAGE',
          'DAME', 'RICH', 'LOHN', 'FORM', 'FUER', 'OHNE', 'RITT', 'REIS', 'HOLT',
          'RUHT', 'GEHT', 'TRAT', 'ZWAR', 'MUOT', 'LANT', 'GUOT', 'TUOT',
          'DIET', 'RIET', 'MAGE', 'KINT', 'STAT', 'STAB', 'WIBE', 'ZAHL',
          'TANZ', 'SAAT', 'SACH', 'DACH', 'BACH', 'DING', 'RING', 'SING',
          'NEST', 'REST', 'TEST', 'BEST', 'FEST', 'WEST', 'MIST', 'LIST', 'GIST',
          'RAST', 'LAST', 'MAST', 'HAST', 'FAST', 'BIST', 'LUST', 'JUST',
          'ROST', 'KOST', 'POST', 'MOST', 'GURT',
          'ENGE', 'DIGE', 'HIHL', 'ENTE', 'HASE', 'KERN', 'LAGE', 'MINE',
          'RAUM', 'WACH', 'ZIEL', 'WAGE',
          'DUFT', 'LUFT', 'SAFT', 'HEFT',
          'NEID', 'STEIN', 'LEHM',
          'DIEB', 'SIEB', 'HIEB', 'TRIEB',
          'GRAU', 'BLAU', 'FRAU', 'SCHAU',
          'STAR', 'SPUR', 'HAAR', 'PAAR',
          'WEIN', 'BEIN', 'SEIN', 'REIN', 'FEIN', 'PEIN', 'HEIN',
          'WEIN', 'DEIN', 'MEIN', 'KEIN',
          'STEIN', 'KLEIN',
          'DIENST', 'KUNST']:
    GERMAN_WORDS.add(w)

# --- 5-letter ---
for w in ['ADLER', 'ALLES', 'ALTEN', 'ALTER', 'ALTES', 'BEIDE', 'BERGE', 'BREIT',
          'DARAN', 'DARIN', 'DARUM', 'DEINE', 'DENEN', 'DERER', 'DIESE', 'DURCH',
          'EIGEN', 'EINEN', 'EINER', 'EINES', 'ENGEL', 'ERDEN', 'ERNST', 'ERSTE',
          'ETWAS', 'FEIND', 'GABEN', 'GEBEN', 'GEGEN', 'GEIST', 'GNADE', 'GRABE',
          'GREIS', 'GRUND', 'GRUFT', 'HABEN', 'HAUPT', 'HEIDE', 'HERRE', 'IMMER',
          'JEDER', 'JEDEN', 'KLAGE', 'KLEIN', 'KRAFT', 'KREUZ', 'KRONE', 'LANDE',
          'LEGEN', 'LESEN', 'LEUTE', 'LICHT', 'LIEBE', 'MACHT', 'MEERE', 'MINNE',
          'NACHT', 'NEIGT', 'NICHT', 'ORTEN', 'RECHT', 'REDEN', 'RUFEN', 'RUHEN',
          'RUNEN', 'SAGEN', 'SCHON', 'SEELE', 'SEGEN', 'SEHEN', 'SENDE', 'SORGE',
          'STAUB', 'STEHE', 'STERN', 'STOLZ', 'UNTER', 'WACHE', 'WAGEN', 'WEGEN',
          'WENDE', 'WESEN', 'WILLE', 'WISSE', 'WORTE', 'WUNDE', 'WURDE',
          'RUINE', 'INSEL', 'TIEFE', 'GROSS', 'STETS', 'TRAUM', 'STURM',
          'IHREN', 'IHREM', 'IHRES', 'IHRER', 'EINEM',
          'SEINER', 'SEINEN', 'SEINES', 'SEINEM',
          'NORDEN', 'OSTEN', 'WESTEN',
          'KEINE', 'KEINEN', 'VIELE', 'DIESEN', 'DIESEM',
          'ACHTE', 'ACHTEN', 'ACHTER', 'DENKE',
          'STEINE', 'STEIN', 'STEINEN',
          'LETZTE', 'LETZTEN', 'ANDERE', 'ANDEREN', 'DIESER', 'DIESES',
          'EDELE', 'SCHULD', 'FLUCH', 'RACHE',
          'DINC', 'HULDE', 'HERRE', 'GEBOT',
          'GEWAN', 'SELDE', 'TUGENT', 'TRIUWE',
          'SWERT', 'RICHE', 'HELDE', 'MINNEN',
          'WIESE', 'EBENE', 'GRUBE', 'MEIDE', 'WEHRT', 'FAHRT',
          'STRIT', 'CRAFT', 'MUOTE', 'LIUT', 'LIUTE',
          'KUENE', 'STARC', 'BURC', 'BURGE', 'STETE',
          'VAREN', 'VINDEN', 'TAGEN', 'NEBEN', 'BEVOR',
          'DIENST', 'FINDEN', 'SCHAUN', 'STANDE', 'NACHTS', 'WISTEN',
          'MANIER', 'URALTE', 'DUNKEL', 'KOENIG',
          'REDER', 'HEIME', 'TRAUT', 'LEICH',
          'ORDEN', 'SCHWUR', 'SCHRAT', 'SCHARDT',
          'GODES', 'MITTE', 'HALBE', 'SINNE',
          'SCHAR', 'SCHAREN', 'EISEN', 'NAHEN',
          'EINST', 'SONST', 'STETS', 'MEIST',
          'ABEND', 'NEBEN', 'BEVOR',
          'KNABE', 'DIENER', 'HERRIN',
          'DEINS', 'MEINS', 'SEINS',
          'TRITT', 'STIRN', 'STIER',
          'LEHRE', 'FEHDE', 'WENDE', 'SENDE',
          'DIENEST', 'HECHELT', 'HEHLEN',
          'EHRT', 'KEHRT', 'WEHRT', 'LEHRT',
          'AHNEN', 'BEUTE', 'LEIDE', 'HEILE',
          'MAUER', 'LAUER', 'BAUER', 'SAUER', 'DAUER',
          'STERN', 'GERNE', 'FERNE', 'LERNE',
          'REISE', 'WEISE', 'LEISE', 'KREISE',
          'TREUE', 'FREUE', 'BEREUE',
          'SUCHE', 'BUCHE', 'KUCHE', 'FLUCHE',
          'STUNDE', 'RUNDE', 'WUNDE', 'KUNDE', 'MUNDE',
          'STEINE', 'BEINE', 'WEINE', 'SEINE', 'REINE', 'FEINE', 'KLEINE',
          'HALTE', 'WALTE', 'SCHALTE',
          'TRAGE', 'FRAGE', 'KLAGE', 'PLAGE',
          'DECKE', 'HECKE', 'STECKE',
          'NACHT', 'MACHT', 'WACHT', 'ACHT', 'TRACHT', 'SCHLACHT',
          'DIENST', 'KUNST', 'GUNST', 'DUNST', 'BRUNST']:
    GERMAN_WORDS.add(w)

# --- 6+ letter ---
for w in ['URALTE', 'URALTEN', 'ZWISCHEN', 'VERSCHIEDENE',
          'KOENIG', 'KRIEGER', 'MEISTER', 'HERREN',
          'INSCHRIFT', 'TEMPEL', 'HOEHLE',
          'GEBOREN', 'GESEHEN', 'GEFUNDEN', 'GESCHAFFEN',
          'GESCHRIEBEN', 'VERSPRECHEN', 'VERSTEHEN',
          'GEHEIMNIS', 'BIBLIOTHEK', 'TAUSEND', 'ANTWORT',
          'STEINE', 'STEINEN', 'STEINES',
          'REICHE', 'REICHEN', 'REICHES',
          'SCHRIFT', 'SCHRIFTEN', 'ZEICHEN',
          'WAHRHEIT', 'DUNKELHEIT',
          'STIMME', 'STIMMEN', 'SCHNELL', 'KAPITEL',
          'HINAUS', 'HIMMEL', 'ERDEN', 'ALLEIN', 'DEREINST',
          'GEMACHT', 'GEGANGEN', 'GEKOMMEN', 'GEGEBEN',
          'SAGTEN', 'GINGEN', 'KAMEN', 'FANDEN', 'SAHEN',
          'KNECHT', 'SCHLECHT', 'GESANDT', 'GERECHT',
          'SICHTEN', 'DICHTEN', 'LICHTEN', 'RICHTEN',
          'WUNDER', 'WANDERN', 'WANDERT', 'DONNER',
          'RICHTER', 'DICHTER', 'LICHTER', 'SICHTER',
          'SUEDEN', 'INSELN', 'RUINEN',
          'EIGENTUM', 'GOTTDIENER', 'GOTTDIENERS',
          'WEICHSTEIN', 'ORANGENSTRASSE', 'SALZBERG',
          'BERUCHTIG', 'BERUCHTIGER',
          'LEICHANBERUCHTIG', 'LEICHANBERUCHTIGER',
          'NACHTEN', 'TRACHTEN', 'SCHLACHTEN',
          'WACHSEN', 'WACHTER', 'MACHTEN',
          'MEISTER', 'GEISTER',
          'EINSICHT', 'AUSSICHT', 'ABSICHT',
          'KNECHTE', 'RECHTE', 'ECHTE', 'SCHLECHTE',
          'RITTER', 'RICHTEN', 'NICHTEN', 'SICHTEN',
          'DACHTE', 'DACHTEN', 'BRACHTE', 'BRACHTEN',
          'BEIDER', 'BEIDEN', 'KEINER', 'KEINEM',
          'MORGEN', 'MITTAG',
          'KIRCHE', 'KLOSTER', 'SCHLOSS',
          'STRASSE', 'BRUECKE', 'GARTEN',
          'HEILIG', 'HEILIGE', 'HEILIGEN',
          'TAPFER', 'TAPFERE', 'TAPFEREN',
          'GEWALTIG', 'MAECHTIG',
          'ENDLICH', 'FREILICH',
          'WAHRHAFT', 'ERNSTHAFT',
          'WINDUNRUHN', 'HECHELT',
          'SCHANDE',
          'ABGRUND', 'EINGANG', 'AUSGANG',
          'EINSAM', 'GEMEINSAM',
          'STANDEN', 'GESTANDEN', 'BESTANDEN',
          'GERUFEN', 'GESUNGEN', 'GETRAGEN',
          'GENOMMEN', 'GEFALLEN', 'ERHOBEN',
          'ERDACHT', 'GEDACHT', 'BEDACHT',
          'RUNESTEIN', 'RUNENSTEIN', 'RUNEORT', 'STEINALT',
          'ERSTEN', 'ANDERE', 'ANDEREN',
          'GANZE', 'GANZEN', 'GANZER', 'GANZES',
          'GROSSE', 'GROSSEN', 'GROSSER', 'GROSSES',
          'KLEINE', 'KLEINEN', 'KLEINER', 'KLEINES',
          'RECHTS', 'NICHTS', 'NACHHER',
          'ENDLICH', 'ENDLOS', 'ANFANG',
          'DICHTER', 'MEISTER', 'RITTER', 'KNECHTE',
          'WACHTER', 'SACHTE', 'DACHTE',
          'STEINER', 'STEINES', 'STEINERN',
          'REISTEN', 'GEISTEN', 'MEISTEN',
          'LEISTEN', 'FEISTEN', 'WEISTEN',
          'ACHTER', 'ACHTEN', 'ACHTES',
          'SECHSTE', 'SIEBTE', 'ACHTE',
          'NEUNTE', 'ZEHNTE', 'ELFTE',
          'HUNDERT', 'TAUSEND',
          'ABENDS', 'MORGENS', 'NACHTS',
          'KONNTE', 'SOLLTE', 'WOLLTE', 'MUSSTE',
          'NIEMALS', 'ZWEIMAL', 'DREIMAL', 'EINMAL',
          'INMITTEN', 'DANEBEN', 'DARUNTER', 'DARUEBER',
          'ERSTER', 'LETZTER', 'ANDERER',
          'RICHTUNG', 'DICHTUNG', 'SICHTUNG',
          'GERICHTET', 'GEDICHTET', 'GESICHTET',
          'ANDERES', 'WEITERES', 'EINIGES',
          'IRDISCH', 'HIMMLISCH', 'MENSCHLICH',
          'STEINERNE', 'STEINERNEN', 'STEINERNER']:
    GERMAN_WORDS.add(w)

# Build anagram lookup: sorted-letters -> list of words
anagram_lookup = defaultdict(list)
for w in GERMAN_WORDS:
    key = ''.join(sorted(w))
    anagram_lookup[key].append(w)

print(f"German word list: {len(GERMAN_WORDS)} words")
print(f"Anagram lookup keys: {len(anagram_lookup)}")

# ============================================================
# DECODE + SEGMENT
# ============================================================

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    return 0 if ic_from_counts(Counter(bp0), len(bp0)) > ic_from_counts(Counter(bp1), len(bp1)) else 1

decoded_books = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    decoded_books.append(''.join(v7.get(p, '?') for p in pairs))

# Apply anagram map
processed_books = []
for text in decoded_books:
    for old in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
        text = text.replace(old, ANAGRAM_MAP[old])
    processed_books.append(text)

raw_concat = ''.join(decoded_books)
processed_concat = ''.join(processed_books)

KNOWN_WORDS = set(w for w in GERMAN_WORDS if len(w) >= 2)

# ============================================================
# DP SEGMENTATION
# ============================================================

def dp_segment(text):
    """DP segmentation returning list of (type, value, start, end) tokens."""
    n = len(text)
    if n == 0:
        return []
    dp = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], None)
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if '?' in cand:
                continue
            if cand in KNOWN_WORDS:
                score = dp[start][0] + wlen
                if score > dp[i][0]:
                    dp[i] = (score, (start, cand))
    tokens = []
    i = n
    while i > 0:
        if dp[i][1] is not None:
            start, word = dp[i][1]
            tokens.append(('word', word, start, i))
            i = start
        else:
            j = i - 1
            while j > 0 and dp[j][1] is None:
                j -= 1
            tokens.append(('garbled', text[j:i], j, i))
            i = j
    tokens.reverse()
    return tokens

# ============================================================
# SEGMENT ALL BOOKS
# ============================================================

print("\n" + "=" * 80)
print("PHASE 1: DP SEGMENTATION OF ALL BOOKS")
print("=" * 80)

book_tokens = []
total_chars = 0
total_covered = 0
garbled_census = Counter()

for bidx, text in enumerate(processed_books):
    tokens = dp_segment(text)
    book_tokens.append(tokens)
    for ttype, tval, tstart, tend in tokens:
        if ttype == 'word':
            total_covered += len(tval)
        total_chars += (tend - tstart)
        if ttype == 'garbled':
            garbled_census[tval] += 1

print(f"Total chars: {total_chars}")
print(f"Covered: {total_covered} ({total_covered/total_chars*100:.1f}%)")
print(f"Unique garbled blocks: {len(garbled_census)}")

for glen in [1, 2, 3, 4]:
    blocks = [(g, c) for g, c in garbled_census.items() if len(g) == glen]
    blocks.sort(key=lambda x: -x[1])
    total_instances = sum(c for _, c in blocks)
    print(f"\n  {glen}-char garbled blocks: {len(blocks)} unique, {total_instances} instances")
    for g, c in blocks[:15]:
        print(f"    {{{g}}} x{c}")

# ============================================================
# PHASE 2: CROSS-BOUNDARY COMBINATIONS
# ============================================================

print("\n" + "=" * 80)
print("PHASE 2: CROSS-BOUNDARY ANAGRAM SEARCH")
print("=" * 80)

candidates = defaultdict(list)

def sorted_key(s):
    return ''.join(sorted(s))

for bidx, tokens in enumerate(book_tokens):
    for ti, (ttype, tval, tstart, tend) in enumerate(tokens):
        if ttype != 'garbled':
            continue
        garbled_len = len(tval)
        if garbled_len > 6:
            continue

        # Only consider directly adjacent words (no garbled between)
        left_word = None
        right_word = None
        if ti > 0 and tokens[ti-1][0] == 'word':
            left_word = tokens[ti-1][1]
        if ti + 1 < len(tokens) and tokens[ti+1][0] == 'word':
            right_word = tokens[ti+1][1]

        # STRATEGY A: garbled + right_word (full)
        if right_word and garbled_len <= 4:
            combo = tval + right_word
            if len(combo) <= 12:
                sk = sorted_key(combo)
                for match in anagram_lookup.get(sk, []):
                    if match != combo:
                        desc = f"{{{tval}}}+{right_word}"
                        candidates[(desc, combo, match, 'exact')].append((bidx, tstart))

        # STRATEGY B: left_word + garbled (full)
        if left_word and garbled_len <= 4:
            combo = left_word + tval
            if len(combo) <= 12:
                sk = sorted_key(combo)
                for match in anagram_lookup.get(sk, []):
                    if match != combo:
                        desc = f"{left_word}+{{{tval}}}"
                        candidates[(desc, combo, match, 'exact')].append((bidx, tstart))

        # STRATEGY C: left + garbled + right (for 1-2 char garbled)
        if left_word and right_word and garbled_len <= 2:
            combo = left_word + tval + right_word
            if len(combo) <= 14:
                sk = sorted_key(combo)
                for match in anagram_lookup.get(sk, []):
                    if match != combo:
                        desc = f"{left_word}+{{{tval}}}+{right_word}"
                        candidates[(desc, combo, match, '3way')].append((bidx, tstart))

        # STRATEGY D: garbled + partial right (split right word)
        if right_word and garbled_len <= 3:
            for take in range(1, min(4, len(right_word))):
                partial = right_word[:take]
                remainder = right_word[take:]
                combo = tval + partial
                if len(combo) >= 3 and len(combo) <= 10:
                    sk = sorted_key(combo)
                    for match in anagram_lookup.get(sk, []):
                        if match != combo and (len(remainder) >= 2 and remainder in GERMAN_WORDS):
                            desc = f"{{{tval}}}+{partial}|{remainder}"
                            candidates[(desc, combo, match, 'split_right')].append((bidx, tstart))

        # STRATEGY E: partial left + garbled (split left word)
        if left_word and garbled_len <= 3:
            for take in range(1, min(4, len(left_word))):
                partial = left_word[-take:]
                remainder = left_word[:-take]
                combo = partial + tval
                if len(combo) >= 3 and len(combo) <= 10:
                    sk = sorted_key(combo)
                    for match in anagram_lookup.get(sk, []):
                        if match != combo and (len(remainder) >= 2 and remainder in GERMAN_WORDS):
                            desc = f"{remainder}|{partial}+{{{tval}}}"
                            candidates[(desc, combo, match, 'split_left')].append((bidx, tstart))

# ============================================================
# PHASE 3: FILTER + VALIDATE
# ============================================================

print("\n" + "=" * 80)
print("PHASE 3: VALIDATION AND RANKING")
print("=" * 80)

frequent = {}
for key, occurrences in candidates.items():
    if len(occurrences) >= 3:
        frequent[key] = occurrences

print(f"Candidates with 3+ occurrences: {len(frequent)}")

def conflicts_with_existing(combo, match):
    """Check if the combo string overlaps with existing anagram I/O."""
    for old_input in EXISTING_ANAGRAM_INPUTS:
        if combo in old_input or old_input in combo:
            return True
    for old_output in EXISTING_ANAGRAM_OUTPUTS:
        if combo in old_output or old_output in combo:
            return True
    return False

results = []
for (desc, combo, match, pattern), occurrences in frequent.items():
    count = len(occurrences)
    unique_books = len(set(b for b, _ in occurrences))

    garbled_part = ''
    for part in desc.split('+'):
        if part.startswith('{') and part.endswith('}'):
            garbled_part = part[1:-1]
            break
    garbled_len = len(garbled_part) if garbled_part else 1

    chars_gained = garbled_len * count
    conflict = conflicts_with_existing(combo, match)

    results.append({
        'desc': desc,
        'combo': combo,
        'match': match,
        'pattern': pattern,
        'count': count,
        'unique_books': unique_books,
        'garbled_len': garbled_len,
        'chars_gained': chars_gained,
        'conflict': conflict,
        'occurrences': occurrences,
    })

results.sort(key=lambda r: (-r['chars_gained'], -r['count']))

print(f"Total ranked results: {len(results)}")

# ============================================================
# DISPLAY TOP RESULTS
# ============================================================

print("\n" + "=" * 80)
print("TOP CROSS-BOUNDARY ANAGRAM CANDIDATES (all)")
print("=" * 80)
print(f"{'Rk':>3} {'Cnt':>4} {'Bks':>4} {'Gain':>5} {'Type':>12} {'Description':35} {'Combo':>15} -> {'Match':15} {'Stat':>8}")
print("-" * 130)

shown = 0
for r in results:
    conflict_str = 'CONFL' if r['conflict'] else 'OK'
    print(f"{shown+1:3d} {r['count']:4d} {r['unique_books']:4d} {r['chars_gained']:5d} {r['pattern']:>12} {r['desc']:35} {r['combo']:>15} -> {r['match']:15} {conflict_str:>8}")
    shown += 1
    if shown >= 80:
        break

# ============================================================
# PHASE 4: SAFE CANDIDATES DEEP ANALYSIS
# ============================================================

print("\n" + "=" * 80)
print("PHASE 4: SAFE CANDIDATES (no conflict) - DETAILED")
print("=" * 80)

safe_results = [r for r in results if not r['conflict']]
print(f"Safe candidates: {len(safe_results)}")

for rank, r in enumerate(safe_results[:30], 1):
    print(f"\n--- #{rank}: {r['desc']} = {r['combo']} -> {r['match']} ({r['count']}x, {r['unique_books']} books, +{r['chars_gained']} chars, {r['pattern']}) ---")
    shown_ctx = 0
    for bidx, pos in r['occurrences'][:5]:
        text = processed_books[bidx]
        ctx_start = max(0, pos - 15)
        ctx_end = min(len(text), pos + len(r['combo']) + 15)
        context = text[ctx_start:ctx_end]
        print(f"  Book {bidx:2d}: ...{context}...")
        shown_ctx += 1
    if len(r['occurrences']) > 5:
        print(f"  ... and {len(r['occurrences']) - 5} more occurrences")

# ============================================================
# PHASE 5: COVERAGE IMPACT TEST
# ============================================================

print("\n" + "=" * 80)
print("PHASE 5: COVERAGE IMPACT SIMULATION")
print("=" * 80)

def count_coverage(text, vocab):
    n = len(text)
    covered = 0
    i = 0
    while i < n:
        best_len = 0
        for l in range(min(20, n-i), 1, -1):
            if text[i:i+l] in vocab:
                best_len = l
                break
        if best_len > 0:
            covered += best_len
            i += best_len
        else:
            i += 1
    return covered

COVERAGE_VOCAB = set(w for w in GERMAN_WORDS if len(w) >= 2)
base_coverage = count_coverage(processed_concat, COVERAGE_VOCAB)
print(f"Baseline coverage: {base_coverage}/{len(processed_concat)} = {base_coverage/len(processed_concat)*100:.1f}%")

print(f"\nIncremental coverage gains from safe candidates:")
print(f"{'Rk':>3} {'Anagram':30} {'NewCov':>8} {'Gain':>7} {'GainPct':>8}")
print("-" * 70)

cumulative_map = dict(ANAGRAM_MAP)
cur_vocab = set(COVERAGE_VOCAB)
cur_base = base_coverage

accepted = []
for rank, r in enumerate(safe_results[:30], 1):
    test_map = dict(cumulative_map)
    test_map[r['combo']] = r['match']

    test_text = raw_concat
    for k in sorted(test_map, key=len, reverse=True):
        test_text = test_text.replace(k, test_map[k])

    test_vocab = cur_vocab | {r['match']}
    new_cov = count_coverage(test_text, test_vocab)
    gain = new_cov - cur_base
    gain_pct = gain / len(processed_concat) * 100

    status = "ACCEPT" if gain > 0 else "skip"
    print(f"{rank:3d} {r['combo']:>12} -> {r['match']:<15} {new_cov:>8} {'+' + str(gain):>7} {gain_pct:>+7.2f}%  {status}")

    if gain > 0:
        cumulative_map[r['combo']] = r['match']
        cur_vocab.add(r['match'])
        cur_base = new_cov
        accepted.append(r)

# ============================================================
# PHASE 6: FINAL REPORT
# ============================================================

print("\n" + "=" * 80)
print("PHASE 6: FINAL REPORT - NEW ANAGRAMS FOUND")
print("=" * 80)

new_anagrams = {k: v for k, v in cumulative_map.items() if k not in ANAGRAM_MAP}
print(f"\nNew anagrams accepted: {len(new_anagrams)}")
for old, new in sorted(new_anagrams.items(), key=lambda x: len(x[0]), reverse=True):
    info = None
    for r in accepted:
        if r['combo'] == old and r['match'] == new:
            info = r
            break
    count_str = f"({info['count']}x, +{info['chars_gained']} chars)" if info else ""
    print(f"  '{old}' -> '{new}' {count_str}")

final_text = raw_concat
for k in sorted(cumulative_map, key=len, reverse=True):
    final_text = final_text.replace(k, cumulative_map[k])

orig_vocab = set(w for w in GERMAN_WORDS if len(w) >= 2)
final_cov = count_coverage(final_text, cur_vocab)
orig_cov = count_coverage(processed_concat, orig_vocab)
print(f"\nOriginal coverage: {orig_cov}/{len(processed_concat)} = {orig_cov/len(processed_concat)*100:.1f}%")
print(f"Final coverage:    {final_cov}/{len(final_text)} = {final_cov/len(final_text)*100:.1f}%")
print(f"Net gain: +{final_cov - orig_cov} chars ({(final_cov - orig_cov)/len(final_text)*100:.2f}%)")

# ============================================================
# PHASE 7: SINGLE-LETTER GARBLED BLOCK CONTEXTS
# ============================================================

print("\n" + "=" * 80)
print("PHASE 7: SINGLE-LETTER GARBLED BLOCK CONTEXTS")
print("=" * 80)

single_letter_blocks = Counter()
single_letter_contexts = defaultdict(list)

for bidx, tokens in enumerate(book_tokens):
    for ti, (ttype, tval, tstart, tend) in enumerate(tokens):
        if ttype == 'garbled' and len(tval) == 1:
            single_letter_blocks[tval] += 1
            left_ctx = ''
            right_ctx = ''
            if ti > 0:
                if tokens[ti-1][0] == 'word':
                    left_ctx = tokens[ti-1][1]
                else:
                    left_ctx = '{' + tokens[ti-1][1] + '}'
            if ti + 1 < len(tokens):
                if tokens[ti+1][0] == 'word':
                    right_ctx = tokens[ti+1][1]
                else:
                    right_ctx = '{' + tokens[ti+1][1] + '}'
            ctx_key = f"{left_ctx}|{tval}|{right_ctx}"
            single_letter_contexts[ctx_key].append(bidx)

print("Single-letter garbled blocks:")
for letter, count in single_letter_blocks.most_common():
    print(f"  {{{letter}}}: {count}x")

print("\nMost common single-letter contexts (left|garbled|right) with 3+ occurrences:")
for ctx, book_list in sorted(single_letter_contexts.items(), key=lambda x: -len(x[1])):
    if len(book_list) >= 3:
        books_str = ','.join(str(b) for b in book_list[:8])
        print(f"  {ctx:45s} x{len(book_list):2d}  [books: {books_str}]")

# ============================================================
# PHASE 8: TWO-LETTER GARBLED CONTEXTS
# ============================================================

print("\n" + "=" * 80)
print("PHASE 8: TWO-LETTER GARBLED BLOCK CONTEXTS")
print("=" * 80)

two_letter_contexts = defaultdict(list)

for bidx, tokens in enumerate(book_tokens):
    for ti, (ttype, tval, tstart, tend) in enumerate(tokens):
        if ttype == 'garbled' and len(tval) == 2:
            left_ctx = ''
            right_ctx = ''
            if ti > 0:
                if tokens[ti-1][0] == 'word':
                    left_ctx = tokens[ti-1][1]
                else:
                    left_ctx = '{' + tokens[ti-1][1] + '}'
            if ti + 1 < len(tokens):
                if tokens[ti+1][0] == 'word':
                    right_ctx = tokens[ti+1][1]
                else:
                    right_ctx = '{' + tokens[ti+1][1] + '}'
            ctx_key = f"{left_ctx}|{tval}|{right_ctx}"
            two_letter_contexts[ctx_key].append(bidx)

print("Most common 2-letter garbled contexts with 3+ occurrences:")
for ctx, book_list in sorted(two_letter_contexts.items(), key=lambda x: -len(x[1])):
    if len(book_list) >= 3:
        books_str = ','.join(str(b) for b in book_list[:8])
        print(f"  {ctx:45s} x{len(book_list):2d}  [books: {books_str}]")

print("\n" + "=" * 80)
print("DONE - Session 25 cross-boundary analysis complete.")
print("=" * 80)
