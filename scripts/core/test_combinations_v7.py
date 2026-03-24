#!/usr/bin/env python3
"""
Test the most promising code reassignment combinations.
Focus on changes that improve BOTH frequency fitness and word coverage.
"""

import json, os
from collections import Counter
from itertools import combinations, product

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

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
    'TAGE', 'TAGEN', 'NEBEN',
    'SAGTE', 'WURDE', 'WAREN', 'HATTE',
    'HABEN', 'LEBEN', 'SEHEN', 'NEHMEN', 'GEBEN',
    'FEUER', 'WASSER', 'STEIN', 'HOLZ', 'EISEN',
    'STERN', 'STERNE', 'MOND', 'SONNE',
    'BLUT', 'BEIN', 'HERZ', 'LEIB', 'HAUPT',
    'HELM', 'SCHILD',
    'FLUCHT', 'FURCHT', 'ZORN', 'STOLZ', 'SCHULD',
    'FRIEDE', 'FRIEDEN', 'FREUND', 'FEIND',
    'WAFFE', 'WAFFEN',
    'DRACHE', 'DRACHEN', 'RIESE', 'RIESEN',
    'ZAUBER', 'FLUCH', 'SEGEN', 'BANN',
    'TURM', 'MAUER', 'STRASSE',
    'DORF', 'STADT', 'SCHLOSS', 'TEMPEL',
    'WALD', 'WIESE', 'FLUSS', 'MEER', 'INSEL',
    'RITTER',
    'SAGE', 'SAGEN', 'LEGENDE',
    'ACHT', 'NEUN', 'ZEHN', 'DREI', 'VIER',
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

def freq_score(m):
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

base_cov, base_total = dp_coverage(MAPPING)
base_pct = base_cov / base_total * 100
base_freq = freq_score(MAPPING)

print("=" * 70)
print("COMBINATION TESTING")
print(f"Baseline: coverage={base_pct:.2f}%, freq_score={base_freq:.2f}")
print("=" * 70)

# Candidate changes (code, from, candidate_letters)
candidates = [
    ('53', 'N', ['O', 'A', 'M']),       # 37 occ, 43% word rate
    ('86', 'E', ['M', 'A', 'O']),       # 30 occ, bigram IM suggests M
    ('13', 'N', ['U', 'A', 'B', 'F']),  # 22 occ, 32% word rate
    ('83', 'N', ['A', 'U', 'W']),       # 28 occ, AM bigram
    ('71', 'N', ['M', 'B']),             # 33 occ, 73% word rate
    ('90', 'N', ['O', 'F']),             # 32 occ, 50% word rate
    ('60', 'N', ['L', 'M']),             # 58 occ, 43% word rate
    ('73', 'N', ['R', 'L']),             # 23 occ, 44% word rate
    ('63', 'D', ['W', 'O']),             # 23 occ, 39% word rate
    ('50', 'I', ['M']),                   # 35 occ, 29% word rate
    ('16', 'I', ['O', 'F']),              # 38 occ, 53% word rate
]

# Test all single changes first
print("\n--- SINGLE CHANGES ---")
single_results = []
for code, from_l, options in candidates:
    for to_l in options:
        test_map = dict(MAPPING)
        test_map[code] = to_l
        cov, total = dp_coverage(test_map)
        pct = cov / total * 100
        fs = freq_score(test_map)
        combined = pct - base_pct - (fs - base_freq) * 0.3  # weighted combined
        single_results.append((code, from_l, to_l, pct, fs, combined))
        if pct >= base_pct - 0.3 and fs < base_freq:
            marker = " ***" if pct > base_pct else ""
            print(f"  [{code}] {from_l}->{to_l}: cov={pct:.2f}%({pct-base_pct:+.2f}), "
                  f"freq={fs:.2f}({fs-base_freq:+.2f}){marker}")

# Now test the BEST combinations
# Pick top candidates for each code
best_per_code = {}
for code, from_l, to_l, pct, fs, combined in single_results:
    if pct >= base_pct - 0.5:  # don't consider big coverage drops
        if code not in best_per_code or combined > best_per_code[code][5]:
            best_per_code[code] = (code, from_l, to_l, pct, fs, combined)

