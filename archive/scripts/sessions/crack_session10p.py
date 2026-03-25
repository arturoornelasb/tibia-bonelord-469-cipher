#!/usr/bin/env python3
"""Session 10p: Test code 15 = P hypothesis + expanded segmentation"""

import json, re
from collections import Counter, defaultdict

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]
books = [parse_codes(b) for b in raw_books]
def decode(book, m=None):
    if m is None: m = mapping
    return ''.join(m.get(c, '?') for c in book)
def collapse(s):
    return re.sub(r'(.)\1+', r'\1', s)

print("=" * 80)
print("SESSION 10p: CODE 15 = P HYPOTHESIS TEST")
print("=" * 80)

# 1. All contexts of code 15
print("\n1. ALL CONTEXTS OF CODE 15 (currently=I, testing P)")
print("-" * 60)

c15_contexts = []
for bi, book in enumerate(books):
    for ci, c in enumerate(book):
        if c == '15':
            start = max(0, ci-4)
            end = min(len(book), ci+5)
            ctx_codes = book[start:end]
            ctx_i = ''.join(mapping.get(x, '?') for x in ctx_codes)
            ctx_p = ''
            for j, x in enumerate(ctx_codes):
                if j == (ci - start):
                    ctx_p += 'P'
                else:
                    ctx_p += mapping.get(x, '?')
            c15_contexts.append((bi, ci, ctx_i, ctx_p))

print(f"  Code 15 total occurrences: {len(c15_contexts)}")
print(f"\n  All unique contexts (as I -> as P):")
seen = set()
for bi, ci, ctx_i, ctx_p in c15_contexts:
    col_i = collapse(ctx_i)
    col_p = collapse(ctx_p)
    key = (col_i, col_p)
    if key not in seen:
        seen.add(key)
        # Highlight known words
        p_good = ""
        for word in ['EMPOR', 'PFLEGE', 'PFAD', 'PRIS', 'SPRUCH',
                      'KAMPF', 'KOPF', 'SPIEL', 'OPFER']:
            if word in col_p:
                p_good = f" ** {word} **"
        i_good = ""
        for word in ['DIESER', 'FINDEN', 'SEINE', 'STEIN', 'RUNE',
                     'EIN', 'IST', 'DIE', 'SIE', 'IN', 'WIR',
                     'MIT', 'LIED', 'VIEL']:
            if word in col_i:
                i_good = f" ({word})"
        print(f"    {col_i:20s} -> {col_p:20s}{p_good}{i_good}")

# 2. Does code 15 appear in any confirmed word?
print("\n" + "=" * 60)
print("2. CODE 15 IN CONFIRMED WORDS")
print("=" * 60)

confirmed_words = [
    'DIESER', 'FINDEN', 'SCHAUN', 'URALTE', 'KOENIG', 'GEIGET',
    'STEIN', 'RUNE', 'ERDE', 'SEGEN', 'SEIN', 'EINE', 'DAS', 'DIE',
    'DER', 'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON', 'MIT', 'WIE',
    'AUS', 'ORT', 'TUN', 'NUR', 'SUN', 'TOT', 'GAR', 'ACH', 'ZUM',
    'HIN', 'HER', 'ALS', 'AUCH', 'TAG', 'WEG', 'DENN', 'ERST',
    'KLAR', 'WIRD', 'STEH', 'DORT', 'GOLD', 'MOND', 'WELT', 'ENDE',
    'REDE', 'HUND', 'HWND', 'LIED', 'NORDEN', 'SONNE', 'UNTER',
    'NICHT', 'WERDE', 'DENEN', 'VIEL', 'RUND', 'SEIDE', 'KELSEI',
    'EINEN', 'EINER', 'SEINE', 'SCHWITEIONE'
]

