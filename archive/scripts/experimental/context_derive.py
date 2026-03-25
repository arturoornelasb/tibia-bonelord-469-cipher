"""
Context-based code derivation: use ONLY the 39 fixed codes,
show ? for unknowns, then analyze what letters the unknowns
must be based on surrounding German word context.
"""
import json
from collections import Counter, defaultdict

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

# 39 fixed codes ONLY
fixed = {
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
}

# Get all book pairs
book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# Decode with fixed only
def decode_fixed(pairs):
    result = []
    for p in pairs:
        if p in fixed:
            result.append(fixed[p])
        else:
            result.append(f'[{p}]')
    return result

# Count all unknown codes
all_pairs_flat = []
for pairs in book_pairs:
    all_pairs_flat.extend(pairs)
pair_counts = Counter(all_pairs_flat)
total_pairs = sum(pair_counts.values())

unknown_codes = sorted(
    [c for c in pair_counts if c not in fixed],
    key=lambda c: -pair_counts[c]
)

print("=" * 70)
print("UNKNOWN CODES BY FREQUENCY")
print("=" * 70)
for c in unknown_codes:
    freq = pair_counts[c]
    pct = freq / total_pairs * 100
    print(f"  {c}: {freq} occurrences ({pct:.1f}%)")

print(f"\nTotal unknown codes: {len(unknown_codes)}")
print(f"Total unknown occurrences: {sum(pair_counts[c] for c in unknown_codes)} / {total_pairs}")

# For each unknown code, find its CONTEXT in the decoded text
# Look at what fixed letters appear before and after it
print(f"\n{'='*70}")
print("CONTEXT ANALYSIS FOR TOP 30 UNKNOWN CODES")
print("=" * 70)

# For each unknown code, collect (left_context, right_context) from fixed codes
for code in unknown_codes[:30]:
    left_letters = Counter()
    right_letters = Counter()
    # Also collect longer context windows
    contexts = []

    for pairs in book_pairs:
        for i, p in enumerate(pairs):
            if p != code:
                continue
            # Left context
            if i > 0 and pairs[i-1] in fixed:
                left_letters[fixed[pairs[i-1]]] += 1
            # Right context
            if i < len(pairs) - 1 and pairs[i+1] in fixed:
                right_letters[fixed[pairs[i+1]]] += 1

            # Wider context (3 on each side)
            ctx_parts = []
            for j in range(max(0, i-3), min(len(pairs), i+4)):
                if j == i:
                    ctx_parts.append(f'[{code}]')
                elif pairs[j] in fixed:
                    ctx_parts.append(fixed[pairs[j]])
                else:
                    ctx_parts.append('?')
            contexts.append(''.join(ctx_parts))

    freq = pair_counts[code]
    pct = freq / total_pairs * 100
    print(f"\n  Code {code} ({freq} occ, {pct:.1f}%):")

    # Show top left/right neighbors
    left_top = left_letters.most_common(6)
    right_top = right_letters.most_common(6)
    print(f"    Left:  {', '.join(f'{l}:{c}' for l, c in left_top)}")
    print(f"    Right: {', '.join(f'{l}:{c}' for l, c in right_top)}")

    # Show unique context samples
    unique_ctx = list(set(contexts))
    unique_ctx.sort(key=lambda x: -len(x.replace('?', '').replace('[', '').replace(']', '')))
    for ctx in unique_ctx[:8]:
        print(f"    ctx: {ctx}")

    # Score candidate letters based on German bigram expectations
    german_bigrams = {
        'EN': 3.88, 'ER': 3.75, 'CH': 2.75, 'DE': 2.00, 'EI': 1.88,
        'ND': 1.88, 'TE': 1.67, 'IN': 1.65, 'IE': 1.64, 'GE': 1.43,
        'ES': 1.36, 'NE': 1.26, 'SE': 1.20, 'RE': 1.18, 'HE': 1.16,
        'AN': 1.14, 'UN': 1.14, 'ST': 1.13, 'BE': 1.06, 'DI': 0.98,
        'EM': 0.93, 'AU': 0.93, 'SC': 0.86, 'DA': 0.86, 'SI': 0.82,
        'LE': 0.82, 'IC': 0.81, 'TI': 0.73, 'AL': 0.71, 'HA': 0.71,
        'NG': 0.67, 'WE': 0.65, 'EL': 0.65, 'HI': 0.58, 'NS': 0.57,
        'NT': 0.56, 'IS': 0.55, 'HT': 0.54, 'MI': 0.52, 'IT': 0.50,
        'RI': 0.41, 'AB': 0.38, 'LI': 0.35, 'ED': 0.35, 'EG': 0.34,
        'NI': 0.33, 'ET': 0.33, 'IG': 0.32, 'AR': 0.31, 'RU': 0.30,
        'LA': 0.29, 'BI': 0.27, 'FE': 0.26, 'ZU': 0.25, 'MA': 0.24,
        'OR': 0.23, 'WA': 0.22, 'SS': 0.22, 'RS': 0.21, 'RT': 0.20,
    }

    candidate_scores = Counter()
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        score = 0
        for left, count in left_letters.items():
            bg = left + letter
            if bg in german_bigrams:
                score += german_bigrams[bg] * count
        for right, count in right_letters.items():
            bg = letter + right
            if bg in german_bigrams:
                score += german_bigrams[bg] * count
        candidate_scores[letter] = score

    top_cands = candidate_scores.most_common(6)
    print(f"    Bigram candidates: {', '.join(f'{l}:{s:.1f}' for l, s in top_cands)}")


