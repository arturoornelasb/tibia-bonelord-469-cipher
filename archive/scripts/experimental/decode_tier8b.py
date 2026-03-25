"""
Tier 8b: Deep analysis of remaining 21 unknown codes.
Focus on deficit letters: O, B, M, F, K, Z, P, V, A, W, S, G, L.
77 codes confirmed through tier 8a.
"""
import json
from collections import Counter, defaultdict

with open('books.json', 'r') as f:
    books = json.load(f)

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

# All 77 tier 8a codes
fixed = {
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
    '47': 'D', '13': 'N', '71': 'I', '79': 'H', '63': 'D',
    '93': 'N', '28': 'D', '86': 'E', '43': 'U',
    '70': 'U', '65': 'I', '16': 'I', '36': 'W',
    '64': 'T', '89': 'A', '80': 'G', '97': 'G', '75': 'T',
    '08': 'R', '20': 'F', '96': 'L', '99': 'O', '55': 'R',
    '67': 'E', '27': 'E', '03': 'E', '09': 'E',
    '05': 'C', '53': 'N',
    '44': 'U', '62': 'B', '68': 'R',
    '23': 'S', '17': 'E', '29': 'E', '66': 'A', '22': 'D', '49': 'E',
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

pair_counts = Counter()
for pairs in book_pairs:
    pair_counts.update(pairs)
total_pairs = sum(pair_counts.values())

german_bigrams = {
    'EN': 3.88, 'ER': 3.75, 'CH': 2.75, 'DE': 2.00, 'EI': 1.88,
    'ND': 1.88, 'TE': 1.67, 'IN': 1.65, 'IE': 1.64, 'GE': 1.43,
    'ES': 1.36, 'NE': 1.26, 'SE': 1.20, 'RE': 1.18, 'HE': 1.16,
    'AN': 1.14, 'UN': 1.14, 'ST': 1.13, 'BE': 1.06, 'DI': 0.98,
    'EL': 0.92, 'AU': 0.87, 'IC': 0.86, 'NG': 0.82, 'SI': 0.77,
    'IT': 0.75, 'NI': 0.75, 'SC': 0.75, 'AL': 0.73, 'ET': 0.73,
    'LI': 0.73, 'RA': 0.72, 'RI': 0.72, 'HI': 0.69, 'IS': 0.69,
    'IG': 0.68, 'DA': 0.66, 'UE': 0.66, 'WI': 0.65, 'WE': 0.64,
    'TI': 0.63, 'ME': 0.63, 'HA': 0.62, 'NT': 0.62, 'EC': 0.61,
    'LE': 0.58, 'NS': 0.57, 'ED': 0.56, 'MI': 0.54, 'AS': 0.53,
    'ON': 0.51, 'RD': 0.50, 'EM': 0.48, 'SS': 0.48, 'US': 0.47,
    'EU': 0.46, 'DU': 0.46, 'UF': 0.45, 'AB': 0.44, 'UR': 0.44,
    'RN': 0.44, 'WA': 0.43, 'OL': 0.43, 'AR': 0.42, 'SO': 0.42,
    'EH': 0.41, 'OC': 0.40, 'HT': 0.40, 'BI': 0.38, 'OR': 0.38,
    'VO': 0.38, 'ZU': 0.38, 'OD': 0.37, 'MA': 0.37, 'AT': 0.37,
    'AH': 0.36, 'SU': 0.35, 'EG': 0.35, 'TO': 0.35, 'NO': 0.35,
    'DO': 0.34, 'TR': 0.34, 'OT': 0.33, 'UG': 0.33, 'UT': 0.32,
    'TA': 0.32, 'IL': 0.32, 'AE': 0.31, 'HN': 0.31, 'FE': 0.31,
    'RU': 0.30, 'TU': 0.30, 'KE': 0.30, 'LT': 0.30, 'ZE': 0.30,
    'OE': 0.29, 'FO': 0.28, 'AG': 0.28, 'EW': 0.28, 'LA': 0.27,
    'EF': 0.26, 'AM': 0.26, 'VE': 0.26, 'NA': 0.25, 'HL': 0.25,
    'OH': 0.24, 'OB': 0.23, 'GR': 0.23, 'NZ': 0.23, 'LS': 0.22,
    'RG': 0.22, 'IM': 0.22, 'OG': 0.21, 'OM': 0.21, 'HU': 0.20,
    'EK': 0.20, 'WO': 0.20, 'ZI': 0.20, 'UL': 0.19, 'NN': 0.19,
    'SA': 0.19, 'KO': 0.19, 'GT': 0.18, 'LO': 0.18, 'AF': 0.17,
    'BL': 0.17, 'BR': 0.17, 'RS': 0.17, 'DR': 0.17, 'AK': 0.16,
    'HO': 0.16, 'KA': 0.16, 'MM': 0.16, 'PE': 0.16, 'TS': 0.16,
    'TT': 0.16, 'PF': 0.15, 'SP': 0.15, 'GI': 0.15, 'GA': 0.15,
    'GL': 0.14, 'ZW': 0.14, 'OO': 0.14, 'MO': 0.14, 'JE': 0.14,
    'GO': 0.13, 'GU': 0.13, 'WU': 0.13, 'RI': 0.72,
    'SH': 0.03, 'HS': 0.08, 'FU': 0.12, 'FA': 0.12,
    'FR': 0.12, 'FL': 0.09, 'FI': 0.10, 'KR': 0.10,
    'KI': 0.09, 'KL': 0.08, 'KU': 0.08, 'ZA': 0.07,
    'PR': 0.07, 'PL': 0.06, 'PI': 0.05, 'PA': 0.08,
    'PO': 0.04, 'PU': 0.03, 'VA': 0.04, 'VI': 0.06,
}

german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
}

