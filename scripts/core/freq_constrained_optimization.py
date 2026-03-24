#!/usr/bin/env python3
"""
Frequency-Constrained Optimization
====================================
The greedy DP optimizer overfits by assigning too many codes to N and I.
This script uses letter frequency as a CONSTRAINT to find the true mapping.

Strategy:
1. Start from v6+v4 baseline (58.76%)
2. Identify which N codes (13!) are most suspicious
3. Test reassigning excess N codes to under-represented letters (B, F, M, L, P)
4. Use combined score: word_coverage + frequency_fitness
5. Avoid changes that make frequency imbalance worse
"""

import json, os
from collections import Counter
from itertools import combinations

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

# V6+V4 = our best VERIFIED mapping
MAPPING = {
    "00": "H", "01": "E", "02": "D", "03": "E", "04": "M", "05": "S",
    "06": "H", "08": "R", "09": "E", "10": "R", "11": "N",
    "12": "S", "13": "N", "14": "N", "15": "I", "16": "I",
    "17": "E", "18": "C", "19": "E", "20": "F", "21": "I",
    "22": "K", "23": "S", "24": "R", "25": "O", "26": "E",
    "27": "E", "28": "D", "29": "E", "30": "E", "31": "A",
    "33": "W", "34": "L", "35": "A", "36": "W", "37": "E",
    "38": "K", "39": "E", "40": "M", "41": "E", "42": "D",
    "43": "U", "44": "U", "45": "D", "46": "I", "47": "D",
    "48": "N", "49": "E", "50": "I", "51": "R", "52": "S",
    "53": "N", "54": "M", "55": "R", "56": "E", "57": "H",
    "58": "N", "59": "S", "60": "N", "61": "U", "62": "B",
    "63": "D", "64": "T", "65": "I", "66": "A", "67": "E",
    "68": "R", "69": "E", "70": "U", "71": "N", "72": "R",
    "73": "N", "74": "E", "75": "T", "76": "E", "77": "Z",
    "78": "T", "79": "O", "80": "G", "81": "T", "82": "O",
    "83": "N", "84": "G", "85": "A", "86": "E", "87": "W",
    "88": "T", "89": "A", "90": "N", "91": "S", "92": "S",
    "93": "N", "94": "H", "95": "E", "96": "L", "97": "G",
    "98": "T", "99": "O",
}

