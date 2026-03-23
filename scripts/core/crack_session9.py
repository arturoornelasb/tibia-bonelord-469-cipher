"""
Session 9: Deep attack on remaining ~25% unknown text.
1. Analyze WIISET, HECHLLT, and other recurring unknowns
2. Test Middle High German / archaic vocabulary
3. Test code reassignments for missing letter P
4. Dynamic programming segmentation for optimal coverage
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
# 1. FULL TEXT ASSEMBLY - decode all books, build complete text
# ============================================================
print("=" * 80)
print("1. FULL DECODED CORPUS")
print("=" * 80)

all_decoded = []
for i, book in enumerate(books):
    dec, pairs = decode(book)
    all_decoded.append((i, dec, pairs))

# Build a combined text for analysis
combined = ''
for i, dec, _ in all_decoded:
    combined += dec

print(f"  Total decoded characters: {len(combined)}")

# ============================================================
# 2. WIISET ANALYSIS - What is this word?
# ============================================================
print(f"\n{'='*80}")
print("2. WIISET DEEP ANALYSIS")
print(f"{'='*80}")

# Find every occurrence of WIISET and its wider context
for i, dec, pairs in all_decoded:
    if 'WIISET' in dec:
        pos = dec.find('WIISET')
        # Get 20 chars each side
        ctx = dec[max(0,pos-20):pos+26]
        codes = pairs[max(0,pos-20):min(len(pairs),pos+26)]
        print(f"  Bk{i:2d}: ...{ctx}...")
        # Show the WIISET codes specifically
        wiiset_codes = pairs[pos:pos+6]
        print(f"         WIISET codes: {' '.join(wiiset_codes)}")

# Try decompositions of WIISET
print(f"\n  WIISET decomposition attempts:")
print(f"    W + IISET -> ?")
print(f"    WI + ISET -> ?")
print(f"    WII + SET -> WII (Roman numeral 7?) + SET")
print(f"    WIIS + ET -> WIIS (archaic WISSEN?) + ET")
print(f"    WIISE + T -> WIISE (archaic WEISE=manner?) + T")
print(f"    WIISET as WISSET -> Middle High German 'wisset' = 'ye know / know ye!'")
print(f"    Note: double I might be encoding artifact of II -> single I")

# Check: if we read WIISET as WISSET (collapsing double letters)
# Does the pattern SCHAUN RUIIN WISSET make sense?
# "Behold the ruin, know ye!"
print(f"\n  If WIISET = WISSET (MHG 'know ye / ye shall know'):")
print(f"    THARSC IST SCHAUN RUIIN WISSET = 'Tharsc is to behold, the ruin, know ye!'")
print(f"    This works as archaic German imperative!")

# ============================================================
# 3. HECHLLT ANALYSIS
# ============================================================
print(f"\n{'='*80}")
print("3. HECHLLT DEEP ANALYSIS")
print(f"{'='*80}")

for i, dec, pairs in all_decoded:
    if 'HECHLLT' in dec:
        pos = dec.find('HECHLLT')
        ctx = dec[max(0,pos-20):pos+27]
        codes = pairs[max(0,pos-20):min(len(pairs),pos+27)]
        print(f"  Bk{i:2d}: ...{ctx}...")
        hech_codes = pairs[pos:pos+7]
        print(f"         HECHLLT codes: {' '.join(hech_codes)}")

print(f"\n  HECHLLT decomposition attempts:")
print(f"    HECH + LLT -> HECHT (pike fish) with extra L? Unlikely.")
print(f"    HE + CHLLT -> ?")
print(f"    If double-L collapses: HECHLT -> HECHELT (MHG: to gasp/pant)?")
print(f"    HECHL + LT -> ?")
print(f"    Could LL be a doubled letter from homophonic encoding?")

# Check what comes before/after HECHLLT
print(f"\n  Context analysis:")
for i, dec, pairs in all_decoded:
    if 'HECHLLT' in dec:
        pos = dec.find('HECHLLT')
        before = dec[max(0,pos-15):pos]
        after = dec[pos+7:min(len(dec),pos+22)]
        print(f"    Before: '{before}' | HECHLLT | After: '{after}'")

# ============================================================
# 4. DOUBLE LETTER HYPOTHESIS
# ============================================================
print(f"\n{'='*80}")
print("4. DOUBLE LETTER HYPOTHESIS")
print(f"{'='*80}")

# Many unknowns have double letters: WIISET (II), HECHLLT (LL), RUIIN (II)
# What if the cipher sometimes produces doubled letters that should be read as single?
# Test: collapse all double letters and re-segment

def collapse_doubles(text):
    """Remove consecutive duplicate characters."""
    if not text:
        return text
    result = [text[0]]
    for c in text[1:]:
        if c != result[-1]:
            result.append(c)
    return ''.join(result)

# Test on key patterns
test_patterns = [
    ('WIISET', 'WISET'),
    ('HECHLLT', 'HECHLT'),
    ('RUIIN', 'RUIN'),
    ('SCHWITEIO', 'SCHWITEIO'),
    ('AUNRSONGETRASES', 'AUNRSONGETRASES'),
    ('STEHWILGTNELNRHELUIRUNNHWND', 'STEHWILGTNELNRHELUIRUNHWND'),
]

print(f"  Pattern           Collapsed         Match?")
for orig, collapsed in test_patterns:
    actual_collapsed = collapse_doubles(orig)
    print(f"  {orig:25s} {actual_collapsed:20s}")

# Full text with collapsed doubles
collapsed_full = collapse_doubles(combined)
print(f"\n  Original combined: {len(combined)} chars")
print(f"  Collapsed doubles: {len(collapsed_full)} chars")
print(f"  Difference: {len(combined) - len(collapsed_full)} chars removed")

# ============================================================
# 5. ARCHAIC GERMAN / MHG WORD LIST
# ============================================================
print(f"\n{'='*80}")
print("5. MIDDLE HIGH GERMAN VOCABULARY TEST")
print(f"{'='*80}")

# Extended word list with MHG and archaic German
MHG_WORDS = set("""
wisset wisst wizzet wisse
hecheln hechelt gehechelt
schauen schau schaun geschaut
ruine ruinen
weisen weiset weist gewiesen
meister meistern
geselle gesellen
ritter rittern
edel edle edlen edlem
frouwe vrouwe
minne minnen
swert schwert
burc burg burgen
lant land lande landen
stat statt statte
kunec kunic koenig
herre herren
dienst dienste
ere ehre ehren
hulde huld
maget magd
tugend tugenden
triuwe treue treuen
reht recht rechte
schuld schulden
sele seele seelen
erde erden
himel himmel himmeln
gote gott gottes
welt welten
volc volk voelker
strit streit streiten
kraft kraefte
gewalt gewalten
friede frieden
zorn zornes
angst aengste
freude freuden
sorge sorgen
schmerz schmerzen
liebe lieben
hass hassen
tod todes
leben lebens
wort worte worten
rede reden
stimme stimmen
name namen
bote boten
brief briefe
zeichen zeichens
wunder wundern
geist geister geistern
macht maechte
orden ordens
gebiet gebiete
mark marken
grenze grenzen
turm tuerme
tor tore toren
mauer mauern
stein steine steinen
fels felsen
berg berge bergen
tal taeler
wald waelder waeldern
see seen
bach baeche
fluss fluesse
quelle quellen
feuer feuers
wasser wassers
erde erden
luft luefte
nacht naechte
tag tage tagen
sonne sonnen
mond mondes
stern sterne sternen
dunkel dunkle dunklen
licht lichter lichtern
schatten
geheim geheime geheimen geheimer geheimes
oede oeden
wuest wueste wuesten
alt alte alten alter altes
neu neue neuen neuer neues
gross grosse grossen grosser grosses
klein kleine kleinen kleiner kleines
hoch hohe hohen hoher hohes
tief tiefe tiefen tiefer tiefes
weit weite weiten weiter weites
nah nahe nahen naher nahes
lang lange langen langer langes
kurz kurze kurzen kurzer kurzes
stark starke starken starker starkes
schwach schwache schwachen
schnell schnelle schnellen
langsam langsame langsamen
still stille stillen
laut laute lauten
ruhig ruhige ruhigen
wild wilde wilden wilder
zahm zahme zahmen
heilig heilige heiligen
boese boesen boeser boeses
gut gute guten guter gutes
schlecht schlechte schlechten
wahr wahre wahren wahrer
falsch falsche falschen
recht rechte rechten
frei freie freien
sicher sichere sicheren
gewiss gewisse gewissen
ewig ewige ewigen ewiger
vergessen vergessene vergessenen
verborgen verborgene verborgenen
verloren verlorene verlorenen
zerbrochen zerbrochene zerbrochenen
versunken versunkene versunkenen
verfallen verfallene verfallenen
gebrochen gebrochene gebrochenen
verschlossen verschlossene verschlossenen
einst einstmals
damals
vormals
dereinst
seither
nunmehr
hinfort
hernach
dieweil
allda
daselbst
alhier
dorten
dortselbst
hierher
dorther
daher
dahin
wohin
woher
woselbst
allwo
wisset gedenket
hoeret vernehmet
sehet schauet
merket achtet
fuerchtet
gebet
nehmet
bringet
saget
leget
traget
sendet
rufet
dienet
huetet
wahret
wehret
streuet
wachet
""".split())

# Our standard word list
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
naechst naechste naechsten
wo woher wohin wovon
dazu dahin dahinter daher
neues neuen neuer neuem
alte alten alter altes
erste ersten erster erstes
lauern lauernd lauernde
nicht nichts wind winde winden
wisset weiset
schwiteio tharsc totniurg hearuchtiger tautr eilch labgzeras minheddem utrunr
labrrni aunrsongetrases uongetrases
""".split())

