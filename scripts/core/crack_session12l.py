#!/usr/bin/env python3
"""Session 12l: Substring alignment assembly
Instead of suffix/prefix overlaps, find where each book ALIGNS within the growing superstring."""

import json, re
from collections import Counter

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

corrected = []
for book_str in raw_books:
    if len(book_str) % 2 != 0:
        corrected.append(book_str[:-1])
    else:
        corrected.append(book_str)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]
def decode_str(s, m=None):
    if m is None: m = mapping
    return ''.join(m.get(c, '?') for c in parse_codes(s))
def collapse(s):
    return re.sub(r'(.)\1+', r'\1', s)

print("=" * 80)
print("SESSION 12l: SUBSTRING ALIGNMENT ASSEMBLY")
print("=" * 80)

# Decode all books
decoded = [decode_str(s) for s in corrected]
collapsed = [collapse(d) for d in decoded]

# 1. Start with the raw-code-level superstring as seed
print("\n1. BUILDING SEED SUPERSTRING")
print("-" * 60)

# Use the raw-code-level best assembly as seed
overlaps = {}
for i in range(len(corrected)):
    for j in range(len(corrected)):
        if i == j: continue
        si = corrected[i]
        sj = corrected[j]
        for k in range(min(len(si), len(sj)), 3, -2):
            if si[-k:] == sj[:k]:
                overlaps[(i,j)] = k // 2
                break

best_merged_raw = ''
best_contained_raw = set()
for start_idx in range(len(corrected)):
    merged = corrected[start_idx]
    used = {start_idx}
    changed = True
    while changed:
        changed = False
        b_bi = None
        b_ov = 0
        b_side = None
        b_new = ''
        for bi in range(len(corrected)):
            if bi in used: continue
            text = corrected[bi]
            for k in range(min(len(merged), len(text)), 3, -2):
                if merged[-k:] == text[:k]:
                    if k > b_ov:
                        b_ov = k
                        b_bi = bi
                        b_side = 'right'
                        b_new = text[k:]
                    break
            for k in range(min(len(merged), len(text)), 3, -2):
                if text[-k:] == merged[:k]:
                    if k > b_ov:
                        b_ov = k
                        b_bi = bi
                        b_side = 'left'
                        b_new = text[:-k]
                    break
        if b_bi is not None and b_ov >= 4:
            used.add(b_bi)
            if b_side == 'right':
                merged += b_new
            else:
                merged = b_new + merged
            changed = True
    contained = set()
    for bi in range(len(corrected)):
        if corrected[bi] in merged:
            contained.add(bi)
    if len(contained) > len(best_contained_raw):
        best_merged_raw = merged
        best_contained_raw = set(contained)

seed_decoded = decode_str(best_merged_raw)
seed_collapsed = collapse(seed_decoded)
print(f"  Seed: {len(parse_codes(best_merged_raw))} codes, {len(seed_collapsed)} collapsed chars")
print(f"  Books contained in seed: {len(best_contained_raw)}")

# 2. For EACH non-contained book, find its best alignment to the seed
# using longest common substring at the decoded level
print("\n2. ALIGNING MISSING BOOKS TO SEED")
print("-" * 60)

def longest_common_substring(s1, s2):
    """Find the longest common substring between s1 and s2.
    Returns (length, start_in_s1, start_in_s2)"""
    m, n = len(s1), len(s2)
    best_len = 0
    best_i = 0
    best_j = 0
    # Use suffix array approach for efficiency
    # But for moderate strings, simple dp is fine
    # Optimized: skip if remaining length can't beat current best
    for i in range(m):
        if m - i <= best_len: break
        for j in range(n):
            if n - j <= best_len: break
            k = 0
            while i+k < m and j+k < n and s1[i+k] == s2[j+k]:
                k += 1
            if k > best_len:
                best_len = k
                best_i = i
                best_j = j
    return best_len, best_i, best_j

# Work with decoded (uncollapsed) text for alignment
super_decoded = seed_decoded
alignments = []

