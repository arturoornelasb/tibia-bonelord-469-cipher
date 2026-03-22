"""Comprehensive superstring reconstruction and word analysis.
Key insight: all 70 books are fragments of ONE continuous text.
Test code 16 as I vs O, and attempt full narrative parse."""
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

base_codes = {
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

# Big German dictionary
word_dict = set([
    'AB', 'AM', 'AN', 'DA', 'DU', 'ER', 'ES', 'IM', 'IN', 'JA', 'OB', 'SO',
    'UM', 'WO', 'ZU',
    'ALS', 'AUF', 'AUS', 'BEI', 'BIS', 'DAS', 'DEM', 'DEN', 'DER', 'DES',
    'DIE', 'DIR', 'EIN', 'FUR', 'GAB', 'GUT', 'HAT', 'HIN', 'ICH', 'IHM',
    'IHN', 'IST', 'KAM', 'MAN', 'MIT', 'NEU', 'NIE', 'NUN', 'NUR', 'ORT',
    'RAT', 'SAH', 'SEI', 'SIE', 'TAG', 'TAT', 'TOD', 'TUN', 'UND', 'VOM',
    'VON', 'VOR', 'WAR', 'WAS', 'WEG', 'WER', 'WIE', 'WIR', 'ZUM', 'ZUR',
    'RUF', 'RUH', 'TOR', 'TOT',
    'ABER', 'ALLE', 'ALSO', 'AUCH', 'BERG', 'BURG', 'DACH', 'DANN', 'DASS',
    'DEIN', 'DENN', 'DIES', 'DOCH', 'DORT', 'DREI', 'EINE', 'ENDE', 'ERDE',
    'ERST', 'EUCH', 'FAND', 'FEST', 'FORT', 'GANZ', 'GEBE', 'GELD', 'GING',
    'GOLD', 'GOTT', 'HALB', 'HAND', 'HAUS', 'HEIL', 'HELD', 'HERR', 'HIER',
    'HOCH', 'JEDE', 'JENE', 'KAUM', 'KEIN', 'KERN', 'LAND', 'LANG', 'LEER',
    'MEHR', 'MEIN', 'MUSS', 'NACH', 'NAHE', 'NAME', 'NOCH', 'ODER', 'OHNE',
    'ORTE', 'RIEF', 'RUNE', 'SAGT', 'SANG', 'SATZ', 'SEHR', 'SEIN', 'SICH',
    'SIND', 'SOHN', 'STAT', 'TEIL', 'TIEF', 'TRUG', 'TURM', 'VIEL', 'VOLK',
    'WEIL', 'WEIT', 'WELT', 'WENN', 'WERT', 'WORT', 'WOHL', 'ZAHL', 'ZEIT',
    'ZWEI', 'ACHT', 'DRAN', 'DRUM', 'EDEL', 'FACH', 'FERN', 'FEST', 'HEIM',
    'HEER', 'HERZ', 'IRGEND', 'KLAR', 'LAUT', 'LEID', 'LIST', 'LUFT',
    'MUTIG', 'NEIN', 'REDE', 'RECHT', 'RUHE', 'SINN', 'SPUR', 'STEIL',
    'TAGE', 'TATEN', 'TIEF', 'WAND', 'WOHL', 'WUND', 'ZEIG',
    'ALLES', 'ALTER', 'ALTEN', 'ALTEM', 'ANDRE', 'BEIDE', 'BERGE', 'BOTEN',
    'BUERG', 'DAHER', 'DENEN', 'DERER', 'DIESE', 'DURCH', 'EIGEN', 'EINEN',
    'EINER', 'EINEM', 'EINES', 'ERSTE', 'ETWAS', 'EUREN', 'EWIGE', 'GANZE',
    'GEGEN', 'GEHEN', 'GEIST', 'GEBEN', 'GIESS', 'GLANZ', 'GROSS', 'HABEN',
    'HEISS', 'JEDER', 'JEDES', 'JEDEM', 'JENEN', 'KEINE', 'KENNT', 'KRAFT',
    'LANDE', 'LANGE', 'LAUFE', 'LEBEN', 'LICHT', 'MACHT', 'NACHT', 'NEBEN',
    'NICHT', 'ORTEN', 'RUNEN', 'SAGEN', 'SAGTE', 'SEHEN', 'SEINE', 'STEHT',
    'STEIN', 'TAGEN', 'TEILE', 'TEILS', 'TRITT', 'UNTER', 'VIELE', 'WAGEN',
    'WEDER', 'WELCH', 'WERDE', 'WESEN', 'IMMER', 'SUCHE', 'STEIL', 'EDLEN',
    'KLARE', 'STEHE', 'SUCHT', 'WUEST', 'SEITE', 'SEIEN', 'SINNE',
    'ANDERE', 'BEIDER', 'DIESER', 'DIESES', 'DIESEM', 'DIESEN', 'DUNKEL',
    'EIGENE', 'ERSTEN', 'ERSTER', 'EWIGEN', 'FINDEN', 'FRAGEN', 'GANZEM',
    'GEHEIM', 'GRENZE', 'GROSSE', 'GRUPPE', 'HELFEN', 'HIMMEL', 'KOENIG',
    'KOMMEN', 'KONNTE', 'LANGEN', 'MACHEN', 'NICHTS', 'NORDEN', 'SEINES',
    'SEINER', 'SEINEM', 'SEINEN', 'STEINE', 'SUEDEN', 'TEMPEL', 'URALTE',
    'VOELKE', 'WIEDER', 'WISSEN', 'WOLLTE', 'ZEIGEN', 'ZEITEN', 'WAENDE',
    'ANDERE', 'ANFANG', 'DIENEN', 'EBENSO', 'EIGNER', 'GEHEIM',
    'ANDEREN', 'ANFANGS', 'EIGENEN', 'FLIEHEN', 'GROSSEN', 'GROSSER',
    'LETZTEN', 'STEINEN', 'STIMMEN', 'URALTEN', 'WAHREND', 'WOLLTEN',
    'GROESSER', 'MENSCHEN', 'VERSCHIEDENE', 'ZUSAMMEN', 'WAHRHEIT',
    # Proper nouns
    'LABGZERAS', 'TOTNIURG', 'HEARUCHTIGER',
    # Common verb forms
    'GIBT', 'GEHT', 'SIEHT', 'STEHT', 'TRAEGT', 'WIRD', 'SAGT',
    'WURDEN', 'HATTEN', 'WAREN', 'SOLLTE', 'SOLLTEN', 'WOLLTE',
    'FINDEN', 'STEHEN', 'LIEGEN', 'KOENNEN', 'MUESSEN',
    'LIESS', 'NAHM', 'TRAT', 'SPRACH', 'SAGTE', 'FRAGTE',
    # More adjective/noun forms
    'HEILIG', 'HEILIGE', 'HEILIGEN',
    'MAECHTIG', 'MAECHTIGER', 'MAECHTIGEN',
    'GEWALTIG', 'GEWALTIGER',
    'WICHTIG', 'WICHTIGER',
    'EINSAM', 'EINZIG',
    'GERECHT', 'GERECHTER',
    'SCHATTEN', 'DUNKELHEIT',
    'DUNKLEN', 'DUNKLER',
    'REISEN', 'WANDERN', 'SUCHEN',
    'FINDET', 'STEHET', 'LIEGET',
    'OSTEN', 'WESTEN', 'SUEDEN', 'NORDEN',
    # Archaic/Middle High German forms that Tibia might use
    'RUNE', 'RUNEN', 'RUNENORT',
    'MEISTER', 'KRIEGER', 'KAISER',
    'WAECHTER', 'HUETER',
    'SCHRIFT', 'ZEICHEN',
    'GEHEIMNIS',
    # Additional common words
    'ODER', 'WEDER', 'WERDE', 'WERDEN',
    'TAGE', 'TAGES', 'NACHT', 'NACHTS',
    'STEIN', 'STEINE', 'STEINEN',
    'ORTEN', 'ORTES',
    'RUNE', 'RUNEN',
    'TEIL', 'TEILE', 'TEILEN', 'TEILS',
    'ENDE', 'ENDEN', 'ENDES',
    'UEBER',
    'EUER', 'EURE', 'EURES',
    'UNSER', 'UNSERE',
    'JENER', 'JENES', 'JENEM',
])

def dp_parse(text, dictionary):
    """DP word segmentation. Returns (coverage, words_found)."""
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
    # Traceback
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

def annotate(text, words_found):
    """Build annotated text with [WORD] for found words, lowercase for uncovered."""
    n = len(text)
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
                result.append(text[i])
                i += 1
        else:
            result.append(text[i].lower())
            i += 1
    out = ''.join(result)
    while '  ' in out:
        out = out.replace('  ', ' ')
    return out.strip()

# Get book pairs
book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# ============================================================
# TEST: Code 16 = I vs O
# ============================================================
print("=" * 100)
print("CODE 16 TEST: I vs O — effect on word coverage")
print("=" * 100)

for test_letter in ['I', 'O']:
    codes = dict(base_codes)
    codes['16'] = test_letter

    # Decode all books and concatenate (without overlap removal)
    all_text = []
    for bpairs in book_pairs:
        text = ''.join(codes.get(p, '?') for p in bpairs)
        all_text.append(text)

    # Test on full concatenation
    full = ''.join(all_text)
    total_cov, total_words = dp_parse(full, word_dict)

    # Count specific word hits that differ
    word_counter = Counter()
    for _, w in total_words:
        word_counter[w] += 1

    print(f"\n  16={test_letter}: coverage={total_cov}/{len(full)} = {total_cov/len(full)*100:.1f}%")
    print(f"         words found: {len(total_words)}")
    print(f"         top 20: {', '.join(f'{w}:{c}' for w, c in word_counter.most_common(20))}")

# ============================================================
# BUILD PROPER SUPERSTRING at decoded level
# ============================================================
print(f"\n{'='*100}")
print("SUPERSTRING RECONSTRUCTION — decoded level, greedy overlap assembly")
print("=" * 100)

codes = dict(base_codes)  # Use 16=I (default)

texts = []
for bpairs in book_pairs:
    text = ''.join(codes.get(p, '?') for p in bpairs)
    texts.append(text)

# Remove exact duplicates and substrings
unique_texts = []
sorted_by_len = sorted(enumerate(texts), key=lambda x: -len(x[1]))

for idx, text in sorted_by_len:
    is_sub = False
    for uidx, utext in unique_texts:
        if text in utext:
            is_sub = True
            break
    if not is_sub:
        unique_texts.append((idx, text))

print(f"  Total books: {len(texts)}")
print(f"  Unique (non-substring): {len(unique_texts)}")

# Greedy assembly
frags = [text for _, text in unique_texts]
frag_ids = [idx for idx, _ in unique_texts]

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

# Sort fragments by length
frags.sort(key=lambda x: -len(x))

print(f"  Fragments after assembly: {len(frags)}")
for i, frag in enumerate(frags):
    print(f"    Fragment {i}: {len(frag)} chars, unknowns={frag.count('?')}")

# The main fragment should be most of the text
main = frags[0]
print(f"\n  MAIN FRAGMENT: {len(main)} chars")

# Print the full main fragment
for i in range(0, len(main), 80):
    print(f"    {i:4d}: {main[i:i+80]}")

# DP parse of main fragment
total_cov, words_found = dp_parse(main, word_dict)
print(f"\n  Coverage: {total_cov}/{len(main)} = {total_cov/len(main)*100:.1f}%")

ann = annotate(main, words_found)
print(f"\n  Annotated text:")
for i in range(0, len(ann), 100):
    print(f"    {ann[i:i+100]}")

# ============================================================
# WORD FREQUENCY in the superstring
# ============================================================
word_freq = Counter(w for _, w in words_found)
print(f"\n  All words ({len(word_freq)} unique):")
for w, cnt in word_freq.most_common():
    print(f"    {w}: {cnt}")

# ============================================================
# UNRECOGNIZED SEGMENTS — what resists parsing?
# ============================================================
print(f"\n{'='*100}")
print("UNRECOGNIZED SEGMENTS — strings that resist word parsing")
print("=" * 100)

covered = [False] * len(main)
for start, word in words_found:
    for j in range(start, start + len(word)):
        covered[j] = True

# Find contiguous uncovered segments
uncovered_segs = []
i = 0
while i < len(main):
    if not covered[i]:
        start = i
        while i < len(main) and not covered[i]:
            i += 1
        seg = main[start:i]
        uncovered_segs.append((start, seg))
    else:
        i += 1

# Sort by length
uncovered_segs.sort(key=lambda x: -len(x[1]))
print(f"  Total uncovered segments: {len(uncovered_segs)}")
print(f"  Total uncovered chars: {sum(len(s) for _, s in uncovered_segs)}")
print(f"\n  Longest uncovered segments:")
for pos, seg in uncovered_segs[:30]:
    # Show context
    ctx_start = max(0, pos - 5)
    ctx_end = min(len(main), pos + len(seg) + 5)
    before = main[ctx_start:pos]
    after = main[pos+len(seg):ctx_end]
    print(f"    pos {pos:4d} ({len(seg):2d}ch): {before}[{seg}]{after}")
