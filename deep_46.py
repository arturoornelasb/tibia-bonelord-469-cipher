"""Deep investigation of code 46: Is it really I? It causes 49/50 II pairs.
Also investigate P — where is it hiding?"""
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

german_words = set([
    'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO', 'DU', 'OB', 'AM', 'IM',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST',
    'WIR', 'ICH', 'SIE', 'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI', 'VOR', 'FUR', 'BIS', 'ALS',
    'TAG', 'ORT', 'TOD', 'OFT', 'NIE', 'ALT', 'NEU', 'NUN', 'HIN',
    'NACH', 'AUCH', 'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN',
    'DASS', 'WENN', 'DANN', 'DENN', 'ABER', 'ODER', 'WEIL',
    'EINE', 'DIES', 'HIER', 'DORT', 'WELT', 'ZEIT', 'TEIL',
    'WORT', 'NAME', 'GANZ', 'SEHR', 'VIEL', 'FORT', 'HOCH',
    'ERDE', 'GOTT', 'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN',
    'HELD', 'MACHT', 'KRAFT', 'GEIST', 'NACHT', 'LICHT',
    'HABEN', 'WERDEN', 'KOMMEN', 'GEHEN', 'SEHEN', 'FINDEN',
    'KENNEN', 'WISSEN', 'MACHEN', 'SAGEN', 'GEBEN', 'NEHMEN',
    'ALLE', 'ALLES', 'ALLEN', 'KEINE', 'VIELE',
    'ERSTE', 'ERSTEN', 'LETZTE', 'ANDERE', 'ANDEREN',
    'DIESE', 'DIESER', 'DIESES', 'DIESEM', 'DIESEN',
    'SEINE', 'SEINER', 'SEINEN', 'SEINES', 'SEINEM',
    'EINEN', 'EINER', 'EINEM', 'EINES',
    'NORDEN', 'GEGEN', 'UNTER', 'DURCH', 'HINTER',
    'IMMER', 'WIEDER', 'SCHON', 'NICHT', 'NICHTS',
    'RUNE', 'RUNEN', 'STEIN', 'STEINE', 'STEINEN',
    'ORTE', 'ORTEN', 'KOENIG', 'URALTE', 'URALTEN',
    'TEMPEL', 'TURM', 'GEBOREN', 'GEHEIMNIS',
    'VOM', 'ZUM', 'ZUR', 'BIS', 'ALS', 'NUN', 'HIN',
    'ZWEI', 'DREI', 'VIER', 'TAGE', 'TAGEN',
    'LAND', 'WASSER', 'FEUER', 'LEBEN', 'ENDE',
    'TEILE', 'TEILEN', 'ERDEN', 'DUNKEL',
    'SAGT', 'SAGTE', 'GING', 'KAM', 'FAND', 'SAH', 'GAB',
    'KONNTE', 'SOLLTE', 'WOLLTE', 'MUSSTE',
    'REICH', 'VOLK', 'SCHRIFT', 'ZEICHEN', 'WAHRHEIT',
    'FUER', 'OHNE', 'NEBEN', 'BEVOR', 'JEDOCH',
])

# ============================================================
# CODE 46: ALL CONTEXTS (172 occurrences!)
# ============================================================
print("=" * 80)
print("CODE 46 ANALYSIS (I) — 172 occurrences, involved in 49/50 II pairs")
print("=" * 80)

count_46 = sum(1 for bps in book_pairs for p in bps if p == '46')
print(f"\nCode 46 total occurrences: {count_46}")

# What precedes and follows code 46?
before_46 = Counter()
after_46 = Counter()
before_46_code = Counter()
after_46_code = Counter()

for bpairs in book_pairs:
    for i, p in enumerate(bpairs):
        if p != '46':
            continue
        if i > 0:
            prev_letter = all_codes.get(bpairs[i-1], '?')
            before_46[prev_letter] += 1
            before_46_code[bpairs[i-1]] += 1
        if i < len(bpairs) - 1:
            nxt_letter = all_codes.get(bpairs[i+1], '?')
            after_46[nxt_letter] += 1
            after_46_code[bpairs[i+1]] += 1

