#!/usr/bin/env python3
"""
Session 20 Part 2: Attack high-frequency patterns.

Key targets:
1. {T} 30x before ER -- is TER a word? (MHG: "der")
2. {E} 30x -- investigate contexts, are these leftovers from +1 anagrams?
3. {HED} 11x -- always in "MIN {HED} DEM {I} DIE" -- why isn't HEDEMI matching?
4. {SD} 7x -- always "AN {SD} IM" -- ANSD->SAND would kill AN, but what about SD+IM?
5. {DE} 9x -- always "SEINE {DE} TOT" or "NEU {DE} DIENST"
6. H overrepresentation in garbled -- which codes produce H?
7. Cross-boundary: test ALL {1-2ch}+WORD and WORD+{1-2ch} combos as real words
"""

import json, os
from collections import Counter, defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

DIGIT_SPLITS = {
    2: (45, '1'), 5: (265, '1'), 6: (12, '0'), 8: (137, '7'),
    10: (169, '0'), 11: (137, '0'), 12: (56, '1'), 13: (45, '0'),
    14: (98, '1'), 15: (98, '0'), 18: (4, '0'), 19: (52, '0'),
    20: (5, '1'), 22: (7, '1'), 23: (22, '4'), 24: (87, '8'),
    25: (0, '0'), 29: (53, '0'), 32: (137, '1'), 34: (101, '0'),
    36: (78, '0'), 39: (44, '0'), 42: (91, '2'), 43: (122, '0'),
    45: (15, '0'), 46: (0, '2'), 48: (126, '0'), 49: (97, '1'),
    50: (16, '6'), 52: (1, '0'), 53: (257, '1'), 54: (49, '1'),
    60: (73, '9'), 61: (93, '7'), 64: (60, '0'), 65: (114, '2'),
    68: (54, '0'),
}

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    return 0 if ic_from_counts(Counter(bp0), len(bp0)) > ic_from_counts(Counter(bp1), len(bp1)) else 1

book_pairs = []
decoded_books = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)
    decoded_books.append(''.join(v7.get(p, '?') for p in pairs))

all_text = ''.join(decoded_books)

ANAGRAM_MAP = {
    'LABGZERAS': 'SALZBERG', 'SCHWITEIONE': 'WEICHSTEIN',
    'SCHWITEIO': 'WEICHSTEIN', 'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'EDETOTNIURG': 'GOTTDIENER', 'EDETOTNIURGS': 'GOTTDIENERS',
    'ADTHARSC': 'SCHARDT', 'TAUTR': 'TRAUT', 'EILCH': 'LEICH',
    'HEDEMI': 'HEIME', 'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG', 'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE', 'TEIGN': 'NEIGT', 'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER', 'SODGE': 'GODES', 'SNDTEII': 'DIENST',
    'IEB': 'BEI', 'TNEDAS': 'STANDE', 'NSCHAT': 'NACHTS',
    'SANGE': 'SAGEN', 'GHNEE': 'GEHEN',
}

resolved = all_text
for anag in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved = resolved.replace(anag, ANAGRAM_MAP[anag])

KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR', 'NU', 'STANDE', 'NACHTS', 'NIT', 'TOT',
    'ABER', 'ALLE', 'ALLES', 'ALTE', 'ALTEN', 'ALTER', 'AUCH', 'BAND',
    'BERG', 'BURG', 'DENN', 'DIES', 'DIESE', 'DIESER', 'DIESEN',
    'DIESEM', 'DOCH', 'DORT', 'DREI', 'DURCH', 'EINE', 'EINEM',
    'EINEN', 'EINER', 'EINES', 'ENDE', 'ERDE', 'ERST', 'ERSTE',
    'FACH', 'FAND', 'FERN', 'FEST', 'FORT', 'GAR', 'GANZ', 'GEGEN',
    'GEIST', 'GOTT', 'GOLD', 'GRAB', 'GROSS', 'GRUFT', 'GUT',
    'HAND', 'HEIM', 'HELD', 'HERR', 'HIER', 'HOCH', 'IMMER',
    'KANN', 'KLAR', 'KRAFT', 'LAND', 'LANG', 'LICHT', 'MACHT',
    'MEHR', 'MUSS', 'NACH', 'NACHT', 'NAHM', 'NAME', 'NEU', 'NEUE',
    'NEUEN', 'NICHT', 'NIE', 'NOCH', 'ODER', 'ORT', 'ORTEN',
    'REDE', 'REDEN', 'REICH', 'RIEF', 'RUIN', 'RUNE', 'RUNEN',
    'SAND', 'SAGT', 'SCHAUN', 'SCHON', 'SEHR', 'SEID', 'SEIN',
    'SEINE', 'SEINEN', 'SEINER', 'SEINEM', 'SEINES',
    'SICH', 'SIND', 'SOHN', 'SOLL', 'STEH', 'STEIN', 'STEINE',
    'STEINEN', 'STERN', 'TAG', 'TAGE', 'TAGEN', 'TAT', 'TEIL',
    'TIEF', 'TOD', 'TURM', 'UNTER', 'URALTE', 'VIEL', 'VIER',
    'WAHR', 'WALD', 'WAND', 'WARD', 'WEIL', 'WELT', 'WENN', 'WERT',
    'WESEN', 'WILL', 'WIND', 'WIRD', 'WORT', 'WORTE', 'ZEIT',
    'ZEHN', 'ZORN',
    'FINDEN', 'GEBEN', 'GEHEN', 'HABEN', 'KOMMEN', 'LEBEN', 'LESEN',
    'NEHMEN', 'SAGEN', 'SEHEN', 'STEHEN', 'SUCHEN', 'WISSEN',
    'WISSET', 'RUFEN', 'WIEDER',
    'OEL', 'SCE', 'MINNE', 'MIN', 'ODE', 'SER', 'GEN', 'INS',
    'GEIGET', 'BERUCHTIG', 'BERUCHTIGER',
    'MEERE', 'NEIGT', 'WISTEN', 'MANIER', 'HUND',
    'GODE', 'GODES', 'EIGENTUM', 'REDER',
    'THENAEUT', 'LABT', 'MORT', 'DIGE', 'WEGE', 'KOENIGS',
    'NAHE', 'NOT', 'NOTH', 'ZUR', 'OWI', 'ENGE', 'SEIDEN',
    'ALTES', 'NUT', 'NUTZ', 'HEIL', 'NEID', 'TREU', 'TREUE',
    'SUN', 'DIENST', 'SANG', 'DINC', 'HULDE', 'LANT', 'HERRE',
    'DIENEST', 'GEBOT', 'SCHWUR', 'ORDEN', 'RICHTER', 'DUNKEL',
    'EHRE', 'EDELE', 'SCHULD', 'SEGEN', 'FLUCH', 'RACHE',
    'KOENIG', 'DASS', 'EDEL', 'ADEL',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME', 'SCHARDT',
])

def dp_segment(text, wordset):
    n = len(text)
    dp = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], None)
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if cand in wordset:
                score = dp[start][0] + wlen
                if score > dp[i][0]:
                    dp[i] = (score, (start, cand))
    tokens = []
    i = n
    while i > 0:
        if dp[i][1] is not None:
            start, word = dp[i][1]
            tokens.append(('W', word))
            i = start
        else:
            tokens.append(('C', text[i-1]))
            i -= 1
    tokens.reverse()
    result = []
    for kind, val in tokens:
        if kind == 'W':
            result.append(val)
        else:
            if result and result[-1].startswith('{'):
                result[-1] = result[-1][:-1] + val + '}'
            else:
                result.append('{' + val + '}')
    return result, dp[n][0]

def dp_count(text, wordset):
    n = len(text)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            if text[start:i] in wordset:
                dp[i] = max(dp[i], dp[start] + wlen)
    return dp[n]

