"""
Session 10b - Deep attack on specific patterns.
Key insights from 10a:
  - WRLGTNELNRHELUIRUNN has rare codes (24=R 35x, 49=E 17x, 55=R 26x)
  - WIIE = WIE (how) collapsed
  - GEIGET appears 6x -- could be MHG verb form
  - The 40-char monster needs systematic segmentation
  - SEII = SEI (be!) collapsed
  - GE- is a German prefix before VMT
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
print("SESSION 10b: TARGETED PATTERN ATTACKS")
print("=" * 80)

# ============================================================
# 1. Verify rare codes 24, 49, 55 in confirmed words
# ============================================================
print("\n1. RARE CODE VERIFICATION")
print("-" * 60)

# Check if codes 24, 49, 55 appear in ANY confirmed German word
confirmed_words = ['STEH', 'STEIN', 'STEINE', 'STEINEN', 'URALTE',
                   'DIE', 'DER', 'DAS', 'DEN', 'DEM', 'DES',
                   'IST', 'ICH', 'WIR', 'SIE', 'UND', 'FINDEN',
                   'SEIN', 'SEINE', 'DIESER', 'HIER', 'AUCH',
                   'NOCH', 'KOENIG', 'WISSET', 'SCHAUN', 'RUIN',
                   'RUNE', 'RUNEN', 'SEID', 'NUN', 'GAR',
                   'EIN', 'ALLE', 'FACH', 'ORT', 'ERDE',
                   'VIEL', 'TEIL', 'HAT', 'ERST', 'ERSTE',
                   'TUN', 'ODE', 'NACH', 'VON', 'AUS',
                   'HECHLT', 'OEL', 'HWND', 'WIND']

rare_codes = ['24', '49', '55']
for rc in rare_codes:
    letter = mapping[rc]
    total = sum(1 for b in books for c in b if c == rc)
    print(f"\n  Code {rc} = {letter} ({total}x total)")

    # Find it in any confirmed word context
    found_in_word = False
    for bi, book_codes in enumerate(books):
        decoded = decode(book_codes)
        for pos, c in enumerate(book_codes):
            if c == rc:
                # Check 5-char window for confirmed words
                for wlen in range(3, 10):
                    for offset in range(wlen):
                        start = pos - offset
                        if start >= 0 and start + wlen <= len(decoded):
                            window = decoded[start:start+wlen]
                            if window in confirmed_words:
                                found_in_word = True
                                print(f"    CONFIRMED: Book {bi} pos {pos} in '{window}'")
                                break
                    if found_in_word:
                        break
                if found_in_word:
                    break
        if found_in_word:
            break

    if not found_in_word:
        print(f"    NOT found in any confirmed word!")
        # Show all contexts
        print(f"    All contexts (up to 10):")
        count = 0
        for bi, book_codes in enumerate(books):
            decoded = decode(book_codes)
            for pos, c in enumerate(book_codes):
                if c == rc:
                    ctx_s = max(0, pos-4)
                    ctx_e = min(len(decoded), pos+5)
                    ctx = decoded[ctx_s:ctx_e]
                    marker = pos - ctx_s
                    display = ctx[:marker] + '[' + ctx[marker] + ']' + ctx[marker+1:]
                    print(f"      Book {bi:2d}: {display}")
                    count += 1
                    if count >= 10:
                        break
            if count >= 10:
                break

# ============================================================
# 2. Test if code 49 could be a different letter
# ============================================================
print(f"\n{'='*60}")
print("2. CODE 49 ALTERNATIVE MAPPING TEST")
print("=" * 60)

# Code 49 = E but only 17 occurrences. Could be wrong.
# What letters are underrepresented? B(0.4%), F(0.3%), K(0.4%), P(missing)
# Test each alternative
code49_contexts = []
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    for pos, c in enumerate(book_codes):
        if c == '49':
            ctx_s = max(0, pos-6)
            ctx_e = min(len(decoded), pos+7)
            before = decoded[max(0,pos-3):pos]
            after = decoded[pos+1:min(len(decoded),pos+4)]
            code49_contexts.append((bi, pos, before, after, decoded[ctx_s:ctx_e]))

print(f"\n  Code 49 ({len(code49_contexts)} occurrences):")
print(f"  Currently mapped to: E")
for bi, pos, before, after, ctx in code49_contexts:
    print(f"    Book {bi:2d}: ...{ctx}...")

# What letters would make these contexts better?
# In the garbled core: ...RH[49]LU... = RH_LU
# If 49=A: RHALU -- not obvious
# If 49=O: RHOLU -- not obvious
# If 49=B: RHBLU -- no
# If 49=Y: RHYLU -- no
# Let's check bigrams
before_49 = Counter()
after_49 = Counter()
for bi, pos, before, after, ctx in code49_contexts:
    decoded = decode(books[bi])
    if pos > 0:
        before_49[decoded[pos-1]] += 1
    if pos < len(decoded)-1:
        after_49[decoded[pos+1]] += 1

print(f"\n  Before code 49: {dict(before_49.most_common())}")
print(f"  After code 49: {dict(after_49.most_common())}")

# ============================================================
# 3. The 40-char monster: systematic deconstruction
# ============================================================
print(f"\n{'='*60}")
print("3. 40-CHAR MONSTER SEGMENTATION")
print("=" * 60)

monster = 'EUGENDRTHENAEDEULGHLWUOEHSGSEIIGEVMTWIIE'
collapsed_monster = collapse(monster)
print(f"\n  Full: {monster}")
print(f"  Collapsed: {collapsed_monster}")
print(f"  Length: {len(monster)} / {len(collapsed_monster)}")

# Get the codes
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find(monster)
    if idx != -1:
        monster_codes = book_codes[idx:idx+len(monster)]
        print(f"\n  Codes (Book {bi}):")
        for j in range(0, len(monster_codes), 10):
            chunk = monster_codes[j:j+10]
            letters = [mapping.get(c, '?') for c in chunk]
            line = ' '.join(f'{c}={l}' for c, l in zip(chunk, letters))
            print(f"    pos {j:2d}: {line}")
        break

# Systematic segmentation with collapsed doubles
print(f"\n  Manual segmentation attempts on collapsed:")
c = collapsed_monster
print(f"  {c}")

# Approach: look for known words and GE- prefixes
# EUGENDRTHENAEDEULGHLWUOEHSGSEIGEVMTWIE
# E-UGEND-R-THEN-AE-DE-ULGHL-WUO-EH-SGSEI-GE-VMT-WIE
# UGEND could be TUGEND (virtue) - but starts with E!
# THEN = then?
# Let me try differently:
# EU-GEND-R-T-HENA-EDE-ULGHL-WUO-EHS-GSEI-GE-VMT-WIE

# WIE = how (MHG)
# SEII -> SEI (be!) -- GE-SEI? Nah
# GE + VMT = GEVMT?
# SGSEIIGE -> S-G-SEI-IGE or SG-SEII-GE
# SGS = ?
# OEHSG = ?
# WUOEH = WUO + EH?
# WUO = MHG "wo" (where)?? In MHG, "wa" or "wo" were used. WUO is unusual.
# Actually in OHG: "wuo" could be a form of "wo" (where)!

# Let me try: EUGEND + RTHEN + AEDE + ULGHL + WUO + EHSG + SEII + GE + VMT + WIIE
# Or: E + UGEND + R + THEN + AE + DE + UL + GHL + WUO + EH + SG + SEII + GE + VMT + WIIE

# GHL: in OHG, GHL doesn't exist. But HL does (OHG cluster).
# ULGHL = UL + GHL? Or ULG + HL?

# What about reading as phrases?
# "...DE ULG HL WUO EHS GS EII GE VMT WIE..."
# EHS = ?
# Or: "DE ULGHL WUO EHSG SEII GE VMT WIIE"

print(f"\n  Key subword analysis:")
print(f"  WIIE = WIE (how/as) with doubled I")
print(f"  SEII = SEI (be!) with doubled I")
print(f"  GE = common prefix")
print(f"  VMT = V-M-T (unresolved, see section 8)")
print(f"  AEDE = AE (=OE?) + DE")
print(f"  RTHEN = R + THEN? Or R-THEN?")

# Check if THEN appears elsewhere
then_count = 0
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    if 'THEN' in decoded:
        then_count += 1
print(f"\n  THEN appears in {then_count} books")

# Check WUO
wuo_count = 0
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    if 'WUO' in decoded:
        wuo_count += 1
print(f"  WUO appears in {wuo_count} books")

# ============================================================
# 4. GEIGET = German verb form?
# ============================================================
print(f"\n{'='*60}")
print("4. GEIGET ANALYSIS")
print("=" * 60)

geiget_contexts = []
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('GEIGET')
    if idx != -1:
        ctx_s = max(0, idx-12)
        ctx_e = min(len(decoded), idx+18)
        geiget_contexts.append((bi, idx, decoded[ctx_s:ctx_e]))

print(f"\n  GEIGET occurrences: {len(geiget_contexts)}")
for bi, idx, ctx in geiget_contexts[:6]:
    print(f"    Book {bi:2d}: ...{ctx}...")

# In MHG:
# GEIGEN = to play the fiddle
# GEIGT = plays fiddle (3rd person)
# But GEI-GET: what if this is GE-IGET?
# GE- prefix + IGET?
# Or: GEIG + ET (suffix)?
# In MHG: past participle GE- + root + -ET
# GEIGET = past participle of GEIGEN? "fiddled/played"?
# Actually MHG pp would be GEGEIGT not GEIGET
# Unless GEIGET = someone's name?

# ============================================================
# 5. UUISEMIV deconstruction
# ============================================================
print(f"\n{'='*60}")
print("5. UUISEMIV ANALYSIS")
print("=" * 60)

uuisemiv_contexts = []
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('UUISEMIV')
    if idx != -1:
        ctx_s = max(0, idx-12)
        ctx_e = min(len(decoded), idx+20)
        codes = book_codes[idx:idx+8]
        uuisemiv_contexts.append((bi, idx, decoded[ctx_s:ctx_e], codes))

print(f"\n  UUISEMIV occurrences: {len(uuisemiv_contexts)}")
for bi, idx, ctx, codes in uuisemiv_contexts[:5]:
    print(f"    Book {bi:2d}: ...{ctx}...")

if uuisemiv_contexts:
    codes = uuisemiv_contexts[0][3]
    print(f"\n  Codes: {codes}")
    for j, c in enumerate(codes):
        print(f"    pos {j}: {c} = {mapping.get(c,'?')}")

    collapsed = collapse('UUISEMIV')
    print(f"\n  Collapsed: {collapsed}")
    # UISEMIV
    # What if read as: UISE + MIV?
    # Or: U + WISE + MIV?
    # WEISE (wise) = W-E-I-S-E, but we have U-I-S-E
    # What about: UU + ISE + MI + V?
    # ISE = MHG for "ice"?
    # MIV = ?
    # Or reversed: VIMESIU -> VIMESIU
    # Or: UUISE + MI + V
    # UUISE = WEISE (wise/manner) with UU=W? No, UU are separate codes 43,44
    # But wait: codes 43=U, 44=U -- these are both U codes, not W
    # What if one of them is actually W? Code 43 or 44?
    # W codes: 33, 36, 87
    # U codes: 43, 44, 61, 70
    # Hmm, 4 U codes seems like a lot for a letter at 4.2%
    # Code 43: 36 uses. Code 44: 30 uses.

# ============================================================
# 6. Full narrative flow - book by book
# ============================================================
print(f"\n{'='*60}")
print("6. NARRATIVE FLOW (first 5 books)")
print("=" * 60)

for bi in range(min(5, len(books))):
    decoded = decode(books[bi])
    collapsed_text = collapse(decoded)
    print(f"\n  Book {bi} ({len(decoded)} chars):")
    print(f"    {collapsed_text}")

    # Auto-segment with expanded word list
    words_found = []
    text = collapsed_text
    known = ['KOENIG', 'LABGZERAS', 'AUNRSONGETRASES', 'TOTNIURG',
             'HEARUCHTIGER', 'SCHWITEIO', 'TAUTR', 'EILCH', 'THARSC',
             'HIHL', 'LABRRNI', 'MINHEDDEM', 'MINHEDEM', 'RUNEORT',
             'UTRUNR', 'HWND', 'LHLADIZ',
             'STEH', 'STEIN', 'STEINE', 'STEINEN', 'URALTE',
             'DIE', 'DER', 'DAS', 'DEN', 'DEM', 'DES',
             'IST', 'ICH', 'WIR', 'SIE', 'UND', 'FINDEN',
             'SEIN', 'SEINE', 'DIESER', 'HIER', 'AUCH',
             'NOCH', 'KOENIG', 'WISET', 'WISSET', 'SCHAUN', 'RUIN',
             'RUNE', 'RUNEN', 'SEID', 'NUN', 'GAR',
             'EIN', 'ALE', 'ALLE', 'FACH', 'ORT', 'ERDE',
             'VIEL', 'TEIL', 'HAT', 'ERST', 'ERSTE',
             'TUN', 'ODE', 'NACH', 'VON', 'AUS',
             'HECHLT', 'OEL', 'WIND', 'GEIGET',
             'SEE', 'SEI', 'ENDE', 'REDE', 'UNTER',
             'WEG', 'WIE', 'NEU', 'ALT', 'ALTE',
             'SO', 'AN', 'IN', 'ER', 'ES', 'AB',
             'BIS', 'TAG', 'DENEN', 'EIGEN',
             'GELT', 'WELT', 'HELD', 'HEIL', 'TEIL',
             'WEIL', 'NUR', 'NICHT', 'WOHL',
             'HEL', 'HELLE', 'GEH', 'STEH']
    for w in sorted(known, key=len, reverse=True):
        start = 0
        while True:
            idx = text.find(w, start)
            if idx == -1:
                break
            words_found.append((idx, w))
            start = idx + 1

    words_found.sort()
    if words_found:
        word_strs = [f'{w}@{p}' for p, w in words_found[:15]]
        print(f"    Words: {', '.join(word_strs)}")

# ============================================================
# 7. Look for MHG HELN/HELEN (to conceal/hide)
# ============================================================
print(f"\n{'='*60}")
print("7. MHG HELN/HELEN (TO CONCEAL) IN GARBLED CORE")
print("=" * 60)

# In the garbled core: pos 10-12 = HEL
# MHG "heln" = to conceal, hide
# MHG "helen" = to conceal
# MHG "hel" = concealing, hidden
# OHG "helan" = to conceal
#
# HELUIRUNN:
# HEL + UI + RUNN
# = "conceal" + ? + "rune/run"?
# Or: HELU + IRUNN
# IRUNN = their (OHG) + N? Or IRUNN = Norse Idunn?
#
# What if the whole thing is:
# STEH WRLGT NELN RHELUIRUNN HWND FINDEN
# = "Stand [at] Wrlgt, Neln R-Hel-ui-runn, hound find"
# = two proper nouns?
#
# Or: STEH WR LGT NELN R HELU IRUNN HWND
# WR = WER (who)?
# LGT = LIEGT (lies)? Missing IE?
# NELN = a name?
# HELU = concealing?
# IRUNN = their run? or a name?

# Check if NELN appears independently elsewhere
print(f"\n  NELN occurrences outside garbled core:")
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = 0
    while True:
        idx = decoded.find('NELN', idx)
        if idx == -1:
            break
        # Skip if part of WRLGTNELNR
        ctx_s = max(0, idx-5)
        ctx_e = min(len(decoded), idx+10)
        full_ctx = decoded[ctx_s:ctx_e]
        if 'WRLGTNELN' not in full_ctx:
            print(f"    Book {bi}: ...{full_ctx}...")
        idx += 1

# Check HELU independently
print(f"\n  HELU occurrences outside garbled core:")
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = 0
    while True:
        idx = decoded.find('HELU', idx)
        if idx == -1:
            break
        ctx_s = max(0, idx-5)
        ctx_e = min(len(decoded), idx+10)
        full_ctx = decoded[ctx_s:ctx_e]
        if 'HELUIRUNN' not in full_ctx:
            print(f"    Book {bi}: ...{full_ctx}...")
        idx += 1

# ============================================================
# 8. Try treating WRLGTNELNRHELUIRUNN as proper noun(s)
# ============================================================
print(f"\n{'='*60}")
print("8. PROPER NOUN ANALYSIS OF GARBLED CORE")
print("=" * 60)

garbled = 'WRLGTNELNRHELUIRUNN'
# Try splitting at every position into 2 words
print(f"\n  All 2-word splits (checking for Tibia/Norse/fantasy resonance):")
for split in range(3, len(garbled)-2):
    w1 = garbled[:split]
    w2 = garbled[split:]
    c1 = collapse(w1)
    c2 = collapse(w2)
    # Flag splits where either part looks name-like
    flags = []
    # Check for Norse/Germanic name elements
    norse_elements = ['GRIM', 'HEIM', 'WALD', 'WULF', 'TRUD', 'HILD',
                      'GARD', 'MUND', 'BERT', 'BALD', 'HELM', 'BRUN',
                      'GUND', 'RUN', 'RUNE', 'HEL', 'ODIN', 'THOR',
                      'FREY', 'TYR', 'LOKI', 'NORN', 'IDUNN', 'IDUN',
                      'SIGURD', 'RAGNAR', 'FENR', 'NIFL', 'MUSP']
    for elem in norse_elements:
        if elem in c1 or elem in c2:
            flags.append(elem)
    if flags:
        print(f"    {c1} | {c2} -- contains: {', '.join(flags)}")

# Also try 3-word splits
print(f"\n  Promising 3-word splits:")
for s1 in range(2, len(garbled)-4):
    for s2 in range(s1+2, len(garbled)-2):
        w1 = garbled[:s1]
        w2 = garbled[s1:s2]
        w3 = garbled[s2:]
        c1, c2, c3 = collapse(w1), collapse(w2), collapse(w3)
        # Check if any part is a known word
        known_short = {'WER', 'EIN', 'DER', 'NUR', 'RUN', 'HEL', 'ELN',
                       'IRE', 'IRN', 'ALS', 'ER', 'IN', 'AN',
                       'HELN', 'RUNN', 'RUNE', 'HELD', 'WELT', 'GELT',
                       'STERN', 'GERN', 'FERN', 'NELN', 'IRUN'}
        matches = []
        for part in [c1, c2, c3]:
            if part in known_short:
                matches.append(part)
        if len(matches) >= 2:
            print(f"    {c1} | {c2} | {c3} -- matches: {matches}")

# ============================================================
# 9. VMT = VERMEINT (believed/supposed)?
# ============================================================
print(f"\n{'='*60}")
print("9. VMT AS MHG ABBREVIATION")
print("=" * 60)

# In medieval manuscripts, scribes used abbreviations:
# - nasals (M/N) were sometimes represented by a tilde over previous letter
# - common prefixes like VER- were abbreviated
# What if VMT represents a longer word?
# VMT could be shorthand for:
# VERMEINT (supposed/believed)
# VERMEIT (avoided)
# VERMAHT (betrothed)
# Or simply the 3 letters V-M-T in sequence

# Check VMTEGE context more carefully
# VMTEGE appears in two different contexts:
# Context 1: "IST VMTEGE VIEL" -- Book 8, 43
# Context 2: "SEIIGEVMTWIIE" -- Books 2, 22, 46, 51

# Let's get full context for both
print("\n  VMTEGE full contexts:")
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('VMTEGE')
    if idx != -1:
        ctx_s = max(0, idx-15)
        ctx_e = min(len(decoded), idx+20)
        print(f"    Book {bi:2d}: ...{decoded[ctx_s:ctx_e]}...")

print("\n  VMT not followed by EGE:")
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = 0
    while True:
        idx = decoded.find('VMT', idx)
        if idx == -1:
            break
        after = decoded[idx+3:idx+6]
        if after != 'EGE':
            ctx_s = max(0, idx-10)
            ctx_e = min(len(decoded), idx+15)
            print(f"    Book {bi:2d}: ...{decoded[ctx_s:ctx_e]}...")
        idx += 1

# ============================================================
# 10. ENDEUTRUNR = ENDE UTRUNR?
# ============================================================
print(f"\n{'='*60}")
print("10. ENDEUTRUNR = ENDE + UTRUNR?")
print("=" * 60)

# ENDEUTRUNR appears 3x -- could be ENDE + UTRUNR (End of Utterance)
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('ENDEUTRUNR')
    if idx != -1:
        ctx_s = max(0, idx-15)
        ctx_e = min(len(decoded), idx+25)
        print(f"  Book {bi:2d}: ...{decoded[ctx_s:ctx_e]}...")

# Check if UTRUNR appears elsewhere
print(f"\n  UTRUNR occurrences:")
utrunr_count = 0
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = 0
    while True:
        idx = decoded.find('UTRUNR', idx)
        if idx == -1:
            break
        ctx_s = max(0, idx-8)
        ctx_e = min(len(decoded), idx+14)
        print(f"    Book {bi:2d}: ...{decoded[ctx_s:ctx_e]}...")
        utrunr_count += 1
        idx += 1
print(f"  Total: {utrunr_count}")

# ============================================================
# 11. U code analysis -- are there too many U codes?
# ============================================================
print(f"\n{'='*60}")
print("11. U CODE ANALYSIS")
print("=" * 60)

u_codes = rev.get('U', [])
print(f"\n  U codes: {u_codes}")
total_u = 0
for uc in u_codes:
    count = sum(1 for b in books for c in b if c == uc)
    total_u += count
    print(f"    Code {uc}: {count}x")

total_all = sum(len(b) for b in books)
u_pct = 100 * total_u / total_all
print(f"\n  Total U: {total_u} ({u_pct:.1f}%)")
print(f"  Expected German U: 4.2%")
print(f"  Excess: {u_pct - 4.2:.1f}%")

# If U is too high, one of the U codes might be W (also underrepresented)
w_codes = rev.get('W', [])
total_w = sum(sum(1 for c in b if c in w_codes) for b in books)
w_pct = 100 * total_w / total_all
print(f"\n  Total W: {total_w} ({w_pct:.1f}%)")
print(f"  Expected German W: 1.9%")

# Code 43 and 44 are both U with similar frequencies (36, 30)
# Check their bigram profiles
for uc in u_codes:
    count = sum(1 for b in books for c in b if c == uc)
    if count < 10:
        continue
    before = Counter()
    after = Counter()
    for book_codes in books:
        decoded = decode(book_codes)
        for pos, c in enumerate(book_codes):
            if c == uc:
                if pos > 0:
                    before[decoded[pos-1]] += 1
                if pos < len(decoded)-1:
                    after[decoded[pos+1]] += 1
    print(f"\n  Code {uc} = U ({count}x):")
    print(f"    Before: {dict(before.most_common(6))}")
    print(f"    After:  {dict(after.most_common(6))}")

# ============================================================
# 12. Full text dump for pattern recognition
# ============================================================
print(f"\n{'='*60}")
print("12. ASSEMBLED PIECE #1 (longest) - COLLAPSED")
print("=" * 60)

# Build the superstring from books that overlap
# For now, just show a few representative books fully decoded + collapsed
for bi in [0, 1, 2, 3, 10]:
    decoded = decode(books[bi])
    c = collapse(decoded)
    # Insert spaces at likely word boundaries
    spaced = c
    known_long = ['KOENIG', 'LABGZERAS', 'AUNRSONGETRASES', 'TOTNIURG',
                  'HEARUCHTIGER', 'SCHWITEIO', 'TAUTR', 'EILCH', 'THARSC',
                  'STEINEN', 'STEINE', 'STEIN', 'URALTE', 'FINDEN',
                  'WISSET', 'SCHAUN', 'RUNEORT', 'RUNEN', 'RUNE', 'RUIN',
                  'DIESER', 'HWND', 'HIHL', 'LABRRNI', 'MINHEDDEM',
                  'LHLADIZ', 'HECHLT', 'GEIGET', 'UTRUNR',
                  'ENDEUTRUNR']
    for w in sorted(known_long, key=len, reverse=True):
        spaced = spaced.replace(w, f' {w} ')
    # Short words
    for w in ['IST', 'ICH', 'WIR', 'SIE', 'UND', 'DIE', 'DER', 'DAS',
              'DEN', 'DEM', 'DES', 'EIN', 'SEIN', 'SEINE',
              'HIER', 'NACH', 'SEID', 'NUN', 'GAR', 'AUCH',
              'NOCH', 'VIEL', 'ORT', 'SEE', 'TUN',
              'HAT', 'VON', 'AUS', 'ODE', 'WIE', 'NEU',
              'ALT', 'OEL', 'SEI', 'ERDE', 'FACH',
              'WIND', 'BIS', 'TAG', 'TEIL', 'WEG',
              'ERST', 'ERSTE', 'UNTER', 'DENEN',
              'ENDE', 'REDE', 'SO', 'AN', 'IN', 'ER', 'ES', 'AB']:
        spaced = re.sub(r'(?<=[A-Z])' + w + r'(?=[A-Z])', f' {w} ', spaced)
    spaced = re.sub(r' +', ' ', spaced).strip()
    print(f"\n  Book {bi:2d}: {spaced}")

print(f"\n{'='*80}")
print("SESSION 10b COMPLETE")
print("=" * 80)
