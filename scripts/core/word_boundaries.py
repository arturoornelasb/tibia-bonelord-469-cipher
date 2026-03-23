"""
Deep word boundary analysis. Key discoveries:
1. FINDEN (to find) appears 11 times
2. WIISET = WISSET (MHG "know ye")
3. STEHWILGTNELNRHELUIRUNNHWND needs decomposition
4. RERSCEAUS context analysis
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

# Expanded word list
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
platz rat recht rede reden rein rest ruin ruine ruinen rune runen runeort
see sehr sei seid sein seine seinem seinen seiner seit
sie sind so soll sollen sonne steil stein steine steinen stieg
tag tage tagen teil teile teilen tod tot tun tut
ueber um und uns unter uralte uralten
vier viel viele vielen vom von vor
wahr wahrheit war was wasser weg weil welt wenn wer wie wir wird wissen wisset wisst wo wohl wort
auch blick dunkel feind flucht gift grabe heer kraft neid recht schau schaun schar sieg tief
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
naechst naechste naechsten
wo woher wohin wovon
dazu dahin dahinter daher
neues neuen neuer neuem
alte alten alter altes
erste ersten erster erstes
lauern lauernd lauernde
nicht nichts wind winde winden finden
wisset weiset weisen
eigen eigene eigenen eigener eigenes
steh stehe stehen steht
neben nebst
innen aussen
runde runden
teil teile teilen teils
erbe erben erbt
schweigen schweiget
wacht wachen
offen offene offenen
vergangenheit vergangen
gedenken gedenket
schuld schulden
fluch flucht
stein steine steinen steins
enden endet
davor danach daraus
hinter hinten
seite seiten
spur spuren
gericht gerichte
lehre lehren
zeuge zeugen
schwiteio tharsc totniurg hearuchtiger tautr eilch labgzeras minheddem utrunr
labrrni aunrsongetrases uongetrases hihl
""".split())

def collapse_doubles(text):
    if not text: return text
    result = [text[0]]
    for c in text[1:]:
        if c != result[-1]:
            result.append(c)
    return ''.join(result)

def dp_segment(text, words=WORDS, max_w=25):
    tl = text.lower()
    n = len(tl)
    dp = [0] * (n + 1)
    bt = [None] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        bt[i] = None
        for ln in range(2, min(max_w, i) + 1):
            start = i - ln
            candidate = tl[start:i]
            if candidate in words:
                score = dp[start] + ln
                if score > dp[i]:
                    dp[i] = score
                    bt[i] = (start, i, candidate)
    tokens = []
    i = n
    covered_positions = set()
    while i > 0:
        if bt[i] is not None:
            start, end, word = bt[i]
            tokens.append((start, end, word.upper()))
            covered_positions.update(range(start, end))
            i = start
        else:
            i -= 1
    tokens.reverse()
    result = []
    pos = 0
    for start, end, word in tokens:
        if pos < start:
            result.append(f'[{text[pos:start]}]')
        result.append(word)
        pos = end
    if pos < n:
        result.append(f'[{text[pos:]}]')
    return result, len(covered_positions)

# ============================================================
# 1. FIND ALL GERMAN WORDS IN THE TEXT
# ============================================================
print("=" * 80)
print("1. ALL RECOGNIZED WORDS IN THE COMPLETE TEXT")
print("=" * 80)

word_occurrences = Counter()
for i, book in enumerate(books):
    dec, _ = decode(book)
    dec_c = collapse_doubles(dec)
    tokens, _ = dp_segment(dec_c)
    for t in tokens:
        if not t.startswith('['):
            word_occurrences[t] += 1

print(f"\n  Distinct words found: {len(word_occurrences)}")
print(f"\n  Word frequencies (all recognized):")
for word, count in word_occurrences.most_common():
    print(f"    {word:20s} {count:3d}x")

# ============================================================
# 2. FINDEN IN CONTEXT
# ============================================================
print(f"\n{'='*80}")
print("2. FINDEN (to find) IN ALL CONTEXTS")
print(f"{'='*80}")

for i, book in enumerate(books):
    dec, pairs = decode(book)
    if 'FINDEN' in dec:
        pos = dec.find('FINDEN')
        ctx = dec[max(0,pos-15):min(len(dec),pos+21)]
        print(f"  Bk{i:2d}: ...{ctx}...")
        # Try to read the full sentence
        before = dec[max(0,pos-15):pos]
        after = dec[pos+6:min(len(dec),pos+30)]
        print(f"         Before: '{before}' FINDEN '{after}'")

