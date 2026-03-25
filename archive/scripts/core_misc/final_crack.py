"""
Final cracking attempt: resolve code 71, identify proper nouns,
decode full narrative with optimal mapping.
"""
import json
import os
from collections import Counter

data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'final_mapping_v3.json'), 'r') as f:
    mapping = json.load(f)

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    def ic(counts, total):
        if total <= 1: return 0
        return sum(c*(c-1) for c in counts.values()) / (total*(total-1))
    return 0 if ic(Counter(bp0), len(bp0)) > ic(Counter(bp1), len(bp1)) else 1

def decode(book, m):
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    return ''.join(m.get(p, '?') for p in pairs), pairs

# ============================================================
# 1. CODE 71: FULL CONTEXT WITH WIDER WINDOW
# ============================================================
print("=" * 80)
print("1. CODE 71: I vs N — FULL CONTEXT COMPARISON")
print("=" * 80)

m_n = dict(mapping)
m_n['71'] = 'N'

for i, book in enumerate(books):
    dec_i, pairs = decode(book, mapping)
    dec_n, _ = decode(book, m_n)
    for k, p in enumerate(pairs):
        if p == '71':
            start = max(0, k-8)
            end = min(len(pairs), k+9)
            ctx_i = dec_i[start:end]
            ctx_n = dec_n[start:end]
            print(f"  Bk{i:2d} pos {k:3d}: I={ctx_i}")
            print(f"               N={ctx_n}")
            print()

# ============================================================
# 2. KEY INSIGHT: ESNICHN → ES NICHT?
# ============================================================
print(f"\n{'='*80}")
print("2. DOES 71=N CREATE 'NICHT' (not)?")
print(f"{'='*80}")

for i, book in enumerate(books):
    dec_n, pairs = decode(book, m_n)
    # ESNICHN: ES + NICH + ...
    if 'NICH' in dec_n:
        pos = dec_n.find('NICH')
        ctx = dec_n[max(0,pos-10):min(len(dec_n),pos+15)]
        codes = pairs[max(0,pos-10):min(len(pairs),pos+15)]
        print(f"  Bk{i}: ...{ctx}...")
        print(f"    Codes: {' '.join(codes)}")

# ============================================================
# 3. WHAT ABOUT WIND?
# ============================================================
print(f"\n{'='*80}")
print("3. DOES 71=N CREATE 'WIND'?")
print(f"{'='*80}")

for i, book in enumerate(books):
    dec_n, pairs = decode(book, m_n)
    if 'WIND' in dec_n:
        pos = dec_n.find('WIND')
        ctx = dec_n[max(0,pos-8):min(len(dec_n),pos+12)]
        codes = pairs[max(0,pos-8):min(len(pairs),pos+12)]
        print(f"  Bk{i}: ...{ctx}...")
        print(f"    Codes: {' '.join(codes)}")

# ============================================================
# 4. FREQUENCY WITH 71=N
# ============================================================
print(f"\n{'='*80}")
print("4. LETTER FREQUENCIES WITH 71=N")
print(f"{'='*80}")

all_text = ''
for book in books:
    dec, _ = decode(book, m_n)
    all_text += dec

freq = Counter(all_text)
total = sum(freq.values())

german_freq = {
    'E': 17.4, 'N': 9.8, 'I': 7.6, 'S': 7.3, 'R': 7.0,
    'A': 6.5, 'T': 6.2, 'D': 5.1, 'H': 4.8, 'U': 4.2,
    'L': 3.4, 'G': 3.0, 'O': 2.5, 'C': 2.7, 'M': 2.5,
    'B': 1.9, 'W': 1.9, 'F': 1.7, 'K': 1.2, 'Z': 1.1,
    'V': 0.7, 'P': 0.8
}

print(f"\nTotal chars: {total}")
print(f"\n  {'Letter':>6} {'Count':>6} {'Actual%':>8} {'Expected%':>10} {'Delta':>8}")
for letter in 'ENISRTADHUGOLMCWFKZBV':
    count = freq.get(letter, 0)
    actual = count / total * 100
    expected = german_freq.get(letter, 0)
    delta = actual - expected
    marker = ' <<<' if abs(delta) > 2.0 else ''
    print(f"  {letter:>6} {count:>6} {actual:>7.1f}% {expected:>9.1f}% {delta:>+7.1f}{marker}")

