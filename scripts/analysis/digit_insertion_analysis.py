#!/usr/bin/env python3
"""
Digit Insertion Analysis for Bonelord 469 Cipher
==================================================
For each of the 37 odd-length books, try inserting EACH digit (0-9) at EACH
position to find the optimal (digit, position) that maximizes word coverage.

Key insight: the old pipeline always inserted '0', but the CORRECT digit may
differ per book. This script tests all 10 digits systematically.

This is a research/analysis script - it does NOT modify narrative_v3_clean.py.
"""

import json, os, sys, time
from collections import Counter
from itertools import permutations

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)

# ============================================================
# IC-based offset detection (from narrative_v3_clean.py)
# ============================================================
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

# ============================================================
# KNOWN WORDS for segmentation (from narrative_v3_clean.py)
# ============================================================
KNOWN = set([
    # Articles, pronouns, prepositions
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    # Short verbs/particles
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR',
    # Common words
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
    'ZEHN', 'ZORN',
    # Verbs
    'FINDEN', 'GEBEN', 'GEHEN', 'HABEN', 'KOMMEN', 'LEBEN', 'LESEN',
    'NEHMEN', 'SAGEN', 'SEHEN', 'STEHEN', 'SUCHEN', 'WISSEN',
    'WISSET', 'RUFEN', 'WIEDER',
    # MHG / archaic
    'OEL', 'SCE', 'MINNE', 'MIN',
    'ODE',
    'SER',
    'GEN',
    'INS',
    'GEIGET',
    'BERUCHTIG', 'BERUCHTIGER',
    'MEERE',
    'NEIGT',
    'WISTEN',
    'MANIER',
    'HUND',
    'GODE',
    'EIGENTUM',
    'REDER',
    'THENAEUT',
    'LABT',
    'MORT',
    'DIGE', 'WEGE',
    'KOENIGS',
    'NAHE',
    'NOT',
    'NOTH',
    'ZUR',
    'OWI',
    'ENGE',
    'SEIDEN',
    'ALTES',
    'DENN',
    'BIS',
    'NIE',
    'NUT', 'NUTZ',
    'HEIL',
    'NEID',
    'TREU', 'TREUE',
    # Resolved anagrams
    'KOENIG',
    'DASS',
    'EDEL', 'ADEL',
    # Proper nouns
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME',
    'SCHARDT',
])

# ============================================================
# Anagram map (from narrative_v3_clean.py)
# ============================================================
ANAGRAM_MAP = {
    'LABGZERAS': 'SALZBERG',
    'SCHWITEIONE': 'WEICHSTEIN',
    'SCHWITEIO': 'WEICHSTEIN',
    'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'EDETOTNIURG': 'GOTTDIENER',
    'EDETOTNIURGS': 'GOTTDIENERS',
    'ADTHARSC': 'SCHARDT',
    'TAUTR': 'TRAUT',
    'EILCH': 'LEICH',
    'HEDEMI': 'HEIME',
    'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG',
    'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE',
    'TEIGN': 'NEIGT',
    'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER',
    'AODGE': 'GODE',
}

# ============================================================
# DP word segmentation (from narrative_v3_clean.py)
# ============================================================
def dp_segment(text):
    """Segment text into known words and unknown blocks."""
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
    # Backtrack
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

    # Merge consecutive unknown chars
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

# ============================================================
# Decode a book string to letters
# ============================================================
def decode_book(book_str):
    """Decode a raw digit string to letters using v7 mapping + IC offset."""
    off = get_offset(book_str)
    pairs = [book_str[j:j+2] for j in range(off, len(book_str)-1, 2)]
    text = ''.join(v7.get(p, '?') for p in pairs)
    return text

def apply_anagrams(text):
    """Apply anagram resolutions (longest first)."""
    for anagram in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
        text = text.replace(anagram, ANAGRAM_MAP[anagram])
    return text

