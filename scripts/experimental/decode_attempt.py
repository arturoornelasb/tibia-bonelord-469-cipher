"""
DECODE ATTEMPT: (5*d1 + 5*d2 + 3*d1*d2) mod 29

This formula gives IC ratio = 2.118 and frequency distribution that
closely matches German letter frequencies. Let's test it thoroughly.
"""

import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

with open("books.json") as f:
    books = json.load(f)

combined = "".join(books)

def encode_pair(d1, d2):
    """Apply the formula to a digit pair."""
    return (5*d1 + 5*d2 + 3*d1*d2) % 29

# Build the full 10x10 mapping table
print("=" * 70)
print("ENCODING TABLE: (5*d1 + 5*d2 + 3*d1*d2) mod 29")
print("=" * 70)

print("\n    ", end="")
for d2 in range(10):
    print(f"  d2={d2}", end="")
print()

for d1 in range(10):
    print(f"d1={d1}", end="")
    for d2 in range(10):
        val = encode_pair(d1, d2)
        print(f"  {val:4d}", end="")
    print()

# Which digit pairs map to each value?
print("\n\nReverse mapping (value -> digit pairs):")
val_to_pairs = {}
for d1 in range(10):
    for d2 in range(10):
        val = encode_pair(d1, d2)
        if val not in val_to_pairs:
            val_to_pairs[val] = []
        val_to_pairs[val].append((d1, d2))

for val in sorted(val_to_pairs.keys()):
    pairs = val_to_pairs[val]
    print(f"  {val:2d}: {pairs}")

# =====================================================================
# 1. FULL FREQUENCY MAPPING
# =====================================================================
print("\n" + "=" * 70)
print("1. FREQUENCY-BASED GERMAN MAPPING")
print("=" * 70)

# Decode the full text
decoded_values = []
for i in range(0, len(combined)-1, 2):
    d1, d2 = int(combined[i]), int(combined[i+1])
    decoded_values.append(encode_pair(d1, d2))

# Frequency count
val_freq = Counter(decoded_values)

# German letter frequencies (26 letters)
german_order = 'ENISRATDHULCGMOBWFKZPVJYXQ'  # by frequency

# Sort our values by frequency
text_order = [v for v, c in val_freq.most_common()]

# Create mapping
mapping = {}
for i, val in enumerate(text_order):
    if i < 26:
        mapping[val] = german_order[i]
    else:
        mapping[val] = '?'  # values beyond 26

print(f"\nMapping (value -> German letter by frequency):")
for val in sorted(mapping.keys()):
    cnt = val_freq.get(val, 0)
    pct = cnt / len(decoded_values) * 100
    print(f"  {val:2d} -> '{mapping[val]}' ({cnt:4d} = {pct:.1f}%)")

# Decode text
decoded_text = ''.join(mapping.get(v, '?') for v in decoded_values)
print(f"\nDecoded text (first 300 chars):")
for i in range(0, min(300, len(decoded_text)), 60):
    print(f"  {decoded_text[i:i+60]}")

# =====================================================================
# 2. VERIFY AGAINST KNIGHTMARE CRIB
# =====================================================================
print("\n" + "=" * 70)
print("2. KNIGHTMARE CRIB VERIFICATION")
print("=" * 70)

# Knightmare (README): 3478 67 90871 97664 3466 0 345
# Plaintext: BE A WIT THAN BE A FOOL
knightmare_cipher = "347867908719766434660345"
knightmare_plain = "BEAWITTHANBEAFOOL"

# But the cipher has spaces! If spaces are word boundaries, we need
# to handle single-digit codes like "0" differently
print(f"\nKnightmare cipher (no spaces): {knightmare_cipher}")
print(f"Knightmare plain: {knightmare_plain}")
print(f"Cipher length: {len(knightmare_cipher)}, plain length: {len(knightmare_plain)}")

# Decode as consecutive pairs
km_values = []
for i in range(0, len(knightmare_cipher)-1, 2):
    d1, d2 = int(knightmare_cipher[i]), int(knightmare_cipher[i+1])
    val = encode_pair(d1, d2)
    km_values.append(val)

km_decoded = ''.join(mapping.get(v, '?') for v in km_values)
print(f"\nDecoded (pair alignment 0): {km_decoded}")
print(f"Values: {km_values}")

