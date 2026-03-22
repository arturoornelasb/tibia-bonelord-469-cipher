"""Crack remaining unknown codes: 74(19), 37(8), 40(7), 02(4), 39(2), 87(2), 69(1), 33(1).
Also investigate I over-representation — which I-codes might be wrong?"""
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
    'HAT', 'WAR', 'HATTE', 'WURDE', 'KANN', 'SOLL', 'WILL', 'MUSS',
    'HABEN', 'WERDEN', 'KOMMEN', 'GEHEN', 'SEHEN', 'FINDEN',
    'KENNEN', 'WISSEN', 'MACHEN', 'SAGEN', 'GEBEN', 'NEHMEN',
    'STEHEN', 'LIEGEN', 'HALTEN', 'FALLEN', 'HELFEN', 'TRAGEN',
    'RUFEN', 'LESEN', 'ALLE', 'ALLES', 'ALLEN',
    'KEINE', 'KEINEN', 'VIELE', 'GROSS', 'KLEIN',
    'ERSTE', 'ERSTEN', 'LETZTE', 'ANDERE', 'ANDEREN',
    'DIESE', 'DIESER', 'DIESES', 'DIESEM', 'DIESEN',
    'SEINE', 'SEINER', 'SEINEN', 'SEINES', 'SEINEM',
    'EINEN', 'EINER', 'EINEM', 'EINES',
    'NORDEN', 'GEGEN', 'UNTER', 'DURCH', 'HINTER', 'UEBER',
    'IMMER', 'WIEDER', 'SCHON', 'NICHT', 'NICHTS',
    'RUNE', 'RUNEN', 'STEIN', 'STEINE', 'STEINEN', 'RUNENSTEIN',
    'ORTE', 'ORTEN', 'RUNEORT', 'KOENIG',
    'URALTE', 'URALTEN', 'INSCHRIFT',
    'TEMPEL', 'TURM', 'GEBOREN', 'GESEHEN', 'GEFUNDEN',
    'GEHEIMNIS', 'TAUSEND', 'ANTWORT', 'SOFORT', 'ZUSAMMEN',
    'VOM', 'ZUM', 'ZUR', 'BIS', 'ALS', 'NUN', 'HIN',
    'ZWEI', 'DREI', 'VIER', 'TAGE', 'TAGEN', 'NACHT',
    'LAND', 'WASSER', 'FEUER', 'LEBEN', 'STERBEN', 'ENDE',
    'TEILE', 'TEILEN', 'WORTE', 'WORTEN', 'ERDEN',
    'DUNKEL', 'HIMMEL', 'SCHNELL', 'VERSCHIEDEN',
    'STIMME', 'STIMMEN', 'KAPITEL',
    'SAGT', 'SAGTE', 'GING', 'GINGEN', 'KAM', 'KAMEN',
    'FAND', 'FANDEN', 'SAH', 'SAHEN', 'GAB', 'GABEN',
    'KONNTE', 'KONNTEN', 'SOLLTE', 'SOLLTEN',
    'WOLLTE', 'WOLLTEN', 'MUSSTE', 'MUSSTEN',
    'REICH', 'REICHE', 'REICHEN', 'VOLK',
    'SCHRIFT', 'SCHRIFTEN', 'ZEICHEN', 'WAHRHEIT',
    'FUER', 'OHNE', 'NEBEN', 'BEVOR', 'JEDOCH',
    'VERSCHIEDENE',
])

unknowns = ['74', '37', '40', '02', '39', '87', '69', '33']

# Show all contexts for each unknown code
print("=" * 80)
print("ALL UNKNOWN CODES - CONTEXTS")
print("=" * 80)

for code in unknowns:
    contexts = []
    for idx, bpairs in enumerate(book_pairs):
        for j, p in enumerate(bpairs):
            if p == code:
                start = max(0, j - 8)
                end = min(len(bpairs), j + 9)
                parts = []
                for k in range(start, end):
                    letter = all_codes.get(bpairs[k], f'[{bpairs[k]}]')
                    if k == j:
                        parts.append(f'>>{letter}<<')
                    else:
                        parts.append(letter)
                contexts.append((idx, ''.join(parts)))

    print(f"\nCode {code} ({len(contexts)} occurrences):")
    for idx, ctx in contexts:
        print(f"  Bk{idx:2d}: {ctx}")

# Test all 26 letters for each unknown
print(f"\n{'='*80}")
print("WORD SCORE FOR EACH UNKNOWN x LETTER")
print("=" * 80)

