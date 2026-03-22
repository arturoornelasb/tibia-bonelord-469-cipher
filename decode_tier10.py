"""
Tier 10: Analyze remaining 11 unknown codes (freq>=3) for assignment.
Focus on deficit letters: B(-1.6%), M(-1.5%), O(-1.3%), F(-1.3%), A(-1.1%).
Also check: some I/D codes might be misassigned.
"""
import json
from collections import Counter

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

all_codes = {
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
    '67': 'E', '27': 'E', '03': 'E', '09': 'E', '05': 'C', '53': 'N',
    '44': 'U', '62': 'B', '68': 'R',
    '23': 'S', '17': 'E', '29': 'E', '66': 'A', '49': 'E',
    '38': 'K', '77': 'Z',
    '22': 'K', '82': 'O', '73': 'N', '50': 'I', '84': 'G',
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

# German bigram frequencies (relative)
german_bigrams = {
    'EN': 3.88, 'ER': 3.75, 'CH': 2.75, 'DE': 2.00, 'EI': 1.88,
    'ND': 1.99, 'TE': 1.82, 'IN': 1.67, 'IE': 1.64, 'GE': 1.85,
    'NE': 1.45, 'ES': 1.52, 'SE': 1.46, 'UN': 1.48, 'ST': 1.41,
    'HE': 1.28, 'AN': 1.21, 'RE': 1.32, 'BE': 1.25, 'AU': 1.15,
    'NG': 1.09, 'EL': 1.00, 'IS': 0.95, 'DI': 0.98, 'IC': 0.87,
    'LE': 0.94, 'SC': 0.93, 'HI': 0.67, 'NS': 0.84, 'NI': 0.81,
    'AS': 0.72, 'AL': 0.73, 'DA': 0.73, 'SI': 0.72, 'RS': 0.70,
    'RN': 0.65, 'HA': 0.64, 'HT': 0.65, 'LI': 0.60, 'RI': 0.57,
    'IT': 0.63, 'TI': 0.68, 'SS': 0.62, 'MI': 0.53, 'ED': 0.56,
    'IG': 0.87, 'US': 0.52, 'EM': 0.54, 'WI': 0.50, 'TU': 0.43,
    'RD': 0.50, 'RA': 0.45, 'UE': 0.43, 'NN': 0.39, 'EE': 0.10,
    'MA': 0.45, 'ME': 0.45, 'AB': 0.42, 'AM': 0.40, 'IM': 0.46,
    'UM': 0.35, 'ET': 0.55, 'NT': 0.48, 'AT': 0.36, 'RT': 0.42,
    'AG': 0.38, 'WE': 0.48, 'WA': 0.35, 'AR': 0.38, 'OR': 0.33,
    'UF': 0.28, 'FI': 0.27, 'OL': 0.20, 'FE': 0.25, 'AF': 0.15,
    'OF': 0.14, 'EF': 0.18, 'IF': 0.10, 'FA': 0.18, 'FL': 0.10,
    'FR': 0.15, 'FU': 0.12, 'RF': 0.10,
    'OB': 0.07, 'BO': 0.08, 'BL': 0.10, 'BR': 0.12, 'BI': 0.10,
    'BU': 0.08, 'BA': 0.10, 'EB': 0.15, 'UB': 0.07,
    'KO': 0.15, 'KE': 0.18, 'KA': 0.12, 'EK': 0.05, 'NK': 0.05,
    'ZU': 0.25, 'ZE': 0.20, 'ZW': 0.10, 'AZ': 0.03, 'TZ': 0.10,
    'II': 0.01, 'DD': 0.01, 'HH': 0.01,
    'OE': 0.20, 'ON': 0.30, 'NO': 0.20, 'OT': 0.15, 'TO': 0.25,
    'SO': 0.25, 'OS': 0.10, 'DO': 0.15, 'OD': 0.10, 'RO': 0.20,
    'OG': 0.08, 'GO': 0.08, 'VO': 0.20, 'OC': 0.05,
    'MU': 0.15, 'MO': 0.12, 'MM': 0.10, 'MN': 0.02, 'NM': 0.04,
    'OM': 0.10, 'PM': 0.01, 'MP': 0.05,
    'VE': 0.25, 'VI': 0.10, 'VA': 0.05, 'VO': 0.20, 'VOR': 0.10,
    'PF': 0.03, 'PR': 0.05, 'PL': 0.03, 'SP': 0.15, 'OP': 0.05,
}

# For each unknown code, score all candidate letters
unknown_codes = ['24', '81', '83', '74', '54', '25', '10', '37', '40', '02', '98']

german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007,
}

