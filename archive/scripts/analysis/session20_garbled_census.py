#!/usr/bin/env python3
"""
Session 20: Systematic garbled block census + new word discovery.

Goals:
1. Complete inventory of ALL garbled blocks with frequencies
2. Find recurring garbled substrings (potential unsolved words)
3. Scan garbled zones for hidden MHG/German words (length 3-8)
4. Test new cross-boundary anagrams with expanded MHG lexicon
5. Try alternative letter assignments for high-frequency garbled codes
"""

import json, os
from collections import Counter, defaultdict
from itertools import permutations

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

tokens, covered = dp_segment(resolved, KNOWN)
total = sum(1 for c in resolved if c != '?')

# ================================================================
# 1. COMPLETE GARBLED BLOCK CENSUS
# ================================================================
print("=" * 80)
print("1. GARBLED BLOCK CENSUS")
print("=" * 80)

garbled_blocks = []
for t in tokens:
    if t.startswith('{'):
        content = t[1:-1]
        garbled_blocks.append(content)

garbled_counter = Counter(garbled_blocks)
total_garbled_chars = sum(len(b) for b in garbled_blocks)
unique_blocks = len(garbled_counter)

print(f"\n  Total garbled blocks: {len(garbled_blocks)}")
print(f"  Unique blocks: {unique_blocks}")
print(f"  Total garbled chars: {total_garbled_chars}")
print(f"  Known coverage: {covered}/{total} = {covered/total*100:.1f}%")

print(f"\n  By frequency (count >= 2):")
for block, count in garbled_counter.most_common():
    if count >= 2:
        chars = len(block) * count
        print(f"    {count:2d}x [{len(block):2d}ch] = {chars:3d}ch total: {block}")

print(f"\n  Single-occurrence blocks ({sum(1 for b,c in garbled_counter.items() if c == 1)}):")
singles = [(b, len(b)) for b, c in garbled_counter.items() if c == 1]
singles.sort(key=lambda x: -x[1])
for block, blen in singles[:30]:
    print(f"    [{blen:2d}ch]: {block}")

# ================================================================
# 2. RECURRING SUBSTRINGS IN GARBLED ZONES
# ================================================================
print(f"\n{'=' * 80}")
print("2. RECURRING SUBSTRINGS IN GARBLED ZONES")
print("=" * 80)

# Concatenate all garbled text and find common substrings
all_garbled = ''.join(garbled_blocks)
substr_counts = Counter()
for slen in range(3, 10):
    for i in range(len(all_garbled) - slen + 1):
        sub = all_garbled[i:i+slen]
        if sub not in substr_counts:  # only count first occurrence in each scan
            count = all_garbled.count(sub)
            if count >= 3:
                substr_counts[sub] = count

# Filter: keep only substrings that aren't just parts of longer frequent ones
# (simple dedup: skip if a longer substring with same count exists)
filtered = {}
for sub, cnt in sorted(substr_counts.items(), key=lambda x: (-x[1], -len(x[0]))):
    # Check if this is a substring of something already in filtered with same count
    is_sub = False
    for existing in filtered:
        if sub in existing and filtered[existing] == cnt:
            is_sub = True
            break
    if not is_sub:
        filtered[sub] = cnt

print(f"\n  Most frequent garbled substrings (deduplicated):")
for sub, cnt in sorted(filtered.items(), key=lambda x: (-x[1], -len(x[0])))[:25]:
    print(f"    {cnt:2d}x [{len(sub):2d}ch]: {sub}")

# ================================================================
# 3. LETTER FREQUENCY IN GARBLED vs KNOWN ZONES
# ================================================================
print(f"\n{'=' * 80}")
print("3. LETTER DISTRIBUTION: GARBLED vs KNOWN")
print("=" * 80)

# Build garbled mask
garbled_chars = Counter()
known_chars = Counter()
pos = 0
for t in tokens:
    if t.startswith('{'):
        content = t[1:-1]
        for c in content:
            garbled_chars[c] += 1
    else:
        for c in t:
            known_chars[c] += 1

print(f"\n  {'Letter':>6} {'Known':>6} {'Garbled':>8} {'K%':>6} {'G%':>6} {'Diff':>6}")
print(f"  {'-'*46}")
k_total = sum(known_chars.values())
g_total = sum(garbled_chars.values())
big_diffs = []
for letter in 'ENISRATDHULCGMOBWFKZP':
    kc = known_chars.get(letter, 0)
    gc = garbled_chars.get(letter, 0)
    kp = kc/k_total*100 if k_total else 0
    gp = gc/g_total*100 if g_total else 0
    diff = gp - kp
    big_diffs.append((letter, diff, gc, gp))
    marker = ' **' if abs(diff) > 3 else ''
    print(f"  {letter:>6} {kc:>6} {gc:>8} {kp:>5.1f}% {gp:>5.1f}% {diff:>+5.1f}{marker}")

print(f"\n  Overrepresented in garbled (likely unmapped or misassigned):")
for letter, diff, gc, gp in sorted(big_diffs, key=lambda x: -x[1])[:5]:
    if diff > 2:
        print(f"    {letter}: +{diff:.1f}% ({gc} occurrences in garbled)")