tokens, covered = dp_segment(resolved, KNOWN)
total = sum(1 for c in resolved if c != '?')
print(f"Baseline: {covered}/{total} = {covered/total*100:.1f}%")

# ================================================================
# 1. WHY ISN'T HEDEMI MATCHING? Investigate {HED} DEM {I}
# ================================================================
print(f"\n{'=' * 80}")
print("1. INVESTIGATING {HED} DEM {I} -- expected HEDEMI->HEIME")
print("=" * 80)

# Find HEDEMI in raw decoded text (before anagram replacement)
raw = all_text  # before anagram replacement
hedemi_count_raw = raw.count('HEDEMI')
print(f"\n  HEDEMI in raw text: {hedemi_count_raw}x")

# Find in resolved text
heime_count = resolved.count('HEIME')
print(f"  HEIME in resolved text: {heime_count}x")

# Find what's actually at those positions
# Look for HED in resolved text with context
print(f"\n  Searching for 'HED' in resolved text with context:")
hed_positions = []
pos = 0
while True:
    idx = resolved.find('HED', pos)
    if idx < 0: break
    ctx_s = max(0, idx - 15)
    ctx_e = min(len(resolved), idx + 20)
    ctx = resolved[ctx_s:ctx_e]
    hed_positions.append((idx, ctx))
    pos = idx + 1

for idx, ctx in hed_positions[:15]:
    # Check raw text at same position area
    raw_ctx = all_text[max(0,idx-15):min(len(all_text),idx+20)]
    print(f"  pos {idx:4d}: resolved: ...{ctx}...")
    print(f"            raw:      ...{raw_ctx}...")

# Check: does the raw text have HEDEMI or something else?
print(f"\n  Raw text occurrences of HEDEM*:")
pos = 0
while True:
    idx = all_text.find('HEDEM', pos)
    if idx < 0: break
    ctx = all_text[max(0,idx-10):min(len(all_text),idx+15)]
    print(f"    pos {idx}: ...{ctx}...")
    pos = idx + 1

# ================================================================
# 2. {T} BEFORE ER -- is TER a word?
# ================================================================
print(f"\n{'=' * 80}")
print("2. {{T}} ER pattern -- testing TER as MHG article")
print("=" * 80)

# Find all {T} ER occurrences and their full context
t_er_contexts = []
for i, t in enumerate(tokens):
    if t == '{T}' and i + 1 < len(tokens) and tokens[i+1] == 'ER':
        prev = tokens[i-1] if i > 0 else ''
        after_er = tokens[i+2] if i + 2 < len(tokens) else ''
        t_er_contexts.append((prev, after_er))

print(f"\n  {{T}}+ER occurrences: {len(t_er_contexts)}")
for prev, after in t_er_contexts:
    pstr = prev if not prev.startswith('{') else f'[{prev[1:-1]}]'
    astr = after if not after.startswith('{') else f'[{after[1:-1]}]'
    print(f"    ...{pstr} {{T}} ER {astr}...")

# But {T} also appears in other contexts
t_other = []
for i, t in enumerate(tokens):
    if t == '{T}' and not (i + 1 < len(tokens) and tokens[i+1] == 'ER'):
        prev = tokens[i-1] if i > 0 else ''
        nxt = tokens[i+1] if i + 1 < len(tokens) else ''
        t_other.append((prev, nxt))

print(f"\n  {{T}} in OTHER contexts: {len(t_other)}")
for prev, nxt in t_other[:10]:
    pstr = prev if not prev.startswith('{') else f'[{prev[1:-1]}]'
    nstr = nxt if not nxt.startswith('{') else f'[{nxt[1:-1]}]'
    print(f"    ...{pstr} {{T}} {nstr}...")

# ================================================================
# 3. {{DE}} 9x -- context analysis
# ================================================================
print(f"\n{'=' * 80}")
print("3. {{DE}} block -- 9x occurrences")
print("=" * 80)