letter_freq = Counter()
for c, l in all_codes.items():
    letter_freq[l] += pair_counts.get(c, 0)

# Compute current surplus/deficit
surplus = {}
for l, exp in german_freq.items():
    obs = letter_freq.get(l, 0) / total_pairs
    surplus[l] = obs - exp  # positive = over-represented

print("=" * 70)
print("TIER 10: REMAINING UNKNOWN CODE ANALYSIS")
print("=" * 70)

for code in unknown_codes:
    freq = pair_counts.get(code, 0)

    # Get extended context: L2-L1-?-R1-R2
    left = Counter()
    right = Counter()
    left2 = Counter()
    right2 = Counter()
    contexts = []

    for bpairs in book_pairs:
        for j, p in enumerate(bpairs):
            if p != code: continue
            if j > 0 and bpairs[j-1] in all_codes:
                left[all_codes[bpairs[j-1]]] += 1
            if j > 1 and bpairs[j-2] in all_codes and bpairs[j-1] in all_codes:
                left2[all_codes[bpairs[j-2]] + all_codes[bpairs[j-1]]] += 1
            if j < len(bpairs)-1 and bpairs[j+1] in all_codes:
                right[all_codes[bpairs[j+1]]] += 1
            if j < len(bpairs)-2 and bpairs[j+1] in all_codes and bpairs[j+2] in all_codes:
                right2[all_codes[bpairs[j+1]] + all_codes[bpairs[j+2]]] += 1

            # Context window
            start = max(0, j-3)
            end = min(len(bpairs), j+4)
            window = bpairs[start:end]
            ctx = ''.join(all_codes.get(pp, f'[{pp}]') for pp in window)
            contexts.append(ctx)

    print(f"\n{'='*50}")
    print(f"CODE {code} (freq={freq})")
    print(f"{'='*50}")
    print(f"  Left:  {dict(left.most_common(8))}")
    print(f"  Right: {dict(right.most_common(8))}")
    print(f"  L2: {dict(left2.most_common(5))}")
    print(f"  R2: {dict(right2.most_common(5))}")

    # Score each candidate letter
    scores = {}
    for letter in 'ABCDEFGHIKLMNOPRSTUVWZ':
        score = 0
        for l_char, l_count in left.items():
            bg = l_char + letter
            score += l_count * german_bigrams.get(bg, 0.01)
        for r_char, r_count in right.items():
            bg = letter + r_char
            score += r_count * german_bigrams.get(bg, 0.01)

        # Frequency adjustment: bonus for deficit letters, penalty for surplus
        freq_adj = -surplus.get(letter, 0) * 100  # +bonus for deficit, -penalty for surplus
        adjusted = score + freq_adj * 0.5
        scores[letter] = (score, adjusted, freq_adj)

    # Sort by adjusted score
    ranked = sorted(scores.items(), key=lambda x: -x[1][1])
    best_raw = max(scores.items(), key=lambda x: x[1][0])

    print(f"\n  Top candidates (raw bigram | freq-adjusted):")
    for letter, (raw, adj, fadj) in ranked[:8]:
        marker = " <-- deficit" if surplus.get(letter, 0) < -0.005 else ""
        marker2 = " <-- surplus" if surplus.get(letter, 0) > 0.01 else ""
        print(f"    {letter}: raw={raw:.1f}, adj={adj:.1f} (freq_adj={fadj:+.1f}){marker}{marker2}")

    # Confidence ratio
    if len(ranked) >= 2:
        conf = ranked[0][1][1] / ranked[1][1][1] if ranked[1][1][1] > 0 else 99
        print(f"  Confidence: {conf:.2f} ({ranked[0][0]} vs {ranked[1][0]})")

    # Show contexts
    print(f"\n  Contexts (first 8):")
    for ctx in contexts[:8]:
        print(f"    {ctx}")

