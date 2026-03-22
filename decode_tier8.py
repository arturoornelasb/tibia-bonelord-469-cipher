"""
Tier 8: Systematic analysis of remaining 27 unknown codes.
Focus on B, O, M, K, Z deficits + high-frequency unknowns.
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

# All 71 tier 7b codes
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

# Decode text
full_text = ''
for bpairs in book_pairs:
    full_text += ''.join(fixed.get(p, '?') for p in bpairs)

# German bigram frequencies
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
    'OB': 0.27, 'KO': 0.26, 'LS': 0.26, 'WO': 0.25, 'HL': 0.25,
    'BL': 0.24, 'LO': 0.24, 'VE': 0.24, 'VI': 0.23, 'EF': 0.23,
    'AUS': 0.22, 'NA': 0.22, 'BU': 0.22, 'EB': 0.21,
}

german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
}

# Current letter counts
letter_counts = Counter()
for c, l in fixed.items():
    letter_counts[l] += pair_counts.get(c, 0)

print("=" * 70)
print("TIER 8: DEEP ANALYSIS OF 27 REMAINING CODES")
print("=" * 70)

# Get all unknown codes with full context
unknown_codes = sorted(set(pair_counts.keys()) - set(fixed.keys()),
                       key=lambda c: -pair_counts.get(c, 0))

# For each unknown, get FULL neighbor profile + trigram context
print(f"\n{'='*70}")
print("DETAILED PROFILES")
print("=" * 70)

for code in unknown_codes:
    freq = pair_counts.get(code, 0)
    if freq < 3:
        continue

    left = Counter()
    right = Counter()
    left_pair = Counter()  # two codes to the left
    right_pair = Counter()  # two codes to the right
    contexts = []

    for bpairs in book_pairs:
        for j, p in enumerate(bpairs):
            if p != code: continue
            if j > 0 and bpairs[j-1] in fixed:
                left[fixed[bpairs[j-1]]] += 1
            if j < len(bpairs)-1 and bpairs[j+1] in fixed:
                right[fixed[bpairs[j+1]]] += 1
            # Trigram context: L2-L1-?-R1-R2
            l2 = fixed.get(bpairs[j-2], '?') if j >= 2 else '^'
            l1 = fixed.get(bpairs[j-1], '?') if j >= 1 else '^'
            r1 = fixed.get(bpairs[j+1], '?') if j < len(bpairs)-1 else '$'
            r2 = fixed.get(bpairs[j+2], '?') if j < len(bpairs)-2 else '$'
            ctx = f"{l2}{l1}_{r1}{r2}"
            contexts.append(ctx)

    # Score each candidate letter
    candidates = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    scores = {}
    for letter in candidates:
        score = 0
        for ll, ct in left.items():
            bg = ll + letter
            if bg in german_bigrams:
                score += ct * german_bigrams[bg]
            else:
                score -= ct * 0.05
        for rl, ct in right.items():
            bg = letter + rl
            if bg in german_bigrams:
                score += ct * german_bigrams[bg]
            else:
                score -= ct * 0.05

        # Frequency deficit bonus
        current_pct = letter_counts.get(letter, 0) / total_pairs
        expected_pct = german_freq.get(letter, 0)
        deficit = expected_pct - current_pct
        if deficit > 0:
            score += deficit * 50 * freq / total_pairs * 50

        scores[letter] = score

    ranked = sorted(scores.items(), key=lambda x: -x[1])[:8]
    best = ranked[0]
    second = ranked[1]
    conf = best[1] / max(second[1], 0.01)

    # Top 5 trigram contexts
    ctx_counter = Counter(contexts)
    top_ctx = ctx_counter.most_common(8)

    print(f"\n  Code {code} (freq={freq}) conf={conf:.2f}")
    print(f"    L={dict(left.most_common(6))}")
    print(f"    R={dict(right.most_common(6))}")
    print(f"    Top: {', '.join(f'{l}:{s:.1f}' for l,s in ranked[:5])}")
    print(f"    Contexts: {', '.join(f'{c}:{n}' for c,n in top_ctx)}")


# Now do targeted word evidence for the top unknowns
print(f"\n{'='*70}")
print("WORD EVIDENCE (targeted)")
print("=" * 70)

def test_word_at(word, target_code, target_pos):
    """Count occurrences of word with target_code at target_pos."""
    count = 0
    for bpairs in book_pairs:
        for j in range(len(bpairs) - len(word) + 1):
            window = bpairs[j:j+len(word)]
            match = True
            for k in range(len(word)):
                if k == target_pos:
                    if window[k] != target_code:
                        match = False; break
                else:
                    if window[k] not in fixed or fixed[window[k]] != word[k]:
                        match = False; break
            if match:
                count += 1
    return count

# Test specific words for deficit letters
word_tests = {
    'O': ['ODER', 'NOCH', 'DORT', 'WORT', 'VOLK', 'GOLD', 'SOHN', 'FORT',
          'OFT', 'HOCH', 'DOCH', 'SOLCH', 'WELCH', 'OBEN', 'VON', 'VOR',
          'GROSSE', 'GROSS', 'GOTT', 'BODEN', 'OFFEN', 'TODE', 'TOTEN'],
    'B': ['ABER', 'HABEN', 'GEBEN', 'LEBEN', 'OBEN', 'NEBEN', 'BUCH',
          'BERG', 'BALD', 'BAND', 'BESCHRIEBEN', 'BRAUCH', 'BIS',
          'BEIDE', 'BEREITS', 'BESSER', 'BRINGEN', 'BRAUCHEN'],
    'K': ['KANN', 'KONNTE', 'KRAFT', 'KENNEN', 'KEIN', 'KEINE', 'KEINEN',
          'KOENNEN', 'KURZ', 'KLAR', 'KLEIN'],
    'Z': ['ZU', 'ZWISCHEN', 'ZEIT', 'ZURÜCK', 'ZEICHEN', 'ZWEI',
          'ZURUECK', 'ZUSAMMEN', 'ZULETZT', 'ZUVOR'],
    'M': ['MACHT', 'MEHR', 'MUSS', 'MUSSTE', 'MANN', 'MENSCHEN',
          'MUESSEN', 'MACHEN', 'MANCHE', 'MORGEN'],
    'P': ['PLATZ', 'PUNKT', 'PFAD', 'PREIS'],
    'V': ['VON', 'VOR', 'VIEL', 'VIELE', 'VIELLEICHT', 'VERSCHIEDENE',
          'VERGESSEN', 'VERSTEHEN', 'VERSUCHEN'],
}

for target_letter, words in word_tests.items():
    print(f"\n  --- {target_letter} words ---")
    for code in unknown_codes:
        freq = pair_counts.get(code, 0)
        if freq < 3: continue
        hits = []
        for word in words:
            for pos in range(len(word)):
                if word[pos] == target_letter:
                    ct = test_word_at(word, code, pos)
                    if ct > 0:
                        hits.append(f"{word}[{pos}]:{ct}")
        if hits:
            total = sum(int(h.split(':')[1]) for h in hits)
            print(f"    {code}(f={freq}): {total} [{', '.join(hits)}]")


# Special: test code 66 as A (DAS pattern)
print(f"\n{'='*70}")
print("SPECIAL TESTS")
print("=" * 70)

# Code 66: L={D:9}, R={S:10} -> DAS?
print("\n  Code 66 (freq=10): D_S pattern")
for letter in 'AEIOU':
    word = f"D{letter}S"
    ct = 0
    for bpairs in book_pairs:
        for j in range(len(bpairs) - 2):
            if (bpairs[j] in fixed and fixed[bpairs[j]] == 'D' and
                bpairs[j+1] == '66' and
                bpairs[j+2] in fixed and fixed[bpairs[j+2]] == 'S'):
                ct += 1
    if ct > 0:
        print(f"    {word}: {ct}")

# Code 23: R={T:11} (100%) -> ?T always
print("\n  Code 23 (freq=11): always followed by T")
for letter in 'AEIOSHCNR':
    ct_bg = 0
    for bpairs in book_pairs:
        for j in range(len(bpairs) - 1):
            if bpairs[j] == '23' and bpairs[j+1] in fixed and fixed[bpairs[j+1]] == 'T':
                if j > 0 and bpairs[j-1] in fixed:
                    pass  # already counted in left
                ct_bg += 1
    # Check left context for this letter
    left_23 = Counter()
    for bpairs in book_pairs:
        for j, p in enumerate(bpairs):
            if p == '23' and j > 0 and bpairs[j-1] in fixed:
                left_23[fixed[bpairs[j-1]]] += 1
    if letter == 'A':
        print(f"    Left of 23: {dict(left_23.most_common(8))}")
    # Test specific _T bigrams
    bg = letter + 'T'
    if bg in german_bigrams:
        print(f"    {bg}: german={german_bigrams[bg]}")

# Code 74: L={H:11}, R={D:11} -> H?D
print("\n  Code 74 (freq=19): H_D pattern")
for letter in 'AEIOUN':
    bg_l = 'H' + letter
    bg_r = letter + 'D'
    l_score = german_bigrams.get(bg_l, 0)
    r_score = german_bigrams.get(bg_r, 0)
    if l_score > 0 or r_score > 0:
        print(f"    H{letter}D: H{letter}={l_score:.2f} {letter}D={r_score:.2f} sum={l_score+r_score:.2f}")

# Code 50: L={M:11, U:7, A:4}, R={D:11} -> M?D / U?D / A?D
print("\n  Code 50 (freq=35): M/U/A on left, D on right")
for letter in 'AEIOUN':
    total_score = 0
    for ll, ct in [('M', 11), ('U', 7), ('A', 4)]:
        bg = ll + letter
        total_score += ct * german_bigrams.get(bg, 0)
    bg_r = letter + 'D'
    total_score += 11 * german_bigrams.get(bg_r, 0)
    if total_score > 0:
        print(f"    {letter}: score={total_score:.1f} (M{letter}+U{letter}+A{letter}+{letter}D)")

# Code 83: R={M:14} dominant -> ?M
print("\n  Code 83 (freq=28): dominant M on right, E/T on left")
for letter in 'AEIOUN':
    bg_r = letter + 'M'
    bg_le = 'E' + letter
    bg_lt = 'T' + letter
    r_score = 14 * german_bigrams.get(bg_r, 0)
    le_score = 12 * german_bigrams.get(bg_le, 0)
    lt_score = 6 * german_bigrams.get(bg_lt, 0)
    total = r_score + le_score + lt_score
    if total > 0:
        print(f"    {letter}: {letter}M={german_bigrams.get(bg_r,0):.2f}*14={r_score:.1f} E{letter}={le_score:.1f} T{letter}={lt_score:.1f} total={total:.1f}")


# NICHT investigation
print(f"\n{'='*70}")
print("NICHT INVESTIGATION")
print("=" * 70)

# Find all N-I-C-H-T sequences where any position could be unknown
n_codes = [c for c, l in fixed.items() if l == 'N']
i_codes = [c for c, l in fixed.items() if l == 'I']
c_codes = [c for c, l in fixed.items() if l == 'C']
h_codes = [c for c, l in fixed.items() if l == 'H']
t_codes = [c for c, l in fixed.items() if l == 'T']

print(f"  N codes ({len(n_codes)}): {n_codes}")
print(f"  I codes ({len(i_codes)}): {i_codes}")
print(f"  C codes ({len(c_codes)}): {c_codes}")
print(f"  H codes ({len(h_codes)}): {h_codes}")
print(f"  T codes ({len(t_codes)}): {t_codes}")

# Search for NICH? and ?ICHT patterns
print("\n  Searching for near-NICHT patterns:")
for bpairs in book_pairs:
    for j in range(len(bpairs) - 4):
        window = bpairs[j:j+5]
        decoded = [fixed.get(p, f'[{p}]') for p in window]
        text = ''.join(d if len(d) == 1 else '?' for d in decoded)
        if text in ('NICH?', '?ICHT', 'NIC?T', 'NI?HT', 'N?CHT'):
            raw = '-'.join(window)
            full = ''.join(decoded)
            print(f"    {text} -> {full} (codes: {raw})")

# Also search for partial matches: NI, ICH, CHT
print("\n  NI bigram codes:")
ni_count = 0
for bpairs in book_pairs:
    for j in range(len(bpairs) - 1):
        if (bpairs[j] in fixed and fixed[bpairs[j]] == 'N' and
            bpairs[j+1] in fixed and fixed[bpairs[j+1]] == 'I'):
            ni_count += 1
print(f"    NI count: {ni_count}")

print("  ICH trigram codes:")
ich_count = 0
for bpairs in book_pairs:
    for j in range(len(bpairs) - 2):
        if (bpairs[j] in fixed and fixed[bpairs[j]] == 'I' and
            bpairs[j+1] in fixed and fixed[bpairs[j+1]] == 'C' and
            bpairs[j+2] in fixed and fixed[bpairs[j+2]] == 'H'):
            ich_count += 1
print(f"    ICH count: {ich_count}")

print("  CHT trigram codes:")
cht_count = 0
for bpairs in book_pairs:
    for j in range(len(bpairs) - 2):
        if (bpairs[j] in fixed and fixed[bpairs[j]] == 'C' and
            bpairs[j+1] in fixed and fixed[bpairs[j+1]] == 'H' and
            bpairs[j+2] in fixed and fixed[bpairs[j+2]] == 'T'):
            cht_count += 1
print(f"    CHT count: {cht_count}")

# What follows ICH?
print("\n  After ICH:")
after_ich = Counter()
for bpairs in book_pairs:
    for j in range(len(bpairs) - 3):
        if (bpairs[j] in fixed and fixed[bpairs[j]] == 'I' and
            bpairs[j+1] in fixed and fixed[bpairs[j+1]] == 'C' and
            bpairs[j+2] in fixed and fixed[bpairs[j+2]] == 'H'):
            if bpairs[j+3] in fixed:
                after_ich[fixed[bpairs[j+3]]] += 1
            else:
                after_ich[f'[{bpairs[j+3]}]'] += 1
for ch, ct in after_ich.most_common(10):
    print(f"    ICH{ch}: {ct}")


print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