def coverage_of(text):
    """Return (covered_chars, total_known_chars) from DP segmentation."""
    _, covered = dp_segment(text)
    total_known = sum(1 for c in text if c != '?')
    return covered, total_known

# ============================================================
# GERMAN WORD LIST for anagram detection (5+ letters)
# ============================================================
GERMAN_5PLUS = set([
    # Common German words 5+ letters for anagram scanning
    'ABEND', 'ABENDS', 'ACKER', 'ADLER', 'ALTER', 'ALTES', 'ANGEL',
    'ARBEIT', 'ASCHE', 'AUGE', 'AUGEN',
    'BAUER', 'BAUEN', 'BERGE', 'BERUF', 'BLATT', 'BLICK', 'BLUME',
    'BLUMEN', 'BLUT', 'BODEN', 'BRAND', 'BRAUN', 'BREIT', 'BRIEF',
    'BRINGEN', 'BRUDER', 'BRUST', 'BUCHE', 'BURG',
    'DAMEN', 'DAMPF', 'DEGEN', 'DEINE', 'DEINEN', 'DEINER',
    'DIENER', 'DIENST', 'DONNER', 'DRACHE', 'DUNKEL',
    'EHRE', 'EHREN', 'EICHE', 'EIGEN', 'EISEN', 'ELEND',
    'ENGEL', 'ERBEN', 'ERNTE', 'EWIGE', 'EWIG',
    'FACKEL', 'FAHNE', 'FAHRT', 'FALKE', 'FALLE', 'FARBE',
    'FEDER', 'FEIER', 'FEIND', 'FEINDE', 'FELDS', 'FELSEN',
    'FEUER', 'FICHTE', 'FLUCH', 'FLUSS', 'FORST', 'FRAGE',
    'FRIEDE', 'FRIEDEN', 'FROST', 'FUCHS', 'FUERST', 'FURCHT',
    'GARTEN', 'GEBET', 'GEGEN', 'GEHEIM', 'GEIST', 'GERICHT',
    'GLAUBE', 'GLEICH', 'GLOCKE', 'GNADE', 'GRABEN', 'GRENZE',
    'GRUBE', 'GRUFT', 'GRUEN', 'GRUND', 'GUNST',
    'HAFEN', 'HALTE', 'HALTEN', 'HANDEL', 'HAUPT', 'HECKE',
    'HEIDE', 'HEILIG', 'HEISS', 'HERRN', 'HERZEN', 'HILFE',
    'HIMMEL', 'HOEHE', 'HORDE', 'HUEGEL', 'HUETER',
    'INSEL', 'IRREN',
    'JAGEN', 'JENER', 'JUGEND',
    'KAMPF', 'KELLER', 'KETTE', 'KIRCHE', 'KLAGE', 'KLEID',
    'KLEIN', 'KLINGE', 'KNABE', 'KNECHT', 'KNOCHEN', 'KOENIG',
    'KOENIGIN', 'KOENIGS', 'KRAFT', 'KRANZ', 'KREIS', 'KREUZ',
    'KRIEG', 'KRONE', 'KUGEL', 'KUNST',
    'LAGER', 'LANDE', 'LANDEN', 'LANGE', 'LANZE', 'LAUBE',
    'LEBER', 'LEGEN', 'LEHRE', 'LEICHE', 'LEINE', 'LEISE',
    'LESEN', 'LEUTE', 'LICHT', 'LIEBE', 'LIEDER', 'LINDE',
    'LINKE', 'LOEWE',
    'MAGEN', 'MAHNE', 'MARKT', 'MAUER', 'MEILE', 'MEISTER',
    'MENGE', 'MESSER', 'MITTE', 'MITTEN', 'MONAT', 'MORGEN',
    'MUEHE', 'MUTTER',
    'NABEL', 'NACHBAR', 'NAMEN', 'NATUR', 'NEBEL', 'NEBEN',
    'NEID', 'NORDEN', 'NUTZEN',
    'OSTEN', 'OSTERN',
    'PACHT', 'PERLE', 'PFAD', 'PFEIL', 'PFLICHT', 'PLATZ',
    'PREIS', 'PRIESTER', 'PRINZ', 'PROBE',
    'QUELLE',
    'RACHE', 'RASTE', 'RATTE', 'RAUCH', 'RAUM', 'REBEN',
    'RECHT', 'REGEN', 'REISE', 'REITER', 'RETTER', 'RICHTE',
    'RITTER', 'RUDER', 'RUEHE', 'RUINE',
    'SACHE', 'SAGEN', 'SCHAF', 'SCHATZ', 'SCHATTEN', 'SCHEIN',
    'SCHERZ', 'SCHILD', 'SCHLAF', 'SCHLAG', 'SCHLANGE',
    'SCHLECHT', 'SCHLOSS', 'SCHLUCK', 'SCHMERZ', 'SCHNEE',
    'SCHRIFT', 'SCHULD', 'SCHULE', 'SCHUTZ', 'SCHWACH',
    'SCHWERT', 'SEELE', 'SEGEN', 'SEIDEN', 'SEITE', 'SEITEN',
    'SICHER', 'SIEGE', 'SIEGEL', 'SILBER', 'SITTE', 'SOMMER',
    'SORGE', 'SPEER', 'SPIEGEL', 'SPRACHE', 'SPRUCH',
    'STAAT', 'STAHL', 'STAMM', 'STAND', 'STARK', 'STATT',
    'STAUB', 'STEHEN', 'STEINE', 'STELLE', 'STIMME',
    'STOLZ', 'STRAFE', 'STRAHL', 'STRAND', 'STRASSE',
    'STROM', 'STURM', 'SUCHE', 'SUEDEN', 'SUMPF',
    'TAFEL', 'TATEN', 'TEMPEL', 'TIERE', 'TINTE', 'TISCH',
    'TITEL', 'TOCHTER', 'TREUE', 'TREIBEN', 'TROTZ', 'TRUHE',
    'TRUPPE', 'TUGEND',
    'UEBER', 'UNTER', 'URALT', 'URALTE',
    'VATER', 'VOEGEL', 'VORNE',
    'WAFFE', 'WAGEN', 'WAHRE', 'WALDE', 'WAPPEN', 'WARUM',
    'WASSER', 'WEBEN', 'WEIDE', 'WEISE', 'WEITE', 'WELLE',
    'WENDE', 'WESTEN', 'WINTER', 'WIRKEN', 'WISSEN',
    'WOCHEN', 'WOLKE', 'WUERDE', 'WUNDE', 'WUNDER', 'WUNSCH',
    'WUESTE', 'WURZEL',
    'ZANGE', 'ZAUBER', 'ZEICHEN', 'ZEILE', 'ZIEGE', 'ZUNGE',
    # Also include the KNOWN set words that are 5+ letters
])
GERMAN_5PLUS.update(w for w in KNOWN if len(w) >= 5)

