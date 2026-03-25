"""
Systematic search for straddling checkerboard parameters.
Tests all possible row marker combinations against the Knightmare crib
and evaluates frequency distribution against German.
"""

import json
from collections import Counter
from itertools import combinations
import math

# Load books
with open('books.json', 'r') as f:
    books = json.load(f)

all_digits = ''.join(books)
print(f"Total digits: {len(all_digits)}")

# Knightmare crib
knightmare = "347867908719766434660345"
plaintext = "BEAWITTHANBEAFOOL"
n_letters = len(plaintext)
print(f"Knightmare: {knightmare} ({len(knightmare)} digits)")
print(f"Plaintext: {plaintext} ({n_letters} letters)")

# German letter frequencies (top 28 including umlauts and ß)
german_freq = {
    'E': 16.4, 'N': 9.8, 'I': 7.6, 'S': 7.3, 'R': 7.0,
    'A': 6.5, 'T': 6.2, 'D': 5.1, 'H': 4.8, 'U': 4.2,
    'L': 3.4, 'C': 3.1, 'G': 3.0, 'M': 2.5, 'O': 2.5,
    'B': 1.9, 'W': 1.9, 'F': 1.7, 'K': 1.2, 'Z': 1.1,
    'P': 0.8, 'V': 0.7, 'J': 0.3, 'Y': 0.0, 'X': 0.0,
    'Q': 0.0
}

def tokenize_checkerboard(text, markers):
    """Tokenize using straddling checkerboard with given row markers."""
    tokens = []
    i = 0
    while i < len(text):
        d = int(text[i])
        if d in markers and i + 1 < len(text):
            tokens.append(text[i:i+2])
            i += 2
        else:
            tokens.append(text[i])
            i += 1
    return tokens

def compute_ic(tokens):
    """Compute Index of Coincidence."""
    counts = Counter(tokens)
    n = len(tokens)
    if n <= 1:
        return 0
    ic = sum(c * (c - 1) for c in counts.values()) / (n * (n - 1))
    return ic

def ic_ratio(ic, n_symbols):
    """IC ratio vs random for n_symbols."""
    random_ic = 1.0 / n_symbols
    return ic / random_ic if random_ic > 0 else 0

def chi_squared_german(token_freqs, n_symbols):
    """Chi-squared goodness-of-fit test against German frequencies."""
    german_sorted = sorted(german_freq.values(), reverse=True)
    observed_sorted = sorted(token_freqs.values(), reverse=True)

    # Pad to same length
    while len(observed_sorted) < len(german_sorted):
        observed_sorted.append(0)
    while len(german_sorted) < len(observed_sorted):
        german_sorted.append(0)

    chi2 = 0
    for obs, exp in zip(observed_sorted, german_sorted):
        if exp > 0:
            chi2 += (obs - exp) ** 2 / exp
        elif obs > 0:
            chi2 += obs ** 2
    return chi2


print("\n" + "=" * 70)
print("1. SEARCH ALL ROW MARKER PAIRS (Knightmare crib test)")
print("=" * 70)

# Test all pairs of row markers
matches = []
for n_markers in [1, 2, 3]:
    for markers in combinations(range(10), n_markers):
        markers_set = set(markers)
        tokens = tokenize_checkerboard(knightmare, markers_set)
        n_tokens = len(tokens)
        n_unique = 10 - n_markers + 10 * n_markers  # single-digit + two-digit codes

        if n_tokens == n_letters:
            # Also test on full corpus
            all_tokens = tokenize_checkerboard(all_digits, markers_set)
            ic = compute_ic(all_tokens)
            ratio = ic_ratio(ic, n_unique)

            # Get frequency distribution
            total = len(all_tokens)
            freqs = {t: count/total*100 for t, count in Counter(all_tokens).most_common()}
            n_actual_unique = len(freqs)

            matches.append({
                'markers': markers,
                'n_markers': n_markers,
                'n_unique_possible': n_unique,
                'n_unique_actual': n_actual_unique,
                'tokens': tokens,
                'ic_ratio': ratio,
                'total_tokens': total,
                'avg_digits_per_token': len(all_digits) / total,
                'freqs': freqs
            })

            print(f"\n  MATCH! Markers={markers}, {n_tokens} tokens = {n_letters} letters")
            print(f"    Tokens: {tokens}")
            print(f"    Unique symbols: {n_actual_unique}/{n_unique}")
            print(f"    IC ratio: {ratio:.4f}")
            print(f"    Total tokens in corpus: {total}")
            print(f"    Avg digits/token: {len(all_digits)/total:.3f}")