GERMAN_WORDS = set([
    'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO',
    'DU', 'OB', 'AM', 'IM', 'AB',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST',
    'WIR', 'ICH', 'SIE', 'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI', 'VOR', 'FUR', 'VOM',
    'ZUM', 'ZUR', 'BIS', 'ALS', 'NUN', 'HIN', 'TAG', 'ORT', 'TOD',
    'OFT', 'NIE', 'ALT', 'NEU', 'GAR', 'NET', 'ODE', 'SEI', 'TUN',
    'MAL', 'RAT', 'RUF', 'MUT', 'HUT', 'NOT', 'ROT', 'TAT',
    'ENDE', 'REDE', 'RUNE', 'WORT', 'NACH', 'AUCH',
    'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN', 'WARD', 'DASS', 'WENN',
    'DANN', 'DENN', 'ABER', 'ODER', 'WEIL', 'WIRD', 'EINE', 'DIES',
    'HIER', 'DORT', 'WELT', 'ZEIT', 'TEIL', 'SEID', 'WORT', 'NAME',
    'GANZ', 'SEHR', 'VIEL', 'FORT', 'HOCH', 'KLAR', 'ERDE', 'GOTT',
    'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN', 'WAHR', 'HELD', 'FACH',
    'WIND', 'FAND', 'GING', 'NAHM', 'SAGT', 'KANN', 'SOLL', 'WILL',
    'MUSS', 'GIBT', 'RIEF', 'LAND', 'HAND', 'BAND', 'SAND', 'WAND',
    'MACHT', 'KRAFT', 'GEIST', 'NACHT', 'LICHT', 'KRIEG', 'REICH',
    'UNTER', 'DURCH', 'GEGEN', 'IMMER', 'NICHT', 'SCHON',
    'DIESE', 'SEINE', 'EINEN', 'EINER', 'EINEM', 'EINES',
    'URALTE', 'STEINEN', 'STEINE', 'STEIN', 'RUNEN', 'FINDEN',
    'STEHEN', 'GEHEN', 'KOMMEN', 'SAGEN', 'WISSEN',
    'ERSTE', 'ANDEREN', 'KOENIG', 'SCHAUN', 'RUIN',
    'ORTE', 'ORTEN', 'WORTE', 'STEH', 'GEH',
    'ALLE', 'ALLES', 'VIELE', 'WIEDER', 'WISSET',
    'SPRACH', 'GESCHAH', 'GEFUNDEN', 'GEBOREN', 'GESTORBEN',
    'ZWISCHEN', 'HEILIG', 'DUNKEL', 'SCHWERT',
    'STIMME', 'ZEICHEN', 'HIMMEL', 'SEELE', 'GEHEIMNIS',
    'MIN', 'SER', 'GEN', 'WEG', 'INS', 'HER',
    'SEI', 'LIES', 'SAG', 'GIB', 'WAR', 'GAR',
    'REDE', 'REDEN', 'WESEN', 'EHRE', 'TREUE', 'GRAB', 'GRUFT',
    'ALTE', 'ALTEN', 'ALTER', 'NEUE', 'NEUEN',
    'DUNKLE', 'DUNKLEN',
    'HWND', 'OEL', 'SCE', 'MINNE', 'RUCHTIG',
    'HEARUCHTIG', 'HEARUCHTIGER',
    'LABGZERAS', 'HEDEMI', 'ADTHARSC', 'TAUTR',
    'TOTNIURG', 'TOTNIURGS', 'EDETOTNIURG', 'EDETOTNIURGS',
    'SCHWITEIONE', 'SCHWITEIO', 'ENGCHD', 'KELSEI',
    'TIUMENGEMI', 'LABRNI', 'UTRUNR', 'GEVMT',
    'AUNRSONGETRASES', 'EILCH', 'EILCHANHEARUCHTIG',
    'DIESEN', 'DIESEM', 'DIESER', 'DIESES',
    'SEINER', 'SEINEN', 'SEINES', 'SEINEM',
    'NORDEN', 'SUEDEN', 'OSTEN', 'WESTEN',
    'RUNEORT', 'RUNENSTEIN',
    'EDEL', 'ADEL', 'HARSCH', 'SCHAR',
    'HIHL', 'SANG',
    'TEIL', 'TEILE', 'TEILEN', 'SEITE', 'SEITEN',
    'GROSSE', 'GROSSEN', 'GROSS', 'KLEINE', 'KLEINEN', 'KLEIN',
    'TAGE', 'TAGEN', 'NEBEN', 'HINEIN', 'HINAUS',
    'LIESS', 'SAGTE', 'WURDE', 'WAREN', 'HATTE',
    'HABEN', 'LEBEN', 'SEHEN', 'NEHMEN', 'GEBEN',
    'HALTEN', 'LASSEN', 'FALLEN', 'TRAGEN', 'SCHLAGEN',
    'BRINGEN', 'DENKEN', 'KENNEN', 'NENNEN', 'BRENNEN',
    'FEUER', 'WASSER', 'STEIN', 'HOLZ', 'EISEN',
    'STERN', 'STERNE', 'STERNEN', 'MOND', 'SONNE',
    'BLUT', 'BEIN', 'HERZ', 'LEIB', 'HAUPT',
    'HELM', 'SCHILD', 'PFEIL', 'BOGEN',
    'FLUCHT', 'FURCHT', 'ZORN', 'STOLZ', 'SCHULD',
    'FRIEDE', 'FRIEDEN', 'FREUND', 'FEIND',
    'WAFFE', 'WAFFEN', 'KLINGE', 'KLINGEN',
    'DRACHE', 'DRACHEN', 'RIESE', 'RIESEN',
    'ZAUBER', 'FLUCH', 'SEGEN', 'BANN',
    'TURM', 'MAUER', 'STRASSE',
    'DORF', 'STADT', 'SCHLOSS', 'TEMPEL',
    'WALD', 'WIESE', 'FLUSS', 'MEER', 'INSEL',
    'KNECHT', 'KRIEGER', 'PRIESTER', 'MAGIER',
    'TOCHTER', 'BRUDER', 'SCHWESTER', 'MUTTER', 'VATER',
    'RITTER', 'GRAF', 'FUERST', 'HERZOG',
    'SAGE', 'SAGEN', 'LEGENDE',
    'RUHE', 'STILLE', 'SCHWEIGEN',
    'DIENST', 'TREUE', 'PFLICHT',
    'GRENZE', 'GRENZEN', 'GEBIET',
    'WACHE', 'WACHT', 'HUETER',
    'SCHRIFT', 'SIEGEL',
    'ACHT', 'NEUN', 'ZEHN', 'DREI', 'VIER', 'FUENF',
    'SECHS', 'SIEBEN', 'ZWEI', 'EINS',
])