letter_freq = Counter()
for c, l in fixed.items():
    letter_freq[l] += pair_counts.get(c, 0)

print("=" * 70)
print("TIER 8b: REMAINING UNKNOWN ANALYSIS")
print("=" * 70)

# Get unknowns
unknown_codes = sorted(set(pair_counts.keys()) - set(fixed.keys()),
                       key=lambda c: -pair_counts.get(c, 0))

# For each unknown, get extended context (L2-L1-?-R1-R2)
print("\n=== EXTENDED CONTEXT FOR EACH UNKNOWN ===\n")

for code in unknown_codes:
    freq = pair_counts.get(code, 0)
    if freq < 3:
        continue

    left1 = Counter()
    right1 = Counter()
    left2 = Counter()
    right2 = Counter()
    trigrams_left = Counter()  # L1_?_R1
    trigrams_right = Counter()
    five_grams = Counter()

    for bpairs in book_pairs:
        for j, p in enumerate(bpairs):
            if p != code:
                continue
            # L1
            if j > 0 and bpairs[j-1] in fixed:
                l1 = fixed[bpairs[j-1]]
                left1[l1] += 1
                # L2
                if j > 1 and bpairs[j-2] in fixed:
                    left2[fixed[bpairs[j-2]] + l1] += 1
            # R1
            if j < len(bpairs)-1 and bpairs[j+1] in fixed:
                r1 = fixed[bpairs[j+1]]
                right1[r1] += 1
                # R2
                if j < len(bpairs)-2 and bpairs[j+2] in fixed:
                    right2[r1 + fixed[bpairs[j+2]]] += 1
            # Trigram: L1+?+R1
            if j > 0 and j < len(bpairs)-1:
                l = fixed.get(bpairs[j-1], '?')
                r = fixed.get(bpairs[j+1], '?')
                if l != '?' and r != '?':
                    trigrams_left[l + '_' + r] += 1

    # Score each candidate letter
    scores = {}
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        score = 0

        # Bigram scoring
        for left_letter, ct in left1.items():
            bg = left_letter + letter
            if bg in german_bigrams:
                score += ct * german_bigrams[bg]
            else:
                score -= ct * 0.05

        for right_letter, ct in right1.items():
            bg = letter + right_letter
            if bg in german_bigrams:
                score += ct * german_bigrams[bg]
            else:
                score -= ct * 0.05

        # Trigram context bonus
        for ctx, ct in trigrams_left.items():
            l, r = ctx.split('_')
            trigram = l + letter + r
            # Check if both constituent bigrams are strong
            bg1 = l + letter
            bg2 = letter + r
            s1 = german_bigrams.get(bg1, 0)
            s2 = german_bigrams.get(bg2, 0)
            if s1 > 0.5 and s2 > 0.5:
                score += ct * 0.5  # bonus for strong trigram

        # Frequency deficit/surplus penalty
        current_pct = letter_freq.get(letter, 0) / total_pairs
        expected_pct = german_freq.get(letter, 0)
        deficit = expected_pct - current_pct
        if deficit > 0:
            score += deficit * freq * 2  # bonus for filling deficit
        else:
            score += deficit * freq * 3  # stronger penalty for over-representing

        scores[letter] = score

    ranked = sorted(scores.items(), key=lambda x: -x[1])
    best = ranked[0]
    second = ranked[1]
    conf = best[1] / max(second[1], 0.01)

    # Determine confidence level
    if conf > 2.0:
        level = "STRONG"
    elif conf > 1.5:
        level = "GOOD"
    elif conf > 1.2:
        level = "MODERATE"
    else:
        level = "WEAK"

    print(f"Code {code} (freq={freq}) [{level}] conf={conf:.2f}")
    print(f"  L1: {dict(left1.most_common(6))}")
    print(f"  R1: {dict(right1.most_common(6))}")
    print(f"  L2: {dict(left2.most_common(5))}")
    print(f"  R2: {dict(right2.most_common(5))}")
    print(f"  Trigrams: {dict(trigrams_left.most_common(8))}")
    print(f"  Top 6: {', '.join(f'{l}:{s:.1f}' for l,s in ranked[:6])}")
    print()


