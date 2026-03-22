"""Deep investigation of code 16: I or O?
Also investigate codes 39, 87, and the MINH[74]DDE pattern."""
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
    '85': 'A', '61': 'U', '00': 'H', '14': 'N', '72': 'R',
    '91': 'S', '15': 'I', '76': 'E', '52': 'S', '42': 'D',
    '46': 'I', '48': 'N', '57': 'H', '04': 'M', '12': 'S',
    '58': 'N', '78': 'T', '51': 'R', '35': 'A', '34': 'L',
    '01': 'E', '59': 'S', '41': 'E', '30': 'E', '94': 'H',
    '47': 'D', '13': 'N', '71': 'I', '63': 'D', '93': 'N',
    '28': 'D', '86': 'E', '43': 'U', '70': 'U', '65': 'I',
    '16': 'I', '36': 'W', '64': 'T', '89': 'A', '80': 'G',
    '97': 'G', '75': 'T', '08': 'R', '20': 'F', '96': 'L',
    '99': 'O', '55': 'R', '67': 'E', '27': 'E', '03': 'E',
    '09': 'E', '05': 'C', '53': 'N', '44': 'U', '62': 'B',
    '68': 'R', '23': 'S', '17': 'E', '29': 'E', '66': 'A',
    '49': 'E', '38': 'K', '77': 'Z', '22': 'K', '82': 'O',
    '73': 'N', '50': 'I', '84': 'G', '25': 'O', '83': 'V',
    '81': 'T', '24': 'I', '79': 'O', '10': 'R', '54': 'M',
    '98': 'T',
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# ============================================================
# CODE 16: Show ALL 38 contexts with I vs O
# ============================================================
print("=" * 80)
print("CODE 16: ALL CONTEXTS — comparing I vs O")
print("=" * 80)

codes_as_I = dict(all_codes)
codes_as_O = {**all_codes, '16': 'O'}

for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p != '16':
            continue
        start = max(0, j - 10)
        end = min(len(bpairs), j + 11)

        text_i = ''.join(codes_as_I.get(bpairs[k], '?') for k in range(start, end))
        text_o = ''.join(codes_as_O.get(bpairs[k], '?') for k in range(start, end))
        pos = j - start

        # Highlight the changed letter
        i_hl = text_i[:pos] + '[' + text_i[pos] + ']' + text_i[pos+1:]
        o_hl = text_o[:pos] + '[' + text_o[pos] + ']' + text_o[pos+1:]

        print(f"  Bk{idx:2d}: I={i_hl}")
        print(f"         O={o_hl}")

# Count bigrams around code 16 with both assignments
print(f"\n{'='*80}")
print("BIGRAM ANALYSIS: code 16 as I vs O")
print("=" * 80)

for label, test_codes in [("16=I", codes_as_I), ("16=O", codes_as_O)]:
    bigrams_16 = Counter()
    for idx, bpairs in enumerate(book_pairs):
        for j, p in enumerate(bpairs):
            if p != '16':
                continue
            # Get the letter before and after
            if j > 0:
                prev = test_codes.get(bpairs[j-1], '?')
                curr = test_codes.get(bpairs[j], '?')
                bigrams_16[prev + curr] += 1
            if j < len(bpairs) - 1:
                curr = test_codes.get(bpairs[j], '?')
                nxt = test_codes.get(bpairs[j+1], '?')
                bigrams_16[curr + nxt] += 1

    print(f"\n{label}:")
    # Show sorted by count
    for bg, cnt in bigrams_16.most_common(20):
        # Flag bad bigrams
        bad = ""
        if bg[0] == bg[1] and bg[0] in 'EIIHDPAOU':
            bad = " <-- DOUBLE!"
        print(f"  {bg}: {cnt}{bad}")

# ============================================================
# FREQUENCY IMPACT: what happens to letter frequencies with 16=O
# ============================================================
print(f"\n{'='*80}")
print("FREQUENCY IMPACT: 16=I vs 16=O")
print("=" * 80)

german_freq = {
    'E': 16.93, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
    'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
    'L': 3.44, 'C': 3.06, 'G': 3.01, 'M': 2.53, 'O': 2.51,
    'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
    'P': 0.79, 'V': 0.67,
}