GERMAN_FREQ = {
    'E': 16.93, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
    'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
    'L': 3.44, 'C': 3.06, 'G': 3.01, 'M': 2.53, 'O': 2.51,
    'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
    'P': 0.79, 'V': 0.67, 'J': 0.27, 'Y': 0.04, 'X': 0.03,
    'Q': 0.02,
}

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

code_counts = Counter()
for bpairs in book_pairs:
    code_counts.update(bpairs)

total_coded = sum(code_counts.values())

def dp_coverage(m):
    total_chars = 0
    total_covered = 0
    for bpairs in book_pairs:
        text = ''.join(m.get(p, '?') for p in bpairs)
        n = len(text)
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i-1]
            for wlen in range(2, min(i, 20) + 1):
                start = i - wlen
                cand = text[start:i]
                if '?' not in cand and cand in GERMAN_WORDS:
                    dp[i] = max(dp[i], dp[start] + wlen)
        known = sum(1 for c in text if c != '?')
        total_chars += known
        total_covered += dp[n]
    return total_covered, total_chars

def word_participation_rate(m, code, letter):
    """What fraction of this code's occurrences fall within recognized words?"""
    in_word = 0
    total = 0
    for bpairs in book_pairs:
        text = ''.join(m.get(p, '?') for p in bpairs)
        n = len(text)
        # Build DP
        dp = [0] * (n + 1)
        choice = [None] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i-1]
            for wlen in range(2, min(i, 20) + 1):
                start = i - wlen
                cand = text[start:i]
                if '?' not in cand and cand in GERMAN_WORDS:
                    if dp[start] + wlen > dp[i]:
                        dp[i] = dp[start] + wlen
                        choice[i] = (start, i)
        # Trace back to find which positions are in words
        in_word_pos = set()
        i = n
        while i > 0:
            if choice[i] is not None:
                s, e = choice[i]
                for p in range(s, e):
                    in_word_pos.add(p)
                i = s
            else:
                i -= 1
        # Check code positions
        pos = 0
        for p in bpairs:
            if p == code:
                total += 1
                if pos in in_word_pos:
                    in_word += 1
            pos += 1
    return in_word, total

print("=" * 70)
print("FREQUENCY-CONSTRAINED OPTIMIZATION")
print("=" * 70)

# ============================================================
# STEP 1: Analyze current letter distribution
# ============================================================
print("\nSTEP 1: Current letter distribution vs German expected")

letter_codes = {}
for code, letter in MAPPING.items():
    if letter not in letter_codes:
        letter_codes[letter] = []
    letter_codes[letter].append(code)

letter_occ = {}
for letter, codes in letter_codes.items():
    letter_occ[letter] = sum(code_counts.get(c, 0) for c in codes)

print(f"\n{'Letter':>3} {'Codes':>5} {'Occ':>5} {'Actual%':>8} {'German%':>8} {'Delta':>8} {'Excess_codes':>12}")
for letter in sorted(GERMAN_FREQ.keys(), key=lambda x: -GERMAN_FREQ[x]):
    codes = letter_codes.get(letter, [])
    occ = letter_occ.get(letter, 0)
    actual_pct = occ / total_coded * 100
    german_pct = GERMAN_FREQ[letter]
    delta = actual_pct - german_pct
    # Expected codes = german_pct / 100 * total_coded / avg_occ_per_code
    avg_occ = total_coded / len(MAPPING)
    expected_codes = german_pct / 100 * total_coded / avg_occ
    excess = len(codes) - expected_codes
    if actual_pct > 0 or german_pct > 0.5:
        print(f"  {letter:>3} {len(codes):>5} {occ:>5} {actual_pct:>7.2f}% {german_pct:>7.2f}% {delta:>+7.2f}% {excess:>+11.1f}")