# Word evidence for deficit letters
print("=" * 70)
print("WORD EVIDENCE (testing deficit letters against unknowns)")
print("=" * 70)

# Build full decoded text
full_text_pairs = []
for bpairs in book_pairs:
    full_text_pairs.extend(bpairs)

def test_word_at_code(word, target_code, target_pos):
    """Test if a word pattern occurs with target_code at target_pos."""
    count = 0
    for bpairs in book_pairs:
        for j in range(len(bpairs) - len(word) + 1):
            window = bpairs[j:j+len(word)]
            match = True
            for k in range(len(word)):
                if k == target_pos:
                    if window[k] != target_code:
                        match = False
                        break
                else:
                    if window[k] not in fixed or fixed[window[k]] != word[k]:
                        match = False
                        break
            if match:
                count += 1
    return count

# Test O words against all unknowns with freq>=3
print("\n--- O word tests ---")
o_words = ['NOCH', 'ODER', 'DORT', 'WORT', 'OFT', 'DOCH', 'HOCH',
           'VON', 'VOR', 'VOLL', 'GROSS', 'GOLD', 'SOHN', 'BODEN',
           'OBEN', 'FORT', 'BORN', 'WOLF', 'KOENIG', 'BOGEN']
for code in unknown_codes:
    if pair_counts.get(code, 0) < 3:
        continue
    hits = []
    for word in o_words:
        for pos in range(len(word)):
            if word[pos] == 'O':
                ct = test_word_at_code(word, code, pos)
                if ct > 0:
                    hits.append(f"{word}[{pos}]:{ct}")
    if hits:
        print(f"  {code} (freq={pair_counts[code]}): {', '.join(hits)}")

# Test K words
print("\n--- K word tests ---")
k_words = ['KANN', 'KEIN', 'KONNTE', 'KRAFT', 'KLAR', 'KLEIN',
           'KENNEN', 'KOENIG', 'KIRCHE', 'KUNST', 'KURZ',
           'KOMMEN', 'KRIEG', 'KNECHT']
for code in unknown_codes:
    if pair_counts.get(code, 0) < 3:
        continue
    hits = []
    for word in k_words:
        for pos in range(len(word)):
            if word[pos] == 'K':
                ct = test_word_at_code(word, code, pos)
                if ct > 0:
                    hits.append(f"{word}[{pos}]:{ct}")
    if hits:
        print(f"  {code} (freq={pair_counts[code]}): {', '.join(hits)}")

# Test Z words
print("\n--- Z word tests ---")
z_words = ['ZU', 'ZWISCHEN', 'ZEIT', 'ZUSAMMEN', 'ZURUECK',
           'ZEICHEN', 'ZUERST', 'ZWEI', 'ZWEIT', 'ZAHL',
           'ZWAR', 'ZUVOR', 'ZEIGEN']
for code in unknown_codes:
    if pair_counts.get(code, 0) < 3:
        continue
    hits = []
    for word in z_words:
        for pos in range(len(word)):
            if word[pos] == 'Z':
                ct = test_word_at_code(word, code, pos)
                if ct > 0:
                    hits.append(f"{word}[{pos}]:{ct}")
    if hits:
        print(f"  {code} (freq={pair_counts[code]}): {', '.join(hits)}")

# Test M words
print("\n--- M word tests ---")
m_words = ['MAN', 'MUSS', 'MUSSTE', 'MACHT', 'MIT', 'MEHR',
           'MENSCHEN', 'MANCHMAL', 'MEISTEN', 'MANCHEM',
           'IMMER', 'STIMME', 'STIMMEN', 'SUMME']
