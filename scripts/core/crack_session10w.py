#!/usr/bin/env python3
"""Session 10w: Raw code pattern analysis + phrase boundary attack"""

import json, re
from collections import Counter, defaultdict

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]
books = [parse_codes(b) for b in raw_books]
def decode(book, m=None):
    if m is None: m = mapping
    return ''.join(m.get(c, '?') for c in book)
def collapse(s):
    return re.sub(r'(.)\1+', r'\1', s)

all_codes = Counter()
for book in books:
    for c in book:
        all_codes[c] += 1

rev_map = defaultdict(list)
for code, letter in mapping.items():
    rev_map[letter].append(code)

print("=" * 80)
print("SESSION 10w: RAW CODE PATTERNS + PHRASE BOUNDARIES")
print("=" * 80)

# Strategy: Look at the FULL phrase "SEIGEVMTWIETUNRTAGRSIC"
# which appears in 7 books identically. The codes must be consistent.
# Let's extract the COMPLETE raw code sequence for this phrase.

print("\n1. FULL PHRASE: SEIGEVMTWIETUNRTAGRSIC")
print("-" * 60)

target_phrase = 'SEIGEVMTWIETUN'
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if target_phrase in col:
        idx = col.index(target_phrase)
        # Find raw position
        decoded = decode(book)
        for ri in range(len(decoded)):
            sub = decoded[ri:ri+40]
            if collapse(sub).startswith(target_phrase):
                # Get extended context
                end_ri = ri + 30
                raw_codes = book[ri:min(end_ri, len(book))]
                raw_text = decode(book[ri:min(end_ri, len(book))])
                col_text = collapse(raw_text)
                code_str = '-'.join(raw_codes)
                letter_str = '-'.join(f"{c}({mapping.get(c,'?')})" for c in raw_codes)
                print(f"  B{bi:02d}: {col_text}")
                print(f"    Codes: {code_str}")
                print(f"    Detail: {letter_str}")
                break
        break  # one example

# 2. Analyze the phrase segments
print("\n\n2. PHRASE SEGMENT ANALYSIS")
print("-" * 60)
print("  Known words in phrase:")
print("    SEI = be (imperative)")
print("    WIE = how/as")
print("    TUN = do")
print("    TAG = day")
print()
print("  Unknown segments:")
print("    GEVMT = ?")
print("    R (between TUN and TAG) = article 'der'?")
print("    R (between TAG and SIC) = article 'der'?")
print("    SIC = SICH (self)?")