# Combine both word sets
ALL_WORDS = GERMAN | MHG_WORDS

print(f"  Standard dict: {len(GERMAN)} words")
print(f"  MHG additions: {len(MHG_WORDS)} words")
print(f"  Combined:      {len(ALL_WORDS)} words")

# ============================================================
# 6. DYNAMIC PROGRAMMING SEGMENTATION
# ============================================================
print(f"\n{'='*80}")
print("6. DYNAMIC PROGRAMMING OPTIMAL SEGMENTATION")
print(f"{'='*80}")

def dp_segment(text, words, max_w=25):
    """Optimal segmentation maximizing covered characters."""
    tl = text.lower()
    n = len(tl)
    # dp[i] = max chars covered for text[0:i]
    dp = [0] * (n + 1)
    # backtrack[i] = (start, end, word) of best word ending at i
    bt = [None] * (n + 1)

    for i in range(1, n + 1):
        # Option 1: skip this char (unknown)
        dp[i] = dp[i-1]
        bt[i] = None

        # Option 2: end a word at position i
        for ln in range(2, min(max_w, i) + 1):
            start = i - ln
            candidate = tl[start:i]
            if candidate in words:
                score = dp[start] + ln
                if score > dp[i]:
                    dp[i] = score
                    bt[i] = (start, i, candidate)

    # Reconstruct
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

    # Fill in unknown gaps
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

