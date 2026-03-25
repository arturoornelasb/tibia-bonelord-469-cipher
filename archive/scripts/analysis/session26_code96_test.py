#!/usr/bin/env python3
"""
Session 26: Code 96 = I hypothesis test
=========================================
Code 96 is currently mapped to L (45 uses). Hypothesis: it should be I.

Evidence:
  - NLNDEF (7 occ) would become NINDEF -> anagram of FINDEN (to find)
  - Code 34 also maps to L, so L is not completely lost
  - German expects L at ~3.44%; losing one L code still leaves code 34
  - If code 96=I, we'd have 7 I codes (15,16,21,46,50,65,96) instead of 6

This script:
  1. Loads the full pipeline from narrative_v3_clean.py
  2. Tests code 96 = I vs L
  3. Compares coverage (original vs modified)
  4. Shows ALL 45 positions where code 96 appears
  5. Identifies broken/new anagrams
  6. Checks overall German text quality
"""

import json, os, sys, copy, re
from collections import Counter, defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')
core_dir = os.path.join(script_dir, '..', 'core')

# ============================================================
# 1. LOAD DATA (same as narrative_v3_clean.py)
# ============================================================
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7_original = json.load(f)

# Import the pipeline components from narrative_v3_clean
sys.path.insert(0, core_dir)

# We need DIGIT_SPLITS, KNOWN, ANAGRAM_MAP, dp_segment from narrative_v3_clean
# but running it prints a ton of output. Let's import the data directly.

# ---------- DIGIT_SPLITS ----------
DIGIT_SPLITS = {
    2: (45, '1'),    5: (265, '1'),   6: (12, '0'),    8: (137, '7'),
    10: (169, '0'),  11: (137, '0'),  12: (56, '1'),   13: (45, '0'),
    14: (98, '1'),   15: (98, '0'),   18: (4, '0'),    19: (52, '0'),
    20: (5, '1'),    22: (7, '1'),    23: (22, '4'),   24: (87, '8'),
    25: (0, '0'),    29: (53, '0'),   32: (137, '1'),  34: (101, '0'),
    36: (78, '0'),   39: (44, '0'),   42: (91, '2'),   43: (122, '0'),
    45: (15, '0'),   46: (0, '2'),    48: (126, '0'),  49: (97, '1'),
    50: (16, '6'),   52: (1, '0'),    53: (257, '1'),  54: (49, '1'),
    60: (73, '9'),   61: (93, '7'),   64: (60, '0'),   65: (114, '2'),
    68: (54, '0'),
}

# ---------- KNOWN words ----------
KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN', 'TUT',
    'SAG', 'WAR',
    'NU', 'SIN', 'STANDE', 'NACHTS', 'NIT', 'TOT', 'TER',
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
    'FINDEN', 'GEBEN', 'GEHEN', 'HABEN', 'KOMMEN', 'LEBEN', 'LESEN',
    'NEHMEN', 'SAGEN', 'SEHEN', 'STEHEN', 'SUCHEN', 'WISSEN',
    'WISSET', 'RUFEN', 'WIEDER',
    'OEL', 'SCE', 'MINNE', 'MIN', 'HEL',
    'ODE', 'SER', 'GEN', 'INS',
    'GEIGET', 'BERUCHTIG', 'BERUCHTIGER',
    'MEERE', 'NEIGT', 'WISTEN', 'MANIER',
    'HUND', 'GODE', 'GODES',
    'EIGENTUM', 'REDER', 'THENAEUT',
    'LABT', 'MORT', 'DIGE', 'WEGE',
    'KOENIGS', 'NAHE', 'NOT', 'NOTH', 'ZUR',
    'OWI', 'ENGE', 'SEIDEN', 'ALTES', 'DENN', 'BIS', 'NIE',
    'NUT', 'NUTZ', 'HEIL', 'NEID', 'TREU', 'TREUE',
    'SUN', 'DIENST', 'SANG', 'DINC', 'HULDE', 'NACH', 'STEINE',
    'LANT', 'HERRE', 'DIENEST', 'GEBOT', 'SCHWUR', 'ORDEN',
    'RICHTER', 'DUNKEL', 'EHRE', 'EDELE', 'SCHULD', 'SEGEN', 'FLUCH', 'RACHE',
    'KOENIG', 'DASS', 'EDEL', 'ADEL', 'SCHRAT',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME', 'SCHARDT',
    'IHM', 'STIER', 'NEST', 'DES',
    'DEGEN', 'REISTEN', 'REIST', 'WINDUNRUH', 'WINDUNRUHS', 'UNRUH',
    'HEHL', 'HECHELT', 'IRREN',
])