print(f"\n  Underrepresented in garbled (well-captured by known words):")
for letter, diff, gc, gp in sorted(big_diffs, key=lambda x: x[1])[:5]:
    if diff < -2:
        print(f"    {letter}: {diff:.1f}% (mostly in known words)")

# ================================================================
# 4. HIDDEN WORDS IN GARBLED ZONES (expanded MHG lexicon)
# ================================================================
print(f"\n{'=' * 80}")
print("4. HIDDEN WORDS IN GARBLED ZONES")
print("=" * 80)

# Expanded MHG/German candidate words NOT already in KNOWN
MHG_CANDIDATES = [
    # Common MHG words
    'VROUWE', 'RITTER', 'SWERT', 'LIHT', 'GOLT', 'HERZE', 'TUGENT',
    'WORT', 'REDE', 'LEIT', 'VOLC', 'HUOTE', 'SITE', 'MUOT',
    'STAT', 'GNADE', 'WISE', 'TUO', 'GUOT', 'TIUVEL', 'ENGEL',
    'KIRCHE', 'MESSE', 'BUOCH', 'GELOUBE', 'SELE', 'HIMEL',
    # German words that might appear
    'TRUG', 'TIER', 'RECHT', 'LEID', 'MUT', 'RUH', 'RUHE',
    'STIL', 'RECHT', 'LEER', 'IRRE', 'HEER', 'EILE', 'SCHEIN',
    'HEIT', 'REISE', 'REIS', 'STIRN', 'ZIER', 'LIST',
    'LUFT', 'LUST', 'TROST', 'ZUCHT', 'FURCHT', 'DEMUT',
    'TRUTZ', 'WUERDE', 'TUGEND', 'HEILIG', 'INNIG',
    # Place-related
    'GROTTE', 'TURM', 'TOR', 'BRUECKE', 'BURG', 'STADT',
    'STRASSE', 'WEG', 'UFER', 'TAL', 'HOEHLE',
    # Short MHG words missed
    'OUZ', 'UF', 'BI', 'MIT', 'VUR', 'NAH', 'HIN', 'HER',
    'VIL', 'WOL', 'DUR', 'SIT', 'DIC', 'MIC',
    # Religious/death
    'GRAB', 'KREUZ', 'ALTAR', 'OPFER', 'SUEHNE', 'BUSSE',
    'TAUFE', 'PRIESTER', 'MOENCH', 'NONNE', 'KLOSTER',
    'SEELE', 'HIMMEL', 'HOELLE', 'ENGEL', 'TEUFEL',
    # Tibia-specific
    'DRUIDE', 'HEXE', 'THAIS', 'VENORE', 'DEMON',
    'KNOCHEN', 'SCHAEDEL', 'GEBEIN',
]

# Remove words already in KNOWN
MHG_CANDIDATES = [w for w in MHG_CANDIDATES if w not in KNOWN]

# Build garbled position map
garbled_positions = []  # (start_pos, end_pos, content) in resolved text
pos = 0
for t in tokens:
    if t.startswith('{'):
        content = t[1:-1]
        start = resolved.find(content, pos)
        if start >= 0:
            garbled_positions.append((start, start + len(content), content))
            pos = start + len(content)
    else:
        pos += len(t)

# Scan for candidates in garbled zones
print(f"\n  Testing {len(MHG_CANDIDATES)} candidate words in garbled zones:")
hits = []
for word in MHG_CANDIDATES:
    count = 0
    contexts = []
    for gstart, gend, content in garbled_positions:
        idx = content.find(word)
        while idx >= 0:
            count += 1
            abs_pos = gstart + idx
            ctx_s = max(0, abs_pos - 10)
            ctx_e = min(len(resolved), abs_pos + len(word) + 10)
            contexts.append(resolved[ctx_s:ctx_e])
            idx = content.find(word, idx + 1)
    if count >= 2:
        hits.append((word, count, contexts))

hits.sort(key=lambda x: -x[1])
for word, count, contexts in hits:
    print(f"\n    {word} ({count}x):")
    for ctx in contexts[:4]:
        print(f"      ...{ctx}...")

# ================================================================
# 5. SINGLE-LETTER GARBLED BLOCKS
# ================================================================
print(f"\n{'=' * 80}")
print("5. SINGLE-LETTER GARBLED BLOCKS (potential word boundary errors)")
print("=" * 80)

single_letter_blocks = []
for i, t in enumerate(tokens):
    if t.startswith('{') and len(t) == 3:  # {X}
        letter = t[1]
        prev_word = tokens[i-1] if i > 0 else ''
        next_word = tokens[i+1] if i < len(tokens)-1 else ''
        single_letter_blocks.append((letter, prev_word, next_word))

letter_context = defaultdict(list)
for letter, prev_w, next_w in single_letter_blocks:
    letter_context[letter].append((prev_w, next_w))

