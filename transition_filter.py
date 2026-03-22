"""
Tibia 469 - Transition Matrix Constraint Filtering
====================================================
Key insight: Certain digit transitions are near-forbidden (3->3: 1x, 0->7: 1x, 3->2: 2x).
In a substitution cipher, these constrain which letters can map to which digits.

This script:
1. Builds the full transition model
2. Filters Knightmare solutions using transition constraints
3. Tries a NEW approach: treating forbidden transitions as word boundaries
4. Tests if the text has a hidden delimiter structure
"""

import json
from collections import Counter, defaultdict
from itertools import product

with open("books.json", "r") as f:
    books = json.load(f)

all_text = "".join(books)

print("=" * 70)
print("TRANSITION MATRIX CONSTRAINT ANALYSIS")
print("=" * 70)

# ============================================================
# 1. FULL TRANSITION ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("1. DETAILED TRANSITION MATRIX")
print("=" * 70)

transitions = Counter()
for i in range(len(all_text) - 1):
    transitions[(all_text[i], all_text[i+1])] += 1

total_trans = sum(transitions.values())

# Build expected vs observed
digit_freq = Counter(all_text)
total_digits = len(all_text)

print("\nObserved vs Expected transition counts:")
print(f"{'Pair':>6} {'Observed':>8} {'Expected':>8} {'Ratio':>8} {'Status'}")
print("-" * 50)

anomalies = []
for d1 in "0123456789":
    for d2 in "0123456789":
        obs = transitions.get((d1, d2), 0)
        # Expected if independent: P(d1) * P(d2) * total_transitions
        exp = (digit_freq[d1] / total_digits) * (digit_freq[d2] / total_digits) * total_trans
        if exp > 0:
            ratio = obs / exp
        else:
            ratio = 0

        if ratio < 0.15 or ratio > 3.0:
            status = "*** ANOMALY ***" if ratio < 0.15 else "** HIGH **"
            anomalies.append((d1, d2, obs, exp, ratio))
            print(f"  {d1}->{d2}  {obs:8d}  {exp:8.1f}  {ratio:8.3f}  {status}")

print(f"\n  Total anomalous transitions: {len(anomalies)}")

# ============================================================
# 2. FORBIDDEN TRANSITION PAIRS AS CONSTRAINTS
# ============================================================
print("\n" + "=" * 70)
print("2. FORBIDDEN TRANSITIONS (ratio < 0.2)")
print("=" * 70)

forbidden = [(d1, d2) for d1, d2, obs, exp, ratio in anomalies if ratio < 0.2]
print(f"\nForbidden pairs: {forbidden}")

# What does this mean for cipher mapping?
# If digit A rarely follows digit B, then the LETTERS that A and B map to
# rarely appear adjacent in the plaintext language.

# In English, the rarest bigrams include: QJ, QX, JQ, ZX, XJ, etc.
# In German: similar rare combinations

# ============================================================
# 3. TRIGRAM TRANSITION ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("3. TRIGRAM ANALYSIS (3-digit sequences)")
print("=" * 70)

trigrams = Counter()
for i in range(len(all_text) - 2):
    trigrams[all_text[i:i+3]] += 1

# How many possible trigrams exist vs how many we see?
possible = 1000  # 000-999
observed_trigrams = len(trigrams)
print(f"\nPossible trigrams: {possible}")
print(f"Observed trigrams: {observed_trigrams}")
print(f"Missing trigrams: {possible - observed_trigrams}")

# List missing trigrams
all_possible = set(f"{i:03d}" for i in range(1000))
missing = all_possible - set(trigrams.keys())
print(f"\nMissing trigrams (never appear): {len(missing)}")

# Group missing by first digit
missing_by_first = defaultdict(list)
for m in sorted(missing):
    missing_by_first[m[0]].append(m)

for d in "0123456789":
    if d in missing_by_first:
        print(f"  Starting with {d}: {len(missing_by_first[d])} missing")
        if len(missing_by_first[d]) <= 20:
            print(f"    {missing_by_first[d]}")

# ============================================================
# 4. WORD BOUNDARY HYPOTHESIS
# ============================================================
print("\n" + "=" * 70)
print("4. FORBIDDEN TRANSITIONS AS WORD BOUNDARIES")
print("=" * 70)

# What if near-forbidden transitions mark word boundaries?
# Split the text wherever a forbidden transition occurs

forbidden_set = set()
for d1, d2, obs, exp, ratio in anomalies:
    if ratio < 0.2:
        forbidden_set.add((d1, d2))