# Try alignment 1
km_values1 = []
for i in range(1, len(knightmare_cipher)-1, 2):
    d1, d2 = int(knightmare_cipher[i]), int(knightmare_cipher[i+1])
    val = encode_pair(d1, d2)
    km_values1.append(val)

km_decoded1 = ''.join(mapping.get(v, '?') for v in km_values1)
print(f"Decoded (pair alignment 1): {km_decoded1}")

# The cipher has odd length (23 digits after removing spaces)
# If encoding is variable-length, pairs don't cover everything
print(f"\nProblem: cipher without spaces is {len(knightmare_cipher)} digits (odd!)")
print(f"This means strict 2-digit pairing leaves 1 digit unaccounted for")

# What if the Knightmare cipher uses the ORIGINAL spacing?
print(f"\n--- Testing with original spacing ---")
words = ['3478', '67', '90871', '97664', '3466', '0', '345']
plains = ['BE', 'A', 'WIT', 'THAN', 'BE', 'A', 'FOOL']

for cipher_word, plain_word in zip(words, plains):
    print(f"\n  '{cipher_word}' = '{plain_word}' ({len(cipher_word)} digits -> {len(plain_word)} letters)")

    # If even length, decode as pairs
    if len(cipher_word) >= 2:
        vals = []
        for i in range(0, len(cipher_word)-1, 2):
            d1, d2 = int(cipher_word[i]), int(cipher_word[i+1])
            val = encode_pair(d1, d2)
            vals.append(val)
        decoded = ''.join(mapping.get(v, '?') for v in vals)
        print(f"    As pairs: values={vals}, decoded='{decoded}'")

        # What letters SHOULD these values map to?
        print(f"    SHOULD map to: {list(plain_word)}")
        for v, letter in zip(vals, plain_word):
            print(f"      value {v:2d} -> should be '{letter}'")
    else:
        val = int(cipher_word)
        print(f"    Single digit: {val}")
        print(f"    SHOULD map to: '{plain_word}'")

# =====================================================================
# 3. BUILD CORRECT MAPPING FROM KNIGHTMARE
# =====================================================================
print("\n" + "=" * 70)
print("3. KNIGHTMARE-DERIVED MAPPING")
print("=" * 70)

# If 3478 = BE, then pair 34 -> B and pair 78 -> E
# If 67 = A, then pair 67 -> A (but 67 is only one pair for one letter)
# If 97664 = THAN, then 97 -> T, 66 -> H, 4? -> AN?

# This doesn't work cleanly with the pair hypothesis because:
# - '90871' has 5 digits (odd) for WIT (3 letters)
# - '97664' has 5 digits (odd) for THAN (4 letters)
# - '345' has 3 digits (odd) for FOOL (4 letters)

# The variable-length nature means our fixed pair encoding is WRONG
# Let's try a different approach: per-word encoding

# Maybe the words encode numbers, not letters
print("\nTreating cipher words as NUMBERS:")
for cipher_word, plain_word in zip(words, plains):
    n = int(cipher_word)
    print(f"  {n:6d} = '{plain_word}'")
    print(f"    n mod 26 = {n % 26} = '{chr(n % 26 + ord('A'))}'")
    print(f"    n mod 29 = {n % 29}")
    print(f"    digit sum = {sum(int(d) for d in cipher_word)}")
    print(f"    digit product = ", end="")
    prod = 1
    for d in cipher_word:
        prod *= max(1, int(d))  # avoid 0
    print(f"{prod}")

# =====================================================================
# 4. LOOK FOR THE CORRECT VARIABLE-LENGTH ENCODING
# =====================================================================
print("\n" + "=" * 70)
print("4. TESTING ALL SIMPLE NUMERICAL ENCODINGS")
print("=" * 70)

# The key constraint: each word-code maps to a word
# 3478 -> BE, 67 -> A, 90871 -> WIT, etc.
# Could the number itself represent something?

for name, func in [
    ("n mod 26", lambda n: n % 26),
    ("n mod 29", lambda n: n % 29),
    ("digit sum mod 26", lambda n: sum(int(d) for d in str(n)) % 26),
    ("digit sum mod 29", lambda n: sum(int(d) for d in str(n)) % 29),
    ("alternating sum", lambda n: sum((-1)**i * int(d) for i, d in enumerate(str(n)))),
    ("alt sum mod 26", lambda n: sum((-1)**i * int(d) for i, d in enumerate(str(n))) % 26),
]:
    results = []
    for cipher_word, plain_word in zip(words, plains):
        n = int(cipher_word)
        val = func(n)
        results.append((cipher_word, plain_word, val))

    print(f"\n{name}:")
    for cw, pw, val in results:
        letter = chr(val % 26 + ord('A')) if val >= 0 else '?'
        print(f"  {cw:>6s} ({pw:>4s}) -> {val:3d} ({letter})")

