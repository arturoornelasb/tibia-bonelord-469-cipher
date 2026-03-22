"""Trace mystery decoded terms back to raw code pairs and test alternatives."""
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

# Find all mystery patterns in decoded text by scanning books for suspicious sequences
# Focus on: LABGZERAS, HEARUCHTIGER, TOTNIURGCE, GETRASES, SCISTSCH

mystery_patterns = ['LABGZERAS', 'HEARUCHTIG', 'TOTNIURG', 'GETRASE', 'SCISTSCH', 'MINH']

print("=" * 80)
print("MYSTERY TERM TRACING — Raw code pairs behind each mystery term")
print("=" * 80)

for pattern in mystery_patterns:
    print(f"\n{'='*70}")
    print(f"PATTERN: {pattern}")
    print("=" * 70)

    for idx, bpairs in enumerate(book_pairs):
        decoded = ''.join(all_codes.get(p, '?') for p in bpairs)

        pos = 0
        while True:
            pos = decoded.find(pattern, pos)
            if pos == -1:
                break

            # Show wider context
            ctx_start = max(0, pos - 8)
            ctx_end = min(len(decoded), pos + len(pattern) + 8)

            # Show decoded with markers
            ctx_decoded = decoded[ctx_start:ctx_end]
            marker_pos = pos - ctx_start
            marked = (ctx_decoded[:marker_pos] +
                      '[' + ctx_decoded[marker_pos:marker_pos+len(pattern)] + ']' +
                      ctx_decoded[marker_pos+len(pattern):])

            # Show raw code pairs
            code_str = ' '.join(bpairs[ctx_start:ctx_end])

            # Mark unknown codes
            codes_annotated = []
            for k in range(ctx_start, ctx_end):
                p = bpairs[k]
                letter = all_codes.get(p, '?')
                if p not in all_codes:
                    codes_annotated.append(f'>>>{p}<<<')
                elif k >= pos and k < pos + len(pattern):
                    codes_annotated.append(f'*{p}={letter}*')
                else:
                    codes_annotated.append(f'{p}={letter}')

            print(f"\n  Bk{idx:2d} pos={pos}: {marked}")
            print(f"    Codes: {' '.join(codes_annotated)}")

            pos += 1

# Now specifically trace what codes produce the unknown terms
# Check if any of codes 74, 54, 37, 40, 98 appear near these patterns
print(f"\n\n{'='*80}")
print("UNKNOWN CODES (74,54,37,40,98) IN CONTEXT — wide windows")
print("=" * 80)

unknown_codes = ['74', '54', '37', '40', '98']
for code in unknown_codes:
    print(f"\n--- Code {code} (freq in books: {sum(1 for bp in book_pairs for p in bp if p == code)}) ---")
    for idx, bpairs in enumerate(book_pairs):
        for j, p in enumerate(bpairs):
            if p != code:
                continue
            # Wide context window
            ctx_start = max(0, j - 12)
            ctx_end = min(len(bpairs), j + 13)

            decoded_parts = []
            for k in range(ctx_start, ctx_end):
                letter = all_codes.get(bpairs[k], f'[{bpairs[k]}]')
                if k == j:
                    decoded_parts.append(f'>>>{letter}<<<')
                else:
                    decoded_parts.append(letter)

            decoded_str = ''.join(decoded_parts)
            print(f"  Bk{idx:2d}: {decoded_str}")

# Test if LABGZERAS could be a proper noun with different unknown code assignments
print(f"\n\n{'='*80}")
print("TESTING: What if mystery terms contain misassigned codes?")
print("=" * 80)

# Find LABGZERAS contexts and check nearby codes
print("\nLABGZERAS — checking if any codes in this sequence could be different:")
for idx, bpairs in enumerate(book_pairs):
    decoded = ''.join(all_codes.get(p, '?') for p in bpairs)
    pos = decoded.find('LABGZERAS')
    if pos == -1:
        continue

    # Get the actual codes
    codes_in_seq = bpairs[pos:pos+9]
    print(f"  Bk{idx}: codes = {' '.join(codes_in_seq)}")
    for k, c in enumerate(codes_in_seq):
        letter = all_codes.get(c, '?')
        # Show frequency rank
        freq = sum(1 for bp in book_pairs for p in bp if p == c)
        # How many other letters this code maps to in tier analysis
        print(f"    pos {k}: code={c} → {letter} (freq={freq})")

# Check HEARUCHTIG similarly
print("\nHEARUCHTIG — checking codes:")
for idx, bpairs in enumerate(book_pairs):
    decoded = ''.join(all_codes.get(p, '?') for p in bpairs)
    pos = decoded.find('HEARUCHTIG')
    if pos == -1:
        continue

    codes_in_seq = bpairs[pos:pos+10]
    print(f"  Bk{idx}: codes = {' '.join(codes_in_seq)}")
    for k, c in enumerate(codes_in_seq):
        letter = all_codes.get(c, '?')
        freq = sum(1 for bp in book_pairs for p in bp if p == c)
        print(f"    pos {k}: code={c} → {letter} (freq={freq})")
    break  # Just show one

# KEY TEST: What if some high-frequency codes mapped to I are actually other letters?
# Code 46=I has 158 occurrences and causes 43 II bigrams
# What if 46 is actually something else? Try all letters and see word impact
print(f"\n\n{'='*80}")
print("WHAT IF LABGZERAS IS A REAL WORD WITH DIFFERENT CODES?")
print("=" * 80)

# The G in LABGZERAS comes from code 80=G or 97=G or 84=G
# The Z comes from 77=Z
# The B comes from 62=B
# If any of these are wrong, the word changes
# Let's find the exact codes
for idx, bpairs in enumerate(book_pairs):
    decoded = ''.join(all_codes.get(p, '?') for p in bpairs)
    pos = decoded.find('LABGZERAS')
    if pos == -1:
        continue

    codes = bpairs[pos:pos+9]  # L A B G Z E R A S
    print(f"\n  LABGZERAS in Bk{idx}: {' '.join(codes)}")

    # Try alternative mappings for each position
    for alt_pos in range(9):
        original_letter = all_codes.get(codes[alt_pos], '?')
        for test_letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if test_letter == original_letter:
                continue
            test_word = list('LABGZERAS')
            test_word[alt_pos] = test_letter
            test_str = ''.join(test_word)
            # Check if this makes a recognizable word/name
            # Focus on patterns that look like German words
            # or Tibia proper nouns
