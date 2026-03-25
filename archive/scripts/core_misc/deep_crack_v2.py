"""
Deep Crack V2: Test reassigning codes 24 and 71.
- Code 24: I->R showed +39 chars improvement
- Code 71: I->N showed +27 chars improvement
Also: formal test of code 33=W, EILABRRNI analysis, MHG vocabulary.
"""
import json
import os
import re
from collections import Counter

data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

# Current best mapping (v2)
with open(os.path.join(data_dir, 'final_mapping_v2.json'), 'r') as f:
    base_mapping = json.load(f)

# Extended German dictionary including Middle High German
WORDS = set("""
ab aber alle allem allen aller alles als also alt alte altem alten alter altes am an andere
anderem anderen anderer anderes ans auch auf aus
bei beim bis bisher da dabei damit dann das dass de dem den denen denn
der deren des dessen die dies diese diesem diesen dieser dieses dir doch dort durch
ein eine einem einen einer einige einiger einiges einst em en ende er erde erst erste
ersten erster erstes es etwa etwas
fach fand fest finden fuer ganz gar geh geheim gehen gegen geben gibt ging gott gross gut
hab habe haben hat heer her herr hier hin
ich ihm ihn ihr ihre ihrem ihren ihrer im in ins ist
ja jede jedem jeden jeder jedes klar koenig koenige koenigen koenigs kommen kam kann
lang lage land lande last leid
macht mehr mein meine meinem meinen meiner min mir mit muss
nach nacht nah nahe name namen neben neu neue neuem neuen neuer neues nicht nichts noch
nun nur ob oder ohne ort orte orten
rat rede reden rein rest ruin rune runen runeort
see sehr sei seid sein seine seinem seinen seiner seit
sie sind so soll sollen sonne steil stein steine steinen stieg
tag tage tagen teil teile teilen tod tot tun tut
ueber um und uns unter uralte uralten
vier viel viele vielen vom von vor
wahr wahrheit war was wasser weg weil welt wenn wer wie wir wird wissen wo wohl wort
zeichen zeit zu zum zur zwei zwischen
schwiteio tharsc totniurg hearuchtiger aunrsongetrases labgzeras labge
finden dass dieser dieses fach nach aus tun ab des geh erde enden
gem steil koenigs tag tage nacht orte orten erste schau
drei rede teil lande heim heil tod ruh ruhe burg hort
neid grab acht
dein deine deinem deinen deiner
kein keine keinem keinen keiner
tat taten
heer heere
berg berge bergen
feld stein grab tod
bund bunde bundes
sache sachen
macht maechte
kraft
wort worte worten
end enden
licht stern
dunkel norden sueden osten westen
alt alte alten alter altes
buch buecher
schrift zeichen
rune runen
knochen gebein
hoch hohe hohem hohen hoher hohes
tief tiefe tiefem tiefen tiefer tiefes
weit weite weitem weiten weiter weites
""".split())

# Also add Middle High German terms
MHG_WORDS = set("""
diu daz waz hie unde niht ouch uber wart
sint sint wirt mit ist von dar dan
sach sprach unt swie
her herre vrouwe ritter knecht
groz grozze grozzen
kunic kunec kunig
burge burc stat lant
tot tode toten
alt alten alte
niuwe niuwan
stein steine steinen
grunt grunde
hort horte
ere eren
tugent tugende
vri vrie
gie gienc
""".split())

ALL_WORDS = WORDS | MHG_WORDS

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

def decode_book(book, m):
    offset = get_offset(book)
    pairs = [book[j:j+2] for j in range(offset, len(book)-1, 2)]
    return ''.join(m.get(p, '?') for p in pairs)

def get_pairs(book):
    offset = get_offset(book)
    return [book[j:j+2] for j in range(offset, len(book)-1, 2)]

