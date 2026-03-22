"""
Deep analysis of straddling checkerboard findings and homophonic encoding.
Key question: Why does the (0,3) checkerboard give IC 2.75 (way above German 1.72)?
And: Can a HOMOPHONIC straddling checkerboard work?
"""

import json
from collections import Counter
import math

with open('books.json', 'r') as f:
    books = json.load(f)

all_digits = ''.join(books)

# German letter frequencies
german_freq_sorted = [
    ('E', 16.4), ('N', 9.8), ('I', 7.6), ('S', 7.3), ('R', 7.0),
    ('A', 6.5), ('T', 6.2), ('D', 5.1), ('H', 4.8), ('U', 4.2),
    ('L', 3.4), ('C', 3.1), ('G', 3.0), ('M', 2.5), ('O', 2.5),
    ('B', 1.9), ('W', 1.9), ('F', 1.7), ('K', 1.2), ('Z', 1.1),
    ('P', 0.8), ('V', 0.7), ('J', 0.3), ('Y', 0.0), ('X', 0.0),
    ('Q', 0.0)
]

def tokenize(text, markers):
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
    counts = Counter(tokens)
    n = len(tokens)
    if n <= 1:
        return 0
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1))


print("=" * 70)
print("1. WHY IS CHECKERBOARD IC SO HIGH?")
print("=" * 70)

# The (0,3) checkerboard gives IC 2.75. German monoalphabetic would be ~1.72.
# IC > 1.72 suggests FEWER effective symbols or MORE concentrated distribution.

markers_03 = {0, 3}
tokens_03 = tokenize(all_digits, markers_03)
counts_03 = Counter(tokens_03)
total_03 = len(tokens_03)

print(f"\nCheckerboard (0,3): {total_03} tokens, {len(counts_03)} unique")

# The issue: 8 single-digit codes absorb ~87% of tokens
single_count = sum(counts_03[str(d)] for d in range(10) if d not in markers_03)
double_count = total_03 - single_count
print(f"Single-digit tokens: {single_count} ({single_count/total_03*100:.1f}%)")
print(f"Double-digit tokens: {double_count} ({double_count/total_03*100:.1f}%)")

# In German, top 8 letters = E+N+I+S+R+A+T+D = 64.2%
# Our top 8 single-digit codes = 87%. Way too high.
# This means the markers 0,3 are too rare to split enough tokens.

# What if we need MORE markers to balance the distribution?
print(f"\nBalancing test: how many markers to get ~64% single-digit?")
for n_mark in range(1, 6):
    from itertools import combinations
    for marks in combinations(range(10), n_mark):
        marks_set = set(marks)
        tokens = tokenize(all_digits, marks_set)
        counts = Counter(tokens)
        total = len(tokens)
        single = sum(counts[str(d)] for d in range(10) if d not in marks_set)
        pct = single / total * 100
        if 60 <= pct <= 68:
            ic = compute_ic(tokens)
            n_unique = len(counts)
            ratio = ic / (1.0 / n_unique)
            print(f"  Markers={marks}: single={pct:.1f}%, unique={n_unique}, IC ratio={ratio:.3f}")


print("\n" + "=" * 70)
print("2. HOMOPHONIC STRADDLING CHECKERBOARD")
print("=" * 70)

# In a HOMOPHONIC cipher, multiple codes map to the same letter.
# In a straddling checkerboard, this could mean:
# - Both a single-digit code AND a double-digit code map to 'E'
# - This balances frequencies (the single-digit 'E' is very common,
#   but the double-digit 'E' absorbs the excess)

# For the Knightmare with markers (3,7):
# Tokens: ['34', '78', '6', '79', '0', '8', '71', '9', '76', '6', '4', '34', '6', '6', '0', '34', '5']
# Plaintext: B  E  A   W  I  T   T  H   A  N  B   E  A  F  O   O  L