# ============================================================
# STEP 2: Find the most suspicious N codes
# ============================================================
print(f"\n{'=' * 70}")
print("STEP 2: ANALYZING N CODES (13 codes, severely over-represented)")
print(f"{'=' * 70}")

n_codes = [c for c, l in MAPPING.items() if l == 'N']
print(f"\nN codes: {sorted(n_codes)}")
print(f"Total N occurrences: {sum(code_counts.get(c, 0) for c in n_codes)}")
print(f"Expected N occurrences: {int(total_coded * 9.78 / 100)}")
print(f"Excess: {sum(code_counts.get(c, 0) for c in n_codes) - int(total_coded * 9.78 / 100)}")

print(f"\n  {'Code':>5} {'Occ':>5} {'WordRate':>10} {'InWord':>8} {'Total':>8}")
n_stats = []
for code in sorted(n_codes, key=lambda c: code_counts.get(c, 0)):
    occ = code_counts.get(code, 0)
    in_w, tot = word_participation_rate(MAPPING, code, 'N')
    rate = in_w / max(tot, 1) * 100
    n_stats.append((code, occ, rate, in_w, tot))
    print(f"  [{code:>2}] {occ:>5} {rate:>9.1f}% {in_w:>8} {tot:>8}")

# ============================================================
# STEP 3: Similarly analyze I and E codes (also over-represented)
# ============================================================
print(f"\n{'=' * 70}")
print("STEP 3: ANALYZING I CODES (7 codes, over-represented)")
print(f"{'=' * 70}")

i_codes = [c for c, l in MAPPING.items() if l == 'I']
print(f"\nI codes: {sorted(i_codes)}")
for code in sorted(i_codes, key=lambda c: code_counts.get(c, 0)):
    occ = code_counts.get(code, 0)
    in_w, tot = word_participation_rate(MAPPING, code, 'I')
    rate = in_w / max(tot, 1) * 100
    print(f"  [{code:>2}] {occ:>5} {rate:>9.1f}%")

print(f"\n{'=' * 70}")
print("STEP 3b: ANALYZING D CODES (6 codes, over-represented)")
print(f"{'=' * 70}")

d_codes = [c for c, l in MAPPING.items() if l == 'D']
print(f"\nD codes: {sorted(d_codes)}")
for code in sorted(d_codes, key=lambda c: code_counts.get(c, 0)):
    occ = code_counts.get(code, 0)
    in_w, tot = word_participation_rate(MAPPING, code, 'D')
    rate = in_w / max(tot, 1) * 100
    print(f"  [{code:>2}] {occ:>5} {rate:>9.1f}%")

# ============================================================
# STEP 4: For lowest-participating N codes, test B/F/M/L/P
# ============================================================
print(f"\n{'=' * 70}")
print("STEP 4: TESTING REASSIGNMENTS FOR SUSPICIOUS N CODES")
print("Target letters: B, F, M, L, P (all under-represented)")
print(f"{'=' * 70}")

base_cov, base_total = dp_coverage(MAPPING)
base_pct = base_cov / base_total * 100
print(f"\nBaseline: {base_pct:.2f}%")

# Sort N codes by word participation rate (lowest first = most suspicious)
n_stats.sort(key=lambda x: x[2])
target_letters = ['B', 'F', 'M', 'L', 'P', 'A', 'O', 'U', 'W']

