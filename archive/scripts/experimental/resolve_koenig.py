"""
Resolve KOENIG conflict: Agent 2 vs Tier 8a/8b assignments.
Test both hypotheses against the full decoded text.

Hypothesis A (Tier 8): 22=D, 82=I, 73=?, 50=?, 84=?
Hypothesis B (Agent 2): 22=K, 82=O, 73=N, 50=I, 84=G

Key: whichever produces better German text wins.
"""
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

# Base: 71 codes from tier 7b (BEFORE the conflict)
base_codes = {
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
    '44': 'U', '62': 'B', '68': 'R',
}

# Non-conflicting tier 8 codes
shared_8 = {
    '23': 'S',  # ERSTE:8 — not part of conflict
    '17': 'E',  # Same in both hypotheses
    '29': 'E',  # TAUSEND — not part of conflict
    '66': 'A',  # DASS:9 — not part of conflict
    '49': 'E',  # HELFEN:2 — not part of conflict
    '38': 'K',  # KLAR:2 — not part of conflict
    '77': 'Z',  # ZU:5 — not part of conflict
}

# Hypothesis A (Tier 8): 22=D, 82=I
hyp_a = {**base_codes, **shared_8, '22': 'D', '82': 'I'}
# Hypothesis B (Agent 2 KOENIG): 22=K, 82=O, 73=N, 50=I, 84=G
hyp_b = {**base_codes, **shared_8, '22': 'K', '82': 'O', '73': 'N', '50': 'I', '84': 'G'}

# Build book pairs
book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

pair_counts = Counter()
for pairs in book_pairs:
    pair_counts.update(pairs)
total_pairs = sum(pair_counts.values())

def decode_text(codes):
    full = ''
    for bpairs in book_pairs:
        full += ''.join(codes.get(p, '?') for p in bpairs)
    return full

def count_words(text, words):
    hits = {}
    for w in words:
        ct = text.count(w)
        if ct > 0:
            hits[w] = ct
    return hits

def letter_freqs(codes):
    lf = Counter()
    for c, l in codes.items():
        lf[l] += pair_counts.get(c, 0)
    return lf

german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
}

# German word list for testing
test_words = [
    'RUNENSTEIN', 'INSCHRIFT', 'VERSCHIEDENE',
    'GESCHRIEBEN', 'SCHREIBEN', 'SCHRIFT',
    'VERSTEHEN', 'GEHEIMNIS', 'GEHEIME',
    'BIBLIOTHEK', 'ZWISCHEN',
    'STEINEN', 'STEINE', 'STEIN',
    'RUNEN', 'RUNE',
    'DIESER', 'DIESES', 'DIESEM', 'DIESEN', 'DIESE',
    'NICHT', 'NICHTS',
    'EINEN', 'EINER', 'EINE', 'EINEM',
    'ANDEREN', 'ANDERE',
    'WERDEN', 'WURDE', 'WORDEN',
    'HABEN', 'HATTE',
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
    'OFT', 'DOCH', 'HOCH',
    'FORT', 'GOLD', 'SOHN',
    'ERSTE', 'ERSTEN', 'ERDE', 'ERDEN',
    'TAUSEND', 'ALLES', 'ALLEN',
    'KLAR', 'ZU',
    'ZEICHEN', 'ZWEI', 'ZWISCHEN',
    'DIESEN', 'DESSEN', 'SEINEN', 'SEINES',
    'HELFEN', 'HELD', 'SCHNELL',
    # KOENIG-related words
    'KOENIG', 'KOENIGE', 'KOENIGS', 'KOENIGEN',
    'KOENIGIN', 'KOENIGLICH',
    'DERKOENIGIN', 'DERKOENIG',
    # Words affected by conflict
    'ERDE', 'ERDEN', 'WURDE', 'WORDEN',
    'DIE', 'DIES', 'DIESES',
    'ORT', 'ORTE', 'DORT',
    'ODER', 'OBEN',
    'GOLD', 'VOLK',
    'KEIN', 'KEINE', 'KEINEN',
    'KIND', 'KINDER',
    'KIRCHE', 'KLEIN',
    'DAZU', 'HIERZULANDE',
    # I words (to test 82=I vs 82=O and 50=I)
    'IMMER', 'IHREN', 'IHREM',
]

print("=" * 70)
print("KOENIG CONFLICT RESOLUTION TEST")
print("=" * 70)

text_a = decode_text(hyp_a)
text_b = decode_text(hyp_b)

known_a = sum(1 for c in text_a if c != '?')
known_b = sum(1 for c in text_b if c != '?')
print(f"\nHyp A (22=D,82=I): {len(hyp_a)} codes, {known_a}/{len(text_a)} known ({known_a/len(text_a)*100:.1f}%)")
print(f"Hyp B (22=K,82=O,73=N,50=I,84=G): {len(hyp_b)} codes, {known_b}/{len(text_b)} known ({known_b/len(text_b)*100:.1f}%)")

# Word comparison
print(f"\n{'='*70}")
print("WORD HITS COMPARISON")
print("=" * 70)

