#!/usr/bin/env python3
"""
Crib Attack on Garbled Segments
================================
Analyzes the most common garbled (un-parseable) segments in the decoded text.
For each, traces the raw cipher codes and systematically tests which letter
reassignments would produce valid German words/phrases.

Key insight: I is over-represented by +3.73% (8 codes assigned to I).
Some I codes likely should be B, F, P, or M (all under-represented).

Target segments (from gap analysis):
- [WRLGTNELNRHELU] x6 (14 chars)
- [NTENTTUIGAA] x4 (11 chars)
- [DRTHENAEU] x3 (9 chars)
- [LGTNELGZ] x3 (8 chars)
- [HECHLLT] x5 (7 chars)
- [WIISETN] x3 (7 chars)
- [TIURIT] x3 (6 chars)
- [NDTEII] x5 (6 chars)
- [GEIGET] x4 (6 chars)
"""

import json, os, sys
from collections import Counter
from itertools import product

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

MAPPING = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U',
    '00': 'H', '14': 'N', '72': 'R', '91': 'S', '15': 'I',
    '76': 'E', '52': 'S', '42': 'D', '46': 'I', '48': 'N',
    '57': 'H', '04': 'M', '12': 'S', '58': 'N',
    '78': 'T', '51': 'R', '35': 'A', '34': 'L',
    '01': 'E', '59': 'S', '41': 'E', '30': 'E',
    '94': 'H',
    '47': 'D', '13': 'N', '71': 'I', '63': 'D',
    '93': 'N', '28': 'D', '86': 'E', '43': 'U',
    '70': 'U', '65': 'I', '16': 'I', '36': 'W',
    '64': 'T', '89': 'A', '80': 'G', '97': 'G', '75': 'T',
    '08': 'R', '20': 'F', '96': 'L', '99': 'O', '55': 'R',
    '67': 'E', '27': 'E', '03': 'E', '09': 'E', '05': 'C', '53': 'N',
    '44': 'U', '62': 'B', '68': 'R',
    '23': 'S', '17': 'E', '29': 'E', '66': 'A', '49': 'E',
    '38': 'K', '77': 'Z',
    '22': 'K', '82': 'O', '73': 'N', '50': 'I', '84': 'G',
    '25': 'O', '83': 'V', '81': 'T', '24': 'I',
    '79': 'O', '10': 'R',
}