# Top picks by combined score
top_picks = sorted(best_per_code.values(), key=lambda x: -x[5])

print(f"\n--- TOP PICKS BY COMBINED SCORE ---")
for code, from_l, to_l, pct, fs, combined in top_picks[:8]:
    print(f"  [{code}] {from_l}->{to_l}: cov={pct:.2f}%, freq={fs:.2f}, combined={combined:.2f}")

# Test pairs of top picks
print(f"\n--- PAIR COMBINATIONS ---")
top_codes = [(code, to_l) for code, _, to_l, _, _, _ in top_picks[:8]]
pair_results = []
for i in range(len(top_codes)):
    for j in range(i+1, len(top_codes)):
        c1, l1 = top_codes[i]
        c2, l2 = top_codes[j]
        test_map = dict(MAPPING)
        test_map[c1] = l1
        test_map[c2] = l2
        cov, total = dp_coverage(test_map)
        pct = cov / total * 100
        fs = freq_score(test_map)
        pair_results.append((c1, l1, c2, l2, pct, fs))

pair_results.sort(key=lambda x: -(x[4] - base_pct - (x[5] - base_freq) * 0.3))
print(f"\n  Top 10 pairs:")
for c1, l1, c2, l2, pct, fs in pair_results[:10]:
    old1 = MAPPING[c1]
    old2 = MAPPING[c2]
    print(f"  [{c1}]{old1}->{l1} + [{c2}]{old2}->{l2}: "
          f"cov={pct:.2f}%({pct-base_pct:+.2f}), freq={fs:.2f}({fs-base_freq:+.2f})")

# Test triples
print(f"\n--- TRIPLE COMBINATIONS ---")
triple_results = []
for i in range(len(top_codes)):
    for j in range(i+1, len(top_codes)):
        for k in range(j+1, len(top_codes)):
            c1, l1 = top_codes[i]
            c2, l2 = top_codes[j]
            c3, l3 = top_codes[k]
            test_map = dict(MAPPING)
            test_map[c1] = l1
            test_map[c2] = l2
            test_map[c3] = l3
            cov, total = dp_coverage(test_map)
            pct = cov / total * 100
            fs = freq_score(test_map)
            triple_results.append((c1, l1, c2, l2, c3, l3, pct, fs))

triple_results.sort(key=lambda x: -(x[6] - base_pct - (x[7] - base_freq) * 0.3))
print(f"\n  Top 10 triples:")
for c1, l1, c2, l2, c3, l3, pct, fs in triple_results[:10]:
    o1, o2, o3 = MAPPING[c1], MAPPING[c2], MAPPING[c3]
    print(f"  [{c1}]{o1}->{l1} + [{c2}]{o2}->{l2} + [{c3}]{o3}->{l3}: "
          f"cov={pct:.2f}%({pct-base_pct:+.2f}), freq={fs:.2f}({fs-base_freq:+.2f})")

# Test quad combinations
print(f"\n--- QUAD COMBINATIONS (top 4 picks) ---")
quad_results = []
for combo in combinations(range(min(6, len(top_codes))), 4):
    changes = [(top_codes[i][0], top_codes[i][1]) for i in combo]
    test_map = dict(MAPPING)
    for c, l in changes:
        test_map[c] = l
    cov, total = dp_coverage(test_map)
    pct = cov / total * 100
    fs = freq_score(test_map)
    quad_results.append((changes, pct, fs))

quad_results.sort(key=lambda x: -(x[1] - base_pct - (x[2] - base_freq) * 0.3))
print(f"\n  Top 5 quads:")
for changes, pct, fs in quad_results[:5]:
    desc = ' + '.join(f'[{c}]{MAPPING[c]}->{l}' for c, l in changes)
    print(f"  {desc}: cov={pct:.2f}%({pct-base_pct:+.2f}), freq={fs:.2f}({fs-base_freq:+.2f})")

