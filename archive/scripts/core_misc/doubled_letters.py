"""
Investigate the doubled-letter phenomenon in the cipher.
Are doubled letters an artifact of homophonic encoding, or intentional?
"""
import json
import os
from collections import Counter

data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'final_mapping_v4.json'), 'r') as f:
    mapping = json.load(f)

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    def ic(counts, total):
        if total <= 1: return 0
        return sum(c*(c-1) for c in counts.values()) / (total*(total-1))
    return 0 if ic(Counter(bp0), len(bp0)) > ic(Counter(bp1), len(bp1)) else 1

def decode(book, m=mapping):
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    return ''.join(m.get(p, '?') for p in pairs), pairs

# ============================================================
# 1. COUNT ALL DOUBLED LETTERS
# ============================================================
print("=" * 80)
print("1. DOUBLED LETTER CENSUS")
print("=" * 80)

double_counts = Counter()
double_code_pairs = Counter()

for i, book in enumerate(books):
    dec, pairs = decode(book)
    for k in range(len(dec) - 1):
        if dec[k] == dec[k+1]:
            double_counts[dec[k]] += 1
            if k < len(pairs) - 1:
                double_code_pairs[(pairs[k], pairs[k+1])] += 1

print(f"\n  Double letter frequencies:")
for letter, count in double_counts.most_common():
    # Expected doubles in German text
    print(f"    {letter}{letter}: {count:3d}x")

print(f"\n  Total doubled pairs: {sum(double_counts.values())}")
print(f"  Total decoded chars: {sum(len(decode(b)[0]) for b in books)}")
pct = sum(double_counts.values()) / sum(len(decode(b)[0]) for b in books) * 100
print(f"  Double rate: {pct:.1f}%")

# ============================================================
# 2. ARE DOUBLES FROM SAME OR DIFFERENT CODES?
# ============================================================
print(f"\n{'='*80}")
print("2. SAME-CODE vs DIFFERENT-CODE DOUBLES")
print(f"{'='*80}")

same_code = 0
diff_code = 0
same_examples = []
diff_examples = []

for i, book in enumerate(books):
    dec, pairs = decode(book)
    for k in range(len(dec) - 1):
        if dec[k] == dec[k+1] and k < len(pairs) - 1:
            if pairs[k] == pairs[k+1]:
                same_code += 1
                if len(same_examples) < 10:
                    ctx = dec[max(0,k-3):k+5]
                    same_examples.append(f"Bk{i}: {pairs[k]}+{pairs[k+1]}={dec[k]}{dec[k+1]} in '{ctx}'")
            else:
                diff_code += 1
                if len(diff_examples) < 10:
                    ctx = dec[max(0,k-3):k+5]
                    diff_examples.append(f"Bk{i}: {pairs[k]}+{pairs[k+1]}={dec[k]}{dec[k+1]} in '{ctx}'")

print(f"\n  Same code: {same_code} ({same_code/(same_code+diff_code)*100:.1f}%)")
print(f"  Diff code: {diff_code} ({diff_code/(same_code+diff_code)*100:.1f}%)")

print(f"\n  Same-code examples:")
for ex in same_examples:
    print(f"    {ex}")

print(f"\n  Diff-code examples:")
for ex in diff_examples:
    print(f"    {ex}")

# ============================================================
# 3. WHICH DOUBLES ARE LEGITIMATE GERMAN?
# ============================================================
print(f"\n{'='*80}")
print("3. LEGITIMATE vs SUSPICIOUS DOUBLES")
print(f"{'='*80}")

# In German, legitimate double letters:
# LL: alle, sollen, voll, stille, schnell
# NN: dann, denn, wenn, koennen, Mann
# SS: wasser, wissen, dass, muss
# TT: Mutter, Ritter, Blatt, Gott
# EE: See, Meer, Tee, Schnee, Seele
# MM: kommen, Flamme, Himmel
# FF: Affe, schaffen, Schiff
# RR: Herr, irren
# PP: Mappe, Grippe
# BB: Ebbe
# DD: rare
# CC: not in German
# GG: not standard
# HH: not standard
# II: not standard (but Bonelord text has many!)
# UU: not standard
# AA: Haar, Aal, Saal

