"""
Deep narrative analysis: decode the full text with best mapping,
manually try to insert word boundaries, and extract the narrative.
"""
import json
import os
from collections import Counter

data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

# Best mapping: Tier 14 + 05=S + 74=E
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
    '74': 'E',  # Best bigram match
}

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

# Build the full superstring from raw digits
def find_overlap(a, b, min_len=4):
    max_overlap = min(len(a), len(b))
    for length in range(max_overlap, min_len - 1, -1):
        if length % 2 != 0:
            continue
        if a[-length:] == b[:length]:
            return length
    return 0

# Remove contained books
n = len(books)
contained = set()
for i in range(n):
    for j in range(n):
        if i != j and books[i] in books[j]:
            contained.add(i)

unique_idx = [i for i in range(n) if i not in contained]
unique = [books[i] for i in unique_idx]

# Greedy assembly
used = [False] * len(unique)
fragments = []
while True:
    unused = [i for i in range(len(unique)) if not used[i]]
    if not unused:
        break
    start = max(unused, key=lambda i: len(unique[i]))
    current = unique[start]
    used[start] = True
    changed = True
    while changed:
        changed = False
        best_ov, best_idx, best_dir = 0, -1, None
        for i in [x for x in range(len(unique)) if not used[x]]:
            ov_r = find_overlap(current, unique[i])
            ov_l = find_overlap(unique[i], current)
            if ov_r > best_ov:
                best_ov, best_idx, best_dir = ov_r, i, 'right'
            if ov_l > best_ov:
                best_ov, best_idx, best_dir = ov_l, i, 'left'
        if best_idx >= 0 and best_ov >= 4:
            if best_dir == 'right':
                current = current + unique[best_idx][best_ov:]
            else:
                current = unique[best_idx] + current[best_ov:]
            used[best_idx] = True
            changed = True
    fragments.append(current)

fragments.sort(key=len, reverse=True)

# Decode each fragment and show with code-level detail
print("=" * 80)
print("FULL NARRATIVE DECODE")
print("=" * 80)

# Track all unknown codes that remain
remaining_unknowns = Counter()

