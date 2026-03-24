#!/usr/bin/env python3
"""Session 30: Safe per-book DIGIT_SPLIT optimization.

Tests each potential DIGIT_SPLIT change individually, only accepting it if:
1. The target book's coverage improves
2. NO other book's coverage decreases (anagram collision safety)

This avoids the regressions seen when applying all 19 changes at once
(books 53 and 69 broke from 100% due to ANAGRAM_MAP dependencies).
"""
import json, os, sys, re
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json')) as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json')) as f:
    books = json.load(f)

# Current DIGIT_SPLITS from narrative_v3_clean.py
DIGIT_SPLITS = {
    2: (45, '1'), 5: (265, '1'), 6: (12, '0'), 8: (137, '7'),
    10: (169, '0'), 11: (137, '0'), 12: (56, '1'), 13: (45, '0'),
    14: (98, '1'), 15: (98, '0'), 18: (4, '0'), 19: (52, '0'),
    20: (5, '1'), 22: (7, '1'), 23: (22, '4'), 24: (87, '8'),
    25: (0, '0'), 29: (53, '0'), 32: (137, '1'), 34: (101, '0'),
    36: (78, '0'), 39: (44, '0'), 42: (91, '2'), 43: (122, '0'),
    45: (15, '0'), 46: (0, '2'), 48: (126, '0'), 49: (97, '1'),
    50: (16, '6'), 52: (1, '0'), 53: (257, '1'), 54: (49, '1'),
    60: (73, '9'), 61: (93, '7'), 64: (60, '0'), 65: (114, '2'),
    68: (54, '0'),
}

# Load KNOWN and ANAGRAM_MAP from narrative_v3_clean.py
src = open(os.path.join(script_dir, '..', 'core', 'narrative_v3_clean.py')).read()
known_start = src.index("KNOWN = set([")
known_end = src.index("])", known_start) + 2
anagram_start = src.index("ANAGRAM_MAP = {")
anagram_end = src.index("\n}", anagram_start) + 2
exec(src[known_start:known_end])
exec(src[anagram_start:anagram_end])

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

def decode_book(book, digit_splits):
    """Decode a single book with given digit_splits dict."""
    for bidx_inner in sorted(digit_splits.keys()):
        if bidx_inner == id(book):  # placeholder, won't match
            pass
    return None  # not used directly

def decode_all(digit_splits):
    """Decode all books and return per-book resolved text."""
    book_texts = []
    for bidx, book in enumerate(books):
        if bidx in digit_splits:
            sp, d = digit_splits[bidx]
            book = book[:sp] + d + book[sp:]
        off = get_offset(book)
        pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
        text = ''.join(v7.get(p, '?') for p in pairs)
        book_texts.append(text)
    return book_texts

def apply_anagrams(text):
    """Apply ANAGRAM_MAP replacements."""
    for a in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
        text = text.replace(a, ANAGRAM_MAP[a])
    return text

def dp_score(text, known_set):
    """DP coverage score."""
    n = len(text)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        for wlen in range(2, min(i, 20) + 1):
            s = i - wlen
            if text[s:i] in known_set:
                dp[i] = max(dp[i], dp[s] + wlen)
    return dp[n]

# ============================================================
# STEP 1: Baseline per-book coverage
# ============================================================
print("=" * 70)
print("STEP 1: BASELINE PER-BOOK COVERAGE")
print("=" * 70)

baseline_texts = decode_all(DIGIT_SPLITS)
baseline_resolved = [apply_anagrams(t) for t in baseline_texts]
baseline_scores = {}
for bidx, rt in enumerate(baseline_resolved):
    total = sum(1 for c in rt if c != '?')
    if total > 0:
        cov = dp_score(rt, KNOWN)
        baseline_scores[bidx] = (cov, total)

total_cov = sum(c for c, t in baseline_scores.values())
total_chars = sum(t for c, t in baseline_scores.values())
print(f"Baseline: {total_cov}/{total_chars} = {total_cov/total_chars*100:.1f}%\n")

# ============================================================
# STEP 2: Find optimal DIGIT_SPLIT for each odd-length book
# ============================================================
print("=" * 70)
print("STEP 2: FIND POTENTIAL IMPROVEMENTS")
print("=" * 70)

candidates = []
for bidx in sorted(DIGIT_SPLITS.keys()):
    book = books[bidx]
    current_sp, current_d = DIGIT_SPLITS[bidx]
    current_cov, current_total = baseline_scores.get(bidx, (0, 0))
    if current_total == 0:
        continue

    best_cov = current_cov
    best_sp = current_sp
    best_d = current_d

    for d in '0123456789':
        for sp in range(len(book) + 1):
            test_book = book[:sp] + d + book[sp:]
            off = get_offset(test_book)
            pairs = [test_book[j:j+2] for j in range(off, len(test_book)-1, 2)]
            bt = ''.join(v7.get(p, '?') for p in pairs)
            bt = apply_anagrams(bt)
            bt_total = sum(1 for c in bt if c != '?')
            if bt_total == 0:
                continue
            cov = dp_score(bt, KNOWN)
            if cov > best_cov:
                best_cov = cov
                best_sp = sp
                best_d = d

    if best_cov > current_cov:
        delta = best_cov - current_cov
        candidates.append((delta, bidx, current_sp, current_d, best_sp, best_d, current_cov, best_cov, current_total))
        print(f"  Book {bidx:2d}: +{delta} chars  ({current_sp},'{current_d}') -> ({best_sp},'{best_d}')  [{current_cov}/{current_total} -> {best_cov}/{current_total}]")

