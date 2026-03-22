"""
Tibia 469 - CRITICAL CLUE ANALYSIS
====================================
Key missed clues from the s2ward README:

1. The Knightmare NPC text might differ from what we used
   README:  "3478 67 90871 97664 3466 0 345!"
   We used: "3478 67 090871 097664 3466 00 0345"

2. "Tibia" = "1" (a wrinkled bonelord says so)

3. CipSoft shows 469 in PAIRS consistently:
   - Facebook post pairs
   - Honeminas formula (4,3,1,5,3).(3,4,7,8,4)
   - Secret Library: 74032 45331

4. Kharos Library has a scrambled version of a Hellgate book

5. Mathemagic: 1+1=1, 1+1=13, 1+1=49, 1+1=94

6. The bonelord's name: 486486 (NOT "Blinky")

7. "0" is obscene/forbidden
"""

import json
from collections import Counter, defaultdict

with open("books.json", "r") as f:
    books = json.load(f)

all_text = "".join(books)

print("=" * 70)
print("CRITICAL CLUE ANALYSIS")
print("=" * 70)

# ============================================================
# 1. KNIGHTMARE CIPHER TEXT CORRECTION
# ============================================================
print("\n" + "=" * 70)
print("1. KNIGHTMARE CIPHER TEXT - WHICH VERSION IS CORRECT?")
print("=" * 70)

# The s2ward README (the authoritative community source) says:
# 3478 67 90871 97664 3466 0 345!
# Plain: BE A WIT THAN BE A FOOL

# Our previous analysis used:
# 3478 67 090871 097664 3466 00 0345

# Let's test BOTH versions
version_readme = "347867908719766434660345"
version_used = "347867090871097664346600345"
plain = "BEAWITTHANBEAFOOL"

print(f"\n  README version: '{version_readme}' ({len(version_readme)} digits)")
print(f"  Previously used: '{version_used}' ({len(version_used)} digits)")
print(f"  Plaintext:      '{plain}' ({len(plain)} letters)")
print(f"\n  Digits/letter: README={len(version_readme)/len(plain):.3f}, Used={len(version_used)/len(plain):.3f}")

# Check if the README version splits differently
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

print("\n--- Testing README version ---")
solutions_readme = find_splits(version_readme, plain)
print(f"  Found {len(solutions_readme)} consistent solutions")

print("\n--- Testing previously used version ---")
solutions_used = find_splits(version_used, plain)
print(f"  Found {len(solutions_used)} consistent solutions")

# Show sample solutions for README version
if solutions_readme:
    print(f"\n  Sample README solutions (first 10):")
    for i, (mapping, split) in enumerate(solutions_readme[:10]):
        inv = defaultdict(list)
        for code, letter in sorted(mapping.items()):
            inv[letter].append(code)
        map_str = " ".join(f"{l}={'|'.join(codes)}" for l, codes in sorted(inv.items()))
        split_str = "|".join(split)
        print(f"    {i+1}. Split: {split_str}")
        print(f"       Map:   {map_str}")

# ============================================================
# 2. "TIBIA = 1" ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("2. 'TIBIA = 1' - WHAT DOES THIS MEAN?")
print("=" * 70)

# If 1 = "Tibia" (5 letters), this could mean:
# a) Digit 1 represents the WORD "Tibia" (word-level encoding)
# b) The NUMBER 1 represents Tibia (the world/concept)
# c) Something else entirely

# How often does '1' appear?
count_1 = all_text.count('1')
print(f"\n  Digit '1' appears {count_1} times ({count_1/len(all_text)*100:.1f}% of text)")
print(f"  If each '1' = 'Tibia', that's way too many occurrences")
print(f"  More likely: '1' is the NUMBER for Tibia as a concept, not as text")
print(f"  Or: the bonelord 469 language uses '1' where we would say 'Tibia'")

# But this is still a clue about the encoding system!
# What if the language works at a WORD level, not letter level?