print(f"\n  Total single-letter garbled: {len(single_letter_blocks)}")
for letter, contexts in sorted(letter_context.items(), key=lambda x: -len(x[1])):
    if len(contexts) >= 2:
        print(f"\n    '{letter}' ({len(contexts)}x):")
        for prev_w, next_w in contexts[:5]:
            pstr = prev_w if not prev_w.startswith('{') else f'[{prev_w[1:-1]}]'
            nstr = next_w if not next_w.startswith('{') else f'[{next_w[1:-1]}]'
            print(f"      ...{pstr} [{letter}] {nstr}...")

# ================================================================
# 6. TWO-LETTER GARBLED BLOCKS
# ================================================================
print(f"\n{'=' * 80}")
print("6. TWO-LETTER GARBLED BLOCKS")
print("=" * 80)

two_letter_blocks = []
for i, t in enumerate(tokens):
    if t.startswith('{') and len(t) == 4:  # {XY}
        content = t[1:-1]
        prev_word = tokens[i-1] if i > 0 else ''
        next_word = tokens[i+1] if i < len(tokens)-1 else ''
        two_letter_blocks.append((content, prev_word, next_word))

pair_context = defaultdict(list)
for content, prev_w, next_w in two_letter_blocks:
    pair_context[content].append((prev_w, next_w))

print(f"\n  Total two-letter garbled: {len(two_letter_blocks)}")
for content, contexts in sorted(pair_context.items(), key=lambda x: -len(x[1])):
    print(f"\n    '{content}' ({len(contexts)}x):")
    for prev_w, next_w in contexts[:5]:
        pstr = prev_w if not prev_w.startswith('{') else f'[{prev_w[1:-1]}]'
        nstr = next_w if not next_w.startswith('{') else f'[{next_w[1:-1]}]'
        # Can prev+content or content+next form a word?
        if not prev_w.startswith('{'):
            combined_prev = prev_w + content
            if combined_prev in KNOWN or combined_prev in ['SEINER', 'DIESEM', 'DIESER']:
                print(f"      ** {prev_w}+{content} = {combined_prev} (MATCH!)")
        if not next_w.startswith('{'):
            combined_next = content + next_w
            if combined_next in KNOWN:
                print(f"      ** {content}+{next_w} = {combined_next} (MATCH!)")
        print(f"      ...{pstr} [{content}] {nstr}...")

# ================================================================
# 7. CONTEXT-BASED WORD COMPLETION
# ================================================================
print(f"\n{'=' * 80}")
print("7. WORD COMPLETION: garbled + known neighbor")
print("=" * 80)

# For each garbled block adjacent to a known word, try combining
completions = []
for i, t in enumerate(tokens):
    if t.startswith('{'):
        content = t[1:-1]
        if len(content) > 4:
            continue  # skip big blocks

        # Try garbled + next_word
        if i + 1 < len(tokens) and not tokens[i+1].startswith('{'):
            combined = content + tokens[i+1]
            # Is this an anagram of any German word?
            sorted_combined = ''.join(sorted(combined))
            for candidate in list(KNOWN) + MHG_CANDIDATES:
                if len(candidate) == len(combined) and ''.join(sorted(candidate)) == sorted_combined:
                    completions.append((f'{{{content}}}+{tokens[i+1]}', combined, candidate, 'anagram'))
                elif candidate == combined:
                    completions.append((f'{{{content}}}+{tokens[i+1]}', combined, candidate, 'direct'))

        # Try prev_word + garbled
        if i > 0 and not tokens[i-1].startswith('{'):
            combined = tokens[i-1] + content
            sorted_combined = ''.join(sorted(combined))
            for candidate in list(KNOWN) + MHG_CANDIDATES:
                if len(candidate) == len(combined) and ''.join(sorted(candidate)) == sorted_combined:
                    completions.append((f'{tokens[i-1]}+{{{content}}}', combined, candidate, 'anagram'))
                elif candidate == combined:
                    completions.append((f'{tokens[i-1]}+{{{content}}}', combined, candidate, 'direct'))

# Deduplicate and show
seen = set()
for source, combined, target, method in completions:
    key = (combined, target)
    if key not in seen:
        seen.add(key)
        print(f"  {source} = {combined} -> {target} ({method})")

# ================================================================
# 8. COVERAGE IF WE ADD TOP CANDIDATES
# ================================================================
print(f"\n{'=' * 80}")
print("8. COVERAGE IMPACT OF NEW CANDIDATES")
print("=" * 80)

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

baseline = dp_count(resolved, KNOWN)
print(f"\n  Baseline: {baseline}/{total} = {baseline/total*100:.1f}%")

# Test adding each hidden word found
if hits:
    print(f"\n  Adding hidden words found in garbled zones:")
    for word, count, _ in hits:
        test_known = set(KNOWN)
        test_known.add(word)
        new_cov = dp_count(resolved, test_known)
        delta = new_cov - baseline
        if delta > 0:
            print(f"    +{word}: {new_cov}/{total} = {new_cov/total*100:.1f}% ({delta:+d} chars)")

print(f"\n  Done.")