# Word tests for deficit letters
print(f"\n\n{'='*70}")
print("WORD TESTS FOR DEFICIT LETTERS")
print("=" * 70)

# Decode with each unknown as each deficit letter and count words
deficit_letters = ['O', 'M', 'B', 'F', 'A', 'P', 'V']
test_words = {
    'O': ['ORT', 'ORTE', 'DORT', 'ODER', 'OBEN', 'GOLD', 'VOLK', 'SOHN',
          'NOCH', 'DOCH', 'HOCH', 'KOMMEN', 'WOLLEN', 'SOLLEN', 'VON', 'VOR',
          'WORDEN', 'KOENIG', 'OFT', 'SO', 'ALSO', 'SCHON'],
    'M': ['IMMER', 'MACHEN', 'MACHT', 'MANN', 'MAN', 'MUESSEN', 'MUSSTE',
          'HEIM', 'GEHEIM', 'GEHEIMNIS', 'KOMMEN', 'NEHMEN', 'STIMME',
          'AMEN', 'FLAMME', 'ZUSAMMEN', 'NAME', 'NAMEN', 'STAMM'],
    'B': ['ABER', 'OBEN', 'NEBEN', 'HABEN', 'GEBEN', 'LEBEN', 'BIS',
          'BUCH', 'BERG', 'BALD', 'BRAUCH', 'BESCHRIEBEN', 'BEREITS',
          'BEIDE', 'BLUT', 'BRUDER', 'GEBIET', 'HERB'],
    'F': ['FUER', 'FUEHREN', 'FALLEN', 'FRAGEN', 'FRUEH',
          'SCHAFFEN', 'TREFFEN', 'HOFFEN', 'RUFEN', 'LAUFEN',
          'WAFFEN', 'HELFEN', 'AUFFINDEN'],
    'A': ['ANDERE', 'ANDERER', 'ABER', 'AUCH', 'AUS', 'AUF', 'WAHR',
          'ANTWORT', 'ALTER', 'ANFANG', 'ARBEIT'],
    'P': ['PLATZ', 'PUNKT', 'PERSON', 'OPFER', 'KOERPER',
          'SPRECHEN', 'BEISPIEL'],
    'V': ['VIEL', 'VIELE', 'VIELLEICHT', 'VOLK', 'VOELKER', 'VERSTEHEN',
          'VERSUCH', 'VERGESSEN', 'VERLOREN', 'VERSCHIEDEN'],
}

for code in unknown_codes:
    freq = pair_counts.get(code, 0)
    if freq < 5: continue

    print(f"\n  Code {code} (freq={freq}):")
    for letter in deficit_letters:
        test_codes = {**all_codes, code: letter}
        test_text = ''
        for bpairs in book_pairs:
            test_text += ''.join(test_codes.get(p, '?') for p in bpairs)

        hits = []
        for w in test_words.get(letter, []):
            ct = test_text.count(w)
            if ct > 0:
                hits.append(f"{w}:{ct}")
        if hits:
            print(f"    {letter}: {', '.join(hits)}")

# Special analysis: code 83 right->M dominance
print(f"\n\n{'='*70}")
print("SPECIAL: CODE 83 TRIGRAM ANALYSIS (right->M dominant)")
print("=" * 70)

for bpairs in book_pairs:
    for j, p in enumerate(bpairs):
        if p != '83': continue
        # Get L2-L1-83-R1-R2-R3
        start = max(0, j-3)
        end = min(len(bpairs), j+4)
        window = bpairs[start:end]
        ctx = ''.join(all_codes.get(pp, f'[{pp}]') for pp in window)
        # What letter at 83 makes sense?
        for candidate in ['O', 'M', 'B', 'V', 'E', 'I']:
            test = ctx.replace(f'[{p}]', candidate)
            # Check if any known words appear
            for w in ['IMMER', 'OMMER', 'HIMMEL', 'STIMME', 'KOMM', 'AMM',
                      'GEHEIM', 'HEIM', 'KOMMEN', 'ZUSAMM', 'VIEL', 'BIER',
                       'OMI', 'OMA', 'BOMM', 'FLAMM']:
                if w in test:
                    print(f"  {ctx} -> {candidate}: {test} (found {w})")

print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
