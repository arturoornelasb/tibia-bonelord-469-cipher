"""Trace the IIIWIIS pattern to raw codes and test alternatives."""
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
    '98': 'T',
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# Find the IIIWIIS pattern
print("=" * 80)
print("TRACING THE 'IIIWIIS' PATTERN")
print("=" * 80)

for idx, bpairs in enumerate(book_pairs):
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    pos = text.find('IIIWII')
    if pos == -1:
        continue

    # Show wide context with raw codes
    start = max(0, pos - 10)
    end = min(len(bpairs), pos + 20)
    print(f"\nBk{idx} pos {pos}:")
    for k in range(start, end):
        letter = all_codes.get(bpairs[k], f'[{bpairs[k]}]')
        marker = " <---" if pos <= k < pos + 6 else ""
        print(f"  pos{k:3d}: code={bpairs[k]} = {letter}{marker}")

    decoded = ''.join(all_codes.get(bpairs[k], '?') for k in range(start, end))
    print(f"  Full: {decoded}")
    break  # Show one example

# Now test: what if we change the I-codes in this pattern?
print(f"\n{'='*80}")
print("TESTING ALTERNATIVES FOR CODES IN IIIWII PATTERN")
print("=" * 80)

# The pattern uses specific codes. Get them:
for idx, bpairs in enumerate(book_pairs):
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    pos = text.find('IIIWII')
    if pos == -1:
        continue

    iii_codes = [bpairs[pos], bpairs[pos+1], bpairs[pos+2]]
    wii_codes = [bpairs[pos+3], bpairs[pos+4], bpairs[pos+5]]
    print(f"III = codes {iii_codes}")
    print(f"WII = codes {wii_codes}")

    # Get WIDE context (30+ chars)
    start = max(0, pos - 15)
    end = min(len(bpairs), pos + 25)
    context_codes = bpairs[start:end]

    # Test substituting each I-code in this pattern
    for i, code in enumerate(iii_codes + wii_codes):
        if all_codes.get(code) != 'I':
            continue
        print(f"\n  Testing alternatives for code {code} (position {i} in pattern):")
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            test = {**all_codes, code: letter}
            decoded = ''.join(test.get(p, '?') for p in context_codes)
            if '?' in decoded:
                continue
            # Check for any words crossing the changed position
            changed_pos = pos - start + i
            found_words = set()
            for wlen in range(3, min(10, len(decoded) + 1)):
                for ws in range(max(0, changed_pos - wlen + 1), min(changed_pos + 1, len(decoded) - wlen + 1)):
                    cand = decoded[ws:ws + wlen]
                    if cand in set(['WIR', 'ICH', 'SIE', 'MAN', 'WER', 'DIE', 'DER', 'DAS',
                                   'IST', 'UND', 'EIN', 'SEIN', 'EINE', 'TEIL', 'NICHT',
                                   'DIESE', 'ALLE', 'HIER', 'DORT', 'ENDE', 'RUNE',
                                   'STEIN', 'STEINE', 'STEINEN', 'KOENIG',
                                   'FINDEN', 'SEHEN', 'GEHEN', 'MACHEN',
                                   'NACH', 'AUCH', 'NOCH', 'DOCH',
                                   'DASS', 'WENN', 'DANN', 'ABER',
                                   'HAT', 'WAR', 'KANN', 'SOLL', 'WILL',
                                   'NUR', 'GUT', 'ORT', 'ORTE',
                                   'SETEI', 'WIESE', 'WIESEN',
                                   'GEIST', 'GEISTER', 'WEISE', 'WEISEN',
                                   'ORTEN', 'ERSTEN', 'ZWEITEN', 'DRITTEN',
                                   'WISSEN', 'GEWISS', 'GEWISSEN',
                                   ]):
                        if ws <= changed_pos < ws + wlen:
                            found_words.add(cand)
            if found_words:
                print(f"    {code}={letter}: {decoded}  --> {', '.join(sorted(found_words, key=lambda x: -len(x)))}")
    break

# HH pattern: trace FACHHECHL
print(f"\n{'='*80}")
print("TRACING THE 'FACHHECHL' PATTERN")
print("=" * 80)

for idx, bpairs in enumerate(book_pairs):
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    pos = text.find('FACHHECH')
    if pos == -1:
        continue

    start = max(0, pos - 5)
    end = min(len(bpairs), pos + 20)
    print(f"\nBk{idx} pos {pos}:")
    for k in range(start, end):
        letter = all_codes.get(bpairs[k], f'[{bpairs[k]}]')
        marker = " <---" if pos <= k < pos + 8 else ""
        print(f"  pos{k:3d}: code={bpairs[k]} = {letter}{marker}")

    decoded = ''.join(all_codes.get(bpairs[k], '?') for k in range(start, end))
    print(f"  Full: {decoded}")
    break

# EXTENDED FACHHECHLL context
print(f"\n{'='*80}")
print("EXTENDED FACHHECHLLTICHOELCODENH PATTERN")
print("=" * 80)

for idx, bpairs in enumerate(book_pairs):
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    if 'FACHHECH' in text:
        pos = text.find('FACH')
        start = max(0, pos - 20)
        end = min(len(bpairs), pos + 30)
        wide = ''.join(all_codes.get(bpairs[k], '?') for k in range(start, end))
        raw = ' '.join(bpairs[start:end])
        print(f"  Bk{idx}: {wide}")
        print(f"     raw: {raw}")
        break

# Test the NACHHECHL pattern too
print(f"\n{'='*80}")
print("NACHHECHL PATTERN")
print("=" * 80)

for idx, bpairs in enumerate(book_pairs):
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    if 'NACHHECH' in text:
        pos = text.find('NACH')
        start = max(0, pos - 10)
        end = min(len(bpairs), pos + 20)
        wide = ''.join(all_codes.get(bpairs[k], '?') for k in range(start, end))
        raw = ' '.join(bpairs[start:end])
        print(f"  Bk{idx}: {wide}")
        print(f"     raw: {raw}")

# What if code 57 is NOT H? Test for the FACH+57+57+ECH pattern
print(f"\n{'='*80}")
print("WHAT IF CODE 57 IS NOT H?")
print("=" * 80)

# Find the FACHHECHL context and test alternatives for code 57
for idx, bpairs in enumerate(book_pairs):
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    if 'FACHHECH' not in text:
        continue
    pos = text.find('FACHHECH')
    start = max(0, pos - 10)
    end = min(len(bpairs), pos + 25)
    context_codes = bpairs[start:end]

    # Code 57 is H. Find positions of code 57 in context
    positions_57 = [i for i, c in enumerate(context_codes) if c == '57']

    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if letter == 'H':
            continue
        test = {**all_codes, '57': letter}
        decoded = ''.join(test.get(p, '?') for p in context_codes)
        if '?' not in decoded:
            # Check if any useful patterns emerge
            for w in ['NICHT', 'NACHT', 'MACHT', 'ACHT', 'NACH', 'DOCH', 'NOCH',
                      'AUCH', 'FACH', 'RECHT', 'SCHLECHT', 'KNECHT',
                      'SPRACHE', 'SACHE', 'DRACHE',
                      'EINFACH', 'VIELFACH', 'MEHRFACH']:
                if w in decoded:
                    print(f"  57={letter}: {decoded}  --> {w}")
    break