# ============================================================
# MAIN ANALYSIS
# ============================================================
print("=" * 70)
print("DIGIT INSERTION ANALYSIS")
print("Testing all 10 digits at all positions for 37 odd-length books")
print("=" * 70)

# Step 1: Identify odd-length books
odd_books = []
for bidx, book in enumerate(books):
    if len(book) % 2 == 1:
        odd_books.append(bidx)

print(f"\nFound {len(odd_books)} odd-length books: {odd_books}")

# Step 2: Baseline - decode all books WITHOUT any insertions
baseline_decoded = []
for bidx, book in enumerate(books):
    baseline_decoded.append(decode_book(book))

baseline_all = ''.join(baseline_decoded)
baseline_resolved = apply_anagrams(baseline_all)
_, baseline_total_covered = dp_segment(baseline_resolved)
baseline_total_known = sum(1 for c in baseline_resolved if c != '?')
baseline_pct = baseline_total_covered / max(baseline_total_known, 1) * 100
print(f"\nBASELINE (no insertions):")
print(f"  Total text length: {len(baseline_resolved)} chars")
print(f"  Word coverage: {baseline_total_covered}/{baseline_total_known} = {baseline_pct:.1f}%")

# Step 3: For each odd-length book, try all (digit, position) combos
print(f"\n{'=' * 70}")
print("PER-BOOK OPTIMAL DIGIT INSERTIONS")
print(f"{'=' * 70}")

