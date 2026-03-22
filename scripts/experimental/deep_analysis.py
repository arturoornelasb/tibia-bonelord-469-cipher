"""
Tibia 469 - Deep Structural Analysis
======================================
Focus on:
1. Book overlap graph - proving they're fragments of one text
2. Reconstructing the original sequence
3. Testing variable-length encoding hypotheses
4. Frequency analysis compared to known ciphers
"""

import json
from collections import Counter, defaultdict

with open("books.json", "r") as f:
    books = json.load(f)

all_text = "".join(books)

print("=" * 70)
print("TIBIA 469 - DEEP STRUCTURAL ANALYSIS")
print("=" * 70)

# ============================================================
# 1. SUFFIX-PREFIX OVERLAP MATRIX
# ============================================================
print("\n" + "=" * 70)
print("1. BOOK OVERLAP ANALYSIS (suffix-prefix)")
print("=" * 70)

def find_overlap(a, b, min_len=10):
    """Find the longest suffix of a that is also a prefix of b."""
    max_overlap = min(len(a), len(b))
    best = 0
    for length in range(min_len, max_overlap + 1):
        if a.endswith(b[:length]):
            best = length
    return best

# Build overlap graph
print("\nComputing suffix-prefix overlaps (>= 10 digits)...")
overlaps = []
for i in range(len(books)):
    for j in range(len(books)):
        if i == j:
            continue
        ov = find_overlap(books[i], books[j], 10)
        if ov >= 10:
            overlaps.append((i+1, j+1, ov))

overlaps.sort(key=lambda x: -x[2])

print(f"\nFound {len(overlaps)} suffix-prefix overlaps >= 10 digits")
print("\nTop 40 overlaps:")
print(f"{'From':>5} {'To':>5} {'Overlap':>8}")
print("-" * 25)
for src, dst, ov in overlaps[:40]:
    print(f"  {src:3d} -> {dst:3d}  {ov:5d} digits")

# Books that don't connect to anything
all_srcs = set(x[0] for x in overlaps)
all_dsts = set(x[1] for x in overlaps)
connected = all_srcs | all_dsts
isolated = set(range(1, len(books)+1)) - connected
print(f"\nIsolated books (no overlap >= 10): {sorted(isolated) if isolated else 'None'}")

# Build adjacency: for each book, what's the best next/prev book?
print("\n--- Best chain connections ---")
best_next = {}
best_prev = {}
for src, dst, ov in overlaps:
    if src not in best_next or ov > best_next[src][1]:
        best_next[src] = (dst, ov)
    if dst not in best_prev or ov > best_prev[dst][1]:
        best_prev[dst] = (src, ov)

for book_num in sorted(best_next.keys()):
    next_book, ov = best_next[book_num]
    print(f"  Book {book_num:2d} -> Book {next_book:2d} (overlap {ov})")

# ============================================================
# 2. CHAIN RECONSTRUCTION
# ============================================================
print("\n" + "=" * 70)
print("2. CHAIN RECONSTRUCTION (greedy)")
print("=" * 70)

# Try to find chains of books using suffix-prefix overlaps
def build_chains():
    """Build chains using greedy best-overlap approach."""
    # Create overlap graph (best overlap for each pair)
    graph = defaultdict(list)
    for src, dst, ov in overlaps:
        graph[src].append((dst, ov))

    # Sort neighbors by overlap (descending)
    for src in graph:
        graph[src].sort(key=lambda x: -x[1])

    # Find chains
    used = set()
    chains = []

    # Start with books that have no predecessor (or weakest predecessor)
    start_candidates = set(range(1, len(books)+1))
    for _, dst, _ in overlaps:
        if dst in start_candidates and dst in best_prev:
            pass  # keep as candidate but prefer ones without prev

    # Actually find starting points: books that aren't a "best next" of another
    all_best_nexts = set(v[0] for v in best_next.values())
    potential_starts = set(range(1, len(books)+1)) - all_best_nexts

    for start in sorted(potential_starts):
        if start in used:
            continue
        chain = [start]
        used.add(start)
        current = start
        while current in best_next:
            next_book, ov = best_next[current]
            if next_book in used:
                break
            chain.append(next_book)
            used.add(next_book)
            current = next_book
        if len(chain) > 1:
            chains.append(chain)

    # Add isolated books
    for b in range(1, len(books)+1):
        if b not in used:
            chains.append([b])

    return chains

