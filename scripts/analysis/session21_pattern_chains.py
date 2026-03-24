#!/usr/bin/env python3
"""
Session 21 Part 4: Pattern chain analysis.

Now that HEDDEMI is fixed (69.4%), look for:
1. The {SD} 7x pattern (always AN|SD|IM) - is ANSD or SDIM a word?
2. The {DE} 10x pattern - NEU|DE|DIENST, SEINE|DE|TOT
3. The {ND} 9x pattern - ORT|ND|TER
4. The {DR} 3x pattern - RUNEN|DR|THENAEUT
5. Cross-boundary recombination attempts
6. The repeating ER {T} EIN pattern - what is the T?
7. The IN {H} IM pattern
"""

import json, os
from collections import Counter, defaultdict

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

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    return 0 if ic_from_counts(Counter(bp0), len(bp0)) > ic_from_counts(Counter(bp1), len(bp1)) else 1

book_pairs = []
decoded_books = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)
    decoded_books.append(''.join(v7.get(p, '?') for p in pairs))

letter_codes = defaultdict(list)
for code, letter in v7.items():
    letter_codes[letter].append(code)

# ================================================================
# 1. THE {SD} PATTERN: always AN + SD + IM
# ================================================================
print("=" * 80)
print("1. {SD} PATTERN: AN + SD + IM (7x)")
print("=" * 80)

# "AN SD IM" -> could be ANSD+IM or AN+SDIM or A+NSD+IM
# ANSD -> SAND? SAND sorted = A,D,N,S = match!
# But the DP already has SAND in KNOWN, and the text has ANSD not SAND.
# So ANSD is an anagram of SAND!

print(f"  ANSD sorted: {sorted('ANSD')}")
print(f"  SAND sorted: {sorted('SAND')}")
print(f"  Match: {sorted('ANSD') == sorted('SAND')}")
print(f"  Context: ...DIENST ORT AN SD IM MIN...")
print(f"  If ANSD -> SAND: ...DIENST ORT SAND IM MIN...")
print(f"  = 'service place sand in love/my...' - makes sense?")

# Check if ANSD is a unique substring (safe for anagram map)
for bidx, text in enumerate(decoded_books):
    count = text.count('ANSD')
    if count > 0:
        pos = 0
        while True:
            idx = text.find('ANSD', pos)
            if idx < 0: break
            ctx = text[max(0,idx-10):idx+14]
            print(f"  Book {bidx}: ...{ctx}...")
            pos = idx + 1

# But wait - ANSD appears inside longer blocks too?
# Let me check DIENST ORT AN SD context more carefully
# The raw decoded text has "...DIENSTOR TANSDIMMIN..."
# After anagram and DP: DIENST+ORT+AN+{SD}+IM+MIN

# What if the actual word boundaries are: DIENST+ORT+ANSD+IM+MIN
# And ANSD = SAND (cross-boundary exact anagram)?
# This is like the TNEDAS -> STANDE pattern!

print(f"\n  This is a CROSS-BOUNDARY EXACT ANAGRAM: AN+SD -> ANSD -> SAND")
print(f"  Like TNEDAS -> STANDE (already confirmed)")

# Check: does adding 'ANSD': 'SAND' to anagram map work?
# ANSD is 4 chars. Does it appear inside any other words/patterns?
all_text = ''.join(decoded_books)
ansd_count = all_text.count('ANSD')
print(f"\n  Total ANSD in decoded text: {ansd_count}x")

# Also check if ANSD appears in processed text (after current anagram map)
ANAGRAM_MAP = {
    'LABGZERAS': 'SALZBERG', 'SCHWITEIONE': 'WEICHSTEIN',
    'SCHWITEIO': 'WEICHSTEIN', 'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'EDETOTNIURG': 'GOTTDIENER', 'EDETOTNIURGS': 'GOTTDIENERS',
    'ADTHARSC': 'SCHARDT', 'TAUTR': 'TRAUT', 'EILCH': 'LEICH',
    'HEDDEMI': 'HEIME',
    'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG', 'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE', 'TEIGN': 'NEIGT', 'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER', 'SODGE': 'GODES', 'SNDTEII': 'DIENST',
    'IEB': 'BEI', 'TNEDAS': 'STANDE', 'NSCHAT': 'NACHTS',
    'SANGE': 'SAGEN', 'GHNEE': 'GEHEN', 'THARSCR': 'SCHRAT',
}

