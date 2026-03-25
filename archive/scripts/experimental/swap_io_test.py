"""
Test whether any I codes should actually be O, and broader O/B/F search.
Also test 67=R and 27=O hypotheses.
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

def code_sets(letter, mapping=None):
    if mapping is None:
        mapping = fixed
    return set(c for c, l in mapping.items() if l == letter)

def test_word_in(word, target_code, target_pos, mapping):
    """Count matches of word pattern with target_code at target_pos using given mapping."""
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
                    if window[k] not in mapping or mapping[window[k]] != word[k]:
                        match = False
                        break
            if match:
                count += 1
    return count

# ================================================================
# PART 1: TEST EACH I CODE AS O
# ================================================================
print("=" * 70)
print("TESTING I CODES AS O")
print("=" * 70)

i_codes = ['21', '15', '46', '71', '65', '16']

o_words = ['NOCH', 'ODER', 'VON', 'OFT', 'DORT', 'WORT', 'GOTT',
           'GROSS', 'SOLL', 'WOHL', 'VOLK', 'GOLD', 'SOHN',
           'WORDEN', 'KONNTE', 'WOLLTE', 'SOLLTE', 'KOMMEN',
           'BODEN', 'OBEN', 'SONNE', 'OSTEN', 'NORDEN']

i_words = ['NICHT', 'IST', 'ICH', 'SIE', 'DIE', 'DIESE', 'DIESER',
           'SEIN', 'EINE', 'SICH', 'HIER', 'IMMER', 'IHRE',
           'INSCHRIFT', 'ZEICHEN', 'RICHTIG', 'SCHRIFT',
           'LICHT', 'GEIST', 'WISSEN', 'MIT', 'BIS', 'BEI']

for code in i_codes:
    freq = pair_counts[code]
    # Count I-word matches (current assignment)
    i_hits = 0
    i_details = []
    for word in i_words:
        for pos in range(len(word)):
            if word[pos] == 'I':
                ct = test_word_in(word, code, pos, fixed)
                if ct > 0:
                    i_hits += ct
                    i_details.append(f"{word}:{ct}")

    # Count O-word matches (hypothetical)
    test_map = dict(fixed)
    test_map[code] = 'O'
    o_hits = 0
    o_details = []
    for word in o_words:
        for pos in range(len(word)):
            if word[pos] == 'O':
                ct = test_word_in(word, code, pos, test_map)
                if ct > 0:
                    o_hits += ct
                    o_details.append(f"{word}:{ct}")

    # Bigram analysis
    left = Counter()
    right = Counter()
    for bpairs in book_pairs:
        for j, p in enumerate(bpairs):
            if p != code:
                continue
            if j > 0 and bpairs[j-1] in fixed:
                left[fixed[bpairs[j-1]]] += 1
            if j < len(bpairs)-1 and bpairs[j+1] in fixed:
                right[fixed[bpairs[j+1]]] += 1

    # Count II pairs involving this code
    i_set = code_sets('I')
    ii_count = 0
    for bpairs in book_pairs:
        for j in range(len(bpairs) - 1):
            if (bpairs[j] == code and bpairs[j+1] in i_set) or \
               (bpairs[j] in i_set and bpairs[j+1] == code):
                ii_count += 1

    print(f"\n  Code {code} (freq={freq})")
    print(f"    As I: {i_hits} word hits [{', '.join(i_details[:5])}]")
    print(f"    As O: {o_hits} word hits [{', '.join(o_details[:5])}]")
    print(f"    II pairs involving this code: {ii_count}")
    print(f"    Left:  {dict(left.most_common(5))}")
    print(f"    Right: {dict(right.most_common(5))}")

    # German O bigrams check: common O bigrams
    o_bigram_score = 0
    for l, ct in left.items():
        if l in 'NVDSWG':  # letters commonly before O
            o_bigram_score += ct
    for r, ct in right.items():
        if r in 'RNDHSLTCG':  # letters commonly after O
            o_bigram_score += ct

    i_bigram_score = 0
    for l, ct in left.items():
        if l in 'ESNDTCHAW':  # letters commonly before I
            i_bigram_score += ct
    for r, ct in right.items():
        if r in 'ENSCTHRDGM':  # letters commonly after I
            i_bigram_score += ct

    print(f"    O-bigram compatibility: {o_bigram_score}")
    print(f"    I-bigram compatibility: {i_bigram_score}")


# ================================================================
# PART 2: FULL DECODE WITH 67=R, 27=O
# ================================================================
print(f"\n{'='*70}")
print("TESTING 67=R, 27=O HYPOTHESIS")
print("=" * 70)

test_map2 = dict(fixed)
test_map2['67'] = 'R'
test_map2['27'] = 'O'

# Check word hits
all_words = ['NOCH', 'ODER', 'VON', 'DORT', 'WORT', 'OFT', 'GROSS',
             'GOTT', 'WORDEN', 'SOLL', 'WOHL', 'VOLK', 'GOLD',
             'DER', 'DIESER', 'JEDER', 'WIEDER', 'WERDEN', 'ANDERE',
             'ABER', 'ODER', 'IMMER', 'UNTER', 'RICHTIG',
             'NICHT', 'MACHT', 'NACHT', 'LICHT', 'RECHT',
             'URALTE', 'STEINE', 'RUNEN', 'ZWISCHEN',
             'INSCHRIFT', 'GEHEIMNIS', 'GEHEIME',
             'DURCH', 'GROSS', 'KOENNEN', 'KONNTE',
             'DAS', 'EINE', 'SEINE', 'DIESE', 'HIER', 'DORT',
             'DREI', 'DRIN', 'DRAN', 'DRUM', 'DRUNTER']

# Decode full text with test mapping
full_text = ''
for bpairs in book_pairs:
    full_text += ''.join(test_map2.get(p, '?') for p in bpairs)

known_pct = sum(1 for c in full_text if c != '?') / len(full_text) * 100
print(f"Known: {known_pct:.1f}%")

# Count words
word_hits = {}
for word in sorted(set(all_words), key=lambda w: -len(w)):
    ct = full_text.count(word)
    if ct > 0:
        word_hits[word] = ct

print(f"\nWord hits with 67=R, 27=O:")
for word, ct in sorted(word_hits.items(), key=lambda x: -len(x[0]) * x[1]):
    if ct >= 2 or len(word) >= 5:
        print(f"  {word}: {ct}")

# Show decoded books
print(f"\nDecoded books (top 3):")
for i, bpairs in enumerate(book_pairs):
    decoded = ''.join(test_map2.get(p, f'[{p}]') for p in bpairs)
    if len(bpairs) > 130:
        print(f"\n  Book {i} ({len(bpairs)} pairs):")
        for j in range(0, len(decoded), 90):
            print(f"    {decoded[j:j+90]}")

# Bigram check
bigram_counts = Counter()
for i in range(len(full_text) - 1):
    if full_text[i] != '?' and full_text[i+1] != '?':
        bigram_counts[full_text[i:i+2]] += 1

print(f"\nUnusual bigrams with 67=R, 27=O:")
for bg in ['OO', 'OA', 'AO', 'RR', 'II', 'HH', 'DD', 'NN', 'OR', 'RO']:
    ct = bigram_counts.get(bg, 0)
    print(f"  {bg}: {ct}")

# Frequency check
letter_freq = Counter()
for c in full_text:
    if c != '?':
        letter_freq[c] += 1
total_known = sum(letter_freq.values())

german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
}

print(f"\nFrequency with 67=R, 27=O:")
for l in sorted(german_freq, key=lambda x: -german_freq[x]):
    obs = letter_freq.get(l, 0) / len(full_text) * 100
    exp = german_freq[l] * 100
    diff = obs - exp
    marker = " !!" if abs(diff) > 2 else ""
    print(f"  {l}: {obs:.1f}% (exp {exp:.1f}%, diff {diff:+.1f}%){marker}")


# ================================================================
# PART 3: SEARCH ALL UNKNOWN CODES FOR O (expanded)
# ================================================================
print(f"\n{'='*70}")
print("ALL UNKNOWN CODES - O/B/F/R/L EVIDENCE")
print("=" * 70)

unknown_codes = sorted(set(pair_counts.keys()) - set(fixed.keys()),
                       key=lambda c: -pair_counts.get(c, 0))

test_words = {
    'O': ['NOCH', 'ODER', 'VON', 'DORT', 'WORT', 'OFT', 'GOTT',
          'GROSS', 'SOLL', 'WOHL', 'VOLK', 'GOLD', 'SOHN',
          'WORDEN', 'KONNTE', 'WOLLTE', 'SOLLTE', 'KOMMEN',
          'DOCH', 'HOCH', 'BODEN', 'OBEN', 'SONNE'],
    'B': ['ABER', 'BEI', 'BEIDE', 'BUCH', 'BERG', 'BIS',
          'HABEN', 'GEBEN', 'LEBEN', 'LIEBE', 'OBEN',
          'BESCHRIEBEN', 'BISHER', 'BALD', 'BEDEUTEN'],
    'F': ['AUF', 'FEST', 'FREI', 'OFT', 'DARF', 'KRAFT',
          'SCHRIFT', 'INSCHRIFT', 'FINDEN', 'FEUER', 'FREUND'],
    'R': ['DER', 'ODER', 'WIEDER', 'WERDEN', 'ANDERE', 'JEDER',
          'RICHTIG', 'DURCH', 'DREHT', 'RUNE', 'RUNEN'],
    'L': ['ALLE', 'SOLL', 'WELT', 'TEIL', 'VIEL', 'LANG',
          'WALD', 'ALLEIN', 'LESEN', 'LICHT', 'LEBEN'],
}

for code in unknown_codes:
    freq = pair_counts[code]
    if freq < 5:
        continue

    results = {}
    for letter, words in test_words.items():
        total = 0
        details = []
        for word in words:
            for pos in range(len(word)):
                if word[pos] == letter:
                    ct = test_word_in(word, code, pos, fixed)
                    if ct > 0:
                        total += ct
                        details.append(f"{word}:{ct}")
        if total > 0:
            results[letter] = (total, details)

    if results:
        best = max(results.items(), key=lambda x: x[1][0])
        print(f"\n  {code} (freq={freq}):")
        for letter, (total, details) in sorted(results.items(), key=lambda x: -x[1][0]):
            marker = " <-- BEST" if letter == best[0] else ""
            print(f"    {letter}: {total} hits [{', '.join(details[:5])}]{marker}")


# ================================================================
# PART 4: SPECIAL CHECK - NOCH, ODER, VON with ALL codes
# ================================================================
print(f"\n{'='*70}")
print("BRUTE FORCE: NOCH, ODER, VON, DORT, GOTT")
print("=" * 70)

# For each word, try every possible code for the O position
for word in ['NOCH', 'ODER', 'VON', 'DORT', 'GOTT', 'WORT', 'GROSS', 'DOCH', 'HOCH']:
    o_pos = word.index('O')
    hits_by_code = {}
    for code in pair_counts:
        ct = test_word_in(word, code, o_pos, fixed)
        if ct > 0:
            hits_by_code[code] = ct
    if hits_by_code:
        print(f"\n  {word} (O at pos {o_pos}):")
        for code, ct in sorted(hits_by_code.items(), key=lambda x: -x[1]):
            assigned = fixed.get(code, '?')
            status = f" [ASSIGNED={assigned}]" if code in fixed else f" [UNKNOWN, freq={pair_counts[code]}]"
            print(f"    code {code}: {ct} hits{status}")


print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
