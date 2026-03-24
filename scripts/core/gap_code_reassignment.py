#!/usr/bin/env python3
"""
Systematic Gap-Only Code Reassignment Attack
=============================================
Identifies codes that NEVER appear in recognized German words, then tests
all possible letter reassignments using bigram context scoring.

Strategy:
1. Use dp_parse mapping (best known, 67.2% coverage)
2. Find which codes produce only gap characters (never in a word)
3. For each gap-only code, analyze what bigrams it forms with neighbors
4. Score all 26 possible letter assignments by German bigram fitness
5. Apply best reassignments and measure improvement

Key insight from anagram analysis:
- LABGZERAS = SALZBERG + extra A -> one A code might be wrong
- N is over-represented in gaps (+4.9%) -> some N codes might be wrong
- B/F/P severely under-represented -> gap-only codes likely belong to these
"""

import json, os, sys
from collections import Counter

# ============================================================
# LOAD DATA & MAPPING (dp_parse version = best known)
# ============================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

# Use dp_parse mapping (the one that gave 67.2%)
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

# German bigram frequencies (log probabilities, normalized)
# Source: standard German corpus analysis
GERMAN_BIGRAMS = {
    'EN': 389, 'ER': 375, 'CH': 271, 'DE': 252, 'EI': 231,
    'ND': 218, 'TE': 217, 'IN': 216, 'IE': 212, 'GE': 186,
    'ST': 184, 'NE': 183, 'BE': 174, 'ES': 174, 'UN': 173,
    'RE': 166, 'AN': 164, 'HE': 160, 'SE': 157, 'AU': 148,
    'DI': 147, 'SC': 146, 'SI': 140, 'IC': 138, 'DA': 136,
    'LE': 133, 'DE': 132, 'AL': 130, 'RI': 128, 'LI': 125,
    'HA': 124, 'NT': 121, 'IT': 118, 'NG': 117, 'EL': 116,
    'WE': 114, 'IG': 112, 'TI': 111, 'VE': 108, 'SO': 107,
    'WI': 106, 'HT': 105, 'RA': 104, 'AR': 103, 'NI': 102,
    'ZU': 101, 'ME': 100, 'NS': 99, 'ET': 98, 'MI': 97,
    'AC': 96, 'RU': 95, 'OR': 94, 'SS': 93, 'NA': 92,
    'AH': 91, 'MA': 90, 'AG': 89, 'FU': 88, 'AB': 87,
    'EC': 86, 'DO': 85, 'OB': 84, 'SA': 83, 'LA': 82,
    'OD': 81, 'VO': 80, 'UE': 79, 'NN': 78, 'NZ': 77,
    'SU': 76, 'KO': 75, 'BI': 74, 'FE': 73, 'FI': 72,
    'UL': 71, 'EP': 70, 'BA': 69, 'PA': 68, 'PF': 67,
    'TU': 66, 'KE': 65, 'KA': 64, 'BL': 63, 'KI': 62,
    'WA': 61, 'WO': 60, 'RO': 59, 'RN': 58, 'DR': 57,
    'EH': 56, 'OE': 55, 'TS': 54, 'GT': 53, 'FO': 52,
    'UF': 51, 'BU': 50, 'AT': 49, 'NB': 48, 'TH': 47,
    'EE': 46, 'UM': 45, 'GR': 44, 'TR': 43, 'OL': 42,
    'EU': 41, 'AE': 40, 'HI': 39, 'ZE': 38, 'PR': 37,
    'GA': 36, 'NF': 35, 'NV': 34, 'ZA': 33, 'SP': 32,
    'TA': 31, 'KL': 30, 'MM': 29, 'BR': 28, 'HR': 27,
    'EW': 26, 'RD': 25, 'RG': 24, 'LL': 23, 'AM': 22,
}

# German letter frequencies (%)
GERMAN_FREQ = {
    'E': 17.40, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
    'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
    'L': 3.44, 'C': 3.06, 'G': 3.01, 'M': 2.53, 'O': 2.51,
    'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
    'P': 0.79, 'V': 0.67, 'J': 0.27, 'Y': 0.04, 'X': 0.03,
}