for fi, frag in enumerate(fragments[:10]):  # Show top 10 fragments
    offset = get_offset(frag)
    pairs = [frag[j:j+2] for j in range(offset, len(frag)-1, 2)]

    decoded = ''
    for p in pairs:
        letter = mapping.get(p)
        if letter:
            decoded += letter
        else:
            decoded += f'[{p}]'
            remaining_unknowns[p] += 1

    print(f"\n{'='*60}")
    print(f"FRAGMENT {fi}: {len(decoded)} chars ({len(pairs)} pairs)")
    print(f"{'='*60}")

    # Print decoded text
    print(f"\nRaw decoded:")
    for start in range(0, len(decoded), 70):
        print(f"  {decoded[start:start+70]}")

    # Try to manually segment into words using pattern matching
    # Use a greedy approach with a large word list
    words = set([
        # 2-letter
        'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO', 'DU', 'OB', 'AM', 'IM',
        'EH', 'AB', 'NU',
        # 3-letter
        'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST', 'WIR', 'ICH', 'SIE',
        'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT', 'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI',
        'VOR', 'TAG', 'ORT', 'TOD', 'OFT', 'NIE', 'ALT', 'NEU', 'VOM', 'ZUM', 'ZUR', 'BIS',
        'ALS', 'NUN', 'HIN', 'TUN', 'TUT', 'SAH', 'GAB', 'KAM', 'WAR', 'SEI', 'RUF', 'RAT',
        'TAT', 'MIR', 'IHR', 'DIR', 'UNS', 'WEG', 'RUH', 'GEH', 'SAG', 'VER', 'GIB',
        # 4-letter
        'NACH', 'AUCH', 'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN', 'DASS', 'WENN', 'DANN',
        'DENN', 'ABER', 'ODER', 'WEIL', 'EINE', 'DIES', 'HIER', 'DORT', 'WELT', 'ZEIT',
        'TEIL', 'WORT', 'NAME', 'GANZ', 'SEHR', 'VIEL', 'FORT', 'HOCH', 'ERDE', 'GOTT',
        'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN', 'HELD', 'ZWEI', 'DREI', 'VIER', 'MEHR',
        'LAND', 'FEST', 'REDE', 'TAGE', 'FREI', 'WAHR', 'VOLK', 'WALD', 'GRAB', 'RUNE',
        'ENDE', 'HAUS', 'NAHM', 'GING', 'LANG', 'KEIN', 'OHNE', 'ALLE', 'WARD', 'BALD',
        'LAUT', 'ERST', 'MUSS', 'WILL', 'SOLL', 'KANN', 'BUCH', 'WEGE', 'SPUR', 'RUHE',
        'KLAR', 'TIEF', 'RUND', 'STEG', 'WAND', 'RAND', 'GALT', 'BAND', 'MORD', 'IURE',
        'DRAN', 'KAUM', 'DRUM', 'KALT', 'HALB', 'RAUM', 'ORTE', 'TAGE', 'DEIN', 'MEIN',
        'SEID', 'EUCH', 'EURE', 'IHRE', 'BEIM', 'RUFT', 'HEIL', 'GALT',
        # 5-letter
        'NICHT', 'DIESE', 'UNTER', 'DURCH', 'GEGEN', 'IMMER', 'KRAFT', 'GEIST', 'NACHT',
        'LICHT', 'KRIEG', 'MACHT', 'STEIN', 'RUNEN', 'HATTE', 'WURDE', 'GROSS', 'KLEIN',
        'ERSTE', 'ALLES', 'ALLEN', 'KEINE', 'VIELE', 'SCHON', 'STEIL', 'ORTE', 'GEBEN',
        'SENDE', 'SAGEN', 'STATT', 'PLATZ', 'JEDER', 'JEDES', 'JEDEN', 'JEDEM',
        'JETZT', 'WOHER', 'WOHIN', 'WORTE', 'SEITE', 'EINES', 'EINEM', 'EINER', 'EINEN',
        'IHREN', 'STEIG', 'FINDE', 'REDEN', 'FERNE', 'SAGTE', 'DERER', 'DAHER', 'DAHIN',
        'DENEN', 'EUREM', 'EUREN', 'EURER', 'EURES', 'IHRER', 'IHREM', 'IHRES',
        'LEBEN', 'ENDEN', 'DUNKL', 'HEISS', 'SONST', 'ZUVOR', 'SOGAR', 'DARUM', 'DAVON',
        'WOVON', 'WOMIT', 'NEUEN', 'NEUER', 'NEUES', 'NEUEM', 'JENES', 'JENER', 'JENEM',
        'JENEN', 'STETS', 'SOLCH', 'MANCH', 'DAHIN', 'DARIN', 'DABEI', 'TEILS', 'RINGS',
        # 6-letter
        'KOENIG', 'STEINE', 'URALTE', 'FINDEN', 'HATTEN', 'WERDEN', 'KOMMEN', 'SEHEN',
        'KENNEN', 'WISSEN', 'MACHEN', 'NEHMEN', 'STEHEN', 'LIEGEN', 'HALTEN', 'FALLEN',
        'ANDERE', 'DIESEM', 'DIESEN', 'DIESER', 'DIESES', 'SEINEN', 'SEINER', 'SEINES',
        'HINTER', 'WIEDER', 'NICHTS', 'DUNKEL', 'NORDEN', 'SUEDEN', 'STIMME', 'HIMMEL',
        'ANFANG', 'SPRACH', 'DARAUF', 'FELSEN', 'TEMPEL', 'ZEICHEN', 'REICHE', 'SEINER',
        'SEINEM', 'WELCHE', 'SPRUCH', 'GEHEIM', 'SOLCHE', 'INSELN', 'SPRACHE',
        'KRIEGER', 'MEISTER',
        # 7-letter
        'STEINEN', 'URALTEN', 'ANDEREN', 'ZWISCHEN', 'WAHRHEIT', 'KAPITEL',
        'SCHNELL', 'INSCHRIFT', 'SCHRIFT', 'KOENIGIN', 'GEHEIMNIS',
        'KOENIGREICH', 'ZUSAMMEN', 'VERSCHIEDEN', 'VERSPRECHEN', 'VERSTEHEN',
        'MAECHTIGER', 'GEFUNDEN', 'GEBOREN', 'GESEHEN', 'GESCHAFFEN',
        'SPRECHEN', 'SCHREIBEN', 'RUNEORT', 'RUNESTEIN', 'RUNENSTEIN',
        # Special patterns from this text
        'SCHWITEIO', 'HEARUCHTIGER', 'TOTNIURG', 'THARSC', 'LABGE',
        'AUNRSONGETRASES',
    ])

    # DP segmentation
    clean = decoded.replace('[', '').replace(']', '')  # strip bracket codes for parsing
    n = len(decoded)

    # Also try to identify the raw text without unknown markers
    raw_for_parse = ''
    for p in pairs:
        letter = mapping.get(p)
        if letter:
            raw_for_parse += letter
        else:
            raw_for_parse += '?'

    # DP parse on raw_for_parse
    def dp_parse(text, word_set):
        n = len(text)
        dp = [(0, -1)] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i-1]
            for wlen in range(2, min(i, 20) + 1):
                word = text[i-wlen:i]
                if '?' not in word and word in word_set:
                    score = wlen * wlen
                    new_score = dp[i-wlen][0] + score
                    if new_score > dp[i][0]:
                        dp[i] = (new_score, i - wlen)
        result_words = []
        pos = n
        while pos > 0:
            prev = dp[pos][1]
            if prev >= 0 and prev != pos - 1:
                w = text[prev:pos]
                if '?' not in w and w in word_set:
                    result_words.append((prev, w))
                    pos = prev
                    continue
            pos -= 1
        result_words.reverse()
        total_cov = sum(len(w) for _, w in result_words)
        return result_words, dp[n][0], total_cov

    found_words, score, coverage = dp_parse(raw_for_parse, words)
    pct = coverage / len(raw_for_parse) * 100 if raw_for_parse else 0

    print(f"\nWord parse: {len(found_words)} words, coverage {coverage}/{len(raw_for_parse)} ({pct:.0f}%)")

    # Show text with word boundaries
    print(f"\nWith word boundaries:")
    word_positions = set()
    word_map = {}
    for pos, w in found_words:
        for k in range(pos, pos + len(w)):
            word_positions.add(k)
        word_map[pos] = w

    # Build annotated output
    line = ''
    for i, ch in enumerate(raw_for_parse):
        if i in word_map:
            line += ' [' + word_map[i] + '] '
            skip_to = i + len(word_map[i])
        elif i not in word_positions:
            line += ch

    # Print clean
    print(f"  {line.strip()}")

    # Also show the word list
    print(f"\n  Words: {' '.join(w for _, w in found_words)}")