def measure_coverage(text, words=ALL_WORDS):
    """Greedy longest-match word coverage."""
    covered = 0
    text_lower = text.lower()
    used = [False] * len(text_lower)
    max_wl = max(len(w) for w in words) if words else 0
    for length in range(max_wl, 1, -1):
        for word in words:
            if len(word) != length:
                continue
            pos = 0
            while True:
                p = text_lower.find(word, pos)
                if p == -1:
                    break
                if not any(used[p:p+len(word)]):
                    for k in range(p, p+len(word)):
                        used[k] = True
                    covered += len(word)
                pos = p + 1
    return covered, used

def word_parse(text, words=ALL_WORDS):
    """DP word segmentation returning list of (word, start, end)."""
    n = len(text)
    t = text.lower()
    dp = [0] * (n + 1)
    back = [None] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]  # skip char
        back[i] = ('skip', i-1)
        for w in words:
            wl = len(w)
            if i >= wl and t[i-wl:i] == w:
                score = dp[i-wl] + wl * wl  # favor longer words
                if score > dp[i]:
                    dp[i] = score
                    back[i] = (w, i-wl)
    # Trace back
    result = []
    pos = n
    while pos > 0:
        action, prev = back[pos]
        if action == 'skip':
            pos = prev
        else:
            result.append((action.upper(), prev, pos))
            pos = prev
    result.reverse()
    return result

# ============================================================
# 1. TEST CODE 24=R AND CODE 71=N (INDIVIDUALLY AND COMBINED)
# ============================================================
print("=" * 80)
print("1. DEEP TEST: CODE 24 AND CODE 71 REASSIGNMENT")
print("=" * 80)

# Baseline
base_total = 0
for book in books:
    dec = decode_book(book, base_mapping)
    cov, _ = measure_coverage(dec)
    base_total += cov
print(f"\nBaseline (all current): {base_total} chars covered")

# Test 24=R only
m24r = dict(base_mapping)
m24r['24'] = 'R'
total_24r = 0
for book in books:
    dec = decode_book(book, m24r)
    cov, _ = measure_coverage(dec)
    total_24r += cov
print(f"Code 24=R: {total_24r} chars (+{total_24r - base_total})")

# Test 71=N only
m71n = dict(base_mapping)
m71n['71'] = 'N'
total_71n = 0
for book in books:
    dec = decode_book(book, m71n)
    cov, _ = measure_coverage(dec)
    total_71n += cov
print(f"Code 71=N: {total_71n} chars (+{total_71n - base_total})")

# Test BOTH 24=R and 71=N
m_both = dict(base_mapping)
m_both['24'] = 'R'
m_both['71'] = 'N'
total_both = 0
for book in books:
    dec = decode_book(book, m_both)
    cov, _ = measure_coverage(dec)
    total_both += cov
print(f"Both 24=R + 71=N: {total_both} chars (+{total_both - base_total})")

# Also test 24=R + 71=N + 33=W
m_all3 = dict(m_both)
m_all3['33'] = 'W'
total_all3 = 0
for book in books:
    dec = decode_book(book, m_all3)
    cov, _ = measure_coverage(dec)
    total_all3 += cov
print(f"24=R + 71=N + 33=W: {total_all3} chars (+{total_all3 - base_total})")

# ============================================================
# 2. CONTEXTUAL ANALYSIS: What words does 24=R create?
# ============================================================
print(f"\n\n{'='*80}")
print("2. WHAT NEW WORDS DOES CODE 24=R CREATE?")
print(f"{'='*80}")

for i, book in enumerate(books):
    pairs = get_pairs(book)
    for k, p in enumerate(pairs):
        if p == '24':
            # Get context with current (I) and proposed (R)
            ctx_base = ''.join(base_mapping.get(pairs[j], '?') for j in range(max(0,k-5), min(len(pairs), k+6)))
            ctx_new = ''.join(m_both.get(pairs[j], '?') for j in range(max(0,k-5), min(len(pairs), k+6)))
            if ctx_base != ctx_new:
                # Find words in new context
                words_new = word_parse(ctx_new)
                word_strs = [w for w, s, e in words_new]
                if word_strs:
                    print(f"  Book {i:2d} pos {k:3d}: {ctx_base} => {ctx_new}  words: {' '.join(word_strs)}")