# Test on key books with both word lists
key_books = [5, 2, 9, 27, 11, 32, 48, 53, 0]
for bi in key_books:
    if bi >= len(books):
        continue
    dec, _ = decode(books[bi])

    # Greedy with standard dict
    tokens_std, cov_std = dp_segment(dec, GERMAN)
    pct_std = cov_std / len(dec) * 100

    # DP with expanded dict
    tokens_exp, cov_exp = dp_segment(dec, ALL_WORDS)
    pct_exp = cov_exp / len(dec) * 100

    # DP with collapsed doubles + expanded dict
    dec_collapsed = collapse_doubles(dec)
    tokens_col, cov_col = dp_segment(dec_collapsed, ALL_WORDS)
    pct_col = cov_col / len(dec_collapsed) * 100 if dec_collapsed else 0

    print(f"\n  Book {bi} ({len(dec)} chars):")
    print(f"    Standard dict:       {cov_std}/{len(dec)} = {pct_std:.1f}%")
    print(f"    + MHG dict:          {cov_exp}/{len(dec)} = {pct_exp:.1f}%")
    print(f"    + collapsed doubles: {cov_col}/{len(dec_collapsed)} = {pct_col:.1f}%")
    if pct_exp > pct_std:
        print(f"    ** +{pct_exp - pct_std:.1f}% from MHG words")
    print(f"    DP segmented: {' '.join(tokens_exp)}")

# ============================================================
# 7. COLLAPSED DOUBLES FULL ANALYSIS
# ============================================================
print(f"\n{'='*80}")
print("7. COLLAPSED DOUBLES: BEST READING")
print(f"{'='*80}")

# For each book, collapse doubles and segment
total_covered = 0
total_chars = 0
for bi in range(len(books)):
    dec, _ = decode(books[bi])
    dec_c = collapse_doubles(dec)
    tokens, cov = dp_segment(dec_c, ALL_WORDS)
    total_covered += cov
    total_chars += len(dec_c)

print(f"  Overall coverage (collapsed + MHG): {total_covered}/{total_chars} = {total_covered/total_chars*100:.1f}%")

# Show best readings for top books
print(f"\n  Best readings (collapsed doubles + MHG dict):")
for bi in [5, 2, 9, 27, 0]:
    if bi >= len(books):
        continue
    dec, _ = decode(books[bi])
    dec_c = collapse_doubles(dec)
    tokens, cov = dp_segment(dec_c, ALL_WORDS)
    pct = cov / len(dec_c) * 100 if dec_c else 0
    print(f"\n  Book {bi} ({pct:.0f}%):")
    print(f"    {' '.join(tokens)}")

