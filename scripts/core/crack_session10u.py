#!/usr/bin/env python3
"""Session 10u: Focused attack on top unknowns + V code analysis + GEDANKE hypothesis"""

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
print("SESSION 10u: FOCUSED UNKNOWN ATTACKS")
print("=" * 80)

# 1. V CODE ANALYSIS - is code 83 really V?
print("\n1. V CODE ANALYSIS")
print("-" * 60)
v_codes = rev_map['V']
print(f"  V codes: {v_codes}")
for c in v_codes:
    print(f"    code {c}: {all_codes.get(c,0)} occurrences")

# Where is V confirmed?
print("\n  V confirmation check (VON, VIEL, etc.):")
v_words = ['VON', 'VIEL', 'VOR']
for vw in v_words:
    for bi, book in enumerate(books):
        col = collapse(decode(book))
        if vw in col:
            decoded = decode(book)
            for ri in range(len(decoded)):
                sub = decoded[ri:ri+len(vw)+3]
                if collapse(sub).startswith(vw):
                    v_pos = vw.index('V')
                    code_at_v = book[ri + v_pos]
                    print(f"    {vw} in B{bi:02d}: V is code {code_at_v}")
                    break
            break

# Full GEVMT analysis
print("\n\n2. GEVMT DEEP ANALYSIS")
print("-" * 60)
print("  GEVMT raw codes: G(97)-E(27)-V(83)-M(04)-T(64)")
print("  Context always: SEI GEVMT WIE TUN R TAG")
print()

# Verify V code in VON vs in GEVMT
print("  Code 83 usage - ALL contexts:")
ctx83 = []
for bi, book in enumerate(books):
    for ci, c in enumerate(book):
        if c == '83':
            start = max(0, ci-4)
            end = min(len(book), ci+5)
            raw = decode(book[start:end])
            col = collapse(raw)
            ctx83.append((bi, ci, col))

seen = set()
for bi, ci, col in ctx83:
    if col not in seen:
        seen.add(col)
        print(f"    B{bi:02d}[{ci}]: {col}")

print(f"\n  Code 83 total occurrences: {all_codes.get('83', 0)}")

# What if code 83 is NOT V but another letter?
print("\n  Testing code 83 as other letters in GEVMT context:")
for letter in 'ABCDEFGHIKLMNOPRSTUWZ':
    mod = dict(mapping)
    mod['83'] = letter
    sample = collapse(decode(books[2], mod))  # B02 has GEVMT
    # Find the modified word
    if 'GEVMT' in collapse(decode(books[2])):
        idx = collapse(decode(books[2])).index('GEVMT')
        new_text = sample[max(0,idx-5):idx+15]
        old_text = collapse(decode(books[2]))[max(0,idx-5):idx+15]
        if new_text != old_text:
            word_at = sample[idx:idx+5]
            print(f"    83={letter}: GEVMT -> GE{letter}MT (full: ...{new_text}...)")

# What if code 04 (M in GEVMT) is wrong?
print("\n  Code 04 (currently M) contexts:")
ctx04 = []
for bi, book in enumerate(books):
    for ci, c in enumerate(book):
        if c == '04':
            start = max(0, ci-3)
            end = min(len(book), ci+4)
            raw = decode(book[start:end])
            col = collapse(raw)
            if col not in [x[2] for x in ctx04[:20]]:
                ctx04.append((bi, ci, col))

for bi, ci, col in ctx04[:15]:
    print(f"    B{bi:02d}[{ci}]: {col}")

print(f"\n  Code 04 total: {all_codes.get('04', 0)} occurrences")
print(f"  Code 04 is UNCONFIRMED M")

# What if GEVMT is actually a known word with wrong M?
print("\n  Testing code 04 as other letters (in GEVMT -> GEV?T):")
for letter in 'ABCDEFGHIKLNOPRSTUWZ':  # skip M (current)
    if letter == 'V': continue  # already have V
    word = f"GEV{letter}T"
    # Check if this is a German word
    german_check = {
        'GEVAT': 'MHG gevaht/gefat (seized)',
        'GEVET': '',
        'GEVIT': '',
        'GEVOT': '',
        'GEVUT': '',
        'GEVNT': '',
        'GEVRT': '',
        'GEVST': '',
        'GEVLT': '',
    }
    if word in german_check and german_check[word]:
        print(f"    04={letter}: {word} = {german_check[word]}")

# 3. DGEDA -> GEDANKE hypothesis
print("\n\n3. DGEDA -> GEDANKE HYPOTHESIS")
print("-" * 60)