# German dictionary for DP parse
GERMAN_WORDS = set([
    'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO',
    'DU', 'OB', 'AM', 'IM', 'AB',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST',
    'WIR', 'ICH', 'SIE', 'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI', 'VOR', 'FUR', 'VOM',
    'ZUM', 'ZUR', 'BIS', 'ALS', 'NUN', 'HIN', 'TAG', 'ORT', 'TOD',
    'OFT', 'NIE', 'ALT', 'NEU', 'NOR', 'GAB', 'SAH', 'KAM', 'SEI',
    'TUN', 'ODE', 'GAR', 'NET', 'MAL',
    'NACH', 'AUCH', 'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN', 'WARD',
    'DASS', 'WENN', 'DANN', 'DENN', 'ABER', 'ODER', 'WEIL', 'WIRD',
    'EINE', 'DIES', 'HIER', 'DORT', 'WELT', 'ZEIT', 'TEIL', 'SEID',
    'WORT', 'NAME', 'GANZ', 'SEHR', 'VIEL', 'FORT', 'HOCH', 'KLAR',
    'ERDE', 'GOTT', 'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN', 'WAHR',
    'HELD', 'RUNE', 'FACH', 'WIND', 'FAND', 'GING', 'NAHM', 'SAGT',
    'HIHL', 'KANN', 'SOLL', 'WILL', 'MUSS', 'ENDE',
    'MACHT', 'KRAFT', 'GEIST', 'NACHT', 'LICHT', 'KRIEG', 'REICH',
    'UNTER', 'DURCH', 'GEGEN', 'IMMER', 'NICHT', 'SCHON',
    'DIESE', 'SEINE', 'EINEN', 'EINER', 'EINEM', 'EINES',
    'KOENIG', 'URALTE', 'STEINEN', 'STEINE', 'STEIN',
    'RUNEN', 'RUNEORT', 'FINDEN', 'STEHEN', 'GEHEN',
    'KOMMEN', 'MACHEN', 'SAGEN', 'WISSEN', 'KENNEN',
    'HALTEN', 'FALLEN', 'HELFEN', 'TRAGEN', 'LESEN',
    'ERSTE', 'ERSTEN', 'LETZTE', 'ANDERE',
    'SEINER', 'SEINEN', 'SEINES', 'DIESEM', 'DIESEN',
    'NORDEN', 'SUEDEN', 'OSTEN', 'WESTEN',
    'ALLE', 'ALLES', 'ALLEN', 'VIELE', 'WIEDER',
    'REDE', 'REDEN', 'WORTE', 'ORTE', 'ORTEN',
    'SCHAUN', 'RUIN', 'STEH', 'GEH', 'WISSET',
    # Proper nouns
    'LABGZERAS', 'HEDEMI', 'ADTHARSC', 'SCHWITEIONE', 'TIUMENGEMI',
    'ENGCHD', 'KELSEI', 'TAUTR', 'TOTNIURG', 'TOTNIURGS',
    'LABRNI', 'UTRUNR', 'GEVMT', 'AUNRSONGETRASES',
    'EILCHANHEARUCHTIG', 'EDETOTNIURGS', 'EDETOTNIURG',
    'EILCH', 'HEARUCHTIG', 'HEARUCHTIGER',
    'SCHWITEIO',
    # MHG
    'HWND', 'OEL', 'SCE', 'MINNE', 'RUCHTIG',
])

# ============================================================
# PREPROCESSING
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

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# ============================================================
# DP PARSE
# ============================================================

def dp_parse(text, word_set=GERMAN_WORDS):
    n = len(text)
    dp = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], None)
        max_wl = min(i, 20)
        for wlen in range(2, max_wl + 1):
            start = i - wlen
            cand = text[start:i]
            if '?' in cand:
                continue
            if cand in word_set:
                score = dp[start][0] + wlen
                if score > dp[i][0]:
                    dp[i] = (score, (start, cand))
    return dp[n][0], n

def word_coverage(m):
    """Calculate total word coverage for a mapping."""
    total_chars = 0
    total_covered = 0
    for bpairs in book_pairs:
        text = ''.join(m.get(p, '?') for p in bpairs)
        covered, n = dp_parse(text)
        known = sum(1 for c in text if c != '?')
        total_chars += known
        total_covered += covered
    return total_covered, total_chars

# ============================================================
# 1. IDENTIFY GAP-ONLY CODES
# ============================================================

print("=" * 70)
print("1. IDENTIFYING GAP-ONLY CODES")
print("=" * 70)

# For each code, check if it ever falls within a recognized word
code_in_word = Counter()
code_in_gap = Counter()
code_total = Counter()