# German word set for validation
GERMAN_WORDS = set([
    'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO',
    'DU', 'OB', 'AM', 'IM', 'AB', 'AUS', 'BEI', 'VOR', 'FUR',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST',
    'WIR', 'ICH', 'SIE', 'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT',
    'MIT', 'VON', 'HAT', 'AUF', 'BIS', 'ALS', 'NUN', 'HIN', 'TAG',
    'ORT', 'TOD', 'OFT', 'NIE', 'ALT', 'NEU', 'ODE', 'GAR', 'NET',
    'SEI', 'TUN', 'MAL', 'RAT', 'ENDE', 'REDE', 'RUNE',
    'NACH', 'AUCH', 'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN', 'WARD',
    'DASS', 'WENN', 'DANN', 'DENN', 'ABER', 'ODER', 'WEIL', 'WIRD',
    'EINE', 'DIES', 'HIER', 'DORT', 'WELT', 'ZEIT', 'TEIL', 'SEID',
    'WORT', 'NAME', 'GANZ', 'SEHR', 'VIEL', 'FORT', 'HOCH', 'KLAR',
    'ERDE', 'GOTT', 'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN', 'WAHR',
    'HELD', 'RUNE', 'FACH', 'WIND', 'FAND', 'GING', 'NAHM', 'SAGT',
    'KANN', 'SOLL', 'WILL', 'MUSS', 'GIBT', 'RIEF',
    'MACHT', 'KRAFT', 'GEIST', 'NACHT', 'LICHT', 'KRIEG', 'REICH',
    'UNTER', 'DURCH', 'GEGEN', 'IMMER', 'NICHT', 'SCHON',
    'DIESE', 'SEINE', 'EINEN', 'EINER', 'EINEM', 'EINES',
    'URALTE', 'STEINEN', 'STEINE', 'STEIN', 'RUNEN', 'FINDEN',
    'STEHEN', 'GEHEN', 'KOMMEN', 'SAGEN', 'WISSEN',
    'ERSTE', 'ANDEREN', 'KOENIG', 'SCHAUN', 'RUIN',
    'ORTE', 'ORTEN', 'WORTE', 'STEH', 'GEH',
    'ALLE', 'ALLES', 'VIELE', 'WIEDER', 'WISSET',
    # Additional for matching
    'SPRACH', 'GESCHAH', 'BRACH', 'SCHRIEB', 'GEFUNDEN',
    'GESCHRIEBEN', 'GEWESEN', 'GEBOREN', 'GESTORBEN',
    'VERFLUCHT', 'VERFLUCHTEN', 'GEFALLEN', 'VERTRIEBEN',
    'ERHALTEN', 'BEWAHREN', 'ERWACHEN', 'ERWACHT',
    'ZWISCHEN', 'HEILIG', 'HEILIGE', 'HEILIGEN',
    'DUNKEL', 'DUNKLE', 'DUNKLEN', 'EWIG', 'EWIGE', 'EWIGEN',
    'MAUER', 'MAUERN', 'TURM', 'TEMPEL', 'GRUFT', 'GRAB',
    'SCHWERT', 'SCHILD', 'WAFFE', 'WAFFEN',
    'KRIEGER', 'MEISTER', 'HERREN', 'PRIESTER',
    'SEHEN', 'GESEHEN', 'HELFEN', 'TRAGEN',
    'SEELE', 'SEELEN', 'GEHEIMNIS',
    'STIMME', 'ZEICHEN', 'HIMMEL',
    'HWND', 'OEL', 'SCE', 'MIN', 'MINNE',
    'HEARUCHTIG', 'HEARUCHTIGER', 'RUCHTIG',
    'LABGZERAS', 'HEDEMI', 'ADTHARSC', 'TAUTR',
    'TOTNIURG', 'TOTNIURGS', 'EDETOTNIURG', 'EDETOTNIURGS',
    'SCHWITEIONE', 'SCHWITEIO', 'ENGCHD', 'KELSEI',
    'TIUMENGEMI', 'LABRNI', 'UTRUNR', 'GEVMT',
    'AUNRSONGETRASES', 'EILCH', 'EILCHANHEARUCHTIG',
    # Common MHG
    'EDEL', 'ADEL', 'HARSCH',
    'SCHAR', 'SCHAREN', 'HEER',
    'RECHT', 'GERICHT',
])

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

# ============================================================
# FIND GARBLED SEGMENTS AND TRACE RAW CODES
# ============================================================

def decode_with_context(bpairs, m, center_start, center_end, ctx=15):
    """Decode a range of codes with surrounding context."""
    start = max(0, center_start - ctx)
    end = min(len(bpairs), center_end + ctx)
    codes = bpairs[start:end]
    text = ''.join(m.get(c, '?') for c in codes)
    return codes, text, center_start - start

# Find all occurrences of garbled segments
def find_garbled_occurrences(target_text, mapping):
    """Find where a specific decoded text appears across all books."""
    occurrences = []
    for bidx, bpairs in enumerate(book_pairs):
        full_text = ''.join(mapping.get(p, '?') for p in bpairs)
        pos = 0
        while True:
            pos = full_text.find(target_text, pos)
            if pos == -1:
                break
            raw_codes = bpairs[pos:pos + len(target_text)]
            # Get wider context
            ctx_start = max(0, pos - 12)
            ctx_end = min(len(full_text), pos + len(target_text) + 12)
            context = full_text[ctx_start:ctx_end]
            occurrences.append({
                'book': bidx,
                'pos': pos,
                'codes': raw_codes,
                'context': context,
                'ctx_offset': pos - ctx_start,
            })
            pos += 1
    return occurrences

