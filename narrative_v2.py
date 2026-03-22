"""Comprehensive narrative reconstruction attempt.
Use ALL fragments (not just the main one) and an expanded dictionary
with archaic German, Middle High German forms, and Tibia-specific terms."""
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

# Massive German dictionary including archaic forms
word_dict = set([
    # 2-letter (all common)
    'AB', 'AM', 'AN', 'DA', 'DU', 'ER', 'ES', 'IM', 'IN', 'JA', 'OB', 'SO',
    'UM', 'WO', 'ZU', 'EI', 'OD', 'OE', 'UE',
    # 3-letter
    'ALS', 'ALT', 'AUF', 'AUS', 'BAT', 'BEI', 'BIS', 'DAM', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DIR', 'EIN', 'FUR', 'GAB', 'GAR', 'GUT',
    'HAT', 'HER', 'HIN', 'ICH', 'IHM', 'IHN', 'IHR', 'IST', 'KAM', 'LOS',
    'MAN', 'MIR', 'MIT', 'NEU', 'NIE', 'NUN', 'NUR', 'ORT', 'RAT', 'RUF',
    'SAH', 'SEI', 'SIE', 'TAG', 'TAT', 'TOD', 'TOR', 'TOT', 'TUN', 'UND',
    'UNS', 'VOM', 'VON', 'VOR', 'WAR', 'WAS', 'WEG', 'WEM', 'WEN', 'WER',
    'WIE', 'WIR', 'WOL', 'ZUM', 'ZUR',
    # 4-letter
    'ABER', 'ALLE', 'ALSO', 'AUCH', 'BERG', 'BIST', 'BLIEB', 'BURG', 'DACH',
    'DANK', 'DANN', 'DASS', 'DEIN', 'DENN', 'DIES', 'DOCH', 'DORT', 'DREI',
    'EDEL', 'EDLE', 'EGAL', 'EINE', 'ENDE', 'ENGE', 'ERDE', 'ERST', 'EUCH',
    'EUER', 'EURE', 'FACH', 'FAND', 'FERN', 'FEST', 'FORT', 'GANZ', 'GEBE',
    'GEHE', 'GEHT', 'GELD', 'GILT', 'GING', 'GLAS', 'GOLD', 'GOTT', 'GROS',
    'GROB', 'HALB', 'HALT', 'HAND', 'HAUS', 'HEER', 'HEIL', 'HEIM', 'HELD',
    'HERR', 'HERZ', 'HIER', 'HOCH', 'IRGD', 'JEDE', 'JENE', 'KAUM', 'KEIN',
    'KERN', 'KLAR', 'LAND', 'LANG', 'LAUT', 'LEER', 'LEID', 'LESE', 'LIST',
    'LUFT', 'MAHL', 'MEHR', 'MEIN', 'MILD', 'MUSS', 'NACH', 'NAHE', 'NAME',
    'NEIN', 'NOCH', 'ODER', 'OHNE', 'ORTE', 'REDE', 'REST', 'RIEF', 'RUHE',
    'RUNE', 'SAGT', 'SANG', 'SEHE', 'SEHR', 'SEIN', 'SEIT', 'SICH', 'SIND',
    'SINN', 'SOHN', 'SUCH', 'TAGE', 'TATEN', 'TEIL', 'TIEF', 'TRUG', 'TURM',
    'VIEL', 'VOLK', 'WAHR', 'WAND', 'WEIL', 'WEIT', 'WELT', 'WENN', 'WERT',
    'WOHL', 'WORT', 'WUND', 'ZAHL', 'ZEIG', 'ZEIT', 'ZORN', 'ZWEI',
    'STEH', 'GEBE', 'SEHE', 'LESE', 'NENN', 'BIET', 'HAELT', 'FIND',
    # 5-letter
    'ALLES', 'ALTER', 'ALTEN', 'ALTEM', 'BEIDE', 'BERGE', 'BOTEN', 'DAHER',
    'DENEN', 'DERER', 'DIESE', 'DURCH', 'EIGEN', 'EINEN', 'EINER', 'EINEM',
    'EINES', 'ENDET', 'ERSTE', 'ETWAS', 'EUREN', 'EWIGE', 'GANZE', 'GEGEN',
    'GEHEN', 'GEIST', 'GEBEN', 'GIESS', 'GLANZ', 'GROSS', 'HABEN', 'HEISS',
    'JEDER', 'JEDES', 'JEDEM', 'JENEN', 'KEINE', 'KENNT', 'KRAFT', 'LANDE',
    'LANGE', 'LAUFE', 'LEBEN', 'LICHT', 'MACHT', 'NACHT', 'NEBEN', 'NICHT',
    'ORTEN', 'OSTEN', 'RECHT', 'REICH', 'RUNEN', 'SAGEN', 'SAGTE', 'SEHEN',
    'SEINE', 'SINNE', 'STEIL', 'STEHT', 'STEIN', 'SUCHE', 'SUCHT', 'TAGEN',
    'TEILE', 'TEILS', 'TRITT', 'UNTER', 'VIELE', 'WAGEN', 'WEDER', 'WELCH',
    'WERDE', 'WESEN', 'IMMER', 'SEITE', 'SEIEN', 'KLARE', 'GRUND', 'HUNDE',
    'EDLEN', 'GEBET', 'STEHE', 'GUTES', 'ALTEM', 'NEUEN', 'NEUER', 'NEUES',
    'GENUG', 'STARK', 'UNSER', 'UNTEN', 'OFFEN', 'GEIST', 'LUGEN',
    'ZEIGT', 'STEIG', 'STEHN', 'GEHEN', 'STEHEN',
    # 6-letter
    'ANDERE', 'BEIDER', 'DIESER', 'DIESES', 'DIESEM', 'DIESEN', 'DUNKEL',
    'EIGENE', 'ERSTEN', 'ERSTER', 'EWIGEN', 'FINDEN', 'FINDET', 'FRAGEN',
    'GEHEIM', 'GRENZE', 'GROSSE', 'GRUPPE', 'HELFEN', 'HIMMEL', 'KOENIG',
    'KOMMEN', 'KONNTE', 'LANGEN', 'MACHEN', 'NICHTS', 'NORDEN', 'SEINES',
    'SEINER', 'SEINEM', 'SEINEN', 'STEINE', 'SUEDEN', 'TEMPEL', 'URALTE',
    'VOELKE', 'WIEDER', 'WISSEN', 'WOLLTE', 'ZEIGEN', 'ZEITEN', 'WAENDE',
    'ANDERE', 'ANFANG', 'DIENEN', 'EBENSO', 'EIGNER', 'GEHEIM', 'WESTEN',
    'SCHAUN', 'DUNKLE', 'GANZEN', 'HEILIG', 'REISEN',
    # 7-letter
    'ANDEREN', 'ANFANGS', 'EIGENEN', 'FLIEHEN', 'GROSSEN', 'GROSSER',
    'LETZTEN', 'STEINEN', 'STIMMEN', 'URALTEN', 'WAHREND', 'WOLLTEN',
    'HEILIGE', 'GEISTER', 'KRIEGER', 'MEISTER',
    # 8+ letter
    'MENSCHEN', 'VERSCHIEDENE', 'ZUSAMMEN', 'WAHRHEIT',
    'HEILIGEN', 'GEHEIMNIS', 'GEWALTIGER',
    # Proper nouns (Tibia-specific — treated as dictionary words for parsing)
    'LABGZERAS', 'TOTNIURG', 'HEARUCHTIGER', 'THARSC', 'MINH',
    'AUNRSONGETRASES', 'LUIRUNNHWND', 'TUIGAA',
    # Multi-word patterns that commonly appear
    'RUNENORT', 'RUNEORT',
])

