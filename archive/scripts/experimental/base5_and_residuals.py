"""
Two promising leads:

1. BASE-5 PAIR ENCODING: (d1%5)*5 + (d2%5) gives 25 unique values
   - 25 values is one short of 26 (alphabet)
   - Each digit 0-4 maps to low, 5-9 maps to high (binary split at 5)
   - Bonelords have 5 EYES

2. FACEBOOK RESIDUALS: R = 0.593*L + 25.28 (R^2 = 0.990)
   - The residuals from this line might encode information
   - The coefficient ~0.6 = 3/5 (five eyes again!)
   - The intercept ~25 = alphabet size - 1
"""

import json
import sys
from collections import Counter
from math import log2

sys.stdout.reconfigure(encoding='utf-8')

with open("books.json") as f:
    books = json.load(f)

combined = "".join(books)

print("=" * 70)
print("BASE-5 AND RESIDUALS DEEP ANALYSIS")
print("=" * 70)

# =====================================================================
# 1. BASE-5 ENCODING: Exhaustive test of all digit->base5 mappings
# =====================================================================
print("\n" + "=" * 70)
print("1. BASE-5 ENCODING VARIANTS")
print("=" * 70)

# Standard: d%5 gives 0-4
# But what if the mapping is different? Test permutations
# There are 10! / (2!*2!) ways to assign 10 digits to 5 groups of 2

# First, let's understand the standard mapping better
print("\n--- Standard: value = (d1 % 5) * 5 + (d2 % 5) ---")
values = []
for i in range(0, len(combined)-1, 2):
    d1, d2 = int(combined[i]), int(combined[i+1])
    val = (d1 % 5) * 5 + (d2 % 5)
    values.append(val)

val_freq = Counter(values)
print(f"Unique values: {len(val_freq)} out of 25 possible (0-24)")
missing = [v for v in range(25) if v not in val_freq]
print(f"Missing values: {missing}")
print(f"\nFrequency distribution (sorted by count):")
for val, cnt in val_freq.most_common():
    pct = cnt / len(values) * 100
    letter = chr(val + ord('A')) if val < 26 else '?'
    print(f"  {val:2d} ({letter}): {cnt:4d} ({pct:5.2f}%)")

# Calculate IC for this encoding
n = len(values)
ic = sum(c * (c-1) for c in val_freq.values()) / (n * (n-1))
ic_random = 1.0 / len(val_freq)
print(f"\nIC = {ic:.6f} (random for {len(val_freq)} symbols = {ic_random:.6f})")
print(f"IC ratio = {ic / ic_random:.3f} (English ~1.73, German ~1.72)")

# =====================================================================
# 2. TRY DIFFERENT ALIGNMENTS (offset by 1)
# =====================================================================
print("\n" + "=" * 70)
print("2. BASE-5 WITH OFFSET 1 (start from digit 1 instead of 0)")
print("=" * 70)

values_off1 = []
for i in range(1, len(combined)-1, 2):
    d1, d2 = int(combined[i]), int(combined[i+1])
    val = (d1 % 5) * 5 + (d2 % 5)
    values_off1.append(val)

val_freq_off1 = Counter(values_off1)
print(f"Unique values: {len(val_freq_off1)} out of 25 possible")
missing_off1 = [v for v in range(25) if v not in val_freq_off1]
print(f"Missing values: {missing_off1}")

n1 = len(values_off1)
ic_off1 = sum(c * (c-1) for c in val_freq_off1.values()) / (n1 * (n1-1))
print(f"IC = {ic_off1:.6f} (ratio = {ic_off1 / (1.0/len(val_freq_off1)):.3f})")

# =====================================================================
# 3. BASE-5 WITH DIFFERENT GROUPINGS
# =====================================================================
print("\n" + "=" * 70)
print("3. ALTERNATIVE BASE-5 GROUPINGS")
print("=" * 70)

# What if the 5 groups aren't {0,5}, {1,6}, {2,7}, {3,8}, {4,9}?
# What if they're based on Tibia-specific rules?

# Test: digits 0-4 = first half, 5-9 = second half (binary)
# Then pair binary values: value = 2*b1 + b2 (only 4 values, too few)