# ============================================================
# 3. PAIRS HYPOTHESIS - DEEP ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("3. PAIRS HYPOTHESIS (CipSoft's strongest hint)")
print("=" * 70)

# CipSoft hints that the text should be read in PAIRS
# The Honeminas formula: (4,3,1,5,3).(3,4,7,8,4) = dot product
# Facebook post: pairs of 3-digit numbers
# Secret Library: 74032 45331 (two 5-digit numbers)

# What if we read the books as PAIRS of consecutive digits?
# And each pair maps to something via an operation (not lookup)?

# Test: pair operation A*10+B (just the pair as a 2-digit number)
# Already tested as simple substitution

# Test: pair operation A+B (sum)
# Already tested in mod analysis

# NEW: What if each consecutive pair (A,B) is processed as:
# a dot product or similar mathematical operation?

# Test: A*B product
print("\n--- Pair products (A*B for consecutive digits) ---")
products = []
for i in range(0, len(all_text) - 1, 2):
    a, b = int(all_text[i]), int(all_text[i+1])
    products.append(a * b)

prod_freq = Counter(products)
print(f"  Product frequency (top 20):")
for prod, count in prod_freq.most_common(20):
    print(f"    {prod:2d}: {count:4d} ({count/len(products)*100:.1f}%)")

# How many unique products?
print(f"\n  Unique products: {len(prod_freq)}")
print(f"  Products that appear: {sorted(prod_freq.keys())}")

# Test: |A-B| absolute difference
print("\n--- Pair differences |A-B| ---")
abs_diffs = []
for i in range(0, len(all_text) - 1, 2):
    a, b = int(all_text[i]), int(all_text[i+1])
    abs_diffs.append(abs(a - b))

diff_freq = Counter(abs_diffs)
print(f"  Difference frequency:")
for d in range(10):
    count = diff_freq.get(d, 0)
    print(f"    |A-B|={d}: {count:4d} ({count/len(abs_diffs)*100:.1f}%)")

# Test: (A+B) mod 5 - bonelord eye connection?
print("\n--- (A+B) mod 5 ---")
sum_mod5 = []
for i in range(0, len(all_text) - 1, 2):
    a, b = int(all_text[i]), int(all_text[i+1])
    sum_mod5.append((a + b) % 5)

sm5_freq = Counter(sum_mod5)
for v in range(5):
    count = sm5_freq.get(v, 0)
    print(f"    (A+B) mod 5 = {v}: {count:4d} ({count/len(sum_mod5)*100:.1f}%)")

# ============================================================
# 4. KHAROS vs HELLGATE COMPARISON
# ============================================================
print("\n" + "=" * 70)
print("4. KHAROS vs HELLGATE LIBRARY - TRANSFORMATION ANALYSIS")
print("=" * 70)

# Hellgate (Isle of Kings copy):
hellgate_iok = "65128896721277889438872151288952196180031145727857261185764219709680579636612527570584521765219727830464876515956461141451988997511216151"

# Kharos Library (Ferumbras Citadel):
kharos = "51595646114145190584521765219727830464879636612527578967212778894388727857261185764217614588952196180031651288899751121615127215196805970"

print(f"\n  Hellgate: {hellgate_iok[:80]}...")
print(f"  Kharos:   {kharos[:80]}...")
print(f"\n  Hellgate length: {len(hellgate_iok)}")
print(f"  Kharos length:   {len(kharos)}")

# Find common substrings
def longest_common_substring(s1, s2, min_len=8):
    """Find all common substrings of length >= min_len."""
    matches = []
    for length in range(min(len(s1), len(s2)), min_len - 1, -1):
        for i in range(len(s1) - length + 1):
            sub = s1[i:i+length]
            j = s2.find(sub)
            if j != -1:
                # Check this isn't inside a previously found match
                is_sub = False
                for m in matches:
                    if sub in m[0]:
                        is_sub = True
                        break
                if not is_sub:
                    matches.append((sub, i, j, length))
    return matches