def test_letter_change(garbled_codes, mapping, code_to_change, new_letter):
    """Test what happens if we change one code's letter assignment."""
    test_map = dict(mapping)
    test_map[code_to_change] = new_letter
    return ''.join(test_map.get(c, '?') for c in garbled_codes)

def find_german_substrings(text, min_len=3):
    """Find German words within a text string."""
    found = []
    for start in range(len(text)):
        for end in range(start + min_len, min(start + 20, len(text) + 1)):
            word = text[start:end]
            if word in GERMAN_WORDS:
                found.append((start, word))
    return found

# ============================================================
# MAIN ANALYSIS
# ============================================================

print("=" * 70)
print("CRIB ATTACK ON GARBLED SEGMENTS")
print("=" * 70)

# Target garbled segments
TARGETS = [
    "WRLGTNELNRHELU",   # 14 chars, x6
    "NTENTTUIGAA",      # 11 chars, x4 (from NTENTTUIGAA)
    "DRTHENAEU",        # 9 chars, x3
    "LGTNELGZ",         # 8 chars, x3
    "HECHLLT",          # 7 chars, x5
    "WIISETN",          # 7 chars, x3
    "GEIGET",           # 6 chars, x4
    "NDTEII",           # 6 chars, x5
    "TIURIT",           # 6 chars, x3
    "CHIS",             # 4 chars, x3
    "NSCHA",            # 5 chars, x4
    "LAUNRLRUNR",       # 10 chars, x2
]

# Suspicious I-codes (over-represented)
I_CODES = ['21', '15', '46', '65', '16', '71', '50', '24']

# Letters that need more codes
DEFICIT_LETTERS = ['B', 'F', 'P', 'M']

print("\n  Suspicious I-codes (I is +3.73% over expected):")
for code in I_CODES:
    total = sum(1 for bp in book_pairs for c in bp if c == code)
    print(f"    [{code}] = I, {total} occurrences")