print(f"\nUsing {len(forbidden_set)} forbidden transitions as delimiters:")
for f in sorted(forbidden_set):
    print(f"  {f[0]}->{f[1]}")

# Split first book at forbidden transitions
sample = books[0]
words = []
current_word = sample[0]
for i in range(1, len(sample)):
    if (sample[i-1], sample[i]) in forbidden_set:
        words.append(current_word)
        current_word = sample[i]
    else:
        current_word += sample[i]
words.append(current_word)

print(f"\nBook 1 split into {len(words)} 'words':")
word_lengths = [len(w) for w in words]
print(f"  Word lengths: {word_lengths}")
print(f"  Average word length: {sum(word_lengths)/len(word_lengths):.1f} digits")
print(f"  Words: {words[:30]}")

# In English, average word length is 4.7 letters
# If ~1.6 digits per letter, average word = 7.5 digits
# If ~2 digits per letter, average word = 9.4 digits

# Word length distribution
wl_dist = Counter(word_lengths)
print(f"\n  Word length distribution:")
for length in sorted(wl_dist.keys()):
    print(f"    {length:3d} digits: {wl_dist[length]:3d} words {'*' * wl_dist[length]}")

# Do the same for ALL books combined
all_words = []
current_word = all_text[0]
for i in range(1, len(all_text)):
    if (all_text[i-1], all_text[i]) in forbidden_set:
        all_words.append(current_word)
        current_word = all_text[i]
    else:
        current_word += all_text[i]
all_words.append(current_word)

print(f"\nAll books combined: {len(all_words)} 'words'")
all_wl = [len(w) for w in all_words]
print(f"  Average length: {sum(all_wl)/len(all_wl):.1f} digits")

# Most common "words"
word_freq = Counter(all_words)
print(f"\n  Most common 'words' (top 30):")
for word, count in word_freq.most_common(30):
    print(f"    '{word}' ({len(word)} digits): {count}x")

# ============================================================
# 5. RELAXED BOUNDARY ANALYSIS (more generous threshold)
# ============================================================
print("\n" + "=" * 70)
print("5. RELAXED WORD BOUNDARIES (ratio < 0.3)")
print("=" * 70)

relaxed_set = set()
for d1 in "0123456789":
    for d2 in "0123456789":
        obs = transitions.get((d1, d2), 0)
        exp = (digit_freq[d1] / total_digits) * (digit_freq[d2] / total_digits) * total_trans
        if exp > 0 and obs / exp < 0.3:
            relaxed_set.add((d1, d2))

print(f"Using {len(relaxed_set)} rare transitions as delimiters")

words_r = []
current_word = all_text[0]
for i in range(1, len(all_text)):
    if (all_text[i-1], all_text[i]) in relaxed_set:
        words_r.append(current_word)
        current_word = all_text[i]
    else:
        current_word += all_text[i]
words_r.append(current_word)

print(f"Total 'words': {len(words_r)}")
all_wl_r = [len(w) for w in words_r]
print(f"Average length: {sum(all_wl_r)/len(all_wl_r):.1f} digits")

wl_dist_r = Counter(all_wl_r)
print(f"\nWord length distribution:")
for length in sorted(wl_dist_r.keys())[:25]:
    bar = '*' * min(wl_dist_r[length], 60)
    print(f"  {length:3d}: {wl_dist_r[length]:4d} {bar}")

# Most common words with relaxed boundaries
word_freq_r = Counter(words_r)
print(f"\nMost common 'words' (top 30):")
for word, count in word_freq_r.most_common(30):
    if count >= 3:
        print(f"  '{word}' ({len(word)} digits): {count}x")

# ============================================================
# 6. FILTER KNIGHTMARE SOLUTIONS WITH TRANSITIONS
# ============================================================
print("\n" + "=" * 70)
print("6. FILTERING KNIGHTMARE SOLUTIONS WITH TRANSITION CONSTRAINTS")
print("=" * 70)

def find_splits(cipher, plain, pos_c=0, pos_p=0, current_mapping=None, current_split=None):
    if current_mapping is None:
        current_mapping = {}
    if current_split is None:
        current_split = []
    if pos_p == len(plain):
        if pos_c == len(cipher):
            return [(dict(current_mapping), list(current_split))]
        return []
    if pos_c >= len(cipher):
        return []
    results = []
    for width in [1, 2, 3]:
        if pos_c + width > len(cipher):
            continue
        code = cipher[pos_c:pos_c + width]
        letter = plain[pos_p]
        if code in current_mapping and current_mapping[code] != letter:
            continue
        new_mapping = dict(current_mapping)
        new_mapping[code] = letter
        new_split = current_split + [code]
        results.extend(find_splits(cipher, plain, pos_c + width, pos_p + 1,
                                   new_mapping, new_split))
    return results

