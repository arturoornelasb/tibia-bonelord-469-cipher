"""Focused analysis of code 74 — test all 26 letters by word impact."""
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
    '85': 'A', '61': 'U',
    '00': 'H', '14': 'N', '72': 'R', '91': 'S', '15': 'I',
    '76': 'E', '52': 'S', '42': 'D', '46': 'I', '48': 'N',
    '57': 'H', '04': 'M', '12': 'S', '58': 'N',
    '78': 'T', '51': 'R', '35': 'A', '34': 'L',
    '01': 'E', '59': 'S', '41': 'E', '30': 'E',
    '94': 'H',
    '47': 'D', '13': 'N', '71': 'I', '63': 'D',
    '93': 'N', '28': 'D', '86': 'E', '43': 'U',
    '70': 'U', '65': 'I', '16': 'I', '36': 'W',
    '64': 'T', '89': 'A', '80': 'G', '97': 'G', '75': 'T',
    '08': 'R', '20': 'F', '96': 'L', '99': 'O', '55': 'R',
    '67': 'E', '27': 'E', '03': 'E', '09': 'E', '05': 'C', '53': 'N',
    '44': 'U', '62': 'B', '68': 'R',
    '23': 'S', '17': 'E', '29': 'E', '66': 'A', '49': 'E',
    '38': 'K', '77': 'Z',
    '22': 'K', '82': 'O', '73': 'N', '50': 'I', '84': 'G',
    '25': 'O', '83': 'V', '81': 'T', '24': 'I',
    '79': 'O', '10': 'R',
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# German words for matching
german_words = set([
    'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO', 'DU', 'OB', 'AM', 'IM',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST',
    'WIR', 'ICH', 'SIE', 'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI', 'VOR', 'FUR', 'BIS', 'ALS',
    'TAG', 'ORT', 'TOD', 'OFT', 'NIE', 'ALT', 'NEU', 'NUN',
    'NACH', 'AUCH', 'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN',
    'DASS', 'WENN', 'DANN', 'DENN', 'ABER', 'ODER', 'WEIL',
    'EINE', 'DIES', 'HIER', 'DORT', 'WELT', 'ZEIT', 'TEIL',
    'WORT', 'NAME', 'GANZ', 'SEHR', 'VIEL', 'FORT', 'HOCH',
    'ERDE', 'GOTT', 'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN',
    'HELD', 'MACHT', 'KRAFT', 'GEIST', 'NACHT', 'LICHT', 'KRIEG',
    'ENDE', 'KLAR', 'WAHR',
    'HABEN', 'WERDEN', 'KOMMEN', 'GEHEN', 'SEHEN', 'FINDEN',
    'KENNEN', 'WISSEN', 'MACHEN', 'SAGEN', 'GEBEN', 'NEHMEN',
    'STEHEN', 'LIEGEN', 'HALTEN', 'FALLEN', 'HELFEN',
    'ALLE', 'ALLES', 'ALLEN', 'KEINE', 'KEINEN', 'VIELE',
    'ERSTE', 'ERSTEN', 'LETZTE', 'ANDERE', 'ANDEREN',
    'DIESE', 'DIESER', 'DIESES', 'DIESEM', 'DIESEN',
    'SEINE', 'SEINER', 'SEINEN', 'SEINES', 'SEINEM',
    'EINEN', 'EINER', 'EINEM', 'EINES',
    'NORDEN', 'GEGEN', 'UNTER', 'DURCH', 'HINTER',
    'IMMER', 'WIEDER', 'SCHON', 'NICHT', 'NICHTS',
    'RUNE', 'RUNEN', 'STEIN', 'STEINE', 'STEINEN', 'RUNENSTEIN',
    'ORT', 'ORTE', 'ORTEN', 'RUNEORT', 'KOENIG',
    'URALTE', 'URALTEN', 'INSCHRIFT',
    'TEMPEL', 'TURM',
    'VERSCHIEDENE', 'GEHEIMNIS', 'TAUSEND',
    'ANTWORT', 'SOFORT', 'ZUSAMMEN',
    'TEILE', 'TEILEN', 'WORTE', 'WORTEN',
    'ERDEN', 'LEBEN', 'STERBEN',
    'DUNKEL', 'HIMMEL', 'SCHNELL',
    'VERSCHIEDEN',
    # Key test words that might appear with correct code 74
    'MINDERHEIT', 'MINDESTENS', 'MINDESTE',
    'HINTERGRUND', 'EINDEUTIG',
    'KINDERN', 'KINDER', 'KIND',
    'BLIND', 'BINDEN', 'FINDEN', 'WINDEN', 'MINDEN',
    'HINDERN', 'HINDERNIS',
    'WANDERN', 'VERAENDERN',
    'DIENEN', 'DIENER',
    'KOENIGIN', 'KOENIGREICHE',
    # Word ending patterns
    'VERDIENT', 'DIENT',
    'ERINNERN', 'ERKENNEN', 'ENTDECKEN',
    'GESICHT', 'GEDICHT',
    'PFLICHT', 'BERICHT',
    'GESCHICHTE', 'GESCHICHTEN',
])