common = longest_common_substring(hellgate_iok, kharos)
common.sort(key=lambda x: -x[3])

print(f"\n  Common substrings (length >= 8):")
for sub, pos1, pos2, length in common[:15]:
    print(f"    '{sub[:50]}{'...' if len(sub) > 50 else ''}' ({length} digits)")
    print(f"      Hellgate pos {pos1}, Kharos pos {pos2}")

# Check digit-by-digit alignment
print(f"\n--- Alignment attempt ---")
# The Kharos version seems to have chunks rearranged
# Let's find the ordering

# Find where each 10-digit chunk of Hellgate appears in Kharos
print("  Hellgate chunk positions in Kharos:")
for i in range(0, min(len(hellgate_iok), 130), 10):
    chunk = hellgate_iok[i:i+10]
    pos = kharos.find(chunk)
    status = f"pos {pos}" if pos != -1 else "NOT FOUND"
    print(f"    H[{i:3d}:{i+10}] = '{chunk}' -> Kharos: {status}")

# ============================================================
# 5. MATHEMAGIC SEQUENCE
# ============================================================
print("\n" + "=" * 70)
print("5. MATHEMAGIC: 1+1=1, 1+1=13, 1+1=49, 1+1=94")
print("=" * 70)

# Tetranacci sequence: 1, 1, 1, 1, 4, 7, 13, 25, 49, 94, 181, 349, ...
# Each term = sum of previous 4 terms

tetranacci = [1, 1, 1, 1]
for i in range(4, 20):
    tetranacci.append(sum(tetranacci[-4:]))

print(f"\n  Tetranacci sequence: {tetranacci}")
print(f"\n  Mathemagic: 1+1={tetranacci[0]}, 1+1={tetranacci[6]}, 1+1={tetranacci[8]}, 1+1={tetranacci[9]}")
print(f"  Indices used: 0, 6, 8, 9 (or 1, 7, 9, 10 if 1-indexed)")

# Do tetranacci numbers appear in the text?
print(f"\n  Tetranacci numbers in the text:")
for n in tetranacci[:15]:
    count = all_text.count(str(n))
    print(f"    {n}: appears {count}x as substring")

# What about tetranacci mod 10?
tet_mod10 = [t % 10 for t in tetranacci[:30]]
print(f"\n  Tetranacci mod 10: {tet_mod10}")
print(f"  Period detection: ", end="")
for period in range(2, 20):
    if tet_mod10[:period] == tet_mod10[period:2*period]:
        print(f"Period = {period}!")
        break
else:
    # Check if there's a period starting from a later point
    for start in range(1, 10):
        for period in range(2, 15):
            match = True
            for i in range(period):
                if start + i + period >= len(tet_mod10):
                    match = False
                    break
                if tet_mod10[start + i] != tet_mod10[start + i + period]:
                    match = False
                    break
            if match:
                print(f"Period = {period} starting at index {start}")
                break
        else:
            continue
        break
    else:
        print("No short period found")

# ============================================================
# 6. THE HELLGATE 4x4 MATRIX
# ============================================================
print("\n" + "=" * 70)
print("6. HELLGATE 4x4 MATRIX")
print("=" * 70)

matrix = [
    [1, 1, 1, 1],
    [1, 3, 6, 1],
    [1, 1, 4, 1],
    [4, 6, 1, 1]
]

print("\n  Matrix:")
for row in matrix:
    print(f"    {row}")