legitimate_doubles = {'LL', 'NN', 'SS', 'TT', 'EE', 'MM', 'FF', 'RR', 'PP', 'AA'}
suspicious_doubles = set()

for letter, count in double_counts.most_common():
    dd = letter + letter
    status = "LEGITIMATE" if dd in legitimate_doubles else "SUSPICIOUS"
    if dd not in legitimate_doubles:
        suspicious_doubles.add(letter)
    print(f"  {dd}: {count:3d}x - {status}")

# ============================================================
# 4. TRACE II DOUBLES (most suspicious)
# ============================================================
print(f"\n{'='*80}")
print("4. ALL II DOUBLES WITH FULL CONTEXT")
print(f"{'='*80}")

ii_contexts = []
for i, book in enumerate(books):
    dec, pairs = decode(book)
    for k in range(len(dec) - 1):
        if dec[k] == 'I' and dec[k+1] == 'I' and k < len(pairs) - 1:
            ctx = dec[max(0,k-8):min(len(dec),k+10)]
            codes = f"{pairs[k]}+{pairs[k+1]}"
            ii_contexts.append((i, k, codes, ctx))

print(f"\n  Total II occurrences: {len(ii_contexts)}")
for bi, pos, codes, ctx in ii_contexts:
    print(f"    Bk{bi:2d} pos {pos:3d}: [{codes}] ...{ctx}...")

# ============================================================
# 5. TEST: WHAT IF II = SINGLE I? (re-decode)
# ============================================================
print(f"\n{'='*80}")
print("5. HYPOTHESIS: SOME CODES PRODUCE 'NOTHING' (NULL)")
print(f"{'='*80}")

# What if certain code pairs that produce doubled letters actually
# mean "this letter is long" or "stress marker" rather than a second letter?
# In other words: what if II should be read as I (with emphasis)?
# This is similar to how bonelords might use number-based emphasis.

# Count how many II appear in contexts where a single I would make a word
def collapse_doubles(text):
    if not text: return text
    result = [text[0]]
    for c in text[1:]:
        if c != result[-1]:
            result.append(c)
    return ''.join(result)

GERMAN = set("""
ab aber acht alle allem allen aller alles als also alt alte altem alten alter altes am an andere
anderem anderen anderer anderes ans auch auf aus
bei beim bis bisher da dabei damit dann das dass de dem den denen denn
der deren des dessen die dies diese diesem diesen dieser dieses dir doch dort drei durch
ein eine einem einen einer einige einiger einiges einst em en ende er erde erst erste
ersten erster erstes es etwa etwas
fach fand fest finden fuer ganz gar geh geheim gehen gegen geben gibt ging gott gross gut
hab habe haben hat heer heere her herr hier hin
ich ihm ihn ihr ihre ihrem ihren ihrer im in ins ist
ja jede jedem jeden jeder jedes klar koenig koenige koenigen koenigs kommen kam kann
lang lage land lande last leid licht
macht mehr mein meine meinem meinen meiner min mir mit muss
nach nacht nah nahe name namen neben neu neue neuem neuen neuer neues nicht nichts noch
nun nur ob oder ohne ort orte orten
platz rat recht rede reden rein rest ruin ruine ruinen rune runen runeort
see sehr sei seid sein seine seinem seinen seiner seit
sie sind so soll sollen sonne steil stein steine steinen stieg
tag tage tagen teil teile teilen tod tot tun tut
ueber um und uns unter uralte uralten
vier viel viele vielen vom von vor
wahr wahrheit war was wasser weg weil welt wenn wer wie wir wird wissen wisset wisst wo wohl wort
auch blick dunkel feind flucht gift grabe heer kraft neid recht schau schar sieg tief
weit wild zorn bild blut burg dorf eben feld fort gang grab haus herz hoch
kalt kern klug last leer letzt link mass naht nein nord rand raum ring
rund sache scharf schlecht schnell schwer still stolz streng stuck stumm suche
traum treue trost turm volk wache wand zehn ziel zug
garen gar ren ann gen ser tier net ode oede
dieser diese dieses seinen seiner seines
toten toter totes tote tod rune stein steine steinen
erde erden koenig koenige
gesehen sehen schauen schaun
derer deren dessen jenen jene jener jenem
eines einer einem einen
herr herrn herren
oben unten rechts links
naechst naechste naechsten
wo woher wohin wovon
dazu dahin dahinter daher
neues neuen neuer neuem
alte alten alter altes
erste ersten erster erstes
lauern lauernd lauernde
nicht nichts wind winde winden
wisset weiset weisen
schwiteio tharsc totniurg hearuchtiger tautr eilch labgzeras minheddem utrunr
labrrni aunrsongetrases uongetrases
""".split())

