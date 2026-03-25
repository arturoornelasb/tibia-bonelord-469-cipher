"""
Reconstruct the full narrative from the best mapping.
Focus on manual sentence parsing with expanded vocabulary,
including archaic German and compound word detection.
"""
import json
import os
from collections import Counter

data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

# Best mapping: Tier 14 + 05=S + 74=E + 37=E + 40=M + 02=D + 69=E
mapping = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U', '00': 'H', '14': 'N', '72': 'R',
    '91': 'S', '15': 'I', '76': 'E', '52': 'S', '42': 'D',
    '46': 'I', '48': 'N', '57': 'H', '04': 'M', '12': 'S',
    '58': 'N', '78': 'T', '51': 'R', '35': 'A', '34': 'L',
    '01': 'E', '59': 'S', '41': 'E', '30': 'E', '94': 'H',
    '47': 'D', '13': 'N', '71': 'I', '63': 'D', '93': 'N',
    '28': 'D', '86': 'E', '43': 'U', '70': 'U', '65': 'I',
    '16': 'I', '36': 'W', '64': 'T', '89': 'A', '80': 'G',
    '97': 'G', '75': 'T', '08': 'R', '20': 'F', '96': 'L',
    '99': 'O', '55': 'R', '67': 'E', '27': 'E', '03': 'E',
    '09': 'E', '05': 'S', '53': 'N', '44': 'U', '62': 'B',
    '68': 'R', '23': 'S', '17': 'E', '29': 'E', '66': 'A',
    '49': 'E', '38': 'K', '77': 'Z', '22': 'K', '82': 'O',
    '73': 'N', '50': 'I', '84': 'G', '25': 'O', '83': 'V',
    '81': 'T', '24': 'I', '79': 'O', '10': 'R', '54': 'M',
    '98': 'T', '39': 'E', '87': 'W',
    '74': 'E', '37': 'E', '40': 'M', '02': 'D', '69': 'E',
}

