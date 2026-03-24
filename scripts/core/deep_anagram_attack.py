#!/usr/bin/env python3
"""
Deep Anagram + Compound Word + MHG Attack on Bonelord 469 Proper Nouns
=====================================================================
CipSoft uses anagrams extensively:
  Vladruc = Dracula, Dallheim = Heimdall, Excalibug = Excalibur

This script systematically tests ALL decoded proper nouns as:
1. Anagrams of German/Tibia words
2. Reversed words (TOTNIURG = GRUINTOT already found)
3. Compound word splits
4. Caesar/ROT shifts on letter values
5. Partial anagrams (some letters fixed, others rearranged)
"""

import json, os, sys
from itertools import permutations
from collections import Counter

# ============================================================
# DATA
# ============================================================

PROPER_NOUNS = {
    # name: (frequency, known_context)
    "LABGZERAS": (8, "KOENIG LABGZERAS - king's name"),
    "TAUTR": (8, "HIER TAUTR IST EILCHANHEARUCHTIG"),
    "EILCHANHEARUCHTIG": (8, "title/adjective of TAUTR"),
    "EDETOTNIURGS": (8, "attribute of TAUTR, contains TOTNIURG"),
    "TOTNIURG": (8, "reversed = GRUINTOT, death+ruin"),
    "HEDEMI": (11, "place with uralte Steinen"),
    "ADTHARSC": (6, "entity at the stones"),
    "LABRNI": (8, "person/place, shares LAB- with LABGZERAS"),
    "KELSEI": (3, "after ENGCHD"),
    "SCHWITEIONE": (10, "possibly bonelord race name"),
    "TIUMENGEMI": (2, "ORT TIUMENGEMI = place"),
    "ENGCHD": (7, "ORT ENGCHD = place"),
    "AUNRSONGETRASES": (11, "most common unrecognized, near KOENIG"),
    "UTRUNR": (5, "ENDE UTRUNR = end of utterance"),
    "HWND": (6, "OHG for HUND = hound"),
    "GEVMT": (7, "SEI GEVMT WIE = be GE-VMT as"),
    "WRLGTNELNRHELUIRUNN": (6, "long garbled segment"),
    "DNRHAUNRNVMHISDIZA": (4, "garbled segment"),
    "LRSZTHK": (3, "7 consonants in a row"),
}

# Known Tibia anagrams for reference
KNOWN_ANAGRAMS = {
    "VLADRUC": "DRACULA",
    "DALLHEIM": "HEIMDALL",
    "EXCALIBUG": "EXCALIBUR",
    "FERUMBRAS": "AMBROSIUS (partial)",
    "BANOR": "BARON",
    "KOSHEI": "KOSCHEI (Slavic)",
    "DURIN": "historical dwarf king",
}

