"""
Build the shortest superstring containing all 70 books.
Use greedy approach: repeatedly merge the pair with longest overlap.
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

print("=" * 70, flush=True)
print("GREEDY SHORTEST SUPERSTRING", flush=True)
print("=" * 70, flush=True)

# First remove books that are fully contained in other books
# Keep only "independent" books
active = list(range(len(books)))
contained_in = {}

for i in range(len(books)):
    for j in range(len(books)):
        if i == j:
            continue
        if len(books[i]) < len(books[j]):
            if books[j].find(books[i]) >= 0:
                contained_in.setdefault(i, []).append(j)

# Find books that are contained in at least one other book
truly_contained = set()
for i, containers in contained_in.items():
    truly_contained.add(i)

independent = [i for i in range(len(books)) if i not in truly_contained]
print(f"Total books: {len(books)}", flush=True)
print(f"Contained in others: {len(truly_contained)}", flush=True)
print(f"Independent: {len(independent)}", flush=True)

# Work with independent books only
strings = [books[i] for i in independent]
string_ids = list(independent)

# Precompute all pairwise suffix-prefix overlaps
def compute_overlap(a, b):
    """Length of longest suffix of a that equals prefix of b."""
    max_k = min(len(a), len(b))
    for k in range(max_k, 0, -1):
        if a[-k:] == b[:k]:
            return k
    return 0

# Greedy merge: repeatedly merge pair with longest overlap
iteration = 0
while len(strings) > 1:
    best_ov = -1
    best_i = -1
    best_j = -1

    for i in range(len(strings)):
        for j in range(len(strings)):
            if i == j:
                continue
            ov = compute_overlap(strings[i], strings[j])
            if ov > best_ov:
                best_ov = ov
                best_i = i
                best_j = j

    if best_ov <= 0:
        # No overlap found, just concatenate
        print(f"  No more overlaps at {len(strings)} strings remaining", flush=True)
        break

    # Merge strings[best_i] and strings[best_j]
    merged = strings[best_i] + strings[best_j][best_ov:]

    if iteration < 20 or iteration % 10 == 0:
        print(f"  Merge {iteration}: books {string_ids[best_i]}+{string_ids[best_j]}, "
              f"overlap={best_ov}, result={len(merged)} digits, {len(strings)-1} remaining", flush=True)

    # Replace best_i with merged, remove best_j
    new_id = f"{string_ids[best_i]}+{string_ids[best_j]}"
    strings[best_i] = merged
    string_ids[best_i] = new_id
    strings.pop(best_j)
    string_ids.pop(best_j)
    iteration += 1

print(f"\nFinal: {len(strings)} string(s)", flush=True)
for i, s in enumerate(strings):
    print(f"  String {i}: {len(s)} digits", flush=True)

# The master text
if len(strings) == 1:
    master = strings[0]
else:
    # Concatenate remaining strings
    master = ''.join(strings)

# Verify all books are contained
contained_count = 0
not_found = []
for i in range(len(books)):
    if master.find(books[i]) >= 0:
        contained_count += 1
    else:
        not_found.append(i)

print(f"\nAll books contained: {contained_count}/{len(books)}", flush=True)
if not_found:
    print(f"NOT found: {not_found}", flush=True)
    for i in not_found:
        print(f"  Book {i}: {len(books[i])} digits, '{books[i][:40]}...'", flush=True)


print("\n" + "=" * 70, flush=True)
print("MASTER TEXT PROPERTIES", flush=True)
print("=" * 70, flush=True)

print(f"Length: {len(master)} digits", flush=True)

# Check circularity
for k in range(min(200, len(master)//2), 4, -1):
    if master[-k:] == master[:k]:
        print(f"CIRCULAR overlap: {k} digits", flush=True)
        break

# IC at both offsets
for off in [0, 1]:
    pairs = [master[j:j+2] for j in range(off, len(master)-1, 2)]
    pc = Counter(pairs)
    ic = ic_from_counts(pc, len(pairs))
    print(f"Offset {off}: IC={ic*100:.4f}, {len(pairs)} pairs, {len(pc)} unique", flush=True)


print("\n" + "=" * 70, flush=True)
print("DECODE MASTER TEXT", flush=True)
print("=" * 70, flush=True)

german_words = [
    'DER', 'DIE', 'DAS', 'UND', 'IST', 'EIN', 'EINE', 'EINEN', 'EINER',
    'DEN', 'DEM', 'VON', 'HAT', 'AUF', 'MIT', 'DES', 'SIE', 'ICH',
    'SIND', 'AUS', 'BEI', 'RUNE', 'RUNEN', 'STEIN', 'STEINEN',
    'ABER', 'AUCH', 'DASS', 'NACH', 'WIR', 'KANN', 'NOCH', 'DIESE',
    'NICHT', 'WIRD', 'SEIN', 'WENN', 'NUR', 'ALLE', 'WELT', 'ENDE',
]

for off in [0, 1]:
    pairs = [master[j:j+2] for j in range(off, len(master)-1, 2)]
    decoded = ''.join(mapping.get(p, '?') for p in pairs)

    word_hits = {}
    for w in german_words:
        c = decoded.count(w)
        if c > 0:
            word_hits[w] = c
    total_hits = sum(word_hits.values())

    print(f"\nOffset {off}: {total_hits} word hits", flush=True)
    print(f"  Top words: {sorted(word_hits.items(), key=lambda x: -x[1])[:20]}", flush=True)

    print(f"\n  FULL decoded text:", flush=True)
    for j in range(0, len(decoded), 80):
        print(f"    {decoded[j:j+80]}", flush=True)


print("\n" + "=" * 70, flush=True)
print("BOOK POSITIONS IN MASTER", flush=True)
print("=" * 70, flush=True)

positions = []
for i in range(len(books)):
    pos = master.find(books[i])
    positions.append((i, pos, len(books[i])))

positions.sort(key=lambda x: x[1])
for bi, pos, blen in positions:
    if pos >= 0:
        # Correct pair offset depends on position in master
        # If master offset is X, book at position pos has offset (pos + X) % 2
        for master_off in [0, 1]:
            correct_off = (pos + master_off) % 2
        print(f"  Book {bi:2d} at pos {pos:4d} ({blen:3d}d) parity={pos%2}", flush=True)

# Save
with open('master_text.txt', 'w') as f:
    f.write(master)
print(f"\nSaved master ({len(master)} digits)", flush=True)

print("\n" + "=" * 70, flush=True)
print("DONE", flush=True)
print("=" * 70, flush=True)
