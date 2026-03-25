"""Trace impossible bigrams (II, HH, UU, AA) back to specific code pairs.
Also trace the LE=0 and AN deficit anomalies."""
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

# ============================================================
# TRACE: Which code pairs produce II bigrams?
# ============================================================
print("=" * 80)
print("II BIGRAM SOURCES (which code pairs produce I+I?)")
print("=" * 80)

ii_sources = Counter()
for bpairs in book_pairs:
    for i in range(len(bpairs) - 1):
        c1, c2 = bpairs[i], bpairs[i+1]
        l1 = all_codes.get(c1)
        l2 = all_codes.get(c2)
        if l1 == 'I' and l2 == 'I':
            ii_sources[(c1, c2)] += 1

print(f"\nTotal II pairs: {sum(ii_sources.values())}")
for (c1, c2), cnt in ii_sources.most_common():
    print(f"  {c1}(I) + {c2}(I): {cnt} times")

# Show context for the most common II pairs
print(f"\nContexts for most common II pair:")
top_pair = ii_sources.most_common(1)[0][0]
count = 0
for idx, bpairs in enumerate(book_pairs):
    for i in range(len(bpairs) - 1):
        if bpairs[i] == top_pair[0] and bpairs[i+1] == top_pair[1]:
            start = max(0, i - 6)
            end = min(len(bpairs), i + 8)
            text = ''.join(all_codes.get(bpairs[k], '?') for k in range(start, end))
            pos1 = i - start
            print(f"  Bk{idx:2d}: {text[:pos1]}[{text[pos1]}{text[pos1+1]}]{text[pos1+2:]}")
            count += 1
            if count >= 8:
                break
    if count >= 8:
        break

# ============================================================
# TRACE: Which code pairs produce HH bigrams?
# ============================================================
print(f"\n{'='*80}")
print("HH BIGRAM SOURCES")
print("=" * 80)

hh_sources = Counter()
for bpairs in book_pairs:
    for i in range(len(bpairs) - 1):
        c1, c2 = bpairs[i], bpairs[i+1]
        l1 = all_codes.get(c1)
        l2 = all_codes.get(c2)
        if l1 == 'H' and l2 == 'H':
            hh_sources[(c1, c2)] += 1

print(f"\nTotal HH pairs: {sum(hh_sources.values())}")
for (c1, c2), cnt in hh_sources.most_common():
    print(f"  {c1}(H) + {c2}(H): {cnt} times")

# Show context for top HH pair
print(f"\nContexts for most common HH pair:")
top_pair = hh_sources.most_common(1)[0][0]
count = 0
for idx, bpairs in enumerate(book_pairs):
    for i in range(len(bpairs) - 1):
        if bpairs[i] == top_pair[0] and bpairs[i+1] == top_pair[1]:
            start = max(0, i - 6)
            end = min(len(bpairs), i + 8)
            text = ''.join(all_codes.get(bpairs[k], '?') for k in range(start, end))
            pos1 = i - start
            print(f"  Bk{idx:2d}: {text[:pos1]}[{text[pos1]}{text[pos1+1]}]{text[pos1+2:]}")
            count += 1
            if count >= 8:
                break
    if count >= 8:
        break

# ============================================================
# TRACE: UU and AA sources
# ============================================================
for target, label in [('U', 'UU'), ('A', 'AA')]:
    sources = Counter()
    for bpairs in book_pairs:
        for i in range(len(bpairs) - 1):
            c1, c2 = bpairs[i], bpairs[i+1]
            l1 = all_codes.get(c1)
            l2 = all_codes.get(c2)
            if l1 == target and l2 == target:
                sources[(c1, c2)] += 1
    if sources:
        print(f"\n{label} sources:")
        for (c1, c2), cnt in sources.most_common():
            # Show a context
            for idx, bpairs in enumerate(book_pairs):
                for i in range(len(bpairs) - 1):
                    if bpairs[i] == c1 and bpairs[i+1] == c2:
                        start = max(0, i - 5)
                        end = min(len(bpairs), i + 7)
                        text = ''.join(all_codes.get(bpairs[k], '?') for k in range(start, end))
                        print(f"  {c1}({target})+{c2}({target}): {cnt}x  ctx: {text}")
                        break
                break

# ============================================================
# TRACE: What follows L-codes (34, 96)?
# ============================================================
print(f"\n{'='*80}")
print("L-CODE NEIGHBORS: What follows codes 34 and 96?")
print("=" * 80)

for l_code in ['34', '96']:
    followers = Counter()
    predecessors = Counter()
    for bpairs in book_pairs:
        for i in range(len(bpairs)):
            if bpairs[i] != l_code:
                continue
            if i < len(bpairs) - 1:
                nxt = bpairs[i+1]
                nxt_letter = all_codes.get(nxt, f'[{nxt}]')
                followers[nxt_letter] += 1
            if i > 0:
                prev = bpairs[i-1]
                prev_letter = all_codes.get(prev, f'[{prev}]')
                predecessors[prev_letter] += 1

    count = sum(1 for bps in book_pairs for p in bps if p == l_code)
    print(f"\nCode {l_code}=L ({count} occurrences):")
    print(f"  Followed by: {', '.join(f'{l}:{c}' for l, c in followers.most_common(10))}")
    print(f"  Preceded by: {', '.join(f'{l}:{c}' for l, c in predecessors.most_common(10))}")

# ============================================================
# TRACE: What follows A-codes? Why is AN so low?
# ============================================================
print(f"\n{'='*80}")
print("A-CODE NEIGHBORS: Why is AN so low?")
print("=" * 80)

