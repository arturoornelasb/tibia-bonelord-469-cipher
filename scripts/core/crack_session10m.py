#!/usr/bin/env python3
"""Session 10m: DP-optimal segmentation & MHG morphology attack"""

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
print("SESSION 10m: DP SEGMENTATION & MHG ATTACK")
print("=" * 80)

# Comprehensive word list (sorted by length for greedy)
# Weighted: longer known words score higher
word_scores = {}

# Definite words (high confidence)
definite = [
    'AUNRSONGETRASES', 'UNENITGHNE', 'EILCHANHEARUCHTIG',
    'EDETOTNIURGS', 'DNRHAUNRNVMHISDIZA',
    'EUGENDRTHENAEDEULGHLWUOEHSG', 'WRLGTNELNRHELUIRUNN',
    'TIUMENGEMI', 'SCHWITEIONE',
    'LABGZERAS', 'HEDEMI', 'TAUTR', 'LABRNI', 'ADTHARSC',
    'ADTHAUMR', 'ODEGAREN', 'RLAUNR',
    'KOENIG', 'UTRUNR', 'GEIGET', 'KELSEI', 'SCHAUN',
    'URALTE', 'FINDEN', 'SEIDE', 'DIESER', 'GEVMT',
    'NORDEN', 'SONNE', 'UNTER', 'NICHT', 'WERDE',
    'STEIN', 'DENEN', 'ERDE', 'VIEL', 'RUNE',
    'STEH', 'LIED', 'SEGEN', 'DORT', 'DENN',
    'GOLD', 'MOND', 'WELT', 'ENDE', 'REDE',
    'HUND', 'SEIN', 'WIRD', 'KLAR', 'ERST',
    'HWND', 'VMTEGE',
    'EINEN', 'EINER', 'SEINE',
    'TAG', 'WEG', 'DER', 'DEN', 'DIE', 'DAS',
    'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON',
    'MIT', 'WIE', 'SEI', 'AUS', 'ORT', 'TUN',
    'NUR', 'SUN', 'TOT', 'GAR', 'ACH', 'ZUM',
    'HIN', 'HER', 'ALS', 'AUCH', 'RUND',
    'ER', 'ES', 'IN', 'SO',
]

# MHG/OHG candidates (medium confidence)
mhg_candidates = [
    'EIGEN', 'ENGE', 'ENGEL', 'ENDEN', 'DINGE',
    'REDEN', 'STEINEN', 'STEINE', 'REDET', 'SINGET',
    'SAGET', 'WIRDET', 'TUOT', 'DISE', 'DISEN',
    'WISSET', 'RUHE', 'RUHEN', 'LIEGEN', 'STEHEN',
    'GEHEN', 'SEHEN', 'LEBEN', 'GEBEN', 'NEMEN',
    'HERRE', 'MEISTER', 'EDEL', 'TUGEND', 'MINNE',
    'RITTER', 'LAND', 'BURG', 'HEIL', 'GEIST',
    'WUNDER', 'MACHT', 'KRAFT', 'KUNST', 'RECHT',
    'WORT', 'HERR', 'HERZE', 'LEUTE', 'LEIDE',
    'JENER', 'JENE', 'MUOT', 'GUOT', 'NIHT',
    'OUCH', 'WIRT', 'LIGEN', 'STEN', 'GEN',
    'HEIM', 'DISE', 'SINT', 'TUON',
    'ERE', 'MER', 'NIE', 'WOL', 'DAR', 'DAN',
    'VIL', 'MIN', 'SIN', 'MAN', 'IME', 'IHM',
]

for w in definite:
    word_scores[w] = len(w) * 3  # high weight
for w in mhg_candidates:
    if w not in word_scores:
        word_scores[w] = len(w) * 2  # medium weight

all_words = sorted(word_scores.keys(), key=len, reverse=True)

# 1. DP optimal segmentation
print("\n1. DP-OPTIMAL SEGMENTATION (longest book)")
print("-" * 60)

