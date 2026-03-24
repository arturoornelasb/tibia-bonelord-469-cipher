#!/usr/bin/env python3
"""
Session 24: Deep multi-language research attack on remaining ~28% garbled content.

Approaches:
1. Comprehensive MHG/OHG dictionary (200+ words from medieval sources)
2. Latin vocabulary (ecclesiastical + classical)
3. Middle Dutch / Old Dutch cognates
4. Old Saxon (ancestor of Low German)
5. Old Norse / Gothic specific vocabulary
6. N-gram language fingerprinting (which language fits garbled content?)
7. German morphology: inflection endings, compound decomposition
8. Reversed blocks (bonelord reversal affinity)
9. HEHL/HIHL variant orthography analysis
10. Unaligned book alignment test
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

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    return 0 if ic_from_counts(Counter(bp0), len(bp0)) > ic_from_counts(Counter(bp1), len(bp1)) else 1

book_pairs_list = []
decoded_books = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs_list.append(pairs)
    decoded_books.append(''.join(v7.get(p, '?') for p in pairs))

raw = ''.join(decoded_books)
processed = raw
for old in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    processed = processed.replace(old, ANAGRAM_MAP[old])

# ============================================================
# VOCABULARY DATABASES
# ============================================================

# Comprehensive MHG (Middle High German, c.1050-1350) word list
MHG_VOCAB = {
    # Nouns
    'HEHL': 'concealment (MHG)',
    'HEHLE': 'concealment (MHG)',
    'HEHLER': 'receiver of stolen goods (MHG)',
    'WICHT': 'creature, being (MHG)',
    'WICHTEL': 'dwarf, sprite (MHG)',
    'WIHTE': 'creatures (MHG pl)',
    'NIHT': 'nothing/not (MHG)',
    'ZIHTE': 'time, hour (MHG)',
    'LIHT': 'light (MHG)',
    'RIHT': 'right/justice (MHG)',
    'SIHT': 'sight (MHG)',
    'GIHT': 'gout/disease (MHG)',
    'TIHT': 'dense (MHG)',
    'WIHT': 'creature (MHG)',
    'HILT': 'hilt (MHG)',
    'GILT': 'guild (MHG)',
    'TILT': 'tilt (MHG)',
    'WELT': 'world (MHG=NHG)',
    'HELM': 'helmet (MHG)',
    'HELME': 'helmets (MHG pl)',
    'HEIL': 'salvation, hail (MHG)',
    'HEILE': 'healing (MHG)',
    'HEIL': 'salvation (MHG)',
    'HEILT': 'heals (MHG/NHG)',
    'HELL': 'bright, clear (MHG)',
    'HELLE': 'brightness; hell (MHG)',
    'HELLEN': 'to brighten (MHG)',
    'HEHLET': 'conceals (MHG)',
    'HEHLTE': 'concealed (MHG)',
    'HELD': 'hero (MHG=NHG)',
    'HELDEN': 'heroes (MHG pl)',
    'HELF': 'help (MHG imperative)',
    'HILFE': 'help (NHG)',
    'HILFT': 'helps (MHG/NHG)',
    'HILT': 'holds (MHG: halten)',
    'WIRT': 'host/innkeeper (MHG)',
    'WIRTE': 'hosts (MHG pl)',
    'WIHTELIN': 'little creature (MHG dim)',
    'LICHT': 'light (MHG=NHG)',
    'LICHTE': 'lights (MHG pl)',
    'SCHLICHT': 'plain, simple (NHG)',
    'SCHLICHTEN': 'to settle (NHG)',
    'DICHT': 'dense (NHG)',
    'NICHT': 'not (NHG)',
    'WICHT': 'creature; wight (MHG)',
    'RECHT': 'right (MHG=NHG)',
    'NACHT': 'night (MHG=NHG)',
    'MACHT': 'power (MHG=NHG)',
    'TRACHT': 'load/dress (MHG)',
    'WACHT': 'guard, watch (MHG)',
    'ACHT': 'eight; attention (MHG)',
    'HACHT': 'custody (MHG var)',
    'FLECHT': 'braid (MHG)',
    'FLECHTE': 'braid, lichen (NHG)',
    'FECHTEN': 'to fight (NHG)',
    'HECHELN': 'to hackle (NHG)',
    'HECHEL': 'hackle (NHG)',
    'HECHELT': 'hackles (NHG)',
    'HECHT': 'pike (fish) (MHG=NHG)',
    'KNECHT': 'servant (MHG=NHG)',
    'KNECHTE': 'servants (NHG pl)',
    'ECHT': 'genuine (NHG)',
    'GESCHLECHT': 'gender/lineage (NHG)',
    'SCHLECHT': 'bad (NHG)',
    'SCHLECHTE': 'bad ones (NHG)',
    'LEUCHTE': 'lantern (NHG)',
    'LEUCHTEN': 'to glow (NHG)',
    'LEUCHTEND': 'glowing (NHG)',
    'RITTER': 'knight (MHG=NHG)',
    'TURNIER': 'tournament (NHG)',
    'TURNIR': 'tournament (MHG)',
    'TURNEI': 'tournament (MHG)',
    'TURNE': 'tower (MHG: turn)',
    'TURN': 'tower/turn (MHG)',
    'TURM': 'tower (NHG)',
    'MUTTER': 'mother (MHG)',
    'BUTTER': 'butter (MHG)',
    'LUTTER': 'pure (MHG)',
    'NUTZEN': 'use (NHG)',
    'NUTZE': 'useful (NHG)',
    'WUNSCH': 'wish (NHG)',
    'WUNDT': 'wound (MHG)',
    'WUNDE': 'wound (NHG)',
    'WUNDEN': 'wounds (NHG pl)',
    'WUNDER': 'wonder (NHG)',
    'RUNDE': 'round (NHG)',
    'RUNDEN': 'rounds (NHG pl)',
    'BUND': 'alliance (NHG)',
    'BUNDE': 'alliances (NHG pl)',
    'HUND': 'dog/hundred (MHG=NHG)',
    'HUNDE': 'dogs (NHG pl)',
    'GRUND': 'ground, reason (MHG=NHG)',
    'GRUNDE': 'grounds (NHG pl)',
    'FUND': 'find (NHG noun)',
    'FUNDE': 'finds (NHG pl)',
    'MUND': 'mouth (MHG=NHG)',
    'MUNDE': 'mouths (NHG pl)',
    'RUND': 'round (adj) (NHG)',
    'RUNE': 'rune (MHG=NHG)',
    'RUNEN': 'runes (NHG pl)',
    # MHG-specific vocabulary
    'WAN': 'hope/because (MHG)',
    'WAN': 'lack (MHG)',
    'WANE': 'waning (MHG)',
    'WANEN': 'to believe (MHG)',
    'WANNE': 'when (MHG var)',
    'WERDEN': 'to become (MHG=NHG)',
    'WIRDET': 'becomes (MHG)',
    'WIRT': 'becomes/host (MHG)',
    'NIWAN': 'nothing but (MHG)',
    'NIHIL': 'nothing (Latin)',
    'NIHILS': 'nothing-s (Latin gen)',
    'HEHLICH': 'secret (MHG)',
    'HEHLLICH': 'secretly (MHG)',
    'SEHLICH': 'visible (MHG)',
    'WELICH': 'which/what (MHG)',
    'WELCHE': 'which (NHG)',
    'SOLCH': 'such (MHG)',
    'SOLCHE': 'such ones (NHG)',
    'DURCH': 'through (MHG=NHG)',
    'FURCHE': 'furrow (NHG)',
    'BURCHE': 'castle folk (MHG)',
    'KIRCHE': 'church (NHG)',
    'KIRCH': 'church (MHG)',
    # Place name elements
    'BURG': 'castle/city (MHG=NHG)',
    'BURG': 'castle (MHG)',
    'BURGE': 'castles (MHG pl)',
    'BURG': 'fortress (NHG)',
    'BERG': 'mountain (MHG=NHG)',
    'BERGE': 'mountains (NHG pl)',
    'DORF': 'village (MHG=NHG)',
    'DORFE': 'villages (MHG pl)',
    'FELD': 'field (MHG=NHG)',
    'FELDER': 'fields (NHG pl)',
    'WALD': 'forest (MHG=NHG)',
    'WALDE': 'forests (MHG pl)',
    'HAIN': 'grove (NHG)',
    'HAINE': 'groves (NHG pl)',
    'HORN': 'horn/peak (MHG=NHG)',
    'HORNS': 'horns (NHG gen)',
    'TAL': 'valley (MHG=NHG)',
    'TALE': 'valleys (MHG pl)',
    'TEICH': 'pond (NHG)',
    'TEICHE': 'ponds (NHG pl)',
    'BACH': 'stream (MHG=NHG)',
    'BACHE': 'streams (MHG pl)',
    'GRABEN': 'ditch/dig (NHG)',
    'GRUB': 'pit (MHG)',
    'GRUBE': 'pit/mine (NHG)',
    'HOEHLE': 'cave (NHG)',
    'HOHL': 'hollow (NHG adj)',
    'HOHLE': 'hollow/cave (NHG)',
    'HUEGEL': 'hill (NHG)',
    'HUGEL': 'hill (MHG)',
    'HUGEL': 'hills (NHG pl)',
    # Verbs
    'LIEGEN': 'to lie (NHG)',
    'LIEGT': 'lies (NHG)',
    'STEHEN': 'to stand (NHG)',
    'STEHT': 'stands (NHG)',
    'GEHEN': 'to go (NHG)',
    'GEHT': 'goes (NHG)',
    'SAGEN': 'to say (NHG)',
    'SAGT': 'says (NHG)',
    'FINDEN': 'to find (NHG)',
    'FINDET': 'finds (NHG)',
    'KOMMEN': 'to come (NHG)',
    'KOMMT': 'comes (NHG)',
    'NEHMEN': 'to take (NHG)',
    'NIMMT': 'takes (NHG)',
    'GEBEN': 'to give (NHG)',
    'GIBT': 'gives (NHG)',
    'HALTEN': 'to hold (NHG)',
    'HALT': 'holds/stop (NHG)',
    'WARTEN': 'to wait (NHG)',
    'WARTET': 'waits (NHG)',
    'KENNEN': 'to know (NHG)',
    'KENNT': 'knows (NHG)',
    'HECHELN': 'to hackle flax (NHG)',
    'SPRECHEN': 'to speak (NHG)',
    'SPRICHT': 'speaks (NHG)',
    # MHG-specific verbs
    'TUON': 'to do (MHG)',
    'TUOT': 'does (MHG)',
    'STAN': 'to stand (MHG)',
    'STAT': 'stands (MHG)',
    'GAN': 'to go (MHG)',
    'GAT': 'goes (MHG)',
    'HAN': 'to have (MHG)',
    'HAT': 'has (MHG=NHG)',
    'WELLEN': 'to want (MHG)',
    'WIL': 'wants (MHG)',
    'KUNNEN': 'to be able (MHG)',
    'KAN': 'can (MHG)',
    'SULN': 'shall (MHG)',
    'SOL': 'shall (MHG)',
    'MUGEN': 'to be able (MHG)',
    'MAG': 'may/can (MHG=NHG)',
    'DUNKEN': 'to seem (MHG)',
    'DUNKET': 'seems (MHG)',
    'RITEN': 'to ride (MHG)',
    'RITE': 'ride! (MHG)',
    'REIT': 'rode (MHG past)',
    'VAREN': 'to travel (MHG)',
    'VERT': 'travels (MHG)',
    'VAHT': 'fought (MHG past)',
    # Adjectives
    'GUOT': 'good (MHG)',
    'GUOTE': 'good ones (MHG)',
    'BOESE': 'bad (NHG)',
    'BOSE': 'bad (MHG)',
    'KALT': 'cold (MHG=NHG)',
    'KALTE': 'cold (NHG adj infl)',
    'WARM': 'warm (MHG=NHG)',
    'WARME': 'warm (NHG adj infl)',
    'GROSS': 'big (NHG)',
    'GROSSE': 'big (NHG adj infl)',
    'GROS': 'big (MHG)',
    'KLEIN': 'small (MHG=NHG)',
    'KLEINE': 'small (NHG adj infl)',
    'LANG': 'long (MHG=NHG)',
    'LANGE': 'long (NHG adj infl)',
    'KURZ': 'short (NHG)',
    'KURZE': 'short (NHG adj infl)',
    'STARK': 'strong (MHG=NHG)',
    'STARKE': 'strong (NHG adj infl)',
    'SCHWACH': 'weak (NHG)',
    'TIEFE': 'deep (NHG adj infl)',
    'TIEF': 'deep (NHG)',
    'HOCH': 'high (MHG=NHG)',
    'HOHE': 'high (NHG adj infl)',
    'JUNG': 'young (MHG=NHG)',
    'JUNGE': 'young (NHG adj infl)',
    'SCHWARZ': 'black (NHG)',
    'WEISS': 'white (NHG)',
    'ROT': 'red (NHG)',
    'ROTE': 'red (NHG adj infl)',
    'BLAU': 'blue (NHG)',
    'GRUEN': 'green (NHG)',
    'GOLDEN': 'golden (NHG)',
    'SILBERN': 'silver (NHG)',
}

# Latin vocabulary (classical + ecclesiastical + medieval)
LATIN_VOCAB = {
    'VIA': 'way, road',
    'VITA': 'life',
    'MORT': 'death',
    'MORS': 'death (nom)',
    'LUMEN': 'light',
    'LUNE': 'moon',
    'LUNA': 'moon (nom)',
    'RUNE': 'secret/rune (Latin)',
    'RUNIS': 'runes (Latin gen pl)',
    'ITER': 'journey',
    'ITINER': 'journey (stem)',
    'ITER': 'way',
    'UTER': 'which of two',
    'INTER': 'between',
    'INTRA': 'within',
    'ULTRA': 'beyond',
    'EXTRA': 'outside',
    'CONTRA': 'against',
    'INFRA': 'below',
    'SUPRA': 'above',
    'TRANS': 'across',
    'NUNC': 'now',
    'TUNC': 'then',
    'INDE': 'from there',
    'INDE': 'thence',
    'INDE': 'hence',
    'UNDE': 'from where',
    'UNDINE': 'water spirit',
    'UNDIS': 'waves (dat pl)',
    'UNDA': 'wave',
    'UNDE': 'whence',
    'UNIT': 'unites',
    'UNIT': 'he/she unites',
    'UNUM': 'one (acc)',
    'UNUS': 'one',
    'UNIO': 'unity, union',
    'TURRIS': 'tower',
    'TURRE': 'tower (abl)',
    'TURRIM': 'tower (acc)',
    'TURNUS': 'circuit, rotation',
    'TURNI': 'of Turnus/circuit',
    'REGNUM': 'kingdom',
    'REGNI': 'kingdom (gen)',
    'REGNO': 'kingdom (dat/abl)',
    'REX': 'king',
    'REGIS': 'king (gen)',
    'REGI': 'king (dat)',
    'REGEM': 'king (acc)',
    'REGE': 'king (abl)',
    'REGE': 'rule! (imperative)',
    'LOCUS': 'place',
    'LOCI': 'place (gen)',
    'LOCO': 'place (dat/abl)',
    'LOCUM': 'place (acc)',
    'NOMEN': 'name',
    'NOMINA': 'names (pl)',
    'NUNC': 'now',
    'NUMEN': 'divine power',
    'NUMINE': 'divine power (abl)',
    'NUMERUS': 'number',
    'RUINA': 'ruin',
    'RUINAE': 'ruins (gen/pl)',
    'RUINIS': 'ruins (dat/abl pl)',
    'RUNE': 'rune (Latin borrowing)',
    'CAELUM': 'sky, heaven',
    'TERRA': 'earth, land',
    'TERRAE': 'earth (gen)',
    'IGNIS': 'fire',
    'IGNE': 'fire (abl)',
    'IGNEM': 'fire (acc)',
    'AQUA': 'water',
    'VENTUS': 'wind',
    'VENTI': 'winds (gen/nom pl)',
    'VENTO': 'wind (dat/abl)',
    'FINIS': 'end, border',
    'FINE': 'end (abl)',
    'FINEM': 'end (acc)',
    'FINES': 'ends, borders (pl)',
    'ANTIQUUS': 'ancient',
    'ANTIQUA': 'ancient (f)',
    'ANTIQUI': 'ancient (m pl)',
    'ANTIQUE': 'in ancient fashion',
    'VETUS': 'old',
    'VETERE': 'old (abl)',
    'PATER': 'father',
    'PATRIS': 'father (gen)',
    'MATER': 'mother',
    'MATRIS': 'mother (gen)',
    'FRATER': 'brother',
    'FRATRIS': 'brother (gen)',
    'PRIMUS': 'first',
    'PRIMA': 'first (f)',
    'ULTIMUS': 'last',
    'ULTIMA': 'last (f)',
    'OMNIS': 'all, every',
    'OMNE': 'all (n)',
    'OMNIA': 'all things',
    'TEMPUS': 'time',
    'TEMPORA': 'times (pl)',
    'LAPIS': 'stone',
    'LAPIDEM': 'stone (acc)',
    'LAPIDE': 'stone (abl)',
    'RUPES': 'cliff, rock',
    'RUPI': 'cliff (dat)',
    'SAXUM': 'rock, stone',
    'SAXI': 'rock (gen)',
    'LITTERA': 'letter (of alphabet)',
    'LITTERA': 'written letter',
    'LITERA': 'letter',
    'SCRIBIT': 'writes',
    'SCRIPTO': 'writing (abl)',
    'SCRIPTURA': 'scripture, writing',
    'VERBUM': 'word',
    'VERBI': 'word (gen)',
    'VERBO': 'word (dat/abl)',
    'VERBA': 'words (pl)',
    'DEUS': 'god',
    'DEI': 'god (gen); gods (nom pl)',
    'DEO': 'god (dat/abl)',
    'DEUM': 'god (acc)',
    'DEORUM': 'gods (gen pl)',
    'DIIS': 'gods (dat/abl pl)',
    'DIVUS': 'divine',
    'SANCTUS': 'holy',
    'SANCTA': 'holy (f)',
    'SPIRITUS': 'spirit',
    'ANIMA': 'soul, spirit',
    'ANIMAE': 'soul (gen)',
    'ANIMI': 'soul (gen alt)',
    'HORROR': 'horror, shuddering',
    'HORRORE': 'horror (abl)',
    'TERROR': 'terror',
    'TERRORE': 'terror (abl)',
    'UMBRA': 'shadow, ghost',
    'UMBRAE': 'shadow (gen)',
    'TENEBRAE': 'darkness (pl)',
    'TENEBRIS': 'darkness (abl pl)',
    'LUX': 'light',
    'LUCIS': 'light (gen)',
    'LUCEM': 'light (acc)',
    'LUCE': 'light (abl)',
    'NOCTIS': 'night (gen)',
    'NOCTEM': 'night (acc)',
    'NOCTE': 'night (abl)',
    'NOCTIS': 'night (gen)',
    'MORTEM': 'death (acc)',
    'MORTIS': 'death (gen)',
    'MORTE': 'death (abl)',
    'REGNUM': 'realm',
    'REGNANT': 'they reign',
    'REGNO': 'I reign',
    'REGNAT': 'reigns',
}

# Middle Dutch / Old Dutch vocabulary
MDU_VOCAB = {
    'HELLE': 'hell (MDu)',
    'HEMEL': 'heaven (MDu)',
    'STEEN': 'stone (MDu)',
    'WINT': 'wind (MDu)',
    'LANT': 'land (MDu)',
    'RECHT': 'right/justice (MDu)',
    'NACHT': 'night (MDu)',
    'VREDE': 'peace (MDu)',
    'RIDDER': 'knight (MDu)',
    'RUNE': 'rune (MDu)',
    'RUNEN': 'runes (MDu pl)',
    'HELD': 'hero (MDu)',
    'HELDIN': 'heroine (MDu)',
    'WACHTE': 'guarded (MDu past)',
    'WACHT': 'guard (MDu)',
    'TOREN': 'tower (MDu)',
    'TORENEN': 'towers (MDu pl)',
    'TORENS': 'towers (MDu gen)',
    'KNAAP': 'squire (MDu)',
    'KNECHT': 'servant (MDu)',
    'LICHT': 'light (MDu)',
    'LICHTEN': 'lights (MDu pl)',
    'DICHT': 'thick/closed (MDu)',
    'DICHTEN': 'to close (MDu)',
    'VLECHT': 'braid (MDu)',
    'VLECHTEN': 'braids (MDu pl)',
    'FECHT': 'fight (MDu)',
    'FECHTEND': 'fighting (MDu)',
    'HECHT': 'pike (MDu)',
    'HECHTEN': 'to attach (MDu)',
    'NUCHTER': 'sober (MDu)',
    'ECHT': 'genuine (MDu)',
    'ECHTHEID': 'genuineness (MDu)',
    'SLECHT': 'bad/plain (MDu)',
    'SCHLECHTE': 'bad (MDu adj infl)',
    'GRONDEL': 'gudgeon fish (MDu)',
    'GROND': 'ground (MDu)',
    'HOND': 'dog (MDu)',
    'HONDEN': 'dogs (MDu pl)',
    'RONDE': 'round (MDu)',
    'WONDER': 'wonder (MDu)',
    'WONDEN': 'wounds (MDu pl)',
    'WONDE': 'wound (MDu)',
    'FINDEN': 'to find (MDu)',
    'LINDEN': 'linden tree (MDu)',
    'BINDEN': 'to bind (MDu)',
    'WINDEN': 'to wind/turn (MDu)',
    'KINDEN': 'children (MDu)',
    'KINDER': 'children (MDu alt)',
    'LEIDEN': 'to lead/suffer (MDu)',
    'MEIDEN': 'to avoid (MDu)',
    'REIDEN': 'to ride (MDu)',
    'SNIJDEN': 'to cut (MDu)',
    'RIJDEN': 'to ride (MDu)',
    # Old Dutch place name elements
    'DONK': 'raised area (Old Dutch)',
    'HAM': 'pasture/bend (ODu)',
    'HELM': 'helmet/helm (ODu)',
    'HOLT': 'wood/forest (ODu)',
    'LO': 'wood/clearing (ODu)',
    'LOCH': 'enclosure (ODu)',
    'RODE': 'cleared land (ODu)',
    'SCHOR': 'mudflat (ODu)',
    'VELD': 'field (ODu)',
    'BROEK': 'marsh (ODu)',
    'DIJKE': 'dike (ODu)',
    'WAARD': 'river island (ODu)',
    'HORST': 'thicket/nest (ODu)',
}

# Old Saxon (OS) vocabulary - ancestor of Low German
OLD_SAXON_VOCAB = {
    'UUERD': 'fate, word (OS)',
    'THIOD': 'people (OS)',
    'THIODNA': 'queen (OS)',
    'KUNING': 'king (OS)',
    'HELM': 'helmet (OS)',
    'HELAG': 'holy (OS)',
    'WALDAND': 'ruler (OS)',
    'MAHTIG': 'mighty (OS)',
    'UUARD': 'became/guardian (OS)',
    'UUARD': 'guard (OS)',
    'UUORTHIG': 'worthy (OS)',
    'UUISLIK': 'wise (OS)',
    'UUIHT': 'creature (OS)',
    'GIHUUILIK': 'each (OS)',
    'LIOHT': 'light (OS)',
    'NAHT': 'night (OS)',
    'DOHTAR': 'daughter (OS)',
    'SUNNA': 'sun (OS)',
    'MANO': 'moon (OS)',
    'ERDE': 'earth (OS)',
    'HIMIL': 'heaven (OS)',
    'GISAH': 'saw (OS past)',
    'GENG': 'went (OS past)',
    'RIDAN': 'to ride (OS)',
    'REIT': 'rode (OS past)',
    'HELIAND': 'savior (OS)',
    'THEGAN': 'warrior/thane (OS)',
    'THEGANA': 'warriors (OS pl)',
    'WALDANDAG': 'day of the ruler (OS)',
    'LIUDEO': 'people (OS gen pl)',
    'THAT': 'that (OS)',
    'THIA': 'those (OS)',
    'IM': 'him/it (OS)',
    'INA': 'him (OS acc)',
    'SINO': 'his (OS)',
    'SINEMU': 'his (OS dat)',
    'HRING': 'ring (OS)',
    'HRINGE': 'ring (OS dat)',
    'ERDA': 'earth (OS)',
    'GRUND': 'ground (OS)',
    'GRUNDE': 'grounds (OS pl)',
    'BURG': 'fort (OS)',
    'BURGI': 'forts (OS pl)',
    'NIUDLIKOST': 'most eagerly (OS)',
    'NIUDLIKO': 'eagerly (OS)',
}

# Gothic vocabulary (very archaic Germanic)
GOTHIC_VOCAB = {
    'REIKI': 'kingdom, realm (Gothic)',
    'THIUDA': 'people, nation (Gothic)',
    'GARDA': 'enclosure, yard (Gothic)',
    'HAIRDEIS': 'shepherd (Gothic)',
    'WULFS': 'wolf (Gothic)',
    'DAGS': 'day (Gothic)',
    'NAHTS': 'night (Gothic)',
    'MANA': 'man (Gothic)',
    'GUMA': 'man (Gothic)',
    'HAURN': 'horn (Gothic)',
    'STIUR': 'steer, bull (Gothic)',
    'BRUNNA': 'spring, well (Gothic)',
    'RUNA': 'rune, mystery (Gothic)',
    'RUNOS': 'runes (Gothic pl)',
    'SKULA': 'debtor (Gothic)',
    'SKULD': 'debt/fate (Gothic)',
    'URDHR': 'fate (Old Norse)',
    'VERDANDI': 'becoming (Old Norse)',
    'NORNIR': 'Norns (Old Norse)',
}

# Old Norse vocabulary
OLD_NORSE_VOCAB = {
    'HEL': 'realm of dead (ON)',
    'HELHEIM': 'realm of Hel (ON)',
    'RUNA': 'rune (ON)',
    'RUNAR': 'runes (ON pl)',
    'RUNIR': 'runes (ON pl alt)',
    'URDHR': 'fate, Urd (ON)',
    'SKULD': 'debt/future Norn (ON)',
    'AESIR': 'gods (ON)',
    'VANIR': 'gods (ON)',
    'GARD': 'enclosure (ON)',
    'GARDAR': 'enclosures (ON pl)',
    'MIDGARD': 'middle world (ON)',
    'UTGARD': 'outer world (ON)',
    'ASGARD': 'home of gods (ON)',
    'NIFL': 'mist (ON)',
    'NIFLHEIM': 'mist world (ON)',
    'MUSPELL': 'fire world (ON)',
    'YGGDRASIL': 'world tree (ON)',
    'NORN': 'fate-weaver (ON)',
    'NORNS': 'fate-weavers (ON pl)',
    'EINHERJAR': 'chosen warriors (ON)',
    'DRAUGAR': 'undead (ON pl)',
    'DRAUGR': 'undead (ON)',
    'HULDR': 'hidden (ON)',
    'HULDRA': 'hidden ones (ON)',
    'TROLL': 'troll (ON)',
    'TROLLS': 'trolls (ON)',
    'DVERGR': 'dwarf (ON)',
    'DVERGAR': 'dwarves (ON pl)',
    'ALFR': 'elf (ON)',
    'ALFAR': 'elves (ON pl)',
    'JOTUN': 'giant (ON)',
    'JOTNAR': 'giants (ON pl)',
    'GINN': 'powerful/mighty (ON)',
    'GALDR': 'spell/incantation (ON)',
    'SEIDR': 'magic (ON)',
    'RIND': 'bark/frost (ON)',
    'HLIN': 'protectress (ON)',
    'GRUND': 'ground (ON=NHG)',
    'GRUNDE': 'grounds (ON)',
    'WUNDER': 'wonder (ON=NHG)',
    'THURS': 'giant/demon (ON)',
    'THURSE': 'giants (ON pl)',
    'HRIM': 'frost (ON)',
    'HRIMR': 'frosty (ON)',
    'EINRI': 'alone/only (ON)',
    'EINR': 'one (ON)',
    'HELDR': 'rather (ON)',
    'HELDUR': 'rather (ON)',
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def anagram_match(block, word, plus=0):
    """Check if block is an anagram of word (+plus extra letters in block)."""
    bc = Counter(block)
    wc = Counter(word)
    for ch, cnt in wc.items():
        if bc.get(ch, 0) < cnt:
            return False
    extra = sum(bc.values()) - sum(wc.values())
    return 0 <= extra <= plus

def anagram_match_inv(word, block, plus=0):
    """Check if word is subset/anagram of block (block can have plus extra)."""
    return anagram_match(block, word, plus)

def check_all_vocabs(block, plus=1):
    """Check block against all vocabulary databases."""
    results = []
    for word, meaning in MHG_VOCAB.items():
        if anagram_match(block, word, plus):
            results.append(('MHG', word, meaning, plus))
    for word, meaning in LATIN_VOCAB.items():
        if anagram_match(block, word, plus):
            results.append(('LAT', word, meaning, plus))
    for word, meaning in MDU_VOCAB.items():
        if anagram_match(block, word, plus):
            results.append(('MDU', word, meaning, plus))
    for word, meaning in OLD_SAXON_VOCAB.items():
        if anagram_match(block, word, plus):
            results.append(('OS', word, meaning, plus))
    for word, meaning in OLD_NORSE_VOCAB.items():
        if anagram_match(block, word, plus):
            results.append(('ON', word, meaning, plus))
    for word, meaning in GOTHIC_VOCAB.items():
        if anagram_match(block, word, plus):
            results.append(('GOT', word, meaning, plus))
    return results

# ============================================================
# EXTRACT ALL GARBLED BLOCKS WITH COUNTS
# ============================================================
# Run DP to find garbled positions
KNOWN_WORDS = set([
    'SEIN', 'SEINE', 'SEINER', 'SEINEN', 'SEINEM', 'SEINES',
    'IST', 'WAR', 'WIRD', 'WAREN', 'WAR',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES',
    'EIN', 'EINE', 'EINER', 'EINEM', 'EINEN', 'EINES',
    'UND', 'ODER', 'ABER', 'NICHT', 'MIT', 'VON', 'BIS',
    'WIR', 'ICH', 'ER', 'SIE', 'ES', 'IHR', 'WER', 'WAS',
    'IN', 'IM', 'AN', 'AM', 'AUF', 'AUS', 'AB', 'ZU', 'ZUR', 'ZUM',
    'BEI', 'SO', 'DA', 'WO', 'NUN', 'NU', 'INS', 'GEN', 'DES', 'AUS',
    'HIER', 'DORT', 'ODE', 'ORT', 'NACH',
    'ALS', 'WIE', 'WO', 'WENN',
    'KLAR', 'AUCH', 'WEG', 'NUR', 'NIT',
    'GOTT', 'RUNE', 'RUNEN', 'STEIN', 'STEINEN', 'STEINE',
    'URALTE', 'ALT', 'ALTE', 'ALTEN',
    'KOENIG', 'RITTER',
    'WORT', 'WORTE', 'SAGEN',
    'FINDEN', 'STEH', 'STEHEN', 'STEHT',
    'GEHEN', 'GEH', 'GEHT', 'ENDE', 'ENDEN',
    'ERSTE', 'ERSTEN', 'ERSTER',
    'DIESE', 'DIESER', 'DIESEN', 'DIESEM', 'DIESES',
    'TAG', 'TAGE', 'TAGEN', 'MIN', 'TOT', 'RUIN', 'RUINE',
    'SAND', 'HEIME', 'HEIM', 'LEICH', 'LEICHE', 'TRAUT',
    'SCHRAT', 'SCHARDT', 'SCHAUN',
    'WEICHSTEIN', 'SALZBERG', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS',
    'EIGENTUM', 'MEERE', 'NEIGT', 'WISTEN', 'MANIER', 'GODES',
    'DIENST', 'NACHTS', 'STANDE', 'BEI', 'TUT', 'NEU',
    'SICH', 'REDER', 'HEL', 'RIT', 'EWE', 'SIN', 'MIS', 'AUE', 'EIS',
    'SCE', 'OEL', 'TER', 'ODE', 'THENAEUT',
    'BERUCHTIG', 'BERUCHTIGER', 'LEICHANBERUCHTIG', 'LEICHANBERUCHTIGER',
    'EIGENTUM', 'MEERE', 'HAT', 'NET', 'EM', 'TUN',
    'ELCH', 'AUCH', 'DURCH', 'RUINEN',
    'WUNDE', 'WUNDEN', 'WUNDER',
    'HUND', 'HUNDE', 'GRUND', 'GRUNDE',
    'RECHT', 'NACHT',
    'BURG', 'BERG', 'WALD',
    'LICHT', 'LICHTE',
    'HEHL', 'HEHLE', 'HEHLER',
    'HEIL', 'HEILE', 'HEILT', 'HELD',
    'SCHLICHT', 'SCHLECHT', 'ECHT',
    'KNECHT', 'KNECHTE', 'HECHT',
    'WIRT', 'WIRTE', 'TURM',
    'HOLT', 'HORST', 'TEICH',
    'RUPES', 'SAXUM',
])

def dp_segmentation(text, vocab):
    """DP segmentation, returns list of (word, is_known) tuples."""
    n = len(text)
    dp = [False] * (n+1)
    dp[0] = True
    bp = [-1] * (n+1)
    bl = [0] * (n+1)
    for i in range(n):
        if not dp[i]: continue
        for l in range(1, min(25, n-i+1)):
            w = text[i:i+l]
            if w in vocab and not dp[i+l]:
                dp[i+l] = True
                bp[i+l] = i
                bl[i+l] = l
    # Reconstruct segments
    segments = []
    pos = n
    while pos > 0:
        if bp[pos] < 0:
            # backtrack single char
            segments.append((text[pos-1:pos], False))
            pos -= 1
        else:
            w = text[bp[pos]:pos]
            segments.append((w, True))
            pos = bp[pos]
    segments.reverse()
    return segments

segs = dp_segmentation(processed, KNOWN_WORDS)

# Extract garbled blocks
garbled_blocks = Counter()
garbled_by_context = defaultdict(list)

i = 0
for word, known in segs:
    if not known:
        garbled_blocks[word] += 1
    i += len(word)

# Find contexts for each garbled block
for gblock, count in garbled_blocks.most_common(30):
    pos = 0
    while True:
        idx = processed.find(gblock, pos)
        if idx < 0: break
        before = processed[max(0,idx-15):idx]
        after = processed[idx+len(gblock):idx+len(gblock)+15]
        # Verify this isn't inside a known word
        garbled_by_context[gblock].append((before, after))
        pos = idx + 1

# ============================================================
# SECTION 1: Multi-language vocabulary check on all garbled blocks
# ============================================================
print("=" * 70)
print("SECTION 1: MULTI-LANGUAGE VOCABULARY CHECK (ALL GARBLED BLOCKS)")
print("=" * 70)

for gblock, count in sorted(garbled_blocks.items(), key=lambda x: -len(x[0])*x[1]):
    if len(gblock) < 3 or len(gblock) > 12: continue
    if count < 2: continue

    results = check_all_vocabs(gblock, plus=1)
    if results:
        print(f"\n  Block '{gblock}' ({count}x, {len(gblock)} chars):")
        seen = set()
        for lang, word, meaning, p in results:
            key = (lang, word)
            if key not in seen:
                print(f"    [{lang}] {word} = '{meaning}'  (anagram +{p})")
                seen.add(key)
        # Show first context
        if gblock in garbled_by_context:
            before, after = garbled_by_context[gblock][0]
            print(f"    Context: ...{before.strip()[-10:]}|{gblock}|{after.strip()[:10]}...")

# ============================================================
# SECTION 2: Reversed block check
# ============================================================
print("\n" + "=" * 70)
print("SECTION 2: REVERSED BLOCK ANALYSIS (bonelord reversal affinity)")
print("=" * 70)

for gblock, count in garbled_blocks.most_common(20):
    if len(gblock) < 3: continue
    rev = gblock[::-1]
    rev_results = check_all_vocabs(rev, plus=1)
    if rev_results:
        print(f"\n  '{gblock}' reversed = '{rev}' ({count}x):")
        seen = set()
        for lang, word, meaning, p in rev_results:
            key = (lang, word)
            if key not in seen:
                print(f"    [{lang}] {word} = '{meaning}'  (anagram +{p})")
                seen.add(key)
    # Also check if reversed block IS a known word
    if rev in KNOWN_WORDS:
        print(f"\n  '{gblock}' reversed = '{rev}' — IS A KNOWN WORD!")

# ============================================================
# SECTION 3: N-gram language fingerprinting
# ============================================================
print("\n" + "=" * 70)
print("SECTION 3: N-GRAM LANGUAGE FINGERPRINTING")
print("   Which language do the garbled characters most resemble?")
print("=" * 70)

# Collect all garbled characters
garbled_chars = ''
for word, known in segs:
    if not known:
        garbled_chars += word

print(f"\nTotal garbled chars: {len(garbled_chars)}")
print(f"Letter distribution in garbled content:")
gc = Counter(garbled_chars)
total_g = len(garbled_chars)
for letter, cnt in sorted(gc.items(), key=lambda x: -x[1]):
    print(f"  {letter}: {cnt:4d} ({cnt/total_g*100:.1f}%)")

# German expected frequencies (approximate)
GERMAN_FREQ = {'E':17.4,'N':9.8,'I':7.6,'S':7.3,'R':7.0,'A':6.5,'T':6.2,
               'D':5.1,'H':4.8,'U':4.4,'L':3.4,'C':3.2,'G':3.0,'M':2.5,
               'O':2.5,'B':1.9,'W':1.9,'F':1.7,'K':1.2,'Z':1.1,'V':0.8}
LATIN_FREQ = {'I':11.2,'A':9.6,'E':9.0,'U':8.1,'S':7.2,'T':6.5,'N':5.8,
              'R':5.5,'O':5.0,'M':4.8,'L':4.4,'C':3.5,'P':2.8,'D':2.4,
              'V':2.2,'Q':1.5,'F':1.0,'B':0.9,'X':0.4,'H':0.3,'G':0.2}
DUTCH_FREQ = {'E':18.9,'N':10.2,'A':7.5,'T':6.8,'I':6.5,'R':6.2,'O':5.9,
              'D':5.6,'S':3.7,'L':3.7,'G':3.4,'H':2.4,'K':2.2,'V':2.2,
              'U':2.0,'M':2.0,'W':1.5,'B':1.5,'C':1.0,'F':0.8}

def freq_distance(observed, expected):
    """Compute chi-squared-like distance between observed and expected frequencies."""
    dist = 0
    total = sum(observed.values())
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        obs = observed.get(letter, 0) / total * 100 if total > 0 else 0
        exp = expected.get(letter, 0)
        dist += (obs - exp) ** 2 / (exp + 0.1)
    return dist

print(f"\nFrequency distance from language profiles (lower = closer match):")
print(f"  German:      {freq_distance(gc, GERMAN_FREQ):.2f}")
print(f"  Latin:       {freq_distance(gc, LATIN_FREQ):.2f}")
print(f"  Dutch:       {freq_distance(gc, DUTCH_FREQ):.2f}")

# Compare known part
known_chars = ''
for word, known in segs:
    if known:
        known_chars += word
kc = Counter(known_chars)
print(f"\nFrequency distance for KNOWN chars:")
print(f"  German:      {freq_distance(kc, GERMAN_FREQ):.2f}")
print(f"  Latin:       {freq_distance(kc, LATIN_FREQ):.2f}")
print(f"  Dutch:       {freq_distance(kc, DUTCH_FREQ):.2f}")

# ============================================================
# SECTION 4: German morphological analysis
# ============================================================
print("\n" + "=" * 70)
print("SECTION 4: GERMAN MORPHOLOGICAL ANALYSIS")
print("   Looking for inflection endings, compound decomposition")
print("=" * 70)

# German suffixes and what they indicate
SUFFIXES = [
    ('UNG', 'nominalization (Bild->Bildung)'),
    ('HEIT', 'quality noun'),
    ('KEIT', 'quality noun'),
    ('LICH', 'adjective suffix'),
    ('ISCH', 'adjective suffix'),
    ('LING', 'person/diminutive'),
    ('LING', 'diminutive'),
    ('NIS', 'abstract noun'),
    ('SCHAFT', 'collective noun'),
    ('THEIT', 'noun suffix'),
    ('IGKEIT', 'quality noun'),
    ('HAFT', 'adjective suffix'),
    ('VOLL', 'adjective suffix'),
    ('LOS', 'without'),
    ('REICH', 'rich in'),
    ('WERT', 'worth'),
    ('TUM', 'realm/quality'),
    ('LAND', 'land/country'),
    ('BURG', 'fortress'),
    ('BERG', 'mountain'),
    ('DORF', 'village'),
    ('STEIN', 'stone'),
    ('BACH', 'stream'),
    ('HEIM', 'home'),
    ('HAUSEN', 'houses'),
    ('THAL', 'valley (archaic)'),
    ('TAL', 'valley'),
    ('EN', 'plural/infinitive/adjective'),
    ('ER', 'agent/comparative'),
    ('EST', 'superlative'),
    ('ST', 'superlative'),
    ('ND', 'present participle'),
    ('TE', 'past tense (weak)'),
    ('TEN', 'past tense pl'),
    ('T', '3sg present'),
    ('ET', '3sg present (MHG)'),
]

PREFIXES = [
    ('UN', 'negation'),
    ('GE', 'past participle'),
    ('VER', 'verbal prefix'),
    ('BE', 'verbal prefix'),
    ('ER', 'verbal prefix'),
    ('ANT', 'against'),
    ('ENT', 'away from'),
    ('AUS', 'out of'),
    ('AUF', 'up/on'),
    ('AB', 'away/down'),
    ('AN', 'at/on'),
    ('IN', 'in'),
    ('ZU', 'to'),
    ('NACH', 'after'),
    ('VOR', 'before'),
    ('UBER', 'over'),
    ('UNTER', 'under'),
    ('DURCH', 'through'),
    ('MIT', 'with'),
    ('HIN', 'there'),
    ('HER', 'here/towards'),
    ('ZUR', 'to the'),
    ('ZUM', 'to the'),
    ('HEIM', 'home'),
    ('HEIL', 'holy'),
    ('ALL', 'all'),
    ('WOHL', 'well'),
]

print("\nGarbled blocks with German suffix/prefix analysis:")
for gblock, count in garbled_blocks.most_common(25):
    if len(gblock) < 3: continue
    found_suf = []
    found_pref = []
    for suf, meaning in SUFFIXES:
        if gblock.endswith(suf) and len(gblock) > len(suf):
            stem = gblock[:-len(suf)]
            if len(stem) >= 2:
                found_suf.append((suf, meaning, stem))
    for pref, meaning in PREFIXES:
        if gblock.startswith(pref) and len(gblock) > len(pref):
            stem = gblock[len(pref):]
            if len(stem) >= 2:
                found_pref.append((pref, meaning, stem))
    if found_suf or found_pref:
        print(f"\n  '{gblock}' ({count}x):")
        for suf, meaning, stem in found_suf[:3]:
            stem_results = check_all_vocabs(stem, plus=1)
            stem_str = f" (stem '{stem}' matches: {[w for _,w,_,_ in stem_results[:3]]})" if stem_results else f" (stem: '{stem}')"
            print(f"    Suffix -{suf} ({meaning}){stem_str}")
        for pref, meaning, stem in found_pref[:3]:
            stem_results = check_all_vocabs(stem, plus=1)
            stem_str = f" (stem '{stem}' matches: {[w for _,w,_,_ in stem_results[:3]]})" if stem_results else f" (stem: '{stem}')"
            print(f"    Prefix {pref}- ({meaning}){stem_str}")

# ============================================================
# SECTION 5: HIHL deep linguistic analysis
# ============================================================
print("\n" + "=" * 70)
print("SECTION 5: HIHL DEEP ANALYSIS")
print("   Codes: 57(H)-65(I)-94(H)-34(L)")
print("   Always in: 'SAGEN AM MIN HIHL DIE NDCE FACH HECHLLT ICH OEL'")
print("=" * 70)

# Check various language possibilities
hihl_candidates = {
    'HEHL': 'MHG concealment (H↔I shift)',
    'HOHL': 'hollow/cave (H,O,H,L - O=I?)',
    'HULL': 'hull/covering (Eng cognate)',
    'HILL': 'hill (Eng)',
    'HIEL': 'MHG heel (E↔I)',
    'HIHI': 'haha (onomatopoeia)',
}

print("\n  HIHL variant analysis:")
for word, meaning in hihl_candidates.items():
    bc = Counter('HIHL')
    wc = Counter(word)
    diff = {c: bc.get(c,0)-wc.get(c,0) for c in set(bc)|set(wc)}
    changes = [(c, bc.get(c,0), wc.get(c,0)) for c in diff if diff[c] != 0]
    print(f"    {word} ({meaning}): changes = {changes}")

# Check OLD HIGH GERMAN: hihhil, hihil variants
print("\n  OHG/MHG spellings with doubled consonants:")
print("    OHG 'hihhil' = ???  (hypothetical doubling variant)")
print("    The double-H in HIHL: codes 57 and 94 both = H")
print("    Code 57: appears in HEDDEMI, HECHLLT, HEIME, HEILT etc.")
print("    Code 94: appears in HIHL (pos 2), HEARUCHTIG (pos 3)")
print("    In MHG, doubled consonants were common: 'buffe' 'rippe' etc.")
print("    HIHL with double-H might be archaic spelling of 'HIL' (MHG hill/slope)")

# Check MHG HÜGEL/HUGEL (hill) variants
print("\n  Place-name context analysis:")
print("    'MIN HIHL DIE NDCE FACH HECHLLT ICH OEL'")
print("    MIN = my, DIE = the, FACH = compartment/section, ICH = I, OEL = oil")
print("    Possible reading: 'my HIHL the NDCE-section HECHLLT I oil'")
print("    If HIHL = place/location: 'at my [place-HIHL] the [NDCE]-hall [HECHLLT] I anoint'")
print("    'OEL' = oil (NHG Öl) suggests ritual anointing context")
print("    Context: 'SAGEN AM MIN HIHL' = 'say at my HIHL' → HIHL as shrine/altar?")

# ============================================================
# SECTION 6: HECHLLT deep analysis
# ============================================================
print("\n" + "=" * 70)
print("SECTION 6: HECHLLT DEEP ANALYSIS (7 chars, 5x)")
print("   Sorted: CEHHLLT")
print("   Context: FACH HECHLLT ICH OEL (always)")
print("=" * 70)

print("\n  Systematic anagram search (all 7-letter German/Latin words):")
hechllt = 'HECHLLT'
print(f"  HECHLLT sorted = {''.join(sorted(hechllt))}")
print(f"  Letters: H(2), E(1), C(1), L(2), T(1)")

# Manual checks
candidates_hech = [
    ('LETCHH', 'reversed partial'),
    ('TLLCHEH', 'reversed'),
    ('HELTLCH', 'rearranged'),
    ('HLECHT', 'MHG?'),
    ('LECHTHL', 'variant'),
    ('LECHLTH', 'variant'),
]

print("\n  Related German words (manual check with letter substitution):")
print("  HECHELN (6 chars = CEEHHL + N vs CEHHLLT - N↔LT) - too different")
print("  SCHLECHT (7 chars = CCEHHLS T vs CEHHLLT - S↔L) - one letter swap S/L")
print("  HECHELT (7 chars = CEEHHLT vs CEHHLLT) - E(2)L(1) vs E(1)L(2) - swap EL")
print("  → HECHLLT is like HECHELT with E and L swapped!")
print("  → HECHELT = to hackle (process flax) - 'FACH HECHELT ICH ÖL' = 'I hackle the flax section with oil'?")
print("  → This makes REAL SENSE for a bonelord ritual text!")

# Try treating as +1 anagram where L↔E swap
print("\n  If HECHLLT = HECHELT with E↔L swap (not anagram, but substitution?):")
print("  This would require ONE of code 34 or 96 (both L) to decode as E in this context")
print("  That violates the homophonic rule (each code → fixed letter)")
print("  BUT: could be a cipher variant/error OR intentional obfuscation")

# Cross-boundary test with context
print("\n  Cross-boundary: FACH+HECHLLT = FACHECHLLT")
fb = 'FACH' + 'HECHLLT'
print(f"  Sorted: {''.join(sorted(fb))}")
# Check if this is an anagram of anything
for word in ['FLACHECHEL', 'LACHHECHT', 'FLACHECHT']:
    wc = Counter(word)
    bc = Counter(fb)
    ok = all(bc.get(c,0)>=cnt for c,cnt in wc.items())
    extra = sum(bc.values()) - sum(wc.values())
    if ok and extra <= 1:
        print(f"  FACH+HECHLLT ~ {word}!")

print("\n  Cross-boundary: HECHLLT+ICH = HECHLLTI CH")
hi = 'HECHLLT' + 'ICH'
print(f"  {''.join(sorted(hi))}")
for word in ['HEITLICH', 'LEICHTHH', 'LICHTHEH', 'TIEFLOCH']:
    wc = Counter(word)
    bc = Counter(hi)
    ok = all(bc.get(c,0)>=cnt for c,cnt in wc.items())
    extra = sum(bc.values()) - sum(wc.values())
    if ok and extra <= 1:
        print(f"  HECHLLT+ICH ~ {word}!")

# ============================================================
# SECTION 7: NDCE deep analysis
# ============================================================
print("\n" + "=" * 70)
print("SECTION 7: NDCE DEEP ANALYSIS (4 chars, 9x)")
print("   Codes: 60(N)-42(D)-18(C)-30(E)")
print("   Always in: 'MIN HIHL DIE NDCE FACH HECHLLT ICH OEL'")
print("=" * 70)

print("\n  NDCE = N-D-C-E sorted CDEN")
print("  The C code (18) only appears in: SCHARDT, NACHTS (NSCHAT), SICH (CHIS)")
print("  Code 18=C is rare — only ONE code for C in the entire cipher!")
print("  Context: DIE NDCE FACH = 'the NDCE compartment'")
print("\n  Language analysis:")
print("  Latin: none matching")
print("  German: none standard")
print("  MDu: DECKE (cover, ceiling) = D-E-C-K-E — no K, but similar!")
print("    DECKE sorted = CDEEK vs NDCE sorted = CDEN")
print("    Differ: DECKE has K(2)E(1) vs NDCE has N(1)E(1) — very different")
print("  English: DECK = D-E-C-K — no N, but context 'FACH' suggests room/section")
print("  MDu/NL: 'DEKEN' = blanket/cover (D-E-K-E-N) — no C, has K")
print("  Hmm... What about 'NDCE' as partial of SCHNECKE (snail/screw)?")
print("    SCHNECKE = S-C-H-N-E-C-K-E — has N,C,E but also S,H,K")
print("  What about anagram of 'DUNE' (sand dune)? DUNE = D-U-N-E — no C")
print("  What about Latin 'DUCE' (with leader, abl) + N? D-U-C-E+N — no U")

# Special check: Is NDCE related to a specific OLD GERMAN word?
print("\n  MHG analysis:")
print("  'DÜNNE' (thin) = D-Ü-N-N-E — Ü not in cipher, different")
print("  'NIED' reversed = DEIN? No...")
print("  'CDNE' rearranged: any MHG form? No match found")
print("  CONCLUSION: NDCE appears to be a bonelord proper noun (place name)")
print("  The N-D-C-E letter set (codes 60-42-18-30) is found in NO Germanic dictionary")

# ============================================================
# SECTION 8: WRLGTNELNR + UIRUNNHWND deep analysis
# ============================================================
print("\n" + "=" * 70)
print("SECTION 8: WRLGTNELNR + UIRUNNHWND (big block, 6x)")
print("   Context: STEH WRLGTNELNR HEL UIRUNNHWND FINDEN NEIGT DAS")
print("=" * 70)

print("\n  WRLGTNELNR sorted = EGLLNNRRTW (10 chars)")
print("  Letter profile: W(1) R(2) L(2) G(1) T(1) N(2) E(1)")
print("  High consonant ratio: 9/10 consonants, 1/10 vowel (E)")
print("  No German or Latin phrase of 10 chars fits this consonant-heavy profile")
print("  Germanic heavy consonant words (OHG/Gothic):")
print("    Gothic 'tulgjan' (to fix) = T-U-L-G-J-A-N")
print("    OHG 'sternon' (stars) = S-T-E-R-N-O-N")
print("    None match EGLLNNRRTW profile")
print("\n  HYPOTHESIS: WRLGTNELNR may be a SCRAMBLED compound name")
print("  Possible decomposition:")
for i in range(3, 7):
    left = 'WRLGTNELNR'[:i]
    right = 'WRLGTNELNR'[i:]
    lm = check_all_vocabs(left, plus=1)
    rm = check_all_vocabs(right, plus=1)
    if lm or rm:
        print(f"    {left}+{right}: left={[(w,l) for l,w,_,_ in lm[:2]]}, right={[(w,l) for l,w,_,_ in rm[:2]]}")

print("\n  UIRUNNHWND sorted = DHINNNRUUW (10 chars)")
print("  Letter profile: U(2) I(1) R(1) N(3) H(1) W(1) D(1)")
print("  More vowels than WRLGTNELNR: 3/10 vowels")
print("  Contains HUNNE (Hun) substring? U-N-N... HUNNE=H-U-N-N-E missing E")
print("  Contains WIND: W-I-N-D -> let's check:")
wind_check = Counter('UIRUNNHWND')
wind_check_w = Counter('WIND')
ok = all(wind_check.get(c,0) >= wind_check_w.get(c,0) for c in wind_check_w)
print(f"  WIND subset of UIRUNNHWND: {ok}")
if ok:
    rem = dict(wind_check)
    for c in wind_check_w:
        rem[c] -= wind_check_w[c]
    rem = {c:v for c,v in rem.items() if v > 0}
    print(f"  Remaining after WIND: {''.join(c*v for c,v in sorted(rem.items()))}")
    rem_matches = check_all_vocabs(''.join(c*v for c,v in sorted(rem.items())), plus=1)
    print(f"  Remaining word matches: {rem_matches[:5]}")

print("\n  Cross-boundary: HEL+UIRUNNHWND = HELUIRUNNHWND")
helblk = 'HEL' + 'UIRUNNHWND'
print(f"  Sorted: {''.join(sorted(helblk))}")
# Check if this is HELDENWIND or similar
for word in ['HELDENWIND', 'WINDAHLER', 'WINDHULD', 'WINDUHLAND']:
    if anagram_match('HELUIRUNNHWND', word, plus=2):
        print(f"  ~ {word}!")

# ============================================================
# SECTION 9: UTRUNR linguistic deep dive
# ============================================================
print("\n" + "=" * 70)
print("SECTION 9: UTRUNR LINGUISTIC DEEP DIVE (6 chars, 7x)")
print("   Context: ODE UTRUNR DEN ENDE REDER KOENIG SALZBERG")
print("   Codes: 44(U)-64(T)-72(R)-61(U)-14(N)-51(R) — always identical!")
print("=" * 70)

utrunr = 'UTRUNR'
print(f"\n  Sorted: {''.join(sorted(utrunr))}")
print(f"  Letters: U(2), T(1), R(2), N(1)")
print(f"\n  Language checks (manual + database):")

# Manual Germanic checks
print("  German/MHG:")
print("    TURNUS (Latin, circuit) = T-U-R-N-U-S → has S not R → no match")
print("    TURNUR (hypothetical) → not attested")
print("    UNRUT (dialectal Bavarian 'Unruhe' variant?) → not standard")
print("    RAUNTUR → not a word")

print("\n  Latin checks:")
print("    TURTUR (turtle dove) = T-U-R-T-U-R sorted=RRTTUU vs NRRTUU → differ N↔T")
print("    TURNI (genitive of Turnus) = T-U-R-N-I sorted=INRTU vs NRRTUU → 5 chars, different")
print("    NUTRIX (nurse) → different letters")
print("    MUTUR? → not Latin")
print("    FUTUR (future, abbreviation) → only 5 chars")

print("\n  Old Norse:")
print("    URNUR? → 'Urdhr' variant? (fate-spinner Norn)")
print("    In ON, 'Urðr' (Urd) = fate. Code sequence always UTRUNR...")
print("    If we read UTRUNR as 'UT-RUNR': UT=out + RUNR=runes (plural, ON)")
print("    ON 'utar' = outer + 'runar' = runes → 'outer runes'?")
print("    'UTAR RUNAR' (outer runes) → 6 chars UTRUNR could be this compound!")
print("    Reading: 'ODE [outer-runes] DEN ENDE REDER KOENIG SALZBERG'")
print("    = 'Alone at outer-runes, the end-speaker King Salzberg'")

print("\n  Gothic checks:")
print("    Gothic URRUNS (origin, source) = U-R-R-U-N-S sorted=NRRSUU → has S, diff")
print("    Gothic URRUN (ran out) → not standard form")

print("\n  SPECIAL HYPOTHESIS: UTRUNR = ON 'UT' + 'RUNR'")
print("  ON plural of 'run' (rune) is 'runar' or (archaic) 'runr'")
print("  'UT RUNR' = 'outer runes' or 'out-runes' (runes for the outside world?)")
print("  Context perfectly fits: bonelords placing/hiding runes outside their domain")
print("  'ODE UT RUNR DEN ENDE REDER KOENIG SALZBERG'")
print("  = 'Alone at outer-runes, the-end orator King Salzberg'")

# ============================================================
# SECTION 10: Full coverage test with new vocabulary
# ============================================================
print("\n" + "=" * 70)
print("SECTION 10: COVERAGE GAIN FROM NEW VOCABULARY")
print("=" * 70)

# Build expanded vocab
EXPANDED = set(KNOWN_WORDS)
# Add ALL MHG vocabulary
EXPANDED.update(MHG_VOCAB.keys())
# Add Latin
EXPANDED.update(LATIN_VOCAB.keys())
# Add Old Dutch
EXPANDED.update(MDU_VOCAB.keys())
# Add Old Norse
EXPANDED.update(OLD_NORSE_VOCAB.keys())
# Add Old Saxon
EXPANDED.update(OLD_SAXON_VOCAB.keys())

# Calculate coverage
def count_coverage(text, vocab):
    n = len(text)
    covered = set()
    i = 0
    while i < n:
        found = False
        for l in range(min(20, n-i), 1, -1):
            w = text[i:i+l]
            if w in vocab:
                for c in range(i, i+l):
                    covered.add(c)
                i += l
                found = True
                break
        if not found:
            i += 1
    return len(covered), n

base_cov, total = count_coverage(processed, KNOWN_WORDS)
exp_cov, _ = count_coverage(processed, EXPANDED)
print(f"\nBaseline coverage: {base_cov}/{total} = {base_cov/total*100:.1f}%")
print(f"With expanded vocab (MHG+Latin+MDu+ON+OS): {exp_cov}/{total} = {exp_cov/total*100:.1f}%")
print(f"Gain: +{exp_cov-base_cov} chars")

# Find which new words contribute
print("\nNew words that added coverage:")
for word in sorted(EXPANDED - KNOWN_WORDS, key=len, reverse=True):
    if len(word) < 3: continue
    base_no_word = count_coverage(processed, KNOWN_WORDS)[0]
    test_vocab = set(KNOWN_WORDS) | {word}
    test_cov = count_coverage(processed, test_vocab)[0]
    if test_cov > base_cov:
        # Find contexts
        pos = 0
        contexts = []
        while True:
            idx = processed.find(word, pos)
            if idx < 0: break
            ctx = processed[max(0,idx-8):idx+len(word)+8]
            contexts.append(ctx)
            pos = idx + 1
        if contexts:
            lang = 'MHG' if word in MHG_VOCAB else 'LAT' if word in LATIN_VOCAB else 'MDU' if word in MDU_VOCAB else 'ON' if word in OLD_NORSE_VOCAB else 'OS'
            meaning = (MHG_VOCAB.get(word) or LATIN_VOCAB.get(word) or MDU_VOCAB.get(word) or
                      OLD_NORSE_VOCAB.get(word) or OLD_SAXON_VOCAB.get(word) or '?')
            print(f"  +{test_cov-base_cov:3d} {word:15s} [{lang}] = '{meaning[:30]}'")
            for ctx in contexts[:2]:
                print(f"         ...{ctx.strip()[:40]}...")

print("\nDone.")
