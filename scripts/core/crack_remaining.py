"""
Session 9 - Attack remaining unknown patterns.
Focus on the most frequent unresolved bracketed sequences.
"""
import json, re
from collections import Counter

with open('data/books.json') as f:
    raw_books = json.load(f)
with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)

# Parse raw digit strings into 2-digit code lists
def parse_codes(digit_str):
    return [digit_str[i:i+2] for i in range(0, len(digit_str), 2)]

books = [{'codes': parse_codes(b)} for b in raw_books]

# Build reverse map: letter -> list of codes
rev = {}
for code, letter in mapping.items():
    rev.setdefault(letter, []).append(code)

def decode_book(codes):
    """Decode a list of 2-digit codes using mapping v4."""
    return ''.join(mapping.get(c, '?') for c in codes)

def get_codes_for_text(book_codes, decoded, target):
    """Find the raw codes that produce a target substring in decoded text."""
    idx = decoded.find(target)
    if idx == -1:
        return None
    return book_codes[idx:idx+len(target)]

print("=" * 80)
print("ATTACK ON REMAINING UNKNOWNS")
print("=" * 80)

# ============================================================
# 1. Extract raw codes for STEHWRLGTNELNRHELUIRUNHWND
# ============================================================
print("\n1. RAW CODES FOR 'STEH...HWND' PATTERN")
print("-" * 60)

found_codes = []
for i, book in enumerate(books):
    codes = book['codes']
    decoded = decode_book(codes)
    idx = decoded.find("STEHW")
    if idx != -1 and "HWND" in decoded[idx:idx+40]:
        # Find the end of HWND
        hwnd_idx = decoded.find("HWND", idx)
        segment = decoded[idx:hwnd_idx+4]
        raw = codes[idx:hwnd_idx+4]
        found_codes.append((i, raw, segment))

seen = set()
for book_i, raw, variant in found_codes:
    key = '-'.join(raw[:15])
    if key not in seen:
        seen.add(key)
        print(f"  Book {book_i}: {variant}")
        print(f"    Codes: {'-'.join(raw)}")
        # Decode letter by letter with code numbers
        for j, c in enumerate(raw):
            letter = mapping.get(c, f'[{c}]')
            print(f"      pos {j:2d}: code {c:>2s} -> {letter}")
        print()

# ============================================================
# 2. What codes map to W? Could any be U instead?
# ============================================================
print(f"\n2. W vs U CODE ANALYSIS")
print("-" * 60)
print(f"  W codes: {rev.get('W', [])}")
print(f"  U codes: {rev.get('U', [])}")

# Count usage of each W code
for w_code in rev.get('W', []):
    count = sum(1 for b in books for c in b['codes'] if c == w_code)
    print(f"  Code {w_code} (W): {count} total uses")
    # Find contexts where this code appears
    contexts = []
    for i, book in enumerate(books):
        codes = book['codes']
        decoded = decode_book(codes)
        for pos, c in enumerate(codes):
            if c == w_code:
                ctx_start = max(0, pos-3)
                ctx_end = min(len(decoded), pos+4)
                ctx = decoded[ctx_start:ctx_end]
                marker = pos - ctx_start
                ctx_display = ctx[:marker] + f'[{ctx[marker]}]' + ctx[marker+1:]
                contexts.append(ctx_display)
    # Show first 10 unique contexts
    unique_ctx = list(dict.fromkeys(contexts))[:10]
    for ctx in unique_ctx:
        print(f"      ...{ctx}...")

# ============================================================
# 3. HWND analysis - every occurrence with context
# ============================================================
print(f"\n3. HWND - ALL OCCURRENCES WITH CONTEXT")
print("-" * 60)
hwnd_occ = []
for i, book in enumerate(books):
    codes = book['codes']
    decoded = decode_book(codes)
    for m in re.finditer('HWND', decoded):
        pos = m.start()
        ctx_start = max(0, pos-8)
        ctx_end = min(len(decoded), pos+15)
        ctx = decoded[ctx_start:ctx_end]
        hwnd_codes = codes[pos:pos+4]
        hwnd_occ.append((i, ctx, hwnd_codes))

print(f"  Total HWND occurrences: {len(hwnd_occ)}")
for book_i, ctx, hw_codes in hwnd_occ[:15]:
    print(f"  Book {book_i:2d}: ...{ctx}...  codes={hw_codes}")

# What if HWND = HUND? Check the W code
if hwnd_occ:
    w_in_hwnd = hwnd_occ[0][2][1]  # The W code
    print(f"\n  The W in HWND is always code: {w_in_hwnd}")
    print(f"  Code {w_in_hwnd} is mapped to: {mapping.get(w_in_hwnd, '?')}")
    # If we changed it to U, what would happen elsewhere?
    # Count how many times code appears outside HWND
    total_uses = sum(1 for b in books for c in b['codes'] if c == w_in_hwnd)
    print(f"  Code {w_in_hwnd} total uses: {total_uses}")

# ============================================================
# 4. NDCE and CE patterns
# ============================================================
print(f"\n4. CE PATTERN - ALL CONTEXTS")
print("-" * 60)
ce_occ = []
for i, book in enumerate(books):
    codes = book['codes']
    decoded = decode_book(codes)
    for m in re.finditer('CE', decoded):
        pos = m.start()
        ctx_start = max(0, pos-8)
        ctx_end = min(len(decoded), pos+10)
        ce_occ.append((i, decoded[ctx_start:ctx_end], codes[pos:pos+2]))