# In the text DGEDA appears as part of "NDGEDANRSEDE"
# D GEDA NR SEDE -> UND GEDAN(KE) R SEDE ?
print("  Looking for full GEDAN context:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'GEDA' in col:
        for idx in range(len(col)):
            if col[idx:idx+4] == 'GEDA':
                ctx = col[max(0,idx-8):idx+12]
                # Get raw codes at this position
                decoded = decode(book)
                for ri in range(len(decoded)):
                    sub = decoded[ri:ri+8]
                    if collapse(sub).startswith('GEDA'):
                        raw_codes = book[ri:ri+8]
                        raw = [f"{c}={mapping.get(c,'?')}" for c in raw_codes[:8]]
                        print(f"    B{bi:02d}: ...{ctx}... codes: {' '.join(raw)}")
                        break
                break

# Could "GEDANR" be "GEDANK" with wrong R/K?
print("\n  After GEDA, what letter comes?")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'GEDA' in col:
        idx = col.index('GEDA')
        after = col[idx+4:idx+8]
        print(f"    B{bi:02d}: GEDA + '{after}'")
        break

# 4. CHN ANALYSIS - what comes before and after
print("\n\n4. CHN IN CONTEXT")
print("-" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    pos = 0
    while True:
        idx = col.find('CHN', pos)
        if idx < 0: break
        # Only count standalone CHN (not part of SCH)
        if idx > 0 and col[idx-1:idx+3] == 'SCHN':
            pos = idx + 1
            continue
        ctx = col[max(0,idx-8):idx+10]
        print(f"  B{bi:02d}: ...{ctx}...")
        pos = idx + 1
        break  # one per book

print("\n  CHN likely: end of word + N(ext word)")
print("  -CH endings: AUCH, NOCH, DOCH, SICH, MICH, DICH, BUCH")
print("  After CH: N could start next word (NICHT, NUR, NOCH, etc.)")

# Check specific: "IN CHN ES" pattern
print("\n  'IN CHN ES' pattern analysis:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'INCHNES' in col.replace(' ', ''):
        idx = col.find('CHN')
        if idx >= 0:
            wider = col[max(0,idx-12):idx+12]
            decoded = decode(book)
            for ri in range(len(decoded)):
                sub = decoded[ri:ri+10]
                if collapse(sub).startswith('CHN'):
                    raw_codes = book[ri:ri+6]
                    raw = [f"{c}={mapping.get(c,'?')}" for c in raw_codes]
                    print(f"    B{bi:02d}: ...{wider}...")
                    print(f"      CHN codes: {' '.join(raw)}")
                    break
            break

# 5. SCE ANALYSIS
print("\n\n5. SCE IN CONTEXT")
print("-" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    pos = 0
    while True:
        idx = col.find('SCE', pos)
        if idx < 0: break
        if idx + 3 < len(col) and col[idx+3] == 'H':  # Skip SCH words
            pos = idx + 1
            continue
        ctx = col[max(0,idx-10):idx+10]
        print(f"  B{bi:02d}: ...{ctx}...")
        pos = idx + 1
        break

print("\n  SCE pattern: 'ER SCE AUS'")
print("  Could be: ER S CE AUS or ER SC E AUS")
print("  Or: ER SCE (=schee, MHG for 'beautiful') AUS?")

# 6. NGETRAS ANALYSIS
print("\n\n6. NGETRAS IN CONTEXT")
print("-" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'NGETRAS' in col:
        idx = col.index('NGETRAS')
        ctx = col[max(0,idx-12):idx+15]
        decoded = decode(book)
        for ri in range(len(decoded)):
            sub = decoded[ri:ri+15]
            if collapse(sub).startswith('NGETRAS'):
                raw_codes = book[ri:ri+10]
                raw = [f"{c}={mapping.get(c,'?')}" for c in raw_codes[:10]]
                print(f"  B{bi:02d}: ...{ctx}...")
                print(f"    codes: {' '.join(raw)}")
                break
        break

# NGETRAS = N-G-E-T-R-A-S
# Could be: N + GETRAS or NGE + TRAS
# GETRAGEN past participle of TRAGEN (carry) loses N: GETRAGE
# Or could be SONGETRAS = SON + GETRAS
print("\n  Full contexts of NGETRAS:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'NGETRAS' in col:
        idx = col.index('NGETRAS')
        before = col[max(0,idx-15):idx]
        after = col[idx+7:idx+15]
        print(f"    before='{before}' [NGETRAS] after='{after}'")

# 7. TEMDIA ANALYSIS (5x)
print("\n\n7. TEMDIA IN CONTEXT")
print("-" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'TEMDIA' in col:
        idx = col.index('TEMDIA')
        ctx = col[max(0,idx-10):idx+15]
        print(f"  B{bi:02d}: ...{ctx}...")
        break

# TEMDIA = T-E-M-D-I-A
# Could be: TEM + DIA or TEMD + IA
# Or word boundary: ... TE M DIA ...

# 8. UISEMIV (5x)
print("\n\n8. UISEMIV IN CONTEXT")
print("-" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'UISEMIV' in col:
        idx = col.index('UISEMIV')
        ctx = col[max(0,idx-10):idx+15]
        decoded = decode(book)
        for ri in range(len(decoded)):
            sub = decoded[ri:ri+12]
            if collapse(sub).startswith('UISEMIV'):
                raw_codes = book[ri:ri+10]
                raw = [f"{c}={mapping.get(c,'?')}" for c in raw_codes[:10]]
                print(f"  B{bi:02d}: ...{ctx}...")
                print(f"    codes: {' '.join(raw)}")
                break
        break

# UISEMIV: could be WISE + MIV or UIS + EMIV
# In MHG: WISE (manner/way), MIV?

# 9. Full B05 narrative attempt (92% decoded)
print("\n\n" + "=" * 60)
print("9. B05 FULL NARRATIVE (92% decoded)")
print("=" * 60)

col05 = collapse(decode(books[5]))
print(f"  Full decoded: {col05}")
print()

# Manual reading attempt
print("  Manual segmentation attempt:")
# From the DP output: HIER TAUTR IST EILCHANHEARUCHTIG ER SO DAS TUN
# DIESER T EINER SEIN EDETOTNIURGS ER LABRNI WIR UND IE M IN
# HEDEMI DIE URALTE ST EINEN T ER ADTHARSC IST SCHAUN RU
segments = [
    ('EN', '?', 'initial particle?'),
    ('HIER', 'W', 'here'),
    ('TAUTR', 'W', 'proper noun? MHG name?'),
    ('IST', 'W', 'is'),
    ('EILCHANHEARUCHTIG', 'W', 'compound adj? -RUCHTIG=famous?'),
    ('ER', 'W', 'he'),
    ('SO', 'W', 'so/thus'),
    ('DAS', 'W', 'that'),
    ('TUN', 'W', 'do'),
    ('DIESER', 'W', 'this'),
    ('T', '?', 'article/prep?'),
    ('EINER', 'W', 'one/a'),
    ('SEIN', 'W', 'his'),
    ('EDETOTNIURGS', 'W', 'contains TOT(dead), proper noun?'),
    ('ER', 'W', 'he'),
    ('LABRNI', 'W', 'proper noun?'),
    ('WIR', 'W', 'we'),
    ('UND', 'W', 'and'),
    ('IE', 'W', 'MHG: the/she'),
    ('MINHE', 'W', 'MHG: minne (love)'),
    ('DEMI', '?', 'dem+i? dative?'),
    ('DIE', 'W', 'the'),
    ('URALTE', 'W', 'ancient'),
    ('ST', '?', 'part of STEIN?'),
    ('EINEN', 'W', 'stones/one'),
    ('T', '?', '?'),
    ('ER', 'W', 'he'),
    ('ADTHARSC', 'W', 'proper noun'),
    ('IST', 'W', 'is'),
    ('SCHAUN', 'W', 'to see/look'),
    ('RU', '?', 'ruhe(rest)? ruhm(glory)?'),
]

for word, wtype, meaning in segments:
    status = '[OK]' if wtype == 'W' else '[??]'
    print(f"    {status} {word:20s} = {meaning}")

# 10. TIUMENGEMI raw code study
print("\n\n" + "=" * 60)
print("10. TIUMENGEMI RAW CODES")
print("=" * 60)
print("  T(78) I(16) U(70) M(54) E(67) N(11) G(80) E(01) M(40) I(15)")
print()
print("  Letter assignments:")
print("    78=T (confirmed in STEIN, ERST, etc.)")
print("    16=I (confirmed? checking...)")
# Check code 16
print(f"    Code 16 is mapped to: {mapping.get('16', '?')}")
print(f"    Code 16 frequency: {all_codes.get('16', 0)}")

# Check code 70
print(f"    Code 70 is mapped to: {mapping.get('70', '?')}")
print(f"    Code 70 frequency: {all_codes.get('70', 0)}")

# Check code 54
print(f"    Code 54 is mapped to: {mapping.get('54', '?')}")
print(f"    Code 54 frequency: {all_codes.get('54', 0)}")

# Check code 01
print(f"    Code 01 is mapped to: {mapping.get('01', '?')}")
print(f"    Code 01 frequency: {all_codes.get('01', 0)}")

# Check code 40
print(f"    Code 40 is mapped to: {mapping.get('40', '?')}")
print(f"    Code 40 frequency: {all_codes.get('40', 0)}")
print(f"    Code 40 is UNCONFIRMED M")

# What if TIUMENGEMI is actually two words?
# TIU + MENGEMI or TIUM + ENGEMI or TIUMEN + GEMI
print("\n  Possible word boundaries in TIUMENGEMI:")
print("    TIU + MENGEMI: TIU = MHG 'diu' (the, fem.)")
print("    TIUM + EN + GEMI: GEMI could be from GEMEIN(DE)")
print("    TI + UMENGE + MI: UMENGE ?")
print("    TIUMENGE + MI: ?")
print("    Note: always followed by ORT (place)")
print()

# TIU MENGEMI ORT ENGCHD
# If TIU = diu (the), then MENGEMI is a noun
# MENGE = crowd/amount -> MENGEMI = ?
# Or: MENGE + MI ?
# ORT = place
# ENGCHD = place name

# What if some letters are wrong? Test key codes
print("  Testing if code 40 (M, unconfirmed) changes reading:")
for letter in 'ABCDEFGHIKLNOPRSTUVWZ':
    if letter == 'M': continue
    mod = dict(mapping)
    mod['40'] = letter
    for bi, book in enumerate(books):
        col = collapse(decode(book, mod))
        if 'TIUMEN' in col[:80] or 'TIUMENGE' in col[:80]:
            # Find the modified word
            for target_start in ['TIU', 'TIUM']:
                idx = col.find(target_start)
                if idx >= 0:
                    result = col[idx:idx+12]
                    print(f"    40={letter}: ...{result}... (was TIUMENGEMI)")
                    break
            break

# 11. Look at STEIEN - appears as known word but what is it?
print("\n\n" + "=" * 60)
print("11. STEIEN ANALYSIS")
print("=" * 60)
print("  STEIEN appears in word list - what is it?")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'STEIEN' in col:
        idx = col.index('STEIEN')
        ctx = col[max(0,idx-10):idx+15]
        print(f"    B{bi:02d}: ...{ctx}...")
        break

print("  STEIEN could be MHG 'steien' = stand/place")
print("  Or: STE + IEN = MHG sten (stand) + ien?")
print("  Context: after URALTE -> 'the ancient STEIEN'")

# 12. VMTEGE analysis
print("\n\n" + "=" * 60)
print("12. VMTEGE ANALYSIS")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'VMTEGE' in col:
        idx = col.index('VMTEGE')
        ctx = col[max(0,idx-10):idx+15]
        decoded = decode(book)
        for ri in range(len(decoded)):
            sub = decoded[ri:ri+12]
            if collapse(sub).startswith('VMTEGE'):
                raw_codes = book[ri:ri+10]
                raw = [f"{c}={mapping.get(c,'?')}" for c in raw_codes[:10]]
                print(f"  B{bi:02d}: ...{ctx}...")
                print(f"    codes: {' '.join(raw)}")
                break
        break

print("\n  VMTEGE and GEVMT share letters V,M,T,G,E")
print("  GEVMT = G-E-V-M-T")
print("  VMTEGE = V-M-T-E-G-E")
print("  These look like the SAME word viewed from different overlap positions!")
print("  Full sequence might be: GEVMTEGE or VMTEGE+VMT")

# Check: does GEVMTEGE appear anywhere?
print("\n  Checking for GEVMTEGE:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'GEVMTEGE' in col:
        idx = col.index('GEVMTEGE')
        ctx = col[max(0,idx-8):idx+15]
        print(f"    Found in B{bi:02d}: ...{ctx}...")

# What about SEIGEVMT or VMTWIETUN?
print("\n  Checking for full SEIGEVMTWIETUN:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'SEIGEVMT' in col:
        idx = col.index('SEIGEVMT')
        full = col[idx:idx+20]
        print(f"    B{bi:02d}: {full}")

print("\n" + "=" * 80)
print("SESSION 10u COMPLETE")
print("=" * 80)
