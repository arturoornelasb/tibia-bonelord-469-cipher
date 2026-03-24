#!/usr/bin/env python3
"""
Session 25: Aggressive vocabulary mining.
Find German/MHG words in decoded text that aren't in the KNOWN set.
"""
import json, os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
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

KNOWN = {
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN', 'TUT',
    'SAG', 'WAR', 'NU', 'SIN', 'STANDE', 'NACHTS', 'NIT', 'TOT', 'TER',
    'ABER', 'ALLE', 'ALLES', 'ALTE', 'ALTEN', 'ALTER', 'AUCH', 'BAND',
    'BERG', 'BURG', 'DENN', 'DIES', 'DIESE', 'DIESER', 'DIESEN',
    'DIESEM', 'DOCH', 'DORT', 'DREI', 'DURCH', 'EINE', 'EINEM',
    'EINEN', 'EINER', 'EINES', 'ENDE', 'ERDE', 'ERST', 'ERSTE',
    'FACH', 'FAND', 'FERN', 'FEST', 'FORT', 'GAR', 'GANZ', 'GEGEN',
    'GEIST', 'GOTT', 'GOLD', 'GRAB', 'GROSS', 'GRUFT', 'GUT',
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
    'WISSEN', 'WISSET', 'RUFEN', 'WIEDER', 'OEL', 'SCE', 'MINNE',
    'MIN', 'HEL', 'ODE', 'SER', 'GEN', 'INS', 'GEIGET',
    'BERUCHTIG', 'BERUCHTIGER', 'MEERE', 'NEIGT', 'WISTEN', 'MANIER',
    'HUND', 'GODE', 'GODES', 'EIGENTUM', 'REDER', 'THENAEUT',
    'LABT', 'MORT', 'DIGE', 'WEGE', 'KOENIGS', 'NAHE', 'NOT', 'NOTH',
    'ZUR', 'OWI', 'ENGE', 'SEIDEN', 'ALTES', 'BIS', 'NUT', 'NUTZ',
    'HEIL', 'NEID', 'TREU', 'TREUE', 'SUN', 'DIENST', 'SANG', 'DINC',
    'HULDE', 'STEINE', 'LANT', 'HERRE', 'DIENEST', 'GEBOT', 'SCHWUR',
    'ORDEN', 'RICHTER', 'DUNKEL', 'EHRE', 'EDELE', 'SCHULD', 'SEGEN',
    'FLUCH', 'RACHE', 'KOENIG', 'DASS', 'EDEL', 'ADEL', 'SCHRAT',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE', 'GOTTDIENER',
    'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME', 'SCHARDT',
    'RIT', 'EWE', 'MIS', 'AUE', 'EIS',
}

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    return 0 if ic_from_counts(Counter(bp0), len(bp0)) > ic_from_counts(Counter(bp1), len(bp1)) else 1

# Decode
decoded = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    decoded.append(''.join(v7.get(p, '?') for p in pairs))

raw = ''.join(decoded)
processed = raw
for k in sorted(ANAGRAM_MAP, key=len, reverse=True):
    processed = processed.replace(k, ANAGRAM_MAP[k])

# DP segmentation to find uncovered positions
def dp_segment(text, vocab):
    n = len(text)
    dp = [0] * (n + 1)
    back = [None] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        for wlen in range(2, min(i, 20) + 1):
            s = i - wlen
            if text[s:i] in vocab and dp[s] + wlen > dp[i]:
                dp[i] = dp[s] + wlen
                back[i] = s
    # Find uncovered positions
    covered = set()
    i = n
    while i > 0:
        if back[i] is not None:
            for j in range(back[i], i):
                covered.add(j)
            i = back[i]
        else:
            i -= 1
    return dp[n], covered

baseline_cov, baseline_covered = dp_segment(processed, KNOWN)
total = sum(1 for c in processed if c != '?')
print(f"Baseline: {baseline_cov}/{total} = {baseline_cov/total*100:.1f}%")

# Build massive candidate word list
CANDIDATES = set()

