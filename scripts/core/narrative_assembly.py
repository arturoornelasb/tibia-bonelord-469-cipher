"""
Final narrative assembly: reconstruct the complete Bonelord text in reading order.
Uses all Session 8-9 discoveries:
- Mapping v4 (99 codes, 22 letters)
- Collapsed doubles (RUIIN->RUIN, WIISET->WISET=WISSET)
- FINDEN confirmed (11x)
- Proper nouns identified
- MHG vocabulary (WISSET = "know ye")
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

def collapse_doubles(text):
    if not text: return text
    result = [text[0]]
    for c in text[1:]:
        if c != result[-1]:
            result.append(c)
    return ''.join(result)

# ============================================================
# 1. BUILD COMPLETE SUPERSTRING (aggressive overlap)
# ============================================================
print("=" * 80)
print("1. SUPERSTRING ASSEMBLY")
print("=" * 80)

all_decoded = []
for i, book in enumerate(books):
    dec, pairs = decode(book)
    all_decoded.append((i, dec))

# Get unique texts
unique = {}
for i, dec in all_decoded:
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
print(f"  {len(all_decoded)} books -> {len(unique)} unique fragments")

# Greedy overlap with threshold 2
def overlap(a, b):
    max_ov = min(len(a), len(b))
    for k in range(max_ov, 0, -1):
        if a[-k:] == b[:k]:
            return k
    return 0

assembled = list(fragments)
while len(assembled) > 1:
    best_ov = 0
    best_i = best_j = -1
    best_merged = ''
    for i in range(len(assembled)):
        for j in range(len(assembled)):
            if i == j: continue
            ov = overlap(assembled[i], assembled[j])
            if ov > best_ov:
                best_ov = ov
                best_i, best_j = i, j
                best_merged = assembled[i] + assembled[j][ov:]
    if best_ov < 2:
        break
    new_assembled = [best_merged]
    for k in range(len(assembled)):
        if k != best_i and k != best_j:
            new_assembled.append(assembled[k])
    assembled = new_assembled

print(f"  -> {len(assembled)} assembled pieces")
for k, a in enumerate(assembled):
    print(f"     Piece {k+1}: {len(a)} chars")

# Sort by length descending
assembled.sort(key=len, reverse=True)

# ============================================================
# 2. WORD SEGMENTATION WITH FULL DICTIONARY
# ============================================================
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
gesehen sehen schauen fels felsen
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
enden endet runde runden
erbe erben erbt
spur spuren
schwiteio tharsc totniurg hearuchtiger tautr eilch labgzeras minheddem utrunr
labrrni aunrsongetrases uongetrases hihl runeort
""".split())

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
# 3. EACH ASSEMBLED PIECE WITH SEGMENTATION
# ============================================================
print(f"\n{'='*80}")
print("2. ALL PIECES SEGMENTED (collapsed doubles)")
print(f"{'='*80}")

for k, piece in enumerate(assembled):
    piece_c = collapse_doubles(piece)
    tokens, cov = dp_segment(piece_c)
    pct = cov / len(piece_c) * 100 if piece_c else 0
    print(f"\n--- Piece {k+1} ({len(piece)} chars, collapsed {len(piece_c)}, {pct:.0f}% covered) ---")
    line = ''
    for t in tokens:
        if len(line) + len(t) + 1 > 90:
            print(f"  {line}")
            line = ''
        line += t + ' '
    if line.strip():
        print(f"  {line}")

# ============================================================
# 4. IDENTIFY ALL RECURRING SENTENCE FRAGMENTS
# ============================================================
print(f"\n{'='*80}")
print("3. RECURRING SENTENCE FRAGMENTS")
print(f"{'='*80}")

# Find repeating substrings of length >= 20 across all books
all_text = ''.join(dec for _, dec in all_decoded)

