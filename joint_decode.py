"""
Joint pattern scoring: test code assignments that must be consistent
across BOTH the 19-pair recurring pattern AND the pre-STEIN context.
Codes 78 and 51 appear in both patterns.
"""
import json
from collections import Counter
from itertools import product

with open('books.json', 'r') as f:
    books = json.load(f)

known = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U',
    '00': 'H', '14': 'N', '72': 'R', '91': 'S', '15': 'I',
    '76': 'E', '52': 'S', '42': 'D', '46': 'I', '48': 'N',
    '57': 'H', '04': 'M', '12': 'S', '58': 'N',
}

german_bigrams = {
    'EN': 3.88, 'ER': 3.75, 'CH': 2.75, 'DE': 2.00, 'EI': 1.88,
    'ND': 1.88, 'TE': 1.67, 'IN': 1.65, 'IE': 1.64, 'GE': 1.43,
    'ES': 1.36, 'NE': 1.26, 'SE': 1.20, 'RE': 1.18, 'HE': 1.16,
    'AN': 1.14, 'UN': 1.14, 'ST': 1.13, 'BE': 1.06, 'DI': 0.98,
    'EM': 0.93, 'AU': 0.93, 'SC': 0.86, 'DA': 0.86, 'SI': 0.82,
    'LE': 0.82, 'IC': 0.81, 'TI': 0.73, 'AL': 0.71, 'HA': 0.71,
    'NG': 0.67, 'WE': 0.65, 'EL': 0.65, 'HI': 0.58, 'NS': 0.57,
    'NT': 0.56, 'IS': 0.55, 'HT': 0.54, 'MI': 0.52, 'IT': 0.50,
    'RI': 0.41, 'AB': 0.38, 'LI': 0.35, 'ED': 0.35, 'EG': 0.34,
    'NI': 0.33, 'ET': 0.33, 'IG': 0.32, 'AR': 0.31, 'RU': 0.30,
    'LA': 0.29, 'BI': 0.27, 'FE': 0.26, 'ZU': 0.25, 'MA': 0.24,
    'OR': 0.23, 'WA': 0.22, 'SS': 0.22, 'RS': 0.21, 'RT': 0.20,
    'RD': 0.19, 'TA': 0.18, 'TH': 0.17, 'RN': 0.17, 'LS': 0.16,
}

german_words = set([
    'DER', 'DIE', 'DAS', 'UND', 'IST', 'EIN', 'EINE', 'EINEN', 'EINER',
    'DEN', 'DEM', 'DES', 'VON', 'HAT', 'AUF', 'MIT', 'SICH', 'SIND',
    'NICHT', 'STEIN', 'STEINE', 'STEINEN', 'RUNE', 'RUNEN',
    'DIESER', 'DIESE', 'DIESES', 'DIESEM', 'DIESEN',
    'NACH', 'NOCH', 'AUCH', 'ABER', 'ODER', 'ALLE', 'WENN', 'DANN',
    'SEIN', 'SEINE', 'SEINEN', 'SEINER', 'SEINES', 'SEINEM',
    'DURCH', 'GEGEN', 'UNTER', 'UEBER', 'HINTER',
    'URALTE', 'URALTEN', 'URALTER', 'URALTES',
    'KLEINE', 'KLEINEN', 'KLEINER',
    'ALTEN', 'ALTE', 'ALTER', 'ALTES',
    'INSCHRIFT', 'INSCHRIFTEN', 'SCHRIFT',
    'EINIGE', 'EINIGEN', 'EINIGER',
    'NEIN', 'KEIN', 'KEINE', 'KEINEN', 'KEINER',
    'ANDERE', 'ANDEREN', 'ANDERER',
    'IMMER', 'WIEDER', 'SCHON', 'NICHTS',
    'FREUNDE', 'FEINDE',
    'STEINER', 'STEINERN', 'STEINERNE',
])

def bigram_score(text):
    return sum(german_bigrams.get(text[i:i+2], 0) for i in range(len(text)-1))

def word_score(text):
    score = 0
    for word in german_words:
        n = text.count(word)
        score += n * len(word)  # weight by word length
    return score

# Pattern 1: 19-pair
# Codes: 45,21,76,52,19,72, 78, 30, 46,48,76, 51, 59, 56,46,11, 41, 45,19
# Known: D  I  E  S  E  R   ?   ?   I  N  E   ?   ?   E  I  N   ?   D  E
# Shared unknowns: 78, 51

# Pattern 2: Pre-STEIN
# Codes: 61, 51, 35, 34, 78, 01, 92,88,95,21,60
# Known: U   ?   ?   ?   ?   ?   S  T  E  I  N
# Shared unknowns: 78, 51

# Expanded candidates (include T and R explicitly)
cands = {
    '78': ['E', 'I', 'U', 'A', 'T', 'C'],
    '30': ['E', 'H', 'N', 'D', 'S', 'L'],
    '51': ['E', 'N', 'I', 'S', 'G', 'R', 'L'],
    '59': ['N', 'I', 'S', 'T', 'D', 'E'],
    '41': ['E', 'D', 'N', 'G', 'S'],
    '35': ['I', 'N', 'A', 'E', 'R', 'L'],
    '34': ['D', 'E', 'N', 'H', 'I', 'L', 'T'],
    '01': ['E', 'I', 'S', 'N', 'H'],
}

