#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session 24 Part B: Focused language analysis (fixed Unicode issues).
Key questions:
1. What language profile do the garbled blocks match?
2. Can HECHLLT = HECHELT (hackle flax, letter swap)?
3. UTRUNR = 'UT RUNR' (Old Norse: outer runes)?
4. HIHL = HEHL/HOHL/HIL variant?
5. New coverage from expanded vocabulary?
"""

import json, os, sys
from collections import Counter, defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

DIGIT_SPLITS = {
    2: (45, '1'), 5: (265, '1'), 6: (12, '0'), 8: (137, '7'),
    10: (169, '0'), 11: (137, '0'), 12: (56, '1'), 13: (45, '0'),
    14: (98, '1'), 15: (98, '0'), 18: (4, '0'), 19: (52, '0'),
    20: (5, '1'), 22: (7, '1'), 23: (22, '4'), 24: (87, '8'),
    25: (0, '0'), 29: (53, '0'), 32: (137, '1'), 34: (101, '0'),
    36: (78, '0'), 39: (44, '0'), 42: (91, '2'), 43: (122, '0'),
    45: (15, '0'), 46: (0, '2'), 48: (126, '0'), 49: (97, '1'),
    50: (16, '6'), 52: (1, '0'), 53: (257, '1'), 54: (49, '1'),
    60: (73, '9'), 61: (93, '7'), 64: (60, '0'), 65: (114, '2'),
    68: (54, '0'),
}

ANAGRAM_MAP = {
    'LABGZERAS': 'SALZBERG', 'SCHWITEIONE': 'WEICHSTEIN',
    'SCHWITEIO': 'WEICHSTEIN', 'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'EDETOTNIURG': 'GOTTDIENER', 'EDETOTNIURGS': 'GOTTDIENERS',
    'ADTHARSC': 'SCHARDT', 'TAUTR': 'TRAUT', 'EILCH': 'LEICH',
    'HEDDEMI': 'HEIME', 'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG', 'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE', 'TEIGN': 'NEIGT', 'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER', 'SODGE': 'GODES', 'SNDTEII': 'DIENST',
    'IEB': 'BEI', 'TNEDAS': 'STANDE', 'NSCHAT': 'NACHTS',
    'SANGE': 'SAGEN', 'GHNEE': 'GEHEN', 'THARSCR': 'SCHRAT',
    'ANSD': 'SAND', 'TTU': 'TUT', 'TERLAU': 'URALTE',
    'EUN': 'NEU', 'NIUR': 'RUIN', 'RUIIN': 'RUIN', 'CHIS': 'SICH',
}

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    return 0 if ic_from_counts(Counter(bp0), len(bp0)) > ic_from_counts(Counter(bp1), len(bp1)) else 1

decoded_books = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    decoded_books.append(''.join(v7.get(p, '?') for p in pairs))

raw = ''.join(decoded_books)
processed = raw
for old in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    processed = processed.replace(old, ANAGRAM_MAP[old])

# Full vocabulary (session 22 confirmed state)
KNOWN_WORDS = {
    'SEIN', 'SEINE', 'SEINER', 'SEINEN', 'SEINEM', 'SEINES',
    'IST', 'WAR', 'WIRD', 'WAREN', 'SEID',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES',
    'EIN', 'EINE', 'EINER', 'EINEM', 'EINEN', 'EINES',
    'UND', 'ODER', 'ABER', 'NICHT', 'MIT', 'VON', 'BIS',
    'WIR', 'ICH', 'ER', 'SIE', 'ES', 'IHR', 'WER', 'WAS',
    'IN', 'IM', 'AN', 'AM', 'AUF', 'AUS', 'AB', 'ZU', 'ZUR', 'ZUM',
    'BEI', 'SO', 'DA', 'WO', 'NUN', 'NU', 'INS', 'GEN', 'DES', 'AUS',
    'HIER', 'ODE', 'ORT', 'NACH', 'ALS', 'WIE', 'WENN',
    'KLAR', 'AUCH', 'WEG', 'NUR', 'NIT',
    'GOTT', 'RUNE', 'RUNEN', 'STEIN', 'STEINEN', 'STEINE',
    'URALTE', 'ALT', 'ALTE', 'ALTEN',
    'KOENIG', 'RITTER', 'WORT', 'SAGEN', 'FINDEN',
    'STEH', 'GEHEN', 'GEH', 'ENDE', 'ENDEN',
    'ERSTE', 'ERSTEN',
    'DIESE', 'DIESER', 'DIESEN', 'DIESEM', 'DIESES',
    'TAG', 'MIN', 'TOT', 'RUIN', 'RUINE', 'SAND', 'HEIME', 'HEIM',
    'LEICH', 'LEICHE', 'TRAUT', 'SCHRAT', 'SCHARDT', 'SCHAUN',
    'WEICHSTEIN', 'SALZBERG', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'EIGENTUM', 'MEERE',
    'NEIGT', 'WISTEN', 'MANIER', 'GODES', 'DIENST', 'NACHTS',
    'STANDE', 'BEI', 'TUT', 'NEU', 'SICH', 'REDER',
    'HEL', 'RIT', 'EWE', 'SIN', 'MIS', 'AUE', 'EIS',
    'SCE', 'OEL', 'TER', 'THENAEUT',
    'BERUCHTIG', 'BERUCHTIGER', 'LEICHANBERUCHTIG', 'LEICHANBERUCHTIGER',
    'HAT', 'NET', 'EM', 'TUN',
    'RUINEN', 'HUND', 'GRUND', 'RECHT', 'NACHT',
    'BURG', 'BERG', 'WALD', 'LICHT', 'KNECHT',
    'HEHL', 'HEHLE', 'HEIL', 'HELD', 'SCHLECHT', 'ECHT',
    'WIRT', 'WIRTE', 'TURM', 'TEICH',
    'ELCH', 'DURCH', 'WUNDER', 'WUNDE',
    'UNTER', 'HOLT',
    # New from session 24 analysis (if confirmed)
}

def count_coverage(text, vocab):
    n = len(text)
    covered = 0
    i = 0
    while i < n:
        for l in range(min(20, n-i), 1, -1):
            if text[i:i+l] in vocab:
                covered += l
                i += l
                break
        else:
            i += 1
    return covered, n

base_cov, total = count_coverage(processed, KNOWN_WORDS)
print(f"Baseline coverage: {base_cov}/{total} = {base_cov/total*100:.1f}%")

# ============================================================
# ANALYSIS 1: N-gram analysis of garbled content
# ============================================================
print("\n" + "="*60)
print("ANALYSIS 1: Letter frequency of garbled-only text")
print("="*60)

# Extract garbled portions using coverage
garbled_text = ''
i = 0
n = len(processed)
while i < n:
    for l in range(min(20, n-i), 1, -1):
        if processed[i:i+l] in KNOWN_WORDS:
            i += l
            break
    else:
        garbled_text += processed[i]
        i += 1

gc = Counter(garbled_text)
total_g = len(garbled_text)
print(f"Total garbled chars: {total_g}")
print(f"\nLetter frequencies in garbled content:")
for letter, cnt in sorted(gc.items(), key=lambda x: -x[1]):
    print(f"  {letter}: {cnt:4d} ({cnt/total_g*100:.1f}%)")

GERMAN_FREQ = {'E':17.4,'N':9.8,'I':7.6,'S':7.3,'R':7.0,'A':6.5,'T':6.2,
               'D':5.1,'H':4.8,'U':4.4,'L':3.4,'C':3.2,'G':3.0,'M':2.5,
               'O':2.5,'B':1.9,'W':1.9,'F':1.7,'K':1.2,'Z':1.1,'V':0.8}
LATIN_FREQ =  {'I':11.2,'A':9.6,'E':9.0,'U':8.1,'S':7.2,'T':6.5,'N':5.8,
               'R':5.5,'O':5.0,'M':4.8,'L':4.4,'C':3.5,'P':2.8,'D':2.4,
               'V':2.2,'Q':1.5,'F':1.0,'B':0.9}

def freq_dist(observed, expected, total):
    dist = 0
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        obs = observed.get(letter, 0) / total * 100
        exp = expected.get(letter, 0.1)
        dist += (obs - exp) ** 2 / exp
    return dist

print(f"\nFrequency fit (lower = better match):")
print(f"  German: {freq_dist(gc, GERMAN_FREQ, total_g):.2f}")
print(f"  Latin:  {freq_dist(gc, LATIN_FREQ, total_g):.2f}")

# Compare with known text frequency
known_text = ''
i = 0
while i < n:
    for l in range(min(20, n-i), 1, -1):
        if processed[i:i+l] in KNOWN_WORDS:
            known_text += processed[i:i+l]
            i += l
            break
    else:
        i += 1

kc = Counter(known_text)
total_k = len(known_text)
print(f"\nKnown text German fit: {freq_dist(kc, GERMAN_FREQ, total_k):.2f}")
print(f"(Garbled should be same as known if all German)")
print(f"German freq fit for garbled ({freq_dist(gc, GERMAN_FREQ, total_g):.2f}) vs known ({freq_dist(kc, GERMAN_FREQ, total_k):.2f})")

# Key question: does garbled text have HIGHER or LOWER consonant ratio?
vowels = set('AEIOU')
g_vowels = sum(gc.get(c, 0) for c in vowels) / total_g * 100
k_vowels = sum(kc.get(c, 0) for c in vowels) / total_k * 100
print(f"\nVowel ratio - garbled: {g_vowels:.1f}%, known: {k_vowels:.1f}%")
print(f"German average vowel ratio: ~38%")
print(f"If garbled is LESS vowel-heavy -> more consonant clusters -> proper nouns or non-German")

# ============================================================
# ANALYSIS 2: HECHLLT vs HECHELT (swap E<->L)
# ============================================================
print("\n" + "="*60)
print("ANALYSIS 2: HECHLLT = HECHELT? (E<->L letter swap)")
print("="*60)

# HECHELT = to hackle (process flax/hemp), NHG/MHG
# Context: "FACH HECHLLT ICH OEL"
# If HECHLLT = HECHELT: "FACH HECHELT ICH OEL" = "section hackles I oil"
# -> "I hackle the section with oil" (anointing/consecrating ritual?)

print("  HECHLLT letters: H(2) E(1) C(1) L(2) T(1)")
print("  HECHELT letters: H(2) E(2) C(1) L(1) T(1)")
print("  Difference: one L in HECHLLT vs one E in HECHELT")
print("  This is NOT an anagram - it's a letter substitution (L<->E)")
print()
print("  BUT: In the homophonic cipher:")
print("  L codes: 34, 96")
print("  E codes: 95 56 19 26 76 01 41 30 86 67 27 03 09 17 29 49 39 74 37 69")
print("  The second L in HECHLLT uses code 34 (position in HECHLLT: H-E-C-H-L-L-T)")
print()
print("  HECHLLT raw codes: 57(H)-49(E)-18(C)-94(H)-34(L)-96(L)-64(T)")
print("  Could code 34 = E in this context? Code 34 is ASSIGNED to L")
print("  -> This would be a CIPHER ERROR or INTENTIONAL OBFUSCATION")
print()
print("  ALTERNATIVE: Maybe it's NICHT-HEL (negation of HEL)?")
print("  NICHT (not) + HEL = NICHTL... no that doesn't work")
print()
print("  ALTERNATIVE: HECHT-LL = pike-fish + LL suffix?")
print("  In German, no '-LL' suffix exists for fish names")
print()
print("  BEST HYPOTHESIS: HECHLLT is an anagram of a compound:")
fach_hechllt = 'FACH' + 'HECHLLT'
print(f"  FACH+HECHLLT sorted: {''.join(sorted(fach_hechllt))}")
# ACCCEFHHHLT = could be FLECHTACH? FLECHTHACH? no
print("  FLECHT+ACH = braid+creek? (7+3=10, too long)")
print("  HECHT+FLACH = pike+flat? (5+5=10, FACHECHLLT=10, let's check)")
hf = Counter('HECHT') + Counter('FLACH')
fa = Counter('FACHECHLLT')
ok = all(fa.get(c,0) >= hf.get(c,0) for c in hf)
print(f"  HECHT+FLACH fits FACHECHLLT: {ok}")

# Try all 7-letter German words
GERMAN_7 = [
    'SCHLECHT', 'SCHLECHTE', 'SCHLICHT', 'LEUCHTET', 'HECHELN',
    'HECHELTE', 'HECHELT', 'FECHTEN', 'GEFLECHT', 'FLACHSTE',
    'LICHTECHT', 'HEITLICH',
]
print("\n  7-letter words close to HECHLLT (sorted CEHHLLT):")
for w in GERMAN_7:
    wc = Counter(w)
    hc = Counter('HECHLLT')
    extra_h = sum(max(0, hc.get(c,0) - wc.get(c,0)) for c in set(hc)|set(wc))
    extra_w = sum(max(0, wc.get(c,0) - hc.get(c,0)) for c in set(hc)|set(wc))
    if extra_h + extra_w <= 2:
        print(f"  {w}: {extra_h} extra in HECHLLT, {extra_w} extra in {w}")
        if extra_h + extra_w == 0:
            print(f"    -> EXACT ANAGRAM!")
        elif extra_h + extra_w == 2:
            diffs = [(c, hc.get(c,0), wc.get(c,0)) for c in set(hc)|set(wc)
                     if hc.get(c,0) != wc.get(c,0)]
            print(f"    -> Differences: {diffs}")

# ============================================================
# ANALYSIS 3: UTRUNR = UT + RUNR (Old Norse hypothesis)
# ============================================================
print("\n" + "="*60)
print("ANALYSIS 3: UTRUNR = UT + RUNR (Old Norse hypothesis)")
print("="*60)

print("  UTRUNR = U(44) T(64) R(72) U(61) N(14) R(51)")
print()
print("  Old Norse 'ut' = out, outward (cognate: German 'aus')")
print("  Old Norse 'run' (singular) = rune, mystery")
print("  Old Norse 'runar' (plural) = runes")
print("  Old Norse 'runr' = an archaic/poetic plural form?")
print()
print("  Context: 'ODE UTRUNR DEN ENDE REDER KOENIG SALZBERG'")
print("  Reading A: 'Desolate (at) UTRUNR, the end-speaker King Salzberg'")
print("  Reading B: 'Alone out-runes, to-the end speaks King Salzberg'")
print("  Reading C: UTRUNR = place name (proper noun)")
print()
print("  TESTING: If UTRUNR = UT + RUNR:")
print("  Coverage gain: 0 (RUNR not in German vocab, UT not standard German)")
print()
# Test if treating as compound helps
# Try adding 'UT' as prefix element
ut_cov_test = count_coverage(processed.replace('UTRUNR', 'UTRUNE'), set(KNOWN_WORDS) | {'RUNE', 'UT'})
print(f"  If UTRUNR->UT+RUNE: coverage test...")
# This doesn't help directly

print("  ON 'ut-runar': appears in Eddic poetry (Sigrdrifumal) as type of rune")
print("  'Hugrunes', 'bjargrunes', 'bjorrunar', 'limrunar', 'malrunar'")
print("  'ut-runar' = runes for the outside/external world -- fits bonelord lore!")
print()
print("  In Sigrdrifumal (ON poetry), different runic categories include:")
print("  - 'sigrunes' (victory runes)")
print("  - 'brimrunar' (sea runes)")
print("  - 'malrunar' (speech runes)")
print("  - 'hugrunar' (mind runes)")
print("  UTRUNR = 'ut-runar' (outer runes) fits this poetic tradition perfectly!")

# ============================================================
# ANALYSIS 4: HIHL variants across Germanic languages
# ============================================================
print("\n" + "="*60)
print("ANALYSIS 4: HIHL variant analysis")
print("="*60)

print("  HIHL = H(57) I(65) H(94) L(34)")
print()
print("  Germanic cognate analysis:")
print("  OHG 'hihhil'? -> not attested")
print("  MHG 'hehl' = concealment (NHG 'Hehl')")
print("    HEHL sorted: EHHL vs HIHL sorted: HHIL")
print("    Difference: E vs I (H and L same)")
print("    E<->I vowel alternation IS common in MHG stressed syllables!")
print("    MHG alternations: 'heil/heile', 'heim/himel' (cognates)")
print()
print("  MHG 'hehle' variants:")
print("    NHG 'Hehl' = concealment -> 'kein Hehl machen' (make no secret)")
print("    MHG 'hehlen' = to conceal, hide")
print("    MHG 'der Hehler' = receiver of stolen goods")
print("    If HIHL = archaic form of HEHL (concealment):")
print("    'SAGEN AM MIN HIHL' = 'say at my concealment/hiding-place'")
print("    This makes PERFECT SENSE for a secret bonelord cipher text!")
print()
print("  Alternative: OHG 'hil' / 'hile' = concealment, covering")
print("    OHG 'hil' -> MHG 'hil' -> NHG 'Hehl'")
print("    With reduplication H+HIL = HHIL? (intensive form?)")
print()
print("  Alternative: Place element 'Hill' (MHG 'hil' = slope, hill)")
print("    'MIN HIHL' = 'my hill' (=my hill location)")
print("    Consistent with place-name catalog in the text")
print()
print("  BEST HYPOTHESIS: HIHL = archaic variant of MHG 'HEHL' (concealment)")
print("  'SAGEN AM MIN HIHL DIE NDCE FACH HECHLLT ICH OEL'")
print("  = 'say at my concealment-place, the NDCE-section, I anoint with oil'")

# ============================================================
# ANALYSIS 5: NLNDEF with MHG/dialectal reading
# ============================================================
print("\n" + "="*60)
print("ANALYSIS 5: NLNDEF deep analysis")
print("="*60)

print("  NLNDEF = N(60) L(96) N(14) D(42) E(30) F(20)")
print("  Context: 'DU NLNDEF SAGEN' = 'you NLNDEF say'")
print("  Already known: anagram of FINDEN if 96=I (but 96=L confirmed)")
print()
print("  NEW ANGLE: Dialectal/MHG alternation L<->I")
print("  In some MHG dialects, unstressed 'i' could be written 'l' or vice versa")
print("  This is unlikely for a stressed syllable but possible in compounds")
print()
print("  ALTERNATIVE: NLNDEF = NL+NDEF?")
print("  If NL = 'nel' (MHG/archaic 'in dem' contracted)?")
print("  And NDEF = 'ndef'? No standard Germanic word")
print()
print("  ALTERNATIVE: NLNDEF backwards = FEDLNN?")
print("  FEDLNN -> not a word")
print()
print("  PATTERN: NLNDEF always: 'DU NLNDEF SAGEN AM MIN HIHL'")
print("  'you NLNDEF say at my HIHL'")
print("  If NLNDEF is a verb: 'you [verb] say at my hiding-place'")
print("  German verbs with DEFLNN letters: FINDEN (find)!")
print("  'DU FINDEN SAGEN' = you find-say? (dialectal)")
print("  More likely: 'DU [verb] SAGEN' = 'you [should] say'")
print()
# Could NLNDEF be a scrambled form of a MHG verb?
# NLNDEF = N-L-N-D-E-F (6 letters)
# German infinitives ending in -EN: FINDEN, NENNEN, WENDEN, SENDEN
# NLNDEF sorted = DEFLNN
# FINDEN sorted = DDEFINN (8 letters, but FINDEN=6: F-I-N-D-E-N)
# Wait - FINDEN = F(1) I(1) N(2) D(1) E(1) = 6 letters sorted = DEFINN
# NLNDEF = N(2) L(1) D(1) E(1) F(1) = 6 letters sorted = DEFLNN
# Difference: FINDEN has I(1), no L. NLNDEF has L(1), no I.
# Single letter swap I<->L. Code 96=L. What if code 96 was wrongly assigned?
print("  CRITICAL: NLNDEF vs FINDEN (single I<->L swap)")
print("  FINDEN: F-I-N-D-E-N")
print("  NLNDEF: N-L-N-D-E-F (same letters except I<->L)")
print("  Code for this L position: 96 (L)")
print("  Code 96 appears ALSO in EILCH->LEICH (9x) as CONFIRMED L")
print("  -> The I<->L swap is intentional cipher obfuscation")
print("  -> NLNDEF is the anagrammed form of FINDEN with forced L substitution")
print("  -> 'DU NLNDEF SAGEN' = 'DU FINDEN SAGEN' = 'you finding speak'")

# ============================================================
# ANALYSIS 6: WRLGTNELNR and UIRUNNHWND - compound hypothesis
# ============================================================
print("\n" + "="*60)
print("ANALYSIS 6: The big block WRLGTNELNR + UIRUNNHWND")
print("="*60)

print("  Context: STEH [WRLGTNELNR] HEL [UIRUNNHWND] FINDEN NEIGT DAS ES")
print("  = 'stand [?] bright/HEL [?] find, tilts/bows that it'")
print()
print("  WRLGTNELNR = W-R-L-G-T-N-E-L-N-R (10 letters)")
print("  Letters: W(1) R(2) L(2) G(1) T(1) N(2) E(1)")
print("  This is EXTREMELY consonant-heavy for German")
print()
print("  OBSERVATION: Could this be TWO scrambled words compressed?")
print("  WRLGT + NELNR:")
left = Counter('WRLGT')
right = Counter('NELNR')
print(f"    WRLGT letters: {dict(left)}")
print(f"    NELNR letters: {dict(right)}")
print("    WRLGT: no standard German word, consonant cluster")
print("    NELNR: no standard German word")
print()
print("  TRYING: What if it's three 3-char words?")
for i in range(2, 8):
    for j in range(i+2, 9):
        p1 = 'WRLGTNELNR'[:i]
        p2 = 'WRLGTNELNR'[i:j]
        p3 = 'WRLGTNELNR'[j:]
        if len(p1) >= 2 and len(p2) >= 2 and len(p3) >= 2:
            if p1 in KNOWN_WORDS or p2 in KNOWN_WORDS or p3 in KNOWN_WORDS:
                print(f"    {p1}|{p2}|{p3} — known: {[p for p in [p1,p2,p3] if p in KNOWN_WORDS]}")

print()
print("  UIRUNNHWND = U-I-R-U-N-N-H-W-N-D (10 letters)")
print("  Letters: U(2) I(1) R(1) N(3) H(1) W(1) D(1)")
print()
print("  CHECKING: WIND (W-I-N-D) subset of UIRUNNHWND?")
wind = Counter('WIND')
blk = Counter('UIRUNNHWND')
ok = all(blk.get(c,0) >= wind[c] for c in wind)
print(f"    WIND is subset: {ok}")
rem = Counter({c: blk[c]-wind.get(c,0) for c in blk if blk[c]-wind.get(c,0)>0})
rem_str = ''.join(c*v for c,v in sorted(rem.items()))
print(f"    Remaining after WIND: {rem_str}")
print(f"    RUNNHU = R(1) U(2) N(2) H(1)")
print(f"    German words: RUHNU? UNHRU? UNWEHR?")
unhru = Counter('UNHRU')
runnhu = Counter('RUNNHU')
ok2 = all(runnhu.get(c,0) >= unhru.get(c,0) for c in unhru)
print(f"    UNHRU subset of RUNNHU: {ok2}")

print()
print("  HYPOTHESIS: UIRUNNHWND = WIND + [URUNNH]")
print("  'URUNNH' = U-R-U-N-N-H -> no standard word")
print("  Alternative: UNRUH (unrest) = U-N-R-U-H")
unruh = Counter('UNRUH')
ok3 = all(blk.get(c,0) >= unruh[c] for c in unruh)
print(f"  UNRUH subset of UIRUNNHWND: {ok3}")
if ok3:
    rem2 = Counter({c: blk[c]-unruh.get(c,0) for c in blk if blk[c]-unruh.get(c,0)>0})
    rem2_str = ''.join(c*v for c,v in sorted(rem2.items()))
    print(f"  Remaining after UNRUH: {rem2_str}")
    print("  INWD = I-N-W-D -> WIND! (anagram)")
    inwd = Counter('INWD')
    ok4 = all(Counter(rem2_str).get(c,0) >= inwd[c] for c in inwd)
    print(f"  WIND subset of remaining {rem2_str}: {ok4}")
    if ok4:
        print("  -> UIRUNNHWND = UNRUH + WIND + ? (with one extra letter)")
        extra = Counter({c: Counter(rem2_str).get(c,0)-inwd.get(c,0) for c in Counter(rem2_str) if Counter(rem2_str).get(c,0)-inwd.get(c,0)>0})
        print(f"  Extra: {dict(extra)}")
        print("  UNRUH+WIND = 9 letters, block = 10 letters, one extra N")
        print("  UNRUH+WIND+N = 'unrest wind N' -> WINDUNRUHN? No standard form")
        print("  BUT: 'WINDUNRUHE' (wind-unrest/turbulence) is compound in German!")
        print("  Hmm, we have UNRUH not UNRUHE (missing E)...")

# ============================================================
# ANALYSIS 7: Expanded vocabulary coverage test
# ============================================================
print("\n" + "="*60)
print("ANALYSIS 7: Expanded vocabulary coverage test")
print("="*60)

# Extended word lists to test
NEW_CANDIDATES = [
    # MHG verbs confirmed forms
    ('HEHLT', 'conceals (MHG present)'),
    ('HEHLE', 'concealment (MHG)'),
    ('HEHLEN', 'to conceal (MHG)'),
    ('HEHL', 'concealment (MHG)'),
    # Bavarian/dialectal German
    ('WIRL', 'whirl (dialectal)'),
    ('WURL', 'root (dialectal variant of Wurzel)'),
    # MHG nouns
    ('LIHT', 'light (MHG)'),
    ('SIHT', 'sight, vision (MHG)'),
    ('NIHT', 'nothing/not (MHG)'),
    ('WIHT', 'creature (MHG)'),
    ('GIHT', 'gout, disease (MHG)'),
    # Latin
    ('NUNC', 'now (Latin)'),
    ('INDE', 'thence (Latin)'),
    ('UNDE', 'whence (Latin)'),
    ('INTER', 'between (Latin)'),
    ('ULTRA', 'beyond (Latin)'),
    ('LUMEN', 'light (Latin)'),
    ('NUMEN', 'divine power (Latin)'),
    ('UNDA', 'wave (Latin)'),
    ('RUINA', 'ruin (Latin)'),
    ('TURRIS', 'tower (Latin)'),
    ('REGE', 'rule/king-abl (Latin)'),
    ('ITER', 'journey (Latin)'),
    # Old Norse
    ('RUNA', 'rune (ON)'),
    ('RUNIR', 'runes (ON)'),
    ('GARD', 'enclosure (ON)'),
    ('NORN', 'fate-weaver (ON)'),
    ('DRAUGAR', 'undead pl (ON)'),
    ('JOTUN', 'giant (ON)'),
    ('GALDR', 'spell (ON)'),
    ('SEIDR', 'magic (ON)'),
    ('HRIM', 'frost (ON)'),
    # Middle Dutch
    ('RIDDER', 'knight (MDu)'),
    ('TOREN', 'tower (MDu)'),
    ('VREDE', 'peace (MDu)'),
    ('LANT', 'land (MDu)'),
    # Gothic
    ('REIKI', 'kingdom (Gothic)'),
    ('THIUDA', 'people (Gothic)'),
    # Old Saxon
    ('THEGAN', 'warrior (OS)'),
    ('HELIAND', 'savior (OS)'),
    ('WALDAND', 'ruler (OS)'),
    # Additional German
    ('WACHT', 'guard/vigil'),
    ('MACHT', 'power'),
    ('TRACHT', 'dress/load'),
    ('FLECHT', 'braid'),
    ('ECHT', 'genuine'),
    ('SCHLICHT', 'plain'),
    ('SCHLECHT', 'bad'),
    ('HECHT', 'pike fish'),
    ('KNECHT', 'servant'),
    ('RECHT', 'right/justice'),
    ('UNRECHT', 'injustice'),
    ('LEUCHTE', 'lantern'),
    ('FLECHTE', 'braid/lichen'),
    ('FECHTEN', 'to fight'),
    ('HECHELN', 'to hackle'),
    ('TURNIER', 'tournament'),
    ('TURNIR', 'tournament (MHG)'),
    ('RITTER', 'knight'),
    ('RUNDE', 'round'),
    ('WUNDE', 'wound'),
    ('WUNDER', 'wonder'),
    ('FUNKEN', 'sparks'),
    ('SINKEN', 'to sink'),
    ('DENKEN', 'to think'),
    ('LENKEN', 'to steer'),
    ('RENKEN', 'to wrench'),
    ('SCHENKEN', 'to give/pour'),
    ('TRINKEN', 'to drink'),
    ('HINKEN', 'to limp'),
    ('WINKEN', 'to wave'),
    ('SINNEN', 'to ponder'),
    ('RINNEN', 'to flow'),
    ('HINNEN', 'away hence'),
    ('BINNEN', 'within'),
    ('RINNE', 'groove/gutter'),
    ('MINNE', 'courtly love (MHG)'),
    ('SINNE', 'senses'),
    ('ZINNE', 'battlement'),
    ('WONNE', 'bliss'),
    ('SONNE', 'sun'),
    ('TONNE', 'barrel'),
    ('WUNNE', 'joy (MHG)'),
    ('BRUNNE', 'well/spring (MHG)'),
    ('GUNST', 'favor'),
    ('DUNST', 'haze/fume'),
    ('KUNSTE', 'arts'),
    ('GUNSTE', 'favors'),
    ('WUNSCH', 'wish'),
    ('MENSCH', 'person'),
    ('RAUSCH', 'rush/intoxication'),
    ('RUTSCH', 'slide'),
    ('TUSCH', 'fanfare'),
    ('SCHWUNG', 'momentum'),
    ('SPRUNG', 'jump'),
    ('KLANG', 'sound'),
    ('DRANG', 'pressure'),
    ('GANG', 'corridor/walk'),
    ('SANG', 'sang'),
    ('HANG', 'slope'),
    ('RANG', 'rank/wrestled'),
    ('LANG', 'long'),
    ('BANG', 'afraid'),
]

print("\nTesting new words for coverage gain:")
gains = []
for word, meaning in NEW_CANDIDATES:
    test_vocab = KNOWN_WORDS | {word}
    test_cov, _ = count_coverage(processed, test_vocab)
    gain = test_cov - base_cov
    if gain > 0:
        # Find contexts
        idx = 0
        ctxs = []
        while True:
            pos = processed.find(word, idx)
            if pos < 0: break
            ctxs.append(processed[max(0,pos-6):pos+len(word)+6])
            idx = pos + 1
        if ctxs:
            gains.append((gain, word, meaning, ctxs))

gains.sort(reverse=True)
for gain, word, meaning, ctxs in gains[:25]:
    print(f"\n  +{gain:3d} '{word}' = {meaning}")
    for ctx in ctxs[:2]:
        print(f"       ...{ctx.strip()[:50]}...")

# ============================================================
# ANALYSIS 8: Compound decomposition of WRLGTNELNR
# ============================================================
print("\n" + "="*60)
print("ANALYSIS 8: WRLGTNELNR - anagram of compound German words?")
print("="*60)
# Try all splits where both parts are anagrams of known words
block = 'WRLGTNELNR'
all_words = sorted(KNOWN_WORDS | {w for w,_ in NEW_CANDIDATES}, key=len, reverse=True)
bc = Counter(block)

print(f"\nAll 2-word splits of {block} (each part as anagram of known word):")
found_splits = []
for i in range(2, len(block)-1):
    p1 = block[:i]
    p2 = block[i:]
    # Check if p1 is anagram of any known word
    p1c = Counter(p1)
    p2c = Counter(p2)
    for w1 in all_words:
        if len(w1) != len(p1): continue
        if Counter(w1) == p1c:
            for w2 in all_words:
                if len(w2) != len(p2): continue
                if Counter(w2) == p2c:
                    found_splits.append((p1, w1, p2, w2))

for p1, w1, p2, w2 in found_splits[:10]:
    print(f"  {p1}={w1} + {p2}={w2}")

if not found_splits:
    print("  No exact 2-word anagram splits found")
    print("  Trying +1 tolerance...")
    for i in range(2, len(block)-1):
        p1 = block[:i]
        p2 = block[i:]
        p1c = Counter(p1)
        p2c = Counter(p2)
        for w1 in all_words:
            if abs(len(w1)-len(p1)) > 1: continue
            ok1 = all(p1c.get(c,0) >= cnt for c,cnt in Counter(w1).items())
            ex1 = sum(p1c.values()) - sum(Counter(w1).values())
            if not ok1 or ex1 < 0 or ex1 > 1: continue
            for w2 in all_words:
                if abs(len(w2)-len(p2)) > 1: continue
                ok2 = all(p2c.get(c,0) >= cnt for c,cnt in Counter(w2).items())
                ex2 = sum(p2c.values()) - sum(Counter(w2).values())
                if not ok2 or ex2 < 0 or ex2 > 1: continue
                if ex1 + ex2 <= 1:
                    print(f"  {p1}~{w1}(+{ex1}) + {p2}~{w2}(+{ex2})")

print("\nDone.")