# German common words (comprehensive)
GERMAN_WORDS = [
    # Verbs - infinitive, past, participle, imperative, conjugated
    'BITTEN', 'BAT', 'GEBETEN', 'BITT', 'BITTET',
    'BLEIBEN', 'BLIEB', 'GEBLIEBEN', 'BLEIB', 'BLEIBT',
    'BRINGEN', 'BRACHTE', 'GEBRACHT', 'BRING', 'BRINGT',
    'DENKEN', 'DACHTE', 'GEDACHT', 'DENK', 'DENKT',
    'FAHREN', 'FUHR', 'GEFAHREN', 'FAHR', 'FAEHRT',
    'FALLEN', 'FIEL', 'GEFALLEN', 'FALL', 'FAELLT',
    'HALTEN', 'HIELT', 'GEHALTEN', 'HALT', 'HAELT',
    'HEISSEN', 'HIESS', 'GEHEISSEN', 'HEISS', 'HEISST',
    'HELFEN', 'HALF', 'GEHOLFEN', 'HILF', 'HILFT',
    'KENNEN', 'KANNTE', 'GEKANNT', 'KENN', 'KENNT',
    'LAUFEN', 'LIEF', 'GELAUFEN', 'LAUF', 'LAEUFT',
    'LEGEN', 'LEGTE', 'GELEGT', 'LEG', 'LEGT',
    'LIEGEN', 'LAG', 'GELEGEN', 'LIEG', 'LIEGT',
    'MACHEN', 'MACHTE', 'GEMACHT', 'MACH', 'MACHT',
    'RUFEN', 'RIEF', 'GERUFEN', 'RUF', 'RUFT',
    'SCHLAGEN', 'SCHLUG', 'GESCHLAGEN', 'SCHLAG',
    'SCHREIBEN', 'SCHRIEB', 'GESCHRIEBEN', 'SCHREIB',
    'SETZEN', 'SETZTE', 'GESETZT', 'SETZ', 'SETZT',
    'SPRECHEN', 'SPRACH', 'GESPROCHEN', 'SPRICH', 'SPRICHT',
    'STELLEN', 'STELLTE', 'GESTELLT', 'STELL',
    'STERBEN', 'STARB', 'GESTORBEN', 'STIRB', 'STIRBT',
    'TRAGEN', 'TRUG', 'GETRAGEN', 'TRAG', 'TRAEGT',
    'TREIBEN', 'TRIEB', 'GETRIEBEN', 'TREIB',
    'TRETEN', 'TRAT', 'GETRETEN', 'TRITT',
    'WACHSEN', 'WUCHS', 'GEWACHSEN', 'WACHS',
    'WERFEN', 'WARF', 'GEWORFEN', 'WIRF', 'WIRFT',
    'ZIEHEN', 'ZOG', 'GEZOGEN', 'ZIEH', 'ZIEHT',
    'RICHTEN', 'RICHTETE', 'GERICHTET', 'RICHT',
    'WANDERN', 'WANDERTE', 'GEWANDERT', 'WANDER',
    'HERRSCHEN', 'HERRSCHTE', 'GEHERRSCHT',
    'DIENEN', 'DIENTE', 'GEDIENT', 'DIEN', 'DIENT',
    'EHREN', 'EHRTE', 'GEEHRT',
    'FLIEHEN', 'FLOH', 'GEFLOHEN', 'FLIEH',
    'FOLGEN', 'FOLGTE', 'GEFOLGT', 'FOLG', 'FOLGT',
    'FUEHREN', 'FUEHRTE', 'GEFUEHRT',
    'GRUENDEN', 'GRUENDETE', 'GEGRUENDET',
    'KAEMPFEN', 'KAEMPFTE', 'GEKAEMPFT',
    'KLAGEN', 'KLAGTE', 'GEKLAGT', 'KLAG',
    'NENNEN', 'NANNTE', 'GENANNT', 'NENN', 'NENNT',
    'SCHWINGEN', 'SCHWANG', 'GESCHWUNGEN',
    'SENKEN', 'SENKTE', 'GESENKT', 'SENK',
    'SINKEN', 'SANK', 'GESUNKEN', 'SINK', 'SINKT',
    'WEICHEN', 'WICH', 'GEWICHEN', 'WEICH', 'WEICHT',
    'WIRKEN', 'WIRKTE', 'GEWIRKT', 'WIRK', 'WIRKT',
    'WOHNEN', 'WOHNTE', 'GEWOHNT', 'WOHN',
    'ZERSTOEREN', 'ZERSTOERTE', 'ZERSTOERT',
    # Nouns
    'BRUDER', 'BRUEDER', 'SCHWESTER', 'MUTTER', 'VATER',
    'SOHN', 'TOCHTER', 'FRAU', 'MANN', 'KIND', 'KINDER',
    'FEIND', 'FEINDE', 'FREUND', 'FREUNDE',
    'KNECHT', 'KNECHTE', 'KRIEGER', 'KRIEGER',
    'DIENER', 'DIENERS', 'MEISTER', 'MEISTERIN',
    'OSTEN', 'WESTEN', 'NORDEN', 'SUEDEN',
    'FEUER', 'WASSER', 'LUFT', 'STURM',
    'STEIN', 'STEINE', 'STEINEN', 'STEINS',
    'NEID', 'SCHULD', 'SCHMERZ', 'EHRE', 'RUHM',
    'FRIEDE', 'FRIEDEN', 'KRIEG', 'KRIEGE',
    'GRENZE', 'GRENZEN', 'INSEL', 'INSELN',
    'DUNKELHEIT', 'FINSTERNIS', 'SCHATTEN',
    'RUINE', 'RUINEN', 'TRUEMMER',
    'GEHEIMNIS', 'GEHEIM', 'FLUCH', 'SEGEN',
    'RITUAL', 'OPFER', 'ALTAR',
    'SCHWERT', 'SCHILD', 'HELM', 'WAFFE', 'WAFFEN',
    'KRONE', 'THRON', 'REICH', 'REICHE', 'REICHEN',
    'GRAB', 'GRAEBER', 'GRUFT', 'GRUFTEN',
    'KERZE', 'KERZEN', 'LICHT', 'LICHTER',
    'NORDEN', 'SUEDEN', 'OSTEN', 'WESTEN',
    'EBENE', 'TAL', 'HUEGEL', 'GIPFEL',
    'QUELLE', 'FLUSS', 'STROM', 'MEER',
    'HOEHLE', 'GROTTE', 'TUNNEL',
    'TEMPEL', 'KIRCHE', 'KLOSTER',
    'TURM', 'TURME', 'TUERME', 'MAUER', 'MAUERN',
    'STRASSE', 'GASSE', 'BRUECKE', 'TOR',
    'BOTSCHAFT', 'BOTE', 'BOTEN',
    'SCHRIFT', 'SCHRIFTEN', 'ZEICHEN',
    'SEELE', 'SEELEN', 'GEIST', 'GEISTER',
    'SCHATTEN', 'SCHATTENS',
    # Adjectives
    'HEILIG', 'HEILIGE', 'HEILIGEN', 'HEILIGER',
    'DUNKEL', 'DUNKLE', 'DUNKLEN', 'DUNKLER',
    'EWIG', 'EWIGE', 'EWIGEN', 'EWIGER',
    'GROSS', 'GROSSE', 'GROSSEN', 'GROSSER', 'GROSSES',
    'KLEIN', 'KLEINE', 'KLEINEN', 'KLEINER',
    'STARK', 'STARKE', 'STARKEN', 'STARKER',
    'WEIT', 'WEITE', 'WEITEN', 'WEITER',
    'HOCH', 'HOHE', 'HOHEN', 'HOHER',
    'TIEF', 'TIEFE', 'TIEFEN', 'TIEFER',
    'LETZT', 'LETZTE', 'LETZTEN', 'LETZTER',
    'RECHT', 'RECHTE', 'RECHTEN', 'RECHTER',
    'WILD', 'WILDE', 'WILDEN', 'WILDER',
    'WAHR', 'WAHRE', 'WAHREN', 'WAHRER',
    'EDEL', 'EDLE', 'EDLEN', 'EDLER',
    'STOLZ', 'STOLZE', 'STOLZEN',
    'GERECHT', 'GERECHTE', 'GERECHTEN',
    'GRAUSAM', 'GRAUSAME', 'GRAUSAMEN',
    'VERBORGEN', 'VERBORGENE', 'VERBORGENEN',
    'VERGESSEN', 'VERGESSENE', 'VERGESSENEN',
    'VERFLUCHT', 'VERFLUCHTE', 'VERFLUCHTEN',
    # Adverbs/particles
    'DANN', 'DARUM', 'DAHER', 'DAVON', 'DARIN',
    'EINST', 'EINSTMALS', 'VORMALS',
    'DARAUF', 'DABEI', 'DARAN', 'DAHIN',
    'DAMALS', 'DEREINST', 'ENDLICH',
    'FORTAN', 'HINFORT', 'HINAUS',
    'STETS', 'IMMER', 'NIMMER', 'NIMMERMEHR',
    'WAHRLICH', 'WIRKLICH', 'SICHER',
    'ALLEIN', 'ZUMAL', 'FREILICH',
    'ZUDEM', 'AUSSER', 'DIESSEITS', 'JENSEITS',
    # Prepositions/conjunctions
    'WIDER', 'SAMT', 'NEBST', 'WEGEN', 'TROTZ',
    'BEVOR', 'NACHDEM', 'WAEHREND', 'INDEM', 'OBWOHL',
    'DAMIT', 'ALSO', 'DOCH', 'JEDOCH', 'DENNOCH',
    # MHG vocabulary
    'VROUWE', 'VROWE', 'WIP', 'RITTER', 'KUNIC', 'KUNEC',
    'MUOT', 'ERE', 'TUGENT', 'TRIUWE', 'STAETE',
    'MILTE', 'ZUHT', 'MASE', 'HOHE', 'MINNE',
    'VRIDE', 'FRIDE', 'STRIT', 'STREIT',
    'LEIT', 'LIEP', 'GUOT', 'BOESE',
    'GAN', 'GEN', 'STEN', 'LIGEN', 'SITZEN',
    'WELLEN', 'SULN', 'MUGEN', 'KUNNEN', 'TURREN',
    'DAZ', 'DEZ', 'NIHT', 'OUCH', 'ZER',
    'DESTE', 'NOCH', 'HARTE', 'SERE', 'WUNDER',
    'SALDE', 'SAELDE', 'HEIDE', 'WUNNE', 'WONNE',
    'MANEC', 'MANIG', 'DICKE', 'STARKE',
    'GESELLE', 'HERRE', 'KNABE', 'KNAPPE',
    'GEBAERDE', 'GEBAREN', 'WUNSCH',
    'VART', 'VAREN', 'RITEN', 'STRITEN',
    'STERBEN', 'GENESEN', 'GESUNT',
    'GELT', 'GULTE', 'SCHULDE',
    'BURC', 'STAT', 'HOLT', 'HEIDE',
    'BALDE', 'SCHIERE', 'IEMER', 'NIEMER',
    'HARTE', 'LISE', 'STILLE',
    'WISE', 'WEISE', 'MEISTER',
    'NAHT', 'MORGEN', 'ABENT',
    'RIUWE', 'KLAGE', 'TRAUER',
    'SWERT', 'SCHILT', 'SPER', 'BOGEN',
    'KEMENATE', 'HALLE', 'SAL',
    'BRUNNE', 'HELM', 'HALSBERC',
    'RECKE', 'DEGEN', 'WIGANT',
    'STIGE', 'STEC', 'BRUECKE',
    'ENT', 'WIDER', 'ZUO',
    # More MHG and archaic
    'SINT', 'SIDER', 'SEDERT', 'ALSE', 'ALSO',
    'DICKE', 'SELTEN', 'STUNDE', 'STUNDEN',
    'NAHT', 'TAGES', 'IARES', 'WINTER', 'SUMER',
    'TUNKEL', 'VINSTER', 'LIEHT', 'GLANTZ',
    'ERDE', 'ERDEN', 'HIMEL', 'HIMELS',
    'MERE', 'MERES', 'WAZZER', 'FIUR',
    'GEBOT', 'GEBOTEN', 'VERBOT', 'VERBOTEN',
    'GESETZ', 'GESETZE', 'URTEIL', 'URTEILE',
    'ZEUGEN', 'ZEUGE', 'SCHWUR', 'EIDLICH',
    'TAUFE', 'SALBUNG', 'WEIHUNG', 'OPFER',
    # Tibia-specific possibilities
    'BONELORD', 'HELLGATE', 'THAIS', 'TIBIA',
    'DEMONA', 'DREFIA', 'CARLIN', 'VENORE',
    'KAZORDOON', 'MINTWALLIN', 'ROOKGAARD',
    'EDRON', 'CORMAYA', 'FIBULA',
    'FERUMBRAS', 'ORSHABAAL', 'GHAZBARAN',
    'ZATHROTH', 'CRUNOR', 'TIBIASULA',
    'NECROMANT', 'NEKROMANT', 'UNTOT', 'UNTOTE', 'UNTOTEN',
]