for bpairs in book_pairs:
    text = ''.join(MAPPING.get(p, '?') for p in bpairs)
    n = len(text)

    # Run DP to find word boundaries
    dp = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], None)
        max_wl = min(i, 20)
        for wlen in range(2, max_wl + 1):
            start = i - wlen
            cand = text[start:i]
            if '?' in cand:
                continue
            if cand in GERMAN_WORDS:
                score = dp[start][0] + wlen
                if score > dp[i][0]:
                    dp[i] = (score, (start, cand))

    # Backtrack to find which positions are in words
    in_word = [False] * n
    i = n
    while i > 0:
        if dp[i][1] is not None:
            start, word = dp[i][1]
            for j in range(start, start + len(word)):
                in_word[j] = True
            i = start
        else:
            i -= 1

    # Map back to codes
    for pos, code in enumerate(bpairs):
        if pos < n:
            code_total[code] += 1
            if in_word[pos]:
                code_in_word[code] += 1
            else:
                code_in_gap[code] += 1

# Classify codes
gap_only = []  # Never in a word
mixed = []     # Sometimes in word, sometimes gap
word_only = [] # Always in a word

for code in sorted(MAPPING.keys(), key=lambda c: int(c)):
    total = code_total.get(code, 0)
    in_w = code_in_word.get(code, 0)
    in_g = code_in_gap.get(code, 0)
    letter = MAPPING[code]

    if total == 0:
        continue

    word_pct = in_w / total * 100 if total > 0 else 0

    if in_w == 0:
        gap_only.append((code, letter, total, in_g))
    elif word_pct < 20:
        mixed.append((code, letter, total, in_w, in_g, word_pct))

print(f"\n  GAP-ONLY codes (NEVER appear in a recognized word):")
print(f"  {'Code':>4s} {'Letter':>6s} {'Occurrences':>11s}")
print(f"  {'----':>4s} {'------':>6s} {'-----------':>11s}")
total_gap_occ = 0
for code, letter, total, in_g in sorted(gap_only, key=lambda x: -x[2]):
    total_gap_occ += total
    print(f"  [{code}]  {letter:>5s}  {total:>10d}")
print(f"\n  Total gap-only occurrences: {total_gap_occ}")

print(f"\n  LOW-WORD codes (<20% in words):")
for code, letter, total, in_w, in_g, wpct in sorted(mixed, key=lambda x: x[5]):
    print(f"  [{code}]  {letter:>5s}  {total:>5d} total, {in_w:>3d} in-word ({wpct:.0f}%)")

# ============================================================
# 2. LETTER FREQUENCY ANALYSIS
# ============================================================

print(f"\n{'=' * 70}")
print("2. LETTER FREQUENCY: ACTUAL vs EXPECTED GERMAN")
print("=" * 70)

# Count actual letter frequencies
letter_counts = Counter()
total_letters = 0
for bpairs in book_pairs:
    for code in bpairs:
        if code in MAPPING:
            letter_counts[MAPPING[code]] += 1
            total_letters += 1

print(f"\n  {'Letter':>6s} {'Actual%':>8s} {'Expected%':>9s} {'Delta':>7s} {'Codes':>5s} {'Status':>10s}")
print(f"  {'------':>6s} {'-------':>8s} {'---------':>9s} {'-----':>7s} {'-----':>5s} {'------':>10s}")

letter_code_counts = Counter()
for code, letter in MAPPING.items():
    letter_code_counts[letter] += 1

for letter in sorted(GERMAN_FREQ.keys(), key=lambda l: -GERMAN_FREQ[l]):
    actual = letter_counts.get(letter, 0) / total_letters * 100
    expected = GERMAN_FREQ[letter]
    delta = actual - expected
    n_codes = letter_code_counts.get(letter, 0)
    status = "OVER" if delta > 2 else "UNDER" if delta < -1 else "ok"
    if letter_counts.get(letter, 0) == 0:
        status = "MISSING!"
    print(f"  {letter:>6s} {actual:7.2f}% {expected:8.2f}% {delta:+6.2f}% {n_codes:>5d}  {status:>10s}")

# ============================================================
# 3. BIGRAM CONTEXT SCORING FOR EACH GAP-ONLY CODE
# ============================================================

print(f"\n{'=' * 70}")
print("3. BIGRAM CONTEXT ANALYSIS FOR GAP-ONLY CODES")
print("=" * 70)

