#!/usr/bin/env python3
"""Session 10o: Genuine doubles, P search, deep re-segmentation"""

import json, re
from collections import Counter, defaultdict

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]
books = [parse_codes(b) for b in raw_books]
def decode(book):
    return ''.join(mapping.get(c, '?') for c in book)
def collapse(s):
    return re.sub(r'(.)\1+', r'\1', s)

rev_map = defaultdict(list)
for code, letter in mapping.items():
    rev_map[letter].append(code)

all_decoded = [(i, decode(b)) for i, b in enumerate(books)]
all_col = [(i, collapse(d)) for i, d in all_decoded]

print("=" * 80)
print("SESSION 10o: GENUINE DOUBLES + P SEARCH + DEEP SEGMENTATION")
print("=" * 80)

# 1. GENUINE DOUBLES ANALYSIS - word boundary clues
print("\n1. GENUINE DOUBLES AS WORD BOUNDARIES")
print("-" * 60)

# Same-code doubles mark real doubled letters or word boundaries
print("  Key same-code doubles and their interpretations:")
print()

# Find all same-code doubles with wider context
doubles_found = []
for bi, book in enumerate(books):
    decoded = decode(book)
    for ci in range(len(book)-1):
        if book[ci] == book[ci+1]:
            code = book[ci]
            letter = mapping.get(code, '?')
            # Get wide context (raw and collapsed)
            start = max(0, ci-5)
            end = min(len(book), ci+7)
            raw_ctx = decoded[start:end]
            col_ctx = collapse(raw_ctx)
            doubles_found.append((bi, ci, code, letter, raw_ctx, col_ctx))

# Group by collapsed context pattern
by_pattern = defaultdict(list)
for bi, ci, code, letter, raw, col in doubles_found:
    by_pattern[col].append((bi, ci, code, letter, raw))

print("  Unique doubled-letter contexts:")
for col_ctx, instances in sorted(by_pattern.items(), key=lambda x: -len(x[1])):
    if len(instances) >= 2:
        bi, ci, code, letter, raw = instances[0]
        print(f"    [{letter}{letter}] {raw} -> {col_ctx} ({len(instances)}x)")

# 2. GEH HIN hypothesis test
print("\n" + "=" * 60)
print("2. GEH HIN HYPOTHESIS (word boundary at double-H)")
print("=" * 60)

for bi, book in enumerate(books):
    decoded = decode(book)
    col = collapse(decoded)
    if 'GEHIH' in col or 'GEHI' in col:
        for ri in range(len(decoded)):
            test = decoded[ri:ri+10]
            if 'GEHH' in test:
                codes = book[ri:ri+10]
                letters = [mapping.get(c, '?') for c in codes]
                print(f"  B{bi:02d}: codes {' '.join(codes[:8])}")
                print(f"        raw:  {''.join(letters[:8])}")
                print(f"        If GEH+HIN: {''.join(letters[:3])} | {''.join(letters[3:6])} | {''.join(letters[6:8])}")
                break
        if bi > 30:
            break

# 3. WISET / WIISED analysis
print("\n" + "=" * 60)
print("3. WISET = WISET (MHG 'shows/guides')?")
print("=" * 60)

for bi, book in enumerate(books):
    decoded = decode(book)
    col = collapse(decoded)
    if 'WISET' in col:
        for ri in range(len(decoded)):
            if 'WIIS' in decoded[ri:ri+8] or 'WISE' in decoded[ri:ri+8]:
                codes = book[ri:ri+6]
                letters = [mapping.get(c, '?') for c in codes]
                raw = ''.join(letters)
                print(f"  B{bi:02d}: codes {' '.join(codes)} = {raw}")
                break
        break

# 4. OWI = MHG interjection "owi/ouwi" (alas!)
print("\n" + "=" * 60)
print("4. OWI = MHG 'OWI' (alas!, oh woe!)")
print("=" * 60)

# In MHG, "ouwi" or "owi" is an interjection of lament
# Context: "DA SIE OWI RUNE" = "there she [cries] alas! rune"
# Or: "DAS IE OWI RUNE" = "that the alas! rune"
# Better: "DA SIE OWI RUNE AU IEN ERDE NGE ENDE"
#       = "then she [cried] alas! rune on the earth end"

