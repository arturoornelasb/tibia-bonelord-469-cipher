"""
PAIRS HYPOTHESIS - Comprehensive Investigation

CipSoft has consistently hinted that 469 comes in PAIRS:
- Facebook post: 23+ pairs with left ~1.6x right
- Honeminas formula: (4,3,1,5,3).(3,4,7,8,4) = two 5-vectors
- Secret Library: "74032 45331" (left > right)
- Bonelord name: 486486 = "486" repeated (a pair!)
- Poll: "663 902073 7223 67538 467 80097" (6 groups)
- Knightmare: "3478 67 90871 97664 3466 0 345" (7 groups)

The key question: HOW do we extract pairs from the continuous digit stream?
"""

import json
import sys
from collections import Counter
from math import gcd

# Force UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

with open("books.json") as f:
    books = json.load(f)

combined = "".join(books)

print("=" * 70)
print("PAIRS HYPOTHESIS - COMPREHENSIVE ANALYSIS")
print("=" * 70)

# =====================================================================
# 1. WORD-LEVEL ANALYSIS: What if spaces in NPC text = word boundaries?
# =====================================================================
print("\n" + "=" * 70)
print("1. WORD-LEVEL ENCODING HYPOTHESIS")
print("=" * 70)

# Known word-level mappings from Knightmare
word_map = {
    '3478': 'BE',
    '67': 'A',
    '90871': 'WIT',
    '97664': 'THAN',
    '3466': 'BE',
    '0': 'A',
    '345': 'FOOL'
}

# Look for these word codes in the books
print("\nSearching for known word codes in books:")
for code, word in word_map.items():
    count = 0
    positions = []
    for i in range(len(combined) - len(code) + 1):
        if combined[i:i+len(code)] == code:
            count += 1
            if len(positions) < 5:
                positions.append(i)
    print(f"  '{code}' ({word}): {count} times, first at: {positions[:5]}")

# Poll answer C: 663 902073 7223 67538 467 80097
# If this is also word-level encoding of a sentence...
print("\n--- Poll answer C word codes ---")
poll_words = ['663', '902073', '7223', '67538', '467', '80097']
print(f"  Words: {poll_words}")
print(f"  Word lengths: {[len(w) for w in poll_words]}")
print(f"  Total digits: {sum(len(w) for w in poll_words)}")

# Secret library: 74032 45331
print("\n--- Secret Library word codes ---")
secret_words = ['74032', '45331']
print(f"  Words: {secret_words}")
print(f"  Word lengths: {[len(w) for w in secret_words]}")

# Elder bonelord: 659978 54764 and 653768764
print("\n--- Elder Bonelord ---")
print(f"  '659978 54764' -> 'Inferior creatures, bow before my power!' or greeting")
print(f"  '653768764' -> same or different phrase")
print(f"  Note: 659978/54764 -> meanings unknown")

# Wrinkled Bonelord greetings
print("\n--- Wrinkled Bonelord greetings (no spaces = single words?) ---")
greetings = ['485611800364197', '78572611857643646724']
for g in greetings:
    print(f"  '{g}' ({len(g)} digits)")

# =====================================================================
# 2. DIGIT-PAIR INTERLEAVING
# =====================================================================
print("\n" + "=" * 70)
print("2. DIGIT-PAIR INTERLEAVING")
print("=" * 70)

# What if we split the text into two streams by position?
even_stream = combined[::2]  # positions 0,2,4,...
odd_stream = combined[1::2]   # positions 1,3,5,...

print(f"\nEven positions ({len(even_stream)} digits): first 50 = {even_stream[:50]}")
print(f"Odd positions ({len(odd_stream)} digits): first 50 = {odd_stream[:50]}")

