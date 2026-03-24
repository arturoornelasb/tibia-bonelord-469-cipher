#!/usr/bin/env python3
"""
Brute-force anagram solver for Bonelord proper nouns.
Tests against comprehensive German word lists and geographic databases.
CipSoft pattern: exact anagram + 1 extra letter.
"""

from itertools import combinations
from collections import Counter

def sorted_key(word):
    return ''.join(sorted(word.upper()))

def find_subanagrams(cipher_word, word_list, extra_allowed=1):
    """Find words that are anagrams of cipher_word minus exactly `extra_allowed` letters."""
    cipher_counts = Counter(cipher_word.upper())
    cipher_len = len(cipher_word)
    target_len = cipher_len - extra_allowed

    results = []
    for word in word_list:
        word_upper = word.upper()
        if len(word_upper) != target_len:
            continue
        word_counts = Counter(word_upper)
        # Check if word_counts is a sub-multiset of cipher_counts
        valid = True
        for char, count in word_counts.items():
            if cipher_counts.get(char, 0) < count:
                valid = False
                break
        if valid:
            # What letter is extra?
            remaining = dict(cipher_counts)
            for char, count in word_counts.items():
                remaining[char] -= count
            extras = ''.join(c * n for c, n in remaining.items() if n > 0)
            results.append((word_upper, extras))
    return results