def bigram_score_for_code(code, test_letter, m):
    """Score a letter assignment for a code by examining bigram context."""
    score = 0
    count = 0

    for bpairs in book_pairs:
        for pos, c in enumerate(bpairs):
            if c != code:
                continue

            # Get left and right neighbors
            left_letter = None
            right_letter = None

            if pos > 0:
                left_code = bpairs[pos - 1]
                left_letter = m.get(left_code, None)

            if pos < len(bpairs) - 1:
                right_code = bpairs[pos + 1]
                right_letter = m.get(right_code, None)

            # Score left bigram
            if left_letter:
                bg = left_letter + test_letter
                score += GERMAN_BIGRAMS.get(bg, 0)
                count += 1

            # Score right bigram
            if right_letter:
                bg = test_letter + right_letter
                score += GERMAN_BIGRAMS.get(bg, 0)
                count += 1

    return score / max(count, 1), count

# Test each gap-only code with all 26 letters
reassignment_candidates = []

for code, current_letter, total, _ in sorted(gap_only, key=lambda x: -x[2]):
    if total < 10:  # Skip very rare codes
        continue

    print(f"\n  --- Code [{code}] = {current_letter} ({total} occurrences) ---")

    scores = []
    for test_letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        avg_score, count = bigram_score_for_code(code, test_letter, MAPPING)
        scores.append((test_letter, avg_score, count))

    scores.sort(key=lambda x: -x[1])

    print(f"  Current ({current_letter}): score = {[s for l,s,c in scores if l==current_letter][0]:.1f}")
    print(f"  Top 5 alternatives:")
    for letter, sc, cnt in scores[:5]:
        delta = sc - [s for l,s,c in scores if l==current_letter][0]
        marker = " <-- CURRENT" if letter == current_letter else ""
        marker = " *** BEST" if delta > 0 and letter != current_letter and scores[0][0] == letter else marker
        deficit = GERMAN_FREQ.get(letter, 0) - letter_counts.get(letter, 0) / total_letters * 100
        print(f"    {letter}: {sc:6.1f} (delta={delta:+.1f}, "
              f"letter deficit={deficit:+.2f}%){marker}")

    # Record if best alternative is significantly better than current
    best_letter, best_score, _ = scores[0]
    current_score = [s for l,s,c in scores if l==current_letter][0]
    if best_letter != current_letter and best_score > current_score + 5:
        reassignment_candidates.append({
            'code': code,
            'current': current_letter,
            'proposed': best_letter,
            'current_score': current_score,
            'proposed_score': best_score,
            'improvement': best_score - current_score,
            'occurrences': total,
        })

# ============================================================
# 4. RANKED REASSIGNMENT CANDIDATES
# ============================================================

print(f"\n{'=' * 70}")
print("4. RANKED REASSIGNMENT CANDIDATES")
print("=" * 70)

reassignment_candidates.sort(key=lambda x: -x['improvement'] * x['occurrences'])

print(f"\n  {'Code':>4s} {'Curr':>5s} {'->':>2s} {'New':>4s} {'Score+':>7s} {'Occur':>5s} {'Impact':>7s}")
print(f"  {'----':>4s} {'-----':>5s} {'--':>2s} {'----':>4s} {'------':>7s} {'-----':>5s} {'------':>7s}")

for r in reassignment_candidates:
    impact = r['improvement'] * r['occurrences']
    print(f"  [{r['code']}]  {r['current']:>4s}  -> {r['proposed']:>3s}  "
          f"{r['improvement']:+6.1f}  {r['occurrences']:>5d}  {impact:>7.0f}")

# ============================================================
# 5. TEST TOP REASSIGNMENTS
# ============================================================

print(f"\n{'=' * 70}")
print("5. TESTING REASSIGNMENTS (DP WORD COVERAGE)")
print("=" * 70)

# Baseline
baseline_cov, baseline_total = word_coverage(MAPPING)
baseline_pct = baseline_cov / baseline_total * 100
print(f"\n  Baseline coverage: {baseline_cov}/{baseline_total} = {baseline_pct:.1f}%")

# Test each reassignment individually
print(f"\n  Individual reassignment tests:")
individual_results = []
for r in reassignment_candidates[:15]:
    test_map = dict(MAPPING)
    test_map[r['code']] = r['proposed']
    cov, total = word_coverage(test_map)
    pct = cov / total * 100
    delta = pct - baseline_pct
    individual_results.append((r, pct, delta))
    marker = " ***" if delta > 0.5 else " **" if delta > 0 else ""
    print(f"    [{r['code']}] {r['current']}->{r['proposed']}: "
          f"{pct:.1f}% (delta={delta:+.1f}%){marker}")

# Test cumulative (best N together)
print(f"\n  Cumulative reassignment tests:")
positive_changes = [(r, pct, delta) for r, pct, delta in individual_results if delta > 0]
positive_changes.sort(key=lambda x: -x[2])

