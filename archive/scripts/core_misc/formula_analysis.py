"""Analyze the repeating formula pattern to crack word boundaries.
The core repeating phrase appears 8-11 times across books.
By aligning all instances, we can see what varies and what's fixed."""
import json
from collections import Counter

with open('books.json', 'r') as f:
    books = json.load(f)

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

all_codes = {
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
    '09': 'E', '05': 'C', '53': 'N', '44': 'U', '62': 'B',
    '68': 'R', '23': 'S', '17': 'E', '29': 'E', '66': 'A',
    '49': 'E', '38': 'K', '77': 'Z', '22': 'K', '82': 'O',
    '73': 'N', '50': 'I', '84': 'G', '25': 'O', '83': 'V',
    '81': 'T', '24': 'I', '79': 'O', '10': 'R', '54': 'M',
    '98': 'T', '39': 'E', '87': 'W',
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

def decode(bpairs):
    return ''.join(all_codes.get(p, '?') for p in bpairs)

texts = [decode(bp) for bp in book_pairs]

# ============================================================
# FIND THE CORE FORMULA — look for HEARUCHTIGER as anchor
# ============================================================
print("=" * 100)
print("FORMULA ANALYSIS — Using HEARUCHTIGER as anchor point")
print("=" * 100)

anchor = "HEARUCHTIGER"
for idx, text in enumerate(texts):
    pos = text.find(anchor)
    if pos == -1:
        continue
    # Get wide context: 40 chars before, full text after anchor
    start = max(0, pos - 40)
    end = min(len(text), pos + len(anchor) + 80)
    context = text[start:end]
    anchor_at = pos - start
    # Mark the anchor
    marked = context[:anchor_at] + '[' + anchor + ']' + context[anchor_at+len(anchor):]
    print(f"  Bk{idx:2d}: {marked}")

# ============================================================
# ALIGN ALL BOOKS ON THE FORMULA
# ============================================================
print(f"\n{'='*100}")
print("FULL BOOK ALIGNMENT — sorted by length, showing formula position")
print("=" * 100)

# Find the longest common substring among books that contain HEARUCHTIGER
formula_books = [(idx, text) for idx, text in enumerate(texts) if anchor in text]
print(f"Books containing '{anchor}': {len(formula_books)}")

for idx, text in sorted(formula_books, key=lambda x: -len(x[1])):
    pos = text.find(anchor)
    print(f"\n  Bk{idx:2d} ({len(text):3d}ch, anchor@{pos:3d}):")
    # Print full text in lines of 70
    for i in range(0, len(text), 70):
        line = text[i:i+70]
        # Highlight anchor position
        if pos >= i and pos < i + 70:
            rel = pos - i
            end_rel = min(rel + len(anchor), 70)
            line = line[:rel] + '[' + line[rel:end_rel] + ']' + line[end_rel:]
        print(f"    {i:4d}: {line}")

# ============================================================
# WHAT VARIES BETWEEN BOOKS?
# ============================================================
print(f"\n{'='*100}")
print("VARIABLE PARTS — What differs between formula instances?")
print("=" * 100)

# Align all books on HEARUCHTIGER position
aligned = []
for idx, text in formula_books:
    pos = text.find(anchor)
    aligned.append((idx, text, pos))

# Compare character-by-character relative to anchor
min_before = min(a[2] for a in aligned)
max_after = max(len(a[1]) - a[2] for a in aligned)

print(f"  Min text before anchor: {min_before}")
print(f"  Max text after anchor: {max_after}")

# Show columns that vary
for offset in range(-min_before, max_after):
    chars_at = []
    for idx, text, anchor_pos in aligned:
        abs_pos = anchor_pos + offset
        if 0 <= abs_pos < len(text):
            chars_at.append(text[abs_pos])
        else:
            chars_at.append('-')
    unique = set(chars_at) - {'-'}
    if len(unique) > 1:
        col_str = ''.join(chars_at)
        print(f"  offset {offset:+4d}: {col_str}  (varies: {unique})")

# ============================================================
# IMPROVED WORD SEGMENTATION of the formula
# ============================================================
print(f"\n{'='*100}")
print("WORD SEGMENTATION — Optimal parse of the core formula")
print("=" * 100)

# Take the longest instance, extract the full formula region
longest_idx, longest_text, longest_pos = max(aligned, key=lambda x: len(x[1]))
print(f"Using Bk{longest_idx} ({len(longest_text)} chars)")
print(f"Full text: {longest_text}")

# Extended German dictionary including archaic/Tibia forms
word_dict = set([
    # 2-letter
    'AB', 'AM', 'AN', 'DA', 'DU', 'ER', 'ES', 'IM', 'IN', 'JA', 'OB', 'SO',
    'UM', 'WO', 'ZU',
    # 3-letter
    'ALS', 'AUF', 'AUS', 'BEI', 'BIS', 'DAS', 'DEM', 'DEN', 'DER', 'DES',
    'DIE', 'DIR', 'EIN', 'FUR', 'GAB', 'GUT', 'HAT', 'HIN', 'ICH', 'IHM',
    'IHN', 'IST', 'KAM', 'MAN', 'MIT', 'NEU', 'NIE', 'NUN', 'NUR', 'ORT',
    'RAT', 'SAH', 'SEI', 'SIE', 'TAG', 'TAT', 'TOD', 'TUN', 'UND', 'VOM',
    'VON', 'VOR', 'WAR', 'WAS', 'WEG', 'WER', 'WIE', 'WIR', 'ZUM', 'ZUR',
    # 4-letter
    'ABER', 'ALLE', 'ALSO', 'AUCH', 'BERG', 'BURG', 'DACH', 'DANN', 'DASS',
    'DEIN', 'DENN', 'DIES', 'DOCH', 'DORT', 'DREI', 'EINE', 'ENDE', 'ERDE',
    'ERST', 'EUCH', 'FAND', 'FEST', 'FORT', 'GANZ', 'GEBE', 'GELD', 'GING',
    'GOLD', 'GOTT', 'HALB', 'HAND', 'HAUS', 'HEIL', 'HELD', 'HERR', 'HIER',
    'HOCH', 'JEDE', 'JENE', 'KAUM', 'KEIN', 'KERN', 'LAND', 'LANG', 'MEHR',
    'MEIN', 'MUSS', 'NACH', 'NAHE', 'NAME', 'NOCH', 'OHNE', 'ORTE', 'RIEF',
    'RUNE', 'SAGT', 'SANG', 'SATZ', 'SEHR', 'SEIN', 'SICH', 'SIND', 'SOHN',
    'STAT', 'TEIL', 'TIEF', 'TRUG', 'TURM', 'VIEL', 'VOLK', 'WEIL', 'WEIT',
    'WELT', 'WENN', 'WERT', 'WORT', 'WOHL', 'ZAHL', 'ZEIT', 'ZWEI',
    # 5-letter
    'ALLES', 'ALTER', 'ALTEN', 'ALTEM', 'ANDRE', 'BEIDE', 'BERGE', 'BOTEN',
    'BUERG', 'DAHER', 'DERER', 'DIESE', 'DURCH', 'EIGEN', 'EINEN', 'EINER',
    'EINEM', 'EINES', 'ERSTE', 'ETWAS', 'EUREN', 'EWIGE', 'GANZE', 'GEGEN',
    'GEHEN', 'GEIST', 'GEBEN', 'GROSS', 'HABEN', 'JEDER', 'JEDES', 'JEDEM',
    'JENEN', 'KEINE', 'KENNT', 'KRAFT', 'LANDE', 'LANGE', 'LAUFE', 'LEBEN',
    'LICHT', 'MACHT', 'NACHT', 'NEBEN', 'NICHT', 'ORTEN', 'RUNEN', 'SAGEN',
    'SAGTE', 'SEHEN', 'SEINE', 'STEHT', 'STEIN', 'TAGEN', 'TEILE', 'TEILS',
    'TRITT', 'UNTER', 'VIELE', 'WAGEN', 'WEDER', 'WELCH', 'WERDE', 'WESEN',
    'IMMER', 'SUCHE', 'STEIL', 'HEILT', 'HEISS',
    # 6-letter
    'ANDERE', 'BEIDER', 'DIESER', 'DIESES', 'DIESEM', 'DIESEN', 'DUNKEL',
    'EIGENE', 'ERSTEN', 'ERSTER', 'EWIGEN', 'FINDEN', 'FRAGEN', 'GANZEM',
    'GEHEIM', 'GRENZE', 'GROSSE', 'GRUPPE', 'HELFEN', 'HIMMEL', 'KOENIG',
    'KOMMEN', 'KONNTE', 'LANGEN', 'MACHEN', 'NICHTS', 'NORDEN', 'SEINES',
    'SEINER', 'SEINEM', 'SEINEN', 'STEINE', 'SUEDEN', 'TEMPEL', 'URALTE',
    'VOELKE', 'WIEDER', 'WISSEN', 'WOLLTE', 'ZEIGEN', 'ZEITEN',
    # 7-letter
    'ANDEREN', 'ANFANGS', 'EIGENEN', 'FLIEHEN', 'GROSSEN', 'LETZTEN',
    'STEINEN', 'STIMMEN', 'URALTEN', 'WAHREND', 'WOLLTEN',
    # 8+ letter
    'MENSCHEN', 'VERSCHIEDENE', 'ZUSAMMEN', 'WAHRHEIT',
    # Proper nouns (Tibia)
    'LABGZERAS', 'TOTNIURG', 'HEARUCHTIGER',
    # Game-specific patterns
    'RUNEORT', 'RUNENORT',
])

# DP word segmentation
n = len(longest_text)
dp = [(0, -1, None)] * (n + 1)
for i in range(1, n + 1):
    dp[i] = (dp[i-1][0], i-1, None)
    for wlen in range(2, min(20, i + 1)):
        start = i - wlen
        candidate = longest_text[start:i]
        if '?' not in candidate and candidate in word_dict:
            new_covered = dp[start][0] + wlen
            if new_covered > dp[i][0]:
                dp[i] = (new_covered, start, candidate)

words_found = []
pos = n
while pos > 0:
    _, prev, word = dp[pos]
    if word:
        words_found.append((prev, word))
        pos = prev
    else:
        pos = prev
words_found.reverse()

total_covered = dp[n][0]
print(f"  Coverage: {total_covered}/{n} = {total_covered/n*100:.1f}%")
print(f"  Words found: {len(words_found)}")

# Build segmented text
covered = [False] * n
for start, word in words_found:
    for j in range(start, start + len(word)):
        covered[j] = True

result = []
i = 0
while i < n:
    if covered[i]:
        for start, word in words_found:
            if start == i:
                result.append(f' {word} ')
                i += len(word)
                break
        else:
            result.append(longest_text[i])
            i += 1
    else:
        result.append(longest_text[i].lower())
        i += 1

annotated = ''.join(result)
while '  ' in annotated:
    annotated = annotated.replace('  ', ' ')

print(f"\n  Segmented text:")
for i in range(0, len(annotated), 90):
    print(f"    {annotated[i:i+90]}")

# Show the words found in order
print(f"\n  Words in order:")
for start, word in words_found:
    print(f"    pos {start:3d}: {word}")

# ============================================================
# STRUCTURAL ANALYSIS — What percentage is formula vs unique?
# ============================================================
print(f"\n{'='*100}")
print("TEXT STRUCTURE — Formula vs. unique content")
print("=" * 100)

# The core formula: HEARUCHTIGER...TOTNIURG
core = "HEARUCHTIGER"
for idx, text in enumerate(texts):
    pos = text.find(core)
    if pos == -1:
        status = "NO FORMULA"
    else:
        before = text[:pos]
        after_anchor = text[pos:]
        status = f"formula@{pos:3d}, before={len(before):3d}ch, total={len(text):3d}ch"
    print(f"  Bk{idx:2d}: {status}")

# Books without the formula
no_formula = [(idx, text) for idx, text in enumerate(texts) if anchor not in text]
print(f"\n  Books WITHOUT formula ({len(no_formula)}):")
for idx, text in no_formula:
    print(f"    Bk{idx:2d} ({len(text):3d}ch): {text[:80]}...")

# ============================================================
# MANUAL OPTIMIZED PARSE of the full formula
# ============================================================
print(f"\n{'='*100}")
print("MANUAL PARSE — Best-effort word boundaries for the formula")
print("=" * 100)

# Let me look at Book 9 (longest, 147 pairs) and try to manually parse
bk9_text = texts[9]
print(f"Book 9 ({len(bk9_text)} chars):")
print(f"  {bk9_text}")

# Try different segmentation hypotheses
hypotheses = [
    # Hypothesis 1: Standard German word boundaries
    "RHE LUIRUNN HWND FINDEN TEIG I DAS ES DER STEINE NGE IORT AUNR SON GETRASES RWIE ESCH FACH HECHL EN HIER TAUT RI S TEIL CH AN HEARUCHTIGER CO DASS T UND DIESER T EINER SEINE DE TOTNIURG CE?I LABRR NI WIR UND DIE MINH?DDE MI DIE URALTE STEINEN TEIAD THARSC IST SCHAUN RU III WII SET EIS",

    # Hypothesis 2: Longer words, different breaks
    "R HELUIRUNN HWND FINDEN TEIG IDAS ES DER STEINEN GE IORT AUNR SON GETRASES R WIE ESCH FACHHECHL EN HIER TAUT RIS TEIL CHAN HEARUCHTIGER CODASS TUND DIESER TEINER SEINE DE TOTNIURG CE?I LAB RR NI WIR UND DIE MINH?DDE MIDI E URALTE STEINEN TEIAD THARSC IST SCHAUN RU IIIWII SET EIS",

    # Hypothesis 3: Focus on German compounds
    "R HE LUIRUNN HWND FINDEN TEIGI DAS ES DER STEINEN GE I ORT AUNR SON GETRASES R WIE ESCH FACH HECHL EN HIER TAUT RI STEIL CH AN HEARUCHTIGER CO DASS TUND DIESER TEINER SEINE DE TOTNIURG CE?I LAB RR NI WIR UND DIE MINH?DDE MIDI URALTE STEINEN TEIAD THARSC IST SCHAUN RUIII WII SET EIS",
]

for i, h in enumerate(hypotheses):
    print(f"\n  Hypothesis {i+1}:")
    words = h.split()
    german_words = [w for w in words if w.replace('?', '') in word_dict]
    non_german = [w for w in words if w.replace('?', '') not in word_dict and len(w) > 1]
    print(f"    German words ({len(german_words)}): {', '.join(german_words)}")
    print(f"    Unknown ({len(non_german)}): {', '.join(non_german)}")

# ============================================================
# RAW CODE PAIRS for the formula region — check for misalignment
# ============================================================
print(f"\n{'='*100}")
print("RAW CODE VERIFICATION — Check offset alignment for formula books")
print("=" * 100)

for idx in [0, 5, 9, 10]:
    bpairs = book_pairs[idx]
    text = decode(bpairs)
    pos = text.find(anchor)
    if pos == -1:
        continue
    # Show raw code pairs around anchor
    start = max(0, pos - 10)
    end = min(len(bpairs), pos + len(anchor) + 10)
    raw = ' '.join(bpairs[start:end])
    decoded = decode(bpairs[start:end])
    print(f"  Bk{idx:2d}: codes: {raw}")
    print(f"         text:  {decoded}")
    print(f"         anchor starts at pair {pos}")