# Extended dictionary including archaic/Middle High German and compounds
WORDS = set()
base_words = """
a ab aber acht alle allem allen aller alles als also alt alte altem alten alter altes am an andere anderem
anderen anderer anderes ans auch auf aus aussen
bei beim bereits besser beste besten bis bisher bleibt blieb bringen bringt da dabei dadurch
dafuer daher dahin damals damit danach dann daran darauf daraus darin darueber
darum das dass davon davor dazu dein deine deinem deinen deiner dem den denen denn
der deren des dessen dich die dies diese diesem diesen dieser dieses dir doch dort drei du durch
eben ebenso ehe eher eigentlich ein eine einem einen einer einige einigem einigen
einiger einiges einst em en ende er erden erde erst erste erstem ersten erster erstes es etwas
fach fand fest finden findet fuer fuenf ganz gar geben gegen geh geheim gehen geht
genug gerade gering gern gibt ging gold gross grosse grossem grossen grosser gut gute gutem guten guter gutes
hab habe haben hat hatte her herr heute hier hin hinter
ich ihm ihn ihnen ihr ihre ihrem ihren ihrer im immer in ins ist
ja jede jedem jeden jeder jedes jedoch jene jenem jenen jener jenes jetzt jung
kalt kam kann kein keine keinem keinen keiner klar klein kleine kleinem kleinen kleiner
koenig koenige koenigen koenigs kommen kommt konnte kraft krieg kurz
lang lange langem langen langer lage leben leer lesen letzt letzte letzten licht liegt
machen macht man mehr mein meine meinem meinen meiner mensch menschen
mir mit morgen muss nach nacht nah nahe nahem nahen naher name namen neben nehmen nein
neu neue neuem neuen neuer neues nicht nichts nie niemand noch nun nur
ob oben oder ohne ort orte orten rede reden ring ruf rufen ruhig ruin rune runen runeort rund
sache sagen schlecht schloss schnell schon schreiben schuld schwer see sehr sei seid sein seine seinem
seinen seiner seit selbst sicher sie sind so soll sondern sonst stark statt stein steine steinem steinen
steil still strafe stueck suchen
tag tage tagen tages tat teil teile teilen teils tief tod tot tragen tritt tun
ueber um und uns unser unsere unserem unseren unserer unter uralte uraltem uralten uralter uraltes
viel viele vielem vielen voll vom von vor
wahr wald wand war warum was wasser weg wegen weil weiss weit weite weitem weiten weiter
welch welche welchem welchen welcher welches welt wenig wenige wenn wer werde werden wie wieder
wir wird wissen wo wohl wollen wort
zehn zeichen zeit zu zum zur zusammen zwei zwischen

stehen stand stehe steht suche recht kennen sehen nehmen geben kommen
gehen halten lassen legen setzen stellen brechen
sterne burg berg tor haus land finden gefunden
stein gebiet schwert gold silber feuer flamme licht dunkel norden sueden osten westen
koenigin koenigreich reich reiche reiches reichen
schau schauen alt hoch hohe hohem hohen hoher
denn doch noch schon eben gar sehr wohl recht erst
hier dort hin her da nun so
nachher demnach daher dahin sodann darauf davon

schwiteio tharsc totniurg hearuchtiger aunrsongetrases labge labgeras labgzeras
nu gem des ortes geh steil heer herrn lande laender koenigs
runeort steinen enden orten uralte dieser dieser dieses
finden rede teil teile nach aus dass tun seiner seine
erste fach heisst ehre klage lauf regen schlag tag tagen nacht

ehe eher ehren ehrte nichtig heilig stein steine steine tage tag rede reden
eid wunder kundig gesandt berg berge berges bergs ende enden
ereilen sagen sprach sprache gem treu treue heilig
am gebet gebiet gebiete gebieten los heil macht
dienen dienst diener dar vorder hinter aussen innen oben unten
gleich frieden frieden lager gesetz kraft schlacht recht
gnade bitte geschicht geschichten alt alten uralte uralten
mauer turm tor burg feste stadt festung
herrscher herr herren herrschaft fuerst fuerstin
trugen trueger truege trueg truge wart warten sagte
sah nahm gab ging kam liess hielt stand
nahmen gaben gingen kamen liessen hielten standen

eis schnee frost kalt kalt wind sturm meer see fluss
min mein dein sein kein lein wein rein fein bein
muessen koennen duerfen sollen wollen moegen
geist seele leib koerper blut herz mund
steinern eisern silbern golden nacht tages naechte
gesamt gleich gemein gering wenig viel gross klein
nah fern weit breit tief hoch lang kurz
dar daran darauf darin daraus darum davon dafuer
woher wohin warum weshalb wofuer

ab an bei bis auf aus durch fuer gegen hinter in mit nach neben ohne seit ueber um unter von vor zu zwischen
hinab hinauf hinaus hinein hindurch hinueber
herein heraus herab herauf herueber herunter

ort orte orten alten altem alte alter
""".split()
for w in base_words:
    if len(w) >= 2:
        WORDS.add(w)

# Add additional compound words and phrases likely in this text
WORDS.update("""
runen stein steine steinen uralte uraltem uralten uralter
koenig koenigin koenige koenigen koenigs koenigreich
schwiteio tharsc totniurg hearuchtiger aunrsongetrases labgzeras labge labgeras
runeort runeorte orten orte ortes finden fand gefunden
rede reden teil teile teilen teils nach dass tun diese dieser dieses diesem
seine seinem seinen seiner sein seid sein
steil an so da hier dort nun wir und die der das dem den des
ende enden rede reden schau schauen klage klagen
ab aus in um am im er es ich du wir sie
erste ersten erstem erster erstes
gehen geht ging kommen kommt kam stehen steht stand
fach faecher feld felder
sagen sage sagte gesagt sprach sprechen
mauer mauern turm tuerme tor tore burg burgen
eins zwei drei vier fuenf sechs sieben acht neun zehn
licht dunkel nacht tag tage nacht naechte
see meer fluss berg berge tal taeler wald waelder
ehrte ehre ehren gross grosse grossen grossem grosser
gnade gnaden barm barmherzig
lande laender landen land herrschaft herr herren herrscher
dienen dienst diener dienerschaft
treue treu untreu schwur schwuere
ueber unter hinter hoch tief
einst einstmals vorher nachher zuletzt
morgen morgens abend abends
""".split())

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    ic0 = ic_from_counts(Counter(bp0), len(bp0))
    ic1 = ic_from_counts(Counter(bp1), len(bp1))
    return 0 if ic0 > ic1 else 1

