"""
Build complete master text from all book overlaps, decode it,
and analyze for German readability. Try both offsets.
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

n = len(books)
print("=" * 70, flush=True)
print("1. BUILD COMPLETE MASTER TEXT", flush=True)
print("=" * 70, flush=True)

# Find all pairwise suffix-prefix overlaps
edges = []
for i in range(n):
    for j in range(n):
        if i == j:
            continue
        bi, bj = books[i], books[j]
        max_k = min(len(bi), len(bj))
        for k in range(max_k, 4, -1):
            if bi[-k:] == bj[:k]:
                edges.append((i, j, k))
                break

# Build best successor/predecessor
best_successor = {}
best_predecessor = {}
for i, j, k in edges:
    if i not in best_successor or k > best_successor[i][1]:
        best_successor[i] = (j, k)
    if j not in best_predecessor or k > best_predecessor[j][1]:
        best_predecessor[j] = (i, k)

# Follow chains
used = set()
chains = []
starting = sorted(range(n), key=lambda i: -len(books[i]))

for start in starting:
    if start in used:
        continue
    chain = [start]
    used.add(start)

    current = start
    while current in best_successor:
        next_b, ov = best_successor[current]
        if next_b in used:
            break
        chain.append(next_b)
        used.add(next_b)
        current = next_b

    current = start
    while current in best_predecessor:
        prev_b, ov = best_predecessor[current]
        if prev_b in used:
            break
        chain.insert(0, prev_b)
        used.add(prev_b)
        current = prev_b

    chains.append(chain)

# Build master text for each chain
chain_masters = []
for ci, chain in enumerate(chains):
    master = books[chain[0]]
    for k in range(1, len(chain)):
        prev, curr = chain[k-1], chain[k]
        overlap = best_successor[prev][1]
        master = master + books[curr][overlap:]
    chain_masters.append(master)
    print(f"Chain {ci}: {len(chain)} books, {len(master)} digits", flush=True)

# The longest chain should be the main text
main_chain_idx = max(range(len(chains)), key=lambda i: len(chain_masters[i]))
master = chain_masters[main_chain_idx]
main_chain = chains[main_chain_idx]

print(f"\nMain chain: chain {main_chain_idx}, {len(main_chain)} books, {len(master)} digits", flush=True)

# Check which books are contained
contained = 0
not_contained = []
for i in range(n):
    if master.find(books[i]) >= 0:
        contained += 1
    else:
        not_contained.append(i)

print(f"Books contained: {contained}/{n}", flush=True)

# Try to merge other chains into master
for ci, cm in enumerate(chain_masters):
    if ci == main_chain_idx:
        continue
    if master.find(cm) >= 0:
        continue
    # Try suffix-prefix
    for k in range(min(200, len(master), len(cm)), 4, -1):
        if cm[-k:] == master[:k]:
            master = cm[:-k] + master
            print(f"  Prepended chain {ci} ({len(cm)} digits, overlap {k})", flush=True)
            break
        if master[-k:] == cm[:k]:
            master = master + cm[k:]
            print(f"  Appended chain {ci} ({len(cm)} digits, overlap {k})", flush=True)
            break

# Recheck containment
contained = 0
for i in range(n):
    if master.find(books[i]) >= 0:
        contained += 1
print(f"\nAfter merge: {len(master)} digits, {contained}/{n} books contained", flush=True)


print("\n" + "=" * 70, flush=True)
print("2. DECODE MASTER TEXT AT BOTH OFFSETS", flush=True)
print("=" * 70, flush=True)

for off in [0, 1]:
    pairs = [master[j:j+2] for j in range(off, len(master)-1, 2)]
    decoded = ''.join(mapping.get(p, '?') for p in pairs)

    # Count German words
    german_words = [
        'DER', 'DIE', 'DAS', 'UND', 'IST', 'EIN', 'EINE', 'EINEN', 'EINER',
        'DEN', 'DEM', 'VON', 'HAT', 'AUF', 'MIT', 'DES', 'SIE', 'ICH',
        'SIND', 'AUS', 'BEI', 'RUNE', 'RUNEN', 'STEIN', 'STEINEN',
        'ABER', 'AUCH', 'DASS', 'NACH', 'WIR', 'KANN', 'NOCH', 'DIESE',
        'NICHT', 'WIRD', 'SEIN', 'WENN', 'NUR', 'ALLE', 'WELT', 'ENDE',
    ]

    word_hits = {}
    for w in german_words:
        c = decoded.count(w)
        if c > 0:
            word_hits[w] = c
    total_hits = sum(word_hits.values())

    pc = Counter(pairs)
    ic = ic_from_counts(pc, len(pairs))

    print(f"\nOffset {off}: {len(decoded)} letters, IC={ic*100:.4f}, {total_hits} word hits", flush=True)
    print(f"  Words: {sorted(word_hits.items(), key=lambda x: -x[1])[:15]}", flush=True)
    print(f"\n  Decoded text (first 500):", flush=True)
    for j in range(0, min(500, len(decoded)), 80):
        print(f"    {decoded[j:j+80]}", flush=True)
    print(f"\n  Decoded text (chars 500-1000):", flush=True)
    for j in range(500, min(1000, len(decoded)), 80):
        print(f"    {decoded[j:j+80]}", flush=True)


print("\n" + "=" * 70, flush=True)
print("3. RAW DIGIT PAIRS AROUND STEIN OCCURRENCES", flush=True)
print("=" * 70, flush=True)

# Find STEIN (92,88,95,21,60) in master text at correct offset
for off in [0, 1]:
    pairs = [master[j:j+2] for j in range(off, len(master)-1, 2)]
    print(f"\nOffset {off}:", flush=True)
    for pi in range(len(pairs) - 4):
        if (pairs[pi] == '92' and pairs[pi+1] == '88' and
            pairs[pi+2] == '95' and pairs[pi+3] == '21' and
            pairs[pi+4] == '60'):
            # Show context: 10 pairs before and after
            ctx_start = max(0, pi-10)
            ctx_end = min(len(pairs), pi+15)
            ctx_pairs = pairs[ctx_start:ctx_end]
            ctx_decoded = ''.join(mapping.get(p, '?') for p in ctx_pairs)
            stein_pos_in_ctx = pi - ctx_start
            print(f"  STEIN at pair {pi}:", flush=True)
            print(f"    Pairs: {ctx_pairs}", flush=True)
            print(f"    Decoded: {ctx_decoded}", flush=True)
            print(f"    Position in master: digit {off + pi*2}", flush=True)


print("\n" + "=" * 70, flush=True)
print("4. LOOK FOR WORD BOUNDARIES USING DOUBLE LETTERS", flush=True)
print("=" * 70, flush=True)

# In German, doubled consonants are rare at word boundaries
# Double vowels like EE, AA are very rare
# Let's look at the decoded master text
off = 0  # Use the offset with more word hits
pairs = [master[j:j+2] for j in range(off, len(master)-1, 2)]
decoded = ''.join(mapping.get(p, '?') for p in pairs)

# Find positions where the same letter appears twice
doubles = Counter()
for i in range(len(decoded)-1):
    if decoded[i] == decoded[i+1]:
        ctx = decoded[max(0,i-5):i+7]
        doubles[decoded[i]] += 1

print("Double letter frequencies:", flush=True)
for letter, count in doubles.most_common():
    print(f"  {letter}{letter}: {count} times", flush=True)


print("\n" + "=" * 70, flush=True)
print("5. FREQUENCY OF EACH CODE IN MASTER TEXT", flush=True)
print("=" * 70, flush=True)

# For the master text at offset 0
pairs_0 = [master[j:j+2] for j in range(0, len(master)-1, 2)]
pairs_1 = [master[j:j+2] for j in range(1, len(master)-1, 2)]

pc0 = Counter(pairs_0)
pc1 = Counter(pairs_1)
ic0 = ic_from_counts(pc0, len(pairs_0))
ic1 = ic_from_counts(pc1, len(pairs_1))
print(f"Master offset 0: IC={ic0*100:.4f}, {len(pairs_0)} pairs", flush=True)
print(f"Master offset 1: IC={ic1*100:.4f}, {len(pairs_1)} pairs", flush=True)


print("\n" + "=" * 70, flush=True)
print("6. SAVE MASTER TEXT", flush=True)
print("=" * 70, flush=True)

with open('master_text.txt', 'w') as f:
    f.write(master)
print(f"Saved master text ({len(master)} digits) to master_text.txt", flush=True)

# Also save the chain structure
chain_info = {
    'main_chain_idx': main_chain_idx,
    'chains': [[int(b) for b in c] for c in chains],
    'master_length': len(master),
    'books_contained': contained
}
with open('chain_info.json', 'w') as f:
    json.dump(chain_info, f, indent=2)
print("Saved chain_info.json", flush=True)

print("\n" + "=" * 70, flush=True)
print("DONE", flush=True)
print("=" * 70, flush=True)
