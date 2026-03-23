"""
Session 9 - Deep attack on shorter solvable unknown patterns.
Strategy: contextual deduction + MHG/archaic German + Tibia lore.
"""
import json, re
from collections import Counter

with open('data/books.json') as f:
    raw_books = json.load(f)
with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)

def parse_codes(digit_str):
    return [digit_str[i:i+2] for i in range(0, len(digit_str), 2)]

books = [{'codes': parse_codes(b)} for b in raw_books]

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
print("DEEP ATTACK ON SHORT PATTERNS")
print("=" * 80)

# ============================================================
# 1. HWND: Could code 36 (W) actually be U in some positions?
# ============================================================
print("\n1. HWND -> HUND TEST")
print("-" * 60)
# Code 36 = W (84 uses). If we temporarily treat 36 as U:
# - HWND -> HUND (dog/hound) -- makes sense!
# - But W->U elsewhere would break everything
# Let's check: what % of code 36 occurrences are in HWND?
code_36_total = sum(1 for b in books for c in b['codes'] if c == '36')
code_36_in_hwnd = 6  # HWND appears 6 times
print(f"  Code 36 total: {code_36_total}, in HWND: {code_36_in_hwnd} ({code_36_in_hwnd/code_36_total*100:.1f}%)")
print(f"  Code 36 elsewhere: {code_36_total - code_36_in_hwnd}")
print(f"  Verdict: Can't change 36->U, it breaks 78 other positions")

# But what if 36 IS W and HWND is a MHG/archaic word?
# MHG "HUNT" = modern "HUND" (dog/hound)
# But W != U... unless the orthography is HWND = a variant spelling?
# In Old High German, /w/ was sometimes written where /u/ is expected
# e.g., OHG "hwaz" = modern "was" (what)
# OHG had an /hw/ cluster! HWND could be OHG "HUND" written with hw-!
print(f"\n  OHG HYPOTHESIS: 'HW' = /hw/ cluster (like 'hwaz' = 'was')")
print(f"  HWND could be OHG spelling of HUND (dog/hound)")
print(f"  'HUND FINDEN' = 'find the hound' -- fits narrative!")

# ============================================================
# 2. OEL: OEL or a verb?
# ============================================================
print("\n2. OEL ANALYSIS")
print("-" * 60)
# Context: "FACH HECHLLT ICH OEL SO DE[N]"
# Collapsed: "FACH HECHLT ICH OEL SO DEN"
# FACH = compartment/trade/profession
# HECHLT = from HECHELN (to hackle/to gasp)
# ICH = I
# OEL = ?
# If OE = OE: OEL = oil. "ICH OEL SO DEN..." = "I oil/anoint thus the..."
# But OEL as a VERB? OELEN = to oil. "ICH OELE" = I oil. But we have OEL not OELE.
# In MHG: "OLEN" = to oil/anoint. Stem: OL/OEL
# "ICH OEL SO DE GAR EN RUNE ORT" = "I anoint thus the enclosed rune-place"?
#
# ALTERNATIVE: What if we're splitting wrong?
# "HECHLLTICHOEL" -> "HECHELT ICH OEL" or "HECHLT + ICHOEL"?
# ICHOEL doesn't work. HECHLT ICH OEL is the better split.
#
# ANOTHER: In MHG, "WOEL" = "WOHL" (well). But our text is ICH OEL not WOEL.
#
# Best guess: OEL = OEL = oil/anoint (MHG verb form "OELEN")
print(f"  'ICH OEL SO DE GAR EN RUNE ORT'")
print(f"  = 'I anoint thus the enclosed rune-place'")
print(f"  OEL likely = OEL/OELEN (to oil/anoint), MHG verb stem")