print(f"\nPreceded by (letter): {', '.join(f'{l}:{c}' for l, c in before_46.most_common(12))}")
print(f"Followed by (letter): {', '.join(f'{l}:{c}' for l, c in after_46.most_common(12))}")
prec_str = ', '.join(f'{c}={all_codes.get(c,"?")}:{n}' for c, n in before_46_code.most_common(12))
foll_str = ', '.join(f'{c}={all_codes.get(c,"?")}:{n}' for c, n in after_46_code.most_common(12))
print(f"\nPreceded by (code):  {prec_str}")
print(f"Followed by (code):  {foll_str}")

# Code 46 is followed by code 46 itself 17 times! Show those contexts
print(f"\nContexts where 46 is followed by 46 (17 times):")
count = 0
for idx, bpairs in enumerate(book_pairs):
    for i in range(len(bpairs) - 1):
        if bpairs[i] == '46' and bpairs[i+1] == '46':
            start = max(0, i - 8)
            end = min(len(bpairs), i + 10)
            text = ''.join(all_codes.get(bpairs[k], '?') for k in range(start, end))
            pos = i - start
            hl = text[:pos] + '[' + text[pos] + text[pos+1] + ']' + text[pos+2:]
            print(f"  Bk{idx:2d}: {hl}")
            count += 1
            if count >= 17:
                break
    if count >= 17:
        break

# Test: What if code 46 is NOT I?
print(f"\n{'='*80}")
print("WORD SCORE: code 46 as every letter")
print("=" * 80)

windows_46 = []
for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p == '46':
            start = max(0, j - 8)
            end = min(len(bpairs), j + 9)
            windows_46.append((idx, j, bpairs[start:end], j - start))

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    test = {**all_codes, '46': letter}
    hits = Counter()
    impossible = 0
    for idx, j, window, rel_pos in windows_46:
        text = ''.join(test.get(p, '?') for p in window)
        if '?' in text:
            continue
        for wlen in range(2, min(16, len(text) + 1)):
            for ws in range(len(text) - wlen + 1):
                cand = text[ws:ws + wlen]
                if cand in german_words and ws <= rel_pos < ws + wlen:
                    hits[cand] += 1
        # Count impossible doubles created
        if rel_pos > 0:
            bg = test.get(window[rel_pos-1], '?') + letter
            if bg[0] == bg[1] and bg[0] not in 'SSNNEETTRRLLFFMMPPBBDDCC':
                impossible += 1
        if rel_pos < len(window) - 1:
            bg = letter + test.get(window[rel_pos+1], '?')
            if bg[0] == bg[1] and bg[0] not in 'SSNNEETTRRLLFFMMPPBBDDCC':
                impossible += 1

    total = sum(hits.values())
    if total > 0 or letter == 'I':
        word_str = ', '.join(f"{w}:{c}" for w, c in hits.most_common(8))
        print(f"  46={letter}: hits={total:3d}, bad_doubles={impossible:3d}  {word_str}")

# ============================================================
# P HUNT: Which codes could possibly be P?
# ============================================================
print(f"\n{'='*80}")
print("P HUNT: Testing ALL codes as P (expected ~44 occurrences)")
print("=" * 80)