# Summary stats
print(f"\n{'='*60}")
print("REMAINING UNKNOWN CODES")
print(f"{'='*60}")
for code, cnt in remaining_unknowns.most_common():
    print(f"  Code {code}: {cnt} remaining occurrences")

# === SPECIFIC DECODED PASSAGES ===
print(f"\n{'='*80}")
print("KEY DECODED PASSAGES (manually parsed)")
print(f"{'='*80}")

# Decode all books individually and find the most readable ones
book_readability = []
for bi, book in enumerate(books):
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    decoded = ''.join(mapping.get(p, '?') for p in pairs)
    found, score, cov = dp_parse(decoded, words)
    pct = cov / len(decoded) * 100 if decoded else 0
    book_readability.append((bi, decoded, found, pct, len(decoded)))

# Sort by readability
book_readability.sort(key=lambda x: -x[3])

print("\nMost readable books:")
for bi, decoded, found, pct, length in book_readability[:15]:
    print(f"\n  Book {bi} ({length} chars, {pct:.0f}% coverage):")
    print(f"    {decoded}")
    print(f"    Words: {' '.join(w for _, w in found)}")

# === SEARCH FOR SPECIFIC GERMAN PHRASES ===
print(f"\n{'='*80}")
print("GERMAN PHRASE SEARCH")
print(f"{'='*80}")

