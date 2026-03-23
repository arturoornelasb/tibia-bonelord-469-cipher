#!/usr/bin/env python3
"""Session 10l: Deep code-level attack on key sequences"""

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

rev_map = defaultdict(list)
for code, letter in mapping.items():
    rev_map[letter].append(code)

all_col = [(i, collapse(decode(b))) for i, b in enumerate(books)]

print("=" * 80)
print("SESSION 10l: DEEP CODE-LEVEL ATTACK")
print("=" * 80)

# 1. FINDENTEIGNDASESDERSTE - complete code analysis
print("\n1. FINDENTEIGNDASESDERSTE CODE-BY-CODE")
print("-" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'FINDENTEIGNDASESDERSTE' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if 'FINDENT' in collapse(decoded[ri:ri+12]):
                # Get enough codes to cover the full sequence
                codes = book[ri:ri+30]
                letters = [mapping.get(c, '?') for c in codes]
                raw = decoded[ri:ri+30]
                print(f"  B{bi:02d}:")
                print(f"    Codes:   {' '.join(codes)}")
                print(f"    Letters: {' '.join(letters)}")
                print(f"    Raw:     {raw}")
                print(f"    Collapsed: {collapse(raw)}")
                print()
                break
        break

# Show all instances with their variant endings
print("  All instances of FINDENTE...:")
for bi, col in all_col:
    if 'FINDENTE' in col:
        pos = col.index('FINDENTE')
        end = min(len(col), pos+40)
        ctx = col[pos:end]
        print(f"    B{bi:02d}: {ctx}")

# 2. Segmentation hypotheses for FINDENTEIGNDASESDERSTE
print("\n" + "=" * 60)
print("2. SEGMENTATION HYPOTHESES")
print("=" * 60)

# The sequence is: F-I-N-D-E-N-T-E-I-G-N-D-A-S-E-S-D-E-R-S-T-E-I-E-N-G-E-H-H-I
# Possible readings:
hypotheses = [
    ("FINDEN T EIGN DAS ES DER STE IEN GEH HI",
     "find T own/EIGEN that it the STE IEN go HI"),
    ("FINDEN TE IGN DAS ES DER STEIEN GEH HI",
     "find TE ? that it the STEIEN go HI"),
    ("FINDEN TEIGN DAS ES DER STE IENGE HHI",
     "find TEIGN that it the STE IENGE HHI"),
    ("FINDEN TEIGND AS ES DERSTE IENGE HHI",
     "find TEIGND out-of it DERSTE IENGE HHI"),
    ("FINDEN T EIGEN DAS ES DER ERSTE IEN GEH HI",
     "find T own that it the first IEN go HI"),
]

for seg, trans in hypotheses:
    print(f"\n  {seg}")
    print(f"  = {trans}")

# KEY HYPOTHESIS: DER ERSTE = "the first"?
# If "DERSTE" = "DER STE" with STE = beginning of STEHEN?
# OR: "DERSTE" = "DER ERSTE" with E absorbed?
# Check: does DERSTE always appear or could it be DER-STE or D-ERSTE?
print("\n  Testing DER ERSTE hypothesis:")
for bi, col in all_col:
    if 'DERSTE' in col:
        pos = col.index('DERSTE')
        start = max(0, pos-5)
        end = min(len(col), pos+20)
        ctx = col[start:end]
        print(f"    B{bi:02d}: ...{ctx}...")

# 3. IENGE / IENGEHHI analysis
print("\n" + "=" * 60)
print("3. IENGE / IENGEHHI ANALYSIS")
print("=" * 60)

# IENGEHHI could be:
# IEN + GEH + HI = ? + go + here
# or: I + ENGE + HHI = ? + narrowness + ?
# GEH = go (imperative of gehen)
# HI = here? hither?

for bi, col in all_col:
    if 'IENGEHI' in col or 'IENGEHH' in col or 'IENGEH' in col:
        pos = col.index('IENGEH')
        start = max(0, pos-10)
        end = min(len(col), pos+20)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")
        if bi > 40:
            break

# Check what follows IENGEHHI
print("\n  What follows IENGEHHI:")
for bi, col in all_col:
    if 'IENGEHI' in col or 'IENGEHH' in col:
        for pattern in ['IENGEHHI', 'IENGEHHEI', 'IENGEHI']:
            if pattern in col:
                pos = col.index(pattern)
                end = min(len(col), pos+30)
                after = col[pos:end]
                print(f"    B{bi:02d}: {after}")
                break

# 4. The ENDENTE / ENDENTT pattern
print("\n" + "=" * 60)
print("4. ENDENTE / ENDENTT PATTERN")
print("=" * 60)

# "ERDENGEENDENTENTTUIGAAERGEIGETES"
# Could be: ERDE + NGE + ENDE + NTE + NTT + UIGAA + ER + GEIGET + ES
# Or: ER + DENGE + ENDEN + TE + NTT + UIGAA + ER + GEIGET + ES
# NGE could be a suffix (-unge = -ung in MHG)
# ENDEN = to end (verb)

for bi, col in all_col:
    if 'ENDENTE' in col:
        pos = col.index('ENDENTE')
        start = max(0, pos-15)
        end = min(len(col), pos+30)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")
        if bi > 40:
            break

# Raw code analysis for ERDENGEEN...
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'ERDENGEENDE' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if collapse(decoded[ri:ri+20]).startswith('ERDENGEENDE'):
                codes = book[ri:ri+20]
                letters = [mapping.get(c, '?') for c in codes]
                print(f"\n  B{bi:02d} codes: {' '.join(codes)}")
                print(f"  B{bi:02d} raw:   {''.join(letters)}")
                break
        break

# 5. TUIGAA analysis
print("\n" + "=" * 60)
print("5. TUIGAA CODE ANALYSIS")
print("=" * 60)

# Codes: 64(T) 61(U) 21(I) 97(G) 85(A) 85(A)
# After collapsing AA -> A, TUIGAA -> TUIGA
# But in context it's TUIGAA (doubled A)
# Could this be: TUI + GA + A? Or T + UIGA + A?
# What if code 85 is NOT A? It's an unconfirmed A code.
# Code 85 appears twice consecutively - suspicious

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'TUIGA' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if 'TUIGAA' in decoded[ri:ri+10]:
                codes = book[ri:ri+6]
                letters = [mapping.get(c, '?') for c in codes]
                print(f"  B{bi:02d}: codes {' '.join(codes)} = {''.join(letters)}")
                print(f"         raw: {decoded[ri:ri+10]}")
                break
        break

# Check code 85 in other contexts
print("\n  Code 85 (currently=A) in ALL contexts:")
c85_contexts = []
for bi, book in enumerate(books):
    for ci, c in enumerate(book):
        if c == '85':
            start = max(0, ci-3)
            end = min(len(book), ci+4)
            ctx_codes = book[start:end]
            ctx_letters = ''.join(mapping.get(x, '?') for x in ctx_codes)
            c85_contexts.append((bi, ctx_letters, ci-start))

# Show unique contexts
seen = set()
for bi, ctx, pos in c85_contexts:
    if ctx not in seen:
        seen.add(ctx)
        marked = ctx[:pos] + '[' + ctx[pos] + ']' + ctx[pos+1:]
        print(f"    B{bi:02d}: {marked}")

# 6. Code 86 - is it E or H?
print("\n" + "=" * 60)
print("6. CODE 86 (E or H?) ANALYSIS")
print("=" * 60)

# If IEM = IHM, code 86 would be H not E
# Check all contexts of code 86

print("  Code 86 contexts (currently = E):")
print("  If E:          If H:")
c86_count = 0
for bi, book in enumerate(books):
    for ci, c in enumerate(book):
        if c == '86':
            start = max(0, ci-3)
            end = min(len(book), ci+4)
            ctx_codes = book[start:end]
            ctx_e = ''.join(mapping.get(x, '?') for x in ctx_codes)
            # Test with H instead
            ctx_h = ''
            for i, x in enumerate(ctx_codes):
                if i == (ci - start):
                    ctx_h += 'H'
                else:
                    ctx_h += mapping.get(x, '?')
            col_e = collapse(ctx_e)
            col_h = collapse(ctx_h)
            print(f"    B{bi:02d}: {col_e:12s} -> {col_h}")
            c86_count += 1
            if c86_count >= 15:
                break
    if c86_count >= 15:
        break

# 7. What about the IEM -> IHM hypothesis?
print("\n" + "=" * 60)
print("7. IEM -> IHM FULL TEST")
print("=" * 60)

# IEM appears as "UND IEM IN HEDEMI"
# If IHM: "und ihm in HEDEMI" = "and to him in HEDEMI" - grammatically perfect!
# Code 86 -> H would change other occurrences too

# Count code 86 total occurrences
c86_total = sum(book.count('86') for book in books)
print(f"  Code 86 total occurrences: {c86_total}")

# Check: if code 86 = H, what effect on known words?
# We need to verify no known word uses code 86 as E
for word in ['STEIN', 'RUNE', 'ERDE', 'FINDEN', 'DIESER', 'ENDE', 'REDE',
             'SEIDE', 'GEIGET', 'URALTE', 'KOENIG', 'KELSEI']:
    for bi, book in enumerate(books):
        col = collapse(decode(book))
        if word in col:
            decoded = decode(book)
            for ri in range(len(decoded)):
                if collapse(decoded[ri:ri+len(word)*2]).startswith(word):
                    codes = book[ri:ri+len(word)]
                    if '86' in codes:
                        print(f"  WARNING: {word} uses code 86 at position "
                              f"{codes.index('86')} in B{bi:02d}")
                    break
            break

print("\n  Code 86 -> H appears SAFE if no warnings above")

# 8. Can we identify more words if code 86 = H?
print("\n" + "=" * 60)
print("8. TEXT WITH CODE 86 = H")
print("=" * 60)

# Create modified mapping
mod_mapping = dict(mapping)
mod_mapping['86'] = 'H'

# Decode longest book with modified mapping
for i, book in enumerate(books):
    decoded = ''.join(mod_mapping.get(c, '?') for c in book)
    col = collapse(decoded)
    if len(col) > 130:
        print(f"  B{i:02d} original:  {collapse(decode(book))[:80]}")
        print(f"  B{i:02d} with 86=H: {col[:80]}")
        # Find differences
        orig = collapse(decode(book))
        diffs = []
        for j in range(min(len(orig), len(col))):
            if j < len(orig) and j < len(col) and orig[j] != col[j]:
                diffs.append((j, orig[j], col[j]))
        if diffs:
            print(f"  Changes: {diffs[:10]}")
        print()
        break

# Show IEM -> IHM specifically
for bi, book in enumerate(books):
    col_orig = collapse(decode(book))
    col_mod = collapse(''.join(mod_mapping.get(c, '?') for c in book))
    if 'IEM' in col_orig and 'IHM' in col_mod:
        pos = col_mod.index('IHM')
        start = max(0, pos-15)
        end = min(len(col_mod), pos+20)
        print(f"  B{bi:02d} IEM->IHM: ...{col_mod[start:end]}...")
        break

# 9. Check HIET -> if code 86=H affects it
print("\n" + "=" * 60)
print("9. HIET with 86=H")
print("=" * 60)

# HIET codes: 00(H) 65(I) 86(E) 75(T)
# If 86=H: HIET -> HIHT - doesn't make sense
# So 86=H might conflict with HIET

# But HIET only appears once (B35)
# Check if HIET is actually a word or artifact
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'HIET' in col:
        pos = col.index('HIET')
        start = max(0, pos-15)
        end = min(len(col), pos+20)
        print(f"  B{bi:02d}: ...{col[start:end]}...")
        # Show with 86=H
        col_mod = collapse(''.join(mod_mapping.get(c, '?') for c in book))
        if 'HIHT' in col_mod:
            pos2 = col_mod.index('HIHT')
            start2 = max(0, pos2-15)
            end2 = min(len(col_mod), pos2+20)
            print(f"  B{bi:02d} 86=H: ...{col_mod[start2:end2]}...")
        else:
            # Position might differ
            print(f"  B{bi:02d} 86=H: HIET pattern gone")
            # Check broader context
            decoded_mod = ''.join(mod_mapping.get(c, '?') for c in book)
            col_m = collapse(decoded_mod)
            # Find the same area
            if 'INHIET' in col:
                for p in range(max(0, pos-5), min(len(col_m), pos+5)):
                    if p < len(col_m):
                        pass
                nearby = col_m[max(0,pos-10):min(len(col_m),pos+15)]
                print(f"  B{bi:02d} nearby: ...{nearby}...")

# 10. Check: does HIET use code 86?
print("\n  HIET code check:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'HIET' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if collapse(decoded[ri:ri+8]).startswith('HIET'):
                codes = book[ri:ri+4]
                print(f"    B{bi:02d}: codes {' '.join(codes)} = "
                      f"{''.join(mapping.get(c,'?') for c in codes)}")
                if '86' in codes:
                    print(f"    ** Code 86 IS used in HIET! **")
                    print(f"    If 86=H: {' '.join(codes)} -> "
                          f"{''.join(mod_mapping.get(c,'?') for c in codes)}")
                break

# 11. Alternative: test code 86 in VMTEGE context
print("\n" + "=" * 60)
print("11. CODE 86 IN VMTEGE")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'VMTEGE' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if collapse(decoded[ri:ri+10]).startswith('VMTEGE'):
                codes = book[ri:ri+6]
                has_86 = '86' in codes
                print(f"  B{bi:02d}: codes {' '.join(codes)} "
                      f"{'** HAS 86 **' if has_86 else ''}")
                break
        if bi > 30:
            break

print("\n" + "=" * 80)
print("SESSION 10l COMPLETE")
print("=" * 80)