# Test: map each digit to its position in frequency ranking
# Freq order: 1(16.6%), 5(12.9%), 4(11.3%), 6(10.1%), 8(9.9%), 9(8.9%), 7(8.5%), 2(8.4%), 0(7.6%), 3(5.8%)
freq_rank = {1:0, 5:1, 4:2, 6:3, 8:4, 9:5, 7:6, 2:7, 0:8, 3:9}

# Map to base-5 by freq rank
print("\n--- Frequency-ranked base-5 ---")
values_freq = []
for i in range(0, len(combined)-1, 2):
    d1, d2 = int(combined[i]), int(combined[i+1])
    r1, r2 = freq_rank[d1], freq_rank[d2]
    val = (r1 % 5) * 5 + (r2 % 5)
    values_freq.append(val)

vf_freq = Counter(values_freq)
print(f"Unique values: {len(vf_freq)}")
n2 = len(values_freq)
ic_freq = sum(c * (c-1) for c in vf_freq.values()) / (n2 * (n2-1))
print(f"IC = {ic_freq:.6f} (ratio = {ic_freq / (1.0/len(vf_freq)):.3f})")

# =====================================================================
# 4. THE "3/5" CONNECTION: R ~ (3/5)*L + 25
# =====================================================================
print("\n" + "=" * 70)
print("4. FACEBOOK PAIRS: THE 3/5 HYPOTHESIS")
print("=" * 70)

fb_pairs = [
    (713, 473), (765, 464), (706, 447), (824, 499), (975, 595),
    (937, 530), (726, 431), (729, 447), (652, 400), (653, 407),
    (565, 375), (746, 458), (1021, 659), (759, 475), (718, 438),
    (737, 469), (648, 428), (818, 520), (985, 621), (2154, 1307),
    (841, 540), (684, 448), (694, 453)
]

print(f"\nTesting R = (3/5)*L + C for various C:")
for c in [0, 5, 10, 15, 20, 25, 26, 30]:
    errors = [abs(r - (3*l/5 + c)) for l, r in fb_pairs]
    avg_err = sum(errors) / len(errors)
    max_err = max(errors)
    print(f"  C={c:2d}: avg_error={avg_err:.1f}, max_error={max_err:.1f}")

# Best fit with exact 3/5 slope
print(f"\nWith slope exactly 3/5:")
residuals_3_5 = [r - 3*l/5 for l, r in fb_pairs]
avg_intercept = sum(residuals_3_5) / len(residuals_3_5)
print(f"  Average intercept: {avg_intercept:.2f}")

# Residuals from R = 3L/5 + avg_intercept
print(f"\n  Residuals from R = 0.6*L + {avg_intercept:.1f}:")
residuals_exact = []
for l, r in fb_pairs:
    predicted = 3*l/5 + avg_intercept
    residual = r - predicted
    residuals_exact.append(residual)
    print(f"    ({l:4d},{r:4d}): pred={predicted:.0f}, resid={residual:+.1f}")

# Could residuals be letters?
print(f"\nResiduals rounded: {[round(r) for r in residuals_exact]}")
print(f"Residuals mod 26: {[round(r) % 26 for r in residuals_exact]}")
print(f"As letters: {''.join(chr(round(r) % 26 + ord('A')) for r in residuals_exact)}")

# =====================================================================
# 5. DIGIT-PRODUCT PAIRS: d1*d2 for consecutive digits
# =====================================================================
print("\n" + "=" * 70)
print("5. DIGIT PRODUCT ENCODING: d1*d2")
print("=" * 70)

products = []
for i in range(0, len(combined)-1, 2):
    d1, d2 = int(combined[i]), int(combined[i+1])
    products.append(d1 * d2)

prod_freq = Counter(products)
print(f"Unique products: {len(prod_freq)} (possible: 0-81)")
print(f"\nProducts 0-25 (alphabet range):")
for p in range(26):
    cnt = prod_freq.get(p, 0)
    pct = cnt / len(products) * 100
    if cnt > 0:
        print(f"  {p:2d} ({chr(p+ord('A'))}): {cnt:4d} ({pct:.2f}%)")