# ============================================================
# 3. CONTEXTUAL ANALYSIS: What words does 71=N create?
# ============================================================
print(f"\n\n{'='*80}")
print("3. WHAT NEW WORDS DOES CODE 71=N CREATE?")
print(f"{'='*80}")

for i, book in enumerate(books):
    pairs = get_pairs(book)
    for k, p in enumerate(pairs):
        if p == '71':
            ctx_base = ''.join(base_mapping.get(pairs[j], '?') for j in range(max(0,k-5), min(len(pairs), k+6)))
            ctx_new = ''.join(m_both.get(pairs[j], '?') for j in range(max(0,k-5), min(len(pairs), k+6)))
            if ctx_base != ctx_new:
                words_new = word_parse(ctx_new)
                word_strs = [w for w, s, e in words_new]
                if word_strs:
                    print(f"  Book {i:2d} pos {k:3d}: {ctx_base} => {ctx_new}  words: {' '.join(word_strs)}")

# ============================================================
# 4. LETTER FREQUENCY WITH PROPOSED CHANGES
# ============================================================
print(f"\n\n{'='*80}")
print("4. LETTER FREQUENCY COMPARISON")
print(f"{'='*80}")

german_expected = {
    'E': 16.93, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
    'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
    'L': 3.44, 'G': 3.01, 'O': 2.51, 'C': 2.73, 'M': 2.53,
    'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
    'V': 0.84, 'P': 0.67
}

for label, mapping in [("Current", base_mapping), ("With 24=R+71=N", m_both)]:
    all_text = ''
    for book in books:
        all_text += decode_book(book, mapping)
    all_text = all_text.replace('?', '')
    total_chars = len(all_text)
    freq = Counter(all_text)

    print(f"\n  {label}:")
    print(f"  {'Letter':>6} {'Count':>6} {'Actual%':>8} {'Expected%':>10} {'Diff':>8}")
    for letter in 'ENISRATDHULGOMCWFKZBV':
        count = freq.get(letter, 0)
        actual_pct = count / total_chars * 100 if total_chars > 0 else 0
        expected_pct = german_expected.get(letter, 0)
        diff = actual_pct - expected_pct
        flag = " <--" if abs(diff) > 2.0 else ""
        print(f"  {letter:>6} {count:>6} {actual_pct:>7.1f}% {expected_pct:>9.1f}% {diff:>+7.1f}%{flag}")

# ============================================================
# 5. EILABRRNI / LABYRINTH INVESTIGATION
# ============================================================
print(f"\n\n{'='*80}")
print("5. EILABRRNI / LABYRINTH DEEP ANALYSIS")
print(f"{'='*80}")

# With the proposed mapping, decode EILABRRNI contexts
for label, mapping in [("Current", base_mapping), ("With 24=R+71=N", m_both)]:
    print(f"\n  --- {label} ---")
    for i, book in enumerate(books):
        dec = decode_book(book, mapping)
        for target in ['EILAB', 'LABR', 'LABRR', 'LABYR']:
            if target in dec:
                pos = dec.find(target)
                ctx = dec[max(0, pos-10):pos+20]
                print(f"  Book {i}: ...{ctx}... (found '{target}')")

# Check specifically: does 24=R turn EILABRRNI into something with LABR?
print("\n  Checking EILAB... patterns with both mappings:")
for i, book in enumerate(books):
    pairs = get_pairs(book)
    dec_base = decode_book(book, base_mapping)
    dec_new = decode_book(book, m_both)
    if 'EILAB' in dec_base or 'EILAB' in dec_new:
        # Find surrounding area
        for target_dec, label2 in [(dec_base, "base"), (dec_new, "new")]:
            if 'EILAB' in target_dec:
                pos = target_dec.find('EILAB')
                ctx = target_dec[max(0, pos-5):min(len(target_dec), pos+20)]
                pairs_ctx = pairs[max(0, pos-5):min(len(pairs), pos+20)]
                print(f"    Book {i} ({label2}): {ctx}")
                print(f"      codes: {' '.join(pairs_ctx)}")

