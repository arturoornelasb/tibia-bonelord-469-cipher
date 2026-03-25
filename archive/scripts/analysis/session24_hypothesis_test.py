#!/usr/bin/env python3
"""
Session 24 Part C: Test coverage gain from Session 24 hypotheses.

Hypotheses to test:
1. UIRUNNHWND -> WINDUNRUHN (+1 anagram, "wind unrest N")
2. HIHL -> HEHL (MHG concealment, E<->I variant)
3. HECHLLT -> HECHELT (hackle flax, E<->L swap -- is this valid?)
4. NLNDEF -> FINDEN (forced, already documented)
5. UTRUNR -> treat as UT+RUNR (split, adds nothing to coverage)
6. Batch test: German words that appear but aren't in vocab
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

raw = ''.join(decoded_books)
processed = raw
for old in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    processed = processed.replace(old, ANAGRAM_MAP[old])

# Session 22 full vocabulary
KNOWN_WORDS = {
    'SEIN', 'SEINE', 'SEINER', 'SEINEN', 'SEINEM', 'SEINES',
    'IST', 'WAR', 'WIRD', 'WAREN', 'SEID',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES',
    'EIN', 'EINE', 'EINER', 'EINEM', 'EINEN', 'EINES',
    'UND', 'ODER', 'ABER', 'NICHT', 'MIT', 'VON', 'BIS',
    'WIR', 'ICH', 'ER', 'SIE', 'ES', 'IHR', 'WER', 'WAS',
    'IN', 'IM', 'AN', 'AM', 'AUF', 'AUS', 'AB', 'ZU', 'ZUR', 'ZUM',
    'BEI', 'SO', 'DA', 'WO', 'NUN', 'NU', 'INS', 'GEN', 'DES', 'AUS',
    'HIER', 'ODE', 'ORT', 'NACH', 'ALS', 'WIE', 'WENN',
    'KLAR', 'AUCH', 'WEG', 'NUR', 'NIT',
    'GOTT', 'RUNE', 'RUNEN', 'STEIN', 'STEINEN', 'STEINE',
    'URALTE', 'ALT', 'ALTE', 'ALTEN',
    'KOENIG', 'RITTER', 'WORT', 'SAGEN', 'FINDEN',
    'STEH', 'GEHEN', 'GEH', 'ENDE', 'ENDEN',
    'ERSTE', 'ERSTEN',
    'DIESE', 'DIESER', 'DIESEN', 'DIESEM', 'DIESES',
    'TAG', 'MIN', 'TOT', 'RUIN', 'RUINE', 'SAND', 'HEIME', 'HEIM',
    'LEICH', 'LEICHE', 'TRAUT', 'SCHRAT', 'SCHARDT', 'SCHAUN',
    'WEICHSTEIN', 'SALZBERG', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'EIGENTUM', 'MEERE',
    'NEIGT', 'WISTEN', 'MANIER', 'GODES', 'DIENST', 'NACHTS',
    'STANDE', 'BEI', 'TUT', 'NEU', 'SICH', 'REDER',
    'HEL', 'RIT', 'EWE', 'SIN', 'MIS', 'AUE', 'EIS',
    'SCE', 'OEL', 'TER', 'THENAEUT',
    'BERUCHTIG', 'BERUCHTIGER', 'LEICHANBERUCHTIG', 'LEICHANBERUCHTIGER',
    'HAT', 'NET', 'EM', 'TUN',
    'RUINEN', 'HUND', 'GRUND', 'RECHT', 'NACHT',
    'BURG', 'BERG', 'WALD', 'LICHT', 'KNECHT',
    'HEHL', 'HEHLE', 'HEIL', 'HELD', 'SCHLECHT', 'ECHT',
    'WIRT', 'WIRTE', 'TURM', 'TEICH',
    'ELCH', 'DURCH', 'WUNDER', 'WUNDE',
    'UNTER', 'HOLT',
}

def count_coverage(text, vocab):
    n = len(text)
    covered = 0
    i = 0
    while i < n:
        for l in range(min(20, n-i), 1, -1):
            if text[i:i+l] in vocab:
                covered += l
                i += l
                break
        else:
            i += 1
    return covered, n

base_cov, total = count_coverage(processed, KNOWN_WORDS)
print(f"Baseline coverage: {base_cov}/{total} = {base_cov/total*100:.1f}%")

def test_anagram(name, old_str, new_str, description):
    """Test adding a new anagram entry to the map."""
    new_map = dict(ANAGRAM_MAP)
    new_map[old_str] = new_str
    p2 = raw
    for k in sorted(new_map, key=len, reverse=True):
        p2 = p2.replace(k, new_map[k])
    cov, tot = count_coverage(p2, KNOWN_WORDS)
    gain = cov - base_cov
    print(f"\n  {name}: {old_str} -> {new_str}")
    print(f"  Description: {description}")
    print(f"  Coverage: {cov}/{tot} = {cov/tot*100:.1f}% (gain: +{gain})")
    if gain > 0:
        # Find occurrences
        pos = 0
        while True:
            idx = p2.find(new_str, pos)
            if idx < 0: break
            ctx = p2[max(0,idx-10):idx+len(new_str)+10]
            print(f"  Occurrence: ...{ctx.strip()[:60]}...")
            pos = idx + 1
    return gain

def test_vocab_addition(word, description):
    """Test adding a word to known vocabulary."""
    vocab2 = KNOWN_WORDS | {word}
    cov, tot = count_coverage(processed, vocab2)
    gain = cov - base_cov
    if gain > 0:
        pos = 0
        ctxs = []
        while True:
            idx = processed.find(word, pos)
            if idx < 0: break
            ctxs.append(processed[max(0,idx-6):idx+len(word)+6])
            pos = idx + 1
        print(f"  +{gain:3d} '{word}' = {description}")
        for ctx in ctxs[:2]:
            print(f"       ...{ctx.strip()[:50]}...")
    return gain

print("\n" + "="*60)
print("TEST 1: ANAGRAM MAP ADDITIONS")
print("="*60)

# Test each Session 24 hypothesis
test_anagram("UIRUNNHWND compound",
    'UIRUNNHWND', 'WINDUNRUHN',
    'WIND + UNRUH + N (+1 extra N); German wind-unrest compound')

test_anagram("HIHL -> HEHL variant",
    'HIHL', 'HEHL',
    'MHG concealment/hiding (E<->I vowel alternation)')

test_anagram("HECHLLT -> HECHELT",
    'HECHLLT', 'HECHELT',
    'to hackle flax (E<->L swap, cipher obfuscation layer)')

test_anagram("NLNDEF -> FINDEN",
    'NLNDEF', 'FINDEN',
    'find (I<->L substitution, cipher obfuscation layer)')

test_anagram("NLNDEF -> NENNDFL? check",
    'NLNDEF', 'FNLNDE',
    'just checking...')

# Additional small anagram tests
test_anagram("IGAA -> GAIA",
    'IGAA', 'GAIA',
    'Greek earth goddess (mythological reference?)')

test_anagram("IGAA -> GAIA2",
    'IGAAE', 'EIGAA',
    'dummy test')

# Test REDER
test_anagram("REDER -> REDNER",
    'REDER', 'REDER',
    'already in vocab check')

print("\n" + "="*60)
print("TEST 2: VOCABULARY ADDITIONS (direct word matching)")
print("="*60)

print("\nTesting words that may appear in processed text but not in vocab:")
vocab_tests = [
    # German inflected forms
    ('GESAGT', 'said (past participle)'),
    ('GESEHEN', 'seen (past participle)'),
    ('GEWESEN', 'been (past participle)'),
    ('GEWORDEN', 'become (past participle)'),
    ('GEFUNDEN', 'found (past participle)'),
    ('GEGANGEN', 'gone (past participle)'),
    ('STANDEN', 'stood (past plural)'),
    ('STANDEN', 'stood'),
    ('GESTAN', 'stood (MHG)'),
    ('STEHEND', 'standing'),
    ('WANDERND', 'wandering'),
    ('WANDERUNG', 'wandering/pilgrimage'),
    ('SCHATTENLOS', 'shadowless'),
    ('DUNKEL', 'dark/darkness'),
    ('SCHATTEN', 'shadow'),
    ('SCHATTEN', 'shadow'),
    ('DUNKELHEIT', 'darkness'),
    ('FINSTERNIS', 'darkness'),
    ('ABENDDUNKEL', 'evening darkness'),
    # Place descriptors
    ('STEIN', 'stone'),  # already in vocab
    ('STEINS', 'stone (gen)'),
    ('STEINE', 'stones'),  # already in vocab
    ('FELS', 'cliff/rock'),
    ('FELSEN', 'cliffs'),
    ('KLIPPE', 'cliff'),
    # Verbs and forms
    ('HECHELN', 'to hackle'),
    ('HECHELT', 'hackles'),
    ('HECHELTE', 'hackled'),
    ('GEHECHELT', 'hackled (pp)'),
    ('SCHWEIGEN', 'to be silent'),
    ('SCHWEIGT', 'is silent'),
    ('SPRECHEN', 'to speak'),
    ('SPRICHT', 'speaks'),
    ('GESPROCHEN', 'spoken'),
    ('WANDERN', 'to wander'),
    ('WANDERT', 'wanders'),
    ('SCHWINDEN', 'to vanish'),
    ('SCHWINDET', 'vanishes'),
    ('VERBERGEN', 'to hide/conceal'),
    ('VERBIRGT', 'hides'),
    ('VERBARG', 'hid (past)'),
    # Specific to context
    ('SALBUNG', 'anointing'),
    ('SALBEN', 'to anoint'),
    ('SALBT', 'anoints'),
    ('GESALBT', 'anointed'),
    ('WEIHUNG', 'consecration'),
    ('WEIHEN', 'to consecrate'),
    ('WEIHT', 'consecrates'),
    ('GEWEIHT', 'consecrated'),
    # MHG verbs
    ('SPRICH', 'speak (MHG imperative)'),
    ('STANT', 'stand (MHG)'),
    ('STANDE', 'stands (MHG)'),  # already in vocab
    ('RITE', 'ride (MHG imperative)'),
    ('RITEND', 'riding (MHG)'),
    ('VART', 'journey (MHG)'),
    ('VAREN', 'to travel (MHG)'),
    # Nouns not in vocab
    ('GEHEIMNIS', 'secret'),
    ('GEHEIM', 'secret (adj)'),
    ('HEHLEN', 'to conceal (MHG verb)'),
    ('GEHEHL', 'concealment (MHG)'),
    ('HOHL', 'hollow/cave (NHG adj)'),
    ('HOHLE', 'cave (NHG)'),
    ('HOEHLE', 'cave (NHG alt)'),
    ('HEHL', 'concealment (MHG)'),  # already tested
    ('HEHLER', 'concealer (MHG)'),
    ('HEHLE', 'concealment (MHG)'),
    ('TURNIS', 'tower (Latin)'),
    ('TURNE', 'tower (MHG)'),
    ('TURNIER', 'tournament'),
    ('TURNIR', 'tournament (MHG)'),
    ('KAMPF', 'battle'),
    ('KAMPFE', 'battles'),
    ('WAFFE', 'weapon'),
    ('WAFFEN', 'weapons'),
    ('SCHWERT', 'sword'),
    ('SCHWERTER', 'swords'),
    ('SPEER', 'spear'),
    ('SPEERE', 'spears'),
    ('HELM', 'helmet (MHG=NHG)'),
    ('HELME', 'helmets'),
    ('SCHILD', 'shield'),
    ('SCHILDEN', 'shields (MHG dat pl)'),
    # Bonelord-specific
    ('BONELORD', 'bonelord (English in Tibia)'),
    ('WEICHSTEIN', 'soft stone (see SCHWITEIONE)'),  # already
    ('WEICHSTEINE', 'soft stones (pl)'),
    ('KNOCHENLORD', 'bonelord (German??)'),
    # OEL contexts
    ('OELEN', 'to oil'),
    ('GEOLT', 'oiled'),
    # FACH contexts
    ('FACHE', 'sections/rooms'),
    ('FACHES', 'section (gen)'),
    ('FACHS', 'section (gen alt)'),
    # Ritual context
    ('RITUAL', 'ritual'),
    ('RITUS', 'ritual (Latin)'),
    ('RITE', 'ritual (Latin abl)'),
    ('RITES', 'rites (pl)'),
    # HIHL context
    ('HIHL', 'concealment (HEHL variant)'),
    # Time expressions
    ('IMMER', 'always'),
    ('NIEMALS', 'never'),
    ('EINMAL', 'once'),
    ('ZWEIMAL', 'twice'),
    ('DREIMAL', 'three times'),
    ('OFTEN', 'often (English/dialectal)'),
    ('OFT', 'often'),
    # Additional from context
    ('GEIGET', 'bows (as in violin bow)'),  # already?
    ('GEIGT', 'bows'),
    ('TURM', 'tower'),  # already
    ('TURME', 'towers'),
    ('WIND', 'wind'),
    ('WINDE', 'winds/winch'),
    ('UNRUH', 'unrest (MHG/NHG)'),
    ('UNRUHE', 'unrest (NHG)'),
    ('WINDUNRUH', 'wind unrest compound'),
    ('WINDUNRUHE', 'wind unrest (NHG compound)'),
    ('TURMUNRUHE', 'tower unrest'),
    ('WINDTURM', 'wind tower'),
    ('BLITZEN', 'lightning'),
    ('DONNER', 'thunder'),
    ('STURM', 'storm'),
    ('STUERME', 'storms'),
    ('GEWITTER', 'thunderstorm'),
    ('REGEN', 'rain'),
    ('SCHNEE', 'snow'),
    ('FROST', 'frost'),
    ('FROSTS', 'frost (gen)'),
    ('EIS', 'ice'),  # already
    ('EISE', 'ice (MHG dat)'),
    ('STEIN', 'stone'),  # already
    ('STEINEN', 'stones'),  # already
    # More from HECHLLT context
    ('FLECHTE', 'braid/lichen'),
    ('FLECHTEN', 'braids'),
    ('GEFLECHT', 'braiding/network'),
    ('FLECHTWERK', 'wickerwork'),
    # NPC context
    ('NOODLES', 'dog NPC'),
    ('AVAR', 'NPC name'),
    ('TAR', 'NPC name'),
]

gains = []
for word, desc in vocab_tests:
    g = test_vocab_addition(word, desc)
    if g > 0:
        gains.append((g, word, desc))

gains.sort(reverse=True)
print(f"\nTop {min(10,len(gains))} gains from vocabulary additions:")
for g, w, d in gains[:10]:
    print(f"  +{g:3d} '{w}' = {d}")

print("\n" + "="*60)
print("TEST 3: COMBINED EFFECT OF SESSION 24 HYPOTHESES")
print("="*60)

# Combine all hypotheses
combined_map = dict(ANAGRAM_MAP)
combined_map['HIHL'] = 'HEHL'
combined_map['HECHLLT'] = 'HECHELT'
combined_map['NLNDEF'] = 'FINDEN'
combined_map['UIRUNNHWND'] = 'WINDUNRUHN'

combined_vocab = KNOWN_WORDS | {'HEHL', 'HECHELT', 'FINDEN', 'WINDUNRUHN',
                                  'WIND', 'UNRUH', 'HEHLEN', 'HEHLTE',
                                  'UNRUHE', 'WINDUNRUHE', 'STURM', 'TURM',
                                  'TURME', 'WINDE'}

p_combined = raw
for k in sorted(combined_map, key=len, reverse=True):
    p_combined = p_combined.replace(k, combined_map[k])

cov_combined, tot = count_coverage(p_combined, combined_vocab)
print(f"\nCombined (all hypotheses + vocab): {cov_combined}/{tot} = {cov_combined/tot*100:.1f}%")
print(f"Net gain: +{cov_combined - base_cov}")

# Also check with session 22 words
session22_map = dict(combined_map)
session22_vocab = combined_vocab.copy()

# Baseline with session 22 MHG words
mhg_words_22 = {'HEL', 'RIT', 'EWE', 'SIN', 'MIS', 'AUE', 'EIS', 'NIT', 'SCE', 'OEL', 'TER'}
cov_22, _ = count_coverage(processed, KNOWN_WORDS | mhg_words_22)
print(f"\nWith session 22 MHG words: {cov_22}/{total} = {cov_22/total*100:.1f}%")
cov_22_combined, _ = count_coverage(p_combined, combined_vocab | mhg_words_22)
print(f"With session 22 + session 24: {cov_22_combined}/{tot} = {cov_22_combined/tot*100:.1f}%")
print(f"Total gain from session 24 on top of session 22: +{cov_22_combined - cov_22}")

# Find all new occurrences
print("\nNew resolved occurrences from session 24 hypotheses:")
for old_block, new_word in [('HIHL', 'HEHL'), ('HECHLLT', 'HECHELT'),
                              ('NLNDEF', 'FINDEN'), ('UIRUNNHWND', 'WINDUNRUHN')]:
    count = p_combined.count(new_word) - processed.count(new_word)
    if count > 0:
        print(f"  {old_block} -> {new_word}: {count} new occurrences")

print("\nDone.")