# How many products fall in 0-25 range?
in_range = sum(1 for p in products if 0 <= p <= 25)
print(f"\n{in_range}/{len(products)} products in 0-25 range ({in_range/len(products)*100:.1f}%)")

# =====================================================================
# 6. SUM MOD 26
# =====================================================================
print("\n" + "=" * 70)
print("6. DIGIT SUM MOD 26: (d1 + d2) % 26")
print("=" * 70)

sums26 = []
for i in range(0, len(combined)-1, 2):
    d1, d2 = int(combined[i]), int(combined[i+1])
    sums26.append((d1 + d2) % 26)

s26_freq = Counter(sums26)
print(f"Unique values: {len(s26_freq)} (range 0-18 since max d1+d2=18)")
# Actually only 0-18 possible from two single digits

# IC
n3 = len(sums26)
ic_s26 = sum(c * (c-1) for c in s26_freq.values()) / (n3 * (n3-1))
print(f"IC = {ic_s26:.6f} (random for 19 symbols = {1/19:.6f})")
print(f"IC ratio = {ic_s26 / (1/19):.3f}")

print(f"\nFrequency distribution:")
for val in range(19):
    cnt = s26_freq.get(val, 0)
    pct = cnt / n3 * 100
    bar = '#' * int(pct)
    print(f"  {val:2d}: {cnt:4d} ({pct:5.2f}%) {bar}")

# =====================================================================
# 7. WEIGHTED SUM: a*d1 + b*d2 for various a,b
# =====================================================================
print("\n" + "=" * 70)
print("7. WEIGHTED SUMS: a*d1 + b*d2 mod M")
print("=" * 70)

# Test which (a, b, M) gives highest IC
best_ic = 0
best_params = None

for a in range(1, 10):
    for b in range(1, 10):
        for M in [26, 29, 25]:
            ws_values = []
            for i in range(0, len(combined)-1, 2):
                d1, d2 = int(combined[i]), int(combined[i+1])
                ws_values.append((a*d1 + b*d2) % M)
            ws_freq = Counter(ws_values)
            n_ws = len(ws_values)
            if len(ws_freq) >= 20:  # Need enough unique values
                ic_ws = sum(c*(c-1) for c in ws_freq.values()) / (n_ws*(n_ws-1))
                ic_rand = 1.0 / M
                ic_ratio = ic_ws / ic_rand
                if ic_ratio > best_ic:
                    best_ic = ic_ratio
                    best_params = (a, b, M)

print(f"Best IC ratio: {best_ic:.4f} at a={best_params[0]}, b={best_params[1]}, M={best_params[2]}")

# Show the best one's distribution
a, b, M = best_params
ws_values = []
for i in range(0, len(combined)-1, 2):
    d1, d2 = int(combined[i]), int(combined[i+1])
    ws_values.append((a*d1 + b*d2) % M)

ws_freq = Counter(ws_values)
n_ws = len(ws_values)
ic_ws = sum(c*(c-1) for c in ws_freq.values()) / (n_ws*(n_ws-1))
print(f"\nDistribution for {a}*d1 + {b}*d2 mod {M}:")
for val in range(M):
    cnt = ws_freq.get(val, 0)
    pct = cnt / n_ws * 100
    letter = chr(val + ord('A')) if val < 26 else '?'
    bar = '#' * int(pct * 2)
    print(f"  {val:2d} ({letter}): {cnt:4d} ({pct:5.2f}%) {bar}")

# =====================================================================
# 8. TRIPLET BASE-5: Three digits -> one value mod 26
# =====================================================================
print("\n" + "=" * 70)
print("8. TRIPLET ENCODING: d1*25 + d2*5 + d3 (base-5 triplets)")
print("=" * 70)

# 3 digits in base-5 encoding: (d%5) for each, then combine as base-5 number
# Value = (d1%5)*25 + (d2%5)*5 + (d3%5)
# Range: 0-124, mod 26 gives letters
triplet_vals = []
for i in range(0, len(combined)-2, 3):
    d1, d2, d3 = int(combined[i]) % 5, int(combined[i+1]) % 5, int(combined[i+2]) % 5
    val = d1 * 25 + d2 * 5 + d3
    triplet_vals.append(val % 26)