# ============================================================
# 3. SCE -> SCHE? (common MHG digraph issue)
# ============================================================
print("\n3. SCE -> SCHE? ANALYSIS")
print("-" * 60)
# "ER SCE AUS" appears frequently
# Could SCE = SCHE? In MHG, SCH was sometimes written SC
# MHG "SC" = modern "SCH"! This is a key insight!
# So "ER SCE AUS" = "ER SCHE AUS" = ER SCHEINT AUS? (he appears from)
# But wait - we only have SCE, not SCEI or SCEIN
# "ER SCHE AUS" -> "ERSCHEINT AUS" if we read it as one word?
# Or: SC = SCH, so SCE = SCHE...
# Check: does the C in SCE use a C code or a CH digraph?
for i, book in enumerate(books):
    codes = book['codes']
    decoded = decode(codes)
    idx = decoded.find("SCEAUS")
    if idx != -1:
        sce_codes = codes[idx:idx+3]
        print(f"  Book {i}: SCE codes = {sce_codes}")
        print(f"    S={sce_codes[0]}({mapping[sce_codes[0]]})")
        print(f"    C={sce_codes[1]}({mapping[sce_codes[1]]})")
        print(f"    E={sce_codes[2]}({mapping[sce_codes[2]]})")
        # What letter is C code?
        c_code = sce_codes[1]
        print(f"    Code {c_code} mapped to: {mapping[c_code]}")
        # How many other codes map to C?
        print(f"    All C codes: {rev.get('C', [])}")
        break

# In MHG, "SC" = "SCH". So "ERSCE AUS" = "ERSCHE AUS"
# = "erscheint aus" (appears from)?
# But we're missing letters. Let me check wider context.
print("\n  All ER...SCE...AUS contexts:")
for i, book in enumerate(books):
    codes = book['codes']
    decoded = decode(codes)
    if "SCE" in decoded:
        idx = decoded.find("SCE")
        ctx_start = max(0, idx-12)
        ctx_end = min(len(decoded), idx+12)
        ctx = decoded[ctx_start:ctx_end]
        if "AUS" in ctx:
            print(f"    Book {i}: {ctx}")

# ============================================================
# 4. LABGZERAS breakdown
# ============================================================
print("\n4. LABGZERAS NAME ANALYSIS")
print("-" * 60)
# KOENIG LABGZERAS = King Labgzeras
# Let's check if this could be a compound:
# LAB + GZERAS
# LAB = rennet/lab (German)
# GZERAS = ?
# Reversed: SAREZGBAL = SAR + EZG + BAL?
# In Tibia: is there a King Labgzeras? Or related character?
# LABGZERAS reversed = SAREZGBAL
# What if we collapse: LABGZERAS -> same (no doubles)
# This is almost certainly a proper noun
for i, book in enumerate(books):
    codes = book['codes']
    decoded = decode(codes)
    idx = decoded.find("LABGZERAS")
    if idx != -1:
        lab_codes = codes[idx:idx+9]
        print(f"  Book {i}: LABGZERAS codes = {lab_codes}")
        for j, c in enumerate(lab_codes):
            print(f"    {decoded[idx+j]}: code {c}")
        break

# ============================================================
# 5. AUNRSONGETRASES breakdown
# ============================================================
print("\n5. AUNRSONGETRASES")
print("-" * 60)
# Always follows LABGZERAS or appears near KOENIG
# Could be a title/epithet
# AUN + R + SONGE + TRASES
# SONGE = song? (archaic?)
# Or: A + UNR + SON + GET + RASES
# UNREASON + GETRASES?
# Reversed: SESARTEGNOSRNUA
# Collapsed: AUNRSONGETRASES (no doubles)
print(f"  AUNRSONGETRASES (16 chars)")
print(f"  Collapsed: AUNRSONGETRASES")
print(f"  Reversed: SESARTEGNOSRNUA")
print(f"  Possible splits:")
print(f"    A-UNR-SON-GET-RASES")
print(f"    AUN-RSON-GET-RASES")
print(f"    AUNR-SONGE-TRASES")
print(f"    A-UN-R-SONGETRASES")