print("=" * 70)
print("JOINT SCORING: 19-PAIR + PRE-STEIN (consistent assignments)")
print("=" * 70)
print()

results = []

# Iterate over shared codes 78 and 51 first
for c78 in cands['78']:
    for c51 in cands['51']:
        # Pattern 2 specific: 35, 34, 01
        for c35 in cands['35']:
            for c34 in cands['34']:
                for c01 in cands['01']:
                    pre = f'U{c51}{c35}{c34}{c78}{c01}STEIN'
                    bs_pre = bigram_score(pre)
                    ws_pre = word_score(pre)

                    # Pattern 1 specific: 30, 59, 41
                    for c30 in cands['30']:
                        for c59 in cands['59']:
                            for c41 in cands['41']:
                                p19 = f'DIESER{c78}{c30}INE{c51}{c59}EIN{c41}DE'
                                bs_19 = bigram_score(p19)
                                ws_19 = word_score(p19)

                                total = (bs_pre + ws_pre * 3) + (bs_19 + ws_19 * 3)

                                if total > 80:  # threshold
                                    results.append((
                                        total, bs_pre, ws_pre, pre,
                                        bs_19, ws_19, p19,
                                        c78, c51, c35, c34, c01, c30, c59, c41
                                    ))

results.sort(key=lambda x: -x[0])

print(f"Found {len(results)} solutions above threshold 80")
print()

for i, (total, bsp, wsp, pre, bs19, ws19, p19,
        c78, c51, c35, c34, c01, c30, c59, c41) in enumerate(results[:30]):
    print(f"  {i+1}. JOINT SCORE: {total:.1f}")
    print(f"     Pre-STEIN:  {pre}  (bigrams={bsp:.1f}, words={wsp})")
    print(f"     19-pair:    {p19}  (bigrams={bs19:.1f}, words={ws19})")
    print(f"     SHARED: 78={c78}, 51={c51}")
    print(f"     Pre-only: 35={c35}, 34={c34}, 01={c01}")
    print(f"     19-only:  30={c30}, 59={c59}, 41={c41}")

    # Try to identify word boundaries in the 19-pair
    words_found = [w for w in german_words if w in p19]
    print(f"     Words in 19-pair: {sorted(words_found, key=len, reverse=True)[:8]}")
    words_pre = [w for w in german_words if w in pre]
    print(f"     Words in pre-STEIN: {sorted(words_pre, key=len, reverse=True)[:5]}")
    print()


# Also check extended context with top assignments
print(f"\n{'='*70}")
print("FULL EXTENDED CONTEXT WITH TOP ASSIGNMENTS")
print("=" * 70)

# Use top 5 solutions for extended context
for i, (total, bsp, wsp, pre, bs19, ws19, p19,
        c78, c51, c35, c34, c01, c30, c59, c41) in enumerate(results[:5]):

    # Add these to known temporarily
    trial = dict(known)
    trial['78'] = c78
    trial['51'] = c51
    trial['35'] = c35
    trial['34'] = c34
    trial['01'] = c01
    trial['30'] = c30
    trial['59'] = c59
    trial['41'] = c41

    # Decode extended context
    ext_codes = ['74','45','45','19','04','50','42','15','95','61',
                 '51','35','34','78','01','92','88','95','21','60',
                 '19','93','64','67','24','31','42','78','94','31',
                 '51','91','18','65','12']
    ext_decoded = ''.join(trial.get(c, f'[{c}]') for c in ext_codes)

    print(f"\n  Solution {i+1} (78={c78}, 51={c51}, 35={c35}, 34={c34}, 01={c01}):")
    print(f"  {ext_decoded}")

    # Also show a bigger context from a STEIN-containing book
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

    # Find first book with STEIN and decode with trial mapping
    for bi, book in enumerate(books):
        off = get_offset(book)
        pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
        decoded = ''.join(trial.get(p, '?') for p in pairs)
        if 'STEIN' in decoded and len(decoded) > 100:
            print(f"  Book {bi} ({len(decoded)} chars):")
            for j in range(0, min(len(decoded), 240), 80):
                print(f"    {decoded[j:j+80]}")
            break


# Count letter distribution for top solution
print(f"\n{'='*70}")
print("FREQUENCY CHECK FOR TOP SOLUTION")
print("=" * 70)
if results:
    _, _, _, _, _, _, _, c78, c51, c35, c34, c01, c30, c59, c41 = results[0]
    trial = dict(known)
    trial['78'] = c78; trial['51'] = c51; trial['35'] = c35
    trial['34'] = c34; trial['01'] = c01; trial['30'] = c30
    trial['59'] = c59; trial['41'] = c41

    # Count how many codes assigned to each letter
    letter_count = Counter()
    for code, letter in trial.items():
        letter_count[letter] += 1

    german_freq = {
        'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
        'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
        'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    }

    print(f"\nAssigned codes per letter (with new assignments):")
    for letter in sorted(letter_count, key=lambda l: -german_freq.get(l, 0)):
        expected = german_freq.get(letter, 0) * 98
        codes = [c for c, l in trial.items() if l == letter]
        print(f"  {letter}: {letter_count[letter]} codes (expected ~{expected:.0f}) = {sorted(codes)}")

print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