# Comprehensive German word list for anagram testing
GERMAN_COMPOUNDS = [
    # Geographic names
    'SALZBERG', 'SALZBURG', 'REGENSBURG', 'NUERNBERG', 'HEIDELBERG',
    'FREIBURG', 'AUGSBURG', 'WUERZBURG', 'BAMBERG', 'PASSAU',
    'INGOLSTADT', 'KELHEIM', 'LANDSHUT', 'STRAUBING', 'DEGGENDORF',
    'AMBERG', 'WEIDEN', 'SCHWANDORF', 'TIRSCHENREUTH',
    'BERLIN', 'MUENCHEN', 'HAMBURG', 'KOELN', 'FRANKFURT',
    'STUTTGART', 'DUESSELDORF', 'DORTMUND', 'ESSEN', 'BREMEN',
    'DRESDEN', 'LEIPZIG', 'HANNOVER', 'KASSEL', 'ERFURT',
    'ROSTOCK', 'LUEBECK', 'MAGDEBURG', 'BRAUNSCHWEIG',
    'AACHEN', 'TRIER', 'MAINZ', 'WORMS', 'SPEYER',
    'WEICHSTEIN', 'BACHSTADT', 'DRACHSTADT', 'GOLDSTADT',
    'STEINBURG', 'STEINHEIM', 'STEINFELD', 'STEINBERG',

    # Fantasy/Tibia relevant compounds
    'TOTENBURG', 'TOTENGRUND', 'TOTENGRUBE', 'TOTENGRUFT',
    'TOTENREICH', 'TOTENGEIST', 'TOTENSTADT', 'TOTENTURM',
    'TOTENRITTER', 'TOTENGRAB', 'TOTENGEBIET', 'TOTENGERICHT',
    'UNTERGOTTEID', 'UNTERGRUND', 'UNTERWELT', 'UNTERGOTTHEIT',
    'GOTTEINRUDE', 'RUINENGOTT', 'GOTTESFURCHT', 'GOTTESRUNE',
    'GOTTESGERICHT', 'GOTTESDIENER', 'GOTTESURTEIL',
    'TURMRUINE', 'TURMGEIST', 'TURMFESTE', 'TURMBURG',
    'RUNDTURM', 'STEINTURM', 'BURGTURM', 'WACHTTURM',
    'DRACHENHORT', 'DRACHENBURG', 'DRACHENTURM',
    'RUNENORT', 'RUNENSTEIN', 'RUNENMEISTER', 'RUNENFELD',
    'RUNENTURM', 'RUNENREICH', 'RUNENSCHRIFT', 'RUNENBUCH',
    'GEISTERBURG', 'GEISTERSTADT', 'GEISTERTURM',
    'GOLDGRUBE', 'GOLDMINE', 'GOLDSCHATZ', 'GOLDQUELLE',
    'EIGENTUEMER', 'EIGENTUM', 'EIGENSCHAFT',
    'STEINGARTEN', 'STEINGROTTE', 'STEINKAMMER',
    'GRABSTAETTE', 'GRABKAMMER', 'GRABMAL',
    'ORANGENSTRASSE', 'ROSENSTRASSE', 'GARTENSTRASSE',
    'RUNENSTRASSE', 'STEINSTRASSE', 'SONNENSTRASSE',
    'STERNENSTRASSE', 'TORSTRASSE', 'GRABENSTRASSE',
    'SONNENAUFGANG', 'SONNENUNTERGANG',
    'KOENIGSTHRON', 'KOENIGSBURG', 'KOENIGSREICH',
    'RITTERGUT', 'RITTERBURG', 'RITTERSAAL',

    # Common German nouns (long ones)
    'DRITTEGUTED', 'UNTERGOTTED', 'INGROTTEDTU',
    'EINGEROTTET', 'GUTERDIENOT', 'RUINENSTADT',
    'UNTERGOTTEID', 'DETOURNIEGT', 'DENIGROTUET',
    'TOTENGRIDUE', 'GOTTUNREIDE',

    # MHG / archaic words
    'TUGENDREICH', 'GOTTESSTREIT', 'RUINENTURM',
    'TRUTZEBURG', 'TODESNOT', 'TODESURTEIL',
    'RITTERGUTES', 'UNTERGOTTDIE',
    'GOETTERBURG', 'GOETTERDIENST',
    'STRASSENTOR', 'TORSTRASSEN',
    'SONNENTOR', 'TORGARTEN', 'ROSENGARTEN',
    'GARTENROSE', 'GARTENTOR', 'STERNENTOR',
    'STURMGARTEN', 'GARTENTURM',

    # Two-word combinations
    'ORANGENGARTEN', 'GARTENSTERNE',
    'STERNGARTEN', 'GARTENSONST',
    'STRASSENGARTEN', 'GARTENSTRASSEN',
    'ROSENGARTENSS', 'STRASSENGROTTE',
    'SONNENSTRASSEN',

    # Place-like compounds
    'STRASSENORT', 'ORTSTRASSEN',
    'ORTSANGRENSS', 'GRENZORTSSNA',
    'STRASSENNORTE', 'NORDSTRASSEN',
    'SUEDSTRASSEN', 'STRASSENSUEDE',
    'OSTSTRASSEN', 'STRASSENOSTEN',
    'WESTSTRASSEN', 'STRASSENWESTE',
]

# Key proper nouns to solve
targets = {
    'EDETOTNIURG': '?? (death-related compound?)',
    'AUNRSONGETRASES': '?? (15 chars, very long)',
    'TAUTR': '?? (5 chars)',
    'EILCH': '?? (5 chars, might mean "hastily")',
    'UTRUNR': '?? (6 chars, ~RUNDTURM?)',
    'HIHL': '?? (4 chars, proper noun)',
    'ENGCHD': '?? (6 chars)',
    'KELSEI': '?? (6 chars)',
    'GEVMT': '?? (5 chars)',
    'TOTNIURG': '?? (8 chars, without EDE prefix)',
    'HWND': '?? (4 chars, appears 10x with FINDEN)',
}

print("=" * 70)
print("BRUTE-FORCE ANAGRAM SOLVER")
print("CipSoft pattern: word = anagram + 1 extra letter")
print("=" * 70)