if not matches:
    print("\n  No marker combination gives exactly 17 tokens for Knightmare!")

    # Show closest matches
    print("\n  Closest matches:")
    close = []
    for n_markers in [1, 2, 3]:
        for markers in combinations(range(10), n_markers):
            markers_set = set(markers)
            tokens = tokenize_checkerboard(knightmare, markers_set)
            close.append((markers, len(tokens), tokens))

    close.sort(key=lambda x: abs(x[1] - n_letters))
    for markers, n_tok, tokens in close[:15]:
        diff = n_tok - n_letters
        print(f"    Markers={markers}: {n_tok} tokens (diff={diff:+d})")
        if abs(diff) <= 2:
            print(f"      Tokens: {tokens}")


print("\n" + "=" * 70)
print("2. VARIABLE-LENGTH ENCODING SEARCH")
print("=" * 70)

# What if some digits are 1-digit codes and others are 2-digit codes,
# but NOT in the straddling checkerboard pattern?
# Try: each digit is either a "code digit" or a "modifier digit"
# A code digit alone = one symbol
# A code digit + modifier = another symbol

# Try all possible 2^10 subsets of "modifier digits"
print("\nSearching all possible modifier sets (2^10 = 1024 combinations)...")

best_var = []
for mask in range(1024):
    modifiers = set()
    for d in range(10):
        if mask & (1 << d):
            modifiers.add(d)

    # Tokenize Knightmare
    tokens = []
    i = 0
    valid = True
    while i < len(knightmare):
        d = int(knightmare[i])
        if d in modifiers:
            if i + 1 < len(knightmare):
                tokens.append(knightmare[i:i+2])
                i += 2
            else:
                valid = False
                break
        else:
            tokens.append(knightmare[i])
            i += 1

    if valid and len(tokens) == n_letters:
        # Test corpus
        all_tokens = tokenize_checkerboard(all_digits, modifiers)
        ic = compute_ic(all_tokens)
        n_unique = len(Counter(all_tokens))
        ratio = ic_ratio(ic, n_unique)

        best_var.append({
            'modifiers': modifiers,
            'tokens': tokens,
            'n_unique': n_unique,
            'ic_ratio': ratio,
            'total': len(all_tokens)
        })

print(f"\nFound {len(best_var)} modifier sets giving 17 tokens for Knightmare")

if best_var:
    # Sort by IC ratio (looking for ~1.72 for German)
    best_var.sort(key=lambda x: abs(x['ic_ratio'] - 1.72))

    print("\nTop 10 closest to German IC ratio (1.72):")
    for i, v in enumerate(best_var[:10]):
        print(f"\n  #{i+1}: Modifiers={sorted(v['modifiers'])}")
        print(f"    Tokens: {v['tokens']}")
        print(f"    Unique symbols: {v['n_unique']}")
        print(f"    IC ratio: {v['ic_ratio']:.4f}")
        print(f"    Total tokens: {v['total']}")

        # Map tokens to plaintext letters
        mapping = {}
        for tok, letter in zip(v['tokens'], plaintext):
            if tok in mapping and mapping[tok] != letter:
                print(f"    CONFLICT: token '{tok}' maps to both '{mapping[tok]}' and '{letter}'")
            mapping[tok] = letter
        print(f"    Mapping: {mapping}")


print("\n" + "=" * 70)
print("3. CONSISTENCY CHECK ON BEST CANDIDATES")
print("=" * 70)

# For each candidate that matches Knightmare, check:
# 1. No conflicting mappings (same token -> different letters)
# 2. IC ratio close to German
# 3. Frequency distribution matches German pattern