# ---------- ANAGRAM_MAP ----------
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
    'HEDDEMI': 'HEIME',
    'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG',
    'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE',
    'TEIGN': 'NEIGT',
    'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER',
    'SODGE': 'GODES',
    'SNDTEII': 'DIENST',
    'IEB': 'BEI',
    'TNEDAS': 'STANDE',
    'NSCHAT': 'NACHTS',
    'SANGE': 'SAGEN',
    'GHNEE': 'GEHEN',
    'THARSCR': 'SCHRAT',
    'ANSD': 'SAND',
    'TTU': 'TUT',
    'TERLAU': 'URALTE',
    'EUN': 'NEU',
    'NIUR': 'RUIN',
    'RUIIN': 'RUIN',
    'CHIS': 'SICH',
    'SERTI': 'STIER',
    'ESR': 'SER',
    'NEDE': 'ENDE',
    'NTES': 'NEST',
    'HIM': 'IHM',
    'EUTR': 'TREU',
    'DIESERTEIN': 'DIEREISTEN',
    'DERSTEI': 'DEREIST',
    'DENGE': 'DEGEN',
    'ESC': 'SCE',
    'DSIE': 'DIES',
    'UIRUNNHWND': 'WINDUNRUH',
    'SIUIRUNNHWND': 'WINDUNRUHS',
    'HIHL': 'HEHL',
    'HECHLLT': 'HECHELT',
    'NLNDEF': 'FINDEN',
    'RRNI': 'IRREN',
}


# ============================================================
# HELPER FUNCTIONS
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

def decode_books(mapping):
    """Decode all books using a given mapping, return decoded texts and pair lists."""
    all_book_pairs = []
    decoded = []
    for bidx, book in enumerate(books):
        if bidx in DIGIT_SPLITS:
            split_pos, digit = DIGIT_SPLITS[bidx]
            book = book[:split_pos] + digit + book[split_pos:]
        off = get_offset(book)
        pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
        all_book_pairs.append(pairs)
        text = ''.join(mapping.get(p, '?') for p in pairs)
        decoded.append(text)
    return decoded, all_book_pairs

def apply_anagrams(text, anagram_map):
    """Apply anagram resolutions to text."""
    for anagram in sorted(anagram_map.keys(), key=len, reverse=True):
        text = text.replace(anagram, anagram_map[anagram])
    return text

def dp_segment(text):
    """DP word segmentation."""
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

def full_pipeline(mapping, anagram_map):
    """Run the complete decode -> anagram -> segment pipeline."""
    decoded, book_pairs = decode_books(mapping)
    all_text = ''.join(decoded)
    resolved = apply_anagrams(all_text, anagram_map)
    tokens, covered = dp_segment(resolved)
    total_known = sum(1 for c in resolved if c != '?')
    pct = covered / max(total_known, 1) * 100
    return {
        'decoded': decoded,
        'book_pairs': book_pairs,
        'all_text': all_text,
        'resolved': resolved,
        'tokens': tokens,
        'covered': covered,
        'total_known': total_known,
        'pct': pct,
    }

def get_freq_score(text):
    """Compute letter frequency deviation score."""
    GERMAN_FREQ = {
        'E': 17.40, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
        'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
        'L': 3.44, 'C': 3.06, 'G': 3.01, 'M': 2.53, 'O': 2.51,
        'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
        'P': 0.79,
    }
    letter_counts = Counter(c for c in text if c.isalpha())
    total = sum(letter_counts.values())
    if total == 0:
        return 999, {}, {}
    score = 0
    details = {}
    for letter, expected in GERMAN_FREQ.items():
        actual = letter_counts.get(letter, 0) / total * 100
        diff = actual - expected
        score += abs(diff)
        details[letter] = (actual, expected, diff)
    return score, details, letter_counts