print("  OWI contexts with segmentation:")
for bi, col in all_col:
    if 'OWI' in col:
        pos = col.index('OWI')
        start = max(0, pos-20)
        end = min(len(col), pos+30)
        ctx = col[start:end]
        # Try segmentation
        seg = ctx
        for word in ['DIESER', 'FINDEN', 'SCHAUN', 'URALTE', 'KOENIG',
                     'STEIN', 'RUNE', 'ERDE', 'SEGEN', 'SEIN', 'EINE',
                     'DAS', 'DIE', 'DER', 'SIE', 'OWI', 'AUS', 'UND',
                     'ORT', 'MIT', 'VON', 'IST', 'EIN']:
            seg = seg.replace(word, f' {word} ')
        print(f"  B{bi:02d}: {ctx}")
        print(f"         {' '.join(seg.split())}")
        if bi > 40:
            break

# 5. Search for P among unconfirmed codes
print("\n" + "=" * 60)
print("5. SEARCH FOR LETTER P")
print("=" * 60)

# P should appear ~38 times. Which codes are unassigned or suspicious?
# First list all codes and their frequencies
all_codes = Counter()
for book in books:
    for c in book:
        all_codes[c] += 1

assigned_codes = set(mapping.keys())
all_used_codes = set()
for book in books:
    all_used_codes.update(book)

unassigned = all_used_codes - assigned_codes
print(f"  Codes in use but not in mapping: {sorted(unassigned)}")

# Check which mapped codes have low confidence
# Codes that appear in contexts where their assigned letter seems wrong
print("\n  Testing each assigned letter - could any be P?")
print("  Letters where German words often need P:")
print("    Common P-words in MHG: PFAD, PFLEGEN, PRIESTER, PRIS, PHLEGER")
print("    P often appears as PF in German (Pferd, Pflanze, etc)")

# Look for contexts that might contain P-words
# If P is missing, words with P would appear garbled
# PRIESTER -> ?RIESTER, PFLEGEN -> ?FLEGEN
for bi, col in all_col:
    for pattern in ['RIESTER', 'FLEGEN', 'FLEG', 'RIEST', 'FERD', 'FLANZ']:
        if pattern in col:
            pos = col.index(pattern)
            start = max(0, pos-5)
            end = min(len(col), pos+len(pattern)+5)
            ctx = col[start:end]
            print(f"  {pattern} in B{bi:02d}: ...{ctx}...")

# Alternative: P might be encoded by one of the codes currently mapped
# to another letter. Which letter has too many codes?
print("\n  Letter code counts:")
letter_codes = defaultdict(list)
for code, letter in mapping.items():
    letter_codes[letter].append(code)
for letter in sorted(letter_codes.keys()):
    codes = letter_codes[letter]
    total_freq = sum(all_codes.get(c, 0) for c in codes)
    print(f"    {letter}: {len(codes)} codes, {total_freq} total occurrences")

# Expected letter frequencies for German text
# (approximate percentages)
print("\n  Expected vs actual letter frequencies:")
expected_pct = {
    'E': 17.4, 'N': 9.8, 'I': 7.6, 'S': 7.3, 'R': 7.0, 'A': 6.5,
    'T': 6.2, 'D': 5.1, 'H': 4.8, 'U': 4.4, 'L': 3.4, 'C': 2.7,
    'G': 3.0, 'M': 2.5, 'O': 2.5, 'B': 1.9, 'W': 1.9, 'F': 1.7,
    'K': 1.2, 'Z': 1.1, 'V': 0.8, 'P': 0.8
}

total_chars = sum(len(book) for book in books)
for letter in sorted(letter_codes.keys()):
    codes = letter_codes[letter]
    actual = sum(all_codes.get(c, 0) for c in codes)
    actual_pct = actual * 100 / total_chars
    exp = expected_pct.get(letter, 0)
    diff = actual_pct - exp
    flag = "***" if abs(diff) > 2.0 else ""
    print(f"    {letter}: actual={actual_pct:.1f}% expected={exp:.1f}% diff={diff:+.1f}% {flag}")

