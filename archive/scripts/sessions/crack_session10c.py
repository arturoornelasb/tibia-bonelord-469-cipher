"""
Session 10c - Colophon structure + new word discoveries.
Key discoveries from 10b:
  - ENDEUTRUNR DENEN DER REDE KOENIG = colophon!
  - WIIE = WIE (how), SEII = SEI (be!)
  - Code 24 = R confirmed via UNTER
  - GEIGET appears in "ER GEIGET ES IN..."
  - VMT appears in two contexts: "IST VMT EGE VIEL" and "SEI GE VMT WIE"
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

def decode(codes):
    return ''.join(mapping.get(c, '?') for c in codes)

def collapse(text):
    if not text: return text
    r = [text[0]]
    for c in text[1:]:
        if c != r[-1]: r.append(c)
    return ''.join(r)

print("=" * 80)
print("SESSION 10c: COLOPHON + NEW WORDS")
print("=" * 80)

# ============================================================
# 1. Trace the full colophon: ENDEUTRUNR...KOENIG LABGZERAS
# ============================================================
print("\n1. FULL COLOPHON TRACE")
print("-" * 60)

# Find books containing ENDEUTRUNR
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('ENDEUTRUNR')
    if idx != -1:
        # Get everything from SCE AUS to end
        sceaus_idx = decoded.rfind('SCEAUS', 0, idx)
        if sceaus_idx == -1:
            sceaus_idx = max(0, idx - 20)
        end_idx = min(len(decoded), idx + 60)
        full_colophon = decoded[sceaus_idx:end_idx]
        print(f"\n  Book {bi}: ...{full_colophon}...")

        # Code-by-code trace for DENEN DER REDE section
        rede_start = decoded.find('DENEN', idx)
        if rede_start != -1:
            rede_codes = book_codes[rede_start:rede_start+25]
            rede_text = decoded[rede_start:rede_start+25]
            print(f"\n  Code trace from DENEN:")
            for j, c in enumerate(rede_codes):
                if j < len(rede_text):
                    print(f"    pos {j:2d}: {c} = {mapping.get(c,'?')}  ({rede_text[j]})")
            # The text DENENDEREDERKOENIG
            # Let's try: DENEN + DER + REDE + KOENIG?
            # But where's REDE? Let me look:
            # D-E-N-E-N-D-E-R-E-D-E-R-K-O-E-N-I-G
            # DENEN = 5 chars
            # DER = 3 chars (pos 5-7)
            # Then: E-D-E-R = pos 8-11
            # EDER? Or E + DER?
            # KOENIG starts at pos 12
            # So: DENEN + DER + EDER + KOENIG
            # But wait: pos 8 = E, 9 = D, 10 = E
            # What if: DENEN + DER + E + DER + KOENIG?
            # That's "of those of the [E] of the King"
            # The E could be: first letter of next word? EDERKOENIG?
            # Or: DENEN + DERE + DER + KOENIG?
            # DERE = MHG dative "to the"!
            # In MHG: DERE = genitive feminine singular of DER
            # "DENEN DERE DER KOENIG" = "to whom, of her, the King"
            # Hmm, or: REDE is hiding in there!
            # DEN-EN-DER-REDE-R-KOENIG?
            # Let me check: D(pos0)-E-N-E-N-D-E-R-E-D-E-R-K-O-E-N-I-G
            # If REDE = pos 7-10 (R-E-D-E): D-E-N-E-N-D-E | R-E-D-E | R-K-O-E-N-I-G
            # That gives: DENENDE + REDE + R + KOENIG
            # DENENDE = ?
            # Or: DENEN + DE + REDE + R + KOENIG?
            # DE REDE = "the speech"? In MHG, DE could be a form of DER
            # "DENEN DE REDE R KOENIG" doesn't quite work
            pass
        break

# ============================================================
# 2. Check if REDE appears elsewhere
# ============================================================
print(f"\n{'='*60}")
print("2. REDE (SPEECH) OCCURRENCES")
print("=" * 60)

rede_count = 0
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = 0
    while True:
        idx = decoded.find('REDE', idx)
        if idx == -1:
            break
        ctx_s = max(0, idx-8)
        ctx_e = min(len(decoded), idx+12)
        codes_here = book_codes[idx:idx+4]
        print(f"  Book {bi:2d}: ...{decoded[ctx_s:ctx_e]}...")
        print(f"    REDE codes: {codes_here}")
        rede_count += 1
        idx += 1

print(f"\n  Total REDE: {rede_count}")

# ============================================================
# 3. Full text of LONGEST PIECES with manual segmentation
# ============================================================
print(f"\n{'='*60}")
print("3. LONG PIECE MANUAL SEGMENTATION")
print("=" * 60)

# Build superstring by overlap
# First, get all unique decoded texts
decoded_books = [(bi, decode(books[bi])) for bi in range(len(books))]

# Find the longest book
longest = max(decoded_books, key=lambda x: len(x[1]))
print(f"\n  Longest book: Book {longest[0]} ({len(longest[1])} chars)")
decoded = longest[1]
collapsed_text = collapse(decoded)
print(f"  Collapsed ({len(collapsed_text)} chars):")
print(f"  {collapsed_text}")

# Manual word-by-word segmentation attempt
# Strategy: mark all known word positions, then inspect gaps
known_words = sorted([
    'KOENIG', 'LABGZERAS', 'AUNRSONGETRASES', 'TOTNIURG',
    'HEARUCHTIGER', 'SCHWITEIO', 'TAUTR', 'EILCH', 'THARSC',
    'STEINEN', 'STEINE', 'STEIN', 'URALTE', 'FINDEN', 'FINDET',
    'WISSET', 'WISET', 'SCHAUN', 'RUNEORT', 'RUNEN', 'RUNE', 'RUIN',
    'DIESER', 'HWND', 'HIHL', 'LABRRNI', 'MINHEDDEM', 'MINHEDEM',
    'LHLADIZ', 'HECHLT', 'GEIGET', 'UTRUNR', 'ENDEUTRUNR',
    'STEH', 'IST', 'ICH', 'WIR', 'SIE', 'UND', 'FACH',
    'DIE', 'DER', 'DAS', 'DEN', 'DEM', 'DES', 'DENEN',
    'SEIN', 'SEINE', 'HIER', 'AUCH', 'NOCH', 'SEID',
    'NUN', 'GAR', 'EIN', 'ALLE', 'ORT', 'ERDE',
    'VIEL', 'TEIL', 'HAT', 'ERST', 'ERSTE', 'EIGEN',
    'TUN', 'ODE', 'NACH', 'VON', 'AUS', 'UNTER',
    'OEL', 'WIND', 'SEE', 'SEI', 'ENDE', 'REDE',
    'WEG', 'WIE', 'NEU', 'ALT', 'ALTE', 'TAG',
    'SO', 'AN', 'IN', 'ER', 'ES', 'AB', 'BIS',
    'WELT', 'GELT', 'HELD', 'HEIL', 'WEIL', 'NUR',
    'NICHT', 'WOHL', 'HEL', 'HELLE', 'GEH',
], key=len, reverse=True)

# Mark covered positions on collapsed text
covered = [False] * len(collapsed_text)
word_at = {}  # position -> word
for word in known_words:
    start = 0
    while True:
        idx = collapsed_text.find(word, start)
        if idx == -1:
            break
        # Only mark if not already covered by a longer word
        if not any(covered[idx:idx+len(word)]):
            for p in range(idx, idx+len(word)):
                covered[p] = True
            word_at[idx] = word
        start = idx + 1

# Build segmented output
result = []
i = 0
while i < len(collapsed_text):
    if i in word_at:
        w = word_at[i]
        result.append(f'[{w}]')
        i += len(w)
    else:
        result.append(collapsed_text[i])
        i += 1

print(f"\n  Segmented: {''.join(result)}")

# Count coverage
covered_count = sum(1 for c in covered if c)
print(f"\n  Coverage: {covered_count}/{len(collapsed_text)} = {100*covered_count/len(collapsed_text):.1f}%")

# Show uncovered gaps
print(f"\n  Uncovered gaps:")
gap_start = None
for i in range(len(covered)):
    if not covered[i]:
        if gap_start is None:
            gap_start = i
    else:
        if gap_start is not None:
            gap_text = collapsed_text[gap_start:i]
            if len(gap_text) >= 3:
                print(f"    pos {gap_start}-{i}: '{gap_text}'")
            gap_start = None
if gap_start is not None:
    gap_text = collapsed_text[gap_start:]
    if len(gap_text) >= 3:
        print(f"    pos {gap_start}-{len(collapsed_text)}: '{gap_text}'")

# ============================================================
# 4. VMTEGE: Test "IST VMT EGE VIEL" reading
# ============================================================
print(f"\n{'='*60}")
print("4. VMT EGE = VERMAG (=can/is able)?")
print("=" * 60)

# In MHG: VERMAC = can/is able to
# VERMAG = can (modern German)
# If VMT = VER-M-T... with some abbreviation...
# What if the whole sequence VMTEGE is a single word?
# VMTEGE reversed = EGETVMV -> nothing
# VMTEGE: could be a proper noun?
# Or: V = VOR (before)? VMT = VORMT? Nah.

# Let me look at the full context including what comes before IST
print("\n  Full contexts for 'IST VMT':")
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('ISTVMT')
    if idx != -1:
        ctx_s = max(0, idx-15)
        ctx_e = min(len(decoded), idx+25)
        print(f"    Book {bi:2d}: ...{decoded[ctx_s:ctx_e]}...")
        # What's before IST?
        before = decoded[max(0,idx-10):idx]
        print(f"      Before IST: '{before}'")

# ============================================================
# 5. Decode ALL books, collapse, build master text
# ============================================================
print(f"\n{'='*60}")
print("5. MASTER COLLAPSED TEXT (all unique segments)")
print("=" * 60)

# Get unique collapsed texts
unique_texts = set()
for bi in range(len(books)):
    decoded = decode(books[bi])
    collapsed = collapse(decoded)
    unique_texts.add(collapsed)

print(f"\n  Total unique collapsed texts: {len(unique_texts)}")

# Find the top 3 longest
sorted_texts = sorted(unique_texts, key=len, reverse=True)
for i, text in enumerate(sorted_texts[:3]):
    # Segment it
    cov = [False] * len(text)
    wat = {}
    for word in known_words:
        s = 0
        while True:
            idx = text.find(word, s)
            if idx == -1:
                break
            if not any(cov[idx:idx+len(word)]):
                for p in range(idx, idx+len(word)):
                    cov[p] = True
                wat[idx] = word
            s = idx + 1
    res = []
    j = 0
    while j < len(text):
        if j in wat:
            w = wat[j]
            res.append(f'[{w}]')
            j += len(w)
        else:
            res.append(text[j])
            j += 1
    cov_count = sum(1 for c in cov if c)
    print(f"\n  Text #{i+1} ({len(text)} chars, {100*cov_count/len(text):.1f}% covered):")
    segmented = ''.join(res)
    # Break into ~80 char lines
    for line_start in range(0, len(segmented), 75):
        print(f"    {segmented[line_start:line_start+75]}")

# ============================================================
# 6. Search for REDE in the correct position
# ============================================================
print(f"\n{'='*60}")
print("6. COLOPHON WORD BOUNDARY ANALYSIS")
print("=" * 60)

# The key question: DENENDEREDERKOENIG
# Could be: DENEN + DER + REDE + KOENIG (with REDE reading backwards)
# Or: DENEN + DER + EDER + KOENIG
# Let me check: what if we read REDE from the right?
# ...D-E-R-E-D-E-R-K-O-E-N-I-G
# Reversed locally: G-I-N-E-O-K-R-E-D-E-R-E-D
# That doesn't help.

# But wait: what about reading it as:
# D-E-N-E-N-D-E-R-E-D-E  | R-K-O-E-N-I-G
# DENENDEREDE | RKOENIG
# DENEN + DEREDE? Or DEN + ENDEREDE?
# ENDEREDE could be a MHG word? ENDERETE (ended)?

# Or: the simplest reading:
# DENEN + DER + REDE + R + KOENIG
# = "of those, of the speech [of] King"
# Where does REDE end? pos 5+3+4 = 12
# Then R at pos 12, then KOENIG at pos 13-18
# But that would require the text to be:
# D-E-N-E-N-D-E-R-R-E-D-E-R-K-O-E-N-I-G = DENENDERR EDERKOENIG
# That's not what we have. We have: DENENDEREDERKOENIG

# Let me trace the exact codes:
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('DENENDEREDERKOENIG')
    if idx != -1:
        codes = book_codes[idx:idx+18]
        print(f"\n  Book {bi}: DENENDEREDERKOENIG")
        print(f"  Codes: {codes}")
        for j, c in enumerate(codes):
            print(f"    pos {j:2d}: {c} = {mapping.get(c,'?')} = {decoded[idx+j]}")
        # Now: pos 0-4: DENEN = D-E-N-E-N
        #       pos 5-7: DER = D-E-R
        #       pos 8-11: EDER = E-D-E-R
        #       pos 12-17: KOENIG = K-O-E-N-I-G
        # So E at pos 8 is the pivot.
        # What if pos 5-7 is not DER but DE + R?
        # DE + REDE = DE REDE (the speech)?
        # D-E | R-E-D-E | R-K-O-E-N-I-G
        # = DE + REDE + R + KOENIG
        # But then: DENEN + DE + REDE + R + KOENIG
        # = "of whom the speech [of/the] King"
        print(f"\n  Possible readings:")
        print(f"    A: DENEN + DER + EDER + KOENIG")
        print(f"       'of those + of the + EDER + King'")
        print(f"    B: DENEN + DE + REDE + R + KOENIG")
        print(f"       'of those + the + speech + [R] + King'")
        print(f"    C: DENEN + DER + E + DER + KOENIG")
        print(f"       'of those + of the + [E] + of the + King'")
        print(f"    D: DENEN + DERE + DER + KOENIG")
        print(f"       'of those + of her(MHG) + of the + King'")
        break

# ============================================================
# 7. New word: GEIGET ES IN -- what follows?
# ============================================================
print(f"\n{'='*60}")
print("7. GEIGET ES IN... FULL TRACE")
print("=" * 60)

for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('GEIGETES')
    if idx != -1:
        ctx_s = max(0, idx-10)
        ctx_e = min(len(decoded), idx+30)
        print(f"  Book {bi:2d}: ...{decoded[ctx_s:ctx_e]}...")
        # GEIGETESINCHNESRER
        # GEIGET + ES + IN + CH + NESRER?
        # GEIGET + ES + INCH + NES + RER?
        # GEIGET + ESIN + CHNE + SRER?
        # In MHG: GEZEIGETES = "shown" (past participle + ES)
        # But our letters are clear: G-E-I-G-E-T
        # If GEIGET = shows/displays: "shows it in CH NESRER"
        # CH = part of a word?
        # NESRER = ?
        # Or: GEIGET + ES + INCH + NES + R + ER + SCE + AUS
        # INCH? Not German.
        # What about: ES IN CHNES = "it in [something]"
        # CHNES = ?
        # Or: ESIN = a name? CHNE = SCHNE (= snow)? In MHG: SNE = snow
        # GEIGET ES IN CHNESRER SCE AUS ENDE UTRUNR
        # = "shows/plays it in [?] [?] appears from end of utterance"

# ============================================================
# 8. New hypothesis: GEIGET = ZEIGET (shows)?
# ============================================================
print(f"\n{'='*60}")
print("8. GEIGET = ZEIGET? (G vs Z)")
print("=" * 60)

# G = codes 80, 84, 97
# Z = code 77
# What if code 97 is actually Z not G?
# GEIGET with code 97=Z: ZEIGET = ZEIGET = MHG "shows" (3rd person of ZEIGEN!)
# This would be a major finding if correct!
# ZEIGEN = to show
# ZEIGET = shows (MHG conjugation with -et ending)
# "ER ZEIGET ES" = "he shows it" -- PERFECT German!

# Check all uses of code 97
code97_contexts = []
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    for pos, c in enumerate(book_codes):
        if c == '97':
            ctx_s = max(0, pos-4)
            ctx_e = min(len(decoded), pos+5)
            code97_contexts.append((bi, pos, decoded[ctx_s:ctx_e]))

total_97 = len(code97_contexts)
print(f"\n  Code 97 currently = G, {total_97} occurrences")

# Show context distribution
before_97 = Counter()
after_97 = Counter()
for bi, pos, ctx in code97_contexts:
    decoded = decode(books[bi])
    if pos > 0:
        before_97[decoded[pos-1]] += 1
    if pos < len(decoded)-1:
        after_97[decoded[pos+1]] += 1

print(f"  Before code 97: {dict(before_97.most_common(8))}")
print(f"  After code 97:  {dict(after_97.most_common(8))}")

# If code 97 = Z, what words does it create?
print(f"\n  Testing code 97 as Z:")
for bi, book_codes in enumerate(books[:20]):
    original = decode(book_codes)
    modified = []
    for c in book_codes:
        if c == '97':
            modified.append('Z')
        else:
            modified.append(mapping.get(c, '?'))
    mod_text = ''.join(modified)

    # Find differences
    if original != mod_text:
        for pos in range(len(original)):
            if original[pos] != mod_text[pos]:
                ctx_s = max(0, pos-5)
                ctx_e = min(len(mod_text), pos+6)
                print(f"    Book {bi:2d} pos {pos}: ...{original[ctx_s:ctx_e]}... -> ...{mod_text[ctx_s:ctx_e]}...")
                break  # just first occurrence per book

# But wait - code 97 is the ONLY code for G?
# G codes: check
g_codes = [c for c, l in mapping.items() if l == 'G']
z_codes = [c for c, l in mapping.items() if l == 'Z']
print(f"\n  G codes: {g_codes}")
print(f"  Z codes: {z_codes}")

# If 97 = Z, then G has codes 80, 84 only
g80_count = sum(1 for b in books for c in b if c == '80')
g84_count = sum(1 for b in books for c in b if c == '84')
g97_count = sum(1 for b in books for c in b if c == '97')
z77_count = sum(1 for b in books for c in b if c == '77')
total_all = sum(len(b) for b in books)

print(f"\n  Code 80(G): {g80_count}x")
print(f"  Code 84(G): {g84_count}x")
print(f"  Code 97(G): {g97_count}x")
print(f"  Code 77(Z): {z77_count}x")
print(f"\n  Current G total: {g80_count+g84_count+g97_count} ({100*(g80_count+g84_count+g97_count)/total_all:.1f}%)")
print(f"  Current Z total: {z77_count} ({100*z77_count/total_all:.1f}%)")
print(f"  Expected G: 3.0%, Expected Z: 1.1%")
print(f"\n  If code 97=Z:")
print(f"    New G total: {g80_count+g84_count} ({100*(g80_count+g84_count)/total_all:.1f}%)")
print(f"    New Z total: {z77_count+g97_count} ({100*(z77_count+g97_count)/total_all:.1f}%)")

# ============================================================
# 9. Check code 97 in confirmed words
# ============================================================
print(f"\n{'='*60}")
print("9. CODE 97 IN CONFIRMED WORDS")
print("=" * 60)

# Does code 97 appear in any word that REQUIRES it to be G?
# Known words with G: KOENIG, LABGZERAS, TAG, WEG, GAR, GEH, EIGEN
# Let's check which G-code is used in each
for word in ['KOENIG', 'TAG', 'WEG', 'GAR', 'GEH', 'EIGEN', 'GEIGET']:
    for bi, book_codes in enumerate(books):
        decoded = decode(book_codes)
        idx = decoded.find(word)
        if idx != -1:
            word_codes = book_codes[idx:idx+len(word)]
            g_positions = [j for j, ch in enumerate(word) if ch == 'G']
            for gp in g_positions:
                g_code = word_codes[gp]
                print(f"  {word}: G at pos {gp} = code {g_code}")
            break

# ============================================================
# 10. Check if 97=Z creates LABZZERAS (LABZERAS with Z)
# ============================================================
print(f"\n{'='*60}")
print("10. IMPACT OF 97=Z ON PROPER NOUNS")
print("=" * 60)

# LABGZERAS: the G is important here!
# If 97=Z, LABGZERAS might change
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('LABGZERAS')
    if idx != -1:
        lab_codes = book_codes[idx:idx+9]
        print(f"  LABGZERAS codes: {lab_codes}")
        # Which code is the G?
        for j, ch in enumerate('LABGZERAS'):
            if ch == 'G':
                print(f"    G at pos {j}: code {lab_codes[j]}")
                if lab_codes[j] == '97':
                    print(f"    *** If 97=Z: LABZZERAS ***")
                else:
                    print(f"    Code {lab_codes[j]} (not 97)")
        break

# Also check GEIGET
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('GEIGET')
    if idx != -1:
        geiget_codes = book_codes[idx:idx+6]
        print(f"\n  GEIGET codes: {geiget_codes}")
        for j, ch in enumerate('GEIGET'):
            if ch == 'G':
                print(f"    G at pos {j}: code {geiget_codes[j]}")
        # If first G (code 97) = Z: ZEIGET
        # If second G (also 97?) = Z: ZEIZET? Or mixed?
        break

# ============================================================
# 11. TENTTUIGAA analysis
# ============================================================
print(f"\n{'='*60}")
print("11. TENTTUIGAA ANALYSIS")
print("=" * 60)

for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('TENTTUIGAA')
    if idx != -1:
        ctx_s = max(0, idx-10)
        ctx_e = min(len(decoded), idx+25)
        codes = book_codes[idx:idx+10]
        print(f"  Book {bi}: ...{decoded[ctx_s:ctx_e]}...")
        print(f"  Codes: {codes}")
        for j, c in enumerate(codes):
            print(f"    pos {j}: {c} = {mapping.get(c,'?')}")
        # TENTTUIGAA collapsed = TENTUIGA
        # With 97=Z: TENTTUIZAA -> collapsed TENTUIZA
        # Or: T-E-N-T-T-U-I-G-A-A
        # The TT is suspicious (doubled T)
        # Collapsed: T-E-N-T-U-I-G-A
        # What if we split: TENT + UIGA?
        # Or: TEN + T + TUIGA?
        # Or: T + ENT + TUIGA?
        # ENT- is a German separable prefix!
        # TUIGA = ?
        # With 97=Z: TENT + UIZA + A? or TEN + TUIZA + A?
        break

print(f"\n{'='*80}")
print("SESSION 10c COMPLETE")
print("=" * 80)