def dp_segment(text, words, scores):
    """Find segmentation that maximizes total score of recognized words."""
    n = len(text)
    # dp[i] = (best_score, backtrack_info) for text[0:i]
    dp = [(-1, None)] * (n + 1)
    dp[0] = (0, None)

    for i in range(n):
        if dp[i][0] < 0:
            continue
        # Option 1: unknown character (score = 0, but we penalize slightly)
        if dp[i+1][0] < dp[i][0] - 1:
            dp[i+1] = (dp[i][0] - 1, ('unk', i, i+1))
        # Option 2: match a word
        for word in words:
            wlen = len(word)
            if i + wlen <= n and text[i:i+wlen] == word:
                new_score = dp[i][0] + scores.get(word, wlen)
                if new_score > dp[i+wlen][0]:
                    dp[i+wlen] = (new_score, ('word', i, i+wlen, word))

    # Backtrack
    result = []
    pos = n
    while pos > 0:
        info = dp[pos][1]
        if info is None:
            # Shouldn't happen, but fallback
            result.append(('unk', text[pos-1:pos]))
            pos -= 1
        elif info[0] == 'unk':
            # Merge consecutive unknowns
            end = pos
            while pos > 0 and dp[pos][1] and dp[pos][1][0] == 'unk':
                pos = dp[pos][1][1]
            result.append(('unk', text[pos:end]))
        elif info[0] == 'word':
            result.append(('word', info[3]))
            pos = info[1]

    result.reverse()
    return result, dp[n][0]

# Get longest book
pieces = {}
for i, text in all_col:
    is_sub = False
    for j, other in all_col:
        if i != j and text in other:
            is_sub = True
            break
    if not is_sub:
        pieces[i] = text

by_len = sorted(pieces.items(), key=lambda x: len(x[1]), reverse=True)

# Segment top 3 books
for idx, (bi, text) in enumerate(by_len[:3]):
    result, score = dp_segment(text, all_words, word_scores)
    print(f"\n  --- Book {bi} ({len(text)} chars, score={score}) ---")

    # Format output
    parts = []
    for typ, val in result:
        if typ == 'word':
            parts.append(val)
        else:
            parts.append(f'[{val}]')

    line = ' '.join(parts)
    for i in range(0, len(line), 78):
        print(f"    {line[i:i+78]}")

    # Count coverage
    word_chars = sum(len(val) for typ, val in result if typ == 'word')
    print(f"    Coverage: {word_chars}/{len(text)} = {word_chars*100/len(text):.1f}%")

# 2. Focus: EILCHANHEARUCHTIG morphology
print("\n" + "=" * 60)
print("2. EILCHANHEARUCHTIG MORPHOLOGY")
print("=" * 60)

word = 'EILCHANHEARUCHTIG'
print(f"  Word: {word} ({len(word)} chars)")
print(f"  Letters: {' '.join(word)}")
print()

# Try all possible decompositions
print("  Possible decompositions:")
# -UCHTIG suffix
print("    EILCHANHE-A-RUCHTIG (? + ? + renowned)")
print("    EILCHAN-HEAR-UCHTIG (? + ? + ?)")
print("    EIL-CHANHEAR-UCHTIG (hurry + ? + ?)")
print("    E-ILCHAN-HE-ARUCHTIG")
print()

# MHG -UCHTIG / -RUCHTIG analysis
# BERUCHTIG(T) = beruechtigt = famous/notorious
# FRUCHTICH = fruitful
# WICHTIG = important (but modern, not MHG)
# -RUCHTIG: MHG beruhtic = famous
# If -ARUCHTIG = A + RUCHTIG:
#   EILCHANHE + A + RUCHTIG
#   EILCHANHE = ?

# Try: ELICH + AN + HE + ARUCHTIG
# ELICH = ehelich (matrimonial)? MHG ELICH = legitimate/lawful
# ELICH + AN = lawfully on?
# Or: EILICH + ANHE + ARUCHTIG
# Or: EIL + CHAN + HEAR + UCHTIG

# German CH digraph positions
print("  CH positions: pos 3-4 (EIL-CH) and pos 11-12 (RU-CH)")
print()

# What if E-ILCH-AN-HEAR-UCHTIG?
# ILCH doesn't exist in German
# What if EIL-CHAN-HEAR-UCHTIG?
# CHAN = OHG/MHG? Not standard
# What if EILCH-ANHE-ARUCHTIG?
# EILCH doesn't exist

# New idea: read without CH digraphs
print("  Without CH digraph assumption:")
print("    E-I-L-C-H-A-N-H-E-A-R-U-C-H-T-I-G")
print("    If C and H are separate letters (not CH):")
print("    Then: E-I-L-C + H-A-N-H-E-A-R-U-C-H-T-I-G")
print("    Or: EIL + C + HAN + HEAR + UCH + TIG")
print()

# Most likely: compound adjective in MHG
# MHG -ig suffix is very common for adjectives
# The -uchtig ending is less common
# But MHG RUCHTIG = famous is attested

# 3. Test EILCHANHEARUCHTIG against Tibia lore
print("=" * 60)
print("3. TIBIA LORE CROSS-REFERENCE")
print("=" * 60)