de_contexts = []
for i, t in enumerate(tokens):
    if t == '{DE}':
        prev = tokens[i-1] if i > 0 else ''
        nxt = tokens[i+1] if i + 1 < len(tokens) else ''
        de_contexts.append((prev, nxt, i))

for prev, nxt, idx in de_contexts:
    pstr = prev if not prev.startswith('{') else f'[{prev[1:-1]}]'
    nstr = nxt if not nxt.startswith('{') else f'[{nxt[1:-1]}]'
    # Can we form a word?
    candidates = []
    if not prev.startswith('{'):
        combined = prev + 'DE'
        if combined in KNOWN: candidates.append(f'{prev}+DE={combined}')
        # Also check: is SEINE+DE = SEINED? No. But SEINE -> SEINEM, SEINEN?
    if not nxt.startswith('{'):
        combined = 'DE' + nxt
        if combined in KNOWN: candidates.append(f'DE+{nxt}={combined}')
    cand_str = f" -> {', '.join(candidates)}" if candidates else ""
    print(f"  [{idx:3d}] ...{pstr} {{DE}} {nstr}...{cand_str}")

# ================================================================
# 4. {SD} 7x -- always "AN {SD} IM"
# ================================================================
print(f"\n{'=' * 80}")
print("4. {SD} block -- pattern analysis")
print("=" * 80)

sd_contexts = []
for i, t in enumerate(tokens):
    if t == '{SD}':
        ctx = ' '.join(tokens[max(0,i-3):min(len(tokens),i+4)])
        sd_contexts.append(ctx)

for ctx in sd_contexts:
    print(f"  {ctx}")

# Test: what if we add DES as a new anagram of {SD}?
# SD -> DS -> DES? No, that's 2 letters, DES is 3.
# But what about the full context: AN + SD + IM = ANSDIM
# Or: A + N + S + D + I + M
# ANSDIM anagram = DINAMS? DANISM? MINADS?
# Actually just SD between AN and IM: SD+IM = SDIM? Not a word.
# AN+SD = ANSD = SAND (already known)

# ================================================================
# 5. H OVERREPRESENTATION -- which codes produce H?
# ================================================================
print(f"\n{'=' * 80}")
print("5. H CODE ANALYSIS -- overrepresented in garbled")
print("=" * 80)

h_codes = [c for c, l in v7.items() if l == 'H']
print(f"\n  Codes that produce H: {sorted(h_codes)}")
print(f"  Total H codes: {len(h_codes)}")

# Count how many times each H code appears
h_code_counts = Counter()
for pairs in book_pairs:
    for p in pairs:
        if v7.get(p) == 'H':
            h_code_counts[p] += 1

print(f"\n  H code frequencies:")
for code, cnt in h_code_counts.most_common():
    print(f"    code {code}: {cnt}x")

# For each H code, check if it appears in known vs garbled positions
# Build a position-to-known mapping
dp_result = dp_segment(resolved, KNOWN)
tokens_list = dp_result[0]

# Build coverage mask
known_mask = [False] * len(resolved)
pos = 0
for t in tokens_list:
    if t.startswith('{'):
        content = t[1:-1]
        pos += len(content)
    else:
        for c in t:
            known_mask[pos] = True
            pos += 1

# Now check each H code's position
print(f"\n  H codes in known vs garbled zones:")
cum_pos = 0
for bidx, pairs in enumerate(book_pairs):
    for pi, pair in enumerate(pairs):
        letter = v7.get(pair)
        if letter == 'H':
            # Map to resolved text position (approximate)
            # This is complex due to anagram replacement changing lengths
            # Skip for now, just count
            pass

# Simpler: count H in garbled vs known
h_in_garbled = 0
h_in_known = 0
pos = 0
for t in tokens_list:
    if t.startswith('{'):
        content = t[1:-1]
        h_in_garbled += content.count('H')
        pos += len(content)
    else:
        h_in_known += t.count('H')
        pos += len(t)