# Count words in decoded text for each candidate letter for code 74
print("=" * 80)
print("CODE 74 — Testing all letters")
print("=" * 80)

# Get all windows around code 74 for word testing
windows_74 = []
for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p == '74':
            start = max(0, j - 8)
            end = min(len(bpairs), j + 9)
            window = bpairs[start:end]
            rel_pos = j - start  # position of code 74 in window
            windows_74.append((idx, j, window, rel_pos))

print(f"Found {len(windows_74)} occurrences of code 74\n")

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    test_codes = {**base_codes, '74': letter}

    # Count new words created (not present in baseline)
    new_words = Counter()
    for idx, j, window, rel_pos in windows_74:
        text = ''.join(test_codes.get(p, '?') for p in window)
        if '?' in text:
            continue

        # Find all words in this window
        for wlen in range(2, min(16, len(text) + 1)):
            for start in range(len(text) - wlen + 1):
                candidate = text[start:start + wlen]
                if candidate in german_words:
                    # Check if this word overlaps with the position of code 74
                    abs_start = start
                    abs_end = start + wlen
                    if abs_start <= rel_pos < abs_end:
                        new_words[candidate] += 1

    # Count bad bigrams created
    bad = 0
    for idx, j, window, rel_pos in windows_74:
        text = ''.join(test_codes.get(p, '?') for p in window)
        for k in range(len(text) - 1):
            if text[k] == text[k+1] and text[k] in 'IHDP' and (k == rel_pos or k+1 == rel_pos):
                bad += 1

    if new_words or letter in 'EAITONRSMPBF':
        total_hits = sum(new_words.values())
        word_str = ', '.join(f"{w}:{c}" for w, c in new_words.most_common(8))
        print(f"  74={letter}: hits={total_hits:2d} bad={bad:2d}  {word_str}")

# Now focus on the MINH[74] pattern specifically
print(f"\n{'='*80}")
print("MINH[74]DDE pattern — trying to find German words")
print("=" * 80)

# The context is: ...DIE MINH[74]DDEMIDIEURAL...
# Let's get the exact codes for a wide window
for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p == '74':
            # Check if this is the MINH pattern
            if j >= 4 and ''.join(base_codes.get(bpairs[k], '?') for k in range(j-4, j)) == 'MINH':
                start = max(0, j - 10)
                end = min(len(bpairs), j + 15)
                for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    test_codes = {**base_codes, '74': letter}
                    text = ''.join(test_codes.get(bpairs[k], '?') for k in range(start, end))
                    if '?' in text:
                        continue
                    # Try to find words crossing the 74 position
                    pos_74 = j - start
                    # Check words of various lengths centered on pos_74
                    found = []
                    for wstart in range(max(0, pos_74 - 10), pos_74 + 1):
                        for wlen in range(3, min(16, len(text) - wstart + 1)):
                            candidate = text[wstart:wstart + wlen]
                            if candidate in german_words and wstart <= pos_74 < wstart + wlen:
                                found.append(candidate)
                    if found:
                        uniq = sorted(set(found), key=lambda x: -len(x))
                        print(f"  74={letter}: {text}  --> words: {', '.join(uniq)}")
                break
    if j >= 4 and ''.join(base_codes.get(bpairs[k], '?') for k in range(j-4, j)) == 'MINH':
        break