hits_a = count_words(text_a, test_words)
hits_b = count_words(text_b, test_words)

all_words = sorted(set(list(hits_a.keys()) + list(hits_b.keys())), key=lambda w: -max(hits_a.get(w,0), hits_b.get(w,0)))

print(f"\n{'Word':<20} {'Hyp A':>8} {'Hyp B':>8} {'Winner':>8}")
print("-" * 50)

score_a = 0
score_b = 0
for w in all_words:
    ca = hits_a.get(w, 0)
    cb = hits_b.get(w, 0)
    if ca == cb:
        winner = "TIE"
    elif ca > cb:
        winner = "A"
        score_a += (ca - cb) * len(w)
    else:
        winner = "B"
        score_b += (cb - ca) * len(w)
    if ca != cb or len(w) >= 5:
        print(f"  {w:<20} {ca:>6} {cb:>6}   {winner}")

print(f"\nWeighted word score: A={score_a}, B={score_b}")

# Bigram comparison
print(f"\n{'='*70}")
print("BIGRAM ANALYSIS")
print("=" * 70)

def bigram_counts(text):
    bg = Counter()
    for i in range(len(text) - 1):
        if text[i] != '?' and text[i+1] != '?':
            bg[text[i:i+2]] += 1
    return bg

bg_a = bigram_counts(text_a)
bg_b = bigram_counts(text_b)

# Check problematic bigrams
print("\nUnusual bigrams (should be LOW in German):")
for bg in ['KK', 'KI', 'IK', 'KD', 'DK', 'KH', 'HK', 'KN', 'NK',
           'OO', 'II', 'DD', 'EE', 'HH', 'NN', 'KE', 'EK',
           'IO', 'OI', 'DO', 'OD', 'GG', 'KG', 'GK']:
    ca = bg_a.get(bg, 0)
    cb = bg_b.get(bg, 0)
    if ca > 0 or cb > 0:
        print(f"  {bg}: A={ca:>3}, B={cb:>3}")

print("\nGood German bigrams (should be HIGH):")
for bg in ['DI', 'IE', 'DER', 'ER', 'EN', 'EI', 'CH', 'IN',
           'KO', 'OE', 'NI', 'IG', 'GE', 'ND', 'EG',
           'ON', 'NO', 'OR', 'RO', 'TO', 'OT', 'DO', 'OD',
           'RD', 'DR', 'DE', 'ED']:
    ca = bg_a.get(bg, 0)
    cb = bg_b.get(bg, 0)
    if ca > 0 or cb > 0:
        if ca != cb:
            print(f"  {bg}: A={ca:>3}, B={cb:>3}")

# Frequency comparison
print(f"\n{'='*70}")
print("FREQUENCY DEVIATION FROM GERMAN")
print("=" * 70)

lf_a = letter_freqs(hyp_a)
lf_b = letter_freqs(hyp_b)
total_a = sum(lf_a.values())
total_b = sum(lf_b.values())

print(f"\n{'Letter':<6} {'Exp%':>6} {'A_obs%':>8} {'A_diff':>8} {'B_obs%':>8} {'B_diff':>8} {'Better':>8}")
print("-" * 60)

total_dev_a = 0
total_dev_b = 0
for l in sorted(german_freq, key=lambda x: -german_freq[x]):
    exp = german_freq[l] * 100
    obs_a = lf_a.get(l, 0) / total_pairs * 100
    obs_b = lf_b.get(l, 0) / total_pairs * 100
    diff_a = obs_a - exp
    diff_b = obs_b - exp
    total_dev_a += abs(diff_a)
    total_dev_b += abs(diff_b)
    better = ""
    if abs(diff_a) < abs(diff_b) - 0.1:
        better = "A"
    elif abs(diff_b) < abs(diff_a) - 0.1:
        better = "B"
    if abs(diff_a) > 0.5 or abs(diff_b) > 0.5 or better:
        print(f"  {l:<4} {exp:>6.1f} {obs_a:>8.1f} {diff_a:>+8.1f} {obs_b:>8.1f} {diff_b:>+8.1f} {better:>8}")

print(f"\nTotal absolute deviation: A={total_dev_a:.1f}%, B={total_dev_b:.1f}%")
if total_dev_a < total_dev_b:
    print("-> Hypothesis A has better frequency match")
else:
    print("-> Hypothesis B has better frequency match")

# Context windows for disputed codes
print(f"\n{'='*70}")
print("CONTEXT WINDOWS FOR DISPUTED CODES")
print("=" * 70)

for code in ['22', '82', '73', '50', '84']:
    print(f"\nCode {code} (Hyp A: {hyp_a.get(code, '?')}, Hyp B: {hyp_b.get(code, '?')}):")
    contexts_a = []
    contexts_b = []
    for bpairs in book_pairs:
        for j, p in enumerate(bpairs):
            if p != code:
                continue
            # Get 3 pairs each side
            start = max(0, j-3)
            end = min(len(bpairs), j+4)
            window = bpairs[start:end]
            ctx_a = ''.join(hyp_a.get(pp, f'[{pp}]') for pp in window)
            ctx_b = ''.join(hyp_b.get(pp, f'[{pp}]') for pp in window)
            contexts_a.append(ctx_a)
            contexts_b.append(ctx_b)
    # Show first 10
    print(f"  Hyp A ({hyp_a.get(code, '?')}):")
    for c in contexts_a[:10]:
        print(f"    {c}")
    print(f"  Hyp B ({hyp_b.get(code, '?')}):")
    for c in contexts_b[:10]:
        print(f"    {c}")

