"""
Targeted search for B, K, Z, O, M codes among remaining unknowns.
Uses word pattern matching and bigram profiling.
"""
import json
from collections import Counter, defaultdict

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

# All 68 confirmed codes
fixed = {
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
    '47': 'D', '13': 'N', '71': 'I', '79': 'H', '63': 'D',
    '93': 'N', '28': 'D', '86': 'E', '43': 'U',
    '70': 'U', '65': 'I', '16': 'I', '36': 'W',
    '64': 'T', '89': 'A', '80': 'G', '97': 'G', '75': 'T',
    '08': 'R', '20': 'F', '96': 'L', '99': 'O', '55': 'R',
    '67': 'E', '27': 'E', '03': 'E', '09': 'E',
    '05': 'C', '53': 'N',
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

pair_counts = Counter()
for pairs in book_pairs:
    pair_counts.update(pairs)
total_pairs = sum(pair_counts.values())

unknown_codes = sorted(set(pair_counts.keys()) - set(fixed.keys()),
                       key=lambda c: -pair_counts.get(c, 0))

def test_word(word, target_code, target_pos):
    count = 0
    for bpairs in book_pairs:
        for j in range(len(bpairs) - len(word) + 1):
            window = bpairs[j:j+len(word)]
            match = True
            for k in range(len(word)):
                if k == target_pos:
                    if window[k] != target_code:
                        match = False
                        break
                else:
                    if window[k] not in fixed or fixed[window[k]] != word[k]:
                        match = False
                        break
            if match:
                count += 1
    return count


# ================================================================
# B SEARCH
# ================================================================
print("=" * 70)
print("B CODE SEARCH")
print("=" * 70)

b_words = {
    'ABER': [1],     # aBer
    'HABEN': [2],    # haBen
    'GEBEN': [2],    # geBen
    'LEBEN': [2],    # leBen
    'LIEBE': [3],    # lieBe
    'BUCH': [0],     # Buch
    'BERG': [0],     # Berg
    'BIS': [0],      # Bis
    'BEI': [0],      # Bei
    'BEIDE': [0],    # Beide
    'BALD': [0],     # Bald
    'BAND': [0],     # Band
    'BESCHRIEBEN': [0],  # Beschrieben
    'BEREITS': [0],  # Bereits
    'BESTIMMTE': [0],  # Bestimmte
    'BESONDERE': [0],  # Besondere
    'BISHER': [0],   # Bisher
    'BEDEUTEN': [0], # Bedeuten
    'OBEN': [1],     # oBen
    'NEBEN': [2],    # neBen
    'UEBER': [2],    # ueBer (UE = Ue)
}

for code in unknown_codes:
    freq = pair_counts[code]
    if freq < 5:
        continue
    total_hits = 0
    details = []
    for word, positions in b_words.items():
        for pos in positions:
            ct = test_word(word, code, pos)
            if ct > 0:
                total_hits += ct
                details.append(f"{word}[{pos}]:{ct}")
    if total_hits > 0:
        print(f"  {code} (freq={freq}): B hits={total_hits} [{', '.join(details)}]")


# Also check B bigram compatibility
print("\n  B bigram profile check:")
b_left_common = {'A': 0.44, 'E': 0.30, 'U': 0.15, 'O': 0.10, 'I': 0.10}  # xB bigrams
b_right_common = {'E': 1.06, 'I': 0.38, 'A': 0.20, 'R': 0.15, 'U': 0.12}  # Bx bigrams

for code in unknown_codes:
    freq = pair_counts[code]
    if freq < 10:
        continue
    left = Counter()
    right = Counter()
    for bpairs in book_pairs:
        for j, p in enumerate(bpairs):
            if p != code: continue
            if j > 0 and bpairs[j-1] in fixed:
                left[fixed[bpairs[j-1]]] += 1
            if j < len(bpairs)-1 and bpairs[j+1] in fixed:
                right[fixed[bpairs[j+1]]] += 1

    b_score = 0
    total_l = sum(left.values())
    total_r = sum(right.values())
    if total_l > 0 and total_r > 0:
        for ch, w in b_left_common.items():
            b_score += left.get(ch, 0) / total_l * w
        for ch, w in b_right_common.items():
            b_score += right.get(ch, 0) / total_r * w
        if b_score > 0.3:
            print(f"    {code} (freq={freq}): B-score={b_score:.2f} L={dict(left.most_common(4))} R={dict(right.most_common(4))}")


# ================================================================
# K SEARCH
# ================================================================
print(f"\n{'='*70}")
print("K CODE SEARCH")
print("=" * 70)

k_words = {
    'KEIN': [0],
    'KEINE': [0],
    'KEINEN': [0],
    'KEINER': [0],
    'KANN': [0],
    'KONNTE': [0],
    'KRAFT': [0],
    'KENNEN': [0],
    'KOMMEN': [0],
    'KLEIN': [0],
    'KAMPF': [0],
    'KUNST': [0],
    'KURZ': [0],
    'KIRCHE': [0],
    'STUECK': [4],   # stueCK
    'ZURUECK': [5],
    'STRECKE': [5],
    'ENTDECKEN': [4],  # entdeCKen
    'WIRKLICH': [3],  # wirKlich
    'STARK': [4],    # starK
    'DUNKELN': [3],  # dunKeln
}

for code in unknown_codes:
    freq = pair_counts[code]
    if freq < 5:
        continue
    total_hits = 0
    details = []
    for word, positions in k_words.items():
        for pos in positions:
            ct = test_word(word, code, pos)
            if ct > 0:
                total_hits += ct
                details.append(f"{word}[{pos}]:{ct}")
    if total_hits > 0:
        print(f"  {code} (freq={freq}): K hits={total_hits} [{', '.join(details)}]")

# K bigram check
print("\n  K bigram profile check:")
k_left_common = {'N': 0.30, 'C': 0.20, 'R': 0.10, 'E': 0.10}  # xK
k_right_common = {'E': 0.30, 'O': 0.15, 'A': 0.10, 'L': 0.08}  # Kx

for code in unknown_codes:
    freq = pair_counts[code]
    if freq < 10:
        continue
    left = Counter()
    right = Counter()
    for bpairs in book_pairs:
        for j, p in enumerate(bpairs):
            if p != code: continue
            if j > 0 and bpairs[j-1] in fixed:
                left[fixed[bpairs[j-1]]] += 1
            if j < len(bpairs)-1 and bpairs[j+1] in fixed:
                right[fixed[bpairs[j+1]]] += 1

    k_score = 0
    total_l = sum(left.values())
    total_r = sum(right.values())
    if total_l > 0 and total_r > 0:
        for ch, w in k_left_common.items():
            k_score += left.get(ch, 0) / total_l * w
        for ch, w in k_right_common.items():
            k_score += right.get(ch, 0) / total_r * w
        if k_score > 0.15:
            print(f"    {code} (freq={freq}): K-score={k_score:.2f} L={dict(left.most_common(4))} R={dict(right.most_common(4))}")


# ================================================================
# Z SEARCH
# ================================================================
print(f"\n{'='*70}")
print("Z CODE SEARCH")
print("=" * 70)

z_words = {
    'ZU': [0],
    'ZUM': [0],
    'ZWISCHEN': [0],
    'ZEICHEN': [0],
    'ZEIT': [0],
    'ZURUECK': [0],
    'ZUSAMMEN': [0],
    'ZULETZT': [0],
    'ZWEI': [0],
    'ZEIGT': [0],
    'NUTZEN': [3],     # nutZen
    'SETZEN': [3],
    'LETZTEN': [3],    # letZten
    'GANZ': [3],       # ganZ
    'SALZ': [3],
    'SCHUTZ': [4],     # schutZ
    'EINZELNE': [3],   # einZelne
    'JETZT': [3],      # jetZt
}

for code in unknown_codes:
    freq = pair_counts[code]
    if freq < 5:
        continue
    total_hits = 0
    details = []
    for word, positions in z_words.items():
        for pos in positions:
            ct = test_word(word, code, pos)
            if ct > 0:
                total_hits += ct
                details.append(f"{word}[{pos}]:{ct}")
    if total_hits > 0:
        print(f"  {code} (freq={freq}): Z hits={total_hits} [{', '.join(details)}]")


# ================================================================
# O SEARCH (additional codes beyond 99)
# ================================================================
print(f"\n{'='*70}")
print("O CODE SEARCH (additional)")
print("=" * 70)

o_words = {
    'NOCH': [1],
    'ODER': [0],
    'DORT': [1],
    'WORT': [1],
    'OFT': [0],
    'GROSS': [2],
    'GOTT': [1],
    'SOHN': [1],
    'GOLD': [1],
    'VOLK': [1],
    'BODEN': [1],
    'OBEN': [0],
    'KOMMEN': [1],
    'SONNE': [1],
    'WORDEN': [1],
    'KONNTE': [1],
    'WOLLTE': [1],
    'SOLLTE': [1],
    'DOCH': [1],
    'HOCH': [1],
    'SOLCH': [1],
    'WELCH': [2],  # wait, this has no O. Remove.
    'TROTZDEM': [2],  # trOtzdem
    'VOR': [1],
    'VOM': [1],
    'VON': [1],
}

# Remove WELCH (no O)
o_words.pop('WELCH', None)

for code in unknown_codes:
    freq = pair_counts[code]
    if freq < 5:
        continue
    total_hits = 0
    details = []
    for word, positions in o_words.items():
        for pos in positions:
            ct = test_word(word, code, pos)
            if ct > 0:
                total_hits += ct
                details.append(f"{word}[{pos}]:{ct}")
    if total_hits > 0:
        print(f"  {code} (freq={freq}): O hits={total_hits} [{', '.join(details)}]")


# ================================================================
# M SEARCH (additional codes beyond 04)
# ================================================================
print(f"\n{'='*70}")
print("M CODE SEARCH (additional)")
print("=" * 70)

m_words = {
    'IMMER': [1],
    'MEHR': [0],
    'MACHT': [0],
    'MUSS': [0],
    'MUSSTE': [0],
    'MENSCH': [0],
    'MEISTEN': [0],
    'MANCHE': [0],
    'MANN': [0],
    'MUND': [0],
    'MAHLEN': [0],  # to grind
    'NEHMEN': [3],
    'STIMME': [4],
    'HIMMEL': [2],
    'IMMER': [1],
    'KOMMEN': [2],
    'FLAMME': [3],
    'KAMMER': [2],
    'NAME': [2],
    'GEHEIMNIS': [5],
}

for code in unknown_codes:
    freq = pair_counts[code]
    if freq < 5:
        continue
    total_hits = 0
    details = []
    for word, positions in m_words.items():
        for pos in positions:
            ct = test_word(word, code, pos)
            if ct > 0:
                total_hits += ct
                details.append(f"{word}[{pos}]:{ct}")
    if total_hits > 0:
        print(f"  {code} (freq={freq}): M hits={total_hits} [{', '.join(details)}]")


# ================================================================
# SPECIFIC PATTERN TESTS
# ================================================================
print(f"\n{'='*70}")
print("SPECIFIC PATTERN TESTS")
print("=" * 70)

# Test code 62 as B more thoroughly
print("\n  Code 62 as B:")
for word in ['ABER', 'HABEN', 'GEBEN', 'LEBEN', 'OBEN', 'NEBEN', 'BESCHRIEBEN']:
    for pos in range(len(word)):
        if word[pos] == 'B':
            ct = test_word(word, '62', pos)
            if ct > 0:
                print(f"    {word} (B at {pos}): {ct}")

# Test code 68 as R
print("\n  Code 68 as R:")
for word in ['DER', 'ODER', 'WIEDER', 'DURCH', 'RUNE', 'RUNEN', 'RICHTIG', 'ANDERE', 'HIER']:
    for pos in range(len(word)):
        if word[pos] == 'R':
            ct = test_word(word, '68', pos)
            if ct > 0:
                print(f"    {word} (R at {pos}): {ct}")

# Test code 83 as various letters
print("\n  Code 83 tests:")
for letter, words in [
    ('B', ['ABER', 'HABEN', 'GEBEN', 'BESCHRIEBEN', 'BUCH', 'BIS']),
    ('M', ['IMMER', 'MEHR', 'MACHT', 'MENSCH', 'MUSS', 'NEHMEN']),
    ('O', ['NOCH', 'ODER', 'DORT', 'KONNTE', 'WORDEN', 'KOMMEN']),
    ('A', ['DAS', 'ALLE', 'ANDERE', 'AUS', 'AUCH', 'HALT']),
]:
    total = 0
    hits = []
    for word in words:
        for pos in range(len(word)):
            if word[pos] == letter:
                ct = test_word(word, '83', pos)
                if ct > 0:
                    total += ct
                    hits.append(f"{word}:{ct}")
    if total > 0:
        print(f"    83={letter}: {total} [{', '.join(hits)}]")

# Test code 50 as various letters
print("\n  Code 50 tests:")
for letter, words in [
    ('B', ['ABER', 'HABEN', 'GEBEN', 'BESCHRIEBEN', 'BUCH', 'BIS', 'LEBEN']),
    ('M', ['IMMER', 'MEHR', 'MACHT', 'MENSCH', 'MUSS', 'NEHMEN']),
    ('O', ['NOCH', 'ODER', 'DORT', 'KONNTE', 'WORDEN', 'KOMMEN', 'VOR', 'VON']),
]:
    total = 0
    hits = []
    for word in words:
        for pos in range(len(word)):
            if word[pos] == letter:
                ct = test_word(word, '50', pos)
                if ct > 0:
                    total += ct
                    hits.append(f"{word}:{ct}")
    if total > 0:
        print(f"    50={letter}: {total} [{', '.join(hits)}]")

# Test code 84 as various letters
print("\n  Code 84 tests:")
for letter, words in [
    ('E', ['EINE', 'DIESE', 'SEINE', 'WERDEN', 'STEINE']),
    ('A', ['ALLE', 'ANDERE', 'AUCH', 'DAS', 'HALT']),
    ('I', ['IST', 'ICH', 'SIE', 'SEIN', 'DIE']),
    ('B', ['ABER', 'HABEN', 'GEBEN', 'BIS', 'BUCH', 'LEBEN']),
]:
    total = 0
    hits = []
    for word in words:
        for pos in range(len(word)):
            if word[pos] == letter:
                ct = test_word(word, '84', pos)
                if ct > 0:
                    total += ct
                    hits.append(f"{word}:{ct}")
    if total > 0:
        print(f"    84={letter}: {total} [{', '.join(hits)}]")

# Test code 44 as various letters
print("\n  Code 44 tests:")
for letter, words in [
    ('S', ['SEIN', 'SICH', 'SIND', 'DASS', 'AUS', 'FEST', 'IST']),
    ('B', ['ABER', 'HABEN', 'GEBEN', 'BIS', 'BUCH', 'OBEN', 'LEBEN']),
    ('U', ['UND', 'AUF', 'AUS', 'AUCH', 'URALTE', 'RUNE']),
    ('E', ['EINE', 'DIESE', 'SEINE', 'WERDEN', 'ANDERE']),
    ('N', ['UND', 'SIND', 'EINE', 'EINEN', 'FINDEN']),
]:
    total = 0
    hits = []
    for word in words:
        for pos in range(len(word)):
            if word[pos] == letter:
                ct = test_word(word, '44', pos)
                if ct > 0:
                    total += ct
                    hits.append(f"{word}:{ct}")
    if total > 0:
        print(f"    44={letter}: {total} [{', '.join(hits)}]")


# ================================================================
# CONTEXT AROUND UNKNOWN CODES
# ================================================================
print(f"\n{'='*70}")
print("CONTEXT AROUND KEY UNKNOWN CODES")
print("=" * 70)

for target_code in ['62', '68', '83', '50', '84', '44', '77', '17', '74']:
    contexts = []
    for bpairs in book_pairs:
        for j, p in enumerate(bpairs):
            if p != target_code:
                continue
            start = max(0, j - 3)
            end = min(len(bpairs), j + 4)
            ctx = bpairs[start:end]
            decoded = ''.join(fixed.get(c, f'[{c}]') for c in ctx)
            contexts.append(decoded)

    print(f"\n  Code {target_code} (freq={pair_counts[target_code]}) contexts (sample):")
    # Show unique contexts
    unique = list(set(contexts))
    for ctx in unique[:12]:
        print(f"    {ctx}")


print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