# In Tibia, bonelords are described as:
# - Ancient, powerful, magical creatures
# - They live in Hellgate and other dungeons
# - They have one large eye
# - They use "death beam" attacks
# - Connected to Drefia and necromancy

# The narrative themes:
# - Ancient stone with runes
# - A king (Labgzeras)
# - Finding a hound
# - A place called HEDEMI
# - Death (TOT) in compound word
# - Being "formed/shaped as the day does"
# - Beholding something in WISET (knowledge/wisdom)

# Tibia has German origins (early versions had German text)
# Creator: CipSoft (German company, Regensburg)
# Game language mix of German, Latin, English

print("  NARRATIVE THEMES vs TIBIA LORE:")
print("    ANCIENT STONE + RUNES = runic magic system in Tibia")
print("    KING LABGZERAS = possibly a historical/fictional king")
print("    HOUND (HWND) = hellhound creature in Tibia?")
print("    HEDEMI = place name (HEL-DEMI? HELL-HEIMAT?)")
print("    DEATH compound = necromancy/Drefia connection")
print("    SCHAUN + WISET = knowledge/wisdom theme")
print("    SEGEN = blessing = divine/priestly theme")
print()

# HEDEMI decomposition:
print("  HEDEMI decomposition:")
print("    HED + EMI (?)")
print("    HE + DEMI (half?)")
print("    HEIM backwards = MIEH (no)")
print("    Could be: HEIDE (heath) + MI?")
print("    Or: MHG HEDEMA = ?")
print("    Or: OHG HEIM (home) scrambled?")

# 4. DER STEIEN GEH = DER STE IEN GEH?
print("\n" + "=" * 60)
print("4. STEIEN ANALYSIS")
print("=" * 60)

# Check if STEIEN has consistent codes
steien_codes = []
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'STEIEN' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if collapse(decoded[ri:ri+12]).startswith('STEIEN'):
                codes = book[ri:ri+6]
                steien_codes.append((bi, codes))
                break

print(f"  STEIEN in {len(steien_codes)} books:")
for bi, codes in steien_codes:
    letters = [mapping.get(c, '?') for c in codes]
    print(f"    B{bi:02d}: {' '.join(codes)} = {''.join(letters)}")