# ============================================================
# 6. KEY PATTERN: NDCE, NDT, NDGE, NDTEI
# ============================================================
print(f"\n{'='*80}")
print("6. ND-PREFIX PATTERNS")
print(f"{'='*80}")

nd_patterns = Counter()
for i, book in enumerate(books):
    dec, pairs = decode(book)
    for k in range(len(dec) - 1):
        if dec[k] == 'N' and dec[k+1] == 'D':
            # Get the following chars
            following = dec[k:min(len(dec), k+8)]
            nd_patterns[following[:min(6, len(following))]] += 1

print(f"\n  ND+ patterns (first 6 chars):")
for pat, count in nd_patterns.most_common(20):
    print(f"    {pat:10s} {count:3d}x")

# ============================================================
# 7. CODE-LEVEL ANALYSIS: IS THERE A MISSING SPACE/SEPARATOR?
# ============================================================
print(f"\n{'='*80}")
print("7. WORD BOUNDARY HYPOTHESIS")
print(f"{'='*80}")

# The ND patterns might be word boundaries that got merged.
# "UND" (and), "END" (end), "RUND" (round), "GRUND" (ground)
# What if many "ND" sequences are actually the end of UND/END?
# Let's look at what comes BEFORE each ND:
before_nd = Counter()
for i, book in enumerate(books):
    dec, pairs = decode(book)
    for k in range(1, len(dec) - 1):
        if dec[k] == 'N' and dec[k+1] == 'D':
            before = dec[max(0,k-5):k]
            after = dec[k+2:min(len(dec),k+7)]
            before_nd[f"{before}|ND|{after}"] += 1

print(f"\n  Context around ND (top 25):")
for ctx, count in before_nd.most_common(25):
    # Is the part before ND the end of a word?
    parts = ctx.split('|')
    if len(parts) == 3:
        before, _, after = parts
        # Check if before ends with a word
        notes = ''
        bl = before.lower()
        if bl.endswith('u'): notes = '<- UND?'
        elif bl.endswith('e'): notes = '<- ENDE?'
        elif bl.endswith('ei'): notes = '<- SEIN/DEIN?'
        elif bl.endswith('i'): notes = '<- KIND?'
        print(f"    ...{before}|ND|{after}... {count:2d}x  {notes}")

# ============================================================
# 8. FACH PATTERN ANALYSIS
# ============================================================
print(f"\n{'='*80}")
print("8. FACH + HECHLLT + ICH OEL PATTERN")
print(f"{'='*80}")

# The sequence "FACHHECHLLTICHOEL" appears 5 times
# FACH = compartment/profession/fold
# HECHLLT = ??? (collapsed: HECHLT)
# ICH = I
# OEL = oil? Or OE = archaic O?
# Full: "NDCE FACH HECHLLT ICH OEL SO DEN HIER TAUTR"

# Let me try reading HECHLLT differently
# HECH + LLT: HECHT (pike) is H-E-C-H-T, our text has H-E-C-H-L-L-T
# What if one L is wrong? Code 34=L, what if one should be something else?

# Trace the HECHLLT codes: 57-19-18-94-34-34-64
# 57=H, 19=E, 18=C, 94=H, 34=L, 34=L, 64=T
# The two L's are the SAME code (34+34)!
# This means either:
# a) The plaintext genuinely has LL here (like HECHELN -> HECHELLT -> HECHLLT in dialect?)
# b) Code 34 is actually a different letter here (but it's used as L everywhere else)

print(f"  HECHLLT codes: 57(H) 19(E) 18(C) 94(H) 34(L) 34(L) 64(T)")
print(f"  Both L's are code 34 -- same code repeated")
print(f"")
print(f"  Possible readings:")
print(f"    HECHELT -> verb 'hecheln' (to hackle/pant), past participle")
print(f"    HECHLET -> verb 'hecheln', archaic conjugation")
print(f"    If LL -> L: HECHLT -> truncated HECHELT")
print(f"    If read as: ... FACH HECHT ICH ... (pike/compartment I)")
print(f"       But codes give LLT not T, so HECHT doesn't work")