def dp_parse(text, dictionary):
    n = len(text)
    dp = [(0, -1, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], i-1, None)
        for wlen in range(2, min(20, i + 1)):
            start = i - wlen
            candidate = text[start:i]
            if '?' not in candidate and candidate in dictionary:
                new_covered = dp[start][0] + wlen
                if new_covered > dp[i][0]:
                    dp[i] = (new_covered, start, candidate)
    words = []
    pos = n
    while pos > 0:
        _, prev, word = dp[pos]
        if word:
            words.append((prev, word))
            pos = prev
        else:
            pos = prev
    words.reverse()
    return dp[n][0], words

def annotate_spaced(text, words_found):
    """Build text with spaces between words, lowercase for uncovered."""
    n = len(text)
    covered = [False] * n
    word_starts = {}
    for start, word in words_found:
        word_starts[start] = word
        for j in range(start, start + len(word)):
            covered[j] = True
    result = []
    i = 0
    while i < n:
        if i in word_starts:
            word = word_starts[i]
            result.append(f' {word} ')
            i += len(word)
        elif covered[i]:
            result.append(text[i])
            i += 1
        else:
            result.append(text[i].lower())
            i += 1
    out = ''.join(result)
    while '  ' in out:
        out = out.replace('  ', ' ')
    return out.strip()

# ============================================================
# DECODE AND PARSE EACH BOOK INDIVIDUALLY
# ============================================================
print("=" * 100)
print("INDIVIDUAL BOOK NARRATIVES — best-effort German reading")
print("=" * 100)

results = []
for idx, bpairs in enumerate(book_pairs):
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    if len(text) < 15:
        continue
    cov, words = dp_parse(text, word_dict)
    pct = cov / len(text) * 100
    ann = annotate_spaced(text, words)
    results.append((idx, len(text), pct, ann, words))

# Sort by coverage descending
results.sort(key=lambda x: -x[2])