for word in confirmed_words:
    for bi, book in enumerate(books):
        col = collapse(decode(book))
        if word in col:
            decoded_raw = decode(book)
            for ri in range(len(decoded_raw)):
                if collapse(decoded_raw[ri:ri+len(word)*2]).startswith(word):
                    codes = book[ri:ri+len(word)]
                    if '15' in codes:
                        pos = codes.index('15')
                        print(f"  WARNING: '{word}' uses code 15 at pos {pos}: {' '.join(codes)}")
                    break
            break

print("  (No warnings = code 15 not in any confirmed word)")

# 3. Full text comparison: I vs P
print("\n" + "=" * 60)
print("3. FULL TEXT WITH CODE 15 = P")
print("=" * 60)

mod_mapping = dict(mapping)
mod_mapping['15'] = 'P'

# Show impact on each book
for bi, book in enumerate(books):
    orig = collapse(decode(book))
    mod = collapse(decode(book, mod_mapping))
    if orig != mod:
        # Find differences
        diffs = []
        for j in range(min(len(orig), len(mod))):
            if orig[j] != mod[j]:
                start = max(0, j-5)
                end = min(len(orig), j+6)
                orig_ctx = orig[start:end]
                mod_ctx = mod[start:end]
                diffs.append((j, orig_ctx, mod_ctx))
        if diffs and bi < 15:
            print(f"\n  Book {bi}:")
            for pos, oc, mc in diffs[:5]:
                print(f"    pos {pos}: {oc} -> {mc}")

# 4. Key improved readings with P
print("\n" + "=" * 60)
print("4. KEY IMPROVEMENTS WITH CODE 15 = P")
print("=" * 60)

# Check specific patterns
for bi, book in enumerate(books):
    mod = collapse(decode(book, mod_mapping))
    for pattern in ['EMPOR', 'PRI', 'SPR', 'OPFE', 'PFLE']:
        if pattern in mod:
            pos = mod.index(pattern)
            start = max(0, pos-10)
            end = min(len(mod), pos+15)
            ctx = mod[start:end]
            print(f"  B{bi:02d}: {pattern} found: ...{ctx}...")

# 5. Check if P makes the proper nouns more recognizable
print("\n" + "=" * 60)
print("5. PROPER NOUNS WITH P")
print("=" * 60)

for bi, book in enumerate(books):
    orig = collapse(decode(book))
    mod = collapse(decode(book, mod_mapping))
    for name in ['EILCHANHEARUCHTIG', 'EDETOTNIURGS', 'LABGZERAS',
                  'TIUMENGEMI', 'SCHWITEIONE', 'ADTHARSC']:
        if name in orig:
            # Find same position in mod
            pos = orig.index(name)
            # The mod text may have different length
            # Find the corresponding segment
            orig_pre = orig[:pos]
            mod_name = mod[pos:pos+len(name)+2]  # approximate
            if name != mod_name[:len(name)]:
                print(f"  {name} -> {mod_name[:len(name)+2]} (changed)")
            break

# 6. Impact on letter frequency
print("\n" + "=" * 60)
print("6. LETTER FREQUENCY IMPACT")
print("=" * 60)

all_codes = Counter()
for book in books:
    for c in book:
        all_codes[c] += 1

total = sum(all_codes.values())
c15_freq = all_codes.get('15', 0)
print(f"  Code 15 frequency: {c15_freq} ({c15_freq*100/total:.1f}%)")
print(f"  Expected P: ~0.8% = ~{int(total*0.008)} codes")
print(f"  Code 15 at {c15_freq} is {c15_freq*100/total:.1f}% - "
      f"{'close to P' if c15_freq*100/total < 2.0 else 'too high for P'}")

# After removing code 15 from I:
remaining_i = sum(all_codes.get(c, 0) for c in ['16', '21', '46', '50', '65'])
print(f"\n  Remaining I (without code 15): {remaining_i} ({remaining_i*100/total:.1f}%)")
print(f"  Expected I: ~7.6%")
print(f"  Diff: {remaining_i*100/total - 7.6:+.1f}%")

# 7. Test: EMPOR in context
print("\n" + "=" * 60)
print("7. EMPOR CONTEXT ANALYSIS")
print("=" * 60)