# ============================================================
# 2. BUILD MODIFIED MAPPING: code 96 = I instead of L
# ============================================================
v7_modified = copy.deepcopy(v7_original)
v7_modified['96'] = 'I'

print("=" * 70)
print("SESSION 26: CODE 96 HYPOTHESIS TEST")
print("  Original: code 96 = L")
print("  Modified: code 96 = I")
print("=" * 70)

# ============================================================
# 3. RUN BOTH PIPELINES
# ============================================================
print("\n--- Running original pipeline (96=L) ---")
orig = full_pipeline(v7_original, ANAGRAM_MAP)
print(f"  Coverage: {orig['covered']}/{orig['total_known']} = {orig['pct']:.1f}%")

print("\n--- Running modified pipeline (96=I) ---")
mod = full_pipeline(v7_modified, ANAGRAM_MAP)
print(f"  Coverage: {mod['covered']}/{mod['total_known']} = {mod['pct']:.1f}%")

delta = mod['covered'] - orig['covered']
print(f"\n  Coverage delta: {delta:+d} chars ({mod['pct']:.1f}% vs {orig['pct']:.1f}%)")

# ============================================================
# 4. FIND ALL 45 POSITIONS WHERE CODE 96 APPEARS
# ============================================================
print(f"\n{'=' * 70}")
print("ALL POSITIONS WHERE CODE 96 APPEARS")
print(f"{'=' * 70}")

code96_positions = []  # (book_idx, pair_idx, pair_code)
for bidx, bpairs in enumerate(orig['book_pairs']):
    for pidx, pair in enumerate(bpairs):
        if pair == '96':
            code96_positions.append((bidx, pidx, pair))

print(f"\nTotal code 96 occurrences: {len(code96_positions)}")

# For each occurrence, show surrounding context in both mappings
print(f"\n{'Bk':>3} {'Pos':>4} | {'Original context (96=L)':^40} | {'Modified context (96=I)':^40}")
print("-" * 95)

for bidx, pidx, pair in code96_positions:
    bpairs_orig = orig['book_pairs'][bidx]
    # Get context: 5 pairs before and after
    start = max(0, pidx - 5)
    end = min(len(bpairs_orig), pidx + 6)

    context_orig = ''
    context_mod = ''
    for i in range(start, end):
        p = bpairs_orig[i]
        ch_orig = v7_original.get(p, '?')
        ch_mod = v7_modified.get(p, '?')
        if i == pidx:
            context_orig += f'[{ch_orig}]'
            context_mod += f'[{ch_mod}]'
        else:
            context_orig += ch_orig
            context_mod += ch_mod

    print(f" {bidx:2d}  {pidx:3d}  | {context_orig:^40} | {context_mod:^40}")

# ============================================================
# 5. IMPACT ON ANAGRAM RESOLUTIONS
# ============================================================
print(f"\n{'=' * 70}")
print("IMPACT ON ANAGRAM RESOLUTIONS")
print(f"{'=' * 70}")

# Check which anagram source patterns contain L (from code 96)
# When code 96 changes L->I, the raw decoded text changes
# So anagram patterns that relied on L from code 96 will now have I instead

# First, find which anagram patterns appear in original text and modified text
print("\n--- Anagrams affected by L->I change ---")
orig_all = orig['all_text']
mod_all = mod['all_text']

for anagram, resolution in sorted(ANAGRAM_MAP.items()):
    orig_count = orig_all.count(anagram)
    mod_count = mod_all.count(anagram)
    if orig_count != mod_count:
        print(f"  {anagram} -> {resolution}")
        print(f"    Original (96=L): {orig_count} occurrences")
        print(f"    Modified (96=I): {mod_count} occurrences")
        # If it disappeared, check what the modified text has instead
        if mod_count < orig_count:
            # Find where it was in original and what replaced it
            pos = 0
            for i in range(orig_count):
                idx = orig_all.find(anagram, pos)
                if idx >= 0:
                    mod_chunk = mod_all[idx:idx+len(anagram)]
                    print(f"    At pos {idx}: orig={anagram} -> mod={mod_chunk}")
                    pos = idx + 1
        elif mod_count > orig_count:
            # New occurrences appeared
            pos = 0
            for i in range(mod_count):
                idx = mod_all.find(anagram, pos)
                if idx >= 0:
                    orig_chunk = orig_all[idx:idx+len(anagram)]
                    if orig_chunk != anagram:
                        print(f"    NEW at pos {idx}: was={orig_chunk} -> now={anagram}")
                    pos = idx + 1

