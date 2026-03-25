"""
Deep code-level analysis of remaining unknowns.
For each recurring unknown segment, trace the exact codes and test
if changing a single code assignment would create German words.
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
# 1. CODE-LEVEL TRACES OF KEY UNKNOWNS
# ============================================================
print("=" * 80)
print("1. CODE TRACES FOR RECURRING UNKNOWNS")
print("=" * 80)

# For each unknown, find ALL occurrences and show the code pairs
targets = [
    'HECHLLT', 'HIHL', 'SCE', 'OEL', 'GEVM', 'NDTEII', 'AEUT',
    'NSCHA', 'GEIGET', 'TTUIGAA', 'ITGHNEE', 'DUNLN', 'NRUI',
    'SCHWITEIO', 'NDGE', 'IEO', 'NDCE'
]

code_traces = {}  # target -> list of code sequences

for target in targets:
    occurrences = []
    for i, book in enumerate(books):
        dec, pairs = decode(book)
        pos = 0
        while True:
            p = dec.find(target, pos)
            if p == -1:
                break
            codes = pairs[p:p+len(target)]
            # Also get wider context codes
            ctx_start = max(0, p-3)
            ctx_end = min(len(pairs), p+len(target)+3)
            ctx_dec = dec[ctx_start:ctx_end]
            ctx_codes = pairs[ctx_start:ctx_end]
            occurrences.append({
                'book': i,
                'pos': p,
                'codes': codes,
                'ctx': ctx_dec,
                'ctx_codes': ctx_codes
            })
            pos = p + 1

    code_traces[target] = occurrences
    if occurrences:
        # Check if codes are always the same
        code_strs = [' '.join(o['codes']) for o in occurrences]
        unique_codes = set(code_strs)
        print(f"\n  {target} ({len(occurrences)}x, {len(unique_codes)} unique code pattern(s)):")
        for uc in sorted(unique_codes):
            count = code_strs.count(uc)
            # Show context for first occurrence with this code pattern
            for o in occurrences:
                if ' '.join(o['codes']) == uc:
                    print(f"    [{uc}] {count}x -- Bk{o['book']}: ...{o['ctx']}...")
                    break

# ============================================================
# 2. SINGLE-CODE SUBSTITUTION TEST
# ============================================================
print(f"\n\n{'='*80}")
print("2. SINGLE-CODE SUBSTITUTION: WHAT IF ONE CODE IS WRONG?")
print(f"{'='*80}")

# German words that could appear if we change one letter in unknowns
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
platz rat recht rede reden rein rest ruin rune runen runeort
see sehr sei seid sein seine seinem seinen seiner seit
sie sind so soll sollen sonne steil stein steine steinen stieg
tag tage tagen teil teile teilen tod tot tun tut
ueber um und uns unter uralte uralten
vier viel viele vielen vom von vor
wahr wahrheit war was wasser weg weil welt wenn wer wie wir wird wissen wo wohl wort
garen gar ren ann gen ser tier net ode oede
nicht nichts wind winde winden
derer deren dessen eines einer einem einen
herr herrn herren hoch hohe hohem hohen hoher hohes
alt alten alter altes oben unten rechts links
dazu dahin dahinter daher neues neuen neuer neuem
lauern lauernd lauernde augen sehen schauen blick
dunkel dunkle dunklen dunkler feind flucht gift grabe
kraft neid recht schar sieg weit wild zorn
bild blut burg dorf eben feld fort gang grab haus herz
kern klug last leer letzt link mass naht nein nord rand raum ring
rund sache scharf schlecht schnell schwer still stolz streng
traum treue trost turm volk wache wand zehn ziel zug
halten halt hielt finden fand sehen sah stehen stand
gehen ging kommen kam sprechen sprach nehmen nahm
geben gab lesen las schreiben schrieb treiben trieb
setzen legen stellen graben
licht dunkel norden sueden osten westen
schwert gold silber bronze eisen feuer flamme
koenig koenigin koenigreich reich
burg berge berg tor
heil heilen heilig heils
""".split())