# 6. Code frequency anomalies - overrepresented letters may contain P
print("\n" + "=" * 60)
print("6. OVERREPRESENTED LETTERS (may contain P codes)")
print("=" * 60)

# If P codes are misassigned to another letter, that letter will be overrepresented
# I is at 10.5% but expected 7.6% - could contain P?
# E, N, S, R could also be checked

# Test: for each I-code, check if changing to P makes better sense
for letter_to_test in ['I', 'E', 'N']:
    codes_for_letter = letter_codes.get(letter_to_test, [])
    if not codes_for_letter:
        continue
    print(f"\n  Testing {letter_to_test}-codes as potential P:")
    for code in codes_for_letter:
        freq = all_codes.get(code, 0)
        # Get contexts
        contexts = []
        for bi, book in enumerate(books):
            for ci, c in enumerate(book):
                if c == code:
                    start = max(0, ci-2)
                    end = min(len(book), ci+3)
                    ctx_codes = book[start:end]
                    ctx_e = ''.join(mapping.get(x, '?') for x in ctx_codes)
                    ctx_p = ''
                    for j, x in enumerate(ctx_codes):
                        if j == (ci - start):
                            ctx_p += 'P'
                        else:
                            ctx_p += mapping.get(x, '?')
                    contexts.append((bi, ctx_e, ctx_p))
                    if len(contexts) >= 3:
                        break
            if len(contexts) >= 3:
                break

        if contexts:
            print(f"    Code {code} ({freq}x): ", end="")
            ctx_strs = []
            for bi, ce, cp in contexts[:3]:
                ctx_strs.append(f"{ce}->{cp}")
            print(", ".join(ctx_strs))

# 7. NDGE analysis - suffix or word?
print("\n" + "=" * 60)
print("7. NDGE / NGE ANALYSIS")
print("=" * 60)

# NGE appears very frequently - could be -UNGE (MHG -ung suffix)
# NDGE = N + DGE? Or ND + GE? Or NDGE as unit?
for bi, col in all_col:
    if 'NGE' in col:
        # Find all NGE positions
        pos = 0
        while True:
            pos = col.find('NGE', pos)
            if pos == -1:
                break
            start = max(0, pos-8)
            end = min(len(col), pos+10)
            ctx = col[start:end]
            print(f"  B{bi:02d} pos {pos}: ...{ctx}...")
            pos += 1
        break  # Just first book for now

# Check raw codes for NGE
print("\n  NGE raw code patterns:")
nge_patterns = Counter()
for bi, book in enumerate(books):
    decoded = decode(book)
    col = collapse(decoded)
    pos = 0
    while True:
        pos = col.find('NGE', pos)
        if pos == -1:
            break
        # Find corresponding raw position
        raw_pos = 0
        col_pos = 0
        for ri in range(len(decoded)):
            if col_pos == pos:
                codes = book[ri:ri+3]
                pattern = '-'.join(codes)
                nge_patterns[pattern] += 1
                break
            if ri == 0 or decoded[ri] != decoded[ri-1]:
                col_pos += 1
        pos += 1

for pattern, count in nge_patterns.most_common(10):
    codes = pattern.split('-')
    letters = ''.join(mapping.get(c, '?') for c in codes)
    print(f"    {pattern} = {letters} ({count}x)")

# 8. Full raw text for longest book with word boundary markers
print("\n" + "=" * 60)
print("8. RAW DECODED TEXT - LONGEST BOOKS WITH DOUBLES MARKED")
print("=" * 60)

# Show raw text (not collapsed) with genuine doubles highlighted
pieces = {}
for i, text in all_col:
    is_sub = False
    for j, other in all_col:
        if i != j and text in other:
            is_sub = True
            break
    if not is_sub:
        pieces[i] = text

by_len = sorted(pieces.items(), key=lambda x: len(x[1]), reverse=True)