processed_text = all_text
for old, new in ANAGRAM_MAP.items():
    processed_text = processed_text.replace(old, new)
ansd_in_processed = processed_text.count('ANSD')
print(f"  Total ANSD in processed text: {ansd_in_processed}x")

# Check if ANSD is always at word boundary (not inside a longer word)
print(f"\n  All ANSD contexts in processed text:")
pos = 0
while True:
    idx = processed_text.find('ANSD', pos)
    if idx < 0: break
    ctx = processed_text[max(0,idx-8):idx+12]
    print(f"  pos {idx}: ...{ctx}...")
    pos = idx + 1

# ================================================================
# 2. THE {DE} PATTERN: 10x
# ================================================================
print(f"\n{'=' * 80}")
print("2. {DE} PATTERN (10x)")
print("=" * 80)

# Contexts: NEU|DE|DIENST (5x), SEINE|DE|TOT (3x), other (2x)
# NEU DE DIENST = "new DE service" = ???
# SEINE DE TOT = "his DE death" = ???
# What if {DE} is DES (of the) with missing S?
# Or what if NEUDED is a word? DIENSTART?
# More likely: DE is just a garbled fragment.

# But wait - "SEINE DE TOT" appears as "SEINEDETOT"
# What if it's SEINEN (his) + DETOT? No...
# Or SEINE + DET + OT? DET is not a word.
# Or SEIN + EDETOT? EDETOT sorted = D,E,E,O,T,T
# TOD (death) = D,O,T
# EDETOT -> EDETO + T -> ?
# Actually: SEINE + DE + TOT = "his DE dead"
# DE could be: DER (the), but missing R
# or DEN, missing N
# or just a garbled article

# In MHG: "sinen tot" (his death) is standard.
# SEINE+DE+TOT in the raw text might be the cipher's way of writing "SEINEN TOD"
# SEINEN = S,E,I,N,E,N and the text has SEINE (5) + DE (2) = 7 chars
# SEINEN is 6 chars. So SEINEDE = 7 chars = SEINEN + D?
# SEINEN + D... or: the raw text is SEINEDETOT
# SEINEDETOT contains SEINEN (at pos 0, but SEINED is not SEINEN)
# Actually: S-E-I-N-E-D-E-T-O-T
# DP finds: SEINE(5) + {DE}(2) + TOT(3) = 5+3 = 8 known
# What if: SEIN(4) + {EDETOT}(6) = 4 known (worse)
# Or: SEIN(4) + {E} + DET + OT = broken
# Or: SEINE(5) + {D} + {E} + TOT(3) = 5+3 = 8 known (same as current)

# What if we try SEINEN?
print(f"  Testing SEINEN as known word...")
print(f"  'SEINEDETOT': SEINE(5) + DE(garbled 2) + TOT(3) = 8 known")
print(f"  With SEINEN: SEINEN(6) + ? SEIN+E+N... but text is SEINED not SEINEN")
# SEINEDETOT: S-E-I-N-E-D-E-T-O-T
# The N at position 3 is followed by E-D, not E-N.
# So SEINEN cannot be matched here.

# Verdict: {DE} is a structural artifact, not a word. Skip.

# ================================================================
# 3. THE {ND} PATTERN: 9x (6x ORT|ND|TER)
# ================================================================
print(f"\n{'=' * 80}")
print("3. {ND} PATTERN (9x, 6x as ORT|ND|TER)")
print("=" * 80)

# ORT ND TER = "place ND of-the" / "place ND TER"
# ORTND = ORTND sorted = D,N,O,R,T -> could be TROND, NORDT, DRONT?
# NDTER sorted = D,E,N,R,T -> TREND? = T,R,E,N,D -> match!
# Wait: NDTER = N,D,T,E,R and TREND = T,R,E,N,D -> sorted both = D,E,N,R,T
# BUT: the text has ORT+ND+TER where TER is already a known word.
# So the {ND} is between ORT and TER, not part of TER.