# ============================================================
# 9. OEL PATTERN
# ============================================================
print(f"\n{'='*80}")
print("9. OEL PATTERN ANALYSIS")
print(f"{'='*80}")

for i, book in enumerate(books):
    dec, pairs = decode(book)
    if 'OEL' in dec:
        pos = dec.find('OEL')
        ctx = dec[max(0,pos-10):min(len(dec),pos+13)]
        codes_ctx = pairs[pos:pos+3]
        print(f"  Bk{i:2d}: ...{ctx}...")
        print(f"         OEL codes: {' '.join(codes_ctx)}")

print(f"\n  OEL interpretations:")
print(f"    OEL = OeL = oil (German: Oel)")
print(f"    OE = Oe (O-umlaut) -> OeL = oil")
print(f"    But in context: 'HECHLLT ICH OEL SO DE' = '??? I oil so the' -- odd")
print(f"    Alternative: ICH OELE SO = 'I oil/anoint so' (verb oelen = to oil)")
print(f"    Or: I + CHOEL = ?")
print(f"    Or repartition: HE + CHLL + TICHOEL -> ?")

# ============================================================
# 10. SCE PATTERN (8x)
# ============================================================
print(f"\n{'='*80}")
print("10. SCE PATTERN ANALYSIS")
print(f"{'='*80}")

for i, book in enumerate(books):
    dec, pairs = decode(book)
    for k in range(len(dec) - 2):
        if dec[k:k+3] == 'SCE':
            ctx = dec[max(0,k-10):min(len(dec),k+13)]
            sce_codes = pairs[k:k+3]
            print(f"  Bk{i:2d} pos {k:3d}: ...{ctx}...")
            print(f"                SCE codes: {' '.join(sce_codes)}")

print(f"\n  SCE interpretations:")
print(f"    SC is not a natural German digraph (SCH is)")
print(f"    Could code 18(C) sometimes = CH? No, C is always C in our mapping")
print(f"    SCE reversed = ECS -> part of WECHSEL?")
print(f"    S + CE -> part of SZENE? No, that would be SZ")
print(f"    Boundary: ...S | CE... or ...SC | E...")

# ============================================================
# 11. HIHL PATTERN (8x)
# ============================================================
print(f"\n{'='*80}")
print("11. HIHL PATTERN ANALYSIS")
print(f"{'='*80}")

for i, book in enumerate(books):
    dec, pairs = decode(book)
    if 'HIHL' in dec:
        pos = dec.find('HIHL')
        ctx = dec[max(0,pos-10):min(len(dec),pos+14)]
        codes_ctx = pairs[pos:pos+4]
        print(f"  Bk{i:2d}: ...{ctx}...")
        print(f"         HIHL codes: {' '.join(codes_ctx)}")

print(f"\n  HIHL interpretations:")
print(f"    Collapsed: HIHL -> no change (no doubles)")
print(f"    H-I-H-L: two H's separated by I")
print(f"    IHL = part of 'Pfuehl' (pool/swamp)?")
print(f"    HIHL reversed = LHIH -> ?")
print(f"    Could be a proper noun or place name")
print(f"    Context always: MINHIHLDIE -> MIN + HIHL + DIE")
print(f"    MIN = my/mine (archaic) or MHG 'minne' (love)")
print(f"    If HIHL is a name: 'my/mine HIHL the...'")

# ============================================================
# 12. TEIGN PATTERN (8x)
# ============================================================
print(f"\n{'='*80}")
print("12. TEIGN PATTERN ANALYSIS")
print(f"{'='*80}")

for i, book in enumerate(books):
    dec, pairs = decode(book)
    if 'TEIGN' in dec:
        pos = dec.find('TEIGN')
        ctx = dec[max(0,pos-10):min(len(dec),pos+15)]
        codes_ctx = pairs[pos:pos+5]
        print(f"  Bk{i:2d}: ...{ctx}...")
        print(f"         TEIGN codes: {' '.join(codes_ctx)}")

