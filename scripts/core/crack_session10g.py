#!/usr/bin/env python3
"""Session 10g: Attack long repeated garbled patterns"""

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
    return re.sub(r'(.)\1+', r'\1', s)

print("=" * 80)
print("SESSION 10g: ATTACK LONG REPEATED PATTERNS")
print("=" * 80)

# 1. FINDEN confirmation and context
print("\n1. FINDEN CONFIRMATION")
print("-" * 60)

# Find all occurrences of code sequence for FINDEN
# F=20, I=15/16/21/46/50/65, N=many, D=many, E=many, N=many
for bi, book in enumerate(books):
    for ci in range(len(book)-5):
        if book[ci] == '20':
            next5 = ''.join(mapping.get(book[ci+x], '?') for x in range(1, 6) if ci+x < len(book))
            if next5.startswith('INDE'):
                ctx_start = max(0, ci-6)
                ctx_end = min(len(book), ci+8)
                ctx = ''.join(mapping.get(book[x], '?') for x in range(ctx_start, ctx_end))
                codes = '-'.join(book[ctx_start:ctx_end])
                print(f"  B{bi:02d}: {ctx}")
                print(f"        codes: {codes}")

# 2. EILCHANHEARUCHTIG - the 18-char monster
print("\n" + "=" * 60)
print("2. EILCHANHEARUCHTIG ANALYSIS (18 chars)")
print("=" * 60)

target = 'EILCHANHEARUCHTIG'
for bi, book in enumerate(books):
    decoded = decode(book)
    col = collapse(decoded)
    if target in col:
        pos = col.index(target)
        # Find corresponding position in raw decoded
        raw_pos = 0
        col_pos = 0
        while col_pos < pos:
            if raw_pos + 1 < len(decoded) and decoded[raw_pos] == decoded[raw_pos+1]:
                while raw_pos + 1 < len(decoded) and decoded[raw_pos] == decoded[raw_pos+1]:
                    raw_pos += 1
            raw_pos += 1
            col_pos += 1

        # Get codes for this segment
        codes = book[raw_pos:raw_pos+len(target)+5]
        letters = [mapping.get(c, '?') for c in codes]
        print(f"\n  B{bi:02d} at raw pos {raw_pos}:")
        for ci, (code, letter) in enumerate(zip(codes, letters)):
            print(f"    pos {ci:2d}: {code} = {letter}")

        # Wider context
        start = max(0, pos-12)
        end = min(len(col), pos+len(target)+12)
        ctx = col[start:end]
        print(f"  Context: ...{ctx}...")
        break  # One detailed view is enough

# Segmentation attempts
print(f"\n  Pattern: {target}")
print("  Segmentation attempts:")
segs = [
    "EIL + CHAN + HE + ARUCHTIG",
    "EILCH + AN + HEARUCHTIG",
    "EIL + CH + AN + HE + A + RUCHTIG",
    "E + ILCH + AN + HEARUCH + TIG",
    "EIL + CHAN + HEARUCH + TIG",
    "E + IL + CHAN + HE + ARUCH + TIG",
]
for s in segs:
    print(f"    {s}")

# MHG analysis
print("\n  MHG word candidates:")
print("    EIL = haste (MHG ile)")
print("    CHAN = ? (not standard)")
print("    HEARUCHTIG = ?")
print("    RUCHTIG = ? (MHG ruchtec = famous?)")
print("    AN = on/at")
print("    HE = he (pronoun)")
print("    TIG = ? (suffix)")

# Actually, what about: EIL-CHAN-HE-A-RUCHTIG?
# Or the whole thing is a name/compound?

# 3. EDETOTNIURGS - another repeated pattern
print("\n" + "=" * 60)
print("3. EDETOTNIURGS ANALYSIS")
print("=" * 60)

target2 = 'EDETOTNIURGS'
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if target2 in col:
        pos = col.index(target2)
        start = max(0, pos-15)
        end = min(len(col), pos+len(target2)+15)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# Code analysis for EDETOTNIURGS