# Context: "RUNE ORT ND TER AM NEU DE DIENST ORT AN SD IM"
# = "rune place ND of-the at new DE service place ..."

# Could ND be part of ORT? ORTND?
# Or: ND = UND (and) missing U? That would make:
# "RUNE ORT UND TER AM NEU..." = "rune place and of-the at new..."
# Hmm, doesn't scan perfectly but "UND" (and) is a super common German word.
# But ND is only 2 chars, UND is 3. The text has ND not UND.

# What if it's part of a longer block: ORTNDTER = "rune ORTNDTER at new..."?
# ORTNDTER sorted: D,E,N,O,R,R,T,T
# Nope, can't make a word from that.

# Actually, let me re-examine: is the {ND} consistently between the same words?
print(f"  All {'{'}ND{'}'} occurrences:")
for bidx, text in enumerate(decoded_books):
    for old, new in ANAGRAM_MAP.items():
        text = text.replace(old, new)
    pos = 0
    while True:
        idx = text.find('ND', pos)
        if idx < 0: break
        # Check if ND is garbled (not part of a known word)
        # Simple check: look at surrounding context
        ctx_s = max(0, idx-6)
        ctx_e = min(len(text), idx+8)
        ctx = text[ctx_s:ctx_e]
        # Is ND preceded by ORT and followed by TER?
        before = text[max(0,idx-3):idx]
        after = text[idx+2:idx+5]
        if before.endswith('ORT') or before.endswith('GEH'):
            print(f"  Book {bidx:2d}: ...{ctx}... (before: '{before}', after: '{after}')")
        pos = idx + 1

# ================================================================
# 4. CROSS-BOUNDARY: ANSD -> SAND
# ================================================================
print(f"\n{'=' * 80}")
print("4. TESTING ANSD -> SAND CROSS-BOUNDARY ANAGRAM")
print("=" * 80)

# Add ANSD -> SAND and measure impact
# But first verify it won't collide with anything
# ANSD is 4 chars. In the processed text, does ANSD appear anywhere it shouldn't?
# From the check above, ANSD appears multiple times, all in "ORTANSDIMMIN" context

# Wait, I need to be careful. ANSD appears in the processed text AFTER other
# anagram replacements. Let me check the raw decoded text for ANSD.
print(f"  Checking ANSD in raw decoded text (before anagram resolution):")
raw_ansd_count = 0
for bidx, text in enumerate(decoded_books):
    pos = 0
    while True:
        idx = text.find('ANSD', pos)
        if idx < 0: break
        ctx = text[max(0,idx-8):idx+12]
        print(f"    Book {bidx:2d}: ...{ctx}...")
        raw_ansd_count += 1
        pos = idx + 1
print(f"  Total raw ANSD: {raw_ansd_count}x")

# Check in SNDTEII context (which becomes DIENST via anagram)
# SNDTEII contains 'ANSD'? S-N-D-T-E-I-I, no it doesn't contain ANSD
# The ANSD appears when the pre-SNDTEII text has "ORTANSD..."
# After SNDTEII -> DIENST, the AN would become... wait, SNDTEII is independent.

# Let me verify: what does the text look like around ANSD BEFORE any anagram resolution?
# The key phrase is "DIENSTOR T ANSDIMMIN"
# But DIENST comes from SNDTEII anagram. So before anagram:
# "SNDTEIIOR T ANSDIMMIN"
# No, the anagram map replaces SNDTEII with DIENST. The raw text would have SNDTEII at some point.

# Actually, looking at the processed text output from the main script:
# "DIENST ORT AN {SD} IM MIN" means the post-anagram text has "DIENSTORTANSDIMMIN"
# The DP finds DIENST+ORT+AN+{SD}+IM+MIN
# The ANSD is at positions AN+SD crossing the boundary.

# The cross-boundary anagram would need to be: replace ANSD with SAND
# But ANSD is not a pre-existing block in the text. It's AN(known)+SD(garbled).
# The anagram map runs BEFORE DP, so if we add 'ANSD' to the map,
# it would replace ANSD in the post-anagram text with SAND.
# Then DP would find SAND as a known word.

