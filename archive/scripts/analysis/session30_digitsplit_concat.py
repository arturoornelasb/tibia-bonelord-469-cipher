#!/usr/bin/env python3
"""Session 30: DIGIT_SPLIT optimizer using concatenated text (matching real pipeline).

The per-book optimizer missed cross-book boundary effects from ANAGRAM_MAP
applied on concatenated text. This version replicates the exact pipeline.
Tests each change individually on the full concatenated text.
"""
import json, os, sys
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json')) as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json')) as f:
    books = json.load(f)

# ORIGINAL DIGIT_SPLITS (before session 30 changes)
ORIGINAL_SPLITS = {
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

# All 19 proposed changes
PROPOSED = {
    2: (34, '0'), 6: (20, '0'), 10: (277, '2'), 12: (0, '0'),
    13: (55, '0'), 15: (36, '6'), 23: (14, '0'), 24: (47, '8'),
    29: (151, '1'), 36: (16, '1'), 43: (26, '1'), 45: (23, '7'),
    48: (127, '0'), 50: (136, '2'), 52: (0, '4'), 53: (248, '2'),
    64: (58, '4'), 65: (94, '0'), 68: (4, '0'),
}

# Load KNOWN and ANAGRAM_MAP
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

def dp_score(text, known_set):
    n = len(text)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        for wlen in range(2, min(i, 20) + 1):
            s = i - wlen
            if text[s:i] in known_set:
                dp[i] = max(dp[i], dp[s] + wlen)
    return dp[n]

def full_pipeline(digit_splits):
    """Run the exact pipeline: decode -> concatenate -> anagrams -> dp_score.
    Returns (global_cov, global_total, per_book_scores).
    """
    # Decode all books
    decoded = []
    for bidx, book in enumerate(books):
        if bidx in digit_splits:
            sp, d = digit_splits[bidx]
            book = book[:sp] + d + book[sp:]
        off = get_offset(book)
        pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
        text = ''.join(v7.get(p, '?') for p in pairs)
        decoded.append(text)

    # Concatenate
    all_text = ''.join(decoded)

    # Apply anagrams on concatenated text (exactly like the real pipeline)
    resolved = all_text
    for a in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
        resolved = resolved.replace(a, ANAGRAM_MAP[a])

    # Split back into per-book chunks
    book_boundaries = []
    pos = 0
    for t in decoded:
        book_boundaries.append(pos)
        pos += len(t)

    # Global score
    total = sum(1 for c in resolved if c != '?')
    cov = dp_score(resolved, KNOWN)

    # Per-book scores on resolved text
    # Note: anagram replacements can change lengths, making per-book boundaries approximate.
    # Instead, compute per-book by applying anagrams per-book
    per_book = {}
    for bidx, text in enumerate(decoded):
        rt = text
        for a in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
            rt = rt.replace(a, ANAGRAM_MAP[a])
        bt = sum(1 for c in rt if c != '?')
        if bt > 0:
            bc = dp_score(rt, KNOWN)
            per_book[bidx] = (bc, bt)

    return cov, total, per_book

# ============================================================
# BASELINE
# ============================================================
print("=" * 70)
print("BASELINE (original DIGIT_SPLITS)")
print("=" * 70)
base_cov, base_total, base_per_book = full_pipeline(ORIGINAL_SPLITS)
print(f"Global: {base_cov}/{base_total} = {base_cov/base_total*100:.1f}%")

# ============================================================
# TEST EACH CHANGE INDIVIDUALLY
# ============================================================
print("\n" + "=" * 70)
print("INDIVIDUAL CHANGE TESTING (on concatenated text)")
print("=" * 70)

safe_changes = {}
for bidx in sorted(PROPOSED.keys()):
    new_sp, new_d = PROPOSED[bidx]
    old_sp, old_d = ORIGINAL_SPLITS[bidx]

    test_splits = dict(ORIGINAL_SPLITS)
    test_splits[bidx] = (new_sp, new_d)

    test_cov, test_total, test_per_book = full_pipeline(test_splits)
    delta = test_cov - base_cov

    # Check all per-book for regressions
    regressions = []
    for cb, (bc, bt) in base_per_book.items():
        if cb in test_per_book:
            tc, tt = test_per_book[cb]
            if tc < bc:
                regressions.append((cb, bc, tc, bc-tc))

    if regressions:
        reg_str = ', '.join(f"b{b}:{bc}->{tc}(-{d})" for b,bc,tc,d in regressions)
        print(f"  Book {bidx:2d}: global {delta:+d}  REGRESSIONS: {reg_str}")
    elif delta > 0:
        print(f"  Book {bidx:2d}: global {delta:+d}  SAFE")
        safe_changes[bidx] = (new_sp, new_d)
    elif delta == 0:
        print(f"  Book {bidx:2d}: global +0   NEUTRAL")
        safe_changes[bidx] = (new_sp, new_d)  # Still accept if no regression
    else:
        print(f"  Book {bidx:2d}: global {delta:+d}  WORSE")

# ============================================================
# INCREMENTAL SAFE APPLICATION
# ============================================================
print("\n" + "=" * 70)
print("INCREMENTAL STACKING (apply safe changes one by one)")
print("=" * 70)

accepted = {}
current_splits = dict(ORIGINAL_SPLITS)
current_cov = base_cov

# Sort by individual gain descending
sorted_safe = sorted(safe_changes.items(),
                     key=lambda x: full_pipeline({**ORIGINAL_SPLITS, x[0]: x[1]})[0] - base_cov,
                     reverse=True)

for bidx, (new_sp, new_d) in sorted_safe:
    test_splits = dict(current_splits)
    test_splits[bidx] = (new_sp, new_d)

    test_cov, test_total, test_per_book = full_pipeline(test_splits)

    # Check regressions against current accepted state
    curr_cov_check, _, curr_per_book = full_pipeline(current_splits)
    regressions = []
    for cb, (bc, bt) in curr_per_book.items():
        if cb in test_per_book:
            tc, tt = test_per_book[cb]
            if tc < bc:
                regressions.append((cb, bc, tc))

    if regressions:
        reg_str = ', '.join(f"b{b}:{bc}->{tc}" for b,bc,tc in regressions)
        print(f"  REJECT book {bidx}: regressions after stacking: {reg_str}")
    else:
        gain = test_cov - current_cov
        print(f"  ACCEPT book {bidx}: +{gain} chars  ({ORIGINAL_SPLITS[bidx]}) -> ({new_sp},'{new_d}')")
        accepted[bidx] = (new_sp, new_d)
        current_splits[bidx] = (new_sp, new_d)
        current_cov = test_cov

# ============================================================
# FINAL VERIFICATION
# ============================================================
print("\n" + "=" * 70)
print("FINAL VERIFICATION")
print("=" * 70)

final_splits = dict(ORIGINAL_SPLITS)
final_splits.update(accepted)
final_cov, final_total, final_per_book = full_pipeline(final_splits)

print(f"\nBaseline: {base_cov}/{base_total} = {base_cov/base_total*100:.1f}%")
print(f"Final:    {final_cov}/{final_total} = {final_cov/final_total*100:.1f}%")
print(f"Gain:     +{final_cov - base_cov} chars")

# Check 100% books
for bidx in [5, 25, 53, 69]:
    if bidx in final_per_book:
        bc, bt = base_per_book.get(bidx, (0,0))
        fc, ft = final_per_book[bidx]
        status = "OK" if fc >= bc else "REGRESSION"
        print(f"  Book {bidx}: {bc}/{bt} -> {fc}/{ft}  {status}")

# Check all regressions
any_reg = False
for bidx in sorted(final_per_book.keys()):
    bc, bt = base_per_book.get(bidx, (0,0))
    fc, ft = final_per_book[bidx]
    if fc < bc:
        print(f"  REGRESSION book {bidx}: {bc}/{bt} -> {fc}/{ft}")
        any_reg = True

if not any_reg:
    print("\nNO REGRESSIONS - Safe to apply!")
    print("\nAccepted DIGIT_SPLIT changes:")
    for bidx in sorted(accepted.keys()):
        old = ORIGINAL_SPLITS[bidx]
        new = accepted[bidx]
        print(f"    {bidx}: ({old[0]}, '{old[1]}') -> ({new[0]}, '{new[1]}'),")
else:
    print("\nREGRESSIONS FOUND - do not apply!")
