"""
Tier 6 investigation:
1. Debug II/HH/DD doubling problems
2. Find O, B, F, K, Z codes
3. Investigate why NICHT=0
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
    '64': 'T', '89': 'A', '80': 'G', '97': 'G', '75': 'T',
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

i_set = code_sets('I')
h_set = code_sets('H')
d_set = code_sets('D')
n_set = code_sets('N')
e_set = code_sets('E')
s_set = code_sets('S')
t_set = code_sets('T')
a_set = code_sets('A')
u_set = code_sets('U')
r_set = code_sets('R')
c_set = code_sets('C')

# ================================================================
# PART 1: DOUBLED LETTER ANALYSIS
# ================================================================
print("=" * 70)
print("DOUBLED LETTER ANALYSIS")
print("=" * 70)

# For each doubled bigram, show which specific code pairs are causing it
for letter, letter_set in [('I', i_set), ('H', h_set), ('D', d_set), ('N', n_set)]:
    pairs_causing = Counter()
    for bpairs in book_pairs:
        for j in range(len(bpairs) - 1):
            if bpairs[j] in letter_set and bpairs[j+1] in letter_set:
                pairs_causing[(bpairs[j], bpairs[j+1])] += 1

    total = sum(pairs_causing.values())
    if total > 5:
        print(f"\n  {letter}{letter}: {total} total occurrences")
        for (c1, c2), ct in pairs_causing.most_common(10):
            # Show context
            examples = []
            for bpairs in book_pairs:
                for j in range(len(bpairs) - 1):
                    if bpairs[j] == c1 and bpairs[j+1] == c2:
                        start = max(0, j-3)
                        end = min(len(bpairs), j+5)
                        ctx = ''.join(fixed.get(p, f'[{p}]') for p in bpairs[start:end])
                        examples.append(ctx)
                        if len(examples) >= 3:
                            break
                if len(examples) >= 3:
                    break
            print(f"    {c1}={letter} + {c2}={letter}: {ct} times")
            for ex in examples[:2]:
                print(f"      ctx: {ex}")


# ================================================================
# PART 2: WHY IS NICHT=0?
# ================================================================
print(f"\n{'='*70}")
print("WHY IS NICHT=0?")
print("=" * 70)

# N codes, I codes, C codes, H codes, T codes
print(f"  N codes: {sorted(n_set)}")
print(f"  I codes: {sorted(i_set)}")
print(f"  C codes: {sorted(c_set)}")
print(f"  H codes: {sorted(h_set)}")
print(f"  T codes: {sorted(t_set)}")

# Search for any NI?HT or N?CHT patterns (5-code windows)
nich_count = 0
for bpairs in book_pairs:
    for j in range(len(bpairs) - 4):
        w = bpairs[j:j+5]
        if (w[0] in n_set and w[1] in i_set and w[2] in c_set
            and w[3] in h_set and w[4] in t_set):
            nich_count += 1
            ctx_start = max(0, j-2)
            ctx_end = min(len(bpairs), j+7)
            ctx = ''.join(fixed.get(p, f'[{p}]') for p in bpairs[ctx_start:ctx_end])
            if nich_count <= 5:
                print(f"  NICHT match: {ctx}")

print(f"  Total NICHT matches: {nich_count}")

# Try partial: search for ICH patterns
ich_count = 0
for bpairs in book_pairs:
    for j in range(len(bpairs) - 2):
        w = bpairs[j:j+3]
        if w[0] in i_set and w[1] in c_set and w[2] in h_set:
            ich_count += 1
print(f"  Total ICH matches: {ich_count}")

# Search CH patterns
ch_count = 0
for bpairs in book_pairs:
    for j in range(len(bpairs) - 1):
        if bpairs[j] in c_set and bpairs[j+1] in h_set:
            ch_count += 1
print(f"  Total CH matches: {ch_count}")

# The only C code is '18'. Show its context
print(f"\n  Code 18 (C) neighbors:")
left18 = Counter()
right18 = Counter()
for bpairs in book_pairs:
    for j, p in enumerate(bpairs):
        if p != '18':
            continue
        if j > 0 and bpairs[j-1] in fixed:
            left18[fixed[bpairs[j-1]]] += 1
        if j < len(bpairs)-1 and bpairs[j+1] in fixed:
            right18[fixed[bpairs[j+1]]] += 1
print(f"    Left:  {dict(left18.most_common(8))}")
print(f"    Right: {dict(right18.most_common(8))}")

# Is there another C code? Check if SCH pattern works with unknowns
print(f"\n  SCH patterns with unknown middle code:")
for bpairs in book_pairs:
    for j in range(len(bpairs) - 2):
        if bpairs[j] in s_set and bpairs[j+2] in h_set:
            mid = bpairs[j+1]
            if mid not in fixed:
                # Check right context for typical SCH continuations
                ctx_end = min(len(bpairs), j+6)
                ctx = ''.join(fixed.get(p, f'[{p}]') for p in bpairs[j:ctx_end])
                # Only show first few
                pass  # too noisy


# ================================================================
# PART 3: HUNT FOR O CODES (2.5% deficit)
# ================================================================
print(f"\n{'='*70}")
print("HUNTING FOR O CODES")
print("=" * 70)

# O-patterns in German: NOCH, ODER, VON, OFT, WORT, DORT, GROSS, GOTT
# Common O bigrams: OR, ON, OC, OU, OB, OD, OG, OH; RO, NO, DO, SO, VO
# Left context: D-O, V-O, N-O, S-O
# Right context: O-R, O-N, O-C, O-D, O-H, O-L, O-S

# Find unknown codes that appear between known contexts suggesting O
unknown_codes = sorted(set(pair_counts.keys()) - set(fixed.keys()),
                       key=lambda c: -pair_counts.get(c, 0))

print(f"\nAll unknown codes by frequency:")
for c in unknown_codes[:20]:
    left = Counter()
    right = Counter()
    for bpairs in book_pairs:
        for j, p in enumerate(bpairs):
            if p != c:
                continue
            if j > 0 and bpairs[j-1] in fixed:
                left[fixed[bpairs[j-1]]] += 1
            if j < len(bpairs)-1 and bpairs[j+1] in fixed:
                right[fixed[bpairs[j+1]]] += 1
    total_known_left = sum(left.values())
    total_known_right = sum(right.values())
    print(f"\n  {c} (freq={pair_counts[c]})")
    print(f"    Left:  {dict(left.most_common(6))} (total={total_known_left})")
    print(f"    Right: {dict(right.most_common(6))} (total={total_known_right})")


# ================================================================
# PART 4: O-SPECIFIC WORD TESTS
# ================================================================
print(f"\n{'='*70}")
print("O-WORD TESTS FOR UNKNOWN CODES")
print("=" * 70)

def test_word_pattern(word, target_code, target_pos):
    """Count matches of word pattern with target_code at target_pos."""
    count = 0
    examples = []
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
                if len(examples) < 2:
                    ctx_start = max(0, j-2)
                    ctx_end = min(len(bpairs), j+len(word)+2)
                    ctx = ''.join(fixed.get(p, f'[{p}]') for p in bpairs[ctx_start:ctx_end])
                    examples.append(ctx)
    return count, examples

o_words = ['NOCH', 'ODER', 'VON', 'WORT', 'DORT', 'OFT', 'GOTT',
           'GROSS', 'SOLL', 'WOHL', 'VOLK', 'GOLD', 'SOHN',
           'WORDEN', 'KONNTE', 'WOLLTE', 'SOLLTE', 'KOMMEN']

for c in unknown_codes[:15]:
    hits = {}
    for word in o_words:
        for pos in range(len(word)):
            if word[pos] == 'O':
                ct, ex = test_word_pattern(word, c, pos)
                if ct > 0:
                    key = f"{word}(O@{pos})"
                    hits[key] = (ct, ex)
    if hits:
        total = sum(v[0] for v in hits.values())
        print(f"\n  {c} (freq={pair_counts[c]}) - O evidence: {total} total hits")
        for k, (ct, ex) in sorted(hits.items(), key=lambda x: -x[1][0]):
            print(f"    {k}: {ct}  {ex[:1]}")


# ================================================================
# PART 5: B-SPECIFIC WORD TESTS
# ================================================================
print(f"\n{'='*70}")
print("B-WORD TESTS FOR UNKNOWN CODES")
print("=" * 70)

b_words = ['ABER', 'BEI', 'BEIDE', 'BUCH', 'BESCHRIEBEN', 'BISHER',
           'BALD', 'BERG', 'BEDEUTEN', 'BEVOR', 'BIS', 'BITTE',
           'HABEN', 'GEBEN', 'LEBEN', 'LIEBE', 'OBEN']

for c in unknown_codes[:15]:
    hits = {}
    for word in b_words:
        for pos in range(len(word)):
            if word[pos] == 'B':
                ct, ex = test_word_pattern(word, c, pos)
                if ct > 0:
                    key = f"{word}(B@{pos})"
                    hits[key] = (ct, ex)
    if hits:
        total = sum(v[0] for v in hits.values())
        print(f"\n  {c} (freq={pair_counts[c]}) - B evidence: {total} total hits")
        for k, (ct, ex) in sorted(hits.items(), key=lambda x: -x[1][0]):
            print(f"    {k}: {ct}  {ex[:1]}")


# ================================================================
# PART 6: F-SPECIFIC WORD TESTS
# ================================================================
print(f"\n{'='*70}")
print("F-WORD TESTS FOR UNKNOWN CODES")
print("=" * 70)

f_words = ['AUF', 'FUER', 'FEST', 'FINDEN', 'FREUND', 'FEUER',
           'FRAU', 'FREI', 'INSCHRIFT', 'SCHRIFT', 'KRAFT',
           'OFT', 'DARF', 'HILFE']

for c in unknown_codes[:15]:
    hits = {}
    for word in f_words:
        for pos in range(len(word)):
            if word[pos] == 'F':
                ct, ex = test_word_pattern(word, c, pos)
                if ct > 0:
                    key = f"{word}(F@{pos})"
                    hits[key] = (ct, ex)
    if hits:
        total = sum(v[0] for v in hits.values())
        print(f"\n  {c} (freq={pair_counts[c]}) - F evidence: {total} total hits")
        for k, (ct, ex) in sorted(hits.items(), key=lambda x: -x[1][0]):
            print(f"    {k}: {ct}  {ex[:1]}")


# ================================================================
# PART 7: Revisit code 27 and 67 (the two biggest unknowns)
# ================================================================
print(f"\n{'='*70}")
print("DETAILED ANALYSIS: CODE 27 (freq=73) and CODE 67 (freq=96)")
print("=" * 70)

for target in ['27', '67']:
    freq = pair_counts[target]
    print(f"\n--- Code {target} (freq={freq}) ---")

    # Test all plausible letters
    test_letters = {
        'O': ['NOCH', 'ODER', 'VON', 'WORT', 'DORT', 'OFT', 'GOTT', 'GROSS', 'WORDEN'],
        'B': ['ABER', 'BEI', 'BUCH', 'HABEN', 'GEBEN', 'LEBEN', 'BERG'],
        'F': ['AUF', 'FEST', 'FREI', 'OFT', 'DARF', 'KRAFT', 'SCHRIFT'],
        'R': ['DER', 'ODER', 'WIEDER', 'WERDEN', 'ANDERE', 'JEDER'],
        'T': ['NICHT', 'MIT', 'HAT', 'TEIL', 'DORT', 'SETZT', 'WELT'],
        'G': ['GEGEN', 'GEIST', 'GEBEN', 'SAGEN', 'ZEIGEN', 'EINIGE'],
        'L': ['ALLE', 'SOLL', 'WELT', 'TEIL', 'VIEL', 'LANG', 'WALD'],
        'E': ['DIESE', 'EINE', 'SEINE', 'ANDERE', 'ERSTE', 'WERDEN'],
    }

    for letter, words in test_letters.items():
        total_hits = 0
        word_hits = []
        for word in words:
            for pos in range(len(word)):
                if word[pos] == letter:
                    ct, ex = test_word_pattern(word, target, pos)
                    if ct > 0:
                        total_hits += ct
                        word_hits.append(f"{word}:{ct}")
        if total_hits > 0:
            print(f"  {target}={letter}: {total_hits} hits [{', '.join(word_hits)}]")


# ================================================================
# PART 8: Check what the post-STEINE context reveals
# ================================================================
print(f"\n{'='*70}")
print("POST-STEINE CONTEXT ANALYSIS")
print("=" * 70)

# STEINE is followed by NT[67][24]ADTHARSCIS
# Let's look at code 24 specifically
print(f"\nCode 24 (freq={pair_counts.get('24', 0)}):")
left24 = Counter()
right24 = Counter()
for bpairs in book_pairs:
    for j, p in enumerate(bpairs):
        if p != '24':
            continue
        if j > 0 and bpairs[j-1] in fixed:
            left24[fixed[bpairs[j-1]]] += 1
        if j < len(bpairs)-1 and bpairs[j+1] in fixed:
            right24[fixed[bpairs[j+1]]] += 1
print(f"  Left:  {dict(left24.most_common(8))}")
print(f"  Right: {dict(right24.most_common(8))}")

# STEINENT[67][24]ADTHARSCIS
# If we read: STEINE N T [67] [24] A D THARSCIS
# 67 and 24 are between known N,T and A,D
# T?A is common: TRA, TEA? No.
# NT[67][24]AD -> N T ? ? A D
# Could be: "STEINEN T?? AD THARSCIS"
# Or the whole thing reads differently if 67 and 24 have values

# What if the N before T67 is actually the end of STEINEN?
# Then we have: STEINEN + [64=T][67][24][89=A][45=D] + THARSCIS
# That's T-?-?-A-D which would be T[67][24]AD
# If it's a German word: TRAAD? No.

# Let's test 67=R and 24=A: STEINEN TRAAD? No
# 67=O and 24=N: STEINEN TONAD? No
# 67=E and 24=N: STEINEN TENAD? No
# 67=R and 24=E: STEINEN TREAD? No

# Actually wait: the T is code 64 which we assigned T.
# Let me re-read: "STEINEN" then "T" (code 64) then "67" then "24" then "A" (89) then "D" (45)
# So the sequence is: STEINEN + T + [67] + [24] + A + D + THARSCIS...

# What German phrase starts with T..AD after STEINEN?
# "DIE URALTE STEINEN TRAGEN DAS..." — no, that's "TRAG" = T-R-A-G
# If 67=R and 24=? then T-R-?-A-D = "TRAD" -> hmm
# What about "STEINEN TRAEDT"? No.
# Maybe "ENTDECKT" fragment?

# Test 67 specifically for R, O, B
for letter in ['R', 'O', 'B', 'F', 'L']:
    for word in ['ODER', 'WERDEN', 'JEDER', 'GOTT', 'ABER', 'VOLK', 'SOLL', 'ALLE']:
        for pos in range(len(word)):
            if word[pos] == letter:
                ct, ex = test_word_pattern(word, '67', pos)
                if ct > 0:
                    print(f"  67={letter}: {word}(pos {pos}): {ct} hits  {ex[:1]}")


print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