# But: does ANSD appear inside any other word we want to keep?
# Check: LEICHANHEARUCHTIG contains ANHEA not ANSD. OK.
# ORANGENSTRASSE: ORANGENSTRASSE doesn't have ANSD. OK.
# STANDE: no ANSD inside. OK.

# Let me just test the impact
print(f"\n  Testing 'ANSD': 'SAND' in anagram map:")

# Simulate
test_text = ''.join(decoded_books)
for old, new in ANAGRAM_MAP.items():
    test_text = test_text.replace(old, new)
test_text = test_text.replace('ANSD', 'SAND')

# Check if SAND now appears and is findable by DP
sand_count = test_text.count('SAND')
print(f"  SAND in text after replacement: {sand_count}x")

# Show contexts
pos = 0
while True:
    idx = test_text.find('SAND', pos)
    if idx < 0: break
    ctx = test_text[max(0,idx-6):idx+10]
    print(f"    ...{ctx}...")
    pos = idx + 1

# ================================================================
# 5. SEARCH FOR MORE CROSS-BOUNDARY ANAGRAMS
# ================================================================
print(f"\n{'=' * 80}")
print("5. SYSTEMATIC CROSS-BOUNDARY ANAGRAM SEARCH")
print("=" * 80)

# For each garbled block of 2-3 chars, combine with adjacent known word
# and check if the combination is an anagram of a German word

KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR', 'NU', 'STANDE', 'NACHTS', 'NIT', 'TOT', 'TER',
    'SAND', 'OEL', 'SCE', 'MIN', 'ODE', 'SER', 'GEN', 'INS',
    'GEIGET', 'BERUCHTIG', 'MEERE', 'NEIGT', 'WISTEN', 'MANIER',
    'GODE', 'GODES', 'EIGENTUM', 'REDER', 'THENAEUT', 'LABT',
    'DIGE', 'WEGE', 'NOT', 'NOTH', 'OWI', 'ENGE', 'SUN',
    'DIENST', 'KOENIG', 'DASS', 'SCHRAT',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME', 'SCHARDT',
    'FINDEN', 'GEHEN', 'SAGEN', 'STEH', 'FACH', 'ENDE', 'ERDE',
    'RUNEN', 'RUNE', 'NEU', 'KLAR', 'SCHAUN', 'TEIL',
])

# German words for cross-boundary matching
GERMAN_WORDS = set([
    # 3-letter
    'ALS', 'AUS', 'BEI', 'DAS', 'DEM', 'DEN', 'DER', 'DES', 'DIE',
    'EIN', 'GAR', 'GEN', 'HAT', 'HER', 'HIN', 'ICH', 'IST', 'MAN',
    'MIT', 'NUN', 'NUR', 'ORT', 'RAT', 'SAG', 'SEI', 'SIE', 'TAG',
    'TUN', 'UND', 'VON', 'VOR', 'WAR', 'WER', 'WIE', 'WIR',
    # 4-letter
    'ACHT', 'ALLE', 'AUCH', 'BEIN', 'DASS', 'DEIN', 'DICH', 'DIES',
    'DOCH', 'DORT', 'DREI', 'EDEL', 'EINE', 'ERDE', 'ERST', 'FACH',
    'FAND', 'FERN', 'GANZ', 'GAST', 'GELD', 'GERN', 'GOTT', 'GRAB',
    'GRAS', 'GRIM', 'GROS', 'GRUN', 'HAND', 'HAUS', 'HEIL', 'HEIM',
    'HELD', 'HERR', 'HIER', 'HOCH', 'HORT', 'HULD', 'HUND', 'KANN',
    'KEIN', 'KIND', 'KLAR', 'KLUG', 'LAND', 'LANG', 'LEID', 'MEHR',
    'MEIN', 'MILD', 'MUSS', 'NACH', 'NAHE', 'NAME', 'NEID', 'NEIN',
    'NOCH', 'REDE', 'REIN', 'RIEF', 'RUIN', 'RUNE', 'SAGT', 'SAND',
    'SANG', 'SEID', 'SEIN', 'SICH', 'SIND', 'SOHN', 'SOLL', 'STEH',
    'TEIL', 'TIEF', 'TREU', 'TURM', 'UFER', 'VIEL', 'VIER', 'WALD',
    'WAND', 'WARD', 'WEIL', 'WEIT', 'WELT', 'WENN', 'WERT', 'WILL',
    'WIND', 'WIRD', 'WORT', 'ZEIT', 'ZORN',
    # 5-letter
    'ALLES', 'ALTEN', 'ALTER', 'BERGE', 'BEIDE', 'DEINE', 'DENEN',
    'DIESE', 'EIGEN', 'EINEN', 'EINER', 'EINES', 'ENGEL', 'ERNST',
    'ERSTE', 'GEBEN', 'GEHEN', 'GEGEN', 'GEIST', 'GNADE', 'GREIS',
    'GRUND', 'HEIDE', 'IMMER', 'KLAGE', 'KRAFT', 'KREUZ', 'KRONE',
    'LANDE', 'LEGEN', 'LESEN', 'LICHT', 'MACHT', 'NACHT', 'NICHT',
    'ORTEN', 'RECHT', 'REDEN', 'RUFEN', 'RUHEN', 'RUNEN', 'SAGEN',
    'SCHON', 'SEELE', 'SEGEN', 'SEHEN', 'STERN', 'UNTER', 'WACHE',
    'WEGEN', 'WENDE', 'WESEN', 'WORTE',
    # 6-letter+
    'DIENST', 'FINDEN', 'KOENIG', 'RITTER', 'GEIGET', 'SCHAUN',
    'STANDE', 'NACHTS', 'WISTEN', 'MANIER', 'STEINEN', 'URALTE',
    'STEINER', 'RICHTER', 'DUNKEL',
])

