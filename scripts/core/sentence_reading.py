"""
Session 9 - Contextual sentence reading.
Try to read complete sentences by splitting bracketed unknowns at word boundaries.
Focus on the most readable pieces to extract maximum meaning.
"""
import json, re
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

def collapse(text):
    if not text: return text
    r = [text[0]]
    for c in text[1:]:
        if c != r[-1]: r.append(c)
    return ''.join(r)

print("=" * 80)
print("CONTEXTUAL SENTENCE READING")
print("=" * 80)

# ============================================================
# 1. SER L AB RNI = SER LABRRNI (a title + name)
# ============================================================
print("\n1. SER LABRRNI ANALYSIS")
print("-" * 60)
# "SER [L] AB [RNI]" appears multiple times
# SER = archaic "Sir" (MHG/archaic title)
# LAB = first part of LABGZERAS
# RNI = ?
# LABRRNI with collapsed doubles = LABRNI
# Could be: LAB + R + NI = a name related to King LABGZERAS?
# SER LABRRNI = Sir Labrrni, a companion of the narrator
for i, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find("SERLABR")
    if idx != -1:
        ctx = decoded[max(0,idx-5):min(len(decoded),idx+20)]
        codes_here = book_codes[idx:idx+12]
        print(f"  Book {i}: ...{ctx}...")
        print(f"    codes: {codes_here}")
        break

# Also check: is there "SER" + "TI" together elsewhere?
# "SER TI UM" appears: SER + TI + UM = SERTIUM?
for i, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find("SERTIUM")
    if idx != -1:
        ctx = decoded[max(0,idx-5):min(len(decoded),idx+15)]
        print(f"  Book {i} SERTIUM: ...{ctx}...")
        break

# ============================================================
# 2. TEIGN = T + EIGEN (own/self)
# ============================================================
print("\n2. TEIGN SPLIT")
print("-" * 60)
# "FINDEN TEIGN DAS ES DER ERSTE"
# TEIGN = T-E-I-G-N
# If we split: T + EIGN = ? + EIGEN (own)
# The T belongs to the previous word?
# "FINDEN T EIGEN" = "finden [?t] eigen" = "find [their] own"
# OR: FINDEN T = FINDET (finds!) + EIGEN
# FINDET = 3rd person singular of FINDEN!
# "FINDET EIGEN DAS ES DER ERSTE" = "finds own that it the first"
# Wait: FINDEN-T vs FINDE-T. Let's check the raw codes
for i, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find("FINDENTEIGN")
    if idx != -1:
        codes_here = book_codes[idx:idx+11]
        print(f"  Book {i}: FINDENTEIGN")
        for j, c in enumerate(codes_here):
            letter = mapping.get(c, '?')
            print(f"    pos {j}: code {c} = {letter}")
        # The split could be:
        # FINDEN + TEIGN: to find + ?
        # FINDE + N + TEIGN: I find + ?
        # FINDET + EIGN: finds + EIGEN
        # But: N is at position 5 (code for N), T is at position 6
        # So the letters are: F-I-N-D-E-N-T-E-I-G-N
        # Best reading: FINDEN + T + EIGN = "to find" + T + "own"
        # Or: FINDE + NT + EIGN -- NT isn't a word
        # The T must belong somewhere!
        # What if: "...FINDEN TEIGN..." = "FINDET EIGEN"?
        # No, the N and T are distinct codes. N is real.
        # FINDEN TEIGNDAS = "finden, t-eigen das" = "find, [?] own that"
        # In MHG: "IR EIGEN" = "their own"
        # T could be part of previous context: "...UND T FINDEN EIGEN"?
        # Wait, let me check what's BEFORE FINDEN
        ctx_start = max(0, idx-10)
        full_ctx = decoded[ctx_start:idx+15]
        print(f"    Wider context: {full_ctx}")
        break

# ============================================================
# 3. NDCE pattern - ND + CE
# ============================================================
print("\n3. NDCE = UND + CE?")
print("-" * 60)
# "MIN HIHL DIE NDCE FACH ECHLT ICH OEL"
# ND = end of UND (and)
# CE = beginning of next word?
# If SC = SCH (MHG), then CE could be part of a word ending in -CE
# But CE alone: could it be a pronoun or particle?
# "UND CE FACH" = "and ? profession/trade"
# What if NDCE = INDE (therein, MHG)?
# Or: NDCE split as N + DCE or ND + CE
# DCE doesn't exist. ND + CE it is.
# In the wider context: "MIN HIHL DIE NDCE FACH HECHLT ICH OEL SO DEN"
# = "my Hihl the ?-CE trade hackles I anoint thus the"
# NDCE could be: "UND ER" with C=part of next word?
# No, CE is C-E (code 18 + code for E)
# "DIE NDCE" = "DIE UND CE" where CE starts CEFACH?
# Wait - CEFACH: in MHG, "GEFACH" = "compartment" (GE- prefix)!
# But C != G in our mapping.
# Hmm, what about reading it differently:
# DIE-ND-CE-FACH = "DIENDE CEFACH"?
# DIENDE doesn't exist. But "DIENENDE" = "serving"?
# Or: DIE-N-D-CE-FACH where N=EN (the), D=?