for idx, (bi, col_text) in enumerate(by_len[:3]):
    book = books[bi]
    decoded = decode(book)

    # Mark genuine doubles (same code used twice)
    marked = []
    for ci in range(len(decoded)):
        if ci > 0 and book[ci] == book[ci-1]:
            marked.append(decoded[ci].lower())  # lowercase = doubled
        else:
            marked.append(decoded[ci])

    print(f"\n  Book {bi} (raw with doubles in lowercase):")
    raw_marked = ''.join(marked)
    # Print in lines
    for i in range(0, len(raw_marked), 70):
        print(f"    {raw_marked[i:i+70]}")

# 9. TEMDIA deep dive
print("\n" + "=" * 60)
print("9. TEMDIA RAW CODE ANALYSIS")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'TEMDIA' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if 'TEMDI' in collapse(decoded[ri:ri+10]):
                codes = book[ri:ri+8]
                raw = decoded[ri:ri+10]
                letters = [mapping.get(c, '?') for c in codes]
                print(f"  B{bi:02d}: codes {' '.join(codes)}")
                print(f"        raw={raw}")
                print(f"        letters: {' '.join(letters)}")
                # Try P substitution for each code
                for j, c in enumerate(codes):
                    test = list(letters)
                    test[j] = 'P'
                    print(f"        P@{j}: {''.join(test)}")
                break
        break

# 10. UISEMIV deep dive
print("\n" + "=" * 60)
print("10. UISEMIV RAW CODE ANALYSIS")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'UISEMIV' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if 'UISEMI' in collapse(decoded[ri:ri+12]):
                codes = book[ri:ri+10]
                raw = decoded[ri:ri+12]
                letters = [mapping.get(c, '?') for c in codes]
                print(f"  B{bi:02d}: codes {' '.join(codes)}")
                print(f"        raw={raw}")
                print(f"        letters: {' '.join(letters)}")
                # Try P substitution
                for j, c in enumerate(codes[:8]):
                    test = list(letters[:8])
                    test[j] = 'P'
                    print(f"        P@{j}: {''.join(test)}")
                break
        break

# 11. HEDDEMI re-analysis with genuine double D
print("\n" + "=" * 60)
print("11. HEDDEMI - GENUINE DOUBLE D")
print("=" * 60)

# Code 45 = D, doubled in HEDDEMI
# Raw: H-E-D-D-E-M-I
# Could be: HED + DEMI, HEDD + EMI, HE + DDEMI
# In MHG: HEID(E) = heath, HEIDE
# With double D: could mark a word boundary