a_codes = [c for c, l in all_codes.items() if l == 'A']
n_codes = [c for c, l in all_codes.items() if l == 'N']

# Count A->N transitions
an_count = 0
a_total = 0
for bpairs in book_pairs:
    for i in range(len(bpairs) - 1):
        if all_codes.get(bpairs[i]) == 'A':
            a_total += 1
            if all_codes.get(bpairs[i+1]) == 'N':
                an_count += 1

print(f"A codes: {a_codes}")
print(f"N codes: {n_codes}")
print(f"A->N transitions: {an_count} out of {a_total} A-followed-by-anything ({an_count/max(a_total,1)*100:.1f}%)")
print(f"Expected: ~{1.16/6.51*100:.0f}% of A's should be followed by N")

# Per A-code breakdown
for a_code in a_codes:
    followers = Counter()
    for bpairs in book_pairs:
        for i in range(len(bpairs) - 1):
            if bpairs[i] == a_code:
                nxt_letter = all_codes.get(bpairs[i+1], '?')
                followers[nxt_letter] += 1
    count = sum(followers.values())
    n_follows = sum(followers.get(l, 0) for l in ['N'])
    print(f"  Code {a_code}=A ({count} follows): {', '.join(f'{l}:{c}' for l, c in followers.most_common(8))}")

# ============================================================
# CODE 24: Investigate whether it might be something other than I
# ============================================================
print(f"\n{'='*80}")
print("CODE 24=I: ALL CONTEXTS (47 occurrences)")
print("=" * 80)

count = 0
for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p != '24':
            continue
        start = max(0, j - 8)
        end = min(len(bpairs), j + 9)
        text = ''.join(all_codes.get(bpairs[k], '?') for k in range(start, end))
        pos = j - start
        hl = text[:pos] + '[' + text[pos] + ']' + text[pos+1:]
        print(f"  Bk{idx:2d}: {hl}")
        count += 1
        if count >= 20:
            print(f"  ... ({47 - count} more)")
            break
    if count >= 20:
        break

# ============================================================
# What SHOULD code 34 be? Test all letters
# ============================================================
print(f"\n{'='*80}")
print("CODE 34: TESTING ALL LETTERS (currently L, 110 occ)")
print("=" * 80)

german_words = set([
    'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO', 'DU', 'OB', 'AM', 'IM',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST',
    'WIR', 'ICH', 'SIE', 'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI', 'VOR', 'FUR', 'BIS', 'ALS',
    'TAG', 'ORT', 'TOD', 'OFT', 'NIE', 'ALT', 'NEU', 'NUN',
    'NACH', 'AUCH', 'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN',
    'DASS', 'WENN', 'DANN', 'DENN', 'ABER', 'ODER', 'WEIL',
    'EINE', 'DIES', 'HIER', 'DORT', 'WELT', 'ZEIT', 'TEIL',
    'ERDE', 'GOTT', 'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN',
    'HELD', 'MACHT', 'KRAFT', 'GEIST', 'NACHT', 'LICHT', 'KRIEG',
    'HABEN', 'WERDEN', 'KOMMEN', 'GEHEN', 'SEHEN', 'FINDEN',
    'KENNEN', 'WISSEN', 'MACHEN', 'SAGEN', 'GEBEN', 'NEHMEN',
    'ALLE', 'ALLES', 'ALLEN', 'KEINE', 'VIELE',
    'ERSTE', 'ERSTEN', 'LETZTE', 'ANDERE', 'ANDEREN',
    'DIESE', 'DIESER', 'DIESES', 'DIESEM', 'DIESEN',
    'SEINE', 'SEINER', 'SEINEN',
    'EINEN', 'EINER', 'EINEM', 'EINES',
    'NORDEN', 'GEGEN', 'UNTER', 'DURCH', 'HINTER',
    'IMMER', 'WIEDER', 'SCHON', 'NICHT', 'NICHTS',
    'RUNE', 'RUNEN', 'STEIN', 'STEINE', 'STEINEN',
    'ORTE', 'ORTEN', 'RUNEORT', 'KOENIG',
    'URALTE', 'URALTEN',
    'VOM', 'ZUM', 'ZUR', 'BIS', 'ALS',
    'TAGE', 'TAGEN', 'NACHT', 'LAND', 'LEBEN', 'ENDE',
    'TEILE', 'TEILEN', 'ERDEN', 'DUNKEL',
])

# Build windows
windows_34 = []
for idx, bpairs in enumerate(book_pairs):
    for j, p in enumerate(bpairs):
        if p == '34':
            start = max(0, j - 6)
            end = min(len(bpairs), j + 7)
            window = bpairs[start:end]
            rel_pos = j - start
            windows_34.append((idx, j, window, rel_pos))

# Count current L words
for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    test = {**all_codes, '34': letter}
    hits = Counter()
    for idx, j, window, rel_pos in windows_34:
        text = ''.join(test.get(p, '?') for p in window)
        if '?' in text:
            continue
        for wlen in range(2, min(12, len(text) + 1)):
            for ws in range(len(text) - wlen + 1):
                cand = text[ws:ws + wlen]
                if cand in german_words and ws <= rel_pos < ws + wlen:
                    hits[cand] += 1
    total = sum(hits.values())
    if total > 5 or letter == 'L':
        word_str = ', '.join(f"{w}:{c}" for w, c in hits.most_common(8))
        print(f"  34={letter}: hits={total:3d}  {word_str}")
