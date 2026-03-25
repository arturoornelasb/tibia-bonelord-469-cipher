#!/usr/bin/env python3
"""Session 10k: Attack remaining fragments, code reassignment check, deep segmentation"""

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
    return re.sub(r'(.)\\1+', r'\\1', s)

# Build reverse mapping: letter -> codes
rev_map = defaultdict(list)
for code, letter in mapping.items():
    rev_map[letter].append(code)

all_col = [(i, collapse(decode(b))) for i, b in enumerate(books)]

print("=" * 80)
print("SESSION 10k: FRAGMENT ATTACK & CODE CONSISTENCY CHECK")
print("=" * 80)

# 1. STEINEN vs STEIN+ENT
print("\n1. STEINEN vs STEIN+ENT ANALYSIS")
print("-" * 60)

# In context: "DIE URALTE STEIN ENT ER ADTHARSC"
# Could be: STEINEN T ER = stones ? he
# Or: STEIN ENT ER = stone ENT he
# Check raw codes for STEINENTER
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'STEINENTER' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if collapse(decoded[ri:ri+16]).startswith('STEINENTER'):
                codes = book[ri:ri+10]
                letters = [mapping.get(c, '?') for c in codes]
                print(f"  B{bi:02d}: {' '.join(codes)}")
                print(f"       {'  '.join(letters)}")
                # Check where word boundaries might be
                print(f"       raw: {decoded[ri:ri+15]}")
                break
        break

# 2. Small unknown fragments: what are NHI, RUI, IEM, HIET, CHN, ENGCHD?
print("\n" + "=" * 60)
print("2. SMALL UNKNOWN FRAGMENTS")
print("=" * 60)

fragments = {
    'NHI': 'Appears at text start',
    'RUI': 'After SCHAUN ("behold RUI in...")',
    'IEM': 'After UND ("and IEM in HEDEMI")',
    'HIET': 'After IN ("in HIET the...")',
    'CHN': 'After IN ("shows it in CHN")',
    'ENGCHD': 'After ORT ("place ENGCHD")',
    'TUIGAA': 'In middle sequence',
    'TEIN': 'Between DIESER and EINER',
    'SCE': 'After ER ("he SCE from")',
    'NDGE': 'After SEIN ("his NDGE that")',
}

for frag, note in fragments.items():
    print(f"\n  {frag} - {note}:")
    contexts = []
    for bi, col in all_col:
        if frag in col:
            pos = col.index(frag)
            start = max(0, pos-10)
            end = min(len(col), pos+len(frag)+10)
            ctx = col[start:end]
            contexts.append((bi, ctx))

    print(f"    Found in {len(contexts)} books")
    for bi, ctx in contexts[:3]:
        print(f"    B{bi:02d}: ...{ctx}...")

    # Show raw codes for first occurrence
    if contexts:
        bi0 = contexts[0][0]
        book = books[bi0]
        col = collapse(decode(book))
        decoded = decode(book)
        pos_in_col = col.index(frag)
        # Map collapsed position to raw position
        for ri in range(len(decoded)):
            if collapse(decoded[ri:ri+len(frag)*3]).startswith(frag):
                codes = book[ri:ri+len(frag)]
                letters = [mapping.get(c, '?') for c in codes]
                print(f"    Codes: {' '.join(codes)} = {''.join(letters)}")
                break

# 3. Investigate IEM - could be IHM (him, dative)?
print("\n" + "=" * 60)
print("3. IEM -> IHM HYPOTHESIS")
print("=" * 60)

# If IEM = IHM, then we need I-H-M
# I codes: 15,16,21,46,50,65
# H codes: 08,17,23,57,68,74
# M codes: 44,54,55
# In IEM: I-E-M, but we need I-H-M
# The E in IEM might actually be H!
# Check: what code is used for the 'E' in IEM?

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'UNDIEM' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if 'UNDIEM' in collapse(decoded[ri:ri+10]):
                # Find exact position of IEM
                d = decoded[ri:ri+10]
                c = book[ri:ri+10]
                print(f"  B{bi:02d}: raw codes {' '.join(c[:8])}")
                print(f"       raw letters {''.join(mapping.get(x,'?') for x in c[:8])}")
                print(f"       raw decoded {d[:10]}")
                break
        break