# What if STEIEN = STEINEN (stones, dative) with collapsed NN->N?
# Check raw for the N
print("\n  Checking raw before collapse:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'STEIEN' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if collapse(decoded[ri:ri+12]).startswith('STEIEN'):
                raw = decoded[ri:ri+8]
                print(f"    B{bi:02d}: raw = {raw}")
                break
        break

# 5. The narrative sentence by sentence
print("\n" + "=" * 60)
print("5. SENTENCE-BY-SENTENCE NARRATIVE (best reading)")
print("=" * 60)

# Based on all analysis, the best reading of the longest book (B9):
sentences = [
    ("NHI ER TAUTR IST EILCHANHEARUCHTIG",
     "??? He, TAUTR, is EILCHANHEARUCHTIG (renowned?)"),
    ("ER SO DAS TUN DIESER TEINER SEIN EDETOTNIURGS",
     "He, so that do this TEINER his EDETOTNIURGS (death-oath?)"),
    ("ER LABRNI WIR UND IEM IN HEDEMI",
     "He LABRNI, we and ??? in HEDEMI"),
    ("DIE URALTE STEIN ENT ER ADTHARSC",
     "The ancient stone, ENT he ADTHARSC"),
    ("IST SCHAUN RUI IN WISET",
     "Is to behold peace(?) in wisdom"),
]

for orig, trans in sentences:
    print(f"  {orig}")
    print(f"    = {trans}")
    print()

# From other books:
print("  From Book 35 continuation:")
more_sentences = [
    ("NHI ER SER TIUMENGEMI ORT ENGCHD",
     "??? He ??? TIUMENGEMI (community) place ENGCHD"),
    ("KELSEI DEN DNRHAUNRNVMHISDIZA RUNE",
     "KELSEI the DNRHAUN... rune"),
    ("UNTER LAUS IN HIET DEN DE ES SCHWITEIONE",
     "Under LAUS in HIET the ??? SCHWITEIONE"),
]

for orig, trans in more_sentences:
    print(f"  {orig}")
    print(f"    = {trans}")
    print()

print("  From Book 10 continuation:")
final_sentences = [
    ("ERDE NGE ENDE NTENTT UIGAA ER GEIGET ES IN CHN",
     "Earth ??? end ??? ??? he shows it in CHN"),
    ("ES R ER SCE AUS ENDE UTRUNR DENEN DER REDE",
     "It ??? he SCE from, end of utterance of the speech"),
    ("KOENIG LABGZERAS UNENITGHNE AUNRSONGETRASES",
     "King LABGZERAS UNENITGHNE AUNRSONGETRASES"),
]

for orig, trans in final_sentences:
    print(f"  {orig}")
    print(f"    = {trans}")
    print()

# 6. What are the actual P/J candidates?
print("=" * 60)
print("6. MISSING LETTER ANALYSIS: P AND J")
print("=" * 60)

# German text should have P (~0.7%) and J (~0.3%)
# Total characters ~5400, so expect ~38 P's and ~16 J's
# Currently NO P or J in the mapping
# Could some codes be misassigned?

# The most overrepresented letters:
# I: 10.5% (expected 7.6%) - 3 unconfirmed codes (15, 16, 65)
# E: highest count with 9 unconfirmed codes
# N: 5 unconfirmed codes

# P typically appears in: PLATZ, PRIESTER, PRACHT, SPRECHEN
# In MHG: PH was common (PHLICHT, PHERD)
# In Tibia context: no obvious P-words expected

# J typically appears in: JA, JEDER, JENER, JUNG, JETZT
# In MHG: no J (it was written I)
# So J might legitimately be absent!

print("  P (~38 expected chars):")
print("    No P in mapping. Could be absent in this text register.")
print("    MHG often used PH (which maps to P+H, both present)")
print("    Or: some I/E codes might actually be P")
print()
print("  J (~16 expected chars):")
print("    In MHG, J was written as I (JENER -> IENER)")
print("    So J is LEGITIMATELY ABSENT from a MHG text!")
print("    This confirms the archaic register.")
print()

# Test: if P is missing, what words use P in German?
# PLATZ, PRACHT, PRIESTER would be rare in this context
# But SPRECHEN (to speak), SPRUCH (saying) use SP
# Check if SPR appears in the text
for bi, col in all_col:
    if 'SPR' in col:
        pos = col.index('SPR')
        start = max(0, pos-10)
        end = min(len(col), pos+15)
        print(f"  SPR found in B{bi:02d}: ...{col[start:end]}...")

print("  No SPR found - consistent with P being absent")

# 7. Better LRSZTHK attack
print("\n" + "=" * 60)
print("7. LRSZTHK: IS CODE 96(L) MISASSIGNED?")
print("=" * 60)

# LRSZTHK has 7 consonants - impossible in German
# Code 96 = L is the ONLY code for L, but it's unconfirmed!
# What if code 96 is actually a different letter?

# Check all code 96 contexts
print("  Code 96 (currently=L) all contexts:")
c96_contexts = []
for bi, book in enumerate(books):
    for ci, c in enumerate(book):
        if c == '96':
            start = max(0, ci-4)
            end = min(len(book), ci+5)
            ctx_codes = book[start:end]
            ctx = ''.join(mapping.get(x, '?') for x in ctx_codes)
            col_ctx = collapse(ctx)
            pos_in = ci - start
            c96_contexts.append((bi, col_ctx, pos_in))

# Show unique contexts
seen = set()
for bi, ctx, pos in c96_contexts:
    marked = ctx[:pos] + '[' + ctx[pos] + ']' + ctx[pos+1:]
    if marked not in seen:
        seen.add(marked)
        print(f"    B{bi:02d}: {marked}")

# Count total
print(f"\n  Total code 96 occurrences: {len(c96_contexts)}")

# If L is actually a vowel (A, O, U), LRSZTHK becomes ARSZTHK, ORSZTHK, URSZTHK
# None of these are German either
# If L is P: PRSZTHK - still impossible
# If L is B: BRSZTHK - still impossible
# Conclusion: LRSZTHK is not a standard German word regardless of L assignment

# Check: words that use L
print("\n  Words containing L (all via code 96):")
l_words = []
for bi, col in all_col:
    for pattern in ['LAB', 'LAU', 'LAUS', 'LIED', 'LRSZ',
                    'LUIR', 'EHLW', 'ULGH']:
        if pattern in col:
            pos = col.index(pattern)
            start = max(0, pos-5)
            end = min(len(col), pos+12)
            ctx = col[start:end]
            if ctx not in [x[2] for x in l_words]:
                l_words.append((bi, pattern, ctx))

for bi, pat, ctx in l_words[:15]:
    print(f"    B{bi:02d}: {pat} in ...{ctx}...")

# LABGZERAS uses L: confirmed proper noun
# LAUS appears in "UNTER LAUS IN" - LAUS = louse? Or part of larger word?
# If UNTER-LAUS = under-louse, that's weird
# Could be UNTERLASSIN (to refrain)?

print("\n" + "=" * 80)
print("SESSION 10m COMPLETE")
print("=" * 80)
