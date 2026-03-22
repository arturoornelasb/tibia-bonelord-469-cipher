"""Build the full superstring from all 70 books using greedy overlap assembly."""
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

# Use raw digit strings for overlap detection (more reliable)
# Convert pair sequences to strings for substring matching
book_strs = [''.join(bp) for bp in book_pairs]

# Greedy Shortest Common Superstring approach:
# 1. Find all pairwise overlaps (suffix of A matches prefix of B)
# 2. Merge the pair with the longest overlap
# 3. Repeat until one string remains

def suffix_prefix_overlap(s1, s2, min_ov=4):
    """Return length of longest suffix of s1 that matches prefix of s2."""
    max_ov = min(len(s1), len(s2))
    for length in range(max_ov, min_ov - 1, -1):
        if s1.endswith(s2[:length]):
            return length
    return 0

# Filter out very short books (< 6 digits) that might be noise
active = [i for i in range(len(book_strs)) if len(book_strs[i]) >= 6]
strings = {i: book_strs[i] for i in active}

print(f"Starting with {len(active)} books")

# Iteratively merge
merge_log = []
while len(strings) > 1:
    best_ov = 0
    best_pair = None

    keys = list(strings.keys())
    for i in range(len(keys)):
        for j in range(len(keys)):
            if keys[i] == keys[j]:
                continue
            # Check if one is substring of other
            s1, s2 = strings[keys[i]], strings[keys[j]]
            if s2 in s1:
                # s2 is contained in s1, remove s2
                best_ov = len(s2)
                best_pair = (keys[i], keys[j], 'contained')
                break
            ov = suffix_prefix_overlap(s1, s2)
            if ov > best_ov:
                best_ov = ov
                best_pair = (keys[i], keys[j], 'overlap')
        if best_pair and best_pair[2] == 'contained':
            break

    if best_pair is None or best_ov < 4:
        break

    id_a, id_b, merge_type = best_pair
    if merge_type == 'contained':
        merge_log.append(f"  Book {id_b} contained in {id_a} (len={best_ov})")
        del strings[id_b]
    else:
        merged = strings[id_a] + strings[id_b][best_ov:]
        merge_log.append(f"  Merge {id_a}+{id_b}: overlap={best_ov} digits, result={len(merged)} digits")
        # Use the smaller key
        new_key = min(id_a, id_b)
        del strings[id_a]
        del strings[id_b]
        strings[new_key] = merged

print(f"\nAfter merging: {len(strings)} string(s)")
for key, s in strings.items():
    print(f"  Fragment (root book {key}): {len(s)} digits = {len(s)//2} pairs")

# Show last 10 merges
print(f"\nLast 10 merges:")
for line in merge_log[-10:]:
    print(line)

# Decode the result
if len(strings) == 1:
    superstr = list(strings.values())[0]
    # Parse into pairs
    super_pairs = [superstr[i:i+2] for i in range(0, len(superstr)-1, 2)]

    decoded = ''
    for p in super_pairs:
        decoded += all_codes.get(p, '.')

    print(f"\n{'='*70}")
    print(f"FULL SUPERSTRING: {len(super_pairs)} pairs, {len(decoded)} chars")
    print("=" * 70)

    unk = decoded.count('.')
    print(f"Unknown: {unk}/{len(decoded)} ({unk/len(decoded)*100:.1f}%)")

    for i in range(0, len(decoded), 80):
        chunk = decoded[i:i+80]
        print(f"  {i:4d}: {chunk}")
else:
    # Multiple fragments - show each
    for key, s in sorted(strings.items(), key=lambda x: -len(x[1])):
        pairs = [s[i:i+2] for i in range(0, len(s)-1, 2)]
        decoded = ''.join(all_codes.get(p, '.') for p in pairs)
        unk = decoded.count('.')
        print(f"\n{'='*70}")
        print(f"FRAGMENT (root {key}): {len(pairs)} pairs, unk={unk}")
        print("=" * 70)
        for i in range(0, len(decoded), 80):
            chunk = decoded[i:i+80]
            print(f"  {i:4d}: {chunk}")