# German word list for anagram matching (expanded)
GERMAN_WORDS = set()
COMMON_GERMAN = [
    # Kings, rulers, titles
    "KAISER", "KOENIG", "FUERST", "HERZOG", "GRAF", "RITTER", "HERRSCHER",
    "ZAUBERER", "PRIESTER", "KRIEGER", "MEISTER", "HEXER", "DRUIDE",
    # Places
    "BERG", "BURG", "STADT", "WALD", "SEE", "FLUSS", "TAL", "HOEHLE",
    "TURM", "TEMPEL", "GRAB", "GRUFT", "SCHLOSS", "FESTUNG", "RUINE",
    # Mythology/fantasy
    "DRACHE", "DAEMON", "GEIST", "SEELE", "SCHICKSAL", "FLUCH", "SEGEN",
    "ZAUBER", "MAGIE", "MACHT", "KRAFT", "DUNKEL", "LICHT", "SCHATTEN",
    "UNTERWELT", "TOTENREICH", "SCHWARZE", "WEISSE",
    # Nature
    "STEIN", "ERDE", "FEUER", "WASSER", "LUFT", "GOLD", "SILBER",
    "EISEN", "KRISTALL", "DIAMANT",
    # Actions/concepts
    "KRIEG", "FRIEDEN", "TOD", "LEBEN", "RACHE", "EHRE", "TREUE",
    "VERRAT", "GERECHTIGKEIT", "EWIGKEIT", "UNSTERBLICH",
    # Common German words for compound splitting
    "DER", "DIE", "DAS", "EIN", "EINE", "UND", "ODER", "ABER",
    "IST", "HAT", "WAR", "WIRD", "KANN", "MUSS", "SOLL",
    "NICHT", "AUCH", "NUR", "NOCH", "SCHON", "SEHR", "VIEL",
    "ALLE", "JEDER", "DIESER", "JENER", "WELCHER",
    "MIT", "VON", "ZU", "AN", "AUF", "IN", "AUS", "NACH", "FUER",
    "ALT", "NEU", "GROSS", "KLEIN", "LANG", "KURZ", "HOCH", "TIEF",
    "GUT", "SCHLECHT", "BOESE", "HEILIG", "DUNKEL", "HELL",
    # MHG words
    "RUCHTIG", "BERUCHTIG", "BERUCHTIGT", "HERACHTIG",
    "EDEL", "ADEL", "RUNE", "RUNEN", "HARSCH", "RAUH",
    "MINNE", "RECKE", "HORT", "NIBELUNGEN", "SIGURD",
    "ACHE", "BACH", "SCHAR", "HEER", "SCHWERT",
    # Tibia-specific
    "BONELORD", "HELLGATE", "DEMONA", "THAIS", "VENORE", "CARLIN",
    "EDRON", "DARASHIA", "ANKRAHMUN", "KAZORDOON", "SVARGROND",
    "TIBIANUS", "HONEMINAS", "EXCALIBUG", "FERUMBRAS",
    "RASHID", "NOODLES", "KNIGHTMARE", "CHAYENNE",
    # Number-related (469)
    "VIER", "SECHS", "NEUN", "VIERHUNDERTSECHSUNDNEUNZIG",
]

for w in COMMON_GERMAN:
    GERMAN_WORDS.add(w)
    # Also add without umlauts
    GERMAN_WORDS.add(w.replace("OE", "O").replace("UE", "U").replace("AE", "A"))

# ============================================================
# ANAGRAM FUNCTIONS
# ============================================================

def get_letter_counts(word):
    return Counter(word.upper())

def is_anagram(word1, word2):
    """Check if two words are exact anagrams."""
    return get_letter_counts(word1) == get_letter_counts(word2)

def is_partial_anagram(word1, word2, max_diff=2):
    """Check if words are anagrams with up to max_diff letter differences."""
    c1 = get_letter_counts(word1)
    c2 = get_letter_counts(word2)
    diff = 0
    all_letters = set(list(c1.keys()) + list(c2.keys()))
    for letter in all_letters:
        diff += abs(c1.get(letter, 0) - c2.get(letter, 0))
    return diff <= max_diff * 2  # each substitution counts as 2 (remove+add)