optimal_insertions = {}  # bidx -> (digit, position, coverage, delta, text)
t0 = time.time()

for bidx in odd_books:
    book = books[bidx]
    book_len = len(book)

    # Baseline for this book (no insertion)
    base_text = decode_book(book)
    base_resolved = apply_anagrams(base_text)
    base_cov, base_known = coverage_of(base_resolved)

    best_digit = None
    best_pos = None
    best_cov = base_cov
    best_text = base_text
    best_resolved = base_resolved

    # Try each digit 0-9 at each position 0..len(book)
    for digit in range(10):
        d = str(digit)
        for pos in range(book_len + 1):
            trial_book = book[:pos] + d + book[pos:]
            trial_text = decode_book(trial_book)
            trial_resolved = apply_anagrams(trial_text)
            trial_cov, trial_known = coverage_of(trial_resolved)

            if trial_cov > best_cov:
                best_cov = trial_cov
                best_digit = digit
                best_pos = pos
                best_text = trial_text
                best_resolved = trial_resolved

    delta = best_cov - base_cov
    if best_digit is not None:
        optimal_insertions[bidx] = (best_digit, best_pos, best_cov, delta, best_text, best_resolved)

elapsed = time.time() - t0
print(f"\nSearch completed in {elapsed:.1f}s")

# Sort by delta (improvement), descending
sorted_opts = sorted(optimal_insertions.items(), key=lambda x: -x[1][3])

print(f"\n{'Book':>5} {'Digit':>6} {'Pos':>5} {'Base':>5} {'New':>5} {'Delta':>6} | Decoded text (first 80 chars)")
print("-" * 130)
for bidx, (digit, pos, cov, delta, text, resolved) in sorted_opts:
    base_text = decode_book(books[bidx])
    base_resolved = apply_anagrams(base_text)
    base_cov, _ = coverage_of(base_resolved)
    tokens, _ = dp_segment(resolved)
    segmented = ' '.join(tokens)[:80]
    print(f"  {bidx:3d}   d={digit}   {pos:4d}   {base_cov:4d}   {cov:4d}  {delta:+5d}  | {segmented}")

# Books with no improvement
no_improve = [bidx for bidx in odd_books if bidx not in optimal_insertions]
if no_improve:
    print(f"\nBooks with no improvement from any insertion: {no_improve}")

# Step 4: Apply ALL optimal insertions and decode full text
print(f"\n{'=' * 70}")
print("FULL TEXT WITH ALL OPTIMAL INSERTIONS ENABLED")
print(f"{'=' * 70}")

inserted_decoded = []
for bidx, book in enumerate(books):
    if bidx in optimal_insertions:
        digit, pos, _, _, _, _ = optimal_insertions[bidx]
        modified_book = book[:pos] + str(digit) + book[pos:]
        inserted_decoded.append(decode_book(modified_book))
    else:
        inserted_decoded.append(decode_book(book))

inserted_all = ''.join(inserted_decoded)
inserted_resolved = apply_anagrams(inserted_all)
_, inserted_total_covered = dp_segment(inserted_resolved)
inserted_total_known = sum(1 for c in inserted_resolved if c != '?')
inserted_pct = inserted_total_covered / max(inserted_total_known, 1) * 100

print(f"\nWith ALL optimal insertions:")
print(f"  Total text length: {len(inserted_resolved)} chars")
print(f"  Word coverage: {inserted_total_covered}/{inserted_total_known} = {inserted_pct:.1f}%")
print(f"  vs Baseline:     {baseline_total_covered}/{baseline_total_known} = {baseline_pct:.1f}%")
print(f"  Delta: {inserted_total_covered - baseline_total_covered:+d} chars ({inserted_pct - baseline_pct:+.1f}%)")