for target in TARGETS:
    print(f"\n{'=' * 70}")
    print(f"TARGET: [{target}] ({len(target)} chars)")
    print(f"{'=' * 70}")

    occurrences = find_garbled_occurrences(target, MAPPING)
    print(f"\n  Found {len(occurrences)} occurrence(s)")

    if not occurrences:
        print("  (skipping)")
        continue

    # Show raw codes for first occurrence
    occ = occurrences[0]
    print(f"\n  Book {occ['book']}, pos {occ['pos']}:")
    print(f"  Codes:   {' '.join(occ['codes'])}")
    print(f"  Letters: {' '.join(MAPPING.get(c,'?') for c in occ['codes'])}")
    print(f"  Context: ...{occ['context']}...")

    # Check if all occurrences have same codes
    code_sets = set()
    for o in occurrences:
        code_sets.add(tuple(o['codes']))
    if len(code_sets) == 1:
        print(f"  All {len(occurrences)} occurrences have identical raw codes [OK]")
    else:
        print(f"  WARNING: {len(code_sets)} different code patterns!")
        for i, cs in enumerate(code_sets):
            decoded = ''.join(MAPPING.get(c, '?') for c in cs)
            print(f"    Pattern {i}: {' '.join(cs)} -> {decoded}")

    # Identify which codes in this segment are I-codes
    i_positions = []
    for pos, code in enumerate(occ['codes']):
        if MAPPING.get(code) == 'I' and code in I_CODES:
            i_positions.append((pos, code))

    if i_positions:
        print(f"\n  I-codes in this segment:")
        for pos, code in i_positions:
            print(f"    Position {pos}: [{code}] = I")

    # Try changing each I-code to deficit letters and see if German words emerge
    print(f"\n  Testing I-code reassignments:")
    best_results = []

    # Get all unique codes in the segment
    unique_codes = set(occ['codes'])

    # For each code in the segment, try all 26 letters
    for code in unique_codes:
        current_letter = MAPPING.get(code, '?')
        if current_letter == '?':
            continue

        for new_letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if new_letter == current_letter:
                continue

            # Get wider context codes (from first occurrence)
            ctx_start = max(0, occ['pos'] - 8)
            ctx_end = min(len(book_pairs[occ['book']]),
                         occ['pos'] + len(target) + 8)
            ctx_codes = book_pairs[occ['book']][ctx_start:ctx_end]

            new_text = test_letter_change(ctx_codes, MAPPING, code, new_letter)
            german_found = find_german_substrings(new_text)

            if german_found:
                # Score by total German word characters found
                total_word_chars = sum(len(w) for _, w in german_found)
                # Compare with baseline
                baseline_text = ''.join(MAPPING.get(c, '?') for c in ctx_codes)
                baseline_found = find_german_substrings(baseline_text)
                baseline_chars = sum(len(w) for _, w in baseline_found)

                improvement = total_word_chars - baseline_chars
                if improvement > 0:
                    best_results.append({
                        'code': code,
                        'current': current_letter,
                        'new': new_letter,
                        'improvement': improvement,
                        'words_found': german_found,
                        'new_text': new_text,
                        'baseline_chars': baseline_chars,
                    })

    # Sort and show best results
    best_results.sort(key=lambda x: -x['improvement'])
    shown = 0
    for r in best_results[:10]:
        words_str = ', '.join(w for _, w in r['words_found'])
        print(f"    [{r['code']}] {r['current']}->{r['new']}: "
              f"+{r['improvement']} chars ({r['baseline_chars']}->{r['baseline_chars']+r['improvement']})")
        print(f"      New text: ...{r['new_text']}...")
        print(f"      Words: {words_str}")
        shown += 1

    if shown == 0:
        print(f"    (no single-code change produces improvement)")

# ============================================================
# DEEP ANALYSIS: MOST PROMISING CODE CHANGES
# ============================================================

print(f"\n{'=' * 70}")
print("DEEP ANALYSIS: GLOBAL IMPACT OF PROMISING CHANGES")
print(f"{'=' * 70}")

# Collect all proposed changes across all segments
all_proposals = Counter()
proposal_details = {}

for target in TARGETS:
    occurrences = find_garbled_occurrences(target, MAPPING)
    if not occurrences:
        continue

    occ = occurrences[0]
    unique_codes = set(occ['codes'])

    for code in unique_codes:
        current = MAPPING.get(code, '?')
        for new_letter in DEFICIT_LETTERS + ['E', 'A', 'N', 'R', 'S', 'T']:
            if new_letter == current:
                continue

            ctx_start = max(0, occ['pos'] - 8)
            ctx_end = min(len(book_pairs[occ['book']]),
                         occ['pos'] + len(target) + 8)
            ctx_codes = book_pairs[occ['book']][ctx_start:ctx_end]

            new_text = test_letter_change(ctx_codes, MAPPING, code, new_letter)
            baseline_text = ''.join(MAPPING.get(c, '?') for c in ctx_codes)

            new_found = find_german_substrings(new_text)
            old_found = find_german_substrings(baseline_text)
            imp = sum(len(w) for _, w in new_found) - sum(len(w) for _, w in old_found)

            if imp > 0:
                key = (code, current, new_letter)
                all_proposals[key] += imp
                if key not in proposal_details:
                    proposal_details[key] = []
                proposal_details[key].append((target, imp,
                    [w for _, w in new_found if w not in [x for _, x in old_found]]))

