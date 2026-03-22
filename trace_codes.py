"""Trace specific decoded patterns back to raw code pairs."""
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
    '47': 'D', '13': 'N', '71': 'I', '79': 'H', '63': 'D',
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
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

def trace_code(code, context=5):
    print(f"Code {code} (all occurrences):")
    for idx, bpairs in enumerate(book_pairs):
        for j, p in enumerate(bpairs):
            if p != code:
                continue
            ctx_start = max(0, j - context)
            ctx_end = min(len(bpairs), j + context + 1)
            decoded_parts = []
            code_parts = []
            for k in range(ctx_start, ctx_end):
                letter = all_codes.get(bpairs[k], f"[{bpairs[k]}]")
                decoded_parts.append(letter)
                if k == j:
                    code_parts.append(f">>>{bpairs[k]}<<<")
                else:
                    code_parts.append(f"{bpairs[k]}={letter}")
            dec_str = "".join(decoded_parts)
            code_str = " ".join(code_parts)
            print(f"  Bk{idx:2d}: {dec_str:<30s} | {code_str}")

def trace_pattern(pattern, context=3):
    print(f"Pattern '{pattern}':")
    for idx, bpairs in enumerate(book_pairs):
        decoded = [all_codes.get(p, f"[{p}]") for p in bpairs]
        text = "".join(decoded)
        pos = text.find(pattern)
        if pos < 0:
            continue
        # Map char position to pair index
        char_to_pair = []
        for j, d in enumerate(decoded):
            for _ in range(len(d)):
                char_to_pair.append(j)
        start_pair = char_to_pair[pos]
        end_pair = char_to_pair[min(pos + len(pattern) - 1, len(char_to_pair) - 1)] + 1
        ctx_start = max(0, start_pair - context)
        ctx_end = min(len(bpairs), end_pair + context)
        code_parts = []
        for k in range(ctx_start, ctx_end):
            letter = all_codes.get(bpairs[k], f"[{bpairs[k]}]")
            code_parts.append(f"{bpairs[k]}={letter}")
        dec = "".join(decoded[ctx_start:ctx_end])
        print(f"  Bk{idx:2d}: {dec}")
        print(f"         {' '.join(code_parts)}")

print("=" * 70)
print("TRACING KEY PATTERNS")
print("=" * 70)

print()
trace_pattern("LABGZERAS")
print()
trace_pattern("HEARUCHTIG")
print()
trace_pattern("TOTNIURGCE")
print()
trace_pattern("SCISTSCH")

print(f"\n{'='*70}")
print("TRACING UNKNOWN CODES")
print("=" * 70)
print()
trace_code("10")
print()
trace_code("37")
print()
trace_code("40")
print()
trace_code("74")
print()
trace_code("54")
print()
trace_code("98")
print()
trace_code("02")