print(f"  H in known words: {h_in_known}")
print(f"  H in garbled blocks: {h_in_garbled}")
print(f"  Ratio garbled/total: {h_in_garbled/(h_in_known+h_in_garbled)*100:.1f}%")
print(f"  (Average letter garbled ratio: {(total-covered)/total*100:.1f}%)")
print(f"  H is {h_in_garbled/(h_in_known+h_in_garbled)*100 - (total-covered)/total*100:+.1f}% more garbled than average")

# What if some H codes should actually be other letters?
# Let's check: for the most common H code, what would the text look like
# if it mapped to a different letter?
print(f"\n  Alternative H mappings -- testing most frequent H code:")
top_h_code = h_code_counts.most_common(1)[0][0]
print(f"  Most common H code: {top_h_code} ({h_code_counts[top_h_code]}x)")

for alt_letter in 'ENISRATDULCGMOBWFKZ':
    # What words would form if this code mapped to alt_letter instead?
    alt_v7 = dict(v7)
    alt_v7[top_h_code] = alt_letter
    # Re-decode with this alternative
    alt_decoded = []
    for bpairs in book_pairs:
        text = ''.join(alt_v7.get(p, '?') for p in bpairs)
        alt_decoded.append(text)
    alt_all = ''.join(alt_decoded)
    # Apply anagram map
    alt_resolved = alt_all
    for anag in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
        alt_resolved = alt_resolved.replace(anag, ANAGRAM_MAP[anag])
    # Count coverage
    alt_cov = dp_count(alt_resolved, KNOWN)
    delta = alt_cov - covered
    if delta > 5:
        print(f"    {top_h_code}: H->{alt_letter}: {alt_cov}/{total} = {alt_cov/total*100:.1f}% ({delta:+d} chars)")

# Test second most common H code too
if len(h_code_counts) >= 2:
    second_h = h_code_counts.most_common(2)[1][0]
    print(f"\n  Second most common H code: {second_h} ({h_code_counts[second_h]}x)")
    for alt_letter in 'ENISRATDULCGMOBWFKZ':
        alt_v7 = dict(v7)
        alt_v7[second_h] = alt_letter
        alt_decoded = []
        for bpairs in book_pairs:
            text = ''.join(alt_v7.get(p, '?') for p in bpairs)
            alt_decoded.append(text)
        alt_all = ''.join(alt_decoded)
        alt_resolved = alt_all
        for anag in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
            alt_resolved = alt_resolved.replace(anag, ANAGRAM_MAP[anag])
        alt_cov = dp_count(alt_resolved, KNOWN)
        delta = alt_cov - covered
        if delta > 5:
            print(f"    {second_h}: H->{alt_letter}: {alt_cov}/{total} = {alt_cov/total*100:.1f}% ({delta:+d} chars)")

# ================================================================
# 6. L OVERREPRESENTATION -- same analysis
# ================================================================
print(f"\n{'=' * 80}")
print("6. L CODE ANALYSIS -- also overrepresented")
print("=" * 80)

l_codes = [c for c, l in v7.items() if l == 'L']
print(f"\n  Codes that produce L: {sorted(l_codes)}")

l_code_counts = Counter()
for pairs in book_pairs:
    for p in pairs:
        if v7.get(p) == 'L':
            l_code_counts[p] += 1

print(f"  L code frequencies:")
for code, cnt in l_code_counts.most_common():
    print(f"    code {code}: {cnt}x")

l_in_garbled = 0
l_in_known = 0
for t in tokens_list:
    if t.startswith('{'):
        l_in_garbled += t[1:-1].count('L')
    else:
        l_in_known += t.count('L')

print(f"  L in known: {l_in_known}, garbled: {l_in_garbled}")
print(f"  L garbled ratio: {l_in_garbled/(l_in_known+l_in_garbled)*100:.1f}% (avg: {(total-covered)/total*100:.1f}%)")