for code, occ, rate, in_w, tot in n_stats:
    if occ < 5:
        continue
    print(f"\n  [{code}] N ({occ} occ, {rate:.1f}% word rate):")
    results = []
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        test_map = dict(MAPPING)
        test_map[code] = letter
        cov, total = dp_coverage(test_map)
        pct = cov / total * 100
        delta = pct - base_pct
        results.append((letter, pct, delta))
    results.sort(key=lambda x: -x[1])
    # Show top 5 and current N
    n_pct = next(p for l, p, d in results if l == 'N')
    print(f"    Current N: {n_pct:.2f}%")
    print(f"    Top 5: {', '.join(f'{l}={p:.2f}%({d:+.2f})' for l, p, d in results[:5])}")
    # Show under-represented letters
    under = [(l, p, d) for l, p, d in results if l in target_letters]
    under.sort(key=lambda x: -x[1])
    print(f"    Under-rep: {', '.join(f'{l}={p:.2f}%({d:+.2f})' for l, p, d in under[:5])}")

# ============================================================
# STEP 5: For suspicious I codes, test alternatives
# ============================================================
print(f"\n{'=' * 70}")
print("STEP 5: TESTING REASSIGNMENTS FOR I CODES")
print(f"{'=' * 70}")

for code in sorted(i_codes, key=lambda c: code_counts.get(c, 0)):
    occ = code_counts.get(code, 0)
    if occ < 10:
        continue
    in_w, tot = word_participation_rate(MAPPING, code, 'I')
    rate = in_w / max(tot, 1) * 100
    print(f"\n  [{code}] I ({occ} occ, {rate:.1f}% word rate):")
    results = []
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        test_map = dict(MAPPING)
        test_map[code] = letter
        cov, total = dp_coverage(test_map)
        pct = cov / total * 100
        delta = pct - base_pct
        results.append((letter, pct, delta))
    results.sort(key=lambda x: -x[1])
    print(f"    Top 5: {', '.join(f'{l}={p:.2f}%({d:+.2f})' for l, p, d in results[:5])}")
    under = [(l, p, d) for l, p, d in results if l in target_letters]
    under.sort(key=lambda x: -x[1])
    print(f"    Under-rep: {', '.join(f'{l}={p:.2f}%({d:+.2f})' for l, p, d in under[:5])}")

# ============================================================
# STEP 6: For suspicious D codes, test alternatives
# ============================================================
print(f"\n{'=' * 70}")
print("STEP 6: TESTING REASSIGNMENTS FOR D CODES")
print(f"{'=' * 70}")

for code in sorted(d_codes, key=lambda c: code_counts.get(c, 0)):
    occ = code_counts.get(code, 0)
    if occ < 10:
        continue
    in_w, tot = word_participation_rate(MAPPING, code, 'D')
    rate = in_w / max(tot, 1) * 100
    print(f"\n  [{code}] D ({occ} occ, {rate:.1f}% word rate):")
    results = []
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        test_map = dict(MAPPING)
        test_map[code] = letter
        cov, total = dp_coverage(test_map)
        pct = cov / total * 100
        delta = pct - base_pct
        results.append((letter, pct, delta))
    results.sort(key=lambda x: -x[1])
    print(f"    Top 5: {', '.join(f'{l}={p:.2f}%({d:+.2f})' for l, p, d in results[:5])}")

# ============================================================
# STEP 7: Bigram context analysis for suspicious codes
# ============================================================
print(f"\n{'=' * 70}")
print("STEP 7: BIGRAM CONTEXT ANALYSIS")
print("What letters appear before/after each suspicious code?")
print(f"{'=' * 70}")

# German bigram frequencies (top ones)
COMMON_BIGRAMS = {
    'EN', 'ER', 'CH', 'DE', 'EI', 'ND', 'TE', 'IN', 'IE', 'GE',
    'ES', 'NE', 'UN', 'ST', 'RE', 'HE', 'AN', 'BE', 'SE', 'HA',
    'AU', 'NG', 'DI', 'LE', 'IC', 'DA', 'SS', 'SC', 'DU', 'WI',
    'SI', 'SO', 'TI', 'EL', 'AL', 'AR', 'MA', 'WE', 'UR', 'UE',
    'MI', 'AB', 'LI', 'NI', 'OR', 'ME', 'RI', 'UND', 'ZU',
    'FU', 'FA', 'FE', 'FI', 'FL', 'FR',
    'BA', 'BI', 'BL', 'BR', 'BU',
    'PF', 'PL', 'PR',
}