# Show decoded books with fixed codes only
print(f"\n{'='*70}")
print("DECODED BOOKS (fixed codes only, ? for unknowns)")
print("=" * 70)

book_decoded = []
for i, pairs in enumerate(book_pairs):
    decoded = decode_fixed(pairs)
    text = ''.join(decoded)
    book_decoded.append((i, decoded, text, len(pairs)))

book_decoded.sort(key=lambda x: -x[3])

for idx, decoded, text, length in book_decoded[:6]:
    print(f"\n  Book {idx} ({length} pairs):")
    # Print as continuous text, 80 chars wide
    flat = text
    for j in range(0, len(flat), 100):
        print(f"    {flat[j:j+100]}")


# Check: what percentage of the text is known vs unknown?
known_count = sum(1 for p in all_pairs_flat if p in fixed)
unknown_count = sum(1 for p in all_pairs_flat if p not in fixed)
print(f"\n  Known: {known_count}/{len(all_pairs_flat)} ({known_count/len(all_pairs_flat)*100:.1f}%)")
print(f"  Unknown: {unknown_count}/{len(all_pairs_flat)} ({unknown_count/len(all_pairs_flat)*100:.1f}%)")


# SPECIFIC ANALYSIS: Look for patterns around DIE_URALTE_STEINE
print(f"\n{'='*70}")
print("SENTENCES CONTAINING 'URALTE STEINE' (with unknowns shown)")
print("=" * 70)

# Find the STEIN pattern in each book
for idx, pairs in enumerate(book_pairs):
    # Find URALTESTEIN subsequence
    target = ['61', '51', '35', '34', '78', '01', '92', '88', '95', '21', '60']
    for i in range(len(pairs) - len(target)):
        if pairs[i:i+len(target)] == target:
            # Show wide context
            start = max(0, i - 15)
            end = min(len(pairs), i + len(target) + 15)
            ctx_pairs = pairs[start:end]
            ctx_decoded = decode_fixed(ctx_pairs)
            text = ''.join(ctx_decoded)
            pos_in_ctx = i - start
            print(f"\n  Book {idx}, pos {i}:")
            print(f"    {text}")
            # Also show the raw codes for unknowns
            code_str = ' '.join(f'{p}={fixed.get(p, "?")}' for p in ctx_pairs)
            print(f"    Codes: {code_str}")


# WORD BOUNDARY ANALYSIS
print(f"\n{'='*70}")
print("HIGH-FREQUENCY UNKNOWN CODES: REQUIRED LETTER ANALYSIS")
print("=" * 70)

# What letters are most needed?
german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
    'Q': 0.001
}

fixed_freq = Counter()
for p in all_pairs_flat:
    if p in fixed:
        fixed_freq[fixed[p]] += 1

print("\nLetter deficit analysis (how much more freq each letter needs):")
for letter in sorted(german_freq, key=lambda l: -german_freq[l]):
    fixed_pct = fixed_freq[letter] / total_pairs * 100
    exp_pct = german_freq[letter] * 100
    deficit = exp_pct - fixed_pct
    n_codes = sum(1 for c in fixed if fixed[c] == letter)
    # Estimate how many more codes needed
    unknown_total = sum(pair_counts[c] for c in unknown_codes)
    if deficit > 0:
        codes_needed = deficit / 100 * total_pairs
        avg_unknown_freq = unknown_total / len(unknown_codes) if unknown_codes else 1
        est_codes = codes_needed / avg_unknown_freq
        print(f"  {letter}: {fixed_pct:.1f}% fixed ({n_codes} codes), exp {exp_pct:.1f}%, deficit {deficit:.1f}%, ~{est_codes:.0f} more codes needed")


print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