# ============================================================
# 8. WHAT GERMAN WORDS APPEAR IN COLLAPSED TEXT?
# ============================================================
print(f"\n{'='*80}")
print("8. NEW WORDS FOUND WITH COLLAPSED DOUBLES")
print(f"{'='*80}")

# Compare: what words are found in collapsed text that weren't in original?
new_words_found = Counter()
for bi in range(len(books)):
    dec, _ = decode(books[bi])
    dec_c = collapse_doubles(dec)

    # Words in collapsed
    tokens_c, _ = dp_segment(dec_c, ALL_WORDS)
    words_c = set(t for t in tokens_c if not t.startswith('['))

    # Words in original
    tokens_o, _ = dp_segment(dec, ALL_WORDS)
    words_o = set(t for t in tokens_o if not t.startswith('['))

    # New words from collapsing
    for w in words_c - words_o:
        new_words_found[w] += 1

print(f"\n  New words found by collapsing doubles:")
for w, c in new_words_found.most_common(30):
    print(f"    {w:20s} {c:3d}x")

# ============================================================
# 9. REMAINING UNKNOWNS AFTER ALL IMPROVEMENTS
# ============================================================
print(f"\n{'='*80}")
print("9. REMAINING UNKNOWNS (collapsed + MHG)")
print(f"{'='*80}")

remaining = Counter()
for bi in range(len(books)):
    dec, _ = decode(books[bi])
    dec_c = collapse_doubles(dec)
    tokens, _ = dp_segment(dec_c, ALL_WORDS)
    for t in tokens:
        if t.startswith('[') and t.endswith(']'):
            unk = t[1:-1]
            if len(unk) >= 2:
                remaining[unk] += 1

print(f"\n  Unknown segments (2+ chars, by frequency):")
for unk, count in remaining.most_common(40):
    # Try to interpret
    notes = ''
    ul = unk.lower()
    if 'sch' in ul: notes = '(contains SCH digraph)'
    if 'ch' in ul: notes = '(contains CH digraph)'
    if ul.endswith('en'): notes = '(German infinitive/plural ending?)'
    if ul.endswith('er'): notes = '(German comparative/agent ending?)'
    if ul.endswith('et'): notes = '(German verb ending?)'
    if ul.endswith('t'): notes = notes or '(German verb ending?)'
    print(f"    {unk:25s} {count:3d}x  {notes}")

# ============================================================
# 10. SINGLE-CODE SWAP TEST FOR P
# ============================================================
print(f"\n{'='*80}")
print("10. TESTING CODES AS POTENTIAL P")
print(f"{'='*80}")

# Count each code's frequency
code_freqs = Counter()
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    for p in pairs:
        code_freqs[p] += 1

# Expected P frequency: ~0.8% of ~5600 pairs = ~45 occurrences
# Look for codes currently assigned to over-represented letters
# that might be P instead

# Current letter frequencies
all_text_combined = ''
for book in books:
    dec, _ = decode(book)
    all_text_combined += dec

letter_freq = Counter(all_text_combined)
total_letters = sum(letter_freq.values())

german_expected = {
    'E': 17.4, 'N': 9.8, 'I': 7.6, 'S': 7.3, 'R': 7.0,
    'A': 6.5, 'T': 6.2, 'D': 5.1, 'H': 4.8, 'U': 4.2,
    'L': 3.4, 'G': 3.0, 'O': 2.5, 'C': 2.7, 'M': 2.5,
    'B': 1.9, 'W': 1.9, 'F': 1.7, 'K': 1.2, 'Z': 1.1,
    'V': 0.7, 'P': 0.8
}

print(f"\n  Letters with excess frequency (candidates to lose a code to P):")
for letter in 'ENISRTADHUGOLMCWFKZBV':
    actual = letter_freq.get(letter, 0) / total_letters * 100
    expected = german_expected.get(letter, 0)
    excess = actual - expected
    if excess > 1.5:
        # List codes for this letter
        codes_for = sorted([c for c, l in mapping.items() if l == letter],
                          key=lambda c: code_freqs.get(c, 0))
        # The rarest code for this letter is the best P candidate
        if codes_for:
            rarest = codes_for[0]
            rarest_freq = code_freqs.get(rarest, 0)
            print(f"    {letter}: {actual:.1f}% (expected {expected:.1f}%, excess +{excess:.1f}%)")
            print(f"       Rarest code: {rarest} ({rarest_freq}x)")
            # Test this code as P
            m_test = dict(mapping)
            m_test[rarest] = 'P'
            # Find words created
            p_words = []
            for bi2, book in enumerate(books):
                dec_t, pairs_t = decode(book, m_test)
                for k, p in enumerate(pairs_t):
                    if p == rarest:
                        ctx = dec_t[max(0,k-4):min(len(dec_t),k+5)]
                        p_words.append(f"Bk{bi2}:{ctx}")
            print(f"       As P: {'; '.join(p_words[:5])}")