def decode_book(book):
    offset = get_offset(book)
    pairs = [book[j:j+2] for j in range(offset, len(book)-1, 2)]
    return ''.join(mapping.get(p, '?') for p in pairs)

def dp_parse(text):
    """DP word segmentation maximizing covered characters."""
    n = len(text)
    # dp[i] = max chars covered ending at position i
    dp = [0] * (n + 1)
    prev = [-1] * (n + 1)
    word_at = [None] * (n + 1)

    for i in range(n):
        # Option 1: skip this character
        if dp[i] > dp[i + 1]:
            dp[i + 1] = dp[i]
            prev[i + 1] = i
            word_at[i + 1] = None
        elif dp[i] == dp[i + 1] and prev[i + 1] == -1:
            dp[i + 1] = dp[i]
            prev[i + 1] = i

        # Option 2: match a word starting at i
        for length in range(2, min(25, n - i) + 1):
            word = text[i:i + length].lower()
            if word in WORDS:
                score = dp[i] + length
                if score > dp[i + length]:
                    dp[i + length] = score
                    prev[i + length] = i
                    word_at[i + length] = text[i:i + length].upper()

    # Backtrack
    words = []
    pos = n
    while pos > 0:
        w = word_at[pos]
        p = prev[pos]
        if p < 0:
            pos -= 1
            continue
        if w:
            words.append(w)
        pos = p
    words.reverse()
    return words, dp[n]

# ============================================================
# Decode all books and build ordered narrative
# ============================================================
print("=" * 80)
print("FULL DECODED NARRATIVE — BEST MAPPING")
print("=" * 80)

# First, build a superstring to establish the canonical order
decoded_books = []
for i, book in enumerate(books):
    dec = decode_book(book)
    decoded_books.append((i, dec))

# Find overlap between all pairs
def find_overlap(a, b, min_len=5):
    best = 0
    for k in range(min_len, min(len(a), len(b)) + 1):
        if a.endswith(b[:k]):
            best = k
    return best

# Greedy superstring assembly
used = [False] * len(decoded_books)
# Start with the longest book
fragments = sorted(decoded_books, key=lambda x: -len(x[1]))

# Remove books that are substrings of others
unique = []
for i, (idx, dec) in enumerate(fragments):
    is_sub = False
    for j, (idx2, dec2) in enumerate(fragments):
        if i != j and dec in dec2 and len(dec) < len(dec2):
            is_sub = True
            break
    if not is_sub:
        unique.append((idx, dec))

print(f"\n{len(decoded_books)} total books, {len(unique)} unique (not substrings)")

# Assemble superstring from unique books
current = unique[0][1]
remaining = list(unique[1:])

while remaining:
    best_overlap = 0
    best_idx = -1
    best_side = None  # 'right' or 'left'

    for i, (idx, dec) in enumerate(remaining):
        # Try appending dec to the right of current
        ov_right = find_overlap(current, dec)
        if ov_right > best_overlap:
            best_overlap = ov_right
            best_idx = i
            best_side = 'right'

        # Try prepending dec to the left of current
        ov_left = find_overlap(dec, current)
        if ov_left > best_overlap:
            best_overlap = ov_left
            best_idx = i
            best_side = 'left'

    if best_idx < 0 or best_overlap < 3:
        # No good overlap — separate fragment
        break

    idx, dec = remaining.pop(best_idx)
    if best_side == 'right':
        current = current + dec[best_overlap:]
    else:
        current = dec + current[best_overlap:]

superstring = current
print(f"Main superstring: {len(superstring)} chars")

# Parse the superstring
words, covered = dp_parse(superstring)
print(f"Word coverage: {covered}/{len(superstring)} ({covered/len(superstring)*100:.1f}%)")