for bi, book in enumerate(books):
    decoded = decode(book)
    if 'HEDDEMI' in decoded:
        pos = decoded.index('HEDDEMI')
        start = max(0, pos-5)
        end = min(len(decoded), pos+15)
        codes = book[start//1:end//1]  # approximate
        raw = decoded[start:end]
        print(f"  B{bi:02d}: raw context = {raw}")

        # Find exact codes
        for ri in range(len(decoded)):
            if decoded[ri:ri+7] == 'HEDDEMI':
                hcodes = book[ri:ri+7]
                hletters = [mapping.get(c, '?') for c in hcodes]
                print(f"        codes: {' '.join(hcodes)}")
                print(f"        letters: {' '.join(hletters)}")
                # The DD are code 45 twice
                print(f"        HED | DEMI  (oath-place + half?)")
                print(f"        HEDD | EMI  (name?)")
                print(f"        HE | DDEMI  (he + dem + i?)")
                print(f"        HEIDE + MI with DD error?")
                break
        break

# 12. Cross-reference with Tibia lore
print("\n" + "=" * 60)
print("12. TIBIA LORE CROSS-REFERENCE")
print("=" * 60)

# Known Tibia locations that might appear in archaic German text:
# The books are in the Hellgate Library near Edron
# Bonelords/Beholders guard these books
# The text describes a quest/journey with RUNE, STEIN, GOLD, etc.

tibia_names = ['EDRON', 'THAIS', 'CARLIN', 'VENORE', 'DREFIA',
               'KAZORD', 'ANKRAH', 'DEMONA', 'FIBULA', 'MINTWA',
               'CYCLO', 'BONELORD', 'FERUMB', 'EXCALI', 'ORSHABAAL',
               'RASHID', 'DURIN', 'NORSEL', 'SENJA']

print("  Searching for Tibia-related names in decoded text:")
for name in tibia_names:
    for bi, col in all_col:
        if name in col:
            pos = col.index(name)
            start = max(0, pos-5)
            end = min(len(col), pos+len(name)+5)
            print(f"    Found {name} in B{bi:02d}: ...{col[start:end]}...")
            break

# Also check if unknown segments match Tibia names with substitution
print("\n  Unknown segments vs Tibia names:")
unknown_segs = ['ENGCHD', 'HEDDEMI', 'ADTHARSC', 'ADTHAUMR', 'TIUMENGEMI',
                'EILCHANHEARUCHTIG', 'EDETOTNIURGS', 'WRLGTNELNRHELUIRUNN',
                'KELSEI', 'LABGZERAS', 'LABRNI']
for seg in unknown_segs:
    print(f"    {seg}: ", end="")
    # Check if any Tibia name is a substring
    found = False
    for name in tibia_names:
        if name in seg or seg in name:
            print(f"matches {name}!")
            found = True
    if not found:
        # Check character overlap
        for name in tibia_names:
            overlap = sum(1 for c in name if c in seg) / len(name) if name else 0
            if overlap > 0.6:
                print(f"~{name} ({overlap:.0%} char overlap)", end=" ")
                found = True
        if not found:
            print("no match")
        else:
            print()

# 13. Updated narrative with all findings
print("\n" + "=" * 60)
print("13. UPDATED NARRATIVE READING")
print("=" * 60)

# Use the longest non-substring book
for bi, col_text in by_len[:1]:
    # Manual segmentation with all known words + new findings
    text = col_text

    # Mark known words
    words = [
        # Long words first
        'EILCHANHEARUCHTIG', 'EDETOTNIURGS', 'WRLGTNELNRHELUIRUNN',
        'TIUMENGEMI', 'SCHWITEIONE', 'ADTHARSC', 'ADTHAUMR',
        'LABGZERAS', 'ENGCHD', 'HEDEMI', 'HEDDEMI',
        'ODEGAREN', 'DIESER', 'FINDEN', 'SCHAUN', 'URALTE',
        'KOENIG', 'GEIGET', 'KELSEI', 'NORDEN',
        'SONNE', 'UNTER', 'NICHT', 'WERDE', 'STEIN', 'STEIEN',
        'DENEN', 'ERDE', 'VIEL', 'RUNE', 'STEH',
        'LIED', 'SEGEN', 'DORT', 'DENN', 'GOLD', 'MOND',
        'WELT', 'ENDE', 'REDE', 'HUND', 'SEIN', 'WIRD',
        'KLAR', 'ERST', 'AUCH', 'EINEN', 'EINER', 'SEINE',
        'TAUTR', 'HWND', 'WISET',
        'RUND', 'TAG', 'WEG', 'DER', 'DEN', 'DIE', 'DAS',
        'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON',
        'MIT', 'WIE', 'SEI', 'AUS', 'ORT', 'TUN', 'OWI',
        'NUR', 'SUN', 'TOT', 'GAR', 'ACH', 'ZUM',
        'HIN', 'HER', 'ALS', 'GEH',
        'ER', 'ES', 'IN', 'SO',
    ]

    # Simple greedy segmentation for display
    result = []
    i = 0
    while i < len(text):
        matched = False
        for w in words:
            if text[i:i+len(w)] == w:
                result.append(w)
                i += len(w)
                matched = True
                break
        if not matched:
            # Collect unknown chars
            unk = ''
            while i < len(text):
                found_word = False
                for w in words:
                    if text[i:i+len(w)] == w:
                        found_word = True
                        break
                if found_word:
                    break
                unk += text[i]
                i += 1
            result.append(f'[{unk}]')

    line = ' '.join(result)
    print(f"\n  Book {bi}:")
    for li in range(0, len(line), 75):
        print(f"    {line[li:li+75]}")

print("\n" + "=" * 80)
print("SESSION 10o COMPLETE")
print("=" * 80)