print(f"\n  Top 20 most impactful code changes (aggregated across all segments):")
print(f"  {'Code':>4s} {'Curr':>5s} {'->':>2s} {'New':>4s} {'Impact':>7s} {'Segments':>8s}")
for (code, curr, new), total_imp in all_proposals.most_common(20):
    n_segments = len(proposal_details[(code, curr, new)])
    # Show what words each produces
    all_new_words = set()
    for _, _, words in proposal_details[(code, curr, new)]:
        for w in words:
            all_new_words.add(w)
    words_preview = ', '.join(list(all_new_words)[:5])
    print(f"  [{code}]  {curr:>4s}  -> {new:>3s}  {total_imp:>7d}  {n_segments:>8d}  {words_preview}")

# ============================================================
# SPECIAL: ANALYZE "WISSET" AND "WISSEN" CONTEXT
# ============================================================

print(f"\n{'=' * 70}")
print("SPECIAL: WISSET/WISSEN PATTERN ANALYSIS")
print(f"{'=' * 70}")

# WIISETN appears 3x - could this be WISSETEN (archaic "knew") or WISSET+N?
target = "WIISETN"
occurrences = find_garbled_occurrences(target, MAPPING)
for occ in occurrences[:2]:
    codes = occ['codes']
    print(f"\n  Book {occ['book']}: codes {' '.join(codes)}")
    print(f"  Current: W I I S E T N")
    print(f"  If [{codes[1]}]=S: WSISETN -> contains WISSEN?")
    print(f"  If [{codes[2]}]=S: WSISSETN?")

    # Test changes
    for pos in range(len(codes)):
        code = codes[pos]
        curr = MAPPING.get(code, '?')
        for new_l in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if new_l == curr:
                continue
            test_text = list(target)
            test_text[pos] = new_l
            test_str = ''.join(test_text)
            # Check if this produces WISSET, WISSEN, or other known words
            for word in ['WISSET', 'WISSEN', 'WISTE', 'WEISEN', 'WEISST']:
                if word in test_str:
                    print(f"    [{code}] pos{pos} {curr}->{new_l}: {test_str} (contains {word})")

# ============================================================
# SPECIAL: HEARUCHTIG - IS IT BERUECHTIGT?
# ============================================================

print(f"\n{'=' * 70}")
print("SPECIAL: EILCH AN HEARUCHTIG - MHG ANALYSIS")
print(f"{'=' * 70}")

# HEARUCHTIG appears 8 times. In MHG, "berüchtigt" = notorious/infamous
# If we read HEARUCHTIG as [H+E+A+RUCHTIG], the H could be wrong
# "BERUCHTIG" = berüchtigt in MHG (without umlaut)
# The full phrase is "EILCH AN HEARUCHTIG ER"

# Find the raw codes
target = "HEARUCHTIG"
occurrences = find_garbled_occurrences(target, MAPPING)
if occurrences:
    occ = occurrences[0]
    codes = occ['codes']
    print(f"\n  Raw codes: {' '.join(codes)}")
    print(f"  Letters:   {' '.join(MAPPING.get(c,'?') for c in codes)}")
    print(f"  Current:   H E A R U C H T I G")
    print(f"\n  HEARUCHTIG analysis:")
    print(f"    If it's BERUCHTIG (MHG 'notorious'):")
    print(f"      Need: B E _ R U C H T I G")
    print(f"      Code [{codes[0]}] = H -> would need to be B")
    print(f"      Code [{codes[2]}] = A -> would need to drop or be part of vowel")
    print(f"\n    If it's HE + ARUCHTIG:")
    print(f"      ARUCHTIG could be 'a-ruchtig' (a + odorous/reputable)")
    print(f"\n    If it's HEAR + UCHTIG:")
    print(f"      HEAR is MHG for 'army/host' (Heer)")
    print(f"      UCHTIG is a suffix meaning '-ous/-ful'")
    print(f"      HEARUCHTIG = 'army-worthy' or 'host-mighty'")
    print(f"\n    Full phrase: EILCH AN HEARUCHTIG ER")
    print(f"      If EILCH = EILIG (hasty/urgent, MHG variant):")
    print(f"        'hastily/urgently HEARUCHTIG he'")