# For each unknown, try changing each position to all 22 letters
for target in ['HECHLLT', 'SCE', 'OEL', 'GEVM', 'NDTEII', 'AEUT',
               'NSCHA', 'NRUI', 'DUNLN', 'IEO', 'NDCE']:
    matches = []

    tl = target.lower()

    # Single substitution
    for i in range(len(tl)):
        for c in 'abcdefghijklmnoprstuvwz':
            if c == tl[i]:
                continue
            candidate = tl[:i] + c + tl[i+1:]
            if candidate in GERMAN:
                matches.append(f"  pos {i}: {tl[i]}->{c} = {candidate.upper()}")
            # Also check if it's a prefix of a word
            for w in GERMAN:
                if w.startswith(candidate) and len(w) <= len(candidate)+2:
                    if candidate != w:
                        matches.append(f"  pos {i}: {tl[i]}->{c} = {candidate.upper()} (prefix of {w.upper()})")
                        break

    # Try reading as compound (split at each position)
    for i in range(2, len(tl)-1):
        left = tl[:i]
        right = tl[i:]
        if left in GERMAN and right in GERMAN:
            matches.append(f"  split at {i}: {left.upper()} + {right.upper()}")
        if left in GERMAN and len(right) >= 2:
            for w in GERMAN:
                if w.startswith(right) and len(w) - len(right) <= 2:
                    matches.append(f"  split at {i}: {left.upper()} + {right.upper()}~{w.upper()}")
                    break

    if matches:
        print(f"\n  {target}:")
        seen = set()
        for m in matches[:15]:
            if m not in seen:
                print(f"    {m}")
                seen.add(m)
    else:
        print(f"\n  {target}: no single-sub or compound matches")

# ============================================================
# 3. WIDER CONTEXT PATTERNS
# ============================================================
print(f"\n\n{'='*80}")
print("3. WIDER CONTEXT: WHAT COMES BEFORE/AFTER UNKNOWNS?")
print(f"{'='*80}")

# For the main unknowns, show what German words surround them
context_patterns = {
    'HECHLLT': 'FACH [HECHLLT] ICH',
    'HIHL': 'MIN [HIHL] DIE',
    'SCE': 'ER [SCE] AUS',
    'OEL': 'ICH [OEL] SO',
    'GEVM': 'AN [GEVM] MIN',
    'NDTEII': 'DES [NDTEII] ORT',
    'AEUT': 'EN [AEUT] ER',
    'NSCHA': 'WIR [NSCHA] ER',
    'NRUI': 'SCHAU [NRUI] IN',
    'NDGE': 'SEIN [NDGE] DAS',
    'IEO': 'DAS [IEO] WIR',
    'NDCE': '[HIHL] DIE [NDCE] FACH',
}

