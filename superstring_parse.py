"""Reconstruct the full superstring and attempt word segmentation.
Use the DP parser with an expanded dictionary to maximize coverage."""
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

# Build superstring from overlaps
def decode_book(bpairs):
    return ''.join(all_codes.get(p, '?') for p in bpairs)

texts = [(i, decode_book(bp)) for i, bp in enumerate(book_pairs)]
texts.sort(key=lambda x: -len(x[1]))

# Find overlaps: check if book A's suffix matches book B's prefix
def find_overlap(a, b, min_overlap=8):
    """Find the longest overlap where end of a matches start of b."""
    max_ov = min(len(a), len(b))
    for ov in range(max_ov, min_overlap - 1, -1):
        if a[-ov:] == b[:ov]:
            return ov
    return 0

# Simple greedy assembly
used = set()
superstring_parts = []

# Start with the longest book
current_idx, current_text = texts[0]
used.add(current_idx)

# Extend forward
while True:
    best_ov = 0
    best_idx = -1
    best_text = ''
    for idx, text in texts:
        if idx in used:
            continue
        ov = find_overlap(current_text, text)
        if ov > best_ov:
            best_ov = ov
            best_idx = idx
            best_text = text
    if best_ov >= 8:
        current_text = current_text + best_text[best_ov:]
        used.add(best_idx)
    else:
        break

# Also try extending backward
while True:
    best_ov = 0
    best_idx = -1
    best_text = ''
    for idx, text in texts:
        if idx in used:
            continue
        ov = find_overlap(text, current_text)
        if ov > best_ov:
            best_ov = ov
            best_idx = idx
            best_text = text
    if best_ov >= 8:
        current_text = best_text + current_text[best_ov:]
        used.add(best_idx)
    else:
        break

superstring = current_text

print("=" * 80)
print(f"SUPERSTRING: {len(superstring)} characters from {len(used)} books")
print(f"Unused books: {len(texts) - len(used)}")
print("=" * 80)

# Print the superstring in lines of 80 chars
for i in range(0, len(superstring), 80):
    print(f"{i:4d}: {superstring[i:i+80]}")

# Count unknowns
unknowns_in_ss = superstring.count('?')
print(f"\nUnknown positions: {unknowns_in_ss} ({unknowns_in_ss/len(superstring)*100:.1f}%)")

# ============================================================
# DP WORD SEGMENTATION with expanded dictionary
# ============================================================
print(f"\n{'='*80}")
print("DP WORD SEGMENTATION")
print("=" * 80)

# Expanded dictionary with more German words
word_dict = set([
    # 2-letter
    'AB', 'AM', 'AN', 'DA', 'DU', 'ER', 'ES', 'IM', 'IN', 'JA', 'OB', 'SO',
    'UM', 'WO', 'ZU',
    # 3-letter
    'ALS', 'AUF', 'AUS', 'BEI', 'BIS', 'DAS', 'DEM', 'DEN', 'DER', 'DES',
    'DIE', 'DIR', 'EIN', 'FUR', 'GAB', 'GUT', 'HAT', 'HIN', 'ICH', 'IHM',
    'IHN', 'IST', 'KAM', 'MAN', 'MIT', 'NEU', 'NIE', 'NUN', 'NUR', 'ORT',
    'SAH', 'SIE', 'TAG', 'TOD', 'UND', 'VOM', 'VON', 'VOR', 'WAR', 'WAS',
    'WER', 'WIE', 'WIR', 'ZUM', 'ZUR',
    # 4-letter
    'ABER', 'ALLE', 'ALSO', 'AUCH', 'BERG', 'BURG', 'DACH', 'DANN', 'DASS',
    'DEIN', 'DENN', 'DIES', 'DOCH', 'DORT', 'DREI', 'EINE', 'ENDE', 'ERDE',
    'ERST', 'FAND', 'FORT', 'GANZ', 'GEBE', 'GELD', 'GING', 'GOLD', 'GOTT',
    'HALB', 'HAND', 'HAUS', 'HELD', 'HERR', 'HIER', 'HOCH', 'JEDE', 'JENE',
    'KAUM', 'KEIN', 'KERN', 'LAND', 'LANG', 'MEHR', 'MEIN', 'MUSS', 'NACH',
    'NAME', 'NOCH', 'OHNE', 'ORTE', 'RUNE', 'SAGT', 'SANG', 'SATZ', 'SEHR',
    'SEIN', 'SICH', 'SIND', 'SOHN', 'TEIL', 'TIEF', 'TURM', 'VIEL', 'VOLK',
    'WEIL', 'WEIT', 'WELT', 'WENN', 'WERT', 'WORT', 'ZAHL', 'ZEIT', 'ZWEI',
    # 5-letter
    'ALLES', 'ALTEN', 'ANDRE', 'BEIDE', 'BERGE', 'BOTEN', 'BUERG', 'DAHER',
    'DERER', 'DIESE', 'DURCH', 'EIGEN', 'EINEN', 'EINER', 'EINEM', 'EINES',
    'ERSTE', 'ETWAS', 'EUREN', 'EWIGE', 'GEGEN', 'GEHEN', 'GEIST', 'GEBEN',
    'GROSS', 'HABEN', 'JEDER', 'JEDES', 'JEDEM', 'JENEN', 'KEINE', 'KENNT',
    'KRAFT', 'LANGE', 'LEBEN', 'LICHT', 'MACHT', 'NACHT', 'NEBEN', 'NICHT',
    'ORTEN', 'RUNEN', 'SAGEN', 'SAGTE', 'SEHEN', 'SEINE', 'STEHT', 'STEIN',
    'TAGEN', 'TEILE', 'TEILT', 'TRITT', 'UNTER', 'VIELE', 'WAGEN', 'WEDER',
    'WERDE', 'WESEN', 'IMMER', 'SUCHE',
    # 6-letter
    'ANDERE', 'BEIDER', 'DIESER', 'DIESES', 'DIESEM', 'DIESEN', 'DUNKEL',
    'EIGENE', 'ERSTEN', 'ERSTER', 'EWIGEN', 'FINDEN', 'FRAGEN', 'GANZEM',
    'GRENZE', 'GROSSE', 'GRUPPE', 'HELFEN', 'HIMMEL', 'KOENIG', 'KOMMEN',
    'KONNTE', 'LANGEN', 'MACHEN', 'NICHTS', 'NORDEN', 'SEINES', 'SEINER',
    'SEINEM', 'SEINEN', 'STEINE', 'SUEDEN', 'TEMPEL', 'URALTE', 'VOELKE',
    'WIEDER', 'WISSEN', 'WOLLTE', 'ZEIGEN', 'ZEITEN',
    # 7-letter
    'ANDEREN', 'ANFANGS', 'EIGENEN', 'FLIEHEN', 'GROSSEN', 'LETZTEN',
    'STEINEN', 'STIMMEN', 'URALTEN', 'WAHREND', 'WOLLTEN',
    # 8+ letter
    'MENSCHEN', 'VERSCHIEDENE', 'ZUSAMMEN', 'WAHRHEIT',
    # Tibia-specific proper nouns (treated as words for segmentation)
    'LABGZERAS', 'TOTNIURG', 'RUNEORT', 'HEARUCHTIGER',
    # Prefix/suffix patterns that help segmentation
    'KEINE', 'KEINEN', 'KEINEM', 'KEINER', 'KEINES',
])