missing = sorted(set(range(len(decoded))) - best_contained_raw)
for bi in missing:
    book_dec = decoded[bi]
    lcs_len, lcs_super, lcs_book = longest_common_substring(super_decoded, book_dec)
    pct = lcs_len * 100 / len(book_dec)

    if lcs_len >= 5:
        # Calculate extension: how much of the book is outside the superstring
        left_ext = lcs_book  # chars in book before the matched region
        right_ext = len(book_dec) - (lcs_book + lcs_len)  # chars after

        alignments.append((bi, lcs_len, lcs_super, lcs_book, left_ext, right_ext, pct))
        if pct >= 20 or lcs_len >= 20:
            lcs_text = collapse(book_dec[lcs_book:lcs_book+lcs_len])
            print(f"  B{bi:02d}: LCS={lcs_len} chars ({pct:.0f}%), L.ext={left_ext}, R.ext={right_ext}")
            print(f"    Matched: '{lcs_text[:50]}...'")

alignments.sort(key=lambda x: -x[1])

# 3. Extend the superstring using aligned books
print("\n3. EXTENDING SUPERSTRING WITH ALIGNED BOOKS")
print("-" * 60)

# Use iterative extension: add the best-aligned book first, then re-align
extended = super_decoded
used_books = set(best_contained_raw)
iteration = 0

while True:
    iteration += 1
    best_extension = None
    best_total_new = 0
    best_bi = None

    for bi in range(len(decoded)):
        if bi in used_books: continue
        book_dec = decoded[bi]

        # Find LCS with current extended superstring
        lcs_len, lcs_ext, lcs_book = longest_common_substring(extended, book_dec)

        if lcs_len < 5: continue

        left_ext = lcs_book
        right_ext = len(book_dec) - (lcs_book + lcs_len)

        # Calculate what the book adds
        # Left extension: book[0:lcs_book] goes before extended[lcs_ext]
        # Right extension: book[lcs_book+lcs_len:] goes after extended[lcs_ext+lcs_len]
        total_new = left_ext + right_ext

        # Only extend if alignment is reliable (covers >30% of book)
        pct = lcs_len * 100 / len(book_dec)
        if pct >= 30 and total_new > 0 and lcs_len > best_total_new:
            # Prefer longer matches
            best_extension = (lcs_ext, lcs_book, lcs_len, left_ext, right_ext, book_dec)
            best_total_new = lcs_len
            best_bi = bi

    if best_bi is None:
        break

    lcs_ext, lcs_book, lcs_len, left_ext, right_ext, book_dec = best_extension
    used_books.add(best_bi)

    # Extend the superstring
    new_left = book_dec[:lcs_book] if left_ext > 0 else ''
    new_right = book_dec[lcs_book+lcs_len:] if right_ext > 0 else ''

    if left_ext > 0:
        # Insert new_left before position lcs_ext in extended
        extended = extended[:lcs_ext] + new_left + extended[lcs_ext:]
    if right_ext > 0:
        # Append new_right after position lcs_ext + lcs_len + left_ext
        insert_pos = lcs_ext + left_ext + lcs_len
        extended = extended[:insert_pos] + new_right + extended[insert_pos:]

    ext_collapsed = collapse(extended)
    pct = lcs_len * 100 / len(book_dec)
    print(f"  Iter {iteration}: Added B{best_bi:02d} (LCS={lcs_len}, {pct:.0f}%, L+={left_ext}, R+={right_ext}) -> {len(ext_collapsed)} chars")

    if iteration > 50: break

# 4. Check containment of extended superstring
print("\n4. EXTENDED SUPERSTRING RESULTS")
print("-" * 60)

ext_collapsed = collapse(extended)
contained_ext = set()
for bi in range(len(decoded)):
    if decoded[bi] in extended:
        contained_ext.add(bi)
    elif collapsed[bi] in ext_collapsed:
        contained_ext.add(bi)