for unk, pattern in context_patterns.items():
    print(f"\n  {pattern}")
    # What German word could fit between the surrounding words?
    parts = pattern.split('[')
    before = parts[0].strip().split()[-1] if parts[0].strip() else ''
    after_parts = parts[1].split(']')
    after = after_parts[1].strip().split()[0] if len(after_parts) > 1 and after_parts[1].strip() else ''

    print(f"    Before: '{before}', After: '{after}'")

    # Linguistic analysis
    if unk == 'HECHLLT':
        print("    FACH = compartment/subject. ICH = I.")
        print("    'compartment [hechllt] I' -- HECHLLT could be a verb")
        print("    HECHELT? RECHNET? (but R,N already assigned)")
    elif unk == 'SCE':
        print("    ER [SCE] AUS = 'he [sce] out/from'")
        print("    SCE -> SEE (lake)? But S-C-E codes...")
        print("    Or SETZE (set/place)? Would need T and Z")
    elif unk == 'OEL':
        print("    ICH [OEL] SO = 'I [oel] so'")
        print("    OEL = oel (oil, German umlaut O)")
        print("    But 'I oil so' doesn't parse")
        print("    What if reading is: ICH OELS ODE = 'I oil's wasteland'?")
    elif unk == 'NDGE':
        print("    SEIN [NDGE] DAS = 'his [ndge] the'")
        print("    NDGE = UND GE...? (UND = and)")
        print("    Or: SEINND GE DAS = SEINN D GE DAS?")
    elif unk == 'IEO':
        print("    DAS [IEO] WIR = 'the [ieo] we'")
        print("    IEO doesn't match any German pattern")
    elif unk == 'NSCHA':
        print("    WIR [NSCHA] ER = 'we [nscha] he'")
        print("    NSCHA could be end of a longer word")
        print("    Like: WIR NSCHAU ER? (WIR ANSCHAUEN = we look at?)")
    elif unk == 'NRUI':
        print("    SCHAU [NRUI] IN = 'look/behold [nrui] in'")
        print("    NRUI reversed = IURN")
        print("    RUIN reversed? NRUI ~ RUIN reversed?")
    elif unk == 'AEUT':
        print("    EN [AEUT] ER = '[en] [aeut] he'")
        print("    AEUT could be 'alten' with wrong codes?")
        print("    Or AEUTT = AEUSSERST (outermost)?")
    elif unk == 'NDTEII':
        print("    DES [NDTEII] ORT = 'of the [ndteii] place'")
        print("    NDTEII ORT = a type of place")
        print("    Could be UND + TEII, where TEII ~ TEIL (part)?")

# ============================================================
# 4. THE SCHWITEIO PATTERN (closing formula)
# ============================================================
print(f"\n\n{'='*80}")
print("4. SCHWITEIO DEEP ANALYSIS")
print(f"{'='*80}")

for i, book in enumerate(books):
    dec, pairs = decode(book)
    if 'SCHWITEIO' in dec:
        pos = dec.find('SCHWITEIO')
        ctx = dec[max(0,pos-20):min(len(dec),pos+25)]
        codes = pairs[pos:pos+9]
        print(f"  Bk{i}: ...{ctx}...")
        print(f"    SCHWITEIO codes: {' '.join(codes)}")

# SCHWITEIO reversed = OIETIWHCS
# Could it be SCHWEIGT IO? (SCHWEIGT = is silent)
# SCH + W + I + T + E + I + O
print("\n  SCHWITEIO analysis:")
print("  Letters: S-C-H-W-I-T-E-I-O")
print("  Could be: SCHWEITE + IO?")
print("  Or: SCHWEIT + EIO?")
print("  Or: SCHW + ITEIO?")
print("  SCHWEIGEN = to be silent -> SCHWITEIO ~ SCHWEIGEN?")
print("  If we permute slightly: SCHWEITI O -> SCHWEIGT (is silent)?")

# Check the codes
# SCH = normal German trigram
# What codes make the WITEIO part?
for i, book in enumerate(books):
    dec, pairs = decode(book)
    if 'SCHWITEIO' in dec:
        pos = dec.find('SCHWITEIO')
        schw_codes = pairs[pos:pos+9]
        print(f"\n  Code breakdown: ", end='')
        for j, c in enumerate(schw_codes):
            print(f"{dec[pos+j]}({c}) ", end='')
        print()
        break

# ============================================================
# 5. RE-EXAMINE WORD BOUNDARIES
# ============================================================
print(f"\n\n{'='*80}")
print("5. ALTERNATIVE WORD BOUNDARIES")
print(f"{'='*80}")

# Many unknowns might be solved by different word boundaries
# Key phrase: "FACH HECHLLT ICH OEL SO DE GAREN RUNEORT"
# Alternative readings:
print("\n  Original: FACH [HECHLLT] ICH [OEL] SO DE GAREN RUNEORT")
print("  Alt 1: FACH HECH LLT ICH OEL SO DE GAREN RUNEORT")
print("  Alt 2: FACH HE CH LLT ICH OE LSO DE GAREN RUNEORT")
print("  Alt 3: FACHHE CH LLTI CH OE LSO DEGARENRUNEORT")