print(f"\n  Segmentation attempts for {target2}:")
segs2 = [
    "EDETO + TN + IURGS",
    "EDE + TOT + NIURGS",
    "EDE + TOTN + I + URGS",
    "E + DE + TOTN + IURG + S",
    "EDET + OTN + IURGS",
]
for s in segs2:
    print(f"    {s}")
print("  Note: TOT = dead (German). EDE + TOT = ??? dead?")

# 4. EUGENDRTHENAEDEULGHLWUOEHSG - the 28-char monster
print("\n" + "=" * 60)
print("4. EUGENDRTHENAEDEULGHLWUOEHSG (28 chars)")
print("=" * 60)

target3 = 'EUGENDRTHENAEDEULGHLWUOEHSG'
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if target3 in col:
        pos = col.index(target3)
        start = max(0, pos-10)
        end = min(len(col), pos+len(target3)+10)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")
        break

print(f"\n  Segmentation attempts:")
segs3 = [
    "EU + GEN + DR + THENA + EDE + UL + GHL + WUO + EHSG",
    "EUGEN + DRTHENA + EDEUL + GHLWUO + EHSG",
    "EU + GENDR + THENAE + DEUL + GHL + WUOEHSG",
    "EUGEN + D + R + THENA + EDEUL + GHL + WUO + EHSG",
]
for s in segs3:
    print(f"    {s}")
print("  Note: EUGEN = name? THENA = ? EHSG = ?")
print("  GHL = consonant cluster - possible mapping error?")

# 5. Look for hidden words in the garbled segments
print("\n" + "=" * 60)
print("5. HIDDEN WORDS IN GARBLED SEGMENTS")
print("=" * 60)

# All major garbled patterns
garbled = [
    'EILCHANHEARUCHTIG',
    'EDETOTNIURGS',
    'EUGENDRTHENAEDEULGHLWUOEHSG',
    'MIHIETUNCISN',
    'TIUMENGEMI',
    'WRLGTNELNRHELUIRUNN',
    'DNRHAUNRNVMHISDIZA',
    'AUNRSONGETRASES',
    'SCHWITEIONE',
    'UNENITGHNE',
]

# German words to search for within garbled text
search_words = [
    'TOT', 'TOD', 'EDE', 'ORT', 'GEN', 'HER', 'UNG',
    'MEN', 'TUN', 'AUS', 'EIN', 'ARM', 'AUG', 'UHR',
    'MIT', 'RUN', 'OHN', 'GUT', 'ALT', 'MUT',
    'NOT', 'RAT', 'TAT', 'WUT', 'TOR', 'URN',
    'HEIT', 'TION', 'ISCH', 'LICH', 'UNGE',
    'CHEN', 'LEIN', 'HEIL', 'WEIS', 'TREU',
    'NACHT', 'MACHT', 'KRAFT', 'GEIST', 'WESEN',
    'LEBEN', 'RUHE', 'EHRE', 'GNADE', 'TUGEND',
    'HAUN', 'DIZA', 'SCHU', 'WEISE',
]

for garb in garbled:
    found = []
    for w in search_words:
        if w in garb:
            pos = garb.index(w)
            found.append(f"{w} at pos {pos}")
    if found:
        print(f"\n  {garb}:")
        for f in found:
            print(f"    -> {f}")

# 6. What context comes after EILCHANHEARUCHTIG?
print("\n" + "=" * 60)
print("6. WHAT FOLLOWS EILCHANHEARUCHTIG?")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'EILCHANHEARUCHTIG' in col:
        pos = col.index('EILCHANHEARUCHTIG') + len('EILCHANHEARUCHTIG')
        end = min(len(col), pos+30)
        after = col[pos:end]
        start = col.index('EILCHANHEARUCHTIG') - 10
        before = col[max(0,start):col.index('EILCHANHEARUCHTIG')]
        print(f"  B{bi:02d}: ...{before}EILCHANHEARUCHTIG|{after}...")

# 7. What context comes before "DIE URALTE STEIN"?
print("\n" + "=" * 60)
print("7. CONTEXT BEFORE 'DIE URALTE STEIN'")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'DIEURALTESTEI' in col:  # STEIN without final N might be collapsed
        pos = col.index('DIEURALTESTEI')
        start = max(0, pos-25)
        ctx = col[start:pos+20]
        print(f"  B{bi:02d}: ...{ctx}...")