# DP parse
n = len(superstring)
# dp[i] = (max_covered, previous_index, word_or_None)
dp = [(0, -1, None)] * (n + 1)

for i in range(1, n + 1):
    # Option 1: this char is uncovered
    dp[i] = (dp[i-1][0], i-1, None)
    # Option 2: a word ends here
    for wlen in range(2, min(20, i + 1)):
        start = i - wlen
        candidate = superstring[start:i]
        if candidate in word_dict:
            new_covered = dp[start][0] + wlen
            if new_covered > dp[i][0]:
                dp[i] = (new_covered, start, candidate)

# Traceback
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
print(f"Coverage: {total_covered}/{n} = {total_covered/n*100:.1f}%")
print(f"Words found: {len(words_found)}")

# Show the segmented text
print(f"\nSegmented superstring:")
# Mark which positions are covered
covered = [False] * n
for start, word in words_found:
    for j in range(start, start + len(word)):
        covered[j] = True

# Build annotated text
result = []
i = 0
while i < n:
    if covered[i]:
        # Find the word starting here
        for start, word in words_found:
            if start == i:
                result.append(f'[{word}]')
                i += len(word)
                break
        else:
            result.append(superstring[i])
            i += 1
    else:
        result.append(superstring[i].lower())
        i += 1

annotated = ''.join(result)

# Print in lines of 100
for i in range(0, len(annotated), 100):
    print(annotated[i:i+100])

# Count word frequencies
word_freq = Counter(w for _, w in words_found)
print(f"\nTop 30 words:")
for w, cnt in word_freq.most_common(30):
    print(f"  {w}: {cnt}")

# ============================================================
# IDENTIFY CODE 02 pattern: always after V (code 83)
# ============================================================
print(f"\n{'='*80}")
print("CODE 02 ANALYSIS: Always preceded by V")
print("=" * 80)

# What follows V in the text?
v_followers = Counter()
for bpairs in book_pairs:
    for i in range(len(bpairs) - 1):
        if bpairs[i] == '83':  # V
            nxt = all_codes.get(bpairs[i+1], f'[{bpairs[i+1]}]')
            v_followers[nxt] += 1

print(f"V followed by: {', '.join(f'{l}:{c}' for l, c in v_followers.most_common())}")
print(f"Total V: {sum(v_followers.values())}")

# In German, V is most commonly followed by:
# O (von, vor, voll, vom) — 43% of V-bigrams
# E (ver-, verschiedene) — 35%
# I (viel, vier) — 15%
# OE (voelker) — rare

# If 02 is one of these, what words form?
for letter in ['O', 'E', 'I', 'A']:
    test = {**all_codes, '02': letter}
    print(f"\n  02={letter}:")
    for idx, bpairs in enumerate(book_pairs):
        for j, p in enumerate(bpairs):
            if p != '02':
                continue
            start = max(0, j - 8)
            end = min(len(bpairs), j + 9)
            text = ''.join(test.get(bpairs[k], '?') for k in range(start, end))
            pos = j - start
            hl = text[:pos] + '[' + text[pos] + ']' + text[pos+1:]
            print(f"    Bk{idx:2d}: {hl}")
