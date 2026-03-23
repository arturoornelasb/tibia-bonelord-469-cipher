"""
Attack underrepresented letters: B(0.3%), F(0.4%), K(0.4%), M(1.4%).
These are drastically below German expectations.
Test if reassigning rare codes from overrepresented letters improves word coverage.
"""
import json
import os
from collections import Counter
from itertools import combinations

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
# 1. CURRENT STATE: letter distribution per code
# ============================================================
print("=" * 80)
print("1. CURRENT CODE DISTRIBUTION AND FREQUENCIES")
print("=" * 80)

code_freqs = Counter()
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    for p in pairs:
        code_freqs[p] += 1

# Group by letter
letter_codes = {}
for code, letter in mapping.items():
    if letter not in letter_codes:
        letter_codes[letter] = []
    letter_codes[letter].append((code, code_freqs.get(code, 0)))

german_expected = {
    'E': 17.4, 'N': 9.8, 'I': 7.6, 'S': 7.3, 'R': 7.0,
    'A': 6.5, 'T': 6.2, 'D': 5.1, 'H': 4.8, 'U': 4.2,
    'L': 3.4, 'G': 3.0, 'O': 2.5, 'C': 2.7, 'M': 2.5,
    'B': 1.9, 'W': 1.9, 'F': 1.7, 'K': 1.2, 'Z': 1.1,
    'V': 0.7, 'P': 0.8
}

total_codes = sum(code_freqs.values())
print(f"\n  Total code pairs: {total_codes}")
print(f"\n  {'Letter':>6} {'Codes':>6} {'Total':>6} {'Actual%':>8} {'Expected%':>9} {'Delta':>7}")

for letter in sorted(letter_codes.keys(), key=lambda l: german_expected.get(l, 0), reverse=True):
    codes = letter_codes[letter]
    total = sum(f for _, f in codes)
    actual = total / total_codes * 100
    expected = german_expected.get(letter, 0)
    delta = actual - expected
    code_list = ', '.join(f"{c}({f})" for c, f in sorted(codes, key=lambda x: x[1]))
    marker = ' <<<' if delta < -1.0 else (' >>>' if delta > 2.0 else '')
    print(f"  {letter:>6} {len(codes):>6} {total:>6} {actual:>7.1f}% {expected:>8.1f}% {delta:>+6.1f}{marker}")
    if abs(delta) > 1.0:
        print(f"         Codes: {code_list}")

# ============================================================
# 2. IDENTIFY CANDIDATE SWAPS
# ============================================================
print(f"\n{'='*80}")
print("2. CANDIDATE CODE REASSIGNMENTS")
print(f"{'='*80}")

# Target letters that need MORE codes: B, F, K, M, P
# Source letters that have EXCESS: E, N, I, D, R

# For each target letter, find the rarest code from each source letter
# and test if swapping improves word coverage

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
wo woher wohin wovon
dazu dahin dahinter daher
neues neuen neuer neuem
alte alten alter altes
erste ersten erster erstes
nicht nichts wind winde winden finden
wisset weiset weisen
eigen eigene eigenen eigener eigenes
steh stehe stehen steht
runde runden
erbe erben erbt
enden endet
spur spuren
bann bannen
brief briefe
blatt blaetter
buch buecher
fels felsen
flucht flug
furcht fuerchte fuerchten
feuer feuers
frost
friede frieden
fall falle faellen
kampf kaempfe
kammer kammern
krone kronen
klage klagen
knochen
kraft kraefte
leib leiber
lager
nacht naechte
nach nachricht
ob oben
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

def count_word_coverage(m):
    """Count total chars covered by known words across all books."""
    total_covered = 0
    for book in books:
        dec, _ = decode(book, m)
        dec_c = collapse_doubles(dec)
        tl = dec_c.lower()
        n = len(tl)
        # Quick greedy coverage count
        i = 0
        covered = 0
        while i < n:
            best = 0
            for ln in range(min(25, n-i), 1, -1):
                if tl[i:i+ln] in WORDS and ln >= 2:
                    best = ln
                    break
            if best:
                covered += best
                i += best
            else:
                i += 1
        total_covered += covered
    return total_covered