# ============================================================
# 6. TOTNIURG -> GRUINTOT analysis
# ============================================================
print("\n6. TOTNIURG = GRUINTOT")
print("-" * 60)
# Reversed: GRUINTOT
# GRUIN + TOT = Green Death? (MHG GRUEEN = green, TOT = death)
# Or RUIN + TOT with a G prefix? G-RUIN-TOT?
# In Tibia: there IS a place called "Green Claw Swamp",
# "Dark Cathedral" near bonelord areas
# GRUINTOT could be:
#   1. GRUENTOD = green death
#   2. GRUIN-TOT = ruin of death (GRUIN = archaic of RUIN?)
#   3. GRUEN + TOT = dead green (as in dead vegetation)
print(f"  TOTNIURG reversed = GRUINTOT")
print(f"  MHG GRUEEN = green -> GRUIN + TOT = 'green death'?")
print(f"  Or: G + RUIN + TOT = 'the ruin of death'")

# ============================================================
# 7. TAUTR and EILCH
# ============================================================
print("\n7. TAUTR IST EILCH AN HEARUCHTIGER")
print("-" * 60)
# "HIER TAUTR IST EILCH AN HEARUCHTIGER"
# = "Here Tautr is Eilch at Hearuchtiger"
# TAUTR: reversed = RTUAT. No obvious word.
# Could be a name. In Tibia: no known character named Tautr.
# EILCH: reversed = HCLIE. No obvious word.
# Could be a title or role.
# HEARUCHTIGER: contains GERUCHT (rumor) reversed? Or GERECHT (just)?
# HE + ARUCHT + IGER
# = the rumored one? The infamous one?
# Or: HERR + UCHTIG -> lord + powerful?
# ARUCHT in MHG doesn't exist as a standalone
# But BERUCHT-IGT = infamous! HE-ARUCHT-IGER?
# Wait: HEARTRUCHTIGER with collapsed doubles would be same
# Actually let me re-check: the text has HEARUCHTIGER, not HERRUCHTIGER
# H-E-A-R-U-C-H-T-I-G-E-R
# Could this be HE + ARUCHTIGER?
# RUCHTIGER = more infamous (comparative of RUCHTIG?)
# In MHG: RUECHTIG/RUCHTIG = famous/notorious
# So HEARUCHTIGER could be "the more notorious one"?
print(f"  TAUTR = proper noun (character/entity)")
print(f"  EILCH = title/role (meaning unclear)")
print(f"  HEARUCHTIGER: H-E-A-R-U-C-H-T-I-G-E-R")
print(f"    Possibly from MHG RUCHTIG (notorious/infamous)")
print(f"    = 'the notorious/infamous [place/person]'")

# ============================================================
# 8. SCHWITEIO
# ============================================================
print("\n8. SCHWITEIO")
print("-" * 60)
# "DEN DE SCHWITEIO" - appears at section boundaries
# SCH + W + ITEIO or SCHWIT + EIO
# Reversed: OIETIWHCS
# If MHG SC=SCH: SCHW + ITEIO
# SCHWITEIO could be: SCHWIT + EIO or SCHWEI + TIO?
# SCHWEIGEN = to be silent? SCHWEIT...
# Or: SCHWITE = archaic SCHWEITE (sweat/toil)?
# "DEN DE SCHWITEIO" = "the/that SCHWITEIO" -- likely closing formula
for i, book in enumerate(books):
    codes = book['codes']
    decoded = decode(codes)
    idx = decoded.find("SCHWITEIO")
    if idx != -1:
        ctx_start = max(0, idx-10)
        ctx_end = min(len(decoded), idx+12)
        sch_codes = codes[idx:idx+9]
        print(f"  Book {i}: {decoded[ctx_start:ctx_end]}")
        print(f"    Codes: {sch_codes}")
        for j, c in enumerate(sch_codes):
            print(f"      {decoded[idx+j]}: code {c}")
        break