# ============================================================
# KEY NARRATIVE PHRASES - ATTEMPT READING
# ============================================================

print(f"\n{'=' * 70}")
print("NARRATIVE RECONSTRUCTION ATTEMPT")
print(f"{'=' * 70}")

# The most coherent repeated phrases, with analysis
phrases = [
    ("HIER TAUTR IST EILCH AN HEARUCHTIGER SO DASS TUN DIESER EIN ER SEIN EDETOTNIURGS",
     "Here TAUTR is urgently/hastily notorious(MHG), so that do this-one, one of his EDETOTNIURGS"),
    ("DIE URALTE STEINEN TER ADTHARSC IST SCHAUN RUIN",
     "The ancient stones TER ADTHARSC is view/show ruin"),
    ("ENDE UTRUNR DEN ENDE REDE DER KOENIG LABGZERAS",
     "End UTRUNR the end speech the King LABGZERAS(=SALZBERG)"),
    ("ICH OEL SO DEN",
     "I OEL(oil/anoint) so the"),
    ("ER SCE AUS ENDE",
     "He SCE(OHG:see/behold) out/from end"),
    ("RUNE ORT ND TER AM NEU DES",
     "Rune place ... at new of-the"),
    ("DIE MIN HED DEM I DIE URALTE STEINE",
     "The MIN(love/MHG) ... the-one the ancient stones"),
    ("FINDEN TEIGN DAS ES ERSTE",
     "'find [TEIGN=ZEIGEN?show?] that it first"),
    ("DU NTER L AUS IN HIE",
     "Du unter(under) ... aus in hier? -> DUNTER + L + AUS + IN + HIE?"),
]

for phrase, interpretation in phrases:
    print(f"\n  PHRASE: {phrase}")
    print(f"  READ:   {interpretation}")

# ============================================================
# HYPOTHESIS: TER = D(ER) with code for D wrong
# ============================================================

print(f"\n{'=' * 70}")
print("HYPOTHESIS: 'TER' pattern analysis")
print(f"{'=' * 70}")

# "TER" appears 28 times (from word count). In German, DER is much more common.
# Could the T-code before ER actually be D?
# This would mean there's a T-code that should be D.

# Find which codes produce the T in TER
target = "TER"
occurrences = find_garbled_occurrences(target, MAPPING)
t_codes_before_er = Counter()
for occ in occurrences:
    if len(occ['codes']) >= 1:
        t_code = occ['codes'][0]
        t_codes_before_er[t_code] += 1

print(f"\n  'TER' appears {len(occurrences)} times")
print(f"  T-code distribution before ER:")
for code, count in t_codes_before_er.most_common():
    all_uses = sum(1 for bp in book_pairs for c in bp if c == code)
    print(f"    [{code}] = {MAPPING[code]}: {count}x in TER (out of {all_uses} total)")
    # If this code were D instead of T, TER becomes DER
    if MAPPING[code] == 'T':
        print(f"      If [{code}]=D: TER -> DER (article!)")

# Check: how many T codes are there?
t_codes = [c for c, l in MAPPING.items() if l == 'T']
d_codes = [c for c, l in MAPPING.items() if l == 'D']
print(f"\n  T codes ({len(t_codes)}): {t_codes}")
print(f"  D codes ({len(d_codes)}): {d_codes}")
print(f"  T actual: {sum(1 for bp in book_pairs for c in bp if MAPPING.get(c)=='T')} occ")
print(f"  D actual: {sum(1 for bp in book_pairs for c in bp if MAPPING.get(c)=='D')} occ")
print(f"  T expected: {5533 * 6.15 / 100:.0f}")
print(f"  D expected: {5533 * 5.08 / 100:.0f}")