# Check if 'R' between known words is always the same code
print("\n  Code for 'R' between TUN and TAG:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'TUNRTAG' in col:
        idx = col.index('TUNRTAG')
        decoded = decode(book)
        for ri in range(len(decoded)):
            sub = decoded[ri:ri+20]
            if collapse(sub).startswith('TUNRTAG'):
                # Find the R code
                col_pos = 0
                for k in range(ri, min(ri+10, len(book))):
                    if k == ri or decoded[k] != decoded[k-1]:
                        if col_pos == 3:  # R is at position 3 (T-U-N-R)
                            print(f"    B{bi:02d}: R = code {book[k]} ({mapping.get(book[k],'?')})")
                            break
                        col_pos += 1
                break
        if bi > 10:
            break

# 3. What does the full text after TAG say?
print("\n\n3. FULL CONTEXT AFTER 'TAG'")
print("-" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'TAG' in col:
        idx = col.index('TAG')
        after = col[idx:idx+30]
        print(f"  B{bi:02d}: ...{after}...")
        if bi > 8:
            break

# 4. Attack the GEDA context more carefully
print("\n\n4. GEDA DEEP ANALYSIS")
print("-" * 60)

# Two contexts found:
# "SEIN D GEDA SIE OWI" (5x)
# "SEIN D GEDA NR SEDE TONI" (2x)

# Let's see if these are actually the same narrative section with slight variation
print("  All GEDA occurrences with full surrounding context:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    pos = 0
    while True:
        idx = col.find('GEDA', pos)
        if idx < 0: break
        ctx = col[max(0,idx-15):idx+20]
        print(f"  B{bi:02d}: ...{ctx}...")
        pos = idx + 1
        break  # one per book

# 5. The ST and RU unknowns - these appear at STEINEN and SCHAUNRU boundaries
print("\n\n5. ST AND RU BOUNDARY ANALYSIS")
print("-" * 60)

# ST appears in "URALTE [ST] EINEN" - could this be STEINEN?
print("  URALTE + ST + EINEN = URALTE STEINEN (ancient stones)?")
print("  Checking if ST is just a segmentation artifact:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'URALTESTEINENTER' in col:
        print(f"    B{bi:02d}: URALTESTEINENTER found - confirms URALTE+STEINEN+TER")
    elif 'URALTESTEIN' in col:
        idx = col.index('URALTESTEIN')
        after = col[idx:idx+20]
        print(f"    B{bi:02d}: {after}")

# RU appears at end of "SCHAUNRU"
print("\n  SCHAUN + RU: what follows?")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'SCHAUNRU' in col:
        idx = col.index('SCHAUNRU')
        ctx = col[idx:idx+20]
        print(f"    B{bi:02d}: {ctx}")

# What if RU = RUHE (rest) or RUE (remorse)?
# Or what if SCHAUNRU is one word = "schaun-ru(h)" = "look at rest/peace"?

# 6. The [T] unknowns - single T between known words
print("\n\n6. SINGLE-LETTER UNKNOWNS")
print("-" * 60)
print("  Context: 'DIESER [T] EINER' and 'STEINEN [T] ER'")
print("  [T] could be:")
print("    - Article 'der' collapsed")
print("    - Part of compound")
print("    - Conjunction")

# Check: in "DIESERTEINER" what code is the T?
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'DIESERTEINER' in col:
        idx = col.index('DIESERTEINER')
        decoded = decode(book)
        for ri in range(len(decoded)):
            sub = decoded[ri:ri+20]
            if collapse(sub).startswith('DIESERTEINER'):
                codes = book[ri:ri+15]
                detail = ' '.join(f"{c}={mapping.get(c,'?')}" for c in codes[:13])
                print(f"  B{bi:02d}: DIESERTEINER codes: {detail}")
                break
        break

# 7. IEM IN HEDEMI - what is IEM?
print("\n\n7. IEM ANALYSIS")
print("-" * 60)
print("  Full context: 'WIR UND IEM IN HEDEMI DIE URALTE'")
print("  IEM could be:")
print("    - MHG 'iem' = 'ihm' (him, dative)")
print("    - Part of 'die m...' boundary")
print()

# Check the raw codes for the IEM segment
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'IEMINHEDEMI' in col:
        idx = col.index('IEMINHEDEMI')
        decoded = decode(book)
        for ri in range(len(decoded)):
            sub = decoded[ri:ri+20]
            if collapse(sub).startswith('IEMINHEDEMI'):
                codes = book[ri:ri+15]
                detail = ' '.join(f"{c}={mapping.get(c,'?')}" for c in codes[:14])
                print(f"  B{bi:02d}: IEMINHEDEMI raw: {detail}")
                # Show with word boundaries
                letters = [mapping.get(c, '?') for c in codes[:14]]
                print(f"         Letters: {' '.join(letters)}")
                # Suggest: I(15)-E(86)-M(04)-I(21)-N(58)-H(57)-E(74)-D(45)-E(45)-M(19)-I(04)
                break
        break

# In MHG "iem" is not standard. But "ie" = demonstrative, "m" could be
# part of next word. So: "ie m..." = "die M..." or "ie min..." (the my)?

# 8. HIET analysis - "IN HIET DEN"
print("\n\n8. HIET ANALYSIS")
print("-" * 60)
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'HIET' in col:
        idx = col.find('HIET')
        ctx = col[max(0,idx-8):idx+15]
        print(f"  B{bi:02d}: ...{ctx}...")
        break

print("  HIET = MHG 'hiet' = past tense of 'heizen' (to call)?")
print("  Or: HI + ET = hi(er) + et(was)?")

# 9. TAUTR analysis - proper noun?
print("\n\n9. TAUTR ANALYSIS")
print("-" * 60)
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'TAUTR' in col:
        idx = col.index('TAUTR')
        decoded = decode(book)
        for ri in range(len(decoded)):
            sub = decoded[ri:ri+10]
            if collapse(sub).startswith('TAUTR'):
                codes = book[ri:ri+8]
                detail = ' '.join(f"{c}={mapping.get(c,'?')}" for c in codes[:6])
                print(f"  B{bi:02d}: TAUTR codes: {detail}")
                break
        break

# In MHG/OHG: tautr could be related to:
# - "toter" (dead one)
# - A proper name
# - "taugen" verb root?
print("  TAUTR could be:")
print("    - MHG 'toter' (dead one) - archaic spelling")
print("    - A proper name (character in the narrative)")
print("    - Compare: 'TAUTR IST EILCHANHEARUCHTIG'")
print("      = 'TAUTR is [adjective]' - describes a person")

# 10. EILCHANHEARUCHTIG decomposition
print("\n\n10. EILCHANHEARUCHTIG DECOMPOSITION")
print("-" * 60)
print("  17 characters: E-I-L-C-H-A-N-H-E-A-R-U-C-H-T-I-G")
print()
print("  Possible splits:")
print("    EIL + CHAN + HEA + RUCHTIG")
print("    EILCH + AN + HEAR + UCHTIG")
print("    EI + LCHAN + HEARUCHTIG")
print()
print("  -RUCHTIG = MHG '-ruohtec/-ruchtig' (famous, renowned)")
print("  -UCHTIG could also be '-uchtec' (powerful)")
print("  EILCHAN = proper noun element?")
print("  HEAR = MHG 'her' (lord, army)?")
print()
print("  Reading attempt: EILCHAN-HEA-RUCHTIG")
print("    = '[name/title]-lord-famous'")
print("    = 'famous lord of EILCHAN'?")

# Check raw codes for EILCHANHEARUCHTIG
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'EILCHANHEARUCHTIG' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            sub = decoded[ri:ri+30]
            if collapse(sub).startswith('EILCHANHEARUCHTIG'):
                codes = book[ri:ri+25]
                # Count how many raw codes make up the 17 collapsed chars
                col_so_far = ''
                for k in range(25):
                    col_so_far = collapse(decoded[ri:ri+k+1])
                    if len(col_so_far) >= 17:
                        raw = codes[:k+1]
                        detail = ' '.join(f"{c}={mapping.get(c,'?')}" for c in raw)
                        print(f"\n  Raw codes ({k+1} codes for 17 chars):")
                        print(f"    {detail}")
                        break
                break
        break

# 11. Full superstring of all books
print("\n\n11. OVERLAP ANALYSIS - BOOK ORDERING")
print("-" * 60)

# Find which books overlap and in what order
decoded_all = [collapse(decode(b)) for b in books]

# Check consecutive pairs that overlap
overlaps = []
for i in range(len(decoded_all)):
    for j in range(len(decoded_all)):
        if i == j: continue
        text_i = decoded_all[i]
        text_j = decoded_all[j]
        # Check if end of i overlaps with start of j
        best_overlap = 0
        for k in range(min(len(text_i), len(text_j)), 2, -1):
            if text_i[-k:] == text_j[:k]:
                best_overlap = k
                break
        if best_overlap >= 8:
            overlaps.append((i, j, best_overlap, text_i[-best_overlap:]))

overlaps.sort(key=lambda x: x[2], reverse=True)
print(f"  Found {len(overlaps)} significant overlaps (>= 8 chars)")
print(f"\n  Top 15 overlaps:")
for i, j, ov, text in overlaps[:15]:
    print(f"    B{i:02d} -> B{j:02d}: {ov} chars overlap: ...{text[:30]}...")

# 12. Build reading order from overlaps
print("\n\n12. NARRATIVE READING ORDER")
print("-" * 60)

# Build chain: find the book that starts the narrative
# (book with no predecessor, or least overlap at start)
if overlaps:
    # Find start: book not appearing as target of any overlap
    targets = set(j for _, j, _, _ in overlaps)
    sources = set(i for i, _, _, _ in overlaps)
    starts = sources - targets
    if starts:
        print(f"  Possible starting books: {sorted(starts)}")
    else:
        print("  All books have predecessors (circular?)")

    # Build chain greedily
    used = set()
    # Try starting from book with smallest index in starts
    chain = []
    if starts:
        current = min(starts)
    else:
        current = 0
    chain.append(current)
    used.add(current)

    for _ in range(len(books)):
        best_next = None
        best_ov = 0
        for i, j, ov, _ in overlaps:
            if i == current and j not in used and ov > best_ov:
                best_next = j
                best_ov = ov
        if best_next is None:
            break
        chain.append(best_next)
        used.add(best_next)
        current = best_next

    print(f"  Chain ({len(chain)} books): {chain[:20]}...")

    # Print first few books in order
    print(f"\n  First 5 books in narrative order:")
    for idx, bi in enumerate(chain[:5]):
        col = decoded_all[bi]
        print(f"    [{idx}] B{bi:02d}: {col[:70]}...")

print("\n" + "=" * 80)
print("SESSION 10w COMPLETE")
print("=" * 80)
