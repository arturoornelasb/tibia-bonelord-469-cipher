"""
Tier 7 decoder: 62 + new high-confidence assignments.
Focus: Fill E deficit (4.2%), add C, resolve N ambiguity.
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

# Tiers 1-6: 62 confirmed codes
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
}

# Tier 7: high-confidence E codes + C + N
# E deficit: need ~235 more pairs. 67(96)+27(73)+03(52)+09(41)=262 -> fills deficit.
tier7 = {
    '67': 'E',  # TE=47, EI=16, EL=12, EN=11 — all top German bigrams, conf 2.3
    '27': 'E',  # DE=24, GE=21, HE=9, NE=8 — GE prefix, conf 2.9
    '03': 'E',  # GE=35 (70%!) — overwhelmingly GE-prefix, conf 2.8
    '09': 'E',  # GE=12, DE=8, ER=10, EF=6 — conf 6.1
    '05': 'C',  # CH=17 on right — clearly C (matches 18=C pattern), conf 1.2
    '53': 'N',  # ND=25 on right (68%), UND:6 word hits; despite E word evidence
}

all_codes = {**fixed, **tier7}

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
print(f"TIER 7 DECODER: {len(all_codes)} fixed codes")
print("=" * 70)

# Frequency check
german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
}

letter_freq = Counter()
for c, l in all_codes.items():
    letter_freq[l] += pair_counts.get(c, 0)

known_total = sum(pair_counts[c] for c in all_codes)
unknown_total = total_pairs - known_total

print(f"\nKnown: {known_total}/{total_pairs} ({known_total/total_pairs*100:.1f}%)")
print(f"Unknown: {unknown_total}/{total_pairs} ({unknown_total/total_pairs*100:.1f}%)")

print(f"\nLetter frequencies ({len(all_codes)} codes):")
for l in sorted(german_freq, key=lambda x: -german_freq[x]):
    obs = letter_freq.get(l, 0) / total_pairs * 100
    exp = german_freq[l] * 100
    diff = obs - exp
    n_codes = sum(1 for c in all_codes if all_codes[c] == l)
    marker = " !!" if abs(diff) > 2 else ""
    print(f"  {l}: {obs:.1f}% (exp {exp:.1f}%, diff {diff:+.1f}%, {n_codes} codes){marker}")


# Decode full text
full_text = ''
for bpairs in book_pairs:
    full_text += ''.join(all_codes.get(p, '?') for p in bpairs)

known_pct = sum(1 for c in full_text if c != '?') / len(full_text) * 100
print(f"\nText known: {known_pct:.1f}%")


# Decode books
print(f"\n{'='*70}")
print("DECODED BOOKS (longest)")
print("=" * 70)

book_decoded = []
for i, bpairs in enumerate(book_pairs):
    decoded = ''.join(all_codes.get(p, f'[{p}]') for p in bpairs)
    book_decoded.append((i, decoded, len(bpairs)))

book_decoded.sort(key=lambda x: -x[2])

for idx, decoded, length in book_decoded[:10]:
    print(f"\n  Book {idx} ({length} pairs):")
    for j in range(0, len(decoded), 90):
        print(f"    {decoded[j:j+90]}")


# Word counting
print(f"\n{'='*70}")
print("GERMAN WORD HITS")
print("=" * 70)

german_words = [
    'RUNENSTEIN', 'INSCHRIFT', 'INSCHRIFTEN',
    'URALTE', 'URALTEN', 'VERSCHIEDENE',
    'GESCHRIEBEN', 'SCHREIBEN', 'SCHRIFT',
    'VERSTEHEN', 'GEHEIMNIS', 'GEHEIME',
    'BIBLIOTHEK', 'ZWISCHEN',
    'STEINEN', 'STEINE', 'STEIN',
    'RUNEN', 'RUNE',
    'DIESER', 'DIESES', 'DIESEM', 'DIESEN', 'DIESE',
    'NICHT', 'NICHTS',
    'EINEN', 'EINER', 'EINE', 'EINEM',
    'ANDEREN', 'ANDERE', 'ANDERER',
    'WERDEN', 'WURDE', 'WORDEN',
    'HABEN', 'HATTE', 'HATTEN',
    'KONNTE', 'KOENNEN', 'KANN',
    'MUSSTE', 'SOLLTE', 'WOLLTE',
    'DURCH', 'GEGEN', 'UNTER', 'HINTER',
    'IMMER', 'WIEDER', 'SCHON', 'NOCH',
    'MACHT', 'KRAFT', 'GEIST',
    'LICHT', 'DUNKEL', 'NACHT',
    'WISSEN', 'KENNEN', 'SEHEN', 'FINDEN',
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
    'OFT', 'DOCH', 'HOCH', 'SOLCH', 'WELCH',
    'FORT', 'SORT', 'MILCH', 'VOLK', 'GOLD', 'SOHN',
    # New: words enabled by more E and C codes
    'GESCHICHTEN', 'GESCHICHTE',
    'GEHEIMEN', 'GEHEIMNISSE',
    'ENTDECKEN', 'ENTDECKT',
    'VERSCHIEDENEN', 'VERSCHIEDENER',
    'VERGESSEN', 'VERGESSENE',
    'GEWESEN', 'GEWESENEN',
    'BESONDERE', 'BESONDERS',
    'GEWOEHNLICH',
    'GEFUNDEN', 'GEFUNDENE',
    'GESCHRIEBEN',
    'GELESEN', 'GELERNT',
    'GEGEBEN', 'GENOMMEN',
    'GESEHEN', 'GESAGT',
    'GEMACHT',
    'BESTIMMTE', 'BESTIMMTEN',
    'BESCHRIEBEN',
    'BENUTZEN', 'BENUTZT',
    'SCHEINT', 'SCHEINEN',
]

word_hits = {}
for word in sorted(set(german_words), key=lambda w: -len(w)):
    ct = full_text.count(word)
    if ct > 0:
        word_hits[word] = ct

print(f"\nTotal unique words found: {len(word_hits)}")
for word, ct in sorted(word_hits.items(), key=lambda x: -len(x[0]) * x[1]):
    if ct >= 2 or len(word) >= 5:
        print(f"  {word}: {ct}")


# Bigram validation
print(f"\n{'='*70}")
print("BIGRAM VALIDATION")
print("=" * 70)

bigram_counts = Counter()
for i in range(len(full_text) - 1):
    if full_text[i] != '?' and full_text[i+1] != '?':
        bigram_counts[full_text[i:i+2]] += 1

print("\nPotentially unusual bigrams:")
unusual = ['EE', 'CC', 'RR', 'FF', 'LL', 'OO', 'AA',
           'II', 'HH', 'DD', 'NN',
           'EC', 'CE', 'GC', 'CG']
for bg in unusual:
    ct = bigram_counts.get(bg, 0)
    if ct > 0:
        print(f"  {bg}: {ct}")

print(f"\nTop 25 bigrams:")
for bg, ct in bigram_counts.most_common(25):
    obs_pct = ct / sum(bigram_counts.values()) * 100
    print(f"  {bg}: {ct} ({obs_pct:.2f}%)")


# Remaining unknown analysis
print(f"\n{'='*70}")
print("REMAINING UNKNOWN CODES")
print("=" * 70)

unknown_codes = sorted(set(pair_counts.keys()) - set(all_codes.keys()),
                       key=lambda c: -pair_counts.get(c, 0))
print(f"\n{len(unknown_codes)} unknown codes, {unknown_total} total pairs ({unknown_total/total_pairs*100:.1f}%)")

print(f"\nFrequency deficits remaining:")
for l in sorted(german_freq, key=lambda l: german_freq[l] - letter_freq.get(l,0)/total_pairs):
    obs = letter_freq.get(l, 0) / total_pairs * 100
    exp = german_freq[l] * 100
    diff = exp - obs
    if diff > 0.3:
        need = diff / 100 * total_pairs
        print(f"  {l}: obs={obs:.1f}% exp={exp:.1f}% deficit={diff:.1f}% (need ~{need:.0f} pairs)")

print(f"\nRemaining unknown codes (freq>=5):")
for c in unknown_codes:
    freq = pair_counts[c]
    if freq >= 5:
        left = Counter()
        right = Counter()
        for bpairs in book_pairs:
            for j, p in enumerate(bpairs):
                if p != c:
                    continue
                if j > 0 and bpairs[j-1] in all_codes:
                    left[all_codes[bpairs[j-1]]] += 1
                if j < len(bpairs)-1 and bpairs[j+1] in all_codes:
                    right[all_codes[bpairs[j+1]]] += 1
        print(f"  {c} (freq={freq}): L={dict(left.most_common(5))} R={dict(right.most_common(5))}")


# Test if NICHT appears now
print(f"\n{'='*70}")
print("KEY WORD TESTS")
print("=" * 70)

for word in ['NICHT', 'NOCH', 'ODER', 'ABER', 'AUCH', 'ZWISCHEN',
             'GESCHRIEBEN', 'GEHEIMNIS', 'VERSCHIEDENE', 'INSCHRIFT',
             'RUNENSTEIN', 'BESCHRIEBEN', 'ENTDECKEN',
             'GEMACHT', 'GESEHEN', 'GEWESEN', 'GEGEBEN',
             'VERGESSEN', 'GEFUNDEN', 'GELESEN',
             'BESTIMMTE', 'BESONDERE',
             'SCHEINT', 'KENNEN', 'WISSEN',
             'ICH', 'SIE', 'WIR', 'SIND', 'SEIN',
             'DIESE', 'JEDER', 'ALLE']:
    ct = full_text.count(word)
    if ct > 0:
        print(f"  {word}: {ct}")


# SEARCH: what comes after GE (past participle prefix)?
print(f"\n{'='*70}")
print("GE- PREFIX ANALYSIS (past participles)")
print("=" * 70)

ge_follows = Counter()
for bpairs in book_pairs:
    for j in range(len(bpairs) - 2):
        # Look for G+E pair followed by something
        if bpairs[j] in all_codes and all_codes[bpairs[j]] == 'G':
            if bpairs[j+1] in all_codes and all_codes[bpairs[j+1]] == 'E':
                if bpairs[j+2] in all_codes:
                    ge_follows[all_codes[bpairs[j+2]]] += 1
                else:
                    ge_follows[f'[{bpairs[j+2]}]'] += 1

print("After GE-:")
for ch, ct in ge_follows.most_common(20):
    print(f"  GE{ch}: {ct}")


# What comes before CH?
print(f"\n{'='*70}")
print("_CH ANALYSIS")
print("=" * 70)

ch_before = Counter()
for bpairs in book_pairs:
    for j in range(1, len(bpairs) - 1):
        if bpairs[j] in all_codes and all_codes[bpairs[j]] == 'C':
            if bpairs[j+1] in all_codes and all_codes[bpairs[j+1]] == 'H':
                if bpairs[j-1] in all_codes:
                    ch_before[all_codes[bpairs[j-1]]] += 1
                else:
                    ch_before[f'[{bpairs[j-1]}]'] += 1

print("Before _CH:")
for ch, ct in ch_before.most_common(20):
    print(f"  {ch}CH: {ct}")


print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