# Now check code 54 similarly
print(f"\n{'='*80}")
print("CODE 54 — Testing all letters")
print("=" * 80)

windows_54 = []
for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p == '54':
            start = max(0, j - 8)
            end = min(len(bpairs), j + 9)
            window = bpairs[start:end]
            rel_pos = j - start
            windows_54.append((idx, j, window, rel_pos))

print(f"Found {len(windows_54)} occurrences of code 54\n")

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    test_codes = {**base_codes, '54': letter}
    new_words = Counter()
    for idx, j, window, rel_pos in windows_54:
        text = ''.join(test_codes.get(p, '?') for p in window)
        if '?' in text:
            continue
        for wlen in range(2, min(16, len(text) + 1)):
            for start in range(len(text) - wlen + 1):
                candidate = text[start:start + wlen]
                if candidate in german_words and start <= rel_pos < start + wlen:
                    new_words[candidate] += 1

    bad = 0
    for idx, j, window, rel_pos in windows_54:
        text = ''.join(test_codes.get(p, '?') for p in window)
        for k in range(len(text) - 1):
            if text[k] == text[k+1] and text[k] in 'EIHDP' and (k == rel_pos or k+1 == rel_pos):
                bad += 1

    if new_words or letter in 'EAITONRSMPBF':
        total_hits = sum(new_words.values())
        word_str = ', '.join(f"{w}:{c}" for w, c in new_words.most_common(8))
        print(f"  54={letter}: hits={total_hits:2d} bad={bad:2d}  {word_str}")

# The key context for 54: SERTIU[54]ENGE[40]IORTEN
# Let's test 54 and 40 TOGETHER
print(f"\n{'='*80}")
print("CODES 54+40 COMBINED — Testing the SERTIU[54]ENGE[40]IORTEN pattern")
print("=" * 80)

# Find the pattern
for idx, bpairs in enumerate(book_pairs):
    text_base = ''.join(base_codes.get(p, '?') for p in bpairs)
    if 'ENGE' in text_base:
        for j, p in enumerate(bpairs):
            if p == '54':
                # Check if 40 is nearby
                for k in range(j+1, min(j+8, len(bpairs))):
                    if bpairs[k] == '40':
                        start = max(0, j - 6)
                        end = min(len(bpairs), k + 8)
                        print(f"\n  Bk{idx}: Testing 54+40 in context:")
                        for l54 in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                            for l40 in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                                tc = {**base_codes, '54': l54, '40': l40}
                                text = ''.join(tc.get(bpairs[i], '?') for i in range(start, end))
                                if '?' in text:
                                    continue
                                # Look for words
                                found = []
                                for wlen in range(4, min(16, len(text) + 1)):
                                    for ws in range(len(text) - wlen + 1):
                                        cand = text[ws:ws + wlen]
                                        if cand in german_words:
                                            # Check it overlaps with 54 or 40 position
                                            p54 = j - start
                                            p40 = k - start
                                            if (ws <= p54 < ws + wlen) or (ws <= p40 < ws + wlen):
                                                found.append(cand)
                                if found:
                                    uniq = list(set(found))
                                    if any(len(w) >= 5 for w in uniq):
                                        print(f"    54={l54} 40={l40}: {text} --> {', '.join(sorted(set(found), key=lambda x: -len(x)))}")
                        break
        break