cipher = "347867090871097664346600345"
plain = "BEAWITTHANBEAFOOL"

print(f"Generating all consistent splits...")
solutions = find_splits(cipher, plain)
print(f"Found {len(solutions)} solutions")

# For each solution, check if the decoded text produces forbidden transitions
# A GOOD solution should NOT produce many forbidden letter-bigrams in English

ENGLISH_FREQ = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0,
    'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3,
    'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4, 'W': 2.4,
    'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5,
    'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
    'Z': 0.07
}

# English quadgram scoring (approximate)
COMMON_QUADS = [
    'TION', 'ATIO', 'THAT', 'THER', 'WITH', 'INTH', 'MENT',
    'HAVE', 'THIS', 'WILL', 'NTHE', 'HING', 'OTHE', 'IGHT',
    'STHE', 'HERE', 'OUGH', 'OULD', 'IGHT', 'FROM', 'THEM',
    'ERED', 'ANDE', 'OFTH', 'SAND', 'THEP', 'FORE', 'THEN'
]

COMMON_TRIGRAMS = [
    'THE', 'AND', 'ING', 'ION', 'TIO', 'ENT', 'ERE', 'HER',
    'ATE', 'VER', 'TER', 'EST', 'ALL', 'HAT', 'FOR', 'HIS',
    'ARE', 'BUT', 'NOT', 'WAS', 'OUR', 'HAS', 'ONE', 'CAN'
]

FORBIDDEN_ENG_BIGRAMS = set([
    'QJ', 'QX', 'JQ', 'ZX', 'XJ', 'QZ', 'JZ', 'ZJ', 'ZQ',
    'QV', 'QK', 'QY', 'QG', 'QW', 'QP', 'QC', 'QF', 'QM',
    'JX', 'XQ', 'ZV', 'VQ', 'JV', 'VJ', 'VX', 'XV', 'BX',
    'CJ', 'FX', 'GX', 'HX', 'JC', 'JD', 'JF', 'JG', 'JH',
    'JK', 'JL', 'JM', 'JN', 'JP', 'JR', 'JS', 'JT', 'JW',
    'KX', 'MX', 'PX', 'QD', 'QH', 'QN', 'QR', 'QS', 'QT',
    'SX', 'TX', 'VZ', 'WX', 'XB', 'XD', 'XF', 'XG', 'XK',
    'XM', 'XN', 'XR', 'XW', 'XZ', 'YX', 'ZB', 'ZD', 'ZF',
    'ZG', 'ZK', 'ZN', 'ZP', 'ZR', 'ZW',
])

def decode_variable(text, mapping):
    result = []
    i = 0
    unmapped = 0
    sorted_codes = sorted(mapping.keys(), key=len, reverse=True)
    while i < len(text):
        matched = False
        for code in sorted_codes:
            if text[i:i + len(code)] == code:
                result.append(mapping[code])
                i += len(code)
                matched = True
                break
        if not matched:
            result.append('?')
            i += 1
            unmapped += 1
    return "".join(result), unmapped

def score_advanced(text):
    """Advanced scoring with trigrams, quadgrams, and frequency match."""
    text = text.upper()
    score = 0.0
    alpha = [c for c in text if c.isalpha()]
    if len(alpha) < 10:
        return -999999

    # Trigram bonus
    for i in range(len(text) - 2):
        tri = text[i:i+3]
        if tri in COMMON_TRIGRAMS:
            score += 5.0

    # Quadgram bonus
    for i in range(len(text) - 3):
        quad = text[i:i+4]
        if quad in COMMON_QUADS:
            score += 10.0

    # Forbidden bigram penalty
    for i in range(len(text) - 1):
        bi = text[i:i+2]
        if bi.isalpha() and bi in FORBIDDEN_ENG_BIGRAMS:
            score -= 20.0

    # Letter frequency match
    counts = Counter(alpha)
    total = len(alpha)
    for letter, expected in ENGLISH_FREQ.items():
        observed = counts.get(letter, 0) / total * 100
        score -= abs(observed - expected) * 0.3

    # Penalty for unmapped
    q_count = text.count('?')
    score -= q_count * 3

    # Bonus for vowel/consonant alternation (natural language pattern)
    vowels = set('AEIOU')
    alternations = 0
    for i in range(len(alpha) - 1):
        if (alpha[i] in vowels) != (alpha[i+1] in vowels):
            alternations += 1
    if len(alpha) > 1:
        alt_ratio = alternations / (len(alpha) - 1)
        # English alternation ratio is roughly 0.5-0.6
        score += max(0, 20 - abs(alt_ratio - 0.55) * 100)

    return score