# ============================================================
# 5b. NEW PATTERNS: What L->I creates in raw text
# ============================================================
print(f"\n--- New patterns created by L->I change ---")
# Find all positions where text changed
diffs = []
for i in range(min(len(orig_all), len(mod_all))):
    if orig_all[i] != mod_all[i]:
        diffs.append(i)

print(f"  Total character changes: {len(diffs)}")
print(f"  All changes are L -> I (as expected)")

# Look at 10-char windows around each change to spot new words
print(f"\n--- Context windows around each L->I change ---")
for di, pos in enumerate(diffs):
    start = max(0, pos - 8)
    end = min(len(mod_all), pos + 9)
    orig_window = orig_all[start:end]
    mod_window = mod_all[start:end]
    # Mark the changed position
    rel_pos = pos - start
    orig_marked = orig_window[:rel_pos] + '[' + orig_window[rel_pos] + ']' + orig_window[rel_pos+1:]
    mod_marked = mod_window[:rel_pos] + '[' + mod_window[rel_pos] + ']' + mod_window[rel_pos+1:]
    print(f"  {di+1:2d}. pos {pos:4d}: {orig_marked:22s} -> {mod_marked:22s}")

# ============================================================
# 5c. NLNDEF specifically - the key evidence
# ============================================================
print(f"\n{'=' * 70}")
print("NLNDEF -> NINDEF ANALYSIS (key evidence)")
print(f"{'=' * 70}")

nlndef_orig = orig_all.count('NLNDEF')
nindef_mod = mod_all.count('NINDEF')
print(f"  NLNDEF in original text: {nlndef_orig}")
print(f"  NINDEF in modified text: {nindef_mod}")
print(f"  NINDEF is anagram of FINDEN: {'YES' if sorted('NINDEF') == sorted('FINDEN') else 'NO'}")
print(f"  NLNDEF is anagram of FINDEN: {'YES' if sorted('NLNDEF') == sorted('FINDEN') else 'NO'}")

# Check FINDEN occurrences from other codes
finden_orig = orig_all.count('FINDEN')
finden_mod = mod_all.count('FINDEN')
print(f"\n  Direct FINDEN in original raw text: {finden_orig}")
print(f"  Direct FINDEN in modified raw text: {finden_mod}")

# ============================================================
# 6. PER-BOOK COVERAGE COMPARISON
# ============================================================
print(f"\n{'=' * 70}")
print("PER-BOOK COVERAGE COMPARISON")
print(f"{'=' * 70}")

print(f"\n{'Book':>5} {'Orig%':>7} {'Mod%':>7} {'Delta':>7} {'Change':>8}")
print("-" * 40)

book_changes = []
for bidx in range(len(books)):
    orig_text = orig['decoded'][bidx]
    mod_text = mod['decoded'][bidx]

    if len(orig_text) < 10:
        continue

    orig_rt = apply_anagrams(orig_text, ANAGRAM_MAP)
    mod_rt = apply_anagrams(mod_text, ANAGRAM_MAP)

    _, orig_cov = dp_segment(orig_rt)
    _, mod_cov = dp_segment(mod_rt)

    orig_known = sum(1 for c in orig_rt if c != '?')
    mod_known = sum(1 for c in mod_rt if c != '?')

    orig_pct = orig_cov / max(orig_known, 1) * 100
    mod_pct = mod_cov / max(mod_known, 1) * 100
    delta_cov = mod_cov - orig_cov

    if delta_cov != 0:
        book_changes.append((bidx, orig_pct, mod_pct, delta_cov))
        marker = "BETTER" if delta_cov > 0 else "WORSE"
        print(f" {bidx:3d}   {orig_pct:5.1f}%  {mod_pct:5.1f}%  {delta_cov:+5d}    {marker}")