# Check digit frequencies in each stream
print("\nFrequency comparison:")
for d in range(10):
    even_pct = even_stream.count(str(d)) / len(even_stream) * 100
    odd_pct = odd_stream.count(str(d)) / len(odd_stream) * 100
    diff = abs(even_pct - odd_pct)
    marker = " ***" if diff > 3 else ""
    print(f"  Digit {d}: even={even_pct:.1f}% odd={odd_pct:.1f}% diff={diff:.1f}%{marker}")

# =====================================================================
# 3. CONSECUTIVE PAIR ANALYSIS (digit pairs as units)
# =====================================================================
print("\n" + "=" * 70)
print("3. CONSECUTIVE DIGIT PAIRS AS ENCODING UNITS")
print("=" * 70)

# Take consecutive pairs: (d0,d1), (d2,d3), (d4,d5)...
pairs_text = []
for i in range(0, len(combined)-1, 2):
    pairs_text.append(combined[i:i+2])

pair_freq = Counter(pairs_text)
print(f"\nTotal pairs: {len(pairs_text)}")
print(f"Unique pairs: {len(pair_freq)}")
print(f"\nMost common pairs:")
for p, c in pair_freq.most_common(26):
    pct = c / len(pairs_text) * 100
    print(f"  {p}: {c} ({pct:.1f}%)")

# If pairs map to letters, most common should match language frequencies
# English: E(12.7%), T(9.1%), A(8.2%), O(7.5%), I(7.0%), N(6.7%)
# German:  E(16.4%), N(9.8%), I(7.6%), S(7.3%), R(7.0%), A(6.5%)

# =====================================================================
# 4. THE 486486 INSIGHT: Pairs as (3-digit, 3-digit)
# =====================================================================
print("\n" + "=" * 70)
print("4. THREE-DIGIT PAIRS (inspired by 486486 = 486+486)")
print("=" * 70)

# Take consecutive 3-digit groups and pair them
triplets = []
for i in range(0, len(combined)-5, 6):
    left = combined[i:i+3]
    right = combined[i+3:i+6]
    triplets.append((left, right))

print(f"\nTotal 3+3 pairs: {len(triplets)}")

# Check the ratio of left/right (CipSoft pairs have ratio ~1.6)
ratios = []
for left, right in triplets:
    l, r = int(left), int(right)
    if r > 0:
        ratios.append(l / r)

print(f"Ratio stats (left/right):")
avg_ratio = sum(ratios) / len(ratios)
ratios_near_1_6 = sum(1 for r in ratios if 1.4 < r < 1.8)
print(f"  Average ratio: {avg_ratio:.3f}")
print(f"  Ratios near 1.6 (1.4-1.8): {ratios_near_1_6}/{len(ratios)} ({ratios_near_1_6/len(ratios)*100:.1f}%)")

# =====================================================================
# 5. HONEMINAS DOT PRODUCT AS PAIRING MECHANISM
# =====================================================================
print("\n" + "=" * 70)
print("5. HONEMINAS-STYLE: 5-DIGIT VECTOR PAIRS")
print("=" * 70)

# The Honeminas formula uses 5-element vectors
# (4,3,1,5,3).(3,4,7,8,4) = 83
# What if we read the text as consecutive 5-digit groups and apply dot products?

v1 = [4, 3, 1, 5, 3]
v2 = [3, 4, 7, 8, 4]

# Method 1: Take pairs of 5-digit groups, dot product each pair
print("\n--- Method 1: Consecutive 5-digit pair dot products ---")
dot_results = []
for i in range(0, len(combined)-9, 10):
    a = [int(d) for d in combined[i:i+5]]
    b = [int(d) for d in combined[i+5:i+10]]
    dot = sum(x*y for x, y in zip(a, b))
    dot_results.append(dot)

print(f"Total dot products: {len(dot_results)}")
print(f"Range: {min(dot_results)} to {max(dot_results)}")
print(f"Mean: {sum(dot_results)/len(dot_results):.1f}")
print(f"First 30: {dot_results[:30]}")

# Map to letters (mod 26)
letters_26 = ''.join(chr(d % 26 + ord('A')) for d in dot_results)
print(f"Mod 26 -> letters: {letters_26[:80]}")