print(f"  Extended decoded: {len(extended)} chars")
print(f"  Collapsed: {len(ext_collapsed)} chars")
print(f"  Books contained (decoded): {len(contained_ext)}/{len(decoded)}")
still_missing = sorted(set(range(len(decoded))) - contained_ext)
print(f"  Still missing: {still_missing}")

# 5. Display the narrative
print("\n5. FULL NARRATIVE")
print("-" * 60)
for i in range(0, len(ext_collapsed), 70):
    print(f"  [{i:4d}] {ext_collapsed[i:i+70]}")

# 6. DP segment
print("\n6. DP SEGMENTED NARRATIVE")
print("-" * 60)

NEG_INF = float('-inf')
german_words = [
    'EILCHANHEARUCHTIG', 'EDETOTNIURGS', 'WRLGTNELNRHELUIRUN',
    'TIUMENGEMI', 'SCHWITEIONE', 'LABGZERAS', 'HEDEMI', 'TAUTR',
    'LABRNI', 'ADTHARSC', 'ENGCHD', 'KELSEI',
    'NGETRAS', 'GEVMT', 'TEIGN', 'CHN', 'SCE',
    'KOENIG', 'GEIGET', 'SCHAUN', 'URALTE', 'FINDEN', 'DIESER',
    'NORDEN', 'SONNE', 'UNTER', 'NICHT', 'WERDE',
    'STEINEN', 'STEIN', 'STEINE', 'DENEN', 'ERDE', 'VIEL', 'RUNE', 'RUNEN',
    'STEH', 'LIED', 'SEGEN', 'DORT', 'DENN',
    'GOLD', 'MOND', 'WELT', 'ENDE', 'REDE',
    'HUND', 'SEIN', 'WIRD', 'KLAR', 'ERST',
    'HWND', 'WISET', 'OWI', 'MINHE',
    'EINEN', 'EINER', 'SEINE', 'SEIDE',
    'TAG', 'WEG', 'DER', 'DEN', 'DIE', 'DAS',
    'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON',
    'MIT', 'WIE', 'SEI', 'AUS', 'ORT', 'TUN',
    'NUR', 'SUN', 'TOT', 'GAR', 'ACH', 'ZUM',
    'HIN', 'HER', 'ALS', 'AUCH', 'RUND', 'GEH',
    'NACH', 'NOCH', 'ALLE', 'WOHL',
    'HIER', 'SICH', 'SIND', 'SEHR',
    'ABER', 'ODER', 'WENN', 'DANN',
    'ALTE', 'EDEL', 'HELD', 'LAND',
    'WARD', 'WART', 'SICHER',
    'ER', 'ES', 'IN', 'SO', 'AN', 'IM',
    'DA', 'NU', 'IR', 'EZ', 'DO', 'OB', 'IE',
    'TER', 'HIET', 'DU', 'HAT', 'BIS', 'SINE',
    'EHRE', 'NIDEN', 'DENN', 'AUCH',
    'UM', 'AM', 'AB', 'ZU', 'BI', 'ALT', 'NEU', 'DIR', 'MAN',
]
german_words = list(dict.fromkeys(german_words))
word_scores = {w: len(w) * 3 for w in german_words}
all_gwords = sorted(word_scores.keys(), key=len, reverse=True)

def dp_segment(text):
    n = len(text)
    if n == 0: return [], 0, 0
    dp = [NEG_INF] * (n + 1)
    back = [None] * (n + 1)
    dp[0] = 0
    for i in range(n):
        if dp[i] == NEG_INF: continue
        ns = dp[i] - 1
        if ns > dp[i+1]:
            dp[i+1] = ns
            back[i+1] = ('unk', i)
        for word in all_gwords:
            wl = len(word)
            if i + wl <= n and text[i:i+wl] == word:
                ns = dp[i] + word_scores.get(word, wl)
                if ns > dp[i+wl]:
                    dp[i+wl] = ns
                    back[i+wl] = ('word', i, word)
    pos = n
    parts = []
    covered = 0
    while pos > 0:
        info = back[pos]
        if info is None:
            parts.append(('?', text[pos-1:pos]))
            pos -= 1
        elif info[0] == 'unk':
            parts.append(('?', text[info[1]:pos]))
            pos = info[1]
        elif info[0] == 'word':
            parts.append(('W', info[2]))
            covered += len(info[2])
            pos = info[1]
    parts.reverse()
    return parts, covered, n