# ============================================================
# 6. FULL NARRATIVE WITH BEST MAPPING
# ============================================================
print(f"\n\n{'='*80}")
print("6. FULL NARRATIVE WITH BEST MAPPING (24=R+71=N+33=W)")
print(f"{'='*80}")

best_mapping = dict(base_mapping)
# Only apply changes that show clear improvement
# For now test with 24=R and 71=N
best_mapping['24'] = 'R'
best_mapping['71'] = 'N'
best_mapping['33'] = 'W'

# Decode all books and show best ones
book_results = []
for i, book in enumerate(books):
    dec = decode_book(book, best_mapping)
    cov, used = measure_coverage(dec)
    pct = cov / len(dec) * 100 if len(dec) > 0 else 0
    book_results.append((i, dec, cov, pct, used))

book_results.sort(key=lambda x: -x[3])

print("\nTop 15 most readable books:\n")
for i, dec, cov, pct, used in book_results[:15]:
    # Word parse
    parsed = word_parse(dec)
    word_strs = []
    for w, s, e in parsed:
        word_strs.append(w)

    print(f"  Book {i} ({len(dec)} chars, {pct:.0f}% coverage):")
    print(f"    Raw:    {dec}")
    if word_strs:
        print(f"    Words:  {' | '.join(word_strs)}")
    print()

# ============================================================
# 7. IIIWII WITH NEW MAPPING
# ============================================================
print(f"\n{'='*80}")
print("7. IIIWII PATTERN WITH CODE 71=N")
print(f"{'='*80}")

# If 71=N, IIIWII (codes 16-46-71-36-46-46) becomes II N W II
# = "IINWII" — that's interesting!
print("\nIIIWII codes: 16=I, 46=I, 71=?, 36=W, 46=I, 46=I")
print(f"  With 71=I: IIIWII")
print(f"  With 71=N: IINWII")

for i, book in enumerate(books):
    dec_base = decode_book(book, base_mapping)
    if 'IIIWII' in dec_base:
        dec_new = decode_book(book, best_mapping)
        # Find the position
        pos = dec_base.find('IIIWII')
        ctx_old = dec_base[max(0,pos-8):pos+14]
        ctx_new = dec_new[max(0,pos-8):pos+14]
        print(f"\n  Book {i}:")
        print(f"    Old: ...{ctx_old}...")
        print(f"    New: ...{ctx_new}...")

# ============================================================
# 8. SUPERSTRING WITH BEST MAPPING
# ============================================================
print(f"\n\n{'='*80}")
print("8. SUPERSTRING ASSEMBLY WITH BEST MAPPING")
print(f"{'='*80}")

# Get unique decoded books
decoded = []
seen = set()
for book in books:
    dec = decode_book(book, best_mapping)
    if dec not in seen:
        decoded.append(dec)
        seen.add(dec)

# Greedy overlap assembly
def find_best_overlap(fragments):
    best_score = 0
    best_i = best_j = -1
    best_merged = ''
    for i in range(len(fragments)):
        for j in range(len(fragments)):
            if i == j: continue
            a, b = fragments[i], fragments[j]
            # Find overlap: suffix of a matches prefix of b
            max_ov = min(len(a), len(b))
            for ov in range(max_ov, 0, -1):
                if a[-ov:] == b[:ov]:
                    if ov > best_score:
                        best_score = ov
                        best_i, best_j = i, j
                        best_merged = a + b[ov:]
                    break
    return best_score, best_i, best_j, best_merged

frags = list(decoded)
while len(frags) > 1:
    score, i, j, merged = find_best_overlap(frags)
    if score < 4:
        break
    frags = [f for k, f in enumerate(frags) if k != i and k != j] + [merged]

