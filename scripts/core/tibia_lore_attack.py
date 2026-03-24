#!/usr/bin/env python3
"""
Tibia Lore Crib Attack
========================
The decoded text contains proper nouns that are CipSoft-style anagrams
(exact anagram + 0 or 1 extra letter). Test all known Tibia proper nouns
against the unresolved garbled segments.

Confirmed pattern:
  LABGZERAS    = SALZBERG + A    (geographic name)
  SCHWITEIONE  = WEICHSTEIN + O  (geographic name)
  AUNRSONGETRASES = ORANGENSTRASSE + U (street name)

Hypothesis: CipSoft used German geographic/cultural names, anagrammed them,
and possibly added 1 extra letter.

Also test: Tibia-specific names (cities, NPCs, gods, creatures).
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

# Decode all books
decoded_books = []
for bpairs in book_pairs:
    text = ''.join(v7.get(p, '?') for p in bpairs)
    decoded_books.append(text)

# ============================================================
# Unresolved proper nouns / garbled segments
# ============================================================
proper_nouns = {
    'EDETOTNIURG': "appears as place/title, context: SEIN EDETOTNIURGS",
    'TIUMENGEMI': "appears as place, compound?",
    'UTRUNR': "appears before DEN ENDE REDE, possibly 6-letter place",
    'HIHL': "appears with RUNE, 4-letter place",
    'EILCH': "appears before AN HEARUCHTIG, 5-letter word",
    'TAUTR': "appears before IST EILCH, 5-letter name",
    'HEDEMI': "appears with DIE URALTE STEINEN, possibly Kelheim",
    'ADTHARSC': "appears with IST SCHAUN RUIN, 8 letters",
    'ENGCHD': "appears in text, 6 letters",
    'KELSEI': "appears in text, 6 letters",
    'GEVMT': "appears in text, 5 letters",
    'LABRNI': "appears with WIR, context: LABRNI WIR",
    'SCHWITEIO': "truncated SCHWITEIONE = WEICHSTEIN+O",
}

# Known garbled text segments (not proper nouns, but consistent)
garbled_segments = {
    'HECHLLT': "appears 5x after FACH, 7 letters",
    'NDCE': "appears 8x in DIE NDCE, 4 letters",
    'RHEIUIRUNN': "appears 6x with HWND, 10 letters",
    'LAUNRLRUNR': "appears 2x near NACH, 10 letters",
    'TEHWRIGTN': "appears before EIN, 9 letters",
    'NTEUTTUIG': "appears in various, 9 letters",
    'UNENITGH': "appears after LABGZERAS, 8 letters",
    'GEIGET': "appears 4x, 6 letters",
    'AUIENNR': "appears after RUNE, 7 letters",
    'HWND': "most common with FINDEN, 4 letters",
}

# ============================================================
# Test database: German geographic names, Tibia names, etc.
# ============================================================

# German cities, mountains, rivers, regions
GERMAN_PLACES = [
    # Major cities
    'BERLIN', 'MUENCHEN', 'HAMBURG', 'KOELN', 'FRANKFURT', 'STUTTGART',
    'DUESSELDORF', 'DORTMUND', 'ESSEN', 'BREMEN', 'DRESDEN', 'LEIPZIG',
    'HANNOVER', 'NUERNBERG', 'AUGSBURG', 'WUERZBURG', 'REGENSBURG',
    'PASSAU', 'BAMBERG', 'BAYREUTH', 'INGOLSTADT',
    # Bavarian towns near Regensburg (CipSoft HQ)
    'KELHEIM', 'STRAUBING', 'DEGGENDORF', 'CHAM', 'AMBERG',
    'WEIDEN', 'SCHWANDORF', 'TIRSCHENREUTH', 'NEUMARKT',
    'LANDSHUT', 'FREISING', 'ERDING', 'DACHAU', 'PFAFFENHOFEN',
    'NEUBURG', 'ABENSBERG', 'MAINBURG', 'RIEDENBURG',
    'EICHSTAETT', 'BERCHING', 'BEILNGRIES', 'DIETFURT',
    'HEMAU', 'LAABER', 'BERATZHAUSEN', 'REGENSTAUF',
    # Historic German cities
    'AACHEN', 'TRIER', 'MAINZ', 'WORMS', 'SPEYER', 'GOSLAR',
    'QUEDLINBURG', 'ROTHENBURG', 'DINKELSBUEHL', 'NOERDLINGEN',
    'LUEBECK', 'ROSTOCK', 'WISMAR', 'STRALSUND', 'GREIFSWALD',
    'MAGDEBURG', 'BRAUNSCHWEIG', 'HILDESHEIM',
    # Austrian/Swiss
    'WIEN', 'GRAZ', 'SALZBURG', 'INNSBRUCK', 'LINZ',
    'BERN', 'ZUERICH', 'BASEL', 'GENF', 'LUZERN',
    # Rivers
    'DONAU', 'RHEIN', 'ELBE', 'WESER', 'MAIN', 'MOSEL',
    'NAAB', 'REGEN', 'ALTMUEHL', 'ISAR', 'LECH', 'INN',
    # Mountains/Regions
    'ALPEN', 'SCHWARZWALD', 'HARZ', 'ERZGEBIRGE',
    'BAYERISCHER', 'OBERPFALZ', 'NIEDERBAYERN', 'OBERBAYERN',
    'FRANKEN', 'SCHWABEN', 'SACHSEN', 'THUERINGEN',
    # Castles/Landmarks
    'WALHALLA', 'BEFREIUNGSHALLE', 'STEINERNE',
    'STEINERNEBRUECKE', 'DOMSTADT',
    # Compound geographic words
    'WEICHSTEIN', 'SALZBERG', 'ORANGENSTRASSE',
    'BACHSTADT', 'STEINBURG', 'GOLDBERG', 'SILBERBERG',
    'EISENBERG', 'KUPFERBERG', 'FICHTELBERG',
    'RUNDTURM', 'STEINTURM', 'BURGTURM', 'KIRCHTURM',
    'MARKTPLATZ', 'RATHAUSPLATZ', 'DOMPLATZ',
    'GRAFSCHAFT', 'HERRSCHAFT', 'RITTERSCHAFT',
    'KOENIGREICH', 'KAISERREICH',
    'TOTENGRUFT', 'TOTENGRUBE', 'TOTENGRUND',
    'GOTTESDIENER', 'GOTTESKNECHT', 'GOTTESHAUS',
    'TOTENGERICHT', 'TOTENREICH', 'TOTENRUHE',
    'STEINMETZ', 'GOLDSCHMIED', 'WAFFENSCHMIED',
    'EIGENTUM', 'HEILIGTUM', 'ALTERTUM', 'RITTERTUM',
    'PRIESTERTUM', 'KAISERTUM', 'KOENIGTUM', 'HERZOGTUM',
    'FUERSTENTUM', 'BISTUM', 'CHRISTENTUM',
    'BRUEDERSCHAFT', 'GEMEINSCHAFT', 'FREUNDSCHAFT',
    'MANNSCHAFT', 'RITTERORDEN', 'MOENCHEN',
]

# Tibia-specific names (classic era, pre-2005)
TIBIA_NAMES = [
    # Cities
    'THAIS', 'CARLIN', 'VENORE', 'EDRON', 'DARASHIA',
    'KAZORDOON', 'ABDENDRIEL', 'ANKRAHMUN', 'LIBERTY',
    'SVARGROND', 'YALAHAR', 'FARMINE', 'ROSHAMUUL',
    # Important locations
    'FIBULA', 'ROOKGAARD', 'MINTWALLIN', 'DEMONA',
    'JAKUNDAF', 'DREFIA', 'BANUTA', 'FORBIDDEN',
    # Gods & important figures
    'ZATHROTH', 'UMAN', 'FARDOS', 'SULA', 'CRUNOR',
    'BASTESH', 'KIROK', 'TOTH', 'URGITH',
    'BANOR', 'TIBIANUS', 'FERUMBRAS',
    # Creatures
    'BONELORD', 'BRAINDEATH', 'ELDER', 'BEHOLDER',
    # Key concepts
    'NIGHTMARE', 'HELLGATE', 'PITS', 'INFERNO',
    'DREAMER', 'DREAMERS', 'CHALICE',
    # Hellgate library context
    'LIBRARY', 'BONELORDS', 'ANCIENT', 'FORBIDDEN',
]

# MHG (Middle High German) words
MHG_WORDS = [
    'MINNE', 'RECKE', 'RECKEN', 'SWERT', 'RICHE',
    'VROUWE', 'EDELE', 'EDELEN', 'GEBET', 'HERRE',
    'HERRSCHAFT', 'RITTERSCHAFT', 'MEISTERSCHAFT',
    'TUGEND', 'TUGENDEN', 'EHRE', 'TREUE',
    'HULDE', 'GNADE', 'URTEIL', 'FREVEL',
    'BUSSE', 'SUEHNE', 'SCHULD', 'SUENDE',
    'SELIGKEIT', 'VERDAMMNIS', 'ERLOESUNG',
    'ABGRUND', 'TIEFE', 'HOEHE', 'WEITE',
    'DUNKELHEIT', 'FINSTERNIS', 'EWIGKEIT',
]

def is_anagram_plus_n(word, target, max_extra=1):
    """Check if word is an anagram of target + up to max_extra letters."""
    wc = Counter(word.upper())
    tc = Counter(target.upper())

    # target should be shorter or equal
    if len(target) > len(word) + max_extra:
        return None
    if len(target) < len(word) - max_extra:
        return None

    # Check: can we get from word to target by adding/removing at most max_extra?
    diff = Counter()
    for c in set(list(wc.keys()) + list(tc.keys())):
        d = wc.get(c, 0) - tc.get(c, 0)
        if d > 0:
            diff[c] = d

    extras = sum(diff.values())
    missing = sum(max(tc.get(c, 0) - wc.get(c, 0), 0) for c in tc)

    if extras <= max_extra and missing == 0:
        extra_letters = ''.join(c * diff[c] for c in sorted(diff))
        return extra_letters if extra_letters else "(exact)"
    return None

# ============================================================
# TEST ALL PROPER NOUNS AGAINST ALL NAMES
# ============================================================
print("=" * 70)
print("TIBIA LORE + GERMAN GEOGRAPHIC ANAGRAM ATTACK")
print("=" * 70)

all_names = GERMAN_PLACES + TIBIA_NAMES + MHG_WORDS

for noun, desc in sorted(proper_nouns.items(), key=lambda x: -len(x[0])):
    matches = []
    for name in all_names:
        result = is_anagram_plus_n(noun, name, max_extra=1)
        if result is not None:
            matches.append((name, result))
        # Also check reverse (noun is shorter)
        result2 = is_anagram_plus_n(name, noun, max_extra=1)
        if result2 is not None and (name, result2) not in matches:
            matches.append((name, f"name+{result2}"))

    if matches:
        print(f"\n  {noun} ({desc}):")
        for name, extra in sorted(matches, key=lambda x: len(x[1])):
            print(f"    -> {name} (extra: {extra})")

print(f"\n{'=' * 70}")
print("GARBLED SEGMENTS ANAGRAM ATTACK")
print(f"{'=' * 70}")

for seg, desc in sorted(garbled_segments.items(), key=lambda x: -len(x[0])):
    matches = []
    for name in all_names:
        result = is_anagram_plus_n(seg, name, max_extra=1)
        if result is not None:
            matches.append((name, result))
        result2 = is_anagram_plus_n(name, seg, max_extra=1)
        if result2 is not None and (name, result2) not in matches:
            matches.append((name, f"name+{result2}"))

    if matches:
        print(f"\n  {seg} ({desc}):")
        for name, extra in sorted(matches, key=lambda x: len(x[1])):
            print(f"    -> {name} (extra: {extra})")

# ============================================================
# COMPOUND DECOMPOSITION for longer nouns
# ============================================================
print(f"\n{'=' * 70}")
print("COMPOUND DECOMPOSITION ATTACK")
print("Testing: can garbled segments be split into 2 German words?")
print(f"{'=' * 70}")

COMPOUND_PARTS = [
    'TOTEN', 'TOTER', 'TODE', 'TODES', 'TOD', 'TOT',
    'GOTT', 'GOTTES', 'GOETTER',
    'STEIN', 'STEINE', 'STEINEN', 'STEINS',
    'BERG', 'BERGE', 'BERGEN', 'BERGS',
    'BURG', 'BURGEN', 'BURGS',
    'TURM', 'TUERME', 'TURMS',
    'RITTER', 'RITTERS', 'RITTER',
    'KOENIG', 'KOENIGS', 'KOENIGIN',
    'KAISER', 'KAISERS',
    'PRIESTER', 'PRIESTERS',
    'MEISTER', 'MEISTERS',
    'DIENER', 'DIENERS',
    'KNECHT', 'KNECHTE', 'KNECHTS',
    'GOLD', 'GOLDS', 'GOLDEN', 'GOLDE',
    'SILBER', 'SILBERS',
    'EISEN', 'EISENS',
    'FEUER', 'FEUERS',
    'WASSER', 'WASSERS',
    'ERDE', 'ERDEN', 'ERDS',
    'LUFT', 'LUEFTE',
    'NACHT', 'NAECHTE', 'NACHTS',
    'LICHT', 'LICHTER', 'LICHTS',
    'GEIST', 'GEISTER', 'GEISTES',
    'SEELE', 'SEELEN',
    'RUHE', 'RUHM',
    'GNADE', 'GNADEN',
    'RECHT', 'RECHTS', 'RECHTE',
    'GERICHT', 'GERICHTS',
    'URTEIL', 'URTEILS',
    'GRUFT', 'GRUFTEN',
    'GRUBE', 'GRUBEN',
    'GRUND', 'GRUENDE', 'GRUNDS',
    'NIEDER', 'NIEDERE',
    'OBER', 'OBERE',
    'UNTER', 'UNTERE',
    'EIGEN', 'EIGENS',
    'HEILIG', 'HEILIGE', 'HEILIGEN',
    'EWIG', 'EWIGE', 'EWIGEN',
    'RUND', 'RUNDE', 'RUNDEN',
    'ALT', 'ALTE', 'ALTEN', 'ALTER', 'ALTES',
    'NEU', 'NEUE', 'NEUEN', 'NEUER', 'NEUES',
    'DUNKEL', 'DUNKLE', 'DUNKLEN',
    'HEIL', 'HEILS',
    'HERR', 'HERREN', 'HERRN',
    'EDEL', 'EDLE', 'EDLEN',
    'FREI', 'FREIE', 'FREIEN',
    'STARK', 'STARKE', 'STARKEN',
    'GROSS', 'GROSSE', 'GROSSEN',
    'RUNEN', 'RUNE',
    'MINNE',
    'GRAB', 'GRABS', 'GRAEBER',
    'SPRUCH', 'SPRUECHE',
    'FLUCH', 'FLUECHE',
    'SEGEN', 'SEGENS',
    'MACHT', 'MAECHTE', 'MACHTS',
    'KRAFT', 'KRAEFTE', 'KRAFTS',
    'EHRE', 'EHREN',
    'TREUE',
    'SCHULD',
    'WACHE', 'WAECHTER',
    'HUETER',
    'SCHUTZ', 'SCHUTZES',
    'RING', 'RINGE', 'RINGEN', 'RINGS',
    'BUND', 'BUENDE', 'BUNDS',
    'ORDEN', 'ORDENS',
    'RAT', 'RATS', 'RATE',
    'GEMEIN', 'GEMEINDE',
]

for noun, desc in sorted(proper_nouns.items(), key=lambda x: -len(x[0])):
    if len(noun) < 6:
        continue
    results = []
    noun_letters = sorted(noun.upper())
    noun_counter = Counter(noun.upper())

    for part1 in COMPOUND_PARTS:
        p1c = Counter(part1.upper())
        # Check if part1 is a sub-multiset of noun
        remaining = Counter(noun_counter)
        valid = True
        for c, cnt in p1c.items():
            if remaining.get(c, 0) < cnt:
                valid = False
                break
            remaining[c] -= cnt
        if not valid:
            continue

        remaining_str = ''.join(sorted(c * remaining[c] for c in remaining if remaining[c] > 0))

        for part2 in COMPOUND_PARTS:
            p2_sorted = ''.join(sorted(part2.upper()))
            # Exact match
            if p2_sorted == remaining_str:
                results.append((part1, part2, "exact"))
            # +1 extra letter
            elif len(remaining_str) == len(p2_sorted) + 1:
                extra = list(remaining_str)
                for c in p2_sorted:
                    if c in extra:
                        extra.remove(c)
                if len(extra) == 1:
                    results.append((part1, part2, f"+{extra[0]}"))

    if results:
        print(f"\n  {noun}:")
        seen = set()
        for p1, p2, extra in sorted(results, key=lambda x: (x[2], -len(x[0])-len(x[1]))):
            key = frozenset([p1, p2, extra])
            if key not in seen:
                seen.add(key)
                print(f"    {p1} + {p2} ({extra})")

# ============================================================
# Verify HEDEMI = KELHEIM hypothesis
# ============================================================
print(f"\n{'=' * 70}")
print("HEDEMI vs KELHEIM")
print(f"{'=' * 70}")

hedemi = Counter('HEDEMI')
kelheim = Counter('KELHEIM')
print(f"  HEDEMI letters:  {dict(hedemi)}")
print(f"  KELHEIM letters: {dict(kelheim)}")

diff = {}
for c in set(list(hedemi.keys()) + list(kelheim.keys())):
    d = hedemi.get(c, 0) - kelheim.get(c, 0)
    if d != 0:
        diff[c] = d
print(f"  Difference: {diff}")
print(f"  HEDEMI has: extra D, missing K, L")
print(f"  NOT an anagram. Would need [code]=K and [code]=L corrections.")

# ============================================================
# Check ADTHARSC = BACHSTADT hypothesis
# ============================================================
print(f"\n{'=' * 70}")
print("ADTHARSC vs BACHSTADT")
print(f"{'=' * 70}")

adtharsc = Counter('ADTHARSC')
bachstadt = Counter('BACHSTADT')
print(f"  ADTHARSC letters:  {dict(adtharsc)}")
print(f"  BACHSTADT letters: {dict(bachstadt)}")

diff = {}
for c in set(list(adtharsc.keys()) + list(bachstadt.keys())):
    d = adtharsc.get(c, 0) - bachstadt.get(c, 0)
    if d != 0:
        diff[c] = d
print(f"  Difference: {diff}")
if not diff:
    print(f"  >> EXACT ANAGRAM! ADTHARSC = BACHSTADT confirmed!")
else:
    result = is_anagram_plus_n('ADTHARSC', 'BACHSTADT', max_extra=1)
    if result is not None:
        print(f"  ADTHARSC = BACHSTADT + {result}")

    # Also try DRACHSTADT
    result2 = is_anagram_plus_n('ADTHARSC', 'DRACHSTADT', max_extra=1)
    if result2 is not None:
        print(f"  ADTHARSC = DRACHSTADT + {result2}")

    # And STADTARCH
    for word in ['HARSTADT', 'HARDTASCH', 'STADTRACH', 'DRACHSTATT',
                 'RACHSTADT', 'SCHATTRAD', 'DRACHSTAT']:
        result3 = is_anagram_plus_n('ADTHARSC', word, max_extra=1)
        if result3 is not None:
            print(f"  ADTHARSC = {word} + {result3}")

# Test ADTHARSC more broadly
print(f"\n  ADTHARSC as EXACT anagram of:")
adtharsc_sorted = ''.join(sorted('ADTHARSC'))
test_words = [
    'DRACHSTAAT', 'RACHSTADT', 'HARSTADT', 'DRACHSAT',
    'SCHARADT', 'STADTCHAR', 'HARDTASC', 'DRACHTAS',
    'CHARDAST', 'DARTSCHA', 'HARDSCAT', 'RACHTADS',
]
for tw in test_words:
    if ''.join(sorted(tw)) == adtharsc_sorted:
        print(f"    {tw} - YES!")

# Compound decomposition for ADTHARSC
print(f"\n  ADTHARSC compound decomposition:")
for p1 in COMPOUND_PARTS:
    p1c = Counter(p1.upper())
    remaining = Counter('ADTHARSC')
    valid = True
    for c, cnt in p1c.items():
        if remaining.get(c, 0) < cnt:
            valid = False
            break
        remaining[c] -= cnt
    if valid:
        rem_str = ''.join(sorted(c * remaining[c] for c in remaining if remaining[c] > 0))
        if len(rem_str) <= 5 and len(rem_str) >= 2:
            print(f"    {p1} + [{rem_str}]")

# ============================================================
# NARRATIVE CONTEXT: What role does each proper noun play?
# ============================================================
print(f"\n{'=' * 70}")
print("PROPER NOUN NARRATIVE CONTEXT")
print(f"{'=' * 70}")

for noun, desc in sorted(proper_nouns.items()):
    for bidx, text in enumerate(decoded_books):
        pos = text.find(noun)
        if pos >= 0:
            ctx_s = max(0, pos - 25)
            ctx_e = min(len(text), pos + len(noun) + 25)
            ctx = text[ctx_s:ctx_e]
            print(f"  {noun} Book {bidx:2d}: ...{ctx}...")
            break  # Just first occurrence for brevity