# Token -> letter mapping:
# 34 -> B, E, O  (3 different letters!)
# 78 -> E
# 6 -> A, N, F   (3 different letters!)
# 79 -> W
# 0 -> I, O      (2 different letters!)
# 8 -> T
# 71 -> T
# 9 -> H
# 76 -> A
# 4 -> B
# 5 -> L

# This has CONFLICTS (same token -> different letters), which is DIFFERENT from homophonic.
# In homophonic, different tokens -> same letter (one-to-many), not same token -> different letters.
# Having same token -> different letters means the cipher is AMBIGUOUS = undecipherable without context.

# Unless... the cipher uses CONTEXT to disambiguate.
# Or unless we have the wrong crib mapping.

print("\nKnightmare with markers (3,7):")
knightmare = "347867908719766434660345"
tokens_km = tokenize(knightmare, {3, 7})
plaintext = "BEAWITTHANBEAFOOL"

print(f"Tokens: {tokens_km}")
print(f"Letters: {list(plaintext)}")

# Check conflicts
tok_to_letters = {}
for tok, letter in zip(tokens_km, plaintext):
    if tok not in tok_to_letters:
        tok_to_letters[tok] = set()
    tok_to_letters[tok].add(letter)

print(f"\nToken-to-letter conflicts:")
for tok, letters in sorted(tok_to_letters.items()):
    status = "CONFLICT" if len(letters) > 1 else "OK"
    print(f"  '{tok}' -> {letters}  [{status}]")

# How many conflicts?
n_conflicts = sum(1 for v in tok_to_letters.values() if len(v) > 1)
print(f"\n{n_conflicts} conflicting tokens out of {len(tok_to_letters)} unique tokens")
print("This RULES OUT a simple monoalphabetic or homophonic substitution with markers (3,7)")


print("\n" + "=" * 70)
print("3. THE 27-DIGIT VERSION REVISITED")
print("=" * 70)

# The 27-digit version had 4,924 consistent letter-level solutions
# 27-digit: 347867090871097664346600345
# 24-digit: 347867908719766434660345

# The differences:
km24 = "347867908719766434660345"
km27 = "347867090871097664346600345"

print(f"24-digit: {km24}")
print(f"27-digit: {km27}")
print(f"Difference: {len(km27) - len(km24)} extra digits")

# Where are the extra digits?
# Let's align them
# 24: 3478 67  90871  97664  3466  0  345
# 27: 3478 67 090871 097664 34660 0  345
# The 27-digit version has leading zeros added to some words!

# Actually the 27-digit version treats it as a continuous stream without spaces.
# Let me check: in the 27-digit version, there are 4,924 consistent solutions.
# Each of those solutions defines a tokenization and a mapping.
# Let me check if any of those used a straddling checkerboard pattern.

# For 27 digits -> 17 letters, each token averages 27/17 = 1.588 digits
# That's consistent with a straddling checkerboard!

# Let me enumerate consistent tokenizations for the 27-digit version
print("\nEnumerating consistent tokenizations for 27-digit version...")