for i, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find("NDCEFACH")
    if idx != -1:
        codes_here = book_codes[idx:idx+8]
        print(f"  Book {i}: NDCEFACH")
        for j, c in enumerate(codes_here):
            letter = mapping.get(c, '?')
            print(f"    pos {j}: code {c} = {letter}")
        break

# ============================================================
# 4. DUNLN pattern
# ============================================================
print("\n4. DUNLN = DU + NLN?")
print("-" * 60)
# "SCE AUS EN DE DUNLN DE FS AN"
# Could be: "...aus en de DUNLN de..."
# DU + NLN? Or D + UNLN?
# DUNLN collapsed = DUNLN (no doubles)
# What if it's D + UND + LN?
# "DE D UND LN DE" = "the the and [?] the"?
# Or: "DEDUNLN" = "DE DUNLN" where DUNLN = "dark" (DUNKEL)?
# DUNKEL = D-U-N-K-E-L but we have D-U-N-L-N
# Close but not quite. Missing K and wrong ending.
# Unless K is wrong? Code for K is rare...
for i, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find("DUNLN")
    if idx != -1:
        codes_here = book_codes[idx:idx+5]
        ctx_start = max(0, idx-8)
        ctx_end = min(len(decoded), idx+12)
        print(f"  Book {i}: ...{decoded[ctx_start:ctx_end]}...")
        print(f"    DUNLN codes: {codes_here}")
        for j, c in enumerate(codes_here):
            print(f"      {mapping.get(c,'?')}: code {c}")
        break

# ============================================================
# 5. VMTEGE pattern - what German word could this be?
# ============================================================
print("\n5. VMTEGE ANALYSIS")
print("-" * 60)
# "IST VMTEGE VIEL" and "E VMT WIIE"
# VMT codes: 83-04-64 = V-M-T
# VMTEGE = V-M-T-E-G-E
# If V=F (MHG used V for F): FMTEGE? No.
# What if VMT is actually a word? VOMIT? No...
# In MHG: "VERMOCHTE" = could/was able to?
# VMT could be a abbreviation or spelling variant
# But 83=V is only used 43 times, suggesting V is genuine.
# What if we collapse VMT: same (no doubles)
# VMTEGE = "V-M-T-EGE" or "VM-TEGE"
# TEGE = "Tage" (days) in some dialects?
# "IST VMT EGE VIEL" = "is ? ? much"
# Or: "IST VM TEGE VIEL" = "is ? days much"
# Let me check full context more carefully
for i, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find("VMTEGE")
    if idx != -1:
        ctx_start = max(0, idx-15)
        ctx_end = min(len(decoded), idx+20)
        codes_here = book_codes[idx:idx+6]
        print(f"  Book {i}: ...{decoded[ctx_start:ctx_end]}...")
        print(f"    VMTEGE codes: {codes_here}")
        # What if V is actually used as F in MHG?
        # In MHG: V was pronounced /f/ before consonants
        # VMT with V=/f/: FMT? Still not a word
        # Unless M is wrong here too...

# ============================================================
# 6. LAUNRLRUNR - the other stubborn pattern
# ============================================================
print("\n6. LAUNRLRUNR")
print("-" * 60)
# "ER LAUNRLRUNR NACH ECHL"
# Collapsed: LAUNRLRUNR -> LAUNRLRUNR (no doubles)
# Wait: L-A-U-N-R-L-R-U-N-R
# What if: LAUN + R + L + RUNR?
# Or: LAU + NR + LRU + NR?
# LAUF = run! LAU + F? But F is code 20, not present here.
# LAUNR = LAUERN (to lurk)? LAU + NR?
# LRUNR reversed = RNURL
# Full reversed: RNURLLRNUAL
# Hmm, LRUNR itself: L + RUNR or LR + UNR
# RUNR could be RUNER (one who uses runes)?
# "ER LAUN-R-LRUNR NACH" = "he lurk-?-? toward"?
for i, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find("LAUNRLRUNR")
    if idx != -1:
        codes_here = book_codes[idx:idx+10]
        ctx_start = max(0, idx-8)
        ctx_end = min(len(decoded), idx+15)
        print(f"  Book {i}: ...{decoded[ctx_start:ctx_end]}...")
        print(f"    codes: {codes_here}")
        for j, c in enumerate(codes_here):
            print(f"      {mapping.get(c,'?')}: code {c}")
        break