print(f"\n  TEIGN interpretations:")
print(f"    T + EIGN -> EIGEN (own/self) with leading T?")
print(f"    -> '...T EIGEN DAS ES' = 'his/its own property the it'")
print(f"    TE + IGN -> ?")
print(f"    TEIG + N -> TEIG (dough) + N? Unlikely in this context")
print(f"    If T is end of previous word: '...T | EIGNDASES'")
print(f"    EIGEN + DAS + ES = 'own/self that it'")
print(f"    This makes sense! TEIGN = T (from prev word) + EIGN (from EIGEN)")

# ============================================================
# 13. COMPREHENSIVE WORD BOUNDARY RE-ANALYSIS
# ============================================================
print(f"\n{'='*80}")
print("13. WORD BOUNDARY RE-ANALYSIS (Book 5)")
print(f"{'='*80}")

# Book 5 is the most complete. Let me manually trace every character.
dec5, pairs5 = decode(books[5])
print(f"\n  Raw text ({len(dec5)} chars): {dec5}")
print(f"\n  Codes: {' '.join(pairs5)}")

# Manual word boundary analysis
# EN HIER TAUTR IST EILCH AN HEARUCHTIGER SO DASS TUN DIESER T EINER SEINE DE TOTNIURG SEE R LABRRNI WIR UND IE MINHEDDEM I DIE URALTE STEINEN T ER AD THARSC IST SCHAUN RU

# Let me try a different reading:
print(f"\n  MANUAL RE-PARSE of Book 5:")
# Position-by-position
text = dec5
print(f"    Position 0-3:   '{text[0:4]}'  = EN + HIER")
print(f"    Position 4:     '{text[4:9]}'   = TAUTR")
print(f"    Position 9-11:  '{text[9:12]}'  = IST")
print(f"    Position 12-16: '{text[12:17]}' = EILCH")
print(f"    Position 17-18: '{text[17:19]}' = AN")
print(f"    Position 19-31: '{text[19:31]}' = HEARUCHTIGER")
print(f"    Position 31-32: '{text[31:33]}' = SO")
print(f"    Position 33-36: '{text[33:37]}' = DASS")
print(f"    Position 37-39: '{text[37:40]}' = TUN")
print(f"    Position 40-45: '{text[40:46]}' = DIESER")

# The tricky part starts here
print(f"    Position 46:    '{text[46]}'    = T (end of DIESERT? or separate)")
print(f"    Position 47-51: '{text[47:52]}' = EINER")
print(f"    Position 52-56: '{text[52:57]}' = SEINE")
print(f"    Position 57-58: '{text[57:59]}' = DE")
print(f"    Position 59-66: '{text[59:67]}' = TOTNIURG")
print(f"    Position 67-69: '{text[67:70]}' = SEE")

# After SEE
print(f"    Position 70:    '{text[70]}'    = R")
print(f"    Position 71-76: '{text[71:77]}' = LABRRNI")
print(f"    Position 77-79: '{text[77:80]}' = WIR")
print(f"    Position 80-82: '{text[80:83]}' = UND")
print(f"    Position 83-84: '{text[83:85]}' = IE")
print(f"    Position 85-93: '{text[85:94]}' = MINHEDDEM")
print(f"    Position 94:    '{text[94]}'    = I")
print(f"    Position 95-97: '{text[95:98]}' = DIE")
print(f"    Position 98-103:'{text[98:104]}'= URALTE")
print(f"    Position 104-111:'{text[104:112]}'= STEINEN (+ T?)")

remaining_text = text[112:]
print(f"    Position 112+:  '{remaining_text}' = T ER AD THARSC IST SCHAUN RU...")

# Key insight: DIESERT = DIESER + T?
# Or: DIES ER T EINER = "dies er tat einer" (this he did, one...)
# T could be part of an archaic verb TAT (did)
print(f"\n  KEY INSIGHT: The 'T' at position 46:")
print(f"    Reading A: DIESER | T | EINER = 'this one | T | one'")
print(f"    Reading B: DIES | ER | TEINER = 'this | he | ?' ")
print(f"    Reading C: DIES ER T | EINER = 'this he did | one' (T=tat truncated?)")
print(f"    Code at pos 46: {pairs5[46]} = {mapping.get(pairs5[46], '?')}")