chains = build_chains()
print(f"\nFound {len(chains)} chains:")
for i, chain in enumerate(chains):
    total_digits = sum(len(books[b-1]) for b in chain)
    print(f"  Chain {i+1} ({len(chain)} books, ~{total_digits} digits): {' -> '.join(str(b) for b in chain)}")

# Merge the longest chain
if chains:
    longest_chain = max(chains, key=len)
    print(f"\n--- Merging longest chain ({len(longest_chain)} books) ---")

    merged = books[longest_chain[0] - 1]
    for i in range(1, len(longest_chain)):
        prev_book = longest_chain[i-1]
        curr_book = longest_chain[i]
        ov = find_overlap(books[prev_book-1], books[curr_book-1], 1)
        merged += books[curr_book-1][ov:]

    print(f"  Merged length: {len(merged)} digits")
    print(f"  First 200 chars: {merged[:200]}")
    print(f"  Last 200 chars: {merged[-200:]}")

# ============================================================
# 3. CONTAINMENT ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("3. CONTAINMENT (books inside other books)")
print("=" * 70)

contained_pairs = []
for i in range(len(books)):
    for j in range(len(books)):
        if i == j:
            continue
        if books[i] in books[j]:
            contained_pairs.append((i+1, j+1, len(books[i])))

if contained_pairs:
    print(f"\nFound {len(contained_pairs)} containment relationships:")
    for child, parent, size in sorted(contained_pairs, key=lambda x: -x[2]):
        print(f"  Book {child:2d} ({size} digits) is INSIDE Book {parent:2d} ({len(books[parent-1])} digits)")
else:
    print("\nNo book is fully contained within another.")

# ============================================================
# 4. VARIABLE-LENGTH ENCODING ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("4. VARIABLE-LENGTH ENCODING ANALYSIS")
print("=" * 70)

# What if the encoding uses variable-length numbers separated by
# certain delimiter digits?

# Check if certain digits could be delimiters
print("\n--- Could certain digits be delimiters/separators? ---")
for delimiter in "0123456789":
    segments = all_text.split(delimiter)
    non_empty = [s for s in segments if s]
    if non_empty:
        avg_len = sum(len(s) for s in non_empty) / len(non_empty)
        lengths = Counter(len(s) for s in non_empty)
        print(f"  Delimiter '{delimiter}': {len(non_empty)} segments, avg length {avg_len:.1f}")
        print(f"    Length distribution (top 5): {dict(lengths.most_common(5))}")

# ============================================================
# 5. REPEATING LONG SEQUENCES ACROSS ALL BOOKS
# ============================================================
print("\n" + "=" * 70)
print("5. LONGEST REPEATING SEQUENCES IN COMBINED TEXT")
print("=" * 70)

def find_repeated_substrings(text, min_len=15, max_len=60):
    """Find substrings that appear more than once."""
    results = {}
    for length in range(max_len, min_len - 1, -1):
        seen = {}
        for i in range(len(text) - length + 1):
            sub = text[i:i+length]
            if sub in seen:
                if sub not in results:
                    # Check it's not a substring of an already-found longer repeat
                    is_sub = False
                    for existing in results:
                        if sub in existing:
                            is_sub = True
                            break
                    if not is_sub:
                        results[sub] = []
                if i not in [p for p in results.get(sub, [])]:
                    results[sub] = results.get(sub, []) + [i]
            seen[sub] = i

    # Filter to actually repeated ones and add first occurrence
    final = {}
    for sub, positions in results.items():
        # Re-find all positions
        all_pos = []
        start = 0
        while True:
            idx = all_text.find(sub, start)
            if idx == -1:
                break
            all_pos.append(idx)
            start = idx + 1
        if len(all_pos) >= 2:
            final[sub] = all_pos

    return final

print("\nSearching for repeated sequences (15-60 digits)...")
repeated = find_repeated_substrings(all_text, 15, 60)

# Sort by length descending
sorted_repeated = sorted(repeated.items(), key=lambda x: -len(x[0]))

print(f"\nFound {len(sorted_repeated)} repeated sequences")
print("\nTop 30 longest repeated sequences:")
for seq, positions in sorted_repeated[:30]:
    print(f"  Length {len(seq):2d}, appears {len(positions)}x: '{seq[:50]}{'...' if len(seq) > 50 else ''}'")