# 8. HEDEMI - place name analysis
print("\n" + "=" * 60)
print("8. HEDEMI AS PLACE NAME")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'HEDEMI' in col:
        pos = col.index('HEDEMI')
        start = max(0, pos-20)
        end = min(len(col), pos+26)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# 9. Try to read "ER TAUTR IST EILCHANHEARUCHTIG ER SO DAS TUN DIE"
print("\n" + "=" * 60)
print("9. FULL SENTENCE ANALYSIS")
print("=" * 60)

sentence = "ENHIERTAUTRISTEILCHANHEARUCHTIGERSODASTUNDIESERTEINERSEINEDETO"
print(f"  Raw: {sentence}")
print(f"  Attempt 1: EN-HI ER TAUTR IST EILCHANHEARUCHTIG ER SO DAS TUN DIE SER-T-EIN-ER-SEIN EDETO")
print(f"  Attempt 2: ENHI ER TAUTR IST EIL-CHAN-HE-ARUCHTIG ER SO DAS TUN DIE S ER T EIN ER SEIN EDETO")
print(f"  Attempt 3: EN HI ER TAUTR IST EILCHANHEARUCHTIG ER SO DAS TUN DIES ER T EIN ER SEIN EDETO")

# Note: "ER SO DAS TUN DIE" = "he so that do the" -> "he, so that the [do]"
# "ER TAUTR IST [adjective]" -> "he TAUTR is [adjective]"
# TAUTR could be a proper noun (name)

# 10. Code distribution for EILCHANHEARUCHTIG
print("\n" + "=" * 60)
print("10. CODE-LEVEL ANALYSIS OF EILCHANHEARUCHTIG")
print("=" * 60)

# Find exact code sequences for all instances
instances = []
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'EILCHANHEARUCHTIG' in col:
        # Find the raw position
        raw = decode(book)
        # Search for the pattern in the raw decoded
        # Need to find where the collapsed pattern starts in raw
        for ri in range(len(raw)):
            collapsed_from_ri = collapse(raw[ri:ri+25])
            if collapsed_from_ri.startswith('EILCHANHEARUCHTIG'):
                raw_segment = raw[ri:ri+25]
                code_segment = book[ri:ri+25]
                # Find how many raw chars make up the collapsed pattern
                raw_len = 0
                col_check = ''
                while raw_len < len(raw_segment) and len(collapse(col_check + raw_segment[raw_len])) <= len('EILCHANHEARUCHTIG'):
                    col_check += raw_segment[raw_len]
                    raw_len += 1
                codes_used = book[ri:ri+raw_len]
                letters_used = [mapping.get(c, '?') for c in codes_used]
                instances.append((bi, codes_used, letters_used))
                break

print(f"\n  Found {len(instances)} instances:")
for bi, codes, letters in instances[:5]:
    print(f"    B{bi:02d}: {'-'.join(codes)}")
    print(f"          {''.join(letters)}")

# Check if all instances use identical codes
if len(instances) >= 2:
    ref = instances[0][1]
    all_same = all(inst[1] == ref for inst in instances)
    print(f"\n  All instances identical codes: {all_same}")
    if not all_same:
        for bi, codes, letters in instances:
            print(f"    B{bi:02d}: {codes}")

# 11. Fresh attempt: what if EILCHANHEARUCHTIG contains NICHT (not)?
print("\n" + "=" * 60)
print("11. HIDDEN NICHT IN EILCHANHEARUCHTIG?")
print("=" * 60)