# Also generate all 3-letter combinations that appear 3+ times
# and could be German syllables
print("\nScanning for frequent substrings not in KNOWN...")
substr_freq = Counter()
for length in range(3, 13):
    for i in range(len(processed) - length + 1):
        s = processed[i:i+length]
        if '?' not in s and s not in KNOWN:
            substr_freq[s] += 1

# Filter to frequent substrings
frequent = {s: c for s, c in substr_freq.items() if c >= 3 and len(s) >= 3}

# Combine all candidates
CANDIDATES = set(GERMAN_WORDS) | set(frequent.keys())

# Test each candidate
print(f"Testing {len(CANDIDATES)} candidates...")
gains = []
for word in CANDIDATES:
    if word in KNOWN or len(word) < 2:
        continue
    vocab2 = KNOWN | {word}
    cov2, _ = dp_segment(processed, vocab2)
    gain = cov2 - baseline_cov
    if gain > 0:
        # Find contexts
        contexts = []
        pos = 0
        while len(contexts) < 3:
            idx = processed.find(word, pos)
            if idx < 0:
                break
            s = max(0, idx - 8)
            e = min(len(processed), idx + len(word) + 8)
            contexts.append(processed[s:e])
            pos = idx + 1
        freq = processed.count(word)
        gains.append((gain, word, freq, contexts))