# Baseline
baseline = count_word_coverage(mapping)
print(f"\n  Baseline word coverage: {baseline}")

# Test each rare code from overrepresented letters as each underrepresented letter
overrep = {'E': 20, 'N': 10, 'I': 7, 'D': 6, 'R': 7}
underrep = ['B', 'F', 'K', 'M', 'P']

results = []

for source_letter in overrep:
    # Get codes for this letter, sorted by frequency (rarest first)
    source_codes = sorted(
        [(c, f) for c, f in letter_codes.get(source_letter, [])],
        key=lambda x: x[1]
    )
    # Only test the 3 rarest codes
    for code, freq in source_codes[:3]:
        if freq > 100:  # Don't reassign frequent codes
            continue
        for target_letter in underrep:
            m_test = dict(mapping)
            m_test[code] = target_letter
            coverage = count_word_coverage(m_test)
            delta = coverage - baseline
            if delta > 0:
                results.append((code, source_letter, target_letter, freq, coverage, delta))

# Sort by improvement
results.sort(key=lambda x: -x[5])

print(f"\n  Top improvements from single-code swaps:")
print(f"  {'Code':>6} {'From':>5} {'To':>4} {'Freq':>5} {'Coverage':>9} {'Delta':>7}")
for code, src, tgt, freq, cov, delta in results[:20]:
    print(f"  {code:>6} {src:>5} {tgt:>4} {freq:>5} {cov:>9} {delta:>+7}")

# ============================================================
# 3. TEST BEST SWAP IN CONTEXT
# ============================================================
if results:
    best = results[0]
    code, src, tgt, freq, cov, delta = best
    print(f"\n{'='*80}")
    print(f"3. BEST SWAP: Code {code}: {src} -> {tgt} (+{delta} chars)")
    print(f"{'='*80}")

    m_test = dict(mapping)
    m_test[code] = tgt

    # Show all contexts where this code appears
    for i, book in enumerate(books):
        dec_old, pairs = decode(book)
        dec_new, _ = decode(book, m_test)
        for k, p in enumerate(pairs):
            if p == code:
                ctx_old = dec_old[max(0,k-6):min(len(dec_old),k+7)]
                ctx_new = dec_new[max(0,k-6):min(len(dec_new),k+7)]
                print(f"  Bk{i:2d} pos {k:3d}: {src}={ctx_old}  {tgt}={ctx_new}")

# ============================================================
# 4. TRACE THE GARBLED SECTION CODES
# ============================================================
print(f"\n{'='*80}")
print("4. GARBLED SECTION CODE TRACE")
print(f"{'='*80}")

# The section STEHWILGTNELNRHELUIRUNNHWNDFINDEN appears in Bk3 and others
# Let's trace the exact codes
target_text = "STEHWILGTNELNRHELUIRUNNHWNDFINDEN"

for i, book in enumerate(books):
    dec, pairs = decode(book)
    if 'STEHWILGT' in dec:
        pos = dec.find('STEHWILGT')
        section_len = len(target_text)
        section_codes = pairs[pos:pos+section_len]
        section_text = dec[pos:pos+section_len]
        print(f"\n  Bk{i:2d} pos {pos}:")
        print(f"    Text:  {section_text}")
        print(f"    Codes: {' '.join(section_codes)}")
        # Letter by letter
        for k in range(len(section_codes)):
            if pos+k < len(dec):
                c = section_codes[k]
                l = dec[pos+k]
                freq_c = code_freqs.get(c, 0)
                print(f"      [{k:2d}] Code {c} = {l} ({freq_c}x total)")
        break  # One example is enough

# ============================================================
# 5. WHAT IF GARBLED SECTION HAS MISASSIGNED CODES?
# ============================================================
print(f"\n{'='*80}")
print("5. TESTING ALTERNATIVE READINGS OF GARBLED SECTION")
print(f"{'='*80}")

