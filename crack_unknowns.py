"""
Targeted bigram analysis for specific unknown codes.
Focus on codes appearing in the two key recurring patterns.
Use ALL confirmed+tier1+tier2 assignments as constraints.
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

# Build all pairs
all_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    all_pairs.extend(pairs)

pair_counts = Counter(all_pairs)
total_pairs = len(all_pairs)

# ALL known assignments (confirmed + tier1 + tier2)
known = {
    # Confirmed
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U',
    # Tier 1
    '00': 'H', '14': 'N', '72': 'R', '91': 'S', '15': 'I',
    # Tier 2
    '76': 'E', '52': 'S', '42': 'D', '46': 'I', '48': 'N',
    '57': 'H', '04': 'M', '12': 'S', '58': 'N',
}

# Build bigram counts
bigrams = Counter()
for i in range(len(all_pairs) - 1):
    bigrams[(all_pairs[i], all_pairs[i+1])] += 1

# German bigram reference (what bigrams are common)
german_bigrams_rank = {
    'EN': 1, 'ER': 2, 'CH': 3, 'DE': 4, 'EI': 5,
    'ND': 6, 'TE': 7, 'IN': 8, 'IE': 9, 'GE': 10,
    'ES': 11, 'NE': 12, 'SE': 13, 'RE': 14, 'HE': 15,
    'AN': 16, 'UN': 17, 'ST': 18, 'BE': 19, 'DI': 20,
    'EM': 21, 'AU': 22, 'SC': 23, 'DA': 24, 'SI': 25,
    'LE': 26, 'IC': 27, 'TI': 28, 'AL': 29, 'HA': 30,
    'NG': 31, 'WE': 32, 'EL': 33, 'HI': 34, 'NS': 35,
    'NT': 36, 'IS': 37, 'HT': 38, 'MI': 39, 'IT': 40,
    'RI': 41, 'EC': 42, 'LI': 43, 'AB': 44, 'SS': 45,
    'ED': 46, 'EG': 47, 'NI': 48, 'ET': 49, 'IG': 50,
    'AR': 51, 'RU': 52, 'ER': 53, 'FE': 54, 'ZU': 55,
    'MA': 56, 'OR': 57, 'WA': 58, 'LA': 59, 'BI': 60,
}

# Uncommon/impossible German bigrams for filtering
rare_bigrams = set([
    'QQ', 'QX', 'XQ', 'YY', 'QZ', 'ZQ', 'XZ', 'ZX',
    'QK', 'KQ', 'QJ', 'JQ', 'QV', 'VQ', 'QW', 'WQ',
])

# Target unknown codes
# From 19-pair pattern: DIESER-[78][30]-INE-[51][59]-EIN-[41]-DE
# From pre-STEIN:       IEU-[51][35][34][78][01]-STEIN
# Post-STEIN:           E-[93][64][67][24]-A-D-?

target_codes = ['78', '30', '51', '59', '41', '35', '34', '01',
                '93', '64', '67', '24',
                # Plus other high-frequency unknowns
                '74', '50', '94', '65']

print("=" * 70)
print("TARGETED BIGRAM ANALYSIS FOR KEY UNKNOWN CODES")
print("=" * 70)

for code in target_codes:
    if code not in pair_counts:
        continue
    freq = pair_counts[code]
    pct = freq / total_pairs * 100

    print(f"\n{'='*50}")
    print(f"CODE '{code}': {freq} occurrences ({pct:.1f}%)")
    print(f"{'='*50}")

    # All bigrams where code is LEFT element (code -> X)
    right_neighbors = Counter()
    for (a, b), count in bigrams.items():
        if a == code:
            right_neighbors[b] += count

    # All bigrams where code is RIGHT element (X -> code)
    left_neighbors = Counter()
    for (a, b), count in bigrams.items():
        if b == code:
            left_neighbors[a] += count

    print(f"\n  code -> X (right neighbors, what follows '{code}'):")
    for nb, cnt in right_neighbors.most_common(12):
        nb_letter = known.get(nb, '?')
        pct_of_code = cnt / freq * 100
        if nb_letter != '?':
            print(f"    {code}->{nb}({nb_letter}): {cnt}x ({pct_of_code:.0f}%) => ?{nb_letter}")
        else:
            print(f"    {code}->{nb}(?): {cnt}x ({pct_of_code:.0f}%)")

    print(f"\n  X -> code (left neighbors, what precedes '{code}'):")
    for nb, cnt in left_neighbors.most_common(12):
        nb_letter = known.get(nb, '?')
        pct_of_code = cnt / freq * 100
        if nb_letter != '?':
            print(f"    {nb}({nb_letter})->{code}: {cnt}x ({pct_of_code:.0f}%) => {nb_letter}?")
        else:
            print(f"    {nb}(?)->{code}: {cnt}x ({pct_of_code:.0f}%)")

    # Letter deduction
    print(f"\n  DEDUCTION for code '{code}':")

    # Score each possible letter
    letter_scores = {}
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        score = 0
        evidence = []

        # Check right neighbors (code=letter, neighbor=known_letter)
        for nb, cnt in right_neighbors.items():
            if nb in known:
                bg = letter + known[nb]
                if bg in german_bigrams_rank:
                    rank = german_bigrams_rank[bg]
                    # Higher count + higher rank = better evidence
                    s = cnt * (60 - rank) / 60
                    score += s
                    if cnt >= 5:
                        evidence.append(f"{bg}(rank{rank})x{cnt}")
                elif bg in rare_bigrams:
                    score -= cnt * 2
                    if cnt >= 3:
                        evidence.append(f"RARE:{bg}x{cnt}")

        # Check left neighbors (neighbor=known_letter, code=letter)
        for nb, cnt in left_neighbors.items():
            if nb in known:
                bg = known[nb] + letter
                if bg in german_bigrams_rank:
                    rank = german_bigrams_rank[bg]
                    s = cnt * (60 - rank) / 60
                    score += s
                    if cnt >= 5:
                        evidence.append(f"{bg}(rank{rank})x{cnt}")
                elif bg in rare_bigrams:
                    score -= cnt * 2
                    if cnt >= 3:
                        evidence.append(f"RARE:{bg}x{cnt}")

        if score > 0:
            letter_scores[letter] = (score, evidence)

    # Show top candidates
    sorted_letters = sorted(letter_scores.items(), key=lambda x: -x[1][0])
    for letter, (score, evidence) in sorted_letters[:5]:
        ev_str = ', '.join(evidence[:6])
        print(f"    {letter}: score={score:.0f}  [{ev_str}]")


# Now specifically analyze the two patterns
print(f"\n\n{'='*70}")
print("PATTERN ANALYSIS: 19-PAIR RECURRING PATTERN")
print("='*70")
print("Codes: 45,21,76,52,19,72,78,30,46,48,76,51,59,56,46,11,41,45,19")
print("Known: D, I, E, S, E, R, ?, ?, I, N, E, ?, ?, E, I, N, ?, D, E")
print()

# What are the constraints?
# Position 7 (code 78): preceded by R (code 72), followed by code 30
# Position 8 (code 30): preceded by code 78, followed by I (code 46)
# Position 12 (code 51): preceded by E (code 76), followed by code 59
# Position 13 (code 59): preceded by code 51, followed by E (code 56)
# Position 17 (code 41): preceded by N (code 11), followed by D (code 45)

print("Positional constraints:")
print("  [78]: R-?-[30]  => R? (R followed by ?)")
print("  [30]: [78]-?-I   => ?I (? followed by I)")
print("  [51]: E-?-[59]  => E? (?)")
print("  [59]: [51]-?-E   => ?E (?)")
print("  [41]: N-?-D     => N?D")
print()

# For code 41 in position 17: N-[41]-D
# German trigrams with N_D: NED, NAD, NID, NUD, NND...
# In context: EIN[41]DE
# EINDE is Dutch, not German...
# But: EIN + ?DE could be word boundary: EIN ?DE...
# Or: EIN? + DE = EIN? DE (but ? comes before D)
# NND is very rare in German. But ENDE is very common.
# What if 41 is... hmm

# Actually let's look at what 41 appears as in the broader corpus
print("CODE 41 in trigram context (N-41-D pattern):")
for i in range(1, len(all_pairs) - 1):
    if all_pairs[i] == '41':
        left = known.get(all_pairs[i-1], '?')
        right = known.get(all_pairs[i+1], '?')
        if left != '?' and right != '?':
            print(f"  ...{all_pairs[i-1]}({left})-41(?)-{all_pairs[i+1]}({right})... = {left}?{right}")

print()

# Let's focus on code 78 since it's in BOTH patterns
print(f"\n{'='*70}")
print("CODE 78 - APPEARS IN BOTH PATTERNS")
print(f"{'='*70}")
print("19-pair context: R-[78]-[30]-I  (DIESER-[78][30]-INE...)")
print("Pre-STEIN context: U-[51]-[35]-[34]-[78]-[01]-STEIN")
print()

# In pre-STEIN: codes 95,61,51,35,34,78,01 before STEIN
# Known: 95=E, 61=U, 51=?, 35=?, 34=?, 78=?, 01=?
# So: E-U-[51]-[35]-[34]-[78]-[01]-S-T-E-I-N
# What 7-letter German word ends with STEIN?
# Or: what's the pattern EU?????STEIN?

# Let me check ALL trigrams for code 78 with known neighbors
print("All trigrams involving code 78 with at least one known neighbor:")
trigram_counts = Counter()
for i in range(1, len(all_pairs) - 1):
    if all_pairs[i] == '78':
        left = all_pairs[i-1]
        right = all_pairs[i+1]
        l_letter = known.get(left, '?')
        r_letter = known.get(right, '?')
        if l_letter != '?' or r_letter != '?':
            key = f"{left}({l_letter})-78-{right}({r_letter})"
            trigram_counts[key] += 1

for tri, cnt in trigram_counts.most_common(15):
    print(f"  {tri}: {cnt}x")


# German words analysis - what 5-letter sequences ?????STEIN make sense?
print(f"\n{'='*70}")
print("WHAT GERMAN WORDS FIT EU?????STEIN?")
print(f"{'='*70}")
print()
print("Pre-STEIN = E-U-[51]-[35]-[34]-[78]-[01]-S-T-E-I-N")
print()
print("With current tier2: 51=? 35=? 34=? 78=? 01=?")
print()

# Let's think about this:
# EU_____STEIN
# Common German patterns:
# RUNENSTEIN = R-U-N-E-N-S-T-E-I-N ... but we proved that wrong
# What about compound words ending in STEIN?
# _____STEIN where the whole thing is EU + 5 letters + STEIN
# Could be: EU + word + STEIN (compound)
# EU + CH + STEIN = EUCHSTEIN? Not a word
# Or word boundary: EU? ????STEIN
# E + U + ? + ? + ? + ? + ? + STEIN
# Could be: (word ending EU?) + (word starting with ?????STEIN)

# Actually, the extended context was: ?DDEM?DIEU?????STEINE????AD??A?SC?S
# With tier2: the full context before STEIN includes more letters
# Let's decode the full extended context with ALL known codes

far_context = ['74','45','45','19','04','50','42','15','95','61','51','35','34','78','01','92','88','95','21','60','19','93','64','67','24','31','42','78','94','31','51','91','18','65','12']
decoded = []
for c in far_context:
    if c in known:
        decoded.append(known[c])
    else:
        decoded.append(f'[{c}]')

print("Full extended STEIN context with all known codes:")
print(' '.join(decoded))
print()

# Let's identify which of these are still unknown
unknowns_in_context = [c for c in far_context if c not in known]
print(f"Still unknown codes in context: {unknowns_in_context}")
print()

# Now check trigrams for code 01
print(f"\n{'='*70}")
print("CODE 01 - Position just before STEIN (pre-STEIN[-1])")
print(f"{'='*70}")
print("Context: [78]-[01]-S (just before STEIN)")
print()

# What letter forms XS with a preceding unknown?
# In German, common digrams ending in S: ES, NS, IS, AS, US, RS
# So code 01 could be E, N, I, A, U, R
# But E, N, I, R are already well-represented
# Let's check bigram evidence

print("Trigrams with code 01:")
for i in range(1, len(all_pairs) - 1):
    if all_pairs[i] == '01' and (all_pairs[i-1] in known or all_pairs[i+1] in known):
        left = all_pairs[i-1]
        right = all_pairs[i+1]
        l_letter = known.get(left, f'[{left}]')
        r_letter = known.get(right, f'[{right}]')
        pass  # handled below

# Simplified: just show bigram evidence
for code in ['01', '30', '35', '34', '59']:
    if code in pair_counts:
        print(f"\n  Code {code} ({pair_counts[code]} total):")
        # right side
        for (a,b), cnt in sorted(bigrams.items(), key=lambda x: -x[1]):
            if a == code and b in known and cnt >= 3:
                print(f"    {code}->{b}({known[b]}): {cnt}x => ?{known[b]}")
        # left side
        for (a,b), cnt in sorted(bigrams.items(), key=lambda x: -x[1]):
            if b == code and a in known and cnt >= 3:
                print(f"    {a}({known[a]})->{code}: {cnt}x => {known[a]}?")


# Final deduction attempt
print(f"\n\n{'='*70}")
print("DEDUCTION: MOST LIKELY LETTERS FOR KEY UNKNOWNS")
print(f"{'='*70}")
print()

# For each target code, show the best-fit letter based on bigram evidence
for code in ['78', '30', '51', '59', '41', '35', '34', '01']:
    if code not in pair_counts:
        continue

    letter_evidence = {}
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        score = 0
        reasons = []

        for (a,b), cnt in bigrams.items():
            if a == code and b in known:
                bg = letter + known[b]
                if bg in german_bigrams_rank:
                    s = cnt * (61 - german_bigrams_rank[bg])
                    score += s
                    if s > 20:
                        reasons.append(f"?{known[b]}={bg}x{cnt}")
            if b == code and a in known:
                bg = known[a] + letter
                if bg in german_bigrams_rank:
                    s = cnt * (61 - german_bigrams_rank[bg])
                    score += s
                    if s > 20:
                        reasons.append(f"{known[a]}?={bg}x{cnt}")

        if score > 0:
            letter_evidence[letter] = (score, reasons)

    sorted_ev = sorted(letter_evidence.items(), key=lambda x: -x[1][0])
    print(f"  Code {code} ({pair_counts[code]}x):")
    for letter, (score, reasons) in sorted_ev[:4]:
        r = ', '.join(reasons[:5])
        print(f"    {letter} (score {score:>5d}): {r}")

    # In 19-pair pattern context
    if code == '78':
        print(f"    Pattern context: R-[78]-[30]-I => R?_ and EU...[78][01]STEIN")
    elif code == '30':
        print(f"    Pattern context: [78]-[30]-I => _?I")
    elif code == '51':
        print(f"    Pattern context: E-[51]-[59] and EU-[51]-...")
    elif code == '59':
        print(f"    Pattern context: [51]-[59]-E")
    elif code == '41':
        print(f"    Pattern context: N-[41]-D")
    print()


print(f"\n{'='*70}")
print("DONE")
print(f"{'='*70}")