suspicious = ['53', '58', '60', '73', '83', '86', '90', '93',  # N codes
              '16', '46', '50', '65',  # I codes
              '02', '42', '45', '47', '63']  # D codes

for code in suspicious:
    occ = code_counts.get(code, 0)
    if occ < 5:
        continue
    letter = MAPPING[code]

    # Collect bigram context
    prev_codes = Counter()
    next_codes = Counter()
    for bpairs in book_pairs:
        for i, p in enumerate(bpairs):
            if p == code:
                if i > 0:
                    prev_codes[bpairs[i-1]] += 1
                if i < len(bpairs) - 1:
                    next_codes[bpairs[i+1]] += 1

    print(f"\n  [{code}]={letter} ({occ} occ):")
    # Show context as decoded letters
    prev_context = []
    for pc, cnt in prev_codes.most_common(8):
        pl = MAPPING.get(pc, '?')
        bigram = pl + letter
        is_good = bigram in COMMON_BIGRAMS
        prev_context.append(f"{pl}_ ({cnt}x){'*' if is_good else ''}")
    print(f"    Before: {', '.join(prev_context)}")

    next_context = []
    for nc, cnt in next_codes.most_common(8):
        nl = MAPPING.get(nc, '?')
        bigram = letter + nl
        is_good = bigram in COMMON_BIGRAMS
        next_context.append(f"_{nl} ({cnt}x){'*' if is_good else ''}")
    print(f"    After:  {', '.join(next_context)}")

# ============================================================
# STEP 8: Combined frequency+coverage scoring
# ============================================================
print(f"\n{'=' * 70}")
print("STEP 8: COMBINED FREQUENCY+COVERAGE SCORING")
print("Testing swaps that IMPROVE frequency AND maintain/improve coverage")
print(f"{'=' * 70}")

def freq_score(m):
    """Lower = better frequency match."""
    letter_counts = Counter()
    total = 0
    for code, letter in m.items():
        occ = code_counts.get(code, 0)
        letter_counts[letter] += occ
        total += occ
    score = 0
    for letter, expected_pct in GERMAN_FREQ.items():
        actual_pct = letter_counts.get(letter, 0) / total * 100
        score += abs(actual_pct - expected_pct)
    return score

base_freq_score = freq_score(MAPPING)
print(f"\nBaseline freq score: {base_freq_score:.2f} (lower = better)")
print(f"Baseline word coverage: {base_pct:.2f}%")

# Try all single swaps for over-represented letters to under-represented
over_letters = ['N', 'I', 'D', 'E']
under_letters = ['B', 'F', 'M', 'L', 'P']

good_swaps = []
for over_l in over_letters:
    codes_for_letter = [c for c, l in MAPPING.items() if l == over_l and code_counts.get(c, 0) >= 5]
    for code in codes_for_letter:
        occ = code_counts.get(code, 0)
        for target_l in under_letters + ['A', 'O', 'U', 'W']:
            test_map = dict(MAPPING)
            test_map[code] = target_l
            cov, total = dp_coverage(test_map)
            pct = cov / total * 100
            fs = freq_score(test_map)
            # Accept if: frequency improves AND coverage doesn't drop much
            if fs < base_freq_score - 0.5 and pct >= base_pct - 0.3:
                good_swaps.append({
                    'code': code,
                    'from': over_l,
                    'to': target_l,
                    'occ': occ,
                    'coverage': pct,
                    'cov_delta': pct - base_pct,
                    'freq_score': fs,
                    'freq_delta': fs - base_freq_score,
                })

good_swaps.sort(key=lambda x: x['freq_delta'])

print(f"\nSwaps that improve frequency (>0.5 reduction) without major coverage loss (<0.3%):")
for s in good_swaps[:20]:
    print(f"  [{s['code']}] {s['from']}->{s['to']} ({s['occ']} occ): "
          f"cov={s['coverage']:.2f}% ({s['cov_delta']:+.2f}%), "
          f"freq={s['freq_score']:.2f} ({s['freq_delta']:+.2f})")