def find_consistent_tokenizations(text, target_len, max_tok_len=3):
    """Find tokenizations where same token always maps to same letter."""
    plain = "BEAWITTHANBEAFOOL"
    results = []

    def backtrack(pos, token_idx, mapping, reverse_map, tokens):
        if token_idx == target_len:
            if pos == len(text):
                results.append((list(tokens), dict(mapping), {k: set(v) for k, v in reverse_map.items()}))
            return
        if pos >= len(text):
            return

        remaining_chars = len(text) - pos
        remaining_tokens = target_len - token_idx
        if remaining_chars < remaining_tokens or remaining_chars > remaining_tokens * max_tok_len:
            return

        letter = plain[token_idx]

        for l in range(1, min(max_tok_len + 1, remaining_chars + 1)):
            tok = text[pos:pos+l]
            # Check consistency
            if tok in mapping:
                if mapping[tok] != letter:
                    continue  # Conflict - skip
            else:
                mapping[tok] = letter

            if letter not in reverse_map:
                reverse_map[letter] = []
            reverse_map[letter].append(tok)

            tokens.append(tok)
            backtrack(pos + l, token_idx + 1, mapping, reverse_map, tokens)
            tokens.pop()

            # Undo
            if mapping.get(tok) == letter and tok not in [t for t in tokens]:
                # Only remove if we added it
                pass
            reverse_map[letter].pop()
            if not reverse_map[letter]:
                del reverse_map[letter]
            if tok in mapping and mapping[tok] == letter:
                # Check if this was the one we added
                still_used = any(t == tok for t in tokens)
                if not still_used:
                    del mapping[tok]

    # This recursive approach has issues with state management
    # Let me use a simpler approach

    results_list = []
    n = len(text)

    def solve(pos, tidx, tok_map, toks):
        if tidx == target_len:
            if pos == n:
                results_list.append((list(toks), dict(tok_map)))
            return
        if pos >= n:
            return

        remaining_c = n - pos
        remaining_t = target_len - tidx
        if remaining_c < remaining_t or remaining_c > remaining_t * max_tok_len:
            return

        letter = plain[tidx]

        for l in range(1, min(max_tok_len + 1, remaining_c + 1)):
            tok = text[pos:pos+l]

            if tok in tok_map:
                if tok_map[tok] != letter:
                    continue
                # Already mapped correctly, proceed
                toks.append(tok)
                solve(pos + l, tidx + 1, tok_map, toks)
                toks.pop()
            else:
                tok_map[tok] = letter
                toks.append(tok)
                solve(pos + l, tidx + 1, tok_map, toks)
                toks.pop()
                del tok_map[tok]

    solve(0, 0, {}, [])
    return results_list

results_27 = find_consistent_tokenizations(km27, 17, max_tok_len=3)
print(f"Consistent tokenizations (27-digit, max 3 digits): {len(results_27)}")

# Filter for those that look like straddling checkerboard (some digits always 1-char, some always prefix)
checkerboard_like = []
for toks, mapping in results_27:
    # Check which digits appear as single-char tokens
    single_digits = set()
    prefix_digits = set()
    for tok in toks:
        if len(tok) == 1:
            single_digits.add(tok)
        elif len(tok) >= 2:
            prefix_digits.add(tok[0])

    # Checkerboard-like: prefix digits never appear as single tokens
    if not (single_digits & prefix_digits):
        checkerboard_like.append((toks, mapping, single_digits, prefix_digits))

print(f"Checkerboard-like (no digit is both single AND prefix): {len(checkerboard_like)}")

for toks, mapping, singles, prefixes in checkerboard_like[:20]:
    print(f"\n  Tokens: {toks}")
    print(f"  Mapping: {mapping}")
    print(f"  Single digits: {sorted(singles)}")
    print(f"  Prefix digits: {sorted(prefixes)}")

    # Test this encoding on corpus
    prefix_set = set(int(d) for d in prefixes)
    corp_tokens = tokenize(all_digits, prefix_set)
    corp_ic = compute_ic(corp_tokens)
    corp_unique = len(Counter(corp_tokens))
    corp_ratio = corp_ic / (1.0 / corp_unique) if corp_unique > 0 else 0
    print(f"  Corpus: {len(corp_tokens)} tokens, {corp_unique} unique, IC ratio={corp_ratio:.3f}")


print("\n" + "=" * 70)
print("4. KEY OBSERVATION: KNIGHTMARE WORD BOUNDARIES")
print("=" * 70)

# In the original NPC text: "3478 67 90871 97664 3466 0 345!"
# These spaces MIGHT indicate actual word boundaries
# But some word codes (90871, 97664, 3466) don't appear in books at all
# While others (3478, 345) appear frequently

# What if the NPC text uses a DIFFERENT encoding than the books?
# Or what if the spaces are just formatting and the actual encoding is different?