# For cross-boundary: garbled block + adjacent known word = anagram of longer word
# Focus on 2-letter garbled blocks

two_letter_garbled = {
    'SD': [('AN', 'IM', 7)],   # AN+SD or SD+IM
    'DE': [('NEU', 'DIENST', 5), ('SEINE', 'TOT', 3)],
    'ND': [('ORT', 'TER', 6), ('GEH', 'FINDEN', 2)],
    'NT': [('ENDE', 'ES', 4)],
    'DR': [('RUNEN', 'THENAEUT', 3)],
    'CH': [('ES', 'IST', 3)],
    'TD': [('IM', 'ENDE', 3)],
    'HH': [('ENGE', 'EIN', 3)],
    'TI': [('SER', 'UM', 3)],
}

print(f"\n  Cross-boundary candidates:")
for garbled, contexts in two_letter_garbled.items():
    for left_word, right_word, freq in contexts:
        # Try: left_word + garbled -> longer word?
        combo_left = left_word + garbled
        combo_left_sorted = ''.join(sorted(combo_left))
        # Try: garbled + right_word -> longer word?
        combo_right = garbled + right_word
        combo_right_sorted = ''.join(sorted(combo_right))

        for gw in GERMAN_WORDS:
            gw_sorted = ''.join(sorted(gw))
            if gw_sorted == combo_left_sorted and gw != combo_left:
                print(f"  {left_word}+{garbled} = {combo_left} -> {gw} (exact anagram, {freq}x)")
            if gw_sorted == combo_right_sorted and gw != combo_right:
                print(f"  {garbled}+{right_word} = {combo_right} -> {gw} (exact anagram, {freq}x)")
            # +1 pattern (combo has one extra letter)
            if len(gw) == len(combo_left) - 1:
                for skip in range(len(combo_left)):
                    reduced = combo_left[:skip] + combo_left[skip+1:]
                    if ''.join(sorted(reduced)) == gw_sorted:
                        print(f"  {left_word}+{garbled} = {combo_left} -> {gw} (+1, extra '{combo_left[skip]}', {freq}x)")
                        break
            if len(gw) == len(combo_right) - 1:
                for skip in range(len(combo_right)):
                    reduced = combo_right[:skip] + combo_right[skip+1:]
                    if ''.join(sorted(reduced)) == gw_sorted:
                        print(f"  {garbled}+{right_word} = {combo_right} -> {gw} (+1, extra '{combo_right[skip]}', {freq}x)")
                        break

# ================================================================
# 6. THE MYSTERIOUS {T} - 13x ER T EIN
# ================================================================
print(f"\n{'=' * 80}")
print("6. THE MYSTERIOUS {T} - 13x in 'ER T EIN ER SEIN GOTTDIENER'")
print("=" * 80)