# =====================================================================
# 5. DOT PRODUCT WITH HONEMINAS VECTOR
# =====================================================================
print("\n" + "=" * 70)
print("5. HONEMINAS DOT PRODUCT ON KNIGHTMARE WORDS")
print("=" * 70)

v1 = [4, 3, 1, 5, 3]
v2 = [3, 4, 7, 8, 4]

for cipher_word, plain_word in zip(words, plains):
    digits = [int(d) for d in cipher_word]
    print(f"\n  '{cipher_word}' = '{plain_word}' (digits: {digits})")

    # Pad or truncate to length 5 for dot product
    if len(digits) <= 5:
        padded = digits + [0] * (5 - len(digits))
        dot1 = sum(a*b for a, b in zip(padded, v1[:len(digits)]))
        dot2 = sum(a*b for a, b in zip(padded, v2[:len(digits)]))
        print(f"    dot with v1 (padded): {dot1}, mod 26 = {dot1 % 26} = '{chr(dot1 % 26 + ord('A'))}'")
        print(f"    dot with v2 (padded): {dot2}, mod 26 = {dot2 % 26} = '{chr(dot2 % 26 + ord('A'))}'")

# =====================================================================
# 6. IS THE CIPHER ACTUALLY BASE-29?
# =====================================================================
print("\n" + "=" * 70)
print("6. TREATING WORD-CODES AS BASE-29 NUMBERS")
print("=" * 70)

# What if each digit represents a base-29 digit?
# But digits only go 0-9, so each digit IS its value
# A word of N digits: sum(d_i * 29^i) or sum(d_i * 29^(N-1-i))

for cipher_word, plain_word in zip(words, plains):
    digits = [int(d) for d in cipher_word]
    # Big-endian
    val_be = 0
    for d in digits:
        val_be = val_be * 29 + d
    # Little-endian
    val_le = 0
    for d in reversed(digits):
        val_le = val_le * 29 + d

    print(f"\n  '{cipher_word}' = '{plain_word}'")
    print(f"    Base-29 big-endian: {val_be} (mod 26 = {val_be % 26} = '{chr(val_be % 26 + ord('A'))}')")

# =====================================================================
# 7. VERIFY THE IC RESULT - Is it real language structure?
# =====================================================================
print("\n" + "=" * 70)
print("7. BIGRAM IC TEST (distinguish real language from coincidence)")
print("=" * 70)

# The single-symbol IC could be artificially high due to the formula
# concentrating values. Test bigram IC to verify.

# Bigram IC of the decoded values
bigrams = [(decoded_values[i], decoded_values[i+1]) for i in range(len(decoded_values)-1)]
bigram_freq = Counter(bigrams)
n_bg = len(bigrams)
unique_bg = len(bigram_freq)
ic_bg = sum(c*(c-1) for c in bigram_freq.values()) / (n_bg*(n_bg-1))

# For a random text with the SAME unigram distribution, expected bigram IC is:
# sum(p_i * p_j)^2 approximately... or just compare to random
import random
random.seed(42)

# Generate random text with same unigram frequencies
freq_list = []
for val, cnt in val_freq.items():
    freq_list.extend([val] * cnt)
random.shuffle(freq_list)
rand_bigrams = [(freq_list[i], freq_list[i+1]) for i in range(len(freq_list)-1)]
rand_bg_freq = Counter(rand_bigrams)
n_rbg = len(rand_bigrams)
ic_rbg = sum(c*(c-1) for c in rand_bg_freq.values()) / (n_rbg*(n_rbg-1))

print(f"\nBigram IC (actual text): {ic_bg:.8f}")
print(f"Bigram IC (shuffled):   {ic_rbg:.8f}")
print(f"Ratio actual/shuffled:  {ic_bg/ic_rbg:.4f}")
print(f"\nIf ratio > 1.3, it suggests REAL language structure beyond frequency")

# =====================================================================
# 8. WHAT IF IT'S MOD 29 (29 symbols, not 26)?
# =====================================================================
print("\n" + "=" * 70)
print("8. 29-SYMBOL ALPHABET HYPOTHESIS")
print("=" * 70)