print(f"\n  Books improved: {sum(1 for _, _, _, d in book_changes if d > 0)}")
print(f"  Books worsened: {sum(1 for _, _, _, d in book_changes if d < 0)}")
print(f"  Books unchanged: {len(books) - len(book_changes)}")
print(f"  Net char change: {sum(d for _, _, _, d in book_changes):+d}")

# ============================================================
# 6b. SHOW SEGMENTATION FOR CHANGED BOOKS
# ============================================================
print(f"\n{'=' * 70}")
print("SEGMENTATION DETAILS FOR CHANGED BOOKS")
print(f"{'=' * 70}")

for bidx, orig_pct, mod_pct, delta_cov in book_changes:
    orig_text = orig['decoded'][bidx]
    mod_text = mod['decoded'][bidx]

    orig_rt = apply_anagrams(orig_text, ANAGRAM_MAP)
    mod_rt = apply_anagrams(mod_text, ANAGRAM_MAP)

    orig_tokens, _ = dp_segment(orig_rt)
    mod_tokens, _ = dp_segment(mod_rt)

    print(f"\n  Book {bidx} ({delta_cov:+d} chars):")
    print(f"    ORIG: {' '.join(orig_tokens)}")
    print(f"    MOD:  {' '.join(mod_tokens)}")

# ============================================================
# 7. FREQUENCY ANALYSIS COMPARISON
# ============================================================
print(f"\n{'=' * 70}")
print("LETTER FREQUENCY COMPARISON")
print(f"{'=' * 70}")

orig_fscore, orig_details, orig_counts = get_freq_score(orig['resolved'])
mod_fscore, mod_details, mod_counts = get_freq_score(mod['resolved'])

GERMAN_FREQ = {
    'E': 17.40, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
    'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
    'L': 3.44, 'C': 3.06, 'G': 3.01, 'M': 2.53, 'O': 2.51,
    'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
    'P': 0.79,
}

print(f"\n  {'Letter':>6} {'German%':>8} | {'Orig%':>7} {'OrigDiff':>9} | {'Mod%':>7} {'ModDiff':>9} | {'Better?':>8}")
print(f"  {'-'*72}")

for letter in sorted(GERMAN_FREQ.keys(), key=lambda x: -GERMAN_FREQ[x]):
    o_actual, o_expected, o_diff = orig_details[letter]
    m_actual, m_expected, m_diff = mod_details[letter]
    better = "YES" if abs(m_diff) < abs(o_diff) else ("same" if abs(m_diff) == abs(o_diff) else "no")
    # Only show letters that change
    if letter in ('L', 'I') or abs(m_diff - o_diff) > 0.01:
        marker = " <<<"
    else:
        marker = ""
    print(f"  {letter:>6} {o_expected:>7.2f}% | {o_actual:>6.2f}% {o_diff:>+8.2f} | {m_actual:>6.2f}% {m_diff:>+8.2f} | {better:>8}{marker}")

print(f"\n  Original freq score: {orig_fscore:.2f}")
print(f"  Modified freq score: {mod_fscore:.2f}")
print(f"  Score delta: {mod_fscore - orig_fscore:+.2f} ({'BETTER' if mod_fscore < orig_fscore else 'WORSE'})")

# Show L and I specifically
orig_total = sum(orig_counts.values())
mod_total = sum(mod_counts.values())
print(f"\n  L counts: orig={orig_counts.get('L',0)} ({orig_counts.get('L',0)/orig_total*100:.2f}%) -> mod={mod_counts.get('L',0)} ({mod_counts.get('L',0)/mod_total*100:.2f}%)")
print(f"  I counts: orig={orig_counts.get('I',0)} ({orig_counts.get('I',0)/orig_total*100:.2f}%) -> mod={mod_counts.get('I',0)} ({mod_counts.get('I',0)/mod_total*100:.2f}%)")
print(f"  German expected: L={GERMAN_FREQ['L']:.2f}%, I={GERMAN_FREQ['I']:.2f}%")

# ============================================================
# 8. WORDS THAT BREAK vs FORM
# ============================================================
print(f"\n{'=' * 70}")
print("WORD IMPACT ANALYSIS")
print(f"{'=' * 70}")