det = (matrix[0][0] * (matrix[1][1]*(matrix[2][2]*matrix[3][3]-matrix[2][3]*matrix[3][2])
                      -matrix[1][2]*(matrix[2][1]*matrix[3][3]-matrix[2][3]*matrix[3][1])
                      +matrix[1][3]*(matrix[2][1]*matrix[3][2]-matrix[2][2]*matrix[3][1]))
      -matrix[0][1] * (matrix[1][0]*(matrix[2][2]*matrix[3][3]-matrix[2][3]*matrix[3][2])
                      -matrix[1][2]*(matrix[2][0]*matrix[3][3]-matrix[2][3]*matrix[3][0])
                      +matrix[1][3]*(matrix[2][0]*matrix[3][2]-matrix[2][2]*matrix[3][0]))
      +matrix[0][2] * (matrix[1][0]*(matrix[2][1]*matrix[3][3]-matrix[2][3]*matrix[3][1])
                      -matrix[1][1]*(matrix[2][0]*matrix[3][3]-matrix[2][3]*matrix[3][0])
                      +matrix[1][3]*(matrix[2][0]*matrix[3][1]-matrix[2][1]*matrix[3][0]))
      -matrix[0][3] * (matrix[1][0]*(matrix[2][1]*matrix[3][2]-matrix[2][2]*matrix[3][1])
                      -matrix[1][1]*(matrix[2][0]*matrix[3][2]-matrix[2][2]*matrix[3][0])
                      +matrix[1][2]*(matrix[2][0]*matrix[3][1]-matrix[2][1]*matrix[3][0])))

print(f"\n  Determinant: {det}")
print(f"  Row sums: {[sum(row) for row in matrix]}")
print(f"  Col sums: {[sum(matrix[r][c] for r in range(4)) for c in range(4)]}")
print(f"  Diagonal sum: {sum(matrix[i][i] for i in range(4))}")
print(f"  Anti-diag sum: {sum(matrix[i][3-i] for i in range(4))}")
print(f"  Total: {sum(sum(row) for row in matrix)}")
print(f"  Unique values: {sorted(set(v for row in matrix for v in row))}")

# Could this matrix be used for Hill cipher?
# Hill cipher: plaintext pairs are multiplied by the matrix mod N
# With a 4x4 matrix, it would process 4 digits at a time

# Test Hill cipher with this matrix
print("\n--- Hill cipher test (4 digits at a time) ---")
sample = all_text[:40]
print(f"  Input: {sample}")

for mod_n in [10, 26]:
    result = []
    for i in range(0, len(sample) - 3, 4):
        vec = [int(sample[j]) for j in range(i, i+4)]
        out = []
        for r in range(4):
            val = sum(matrix[r][c] * vec[c] for c in range(4)) % mod_n
            out.append(val)
        result.extend(out)

    if mod_n == 26:
        letters = "".join(chr(v + 65) for v in result)
        print(f"  Hill mod {mod_n}: {result[:20]}... -> {letters[:20]}...")
    else:
        print(f"  Hill mod {mod_n}: {result[:20]}...")

# ============================================================
# 7. NAME "486486" ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("7. BONELORD NAME '486486' ANALYSIS")
print("=" * 70)

name = "486486"
print(f"\n  Name: {name}")
print(f"  Palindromic pattern: {name[:3]} repeated")
print(f"  Individual digits: 4, 8, 6, 4, 8, 6")
print(f"  Sum: {sum(int(d) for d in name)} (digital root: {sum(int(d) for d in name) % 9 or 9})")

# Does 486486 appear in any book?
for i, book in enumerate(books):
    pos = book.find(name)
    if pos != -1:
        print(f"  FOUND in Book {i+1} at position {pos}!")

# Does 486 appear?
count_486 = sum(book.count("486") for book in books)
print(f"\n  '486' appears {count_486} times across all books")

# Mathematical properties of 486486
print(f"\n  486486 = 2 * 3 * 7 * 11 * 1053 = 2 * 243243 = 6 * 81081")
print(f"  486486 / 1001 = {486486 / 1001}")  # 1001 = 7*11*13
print(f"  486 = 2 * 3^5 = 2 * 243")

# ============================================================
# 8. PAIRS + HONEMINAS: DIGIT-BY-DIGIT DOT PRODUCT
# ============================================================
print("\n" + "=" * 70)
print("8. HONEMINAS-STYLE DOT PRODUCT ON THE TEXT")
print("=" * 70)