# 4. NHI at start - could be a truncation artifact?
print("\n" + "=" * 60)
print("4. NHI START ANALYSIS")
print("=" * 60)

# NHI starts several books. What if it's the end of a word from overlap?
# Or: IN reversed = NI, but NHI has an H
# MHG NIH = nothing? NIHT = nicht (not)?
# What if NHI = truncated from a longer word?

for bi, col in all_col:
    if col.startswith('NHI') or 'SNHI' in col:
        print(f"  B{bi:02d}: {col[:30]}...")

# 5. ENGCHD analysis
print("\n" + "=" * 60)
print("5. ENGCHD / ORT ENGCHD ANALYSIS")
print("=" * 60)

# ORT ENGCHD - "place ENGCHD"
# ENGCHD could be: ENGEL (angel) with CH corruption?
# Or: ENG + CHD = narrow + ?
# In German: ENGEL = angel, ENG = narrow/tight
# Check if the G and C and H are always the same codes

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'ENGCHD' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if collapse(decoded[ri:ri+12]).startswith('ENGCHD'):
                codes = book[ri:ri+6]
                letters = [mapping.get(c, '?') for c in codes]
                print(f"  B{bi:02d}: codes {' '.join(codes)} = {''.join(letters)}")
                break
        break

# Multiple occurrences
engchd_codes = []
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'ENGCHD' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if collapse(decoded[ri:ri+12]).startswith('ENGCHD'):
                codes = book[ri:ri+6]
                engchd_codes.append((bi, codes))
                break

print(f"\n  ENGCHD in {len(engchd_codes)} books:")
for bi, codes in engchd_codes:
    print(f"    B{bi:02d}: {' '.join(codes)}")

# 6. The FINDENTEIGNDASESDERSTE sequence
print("\n" + "=" * 60)
print("6. FINDEN-TEIGN-DAS-ES-DER-STE ANALYSIS")
print("=" * 60)

# "HWND FINDEN TEIGN DAS ES DER STE IEN GEH"
# TEIGN = ? TEIG = dough? TEIGN = ?
# Actually: FINDEN + T + EIGN + DAS + ES + DER + STE + IEN + GEH
# EIGN = OWN (eigen)? FINDEN T EIGEN DAS ES DER STE...
# Wait: FINDEN + TEIGN or FINDENT + EIGN?
# FINDENT is not a word, but FINDEN + T is odd too
# What about: FINDEN TE IGN DAS ES DER STEIEN GEH HI
# Or: FINDEN TEIGNDASESDERSTEIENGEHHI

for bi, col in all_col:
    if 'FINDENTE' in col:
        pos = col.index('FINDENTE')
        end = min(len(col), pos+35)
        ctx = col[pos:end]
        print(f"  B{bi:02d}: {ctx}")

# Check raw codes
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'FINDENTE' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if collapse(decoded[ri:ri+20]).startswith('FINDENTE'):
                codes = book[ri:ri+15]
                letters = [mapping.get(c, '?') for c in codes]
                print(f"\n  B{bi:02d} codes: {' '.join(codes)}")
                print(f"  B{bi:02d} letters: {''.join(letters)}")
                print(f"  B{bi:02d} raw: {decoded[ri:ri+20]}")
                break
        break

# 7. SCHWITEIONE analysis
print("\n" + "=" * 60)
print("7. SCHWITEIONE ANALYSIS")
print("=" * 60)

# SCHWITEIONE could be:
# SCHWIT = ? + EIONE = ?
# SCHWEIGEN (silence) with corruption?
# GESCHWEIGE (let alone)?
# Or: S-CHWIT-EIONE
# MHG SWIGEN = to be silent?

for bi, col in all_col:
    if 'SCHWIT' in col:
        pos = col.index('SCHWIT')
        start = max(0, pos-15)
        end = min(len(col), pos+25)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# Code consistency
schwit_codes = []
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'SCHWITEIONE' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if collapse(decoded[ri:ri+20]).startswith('SCHWITEIONE'):
                codes = book[ri:ri+11]
                letters = [mapping.get(c, '?') for c in codes]
                schwit_codes.append((bi, codes, letters))
                break