# Find words in original resolved text that contain L (from code 96 positions)
# and check what happens when those L become I
orig_resolved = orig['resolved']
mod_resolved = mod['resolved']

orig_tokens_flat = orig['tokens']
mod_tokens_flat = mod['tokens']

# Count known words in each
orig_word_counts = Counter(t for t in orig_tokens_flat if not t.startswith('{'))
mod_word_counts = Counter(t for t in mod_tokens_flat if not t.startswith('{'))

# Find differences
all_words = set(orig_word_counts.keys()) | set(mod_word_counts.keys())
print("\n  Words that changed frequency:")
print(f"  {'Word':<20} {'Orig':>5} {'Mod':>5} {'Delta':>6}")
print(f"  {'-'*40}")
for word in sorted(all_words):
    oc = orig_word_counts.get(word, 0)
    mc = mod_word_counts.get(word, 0)
    if oc != mc:
        print(f"  {word:<20} {oc:>5} {mc:>5} {mc-oc:>+5}")

# ============================================================
# 9. GARBLED BLOCKS COMPARISON
# ============================================================
print(f"\n{'=' * 70}")
print("GARBLED BLOCKS COMPARISON (top changes)")
print(f"{'=' * 70}")

orig_garbled = [t for t in orig_tokens_flat if t.startswith('{')]
mod_garbled = [t for t in mod_tokens_flat if t.startswith('{')]

orig_garbled_counts = Counter(orig_garbled)
mod_garbled_counts = Counter(mod_garbled)

# Find garbled blocks that changed
all_garbled = set(orig_garbled_counts.keys()) | set(mod_garbled_counts.keys())
garbled_changes = []
for g in all_garbled:
    oc = orig_garbled_counts.get(g, 0)
    mc = mod_garbled_counts.get(g, 0)
    if oc != mc:
        garbled_changes.append((g, oc, mc))

garbled_changes.sort(key=lambda x: abs(x[2]-x[1]), reverse=True)
print(f"\n  Total garbled blocks: orig={len(orig_garbled)}, mod={len(mod_garbled)} (delta={len(mod_garbled)-len(orig_garbled):+d})")
print(f"\n  {'Garbled Block':<30} {'Orig':>5} {'Mod':>5} {'Delta':>6}")
print(f"  {'-'*50}")
for g, oc, mc in garbled_changes[:30]:
    print(f"  {g:<30} {oc:>5} {mc:>5} {mc-oc:>+5}")

# ============================================================
# 10. FINAL VERDICT
# ============================================================
print(f"\n{'=' * 70}")
print("FINAL VERDICT")
print(f"{'=' * 70}")

print(f"""
  Code 96 test: L -> I

  Coverage:
    Original (96=L): {orig['covered']}/{orig['total_known']} = {orig['pct']:.1f}%
    Modified (96=I): {mod['covered']}/{mod['total_known']} = {mod['pct']:.1f}%
    Delta: {mod['covered'] - orig['covered']:+d} chars ({mod['pct'] - orig['pct']:+.1f}%)

  Frequency analysis:
    Original freq score: {orig_fscore:.2f}
    Modified freq score: {mod_fscore:.2f}
    Delta: {mod_fscore - orig_fscore:+.2f} ({'BETTER' if mod_fscore < orig_fscore else 'WORSE'})

  L count: {orig_counts.get('L',0)} -> {mod_counts.get('L',0)} (lost {orig_counts.get('L',0) - mod_counts.get('L',0)})
  I count: {orig_counts.get('I',0)} -> {mod_counts.get('I',0)} (gained {mod_counts.get('I',0) - orig_counts.get('I',0)})

  Books improved: {sum(1 for _, _, _, d in book_changes if d > 0)}
  Books worsened: {sum(1 for _, _, _, d in book_changes if d < 0)}

  NLNDEF -> NINDEF = FINDEN: {'confirmed' if sorted('NINDEF') == sorted('FINDEN') else 'failed'}

  RECOMMENDATION: {'ACCEPT code 96=I' if mod['pct'] > orig['pct'] and mod_fscore <= orig_fscore + 1 else 'REJECT - investigate further' if mod['pct'] <= orig['pct'] else 'MIXED RESULTS - needs judgment'}
""")