candidates.sort(key=lambda x: -x[0])
print(f"\n  {len(candidates)} candidates found, total potential: +{sum(d for d,*_ in candidates)} chars")

# ============================================================
# STEP 3: SAFE APPLICATION - test each change individually
# ============================================================
print("\n" + "=" * 70)
print("STEP 3: SAFE APPLICATION (no regressions allowed)")
print("=" * 70)

accepted = []
rejected = []

for delta, bidx, old_sp, old_d, new_sp, new_d, old_cov, new_cov, btotal in candidates:
    # Create modified DIGIT_SPLITS with just this one change
    test_splits = dict(DIGIT_SPLITS)
    test_splits[bidx] = (new_sp, new_d)

    # Apply any previously accepted changes too
    for _, abidx, _, _, asp, ad, _, _, _ in accepted:
        test_splits[abidx] = (asp, ad)

    # Decode ALL books with this change
    test_texts = decode_all(test_splits)
    test_resolved = [apply_anagrams(t) for t in test_texts]

    # Check every book for regressions
    regression = False
    regressions = []
    for check_bidx, rt in enumerate(test_resolved):
        check_total = sum(1 for c in rt if c != '?')
        if check_total == 0:
            continue
        check_cov = dp_score(rt, KNOWN)
        base_cov, base_total = baseline_scores.get(check_bidx, (0, 0))
        # Also check against accepted changes
        if check_cov < base_cov and check_bidx != bidx:
            regression = True
            regressions.append((check_bidx, base_cov, check_cov))

    if regression:
        reg_str = ', '.join(f"book {b}: {bc}->{cc}" for b, bc, cc in regressions)
        print(f"  REJECT book {bidx}: +{delta} but regressions: {reg_str}")
        rejected.append((bidx, delta, regressions))
    else:
        # Verify the target book actually improved
        target_cov = dp_score(test_resolved[bidx], KNOWN)
        target_total = sum(1 for c in test_resolved[bidx] if c != '?')
        actual_delta = target_cov - old_cov
        if actual_delta > 0:
            print(f"  ACCEPT book {bidx}: +{actual_delta} chars  ({old_sp},'{old_d}') -> ({new_sp},'{new_d}')  [{old_cov}/{btotal} -> {target_cov}/{btotal}]")
            accepted.append((delta, bidx, old_sp, old_d, new_sp, new_d, old_cov, target_cov, btotal))
        else:
            print(f"  SKIP book {bidx}: no actual improvement after stacking")

# ============================================================
# STEP 4: VERIFY FINAL STATE
# ============================================================
print("\n" + "=" * 70)
print("STEP 4: FINAL VERIFICATION")
print("=" * 70)

if accepted:
    final_splits = dict(DIGIT_SPLITS)
    for _, bidx, _, _, new_sp, new_d, _, _, _ in accepted:
        final_splits[bidx] = (new_sp, new_d)

    final_texts = decode_all(final_splits)
    final_resolved = [apply_anagrams(t) for t in final_texts]

    print("\nPer-book comparison (changed books only):")
    total_gain = 0
    any_regression = False
    for check_bidx, rt in enumerate(final_resolved):
        check_total = sum(1 for c in rt if c != '?')
        if check_total == 0:
            continue
        check_cov = dp_score(rt, KNOWN)
        base_cov, base_total = baseline_scores.get(check_bidx, (0, 0))
        diff = check_cov - base_cov
        if diff != 0:
            marker = "+" if diff > 0 else "REGRESSION"
            print(f"  Book {check_bidx:2d}: {base_cov}/{base_total} -> {check_cov}/{check_total}  ({marker}{diff})")
            total_gain += diff
            if diff < 0:
                any_regression = True

    new_total_cov = sum(dp_score(rt, KNOWN) for rt in final_resolved
                        if sum(1 for c in rt if c != '?') > 0)
    new_total_chars = sum(sum(1 for c in rt if c != '?') for rt in final_resolved)
    print(f"\nFinal: {new_total_cov}/{new_total_chars} = {new_total_cov/new_total_chars*100:.1f}%")
    print(f"Gain: +{total_gain} chars ({total_cov/total_chars*100:.1f}% -> {new_total_cov/new_total_chars*100:.1f}%)")
    print(f"Any regressions: {'YES - DO NOT APPLY' if any_regression else 'NO - SAFE TO APPLY'}")

    if not any_regression:
        print("\n" + "=" * 70)
        print("SAFE DIGIT_SPLIT UPDATES TO APPLY:")
        print("=" * 70)
        for _, bidx, old_sp, old_d, new_sp, new_d, old_cov, new_cov, btotal in accepted:
            print(f"    {bidx}: ({old_sp}, '{old_d}') -> ({new_sp}, '{new_d}'),  # +{new_cov - old_cov} chars")
else:
    print("No changes accepted - all candidates caused regressions.")
    print(f"Current: {total_cov}/{total_chars} = {total_cov/total_chars*100:.1f}%")