if best_var:
    print("\nDetailed analysis of top 5 candidates:")

    for i, v in enumerate(best_var[:5]):
        print(f"\n{'='*50}")
        print(f"Candidate #{i+1}: Modifiers={sorted(v['modifiers'])}")
        print(f"{'='*50}")

        modifiers = v['modifiers']
        tokens = v['tokens']
        mapping = {}
        conflicts = []

        for tok, letter in zip(tokens, plaintext):
            if tok in mapping:
                if mapping[tok] != letter:
                    conflicts.append(f"'{tok}' -> '{mapping[tok]}' and '{letter}'")
            else:
                mapping[tok] = letter

        if conflicts:
            print(f"  CONFLICTS: {conflicts}")
            continue

        print(f"  Knightmare mapping (no conflicts): {mapping}")
        print(f"  Assigned letters: {len(mapping)} tokens -> {len(set(mapping.values()))} unique letters")

        # Corpus analysis
        all_tokens = tokenize_checkerboard(all_digits, modifiers)
        total = len(all_tokens)
        counts = Counter(all_tokens)
        n_unique = len(counts)

        print(f"  Corpus: {total} tokens, {n_unique} unique")
        print(f"  Avg digits/token: {len(all_digits)/total:.3f}")

        # Frequency distribution
        print(f"\n  Token frequencies (top 30):")
        for tok, count in counts.most_common(30):
            pct = count / total * 100
            assigned = mapping.get(tok, '?')
            print(f"    '{tok}': {count:5d} ({pct:5.1f}%) -> {assigned}")

        # Compute chi-squared against German
        freqs_pct = {t: c/total*100 for t, c in counts.items()}
        chi2 = chi_squared_german(freqs_pct, n_unique)
        print(f"\n  Chi-squared vs German: {chi2:.1f}")

        # IC analysis
        ic = compute_ic(all_tokens)
        ratio = ic_ratio(ic, n_unique)
        print(f"  IC = {ic:.6f}, ratio = {ratio:.4f}")


print("\n" + "=" * 70)
print("4. WORD-LEVEL SUBSTITUTION ANALYSIS")
print("=" * 70)

# The Knightmare text has spaces: "3478 67 90871 97664 3466 0 345"
# What if the books also have word boundaries but unmarked?
# Check: are the Knightmare word codes frequent patterns in the books?

word_codes = {
    '3478': 'BE', '67': 'A', '90871': 'WIT',
    '97664': 'THAN', '3466': 'BE', '0': 'A', '345': 'FOOL'
}

print("\nKnightmare word codes in corpus:")
for code, word in word_codes.items():
    count = all_digits.count(code)
    # Expected by random chance
    expected = len(all_digits) * (0.1 ** len(code))
    ratio = count / expected if expected > 0 else float('inf')
    print(f"  '{code}' = {word}: {count} occurrences (expected {expected:.1f}, ratio {ratio:.1f}x)")

# Note: "BE" maps to both 3478 and 3466 - homophonic at word level?
print(f"\n  'BE' has two codes: '3478' and '3466'")
print(f"  'A' has two codes: '67' and '0'")

# If word-level, look for repeated substrings that could be common words
print("\n  Most common substrings of various lengths:")
for length in [2, 3, 4, 5]:
    substr_counts = Counter()
    for i in range(len(all_digits) - length + 1):
        substr_counts[all_digits[i:i+length]] += 1

    print(f"\n  Length {length}:")
    for substr, count in substr_counts.most_common(10):
        print(f"    '{substr}': {count}")


print("\n" + "=" * 70)
print("5. TRIPLE ROW MARKER AND MIXED-LENGTH SEARCH")
print("=" * 70)

# What if there are 1-digit, 2-digit, AND 3-digit codes?
# E.g., certain digits always start 3-digit codes

# Try: prefix digits that require 2 MORE digits after them
# This would allow encoding more symbols
print("\nSearching for mixed 1/2/3-digit encoding...")

# Approach: certain digits are "immediate" (1-digit code),
# certain are "prefix" (need 1 more digit),
# certain are "double prefix" (need 2 more digits)

# For Knightmare "347867908719766434660345" = 17 letters
# Try simple split: which way to parse 24 digits into 17 tokens?
# 17 tokens from 24 digits means 24-17 = 7 "extra" digits consumed by multi-digit codes
# So we need 7 two-digit codes and 10 one-digit codes, OR
# 5 two-digit + 1 three-digit + 11 one-digit, etc.

from itertools import product

def all_tokenizations(text, max_len=3):
    """Generate all possible tokenizations of text into tokens of length 1 to max_len."""
    if not text:
        yield []
        return
    for length in range(1, min(max_len + 1, len(text) + 1)):
        token = text[:length]
        for rest in all_tokenizations(text[length:], max_len):
            yield [token] + rest

# Count tokenizations of Knightmare into exactly 17 tokens
count_17 = 0
valid_tokenizations = []