ce_counter = Counter(c[1] for c in ce_occ)
print(f"  Total CE occurrences: {len(ce_occ)}")
print(f"  Unique contexts:")
for ctx, count in ce_counter.most_common(15):
    print(f"    x{count:2d}  ...{ctx}...")

# ============================================================
# 5. VMT pattern
# ============================================================
print(f"\n5. VMT PATTERN")
print("-" * 60)
vmt_occ = []
for i, book in enumerate(books):
    codes = book['codes']
    decoded = decode_book(codes)
    for m in re.finditer('VMT', decoded):
        pos = m.start()
        ctx_start = max(0, pos-5)
        ctx_end = min(len(decoded), pos+15)
        vmt_occ.append((i, decoded[ctx_start:ctx_end], codes[pos:pos+3]))

print(f"  Total VMT occurrences: {len(vmt_occ)}")
for book_i, ctx, vmt_codes in vmt_occ[:10]:
    print(f"  Book {book_i:2d}: ...{ctx}...  codes={vmt_codes}")

# ============================================================
# 6. OEL in context
# ============================================================
print(f"\n6. OEL IN CONTEXT")
print("-" * 60)
for i, book in enumerate(books):
    codes = book['codes']
    decoded = decode_book(codes)
    idx = decoded.find("OEL")
    if idx != -1:
        ctx_start = max(0, idx-15)
        ctx_end = min(len(decoded), idx+15)
        print(f"  Book {i}: ...{decoded[ctx_start:ctx_end]}...")
        print(f"    OEL codes: {codes[idx:idx+3]}")

# ============================================================
# 7. UONGETRASES vs AUNRSONGETRASES
# ============================================================
print(f"\n7. *ONGETRASES VARIANTS")
print("-" * 60)
for i, book in enumerate(books):
    codes = book['codes']
    decoded = decode_book(codes)
    idx = decoded.find("ONGETRASES")
    if idx != -1:
        ctx_start = max(0, idx-15)
        ctx_end = min(len(decoded), idx+10)
        print(f"  Book {i}: ...{decoded[ctx_start:ctx_end]}...")

# ============================================================
# 8. What German words could these unknowns be?
# ============================================================
print(f"\n8. CANDIDATE GERMAN WORDS FOR UNKNOWN SEGMENTS")
print("-" * 60)

# LHLADIZ - appears as "EIN LHLADIZ..."
print("  LHLADIZ (in 'EIN LHLADIZ...'):")
print("    - If L is wrong: could be BLADIZ? HLADIZ?")
print("    - LHLA + DIZ: HLADI = ? DIZ = ding (MHG)?")
print("    - Could be a proper noun (name of a place/person)")

# TUIG - appears in "EN TUIG"
print("  TUIG (in '...EN TUIG...'):")
print("    - ZEUG (stuff) if T=Z? But T is well-established")
print("    - TUG (virtue, MHG TUGEND)")

# LAUNRLRUNR
print("  LAUNRLRUNR (in 'ER LAUNRLRUNR NACH'):")
print("    - LAUN + R + LRUNR?")
print("    - LAUF + LAUF (run + run) with code errors?")

# Check collapsed versions
for pattern in ["LHLADIZ", "TUIG", "LAUNRLRUNR", "VMTG", "DHTNIURG"]:
    collapsed = []
    if pattern:
        collapsed.append(pattern[0])
        for c in pattern[1:]:
            if c != collapsed[-1]:
                collapsed.append(c)
    collapsed_str = ''.join(collapsed)
    if collapsed_str != pattern:
        print(f"  {pattern} collapsed = {collapsed_str}")

# ============================================================
# 9. Full code-by-code trace of longest piece
# ============================================================
print(f"\n9. BOOK 52 FULL CODE TRACE")
print("-" * 60)
codes = books[52]['codes']
decoded = decode_book(codes)
print(f"  Length: {len(codes)} codes")
print(f"  Decoded: {decoded}")
print(f"\n  Code-by-code:")
for j in range(0, len(codes), 12):
    chunk = codes[j:j+12]
    letters = [mapping.get(c, '?') for c in chunk]
    line1 = ' '.join(f'{c:>2s}' for c in chunk)
    line2 = ' '.join(f'{l:>2s}' for l in letters)
    print(f"    [{j:3d}] {line1}")
    print(f"          {line2}")

# ============================================================
# 10. Reversed text analysis (TOTNIURG = GRUINTOT)
# ============================================================
print(f"\n10. REVERSED PATTERNS CHECK")
print("-" * 60)
# Known: TOTNIURG reversed = GRUINTOT
# Are there other reversed words?
proper_nouns = ['LABGZERAS', 'AUNRSONGETRASES', 'TOTNIURG', 'HEARUCHTIGER',
                'TAUTR', 'EILCH', 'THARSC', 'SCHWITEIO', 'UTRUNR',
                'LABRRNI', 'HIHL', 'LHLADIZ', 'MINHEDDEM']

for noun in proper_nouns:
    rev_noun = noun[::-1]
    # Try to read reversed version
    collapsed_rev = [rev_noun[0]]
    for c in rev_noun[1:]:
        if c != collapsed_rev[-1]:
            collapsed_rev.append(c)
    collapsed_rev_str = ''.join(collapsed_rev)

    print(f"  {noun:20s} reversed = {rev_noun:20s} collapsed = {collapsed_rev_str}")

print("\n" + "=" * 80)
print("DONE")
print("=" * 80)