# ============================================================
# APPLY BEST COMBINATION AND SHOW DECODED TEXT
# ============================================================
print(f"\n{'=' * 70}")
print("BEST VERIFIED V7 MAPPING")
print(f"{'=' * 70}")

# Apply the best triple or quad
if quad_results:
    best_combo = quad_results[0]
elif triple_results:
    best_combo_data = triple_results[0]
    best_combo = ([(best_combo_data[0], best_combo_data[1]),
                   (best_combo_data[2], best_combo_data[3]),
                   (best_combo_data[4], best_combo_data[5])],
                  best_combo_data[6], best_combo_data[7])
else:
    best_combo = None

if best_combo:
    changes, pct, fs = best_combo
    v7 = dict(MAPPING)
    for c, l in changes:
        v7[c] = l

    print(f"\nChanges applied:")
    for c, l in changes:
        print(f"  [{c}] {MAPPING[c]} -> {l} ({code_counts.get(c, 0)} occ)")
    print(f"\nCoverage: {pct:.2f}% (was {base_pct:.2f}%, delta={pct-base_pct:+.2f}%)")
    print(f"Freq score: {fs:.2f} (was {base_freq:.2f}, delta={fs-base_freq:+.2f})")

    # Save
    v7_path = os.path.join(data_dir, 'mapping_v7.json')
    with open(v7_path, 'w') as f:
        json.dump(v7, f, indent=2, sort_keys=True)
    print(f"\nSaved to {v7_path}")

    # Show letter frequency improvement
    print(f"\n  Letter frequency with v7:")
    letter_counts = Counter()
    for code, letter in v7.items():
        letter_counts[letter] += code_counts.get(code, 0)

    print(f"  {'Ltr':>3} {'Codes':>5} {'Pct':>7} {'German':>7} {'Delta':>7}")
    for letter in 'ABCDEFGHIJKLMNOPRSTUVWZ':
        if letter not in GERMAN_FREQ:
            continue
        num_codes = sum(1 for v in v7.values() if v == letter)
        actual = letter_counts.get(letter, 0) / total_coded * 100
        german = GERMAN_FREQ[letter]
        delta = actual - german
        flag = " <<<" if abs(delta) > 2.0 else ""
        if actual > 0 or german > 0.5:
            print(f"  {letter:>3} {num_codes:>5} {actual:>6.2f}% {german:>6.2f}% {delta:>+6.2f}%{flag}")

    # Decode sample books
    def dp_parse(text):
        n = len(text)
        dp = [(0, None)] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = (dp[i-1][0], None)
            for wlen in range(2, min(i, 20) + 1):
                start = i - wlen
                cand = text[start:i]
                if '?' not in cand and cand in GERMAN_WORDS:
                    score = dp[start][0] + wlen
                    if score > dp[i][0]:
                        dp[i] = (score, (start, cand))
        tokens = []
        i = n
        while i > 0:
            if dp[i][1] is not None:
                start, word = dp[i][1]
                tokens.append(('WORD', word))
                i = start
            else:
                tokens.append(('CHAR', text[i-1]))
                i -= 1
        tokens.reverse()
        merged = []
        for kind, val in tokens:
            if kind == 'WORD':
                merged.append(val)
            else:
                if merged and merged[-1].startswith('['):
                    merged[-1] = merged[-1][:-1] + val + ']'
                else:
                    merged.append('[' + val + ']')
        return merged, dp[n][0]

    print(f"\n--- DECODED SAMPLES (top coverage books) ---")
    book_covs = []
    for idx, bpairs in enumerate(book_pairs):
        if len(bpairs) < 30:
            continue
        text = ''.join(v7.get(p, '?') for p in bpairs)
        tokens, covered = dp_parse(text)
        known = sum(1 for c in text if c != '?')
        pct_book = covered / max(known, 1) * 100
        book_covs.append((idx, pct_book, tokens))

    book_covs.sort(key=lambda x: -x[1])
    for idx, pct_book, tokens in book_covs[:15]:
        parsed = ' '.join(tokens)
        print(f"\n  Book {idx:2d} ({pct_book:2.0f}%): {parsed[:250]}")