# Special test: the KOENIG pattern in context
print(f"\n{'='*70}")
print("THE KOENIG PATTERN [22][82][17][73][50][84] IN FULL CONTEXT")
print("=" * 70)

# Find occurrences of the 6-code pattern
koenig_seq = ['22', '82', '17', '73', '50', '84']
for bidx, bpairs in enumerate(book_pairs):
    for j in range(len(bpairs) - 5):
        if bpairs[j:j+6] == koenig_seq:
            start = max(0, j-4)
            end = min(len(bpairs), j+10)
            window = bpairs[start:end]
            ctx_a = ''.join(hyp_a.get(pp, f'[{pp}]') for pp in window)
            ctx_b = ''.join(hyp_b.get(pp, f'[{pp}]') for pp in window)
            print(f"\n  Book {bidx}, pos {j}:")
            print(f"    Hyp A: {ctx_a}")
            print(f"    Hyp B: {ctx_b}")

# Test: does RD (from 22=D) vs RK (from 22=K) make sense?
print(f"\n{'='*70}")
print("SPECIFIC BIGRAM TEST: 22's NEIGHBORS")
print("=" * 70)

left_22 = Counter()
right_22 = Counter()
for bpairs in book_pairs:
    for j, p in enumerate(bpairs):
        if p != '22': continue
        if j > 0 and bpairs[j-1] in base_codes:
            left_22[base_codes[bpairs[j-1]]] += 1
        if j < len(bpairs)-1 and bpairs[j+1] in base_codes:
            right_22[base_codes[bpairs[j+1]]] += 1

print(f"Code 22 neighbors:")
print(f"  Left:  {dict(left_22.most_common(10))}")
print(f"  Right: {dict(right_22.most_common(10))}")
print(f"\n  If 22=D: RD={left_22.get('R',0)}, DE={right_22.get('E',0)}, DA={right_22.get('A',0)}, DN={right_22.get('N',0)}")
print(f"  If 22=K: RK={left_22.get('R',0)}(?), KE={right_22.get('E',0)}, KA={right_22.get('A',0)}, KN={right_22.get('N',0)}")
print(f"  German bigram ranks: RD=medium, DE=common, DA=common")
print(f"  German bigram ranks: RK=rare, KE=medium, KA=medium, KN=rare")

# ERDE test
print(f"\n{'='*70}")
print("ERDE vs ERKE TEST")
print("=" * 70)

# In hyp A: ER22E = ERDE
# In hyp B: ER22E = ERKE
erde_count_a = text_a.count('ERDE')
erke_count_b = text_b.count('ERKE')
print(f"  Hyp A: ERDE appears {erde_count_a} times (earth — real German word)")
print(f"  Hyp B: ERKE appears {erke_count_b} times (not a German word!)")

# DIE test
print(f"\nDIE count:")
die_a = text_a.count('DIE')
die_b = text_b.count('DIE')
print(f"  Hyp A: DIE={die_a}")
print(f"  Hyp B: DIE={die_b}")

# KOENIG test
koenig_a = text_a.count('DEINIG')  # What KOENIG becomes in hyp A
koenig_b = text_b.count('KOENIG')
print(f"\nKOENIG test:")
print(f"  Hyp A: the pattern becomes DEINIG (nonsense) = {text_a.count('DEINIG')}")
print(f"  Hyp B: KOENIG = {koenig_b}")

# But what about ERDE, ERDEN, DASS?
erde_b = text_b.count('ERDE')
erden_b = text_b.count('ERDEN')
erste_b = text_b.count('ERSTE')
print(f"\nERDE/ERDEN/ERSTE in Hyp B:")
print(f"  ERDE={erde_b}, ERDEN={erden_b}, ERSTE={erste_b}")
print(f"  (In Hyp A: ERDE={erde_count_a}, ERDEN={text_a.count('ERDEN')}, ERSTE={text_a.count('ERSTE')})")

# Summary judgment
print(f"\n{'='*70}")
print("SUMMARY")
print("=" * 70)

print(f"\nWord hit totals:")
total_hits_a = sum(hits_a.values())
total_hits_b = sum(hits_b.values())
long_hits_a = sum(v for w,v in hits_a.items() if len(w) >= 5)
long_hits_b = sum(v for w,v in hits_b.items() if len(w) >= 5)
print(f"  All words: A={total_hits_a}, B={total_hits_b}")
print(f"  Words 5+ chars: A={long_hits_a}, B={long_hits_b}")
print(f"  Frequency deviation: A={total_dev_a:.1f}%, B={total_dev_b:.1f}%")

print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