# Score with advanced scoring
sample = all_text[:3000]
print(f"\nScoring {len(solutions)} solutions with advanced scoring...")

scored = []
for idx, (mapping, split) in enumerate(solutions):
    decoded, unmapped = decode_variable(sample, mapping)
    s = score_advanced(decoded)
    scored.append((s, idx, mapping, split, decoded, unmapped))

scored.sort(key=lambda x: -x[0])

print(f"\n{'Rank':>4} {'Score':>8} {'Unmapped':>8} {'%mapped':>7} | Key summary")
print("-" * 85)

for rank in range(min(20, len(scored))):
    score, idx, mapping, split, decoded, unmapped = scored[rank]
    pct_mapped = (1 - unmapped/len(decoded)) * 100

    inv = defaultdict(list)
    for code, letter in sorted(mapping.items()):
        inv[letter].append(code)
    map_str = " ".join(f"{l}={','.join(codes)}" for l, codes in sorted(inv.items()))
    print(f"  {rank+1:3d}  {score:8.1f}  {unmapped:6d}  {pct_mapped:5.1f}%  | {map_str[:55]}")

# Show best 3 decoded texts
print("\n" + "=" * 70)
print("TOP 3 DECODED TEXTS")
print("=" * 70)

for rank in range(min(3, len(scored))):
    score, idx, mapping, split, decoded, unmapped = scored[rank]
    print(f"\n--- Rank {rank+1} (score: {score:.1f}) ---")

    # Show mapping
    inv = defaultdict(list)
    for code, letter in sorted(mapping.items()):
        inv[letter].append(code)
    for letter in sorted(inv.keys()):
        print(f"  {letter}: {', '.join(inv[letter])}")

    print(f"\n  First 200 chars: {decoded[:200]}")

    # Decode NPC dialogues
    print(f"\n  NPC Dialogues:")
    for name, npc_text in [("Knightmare", "347867090871097664346600345"),
                            ("Greeting1", "485611800364197"),
                            ("Greeting2", "78572611857643646724"),
                            ("Chayenne", "114514519485611451908304576512282177")]:
        d, u = decode_variable(npc_text, mapping)
        print(f"    {name:>12}: {d}")

# ============================================================
# 7. ENTROPY AT DIFFERENT SCALES
# ============================================================
print("\n" + "=" * 70)
print("7. ENTROPY ANALYSIS AT DIFFERENT SCALES")
print("=" * 70)

import math

def entropy(counter):
    total = sum(counter.values())
    if total == 0:
        return 0
    ent = 0
    for count in counter.values():
        if count > 0:
            p = count / total
            ent -= p * math.log2(p)
    return ent

# Entropy of single digits
e1 = entropy(Counter(all_text))
print(f"\n  Single digit entropy: {e1:.4f} bits (max for 10 symbols: {math.log2(10):.4f})")

# Entropy of pairs
pairs = [all_text[i:i+2] for i in range(0, len(all_text)-1, 2)]
e2 = entropy(Counter(pairs))
print(f"  Digit pair entropy: {e2:.4f} bits (max for 100 pairs: {math.log2(100):.4f})")
print(f"  Per-digit in pairs: {e2/2:.4f} bits")

# Entropy of triplets
trips = [all_text[i:i+3] for i in range(0, len(all_text)-2, 3)]
e3 = entropy(Counter(trips))
print(f"  Digit triple entropy: {e3:.4f} bits (max: {math.log2(1000):.4f})")
print(f"  Per-digit in triples: {e3/3:.4f} bits")

# Conditional entropy (entropy of next digit given current)
cond_ent = 0
for d1 in "0123456789":
    d1_count = digit_freq[d1]
    if d1_count == 0:
        continue
    given_d1 = Counter()
    for i in range(len(all_text) - 1):
        if all_text[i] == d1:
            given_d1[all_text[i+1]] += 1
    if sum(given_d1.values()) > 0:
        cond_ent += (d1_count / total_digits) * entropy(given_d1)

print(f"\n  Conditional entropy H(X|X-1): {cond_ent:.4f} bits")
print(f"  Reduction from unconditional: {e1 - cond_ent:.4f} bits ({(e1-cond_ent)/e1*100:.1f}%)")

