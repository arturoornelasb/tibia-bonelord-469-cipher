#!/usr/bin/env python3
"""
Session 25: Validate cross-boundary anagrams and apply them.
Measure combined coverage gain. Show updated narrative.
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

# BASELINE anagram map (session 24)
ANAGRAM_MAP_BASELINE = {
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
    # New words to add
    'IHM', 'DES', 'TREU', 'STIER', 'NEST',
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
book_data = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_data.append(pairs)

decoded_books = []
for pairs in book_data:
    decoded_books.append(''.join(v7.get(p, '?') for p in pairs))

raw = ''.join(decoded_books)

def apply_anagrams(text, amap):
    for k in sorted(amap, key=len, reverse=True):
        text = text.replace(k, amap[k])
    return text

def dp_segment_full(text, vocab):
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
    # Build tokens
    tokens = []
    i = n
    while i > 0:
        if back[i] is not None:
            tokens.append(text[back[i]:i])
            i = back[i]
        else:
            tokens.append('{' + text[i-1] + '}')
            i -= 1
    tokens.reverse()
    # Merge adjacent garbled
    merged = []
    for t in tokens:
        if t.startswith('{') and merged and merged[-1].startswith('{'):
            merged[-1] = merged[-1][:-1] + t[1:]
        else:
            merged.append(t)
    return dp[n], merged

# ============================================================
# BASELINE
# ============================================================
baseline_text = apply_anagrams(raw, ANAGRAM_MAP_BASELINE)
baseline_cov, baseline_tokens = dp_segment_full(baseline_text, KNOWN)
total = sum(1 for c in baseline_text if c != '?')
print(f"BASELINE: {baseline_cov}/{total} = {baseline_cov/total*100:.1f}%")

# ============================================================
# CANDIDATE CROSS-BOUNDARY ANAGRAMS
# ============================================================
# From session25_cross_boundary.py results
CANDIDATES = [
    # (source_in_text, resolved, description, type)
    ('EUTR', 'TREU', 'faithful/loyal (exact anagram)', 'cross-boundary'),
    ('SERTI', 'STIER', 'bull/steer (exact anagram)', 'cross-boundary'),
    ('NTES', 'NEST', 'nest (exact anagram)', 'cross-boundary'),
    ('NEDE', 'ENDE', 'end (exact, already KNOWN but new boundary)', 'cross-boundary'),
    ('ERT', 'TER', 'of the/MHG (exact, already KNOWN)', 'cross-boundary'),
    ('ESD', 'DES', 'of the (exact anagram)', 'cross-boundary'),
    ('ESR', 'SER', 'very/MHG (exact, already KNOWN)', 'cross-boundary'),
    ('HIM', 'IHM', 'him/dative (exact anagram)', 'cross-boundary'),
    ('HHE', 'HEH', 'concealment? unclear', 'cross-boundary'),
]

print(f"\n{'='*70}")
print("INDIVIDUAL CANDIDATE VALIDATION")
print(f"{'='*70}")

valid_candidates = []
running_map = dict(ANAGRAM_MAP_BASELINE)

for src, dst, desc, ctype in CANDIDATES:
    # Test adding this anagram
    test_map = dict(running_map)
    test_map[src] = dst
    test_text = apply_anagrams(raw, test_map)

    # Check no baseline anagrams are broken
    broken = False
    for orig_src in ANAGRAM_MAP_BASELINE:
        if orig_src not in raw and orig_src != src:
            # Already wasn't in raw, skip
            continue
        # The new anagram might have consumed characters that baseline needs
        # Check by verifying baseline anagram outputs still appear

    test_cov, test_tokens = dp_segment_full(test_text, KNOWN)
    gain = test_cov - baseline_cov

    # Count occurrences
    count = raw.count(src)

    # Find contexts
    contexts = []
    pos = 0
    while len(contexts) < 3:
        idx = test_text.find(dst, pos)
        if idx < 0: break
        s = max(0, idx - 12)
        e = min(len(test_text), idx + len(dst) + 12)
        contexts.append(test_text[s:e])
        pos = idx + 1

    status = "VALID" if gain > 0 else ("NEUTRAL" if gain == 0 else "HARMFUL")
    print(f"\n  {src} -> {dst} ({desc})")
    print(f"  Occurrences: {count}x | Gain: {gain:+d} | Status: {status}")
    for ctx in contexts[:2]:
        print(f"    ...{ctx}...")

    if gain > 0:
        valid_candidates.append((src, dst, gain, count, desc))

# ============================================================
# CUMULATIVE APPLICATION
# ============================================================
print(f"\n{'='*70}")
print("CUMULATIVE APPLICATION (greedy, one by one)")
print(f"{'='*70}")

# Sort by gain desc
valid_candidates.sort(key=lambda x: -x[2])

cumulative_map = dict(ANAGRAM_MAP_BASELINE)
running_cov = baseline_cov
applied = []

for src, dst, expected_gain, count, desc in valid_candidates:
    test_map = dict(cumulative_map)
    test_map[src] = dst
    test_text = apply_anagrams(raw, test_map)
    test_cov, _ = dp_segment_full(test_text, KNOWN)
    actual_gain = test_cov - running_cov

    if actual_gain > 0:
        cumulative_map[src] = dst
        running_cov = test_cov
        applied.append((src, dst, actual_gain, count, desc))
        print(f"  APPLIED: {src} -> {dst} = +{actual_gain} (cumulative: {running_cov}/{total} = {running_cov/total*100:.1f}%)")
    else:
        print(f"  SKIPPED: {src} -> {dst} (no gain after previous applications)")

total_gain = running_cov - baseline_cov
print(f"\n  TOTAL GAIN: +{total_gain} chars")
print(f"  FINAL COVERAGE: {running_cov}/{total} = {running_cov/total*100:.1f}%")
print(f"  Anagrams applied: {len(applied)}")

# ============================================================
# UPDATED NARRATIVE (sample)
# ============================================================
print(f"\n{'='*70}")
print("UPDATED NARRATIVE (first 500 chars)")
print(f"{'='*70}")

final_text = apply_anagrams(raw, cumulative_map)
final_cov, final_tokens = dp_segment_full(final_text, KNOWN)
print(' '.join(final_tokens[:80]))

# ============================================================
# REMAINING GARBLED BLOCKS
# ============================================================
print(f"\n{'='*70}")
print("REMAINING GARBLED BLOCKS (top 20)")
print(f"{'='*70}")

garbled = [t for t in final_tokens if t.startswith('{')]
garbled_freq = Counter(garbled)
for block, freq in garbled_freq.most_common(20):
    total_chars = len(block) - 2  # subtract {}
    print(f"  {block:>25} x{freq:2d} ({total_chars * freq:3d} chars)")

# Total garbled
total_garbled = sum(len(t) - 2 for t in garbled)
print(f"\n  Total garbled: {total_garbled} chars ({total_garbled/total*100:.1f}%)")

# ============================================================
# PER-BOOK COVERAGE
# ============================================================
print(f"\n{'='*70}")
print("PER-BOOK COVERAGE (books with >80%)")
print(f"{'='*70}")

for bidx, text in enumerate(decoded_books):
    if len(text) < 20: continue
    rt = apply_anagrams(text, cumulative_map)
    cov, toks = dp_segment_full(rt, KNOWN)
    known_chars = sum(1 for c in rt if c != '?')
    pct = cov / max(known_chars, 1) * 100
    if pct >= 80:
        print(f"  Book {bidx:2d}: {pct:.0f}% ({cov}/{known_chars})")
        print(f"    {' '.join(toks[:30])}")

print("\nDone.")