# ============================================================
# 5. FULL GREEDY SEGMENTATION WITH 71=N
# ============================================================
print(f"\n{'='*80}")
print("5. NARRATIVE WITH 71=N (GREEDY SEGMENTATION)")
print(f"{'='*80}")

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
auch blick dunkel feind flucht gift grabe heer kraft macht neid recht schau schar sieg tief
weit wild zorn bild blut burg dorf eben feld fest fort gang grab haus herz hoch
kalt kern klug land last leer letzt link mass nacht naht nein nord rand raum rein ring
rund sache scharf schlecht schnell schwer still stolz streng stuck stumm suche tief
traum treue trost turm volk wache wand zehn ziel zug
garen gar ren ann gen ser tier net ode oede
dieser diese dieses seinen seiner seines
toten toter totes tote tod
rune stein steine steinen
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
nicht nichts
wind winde winden
schwiteio tharsc totniurg hearuchtiger tautr eilch labgzeras minheddem utrunr
labrrni aunrsongetrases uongetrases
""".split())

def segment_greedy(text, words=GERMAN, max_word=20):
    text_lower = text.lower()
    n = len(text_lower)
    result = []
    i = 0
    while i < n:
        best_word = None
        best_len = 0
        for length in range(min(max_word, n-i), 1, -1):
            candidate = text_lower[i:i+length]
            if candidate in words and length >= 2:
                best_word = candidate
                best_len = length
                break
        if best_word:
            result.append(best_word.upper())
            i += best_len
        else:
            unk = text[i].upper()
            i += 1
            while i < n:
                found = False
                for length in range(min(max_word, n-i), 1, -1):
                    if text_lower[i:i+length] in words and length >= 2:
                        found = True
                        break
                if found:
                    break
                unk += text[i].upper()
                i += 1
            result.append(f'[{unk}]')
    return ' '.join(result)

# Segment key books with 71=N
key_books = [5, 2, 9, 27, 11, 32, 48, 53, 0, 23, 24, 28, 6, 50]
for bi in key_books:
    if bi < len(books):
        dec, _ = decode(books[bi], m_n)
        segmented = segment_greedy(dec)
        covered = sum(len(w) for w in segmented.split() if not w.startswith('['))
        total_chars = len(dec)
        pct = covered / total_chars * 100 if total_chars > 0 else 0
        print(f"\n  Book {bi} ({pct:.0f}% covered):")
        print(f"    {segmented}")

# ============================================================
# 6. UNKNOWN SEGMENTS AFTER 71=N
# ============================================================
print(f"\n{'='*80}")
print("6. REMAINING UNKNOWNS (71=N)")
print(f"{'='*80}")

unknowns = Counter()
for i, book in enumerate(books):
    dec, _ = decode(book, m_n)
    seg = segment_greedy(dec)
    for token in seg.split():
        if token.startswith('[') and token.endswith(']'):
            unk = token[1:-1]
            if len(unk) >= 2:
                unknowns[unk] += 1

print("\n  Unknown segments (2+ chars, by frequency):")
for unk, count in unknowns.most_common(40):
    print(f"    {unk:25s} {count:3d}x")

# ============================================================
# 7. RARE CODE VERIFICATION
# ============================================================
print(f"\n{'='*80}")
print("7. RARE CODES (<=5 occurrences)")
print(f"{'='*80}")

code_freqs = Counter()
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    for p in pairs:
        code_freqs[p] += 1

rare = [(c, f, m_n.get(c, '?')) for c, f in code_freqs.items() if f <= 5]
rare.sort(key=lambda x: x[1])
for code, freq, letter in rare:
    # Show contexts
    ctxs = []
    for i, book in enumerate(books):
        dec, pairs = decode(book, m_n)
        for k, p in enumerate(pairs):
            if p == code:
                ctx = dec[max(0,k-4):min(len(dec),k+5)]
                ctxs.append(f"Bk{i}:{ctx}")
    print(f"  Code {code}: {freq}x = {letter} — {'; '.join(ctxs[:3])}")

# ============================================================
# 8. SAVE MAPPING V4 (71=N)
# ============================================================
print(f"\n{'='*80}")
print("8. SAVING MAPPING V4")
print(f"{'='*80}")

m4 = dict(m_n)
output_path = os.path.join(data_dir, 'final_mapping_v4.json')
with open(output_path, 'w') as f:
    json.dump(m4, f, indent=2, sort_keys=True)
print(f"Saved to {output_path}")
print("Changes v3 -> v4: 71: I -> N (word coverage 36 vs 21)")

# Letter distribution
lc = Counter()
for c, l in m4.items():
    lc[l] += 1
print(f"\nCode distribution (v4):")
for letter in 'ENISRTADHUGOLMCWFKZBV':
    codes = sorted([c for c, l in m4.items() if l == letter])
    total_f = sum(code_freqs.get(c, 0) for c in codes)
    print(f"  {letter}: {lc.get(letter,0):2d} codes, {total_f:4d}x — {', '.join(codes)}")

# ============================================================
# 9. FULL NARRATIVE RECONSTRUCTION (best attempt)
# ============================================================
print(f"\n{'='*80}")
print("9. FULL NARRATIVE — BOOK 5 (most complete)")
print(f"{'='*80}")

dec5, pairs5 = decode(books[5], m4)
seg5 = segment_greedy(dec5)
print(f"\n  Raw decoded: {dec5}")
print(f"\n  Segmented:   {seg5}")

# Manual word boundary analysis
print(f"\n  MANUAL PARSING:")
# Book 5 decoded with 71=N
# Looking at the raw text and applying known word boundaries
text = dec5
# Known patterns:
# EN HIER [TAUTR] IST [EILCH] AN [HEARUCHTIGER] SO DASS TUN DIESER
# T EINER SEINE DE [TOTNIURG] SEE RL AB RRNI WIR UND IE
# [MINHEDDEM] ID DIE URALTE STEINEN TER AD [THARSC] IST SCHAU NRU

# With 71=N, IIIWII becomes INNWII and others change
# Let me trace specific positions
for k, p in enumerate(pairs5):
    if p == '71':
        ctx = dec5[max(0,k-5):min(len(dec5),k+6)]
        ctx_i = ''.join(mapping.get(pairs5[j], '?') for j in range(max(0,k-5), min(len(pairs5),k+6)))
        print(f"  pos {k}: with N={ctx}  (was I: {ctx_i})")