for code in unknown_codes:
    if pair_counts.get(code, 0) < 3:
        continue
    hits = []
    for word in m_words:
        for pos in range(len(word)):
            if word[pos] == 'M':
                ct = test_word_at_code(word, code, pos)
                if ct > 0:
                    hits.append(f"{word}[{pos}]:{ct}")
    if hits:
        print(f"  {code} (freq={pair_counts[code]}): {', '.join(hits)}")

# Test B words (need more B codes)
print("\n--- B word tests ---")
b_words = ['ABER', 'BIS', 'BUCH', 'BERG', 'BALD', 'BAND',
           'BEIDE', 'BRAUCH', 'BESCHRIEBEN', 'BESTIMMT',
           'BESONDER', 'BENUTZT', 'BEDEUT', 'BLEIB', 'BLUT',
           'BREIT', 'BRUDER', 'BRINGEN', 'BRAUCHT']
for code in unknown_codes:
    if pair_counts.get(code, 0) < 3:
        continue
    hits = []
    for word in b_words:
        for pos in range(len(word)):
            if word[pos] == 'B':
                ct = test_word_at_code(word, code, pos)
                if ct > 0:
                    hits.append(f"{word}[{pos}]:{ct}")
    if hits:
        print(f"  {code} (freq={pair_counts[code]}): {', '.join(hits)}")

# Test F words (need more F codes)
print("\n--- F word tests ---")
f_words = ['FUER', 'FINDEN', 'FORT', 'FRUEH', 'FREUND',
           'FRIEDE', 'FOLGE', 'FORMEN', 'FEST', 'FERN',
           'FEUER', 'FLUCHT', 'FUEHRT', 'FUENF']
for code in unknown_codes:
    if pair_counts.get(code, 0) < 3:
        continue
    hits = []
    for word in f_words:
        for pos in range(len(word)):
            if word[pos] == 'F':
                ct = test_word_at_code(word, code, pos)
                if ct > 0:
                    hits.append(f"{word}[{pos}]:{ct}")
    if hits:
        print(f"  {code} (freq={pair_counts[code]}): {', '.join(hits)}")

# Test P words
print("\n--- P word tests ---")
p_words = ['PLATZ', 'PLATTE', 'PLATTFORM', 'PFAD', 'PFLICHT',
           'PUNKT', 'PRACHT', 'PREIS']
for code in unknown_codes:
    if pair_counts.get(code, 0) < 3:
        continue
    hits = []
    for word in p_words:
        for pos in range(len(word)):
            if word[pos] == 'P':
                ct = test_word_at_code(word, code, pos)
                if ct > 0:
                    hits.append(f"{word}[{pos}]:{ct}")
    if hits:
        print(f"  {code} (freq={pair_counts[code]}): {', '.join(hits)}")

# Test V words
print("\n--- V word tests ---")
v_words = ['VON', 'VIEL', 'VIELE', 'VOLK', 'VERSCHIEDE',
           'VERSTEH', 'VERGESS', 'VERSUCH', 'VOR']
for code in unknown_codes:
    if pair_counts.get(code, 0) < 3:
        continue
    hits = []
    for word in v_words:
        for pos in range(len(word)):
            if word[pos] == 'V':
                ct = test_word_at_code(word, code, pos)
                if ct > 0:
                    hits.append(f"{word}[{pos}]:{ct}")
    if hits:
        print(f"  {code} (freq={pair_counts[code]}): {', '.join(hits)}")


# Special: code 82 = likely I or U (D_E/T context)
# Test patterns
print("\n" + "=" * 70)
print("SPECIAL PATTERN TESTS")
print("=" * 70)

# Code 82: D[82]E dominant. Test DIE vs DUE
print("\n--- Code 82: DIE/DUE/DOE test ---")
for letter in ['I', 'U', 'O', 'E', 'A']:
    ct_die = test_word_at_code('D' + letter + 'E', '82', 1)
    ct_dis = test_word_at_code('D' + letter + 'S', '82', 1) if letter != 'S' else 0
    ct_dir = test_word_at_code('D' + letter + 'R', '82', 1)
    if ct_die + ct_dis + ct_dir > 0:
        print(f"  {letter}: D{letter}E={ct_die}, D{letter}S={ct_dis}, D{letter}R={ct_dir}")