# Step 5: Check which ANAGRAM_MAP entries break
print(f"\n{'=' * 70}")
print("ANAGRAM MAP SURVIVAL CHECK")
print(f"{'=' * 70}")

# Check in per-book decoded text (before anagram resolution)
inserted_raw = ''.join(inserted_decoded)
baseline_raw = ''.join(baseline_decoded)

print(f"\n{'Anagram Pattern':<25} {'Baseline':>10} {'Inserted':>10} {'Status':<10}")
print("-" * 60)
broken_anagrams = []
surviving_anagrams = []
for anagram, resolved in sorted(ANAGRAM_MAP.items(), key=lambda x: -len(x[0])):
    in_base = anagram in baseline_raw
    in_inserted = anagram in inserted_raw
    if in_base and not in_inserted:
        status = "BROKEN"
        broken_anagrams.append(anagram)
    elif in_base and in_inserted:
        status = "OK"
        surviving_anagrams.append(anagram)
    elif not in_base and in_inserted:
        status = "NEW"
        surviving_anagrams.append(anagram)
    else:
        status = "absent"
    print(f"  {anagram:<23} {'yes' if in_base else 'no':>10} {'yes' if in_inserted else 'no':>10} {status:<10}")

if broken_anagrams:
    print(f"\n  WARNING: {len(broken_anagrams)} anagram(s) BROKEN by insertions: {broken_anagrams}")
else:
    print(f"\n  All existing anagram patterns survive.")

# Step 6: Scan for NEW anagram-like patterns (5+ letter German words)
print(f"\n{'=' * 70}")
print("NEW ANAGRAM-LIKE PATTERNS (5+ letter German words)")
print(f"{'=' * 70}")

def find_anagram_matches(text, word_set, min_len=5, max_len=15):
    """Find substrings that are anagrams of words in word_set."""
    matches = []
    for wlen in range(min_len, max_len + 1):
        for i in range(len(text) - wlen + 1):
            substr = text[i:i+wlen]
            if '?' in substr:
                continue
            sorted_sub = ''.join(sorted(substr))
            for word in word_set:
                if len(word) == wlen and ''.join(sorted(word)) == sorted_sub:
                    if substr != word:  # Only actual anagrams, not exact matches
                        matches.append((i, substr, word))
    return matches

# Find anagrams in the inserted text that are NOT in the baseline
print("\nScanning for anagram patterns in inserted text (this may take a moment)...")
t1 = time.time()

# Use the raw decoded text (before anagram resolution) for scanning
new_anagrams = find_anagram_matches(inserted_raw, GERMAN_5PLUS, min_len=5, max_len=15)
old_anagrams_set = set()
old_anagrams = find_anagram_matches(baseline_raw, GERMAN_5PLUS, min_len=5, max_len=15)
for _, substr, word in old_anagrams:
    old_anagrams_set.add((substr, word))

elapsed2 = time.time() - t1
print(f"Scan completed in {elapsed2:.1f}s")

truly_new = [(pos, substr, word) for pos, substr, word in new_anagrams
             if (substr, word) not in old_anagrams_set]

if truly_new:
    print(f"\n  Found {len(truly_new)} NEW anagram patterns:")
    # Deduplicate by (substr, word)
    seen = set()
    for pos, substr, word in truly_new:
        key = (substr, word)
        if key not in seen:
            seen.add(key)
            print(f"    pos {pos:4d}: {substr} -> {word}")
else:
    print("\n  No new anagram patterns found.")

# Also list anagrams lost
lost_anagrams_set = set()
for _, substr, word in old_anagrams:
    if (substr, word) not in set((s, w) for _, s, w in new_anagrams):
        lost_anagrams_set.add((substr, word))