gains.sort(key=lambda x: -x[0])

print(f"\n{'='*60}")
print(f"NEW WORDS WITH COVERAGE GAIN (top 50)")
print(f"{'='*60}")
total_gain = 0
for gain, word, freq, contexts in gains[:50]:
    total_gain += gain
    print(f"\n  +{gain:3d} '{word}' ({freq}x)")
    for ctx in contexts[:2]:
        print(f"       ...{ctx}...")

print(f"\n{'='*60}")
print(f"SUMMARY")
print(f"{'='*60}")
print(f"Total words with gain: {len(gains)}")
print(f"Top 20 combined gain: {sum(g[0] for g in gains[:20])}")
print(f"All combined gain (greedy, non-overlapping): calculating...")

# Greedy non-overlapping application of top gains
combined_vocab = set(KNOWN)
running_cov = baseline_cov
for gain, word, freq, ctx in gains:
    test_vocab = combined_vocab | {word}
    test_cov, _ = dp_segment(processed, test_vocab)
    actual_gain = test_cov - running_cov
    if actual_gain > 0:
        combined_vocab.add(word)
        running_cov = test_cov

final_gain = running_cov - baseline_cov
print(f"Greedy combined gain: +{final_gain} ({baseline_cov} -> {running_cov}/{total} = {running_cov/total*100:.1f}%)")

# Show new words added
new_words = combined_vocab - KNOWN
print(f"\nNew words added ({len(new_words)}):")
for w in sorted(new_words, key=lambda x: -processed.count(x)):
    print(f"  '{w}' ({processed.count(w)}x)")

print("\nDone.")