# ============================================================
# 9. VMTG / VMT pattern - could V=F?
# ============================================================
print("\n9. VMT PATTERN DEEP ANALYSIS")
print("-" * 60)
# VMT appears 13 times. Contexts:
# "IST VMTEGE VIEL" -- VMTEGE = ?
# "EIGE VMT WIIE" -- ?
# What if V = F (MHG used V for F sound)?
# FMT? No...
# V codes: rev['V']
print(f"  V codes: {rev.get('V', [])}")
print(f"  M codes: {rev.get('M', [])}")
# What if code 83 (V) is actually something else?
# 83 is mapped to V. Let's check its frequency
v_count = sum(1 for b in books for c in b['codes'] if c == '83')
print(f"  Code 83 (V) total: {v_count}")
# In German, V is relatively rare. 83 appearing frequently might mean it's wrong
# What letter would make VMTEGE readable?
# If V->B: BMTEGE? No.
# If V->F: FMTEGE? No.
# If V->G: GMTEGE? No.
# If V->A: AMTEGE? No.
# What if it's reading order issue and VMT = a prefix?
# VER- is a common German prefix but V-M-T != V-E-R
# Unless M is wrong? But M is well-established.
#
# Let's check what "VMTEGE VIEL" could be:
# Collapsed: VMTEGE VIEL = VMTEGE VIEL
# If we read "E VMT EGE VIEL" -> "E VMT EGE VIEL"
# VIEL = much/many. So "...VMT EGE VIEL..." = "...? ? much..."
#
# What about code 04 = M? Is it really M?
m_code_04 = sum(1 for b in books for c in b['codes'] if c == '04')
print(f"  Code 04 (M) total: {m_code_04}")
# Show contexts of code 04
m_contexts = []
for i, book in enumerate(books):
    codes = book['codes']
    decoded = decode(codes)
    for pos, c in enumerate(codes):
        if c == '04':
            ctx_start = max(0, pos-2)
            ctx_end = min(len(decoded), pos+3)
            m_contexts.append(decoded[ctx_start:ctx_end])
unique_m = Counter(m_contexts).most_common(15)
print(f"  Code 04 (M) in context:")
for ctx, cnt in unique_m:
    print(f"    x{cnt:2d}: ...{ctx}...")

# ============================================================
# 10. STEH...HWND: try splitting at every position
# ============================================================
print("\n10. STEH...HWND EXHAUSTIVE SPLIT")
print("-" * 60)
seq = "WRLGTNELNRHELUIRUNN"  # Between STEH and HWND (without them)
print(f"  Core unknown: {seq} ({len(seq)} chars)")
print(f"  Collapsed: {collapse(seq)}")

# Try all splits into 2-5 parts
mhg_words = {
    'wir', 'wirt', 'wol', 'wort', 'wurm',
    'leit', 'liht', 'lant', 'luft',
    'gelt', 'got', 'gut', 'gern',
    'tur', 'tun', 'tot', 'teil',
    'nit', 'nie', 'not', 'nun', 'neln',
    'elt', 'eli', 'ein',
    'hel', 'her', 'hin', 'hunt',
    'rune', 'runen', 'ruin',
    'ir', 'in', 'un', 'er',
}

# Simple: try to find ANY known substring
print("\n  Known substrings found:")
for wlen in range(3, min(len(seq)+1, 8)):
    for start in range(len(seq) - wlen + 1):
        candidate = seq[start:start+wlen].lower()
        if candidate in mhg_words:
            print(f"    pos {start}-{start+wlen}: {seq[start:start+wlen]} ({candidate})")

# What about reading parts backwards?
rev_seq = seq[::-1]
print(f"\n  Reversed: {rev_seq}")
print(f"  Reversed collapsed: {collapse(rev_seq)}")
# Known substrings in reversed
for wlen in range(3, min(len(rev_seq)+1, 8)):
    for start in range(len(rev_seq) - wlen + 1):
        candidate = rev_seq[start:start+wlen].lower()
        if candidate in mhg_words:
            print(f"    rev pos {start}-{start+wlen}: {rev_seq[start:start+wlen]} ({candidate})")