parts, covered, total = dp_segment(ext_collapsed)
print(f"  Coverage: {covered}/{total} = {covered*100/total:.1f}%\n")

line = ''
line_num = 1
for ptype, ptext in parts:
    if ptype == 'W':
        word = ptext
    else:
        word = f'[{ptext}]'
    if len(line) + len(word) + 1 > 75:
        print(f"    {line_num:3d}| {line}")
        line = word + ' '
        line_num += 1
    else:
        line += word + ' '
if line.strip():
    print(f"    {line_num:3d}| {line}")

# 7. Are there SEPARATE narrative segments?
print("\n7. SEPARATE NARRATIVE SEGMENTS")
print("-" * 60)

# Group the missing books by shared content
# Find connected components among missing books
if still_missing:
    # Find all pairs that share decoded substrings of 10+ chars
    missing_connections = {}
    for i in still_missing:
        for j in still_missing:
            if i >= j: continue
            lcs_len, _, _ = longest_common_substring(decoded[i], decoded[j])
            if lcs_len >= 10:
                missing_connections.setdefault(i, set()).add(j)
                missing_connections.setdefault(j, set()).add(i)

    # Find connected components
    visited = set()
    components = []
    for bi in still_missing:
        if bi in visited: continue
        component = set()
        stack = [bi]
        while stack:
            node = stack.pop()
            if node in visited: continue
            visited.add(node)
            component.add(node)
            for neighbor in missing_connections.get(node, set()):
                if neighbor not in visited:
                    stack.append(neighbor)
        components.append(sorted(component))

    print(f"  Components among missing books: {len(components)}")
    for ci, comp in enumerate(components[:10]):
        total_chars = sum(len(collapsed[bi]) for bi in comp)
        print(f"    Component {ci}: {comp} ({total_chars} total collapsed chars)")

    # Try to assemble each component separately
    for ci, comp in enumerate(components[:5]):
        if len(comp) < 2: continue
        # Greedy assembly within component
        comp_decoded = {bi: decoded[bi] for bi in comp}
        best_comp = ''
        best_comp_n = 0
        for start in comp:
            m = comp_decoded[start]
            u = {start}
            ch = True
            while ch:
                ch = False
                b_bi = None
                b_ov = 0
                b_side = None
                b_new = ''
                for bi in comp:
                    if bi in u: continue
                    text = comp_decoded[bi]
                    lcs_len, lcs_m, lcs_b = longest_common_substring(m, text)
                    if lcs_len >= 5:
                        if lcs_len > b_ov:
                            b_ov = lcs_len
                            b_bi = bi
                            b_side = (lcs_m, lcs_b, lcs_len)
                if b_bi is not None:
                    u.add(b_bi)
                    lcs_m, lcs_b, lcs_len = b_side
                    text = comp_decoded[b_bi]
                    left = text[:lcs_b]
                    right = text[lcs_b+lcs_len:]
                    if lcs_b > 0:
                        m = m[:lcs_m] + left + m[lcs_m:]
                    if len(right) > 0:
                        insert_pos = lcs_m + len(left) + lcs_len
                        m = m[:insert_pos] + right + m[insert_pos:]
                    ch = True
            if len(u) > best_comp_n:
                best_comp = m
                best_comp_n = len(u)

        comp_collapsed = collapse(best_comp)
        print(f"\n    Component {ci} assembled: {best_comp_n} books, {len(comp_collapsed)} collapsed chars")
        print(f"    Text: {comp_collapsed[:120]}...")

print("\n" + "=" * 80)
print("SESSION 12l COMPLETE")
print("=" * 80)
