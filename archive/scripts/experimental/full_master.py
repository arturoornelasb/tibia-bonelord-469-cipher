"""
Full master text reconstruction using graph-based approach.
Key insight: IC-based offset detection is INVERTED.
Use lower-IC offset for each book.
"""

import json
from collections import Counter, defaultdict

with open('books.json', 'r') as f:
    books = json.load(f)

print("=" * 70)
print("1. BUILD OVERLAP GRAPH")
print("=" * 70)

n = len(books)

# Find all pairwise overlaps
# For each pair of books, find the maximum overlap
edges = []  # (book_i, book_j, overlap_length, type)

for i in range(n):
    for j in range(n):
        if i == j:
            continue
        bi, bj = books[i], books[j]

        # Check if bi's suffix = bj's prefix (bi comes before bj)
        max_k = min(len(bi), len(bj))
        for k in range(max_k, 4, -1):
            if bi[-k:] == bj[:k]:
                edges.append((i, j, k, 'chain'))
                break

# Also check containment
for i in range(n):
    for j in range(n):
        if i == j:
            continue
        if len(books[i]) <= len(books[j]):
            pos = books[j].find(books[i])
            if pos >= 0:
                edges.append((i, j, len(books[i]), 'contained', pos))

print(f"Found {len(edges)} directed edges")
chain_edges = [e for e in edges if e[3] == 'chain']
contain_edges = [e for e in edges if e[3] == 'contained']
print(f"  Chain edges (suffix-prefix): {len(chain_edges)}")
print(f"  Containment edges: {len(contain_edges)}")

# Show strongest chain edges
chain_edges.sort(key=lambda e: -e[2])
print(f"\nTop 20 chain overlaps:")
for i, j, k, t in chain_edges[:20]:
    print(f"  Book {i} -> Book {j}: {k} digit overlap")


print("\n" + "=" * 70)
print("2. GREEDY RECONSTRUCTION (multiple passes)")
print("=" * 70)

# Build adjacency: for each book, find best successor (longest suffix-prefix overlap)
best_successor = {}
best_predecessor = {}
for i, j, k, t in chain_edges:
    if i not in best_successor or k > best_successor[i][1]:
        best_successor[i] = (j, k)
    if j not in best_predecessor or k > best_predecessor[j][1]:
        best_predecessor[j] = (i, k)

# Follow chains to build sequences
used_in_chain = set()
chains = []

# Start from books that have no strong predecessor
starting_books = sorted(range(n), key=lambda i: -len(books[i]))

for start in starting_books:
    if start in used_in_chain:
        continue

    chain = [start]
    used_in_chain.add(start)

    # Extend forward
    current = start
    while current in best_successor:
        next_book, overlap = best_successor[current]
        if next_book in used_in_chain:
            break
        chain.append(next_book)
        used_in_chain.add(next_book)
        current = next_book

    # Extend backward
    current = start
    while current in best_predecessor:
        prev_book, overlap = best_predecessor[current]
        if prev_book in used_in_chain:
            break
        chain.insert(0, prev_book)
        used_in_chain.add(prev_book)
        current = prev_book

    if len(chain) > 1:
        chains.append(chain)

print(f"Found {len(chains)} chains:")
for ci, chain in enumerate(chains):
    # Build the master text for this chain
    master = books[chain[0]]
    for k in range(1, len(chain)):
        prev, curr = chain[k-1], chain[k]
        overlap = best_successor[prev][1]
        master = master + books[curr][overlap:]

    print(f"  Chain {ci}: {len(chain)} books, master length = {len(master)} digits")
    print(f"    Books: {chain[:15]}{'...' if len(chain) > 15 else ''}")

# Unused books
unused = set(range(n)) - used_in_chain
print(f"\nUnused books: {len(unused)}")
for i in sorted(unused):
    print(f"  Book {i}: {len(books[i])} digits")


print("\n" + "=" * 70)
print("3. FULL MASTER FROM LONGEST CHAIN")
print("=" * 70)

