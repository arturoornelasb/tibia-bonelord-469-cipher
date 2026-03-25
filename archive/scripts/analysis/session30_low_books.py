#!/usr/bin/env python3
"""Session 30: Attack lowest-coverage books."""
import json, os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json')) as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json')) as f:
    books = json.load(f)

src = open(os.path.join(script_dir, '..', 'core', 'narrative_v3_clean.py')).read()
code_end = src.index("\n# ============================================================\n# RECONSTRUCT")
exec(src[:code_end])

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

# Per-book coverage
book_stats = []
for bidx, text in enumerate(decoded_books):
    rt = text
    for a in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
        rt = rt.replace(a, ANAGRAM_MAP[a])
    rt = rt.replace('TREUUNR', 'TREUNUR')
    total = sum(1 for c in rt if c != '?')
    if total == 0:
        continue
    cov = dp_score(rt, KNOWN)
    pct = cov / total * 100
    tokens_b, _ = dp_segment(rt)
    garbled = [t[1:-1] for t in tokens_b if t.startswith('{')]
    book_stats.append((pct, bidx, cov, total, rt, garbled))

book_stats.sort()

print("=" * 70)
print("LOW-COVERAGE BOOKS (bottom 15)")
print("=" * 70)
for pct, bidx, cov, total, rt, garbled in book_stats[:15]:
    tokens_b, _ = dp_segment(rt)
    seg = ' '.join(tokens_b)
    print(f"\n  Book {bidx:2d}: {cov}/{total} = {pct:.0f}%  (len={total})")
    print(f"    {seg}")
    if garbled:
        print(f"    Garbled: {garbled}")

# Find garbled blocks unique to low-coverage books
print("\n" + "=" * 70)
print("GARBLED BLOCKS UNIQUE TO BOTTOM 10 BOOKS")
print("=" * 70)

# Collect garbled from all books
all_garbled = {}
for pct, bidx, cov, total, rt, garbled in book_stats:
    for g in garbled:
        if g not in all_garbled:
            all_garbled[g] = []
        all_garbled[g].append(bidx)

# Show garbled blocks that only appear in bottom 10
bottom_10_ids = set(bidx for _, bidx, _, _, _, _ in book_stats[:10])
for g, book_ids in sorted(all_garbled.items(), key=lambda x: -len(x[0])):
    if len(g) >= 3 and all(b in bottom_10_ids for b in book_ids):
        print(f"  {g!r:15s} (len={len(g)}, books={book_ids})")