# Method 2: Dot each 5-digit group with the Honeminas vectors
print("\n--- Method 2: Each 5-group dotted with v1=[4,3,1,5,3] ---")
dot_v1 = []
for i in range(0, len(combined)-4, 5):
    digits = [int(d) for d in combined[i:i+5]]
    dot = sum(x*y for x, y in zip(digits, v1))
    dot_v1.append(dot)

dot_v1_mod26 = ''.join(chr(d % 26 + ord('A')) for d in dot_v1)
print(f"Mod 26: {dot_v1_mod26[:80]}")

# Method 3: Dot each 5-group with v2
print("\n--- Method 3: Each 5-group dotted with v2=[3,4,7,8,4] ---")
dot_v2 = []
for i in range(0, len(combined)-4, 5):
    digits = [int(d) for d in combined[i:i+5]]
    dot = sum(x*y for x, y in zip(digits, v2))
    dot_v2.append(dot)

dot_v2_mod26 = ''.join(chr(d % 26 + ord('A')) for d in dot_v2)
print(f"Mod 26: {dot_v2_mod26[:80]}")

# =====================================================================
# 6. FACEBOOK PAIR MATHEMATICAL RELATIONSHIPS
# =====================================================================
print("\n" + "=" * 70)
print("6. FACEBOOK PAIR DEEP ANALYSIS")
print("=" * 70)

fb_pairs = [
    (713, 473), (765, 464), (706, 447), (824, 499), (975, 595),
    (937, 530), (726, 431), (729, 447), (652, 400), (653, 407),
    (565, 375), (746, 458), (1021, 659), (759, 475), (718, 438),
    (737, 469), (648, 428), (818, 520), (985, 621), (2154, 1307),
    (841, 540), (684, 448), (694, 453)
]

print("\nSearching for mathematical formula F(left) = right:")
print("\n--- Testing: right = (left * a + b) for constants a, b ---")

# Try linear relationship: R = a*L + b
# Using least squares
n = len(fb_pairs)
sum_l = sum(l for l, r in fb_pairs)
sum_r = sum(r for l, r in fb_pairs)
sum_ll = sum(l*l for l, r in fb_pairs)
sum_lr = sum(l*r for l, r in fb_pairs)

a = (n * sum_lr - sum_l * sum_r) / (n * sum_ll - sum_l * sum_l)
b = (sum_r - a * sum_l) / n
print(f"  Best fit: right = {a:.6f} * left + {b:.2f}")
print(f"  R^2 correlation:")
ss_res = sum((r - (a*l + b))**2 for l, r in fb_pairs)
ss_tot = sum((r - sum_r/n)**2 for l, r in fb_pairs)
r_squared = 1 - ss_res/ss_tot
print(f"  R^2 = {r_squared:.6f}")

# Check residuals
print(f"\n  Residuals (actual - predicted):")
for l, r in fb_pairs:
    predicted = a * l + b
    residual = r - predicted
    print(f"    ({l:4d}, {r:4d}): predicted={predicted:.0f}, residual={residual:+.1f}")

# Try: right = floor(left * 469 / 737) or similar
print("\n--- Testing: right = left * K / M for various K, M ---")
best_fit = None
best_error = float('inf')
for K in range(1, 1000):
    for M in range(K+1, 1500):
        error = sum(abs(r - round(l * K / M)) for l, r in fb_pairs)
        if error < best_error:
            best_error = error
            best_fit = (K, M)

print(f"  Best integer ratio: right ~ left * {best_fit[0]} / {best_fit[1]}")
print(f"  = left * {best_fit[0]/best_fit[1]:.6f}")
print(f"  Total absolute error: {best_error}")