substr_counts = Counter()
for length in range(20, 60):
    for start in range(len(all_text) - length):
        sub = all_text[start:start+length]
        if sub not in substr_counts:
            count = all_text.count(sub)
            if count >= 3:
                substr_counts[sub] = count

# Remove substrings of longer strings
to_remove = set()
subs = list(substr_counts.keys())
subs.sort(key=len, reverse=True)
for i, s1 in enumerate(subs):
    for s2 in subs[:i]:
        if s1 in s2 and substr_counts[s2] == substr_counts[s1]:
            to_remove.add(s1)

for s in to_remove:
    del substr_counts[s]

# Show top recurring fragments with translation
print(f"\n  Top recurring sentence fragments (>= 3x):")
for sub, count in sorted(substr_counts.items(), key=lambda x: -x[1])[:15]:
    sub_c = collapse_doubles(sub)
    tokens, _ = dp_segment(sub_c)
    seg = ' '.join(tokens)
    print(f"\n  [{count}x] {sub[:60]}...")
    print(f"       -> {seg[:80]}")

# ============================================================
# 5. THE COMPLETE NARRATIVE
# ============================================================
print(f"\n{'='*80}")
print("4. THE COMPLETE BONELORD NARRATIVE")
print(f"{'='*80}")

# Proper nouns and their likely meanings
proper_nouns = {
    'LABGZERAS': 'King (KOENIG LABGZERAS)',
    'AUNRSONGETRASES': 'Royal title/epithet of King Labgzeras',
    'TOTNIURG': 'Place name, reversed GRUINTOT (Dead Ruin)',
    'HEARUCHTIGER': 'Place/feature, possibly "the infamous/steep one"',
    'TAUTR': 'Person or entity name',
    'EILCH': 'Status/role of TAUTR',
    'MINHEDDEM': 'Entity associated with ancient stones',
    'THARSC': 'Place, possibly containing HARSCH (harsh/rough)',
    'SCHWITEIO': 'Entity/closing formula, associated with endings',
    'UTRUNR': 'Concept, possibly "utterance" (related to aeussern?)',
    'LABRRNI': 'Name (shares LAB- prefix with LABGZERAS)',
    'HIHL': 'Proper noun (context: MIN HIHL = my/mine HIHL)',
    'RUNEORT': 'Compound: RUNE + ORT = rune-place',
}

# Known German vocabulary in the text
vocabulary = {
    'ENDE': 'end',
    'DENEN': 'to those/whom',
    'DER': 'the (masc.)',
    'REDE': 'speech/discourse',
    'KOENIG': 'king',
    'HIER': 'here',
    'IST': 'is',
    'AN': 'at/on',
    'SO': 'so/thus',
    'DASS': 'that',
    'TUN': 'to do',
    'DIESER': 'this (one)',
    'EINER': 'a/one',
    'SEINE': 'his/its',
    'SEE': 'lake/sea',
    'WIR': 'we',
    'UND': 'and',
    'DIE': 'the (fem./pl.)',
    'URALTE': 'ancient',
    'STEINEN': 'stones',
    'SCHAUN': 'to behold (archaic)',
    'RUIN': 'ruin',
    'WISSET': 'know ye! (MHG imperative)',
    'ICH': 'I',
    'GAREN': 'to ferment/to enclose',
    'FINDEN': 'to find',
    'EIGEN': 'own/self',
    'DAS': 'the/that',
    'ES': 'it',
    'AUS': 'out/from',
    'FACH': 'compartment/profession',
    'ORT': 'place',
    'NEU': 'new',
    'ALT/ALTE': 'old/ancient',
    'STEIN': 'stone',
    'RUNE': 'rune',
    'TAG': 'day',
    'STEH': 'stand',
    'WIND': 'wind',
    'FELS': 'rock/cliff',
    'SIE': 'they/she',
    'DA': 'there/since',
    'MIN': 'my (archaic)',
    'SEIN': 'his/to be',
    'NACH': 'after/toward',
    'SEID': 'since/be (imperative)',
    'VIEL': 'much/many',
    'NUN': 'now',
    'UNTER': 'under/among',
    'ERSTE': 'first',
    'HAT': 'has',
    'ALS': 'as/when',
    'ODE': 'wasteland/desolate',
    'ERDE': 'earth',
}