for bi, book in enumerate(books):
    mod = collapse(decode(book, mod_mapping))
    if 'EMPOR' in mod:
        pos = mod.index('EMPOR')
        start = max(0, pos-15)
        end = min(len(mod), pos+20)
        ctx = mod[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# 8. What other words appear with P?
print("\n" + "=" * 60)
print("8. NEW WORDS FOUND WITH CODE 15 = P")
print("=" * 60)

# Search for known German words that contain P
p_words = ['EMPOR', 'OPFER', 'KAMPF', 'KOPF', 'PFAD', 'PFLEGE',
           'PRIESTER', 'PRACHT', 'PREIS', 'SPRUCH', 'SPRECHEN',
           'SPIELEN', 'SPEER', 'SPUREN', 'SPUR', 'PLATZ',
           'PFLICHT', 'PFORTE', 'PILGER', 'PROPHET']

for word in p_words:
    for bi, book in enumerate(books):
        mod = collapse(decode(book, mod_mapping))
        if word in mod:
            pos = mod.index(word)
            start = max(0, pos-8)
            end = min(len(mod), pos+len(word)+8)
            ctx = mod[start:end]
            print(f"  {word}: B{bi:02d} ...{ctx}...")
            break

# 9. Also check for P in MHG spellings
print("\n  MHG P-words:")
mhg_p_words = ['PHLEGE', 'PHERD', 'PHAT', 'PHLEGER', 'PRISEN',
                'PRISLICH', 'PREDIGEN', 'PALAST', 'PARADIS']
for word in mhg_p_words:
    for bi, book in enumerate(books):
        mod = collapse(decode(book, mod_mapping))
        if word in mod:
            pos = mod.index(word)
            start = max(0, pos-5)
            end = min(len(mod), pos+len(word)+5)
            ctx = mod[start:end]
            print(f"  {word}: B{bi:02d} ...{ctx}...")
            break

# 10. DP segmentation with P included
print("\n" + "=" * 60)
print("10. DP SEGMENTATION WITH CODE 15 = P")
print("=" * 60)

NEG_INF = float('-inf')

word_scores = {}
definite = [
    'AUNRSONGETRASES', 'UNENITGHNE', 'EILCHANHEARUCHTIG',
    'EDETOTNIURGS', 'DNRHAUNRNVMHISDIZA',
    'EUGENDRTHENAEDEULGHLWUOEHSG', 'WRLGTNELNRHELUIRUNN',
    'TIUMENGEMI', 'SCHWITEIONE',
    'LABGZERAS', 'HEDEMI', 'TAUTR', 'LABRNI', 'ADTHARSC',
    'ADTHAUMR', 'ODEGAREN', 'RLAUNR',
    'KOENIG', 'UTRUNR', 'GEIGET', 'KELSEI', 'SCHAUN',
    'URALTE', 'FINDEN', 'SEIDE', 'DIESER', 'GEVMT',
    'NORDEN', 'SONNE', 'UNTER', 'NICHT', 'WERDE',
    'STEIN', 'DENEN', 'ERDE', 'VIEL', 'RUNE',
    'STEH', 'LIED', 'SEGEN', 'DORT', 'DENN',
    'GOLD', 'MOND', 'WELT', 'ENDE', 'REDE',
    'HUND', 'SEIN', 'WIRD', 'KLAR', 'ERST',
    'HWND', 'VMTEGE', 'EMPOR', 'OWI', 'STEIEN',
    'EINEN', 'EINER', 'SEINE',
    'TAG', 'WEG', 'DER', 'DEN', 'DIE', 'DAS',
    'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON',
    'MIT', 'WIE', 'SEI', 'AUS', 'ORT', 'TUN',
    'NUR', 'SUN', 'TOT', 'GAR', 'ACH', 'ZUM',
    'HIN', 'HER', 'ALS', 'AUCH', 'RUND', 'GEH',
    'ER', 'ES', 'IN', 'SO',
]

for w in definite:
    word_scores[w] = len(w) * 3

all_words = sorted(word_scores.keys(), key=len, reverse=True)

def dp_segment(text, words, scores):
    n = len(text)
    dp = [NEG_INF] * (n + 1)
    back = [None] * (n + 1)
    dp[0] = 0
    for i in range(n):
        if dp[i] == NEG_INF:
            continue
        new_score = dp[i] - 1
        if new_score > dp[i+1]:
            dp[i+1] = new_score
            back[i+1] = ('unk', i)
        for word in words:
            wlen = len(word)
            if i + wlen <= n and text[i:i+wlen] == word:
                new_score = dp[i] + scores.get(word, wlen)
                if new_score > dp[i+wlen]:
                    dp[i+wlen] = new_score
                    back[i+wlen] = ('word', i, word)
    result = []
    pos = n
    while pos > 0:
        info = back[pos]
        if info is None:
            result.append(('unk', text[pos-1:pos]))
            pos -= 1
        elif info[0] == 'unk':
            end = pos
            while pos > 0 and back[pos] and back[pos][0] == 'unk':
                pos = back[pos][1]
            result.append(('unk', text[pos:end]))
        elif info[0] == 'word':
            result.append(('word', info[2]))
            pos = info[1]
    result.reverse()
    return result, dp[n]

# Segment with modified mapping
all_col_mod = [(i, collapse(decode(b, mod_mapping))) for i, b in enumerate(books)]

pieces = {}
for i, text in all_col_mod:
    is_sub = False
    for j, other in all_col_mod:
        if i != j and text in other:
            is_sub = True
            break
    if not is_sub:
        pieces[i] = text

by_len = sorted(pieces.items(), key=lambda x: len(x[1]), reverse=True)

total_chars = 0
total_covered = 0
for bi, text in all_col_mod:
    result, score = dp_segment(text, all_words, word_scores)
    word_chars = sum(len(val) for typ, val in result if typ == 'word')
    total_chars += len(text)
    total_covered += word_chars

print(f"  Overall coverage with P: {total_covered*100/total_chars:.1f}%")

# Compare to without P
all_col_orig = [(i, collapse(decode(b))) for i, b in enumerate(books)]
total_orig = 0
covered_orig = 0
for bi, text in all_col_orig:
    result, _ = dp_segment(text, all_words, word_scores)
    wc = sum(len(val) for typ, val in result if typ == 'word')
    total_orig += len(text)
    covered_orig += wc

print(f"  Overall coverage without P: {covered_orig*100/total_orig:.1f}%")
print(f"  Improvement: {(total_covered*100/total_chars) - (covered_orig*100/total_orig):+.1f}%")

# Show top 3 books with P
print("\n  Top 3 books with P:")
for idx, (bi, text) in enumerate(by_len[:3]):
    result, score = dp_segment(text, all_words, word_scores)
    parts = []
    for typ, val in result:
        if typ == 'word':
            parts.append(val)
        else:
            parts.append(f'[{val}]')
    word_chars = sum(len(val) for typ, val in result if typ == 'word')
    pct = word_chars * 100 / len(text) if text else 0
    print(f"\n  Book {bi} ({len(text)} chars, coverage={pct:.0f}%):")
    line = ' '.join(parts)
    for li in range(0, len(line), 76):
        print(f"    {line[li:li+76]}")

# 11. Most common unknowns with P
print("\n" + "=" * 60)
print("11. REMAINING UNKNOWNS WITH P")
print("=" * 60)

unk_counter = Counter()
for bi, text in all_col_mod:
    result, _ = dp_segment(text, all_words, word_scores)
    for typ, val in result:
        if typ == 'unk' and len(val) > 1:
            unk_counter[val] += 1

for unk, count in unk_counter.most_common(20):
    print(f"  [{unk:20s}] ({count:2d}x)")

print("\n" + "=" * 80)
print("SESSION 10p COMPLETE")
print("=" * 80)
