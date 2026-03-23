"""
Session 10d - Deeper segmentation of remaining unknowns.
Targets:
  1. TENTTUIGAA ER GEIGET ES IN CHN ES RER -- full phrase parse
  2. UUISEMIV -- MHG reading attempt
  3. DNRHAUNRNVMHISDIZA -- MHG compound decomposition
  4. Try reading full narrative in order
  5. TEMDIA pattern
  6. LRSZTHK pattern
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
print("SESSION 10d: REMAINING UNKNOWNS")
print("=" * 80)

# ============================================================
# 1. Full phrase: ...TENTTUIGAA ER GEIGET ES IN CHN ES R ER...
# ============================================================
print("\n1. FULL PHRASE AROUND GEIGET")
print("-" * 60)

# Get the full context from longest book containing this
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('GEIGET')
    if idx != -1:
        # Get wide context
        ctx_s = max(0, idx-25)
        ctx_e = min(len(decoded), idx+40)
        full = decoded[ctx_s:ctx_e]
        codes_here = book_codes[ctx_s:ctx_e]

        print(f"  Book {bi}: ...{full}...")
        print(f"\n  Code-by-code:")
        for j in range(len(full)):
            c = codes_here[j] if j < len(codes_here) else '??'
            print(f"    pos {j:2d}: {c} = {full[j]}")

        collapsed_full = collapse(full)
        print(f"\n  Collapsed: {collapsed_full}")

        # Try manual word splits on collapsed
        # DEN GE ENDEN TENTUIGA ER GEIGET ES IN CHN ES RER
        # Or: DENGEENDENTENTUIGAERGEIGETESINCHNESSRER
        # Possible words:
        # DEN = the
        # ENDEN = ends/to end
        # GEIGET = plays/sounds
        # ES = it
        # IN = in
        # ER = he

        # What about TENTUIGA?
        # TEN + TUIGA?
        # TENT + UIGA?
        # In MHG: TUGE = virtue (variant of TUGENT)?
        # TUIGE = ? TUIG = ZEUG (stuff) in dialect?
        # TENTUIGA reversed = AGIUTNET
        # What about: T + ENT + UI + GA?
        # ENT- prefix + UI + GA?

        print(f"\n  Segmentation attempts:")
        print(f"    A: DEN GE-ENDEN TENT-UIGA ER GEIGET ES IN CHN ES RER")
        print(f"    B: DEN GEENDEN-TENT-UIGA-ER GEIGET ES IN CHN-ES-RER")
        print(f"    C: DENGE + ENDEN + TENTUIGA + ER + GEIGET + ES + IN + CHN + ES + R + ER")
        print(f"    D: DEN + GEN + DEN + TENTUIGA + ER + GEIGET + ES + IN + CHNES + RER")
        break

# ============================================================
# 2. CHN pattern -- what is CHN?
# ============================================================
print(f"\n{'='*60}")
print("2. CHN ANALYSIS")
print("=" * 60)

# CH is the MHG digraph (= SCH or CH in modern German)
# CHN: CH + N? or C + HN?
# In MHG: CHN doesn't occur often. But CHNE could be = KEINE?
# Or: it's a word boundary: ...IN CH-N...
# where CH = part of next word, N = start after that

# Check what comes after GEIGET ES IN:
print("\n  After 'GEIGETESIN':")
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('GEIGETESIN')
    if idx != -1:
        rest = decoded[idx+10:idx+25]
        rest_codes = book_codes[idx+10:idx+25]
        print(f"  Book {bi}: GEIGETESIN + '{rest}'")
        for j, c in enumerate(rest_codes[:8]):
            print(f"    {c} = {mapping.get(c, '?')}")
        break

# ============================================================
# 3. UUISEMIV deep analysis
# ============================================================
print(f"\n{'='*60}")
print("3. UUISEMIV (collapsed: UISEMIV)")
print("=" * 60)

# Context: TEMDIA ES UUISEMIV DENGINSA UUII
# Codes: 43-44-21-59-56-04-21-83 = U-U-I-S-E-M-I-V
# Reversed: VIMESIU -> VIMESIU

# What if we read the full context?
# "DHER TEMDIA ES UUISEMIV DENGINSA UUII"
# DHER = DER (the)?
# TEMDIA = TEM + DIA? Or TEMDI + A?
# DEN GINSA = DEN + GINSA? GINSAU = ?

print("\n  Full UUISEMIV contexts with codes:")
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('UUISEMIV')
    if idx != -1:
        ctx_s = max(0, idx-15)
        ctx_e = min(len(decoded), idx+20)
        ctx = decoded[ctx_s:ctx_e]
        collapsed = collapse(ctx)
        print(f"  Book {bi}: {ctx}")
        print(f"           {collapsed}")
        # Just first 3
        if bi > 55:
            break

# TEMDIA codes
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('TEMDIA')
    if idx != -1:
        codes = book_codes[idx:idx+6]
        print(f"\n  TEMDIA codes: {codes}")
        for j, c in enumerate(codes):
            print(f"    {c} = {mapping.get(c,'?')}")

        # What if: TEM + DIA? Or TE + MDIA?
        # TEMDIA reversed = AIDMET
        # In MHG: TEMDIA could be TEM(= DEM = the) + DIA?
        # Wait: code 78=T, 30=E, 40=M, 42=D, 15=I, 85=A
        # TEM = ? or TEME = ?
        # What about: T + EM + DIA? EM = MHG "ihm" (him)
        # "T EM DIA ES UISE MIV" = "? him ? it wise my?"
        # Hmm

        # What if TEMDIA is actually TEM DIA = DEM DIA?
        # T and D are different codes (78 vs 42), so T is genuine
        # But: TEMDIA could contain MEDIA?
        # T + MEDIA? Not in German
        # Or: TE(M) + DIA = ? + DIA(=DIA? Slavic for "for"?)
        break

# ============================================================
# 4. DNRHAUNRNVMHISDIZA full decomposition
# ============================================================
print(f"\n{'='*60}")
print("4. DNRHAUNRNVMHISDIZA DECOMPOSITION")
print("=" * 60)

# Full context: KELSEIDEN DNRHAUNRN VMHISDIZA RUNE DUNTERLAUS
# Codes: 45-14-51-94-85-61-14-51-90-83-04-57-65-12-28-21-77-35

for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('DNRHAUNRNVMHISDIZA')
    if idx != -1:
        ctx_s = max(0, idx-12)
        ctx_e = min(len(decoded), idx+30)
        codes = book_codes[idx:idx+18]
        print(f"  Book {bi}: ...{decoded[ctx_s:ctx_e]}...")
        print(f"\n  Full codes:")
        for j, c in enumerate(codes):
            print(f"    pos {j:2d}: {c} = {mapping.get(c,'?')}")

        # Split attempts on collapsed:
        collapsed = collapse('DNRHAUNRNVMHISDIZA')
        print(f"\n  Collapsed: {collapsed}")

        # DNRHAUNRN + VMHISDIZA
        # Or: DNR + HAUNRN + VMH + ISDIZA
        # Or: D + NR + HAUN + RN + VMHI + SDIZA
        # Or: DEN + RHAUNRN + VMH + IS + DIZA
        # DIZA reversed = AZID
        # SDIZA reversed = AZIDS

        # MHG possibilities:
        # HAUN = hauwen (to strike/chop)
        # VMH = ?
        # ISDIZA = IS + DIZA
        # IS = ist (is)? Or just "is"
        # DIZA = DIZA (name)? or DITZE (MHG = "this")?

        # In MHG: DITZE / DITZ = "this" (demonstrative)
        # SDIZA could be S + DIZA
        # "HAUN RN VMH IS DIZA" = "strike ? ? is this"?
        # Or: "IS DIZA" = "is this"?

        # VMHIS: V + MH + IS?
        # MH doesn't occur in German normally
        # Unless: VM + HIS = ? + HIS
        # HIS = HIES (was called, MHG preterite of HEIZEN)?
        # VM + HISDIZA = ? + "was-called-this"?

        print(f"\n  MHG segmentation attempts:")
        print(f"    A: DNR + HAUN + RN + VMH + IS + DIZA")
        print(f"       '? + strike + ? + ? + is + this(MHG DITZ)?'")
        print(f"    B: D + NR + HAUNRN + VM + HIS + DIZA")
        print(f"       '[d] + [nr] + striking + ? + hies(=called MHG) + this?'")
        print(f"    C: DEN + RHAUNRN + VMHIS + DIZA")
        print(f"    D: DNR + HAUN + RN + V + MHIS + DIZA")
        break

# ============================================================
# 5. Attempt full narrative reading (longest piece)
# ============================================================
print(f"\n{'='*60}")
print("5. FULL NARRATIVE READING ATTEMPT")
print("=" * 60)

# Book 10 is one of the longest and most complete
bi = 10
decoded = decode(books[bi])
collapsed = collapse(decoded)
print(f"\n  Book 10 collapsed ({len(collapsed)} chars):")
print(f"  {collapsed}")

# Manual word-by-word reading:
# MISEINDGEDASIEOVIRUNEAUIENERDENGENDENTENTUIGA
# ERGEIGETESINCHNESRERSCEAUSENDEUTRUNRDENENDEREDER
# KOENIGLABGZERASUNENITGHNEAUNRSONGETRASES RW?

print(f"\n  Manual word-by-word reading:")
print(f"    MI SEIN DGEDA SIE OWI RUNE AUIEN ER DEN GEN DEN")
print(f"    TENTUIGA ER GEIGET ES IN CHN ES R ER SCE AUS")
print(f"    ENDE UTRUNR DENEN DER REDE R KOENIG LABGZERAS")
print(f"    UNENITGHNE AUNRSONGETRASES RW")

# German interpretation attempt:
print(f"\n  German interpretation:")
print(f"    MI(=mein) SEIN DGEDA SIE OWI RUNE(=Runen)")
print(f"    AUIEN(=?) ER(=he) DEN GEN DEN")
print(f"    TENTUIGA(=?) ER(=he) GEIGET(=plays/shows) ES(=it)")
print(f"    IN CHN(=?) ES(=it) R(=?) ER(=he) SCE(=SCHE=erscheint)")
print(f"    AUS(=from) ENDE(=end) UTRUNR(=utterance)")
print(f"    DENEN(=those) DER(=of the) REDE(=speech) R(=?)")
print(f"    KOENIG(=king) LABGZERAS UNENITGHNE AUNRSONGETRASES")

# ============================================================
# 6. DGEDA, OWI, AUIEN patterns
# ============================================================
print(f"\n{'='*60}")
print("6. SHORT UNKNOWN PATTERNS")
print("=" * 60)

patterns = ['DGEDA', 'OWI', 'AUIEN', 'LRSZTHK', 'URIHWNRS',
            'SCUIT', 'RLAUNR', 'OIAITOE', 'NESRER',
            'ENGCHD', 'TIUMENGEMI', 'ADAIEB']

for pat in patterns:
    count = 0
    example_ctx = None
    for bi, book_codes in enumerate(books):
        decoded = decode(book_codes)
        if pat in decoded:
            count += 1
            if example_ctx is None:
                idx = decoded.find(pat)
                ctx_s = max(0, idx-6)
                ctx_e = min(len(decoded), idx+len(pat)+6)
                example_ctx = decoded[ctx_s:ctx_e]
                # Get codes
                codes_pat = book_codes[idx:idx+len(pat)]

    if count > 0:
        collapsed_pat = collapse(pat)
        print(f"\n  {pat} ({count}x)  collapsed: {collapsed_pat}")
        print(f"    Context: ...{example_ctx}...")
        if codes_pat:
            code_str = '-'.join(f'{c}({mapping.get(c,"?")})' for c in codes_pat)
            print(f"    Codes: {code_str}")

        # Try MHG decomposition
        # DGEDA: D-G-E-D-A -> in MHG? GEDACHT reversed is THCADEG
        # OWI: O-W-I = OWI? In Tibia, OWI? Or OHG form?
        # AUIEN: A-U-I-E-N = AUIEN? Or AU-IEN?
        # LRSZTHK: very consonant-heavy, likely proper noun
        # URIHWNRS: contains HWND variant? HWN = OHG form
        # NESRER: NES + RER? Or NESRER = ?
        # TIUMENGEMI: TIUM + EN + GEMI? Or TI + UMENGE + MI?

# ============================================================
# 7. URIHWNRS - contains HWN (OHG cluster!)
# ============================================================
print(f"\n{'='*60}")
print("7. URIHWNRS - OHG HWN CLUSTER")
print("=" * 60)

# HWND = OHG HUND (dog). Does HWN here relate?
# URIHWNRS: U-R-I-H-W-N-R-S
# Split: URI + HWNR + S? Or UR + IHWN + RS?
# HWNR could be HWN + R
# URI reversed = IRU (OHG "their")
# "IRU HWN RS" = "their dog/hound [?]"?

for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('URIHWNRS')
    if idx != -1:
        ctx_s = max(0, idx-10)
        ctx_e = min(len(decoded), idx+15)
        codes = book_codes[idx:idx+8]
        print(f"  Book {bi}: ...{decoded[ctx_s:ctx_e]}...")
        print(f"  Codes:")
        for j, c in enumerate(codes):
            total = sum(1 for b in books for x in b if x == c)
            print(f"    pos {j}: {c} = {mapping.get(c,'?')} ({total}x)")

        # Context: "WIR URI HWNR S IST VMT EGE VIEL"
        # = "we ? OHG-hound-? is VMT EGE much"?
        # Or: "WIR URIHWNRS IST VMTEGE VIEL"
        # What if URIHWNRS = ? + HWND-variant + S?
        # URI = origin/source?
        # HWNRS = HWNR + S (genitive?)
        break

# ============================================================
# 8. Try reading OIAITOE
# ============================================================
print(f"\n{'='*60}")
print("8. OIAITOE = OI + AI + TOE?")
print("=" * 60)

# Full context from Book 3: OIAITOEMENDGEMKMTGRSCASEZSTEIE
# OIAITOE + MEND + GE + MKMTGRSCASEZ + STEIE
# Or: OI + AI + TOE + MEND + GEMKMTGRSCASEZ + STEIE
# MEND = ? GEMKMTGRSCASEZ = ?
# STEIE = STEI + E = STEINE with missing N?

for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('OIAITOE')
    if idx != -1:
        ctx_s = max(0, idx-8)
        ctx_e = min(len(decoded), idx+30)
        codes = book_codes[idx:idx+7]
        print(f"  Book {bi}: ...{decoded[ctx_s:ctx_e]}...")
        print(f"  Codes:")
        for j, c in enumerate(codes):
            print(f"    pos {j}: {c} = {mapping.get(c,'?')}")
        collapsed = collapse('OIAITOE')
        print(f"  Collapsed: {collapsed}")
        # OIAITOE collapsed = OIAITOE (no doubles)
        # Try reversed: EOTIAIOE? No that's wrong
        # Reversed: EOTIAIO
        # What about: OI + AITOE or OIA + ITOE?
        # In MHG: "ouch" = also, "ode" = or
        # What if O = end of previous word, IAITOE = ?
        # IAITOE reversed = EOTIAI
        break

# ============================================================
# 9. Statistics update
# ============================================================
print(f"\n{'='*60}")
print("9. UPDATED COVERAGE STATISTICS")
print("=" * 60)

# Count how many total chars are in recognized words
total_chars = 0
covered_chars = 0
all_known = [
    'KOENIG', 'LABGZERAS', 'AUNRSONGETRASES', 'TOTNIURG',
    'HEARUCHTIGER', 'SCHWITEIO', 'TAUTR', 'EILCH', 'THARSC',
    'STEINEN', 'STEINE', 'STEIN', 'URALTE', 'FINDEN',
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
]

# Sort by length descending for greedy matching
all_known_sorted = sorted(set(all_known), key=len, reverse=True)

for bi in range(len(books)):
    decoded = decode(books[bi])
    collapsed = collapse(decoded)
    total_chars += len(collapsed)

    covered = [False] * len(collapsed)
    for word in all_known_sorted:
        start = 0
        while True:
            idx = collapsed.find(word, start)
            if idx == -1:
                break
            if not any(covered[idx:idx+len(word)]):
                for p in range(idx, idx+len(word)):
                    covered[p] = True
            start = idx + 1
    covered_chars += sum(1 for c in covered if c)

print(f"\n  Total collapsed chars: {total_chars}")
print(f"  Covered by known words: {covered_chars}")
print(f"  Coverage: {100*covered_chars/total_chars:.1f}%")
print(f"  Uncovered: {total_chars - covered_chars} chars")

# Count unique German words found
german_words_found = set()
proper_nouns_found = set()
proper = {'KOENIG', 'LABGZERAS', 'AUNRSONGETRASES', 'TOTNIURG',
          'HEARUCHTIGER', 'SCHWITEIO', 'TAUTR', 'EILCH', 'THARSC',
          'HIHL', 'LABRRNI', 'MINHEDDEM', 'MINHEDEM', 'LHLADIZ',
          'HWND', 'RUNEORT', 'UTRUNR'}

for word in all_known_sorted:
    for bi in range(len(books)):
        decoded = decode(books[bi])
        collapsed = collapse(decoded)
        if word in collapsed:
            if word in proper:
                proper_nouns_found.add(word)
            else:
                german_words_found.add(word)
            break

print(f"\n  German words confirmed: {len(german_words_found)}")
print(f"  Proper nouns: {len(proper_nouns_found)}")
print(f"  Total vocabulary: {len(german_words_found) + len(proper_nouns_found)}")

# Show newly found words since session 9
new_words = {'REDE', 'GEIGET', 'WIE', 'SEI', 'UNTER', 'ENDE', 'WELT',
             'HEIL', 'WEIL', 'NUR', 'ENDEUTRUNR', 'EIGEN'}
actually_found = set()
for w in new_words:
    for bi in range(len(books)):
        decoded = decode(books[bi])
        collapsed = collapse(decoded)
        if w in collapsed:
            actually_found.add(w)
            break

print(f"\n  New words found in Session 10:")
for w in sorted(actually_found):
    print(f"    {w}")

print(f"\n{'='*80}")
print("SESSION 10d COMPLETE")
print("=" * 80)