# Test alternatives for L codes
for lcode in [c for c, _ in l_code_counts.most_common(2)]:
    print(f"\n  Testing alternatives for L code {lcode} ({l_code_counts[lcode]}x):")
    for alt_letter in 'ENISRATDHUCGMOBWFKZ':
        alt_v7 = dict(v7)
        alt_v7[lcode] = alt_letter
        alt_decoded = []
        for bpairs in book_pairs:
            text = ''.join(alt_v7.get(p, '?') for p in bpairs)
            alt_decoded.append(text)
        alt_all = ''.join(alt_decoded)
        alt_resolved = alt_all
        for anag in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
            alt_resolved = alt_resolved.replace(anag, ANAGRAM_MAP[anag])
        alt_cov = dp_count(alt_resolved, KNOWN)
        delta = alt_cov - covered
        if delta > 5:
            print(f"    {lcode}: L->{alt_letter}: {alt_cov}/{total} = {alt_cov/total*100:.1f}% ({delta:+d} chars)")

# ================================================================
# 7. COMPREHENSIVE WORD BOUNDARY SCAN
# ================================================================
print(f"\n{'=' * 80}")
print("7. COMPREHENSIVE SMALL-BLOCK WORD FORMATION")
print("=" * 80)

# Extended German word list for testing combinations
EXTENDED_WORDS = set([
    # Common German words not yet in KNOWN
    'TER', 'MIT', 'DES', 'VOM', 'ZUM', 'DIR', 'MIR', 'IHR', 'IHM',
    'TAG', 'RAT', 'MAL', 'TOR', 'ARM', 'BEIN', 'BLUT', 'BROT',
    'DEIN', 'DEINE', 'DEINER', 'DEINEM', 'DEINEN',
    'JEDER', 'JEDE', 'JEDEM', 'JEDEN',
    'MEIN', 'MEINE', 'MEINER', 'MEINEM', 'MEINEN',
    'SEIN', 'SEINE', 'SEINER', 'SEINEM', 'SEINEN',
    'EUER', 'EURE', 'EUREM', 'EUREN',
    'WEM', 'WEN', 'WESSEN',
    'OFT', 'BALD', 'LANG', 'LAUT', 'STILL',
    'ALT', 'JUNG', 'ARM', 'LANG', 'WEIT',
    'GIE', 'TUE', 'SEH', 'LES',
    # MHG specifics
    'TER', 'DER', 'SIN', 'WAN', 'DAZ', 'MHT', 'NIHT',
    'ENEM', 'ENER', 'ENES', 'ENE',
    'DIT', 'DAT', 'SET', 'TIS',
    'SINER', 'SINEM', 'SINEN',
    'ANDER', 'ANDERE', 'ANDEREM', 'ANDEREN',
])

# Test adding each extended word
print(f"\n  Testing extended word list for coverage gains:")
gains = []
for word in sorted(EXTENDED_WORDS - KNOWN):
    if len(word) < 2: continue
    test_known = set(KNOWN)
    test_known.add(word)
    new_cov = dp_count(resolved, test_known)
    delta = new_cov - covered
    if delta > 0:
        gains.append((word, delta, new_cov))

gains.sort(key=lambda x: -x[1])
for word, delta, new_cov in gains:
    print(f"    +{word}: {new_cov}/{total} = {new_cov/total*100:.1f}% ({delta:+d} chars)")

# Cumulative test
if gains:
    print(f"\n  Cumulative test (all gainers):")
    test_known = set(KNOWN)
    for word, _, _ in gains:
        test_known.add(word)
    cum_cov = dp_count(resolved, test_known)
    cum_delta = cum_cov - covered
    print(f"    All together: {cum_cov}/{total} = {cum_cov/total*100:.1f}% ({cum_delta:+d} chars)")

print(f"\n  Done.")