for label, test_codes in [("16=I", codes_as_I), ("16=O", codes_as_O)]:
    counts = Counter()
    total = 0
    for bpairs in book_pairs:
        for p in bpairs:
            letter = test_codes.get(p)
            if letter:
                counts[letter] += 1
                total += 1

    print(f"\n{label}:")
    for letter in ['I', 'O', 'S', 'E', 'N']:
        pct = counts[letter] / total * 100
        expected = german_freq[letter]
        delta = pct - expected
        print(f"  {letter}: {pct:5.1f}% (exp {expected:4.1f}%, {delta:+5.1f}%)")

# ============================================================
# CODE 39: Validate E assignment
# ============================================================
print(f"\n{'='*80}")
print("CODE 39: Both contexts with E")
print("=" * 80)

codes_39E = {**all_codes, '39': 'E'}
for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p != '39':
            continue
        start = max(0, j - 12)
        end = min(len(bpairs), j + 13)
        text = ''.join(codes_39E.get(bpairs[k], '?') for k in range(start, end))
        pos = j - start
        hl = text[:pos] + '[' + text[pos] + ']' + text[pos+1:]
        print(f"  Bk{idx:2d}: {hl}")

# ============================================================
# CODE 87: Both contexts with W
# ============================================================
print(f"\n{'='*80}")
print("CODE 87: Both contexts with W")
print("=" * 80)

codes_87W = {**all_codes, '87': 'W'}
for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p != '87':
            continue
        start = max(0, j - 12)
        end = min(len(bpairs), j + 13)
        text = ''.join(codes_87W.get(bpairs[k], '?') for k in range(start, end))
        pos = j - start
        hl = text[:pos] + '[' + text[pos] + ']' + text[pos+1:]
        print(f"  Bk{idx:2d}: {hl}")

# ============================================================
# MINH[74]DDE: Look at the raw codes around this pattern
# ============================================================
print(f"\n{'='*80}")
print("MINH[74]DDE: RAW CODE PAIRS for the full pattern context")
print("=" * 80)

for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p != '74':
            continue
        # Check if this is the MINH pattern
        if j >= 4:
            context = ''.join(all_codes.get(bpairs[k], '?') for k in range(j-4, j))
            if context == 'MINH':
                start = max(0, j - 8)
                end = min(len(bpairs), j + 12)
                raw = ' '.join(bpairs[start:end])
                decoded = ''.join(all_codes.get(bpairs[k], f'[{bpairs[k]}]') for k in range(start, end))
                print(f"  Bk{idx:2d}: raw={raw}")
                print(f"         dec={decoded}")
                break  # Only show first occurrence per book

# ============================================================
# What is MINH? Could it be a fragment of a larger word?
# ============================================================
print(f"\n{'='*80}")
print("EXTENDED CONTEXT around MINH[74]DDE pattern")
print("=" * 80)

for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p != '74':
            continue
        if j >= 4:
            context = ''.join(all_codes.get(bpairs[k], '?') for k in range(j-4, j))
            if context == 'MINH':
                start = max(0, j - 15)
                end = min(len(bpairs), j + 20)
                decoded = ''.join(all_codes.get(bpairs[k], f'[{bpairs[k]}]') for k in range(start, end))
                print(f"  Bk{idx:2d}: {decoded}")
                break

# ============================================================
# What about code 74 in NON-MINH contexts?
# ============================================================
print(f"\n{'='*80}")
print("CODE 74 in NON-MINH contexts (wider view)")
print("=" * 80)

for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p != '74':
            continue
        # Check if this is NOT the MINH pattern
        if j >= 4:
            context = ''.join(all_codes.get(bpairs[k], '?') for k in range(j-4, j))
        else:
            context = ''
        if context != 'MINH':
            start = max(0, j - 12)
            end = min(len(bpairs), j + 13)
            decoded = ''.join(all_codes.get(bpairs[k], f'[{bpairs[k]}]') for k in range(start, end))
            pos = j - start
            raw_pairs = ' '.join(bpairs[start:end])
            print(f"  Bk{idx:2d}: {decoded}")
            print(f"         raw: {raw_pairs}")

# ============================================================
# Full superstring readability test
# ============================================================
print(f"\n{'='*80}")
print("FULL DECODED TEXT (books 60+ pairs, one line each)")
print("=" * 80)

for idx, bpairs in enumerate(book_pairs):
    if len(bpairs) < 60:
        continue
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    print(f"\nBk{idx:2d} ({len(bpairs)}p): {text}")