if chains:
    # Use the longest chain
    main_chain = max(chains, key=len)
    master = books[main_chain[0]]
    for k in range(1, len(main_chain)):
        prev, curr = main_chain[k-1], main_chain[k]
        overlap = best_successor[prev][1]
        master = master + books[curr][overlap:]

    print(f"Main chain: {len(main_chain)} books")
    print(f"Master text: {len(master)} digits")

    # Check how many of ALL books are contained
    all_contained = 0
    positions = {}
    for i in range(n):
        pos = master.find(books[i])
        if pos >= 0:
            all_contained += 1
            positions[i] = pos

    print(f"Books contained in master: {all_contained}/{n}")

    # Check if master is circular
    for k in range(min(200, len(master)//2), 4, -1):
        if master[-k:] == master[:k]:
            print(f"\nCIRCULAR overlap: {k} digits")
            # Trim the circular part
            master_trimmed = master[:-k]
            print(f"Trimmed master: {len(master_trimmed)} digits")
            break

    print(f"\nFirst 200 digits: {master[:200]}")
    print(f"Last 200 digits:  {master[-200:]}")


print("\n" + "=" * 70)
print("4. IC OFFSET ANALYSIS - INVERTED HYPOTHESIS")
print("=" * 70)

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

# Test: use LOWER IC offset for each book (inverting the usual choice)
for strategy_name, pick_higher_ic in [("Higher IC (standard)", True), ("Lower IC (inverted)", False)]:
    all_pairs = []
    for i, book in enumerate(books):
        bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
        bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
        ic0 = ic_from_counts(Counter(bp0), len(bp0))
        ic1 = ic_from_counts(Counter(bp1), len(bp1))

        if pick_higher_ic:
            off = 0 if ic0 > ic1 else 1
        else:
            off = 0 if ic0 < ic1 else 1

        pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
        all_pairs.extend(pairs)

    pc = Counter(all_pairs)
    ic = ic_from_counts(pc, len(all_pairs))
    print(f"\n{strategy_name}: IC = {ic*100:.4f}, unique pairs = {len(pc)}")


print("\n" + "=" * 70)
print("5. MASTER-POSITION BASED OFFSET")
print("=" * 70)

if chains and positions:
    # Use master position to determine correct offset
    for master_off in [0, 1]:
        all_pairs = []
        books_with_pos = 0
        books_without = 0

        for i in range(n):
            if i in positions:
                pos = positions[i]
                correct_off = (pos + master_off) % 2
                books_with_pos += 1
            else:
                # Fallback: use IC-based (inverted)
                bp0 = [books[i][j:j+2] for j in range(0, len(books[i])-1, 2)]
                bp1 = [books[i][j:j+2] for j in range(1, len(books[i])-1, 2)]
                ic0 = ic_from_counts(Counter(bp0), len(bp0))
                ic1 = ic_from_counts(Counter(bp1), len(bp1))
                correct_off = 0 if ic0 < ic1 else 1  # INVERTED
                books_without += 1

            pairs = [books[i][j:j+2] for j in range(correct_off, len(books[i])-1, 2)]
            all_pairs.extend(pairs)

        pc = Counter(all_pairs)
        ic = ic_from_counts(pc, len(all_pairs))
        print(f"Master offset {master_off}: IC = {ic*100:.4f} ({books_with_pos} positioned, {books_without} fallback)")


print("\n" + "=" * 70)
print("6. DECODE WITH INVERTED OFFSETS")
print("=" * 70)

with open('best_mapping.json', 'r') as f:
    mapping = json.load(f)

# Decode with INVERTED IC offsets
all_pairs_inv = []
book_pairs_inv = []
for i, book in enumerate(books):
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    ic0 = ic_from_counts(Counter(bp0), len(bp0))
    ic1 = ic_from_counts(Counter(bp1), len(bp1))
    off = 0 if ic0 < ic1 else 1  # INVERTED

    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs_inv.append(pairs)
    all_pairs_inv.extend(pairs)

decoded_inv = ''.join(mapping.get(p, '?') for p in all_pairs_inv)

german_words = [
    'DER', 'DIE', 'DAS', 'UND', 'IST', 'EIN', 'EINE', 'EINEN', 'EINER',
    'DEN', 'DEM', 'VON', 'HAT', 'AUF', 'MIT', 'DES', 'SIE', 'ICH',
    'SIND', 'AUS', 'BEI', 'RUNE', 'RUNEN', 'STEIN', 'NICHT',
    'ABER', 'AUCH', 'NACH', 'NOCH', 'KANN', 'WIRD', 'SEIN',
    'ENDE', 'FEUER', 'WASSER', 'ERDE', 'LICHT', 'LEBEN',
]

word_counts_inv = {}
for word in german_words:
    c = decoded_inv.count(word)
    if c > 0:
        word_counts_inv[word] = c

total_inv = sum(word_counts_inv.values())
print(f"Inverted offsets: {total_inv} German word hits")
print(f"Words: {sorted(word_counts_inv.items(), key=lambda x: -x[1])[:20]}")

# Compare with standard offsets
all_pairs_std = []
for i, book in enumerate(books):
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    ic0 = ic_from_counts(Counter(bp0), len(bp0))
    ic1 = ic_from_counts(Counter(bp1), len(bp1))
    off = 0 if ic0 > ic1 else 1  # STANDARD

    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    all_pairs_std.extend(pairs)

decoded_std = ''.join(mapping.get(p, '?') for p in all_pairs_std)

word_counts_std = {}
for word in german_words:
    c = decoded_std.count(word)
    if c > 0:
        word_counts_std[word] = c

total_std = sum(word_counts_std.values())
print(f"\nStandard offsets: {total_std} German word hits")
print(f"Words: {sorted(word_counts_std.items(), key=lambda x: -x[1])[:20]}")

# Show some decoded books with inverted offsets
print(f"\nSample books (inverted offsets):")
for i in range(min(10, len(book_pairs_inv))):
    decoded = ''.join(mapping.get(p, '?') for p in book_pairs_inv[i])
    bp0 = [books[i][j:j+2] for j in range(0, len(books[i])-1, 2)]
    bp1 = [books[i][j:j+2] for j in range(1, len(books[i])-1, 2)]
    ic0 = ic_from_counts(Counter(bp0), len(bp0))
    ic1 = ic_from_counts(Counter(bp1), len(bp1))
    std_off = 0 if ic0 > ic1 else 1
    inv_off = 1 - std_off
    print(f"\n  Book {i:2d} (std_off={std_off} inv_off={inv_off}, {len(decoded)} letters):")
    for j in range(0, len(decoded), 70):
        print(f"    {decoded[j:j+70]}")


print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