for cipher, desc in targets.items():
    print(f"\n{'=' * 50}")
    print(f"{cipher} ({len(cipher)} chars) - {desc}")
    print(f"Letters: {dict(Counter(cipher))}")
    print(f"{'=' * 50}")

    # Test with +0 (exact anagram) and +1 extra
    for extra in [0, 1]:
        results = find_subanagrams(cipher, GERMAN_COMPOUNDS, extra_allowed=extra)
        if results:
            label = "EXACT ANAGRAM" if extra == 0 else "ANAGRAM +1"
            print(f"\n  {label}:")
            for word, extras in sorted(results, key=lambda x: len(x[1])):
                print(f"    {word} (+{extras})")

    # Also test short words from a basic list
    basic_words = [
        'TURM', 'BURG', 'BERG', 'FELD', 'WALD', 'LAND', 'DORF',
        'STADT', 'GRUB', 'GRUBE', 'GRUFT', 'GRAB', 'RUIN', 'RUINE',
        'STEIN', 'GOLD', 'SILBER', 'EISEN', 'HOLZ', 'WAND',
        'TOTEN', 'GEIST', 'GOTT', 'GOETTER', 'RUNE', 'RUNEN',
        'NACHT', 'LICHT', 'DUNKEL', 'FEUER', 'WASSER', 'ERDE',
        'DRACULA', 'DRAKUL', 'VLAD', 'DRACHE', 'DRACHEN',
        'HELD', 'RITTER', 'KOENIG', 'PRIESTER', 'MAGIER',
        'SOHN', 'TOCHTER', 'BRUDER', 'SCHWESTER',
        'RECHT', 'GERICHT', 'URTEIL', 'RACHE',
        'SEELE', 'GEHEIMNIS', 'ZAUBER', 'FLUCH', 'SEGEN',
        'EHRE', 'TREUE', 'SCHULD', 'ZORN', 'STOLZ',
        'LIEBE', 'MINNE', 'HASS', 'FURCHT',
        'STERN', 'MOND', 'SONNE', 'HIMMEL',
        'BLUT', 'HERZ', 'HAUPT', 'LEIB',
        'SCHWERT', 'SCHILD', 'HELM', 'BOGEN',
        'KLINGE', 'DOLCH', 'LANZE', 'AXT',
        'HUETTE', 'HUET', 'WACHE', 'TORWART',
        # Short words
        'TOR', 'ORT', 'RAT', 'TAT', 'MAL', 'RUF', 'MUT',
        'TAG', 'NOT', 'TOD', 'LOT', 'HUT',
        'LEID', 'NEID', 'WELT', 'HELD',
        'GRUEN', 'BLAU', 'GELB', 'WEISS', 'SCHWARZ',
        # Verbs/adjectives
        'KLEIN', 'GROSS', 'ALT', 'NEU', 'GUT', 'SCHLECHT',
        'EDEL', 'ADLIG', 'WILD', 'FREI', 'STARK', 'SCHWACH',
    ]

    for extra in [0, 1]:
        results = find_subanagrams(cipher, basic_words, extra_allowed=extra)
        if results:
            label = "basic +0" if extra == 0 else "basic +1"
            print(f"\n  {label}:")
            for word, extras in sorted(results, key=lambda x: len(x[1])):
                if len(word) >= 3:
                    print(f"    {word} (+{extras})")

# ============================================================
# SPECIAL: Try to decompose EDETOTNIURG and AUNRSONGETRASES
# ============================================================
print(f"\n{'=' * 70}")
print("COMPOUND DECOMPOSITION")
print(f"{'=' * 70}")

# For EDETOTNIURG: try TOTEN + X or GOTT + X
cipher = 'EDETOTNIURG'
cipher_counts = Counter(cipher)
print(f"\nEDETOTNIURG decomposition:")

components = ['TOTEN', 'GOTT', 'RUIN', 'RUINE', 'BURG', 'TURM', 'GERICHT',
              'URTEIL', 'ERDE', 'GROTTE', 'GRUFT', 'GRUBE', 'GRUND',
              'TIGER', 'GEIST', 'ODIN', 'TUGENDE', 'TUGEND', 'DOTTER',
              'GOETTER', 'REIDE', 'TREUE', 'DIENER', 'RICHTER',
              'EDEL', 'RITTE', 'RITTER', 'DUNKEL', 'EINODE',
              'BITTER', 'MUTTER', 'NORDEN', 'ORIENT', 'ORIENT',
              'GUTER', 'NIEDER', 'RIEDE', 'GUIDE', 'DEUTERIG',
              'EIDE', 'EIDOTTER']