print(f"\n  SCHWITEIONE in {len(schwit_codes)} books:")
for bi, codes, letters in schwit_codes:
    print(f"    B{bi:02d}: {' '.join(codes)} = {''.join(letters)}")

# 8. TIUMENGEMI analysis
print("\n" + "=" * 60)
print("8. TIUMENGEMI (community/gathering?) ANALYSIS")
print("=" * 60)

# Could be: TIUM + EN + GEMI
# GEMEINDE = community in modern German
# GIMEINDE/GIMEINIDA in OHG
# Could GEMI = reversed INGE? or part of GEMEINDE?
# Or: TIU + MENGEMI or TIUM + ENGEMI

for bi, col in all_col:
    if 'TIUMENGEMI' in col:
        pos = col.index('TIUMENGEMI')
        start = max(0, pos-15)
        end = min(len(col), pos+25)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# 9. KELSEI - MHG verb?
print("\n" + "=" * 60)
print("9. KELSEI ANALYSIS")
print("=" * 60)

# KELSEI could be:
# KELSE + I (?)
# Or a MHG verb form
# MHG KIESEN = to choose -> past: KOS, KURN
# MHG KELEN = to torture?
# Or: KEL + SEI = ? + be(subj)
# Actually: KELSEI DEN DNRHAUNRNVMHISDIZA RUNE
# "KELSEI the DNRHAUN... rune"
# Could KELSEI = imperativ? "Choose/pick the ... rune"?

for bi, col in all_col:
    if 'KELSEI' in col:
        pos = col.index('KELSEI')
        start = max(0, pos-15)
        end = min(len(col), pos+25)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# 10. What does the full STEIN-ENT-ER-ADTHARSC passage say?
print("\n" + "=" * 60)
print("10. FULL PASSAGE ANALYSIS: STEIN TO WISET")
print("=" * 60)

# "DIE URALTE STEIN ENT ER ADTHARSC IST SCHAUN RUI IN WISET"
# Multiple readings:
print("  READING 1: DIE URALTE STEIN ENT ER ADTHARSC IST SCHAUN RUI IN WISET")
print("    = The ancient stone, ENT he ADTHARSC, is to behold RUI in WISET")
print()
print("  READING 2: DIE URALTE STEINEN T ER ADTHARSC IST SCHAUN RU IN WISET")
print("    = The ancient stones ? he ADTHARSC, is to behold RU in WISET")
print()
print("  READING 3: DIE URALTE STEIN ENTER ADTHARSC IST SCHAUN RU IN WISET")
print("    = The ancient stone entered(?) ADTHARSC, is to behold RU in wisdom")
print()

# WISET = WISSET (know ye!) or WISSEN (knowledge)?
# RUI = RUHE (peace/rest)?
# Check if RUI has consistent codes
rui_codes = []
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'SCHAUNRUI' in col or 'SCHAUNRU' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            d = collapse(decoded[ri:ri+15])
            if d.startswith('SCHAUNRU'):
                codes = book[ri:ri+10]
                letters = [mapping.get(c, '?') for c in codes]
                rui_codes.append((bi, codes, letters, decoded[ri:ri+15]))
                break

print("\n  SCHAUN + RU/RUI code analysis:")
for bi, codes, letters, raw in rui_codes[:5]:
    print(f"    B{bi:02d}: {' '.join(codes)} = {''.join(letters)}")
    print(f"           raw: {raw}")

# 11. The 30 unconfirmed codes: frequency and context
print("\n" + "=" * 60)
print("11. UNCONFIRMED CODES: TOP SUSPECTS FOR REASSIGNMENT")
print("=" * 60)

# These codes have never appeared in a confirmed known word
# They might be correctly assigned OR might need reassignment
confirmed_in_words = set()
# Words that definitively confirm their constituent codes
confirmed_words = {
    'STEIN': None, 'RUNE': None, 'ERDE': None, 'KOENIG': None,
    'FINDEN': None, 'SCHAUN': None, 'URALTE': None, 'DIESER': None,
    'KLAR': None, 'GEIGET': None, 'SEIDE': None, 'STEH': None,
    'UNTER': None,
}