# The Honeminas formula suggests processing 5 digits at a time
# with a dot product against a fixed vector

v1 = [4, 3, 1, 5, 3]  # These are the vectors from the formula
v2 = [3, 4, 7, 8, 4]

print(f"\n  Vector 1: {v1}")
print(f"  Vector 2: {v2}")
print(f"  Dot product v1.v2 = {sum(a*b for a,b in zip(v1,v2))}")

# Process text in groups of 5, compute dot products with v1 and v2
sample = all_text[:200]
print(f"\n--- Processing 5 digits at a time with v1 ---")
results_v1 = []
for i in range(0, len(sample) - 4, 5):
    group = [int(sample[j]) for j in range(i, i+5)]
    dot = sum(a*b for a, b in zip(group, v1))
    results_v1.append(dot)

print(f"  Dot products: {results_v1[:20]}")
print(f"  Range: {min(results_v1)} to {max(results_v1)}")
print(f"  Mod 26: {[d % 26 for d in results_v1[:20]]}")
print(f"  As letters (mod 26): {''.join(chr(d % 26 + 65) for d in results_v1[:20])}")

print(f"\n--- Processing 5 digits at a time with v2 ---")
results_v2 = []
for i in range(0, len(sample) - 4, 5):
    group = [int(sample[j]) for j in range(i, i+5)]
    dot = sum(a*b for a, b in zip(group, v2))
    results_v2.append(dot)

print(f"  Dot products: {results_v2[:20]}")
print(f"  Mod 26: {[d % 26 for d in results_v2[:20]]}")
print(f"  As letters (mod 26): {''.join(chr(d % 26 + 65) for d in results_v2[:20])}")

# What if both vectors are combined?
print(f"\n--- Combined: dot with v1, then take mod to get letter ---")
for mod_n in [26, 29, 36]:
    letters = []
    for i in range(0, len(all_text[:500]) - 4, 5):
        group = [int(all_text[j]) for j in range(i, i+5)]
        dot = sum(a*b for a, b in zip(group, v1))
        if mod_n <= 26:
            letters.append(chr(dot % mod_n + 65))
        else:
            val = dot % mod_n
            if val < 26:
                letters.append(chr(val + 65))
            else:
                letters.append(' ')
    decoded = "".join(letters)
    print(f"  Mod {mod_n}: {decoded[:80]}")

# ============================================================
# 9. FACEBOOK POST PAIRS ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("9. FACEBOOK POST PAIRS - MATHEMATICAL RELATIONSHIP")
print("=" * 70)

# From the README - the pairs from the mirrored image
fb_pairs = [
    (713, 473), (765, 464), (706, 447), (824, 499),
    (975, 595), (937, 530), (726, 431), (729, 447),
    (652, 400), (653, 407), (565, 375), (746, 458),
    (1021, 659), (759, 475), (718, 438), (737, 469),
    (648, 428), (818, 520), (985, 621), (2154, 1307),
    (841, 540), (684, 448), (694, 453),
]

print("\nPair analysis:")
print(f"  {'Left':>6} {'Right':>6} {'Ratio':>7} {'Diff':>6} {'L-R':>6} {'L%R':>5} {'dot':>5}")
print("-" * 55)

for left, right in fb_pairs:
    ratio = left / right if right > 0 else 0
    diff = left - right
    l_mod_r = left % right if right > 0 else 0

    # Digit-wise dot product (if same length)
    l_str, r_str = str(left), str(right)
    if len(l_str) == len(r_str):
        dot = sum(int(a)*int(b) for a, b in zip(l_str, r_str))
    else:
        dot = -1

    print(f"  {left:6d} {right:6d} {ratio:7.4f} {diff:6d} {l_mod_r:6d} {dot:5d}")