for comp in components:
    comp_counts = Counter(comp)
    remaining_counts = dict(cipher_counts)
    valid = True
    for c, n in comp_counts.items():
        if remaining_counts.get(c, 0) < n:
            valid = False
            break
        remaining_counts[c] -= n
    if valid:
        remaining = ''.join(c * n for c, n in remaining_counts.items() if n > 0)
        remaining_sorted = ''.join(sorted(remaining))
        print(f"  {comp} + [{remaining_sorted}]")

        # Try to match the remainder
        for comp2 in components:
            if sorted(comp2.upper()) == sorted(remaining_sorted.upper()):
                print(f"    >>> {comp} + {comp2} = EXACT MATCH!")
            # Also try with +1 tolerance (CipSoft pattern)
            comp2_counts = Counter(comp2.upper())
            rem_counts = Counter(remaining_sorted.upper())
            total_diff = 0
            for ch in set(list(comp2_counts.keys()) + list(rem_counts.keys())):
                total_diff += abs(comp2_counts.get(ch, 0) - rem_counts.get(ch, 0))
            if total_diff <= 2 and len(comp2) >= len(remaining_sorted) - 1:
                print(f"    ~~ {comp} + {comp2} (diff={total_diff//2})")

# For AUNRSONGETRASES
cipher2 = 'AUNRSONGETRASES'
cipher2_counts = Counter(cipher2)
print(f"\nAUNRSONGETRASES decomposition:")

components2 = ['STRASSE', 'STRASSEN', 'GARTEN', 'ROSEN', 'ORANGE', 'ORANGEN',
               'STERN', 'STERNE', 'SONNEN', 'SONNE', 'NATUR', 'TOREN',
               'ORGAN', 'ORGANE', 'RUNEN', 'REGEN', 'SEGEN', 'GEGEN',
               'SORGEN', 'SORGE', 'NORDEN', 'OSTEN', 'SUEDEN', 'WESTEN',
               'RASEN', 'NASEN', 'ROSEN', 'GROTTEN', 'GARTEN',
               'GESANG', 'STRANG', 'ORANGE', 'ORANGEN',
               'ENGST', 'ANGST', 'ERNST', 'OSTEN',
               'SENATORENGAS', 'GRANATENROSS', 'ROSENGARTENS',
               'ORANGENSTERNS', 'STERNENORANGAS', 'ORANGENGARTENS',
               'GARTENSORANENS', 'GARTENSONNERS', 'SONNENGARTERAS']

for comp in components2:
    comp_counts = Counter(comp.upper())
    remaining_counts = dict(cipher2_counts)
    valid = True
    for c, n in comp_counts.items():
        if remaining_counts.get(c, 0) < n:
            valid = False
            break
        remaining_counts[c] -= n
    if valid:
        remaining = ''.join(c * n for c, n in remaining_counts.items() if n > 0)
        remaining_sorted = ''.join(sorted(remaining))
        if len(remaining_sorted) <= 8:  # Only show reasonable remainders
            print(f"  {comp} + [{remaining_sorted}]")

            for comp2 in components2 + components:
                if len(comp2) >= len(remaining_sorted) - 1 and len(comp2) <= len(remaining_sorted) + 1:
                    comp2_sorted = ''.join(sorted(comp2.upper()))
                    if comp2_sorted == remaining_sorted:
                        print(f"    >>> {comp} + {comp2} = EXACT!")
                    comp2_counts = Counter(comp2.upper())
                    rem_c = Counter(remaining_sorted)
                    diff = sum(abs(comp2_counts.get(ch, 0) - rem_c.get(ch, 0)) for ch in set(list(comp2_counts.keys()) + list(rem_c.keys())))
                    if diff <= 2 and diff > 0:
                        print(f"    ~~ {comp} + {comp2} (diff={diff//2})")