# For each confirmed word, find which codes it uses
for word in confirmed_words:
    for bi, book in enumerate(books):
        col = collapse(decode(book))
        if word in col:
            decoded = decode(book)
            for ri in range(len(decoded)):
                if collapse(decoded[ri:ri+len(word)*3]).startswith(word):
                    codes = book[ri:ri+len(word)]
                    for ci, code in enumerate(codes):
                        if mapping.get(code, '?') == word[ci]:
                            confirmed_in_words.add(code)
                    break
            break

all_codes = set(mapping.keys())
unconfirmed = all_codes - confirmed_in_words

print(f"\n  Total codes: {len(all_codes)}")
print(f"  Confirmed in words: {len(confirmed_in_words)}")
print(f"  Unconfirmed: {len(unconfirmed)}")

# Show unconfirmed codes by letter
unconf_by_letter = defaultdict(list)
for code in sorted(unconfirmed):
    letter = mapping[code]
    unconf_by_letter[letter].append(code)

print("\n  Unconfirmed codes by letter:")
for letter in sorted(unconf_by_letter.keys()):
    codes = unconf_by_letter[letter]
    # Count total occurrences
    total = 0
    for code in codes:
        for book in books:
            total += book.count(code)
    print(f"    {letter}: codes {', '.join(codes)} ({total} total occurrences)")

# 12. Test: what if some I codes are actually other letters?
print("\n" + "=" * 60)
print("12. I-CODE REASSIGNMENT TEST")
print("=" * 60)

# I has 6 codes but is at 10.5% (expected 7.6%)
# Maybe some I codes are actually P, J, or another missing letter?
i_codes = rev_map['I']  # 15,16,21,46,50,65
print(f"  I codes: {i_codes}")

# Check which I codes are confirmed
conf_i = [c for c in i_codes if c in confirmed_in_words]
unconf_i = [c for c in i_codes if c not in confirmed_in_words]
print(f"  Confirmed: {conf_i}")
print(f"  Unconfirmed: {unconf_i}")

# For each unconfirmed I code, show contexts
for code in unconf_i:
    print(f"\n  Code {code} (currently=I):")
    count = 0
    for bi, book in enumerate(books):
        for ci, c in enumerate(book):
            if c == code:
                start = max(0, ci-3)
                end = min(len(book), ci+4)
                ctx_codes = book[start:end]
                ctx_letters = [mapping.get(x, '?') for x in ctx_codes]
                pos_in = ci - start
                ctx_letters[pos_in] = f'[{ctx_letters[pos_in]}]'
                ctx = ''.join(ctx_letters)
                col_ctx = collapse(ctx)
                print(f"    B{bi:02d}: {''.join(ctx_letters)} -> {col_ctx}")
                count += 1
                if count >= 4:
                    break
        if count >= 4:
            break

# 13. Check W codes (also many)
print("\n" + "=" * 60)
print("13. W-CODE CHECK")
print("=" * 60)

w_codes = rev_map['W']
print(f"  W codes: {w_codes}")
conf_w = [c for c in w_codes if c in confirmed_in_words]
unconf_w = [c for c in w_codes if c not in confirmed_in_words]
print(f"  Confirmed: {conf_w}")
print(f"  Unconfirmed: {unconf_w}")

for code in unconf_w:
    print(f"\n  Code {code} (currently=W):")
    count = 0
    for bi, book in enumerate(books):
        for ci, c in enumerate(book):
            if c == code:
                start = max(0, ci-3)
                end = min(len(book), ci+4)
                ctx_codes = book[start:end]
                ctx_letters = [mapping.get(x, '?') for x in ctx_codes]
                pos_in = ci - start
                ctx_letters[pos_in] = f'[{ctx_letters[pos_in]}]'
                print(f"    B{bi:02d}: {''.join(ctx_letters)}")
                count += 1
                if count >= 4:
                    break
        if count >= 4:
            break

print("\n" + "=" * 80)
print("SESSION 10k COMPLETE")
print("=" * 80)