# Code 73: E_N/D dominant. Test patterns
print("\n--- Code 73: E_N, E_D, L_N patterns ---")
for letter in ['I', 'N', 'S', 'R', 'L', 'U', 'A']:
    ct1 = test_word_at_code('E' + letter + 'N', '73', 1)
    ct2 = test_word_at_code('E' + letter + 'D', '73', 1)
    ct3 = test_word_at_code('L' + letter + 'N', '73', 1)
    if ct1 + ct2 + ct3 > 0:
        print(f"  {letter}: E{letter}N={ct1}, E{letter}D={ct2}, L{letter}N={ct3}")

# Code 54: U_N dominant. Test UN vs UGN, etc.
print("\n--- Code 54: U_N, A_N, _E, _R patterns ---")
for letter in ['N', 'G', 'S', 'R', 'L', 'B', 'F']:
    ct1 = test_word_at_code('U' + letter + 'N', '54', 1)
    ct2 = test_word_at_code('A' + letter + 'N', '54', 1)
    ct3 = test_word_at_code('E' + letter + 'N', '54', 1)
    if ct1 + ct2 + ct3 > 0:
        print(f"  {letter}: U{letter}N={ct1}, A{letter}N={ct2}, E{letter}N={ct3}")

# Code 24: E_L and E_A dominant
print("\n--- Code 24: E_L, E_A, W_L patterns ---")
for letter in ['L', 'A', 'I', 'N', 'R', 'H', 'S', 'O', 'K', 'B', 'F', 'M', 'T']:
    ct1 = test_word_at_code('E' + letter + 'L', '24', 1)
    ct2 = test_word_at_code('E' + letter + 'A', '24', 1)
    ct3 = test_word_at_code('W' + letter + 'L', '24', 1)
    ct4 = test_word_at_code('E' + letter + 'T', '24', 1)
    if ct1 + ct2 + ct3 + ct4 > 0:
        print(f"  {letter}: E{letter}L={ct1}, E{letter}A={ct2}, W{letter}L={ct3}, E{letter}T={ct4}")

# Code 84: L_L, B_L dominant, L_T also
print("\n--- Code 84: L_L, B_L, L_T, L_A patterns ---")
for letter in ['A', 'E', 'I', 'O', 'U', 'K']:
    ct1 = test_word_at_code('L' + letter + 'L', '84', 1)
    ct2 = test_word_at_code('B' + letter + 'L', '84', 1)
    ct3 = test_word_at_code('L' + letter + 'T', '84', 1)
    ct4 = test_word_at_code('L' + letter + 'A', '84', 1)
    if ct1 + ct2 + ct3 + ct4 > 0:
        print(f"  {letter}: L{letter}L={ct1}, B{letter}L={ct2}, L{letter}T={ct3}, L{letter}A={ct4}")


# Over-representation analysis: check if any current assignments are wrong
print("\n" + "=" * 70)
print("OVER-REPRESENTATION CHECK")
print("=" * 70)

print("\nLetters with excess > 1%:")
for l in sorted(german_freq, key=lambda x: -(letter_freq.get(x,0)/total_pairs - german_freq[x])):
    obs = letter_freq.get(l, 0) / total_pairs * 100
    exp = german_freq[l] * 100
    excess = obs - exp
    if excess > 1.0:
        codes = [c for c, v in fixed.items() if v == l]
        codes_str = ', '.join(f"{c}({pair_counts.get(c,0)})" for c in sorted(codes, key=lambda c: -pair_counts.get(c,0)))
        print(f"  {l}: obs={obs:.1f}% exp={exp:.1f}% excess={excess:+.1f}%")
        print(f"    Codes: {codes_str}")


# Specific word pattern test for each major unknown
print("\n" + "=" * 70)
print("DECODED CONTEXT WINDOWS")
print("=" * 70)

for code in unknown_codes:
    freq = pair_counts.get(code, 0)
    if freq < 6:
        continue

    print(f"\n--- Code {code} (freq={freq}) in context: ---")
    shown = 0
    for bi, bpairs in enumerate(book_pairs):
        for j, p in enumerate(bpairs):
            if p != code:
                continue
            # Get context window: 4 codes on each side
            start = max(0, j - 4)
            end = min(len(bpairs), j + 5)
            ctx = []
            for k in range(start, end):
                if k == j:
                    ctx.append(f'[{bpairs[k]}]')
                elif bpairs[k] in fixed:
                    ctx.append(fixed[bpairs[k]])
                else:
                    ctx.append(f'({bpairs[k]})')

            print(f"  {''.join(ctx)}")
            shown += 1
            if shown >= 10:
                break
        if shown >= 10:
            break
    if shown < freq:
        print(f"  ... ({freq - shown} more)")


print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