# For the garbled section, test if any single code change makes German words
# First, identify the unique codes in the section
for i, book in enumerate(books):
    dec, pairs = decode(book)
    if 'STEHWILGT' in dec:
        pos = dec.find('STEHWILGT')
        # Get section up to FINDEN
        if 'FINDEN' in dec[pos:]:
            end = dec.find('FINDEN', pos)
            section_codes = pairs[pos:end]
            section_text = dec[pos:end]
        else:
            section_codes = pairs[pos:pos+27]
            section_text = dec[pos:pos+27]

        print(f"  Section: {section_text}")
        print(f"  Codes:   {' '.join(section_codes)}")

        # Try changing each code to every letter and see if words appear
        best_changes = []
        for k in range(len(section_codes)):
            orig_letter = section_text[k]
            for test_letter in 'ABCDEFGHIKLMNOPRSTUVWZ':
                if test_letter == orig_letter:
                    continue
                # Make the change
                new_text = section_text[:k] + test_letter + section_text[k+1:]
                new_collapsed = collapse_doubles(new_text)
                # Check if new words appear
                tl = new_collapsed.lower()
                for wlen in range(3, min(10, len(tl) - k + 3)):
                    for start in range(max(0, k-wlen+1), min(k+1, len(tl)-wlen+1)):
                        candidate = tl[start:start+wlen]
                        if candidate in WORDS and candidate not in section_text.lower():
                            old_frag = section_text[start:start+wlen]
                            best_changes.append((k, section_codes[k], orig_letter,
                                               test_letter, candidate, old_frag))

        # Show top unique changes
        seen = set()
        print(f"\n  Potential single-letter fixes:")
        for k, code, orig, new, word, old_frag in best_changes:
            key = (k, new)
            if key not in seen:
                seen.add(key)
                print(f"    pos {k}: {code}({orig})->{new} creates '{word}' (was '{old_frag}')")

        break

# ============================================================
# 6. MULTI-CODE SWAP TEST
# ============================================================
print(f"\n{'='*80}")
print("6. TESTING 2-CODE SWAPS")
print(f"{'='*80}")

# Test pairs of code reassignments
# Only test the top single-swap candidates
if len(results) >= 2:
    top_singles = results[:8]
    best_pair = None
    best_pair_delta = 0

    for i in range(len(top_singles)):
        for j in range(i+1, len(top_singles)):
            code1, src1, tgt1, _, _, _ = top_singles[i]
            code2, src2, tgt2, _, _, _ = top_singles[j]
            if code1 == code2:
                continue
            m_test = dict(mapping)
            m_test[code1] = tgt1
            m_test[code2] = tgt2
            cov = count_word_coverage(m_test)
            delta = cov - baseline
            if delta > best_pair_delta:
                best_pair_delta = delta
                best_pair = (code1, src1, tgt1, code2, src2, tgt2, cov, delta)

    if best_pair:
        c1, s1, t1, c2, s2, t2, cov, delta = best_pair
        print(f"  Best pair: Code {c1}:{s1}->{t1} + Code {c2}:{s2}->{t2}")
        print(f"  Coverage: {cov} (+{delta} from baseline {baseline})")

        # Show this mapping's segmentation
        m_test = dict(mapping)
        m_test[c1] = t1
        m_test[c2] = t2

        for bi in [5, 2, 9, 27, 53]:
            if bi < len(books):
                dec, _ = decode(books[bi], m_test)
                dec_c = collapse_doubles(dec)
                # Quick segment
                tl = dec_c.lower()
                n = len(tl)
                result = []
                pos = 0
                while pos < n:
                    best_w = None
                    for ln in range(min(25, n-pos), 1, -1):
                        if tl[pos:pos+ln] in WORDS and ln >= 2:
                            best_w = tl[pos:pos+ln].upper()
                            break
                    if best_w:
                        result.append(best_w)
                        pos += len(best_w)
                    else:
                        unk = ''
                        while pos < n:
                            found = False
                            for ln in range(min(25, n-pos), 1, -1):
                                if tl[pos:pos+ln] in WORDS and ln >= 2:
                                    found = True
                                    break
                            if found:
                                break
                            unk += dec_c[pos]
                            pos += 1
                        result.append(f'[{unk}]')
                print(f"\n    Bk{bi}: {' '.join(result)}")
    else:
        print("  No pair improvement found")
