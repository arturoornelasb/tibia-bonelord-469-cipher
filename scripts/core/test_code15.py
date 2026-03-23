"""
Session 9 - Deep test: Is code 15 actually F instead of I?
Code 15 has suspicious bigrams: IA (12x), IO (7x) -- very rare in German.
Changing to F creates AUF (x7) and FORT (x4).
"""
import json
from collections import Counter

with open('data/books.json') as f:
    raw_books = json.load(f)
with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]

books = [parse_codes(b) for b in raw_books]

rev = {}
for code, letter in mapping.items():
    rev.setdefault(letter, []).append(code)

def decode(codes):
    return ''.join(mapping.get(c, '?') for c in codes)

print("=" * 80)
print("DEEP TEST: CODE 15 = I vs F")
print("=" * 80)

# First: what codes currently map to F?
print(f"\nF codes in mapping: {rev.get('F', [])}")
print(f"B codes in mapping: {rev.get('B', [])}")

# Show every occurrence of code 15 with context
print(f"\nALL code 15 occurrences with 8-char context:")
print("-" * 60)

occurrences = []
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    for pos, c in enumerate(book_codes):
        if c == '15':
            ctx_start = max(0, pos-4)
            ctx_end = min(len(decoded), pos+5)
            ctx = decoded[ctx_start:ctx_end]
            marker_pos = pos - ctx_start
            # Show I highlighted
            display = ctx[:marker_pos] + '[' + ctx[marker_pos] + ']' + ctx[marker_pos+1:]
            occurrences.append((bi, pos, display, ctx))

# Group by 4-char context (2 before, code, 1 after)
context_groups = Counter()
for bi, pos, display, ctx in occurrences:
    decoded = decode(books[bi])
    before2 = decoded[max(0,pos-2):pos]
    after2 = decoded[pos+1:min(len(decoded),pos+3)]
    key = before2 + '_' + after2
    context_groups[key] += 1

print(f"\nTop contexts for code 15 (I):")
for ctx, cnt in context_groups.most_common(20):
    parts = ctx.split('_')
    before = parts[0]
    after = parts[1]
    # What would this be if 15=F?
    as_f = before + 'F' + after
    as_i = before + 'I' + after
    print(f"  x{cnt:2d}: {as_i:6s} (as F: {as_f:6s})")

# ============================================================
# Check if code 15 appears in any CONFIRMED German words
# ============================================================
print(f"\n{'='*60}")
print("CODE 15 IN CONFIRMED WORDS")
print(f"{'='*60}")

# Known confirmed word positions: DIE, DIES, DIESER
# Let's find where DIE appears and check which I code is used
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    # Find "DIE" in decoded
    for idx in range(len(decoded)-2):
        if decoded[idx:idx+3] == "DIE":
            d_code = book_codes[idx]
            i_code = book_codes[idx+1]
            e_code = book_codes[idx+2]
            # What follows?
            after = decoded[idx+3:idx+8] if idx+8 <= len(decoded) else decoded[idx+3:]
            # Only show if i_code is code 15
            if i_code == '15':
                print(f"  Book {bi}: DIE{after} -- I code = {i_code} (code 15!)")
                print(f"    Full: D({d_code}) I({i_code}) E({e_code}) {after}")
                break

# Check all "DI" occurrences - which I code follows D?
print(f"\nWhich I code follows D?")
d_then_i = Counter()
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    for pos in range(len(book_codes)-1):
        if decoded[pos] == 'D' and decoded[pos+1] == 'I':
            d_then_i[book_codes[pos+1]] += 1

for code, cnt in d_then_i.most_common():
    print(f"  D + code {code} (I): {cnt}x")

# If code 15 mostly appears after D, is it in DI-E or DI-something-else?
print(f"\nCode 15 after D -- what follows?")
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    for pos in range(len(book_codes)-2):
        if decoded[pos] == 'D' and book_codes[pos+1] == '15':
            after = decoded[pos+2:pos+6]
            print(f"  Book {bi} pos {pos}: D-[15]-{after} = D{decoded[pos+1]}{after}")

# ============================================================
# What would the full text look like with 15=F?
# ============================================================
print(f"\n{'='*60}")
print("SAMPLE TEXT WITH CODE 15 = F (first 5 books)")
print(f"{'='*60}")

for bi in range(min(5, len(books))):
    book_codes = books[bi]
    # Original
    orig = decode(book_codes)
    # Modified
    mod_chars = []
    for c in book_codes:
        if c == '15':
            mod_chars.append('F')
        else:
            mod_chars.append(mapping.get(c, '?'))
    modified = ''.join(mod_chars)

    # Show differences
    if orig != modified:
        print(f"\n  Book {bi}:")
        print(f"    ORIG: {orig}")
        print(f"    MOD:  {modified}")
        # Highlight changes
        diffs = [i for i in range(len(orig)) if orig[i] != modified[i]]
        if diffs:
            print(f"    Changes at positions: {diffs}")
            for d in diffs:
                ctx_s = max(0, d-5)
                ctx_e = min(len(modified), d+6)
                print(f"      pos {d}: ...{orig[ctx_s:ctx_e]}... -> ...{modified[ctx_s:ctx_e]}...")

# ============================================================
# If 15=F, check the impact on known proper nouns
# ============================================================
print(f"\n{'='*60}")
print("IMPACT ON PROPER NOUNS IF 15=F")
print(f"{'='*60}")

proper_nouns = ['AUNRSONGETRASES', 'TOTNIURG', 'HEARUCHTIGER', 'SCHWITEIO',
                'TAUTR', 'EILCH', 'THARSC', 'HIHL', 'LABRRNI', 'MINHEDDEM']
for noun in proper_nouns:
    # Check if code 15 produces any I in this noun
    for bi, book_codes in enumerate(books):
        decoded = decode(book_codes)
        idx = decoded.find(noun)
        if idx != -1:
            noun_codes = book_codes[idx:idx+len(noun)]
            if '15' in noun_codes:
                positions = [j for j, c in enumerate(noun_codes) if c == '15']
                print(f"  {noun}: code 15 at position(s) {positions}")
                modified_noun = list(noun)
                for p in positions:
                    modified_noun[p] = 'F'
                print(f"    Would become: {''.join(modified_noun)}")
            break

# ============================================================
# Also check code 50 (I, 36x) -- preceded by A(10x) and M(10x)
# ============================================================
print(f"\n{'='*60}")
print("CODE 50 ANALYSIS (I, 36x)")
print(f"{'='*60}")

print(f"\nCode 50 after A -- what follows?")
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    for pos in range(len(book_codes)-2):
        if decoded[pos] == 'A' and book_codes[pos+1] == '50':
            ctx_s = max(0, pos-3)
            ctx_e = min(len(decoded), pos+6)
            print(f"  Book {bi}: ...{decoded[ctx_s:ctx_e]}...")

print(f"\nAll code 50 contexts:")
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    for pos, c in enumerate(book_codes):
        if c == '50':
            ctx_s = max(0, pos-4)
            ctx_e = min(len(decoded), pos+5)
            ctx = decoded[ctx_s:ctx_e]
            marker = pos - ctx_s
            display = ctx[:marker] + '[' + ctx[marker] + ']' + ctx[marker+1:]
            print(f"  Book {bi} pos {pos:3d}: {display}")
    # Only show first few books
    if bi > 10:
        break

print("\n" + "=" * 80)
print("DONE")
print("=" * 80)