trip_freq = Counter(triplet_vals)
n_t = len(triplet_vals)
ic_trip = sum(c*(c-1) for c in trip_freq.values()) / (n_t*(n_t-1))
print(f"IC = {ic_trip:.6f} (random = {1/26:.6f})")
print(f"IC ratio = {ic_trip / (1/26):.3f}")

# =====================================================================
# 9. OPTIMAL PAIR ENCODING SEARCH
# =====================================================================
print("\n" + "=" * 70)
print("9. SEARCHING FOR OPTIMAL PAIR ENCODING")
print("=" * 70)

# Try all functions f(d1,d2) = (a*d1^2 + b*d1*d2 + c*d2^2 + d*d1 + e*d2) mod M
# for small a,b,c,d,e and M in [25,26,29]
print("\nSearching (a*d1 + b*d2 + c*d1*d2) mod M for best IC...")

best_ic = 0
best_params = None

for a in range(0, 6):
    for b in range(0, 6):
        for c in range(0, 4):
            for M in [25, 26, 29]:
                if a == 0 and b == 0 and c == 0:
                    continue
                test_vals = []
                for i in range(0, min(len(combined)-1, 4000), 2):
                    d1, d2 = int(combined[i]), int(combined[i+1])
                    val = (a*d1 + b*d2 + c*d1*d2) % M
                    test_vals.append(val)
                tf = Counter(test_vals)
                n_test = len(test_vals)
                if len(tf) >= M * 0.7:  # At least 70% of values used
                    ic_test = sum(v*(v-1) for v in tf.values()) / (n_test*(n_test-1))
                    ic_ratio = ic_test / (1.0/M)
                    if ic_ratio > best_ic:
                        best_ic = ic_ratio
                        best_params = (a, b, c, M)

if best_params:
    a, b, c, M = best_params
    print(f"\nBest: ({a}*d1 + {b}*d2 + {c}*d1*d2) mod {M}")
    print(f"IC ratio: {best_ic:.4f}")

    # Apply to full text
    full_vals = []
    for i in range(0, len(combined)-1, 2):
        d1, d2 = int(combined[i]), int(combined[i+1])
        val = (a*d1 + b*d2 + c*d1*d2) % M
        full_vals.append(val)

    ff = Counter(full_vals)
    print(f"\nFull text distribution:")
    for val in range(M):
        cnt = ff.get(val, 0)
        pct = cnt / len(full_vals) * 100
        bar = '#' * int(pct * 2)
        print(f"  {val:2d}: {cnt:4d} ({pct:5.2f}%) {bar}")

    # Compare to German letter frequencies
    german_freq = {'E':16.4,'N':9.8,'I':7.6,'S':7.3,'R':7.0,'A':6.5,'T':6.2,'D':5.1,'H':4.8,'U':4.2,
                   'L':3.4,'C':3.1,'G':3.0,'M':2.5,'O':2.5,'B':1.9,'W':1.9,'F':1.7,'K':1.2,'Z':1.1,
                   'P':0.8,'V':0.7,'J':0.3,'Y':0.04,'X':0.03,'Q':0.02}

    # Sort both by frequency and compare
    text_sorted = sorted(ff.items(), key=lambda x: -x[1])
    german_sorted = sorted(german_freq.items(), key=lambda x: -x[1])

    print(f"\nComparison: text frequency vs German:")
    for i, ((val, cnt), (letter, gfreq)) in enumerate(zip(text_sorted[:20], german_sorted[:20])):
        tpct = cnt / len(full_vals) * 100
        print(f"  Rank {i+1}: val={val:2d} ({tpct:.1f}%) vs German '{letter}' ({gfreq:.1f}%)")

# =====================================================================
# 10. THE 469 AS KEY
# =====================================================================
print("\n" + "=" * 70)
print("10. USING 469 AS THE KEY")
print("=" * 70)

# "469" is the name of the language
# What if 4, 6, 9 are the key values for decoding?

