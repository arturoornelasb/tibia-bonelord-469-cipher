"""
Final narrative assembly: use mapping v4 (71=N) to produce the best possible
reading of the Bonelord Language text. Focus on the STORY, not individual codes.
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
# 1. SUPERSTRING ASSEMBLY
# ============================================================
print("=" * 80)
print("1. ASSEMBLING THE COMPLETE TEXT")
print("=" * 80)

# Decode all books, find unique texts, build superstring by overlap
decoded_texts = []
for i, book in enumerate(books):
    dec, _ = decode(book)
    decoded_texts.append((i, dec))

# Remove duplicates
unique = {}
for i, dec in decoded_texts:
    if dec not in unique.values():
        unique[i] = dec

# Remove substrings
to_remove = set()
keys = list(unique.keys())
for i in range(len(keys)):
    for j in range(len(keys)):
        if i != j and unique[keys[i]] in unique[keys[j]]:
            to_remove.add(keys[i])

for k in to_remove:
    del unique[k]

print(f"  {len(decoded_texts)} books -> {len(unique)} unique non-substring fragments")

# Sort by length descending
fragments = sorted(unique.values(), key=len, reverse=True)

# Greedy overlap assembly
def overlap(a, b):
    """Find longest suffix of a that is prefix of b."""
    max_ov = min(len(a), len(b))
    for k in range(max_ov, 0, -1):
        if a[-k:] == b[:k]:
            return k
    return 0

# Build superstring greedily
assembled = list(fragments)
while len(assembled) > 1:
    best_ov = 0
    best_i = best_j = -1
    best_merged = ''
    for i in range(len(assembled)):
        for j in range(len(assembled)):
            if i == j:
                continue
            ov = overlap(assembled[i], assembled[j])
            if ov > best_ov:
                best_ov = ov
                best_i, best_j = i, j
                best_merged = assembled[i] + assembled[j][ov:]
    if best_ov < 3:
        break
    # Merge
    new_assembled = [best_merged]
    for k in range(len(assembled)):
        if k != best_i and k != best_j:
            new_assembled.append(assembled[k])
    assembled = new_assembled

print(f"  After assembly: {len(assembled)} fragment(s)")
for k, frag in enumerate(assembled):
    print(f"  Fragment {k+1}: {len(frag)} chars")

# ============================================================
# 2. THE FULL TEXT
# ============================================================
print(f"\n{'='*80}")
print("2. FULL DECODED TEXT (longest fragment)")
print(f"{'='*80}")

main_text = assembled[0] if assembled else ''
print(f"\n  Length: {len(main_text)} chars")
print(f"\n  Raw text:")
# Print in lines of 80 chars
for i in range(0, len(main_text), 80):
    print(f"  {main_text[i:i+80]}")

# ============================================================
# 3. WORD SEGMENTATION
# ============================================================
print(f"\n{'='*80}")
print("3. WORD SEGMENTATION (greedy, longest match)")
print(f"{'='*80}")

WORDS = set("""
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
auch blick dunkel feind flucht gift grabe heer kraft neid recht schau schar sieg tief
weit wild zorn bild blut burg dorf eben feld fort gang grab haus herz hoch
kalt kern klug last leer letzt link mass naht nein nord rand raum ring
rund sache scharf schlecht schnell schwer still stolz streng stuck stumm suche
traum treue trost turm volk wache wand zehn ziel zug
garen gar ren ann gen ser tier net ode oede
dieser diese dieses seinen seiner seines
toten toter totes tote tod rune stein steine steinen
erde erden koenig koenige
gesehen sehen schauen
derer deren dessen jenen jene jener jenem
eines einer einem einen
herr herrn herren
oben unten rechts links
wo woher wohin wovon
dazu dahin dahinter daher
neues neuen neuer neuem
alte alten alter altes
erste ersten erster erstes
nicht nichts wind winde winden
schwiteio tharsc totniurg hearuchtiger tautr eilch labgzeras minheddem utrunr
labrrni aunrsongetrases uongetrases
""".split())

def segment(text, words=WORDS, max_w=20):
    tl = text.lower()
    n = len(tl)
    result = []
    i = 0
    while i < n:
        best = None
        for ln in range(min(max_w, n-i), 1, -1):
            if tl[i:i+ln] in words and ln >= 2:
                best = tl[i:i+ln]
                break
        if best:
            result.append(best.upper())
            i += len(best)
        else:
            unk = ''
            while i < n:
                found = False
                for ln in range(min(max_w, n-i), 1, -1):
                    if tl[i:i+ln] in words and ln >= 2:
                        found = True
                        break
                if found:
                    break
                unk += text[i]
                i += 1
            result.append(f'[{unk}]')
    return result

tokens = segment(main_text)
covered = sum(len(t) for t in tokens if not t.startswith('['))
pct = covered / len(main_text) * 100

print(f"\n  Coverage: {covered}/{len(main_text)} = {pct:.1f}%")
print(f"\n  Segmented text:")
line = '  '
for t in tokens:
    if len(line) + len(t) + 1 > 100:
        print(line)
        line = '  '
    line += t + ' '
if line.strip():
    print(line)

# ============================================================
# 4. IDENTIFY PROPER NOUNS AND INTERPRET
# ============================================================
print(f"\n{'='*80}")
print("4. PROPER NOUNS AND INTERPRETATION")
print(f"{'='*80}")

proper_nouns = {
    'LABGZERAS': 'King name (KOENIG LABGZERAS)',
    'TOTNIURG': 'Place name - reversed GRUNTOT? (dead ground/ruin)',
    'HEARUCHTIGER': 'Place/feature name (at HEARUCHTIGER)',
    'TAUTR': 'Name/title (TAUTR IST EILCH = "[Tautr] is [Eilch]")',
    'EILCH': 'Name/title (complement of TAUTR)',
    'MINHEDDEM': 'Name/concept (before "DIE URALTE STEINEN")',
    'THARSC': 'Place name (IST SCHAU THARSC = "is look/behold Tharsc")',
    'SCHWITEIO': 'Name/concept (in closing phrase)',
    'UTRUNR': 'Verb/concept (ENDE UTRUNR DENEN DER REDE)',
    'LABRRNI': 'Name (after TOTNIURG SEE, before WIR UND)',
    'AUNRSONGETRASES': 'Title/epithet of LABGZERAS',
    'RUNEORT': 'Compound: RUNE + ORT = "rune place"',
}

for noun, meaning in proper_nouns.items():
    count = main_text.count(noun)
    if count > 0:
        pos = main_text.find(noun)
        ctx = main_text[max(0,pos-15):pos+len(noun)+15]
        print(f"\n  {noun} ({count}x): {meaning}")
        print(f"    Context: ...{ctx}...")

# ============================================================
# 5. REVERSAL ANALYSIS
# ============================================================
print(f"\n{'='*80}")
print("5. REVERSAL ANALYSIS (bonelord mirror motif)")
print(f"{'='*80}")

for noun in proper_nouns:
    rev = noun[::-1]
    # Check if reversed form matches anything meaningful
    rev_lower = rev.lower()
    # Check against German words
    matches = []
    for word in WORDS:
        if len(word) >= 4 and (rev_lower.startswith(word) or word.startswith(rev_lower)):
            matches.append(word)
    if matches:
        print(f"  {noun} reversed = {rev}")
        print(f"    Partial matches: {', '.join(matches[:5])}")
    else:
        print(f"  {noun} reversed = {rev} (no German word match)")

# Special analysis
print("\n  Notable reversals:")
print("  TOTNIURG -> GRUNTOT = GRUND + TOT? (ground/base + dead)")
print("  TAUTR -> RTUAT (nothing)")
print("  EILCH -> HCLIE (nothing)")
print("  THARSC -> CSRAHT (nothing)")
print("  LABGZERAS -> SAREZGBAL (nothing)")
print("  SCHWITEIO -> OIETIWCHS (nothing)")
print("  LABRRNI -> INRRBAL (nothing)")
print("  UTRUNR -> RNURTU (nothing)")
print("  MINHEDDEM -> MEDDEHNIM (nothing)")

# ============================================================
# 6. SENTENCE-BY-SENTENCE TRANSLATION ATTEMPT
# ============================================================
print(f"\n{'='*80}")
print("6. SENTENCE-BY-SENTENCE TRANSLATION")
print(f"{'='*80}")

# Based on the segmented text and proper noun identification,
# attempt to read the narrative as German sentences

print("""
RECONSTRUCTED NARRATIVE (German with translations):

