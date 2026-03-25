#!/usr/bin/env python3
"""Session 30: Quick remaining garbled inventory after all fixes."""
import json, os, re
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

all_text = ''.join(decoded_books)
resolved_text = all_text
for anagram in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved_text = resolved_text.replace(anagram, ANAGRAM_MAP[anagram])
resolved_text = resolved_text.replace('TREUUNR', 'TREUNUR')

tokens, covered = dp_segment(resolved_text)
total_known = sum(1 for c in resolved_text if c != '?')
print(f"Coverage: {covered}/{total_known} = {covered/total_known*100:.1f}%")

garbled = []
for i, tok in enumerate(tokens):
    if tok.startswith('{'):
        block = tok[1:-1]
        prev = tokens[i-1] if i > 0 else '^'
        nxt = tokens[i+1] if i < len(tokens)-1 else '$'
        garbled.append((block, prev, nxt, i))

block_counts = Counter(b for b, _, _, _ in garbled)
total_garbled = sum(len(v)*c for v, c in block_counts.items())
print(f"Garbled: {total_garbled} chars in {len(garbled)} blocks ({len(block_counts)} unique)")

# Show by impact
scored = [(len(v)*c, v, c) for v, c in block_counts.items()]
scored.sort(key=lambda x: -x[0])

print(f"\nTop 30 garbled blocks:")
for impact, block, count in scored[:30]:
    contexts = [(p, n) for b, p, n, _ in garbled if b == block]
    ctx = f"{contexts[0][0]}|{block}|{contexts[0][1]}"
    print(f"  {impact:3d} chars: {block!r:15s} ({count}x)  {ctx}")

# Check what percentage is single-char vs multi-char
single = sum(c for v,c in block_counts.items() if len(v)==1)
multi = sum(len(v)*c for v,c in block_counts.items() if len(v)>=2)
print(f"\nSingle-char residues: {single} chars ({single/total_garbled*100:.0f}%)")
print(f"Multi-char blocks: {multi} chars ({multi/total_garbled*100:.0f}%)")

# What would coverage be if we added all single-letters to KNOWN?
print(f"\nIf we reduce min word length to 1 (hypothetical):")
KNOWN_EXT = set(KNOWN)
for c in 'ABCDEFGHIKLMNORSTUWZ':
    KNOWN_EXT.add(c)
_, cov_ext = dp_segment.__wrapped__(resolved_text) if hasattr(dp_segment, '__wrapped__') else (None, None)

# Manual DP with min_wlen=1
n = len(resolved_text)
dp = [0] * (n + 1)
for i in range(1, n + 1):
    dp[i] = dp[i-1]
    for wlen in range(1, min(i, 20) + 1):  # wlen=1 allowed
        s = i - wlen
        cand = resolved_text[s:i]
        if wlen == 1 and cand.isalpha():
            dp[i] = max(dp[i], dp[s] + 1)
        elif wlen >= 2 and cand in KNOWN:
            dp[i] = max(dp[i], dp[s] + wlen)
print(f"  With min_wlen=1: {dp[n]}/{total_known} = {dp[n]/total_known*100:.1f}%")
print(f"  Ceiling (non-? chars): {total_known}/{total_known} = 100%")
print(f"  '?' chars: {sum(1 for c in resolved_text if c == '?')}")