# What about digit-wise operations?
print("\n--- Digit-wise analysis of pairs ---")
for l, r in fb_pairs[:10]:
    ls = str(l).zfill(3)
    rs = str(r).zfill(3)
    diffs = [int(a)-int(b) for a, b in zip(ls, rs)]
    sums = [(int(a)+int(b)) % 10 for a, b in zip(ls, rs)]
    prods = [(int(a)*int(b)) % 10 for a, b in zip(ls, rs)]
    print(f"  ({l:4d},{r:3d}): digits {ls},{rs}  diff={diffs}  sum%10={sums}  prod%10={prods}")

# =====================================================================
# 7. THE 1001 CONNECTION: 486486 / 1001 = 486
# =====================================================================
print("\n" + "=" * 70)
print("7. THE 1001 CONNECTION")
print("=" * 70)

print(f"\n486486 = 486 * 1001")
print(f"1001 = 7 * 11 * 13")
print(f"486 = 2 * 3^5 = 2 * 243")
print(f"\nAny N repeated as ABABAB = N * 1001 (for 3-digit N)")
print(f"So '486486' as a name means: the bonelord's name is literally '486' doubled")
print(f"\nDoes 486 have special properties?")
print(f"  486 in base 5: {486 // 125}-{(486 % 125)//25}-{(486 % 25)//5}-{486 % 5} = ", end="")
d5 = []
n = 486
while n > 0:
    d5.append(n % 5)
    n //= 5
d5.reverse()
print("".join(str(x) for x in d5))

# Could 486 be the number of something?
print(f"\n  486 / 26 = {486/26:.2f} (not a clean division for alphabet)")
print(f"  486 / 29 = {486/29:.2f} (29-letter alphabet?)")
print(f"  sqrt(486) = {486**0.5:.4f}")

# =====================================================================
# 8. CRITICAL: Pair-based reading of the books
# =====================================================================
print("\n" + "=" * 70)
print("8. PAIR-BASED READING: Split books into (left, right) columns")
print("=" * 70)

# What if each book is meant to be read as two columns?
# Split each book in half: left column and right column
print("\n--- Splitting each book in half ---")
for idx, book in enumerate(books[:10]):
    mid = len(book) // 2
    left_half = book[:mid]
    right_half = book[mid:]

    # Check ratio
    l_sum = sum(int(d) for d in left_half)
    r_sum = sum(int(d) for d in right_half)
    ratio = l_sum / r_sum if r_sum > 0 else 0

    # Check digit-wise relationship
    min_len = min(len(left_half), len(right_half))
    diffs = [int(left_half[i]) - int(right_half[i]) for i in range(min(20, min_len))]

    print(f"  Book {idx+1} ({len(book)} digits): L_avg={l_sum/len(left_half):.2f}, R_avg={r_sum/len(right_half):.2f}, ratio={ratio:.3f}")
    print(f"    First 20 diffs: {diffs}")

# =====================================================================
# 9. VARIABLE-LENGTH WORD CODES: Using forbidden transitions as delimiters
# =====================================================================
print("\n" + "=" * 70)
print("9. WORD SEGMENTATION USING TRANSITION RARITY")
print("=" * 70)

# From transition_filter.py: forbidden/rare transitions
# 3->3 (1x), 0->7 (1x), 3->2 (2x), 3->9 (5x), 6->6 (12x), 6->9 (13x), 0->2 (13x)
rare_transitions = {
    (3,3): 1, (0,7): 1, (3,2): 2, (3,9): 5,
    (6,6): 12, (6,9): 13, (0,2): 13
}

# But what if the rare transitions NEVER appear within a word code?
# They only appear at word boundaries (between the last digit of one code
# and the first digit of the next)