# Compare to English
# English has ~1.0-1.5 bits per character of true entropy
# If our text encodes English at ~1.6 digits/letter:
# Expected entropy per digit ≈ 1.3 / 1.6 ≈ 0.81 bits
# But we observe ~3.2 bits per digit
# This means either: (a) not English, (b) inefficient encoding, or (c) the unit isn't single digits

print(f"\n  If encoding English at 1.6 digits/letter:")
print(f"    Expected entropy/digit: ~{1.3/1.6:.2f} bits")
print(f"    Observed entropy/digit: {e1:.2f} bits")
print(f"    Ratio: {e1/(1.3/1.6):.1f}x higher than expected")
print(f"    This suggests the encoding unit is LARGER than single digits")

# ============================================================
# 8. VARIABLE-LENGTH CODE DETECTION
# ============================================================
print("\n" + "=" * 70)
print("8. VARIABLE-LENGTH CODE BOUNDARY DETECTION")
print("=" * 70)

# If this is a variable-length code, certain digit positions should show
# different statistical properties depending on whether they're at the
# START or MIDDLE of a code unit

# Test: are certain digits more likely to START a code unit?
# In Huffman-like codes, shorter codes have higher probability
# The most frequent digit (1, 16.59%) might be a common 1-digit code

# If digit '1' is a single-character code (like 'E' in English):
# Then '1' should rarely be the second digit of a 2-digit code
# This means transitions INTO '1' might show different patterns than
# transitions FROM '1'

print("\n--- Asymmetry analysis: transitions INTO vs FROM each digit ---")
for d in "0123456789":
    into = sum(transitions.get((other, d), 0) for other in "0123456789")
    from_d = sum(transitions.get((d, other), 0) for other in "0123456789")

    # Distribution of what comes BEFORE d
    before_dist = Counter()
    for other in "0123456789":
        before_dist[other] = transitions.get((other, d), 0)

    # Distribution of what comes AFTER d
    after_dist = Counter()
    for other in "0123456789":
        after_dist[other] = transitions.get((d, other), 0)

    h_before = entropy(before_dist)
    h_after = entropy(after_dist)

    asymmetry = abs(h_before - h_after)
    marker = " ***" if asymmetry > 0.3 else ""
    print(f"  Digit {d}: H(before)={h_before:.3f}  H(after)={h_after:.3f}  asymmetry={asymmetry:.3f}{marker}")

# ============================================================
# 9. POSITIONAL ANALYSIS WITHIN BOOKS
# ============================================================
print("\n" + "=" * 70)
print("9. POSITIONAL FREQUENCY (first/last digits of books)")
print("=" * 70)

first_digits = Counter(book[0] for book in books)
last_digits = Counter(book[-1] for book in books)

print("\nFirst digit of each book:")
for d in "0123456789":
    count = first_digits.get(d, 0)
    print(f"  {d}: {count:3d} ({count/70*100:.1f}%)")

print("\nLast digit of each book:")
for d in "0123456789":
    count = last_digits.get(d, 0)
    print(f"  {d}: {count:3d} ({count/70*100:.1f}%)")

# First 3 digits
print("\nFirst 3 digits of each book (potential header):")
first3 = Counter(book[:3] for book in books)
for seq, count in first3.most_common(15):
    print(f"  '{seq}': {count}x")

# Last 3 digits
print("\nLast 3 digits of each book (potential footer):")
last3 = Counter(book[-3:] for book in books)
for seq, count in last3.most_common(15):
    print(f"  '{seq}': {count}x")

# ============================================================
# 10. REPEATING UNIT DETECTION
# ============================================================
print("\n" + "=" * 70)
print("10. LOOKING FOR REPEATING STRUCTURAL UNITS")
print("=" * 70)

# If the text has a fixed-period structure, autocorrelation should peak
# at that period

def autocorrelation(text, lag):
    """Count matching digits at distance 'lag'."""
    matches = sum(1 for i in range(len(text) - lag) if text[i] == text[i + lag])
    return matches / (len(text) - lag)

print("\nAutocorrelation at various lags:")
for lag in range(1, 51):
    ac = autocorrelation(all_text, lag)
    bar = '#' * int(ac * 200)
    marker = " <---" if ac > 0.115 else ""
    print(f"  Lag {lag:3d}: {ac:.4f} {bar}{marker}")

# Check if any period produces significantly higher autocorrelation
print("\nLarger lags (looking for long-period structure):")
for lag in [60, 70, 80, 100, 120, 140, 150, 200, 250, 300]:
    ac = autocorrelation(all_text, lag)
    marker = " <---" if ac > 0.115 else ""
    print(f"  Lag {lag:3d}: {ac:.4f}{marker}")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