# German has 26 letters + 3 umlauts (ae, oe, ue) = 29 symbols!
# This would explain why the formula uses mod 29
german_29 = 'ENISRATDHULCGMOBWFKZPVJYXQAOU'  # last 3 = umlauts

print(f"\nGerman 26 + umlauts = 29 symbols: {german_29}")
print(f"(A=ae, O=oe, U=ue would be the 27th, 28th, 29th)")

# Remap using 29 symbols
mapping_29 = {}
for i, val in enumerate(text_order):
    if i < 29:
        mapping_29[val] = german_29[i]
    else:
        mapping_29[val] = '?'

decoded_29 = ''.join(mapping_29.get(v, '?') for v in decoded_values)
print(f"\nDecoded with 29 symbols (first 300 chars):")
for i in range(0, min(300, len(decoded_29)), 60):
    print(f"  {decoded_29[i:i+60]}")

# =====================================================================
# 9. CHECK IF FORMULA WORKS AT ALL ALIGNMENTS
# =====================================================================
print("\n" + "=" * 70)
print("9. ALIGNMENT SENSITIVITY")
print("=" * 70)

# Test if the IC holds when we shift alignment by 1
for offset in [0, 1]:
    vals = []
    for i in range(offset, len(combined)-1, 2):
        d1, d2 = int(combined[i]), int(combined[i+1])
        vals.append(encode_pair(d1, d2))
    vf = Counter(vals)
    nv = len(vals)
    ic = sum(c*(c-1) for c in vf.values()) / (nv*(nv-1))
    ic_rand = 1.0/29
    print(f"Offset {offset}: IC={ic:.6f}, ratio={ic/ic_rand:.4f}, unique={len(vf)}")

# =====================================================================
# 10. PER-BOOK DECODING
# =====================================================================
print("\n" + "=" * 70)
print("10. PER-BOOK DECODING (first 5 books)")
print("=" * 70)

for idx in range(5):
    book = books[idx]
    bvals = []
    for i in range(0, len(book)-1, 2):
        d1, d2 = int(book[i]), int(book[i+1])
        bvals.append(encode_pair(d1, d2))

    decoded_book = ''.join(mapping.get(v, '?') for v in bvals)
    print(f"\nBook {idx+1} ({len(book)} digits -> {len(bvals)} chars):")
    print(f"  {decoded_book[:80]}")

# =====================================================================
# 11. SEARCH FOR COMMON GERMAN WORDS IN DECODED TEXT
# =====================================================================
print("\n" + "=" * 70)
print("11. GERMAN WORD SEARCH")
print("=" * 70)

german_words = [
    'DER', 'DIE', 'DAS', 'UND', 'IST', 'EIN', 'EINE', 'VON', 'MIT', 'AUF',
    'SICH', 'DEN', 'DEM', 'FUR', 'NICHT', 'HAT', 'WAR', 'ALS', 'SIE', 'ZUR',
    'AUCH', 'NUR', 'MAN', 'WIR', 'MIR', 'DIR', 'SEIN', 'WIRD', 'WER', 'WAS',
    'KANN', 'MUS', 'ALLE', 'WENN', 'DANN', 'NOCH', 'BIS', 'ODE', 'UNS', 'IHR',
    'TOD', 'MACHT', 'LEBEN', 'KRIEG', 'FEIND', 'AUGE', 'BUCH', 'RUNE',
    'THE', 'AND', 'ARE', 'FOR', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS',
    'DEATH', 'MAGIC', 'SPELL', 'BONE', 'LORD', 'POWER', 'EYE', 'BOOK',
    'NECRO', 'UNDEAD', 'BLINK', 'TIBIA'
]

found_words = []
for word in german_words:
    count = decoded_text.count(word)
    # Expected by chance
    expected = len(decoded_text) / (26 ** len(word))
    if count > 0:
        ratio = count / expected if expected > 0 else float('inf')
        found_words.append((word, count, expected, ratio))

found_words.sort(key=lambda x: -x[3])
print(f"\nWords found (sorted by ratio over expected):")
for word, count, expected, ratio in found_words[:30]:
    marker = " ***" if ratio > 3 else ""
    print(f"  '{word}': {count} times (expected {expected:.1f}, ratio={ratio:.1f}x){marker}")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