# Use Knightmare to check: 3478 67 90871 97664 3466 0 345
# Boundaries: 8|6, 7|9, 1|9, 4|3, 6|0, 0|3
knightmare_boundaries = [(8,6), (7,9), (1,9), (4,3), (6,0), (0,3)]
print("\nKnightmare word boundaries (last digit of word -> first of next):")
for pair in knightmare_boundaries:
    trans = f"{pair[0]}->{pair[1]}"
    # Count this transition in the combined text
    count = 0
    for i in range(len(combined)-1):
        if int(combined[i]) == pair[0] and int(combined[i+1]) == pair[1]:
            count += 1
    expected = len(combined) / 100  # if uniform
    ratio = count / expected if expected > 0 else 0
    is_rare = pair in rare_transitions
    print(f"  {trans}: {count} times (expected ~{expected:.0f}, ratio={ratio:.2f}){' RARE!' if is_rare else ''}")

print("\nNone of the Knightmare boundaries are forbidden transitions!")
print("This means word boundaries DON'T use rare transitions as delimiters.")

# =====================================================================
# 10. POLL ANSWER C STRUCTURE
# =====================================================================
print("\n" + "=" * 70)
print("10. POLL ANSWER C: '663 902073 7223 67538 467 80097'")
print("=" * 70)

poll_c = ['663', '902073', '7223', '67538', '467', '80097']
# The poll question was: "When the veils of shrouded truths are lifted, who can stand?"
# This is a very specific question that might have a known answer in Tibia lore

print(f"\nPoll question: 'When the veils of shrouded truths are lifted, who can stand?'")
print(f"\n6 word codes: {poll_c}")
print(f"Digits/word: {[len(w) for w in poll_c]}")
print(f"Total digits: {sum(len(w) for w in poll_c)} for likely 6 words")

# Common 6-word answers to "who can stand?":
# "ONLY THE WISE CAN STAND" (6 words if "can stand" is 2)
# "THE BONELORDS ALONE CAN STAND TALL"
# "NO ONE BUT US BONELORDS (CAN)"

# Check if these word codes appear in the books
print(f"\nSearching poll word codes in books:")
for code in poll_c:
    count = combined.count(code)
    print(f"  '{code}': {count} times in books")

# Interesting: '467' appears in books - same as '469' neighbor
# '67' = A (from Knightmare), '467' = ?
print(f"\n'467' vs '67': note that '67' = 'A' in Knightmare")
print(f"'469' = the language name, '467' is in poll...")

# =====================================================================
# 11. THE 0/3/6 ANOMALY
# =====================================================================
print("\n" + "=" * 70)
print("11. DIGITS 0, 3, 6 SPECIAL BEHAVIOR")
print("=" * 70)

# Digit 3 has forbidden transitions: 3->3 (1x), 3->2 (2x), 3->9 (5x)
# Digit 0 has: 0->7 (1x), 0->2 (13x)
# Digit 6 has: 6->6 (12x), 6->9 (13x)
# AND: 0 is "obscene", digit 3 is the least frequent (5.78%)

print("\nDigits 0, 3, 6 all have near-forbidden following transitions")
print("AND digit 0 is 'obscene'")
print("AND digit 3 is the LEAST frequent (5.78%)")
print("AND 486 (bonelord name) uses digits 4, 8, 6")

# What precedes 0, 3, 6?
for special in [0, 3, 6]:
    before = Counter()
    for i in range(1, len(combined)):
        if int(combined[i]) == special:
            before[int(combined[i-1])] += 1
    total = sum(before.values())
    print(f"\nDigit {special} preceded by:")
    for d in range(10):
        pct = before.get(d, 0) / total * 100 if total > 0 else 0
        bar = '#' * int(pct / 2)
        print(f"  {d}: {before.get(d,0):4d} ({pct:5.1f}%) {bar}")

# =====================================================================
# 12. TESTING: Books as pairs of digit-vectors
# =====================================================================
print("\n" + "=" * 70)
print("12. BOOKS AS PAIRS OF K-DIGIT VECTORS")
print("=" * 70)