# Test: (4*d1 + 6*d2 + 9*d3) mod 26 for triplets
print("\n--- (4*d1 + 6*d2 + 9*d3) mod 26 ---")
vals_469 = []
for i in range(0, len(combined)-2, 3):
    d1, d2, d3 = int(combined[i]), int(combined[i+1]), int(combined[i+2])
    val = (4*d1 + 6*d2 + 9*d3) % 26
    vals_469.append(val)

f469 = Counter(vals_469)
n469 = len(vals_469)
ic_469 = sum(c*(c-1) for c in f469.values()) / (n469*(n469-1))
print(f"IC = {ic_469:.6f} (ratio = {ic_469/(1/26):.3f})")

# Test: (d1*d2) mod 9 + d3 for various combos
print("\n--- d1*9 + d2 mod 26 (using 9 from 469) ---")
vals_9 = []
for i in range(0, len(combined)-1, 2):
    d1, d2 = int(combined[i]), int(combined[i+1])
    val = (d1 * 9 + d2) % 26
    vals_9.append(val)

f9 = Counter(vals_9)
n9 = len(vals_9)
ic_9 = sum(c*(c-1) for c in f9.values()) / (n9*(n9-1))
print(f"IC = {ic_9:.6f} (ratio = {ic_9/(1/26):.3f})")

# =====================================================================
# 11. PER-BOOK IC COMPARISON
# =====================================================================
print("\n" + "=" * 70)
print("11. BEST ENCODING IC PER BOOK")
print("=" * 70)

# Use the base-5 encoding and check IC per book
print("\n--- Base-5 pair encoding IC per book ---")
high_ic_books = []
for idx, book in enumerate(books):
    bvals = []
    for i in range(0, len(book)-1, 2):
        d1, d2 = int(book[i]), int(book[i+1])
        val = (d1 % 5) * 5 + (d2 % 5)
        bvals.append(val)

    if len(bvals) < 10:
        continue

    bf = Counter(bvals)
    nb = len(bvals)
    ic_b = sum(c*(c-1) for c in bf.values()) / (nb*(nb-1))
    unique = len(bf)
    ic_ratio = ic_b / (1.0/unique) if unique > 1 else 0

    if ic_ratio > 1.4:
        high_ic_books.append((idx+1, ic_ratio, nb, unique))
        print(f"  Book {idx+1:2d}: IC ratio={ic_ratio:.3f}, pairs={nb}, unique={unique}")

if not high_ic_books:
    print("  No books with IC ratio > 1.4")

# =====================================================================
# 12. GERMAN QUADGRAM SCORING
# =====================================================================
print("\n" + "=" * 70)
print("12. BASE-5 TEXT QUALITY CHECK")
print("=" * 70)

# Generate the base-5 decoded text and look for patterns
decoded_b5 = ''.join(chr(v + ord('A')) for v in values)
print(f"\nBase-5 decoded text (first 200 chars):")
print(f"  {decoded_b5[:100]}")
print(f"  {decoded_b5[100:200]}")

# Look for common German words
german_words = ['DER', 'DIE', 'DAS', 'UND', 'IST', 'EIN', 'EINE', 'VON', 'MIT', 'AUF',
                'DEN', 'DEM', 'FUR', 'SICH', 'NICHT', 'HAT', 'WAR', 'ALS', 'SIE', 'ZUR',
                'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER',
                'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'HAD', 'HAS', 'HIS', 'HOW', 'MAN']

print(f"\nSearching for common words in decoded text:")
found = []
for word in german_words:
    count = decoded_b5.count(word)
    if count > 0:
        expected = len(decoded_b5) / (25 ** len(word))
        ratio = count / expected if expected > 0 else 0
        if ratio > 2:  # More than 2x expected
            found.append((word, count, ratio))
            print(f"  '{word}': {count} times (expected ~{expected:.1f}, ratio={ratio:.1f}x)")

if not found:
    print("  No significant word matches found")

# Bigram analysis
print(f"\nBigram frequency (top 15):")
bigrams = Counter(decoded_b5[i:i+2] for i in range(len(decoded_b5)-1))
for bg, cnt in bigrams.most_common(15):
    print(f"  {bg}: {cnt}")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