# Let me check: does the NPC text share ANY substrings with the books?
print("NPC word codes as substrings in books:")
npc_words = ['3478', '67', '90871', '97664', '3466', '0', '345']
for word in npc_words:
    if len(word) >= 3:
        count = all_digits.count(word)
        # Find positions
        positions = []
        start = 0
        while True:
            pos = all_digits.find(word, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        print(f"  '{word}': {count} times, positions={positions[:10]}{'...' if len(positions)>10 else ''}")

# Check if the NPC text (as continuous string) appears anywhere
npc_continuous = "347867908719766434660345"
for length in range(24, 4, -1):
    found = all_digits.find(npc_continuous[:length])
    if found != -1:
        print(f"\n  Longest NPC prefix in books: '{npc_continuous[:length]}' at position {found}")
        break

# Also check substrings of the NPC text
print(f"\nSubstrings of NPC text found in books:")
for l in range(8, 3, -1):
    for i in range(len(npc_continuous) - l + 1):
        sub = npc_continuous[i:i+l]
        count = all_digits.count(sub)
        if count > 0:
            print(f"  '{sub}' (pos {i}-{i+l}): {count} times in books")
    print()


print("\n" + "=" * 70)
print("5. ENCODING UNIT LENGTH FROM ENTROPY AND MI")
print("=" * 70)

# If we look at mutual information between consecutive groups of K digits,
# the point where MI drops to noise level suggests the encoding unit length

# Compute entropy of K-grams
for k in range(1, 7):
    grams = [all_digits[i:i+k] for i in range(len(all_digits) - k + 1)]
    counts = Counter(grams)
    total = len(grams)
    entropy = -sum((c/total) * math.log2(c/total) for c in counts.values())
    max_entropy = k * math.log2(10)
    efficiency = entropy / max_entropy
    n_unique = len(counts)
    n_possible = 10 ** k

    print(f"  {k}-gram: H={entropy:.3f} bits, max={max_entropy:.3f}, efficiency={efficiency:.3f}, unique={n_unique}/{n_possible}")

# Conditional entropy: H(X_k | X_1...X_{k-1})
print(f"\nConditional entropy (bits added by each new digit):")
prev_h = 0
for k in range(1, 7):
    grams = [all_digits[i:i+k] for i in range(len(all_digits) - k + 1)]
    counts = Counter(grams)
    total = len(grams)
    h = -sum((c/total) * math.log2(c/total) for c in counts.values())
    cond_h = h - prev_h
    max_cond = math.log2(10)  # 3.322 bits
    print(f"  H(d_{k}|d_1..d_{k-1}) = {cond_h:.3f} bits (max {max_cond:.3f}, ratio {cond_h/max_cond:.3f})")
    prev_h = h


print("\n" + "=" * 70)
print("6. POLL ANSWER ANALYSIS")
print("=" * 70)

# From README: Poll answer C was "663 902073 7223 67538 467 80097"
# If spaces are word boundaries:
poll_words = ['663', '902073', '7223', '67538', '467', '80097']
print("Poll answer C word codes in books:")
for word in poll_words:
    count = all_digits.count(word)
    expected = len(all_digits) * (0.1 ** len(word))
    ratio = count / expected if expected > 0 else float('inf')
    print(f"  '{word}': {count} times (expected {expected:.1f}, ratio {ratio:.1f}x)")

# Secret Library cipher: "74032 45331"
secret_words = ['74032', '45331']
print(f"\nSecret Library word codes in books:")
for word in secret_words:
    count = all_digits.count(word)
    expected = len(all_digits) * (0.1 ** len(word))
    print(f"  '{word}': {count} times (expected {expected:.1f})")


print("\n" + "=" * 70)
print("7. FIXED-LENGTH CODE ANALYSIS")
print("=" * 70)

# What if all codes are the same length? Test different fixed lengths.
for code_len in range(1, 6):
    # Split all_digits into groups of code_len
    groups = [all_digits[i:i+code_len] for i in range(0, len(all_digits) - code_len + 1, code_len)]
    counts = Counter(groups)
    n_unique = len(counts)
    total = len(groups)

    ic = sum(c*(c-1) for c in counts.values()) / (total * (total - 1))
    random_ic = 1.0 / n_unique
    ratio = ic / random_ic

    # Number of possible codes
    n_possible = 10 ** code_len

    print(f"\n  Code length {code_len}: {total} codes, {n_unique} unique (of {n_possible} possible)")
    print(f"    IC = {ic:.6f}, ratio = {ratio:.3f}")
    print(f"    Top 10: {counts.most_common(10)}")

    # Check if Knightmare words fit this length
    km_words = ['3478', '67', '90871', '97664', '3466', '0', '345']
    matching = [w for w in km_words if len(w) == code_len]
    if matching:
        print(f"    Knightmare words of this length: {matching}")


print("\n" + "=" * 70)
print("8. BIGRAM TRANSITION ANALYSIS FOR ENCODING BOUNDARIES")
print("=" * 70)

# If there are encoding boundaries, transitions at boundaries should differ
# from transitions within codes. Look for positions where the transition
# pattern changes.

# Compute transition frequency at each offset within a fixed window
print("\nTransition entropy at different pair offsets:")
for offset in range(6):
    transitions = Counter()
    for i in range(offset, len(all_digits) - 1, 1):
        pair = all_digits[i:i+2]
        if len(pair) == 2:
            transitions[pair] += 1

    total = sum(transitions.values())
    h = -sum((c/total) * math.log2(c/total) for c in transitions.values())
    print(f"  Offset {offset}: H = {h:.4f} bits ({len(transitions)} unique pairs)")

# Look for periodicity in transition entropy
print("\nTransition entropy by position mod K:")
for period in [2, 3, 4, 5]:
    print(f"\n  Period {period}:")
    for phase in range(period):
        transitions = Counter()
        for i in range(len(all_digits) - 1):
            if i % period == phase:
                transitions[all_digits[i:i+2]] += 1
        total = sum(transitions.values())
        if total > 0:
            h = -sum((c/total) * math.log2(c/total) for c in transitions.values())
            print(f"    Phase {phase}: H = {h:.4f} bits (n={total})")


print("\n" + "=" * 70)
print("9. DO BOOKS HAVE INTERNAL STRUCTURE?")
print("=" * 70)

# Each of the 70 books is a separate text. Do books start/end with
# specific patterns that might indicate encoding structure?

print("\nBook start/end patterns:")
starts = Counter()
ends = Counter()
for book in books:
    if len(book) >= 3:
        starts[book[:3]] += 1
        ends[book[-3:]] += 1

print(f"\nMost common first 3 digits:")
for pat, count in starts.most_common(10):
    print(f"  '{pat}': {count} books")

print(f"\nMost common last 3 digits:")
for pat, count in ends.most_common(10):
    print(f"  '{pat}': {count} books")

# Book length distribution
lengths = [len(b) for b in books]
print(f"\nBook lengths: min={min(lengths)}, max={max(lengths)}, mean={sum(lengths)/len(lengths):.1f}")
print(f"Lengths mod 2: {Counter(l%2 for l in lengths)}")
print(f"Lengths mod 3: {Counter(l%3 for l in lengths)}")
print(f"Lengths mod 4: {Counter(l%4 for l in lengths)}")
print(f"Lengths mod 5: {Counter(l%5 for l in lengths)}")

# Do books that are contained in other books share alignment?
print("\nBook containment relationships:")
n_contained = 0
for i, b1 in enumerate(books):
    for j, b2 in enumerate(books):
        if i != j and b1 in b2:
            pos = b2.index(b1)
            print(f"  Book {i} ({len(b1)} digits) contained in Book {j} ({len(b2)} digits) at position {pos}")
            n_contained += 1
            if n_contained >= 15:
                break
    if n_contained >= 15:
        break


print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