# What's the consistent mathematical relationship?
ratios = [l/r for l, r in fb_pairs if r > 0]
print(f"\n  Average ratio L/R: {sum(ratios)/len(ratios):.4f}")
print(f"  Min ratio: {min(ratios):.4f}")
print(f"  Max ratio: {max(ratios):.4f}")

# Could these pairs generate letters via some formula?
print("\n--- Could pairs encode letters? ---")
for formula_name, formula in [
    ("(L-R) mod 26", lambda l, r: (l - r) % 26),
    ("(L+R) mod 26", lambda l, r: (l + r) % 26),
    ("(L*R) mod 26", lambda l, r: (l * r) % 26),
    ("(L xor R) mod 26", lambda l, r: (l ^ r) % 26),
    ("L mod 26", lambda l, r: l % 26),
    ("(L-R) mod 29", lambda l, r: (l - r) % 29),
]:
    results = [formula(l, r) for l, r in fb_pairs]
    if max(results) < 26:
        letters = "".join(chr(v + 65) for v in results)
    else:
        letters = "".join(chr(v + 65) if v < 26 else ' ' for v in results)
    print(f"  {formula_name:20s}: {results[:10]}... = '{letters[:23]}'")

# ============================================================
# 10. COMBINING KNIGHTMARE + TIBIA CLUES
# ============================================================
print("\n" + "=" * 70)
print("10. COMBINING ALL KNOWN PLAINTEXT")
print("=" * 70)

print("\n  Known cipher-plain pairs:")
print("  1. 'Tibia' = 1 (from wrinkled bonelord)")
print("  2. '486486' = bonelord name (not 'Blinky')")
print("  3. Knightmare: BE A WIT THAN BE A FOOL")
print("  4. '469' = the language name")
print("  5. '0' = obscene/forbidden")

# If the Knightmare spacing is meaningful:
print("\n--- If spaces in NPC text are WORD BOUNDARIES ---")
knightmare_words = [("3478", "BE"), ("67", "A"), ("90871", "WIT"),
                     ("97664", "THAN"), ("3466", "BE"), ("0", "A"), ("345", "FOOL")]

print("  Word mappings:")
for cipher_word, plain_word in knightmare_words:
    ratio = len(cipher_word) / len(plain_word) if len(plain_word) > 0 else 0
    print(f"    '{cipher_word}' = '{plain_word}' ({len(cipher_word)} digits / {len(plain_word)} letters = {ratio:.2f} d/l)")

# Note: 0 = "A" and the bonelord says 0 is obscene!
# But "A" is the most common word in English...
# Unless 0 is a SPECIAL code, not the digit zero
print("\n  KEY: '0' = 'A' in the Knightmare crib, but bonelord says 0 is 'obscene'!")
print("  This suggests: '0' is a VALID code (for a common letter/word)")
print("  but it's considered 'rude' in bonelord culture")

# What if the spacing is significant and each space-separated
# group encodes one WORD?
print("\n--- Chayenne's text with hypothetical word boundaries ---")
chayenne = "114514519485611451908304576512282177"
# From the interview, followed by "6612527570584"
print(f"  Text 1: {chayenne}")
print(f"  Text 2: 6612527570584")

# The Wrinkled Bonelord's greetings:
# 485611800364197
# 78572611857643646724
# These have no spaces - are they single words or sentences?
print("\n--- Bonelord greeting analysis ---")
g1 = "485611800364197"
g2 = "78572611857643646724"
print(f"  Greeting 1: {g1} ({len(g1)} digits)")
print(f"  Greeting 2: {g2} ({len(g2)} digits)")

# If these are greetings, possible translations:
# "Hello" (5 letters)
# "Greetings" (9 letters)
# "Welcome" (7 letters)
# "Good day" (7 letters)

for word, expected_len in [("HELLO", 5), ("GREETINGS", 9),
                            ("WELCOME", 7), ("GOODDAY", 7)]:
    ratio = len(g1) / expected_len
    print(f"  If greeting 1 = '{word}': {ratio:.2f} digits/letter")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