# EILCH-AN-HE-ARUCHTIG
# No NICHT visible directly. But what about code swaps?
# Let's check if CHT in RUCHTIG could be part of NICHT
print("  EILCHANHEARUCHTIG:")
print("  Position of CH:  pos 3-4 (EILCH)")
print("  Position of CHT: pos 13-15 (RUCHTIG)")
print("  If we read backwards from CHT: ...A-RU-CHT-IG")
print("  RUCHTIG: in MHG, 'ruchtec' = famous, known")
print("  A-RUCHTIG: not standard")
print("  BEARUCHTIG: not standard")
print("  HE-ARUCHTIG: not standard")
print()
print("  Alternative: EILCH + AN + HE + A + RUCHTIG")
print("  Or: EIL + CH + ANH + EAR + UCHTIG")
print("  UCHTIG: not a known suffix")
print()
print("  MHG RUCHTIG = famous, well-known")
print("  MHG EILICH = hasty")
print("  Could EILCH = EILICH (hasty) with collapse?")
print("  EILICH-AN-HE-ARUCHTIG -> 'hastily on him famous'?")

# 12. Summary of all confirmed words
print("\n" + "=" * 60)
print("12. ALL CONFIRMED GERMAN WORDS")
print("=" * 60)

all_words = [
    # Nouns
    ('KOENIG', 'king', 6),
    ('STEIN', 'stone', 9),
    ('ERDE', 'earth', 13),
    ('RUNE', 'rune(s)', 23),
    ('REDE', 'speech', 6),
    ('SEGEN', 'blessing', 0),
    ('GOLD', 'gold', 0),
    ('SONNE', 'sun', 0),
    ('MOND', 'moon', 0),
    ('SEIDE', 'silk', 6),
    ('TAG', 'day', 5),
    ('WEG', 'way', 3),
    ('WELT', 'world', 0),
    ('LIED', 'song', 0),
    ('HUND', 'hound (OHG HWND)', 3),
    ('ORT', 'place', 10),
    ('ENDE', 'end', 15),
    ('NORDEN', 'north', 0),
    # Verbs
    ('IST', 'is', 30),
    ('GEIGET', 'plays/shows (MHG)', 7),
    ('STEH', 'stand', 7),
    ('FINDEN', 'to find (NEW!)', 6),
    ('TUN', 'to do', 5),
    ('SEIN', 'to be / his', 12),
    ('WIRD', 'becomes/will', 4),
    ('SEI', 'be (subj.)', 8),
    ('WIE', 'as/how', 6),
    ('SCHAUN', 'to behold (MHG)', 8),
    # Articles/pronouns
    ('DER', 'the (m.)', 20),
    ('DIE', 'the (f./pl.)', 15),
    ('DAS', 'the (n.)/that', 12),
    ('DEN', 'the (acc.)', 18),
    ('DENEN', 'to those', 6),
    ('EIN', 'a/one', 15),
    ('ER', 'he', 50),
    ('ES', 'it', 20),
    ('SIE', 'she/they', 5),
    ('WIR', 'we', 15),
    # Prepositions/conjunctions
    ('IN', 'in', 25),
    ('UND', 'and', 5),
    ('VON', 'from', 3),
    ('MIT', 'with', 3),
    ('AUS', 'from/out', 8),
    ('SO', 'so', 5),
    ('NICHT', 'not', 1),
    ('UNTER', 'under', 3),
    ('VIEL', 'much', 8),
    # Adjectives
    ('URALTE', 'ancient', 9),
    # MHG specific
    ('UTRUNR', 'utterance? (5x)', 5),
    ('KELSEI', 'unknown MHG', 5),
    ('DENN', 'for/then', 0),
    ('DORT', 'there', 0),
    ('WERDE', 'become', 3),
    # Proper nouns
    ('LABGZERAS', 'king name', 6),
    ('AUNRSONGETRASES', 'king title', 5),
    ('HEDEMI', 'place name', 7),
]

total_coverage = 0
for word, meaning, count in sorted(all_words, key=lambda x: -x[2]):
    if count > 0:
        print(f"    {word:20s} ({count:2d}x) = {meaning}")
        total_coverage += len(word) * count

# Approximate total text
total_chars = sum(len(collapse(decode(b))) for b in books)
print(f"\n  Approximate coverage: {total_coverage}/{total_chars} = {total_coverage/total_chars*100:.1f}%")

print("\n" + "=" * 80)
print("SESSION 10g COMPLETE")
print("=" * 80)
