#!/usr/bin/env python3
"""Debug: find all UNR in resolved text to understand post-ANAGRAM_MAP context."""
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

all_text = ''.join(decoded_books)
resolved_text = all_text
for anagram in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved_text = resolved_text.replace(anagram, ANAGRAM_MAP[anagram])

print(f"TREUUNR count: {resolved_text.count('TREUUNR')}")
print(f"Total UNR count: {resolved_text.count('UNR')}")

# Find all UNR with context
for i in range(len(resolved_text)-2):
    if resolved_text[i:i+3] == 'UNR':
        ctx = resolved_text[max(0,i-12):min(len(resolved_text),i+15)]
        in_windunruh = 'WINDUNRUH' in resolved_text[max(0,i-5):i+8]
        marker = " [WINDUNRUH]" if in_windunruh else ""
        print(f"  pos {i:4d}: ...{ctx}...{marker}")
