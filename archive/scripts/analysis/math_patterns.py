#!/usr/bin/env python3
"""
Mathematical pattern analysis for the Tibia Bonelord 469 cipher.
Analyzes v7 mapping for structural, numerical, and frequency patterns.
"""

import json
import os
import math
from collections import Counter, defaultdict
from itertools import product

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "..", "data")

MAPPING_PATH = os.path.join(DATA_DIR, "mapping_v7.json")
BOOKS_PATH = os.path.join(DATA_DIR, "books.json")

# German letter frequencies (approximate, in %)
GERMAN_FREQ = {
    'E': 17.40, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
    'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
    'L': 3.44, 'C': 3.06, 'G': 3.01, 'M': 2.53, 'O': 2.51,
    'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
    'P': 0.79, 'V': 0.67, 'J': 0.27, 'Y': 0.04, 'X': 0.03,
    'Q': 0.02
}

SEPARATOR = "=" * 72


def load_data():
    with open(MAPPING_PATH, "r") as f:
        mapping = json.load(f)
    with open(BOOKS_PATH, "r") as f:
        books = json.load(f)
    return mapping, books


def letter_pos(ch):
    """A=0, B=1, ..., Z=25"""
    return ord(ch.upper()) - ord('A')


def pos_letter(p):
    """0=A, 1=B, ..., 25=Z"""
    return chr((p % 26) + ord('A'))