# Test different k values for vector pairing
for k in [2, 3, 4, 5]:
    print(f"\n--- k={k}: pairs of {k}-digit vectors ---")
    # Take first book, split into k-digit groups, pair consecutive
    book = combined[:200]  # first 200 digits

    groups = []
    for i in range(0, len(book) - k + 1, k):
        groups.append([int(d) for d in book[i:i+k]])

    # Pair consecutive groups and compute dot product
    dots = []
    for i in range(0, len(groups)-1, 2):
        dot = sum(a*b for a, b in zip(groups[i], groups[i+1]))
        dots.append(dot)

    if dots:
        print(f"  Dot products (first 20): {dots[:20]}")
        print(f"  Range: {min(dots)} to {max(dots)}")
        unique_dots = len(set(dots))
        print(f"  Unique values: {unique_dots} / {len(dots)} total")

        # Map to letters
        letters = ''.join(chr(d % 26 + ord('A')) for d in dots)
        print(f"  Mod 26: {letters[:40]}")

        # Check if 26 unique values (for alphabet)
        mod26_vals = [d % 26 for d in dots]
        print(f"  Unique mod 26: {len(set(mod26_vals))}")

# =====================================================================
# 13. KHAROS PERMUTATION PATTERN
# =====================================================================
print("\n" + "=" * 70)
print("13. KHAROS BLOCK PERMUTATION ANALYSIS")
print("=" * 70)

hellgate_book = "65128896721277889438872151288952196180031145727857261185764219709680579636612527570584521765219727830464876515956461141451988997511216151"
kharos_book = "51595646114145190584521765219727830464879636612527578967212778894388727857261185764217614588952196180031651288899751121615127215196805970"

print(f"\nHellgate (137 digits): {hellgate_book}")
print(f"Kharos  (137 digits): {kharos_book}")

# Try different block sizes for permutation
for bs in range(5, 25):
    h_blocks = [hellgate_book[i:i+bs] for i in range(0, len(hellgate_book)-bs+1, bs)]
    k_blocks = [kharos_book[i:i+bs] for i in range(0, len(kharos_book)-bs+1, bs)]

    # How many H blocks appear in K?
    matches = sum(1 for hb in h_blocks if hb in kharos_book)
    if matches > len(h_blocks) * 0.3:  # At least 30% match
        print(f"  Block size {bs}: {matches}/{len(h_blocks)} H blocks found in K")

# Byte-level comparison
print(f"\n--- Character-by-character alignment ---")
matches_at_offset = []
for offset in range(-136, 137):
    matches = 0
    count = 0
    for i in range(137):
        j = i + offset
        if 0 <= j < 137:
            count += 1
            if hellgate_book[i] == kharos_book[j]:
                matches += 1
    if count > 0:
        pct = matches / count * 100
        if pct > 15:
            matches_at_offset.append((offset, matches, count, pct))

matches_at_offset.sort(key=lambda x: -x[3])
print("Top offsets by match rate:")
for offset, matches, count, pct in matches_at_offset[:10]:
    print(f"  Offset {offset:+4d}: {matches}/{count} ({pct:.1f}%)")

# =====================================================================
# 14. WHAT IF THE TEXT IS IN BASE-5 PAIRS?
# =====================================================================
print("\n" + "=" * 70)
print("14. BASE-5 PAIR ENCODING")
print("=" * 70)

# Each digit 0-9 could represent TWO base-5 digits (since 5^2 = 25 ~ 26)
# Digit d -> (d//5, d%5) gives a base-5 pair
print("\nMapping digits to base-5 pairs:")
for d in range(10):
    high = d // 5
    low = d % 5
    print(f"  {d} -> ({high}, {low})")

