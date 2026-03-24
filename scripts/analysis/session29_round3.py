#!/usr/bin/env python3
"""Session 29 Round 3: Context-aware replacement for ND, DE, UNR.
These can't be fixed with simple ANAGRAM_MAP because the short strings
appear inside other words. Try a post-DP garbled-block-specific approach.
"""
import json, os, re
from collections import Counter, defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json')) as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json')) as f:
    books = json.load(f)

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

book_pairs_list = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        sp, d = DIGIT_SPLITS[bidx]
        book = book[:sp] + d + book[sp:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs_list.append(pairs)

# Load full pipeline (import-style copy from narrative_v3_clean.py)
exec(open(os.path.join(script_dir, '..', 'core', 'narrative_v3_clean.py')).read().split('# ============================================================')[0]
     .replace("print(", "#print("))

# Actually, let's just rebuild what we need
decoded_books_raw = [''.join(v7.get(p, '?') for p in bpairs) for bpairs in book_pairs_list]

# Read KNOWN and ANAGRAM_MAP from narrative_v3_clean.py by parsing
import importlib.util
spec = importlib.util.spec_from_file_location("narrative", os.path.join(script_dir, '..', 'core', 'narrative_v3_clean.py'))

# Actually, let's just hardcode what we need - read the source and extract
src = open(os.path.join(script_dir, '..', 'core', 'narrative_v3_clean.py')).read()

# Find KNOWN and ANAGRAM_MAP by exec-ing just those parts
# For safety, extract just the data declarations
known_start = src.index("KNOWN = set([")
known_end = src.index("])", known_start) + 2
anagram_start = src.index("ANAGRAM_MAP = {")
anagram_end = src.index("\n}", anagram_start) + 2

exec(src[known_start:known_end])
exec(src[anagram_start:anagram_end])

all_text = ''.join(decoded_books_raw)

# Apply anagrams
resolved_text = all_text
for a in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved_text = resolved_text.replace(a, ANAGRAM_MAP[a])

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

def dp_segment_full(text, known_set):
    n = len(text)
    dp_arr = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp_arr[i] = (dp_arr[i-1][0], None)
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if cand in known_set:
                score = dp_arr[start][0] + wlen
                if score > dp_arr[i][0]:
                    dp_arr[i] = (score, (start, cand))
    tokens = []
    i = n
    while i > 0:
        if dp_arr[i][1] is not None:
            start, word = dp_arr[i][1]
            tokens.append(('W', word, start, i))
            i = start
        else:
            tokens.append(('G', text[i-1], i-1, i))
            i -= 1
    tokens.reverse()
    result = []
    for kind, val, s, e in tokens:
        if kind == 'G' and result and result[-1][0] == 'G':
            prev = result[-1]
            result[-1] = ('G', prev[1] + val, prev[2], e)
        else:
            result.append((kind, val, s, e))
    return result

total = sum(1 for c in resolved_text if c != '?')
base_cov = dp_score(resolved_text, KNOWN)
print(f"BASELINE: {base_cov}/{total} = {base_cov/total*100:.1f}%")

tokens = dp_segment_full(resolved_text, KNOWN)

# ============================================================
# ANALYSIS: What exactly remains garbled?
# ============================================================
print("\n" + "="*70)
print("COMPLETE GARBLED BLOCK INVENTORY")
print("="*70)

garbled_total = 0
garbled_inventory = []
for i, (kind, val, s, e) in enumerate(tokens):
    if kind != 'G': continue
    garbled_total += len(val)
    prev = tokens[i-1][1] if i > 0 and tokens[i-1][0] == 'W' else '^'
    nxt = tokens[i+1][1] if i < len(tokens)-1 and tokens[i+1][0] == 'W' else '$'
    garbled_inventory.append((val, len(val), prev, nxt))

# Group by block text
block_counts = Counter()
for val, length, prev, nxt in garbled_inventory:
    block_counts[val] += 1

print(f"Total garbled chars: {garbled_total}")
print(f"Unique blocks: {len(block_counts)}")
print(f"Total block instances: {len(garbled_inventory)}")

# Categorize
single_chars = sum(c for v,c in block_counts.items() if len(v) == 1)
two_chars = sum(c for v,c in block_counts.items() if len(v) == 2)
three_plus = sum(c for v,c in block_counts.items() if len(v) >= 3)
print(f"\nBy length:")
print(f"  1-char blocks: {single_chars} instances ({sum(c for v,c in block_counts.items() if len(v)==1)} chars)")
print(f"  2-char blocks: {two_chars} instances ({sum(len(v)*c for v,c in block_counts.items() if len(v)==2)} chars)")
print(f"  3+ char blocks: {three_plus} instances ({sum(len(v)*c for v,c in block_counts.items() if len(v)>=3)} chars)")

# Show all remaining blocks
print("\nAll remaining garbled (sorted by total char impact):")
scored = [(len(v)*c, v, c) for v,c in block_counts.items()]
scored.sort(key=lambda x: -x[0])
for impact, block, count in scored:
    contexts = []
    for val, length, prev, nxt in garbled_inventory:
        if val == block and len(contexts) < 2:
            contexts.append(f"{prev} |{block}| {nxt}")
    print(f"  {impact:3d} chars: {block!r:15s} ({count}x)  {contexts[0]}")

# ============================================================
# DIGIT_SPLIT RE-OPTIMIZATION
# ============================================================
print("\n" + "="*70)
print("DIGIT_SPLIT RE-OPTIMIZATION CHECK")
print("="*70)
print("Checking if any DIGIT_SPLIT changes improve coverage...")

# For each book with a DIGIT_SPLIT, try all 10 digits and all positions
improvements = []
for bidx in sorted(DIGIT_SPLITS.keys()):
    book = books[bidx]
    current_sp, current_d = DIGIT_SPLITS[bidx]

    # Current coverage for this book
    test_book = book[:current_sp] + current_d + book[current_sp:]
    off = get_offset(test_book)
    pairs = [test_book[j:j+2] for j in range(off, len(test_book)-1, 2)]
    book_text = ''.join(v7.get(p, '?') for p in pairs)
    for a in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
        book_text = book_text.replace(a, ANAGRAM_MAP[a])
    book_total = sum(1 for c in book_text if c != '?')
    if book_total == 0: continue
    current_cov = dp_score(book_text, KNOWN)

    best_cov = current_cov
    best_sp = current_sp
    best_d = current_d

    for d in '0123456789':
        for sp in range(len(book) + 1):
            test_book2 = book[:sp] + d + book[sp:]
            off2 = get_offset(test_book2)
            pairs2 = [test_book2[j:j+2] for j in range(off2, len(test_book2)-1, 2)]
            bt2 = ''.join(v7.get(p, '?') for p in pairs2)
            for a in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
                bt2 = bt2.replace(a, ANAGRAM_MAP[a])
            bt2_total = sum(1 for c in bt2 if c != '?')
            if bt2_total == 0: continue
            cov2 = dp_score(bt2, KNOWN)
            if cov2 > best_cov:
                best_cov = cov2
                best_sp = sp
                best_d = d

    if best_cov > current_cov:
        delta = best_cov - current_cov
        improvements.append((delta, bidx, current_sp, current_d, best_sp, best_d, current_cov, best_cov))
        print(f"  Book {bidx}: +{delta} chars if DIGIT_SPLIT ({current_sp},'{current_d}') -> ({best_sp},'{best_d}')")

if not improvements:
    print("  No improvements found - current DIGIT_SPLITS are optimal at 91.2%")
else:
    total_gain = sum(d for d,_,_,_,_,_,_,_ in improvements)
    print(f"\n  Total potential gain: +{total_gain} chars")

# ============================================================
# UNMAPPED CODE CHECK
# ============================================================
print("\n" + "="*70)
print("UNMAPPED CODE ANALYSIS")
print("="*70)

# Check which 2-digit codes are NOT in mapping
all_codes = set(f"{i:02d}" for i in range(100))
mapped_codes = set(v7.keys())
unmapped = all_codes - mapped_codes
print(f"Mapped codes: {len(mapped_codes)}/100")
print(f"Unmapped codes: {sorted(unmapped)}")

# Check how many times unmapped codes appear in books
unmapped_count = 0
for book in books:
    for i in range(0, len(book)-1, 2):
        pair = book[i:i+2]
        if pair in unmapped:
            unmapped_count += 1
print(f"Unmapped code occurrences in raw books: {unmapped_count}")

# Check what letter each unmapped code might be
# by looking at context in decoded text
for code in sorted(unmapped):
    occurrences = 0
    for book in books:
        for i in range(0, len(book)-1, 2):
            if book[i:i+2] == code:
                occurrences += 1
    if occurrences > 0:
        print(f"  Code {code}: {occurrences} occurrences")