# This could be slow, let's use dynamic programming
def count_tokenizations_dp(text, target_tokens, max_token_len=3):
    """Find all tokenizations of text into exactly target_tokens tokens."""
    n = len(text)
    # dp[i][j] = list of ways to tokenize text[:i] into j tokens
    # Too memory-intensive to store all; just count first

    # dp[i][j] = number of ways
    dp = [[0] * (target_tokens + 1) for _ in range(n + 1)]
    dp[0][0] = 1

    for i in range(n):
        for j in range(target_tokens):
            if dp[i][j] == 0:
                continue
            for l in range(1, min(max_token_len + 1, n - i + 1)):
                dp[i + l][j + 1] += dp[i][j]

    return dp[n][target_tokens]

n_ways = count_tokenizations_dp(knightmare, n_letters, max_token_len=3)
print(f"\nWays to split Knightmare into 17 tokens (max 3 digits each): {n_ways}")

# That's a lot. Let's add constraints.
# Constraint: consistent encoding (each position in text gets the same treatment)
# This means: certain DIGITS always start multi-digit tokens

# Actually, let me enumerate a subset and check for consistency
def find_tokenizations(text, target_tokens, max_len=3):
    """Find all tokenizations into exactly target_tokens tokens."""
    n = len(text)
    results = []

    def backtrack(pos, tokens):
        if len(tokens) == target_tokens:
            if pos == n:
                results.append(list(tokens))
            return
        if pos >= n:
            return
        remaining_chars = n - pos
        remaining_tokens = target_tokens - len(tokens)
        if remaining_chars < remaining_tokens or remaining_chars > remaining_tokens * max_len:
            return
        for l in range(1, min(max_len + 1, remaining_chars + 1)):
            tokens.append(text[pos:pos+l])
            backtrack(pos + l, tokens)
            tokens.pop()

    backtrack(0, [])
    return results

print(f"\nEnumerating tokenizations...")
all_toks = find_tokenizations(knightmare, n_letters, max_len=3)
print(f"Found {len(all_toks)} tokenizations")

# Check each for internal consistency (same token = same letter, different tokens = different letters)
consistent = []
for toks in all_toks:
    mapping = {}
    reverse_mapping = {}  # letter -> tokens
    valid = True

    for tok, letter in zip(toks, plaintext):
        if tok in mapping:
            if mapping[tok] != letter:
                valid = False
                break
        else:
            mapping[tok] = letter

        if letter in reverse_mapping:
            reverse_mapping[letter].add(tok)
        else:
            reverse_mapping[letter] = {tok}

    if valid:
        consistent.append({
            'tokens': toks,
            'mapping': mapping,
            'reverse': reverse_mapping,
            'n_unique_tokens': len(set(toks)),
            'token_lengths': [len(t) for t in toks]
        })

print(f"Consistent tokenizations (same token -> same letter): {len(consistent)}")

# Filter: also require that same letter maps to at most 2 different tokens (homophonic)
strict = [c for c in consistent if all(len(v) <= 3 for v in c['reverse'].values())]
print(f"With homophonic limit (≤3 codes per letter): {len(strict)}")

# Show best candidates sorted by number of unique tokens (closest to 26 = full alphabet)
if strict:
    strict.sort(key=lambda x: -x['n_unique_tokens'])
    print(f"\nTop candidates (most unique tokens):")
    for i, s in enumerate(strict[:15]):
        lengths = s['token_lengths']
        n1 = lengths.count(1)
        n2 = lengths.count(2)
        n3 = lengths.count(3)
        print(f"\n  #{i+1}: {s['n_unique_tokens']} unique tokens ({n1} single, {n2} double, {n3} triple)")
        print(f"    Tokens: {s['tokens']}")
        print(f"    Mapping: {s['mapping']}")

        # Check if there's a pattern in which digits start multi-digit tokens
        multi_starters = set()
        for tok in s['tokens']:
            if len(tok) > 1:
                multi_starters.add(int(tok[0]))
        single_digits = set()
        for tok in s['tokens']:
            if len(tok) == 1:
                single_digits.add(int(tok))

        overlap = multi_starters & single_digits
        print(f"    Multi-digit starters: {sorted(multi_starters)}")
        print(f"    Single-digit codes: {sorted(single_digits)}")
        if overlap:
            print(f"    OVERLAP (ambiguous): {sorted(overlap)}")
        else:
            print(f"    NO OVERLAP -> valid checkerboard encoding!")

            # Test this encoding on corpus
            markers_for_test = multi_starters
            corp_tokens = tokenize_checkerboard(all_digits, markers_for_test)
            corp_ic = compute_ic(corp_tokens)
            corp_unique = len(Counter(corp_tokens))
            corp_ratio = ic_ratio(corp_ic, corp_unique)
            print(f"    Corpus: {len(corp_tokens)} tokens, {corp_unique} unique, IC ratio={corp_ratio:.4f}")