# ─────────────────────────────────────────────────────────────────────────────
# 1. Units digit clustering
# ─────────────────────────────────────────────────────────────────────────────
def analysis_units_digit(mapping):
    print(f"\n{SEPARATOR}")
    print("1. UNITS DIGIT CLUSTERING")
    print(SEPARATOR)

    groups = defaultdict(list)
    for code, letter in sorted(mapping.items()):
        units = int(code) % 10
        groups[units].append((code, letter))

    for d in range(10):
        entries = groups.get(d, [])
        letters = [e[1] for e in entries]
        freq = Counter(letters)
        codes_str = ", ".join(f"{c}->{l}" for c, l in entries)
        print(f"\n  Units digit {d}: ({len(entries)} codes)")
        print(f"    Codes: {codes_str}")
        print(f"    Letter freq: {dict(sorted(freq.items(), key=lambda x: -x[1]))}")

    # Chi-square-like metric: for each units digit, how concentrated are letters?
    print("\n  Concentration metric (entropy per units group, lower = more clustered):")
    for d in range(10):
        entries = groups.get(d, [])
        if not entries:
            print(f"    Units {d}: no codes")
            continue
        letters = [e[1] for e in entries]
        freq = Counter(letters)
        n = len(letters)
        entropy = -sum((c / n) * math.log2(c / n) for c in freq.values())
        max_entropy = math.log2(n) if n > 1 else 0
        print(f"    Units {d}: entropy={entropy:.3f} (max possible={max_entropy:.3f}), "
              f"dominant={freq.most_common(1)[0] if freq else 'N/A'}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. Tens digit clustering
# ─────────────────────────────────────────────────────────────────────────────
def analysis_tens_digit(mapping):
    print(f"\n{SEPARATOR}")
    print("2. TENS DIGIT CLUSTERING")
    print(SEPARATOR)

    groups = defaultdict(list)
    for code, letter in sorted(mapping.items()):
        tens = int(code) // 10
        groups[tens].append((code, letter))

    for d in range(10):
        entries = groups.get(d, [])
        letters = [e[1] for e in entries]
        freq = Counter(letters)
        codes_str = ", ".join(f"{c}->{l}" for c, l in entries)
        print(f"\n  Tens digit {d}: ({len(entries)} codes)")
        print(f"    Codes: {codes_str}")
        print(f"    Letter freq: {dict(sorted(freq.items(), key=lambda x: -x[1]))}")

    print("\n  Concentration metric (entropy per tens group):")
    for d in range(10):
        entries = groups.get(d, [])
        if not entries:
            print(f"    Tens {d}: no codes")
            continue
        letters = [e[1] for e in entries]
        freq = Counter(letters)
        n = len(letters)
        entropy = -sum((c / n) * math.log2(c / n) for c in freq.values())
        max_entropy = math.log2(n) if n > 1 else 0
        print(f"    Tens {d}: entropy={entropy:.3f} (max possible={max_entropy:.3f}), "
              f"dominant={freq.most_common(1)[0] if freq else 'N/A'}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Digit sum patterns
# ─────────────────────────────────────────────────────────────────────────────
def analysis_digit_sum(mapping):
    print(f"\n{SEPARATOR}")
    print("3. DIGIT SUM PATTERNS")
    print(SEPARATOR)

    groups = defaultdict(list)
    for code, letter in sorted(mapping.items()):
        d1 = int(code) // 10
        d2 = int(code) % 10
        dsum = d1 + d2
        groups[dsum].append((code, letter))

    for s in range(19):
        entries = groups.get(s, [])
        if not entries:
            continue
        letters = [e[1] for e in entries]
        freq = Counter(letters)
        codes_str = ", ".join(f"{c}->{l}" for c, l in entries)
        print(f"\n  Digit sum {s:2d}: ({len(entries)} codes)")
        print(f"    Codes: {codes_str}")
        print(f"    Letter freq: {dict(sorted(freq.items(), key=lambda x: -x[1]))}")

    # Check: digit sum mod N -> letter position?
    print("\n  Checking digit_sum mod N -> letter_pos correlation:")
    for mod_val in [5, 7, 13, 26]:
        matches = 0
        for code, letter in mapping.items():
            d1 = int(code) // 10
            d2 = int(code) % 10
            if (d1 + d2) % mod_val == letter_pos(letter) % mod_val:
                matches += 1
        pct = 100 * matches / len(mapping)
        expected = 100 / mod_val
        print(f"    digit_sum mod {mod_val:2d} == letter_pos mod {mod_val:2d}: "
              f"{matches}/{len(mapping)} ({pct:.1f}%, expected random ~{expected:.1f}%)")


# ─────────────────────────────────────────────────────────────────────────────
# 4. Mathematical formula search
# ─────────────────────────────────────────────────────────────────────────────
def analysis_formula_search(mapping):
    print(f"\n{SEPARATOR}")
    print("4. MATHEMATICAL FORMULA SEARCH")
    print(SEPARATOR)

    codes_letters = [(int(c), letter_pos(l)) for c, l in mapping.items()]
    n = len(codes_letters)

    # 4a. (a * code + b) mod 26
    print("\n  4a. Testing (a * code + b) mod 26:")
    best_linear = (0, 0, 0)
    for a in range(26):
        for b in range(26):
            matches = sum(1 for code, lp in codes_letters if (a * code + b) % 26 == lp)
            if matches > best_linear[2]:
                best_linear = (a, b, matches)
    a, b, m = best_linear
    pct = 100 * m / n
    print(f"    Best: ({a} * code + {b}) mod 26 => {m}/{n} matches ({pct:.1f}%)")
    expected = n / 26
    print(f"    Expected by chance: ~{expected:.1f}")

    # 4b. (a * d1 + b * d2 + c) mod 26
    print("\n  4b. Testing (a * d1 + b * d2 + c) mod 26:")
    best_bilinear = (0, 0, 0, 0)
    for a in range(26):
        for b in range(26):
            for c in range(26):
                matches = sum(1 for code, lp in codes_letters
                              if (a * (code // 10) + b * (code % 10) + c) % 26 == lp)
                if matches > best_bilinear[3]:
                    best_bilinear = (a, b, c, matches)
    a, b, c, m = best_bilinear
    pct = 100 * m / n
    print(f"    Best: ({a}*d1 + {b}*d2 + {c}) mod 26 => {m}/{n} matches ({pct:.1f}%)")

    # 4c. (a * d1 * d2 + b * d1 + c * d2 + d) mod 26
    print("\n  4c. Testing (a*d1*d2 + b*d1 + c*d2 + d) mod 26 (quadratic):")
    best_quad = (0, 0, 0, 0, 0)
    # Reduced search: a in 0..25, b,c,d in 0..25, but only check promising a values
    for a in range(26):
        for b in range(26):
            for c in range(26):
                # Quick inner loop with fixed a,b,c
                residuals = [(lp - a * (code // 10) * (code % 10) - b * (code // 10) - c * (code % 10)) % 26
                             for code, lp in codes_letters]
                d_counts = Counter(residuals)
                best_d, best_count = d_counts.most_common(1)[0]
                if best_count > best_quad[4]:
                    best_quad = (a, b, c, best_d, best_count)
    a, b, c, d, m = best_quad
    pct = 100 * m / n
    print(f"    Best: ({a}*d1*d2 + {b}*d1 + {c}*d2 + {d}) mod 26 => {m}/{n} matches ({pct:.1f}%)")

    # 4d. (code * a) mod b for various b near 26-30
    print("\n  4d. Testing (code * a) mod b -> letter_pos:")
    best_modn = (0, 0, 0)
    for mod_b in range(20, 35):
        for a in range(1, mod_b):
            matches = sum(1 for code, lp in codes_letters if (code * a) % mod_b == lp)
            if matches > best_modn[2]:
                best_modn = (a, mod_b, matches)
    a, b, m = best_modn
    pct = 100 * m / n
    print(f"    Best: (code * {a}) mod {b} => {m}/{n} matches ({pct:.1f}%)")


# ─────────────────────────────────────────────────────────────────────────────
# 5. The number 469
# ─────────────────────────────────────────────────────────────────────────────
def analysis_469(mapping):
    print(f"\n{SEPARATOR}")
    print("5. THE NUMBER 469 (= 7 x 67)")
    print(SEPARATOR)

    codes_letters = [(int(c), letter_pos(l)) for c, l in mapping.items()]
    n = len(codes_letters)

    # 5a. code XOR with 469-related values
    print("\n  5a. XOR tests:")
    for xor_val in [469, 469 % 100, 7, 67, 4, 6, 9, 46, 69, 49]:
        matches = sum(1 for code, lp in codes_letters
                      if (code ^ xor_val) % 26 == lp)
        print(f"    (code XOR {xor_val:3d}) mod 26 == letter_pos: {matches}/{n}")

    # 5b. code mod 7, code mod 67
    print("\n  5b. Modular residue clustering:")
    for mod_val in [7, 67]:
        groups = defaultdict(list)
        for code, letter in sorted(mapping.items()):
            r = int(code) % mod_val
            groups[r].append((code, letter))
        print(f"\n    code mod {mod_val}:")
        for r in sorted(groups.keys()):
            entries = groups[r]
            letters = [e[1] for e in entries]
            freq = Counter(letters)
            codes_list = [e[0] for e in entries]
            print(f"      r={r}: codes={codes_list}, letters={dict(freq)}")

    # 5c. (code * 469) mod various
    print("\n  5c. (code * 469) mod N tests:")
    for mod_n in [26, 29, 30, 31, 32, 97, 100, 127]:
        matches = sum(1 for code, lp in codes_letters
                      if (code * 469) % mod_n == lp)
        pct = 100 * matches / n
        print(f"    (code * 469) mod {mod_n:3d}: {matches}/{n} ({pct:.1f}%)")

    # 5d. (code + 469) mod 26, (code - 469) mod 26
    print("\n  5d. Additive 469 tests:")
    for op_name, func in [("code + 469", lambda c: (c + 469) % 26),
                           ("code + 69", lambda c: (c + 69) % 26),
                           ("code + 46", lambda c: (c + 46) % 26),
                           ("code * 4 + 69", lambda c: (c * 4 + 69) % 26),
                           ("code * 46 + 9", lambda c: (c * 46 + 9) % 26),
                           ("code * 4 * 6 + 9", lambda c: (c * 24 + 9) % 26)]:
        matches = sum(1 for code, lp in codes_letters if func(code) == lp)
        print(f"    ({op_name}) mod 26: {matches}/{n}")


# ─────────────────────────────────────────────────────────────────────────────
# 6. 486486 (bonelord race name)
# ─────────────────────────────────────────────────────────────────────────────
def analysis_486486(mapping):
    print(f"\n{SEPARATOR}")
    print("6. 486486 (= 2 x 3^5 x 7 x 11 x 13 = 486 x 1001 = 486 x 7 x 11 x 13)")
    print(SEPARATOR)

    codes_letters = [(int(c), letter_pos(l)) for c, l in mapping.items()]
    n = len(codes_letters)

    # Factors of 486486
    factors = [2, 3, 6, 7, 9, 11, 13, 14, 18, 21, 22, 26, 27, 33, 39, 42,
               54, 66, 77, 78, 91, 143, 154, 162, 231, 243, 286, 462, 486,
               693, 1001, 1386, 2002, 3003, 6006, 486486]

    print("\n  (code * factor) mod 26 tests for factors of 486486:")
    for f in factors:
        if f > 10000:
            continue
        matches = sum(1 for code, lp in codes_letters if (code * f) % 26 == lp)
        if matches > n / 26 + 2:  # Only show above-chance
            pct = 100 * matches / n
            print(f"    (code * {f:4d}) mod 26: {matches}/{n} ({pct:.1f}%)")

    # Check code mod factor patterns
    print("\n  Residue patterns for key factors:")
    for mod_val in [7, 11, 13]:
        groups = defaultdict(Counter)
        for code, lp in codes_letters:
            r = code % mod_val
            groups[r][pos_letter(lp)] += 1
        print(f"\n    code mod {mod_val}:")
        for r in sorted(groups.keys()):
            dominant = groups[r].most_common(3)
            total = sum(groups[r].values())
            dom_str = ", ".join(f"{l}:{c}" for l, c in dominant)
            print(f"      r={r} ({total} codes): top letters = {dom_str}")

    # 486 specific
    print("\n  486-related tests:")
    for val in [486, 486 % 100, 486 % 26]:
        matches = sum(1 for code, lp in codes_letters if (code + val) % 26 == lp)
        print(f"    (code + {val}) mod 26: {matches}/{n}")
    for val in [486, 486 % 100, 486 % 26]:
        matches = sum(1 for code, lp in codes_letters if (code * val) % 26 == lp)
        print(f"    (code * {val}) mod 26: {matches}/{n}")


# ─────────────────────────────────────────────────────────────────────────────
# 7. Base-5 interpretation (bonelords have 5 eyes)
# ─────────────────────────────────────────────────────────────────────────────
def analysis_base5(mapping):
    print(f"\n{SEPARATOR}")
    print("7. BASE-5 / 5-BIT INTERPRETATION")
    print(SEPARATOR)

    codes_letters = [(int(c), letter_pos(l)) for c, l in mapping.items()]
    n = len(codes_letters)

    # 7a. Interpret code as base-5: d1*5 + d2
    print("\n  7a. Interpret 2-digit code as base-5 number (d1*5 + d2):")
    print("      (Only valid if both digits 0-4)")
    valid = [(code, lp) for code, lp in codes_letters if code // 10 < 5 and code % 10 < 5]
    print(f"      Valid codes (both digits <5): {len(valid)}/{n}")
    if valid:
        matches = sum(1 for code, lp in valid if (code // 10) * 5 + (code % 10) == lp)
        print(f"      Direct d1*5+d2 == letter_pos: {matches}/{len(valid)}")
        # Try with offset
        for offset in range(26):
            matches = sum(1 for code, lp in valid
                          if ((code // 10) * 5 + (code % 10) + offset) % 26 == lp)
            if matches > len(valid) / 26 + 1:
                print(f"      (d1*5+d2+{offset}) mod 26 == letter_pos: {matches}/{len(valid)}")

    # 7b. 5-bit binary: code -> 5-bit pattern -> letter
    print("\n  7b. Code mod 32 -> 5-bit -> letter_pos:")
    for offset in range(26):
        matches = sum(1 for code, lp in codes_letters if (code % 32 + offset) % 26 == lp)
        if matches > n / 26 + 2:
            print(f"      (code mod 32 + {offset}) mod 26: {matches}/{n}")

    # 7c. Check if code XOR with 5-based masks gives letter positions
    print("\n  7c. XOR with 5-based values:")
    for xor_val in [5, 25, 31, 15, 10, 20]:
        matches = sum(1 for code, lp in codes_letters if (code ^ xor_val) % 26 == lp)
        print(f"      (code XOR {xor_val:2d}) mod 26: {matches}/{n}")

    # 7d. Interpret digits as base-5 trits from different decomposition
    print("\n  7d. Alternative base-5 decompositions of code value:")
    # code = a*25 + b*5 + c (base-5 with 3 digits: codes 0-99 fit in 0-4,0-4,0-4 for <125)
    for perm_a, perm_b in [(1, 0), (0, 1), (2, 0), (0, 2), (1, 1), (2, 1), (1, 2)]:
        matches = sum(1 for code, lp in codes_letters
                      if ((code // 25) * perm_a + ((code % 25) // 5) * perm_b + (code % 5)) % 26 == lp)
        if matches > n / 26 + 1:
            print(f"      base5: [{perm_a}*c2 + {perm_b}*c1 + c0] mod 26: {matches}/{n}")


# ─────────────────────────────────────────────────────────────────────────────
# 8. "0 is obscene" - special codes analysis
# ─────────────────────────────────────────────────────────────────────────────
def analysis_zero_obscene(mapping):
    print(f"\n{SEPARATOR}")
    print("8. '0 IS OBSCENE' - SPECIAL CODES ANALYSIS")
    print(SEPARATOR)

    all_codes = set(f"{i:02d}" for i in range(100))
    mapped_codes = set(mapping.keys())
    missing_codes = sorted(all_codes - mapped_codes)

    print(f"\n  Missing codes (not in mapping): {missing_codes}")
    missing_ints = [int(c) for c in missing_codes]
    print(f"  As integers: {missing_ints}")

    # Properties of missing codes
    print("\n  Properties of missing codes:")
    for c in missing_codes:
        ci = int(c)
        d1, d2 = ci // 10, ci % 10
        print(f"    {c}: d1={d1}, d2={d2}, sum={d1+d2}, prod={d1*d2}, "
              f"mod7={ci%7}, mod13={ci%13}, mod67={ci%67}")

    # Check if 07 and 32 have special properties
    print("\n  Special analysis of 07 and 32:")
    for code_val in [7, 32]:
        print(f"    Code {code_val:02d}:")
        print(f"      mod 7 = {code_val % 7}, mod 13 = {code_val % 13}")
        print(f"      Binary: {bin(code_val)}")
        print(f"      In base 5: {code_val // 25},{(code_val % 25) // 5},{code_val % 5}")
        print(f"      Is prime: {all(code_val % i != 0 for i in range(2, code_val)) if code_val > 1 else False}")

    # Letter positions never assigned
    assigned_letters = set(mapping.values())
    all_letters = set(chr(i) for i in range(ord('A'), ord('Z') + 1))
    missing_letters = sorted(all_letters - assigned_letters)
    print(f"\n  Letters NEVER assigned to any code: {missing_letters}")
    if missing_letters:
        for l in missing_letters:
            pos = letter_pos(l)
            print(f"    {l}: position={pos}, German freq={GERMAN_FREQ.get(l, 0):.2f}%")

    # Check if codes containing 0 have any pattern
    print("\n  Codes containing digit 0:")
    zero_codes = [(c, mapping.get(c, '?')) for c in all_codes if '0' in c]
    for c, l in sorted(zero_codes):
        status = "MAPPED" if c in mapped_codes else "MISSING"
        print(f"    {c} -> {l} [{status}]")

    # Count how many of each digit 0-9 appear in missing vs mapped codes
    print("\n  Digit frequency in missing vs mapped codes:")
    missing_digits = Counter()
    mapped_digits = Counter()
    for c in missing_codes:
        for d in c:
            missing_digits[d] += 1
    for c in mapped_codes:
        for d in c:
            mapped_digits[d] += 1
    for d in '0123456789':
        print(f"    Digit {d}: missing={missing_digits.get(d, 0)}, mapped={mapped_digits.get(d, 0)}")


# ─────────────────────────────────────────────────────────────────────────────
# 9. Complementary codes (sum to 99)
# ─────────────────────────────────────────────────────────────────────────────
def analysis_complementary(mapping):
    print(f"\n{SEPARATOR}")
    print("9. COMPLEMENTARY CODES (SUM TO 99)")
    print(SEPARATOR)

    print("\n  Pairs summing to 99:")
    same_count = 0
    total_pairs = 0
    for i in range(50):
        c1 = f"{i:02d}"
        c2 = f"{99 - i:02d}"
        l1 = mapping.get(c1, "?")
        l2 = mapping.get(c2, "?")
        if l1 != "?" and l2 != "?":
            same = "SAME" if l1 == l2 else ""
            diff = abs(letter_pos(l1) - letter_pos(l2)) if l1 != "?" and l2 != "?" else "?"
            print(f"    {c1}({l1}) + {c2}({l2}) = 99  |  diff={diff:2d}  {same}")
            total_pairs += 1
            if l1 == l2:
                same_count += 1
    print(f"\n  Same letter pairs: {same_count}/{total_pairs}")
    expected = total_pairs / 26
    print(f"  Expected by chance: ~{expected:.1f}")

    # Also check sums to 100
    print("\n  Pairs summing to 100:")
    same_100 = 0
    total_100 = 0
    for i in range(50):
        c1 = f"{i:02d}"
        c2 = f"{100 - i:02d}" if 100 - i < 100 else None
        if c2 is None:
            continue
        l1 = mapping.get(c1, "?")
        l2 = mapping.get(c2, "?")
        if l1 != "?" and l2 != "?":
            same = "SAME" if l1 == l2 else ""
            diff = abs(letter_pos(l1) - letter_pos(l2))
            print(f"    {c1}({l1}) + {c2}({l2}) = 100 |  diff={diff:2d}  {same}")
            total_100 += 1
            if l1 == l2:
                same_100 += 1
    if total_100 > 0:
        print(f"\n  Same letter pairs: {same_100}/{total_100}")

    # Check digit-reversal pairs (ab -> ba)
    print("\n  Digit reversal pairs (ab <-> ba):")
    rev_same = 0
    rev_total = 0
    for i in range(10):
        for j in range(i + 1, 10):
            c1 = f"{i}{j}"
            c2 = f"{j}{i}"
            l1 = mapping.get(c1, "?")
            l2 = mapping.get(c2, "?")
            if l1 != "?" and l2 != "?":
                same = "SAME" if l1 == l2 else ""
                print(f"    {c1}({l1}) <-> {c2}({l2})  {same}")
                rev_total += 1
                if l1 == l2:
                    rev_same += 1
    print(f"\n  Same letter reversals: {rev_same}/{rev_total}")
    expected = rev_total / 26
    print(f"  Expected by chance: ~{expected:.1f}")


# ─────────────────────────────────────────────────────────────────────────────
# 10. Code frequency from books data
# ─────────────────────────────────────────────────────────────────────────────
def index_of_coincidence(pairs):
    """Calculate IC for a list of 2-digit code strings."""
    freq = Counter(pairs)
    n = len(pairs)
    if n <= 1:
        return 0
    ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    return ic


def parse_books(books, mapping):
    """Parse books into code pairs using IC-based offset detection."""
    all_pairs = []

    for idx, book in enumerate(books):
        digits = book.strip()
        # Try offset 0 and offset 1
        pairs_0 = [digits[i:i+2] for i in range(0, len(digits) - 1, 2)]
        pairs_1 = [digits[i:i+2] for i in range(1, len(digits) - 1, 2)]

        ic_0 = index_of_coincidence(pairs_0)
        ic_1 = index_of_coincidence(pairs_1)

        if ic_0 >= ic_1:
            chosen_pairs = pairs_0
            chosen_offset = 0
        else:
            chosen_pairs = pairs_1
            chosen_offset = 1

        all_pairs.extend(chosen_pairs)

    return all_pairs


def analysis_frequency(mapping, books):
    print(f"\n{SEPARATOR}")
    print("10. CODE FREQUENCY FROM BOOKS DATA")
    print(SEPARATOR)

    all_pairs = parse_books(books, mapping)
    total = len(all_pairs)
    code_freq = Counter(all_pairs)

    print(f"\n  Total code pairs parsed: {total}")
    print(f"  Unique codes seen: {len(code_freq)}")

    # Show frequency of each code
    print("\n  Code frequencies (sorted by count):")
    for code, count in code_freq.most_common():
        letter = mapping.get(code, "?")
        pct = 100 * count / total
        print(f"    {code} -> {letter}: {count:4d} ({pct:5.2f}%)")

    # Codes in mapping but never seen
    never_seen = set(mapping.keys()) - set(code_freq.keys())
    if never_seen:
        print(f"\n  Codes in mapping but never seen in books: {sorted(never_seen)}")

    # Codes seen but not in mapping
    unmapped_seen = set(code_freq.keys()) - set(mapping.keys())
    if unmapped_seen:
        unmapped_detail = sorted([(c, code_freq[c]) for c in unmapped_seen],
                                 key=lambda x: -x[1])
        print(f"\n  Codes seen in books but NOT in mapping:")
        for c, cnt in unmapped_detail:
            print(f"    {c}: {cnt} times")

    # Aggregate by letter: sum frequencies of all codes mapping to same letter
    print("\n  Letter frequency comparison (observed vs expected German):")
    letter_counts = Counter()
    for code, count in code_freq.items():
        letter = mapping.get(code, None)
        if letter:
            letter_counts[letter] += count

    letter_total = sum(letter_counts.values())

    # Calculate the number of codes allocated to each letter
    codes_per_letter = Counter()
    for code, letter in mapping.items():
        codes_per_letter[letter] += 1

    print(f"\n  {'Letter':>6} {'Codes':>5} {'Obs_Count':>9} {'Obs%':>7} {'German%':>8} {'Ratio':>7}")
    print(f"  {'-'*6:>6} {'-'*5:>5} {'-'*9:>9} {'-'*7:>7} {'-'*8:>8} {'-'*7:>7}")
    for letter in sorted(GERMAN_FREQ.keys(), key=lambda l: -GERMAN_FREQ[l]):
        obs_count = letter_counts.get(letter, 0)
        obs_pct = 100 * obs_count / letter_total if letter_total > 0 else 0
        exp_pct = GERMAN_FREQ.get(letter, 0)
        ratio = obs_pct / exp_pct if exp_pct > 0 else float('inf')
        n_codes = codes_per_letter.get(letter, 0)
        print(f"  {letter:>6} {n_codes:>5} {obs_count:>9} {obs_pct:>6.2f}% {exp_pct:>7.2f}% {ratio:>6.2f}")

    # Proportionality check: are # of codes ~ proportional to German frequency?
    print("\n  Proportionality: codes_per_letter vs German freq:")
    print(f"  {'Letter':>6} {'#Codes':>6} {'Expected_codes':>14} {'Ratio':>7}")
    total_codes = len(mapping)
    total_freq = sum(GERMAN_FREQ[l] for l in codes_per_letter if l in GERMAN_FREQ)
    for letter in sorted(codes_per_letter.keys(), key=lambda l: -GERMAN_FREQ.get(l, 0)):
        n_codes = codes_per_letter[letter]
        expected = total_codes * GERMAN_FREQ.get(letter, 0) / total_freq
        ratio = n_codes / expected if expected > 0 else float('inf')
        print(f"  {letter:>6} {n_codes:>6} {expected:>13.2f} {ratio:>6.2f}")

    # IC analysis per book
    print("\n  Index of Coincidence per book (offset selection):")
    for idx, book in enumerate(books):
        digits = book.strip()
        pairs_0 = [digits[i:i+2] for i in range(0, len(digits) - 1, 2)]
        pairs_1 = [digits[i:i+2] for i in range(1, len(digits) - 1, 2)]
        ic_0 = index_of_coincidence(pairs_0)
        ic_1 = index_of_coincidence(pairs_1)
        chosen = 0 if ic_0 >= ic_1 else 1
        ic_chosen = max(ic_0, ic_1)
        if idx < 10 or ic_chosen > 0.02:
            print(f"    Book {idx:2d}: IC(off=0)={ic_0:.5f}, IC(off=1)={ic_1:.5f}, "
                  f"chosen={chosen}, len={len(digits)}")
    print(f"    ... (showing first 10 + notable ICs)")


# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────
def summary(mapping):
    print(f"\n{SEPARATOR}")
    print("SUMMARY OF MAPPING STATISTICS")
    print(SEPARATOR)

    # Basic stats
    letter_counts = Counter(mapping.values())
    print(f"\n  Total codes mapped: {len(mapping)}")
    print(f"  Unique letters used: {len(letter_counts)}")
    print(f"  Letter distribution: {dict(sorted(letter_counts.items(), key=lambda x: -x[1]))}")

    # Most and least assigned
    print(f"\n  Most codes: {letter_counts.most_common(5)}")
    print(f"  Fewest codes: {letter_counts.most_common()[-5:]}")

    # Homophonic ratio
    print(f"\n  Codes per letter vs German frequency ranking:")
    german_rank = sorted(GERMAN_FREQ.keys(), key=lambda l: -GERMAN_FREQ[l])
    code_rank = sorted(letter_counts.keys(), key=lambda l: -letter_counts[l])
    print(f"    By German freq: {' '.join(german_rank[:15])}")
    print(f"    By code count:  {' '.join(code_rank[:15])}")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    mapping, books = load_data()
    print("BONELORD 469 CIPHER - MATHEMATICAL PATTERN ANALYSIS")
    print(f"Mapping: {len(mapping)} codes, Books: {len(books)} texts")

    summary(mapping)
    analysis_units_digit(mapping)
    analysis_tens_digit(mapping)
    analysis_digit_sum(mapping)
    analysis_formula_search(mapping)
    analysis_469(mapping)
    analysis_486486(mapping)
    analysis_base5(mapping)
    analysis_zero_obscene(mapping)
    analysis_complementary(mapping)
    analysis_frequency(mapping, books)

    print(f"\n{SEPARATOR}")
    print("ANALYSIS COMPLETE")
    print(SEPARATOR)


if __name__ == "__main__":
    main()
