"""
Analyze decoded text from crib-constrained mapping.
Look for almost-words, consistent patterns, and potential fixes.
"""
import json
from collections import Counter

with open('books.json', 'r') as f:
    books = json.load(f)

with open('best_mapping.json', 'r') as f:
    mapping = json.load(f)

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

# Per-book alignment
book_offsets = []
for book in books:
    if len(book) < 10:
        book_offsets.append(0)
        continue
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    ic0 = ic_from_counts(Counter(bp0), len(bp0))
    ic1 = ic_from_counts(Counter(bp1), len(bp1))
    book_offsets.append(0 if ic0 > ic1 else 1)

book_pairs = []
for i, book in enumerate(books):
    off = book_offsets[i]
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# Decode all books
print("=" * 70)
print("ALL BOOKS DECODED")
print("=" * 70)

all_decoded = []
for i, bp in enumerate(book_pairs):
    decoded = ''.join(mapping.get(p, '?') for p in bp)
    all_decoded.append(decoded)
    print(f"\nBook {i:2d} (off={book_offsets[i]}, {len(decoded)} letters, raw {len(books[i])} digits):")
    for j in range(0, len(decoded), 80):
        print(f"  {decoded[j:j+80]}")

# Now look for recurring decoded substrings across books
print("\n" + "=" * 70)
print("RECURRING DECODED SUBSTRINGS (length >= 5)")
print("=" * 70)

all_text = '|'.join(all_decoded)

# Find common substrings of length 5-15
for slen in [15, 12, 10, 8, 6, 5]:
    substr_count = Counter()
    for d in all_decoded:
        seen = set()
        for j in range(len(d) - slen + 1):
            s = d[j:j+slen]
            if s not in seen:
                substr_count[s] += 1
                seen.add(s)

    common = [(s, c) for s, c in substr_count.items() if c >= 2]
    common.sort(key=lambda x: (-x[1], -len(x[0])))

    if common:
        print(f"\nLength {slen} substrings appearing >= 2 books:")
        for s, c in common[:15]:
            print(f"  '{s}' in {c} books")


print("\n" + "=" * 70)
print("LOOK FOR KNOWN GERMAN WORDS IN CONTEXT")
print("=" * 70)

# Concatenate decoded text
full = ''.join(all_decoded)

# Find STEIN contexts
for word in ['STEIN', 'ENDE', 'NICHT', 'EINE', 'NACH', 'AUCH']:
    print(f"\n  Contexts of '{word}':")
    start = 0
    while True:
        pos = full.find(word, start)
        if pos == -1:
            break
        ctx_start = max(0, pos - 10)
        ctx_end = min(len(full), pos + len(word) + 10)
        before = full[ctx_start:pos]
        after = full[pos+len(word):ctx_end]
        print(f"    ...{before}[{word}]{after}...")
        start = pos + 1
        if start - pos > 300:  # limit
            break


print("\n" + "=" * 70)
print("PAIR CODE ANALYSIS - WHICH CODES ARE MOST AMBIGUOUS?")
print("=" * 70)

# Build reverse mapping
reverse_map = {}
for code, letter in mapping.items():
    if letter not in reverse_map:
        reverse_map[letter] = []
    reverse_map[letter].append(code)

all_pairs_flat = []
for bp in book_pairs:
    all_pairs_flat.extend(bp)
pair_counts = Counter(all_pairs_flat)

# For each letter, show the codes and their frequencies
print("\nLetter -> Codes (with frequencies):")
for letter in sorted(reverse_map.keys(), key=lambda l: -len(reverse_map[l])):
    codes = sorted(reverse_map[letter])
    freqs = [(c, pair_counts.get(c, 0)) for c in codes]
    total = sum(f for _, f in freqs)
    print(f"  {letter} (total {total}): {freqs}")


print("\n" + "=" * 70)
print("WHAT IF WE TRY READING WITH SPACING HEURISTIC?")
print("=" * 70)

# German word boundary detection: try to insert spaces
# Use common German word starters/enders
# Very simple: split on common patterns

# Instead, try to find the longest German words
long_german_words = [
    'RUNENSTEIN', 'RUNENSTEINEN', 'STEINEN', 'STEINE', 'STEIN',
    'BONELORD', 'BONELORDS',
    'NICHT', 'EINER', 'EINEN', 'DIESE', 'DIESER',
    'WERDEN', 'WURDE', 'HATTE',
    'FEUER', 'WASSER', 'ERDE', 'LICHT', 'LEBEN',
    'GEIST', 'SEELE', 'KRAFT', 'MACHT',
    'SCHRIFT', 'ZEICHEN', 'SPRACHE',
    'DUNKEL', 'DUNKELHEIT',
    'AUGE', 'AUGEN',
    'RUNE', 'RUNEN',
    'ENDE', 'ANFANG',
    'DURCH', 'GEGEN', 'UNTER', 'UEBER',
]

for word in sorted(long_german_words, key=lambda w: -len(w)):
    count = full.count(word)
    if count > 0:
        print(f"  '{word}': {count} times")


print("\n" + "=" * 70)
print("BOOK OVERLAPS IN DECODED TEXT")
print("=" * 70)

# Check if decoded books have consistent overlapping text
for i in range(len(all_decoded)):
    for j in range(i+1, len(all_decoded)):
        di = all_decoded[i]
        dj = all_decoded[j]
        # Check suffix of i = prefix of j
        for k in range(min(30, len(di), len(dj)), 3, -1):
            if di[-k:] == dj[:k]:
                print(f"  Book {i} suffix -> Book {j} prefix: '{di[-k:]}' ({k} chars)")
                break
            if dj[-k:] == di[:k]:
                print(f"  Book {j} suffix -> Book {i} prefix: '{dj[-k:]}' ({k} chars)")
                break


print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