# For each currently assigned code, compute word hits with current letter vs P
for code, current_letter in sorted(all_codes.items(), key=lambda x: -sum(1 for bps in book_pairs for p in bps if p == x[0])):
    count = sum(1 for bps in book_pairs for p in bps if p == code)
    if count < 5 or count > 100:
        continue  # P should be moderate frequency

    windows = []
    for idx, bpairs in enumerate(book_pairs):
        for j, p in enumerate(bpairs):
            if p == code:
                start = max(0, j - 6)
                end = min(len(bpairs), j + 7)
                windows.append((idx, j, bpairs[start:end], j - start))

    # Current letter word hits
    curr_hits = 0
    for idx, j, window, rel_pos in windows:
        text = ''.join(all_codes.get(p, '?') for p in window)
        if '?' in text:
            continue
        for wlen in range(2, min(12, len(text) + 1)):
            for ws in range(len(text) - wlen + 1):
                cand = text[ws:ws + wlen]
                if cand in german_words and ws <= rel_pos < ws + wlen:
                    curr_hits += 1

    # P word hits
    test = {**all_codes, code: 'P'}
    p_hits = Counter()
    for idx, j, window, rel_pos in windows:
        text = ''.join(test.get(p, '?') for p in window)
        if '?' in text:
            continue
        for wlen in range(2, min(12, len(text) + 1)):
            for ws in range(len(text) - wlen + 1):
                cand = text[ws:ws + wlen]
                if cand in german_words and ws <= rel_pos < ws + wlen:
                    p_hits[cand] += 1

    p_total = sum(p_hits.values())
    if p_total > 0:
        p_str = ', '.join(f"{w}:{c}" for w, c in p_hits.most_common(5))
        print(f"  {code}={current_letter}({count}occ): curr={curr_hits}, P={p_total}  {p_str}")

# Also test the unknown codes for P
print(f"\nUnknown codes as P:")
for code in ['74', '37', '40', '02', '69', '33']:
    count = sum(1 for bps in book_pairs for p in bps if p == code)
    windows = []
    for idx, bpairs in enumerate(book_pairs):
        for j, p in enumerate(bpairs):
            if p == code:
                start = max(0, j - 6)
                end = min(len(bpairs), j + 7)
                windows.append((idx, j, bpairs[start:end], j - start))

    test = {**all_codes, code: 'P'}
    p_hits = Counter()
    for idx, j, window, rel_pos in windows:
        text = ''.join(test.get(p, '?') for p in window)
        if '?' in text:
            continue
        for wlen in range(2, min(12, len(text) + 1)):
            for ws in range(len(text) - wlen + 1):
                cand = text[ws:ws + wlen]
                if cand in german_words and ws <= rel_pos < ws + wlen:
                    p_hits[cand] += 1

    p_total = sum(p_hits.values())
    p_str = ', '.join(f"{w}:{c}" for w, c in p_hits.most_common(5)) if p_hits else "(none)"
    print(f"  {code}=?({count}occ): P={p_total}  {p_str}")

# ============================================================
# BIGRAM IMPACT: What if 46 is changed to a deficit letter?
# ============================================================
print(f"\n{'='*80}")
print("BIGRAM IMPACT: changing code 46 from I")
print("=" * 80)

for test_letter in ['E', 'N', 'A', 'S', 'R', 'T', 'D', 'H', 'U', 'O', 'B', 'F', 'P']:
    test = {**all_codes, '46': test_letter}
    bigrams = Counter()
    total = 0
    for bpairs in book_pairs:
        for i in range(len(bpairs) - 1):
            l1 = test.get(bpairs[i])
            l2 = test.get(bpairs[i+1])
            if l1 and l2:
                bigrams[l1 + l2] += 1
                total += 1

    # Count impossible doubles
    bad_doubles = sum(bigrams.get(c+c, 0) for c in 'IIHHAAUU')
    ii = bigrams.get('II', 0)
    hh = bigrams.get('HH', 0)
    aa = bigrams.get('AA', 0)
    uu = bigrams.get('UU', 0)

    # Count letter frequency
    letter_count = Counter()
    for bpairs in book_pairs:
        for p in bpairs:
            l = test.get(p)
            if l:
                letter_count[l] += 1
    ltotal = sum(letter_count.values())
    i_pct = letter_count['I'] / ltotal * 100
    test_pct = letter_count[test_letter] / ltotal * 100

    print(f"  46={test_letter}: II={ii:2d} HH={hh:2d} AA={aa:2d} UU={uu:2d} | I={i_pct:.1f}% {test_letter}={test_pct:.1f}%")