def find_anagrams_in_wordlist(target, wordlist, max_diff=0):
    """Find words in wordlist that are anagrams (or near-anagrams) of target."""
    results = []
    target_len = len(target)
    target_counts = get_letter_counts(target)

    for word in wordlist:
        if abs(len(word) - target_len) > max_diff:
            continue
        if max_diff == 0:
            if is_anagram(target, word):
                results.append((word, 0))
        else:
            if is_partial_anagram(target, word, max_diff):
                c2 = get_letter_counts(word)
                diff = sum(abs(target_counts.get(l, 0) - c2.get(l, 0)) for l in set(list(target_counts.keys()) + list(c2.keys())))
                results.append((word, diff // 2))
    return sorted(results, key=lambda x: x[1])

def reverse_word(word):
    return word[::-1]

def caesar_shift(word, shift):
    """Apply Caesar shift to a word (A=0, B=1, ...)."""
    result = ""
    for c in word.upper():
        if c.isalpha():
            result += chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
        else:
            result += c
    return result

def find_compound_splits(word, wordlist, min_part_len=2):
    """Find ways to split a word into known German words."""
    results = []
    word = word.upper()
    n = len(word)

    # Try all possible 2-part splits
    for i in range(min_part_len, n - min_part_len + 1):
        part1 = word[:i]
        part2 = word[i:]
        if part1 in wordlist and part2 in wordlist:
            results.append((part1, part2))

    # Try 3-part splits
    for i in range(min_part_len, n - 2 * min_part_len + 1):
        for j in range(i + min_part_len, n - min_part_len + 1):
            p1, p2, p3 = word[:i], word[i:j], word[j:]
            matches = sum(1 for p in [p1, p2, p3] if p in wordlist)
            if matches >= 2:  # at least 2 of 3 parts are known words
                results.append((p1, p2, p3, f"{matches}/3 matched"))

    return results

def generate_all_permutations_check(word, wordlist, max_len=10):
    """For short words, check all permutations against wordlist."""
    if len(word) > max_len:
        return []
    results = []
    seen = set()
    for perm in permutations(word.upper()):
        candidate = ''.join(perm)
        if candidate not in seen and candidate in wordlist:
            results.append(candidate)
            seen.add(candidate)
    return results

# ============================================================
# EXPANDED WORD LIST FROM GERMAN DICTIONARY
# ============================================================

def build_expanded_wordlist():
    """Build a comprehensive word list from various sources."""
    words = set(GERMAN_WORDS)

    # Add all German words from 3-18 letters that could be anagrams
    # Common German nouns, verbs, adjectives
    extra_words = [
        # Rulers/titles
        "SALZBURG", "NÜRNBERG", "REGENSBURG", "AUGSBURG", "MAGDEBURG",
        "STRASSBURG", "BRESLAU", "DANZIG", "GRAZ", "BASEL",
        "ERLKOENIG", "SIEGFRIED", "BRUNHILDE", "KRIEMHILD",
        "HAGEN", "ETZEL", "DIETRICH", "HILDEBRAND",
        # MHG terms
        "GEZELT", "GEWAFFEN", "BEREIT", "GEWALTIG", "MAECHTIG",
        "PRAECHTIG", "FUERCHTERLICH", "SCHRECKLICH", "GRAUSAM",
        "EHRFUERCHTIG", "ANDAECHTIG", "NACHLAESSIG",
        # Adjective endings
        "RICHTIG", "WICHTIG", "MAECHTIG", "PRAECHTIG", "SUECHTIG",
        "TRAEUCHTIG", "VERDAECHTIG", "BEDAECHTIG", "UEBERMAECHTIG",
        "ALLMAECHTIG", "GLEICHGUELTIG", "EHRFUERCHTIG",
        # -IG adjectives (without umlauts, as they appear in the cipher)
        "BERUCHTIG", "BERUCHTIGT",
        "EHRFURCHTIG", "ANDACHTIG", "NACHTIG",
        "PRACHTIG", "MACHTIG", "WICHTIG", "RICHTIG", "SUCHTIG",
        "TRACHTIG", "VERDACHTIG", "BEDACHTIG", "UBERMACHTIG",
        "ALLMACHTIG", "GEWALTIG", "KRAFTIG", "FLEISSIG",
        # Fantasy/archaic
        "SCHWARZKUENSTLER", "TOTENBESCHWORER", "RUNENSTEIN",
        "STEINTAFEL", "GRABSTEIN", "DENKSTEIN", "GRENZSTEIN",
        "HEILIGENSCHEIN", "TOTENSCHAEDEL", "SEELENSTEIN",
        # Words with exact letter sets matching our nouns
        "GALEERE", "GALERASS", "GALERAS", "SBERG",
        "SALZBERG", "BERGLAS", "GLASBERG", "GLASER",
        "LAZARETT", "LAZARUS", "ZEBRA", "GABEL",
        "BALG", "LAGER", "REGAL", "GRAL", "KLAGE",
        "SCHLAGE", "ERTRAGEN", "GETRAGEN",
        # More compounds
        "STEINREICH", "STEINZEIT", "STEINBRUCH",
        "TOTENREICH", "TOTENTANZ", "TODESRUNE",
        "RUNENMEISTER", "RUNENSTEIN", "RUNENORT",
        "KOENIGSREDE", "KOENIGREICH",
    ]

    for w in extra_words:
        words.add(w.upper())
        words.add(w.upper().replace("OE", "O").replace("UE", "U").replace("AE", "A"))

    return words

# ============================================================
# MAIN ANALYSIS
# ============================================================

def analyze_proper_noun(name, freq, context, wordlist):
    """Run comprehensive analysis on a single proper noun."""
    results = {
        'name': name,
        'freq': freq,
        'context': context,
        'reversed': reverse_word(name),
        'anagrams': [],
        'near_anagrams': [],
        'compound_splits': [],
        'caesar_shifts': [],
        'reversed_compounds': [],
        'substring_matches': [],
        'letter_frequency': dict(get_letter_counts(name)),
    }

    # 1. Exact anagram search
    results['anagrams'] = find_anagrams_in_wordlist(name, wordlist, max_diff=0)

    # 2. Near-anagram search (1-2 letter difference)
    results['near_anagrams'] = find_anagrams_in_wordlist(name, wordlist, max_diff=2)[:10]

    # 3. Brute-force permutation check (only for short words)
    if len(name) <= 9:
        results['permutation_matches'] = generate_all_permutations_check(name, wordlist)

    # 4. Compound word splits
    results['compound_splits'] = find_compound_splits(name, wordlist, min_part_len=2)

    # 5. Reversed word compound splits
    rev = reverse_word(name)
    results['reversed_compounds'] = find_compound_splits(rev, wordlist, min_part_len=2)

    # 6. Caesar shifts
    for shift in range(1, 26):
        shifted = caesar_shift(name, shift)
        if shifted in wordlist:
            results['caesar_shifts'].append((shift, shifted))
        # Also check reversed + shifted
        shifted_rev = caesar_shift(rev, shift)
        if shifted_rev in wordlist:
            results['caesar_shifts'].append((shift, f"REV+{shifted_rev}"))

    # 7. Substring matches (find known words hidden inside)
    for wlen in range(3, len(name)):
        for start in range(len(name) - wlen + 1):
            sub = name[start:start+wlen]
            if sub in wordlist and wlen >= 3:
                results['substring_matches'].append((start, sub))

    return results

def print_analysis(analysis):
    """Pretty-print analysis results."""
    print(f"\n{'='*70}")
    print(f"  {analysis['name']}  ({analysis['freq']}x)")
    print(f"  Context: {analysis['context']}")
    print(f"  Reversed: {analysis['reversed']}")
    print(f"  Letters: {analysis['letter_frequency']}")
    print(f"{'='*70}")

    if analysis['anagrams']:
        print(f"  *** EXACT ANAGRAMS: {analysis['anagrams']}")

    if analysis.get('permutation_matches'):
        print(f"  *** PERMUTATION MATCHES: {analysis['permutation_matches']}")

    if analysis['near_anagrams']:
        print(f"  Near-anagrams (1-2 diff): {analysis['near_anagrams'][:5]}")

    if analysis['compound_splits']:
        print(f"  Compound splits:")
        for split in analysis['compound_splits'][:5]:
            print(f"    {' + '.join(str(s) for s in split)}")

    if analysis['reversed_compounds']:
        print(f"  Reversed compound splits ({analysis['reversed']}):")
        for split in analysis['reversed_compounds'][:5]:
            print(f"    {' + '.join(str(s) for s in split)}")

    if analysis['caesar_shifts']:
        print(f"  Caesar shifts: {analysis['caesar_shifts']}")

    if analysis['substring_matches']:
        subs = [(s, sub) for s, sub in analysis['substring_matches'] if len(sub) >= 3]
        if subs:
            print(f"  Substrings found: {subs[:8]}")

    if not any([analysis['anagrams'], analysis.get('permutation_matches'),
                analysis['compound_splits'], analysis['reversed_compounds'],
                analysis['caesar_shifts']]):
        print(f"  (No matches found)")

# ============================================================
# SPECIAL ANALYSES
# ============================================================

def analyze_eilchanhearuchtig():
    """Deep analysis of the long compound adjective."""
    word = "EILCHANHEARUCHTIG"
    print("\n" + "="*70)
    print("DEEP ANALYSIS: EILCHANHEARUCHTIG")
    print("="*70)

    # Try all possible 2-part splits
    print("\n--- All 2-part splits ---")
    for i in range(2, len(word)-1):
        p1, p2 = word[:i], word[i:]
        notes = []
        if "RICHTIG" in p2: notes.append("contains RICHTIG (correct)")
        if "WICHTIG" in p2: notes.append("contains WICHTIG (important)")
        if "MACHTIG" in p2: notes.append("contains MACHTIG (powerful)")
        if "UCHTIG" in p2: notes.append("ends -UCHTIG (addiction/tendency)")
        if "ACHTIG" in p2: notes.append("ends -ACHTIG (like/similar)")
        if "PRACHTIG" in p2: notes.append("contains PRACHTIG (splendid)")
        if "BERUCHTIG" in p2: notes.append("contains BERUCHTIG (notorious)")
        if p1 in ["EIL", "EILCH", "EI", "EILCHAN"]: notes.append(f"prefix: {p1}")
        if "RUCHTIG" in p2: notes.append("*** RUCHTIG = notorious (MHG) ***")
        if "HEARUCHTIG" in p2: notes.append("*** HEARUCHTIG = honorable/glorious? ***")
        if "AN" in p1[-2:] and "HEARUCHTIG" in p2:
            notes.append("*** EILCH AN HEARUCHTIG = Eilch at/on the notorious? ***")
        if notes:
            print(f"  {p1} | {p2} -- {'; '.join(notes)}")

    # Try 3-part splits focusing on -AN- as separator
    print("\n--- 3-part splits with AN ---")
    an_pos = word.find("AN")
    while an_pos >= 0:
        p1 = word[:an_pos]
        p3 = word[an_pos+2:]
        if p1 and p3:
            print(f"  {p1} + AN + {p3}")
            # Further split p3
            for j in range(2, len(p3)):
                pp1, pp2 = p3[:j], p3[j:]
                if "UCHTIG" in pp2 or "RICHTIG" in pp2:
                    print(f"    => {p1} + AN + {pp1} + {pp2}")
        an_pos = word.find("AN", an_pos + 1)

    # Try as anagram of known German compounds
    print("\n--- Letter analysis ---")
    counts = get_letter_counts(word)
    print(f"  Letters: {dict(counts)}")
    print(f"  Total: {sum(counts.values())} chars")
    print(f"  Vowels: {sum(counts.get(v, 0) for v in 'AEIOU')} ({sum(counts.get(v, 0) for v in 'AEIOU')/len(word)*100:.0f}%)")

    # Check if EILCH could be a word
    print("\n--- EILCH analysis ---")
    print("  EILCH reversed = HCLIE")
    print("  ELCH = elk/moose (German animal)")
    print("  If I and L swapped: ELICH -> ELICH = MHG 'elich' (legitimate/lawful)")
    print("  EILCHANHEARUCHTIG -> ELICH AN HEARUCHTIG?")
    print("  = 'the legitimate/lawful one at the notorious [place]'?")

def analyze_edetotniurgs():
    """Deep analysis of EDETOTNIURGS."""
    word = "EDETOTNIURGS"
    print("\n" + "="*70)
    print("DEEP ANALYSIS: EDETOTNIURGS")
    print("="*70)

    print("\n--- Known components ---")
    print("  Contains: EDE + TOT + NIURG + S")
    print("  TOTNIURG reversed = GRUINTOT")
    print("  EDE could be: EDEL (noble) without L?")
    print("  Or: E + DE + TOTNIURGS = 'it the TOTNIURGS'")

    # Reversed
    rev = reverse_word(word)
    print(f"\n  Reversed: {rev}")
    print(f"  SGRUINTOTEDE")
    print(f"  S + GRUIN + TOT + EDE")
    print(f"  S + GRUEN + TOT + EDE = 's green death noble'?")

    # Try compound splits
    print("\n--- Meaningful splits ---")
    splits = [
        ("EDE", "TOTNIURGS", "EDE (noble lineage) + TOTNIURGS (of the death ruin)"),
        ("EDET", "OT", "NIURGS", "unclear"),
        ("E", "DE", "TOTNIURG", "S", "article + proper noun + genitive-S"),
        ("EDEL", "-missing L-", "TOTNIURGS", "EDEL (noble) + TOTNIURGS?"),
    ]
    for s in splits:
        print(f"  {' | '.join(s[:-1])} -- {s[-1]}")

def analyze_aunrsongetrases():
    """Deep analysis of the most common unrecognized phrase."""
    word = "AUNRSONGETRASES"
    print("\n" + "="*70)
    print("DEEP ANALYSIS: AUNRSONGETRASES (11 occurrences)")
    print("="*70)

    rev = reverse_word(word)
    print(f"  Reversed: {rev}")

    print("\n--- Contains GETRAS ---")
    print("  GETRAS could be from MHG 'getragen' (carried/worn)")
    print("  GE- prefix = past participle marker")
    print("  TRAS = from 'tragen' (to carry)")
    print("  AUNR + SON + GETRASES")
    print("  = 'AUNR son [of the] carried-ones'?")

    print("\n--- Anagram test ---")
    counts = get_letter_counts(word)
    print(f"  Letters: {dict(counts)}")
    print(f"  Has double: S(3), E(2), A(2), R(2), N(2)")

    print("\n--- SONGETRASES ---")
    print("  SON = son (MHG/English)")
    print("  GETRASES = past participle variant?")
    print("  AUN + R + SONGETRASES")

    # As anagram of known German phrases
    print("\n--- Subset search ---")
    # Check if any long German word uses these exact letters
    print("  AUSGETRAGEN = carried out (15 letters)")
    print("  AUNRSONGETRASES has 15 letters")
    ag_counts = get_letter_counts("AUSGETRAGEN")
    print(f"  AUSGETRAGEN letters: {dict(ag_counts)}")
    print(f"  AUNRSONGETRASES letters: {dict(counts)}")

    # Compare
    diff_letters = []
    all_l = set(list(counts.keys()) + list(ag_counts.keys()))
    for l in sorted(all_l):
        c1, c2 = counts.get(l, 0), ag_counts.get(l, 0)
        if c1 != c2:
            diff_letters.append(f"{l}: ours={c1} vs AUSGETRAGEN={c2}")
    if diff_letters:
        print(f"  Differences: {diff_letters}")
    else:
        print("  *** EXACT ANAGRAM! ***")

def analyze_schwiteione():
    """Deep analysis of SCHWITEIONE."""
    word = "SCHWITEIONE"
    print("\n" + "="*70)
    print("DEEP ANALYSIS: SCHWITEIONE (10x, possibly bonelord race name)")
    print("="*70)

    counts = get_letter_counts(word)
    print(f"  Letters: {dict(counts)}")
    print(f"  Reversed: {reverse_word(word)}")

    print("\n--- Compound splits ---")
    print("  SCHWIT + EIONE")
    print("  SCHW + ITEIONE")
    print("  SCH + WITEIONE")
    print("  SCH + WIT + EIONE")
    print("  SCHWI + TEIONE")
    print("  SCHWI + TEI + ONE")

    print("\n--- Anagram candidates ---")
    # SCHWITEIONE has 11 letters: C E H I I N O S T W E
    # Check EINWEIHSTORC, etc.
    candidates = [
        "EINWEIHSTOC",  # not a word but close to EINWEIHUNG (inauguration)
        "STEINWEICHE",  # stone-soft?
        "WEIHNACHSTE",  # close to Christmas?
        "WISSENSCHE",   # scientific?
        "GESCHICHTEN",  # stories (10 letters, close)
    ]
    for c in candidates:
        if is_anagram(word, c):
            print(f"  *** EXACT ANAGRAM: {c} ***")
        elif is_partial_anagram(word, c, 2):
            diff = sum(abs(counts.get(l, 0) - get_letter_counts(c).get(l, 0))
                      for l in set(list(counts.keys()) + list(get_letter_counts(c).keys())))
            print(f"  Near anagram ({diff//2} diff): {c}")

    # More systematic check
    print("\n--- Contains ---")
    subwords = ["SCHW", "WEIT", "STEIN", "WEISS", "SCHWEIN", "EICHE", "WOCHE",
                "SCHEINT", "SEICHT", "WEICHE", "TEICH", "WISCHE", "TISCHE",
                "NISCHE", "EICHHORN", "SEITWICH"]
    for sw in subwords:
        if all(counts.get(l, 0) >= get_letter_counts(sw).get(l, 0) for l in get_letter_counts(sw)):
            remaining = dict(counts)
            for l in sw:
                remaining[l] -= 1
            rem_str = ''.join(l*c for l, c in sorted(remaining.items()) if c > 0)
            print(f"  {sw} + [{rem_str}]")

def analyze_labgzeras():
    """Deep analysis of the king's name."""
    word = "LABGZERAS"
    print("\n" + "="*70)
    print("DEEP ANALYSIS: LABGZERAS (king's name)")
    print("="*70)

    counts = get_letter_counts(word)
    print(f"  Letters: {dict(counts)}")
    print(f"  Reversed: {reverse_word(word)} = SAREZGBAL")

    print("\n--- Known Tibia kings for comparison ---")
    tibia_kings = ["TIBIANUS", "YORIK", "RODMUND", "OTTREMAR", "ZELOS",
                   "ILGRAM", "XENOM", "HONEMINAS"]
    for tk in tibia_kings:
        if is_partial_anagram(word, tk, 3):
            diff = sum(abs(counts.get(l, 0) - get_letter_counts(tk).get(l, 0))
                      for l in set(list(counts.keys()) + list(get_letter_counts(tk).keys())))
            print(f"  Near anagram ({diff//2} diff) of {tk}")

    print("\n--- Anagram candidates ---")
    candidates = [
        "GLASBERG", "SALZBERG", "BERGLAS", "GALEERS",
        "ERZGABEL", "GRABSEEL", "LAZEBERG",
        "GALSBERG", "LASBERG", "GALERBS",
        "SAALBERG", "BERGSAL",
    ]
    for c in candidates:
        c_counts = get_letter_counts(c)
        if is_anagram(word, c):
            print(f"  *** EXACT ANAGRAM: {c} ***")
        elif is_partial_anagram(word, c, 1):
            print(f"  Near: {c}")

    print("\n--- Compound splits ---")
    print("  LAB + G + ZERAS")
    print("  LABG + ZERAS")
    print("  LAB + GZERAS")
    print("  L + AB + GZERAS")
    print("  LAB shares prefix with LABRNI")
    print("  ZERAS could relate to ZORN (anger) / ZERASS / ZERAS (tear apart)")

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  BONELORD 469 - DEEP ANAGRAM & COMPOUND WORD ATTACK")
    print("=" * 70)

    wordlist = build_expanded_wordlist()
    print(f"\nWord list: {len(wordlist)} words")

    # Run analysis on all proper nouns
    all_analyses = []
    for name, (freq, context) in PROPER_NOUNS.items():
        analysis = analyze_proper_noun(name, freq, context, wordlist)
        all_analyses.append(analysis)
        print_analysis(analysis)

    # Run deep analyses on key nouns
    analyze_eilchanhearuchtig()
    analyze_edetotniurgs()
    analyze_aunrsongetrases()
    analyze_schwiteione()
    analyze_labgzeras()

    # Summary of all findings
    print("\n" + "=" * 70)
    print("  SUMMARY OF FINDINGS")
    print("=" * 70)

    hits = []
    for a in all_analyses:
        if a['anagrams'] or a.get('permutation_matches') or a['compound_splits'] or a['reversed_compounds'] or a['caesar_shifts']:
            hits.append(a['name'])

    if hits:
        print(f"\n  Nouns with matches: {hits}")
    else:
        print(f"\n  No exact matches found. The proper nouns are likely:")
        print(f"    1. Invented names specific to bonelord lore")
        print(f"    2. MHG (Middle High German) vocabulary not in our wordlist")
        print(f"    3. Multi-word phrases that need different word boundaries")

    # Cross-reference: do any nouns share letter patterns?
    print("\n--- Cross-noun letter sharing ---")
    for n1, (f1, c1) in PROPER_NOUNS.items():
        for n2, (f2, c2) in PROPER_NOUNS.items():
            if n1 >= n2:
                continue
            shared = sum(min(get_letter_counts(n1).get(l, 0), get_letter_counts(n2).get(l, 0))
                        for l in set(n1) & set(n2))
            ratio = shared / max(len(n1), len(n2))
            if ratio > 0.5 and len(n1) >= 4 and len(n2) >= 4:
                print(f"  {n1} <-> {n2}: {shared} shared letters ({ratio:.0%})")