=== SECTION 1: Introduction ===
"ENDE UTRUNR DENEN DER REDE KOENIG LABGZERAS"
= "End [utrunr] to-whom the speech King Labgzeras"
> "The end of [utrunr/utterance] of those of the speech of King Labgzeras"

"AUNRSONGETRASES" / "UONGETRASES"
= Title/epithet of King Labgzeras (unknown meaning)

=== SECTION 2: The Location ===
"EN HIER TAUTR IST EILCH AN HEARUCHTIGER"
= "[en] here [Tautr] is [Eilch] at [Hearuchtiger]"
> "Here [Tautr] is [Eilch] at [Hearuchtiger]"
(Describes a person/thing named Tautr being Eilch at a place called Hearuchtiger)

"SO DASS TUN DIESER [T] EINER SEINE DE TOTNIURG SEE"
= "so that do this [t] one his the [Totniurg] lake/sea"
> "so that this one does his [thing at] the Totniurg Lake"
(TOTNIURG reversed = GRUNTOT = "dead ground" or "ruin ground")

=== SECTION 3: The Journey ===
"LABRRNI WIR UND [IE] MINHEDDEM [ID] DIE URALTE STEINEN"
= "[Labrrni] we and [ie] [Minheddem] [id] the ancient stones"
> "[Labrrni], we and [Minheddem] [at] the ancient stones"