# ============================================================
# 3. STEHWILGTNELNRHELUIRUNNHWND DECOMPOSITION
# ============================================================
print(f"\n{'='*80}")
print("3. LONG GARBLED SECTION DECOMPOSITION")
print(f"{'='*80}")

long_section = "STEHWILGTNELNRHELUIRUNNHWND"
print(f"\n  Raw: {long_section}")
print(f"  Collapsed: {collapse_doubles(long_section)}")

# Try to find word boundaries
# STEH + WILGT + NELN + RHEL + UIR + UNNHWND
# Or: STEH + W + ILGT + NELN + RHE + LUIR + UNN + HWND
# Or: S + TEHWILGT + NELN + RHE + LUIRUNN + HWND
# S+T+E+H+W+I+L+G+T+N+E+L+N+R+H+E+L+U+I+R+U+N+N+H+W+N+D

# Known words that might be in here:
# STEH (stand) - YES
# STEHE (stand)
# WELT (world) - check: no, WILG not WELT
# HELD (hero) - check: RHEL could end ...HELD?
# NELN - ?
# RUNN - run?
# HWND - hound/dog? (MHG hunt = dog)
# WIND - in HWNDFINDEN = HWIND FINDEN?

print(f"\n  Attempt 1: STEH + WILGT + NELN + RHEL + UIR + UNN + HWND")
print(f"    STEH = stand (verb)")
print(f"    WILGT = ? (WILD + T?)")
print(f"    NELN = ?")
print(f"    RHEL = ?")
print(f"    HWND = HUND (dog/hound) with W insertion?")

print(f"\n  Attempt 2 (collapsed): STEHWILGTNELNRHELUIRUNHWND")
collapsed = collapse_doubles(long_section)
tokens, cov = dp_segment(collapsed)
print(f"    DP segmented: {' '.join(tokens)}")
print(f"    Coverage: {cov}/{len(collapsed)} = {cov/len(collapsed)*100:.1f}%")

# Check with even more words
extra = WORDS | set(['gilt', 'gilt', 'willen', 'wille', 'willig',
    'helm', 'held', 'helden', 'hund', 'hunde', 'hunden',
    'nelke', 'rune', 'runen', 'lehr', 'lehre', 'lehren',
    'heul', 'heulen', 'eule', 'eulen', 'turm', 'wund', 'wunde',
    'lunge', 'lungen', 'irren', 'irrung', 'irrungen',
    'gilt', 'gelte', 'gelten', 'stehend', 'stehende',
    'umher', 'umhergehen', 'herum', 'herumlaufen'])

tokens2, cov2 = dp_segment(collapsed, extra)
print(f"    Extended: {' '.join(tokens2)}")
print(f"    Coverage: {cov2}/{len(collapsed)} = {cov2/len(collapsed)*100:.1f}%")

# ============================================================
# 4. RERSCEAUS ANALYSIS
# ============================================================
print(f"\n{'='*80}")
print("4. RERSCEAUS IN FULL CONTEXT")
print(f"{'='*80}")

for i, book in enumerate(books):
    dec, pairs = decode(book)
    if 'RERSCEAUS' in dec:
        pos = dec.find('RERSCEAUS')
        ctx = dec[max(0,pos-20):min(len(dec),pos+29)]
        print(f"  Bk{i:2d}: ...{ctx}...")

# With collapsed doubles
print(f"\n  Collapsed doubles contexts:")
for i, book in enumerate(books):
    dec, _ = decode(book)
    dec_c = collapse_doubles(dec)
    if 'RERSCEAUS' in dec_c:
        pos = dec_c.find('RERSCEAUS')
        ctx = dec_c[max(0,pos-20):min(len(dec_c),pos+29)]
        print(f"  Bk{i:2d}: ...{ctx}...")

# ============================================================
# 5. FULL NARRATIVE WITH MANUAL WORD BOUNDARIES
# ============================================================
print(f"\n{'='*80}")
print("5. FULL NARRATIVE RECONSTRUCTION (manual parse)")
print(f"{'='*80}")

# Use the longest assembled fragment and manually parse it
# First, build superstring
all_decoded = []
for i, book in enumerate(books):
    dec, pairs = decode(book)
    all_decoded.append((i, dec, pairs))

unique = {}
for i, dec, _ in all_decoded:
    if dec not in unique.values():
        unique[i] = dec

