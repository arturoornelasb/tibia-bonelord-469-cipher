"""Validate code 54=M and test comprehensive remaining unknown assignments."""
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

# Show all 16 contexts for code 54 with M assignment
print("=" * 80)
print("CODE 54 = M: All 16 contexts")
print("=" * 80)

test_codes = {**base_codes, '54': 'M'}
for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p != '54':
            continue
        start = max(0, j - 10)
        end = min(len(bpairs), j + 11)
        parts = []
        for k in range(start, end):
            letter = test_codes.get(bpairs[k], f'[{bpairs[k]}]')
            if k == j:
                parts.append(f'>>{letter}<<')
            else:
                parts.append(letter)
        decoded = ''.join(parts)
        print(f"  Bk{idx:2d}: {decoded}")

# Check what German words are created/destroyed by 54=M
german_test = [
    'AM', 'UM', 'IM', 'DEM', 'VOM', 'ZUM',
    'STIMME', 'STIMMEN', 'HIMMEL',
    'MACHEN', 'GEMACHT', 'ZUSAMMEN',
    'IMMER', 'HAMMER', 'KAMMER',
    'KOMMEN', 'GEKOMMEN', 'GENOMMEN',
    'SOMMER', 'NUMMER', 'ZIMMER',
    'NEHMEN', 'NEHMEN',
    'AM', 'UM', 'IM',
    'MACHT', 'NACHT',
]

# Build full text with and without 54=M
text_base = ''
text_with_54M = ''
for bpairs in book_pairs:
    text_base += ''.join(base_codes.get(p, '?') for p in bpairs)
    text_with_54M += ''.join(test_codes.get(p, '?') for p in bpairs)

print(f"\nWord count changes with 54=M:")
for w in sorted(set(german_test)):
    old = text_base.count(w)
    new = text_with_54M.count(w)
    if new != old:
        print(f"  {w}: {old} -> {new} ({'+' if new > old else ''}{new-old})")

# Check bad bigrams
bad_pairs = ['MM', 'MH', 'HM', 'MC', 'CM']
print(f"\nBad bigram changes:")
for bp in bad_pairs:
    old = text_base.count(bp)
    new = text_with_54M.count(bp)
    if new != old:
        print(f"  {bp}: {old} -> {new} ({'+' if new > old else ''}{new-old})")

# Check letter frequency with 54=M
all_letters = Counter()
for p in test_codes.values():
    pass
for bpairs in book_pairs:
    for p in bpairs:
        letter = test_codes.get(p)
        if letter:
            all_letters[letter] += 1

total = sum(all_letters.values())
german_freq = {
    'E': 16.93, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
    'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
    'L': 3.44, 'C': 3.06, 'G': 3.01, 'M': 2.53, 'O': 2.51,
    'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
    'P': 0.79, 'V': 0.67, 'J': 0.27, 'Y': 0.04, 'X': 0.03, 'Q': 0.02,
}

print(f"\nLetter frequency comparison with 54=M (focus on deficit letters):")
for letter in ['M', 'B', 'F', 'P', 'W', 'L', 'O']:
    count = all_letters.get(letter, 0)
    pct = count / total * 100
    expected = german_freq.get(letter, 0)
    delta = pct - expected
    marker = " <-- FIXED" if abs(delta) < 0.5 else (" <-- still off" if abs(delta) > 1.0 else "")
    print(f"  {letter}: {pct:.1f}% (expected {expected:.1f}%, delta={delta:+.1f}%){marker}")

# Now test the SERTIU[54]ENGE[40]IORTEN pattern with 54=M
print(f"\n{'='*80}")
print("SERTIU[54]ENGE[40]IORTEN with 54=M — what is code 40?")
print("=" * 80)