# ============================================================
# Show the superstring with word boundaries
# ============================================================
print(f"\n{'='*80}")
print("SUPERSTRING WITH WORD BOUNDARIES")
print(f"{'='*80}")

# Mark word positions in the superstring
word_positions = []
pos = 0
text_lower = superstring.lower()
for word in words:
    # Find this word starting from current position
    found = text_lower.find(word.lower(), pos)
    if found >= 0:
        word_positions.append((found, found + len(word), word))
        pos = found + len(word)

# Print the superstring in segments with word boundaries
print()
seg_size = 60
for start in range(0, len(superstring), seg_size):
    chunk = superstring[start:start + seg_size]
    # Build annotation line
    anno = [' '] * len(chunk)
    word_line = ''
    chunk_words = []
    for ws, we, w in word_positions:
        if ws >= start and we <= start + seg_size:
            # This word is in this chunk
            rel_start = ws - start
            for k in range(rel_start, min(we - start, len(chunk))):
                anno[k] = '^'
            chunk_words.append(w)

    print(f"  {start:4d}: {chunk}")
    print(f"        {''.join(anno)}")
    if chunk_words:
        print(f"        [{' '.join(chunk_words)}]")
    print()

# ============================================================
# Extract the most readable consecutive sequences
# ============================================================
print(f"\n{'='*80}")
print("LONGEST READABLE SEQUENCES")
print(f"{'='*80}")

# Find runs of consecutive recognized words
min_run_len = 20  # minimum chars in a readable run
runs = []
if word_positions:
    run_start = word_positions[0][0]
    run_end = word_positions[0][1]
    run_words = [word_positions[0][2]]

    for i in range(1, len(word_positions)):
        ws, we, w = word_positions[i]
        gap = ws - run_end
        if gap <= 5:  # Allow up to 5 unrecognized chars between words
            run_end = we
            run_words.append(w)
        else:
            if run_end - run_start >= min_run_len:
                runs.append((run_start, run_end, run_words[:]))
            run_start = ws
            run_end = we
            run_words = [w]

    if run_end - run_start >= min_run_len:
        runs.append((run_start, run_end, run_words[:]))

runs.sort(key=lambda x: -(x[1] - x[0]))

print(f"\nFound {len(runs)} readable sequences (>{min_run_len} chars):\n")
for start, end, run_words in runs[:15]:
    raw = superstring[start:end]
    print(f"  Pos {start}-{end} ({end-start} chars):")
    print(f"    Raw: {raw}")
    print(f"    Words: {' '.join(run_words)}")
    print()

# ============================================================
# Attempt translation of the best passages
# ============================================================
print(f"\n{'='*80}")
print("ATTEMPTED GERMAN -> ENGLISH TRANSLATION")
print(f"{'='*80}")

# Key phrases we can translate
translations = [
    ("SO DASS TUN DIESER EINER SEINE", "so that this one does his"),
    ("WIR UND DIE URALTE STEINEN", "we and the ancient stones"),
    ("DENEN DER DER KOENIG LABGZERAS", "those of the/of King Labgzeras"),
    ("HIER STEIL AN HEARUCHTIGER", "here steep at Hearuchtiger"),
    ("AM NEU DES ORT AN", "at the new, of the place at"),
    ("IN DEM DIE URALTE STEINEN", "in which the ancient stones"),
    ("THARSC IST SCHAU", "Tharsc is look/see"),
    ("FINDEN DAS ES ERSTE", "find that it [is] the first"),
    ("RUNE DU TEIL AUS IN", "rune you part from in"),
    ("TOTNIURG SEE", "Totniurg lake (or: Totniurg, see!)"),
    ("RUNEORT AM NEU DES ORT", "rune-place at the new, of the place"),
    ("DIESER EINER SEINE", "this one his"),
    ("DEN ENDE REDE KOENIG", "the concluding speech [of] king"),
    ("AUNRSONGETRASES", "[proper noun - unknown meaning]"),
    ("SCHWITEIO", "[proper noun - unknown meaning]"),
    ("GAR EN RUNEORT", "entirely/fully at the rune-place"),
    ("NACH", "after/to"),
    ("DA TEIL", "there part"),
    ("AB WIR UND", "from, we and"),
    ("ERDE ENDEN", "earth ends"),
    ("RUNE ERDE ENDEN", "rune earth ends"),
    ("ICH ES ER AUS ENDE", "I it he from the end"),
]