# ============================================================
# 11. SPECIFIC P-WORD TEST
# ============================================================
print(f"\n{'='*80}")
print("11. SEARCHING FOR PLATZ, PLAGE, PFORTE, etc.")
print(f"{'='*80}")

# Common German words with P that might appear in this narrative
p_words_test = ['platz', 'plage', 'pforte', 'pfad', 'priester', 'prophet',
                'palast', 'pein', 'pilger', 'pracht', 'preis']

# For each, check if changing one letter to P in decoded text creates the word
for pw in p_words_test:
    # Search for the word with each position replaced by any letter
    for pos in range(len(pw)):
        if pw[pos] == 'p':
            # What letter is currently there instead of P?
            pattern = pw[:pos] + '.' + pw[pos+1:]
            # Search in decoded text
            import re
            for bi, dec, pairs in all_decoded:
                for match in re.finditer(pattern.upper(), dec):
                    start = match.start()
                    actual_char = dec[start + pos]
                    actual_code = pairs[start + pos] if start + pos < len(pairs) else '??'
                    ctx = dec[max(0,start-5):min(len(dec),start+len(pw)+5)]
                    print(f"  '{pw}' at Bk{bi} pos {start}: {ctx} (code {actual_code}={actual_char} should be P)")

# ============================================================
# 12. SUPERSTRING WITH LOWER OVERLAP THRESHOLD
# ============================================================
print(f"\n{'='*80}")
print("12. SUPERSTRING ASSEMBLY (overlap >= 2)")
print(f"{'='*80}")

# Decode all, get unique fragments
unique = {}
for i, dec, _ in all_decoded:
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

fragments = sorted(unique.values(), key=len, reverse=True)
print(f"  {len(fragments)} unique non-substring fragments")

# Greedy overlap with threshold 2
def overlap(a, b):
    max_ov = min(len(a), len(b))
    for k in range(max_ov, 0, -1):
        if a[-k:] == b[:k]:
            return k
    return 0

assembled = list(fragments)
merge_log = []
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
    if best_ov < 2:  # Lower threshold
        break
    merge_log.append(f"  Merged {len(assembled[best_i])}+{len(assembled[best_j])} chars (overlap {best_ov})")
    new_assembled = [best_merged]
    for k in range(len(assembled)):
        if k != best_i and k != best_j:
            new_assembled.append(assembled[k])
    assembled = new_assembled

print(f"  After assembly (threshold 2): {len(assembled)} fragment(s)")
for k, frag in enumerate(assembled):
    print(f"    Fragment {k+1}: {len(frag)} chars")

# Show the merged result
if len(assembled) < 31:  # Improved from before
    print(f"\n  Assembly improved! Was 31 fragments, now {len(assembled)}")

# Show largest fragment with DP segmentation
if assembled:
    main = assembled[0]
    main_c = collapse_doubles(main)
    tokens, cov = dp_segment(main_c, ALL_WORDS)
    pct = cov / len(main_c) * 100
    print(f"\n  Largest fragment ({len(main)} chars, collapsed {len(main_c)}):")
    print(f"  Coverage: {pct:.1f}%")
    print(f"  {' '.join(tokens)}")

# ============================================================
# 13. LETTER FREQUENCY COMPARISON WITH COLLAPSED DOUBLES
# ============================================================
print(f"\n{'='*80}")
print("13. LETTER FREQUENCIES (collapsed doubles)")
print(f"{'='*80}")

collapsed_all = collapse_doubles(all_text_combined)
freq_c = Counter(collapsed_all)
total_c = sum(freq_c.values())

print(f"\n  {'Letter':>6} {'Original':>10} {'Collapsed':>10} {'Expected':>10}")
for letter in 'ENISRTADHUGOLMCWFKZBV':
    orig_pct = letter_freq.get(letter, 0) / total_letters * 100
    coll_pct = freq_c.get(letter, 0) / total_c * 100
    expected = german_expected.get(letter, 0)
    marker = ''
    if abs(coll_pct - expected) < abs(orig_pct - expected):
        marker = ' (improved)'
    print(f"  {letter:>6} {orig_pct:>9.1f}% {coll_pct:>9.1f}% {expected:>9.1f}%{marker}")