to_remove = set()
keys = list(unique.keys())
for i in range(len(keys)):
    for j in range(len(keys)):
        if i != j and unique[keys[i]] in unique[keys[j]]:
            to_remove.add(keys[i])
for k in to_remove:
    del unique[k]

fragments = sorted(unique.values(), key=len, reverse=True)

# Show top 5 fragments with DP segmentation
print(f"\n  {len(fragments)} unique fragments. Top 5:")
for k, frag in enumerate(fragments[:5]):
    frag_c = collapse_doubles(frag)
    tokens, cov = dp_segment(frag_c)
    pct = cov / len(frag_c) * 100
    print(f"\n  Fragment {k+1} ({len(frag)} chars, {pct:.0f}% covered):")
    # Print tokens with manual interpretation
    line = '  '
    for t in tokens:
        if len(line) + len(t) + 1 > 100:
            print(line)
            line = '  '
        line += t + ' '
    if line.strip():
        print(line)

# ============================================================
# 6. SEARCH FOR SPECIFIC GERMAN PHRASES
# ============================================================
print(f"\n{'='*80}")
print("6. SEARCHING FOR COMMON GERMAN PHRASES")
print(f"{'='*80}")

# Build one big collapsed text
all_text = ''
for i, book in enumerate(books):
    dec, _ = decode(book)
    all_text += dec + '|'

all_collapsed = collapse_doubles(all_text)

phrases = [
    'DERKOENIG', 'KOENIGLABGZERAS', 'TOTNIURGSEE', 'DIEURALTESTEINEN',
    'ISTSCHAUN', 'THARSCIST', 'HEARUCHTIGER', 'DASSWIR',
    'SODASSTUN', 'FINDEN', 'WISSET', 'RUNEORT', 'EINERSEINE',
    'ENDEUTRUNR', 'DEREDEKOENIG', 'DIEMINHEDDEM',
    'AUNRSONGETRASES', 'SCHWITEIO', 'TAUTRISTEILCH',
    'ICHOEL', 'FACHCHLLT', 'ENDEDEREDEKOENIG',
    'WINDENFINDEN', 'HWINDFINDEN', 'EIGENDASESDER',
    'DERWIRDWISSEN', 'DENENDERED', 'DEREDEKOENIGLABGZERAS',
]

for phrase in phrases:
    count = all_collapsed.count(phrase)
    if count > 0:
        pos = all_collapsed.find(phrase)
        ctx = all_collapsed[max(0,pos-5):min(len(all_collapsed),pos+len(phrase)+5)]
        print(f"  {phrase}: {count}x  ...{ctx}...")

# ============================================================
# 7. MOST IMPORTANT: SUPERSTRING RECONSTRUCTION
# ============================================================
print(f"\n{'='*80}")
print("7. BEST POSSIBLE NARRATIVE READING")
print(f"{'='*80}")

# Take the longest fragment, collapse doubles, and manually annotate
longest = fragments[0]
longest_c = collapse_doubles(longest)
tokens, cov = dp_segment(longest_c)

print(f"\n  Longest fragment: {len(longest)} chars -> {len(longest_c)} collapsed")
print(f"  Coverage: {cov}/{len(longest_c)} = {cov/len(longest_c)*100:.1f}%")
print(f"\n  Segmented tokens:")
line = '  '
for t in tokens:
    if len(line) + len(t) + 1 > 100:
        print(line)
        line = '  '
    line += t + ' '
if line.strip():
    print(line)

# Now try the second longest
if len(fragments) > 1:
    second = fragments[1]
    second_c = collapse_doubles(second)
    tokens2, cov2 = dp_segment(second_c)
    print(f"\n  Second fragment: {len(second)} chars -> {len(second_c)} collapsed")
    print(f"  Coverage: {cov2}/{len(second_c)} = {cov2/len(second_c)*100:.1f}%")
    print(f"\n  Segmented tokens:")
    line = '  '
    for t in tokens2:
        if len(line) + len(t) + 1 > 100:
            print(line)
            line = '  '
        line += t + ' '
    if line.strip():
        print(line)

# ============================================================
# 8. ATTEMPT: READING THE NARRATIVE AS GERMAN SENTENCES
# ============================================================
print(f"\n{'='*80}")
print("8. SENTENCE-BY-SENTENCE READING")
print(f"{'='*80}")

