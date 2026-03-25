#!/usr/bin/env python3
"""Session 10n: Attack top unknown segments, raw text analysis"""

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

all_col = [(i, collapse(decode(b))) for i, b in enumerate(books)]

print("=" * 80)
print("SESSION 10n: ATTACK UNKNOWN SEGMENTS")
print("=" * 80)

# 1. OWI (7x) - full context analysis
print("\n1. OWI ANALYSIS (7x)")
print("-" * 60)

for bi, col in all_col:
    if 'OWI' in col:
        pos = col.index('OWI')
        start = max(0, pos-15)
        end = min(len(col), pos+15)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# OWI raw codes
print("\n  OWI code check:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'OWI' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if collapse(decoded[ri:ri+6]).startswith('OWI'):
                codes = book[ri:ri+3]
                letters = [mapping.get(c,'?') for c in codes]
                print(f"    B{bi:02d}: {' '.join(codes)} = {''.join(letters)}")
                # also show wider context raw
                wider = book[max(0,ri-3):ri+6]
                wletters = ''.join(mapping.get(c,'?') for c in wider)
                print(f"           context: {wletters}")
                break
        break

# Could OWI be OWI=? In MHG: OWIE = oh woe?
# Or is it part of a larger word?
# Context: "SEIN NDGE DAS IEO WI RUNE"
# Wait - what if the segmentation is wrong?
# "DASIEOWIRUNE" = DAS IE O WI RUNE? Or DAS IEO WIR UNE?
# IEO could be IEO = a name? Or I + EO?
# WIR = we! "DAS WIR RUNE" = "that we rune"?

print("\n  Re-segmentation tests:")
print("    DASIEOWIRUNEAUIEN = DAS IE O WIR UNE AUIEN")
print("    DASIEOWIRUNEAUIEN = DAS IEO WIR UNE AU IEN")
print("    DASIEOWIRUNEAUIEN = DA SIE OWI RUNE AUIEN")
print("    DA SIE = 'then she' / 'there she'")

# 2. DGEDA (6x) - full analysis
print("\n" + "=" * 60)
print("2. DGEDA ANALYSIS (6x)")
print("=" * 60)

for bi, col in all_col:
    if 'DGEDA' in col:
        pos = col.index('DGEDA')
        start = max(0, pos-15)
        end = min(len(col), pos+15)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")
        if bi > 40:
            break

# Raw codes
print("\n  DGEDA codes:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'DGEDA' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if collapse(decoded[ri:ri+10]).startswith('DGEDA'):
                codes = book[ri:ri+5]
                raw = decoded[ri:ri+8]
                print(f"    B{bi:02d}: codes {' '.join(codes)} raw={raw}")
                break
        break

# 3. SCE (6x) - "ER SCE AUS"
print("\n" + "=" * 60)
print("3. SCE / ERSCE ANALYSIS (6x)")
print("=" * 60)

for bi, col in all_col:
    if 'RSCE' in col or 'SCEA' in col:
        for pattern in ['RSCE', 'SCEA']:
            if pattern in col:
                pos = col.index(pattern)
                start = max(0, pos-12)
                end = min(len(col), pos+15)
                ctx = col[start:end]
                print(f"  B{bi:02d}: ...{ctx}...")
                break
        if bi > 40:
            break

# What if it's ER-SCE or ERS-CE?
# ERSCHEINEN (to appear) = ER-SCHEIN-EN
# But SCE is not SCHEIN
# VERSCHWINDEN = disappear
# GESCHEHEN = happen -> GESCHEN in MHG
# What about BESCHEID = information?
# ER SCE AUS = "he ??? from/out"
# AUSSCHEIDEN = to separate/excrete?
# REISE (journey)?

# Check raw codes for SCE
print("\n  SCE raw codes:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'ERSCEAUS' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if 'ERSCEAUS' in collapse(decoded[ri:ri+12]):
                codes = book[ri:ri+8]
                raw = decoded[ri:ri+10]
                print(f"    B{bi:02d}: codes {' '.join(codes)}")
                print(f"           raw={raw}")
                break
        break

# 4. CHN (7x) - "IN CHN ES"
print("\n" + "=" * 60)
print("4. CHN ANALYSIS (7x)")
print("=" * 60)

# CHN always in: "GEIGET ES IN CHN ES R ER SCE AUS"
# So: "he shows it in CHN"
# CHN could be a place name (3-letter abbreviation?)
# Or: CH + N where N starts the next word?
# GEIGET ES IN CH NES RER SCE AUS = "shows it in CH NES..."
# NES = genitive suffix?

for bi, col in all_col:
    if 'CHN' in col:
        pos = col.index('CHN')
        start = max(0, pos-12)
        end = min(len(col), pos+15)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")
        if bi > 30:
            break

# 5. NTENTUIGA (5x) - from ENDENTENTUIGAA
print("\n" + "=" * 60)
print("5. NTENTUIGA ANALYSIS")
print("=" * 60)

# Full context: "ERDE NGE ENDE NTENTUIGA ER GEIGET ES"
# Or: "ERDENGEENDENTENTUIGAAERGEIGETES"
# Let's try: ERDE NGE ENDEN TENTUIGA ER GEIGET ES
# ENDEN = to end
# TENTUIGA = ?
# Or: ERDE NGE ENDENT ENTUIGA
# Or: ERDENGE ENDENTE NTUIGA
# NTUIGA doesn't look German

# What if TUIGA is a proper noun?
# Or: TUI + GA + A = ?
# In Tibia: Tuiga? Not a known place

# Raw code analysis
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'TUIGA' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if 'TUIG' in decoded[ri:ri+6]:
                codes = book[ri:ri+6]
                raw = decoded[ri:ri+8]
                print(f"  B{bi:02d}: codes {' '.join(codes)}")
                print(f"         raw={raw}")
                break
        break

# 6. TEMDIA (5x)
print("\n" + "=" * 60)
print("6. TEMDIA ANALYSIS (5x)")
print("=" * 60)

for bi, col in all_col:
    if 'TEMDIA' in col:
        pos = col.index('TEMDIA')
        start = max(0, pos-15)
        end = min(len(col), pos+15)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# 7. UISEMIV (5x)
print("\n" + "=" * 60)
print("7. UISEMIV ANALYSIS (5x)")
print("=" * 60)

for bi, col in all_col:
    if 'UISEMIV' in col or 'ISEMIV' in col:
        for p in ['UISEMIV', 'ISEMIV']:
            if p in col:
                pos = col.index(p)
                start = max(0, pos-15)
                end = min(len(col), pos+15)
                ctx = col[start:end]
                print(f"  B{bi:02d}: ...{ctx}...")
                break

# Could UISEMIV contain WEISE (manner/way)?
# U + ISEMIV or UI + SEMIV?
# WEISEMIV with W->U substitution? No, W is a separate letter
# What about: UISE + MIV?
# Or reading backward: VIMESIU?

# 8. AMNEUD (3x)
print("\n" + "=" * 60)
print("8. AMNEUD ANALYSIS (3x)")
print("=" * 60)

for bi, col in all_col:
    if 'AMNEUD' in col:
        pos = col.index('AMNEUD')
        start = max(0, pos-15)
        end = min(len(col), pos+15)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# 9. RAW (pre-collapse) text analysis for doubles
print("\n" + "=" * 60)
print("9. RAW TEXT - GENUINE DOUBLES ANALYSIS")
print("=" * 60)

# Find cases where the raw text has doubled letters that use
# the SAME code (which would be unusual in homophonic cipher)
same_code_doubles = Counter()
diff_code_doubles = Counter()

for bi, book in enumerate(books):
    for ci in range(len(book)-1):
        if book[ci] == book[ci+1]:  # Same code used twice
            letter = mapping.get(book[ci], '?')
            same_code_doubles[letter] += 1
        elif mapping.get(book[ci], '?') == mapping.get(book[ci+1], '?'):
            # Different codes, same letter
            letter = mapping.get(book[ci], '?')
            diff_code_doubles[letter] += 1

print("  Same-code doubles (unusual - might be genuine doubles):")
for letter, count in same_code_doubles.most_common():
    if count > 0:
        print(f"    {letter}: {count}x same code used twice")

print("\n  Different-code doubles (expected - cipher alternation):")
for letter, count in diff_code_doubles.most_common(10):
    print(f"    {letter}: {count}x different codes for same letter")

# 10. Look for the same-code doubles in context
print("\n" + "=" * 60)
print("10. SAME-CODE DOUBLES IN CONTEXT")
print("=" * 60)

for bi, book in enumerate(books):
    for ci in range(len(book)-1):
        if book[ci] == book[ci+1]:
            code = book[ci]
            letter = mapping.get(code, '?')
            start = max(0, ci-3)
            end = min(len(book), ci+5)
            ctx_codes = book[start:end]
            ctx = ''.join(mapping.get(c, '?') for c in ctx_codes)
            col = collapse(ctx)
            pos = ci - start
            print(f"  B{bi:02d}: code {code}({letter}) doubled: "
                  f"{ctx} -> {col}")
    if bi > 10:
        break

# 11. The big unknown: OIAITOEMENDGEMKMTGRSCASEZSTEIEHIS
print("\n" + "=" * 60)
print("11. LONG GARBLED SEGMENT ANALYSIS")
print("=" * 60)

seg = 'OIAITOEMENDGEMKMTGRSCASEZSTEIEHIS'
print(f"  Segment: {seg} ({len(seg)} chars)")
print(f"  Contains: OI-AI-TOE-MEND-GEM-KMT-GR-SCA-SEZ-STEIE-HIS")
print(f"  Or: O-IAI-TOE-MEND-GE-MKM-TGR-SCA-SEZ-STEI-EHIS")
print()

# Try to find known words within
for w in ['STEIN', 'ERDE', 'RUNE', 'MEND', 'STEIE', 'STEI',
          'SEZ', 'SCA', 'ORT', 'IST', 'EIN', 'TOE', 'GEM']:
    if w in seg:
        pos = seg.index(w)
        print(f"  Found '{w}' at pos {pos}: ...{seg[max(0,pos-3):pos+len(w)+3]}...")

# MHG words that might be here:
# GEMEINDE = community
# GERICHT = court/judgment
# GESCHLECHT = lineage
# MEISTER = master
# OHEIM = uncle

# 12. Look for GEMEINDE in text
print("\n" + "=" * 60)
print("12. GEMEINDE / GERICHT / GEME SEARCH")
print("=" * 60)

for pattern in ['GEMEIN', 'GERICHT', 'GEME', 'MEIND', 'RICHT']:
    found = False
    for bi, col in all_col:
        if pattern in col:
            pos = col.index(pattern)
            start = max(0, pos-8)
            end = min(len(col), pos+len(pattern)+8)
            ctx = col[start:end]
            print(f"  {pattern} in B{bi:02d}: ...{ctx}...")
            found = True
            break
    if not found:
        print(f"  {pattern}: not found")

# 13. What is ENGCHD?
print("\n" + "=" * 60)
print("13. ENGCHD DEEP ANALYSIS")
print("=" * 60)

# ENGCHD = E-N-G-C-H-D
# In German: ENG = narrow, ENGEL = angel
# Could ENGCHD be: ENG + CHD?
# CH is a digraph: so ENG-CH-D
# Could it be a truncation of ENGACHT (narrowed)?
# Or ENGE + CHD?
# What about: if we read ORTENGCHD as ORT-ENG-CHD?
# Or: ORT + ENGCHD (place ENGCHD)
# ENGCHD could be a proper noun = a place name

# Compare with TIUMENGEMI ORT ENGCHD
# TIUMENGEMI = community? + ORT = place + ENGCHD = ?
# So: "community-place ENGCHD"
# This describes a specific location

print("  TIUMENGEMI ORT ENGCHD contexts:")
for bi, col in all_col:
    if 'ORTENGCHD' in col:
        pos = col.index('ORTENGCHD')
        start = max(0, pos-20)
        end = min(len(col), pos+20)
        ctx = col[start:end]
        print(f"    B{bi:02d}: ...{ctx}...")

print("\n  ENGCHD likely = proper noun (place name)")
print("  Full phrase: 'TIUMENGEMI ORT ENGCHD' = 'community place ENGCHD'")

print("\n" + "=" * 80)
print("SESSION 10n COMPLETE")
print("=" * 80)