print("\nApplying to first 40 digits of text:")
base5_pairs = []
for d in combined[:40]:
    n = int(d)
    base5_pairs.append((n // 5, n % 5))

print(f"  Text: {combined[:40]}")
print(f"  Base5: {base5_pairs}")

# If each pair gives a base-5 number: 5*high + low = original digit (trivially)
# But TWO consecutive base-5 pairs: value = 5*a + b = 0..24 -> 25 values ~ alphabet
two_b5 = []
for i in range(0, len(combined)-1, 2):
    a = int(combined[i])
    b = int(combined[i+1])
    # Extract base-5 components
    val = (a % 5) * 5 + (b % 5)  # just use low bits
    two_b5.append(val)

unique_vals = sorted(set(two_b5[:100]))
print(f"\n(d1%5)*5 + (d2%5) for consecutive pairs:")
print(f"  Unique values: {len(set(two_b5))} (need 26 for alphabet)")
print(f"  First 50 values: {two_b5[:50]}")
letters_b5 = ''.join(chr(v + ord('A')) if v < 26 else '?' for v in two_b5)
print(f"  As letters: {letters_b5[:60]}")

# Alternative: use high bits
two_b5h = []
for i in range(0, len(combined)-1, 2):
    a = int(combined[i])
    b = int(combined[i+1])
    val = (a // 5) * 5 + (b // 5)  # just use high bits (0 or 1)
    two_b5h.append(val)
print(f"\n(d1//5)*5 + (d2//5) for consecutive pairs:")
print(f"  Unique values: {sorted(set(two_b5h))}")
# Only 4 values (00,01,10,11 in binary) -> not useful for alphabet

# =====================================================================
# 15. THE "5 EYES" CONNECTION
# =====================================================================
print("\n" + "=" * 70)
print("15. THE 5 EYES: Each digit blinked by one of 5 eyes")
print("=" * 70)

# Bonelords have 5 eyes. The Honeminas formula uses 5-element vectors.
# What if each group of 5 consecutive digits represents one "blink" of all 5 eyes?
# And the VALUE of each eye's blink (0-9) matters?

print("\n'469 is spoken between bonelords by blinking numbers'")
print("'Each eye can blink a digit 0-9'")
print("'5 eyes blinking simultaneously = 1 unit of information'")
print(f"\nTotal digits: {len(combined)}")
print(f"Groups of 5: {len(combined) // 5} = potential 'blink units'")
print(f"Each blink: 5 digits, range per eye: 0-9")
print(f"Information per blink: 10^5 = 100,000 possible values")
print(f"Far more than 26 letters -> could encode words/syllables directly")

# Distribution of 5-digit groups as numbers
groups_5 = []
for i in range(0, len(combined)-4, 5):
    val = int(combined[i:i+5])
    groups_5.append(val)

print(f"\n5-digit group statistics:")
print(f"  Total groups: {len(groups_5)}")
print(f"  Unique groups: {len(set(groups_5))}")
print(f"  Min: {min(groups_5)}")
print(f"  Max: {max(groups_5)}")
print(f"  Average: {sum(groups_5)/len(groups_5):.0f}")

# Most common 5-digit groups
grp5_freq = Counter(groups_5)
print(f"\n  Most common 5-digit groups:")
for grp, cnt in grp5_freq.most_common(15):
    print(f"    {grp:05d}: {cnt} times")

# If 5-digit groups encode words: ~2252 unique groups for ~2252 positions
# German vocabulary: ~5000 common words needed
# But with Honeminas dot product, the OUTPUT space is smaller

print("\n--- Honeminas reduction: 5-digit group -> dot product with [4,3,1,5,3] ---")
dot_values = []
for i in range(0, len(combined)-4, 5):
    digits = [int(d) for d in combined[i:i+5]]
    dot = sum(a*b for a, b in zip(digits, v1))
    dot_values.append(dot)

dot_freq = Counter(dot_values)
print(f"  Unique dot products: {len(dot_freq)} (from {len(dot_values)} groups)")
print(f"  Range: {min(dot_values)} to {max(dot_values)}")
print(f"  Most common:")
for val, cnt in dot_freq.most_common(10):
    letter = chr(val % 26 + ord('A'))
    print(f"    {val} ({letter}): {cnt} times ({cnt/len(dot_values)*100:.1f}%)")

# =====================================================================
print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