# Based on all analysis, the best reading of the complete narrative:
print("""
RECONSTRUCTED NARRATIVE (v2, with collapsed doubles + MHG):

=== PROLOGUE ===
"ENDE UTRUNR DENEN DER REDE KOENIG LABGZERAS AUNRSONGETRASES"
= "End of [Utrunr/utterance] of those of the speech of King Labgzeras [Aunrsongetrases]"
> "The conclusion of the proclamation of King Labgzeras the [Aunrsongetrases]"

=== THE LOCATION ===
"EN HIER TAUTR IST EILCH AN HEARUCHTIGER SO DASS TUN DIESER..."
= "[En] here Tautr is Eilch at Hearuchtiger, so that this one does..."
> "Here Tautr is Eilch at Hearuchtiger, so that this one acts..."

"...T EINER SEINE DE TOTNIURG SEE"
= "...his [at] the Totniurg Lake"
> "...his [actions at] Totniurg Lake" (TOTNIURG reversed = GRUNTOT = Dead Ruin)

=== THE COMPANIONS ===
"R LABRRNI WIR UND IE MINHEDDEM I DIE URALTE STEINEN"
= "[R] Labrrni, we and [ie] Minheddem [i] the ancient stones"
> "Labrrni, we and Minheddem [at] the ancient stones"

=== THE VISION ===
"T ER AD THARSC IST SCHAUN RUIN WISSET"
= "[T] er [ad] Tharsc ist schaun Ruin, wisset!"
> "[Then] he [at] Tharsc: behold the Ruin, know ye!"
(WISSET = MHG imperative "ye shall know / know ye!")

=== THE RUNE PLACE ===
"ICH OEL SO DE GAREN RUNEORT NDT ER AM NEU DES NDTEII ORT ANN DIE MINHEDDEM"
= "Ich [oel] so de garen Runeort, [ndt] er am neu des [ndteii] Ort, ann die Minheddem"
> "I [oel] so the [garen] rune-place, he at the new [ndteii] place, at the Minheddem"

=== DISCOVERY ===
"HWIND FINDEN TEIGN DAS ES DER..."
= "H-Wind finden [t]eigen, das es der..."
> "[Through] wind find [their] own, that it the..."
(FINDEN = to find, EIGEN = own/self)

=== THE CLOSING ===
"DEN DE ES SCHWITEIO"
= "Den de es Schwiteio"
> "The [of] it Schwiteio"

"DAS WIR NSCHA ER ALTE"
= "Das wir [nscha] er alte"
> "That we [...] the old [one]"

=== RECURRING ELEMENTS ===
- FACH HECHLLT ICH OEL: "[skill/profession] [hechelt/pants] I [oil/anoint]"
  (HECHLLT collapsed = HECHLT, possibly from HECHELN = to pant/gasp)
- HIHL DIE NDCE FACH: "HIHL the [ndce] profession/skill"
  (HIHL likely a proper noun; NDCE = boundary artifact)
- SCE AUS ENDE: "...out/from [the] end"
  (SCE possibly = GESCHEHEN = happen, truncated)
""")

# ============================================================
# 9. COVERAGE STATISTICS
# ============================================================
print(f"{'='*80}")
print("9. FINAL COVERAGE STATISTICS")
print(f"{'='*80}")

total_chars = 0
total_covered = 0
proper_noun_chars = 0
proper_nouns = {'SCHWITEIO', 'THARSC', 'TOTNIURG', 'HEARUCHTIGER', 'TAUTR',
                'EILCH', 'LABGZERAS', 'MINHEDDEM', 'UTRUNR', 'LABRRNI',
                'AUNRSONGETRASES', 'HIHL', 'UONGETRASES'}

for book in books:
    dec, _ = decode(book)
    dec_c = collapse_doubles(dec)
    tokens, cov = dp_segment(dec_c)
    total_covered += cov
    total_chars += len(dec_c)
    for t in tokens:
        if not t.startswith('[') and t in proper_nouns:
            proper_noun_chars += len(t)

german_chars = total_covered - proper_noun_chars
unknown_chars = total_chars - total_covered

print(f"\n  Total decoded chars:  {total_chars}")
print(f"  German words:         {german_chars} ({german_chars/total_chars*100:.1f}%)")
print(f"  Proper nouns:         {proper_noun_chars} ({proper_noun_chars/total_chars*100:.1f}%)")
print(f"  Unknown:              {unknown_chars} ({unknown_chars/total_chars*100:.1f}%)")
print(f"  Total identified:     {total_covered} ({total_covered/total_chars*100:.1f}%)")
print(f"\n  Improvement from Session 8: was ~60%, now {total_covered/total_chars*100:.1f}%")