# With 54=M: SERTIUMENGE[40]IORTEN
# What could [40] be to make this a German phrase?
# SERTIU M ENGE [40]I ORTEN
# ENGE = narrow/tightness
# ORTEN = places (dative)
# So: "...SERTIUM ENGE [40]I ORTEN..."
# If 40=N: "SERTIUM ENGE NI ORTEN" → doesn't help
# If 40=D: "SERTIUM ENGE DI ORTEN" → "DIE ORTEN" with split DI?
# Hmm, but 40 comes before I, so [40]I could be a 2-letter word

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    test2 = {**base_codes, '54': 'M', '40': letter}
    # Find the pattern
    for idx, bpairs in enumerate(book_pairs):
        for j, p in enumerate(bpairs):
            if p == '40':
                start = max(0, j - 8)
                end = min(len(bpairs), j + 8)
                text = ''.join(test2.get(bpairs[k], '?') for k in range(start, end))
                if '?' in text:
                    continue
                # Check for long words
                found = []
                pos_40 = j - start
                for wlen in range(4, min(16, len(text) + 1)):
                    for ws in range(len(text) - wlen + 1):
                        cand = text[ws:ws + wlen]
                        if cand in set(['ORTEN', 'FORT', 'NORDEN', 'DORT', 'SOFORT',
                                       'ANTWORT', 'FINDEN', 'BINDEN', 'WINDEN',
                                       'HINTER', 'UNTER', 'UEBER', 'GEGEN',
                                       'DIESE', 'DIESER', 'KOENIG', 'KOENIGIN',
                                       'STEINE', 'STEINEN', 'RUNEORT',
                                       'NIMMER', 'IMMER', 'GEHEN', 'SEHEN',
                                       'DIESEN', 'DIESEM', 'DIESES',
                                       'NICHT', 'NICHTS', 'MACHT',
                                       'ERDE', 'ERDEN', 'LEBEN',
                                       'WELT', 'LAND', 'REICH',
                                       'HERR', 'GOTT', 'HELD',
                                       ]):
                            if ws <= pos_40 < ws + wlen:
                                found.append(cand)
                if found:
                    uniq = sorted(set(found), key=lambda x: -len(x))
                    print(f"  40={letter}: Bk{idx}: {text} -> {', '.join(uniq)}")
                break
        if found:
            break

# Also show ALL contexts for code 40 with different test letters
print(f"\n{'='*80}")
print("CODE 40: All contexts (testing promising letters)")
print("=" * 80)

for letter in 'ABDHINPSTW':
    test2 = {**base_codes, '54': 'M', '40': letter}
    print(f"\n--- 40={letter} ---")
    for idx, bpairs in enumerate(book_pairs):
        for j, p in enumerate(bpairs):
            if p != '40':
                continue
            start = max(0, j - 8)
            end = min(len(bpairs), j + 9)
            parts = []
            for k in range(start, end):
                l = test2.get(bpairs[k], f'[{bpairs[k]}]')
                if k == j:
                    parts.append(f'>>{l}<<')
                else:
                    parts.append(l)
            print(f"  Bk{idx:2d}: {''.join(parts)}")

# Test code 98 similarly
print(f"\n{'='*80}")
print("CODE 98 (4 occurrences): All contexts with different letters")
print("=" * 80)

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    test2 = {**base_codes, '54': 'M', '98': letter}
    found_any = False
    for idx, bpairs in enumerate(book_pairs):
        for j, p in enumerate(bpairs):
            if p != '98':
                continue
            start = max(0, j - 8)
            end = min(len(bpairs), j + 9)
            text = ''.join(test2.get(bpairs[k], '?') for k in range(start, end))
            if '?' in text:
                continue
            # Check for words
            pos_98 = j - start
            for wlen in range(3, min(14, len(text) + 1)):
                for ws in range(len(text) - wlen + 1):
                    cand = text[ws:ws + wlen]
                    if cand in set(['FINDEN', 'BINDEN', 'WINDEN', 'ENDEN', 'SENDEN',
                                   'WENDEN', 'RENDEN', 'FANGEN', 'GANGEN', 'LANGEN',
                                   'STEHEN', 'GEHEN', 'SEHEN', 'DREHEN',
                                   'NACH', 'DOCH', 'NOCH', 'AUCH',
                                   'ALLE', 'ALLES', 'ALLEN',
                                   'KOENIG', 'KOENIGIN',
                                   'ERDE', 'ERDEN', 'WERDEN',
                                   'DIESEN', 'DIESER', 'DIESEM',
                                   'NORDEN', 'SUEDEN', 'OSTEN', 'WESTEN',
                                   'LAND', 'BURG', 'BERG', 'GOLD', 'GOTT',
                                   'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES',
                                   'HERR', 'HERREN', 'RUNE', 'RUNEN', 'STEIN',
                                   'MACHEN', 'SAGEN', 'HALTEN',
                                   'TAG', 'TAGE', 'TAGEN',
                                   'NACHT', 'NAECHTE',
                                   'ENDE', 'ANFANG',
                                   ]):
                        if ws <= pos_98 < ws + wlen:
                            if not found_any:
                                found_any = True
                            print(f"  98={letter}: Bk{idx}: {text} -> {cand}")