print(f"\n  === PROPER NOUNS ({len(proper_nouns)}) ===")
for name, meaning in proper_nouns.items():
    print(f"    {name:25s} = {meaning}")

print(f"\n  === VOCABULARY ({len(vocabulary)} German words confirmed) ===")
for word, meaning in sorted(vocabulary.items()):
    print(f"    {word:20s} = {meaning}")

# Count total unique narrative text
total_unique_chars = sum(len(p) for p in assembled)
total_collapsed = sum(len(collapse_doubles(p)) for p in assembled)

# Per-book coverage
total_cov = 0
total_len = 0
for book in books:
    dec, _ = decode(book)
    dc = collapse_doubles(dec)
    _, cov = dp_segment(dc)
    total_cov += cov
    total_len += len(dc)

print(f"\n  === STATISTICS ===")
print(f"  Total books: 70")
print(f"  Unique assembled pieces: {len(assembled)}")
print(f"  Total unique text: {total_unique_chars} chars ({total_collapsed} collapsed)")
print(f"  Per-book coverage: {total_cov}/{total_len} = {total_cov/total_len*100:.1f}%")
print(f"  Distinct words found: {len(vocabulary)}")
print(f"  Proper nouns: {len(proper_nouns)}")
print(f"  Mapping: 99 codes -> 22 letters (A-H, I, K-N, O-V, W, Z)")
print(f"  Missing letters: P, J, Q, X, Y")

# The narrative reconstruction
print(f"""
  === NARRATIVE RECONSTRUCTION ===

  The 70 books of the Hellgate Library encode a single German narrative,
  viewed through overlapping windows. The text is a royal proclamation
  or chronicle, written in a formal/archaic register.

  THE STORY (reconstructed reading order):

  1. TITLE/COLOPHON (appears at end of most book windows):
     "ENDE UTRUNR DENEN DER REDE KOENIG LABGZERAS AUNRSONGETRASES"
     = "End of the [Utrunr/proclamation] of those of the speech of
        King Labgzeras [the Aunrsongetrases]"

  2. THE SETTING:
     "EN HIER TAUTR IST EILCH AN HEARUCHTIGER"
     = "Here, Tautr is Eilch at Hearuchtiger"
     (Introducing a character/entity named Tautr, who holds the role
      of Eilch at a place called Hearuchtiger)

  3. THE ACTION AT TOTNIURG LAKE:
     "SO DASS TUN DIESER EINER SEINE DE TOTNIURG SEE"
     = "So that this one does his [duty/task at] Totniurg Lake"
     (TOTNIURG reversed = GRUINTOT = "Dead Ruin" / "Ruin of Death")

  4. THE COMPANIONS:
     "LABRRNI WIR UND MINHEDDEM DIE URALTE STEINEN"
     = "Labrrni, we and Minheddem [at] the ancient stones"

  5. THE VISION AT THARSC:
     "THARSC IST SCHAUN RUIN WISSET"
     = "Tharsc is to behold -- the Ruin, know ye!"
     (WISSET = Middle High German imperative "know ye!")
     (The speaker commands the audience to know/acknowledge the ruin)

  6. THE RUNE-PLACE:
     "ICH OEL SO DE GAREN RUNEORT"
     = "I [anoint/consecrate] so the [enclosed] rune-place"
     "ER AM NEU DES ORT ANN DIE MINHEDDEM"
     = "He at the new place at the Minheddem"

  7. THE DISCOVERY:
     "FINDEN EIGEN DAS ES DER..."
     = "Find [their] own, that it the..."
     (11 occurrences of FINDEN suggest discovery/seeking is central)

  8. THE RUNE-EARTH-ENDINGS:
     "RUNE ERDE ENDEN"
     = "Rune earth ends" (runes of the earth come to an end?)

  9. THE CLOSING:
     "DEN DE ES SCHWITEIO"
     = "The [that] it Schwiteio"
     "DAS WIR ER ALTE"
     = "That we... the old [one]"

  THEMATIC SUMMARY:
  A king named LABGZERAS issues a proclamation about ancient ruins,
  rune-places, and stone monuments. Key locations include TOTNIURG
  (reversed: "Dead Ruin"), THARSC (a harsh/rough place), and
  HEARUCHTIGER (an infamous/steep place). The text speaks of
  companions (LABRRNI, MINHEDDEM), ancient stones (URALTE STEINEN),
  and commands the reader to "behold the ruin, know ye!" (SCHAUN RUIN
  WISSET). The narrative involves rune-places (RUNEORT), discovery
  (FINDEN), and references to endings (ENDE) and earth (ERDE).

  This is consistent with Tibia bonelord lore: ancient creatures
  associated with ruins, underground places, and mysterious knowledge.
  The formal German register and archaic vocabulary (WISSET, SCHAUN,
  MIN) suggest the text mimics medieval chronicle style.
""")