# ============================================================
# 11. Frequency of each code in the FULL text
# ============================================================
print("\n11. CODE FREQUENCY DISTRIBUTION")
print("-" * 60)
code_freq = Counter()
for book in books:
    for c in book['codes']:
        code_freq[c] += 1

# Group by mapped letter
letter_freq = Counter()
for code, count in code_freq.items():
    letter = mapping.get(code, '?')
    letter_freq[letter] += count

total_letters = sum(letter_freq.values())
print(f"  Total codes: {total_letters}")
print(f"\n  Letter frequencies (our text vs expected German):")
german_freq = {
    'E': 17.4, 'N': 9.8, 'I': 7.6, 'S': 7.3, 'R': 7.0,
    'A': 6.5, 'T': 6.2, 'D': 5.1, 'H': 4.8, 'U': 4.2,
    'L': 3.4, 'C': 3.1, 'G': 3.0, 'M': 2.5, 'O': 2.5,
    'W': 1.9, 'B': 1.9, 'F': 1.7, 'K': 1.2, 'Z': 1.1,
    'V': 0.8, 'P': 0.7
}

for letter, count in sorted(letter_freq.items(), key=lambda x: -x[1]):
    our_pct = count / total_letters * 100
    exp_pct = german_freq.get(letter, 0)
    diff = our_pct - exp_pct
    flag = " <<<" if abs(diff) > 2.0 else ""
    print(f"    {letter}: {our_pct:5.1f}% (expected {exp_pct:4.1f}%, diff {diff:+5.1f}){flag}")

# ============================================================
# 12. Check for codes appearing only in unknown segments
# ============================================================
print("\n12. CODES THAT ONLY APPEAR IN UNKNOWN SEGMENTS")
print("-" * 60)
# If a code appears ONLY in contexts we can't read, it might be misassigned
# Check codes with very low frequency
rare_codes = [(code, count) for code, count in code_freq.items() if count <= 3]
for code, count in sorted(rare_codes, key=lambda x: x[1]):
    letter = mapping.get(code, '?')
    # Find all contexts
    contexts = []
    for i, book in enumerate(books):
        codes_list = book['codes']
        decoded = decode(codes_list)
        for pos, c in enumerate(codes_list):
            if c == code:
                ctx_start = max(0, pos-4)
                ctx_end = min(len(decoded), pos+5)
                contexts.append(f"Book{i}:{decoded[ctx_start:ctx_end]}")
    print(f"  Code {code:>2s} -> {letter} (x{count}): {'; '.join(contexts[:3])}")

print("\n" + "=" * 80)
print("SYNTHESIS")
print("=" * 80)
print("""
KEY DEDUCTIONS:

1. HWND = Old High German spelling of HUND (dog/hound)
   - OHG had /hw/ cluster (cf. hwaz -> was, hwerban -> werben)
   - "HUND FINDEN" = "find the hound" -- thematic fit with quest narrative

2. OEL = OEL/OELEN (to oil/anoint) -- MHG verb form
   - "ICH OEL SO DE GAR EN RUNE ORT" = "I anoint the enclosed rune-place"

3. SCE = MHG spelling of SCHE (modern SCH)
   - "ER SCE AUS" = "ER SCHE AUS" = "erscheint aus" (appears from)?
   - Or simply the SC->SCH orthography shift

4. HEARUCHTIGER = from MHG RUCHTIG (notorious/famous)
   - "the notorious one" -- a place or person epithet

5. TOTNIURG = GRUINTOT reversed = "Green Death" or "Ruin of Death"
   - MHG GRUEEN (green) + TOT (death)

6. STEH...HWND core "WRLGTNELNRHELUIRUNN" remains unsolved
   - 19 chars, no obvious German words
   - Likely contains proper nouns or heavily archaic vocabulary
""")