cumulative_map = dict(MAPPING)
for i, (r, pct, delta) in enumerate(positive_changes):
    cumulative_map[r['code']] = r['proposed']
    cum_cov, cum_total = word_coverage(cumulative_map)
    cum_pct = cum_cov / cum_total * 100
    cum_delta = cum_pct - baseline_pct
    print(f"    +[{r['code']}] {r['current']}->{r['proposed']}: "
          f"cumulative = {cum_pct:.1f}% ({cum_delta:+.1f}%)")

# ============================================================
# 6. SHOW IMPROVED TEXT FOR KEY PASSAGES
# ============================================================

print(f"\n{'=' * 70}")
print("6. IMPROVED TEXT COMPARISON (key passages)")
print("=" * 70)

# Build best mapping
best_map = dict(MAPPING)
for r, pct, delta in positive_changes:
    best_map[r['code']] = r['proposed']

# Show key books with both mappings
for book_idx in [0, 2, 5, 9, 31]:
    bpairs = book_pairs[book_idx]
    old_text = ''.join(MAPPING.get(p, '?') for p in bpairs)
    new_text = ''.join(best_map.get(p, '?') for p in bpairs)

    if old_text != new_text:
        print(f"\n  Book {book_idx}:")
        # Show differences
        diff_positions = [i for i in range(len(old_text)) if old_text[i] != new_text[i]]
        if diff_positions:
            # Show context around first difference
            for dp in diff_positions[:5]:
                ctx_start = max(0, dp - 10)
                ctx_end = min(len(old_text), dp + 10)
                old_ctx = old_text[ctx_start:ctx_end]
                new_ctx = new_text[ctx_start:ctx_end]
                changed_code = bpairs[dp]
                print(f"    pos {dp}: [{changed_code}] {MAPPING[changed_code]}->{best_map[changed_code]}")
                print(f"      old: ...{old_ctx}...")
                print(f"      new: ...{new_ctx}...")

# ============================================================
# 7. SAVE IMPROVED MAPPING
# ============================================================

if positive_changes:
    output_path = os.path.join(data_dir, 'mapping_v5_improved.json')
    with open(output_path, 'w') as f:
        json.dump(best_map, f, indent=2, sort_keys=True)
    print(f"\n  Saved improved mapping to: {output_path}")
    print(f"  Changes made:")
    for r, pct, delta in positive_changes:
        print(f"    [{r['code']}] {r['current']} -> {r['proposed']} ({delta:+.1f}%)")

# ============================================================
# 8. INVESTIGATION: LABGZERAS RAW CODES
# ============================================================

print(f"\n{'=' * 70}")
print("8. LABGZERAS CODE ANALYSIS")
print("=" * 70)

# The codes for LABGZERAS: 34 85 62 84 77 09 08 89 52
lab_codes = ['34', '85', '62', '84', '77', '09', '08', '89', '52']
lab_letters = [MAPPING[c] for c in lab_codes]
print(f"\n  LABGZERAS codes: {' '.join(lab_codes)}")
print(f"  Current letters: {' '.join(lab_letters)} = {''.join(lab_letters)}")
print(f"  SALZBERG target: S  A  L  Z  B  E  R  G")
print()

# If LABGZERAS = SALZBERG, which code is the "extra A"?
print(f"  Two A codes in LABGZERAS:")
print(f"    Code [85] = A (position 2 in name)")
print(f"    Code [89] = A (position 8 in name)")
print(f"\n  Code [85] statistics:")
print(f"    Total occurrences: {code_total.get('85', 0)}")
print(f"    In words: {code_in_word.get('85', 0)}")
print(f"    In gaps: {code_in_gap.get('85', 0)}")
bg_score_85_a, _ = bigram_score_for_code('85', 'A', MAPPING)
print(f"    Bigram score as A: {bg_score_85_a:.1f}")

print(f"\n  Code [89] statistics:")
print(f"    Total occurrences: {code_total.get('89', 0)}")
print(f"    In words: {code_in_word.get('89', 0)}")
print(f"    In gaps: {code_in_gap.get('89', 0)}")
bg_score_89_a, _ = bigram_score_for_code('89', 'A', MAPPING)
print(f"    Bigram score as A: {bg_score_89_a:.1f}")

# Test alternative assignments for codes 85 and 89
print(f"\n  Alternative letter tests for code [89]:")
for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    sc, cnt = bigram_score_for_code('89', letter, MAPPING)
    if sc > bg_score_89_a - 5:
        print(f"    [89]={letter}: score={sc:.1f} (vs A={bg_score_89_a:.1f})")