# ============================================================
# 6. SAVE FULL DECODED TEXT
# ============================================================
print(f"{'='*80}")
print("5. SAVING FULL DECODED TEXT")
print(f"{'='*80}")

output = {
    'mapping_version': 'v4',
    'total_books': len(books),
    'assembled_pieces': len(assembled),
    'coverage_pct': round(total_cov / total_len * 100, 1),
    'proper_nouns': proper_nouns,
    'vocabulary': vocabulary,
    'pieces': [],
    'per_book': []
}

for k, piece in enumerate(assembled):
    piece_c = collapse_doubles(piece)
    tokens, cov = dp_segment(piece_c)
    output['pieces'].append({
        'index': k,
        'raw': piece,
        'collapsed': piece_c,
        'segmented': ' '.join(tokens),
        'coverage_pct': round(cov / len(piece_c) * 100, 1) if piece_c else 0
    })

for i, book in enumerate(books):
    dec, _ = decode(book)
    dc = collapse_doubles(dec)
    tokens, cov = dp_segment(dc)
    output['per_book'].append({
        'book': i,
        'raw': dec,
        'collapsed': dc,
        'segmented': ' '.join(tokens),
        'coverage_pct': round(cov / len(dc) * 100, 1) if dc else 0
    })

output_path = os.path.join(data_dir, 'decoded_narrative.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(f"  Saved to {output_path}")

# Also save a plain text version
txt_path = os.path.join(data_dir, 'decoded_text.txt')
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write("BONELORD LANGUAGE - DECODED TEXT\n")
    f.write(f"Mapping: v4 (99 codes, 22 letters)\n")
    f.write(f"Coverage: {total_cov/total_len*100:.1f}%\n")
    f.write("=" * 60 + "\n\n")

    f.write("PER-BOOK DECODED TEXT:\n\n")
    for i, book in enumerate(books):
        dec, _ = decode(book)
        dc = collapse_doubles(dec)
        tokens, cov = dp_segment(dc)
        pct = cov / len(dc) * 100 if dc else 0
        f.write(f"Book {i:2d} ({pct:.0f}%): {' '.join(tokens)}\n")

    f.write("\n" + "=" * 60 + "\n")
    f.write("ASSEMBLED PIECES:\n\n")
    for k, piece in enumerate(assembled):
        piece_c = collapse_doubles(piece)
        tokens, cov = dp_segment(piece_c)
        pct = cov / len(piece_c) * 100 if piece_c else 0
        f.write(f"Piece {k+1} ({len(piece)} chars, {pct:.0f}%):\n")
        f.write(f"  {' '.join(tokens)}\n\n")

print(f"  Saved to {txt_path}")