# Show top 15 by coverage
print("\nTOP 15 BOOKS BY WORD COVERAGE:")
for idx, length, pct, ann, words in results[:15]:
    print(f"\n  Bk{idx:2d} ({length:3d}ch, {pct:.0f}%):")
    # Print annotated in lines of 90
    for i in range(0, len(ann), 90):
        print(f"    {ann[i:i+90]}")

# ============================================================
# FULL SUPERSTRING NARRATIVE — assemble decoded books into order
# ============================================================
print(f"\n{'='*100}")
print("FULL NARRATIVE ATTEMPT — assembled from all books")
print("=" * 100)

# Get all decoded texts
all_texts = []
for bpairs in book_pairs:
    all_texts.append(''.join(all_codes.get(p, '?') for p in bpairs))

# Remove exact substrings
unique = []
sorted_texts = sorted(enumerate(all_texts), key=lambda x: -len(x[1]))
for idx, text in sorted_texts:
    is_sub = False
    for _, utext in unique:
        if text in utext:
            is_sub = True
            break
    if not is_sub:
        unique.append((idx, text))

# Greedy assembly
frags = [text for _, text in unique]
while True:
    best_ov = 0
    best_i = -1
    best_j = -1
    for i in range(len(frags)):
        for j in range(len(frags)):
            if i == j:
                continue
            ti = frags[i]
            tj = frags[j]
            max_ov = min(len(ti), len(tj))
            for ov in range(max_ov, 5, -1):
                if ti[-ov:] == tj[:ov]:
                    if ov > best_ov:
                        best_ov = ov
                        best_i = i
                        best_j = j
                    break
    if best_ov <= 5:
        break
    merged = frags[best_i] + frags[best_j][best_ov:]
    frags[best_i] = merged
    frags.pop(best_j)

frags.sort(key=lambda x: -len(x))

# Parse all fragments
total_chars = sum(len(f) for f in frags)
total_cov = 0
print(f"\n  Total fragments: {len(frags)}, total chars: {total_chars}")

for fi, frag in enumerate(frags[:10]):  # Top 10 fragments
    cov, words = dp_parse(frag, word_dict)
    pct = cov / len(frag) * 100
    total_cov += cov
    ann = annotate_spaced(frag, words)

    print(f"\n  --- Fragment {fi} ({len(frag)} chars, {pct:.0f}% coverage) ---")
    for i in range(0, len(ann), 100):
        print(f"    {ann[i:i+100]}")

# ============================================================
# OVERALL STATISTICS
# ============================================================
print(f"\n{'='*100}")
print("OVERALL STATISTICS")
print("=" * 100)

# Parse ALL fragments
total_chars_all = 0
total_cov_all = 0
all_words = Counter()
for frag in frags:
    cov, words = dp_parse(frag, word_dict)
    total_chars_all += len(frag)
    total_cov_all += cov
    for _, w in words:
        all_words[w] += 1

print(f"  Total decoded characters: {total_chars_all}")
print(f"  Total recognized characters: {total_cov_all}")
print(f"  Overall coverage: {total_cov_all/total_chars_all*100:.1f}%")
print(f"  Unique words: {len(all_words)}")
print(f"\n  Word frequency (all fragments):")
for w, c in all_words.most_common(40):
    tag = ""
    if w in ['LABGZERAS', 'TOTNIURG', 'HEARUCHTIGER', 'THARSC', 'MINH',
             'AUNRSONGETRASES', 'LUIRUNNHWND', 'TUIGAA']:
        tag = " [proper noun]"
    elif w in ['SCHAUN']:
        tag = " [dialectal: schauen=to look]"
    print(f"    {w:20s}: {c:3d}{tag}")

# ============================================================
# LETTER FREQUENCY of the FINAL decoded text
# ============================================================
print(f"\n{'='*100}")
print("LETTER FREQUENCY — final decoded text vs German expected")
print("=" * 100)

all_decoded = ''.join(frags)
letter_freq = Counter(c for c in all_decoded if c != '?')
total_letters = sum(letter_freq.values())

german_expected = {
    'E': 16.93, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
    'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
    'L': 3.44, 'C': 2.73, 'G': 3.01, 'M': 2.53, 'O': 2.51,
    'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
    'V': 0.84,
}

print(f"  {'Letter':8s} {'Count':6s} {'Actual%':8s} {'Expected%':10s} {'Diff':6s}")
for letter in sorted(german_expected.keys(), key=lambda l: -german_expected[l]):
    count = letter_freq.get(letter, 0)
    actual = count / total_letters * 100
    expected = german_expected[letter]
    diff = actual - expected
    flag = " <--" if abs(diff) > 2.0 else ""
    print(f"  {letter:8s} {count:6d} {actual:7.2f}% {expected:9.2f}% {diff:+5.2f}{flag}")
