"""
Tier 5 decoder: 52 + new T, A, G assignments.
Test whether the new assignments produce readable German.
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

# 52 confirmed codes
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

# Tier 5 candidates
tier5 = {
    '64': 'T',  # HT:11, NT:20, IT:11, TI:16, TR:11 — strong T profile
    '89': 'A',  # DAS=28 hits, S-right 96%
    '80': 'G',  # NG=47 (N-left 77%)
    '97': 'G',  # IG=44 (I-left 76%)
    '75': 'T',  # ST=19, broad bigram fit
}

all_codes = {**fixed, **tier5}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

pair_counts = Counter()
for pairs in book_pairs:
    pair_counts.update(pairs)
total_pairs = sum(pair_counts.values())

print("=" * 70)
print(f"TIER 5 DECODER: {len(all_codes)} fixed codes")
print("=" * 70)

# Frequency check
german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
}

letter_freq = Counter()
for c, l in all_codes.items():
    letter_freq[l] += pair_counts.get(c, 0)

known_total = sum(pair_counts[c] for c in all_codes)
unknown_total = total_pairs - known_total

print(f"\nKnown: {known_total}/{total_pairs} ({known_total/total_pairs*100:.1f}%)")
print(f"Unknown: {unknown_total}/{total_pairs} ({unknown_total/total_pairs*100:.1f}%)")

print(f"\nLetter frequencies (57 fixed codes):")
for l in sorted(german_freq, key=lambda x: -german_freq[x]):
    obs = letter_freq.get(l, 0) / total_pairs * 100
    exp = german_freq[l] * 100
    diff = obs - exp
    n_codes = sum(1 for c in all_codes if all_codes[c] == l)
    marker = " !!" if abs(diff) > 2 else ""
    print(f"  {l}: {obs:.1f}% (exp {exp:.1f}%, diff {diff:+.1f}%, {n_codes} codes){marker}")


# Decode books
print(f"\n{'='*70}")
print("DECODED BOOKS (longest)")
print("=" * 70)

book_decoded = []
for i, pairs in enumerate(book_pairs):
    decoded = ''.join(all_codes.get(p, f'[{p}]') for p in pairs)
    book_decoded.append((i, decoded, len(pairs)))

book_decoded.sort(key=lambda x: -x[2])

for idx, decoded, length in book_decoded[:6]:
    print(f"\n  Book {idx} ({length} pairs):")
    for j in range(0, len(decoded), 90):
        print(f"    {decoded[j:j+90]}")


# Word counting
print(f"\n{'='*70}")
print("GERMAN WORD HITS")
print("=" * 70)

# Concatenate all decoded text
full_text = ''
for pairs in book_pairs:
    full_text += ''.join(all_codes.get(p, '?') for p in pairs)

german_words = [
    'RUNENSTEIN', 'RUNENSTEINEN', 'INSCHRIFT', 'INSCHRIFTEN',
    'URALTE', 'URALTEN', 'URALTER',
    'ZWISCHEN', 'VERSCHIEDENE', 'VERSCHIEDENEN',
    'GESCHRIEBEN', 'SCHREIBEN', 'SCHRIFT',
    'VERSTEHEN', 'VERSTANDEN',
    'GEHEIMNIS', 'GEHEIME',
    'BIBLIOTHEK',
    'STEINEN', 'STEINE', 'STEIN',
    'RUNEN', 'RUNE',
    'DIESER', 'DIESES', 'DIESEM', 'DIESEN', 'DIESE',
    'NICHT', 'NICHTS',
    'EINEN', 'EINER', 'EINE', 'EINEM',
    'ANDEREN', 'ANDERE', 'ANDERER',
    'WERDEN', 'WURDE', 'WORDEN', 'WERDEN',
    'HABEN', 'HATTE', 'HATTEN',
    'KONNTE', 'KOENNEN', 'KANN',
    'MUSSTE', 'SOLLTE', 'WOLLTE',
    'DURCH', 'GEGEN', 'UNTER', 'HINTER',
    'IMMER', 'WIEDER', 'SCHON', 'NOCH',
    'GROSS', 'KLEIN', 'LANG',
    'MACHT', 'KRAFT', 'GEIST',
    'LICHT', 'DUNKEL', 'NACHT',
    'WISSEN', 'KENNEN', 'SEHEN',
    'ALLE', 'JEDER', 'JEDES', 'JEDE',
    'AUCH', 'ABER', 'ODER', 'WENN', 'DANN', 'DENN',
    'GANZ', 'SEHR', 'VIEL', 'WENIG',
    'SICH', 'SIND', 'SEIN', 'SEINE',
    'DASS', 'HIER', 'DORT', 'WELT',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES',
    'UND', 'IST', 'EIN', 'WIR', 'ICH', 'SIE',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI',
    'NUR', 'WAS', 'MAN', 'WER', 'WIE', 'GUT',
    'TAG', 'TEIL', 'ZEIT', 'WORT', 'NAME',
]

print(f"\nWord hits in decoded text:")
word_hits = {}
for word in sorted(set(german_words), key=lambda w: -len(w)):
    ct = full_text.count(word)
    if ct > 0:
        word_hits[word] = ct

# Sort by word length * count (impact)
for word, ct in sorted(word_hits.items(), key=lambda x: -len(x[0]) * x[1]):
    if ct >= 2 or len(word) >= 6:
        print(f"  {word}: {ct}")


# Show the URALTE STEINE context
print(f"\n{'='*70}")
print("EXTENDED CONTEXTS")
print("=" * 70)

# Find URALTE STEINE
for i, pairs in enumerate(book_pairs):
    target = ['61', '51', '35', '34', '78', '01', '92', '88', '95', '21', '60']
    for j in range(len(pairs) - len(target)):
        if pairs[j:j+len(target)] == target:
            start = max(0, j - 20)
            end = min(len(pairs), j + len(target) + 20)
            ctx = pairs[start:end]
            decoded = ''.join(all_codes.get(p, f'[{p}]') for p in ctx)
            print(f"\n  Book {i}, URALTE STEINE context:")
            print(f"    {decoded}")
            break

# Show 19-pair pattern
p19 = ['45','21','76','52','19','72','78','30','46','48','76','51','59','56','46','11','41','45','19']
decoded_19 = ''.join(all_codes.get(c, f'[{c}]') for c in p19)
print(f"\n  19-pair pattern: {decoded_19}")


# Look for NEW words enabled by tier 5
print(f"\n{'='*70}")
print("NEW WORDS ENABLED BY TIER 5 (T, A, G codes)")
print("=" * 70)

# Test NICHT specifically
nicht_count = full_text.count('NICHT')
print(f"  NICHT: {nicht_count}")
print(f"  MACHT: {full_text.count('MACHT')}")
print(f"  NACHT: {full_text.count('NACHT')}")
print(f"  LICHT: {full_text.count('LICHT')}")
print(f"  RECHT: {full_text.count('RECHT')}")
print(f"  GEGEN: {full_text.count('GEGEN')}")
print(f"  GEIST: {full_text.count('GEIST')}")
print(f"  GUT: {full_text.count('GUT')}")
print(f"  LANG: {full_text.count('LANG')}")
print(f"  TAG: {full_text.count('TAG')}")
print(f"  RICHTIG: {full_text.count('RICHTIG')}")
print(f"  EWIG: {full_text.count('EWIG')}")
print(f"  EINIGE: {full_text.count('EINIGE')}")
print(f"  WENIGE: {full_text.count('WENIGE')}")
print(f"  DAS: {full_text.count('DAS')}")
print(f"  DASS: {full_text.count('DASS')}")
print(f"  WAS: {full_text.count('WAS')}")
print(f"  TEIL: {full_text.count('TEIL')}")


# Check for problematic bigrams (unlikely in German)
print(f"\n{'='*70}")
print("VALIDATION: UNUSUAL BIGRAMS")
print("=" * 70)

# Count all bigrams in decoded text
bigram_counts = Counter()
for i in range(len(full_text) - 1):
    if full_text[i] != '?' and full_text[i+1] != '?':
        bigram_counts[full_text[i:i+2]] += 1

# Flag unusual German bigrams
unusual = ['GG', 'GS', 'TG', 'GT', 'GN', 'GD', 'GA', 'GO',
           'TT', 'AA', 'DD', 'HH', 'UU', 'II', 'NN']
for bg in unusual:
    ct = bigram_counts.get(bg, 0)
    if ct > 5:
        print(f"  {bg}: {ct} times (check if excessive)")

# Also check NG and IG specifically
print(f"\n  NG: {bigram_counts.get('NG', 0)} (expected common)")
print(f"  IG: {bigram_counts.get('IG', 0)} (expected common)")
print(f"  GE: {bigram_counts.get('GE', 0)} (expected common)")
print(f"  ST: {bigram_counts.get('ST', 0)} (expected common)")
print(f"  EN: {bigram_counts.get('EN', 0)} (expected very common)")
print(f"  ER: {bigram_counts.get('ER', 0)} (expected very common)")
print(f"  CH: {bigram_counts.get('CH', 0)} (expected common)")

# Show top 20 bigrams
print(f"\nTop 20 bigrams:")
for bg, ct in bigram_counts.most_common(20):
    german_expected = {'EN': 3.88, 'ER': 3.75, 'CH': 2.75, 'DE': 2.00,
                       'EI': 1.88, 'ND': 1.88, 'TE': 1.67, 'IN': 1.65,
                       'IE': 1.64, 'GE': 1.43, 'ES': 1.36, 'NE': 1.26,
                       'SE': 1.20, 'RE': 1.18, 'HE': 1.16, 'AN': 1.14,
                       'UN': 1.14, 'ST': 1.13, 'BE': 1.06, 'DI': 0.98}
    exp = german_expected.get(bg, 0)
    known_chars = sum(1 for c in full_text if c != '?')
    obs_pct = ct / max(1, known_chars - 1) * 100
    marker = " <--" if exp > 0 else ""
    print(f"  {bg}: {ct} ({obs_pct:.2f}%){marker}")

print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
