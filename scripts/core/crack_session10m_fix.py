#!/usr/bin/env python3
"""Session 10m fix: DP segmentation with corrected algorithm"""

import json, re
from collections import defaultdict

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]
books = [parse_codes(b) for b in raw_books]
def decode(book):
    return ''.join(mapping.get(c, '?') for c in book)
def collapse(s):
    return re.sub(r'(.)\\1+', r'\\1', s)

all_col = [(i, collapse(decode(b))) for i, b in enumerate(books)]

print("=" * 80)
print("SESSION 10m FIX: CORRECTED DP SEGMENTATION")
print("=" * 80)

# Word list with scores
word_scores = {}
definite = [
    'AUNRSONGETRASES', 'UNENITGHNE', 'EILCHANHEARUCHTIG',
    'EDETOTNIURGS', 'DNRHAUNRNVMHISDIZA',
    'EUGENDRTHENAEDEULGHLWUOEHSG', 'WRLGTNELNRHELUIRUNN',
    'TIUMENGEMI', 'SCHWITEIONE',
    'LABGZERAS', 'HEDEMI', 'TAUTR', 'LABRNI', 'ADTHARSC',
    'ADTHAUMR', 'ODEGAREN', 'RLAUNR',
    'KOENIG', 'UTRUNR', 'GEIGET', 'KELSEI', 'SCHAUN',
    'URALTE', 'FINDEN', 'SEIDE', 'DIESER', 'GEVMT',
    'NORDEN', 'SONNE', 'UNTER', 'NICHT', 'WERDE',
    'STEIN', 'DENEN', 'ERDE', 'VIEL', 'RUNE',
    'STEH', 'LIED', 'SEGEN', 'DORT', 'DENN',
    'GOLD', 'MOND', 'WELT', 'ENDE', 'REDE',
    'HUND', 'SEIN', 'WIRD', 'KLAR', 'ERST',
    'HWND', 'VMTEGE',
    'EINEN', 'EINER', 'SEINE',
    'TAG', 'WEG', 'DER', 'DEN', 'DIE', 'DAS',
    'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON',
    'MIT', 'WIE', 'SEI', 'AUS', 'ORT', 'TUN',
    'NUR', 'SUN', 'TOT', 'GAR', 'ACH', 'ZUM',
    'HIN', 'HER', 'ALS', 'AUCH', 'RUND',
    'ER', 'ES', 'IN', 'SO',
]

for w in definite:
    word_scores[w] = len(w) * 3

all_words = sorted(word_scores.keys(), key=len, reverse=True)

NEG_INF = float('-inf')

def dp_segment(text, words, scores):
    """Find segmentation maximizing recognized word coverage."""
    n = len(text)
    # dp[i] = best score for text[0:i], None = unreachable
    dp = [NEG_INF] * (n + 1)
    back = [None] * (n + 1)
    dp[0] = 0

    for i in range(n):
        if dp[i] == NEG_INF:
            continue
        # Option 1: skip one char as unknown (penalty = -1)
        new_score = dp[i] - 1
        if new_score > dp[i+1]:
            dp[i+1] = new_score
            back[i+1] = ('unk', i)

        # Option 2: match a known word
        for word in words:
            wlen = len(word)
            if i + wlen <= n and text[i:i+wlen] == word:
                new_score = dp[i] + scores.get(word, wlen)
                if new_score > dp[i+wlen]:
                    dp[i+wlen] = new_score
                    back[i+wlen] = ('word', i, word)

    # Backtrack
    result = []
    pos = n
    while pos > 0:
        info = back[pos]
        if info is None:
            result.append(('unk', text[pos-1:pos]))
            pos -= 1
        elif info[0] == 'unk':
            # Collect consecutive unknowns
            end = pos
            while pos > 0 and back[pos] and back[pos][0] == 'unk':
                pos = back[pos][1]
            result.append(('unk', text[pos:end]))
        elif info[0] == 'word':
            result.append(('word', info[2]))
            pos = info[1]

    result.reverse()
    return result, dp[n]

# Get maximal (non-substring) pieces
pieces = {}
for i, text in all_col:
    is_sub = False
    for j, other in all_col:
        if i != j and text in other:
            is_sub = True
            break
    if not is_sub:
        pieces[i] = text

by_len = sorted(pieces.items(), key=lambda x: len(x[1]), reverse=True)

# Segment top 5
for idx, (bi, text) in enumerate(by_len[:5]):
    result, score = dp_segment(text, all_words, word_scores)

    # Format
    parts = []
    for typ, val in result:
        if typ == 'word':
            parts.append(val)
        else:
            parts.append(f'[{val}]')

    word_chars = sum(len(val) for typ, val in result if typ == 'word')
    pct = word_chars * 100 / len(text) if text else 0

    print(f"\n  --- Book {bi} ({len(text)} chars, coverage={pct:.0f}%) ---")
    line = ' '.join(parts)
    for i in range(0, len(line), 78):
        print(f"    {line[i:i+78]}")

# Overall stats
print("\n" + "=" * 60)
print("OVERALL COVERAGE STATISTICS")
print("=" * 60)

total_chars = 0
total_covered = 0
for bi, text in all_col:
    result, score = dp_segment(text, all_words, word_scores)
    word_chars = sum(len(val) for typ, val in result if typ == 'word')
    total_chars += len(text)
    total_covered += word_chars

print(f"  Total collapsed chars: {total_chars}")
print(f"  Covered by words: {total_covered}")
print(f"  Overall coverage: {total_covered*100/total_chars:.1f}%")

# Most common unknown segments
print("\n  Most common unknown segments:")
unk_counter = Counter()
for bi, text in all_col:
    result, _ = dp_segment(text, all_words, word_scores)
    for typ, val in result:
        if typ == 'unk' and len(val) > 1:
            unk_counter[val] += 1

from collections import Counter
for unk, count in unk_counter.most_common(25):
    print(f"    [{unk:20s}] ({count:2d}x)")

print("\n" + "=" * 80)
print("SESSION 10m FIX COMPLETE")
print("=" * 80)
