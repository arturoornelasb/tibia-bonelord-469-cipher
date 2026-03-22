"""
Deep analysis of top unknown codes: 64, 89, 80, 67, 27, 97, 75, 96, 99, 03
Focus on finding T, R, G, O, B, F, K, Z assignments.
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
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

pair_counts = Counter()
for pairs in book_pairs:
    pair_counts.update(pairs)

def code_sets(letter):
    return set(c for c, l in fixed.items() if l == letter)

def test_word(word, target_code, target_pos):
    """Count how many times target_code at target_pos completes the word."""
    count = 0
    examples = []
    for pairs in book_pairs:
        for i in range(len(pairs) - len(word) + 1):
            window = pairs[i:i+len(word)]
            match = True
            for j in range(len(word)):
                if j == target_pos:
                    if window[j] != target_code:
                        match = False
                        break
                else:
                    if window[j] not in fixed or fixed[window[j]] != word[j]:
                        match = False
                        break
            if match:
                count += 1
                if count <= 3:
                    ctx = pairs[max(0,i-2):i+len(word)+2]
                    decoded = ''.join(fixed.get(c, '?') for c in ctx)
                    examples.append(decoded)
    return count, examples

n_set = code_sets('N')
i_set = code_sets('I')
c_set = code_sets('C')
h_set = code_sets('H')
e_set = code_sets('E')
s_set = code_sets('S')
d_set = code_sets('D')
t_set = code_sets('T')
a_set = code_sets('A')
u_set = code_sets('U')
r_set = code_sets('R')
l_set = code_sets('L')
m_set = code_sets('M')
w_set = code_sets('W')

print("=" * 70)
print("CODE 64 (freq=124, 2.2%) - HIGHEST FREQUENCY UNKNOWN")
print("=" * 70)

# Left/right analysis
left = Counter()
right = Counter()
for pairs in book_pairs:
    for i, p in enumerate(pairs):
        if p != '64':
            continue
        if i > 0 and pairs[i-1] in fixed:
            left[fixed[pairs[i-1]]] += 1
        if i < len(pairs)-1 and pairs[i+1] in fixed:
            right[fixed[pairs[i+1]]] += 1

print(f"Left:  {dict(left.most_common(8))}")
print(f"Right: {dict(right.most_common(8))}")

# Test as T
print("\nTesting 64=T:")
for word in ['NICHT', 'HAT', 'MIT', 'LICHT', 'MACHT', 'NACHT', 'RECHT']:
    for pos in range(len(word)):
        if word[pos] == 'T':
            ct, ex = test_word(word, '64', pos)
            if ct > 0:
                print(f"  {word} (T at pos {pos}): {ct} hits  {ex[:2]}")

# Count HT, NT, IT, DT, ET patterns
for prefix_letter in 'HNIDET':
    prefix_set = code_sets(prefix_letter)
    ct = sum(1 for pairs in book_pairs for i in range(len(pairs)-1)
             if pairs[i] in prefix_set and pairs[i+1] == '64')
    if ct > 2:
        print(f"  {prefix_letter}[64]: {ct}")

# Count TI, TR, TE, TU patterns
for suffix_letter in 'IREUA':
    suffix_set = code_sets(suffix_letter)
    ct = sum(1 for pairs in book_pairs for i in range(len(pairs)-1)
             if pairs[i] == '64' and pairs[i+1] in suffix_set)
    if ct > 2:
        print(f"  [64]{suffix_letter}: {ct}")


print("\n" + "=" * 70)
print("CODE 89 (freq=96, 1.7%) - S on right 96%")
print("=" * 70)

# Test as A
print("Testing 89=A:")
for word in ['DAS', 'DASS', 'WAS', 'ALS', 'MAN', 'NACH', 'WALD']:
    for pos in range(len(word)):
        if word[pos] == 'A':
            ct, ex = test_word(word, '89', pos)
            if ct > 0:
                print(f"  {word} (A at pos {pos}): {ct} hits  {ex[:2]}")

# Test as G
print("Testing 89=G:")
for word in ['GUT', 'GROSS', 'GEGEN', 'GIBT', 'GANZ', 'GEIST']:
    for pos in range(len(word)):
        if word[pos] == 'G':
            ct, ex = test_word(word, '89', pos)
            if ct > 0:
                print(f"  {word} (G at pos {pos}): {ct} hits  {ex[:2]}")


print("\n" + "=" * 70)
print("CODE 80 (freq=79, 1.4%) - N on left 77%")
print("=" * 70)

print("Testing 80=G (NG pattern):")
for word in ['LANG', 'DING', 'RING']:
    for pos in range(len(word)):
        if word[pos] == 'G':
            ct, ex = test_word(word, '80', pos)
            if ct > 0:
                print(f"  {word} (G at pos {pos}): {ct} hits  {ex[:2]}")

# UNG pattern
ung_ct = 0
for pairs in book_pairs:
    for i in range(len(pairs) - 2):
        if pairs[i] in u_set and pairs[i+1] in n_set and pairs[i+2] == '80':
            ung_ct += 1
print(f"  UNG pattern: {ung_ct}")

# NG total
ng_ct = sum(1 for pairs in book_pairs for i in range(len(pairs)-1)
            if pairs[i] in n_set and pairs[i+1] == '80')
print(f"  NG total: {ng_ct}")

print("\nTesting 80=O:")
for word in ['NOCH', 'ODER', 'VON', 'WORT', 'OFT', 'VOLK', 'GROSS', 'GOTT']:
    for pos in range(len(word)):
        if word[pos] == 'O':
            ct, ex = test_word(word, '80', pos)
            if ct > 0:
                print(f"  {word} (O at pos {pos}): {ct} hits  {ex[:2]}")

print("\nTesting 80=T:")
for word in ['NICHT', 'MIT', 'HAT', 'STEHT', 'WELT', 'HALT']:
    for pos in range(len(word)):
        if word[pos] == 'T':
            ct, ex = test_word(word, '80', pos)
            if ct > 0:
                print(f"  {word} (T at pos {pos}): {ct} hits  {ex[:2]}")


print("\n" + "=" * 70)
print("CODE 67 (freq=96, 1.7%)")
print("=" * 70)

left67 = Counter()
right67 = Counter()
for pairs in book_pairs:
    for i, p in enumerate(pairs):
        if p != '67':
            continue
        if i > 0 and pairs[i-1] in fixed:
            left67[fixed[pairs[i-1]]] += 1
        if i < len(pairs)-1 and pairs[i+1] in fixed:
            right67[fixed[pairs[i+1]]] += 1

print(f"Left:  {dict(left67.most_common(8))}")
print(f"Right: {dict(right67.most_common(8))}")

print("Testing 67=T:")
for word in ['NICHT', 'HAT', 'MIT', 'TEIL', 'DORT', 'SETZT']:
    for pos in range(len(word)):
        if word[pos] == 'T':
            ct, ex = test_word(word, '67', pos)
            if ct > 0:
                print(f"  {word} (T at pos {pos}): {ct} hits  {ex[:2]}")

print("Testing 67=R:")
for word in ['DER', 'ODER', 'WIEDER', 'WERDEN', 'ANDERE', 'ANDEREN']:
    for pos in range(len(word)):
        if word[pos] == 'R':
            ct, ex = test_word(word, '67', pos)
            if ct > 0:
                print(f"  {word} (R at pos {pos}): {ct} hits  {ex[:2]}")

print("Testing 67=G:")
for word in ['GEGEN', 'GEIST', 'GEBEN', 'ZEIGEN', 'EINIGE', 'SAGEN']:
    for pos in range(len(word)):
        if word[pos] == 'G':
            ct, ex = test_word(word, '67', pos)
            if ct > 0:
                print(f"  {word} (G at pos {pos}): {ct} hits  {ex[:2]}")


print("\n" + "=" * 70)
print("CODE 27 (freq=73, 1.3%)")
print("=" * 70)

left27 = Counter()
right27 = Counter()
for pairs in book_pairs:
    for i, p in enumerate(pairs):
        if p != '27':
            continue
        if i > 0 and pairs[i-1] in fixed:
            left27[fixed[pairs[i-1]]] += 1
        if i < len(pairs)-1 and pairs[i+1] in fixed:
            right27[fixed[pairs[i+1]]] += 1

print(f"Left:  {dict(left27.most_common(8))}")
print(f"Right: {dict(right27.most_common(8))}")

print("Testing 27=F:")
for word in ['AUF', 'FUER', 'FEST', 'FREUND', 'OFT', 'DARF', 'SCHRIFT']:
    for pos in range(len(word)):
        if word[pos] == 'F':
            ct, ex = test_word(word, '27', pos)
            if ct > 0:
                print(f"  {word} (F at pos {pos}): {ct} hits  {ex[:2]}")

print("Testing 27=O:")
for word in ['ODER', 'NOCH', 'VON', 'WORT', 'DORT', 'SOLL']:
    for pos in range(len(word)):
        if word[pos] == 'O':
            ct, ex = test_word(word, '27', pos)
            if ct > 0:
                print(f"  {word} (O at pos {pos}): {ct} hits  {ex[:2]}")


print("\n" + "=" * 70)
print("CODE 97 (freq=58, 1.0%) - I on left 76%")
print("=" * 70)

left97 = Counter()
right97 = Counter()
for pairs in book_pairs:
    for i, p in enumerate(pairs):
        if p != '97':
            continue
        if i > 0 and pairs[i-1] in fixed:
            left97[fixed[pairs[i-1]]] += 1
        if i < len(pairs)-1 and pairs[i+1] in fixed:
            right97[fixed[pairs[i+1]]] += 1

print(f"Left:  {dict(left97.most_common(8))}")
print(f"Right: {dict(right97.most_common(8))}")

# I on left 76%: common German bigrams starting with I: IN, IE, IS, IM, IR, IG, IT
# Test IG pattern (RICHTIG, EWIG, etc.)
print("Testing 97=G (IG pattern):")
ig_ct = sum(1 for pairs in book_pairs for i in range(len(pairs)-1)
            if pairs[i] in i_set and pairs[i+1] == '97')
print(f"  I[97] total: {ig_ct}")

for word in ['RICHTIG', 'EWIG', 'EINIG', 'WENIG']:
    for pos in range(len(word)):
        if word[pos] == 'G':
            ct, ex = test_word(word, '97', pos)
            if ct > 0:
                print(f"  {word} (G at pos {pos}): {ct} hits  {ex[:2]}")


print("\n" + "=" * 70)
print("CODE 75 (freq=56, 1.0%) - S on left 34%")
print("=" * 70)

left75 = Counter()
right75 = Counter()
for pairs in book_pairs:
    for i, p in enumerate(pairs):
        if p != '75':
            continue
        if i > 0 and pairs[i-1] in fixed:
            left75[fixed[pairs[i-1]]] += 1
        if i < len(pairs)-1 and pairs[i+1] in fixed:
            right75[fixed[pairs[i+1]]] += 1

print(f"Left:  {dict(left75.most_common(8))}")
print(f"Right: {dict(right75.most_common(8))}")

# S left, N right: possible T (ST->TN? no), O (SO->ON? no)
# Wait: left S and right N with total freq 56
# Test as T: ST (very common!), then T->N
print("Testing 75=T:")
st_ct = sum(1 for pairs in book_pairs for i in range(len(pairs)-1)
            if pairs[i] in s_set and pairs[i+1] == '75')
print(f"  S[75] (ST): {st_ct}")
for word in ['STEIN', 'STEINE', 'STEINEN', 'STARK', 'SIND']:
    for pos in range(len(word)):
        if word[pos] == 'T':
            ct, ex = test_word(word, '75', pos)
            if ct > 0:
                print(f"  {word} (T at pos {pos}): {ct} hits  {ex[:2]}")


print("\n" + "=" * 70)
print("SUMMARY OF CANDIDATE ASSIGNMENTS")
print("=" * 70)

# Calculate what each assignment would do to frequencies
german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
}

total = sum(pair_counts.values())
current_freq = Counter()
for c, l in fixed.items():
    current_freq[l] += pair_counts.get(c, 0)

print("\nCurrent frequency deficits:")
for l in sorted(german_freq, key=lambda x: german_freq[x] - current_freq.get(x,0)/total):
    obs = current_freq.get(l, 0) / total * 100
    exp = german_freq[l] * 100
    diff = exp - obs
    if diff > 0.5:
        need_freq = diff / 100 * total
        print(f"  {l}: obs={obs:.1f}% exp={exp:.1f}% deficit={diff:.1f}% (need ~{need_freq:.0f} more pairs)")

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