"TER AD THARSC IST SCHAU NRUI"
= "[ter ad] Tharsc is look/behold [nrui]"
> "Tharsc is [to] behold [nrui]"

=== SECTION 4: The Rune Place ===
"ICH OEL SO DE GAREN RUNEORT"
= "I [oel] so the garden/enclosure rune-place"
> "I [oel] so the [garen] rune-place"
(RUNEORT = rune + place, OEL could be OeL = oil, or encoding error)

"NDT ER AM NEU DES NDTEII ORT ANN DIE MINHEDDEM"
= "[ndt] he at new of-the [ndteii] place at the [Minheddem]"
> "[ndt] he at the new [ndteii] place at [Minheddem]"

=== SECTION 5: The Ending ===
"DEN DE ES SCHWITEIO"
= "the the it [Schwiteio]"
> "the [Schwiteio]" (name or closing formula)

"DAS WIR NSCHA ER ALTE"
= "that we [nscha] he old"
> "that we [nscha] the old [one]"

REMAINING UNRESOLVED:
- TAUTR, EILCH: Proper nouns (person/place names)
- HEARUCHTIGER: Place name (at ~steil = steep?)
- MINHEDDEM: Entity name (associated with ancient stones)
- THARSC: Place name (to be beheld/seen)
- SCHWITEIO: Closing word/name
- UTRUNR: Could be related to "Aeusserung" (utterance)
- OEL: Possibly OeL (oil) or encoding error
- LABRRNI: Name (after Totniurg See)
- AUNRSONGETRASES: Royal epithet
""")

# ============================================================
# 7. STATISTICS
# ============================================================
print(f"\n{'='*80}")
print("7. FINAL STATISTICS")
print(f"{'='*80}")

# Count recognized vs unknown characters
total_chars = 0
recognized_chars = 0
proper_noun_chars = 0
unknown_chars = 0

for t in tokens:
    if t.startswith('['):
        unk = t[1:-1]
        unknown_chars += len(unk)
        total_chars += len(unk)
    elif t.upper() in [n.upper() for n in proper_nouns]:
        proper_noun_chars += len(t)
        total_chars += len(t)
    else:
        recognized_chars += len(t)
        total_chars += len(t)

print(f"\n  Total characters: {total_chars}")
print(f"  German words:     {recognized_chars} ({recognized_chars/total_chars*100:.1f}%)")
print(f"  Proper nouns:     {proper_noun_chars} ({proper_noun_chars/total_chars*100:.1f}%)")
print(f"  Unknown:          {unknown_chars} ({unknown_chars/total_chars*100:.1f}%)")
print(f"  Total identified: {recognized_chars+proper_noun_chars} ({(recognized_chars+proper_noun_chars)/total_chars*100:.1f}%)")

print(f"\n  Mapping: 99 codes -> 21 letters + 1 (W)")
print(f"  Missing letters: P, J, Q, X, Y (expected low freq in German)")
print(f"  Code 71: N (changed from I in v3)")

# ============================================================
# 8. OTHER FRAGMENTS (if multiple superstring pieces)
# ============================================================
if len(assembled) > 1:
    print(f"\n{'='*80}")
    print("8. DISCONNECTED FRAGMENTS")
    print(f"{'='*80}")
    for k, frag in enumerate(assembled[1:], 2):
        toks = segment(frag)
        print(f"\n  Fragment {k} ({len(frag)} chars):")
        print(f"    {' '.join(toks)}")