# Key phrase: "MIN HIHL DIE NDCE FACH"
print("\n  Original: MIN [HIHL] DIE [NDCE] FACH")
print("  Alt 1: MINH IHL DIEND CE FACH")
print("  Alt 2: MIN HIHLDIE NDCE FACH")
print("  Note: MINH appears in MINHEDDEM too -- MIN is likely a prefix/word")

# Key phrase: "AN GEVM MIN HIHL"
print("\n  Original: AN [GEVM] MIN [HIHL]")
print("  Alt 1: ANGE VM MIN HIHL")
print("  Alt 2: AN GE VMMINH IHL")
print("  Note: ANGE = near? GE = prefix?")

# ============================================================
# 6. WHAT IS THE OVERALL NARRATIVE?
# ============================================================
print(f"\n\n{'='*80}")
print("6. NARRATIVE RECONSTRUCTION (natural reading)")
print(f"{'='*80}")

# Using all our analysis, attempt the most natural reading
# of the continuous text from the longest fragments

# Fragment from Book 5 (most complete single book):
dec5, _ = decode(books[5])
print(f"\n  Book 5 raw: {dec5}")

print("""
  BEST READING (Book 5, mapping v4):

  EN HIER TAUTR IST EILCH AN HEARUCHTIGER
  "Here Tautr is Eilch at Hearuchtiger"

  SO DASS TUN DIESER T EINER SEINE DE
  "so that this one does his the"

  TOTNIURG SEE R LABRRNI
  "Totniurg Lake [r] Labrrni"

  WIR UND IEM IN HED DEM I
  "we and [iem] in [hed] the [i]"

  DIE URALTE STEINEN T ER AD THARSC
  "the ancient stones [t] he [ad] Tharsc"

  IST SCHAU NRUI
  "is behold [nrui]"
""")

# The longer assembled narrative (from fragments 4+5):
print("  FULL NARRATIVE (assembled from all books):")
print("""
  1. KOENIG LABGZERAS AUNRSONGETRASES
     "King Labgzeras [Aunrsongetrases]"
     (Introduction of the king with his epithet)

  2. ENDE UTRUNR DENEN DER REDE
     "End of [utterance] to whom the speech"
     (Reference to the king's proclamation/speech)

  3. EN HIER TAUTR IST EILCH AN HEARUCHTIGER
     "Here Tautr is Eilch at Hearuchtiger"
     (A person/entity named Tautr is described as Eilch at a steep place)

  4. SO DASS TUN DIESER EINER SEINE DE TOTNIURG SEE
     "So that this one does his [deed at] the Totniurg Lake"
     (Action at "Dead-Ruin Lake" - TOTNIURG reversed ~ GRUNTOT)

  5. LABRRNI WIR UND MINHEDDEM DIE URALTE STEINEN
     "Labrrni, we and Minheddem, the ancient stones"
     (Named entities at the ancient stones)

  6. THARSC IST SCHAU
     "Tharsc is [to] behold"
     (A place called Tharsc that is to be seen/beheld)

  7. RUNEORT ER AM NEU DES NDTEII ORT ANN DIE MINHEDDEM
     "Rune-place, he at new of the [ndteii] place at the Minheddem"
     (Description of a rune-place, new, connected to Minheddem)

  8. ICH OEL SO DE GAREN RUNEORT
     "I [oel] so the [garen] rune-place"
     (First-person reference to the rune-place)

  9. DEN DE ES SCHWITEIO
     "the the it Schwiteio"
     (Closing formula/name)

  THEME: A royal proclamation by King Labgzeras about locations,
  entities, and ancient rune-stones. The text describes a journey
  involving Totniurg Lake, the ancient stones, and a rune-place,
  mentioning various named entities (Tautr, Eilch, Labrrni,
  Minheddem, Tharsc, Hearuchtiger, Schwiteio).
""")