print("\n" + "=" * 70)
print("6. FACEBOOK PAIRS AS WORD CODES")
print("=" * 70)

# Facebook data: Left (L) and Right (R) numbers with R ≈ 0.593*L + 25.28
# If these are word codes in the cipher, what properties do they have?

# From README-469.md, known Facebook pairs
fb_pairs = [
    (75, 67), (94, 86), (103, 86), (113, 90), (140, 102),
    (147, 119), (156, 118), (201, 143), (211, 149), (223, 155),
    (242, 173), (259, 179), (341, 227), (344, 232), (359, 233),
    (421, 268), (444, 283), (448, 289), (460, 293), (526, 335),
    (632, 399), (739, 467), (795, 494)
]

print(f"\nFacebook pairs: {len(fb_pairs)} pairs")
print(f"\nChecking if pair numbers appear as substrings in books:")

for L, R in fb_pairs[:10]:
    L_str = str(L)
    R_str = str(R)
    L_count = all_digits.count(L_str)
    R_count = all_digits.count(R_str)
    print(f"  L={L} ({L_count}x), R={R} ({R_count}x)")

# Are Facebook numbers positions/indices in the digit string?
print(f"\nFacebook L values as positions in concatenated text:")
for L, R in fb_pairs[:10]:
    if L < len(all_digits):
        context = all_digits[max(0,L-3):L+4]
        print(f"  Position {L}: ...{context}... (digit at L: '{all_digits[L]}')")

# Differences between pairs
print(f"\nDifferences (L - R) for each pair:")
diffs = [L - R for L, R in fb_pairs]
print(f"  {diffs}")
print(f"  Set of diffs: {sorted(set(diffs))}")
print(f"  Most common diff: {Counter(diffs).most_common(5)}")

# L - R relationship
print(f"\nL - R values:")
for L, R in fb_pairs:
    diff = L - R
    ratio = L / R if R else 0
    print(f"  L={L:4d}, R={R:4d}, L-R={diff:4d}, L/R={ratio:.4f}")


print("\n" + "=" * 70)
print("7. DIGIT PATTERN IN KNIGHTMARE WORDS")
print("=" * 70)

# Look at the digit patterns in the Knightmare word codes
words = [('3478', 'BE'), ('67', 'A'), ('90871', 'WIT'),
         ('97664', 'THAN'), ('3466', 'BE'), ('0', 'A'), ('345', 'FOOL')]

print("\nDigit sum and product analysis of word codes:")
for code, word in words:
    digits = [int(d) for d in code]
    dsum = sum(digits)
    dprod = 1
    for d in digits:
        dprod *= d if d > 0 else 1  # skip 0 in product

    print(f"  '{code}' = {word}: sum={dsum}, prod={dprod}, len={len(code)}")

    # Check if digit sum mod 26 maps to anything
    pos = dsum % 26
    letter = chr(ord('A') + pos)
    print(f"    sum mod 26 = {pos} = '{letter}'")

    # Check base representations
    try:
        val = int(code)
        print(f"    decimal value = {val}")
        print(f"    mod 26 = {val % 26} = '{chr(ord('A') + val % 26)}'")
        print(f"    mod 29 = {val % 29}")
    except:
        pass

# Check if word code values mod 26 map to first letter of word
print(f"\nDo decimal values mod N map to word's first letter?")
for mod_val in [26, 29, 100]:
    results = []
    for code, word in words:
        val = int(code) % mod_val
        first_letter_pos = ord(word[0]) - ord('A')
        results.append((code, word, val, first_letter_pos, val == first_letter_pos))

    matches = sum(1 for r in results if r[4])
    print(f"\n  mod {mod_val}: {matches}/{len(words)} match first letter")
    for code, word, val, flp, match in results:
        print(f"    {code} = {word}: val%{mod_val}={val}, first_letter_pos={flp}, match={match}")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
