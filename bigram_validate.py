"""Bigram frequency validation of the cipher mapping.
Compare decoded text bigrams against expected German bigram frequencies.
Also test impact of 16=O vs 16=I."""
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

# Top German bigrams (approximate frequency %)
# Source: various German corpora
german_bigrams_top = {
    'EN': 3.88, 'ER': 3.75, 'CH': 2.75, 'DE': 2.00, 'EI': 1.88,
    'ND': 1.88, 'TE': 1.67, 'IN': 1.67, 'IE': 1.57, 'GE': 1.43,
    'ES': 1.39, 'NE': 1.35, 'UN': 1.32, 'ST': 1.29, 'RE': 1.23,
    'HE': 1.19, 'AN': 1.16, 'AU': 1.05, 'SE': 1.03, 'DI': 1.02,
    'BE': 0.97, 'DE': 0.96, 'NG': 0.92, 'IC': 0.90, 'DA': 0.87,
    'SC': 0.86, 'ET': 0.81, 'IT': 0.79, 'NT': 0.79, 'IS': 0.76,
    'NI': 0.73, 'SI': 0.73, 'AL': 0.72, 'LE': 0.71, 'EL': 0.70,
    'RU': 0.68, 'TA': 0.67, 'NS': 0.67, 'SS': 0.65, 'RI': 0.63,
    'EC': 0.61, 'AS': 0.59, 'HA': 0.58, 'LI': 0.57, 'RS': 0.56,
    'ED': 0.55, 'WE': 0.54, 'SO': 0.53, 'DU': 0.51, 'AC': 0.50,
}

# Bigrams that should be RARE/IMPOSSIBLE in German
impossible_bigrams = ['II', 'UU', 'AA', 'QQ', 'XX', 'YY',
                      'QA', 'QE', 'QI', 'QO', 'QH', 'QN',
                      'XQ', 'YQ', 'ZQ']

def compute_bigrams(codes_map):
    """Compute bigram counts from decoded text using given code mapping."""
    bigrams = Counter()
    total = 0
    for bpairs in book_pairs:
        for i in range(len(bpairs) - 1):
            l1 = codes_map.get(bpairs[i])
            l2 = codes_map.get(bpairs[i+1])
            if l1 and l2:
                bigrams[l1 + l2] += 1
                total += 1
    return bigrams, total

def score_mapping(codes_map, label):
    """Score a mapping by comparing bigram frequencies to German."""
    bigrams, total = compute_bigrams(codes_map)

    # Score 1: Sum of squared deviations from expected German bigrams
    deviation_score = 0
    for bg, expected_pct in german_bigrams_top.items():
        observed = bigrams.get(bg, 0) / total * 100
        deviation_score += (observed - expected_pct) ** 2

    # Score 2: Count of impossible bigrams
    impossible_count = 0
    for bg in impossible_bigrams:
        impossible_count += bigrams.get(bg, 0)

    # Score 3: Count of double-letter bigrams
    doubles = 0
    for bg, cnt in bigrams.items():
        if bg[0] == bg[1]:
            doubles += cnt

    return deviation_score, impossible_count, doubles, bigrams, total

# Test current mapping vs 16=O
codes_16I = dict(all_codes)
codes_16O = {**all_codes, '16': 'O'}

# Also test with 39=E and 87=W added
codes_plus = {**all_codes, '39': 'E', '87': 'W'}
codes_plus_16O = {**codes_plus, '16': 'O'}

print("=" * 80)
print("BIGRAM FREQUENCY VALIDATION")
print("=" * 80)

for label, codes_map in [
    ("Current (16=I)", codes_16I),
    ("Test (16=O)", codes_16O),
    ("Current+39E+87W (16=I)", codes_plus),
    ("Full test (16=O, 39=E, 87=W)", codes_plus_16O),
]:
    dev, imp, dbl, bigrams, total = score_mapping(codes_map, label)
    print(f"\n{label}:")
    print(f"  Deviation score: {dev:.2f}")
    print(f"  Impossible bigrams: {imp}")
    print(f"  Double letters: {dbl}")
    print(f"  Total bigrams: {total}")

    # Show top bigrams vs expected
    print(f"  Top 15 bigrams:")
    for bg, cnt in bigrams.most_common(15):
        pct = cnt / total * 100
        expected = german_bigrams_top.get(bg, None)
        exp_str = f"(exp {expected:.1f}%)" if expected else "(not in top)"
        print(f"    {bg}: {pct:.2f}% {exp_str}  [{cnt}]")

    # Show all double-letter bigrams
    doubles_list = [(bg, cnt) for bg, cnt in bigrams.items() if bg[0] == bg[1] and cnt > 0]
    if doubles_list:
        doubles_list.sort(key=lambda x: -x[1])
        print(f"  Double-letter bigrams:")
        for bg, cnt in doubles_list:
            # Some doubles are OK in German: SS, EE, LL, NN, TT, RR, FF, MM, PP, BB, DD
            ok = bg in ['SS', 'EE', 'LL', 'NN', 'TT', 'RR', 'FF', 'MM', 'PP', 'BB', 'DD', 'CC', 'GG']
            flag = "" if ok else " <-- INVALID in German!"
            pct = cnt / total * 100
            print(f"    {bg}: {cnt} ({pct:.2f}%){flag}")

# Show bigrams that are MUCH higher or lower than expected
print(f"\n{'='*80}")
print("BIGGEST DEVIATIONS FROM GERMAN BIGRAMS (current mapping)")
print("=" * 80)

bigrams, total = compute_bigrams(codes_16I)
deviations = []
for bg, expected_pct in german_bigrams_top.items():
    observed = bigrams.get(bg, 0) / total * 100
    deviations.append((bg, observed, expected_pct, observed - expected_pct))

# Also check common bigrams we have that are NOT in the expected list
for bg, cnt in bigrams.most_common(30):
    if bg not in german_bigrams_top:
        observed = cnt / total * 100
        deviations.append((bg, observed, 0, observed))

deviations.sort(key=lambda x: -abs(x[3]))
print("\nBigrams with largest deviation from expected German frequency:")
for bg, obs, exp, delta in deviations[:25]:
    flag = " !!!" if abs(delta) > 0.5 else ""
    print(f"  {bg}: observed={obs:.2f}%, expected={exp:.2f}%, delta={delta:+.2f}%{flag}")

# SPECIFIC ANALYSIS: What bigrams would change with 16=O?
print(f"\n{'='*80}")
print("BIGRAM CHANGES if 16 switches from I to O")
print("=" * 80)

bigrams_I, _ = compute_bigrams(codes_16I)
bigrams_O, _ = compute_bigrams(codes_16O)

changed = set()
for bg in set(list(bigrams_I.keys()) + list(bigrams_O.keys())):
    if 'I' in bg or 'O' in bg:
        cnt_I = bigrams_I.get(bg, 0)
        cnt_O = bigrams_O.get(bg, 0)
        if cnt_I != cnt_O:
            changed.add(bg)

for bg in sorted(changed, key=lambda x: abs(bigrams_O.get(x, 0) - bigrams_I.get(x, 0)), reverse=True):
    cnt_I = bigrams_I.get(bg, 0)
    cnt_O = bigrams_O.get(bg, 0)
    exp = german_bigrams_top.get(bg, None)
    exp_str = f" (exp: {exp:.2f}%)" if exp else ""
    if cnt_I != cnt_O:
        print(f"  {bg}: {cnt_I} -> {cnt_O} ({cnt_O - cnt_I:+d}){exp_str}")