for german, english in translations:
    print(f"  {german}")
    print(f"    => {english}")
    print()

# ============================================================
# Check proper noun reversals
# ============================================================
print(f"\n{'='*80}")
print("PROPER NOUN ANALYSIS")
print(f"{'='*80}")

nouns = {
    'TOTNIURG': 'GRUINTOT => GRUIN + TOT (death/dead)',
    'SCHWITEIO': 'OIETIWHCS => no clear reversal',
    'HEARUCHTIGER': 'REGIITHCURAEH => no clear reversal',
    'AUNRSONGETRASES': 'SESARTEQNOSRNUA => no clear reversal',
    'THARSC': 'CSRAHT => no clear reversal',
    'LABGZERAS': 'SAREZGBAL => no clear reversal',
    'LABGE': 'EGBAL => no clear reversal',
}

for noun, analysis in nouns.items():
    rev = noun[::-1]
    print(f"\n  {noun}")
    print(f"    Reversed: {rev}")
    print(f"    Analysis: {analysis}")

    # Check for meaningful substrings in reversed form
    for length in range(3, len(rev) + 1):
        for start in range(len(rev) - length + 1):
            sub = rev[start:start + length].lower()
            if sub in WORDS:
                print(f"    Contains word: {sub.upper()} (at pos {start})")

# ============================================================
# Frequency analysis - how many codes map to each letter
# ============================================================
print(f"\n{'='*80}")
print("CIPHER STATISTICS")
print(f"{'='*80}")

# Compare our letter frequencies with standard German
letter_freq_german = {
    'E': 16.93, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
    'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
    'L': 3.44, 'G': 3.01, 'O': 2.51, 'C': 2.73, 'M': 2.53,
    'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
    'V': 0.67, 'P': 0.79, 'J': 0.27, 'Q': 0.02, 'X': 0.03, 'Y': 0.04,
}

# Count actual letter frequencies in our decoded text
all_decoded = ''.join(decode_book(book) for book in books)
total_chars = len(all_decoded)
letter_counts = Counter(all_decoded)

print(f"\nTotal decoded characters: {total_chars}")
print(f"\n{'Letter':>6} {'Count':>6} {'Our %':>7} {'German %':>9} {'Codes':>6} {'Match':>7}")
print("-" * 50)
for letter in sorted(letter_freq_german.keys(), key=lambda x: -letter_freq_german[x]):
    count = letter_counts.get(letter, 0)
    our_pct = count / total_chars * 100
    german_pct = letter_freq_german[letter]
    num_codes = sum(1 for c, l in mapping.items() if l == letter)
    match = "OK" if abs(our_pct - german_pct) < 3 else ("HIGH" if our_pct > german_pct else "LOW")
    if letter not in [l for l in mapping.values()]:
        match = "MISSING"
    print(f"  {letter:>4} {count:>6} {our_pct:>6.1f}% {german_pct:>8.1f}% {num_codes:>5} {match:>7}")

# Missing letters
all_assigned = set(mapping.values())
missing = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ') - all_assigned
if missing:
    print(f"\nMissing letters (no codes assigned): {', '.join(sorted(missing))}")

# Unassigned codes
all_codes = set(f'{i:02d}' for i in range(100))
assigned = set(mapping.keys())
unassigned = all_codes - assigned
if unassigned:
    print(f"Unassigned codes: {', '.join(sorted(unassigned))}")

    # Check if they appear in any book
    for code in sorted(unassigned):
        count = 0
        for book in books:
            offset = get_offset(book)
            pairs = [book[j:j+2] for j in range(offset, len(book)-1, 2)]
            count += pairs.count(code)
        if count > 0:
            print(f"  Code {code}: appears {count} times (NOT MAPPED!)")
        else:
            print(f"  Code {code}: never appears in any book")
