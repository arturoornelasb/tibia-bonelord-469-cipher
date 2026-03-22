"""Reconstruct the superstring from overlapping books and try to read it."""
import json
from collections import Counter

with open('books.json', 'r') as f:
    books = json.load(f)

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

all_codes = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U',
    '00': 'H', '14': 'N', '72': 'R', '91': 'S', '15': 'I',
    '76': 'E', '52': 'S', '42': 'D', '46': 'I', '48': 'N',
    '57': 'H', '04': 'M', '12': 'S', '58': 'N',
    '78': 'T', '51': 'R', '35': 'A', '34': 'L',
    '01': 'E', '59': 'S', '41': 'E', '30': 'E',
    '94': 'H',
    '47': 'D', '13': 'N', '71': 'I', '63': 'D',
    '93': 'N', '28': 'D', '86': 'E', '43': 'U',
    '70': 'U', '65': 'I', '16': 'I', '36': 'W',
    '64': 'T', '89': 'A', '80': 'G', '97': 'G', '75': 'T',
    '08': 'R', '20': 'F', '96': 'L', '99': 'O', '55': 'R',
    '67': 'E', '27': 'E', '03': 'E', '09': 'E', '05': 'C', '53': 'N',
    '44': 'U', '62': 'B', '68': 'R',
    '23': 'S', '17': 'E', '29': 'E', '66': 'A', '49': 'E',
    '38': 'K', '77': 'Z',
    '22': 'K', '82': 'O', '73': 'N', '50': 'I', '84': 'G',
    '25': 'O', '83': 'V', '81': 'T', '24': 'I',
    '79': 'O', '10': 'R',
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# Decode all books to code-pair sequences (for overlap detection)
book_raw = []
for bpairs in book_pairs:
    book_raw.append(' '.join(bpairs))

# Build superstring by finding overlaps between books
# Use raw code pairs for matching (more reliable than decoded text)
def find_overlap(seq1, seq2, min_overlap=8):
    """Find if end of seq1 overlaps with start of seq2."""
    for length in range(min(len(seq1), len(seq2)), min_overlap - 1, -1):
        if seq1[-length:] == seq2[:length]:
            return length
    return 0

# Find all pairwise overlaps
overlaps = {}
for i in range(len(book_pairs)):
    for j in range(len(book_pairs)):
        if i == j:
            continue
        if len(book_pairs[i]) < 8 or len(book_pairs[j]) < 8:
            continue
        ov = find_overlap(book_pairs[i], book_pairs[j])
        if ov >= 8:
            overlaps[(i, j)] = ov

# Build chain: find which book continues each book
print("=" * 70)
print("BOOK OVERLAP CHAINS")
print("=" * 70)

# For each book, find the best continuation
continuations = {}
for (i, j), ov in sorted(overlaps.items(), key=lambda x: -x[1]):
    if i not in continuations:
        continuations[i] = (j, ov)

# Find chain starts (books that no other book continues into)
all_targets = set(j for j, _ in continuations.values())
chain_starts = []
for i in range(len(book_pairs)):
    if len(book_pairs[i]) >= 8 and i not in all_targets:
        chain_starts.append(i)

# Follow chains
chains = []
for start in chain_starts:
    chain = [start]
    visited = {start}
    current = start
    while current in continuations:
        next_book, ov = continuations[current]
        if next_book in visited:
            break
        chain.append(next_book)
        visited.add(next_book)
        current = next_book
    chains.append(chain)

# Find the longest chain
chains.sort(key=lambda c: -len(c))

for ci, chain in enumerate(chains[:3]):
    print(f"\nChain {ci} ({len(chain)} books): {' -> '.join(str(b) for b in chain[:20])}...")

# Build the superstring from the longest chain
if chains:
    main_chain = chains[0]
    super_pairs = list(book_pairs[main_chain[0]])
    for k in range(1, len(main_chain)):
        prev = main_chain[k-1]
        curr = main_chain[k]
        ov = overlaps.get((prev, curr), 0)
        # Append non-overlapping part
        super_pairs.extend(book_pairs[curr][ov:])

    print(f"\nSuperstring: {len(super_pairs)} pairs from {len(main_chain)} books")

    # Decode the superstring
    decoded = ''
    for p in super_pairs:
        decoded += all_codes.get(p, f'?')

    # Print in 80-char lines with position markers
    print(f"\n{'='*70}")
    print("DECODED SUPERSTRING")
    print("=" * 70)
    for i in range(0, len(decoded), 80):
        chunk = decoded[i:i+80]
        print(f"  {i:4d}: {chunk}")

    # Also print with [??] for unknowns to see where gaps are
    print(f"\n{'='*70}")
    print("DECODED WITH UNKNOWN MARKERS")
    print("=" * 70)
    decoded_marked = ''
    for p in super_pairs:
        if p in all_codes:
            decoded_marked += all_codes[p]
        else:
            decoded_marked += '.'
    for i in range(0, len(decoded_marked), 80):
        chunk = decoded_marked[i:i+80]
        print(f"  {i:4d}: {chunk}")

    # Count unknowns
    unk = decoded_marked.count('.')
    print(f"\nUnknowns in superstring: {unk}/{len(decoded_marked)} ({unk/len(decoded_marked)*100:.1f}%)")