print(f"\n{len(frags)} fragments after assembly:")
for k, frag in enumerate(frags):
    cov, used = measure_coverage(frag)
    pct = cov / len(frag) * 100 if len(frag) > 0 else 0

    # Show with word boundaries marked
    parsed = word_parse(frag)

    # Build annotated string
    annotated = list(frag)
    for w, s, e in parsed:
        annotated[s] = '[' + annotated[s]
        annotated[e-1] = annotated[e-1] + ']'
    annotated_str = ''.join(annotated)

    print(f"\n  Fragment {k+1} ({len(frag)} chars, {pct:.0f}% coverage):")
    # Print in chunks of 80
    for start in range(0, len(annotated_str), 80):
        print(f"    {annotated_str[start:start+80]}")

# ============================================================
# 9. UNRECOGNIZED SEGMENTS - LOOK FOR PATTERNS
# ============================================================
print(f"\n\n{'='*80}")
print("9. UNRECOGNIZED SEGMENTS WITH NEW MAPPING")
print(f"{'='*80}")

all_text = ''
for book in books:
    all_text += decode_book(book, best_mapping) + ' '

# Remove known words
remaining = all_text.lower()
for length in range(max(len(w) for w in ALL_WORDS), 1, -1):
    for word in ALL_WORDS:
        if len(word) == length:
            remaining = remaining.replace(word, ' ' * len(word))

# Extract unrecognized segments
seg_counts = Counter()
current = ''
for ch in remaining:
    if ch != ' ':
        current += ch
    else:
        if len(current) >= 3:
            seg_counts[current.upper()] += 1
        current = ''
if len(current) >= 3:
    seg_counts[current.upper()] += 1

print("\nTop 30 unrecognized segments (new mapping):")
for seg, count in seg_counts.most_common(30):
    # Try reversing
    rev = seg[::-1]
    rev_words = []
    for l in range(3, len(rev)+1):
        for s in range(len(rev)-l+1):
            sub = rev[s:s+l].lower()
            if sub in ALL_WORDS:
                rev_words.append(sub.upper())
    rev_info = f" (reversed: {rev}" + (f", contains: {','.join(set(rev_words))}" if rev_words else "") + ")"
    print(f"  {seg}: {count}x{rev_info}")

# ============================================================
# 10. DECISION: APPLY 24=R and 71=N?
# ============================================================
print(f"\n\n{'='*80}")
print("10. FINAL DECISION ANALYSIS")
print(f"{'='*80}")

# Check I frequency with proposed changes
all_text_new = ''
for book in books:
    all_text_new += decode_book(book, best_mapping)
all_text_new = all_text_new.replace('?', '')
total = len(all_text_new)
freq_new = Counter(all_text_new)

i_pct = freq_new['I'] / total * 100
r_pct = freq_new['R'] / total * 100
n_pct = freq_new['N'] / total * 100

print(f"\n  With 24=R + 71=N:")
print(f"    I: {freq_new['I']} ({i_pct:.1f}%) - expected 7.5%")
print(f"    R: {freq_new['R']} ({r_pct:.1f}%) - expected 7.0%")
print(f"    N: {freq_new['N']} ({n_pct:.1f}%) - expected 9.8%")
print(f"    Word coverage improvement: +{total_both - base_total} chars")

# Compare IIIWII interpretation
print(f"\n  IIIWII becomes IINWII:")
print(f"    Could be: II N W II = '2 N W 2'? Or part of a word?")
print(f"    N and W together is unusual in German...")

# Verdict
if total_both > base_total + 20:
    print(f"\n  VERDICT: Changes IMPROVE coverage by {total_both - base_total} chars.")
    print(f"  However, need to verify that no existing confirmed words break.")
else:
    print(f"\n  VERDICT: Changes show marginal improvement ({total_both - base_total} chars).")
    print(f"  May not be worth the risk of breaking confirmed patterns.")