# ============================================================
# 6. BOOK LENGTH VS DIGIT DISTRIBUTION
# ============================================================
print("\n" + "=" * 70)
print("6. PER-BOOK DIGIT DISTRIBUTIONS")
print("=" * 70)

print(f"\n{'Book':>4} {'Len':>4} {'Avg':>7} | 0    1    2    3    4    5    6    7    8    9")
print("-" * 80)
for i, book in enumerate(books):
    avg = sum(int(d) for d in book) / len(book)
    dist = Counter(book)
    row = f"  {i+1:2d}  {len(book):3d}  {avg:.3f} |"
    for d in "0123456789":
        pct = dist.get(d, 0) / len(book) * 100
        row += f" {pct:4.1f}"
    print(row)

# ============================================================
# 7. NPC DIALOGUE ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("7. NPC DIALOGUE CROSS-REFERENCE")
print("=" * 70)

npc_texts = {
    "Wrinkled Bonelord greeting 1": "485611800364197",
    "Wrinkled Bonelord greeting 2": "78572611857643646724",
    "Elder Bonelord 1": "659978 54764",
    "Elder Bonelord 2": "653768764",
    "Evil Eye": "653768764",
    "Knightmare": "3478 67 090871 097664 3466 00 0345",
    "Chayenne": "114514519485611451908304576512282177",
    "Poll 2020 answer C": "663 902073 7223 67538 467 80097",
    "Secret Library": "74032 45331",
}

print("\nSearching for NPC dialogue fragments in books...\n")
for npc_name, dialogue in npc_texts.items():
    # Remove spaces for searching
    clean = dialogue.replace(" ", "")
    print(f"{npc_name}: '{dialogue}'")

    # Search in books
    found = False
    for i, book in enumerate(books):
        pos = book.find(clean)
        if pos != -1:
            print(f"  FOUND in Book {i+1} at position {pos}!")
            found = True

    # Search for fragments
    if not found:
        # Try substrings of length 8+
        frags_found = []
        for frag_len in range(min(len(clean), 15), 7, -1):
            for start in range(len(clean) - frag_len + 1):
                frag = clean[start:start+frag_len]
                for bi, book in enumerate(books):
                    if frag in book:
                        frags_found.append((frag_len, frag, bi+1))
                        break
            if frags_found:
                break
        if frags_found:
            best = max(frags_found, key=lambda x: x[0])
            print(f"  Longest fragment match: '{best[1]}' ({best[0]} digits) in Book {best[2]}")
        else:
            print(f"  No match found")
    print()

# ============================================================
# 8. MATHEMATICAL PROPERTIES
# ============================================================
print("\n" + "=" * 70)
print("8. MATHEMATICAL PROPERTIES")
print("=" * 70)

# Test: do books encode coordinates? (Tibia map is ~2048x2048)
print("\n--- Testing coordinate encoding hypothesis ---")
# If pairs of 3-5 digit numbers are coordinates (xxxxx,yyyyy)
# Tibia coordinates range roughly: x=30000-35000, y=30000-35000, z=0-15
for i, book in enumerate(books[:5]):
    print(f"\nBook {i+1} as 5-digit groups:")
    groups = [book[j:j+5] for j in range(0, len(book)-4, 5)]
    coords = [(int(groups[k]), int(groups[k+1])) for k in range(0, len(groups)-1, 2)]
    tibia_range = [(x,y) for x,y in coords if 30000 <= x <= 35000 and 30000 <= y <= 35000]
    print(f"  Groups: {groups[:10]}...")
    print(f"  As coordinate pairs: {coords[:5]}...")
    print(f"  In Tibia map range: {len(tibia_range)} / {len(coords)} pairs")

# Test: digit sum properties
print("\n--- Digit sum cascade ---")
for i, book in enumerate(books[:10]):
    s = sum(int(d) for d in book)
    s2 = sum(int(d) for d in str(s))
    s3 = sum(int(d) for d in str(s2))
    print(f"  Book {i+1}: sum={s}, digital root cascade: {s} -> {s2} -> {s3}")

# Digital root
print("\n--- Digital roots ---")
roots = []
for i, book in enumerate(books):
    s = sum(int(d) for d in book)
    root = s % 9 if s % 9 != 0 else 9
    roots.append(root)
print(f"  Digital roots: {roots}")
print(f"  Distribution: {dict(Counter(roots))}")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