for code in unknowns:
    windows = []
    for idx, bpairs in enumerate(book_pairs):
        for j, p in enumerate(bpairs):
            if p == code:
                start = max(0, j - 8)
                end = min(len(bpairs), j + 9)
                window = bpairs[start:end]
                rel_pos = j - start
                windows.append((idx, j, window, rel_pos))

    print(f"\nCode {code} ({len(windows)} occ):")
    results = []
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        test_codes = {**all_codes, code: letter}
        hits = Counter()
        for idx, j, window, rel_pos in windows:
            text = ''.join(test_codes.get(p, '?') for p in window)
            if '?' in text:
                continue
            for wlen in range(2, min(16, len(text) + 1)):
                for ws in range(len(text) - wlen + 1):
                    cand = text[ws:ws + wlen]
                    if cand in german_words and ws <= rel_pos < ws + wlen:
                        hits[cand] += 1

        total = sum(hits.values())
        if total > 0:
            word_str = ', '.join(f"{w}:{c}" for w, c in hits.most_common(5))
            results.append((letter, total, word_str))

    results.sort(key=lambda x: -x[1])
    for letter, total, word_str in results[:8]:
        print(f"  {code}={letter}: hits={total:2d}  {word_str}")

# I over-representation analysis
print(f"\n{'='*80}")
print("I OVER-REPRESENTATION ANALYSIS")
print("=" * 80)

i_codes = [c for c, l in all_codes.items() if l == 'I']
print(f"\nCodes assigned to I: {i_codes}")

# For each I-code, check what happens if we change it to deficit letters
deficit_letters = ['B', 'F', 'P', 'W', 'L', 'A', 'O']

for i_code in sorted(i_codes, key=lambda c: -sum(1 for bps in book_pairs for p in bps if p == c)):
    count = sum(1 for bps in book_pairs for p in bps if p == i_code)

    # Get all contexts for this I-code
    windows = []
    for idx, bpairs in enumerate(book_pairs):
        for j, p in enumerate(bpairs):
            if p == i_code:
                start = max(0, j - 6)
                end = min(len(bpairs), j + 7)
                window = bpairs[start:end]
                rel_pos = j - start
                windows.append((idx, j, window, rel_pos))

    # Count I-words vs alternative words
    i_words = Counter()
    for idx, j, window, rel_pos in windows:
        text = ''.join(all_codes.get(p, '?') for p in window)
        if '?' in text:
            continue
        for wlen in range(2, min(16, len(text) + 1)):
            for ws in range(len(text) - wlen + 1):
                cand = text[ws:ws + wlen]
                if cand in german_words and ws <= rel_pos < ws + wlen:
                    i_words[cand] += 1

    i_total = sum(i_words.values())

    print(f"\nCode {i_code}=I ({count} occ, {i_total} word hits as I):")
    if i_words:
        print(f"  As I: {', '.join(f'{w}:{c}' for w, c in i_words.most_common(5))}")

    # Test alternatives
    for alt in deficit_letters:
        test = {**all_codes, i_code: alt}
        alt_words = Counter()
        for idx, j, window, rel_pos in windows:
            text = ''.join(test.get(p, '?') for p in window)
            if '?' in text:
                continue
            for wlen in range(2, min(16, len(text) + 1)):
                for ws in range(len(text) - wlen + 1):
                    cand = text[ws:ws + wlen]
                    if cand in german_words and ws <= rel_pos < ws + wlen:
                        alt_words[cand] += 1

        alt_total = sum(alt_words.values())
        if alt_total > i_total:
            print(f"  ** {i_code}={alt}: {alt_total} hits (BETTER!) {', '.join(f'{w}:{c}' for w, c in alt_words.most_common(5))}")
        elif alt_total > 0:
            print(f"  {i_code}={alt}: {alt_total} hits  {', '.join(f'{w}:{c}' for w, c in alt_words.most_common(5))}")

# Show some decoded contexts
print(f"\n{'='*80}")
print("SAMPLE DECODED CONTEXTS (focusing on ?-containing segments)")
print("=" * 80)

for idx, bpairs in enumerate(book_pairs):
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    if '?' not in text:
        continue
    # Find ? positions
    for i, c in enumerate(text):
        if c == '?':
            start = max(0, i - 15)
            end = min(len(text), i + 16)
            ctx = text[start:end]
            # Find which code is unknown
            code_idx = sum(1 for ch in text[:i] if ch != '?') + sum(1 for ch in text[:i] if ch == '?')
            raw_code = bpairs[i] if i < len(bpairs) else '??'
            print(f"  Bk{idx:2d} pos{i:3d} code={raw_code}: ...{ctx}...")
    if idx > 60:
        break