# Raw context: "DIESERTEINERSEIN..."
# The phrase in the narrative is: "...SO DASS TUN DIES ER {T} EIN ER SEIN GOTTDIENER..."
# This is the most-repeated phrase. The {T} is always code 78.
# What if the {T} is not a separate word but part of a compound?
# DIES + ERTEIN + ER + SEIN = doesn't make sense
# DIES + ER + TEINER + SEIN = TEINER? Not a word
# DIES + ER + T + EINER + SEIN = T + EINER? "one of them"?
# Wait: EINER is a real German word (one, someone)
# "ER T EINER SEIN GOTTDIENER" = "he T one his God's Servant"
# Still doesn't help because T is isolated.

# What about the full raw block including context?
# The text is: ...DASSTUNDIISERTEINERSEIN...
# Wait, let me look at the actual raw text more carefully.
# From the code 78 analysis: "SERTEIN" with codes 52 19 72 78 30 46 48
# That's: S(52) E(19) R(72) T(78) E(30) I(46) N(48)
# Wait - so the raw text around {T} is "SERTEIN"
# = SER + T + EIN
# = SER(very) + {T} + EIN(one/a)

# But what if it's actually: SE + RTEIN? Or SERT + EIN?
# SERT isn't a word. RTEIN isn't a word.
# Or: S + ERTEIN? ERTEIN -> ?

# What if the boundary is wrong and it should be:
# "...DIES ERS..." or something else?
# The text before is: ...DASSTUNDIIS ER TEIN ER SEIN...
# DASSTUNDII = DASS+TUN+DIES (after anagram, DIIS might be part of DIES)

# Actually, let me check the exact decoded text for one book
for bidx, text in enumerate(decoded_books):
    processed = text
    for old, new in ANAGRAM_MAP.items():
        processed = processed.replace(old, new)
    idx = processed.find('TEINERSEIN')
    if idx >= 0:
        full_ctx = processed[max(0,idx-20):idx+25]
        print(f"  Book {bidx}: ...{full_ctx}...")
        # Raw codes for this section
        codes_start = max(0, idx - 20)
        codes_end = min(len(book_pairs[bidx]), idx + 25)
        break

# ================================================================
# 7. COMBINED ANSD/SAND COVERAGE TEST
# ================================================================
print(f"\n{'=' * 80}")
print("7. COVERAGE TEST: ANSD -> SAND")
print("=" * 80)

# ANSD -> SAND is a cross-boundary exact anagram (AN+SD = ANSD -> SAND)
# Similar to TNEDAS -> STANDE, NSCHAT -> NACHTS, SANGE -> SAGEN

# Safe? ANSD is 4 chars. Let me verify no collisions:
for bidx, text in enumerate(decoded_books):
    processed = text
    for old, new in ANAGRAM_MAP.items():
        processed = processed.replace(old, new)
    pos = 0
    while True:
        idx = processed.find('ANSD', pos)
        if idx < 0: break
        ctx = processed[max(0,idx-10):idx+14]
        # Check if this ANSD is at the expected position
        before = processed[max(0,idx-3):idx]
        after = processed[idx+4:idx+8]
        print(f"  Book {bidx:2d}: ...{ctx}... (before='{before}' after='{after}')")
        pos = idx + 1

# Verify: ANSD doesn't appear inside ORANGENSTRASSE or other compound
print(f"\n  Collision check: ORANGENSTRASSE contains ANSD? {'ANSD' in 'ORANGENSTRASSE'}")
print(f"  LEICHANBERUCHTIG contains ANSD? {'ANSD' in 'LEICHANBERUCHTIG'}")
print(f"  SCHARDT contains ANSD? {'ANSD' in 'SCHARDT'}")
print(f"  STANDE contains ANSD? {'ANSD' in 'STANDE'}")

print(f"\n  ANSD -> SAND appears safe. Adding to anagram map would give:")
print(f"  'DIENST ORT SAND IM MIN' instead of 'DIENST ORT AN {{SD}} IM MIN'")
print(f"  = 'service place sand in my...' -> location reference!")

print(f"\nDone.")