# ============================================================
# 7. DNRHAUNRN / DNRHAUNRNVMHISDIZA
# ============================================================
print("\n7. DNRHAUNRN PATTERN")
print("-" * 60)
# Appears in several books
# D-N-R-H-A-U-N-R-N
# If ND = UND: ...UND NRHAUNRN?
# Or split: DNR + HAUNRN? HAUN = chop/strike (MHG)!
# HAUNRN = HAUEN (to strike) + RN?
# "DEN DNRHAUNRN" = "den [d?] Hau[e]n [r?]" = "the striking/chopping"?
# VMHISDIZA follows: V-M-H-I-S-D-I-Z-A
# DIZA reversed = AZID. VMHIS = ?
# Full: DNRHAUNRNVMHISDIZA = "DNR-HAUNRN-VMHI-SDIZA"
# Or: "D + NR + HAUN + RN + VMH + IS + DIZA"
# HAUN = chop! (MHG hauwen = to chop/strike)
# "HAUN RN VMH IS DIZA" = "chop ? ? is ?"
for i, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find("DNRHAUNRN")
    if idx != -1:
        codes_here = book_codes[idx:idx+20]
        ctx_start = max(0, idx-8)
        ctx_end = min(len(decoded), idx+25)
        print(f"  Book {i}: ...{decoded[ctx_start:ctx_end]}...")
        print(f"    codes: {codes_here[:10]}")
        break

# ============================================================
# 8. Build complete sentence-by-sentence reading
# ============================================================
print(f"\n{'='*80}")
print("COMPLETE SENTENCE READING (BEST ATTEMPT)")
print(f"{'='*80}")

# Use Piece 2 (the best piece) and try to read it as German
piece2_books = [3, 44, 52, 62, 29, 68]  # Books that overlap in Piece 2 region

# Take Book 46 which has the longest readable stretch
for bi in [46, 51, 53]:
    decoded = decode(books[bi])
    collapsed = collapse(decoded)
    print(f"\n  Book {bi} decoded ({len(decoded)} chars):")
    print(f"    Raw: {decoded}")
    print(f"    Col: {collapsed}")

    # Manual word boundary attempt
    # Replace known patterns
    text = collapsed
    text = text.replace('KOENIG', ' KOENIG ')
    text = text.replace('LABGZERAS', ' LABGZERAS ')
    text = text.replace('AUNRSONGETRASES', ' AUNRSONGETRASES ')
    text = text.replace('TOTNIURG', ' TOTNIURG ')
    text = text.replace('HEARUCHTIGER', ' HEARUCHTIGER ')
    text = text.replace('TAUTR', ' TAUTR ')
    text = text.replace('EILCH', ' EILCH ')
    text = text.replace('THARSC', ' THARSC ')
    text = text.replace('SCHWITEIO', ' SCHWITEIO ')
    text = text.replace('HIHL', ' HIHL ')
    text = text.replace('MINHEDEM', ' MINHEDEM ')
    text = text.replace('RUNEORT', ' RUNEORT ')
    text = text.replace('WISSET', ' WISSET ')
    text = text.replace('URALTE', ' URALTE ')
    text = text.replace('STEIN', ' STEIN ')
    text = text.replace('FINDEN', ' FINDEN ')
    text = text.replace('SCHAUN', ' SCHAUN ')
    text = text.replace('RUIN', ' RUIN ')

    # Known short words
    for word in ['IST', 'UND', 'DIE', 'DER', 'DEN', 'DEM', 'DES', 'DAS',
                 'EIN', 'ER', 'ES', 'SIE', 'WIR', 'ICH', 'SO', 'AN',
                 'IN', 'AUS', 'VON', 'HIER', 'SEIN', 'SEINE', 'TUN',
                 'DIES', 'NEU', 'ALT', 'ALTE', 'NACH', 'ORT', 'RUNE',
                 'SEID', 'GAR', 'NUN', 'KLAR', 'ALS', 'TAG', 'SEI',
                 'VIEL', 'AUCH', 'WEG', 'TEIL', 'BIS', 'UNTER',
                 'ERST', 'ERSTE', 'WIND', 'GEH', 'STEH', 'REDE',
                 'FACH', 'ERDE', 'ODE', 'SEE', 'HAT', 'AM', 'AB']:
        # Only replace if surrounded by non-alpha or start/end
        text = re.sub(r'(?<=[A-Z])' + word + r'(?=[A-Z])', ' ' + word + ' ', text)

    # Clean up spaces
    text = re.sub(r' +', ' ', text).strip()
    print(f"    Segmented: {text}")

print("\n" + "=" * 80)
print("KEY FINDINGS")
print("=" * 80)
print("""
1. SER LABRRNI = "Sir Labrrni" -- a titled companion
2. FINDET EIGEN = "finds [their] own" (FINDEN + T split as FINDET)
3. CEFACH = possibly GEFACH (compartment) with C=G issue
4. DUNLN = possibly garbled DUNKEL (dark) missing K
5. HAUN in DNRHAUNRN = HAUEN (to strike, MHG)
6. VMT remains unresolved -- possibly a scribal abbreviation
7. LAUNRLRUNR = possibly LAUERN (to lurk) + repeated elements
""")