if lost_anagrams_set:
    print(f"\n  {len(lost_anagrams_set)} anagram pattern(s) LOST:")
    for substr, word in sorted(lost_anagrams_set):
        print(f"    {substr} -> {word}")

# Step 7: Compare digit=0 vs optimal digit
print(f"\n{'=' * 70}")
print("DIGIT=0 vs OPTIMAL DIGIT COMPARISON")
print(f"{'=' * 70}")

print(f"\n{'Book':>5} {'Opt.Digit':>10} {'Opt.Pos':>8} {'d=0 best pos':>13} {'d=0 cov':>8} {'Opt cov':>8} {'Diff':>6}")
print("-" * 75)
for bidx in odd_books:
    book = books[bidx]
    book_len = len(book)

    # Best with digit=0
    base_text = decode_book(book)
    base_resolved = apply_anagrams(base_text)
    base_cov, _ = coverage_of(base_resolved)

    best_0_cov = base_cov
    best_0_pos = -1
    for pos in range(book_len + 1):
        trial_book = book[:pos] + '0' + book[pos:]
        trial_text = decode_book(trial_book)
        trial_resolved = apply_anagrams(trial_text)
        trial_cov, _ = coverage_of(trial_resolved)
        if trial_cov > best_0_cov:
            best_0_cov = trial_cov
            best_0_pos = pos

    # Optimal
    if bidx in optimal_insertions:
        opt_digit, opt_pos, opt_cov, _, _, _ = optimal_insertions[bidx]
        diff = opt_cov - best_0_cov
        marker = " ***" if diff > 0 and opt_digit != 0 else ""
        print(f"  {bidx:3d}   d={opt_digit:1d}       {opt_pos:5d}       {best_0_pos:5d}     {best_0_cov:4d}     {opt_cov:4d}  {diff:+4d}{marker}")
    else:
        print(f"  {bidx:3d}   none       -            {best_0_pos:5d}     {best_0_cov:4d}     {base_cov:4d}    +0")

# Step 8: Summary
print(f"\n{'=' * 70}")
print("SUMMARY")
print(f"{'=' * 70}")

total_delta = sum(v[3] for v in optimal_insertions.values())
improved_books = sum(1 for v in optimal_insertions.values() if v[3] > 0)
non_zero_digit = sum(1 for v in optimal_insertions.values() if v[0] != 0 and v[3] > 0)

print(f"""
  Odd-length books:         {len(odd_books)}
  Books improved:           {improved_books} (of {len(odd_books)})
  Total char improvement:   {total_delta:+d}
  Books where d!=0 is best: {non_zero_digit}

  Baseline coverage:        {baseline_total_covered}/{baseline_total_known} = {baseline_pct:.1f}%
  With optimal insertions:  {inserted_total_covered}/{inserted_total_known} = {inserted_pct:.1f}%
  Net change:               {inserted_total_covered - baseline_total_covered:+d} chars ({inserted_pct - baseline_pct:+.1f}%)

  Broken anagrams:          {len(broken_anagrams)}
  Surviving anagrams:       {len(surviving_anagrams)}
""")

# Print the top-10 most impactful insertions with full decoded text
print(f"{'=' * 70}")
print("TOP 10 MOST IMPACTFUL INSERTIONS - FULL DECODED TEXT")
print(f"{'=' * 70}")

for bidx, (digit, pos, cov, delta, text, resolved) in sorted_opts[:10]:
    tokens, _ = dp_segment(resolved)
    segmented = ' '.join(tokens)
    base_text = decode_book(books[bidx])
    base_resolved = apply_anagrams(base_text)
    base_tokens, _ = dp_segment(base_resolved)
    base_segmented = ' '.join(base_tokens)

    print(f"\n  Book {bidx} (insert d={digit} at pos {pos}, delta={delta:+d}):")
    print(f"    BEFORE: {base_segmented}")
    print(f"    AFTER:  {segmented}")
