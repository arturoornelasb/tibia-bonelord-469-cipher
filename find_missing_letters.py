"""
Targeted search for T, R, G, O, B, F, K, Z codes.
These letters are severely underrepresented in the current 52-code mapping.
Uses word-pattern matching with 2+ unknowns and trigram analysis.
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

# 52 fixed codes
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
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

all_pairs_flat = []
for pairs in book_pairs:
    all_pairs_flat.extend(pairs)
pair_counts = Counter(all_pairs_flat)
total_pairs = len(all_pairs_flat)

unknown_codes = sorted(
    [c for c in pair_counts if c not in fixed],
    key=lambda c: -pair_counts[c]
)

print("=" * 70)
print("TARGETED SEARCH FOR MISSING LETTERS: T, R, G, O, B, F, K, Z")
print("=" * 70)
print(f"\n46 unknown codes by frequency:")
for c in unknown_codes:
    print(f"  {c}: {pair_counts[c]} ({pair_counts[c]/total_pairs*100:.1f}%)")

# STRATEGY 1: German trigram patterns with 1 unknown
# Focus on trigrams containing T, R, G, O, B, F, K, Z
print(f"\n{'='*70}")
print("STRATEGY 1: TRIGRAM PATTERNS (3 codes, 1 unknown)")
print("=" * 70)

# Common German trigrams containing our target letters
target_trigrams = {
    # T-containing (T is position we need to find)
    'T': [
        ('T', 'E', 'R'),  # TER - very common
        ('E', 'T', None),  # E?  with T in middle (covered by words)
        ('I', 'C', 'H'),  # not T but...
    ],
}

# Better approach: for each unknown code, check what KNOWN trigrams it participates in
print("\nFor each unknown code, check trigram contexts with 2 known neighbors:")
evidence = defaultdict(lambda: defaultdict(int))

for pairs in book_pairs:
    for i in range(1, len(pairs) - 1):
        code = pairs[i]
        if code in fixed:
            continue
        left = pairs[i-1]
        right = pairs[i+1]
        if left in fixed and right in fixed:
            trigram_context = (fixed[left], '?', fixed[right])
            evidence[code][trigram_context] += 1

# German trigram expectations
german_trigrams_by_middle = {
    # (left, right) -> expected middle letter
    ('E', 'N'): {'I': 3.0, 'E': 1.0, 'D': 1.0},  # EIN, EEN, EDN
    ('S', 'E'): {'I': 2.0, 'S': 1.0, 'H': 1.0},  # SIE, SSE, SHE
    ('N', 'E'): {'I': 2.0, 'D': 1.0},  # NIE, NDE
    ('E', 'E'): {'I': 1.0, 'S': 1.0, 'R': 1.0},  # EIE, ESE, ERE
    ('I', 'H'): {'C': 3.0},  # ICH (very common)
    ('S', 'H'): {'C': 3.0},  # SCH (very common)
    ('A', 'H'): {'C': 2.0},  # ACH
    ('U', 'H'): {'C': 2.0, 'R': 1.0},  # UCH, URH (DURCH)
    ('I', 'T'): {'C': 2.0, 'S': 1.0, 'N': 1.0, 'E': 0.5},  # ICT→ICHT, IST, INT
    ('E', 'H'): {'C': 1.0, 'I': 1.0},  # ECH, EIH
    ('E', 'T'): {'I': 1.0, 'S': 1.0, 'H': 0.5, 'R': 0.5, 'N': 0.5},  # EIT, EST, EHT
    ('E', 'D'): {'I': 1.0, 'N': 1.0, 'R': 0.5},  # EID, END, ERD
    ('N', 'C'): {'I': 1.0},  # NIC(HT)
    ('I', 'E'): {'N': 1.5, 'S': 1.0, 'E': 0.5, 'D': 0.5, 'L': 0.5},  # INE, ISE, IEE, IDE, ILE
    ('A', 'E'): {'L': 1.0, 'S': 0.5, 'G': 0.5, 'R': 0.5, 'T': 0.5},  # ALE, ASE, AGE, ARE, ATE
    ('D', 'E'): {'I': 1.5, 'R': 1.0, 'N': 0.5},  # DIE, DRE, DNE→ORDNEN
    ('E', 'S'): {'I': 1.0, 'A': 0.5, 'E': 0.5},  # EIS, EAS, EES
    ('I', 'D'): {'N': 2.0, 'E': 0.5},  # IND (SIND, WIND)
    ('U', 'D'): {'N': 3.0},  # UND
    ('E', 'I'): {'N': 1.0, 'S': 0.5, 'T': 0.5, 'L': 0.5},  # ENI, ESI, ETI, ELI
    ('H', 'N'): {'E': 1.0, 'I': 0.5},  # HEN, HIN
    ('S', 'A'): {'T': 0.5, 'G': 0.5},  # STA→STADT, SGA
    ('A', 'S'): {'U': 1.0, 'L': 0.5},  # AUS, ALS
    ('N', 'S'): {'C': 1.0, 'I': 0.5},  # NSC(HRIFT), NSI
    ('H', 'I'): {'E': 1.0},  # HEI(SST)
    ('S', 'I'): {'E': 1.0, 'N': 0.5},  # SIE, SIN(D)
    ('H', 'E'): {'I': 1.0, 'R': 0.5},  # HIE, HRE→SCHREIBEN
}

# Score each unknown code
print(f"\nUnknown code scoring based on trigram contexts:")
for code in unknown_codes[:30]:
    trigram_data = evidence[code]
    if not trigram_data:
        continue

    letter_scores = defaultdict(float)
    total_occ = sum(trigram_data.values())

    for (left, _, right), count in sorted(trigram_data.items(), key=lambda x: -x[1]):
        key = (left, right)
        if key in german_trigrams_by_middle:
            for letter, weight in german_trigrams_by_middle[key].items():
                letter_scores[letter] += weight * count

    if letter_scores:
        top = sorted(letter_scores.items(), key=lambda x: -x[1])[:5]
        freq = pair_counts[code]
        print(f"\n  Code {code} (freq={freq}):")
        # Show top 5 trigram contexts
        top_contexts = sorted(trigram_data.items(), key=lambda x: -x[1])[:6]
        for (l, _, r), ct in top_contexts:
            print(f"    {l}[{code}]{r}: {ct} times")
        print(f"    Trigram scores: {', '.join(f'{l}:{s:.1f}' for l, s in top)}")


# STRATEGY 2: Word patterns with focus on MISSING letters
print(f"\n{'='*70}")
print("STRATEGY 2: TARGETED WORD PATTERNS FOR T, R, G, O, B, F, K, Z")
print("=" * 70)

# Words containing our target letters in positions where they'd be the unknown
target_words = {
    'T': ['NICHT', 'HINTER', 'UNTER', 'MUTTER', 'VATER', 'WORT', 'DORT',
          'RECHT', 'NACHT', 'MACHT', 'KRAFT', 'SCHRIFT', 'HATTE', 'GEIST',
          'LETZT', 'ERSTE', 'TEIL', 'WEIT', 'ZEIT', 'SETZT', 'LIEST',
          'STEHT', 'BITTE', 'HAETTE', 'KONNTE', 'SOLLTE', 'MUSSTE',
          'LICHT', 'STEIN', 'ALTE', 'ALTEN', 'HINTER'],
    'R': ['RUNEN', 'ANDERE', 'ANDEREN', 'ANDERER', 'UNSERE', 'UNSERER',
          'MEISTER', 'BRUDER', 'FERNER', 'WAERE', 'WUERDEN', 'ERSTER',
          'UEBER', 'FREUND', 'FREUNDE', 'GROSS', 'GROSSEN', 'ERST',
          'DARAUF', 'DARUEBER', 'HERR', 'BERG', 'BURG', 'STARK',
          'DURCH', 'WERDEN', 'WIEDER', 'SPRACHE', 'SCHREIBEN'],
    'G': ['GEGEN', 'GROSS', 'GEIST', 'GEBEN', 'GIBT', 'GANZ', 'GOTT',
          'GUT', 'GESAGT', 'GELESEN', 'GESCHRIEBEN', 'GEHEIMNIS',
          'ZEIGEN', 'TRAGEN', 'FRAGEN', 'SAGEN', 'LIEGEN', 'BRINGEN',
          'LANG', 'DING', 'BURG', 'BERG', 'TAG', 'WEG', 'KLUG',
          'EWIG', 'EINIGE', 'WENIGE', 'RICHTIG'],
    'O': ['ODER', 'NOCH', 'WORT', 'VOLK', 'VON', 'GOTT', 'DORT',
          'SOLL', 'WOHL', 'GROSS', 'TOD', 'BODEN', 'OBEN', 'KOENNEN',
          'SOLLEN', 'WOLLEN', 'FORM', 'MOND', 'LOHN', 'GOLD',
          'KRONE', 'WORDEN', 'KONNTE', 'OFT', 'ORT'],
    'B': ['ABER', 'BEI', 'BIS', 'BUCH', 'BERG', 'BURG', 'BEIDE',
          'BITTE', 'BRINGEN', 'BRUDER', 'BODEN', 'BALD', 'BLEIBEN',
          'BRAUCHEN', 'BISHER', 'BISHER', 'HABEN', 'GEBEN', 'LEBEN',
          'LIEBEN', 'UEBEN', 'OBEN'],
    'F': ['FUER', 'FINDEN', 'FREUND', 'FREUNDE', 'FEUER', 'FEIND',
          'FERN', 'FEST', 'FRAGEN', 'FRUEH', 'FUEHREN', 'FALLEN',
          'FORM', 'FOLGEN', 'SCHRIFT', 'KRAFT', 'AUF', 'OFT', 'LAUF',
          'DARF', 'RUFEN', 'SCHAFFEN', 'HELFEN'],
    'K': ['KANN', 'KEIN', 'KEINE', 'KEINER', 'KLEIN', 'KLEINEN',
          'KONNTE', 'KOENNEN', 'KRAFT', 'KRONE', 'KLUG', 'KENNEN',
          'KOMMEN', 'DUNKEL', 'DENKEN', 'WIRKEN', 'STARK', 'STÜCK'],
    'Z': ['ZEIT', 'ZEICHEN', 'ZEIGEN', 'ZWISCHEN', 'ZUERST', 'ZURUECK',
          'ZUSAMMEN', 'ZUM', 'ZUR', 'ZWAR', 'ZWEI', 'KURZ', 'GANZ',
          'SATZ', 'PLATZ', 'SCHATZ', 'SCHUTZ'],
}

word_evidence = defaultdict(lambda: defaultdict(list))

for target_letter, words in target_words.items():
    for word in words:
        wlen = len(word)
        if wlen < 3 or wlen > 12:
            continue

        # Find positions where target_letter appears
        target_positions = [i for i in range(wlen) if word[i] == target_letter]

        for unk_pos in target_positions:
            known_letters = [(i, word[i]) for i in range(wlen) if i != unk_pos]

            for pairs in book_pairs:
                for start in range(len(pairs) - wlen + 1):
                    window = pairs[start:start + wlen]

                    match = True
                    for i, expected_letter in known_letters:
                        code = window[i]
                        if code not in fixed or fixed[code] != expected_letter:
                            match = False
                            break
                    if not match:
                        continue

                    unk_code = window[unk_pos]
                    if unk_code in fixed:
                        if fixed[unk_code] == target_letter:
                            continue  # Already confirmed
                        else:
                            continue  # Contradicts
                    word_evidence[unk_code][target_letter].append(word)

# Report
for code in unknown_codes[:40]:
    if code not in word_evidence:
        continue
    ev = word_evidence[code]
    if not ev:
        continue

    total_hits = sum(len(v) for v in ev.values())
    if total_hits < 2:
        continue

    freq = pair_counts[code]
    print(f"\n  Code {code} (freq={freq}):")
    for letter in sorted(ev, key=lambda l: -len(ev[l])):
        hits = len(ev[letter])
        unique_words = sorted(set(ev[letter]))
        if hits >= 2:
            print(f"    {letter}: {hits} hits from {unique_words[:8]}")


# STRATEGY 3: SCH trigram — find codes that complete S_H to SCH
print(f"\n{'='*70}")
print("STRATEGY 3: SCH TRIGRAM ANALYSIS")
print("=" * 70)

# We know S codes and H codes. Find what appears between them
s_codes = [c for c, l in fixed.items() if l == 'S']
h_codes = [c for c, l in fixed.items() if l == 'H']
c_codes = [c for c, l in fixed.items() if l == 'C']

print(f"S codes: {s_codes}")
print(f"C codes: {c_codes}")
print(f"H codes: {h_codes}")

# Find S_?_H patterns where ? could be C
sch_candidates = Counter()
for pairs in book_pairs:
    for i in range(len(pairs) - 2):
        if pairs[i] in fixed and fixed[pairs[i]] == 'S':
            if pairs[i+2] in fixed and fixed[pairs[i+2]] == 'H':
                middle = pairs[i+1]
                if middle not in fixed:
                    sch_candidates[middle] += 1
                elif fixed[middle] == 'C':
                    pass  # Already confirmed SCH

print(f"\nCodes appearing between S and H (S_?_H pattern):")
for code, count in sch_candidates.most_common(10):
    print(f"  {code}: {count} times (freq={pair_counts[code]})")


# STRATEGY 4: NICHT pattern — extremely common German word
print(f"\n{'='*70}")
print("STRATEGY 4: NICHT PATTERN (5 letters, 2 known: N, I, H already assigned)")
print("=" * 70)

# NICHT: N=known, I=known, C=known(18), H=known, T=known(78,88)
# But we need MORE T codes. Look for N_I_C_H_T where T position has an unknown
# Actually NICHT = N,I,C,H,T — all 5 letters have codes
# What we want: find patterns where NICHT appears with UNKNOWN codes for known letters
# This means: find 5-code windows where some codes are unknown but the pattern fits NICHT

# Better: find all occurrences where 4 of 5 positions match NICHT
# and the remaining position has an unknown code
n_codes_set = set(c for c, l in fixed.items() if l == 'N')
i_codes_set = set(c for c, l in fixed.items() if l == 'I')
c_codes_set = set(c for c, l in fixed.items() if l == 'C')
h_codes_set = set(c for c, l in fixed.items() if l == 'H')
t_codes_set = set(c for c, l in fixed.items() if l == 'T')

nicht_evidence = Counter()
for pairs in book_pairs:
    for i in range(len(pairs) - 4):
        window = pairs[i:i+5]
        # Count how many positions match NICHT
        matches = [
            window[0] in n_codes_set,
            window[1] in i_codes_set,
            window[2] in c_codes_set,
            window[3] in h_codes_set,
            window[4] in t_codes_set,
        ]
        n_matches = sum(matches)
        if n_matches == 4:
            # Exactly one unknown — which position?
            unk_pos = matches.index(False)
            unk_code = window[unk_pos]
            if unk_code not in fixed:
                target = 'NICHT'[unk_pos]
                nicht_evidence[(unk_code, target)] += 1

print("Codes that complete NICHT (4 of 5 positions confirmed):")
for (code, letter), count in nicht_evidence.most_common(20):
    if count >= 2:
        freq = pair_counts[code]
        print(f"  {code} = {letter}: {count} matches (freq={freq})")


# STRATEGY 5: Look at the 10 highest-frequency unknown codes in detail
print(f"\n{'='*70}")
print("STRATEGY 5: TOP 10 UNKNOWN CODES - FULL NEIGHBOR ANALYSIS")
print("=" * 70)

for code in unknown_codes[:10]:
    freq = pair_counts[code]
    pct = freq / total_pairs * 100

    # Left and right neighbors (only fixed codes)
    left = Counter()
    right = Counter()
    # Also track left/right PAIRS (bigram context)
    left_bigrams = Counter()
    right_bigrams = Counter()

    for pairs in book_pairs:
        for i, p in enumerate(pairs):
            if p != code:
                continue
            if i > 0 and pairs[i-1] in fixed:
                left[fixed[pairs[i-1]]] += 1
            if i < len(pairs) - 1 and pairs[i+1] in fixed:
                right[fixed[pairs[i+1]]] += 1
            # Bigram context (2 known on each side)
            if i > 1 and pairs[i-2] in fixed and pairs[i-1] in fixed:
                left_bigrams[fixed[pairs[i-2]] + fixed[pairs[i-1]]] += 1
            if i < len(pairs) - 2 and pairs[i+1] in fixed and pairs[i+2] in fixed:
                right_bigrams[fixed[pairs[i+1]] + fixed[pairs[i+2]]] += 1

    print(f"\n  Code {code} (freq={freq}, {pct:.1f}%):")
    print(f"    Left:  {', '.join(f'{l}:{c}' for l, c in left.most_common(8))}")
    print(f"    Right: {', '.join(f'{l}:{c}' for l, c in right.most_common(8))}")
    print(f"    Left bigrams:  {', '.join(f'{b}:{c}' for b, c in left_bigrams.most_common(6))}")
    print(f"    Right bigrams: {', '.join(f'{b}:{c}' for b, c in right_bigrams.most_common(6))}")

    # Score for MISSING letters specifically
    german_bigrams = {
        'EN': 3.88, 'ER': 3.75, 'CH': 2.75, 'DE': 2.00, 'EI': 1.88,
        'ND': 1.88, 'TE': 1.67, 'IN': 1.65, 'IE': 1.64, 'GE': 1.43,
        'ES': 1.36, 'NE': 1.26, 'SE': 1.20, 'RE': 1.18, 'HE': 1.16,
        'AN': 1.14, 'UN': 1.14, 'ST': 1.13, 'BE': 1.06, 'DI': 0.98,
        'EM': 0.93, 'AU': 0.93, 'SC': 0.86, 'DA': 0.86, 'SI': 0.82,
        'LE': 0.82, 'IC': 0.81, 'TI': 0.73, 'AL': 0.71, 'HA': 0.71,
        'NG': 0.67, 'WE': 0.65, 'EL': 0.65, 'HI': 0.58, 'NS': 0.57,
        'NT': 0.56, 'IS': 0.55, 'HT': 0.54, 'MI': 0.52, 'IT': 0.50,
        'RI': 0.41, 'AB': 0.38, 'LI': 0.35, 'ED': 0.35, 'EG': 0.34,
        'NI': 0.33, 'ET': 0.33, 'IG': 0.32, 'AR': 0.31, 'RU': 0.30,
        'LA': 0.29, 'BI': 0.27, 'FE': 0.26, 'ZU': 0.25, 'MA': 0.24,
        'OR': 0.23, 'WA': 0.22, 'SS': 0.22, 'RS': 0.21, 'RT': 0.20,
        'RD': 0.19, 'TA': 0.18, 'TH': 0.17, 'RN': 0.17, 'LS': 0.16,
        'OB': 0.15, 'AG': 0.15, 'VO': 0.15, 'OC': 0.14, 'FU': 0.13,
        'RA': 0.13, 'WI': 0.13, 'BU': 0.12, 'KE': 0.12, 'OD': 0.12,
        'OL': 0.11, 'RO': 0.11, 'GT': 0.11, 'AF': 0.10, 'KO': 0.10,
        'TT': 0.10, 'GR': 0.10, 'VE': 0.10, 'ZE': 0.10, 'GL': 0.09,
        'TR': 0.09, 'LT': 0.09, 'GA': 0.09, 'OG': 0.08, 'BR': 0.08,
        'FI': 0.08, 'FO': 0.07, 'PR': 0.07, 'KA': 0.07, 'SP': 0.07,
    }

    # Only score for MISSING letters
    missing = 'TRGOBFKZPV'
    scores = {}
    for letter in missing:
        score = 0
        for l_letter, count in left.items():
            bg = l_letter + letter
            if bg in german_bigrams:
                score += german_bigrams[bg] * count
        for r_letter, count in right.items():
            bg = letter + r_letter
            if bg in german_bigrams:
                score += german_bigrams[bg] * count
        if score > 0:
            scores[letter] = score

    if scores:
        top = sorted(scores.items(), key=lambda x: -x[1])[:5]
        print(f"    Missing-letter scores: {', '.join(f'{l}:{s:.1f}' for l, s in top)}")

    # Word evidence for this code (from strategy 2)
    if code in word_evidence:
        for letter in sorted(word_evidence[code], key=lambda l: -len(word_evidence[code][l])):
            hits = len(word_evidence[code][letter])
            if hits >= 2:
                words = sorted(set(word_evidence[code][letter]))[:5]
                print(f"    Word evidence: {letter} = {hits} hits ({words})")


# STRATEGY 6: NOCH/ODER/DORT — common words with O
print(f"\n{'='*70}")
print("STRATEGY 6: NOCH, ODER, DORT, WORT, OFT — finding O codes")
print("=" * 70)

# NOCH = N,O,C,H — N and C and H are known, O is unknown
# Look for N_?_C_H where ? is unknown
noch_candidates = Counter()
for pairs in book_pairs:
    for i in range(len(pairs) - 3):
        w = pairs[i:i+4]
        if (w[0] in n_codes_set and w[2] in c_codes_set and w[3] in h_codes_set
            and w[1] not in fixed):
            noch_candidates[w[1]] += 1

print("NOCH candidates (N_?_CH pattern):")
for code, count in noch_candidates.most_common(10):
    print(f"  {code} = O: {count} matches (freq={pair_counts[code]})")

# ODER = O,D,E,R — D,E,R known, O unknown
d_codes_set = set(c for c, l in fixed.items() if l == 'D')
e_codes_set = set(c for c, l in fixed.items() if l == 'E')
r_codes_set = set(c for c, l in fixed.items() if l == 'R')

oder_candidates = Counter()
for pairs in book_pairs:
    for i in range(len(pairs) - 3):
        w = pairs[i:i+4]
        if (w[1] in d_codes_set and w[2] in e_codes_set and w[3] in r_codes_set
            and w[0] not in fixed):
            oder_candidates[w[0]] += 1

print("\nODER candidates (?_D_E_R pattern):")
for code, count in oder_candidates.most_common(10):
    print(f"  {code} = O: {count} matches (freq={pair_counts[code]})")


# STRATEGY 7: AUCH — A,U,C,H all known! Use it to validate
print(f"\n{'='*70}")
print("STRATEGY 7: VALIDATION — AUCH should appear with all-known codes")
print("=" * 70)

a_codes_set = set(c for c, l in fixed.items() if l == 'A')
u_codes_set = set(c for c, l in fixed.items() if l == 'U')

auch_count = 0
for pairs in book_pairs:
    for i in range(len(pairs) - 3):
        w = pairs[i:i+4]
        if (w[0] in a_codes_set and w[1] in u_codes_set
            and w[2] in c_codes_set and w[3] in h_codes_set):
            auch_count += 1
            if auch_count <= 10:
                print(f"  AUCH at book pos: {w}")

print(f"Total AUCH matches: {auch_count}")


# STRATEGY 8: GE- prefix (extremely common in German)
print(f"\n{'='*70}")
print("STRATEGY 8: GE- PREFIX — finding G codes")
print("=" * 70)

# G is always followed by E in GE- prefix. Look for ?_E patterns
# where ? precedes E very frequently
ge_candidates = Counter()
for pairs in book_pairs:
    for i in range(len(pairs) - 1):
        if pairs[i] not in fixed and pairs[i+1] in fixed and fixed[pairs[i+1]] == 'E':
            ge_candidates[pairs[i]] += 1

# Filter to high-frequency unknowns that strongly precede E
print("Codes that frequently precede E (potential G, B, F, etc.):")
for code, count in ge_candidates.most_common(15):
    freq = pair_counts[code]
    ratio = count / freq * 100
    if count >= 10:
        # Also check what follows E after this code (?_E_?)
        following = Counter()
        for pairs in book_pairs:
            for i in range(len(pairs) - 2):
                if pairs[i] == code and pairs[i+1] in fixed and fixed[pairs[i+1]] == 'E':
                    if pairs[i+2] in fixed:
                        following[fixed[pairs[i+2]]] += 1

        # G should be followed by E then typically I,N,S,H,R
        print(f"  {code}: {count} times before E ({ratio:.0f}% of {freq}), then E->{dict(following.most_common(5))}")


print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
