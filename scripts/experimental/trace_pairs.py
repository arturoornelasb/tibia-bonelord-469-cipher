"""
Trace digit pairs alongside decoded text for key books.
Show which codes are fixed vs free to identify correction opportunities.
"""
import json
from collections import Counter

with open('books.json', 'r') as f:
    books = json.load(f)

with open('best_mapping.json', 'r') as f:
    mapping = json.load(f)

# Fixed codes from cribs
confirmed = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U',
}

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10:
        return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    ic0 = ic_from_counts(Counter(bp0), len(bp0))
    ic1 = ic_from_counts(Counter(bp1), len(bp1))
    return 0 if ic0 > ic1 else 1

# Show detailed pair-by-pair trace for key books
print("=" * 70, flush=True)
print("PAIR-BY-PAIR TRACE OF KEY BOOKS", flush=True)
print("=" * 70, flush=True)

# Pick books that contain STEIN
stein_books = []
for i, book in enumerate(books):
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    decoded = ''.join(mapping.get(p, '?') for p in pairs)
    if 'STEIN' in decoded:
        stein_books.append(i)

print(f"\nBooks containing STEIN: {stein_books}", flush=True)

for bi in stein_books[:5]:
    book = books[bi]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    decoded = ''.join(mapping.get(p, '?') for p in pairs)

    print(f"\n--- Book {bi} (offset={off}, {len(decoded)} letters) ---", flush=True)

    # Show in groups of 10 pairs
    for start in range(0, len(pairs), 10):
        end = min(start + 10, len(pairs))
        chunk_pairs = pairs[start:end]
        chunk_decoded = decoded[start:end]

        pair_str = ' '.join(chunk_pairs)
        letter_str = ' '.join(f' {c} ' if p not in confirmed else f'[{c}]' for p, c in zip(chunk_pairs, chunk_decoded))

        print(f"  Pairs:   {pair_str}", flush=True)
        print(f"  Letters: {letter_str}", flush=True)
        print(flush=True)


print("\n" + "=" * 70, flush=True)
print("CONTEXT AROUND RECURRING 'DIERELGERGENNERNNDE'", flush=True)
print("=" * 70, flush=True)

# Find this pattern in raw digit pairs
target_decoded = 'DIERELGERGENNERNNDE'
for bi in range(len(books)):
    book = books[bi]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    decoded = ''.join(mapping.get(p, '?') for p in pairs)

    pos = decoded.find(target_decoded)
    if pos >= 0:
        ctx_start = max(0, pos - 5)
        ctx_end = min(len(pairs), pos + len(target_decoded) + 5)
        ctx_pairs = pairs[ctx_start:ctx_end]
        ctx_decoded = decoded[ctx_start:ctx_end]

        print(f"\n  Book {bi} at decoded position {pos}:", flush=True)
        pair_line = ' '.join(ctx_pairs)
        letter_line = ' '.join(f'[{mapping.get(p,"?")}]' if p in confirmed else f' {mapping.get(p,"?")} ' for p in ctx_pairs)
        print(f"    Pairs:   {pair_line}", flush=True)
        print(f"    Decoded: {ctx_decoded}", flush=True)
        print(f"    Fixed:   {letter_line}", flush=True)

        # Show just the target part
        target_pairs = pairs[pos:pos+len(target_decoded)]
        print(f"    Target pairs: {target_pairs}", flush=True)

        if bi > 5:
            break  # limit output


print("\n" + "=" * 70, flush=True)
print("ANALYZE 'STEINER' CONTEXT IN DETAIL", flush=True)
print("=" * 70, flush=True)

# STEIN = 92,88,95,21,60
# What comes right before and after in each occurrence?
for bi in stein_books:
    book = books[bi]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]

    for pi in range(len(pairs) - 4):
        if (pairs[pi] == '92' and pairs[pi+1] == '88' and
            pairs[pi+2] == '95' and pairs[pi+3] == '21' and
            pairs[pi+4] == '60'):

            # Context: 8 pairs before, STEIN, 8 pairs after
            before_start = max(0, pi - 8)
            after_end = min(len(pairs), pi + 5 + 8)

            before_pairs = pairs[before_start:pi]
            after_pairs = pairs[pi+5:after_end]
            before_decoded = ''.join(mapping.get(p, '?') for p in before_pairs)
            after_decoded = ''.join(mapping.get(p, '?') for p in after_pairs)

            print(f"\n  Book {bi}: ...{before_decoded}[STEIN]{after_decoded}...", flush=True)
            print(f"    Before pairs: {before_pairs}", flush=True)
            print(f"    After pairs:  {after_pairs}", flush=True)


print("\n" + "=" * 70, flush=True)
print("WHAT GERMAN WORDS COULD 'UNSTGTSTEIN' BE?", flush=True)
print("=" * 70, flush=True)

# The pattern before STEIN is always: ...UNSTGT...
# Pairs: look at all occurrences
# The letters U N S T G T come from codes:
# Let's find the actual codes
for bi in stein_books[:3]:
    book = books[bi]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    decoded = ''.join(mapping.get(p, '?') for p in pairs)

    pos = decoded.find('STEIN')
    if pos >= 6:
        pre_pairs = pairs[pos-6:pos]
        pre_decoded = decoded[pos-6:pos]
        print(f"\n  Book {bi}: '{pre_decoded}' before STEIN", flush=True)
        for i, (p, d) in enumerate(zip(pre_pairs, pre_decoded)):
            fixed = "FIXED" if p in confirmed else "free"
            print(f"    [{p}] -> {d}  ({fixed})", flush=True)


print("\n" + "=" * 70, flush=True)
print("FREQUENCY OF CODE '34' (currently T)", flush=True)
print("=" * 70, flush=True)

# Code 34 appears in UNSTGT before STEIN
# Let's see what bigrams 34 forms with other codes
all_pairs_flat = []
for i, book in enumerate(books):
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    all_pairs_flat.extend(pairs)

# Bigrams involving 34
bigrams_34 = Counter()
for i in range(len(all_pairs_flat)-1):
    if all_pairs_flat[i] == '34' or all_pairs_flat[i+1] == '34':
        bg = (all_pairs_flat[i], all_pairs_flat[i+1])
        decoded_bg = mapping.get(bg[0], '?') + mapping.get(bg[1], '?')
        bigrams_34[(bg, decoded_bg)] += 1

for (bg, decoded), count in bigrams_34.most_common(20):
    print(f"  {bg[0]}-{bg[1]} -> {decoded}: {count} times", flush=True)


print("\n" + "=" * 70, flush=True)
print("DONE", flush=True)
print("=" * 70, flush=True)