# Decode ALL text into one long string
all_text = ''
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    decoded = ''.join(mapping.get(p, '?') for p in pairs)
    all_text += decoded + '|'  # separator between books

# Search for German patterns
patterns_to_find = [
    ('DER KOENIG', 'the king'),
    ('DIE URALTE', 'the ancient'),
    ('URALTE STEINEN', 'ancient stones'),
    ('SO DASS', 'so that'),
    ('ICH FINDE', 'I find'),
    ('WIR FINDEN', 'we find'),
    ('DAS ENDE', 'the end'),
    ('DEN ENDE', 'the end (dat.)'),
    ('ENDE REDE', 'concluding speech'),
    ('WIR UND', 'we and'),
    ('ER IST', 'he is'),
    ('ES IST', 'it is'),
    ('AUS DEM', 'from the'),
    ('IN DEM', 'in the'),
    ('IN DEN', 'in the'),
    ('AN DEN', 'at the'),
    ('AUF DEN', 'on the'),
    ('STEIL AN', 'steep at'),
    ('STEINEN', 'stones'),
    ('SCHWITEIO', 'mystery word'),
    ('KOENIG LABGE', 'King LABGE'),
    ('TOTNIURG', 'Totniurg'),
    ('HEARUCHTIGER', 'Hearuchtiger'),
    ('THARSC', 'Tharsc'),
    ('RUNEORT', 'rune-place'),
    ('RUNEN', 'runes'),
    ('SODASSTUN', 'so that do'),
]

for pattern, meaning in patterns_to_find:
    count = all_text.count(pattern)
    if count > 0:
        print(f"\n  '{pattern}' ({meaning}): {count} times")
        # Show context
        idx = 0
        shown = 0
        while shown < 3 and idx < len(all_text):
            pos = all_text.find(pattern, idx)
            if pos < 0:
                break
            ctx_start = max(0, pos - 15)
            ctx_end = min(len(all_text), pos + len(pattern) + 15)
            ctx = all_text[ctx_start:ctx_end].replace('|', ' | ')
            print(f"    ...{ctx}...")
            idx = pos + 1
            shown += 1

# === TRY TO BUILD FULL SENTENCES ===
print(f"\n{'='*80}")
print("SENTENCE RECONSTRUCTION")
print(f"{'='*80}")

# Find the longest readable passages
# Look for sequences of consecutive words
for bi, decoded, found, pct, length in book_readability[:10]:
    if not found:
        continue
    # Find consecutive word sequences
    sequences = []
    current_seq = [found[0]]
    for i in range(1, len(found)):
        prev_end = found[i-1][0] + len(found[i-1][1])
        curr_start = found[i][0]
        gap = curr_start - prev_end
        if gap <= 3:  # Allow small gaps (1-3 unrecognized chars)
            current_seq.append(found[i])
        else:
            if len(current_seq) >= 3:
                sequences.append(current_seq)
            current_seq = [found[i]]
    if len(current_seq) >= 3:
        sequences.append(current_seq)

    if sequences:
        print(f"\n  Book {bi} - readable sequences:")
        for seq in sequences:
            start_pos = seq[0][0]
            end_pos = seq[-1][0] + len(seq[-1][1])
            raw = decoded[start_pos:end_pos]
            word_str = ' '.join(w for _, w in seq)
            print(f"    pos {start_pos}-{end_pos}: {raw}")
            print(f"    Parsed: {word_str}")
