#!/usr/bin/env python3
"""Session 12i: Aggressive full assembly + proper noun analysis"""

import json, re
from collections import Counter, defaultdict

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

# Trim odd-length books
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
    codes = parse_codes(s)
    return ''.join(m.get(c, '?') for c in codes)
def collapse(s):
    return re.sub(r'(.)\1+', r'\1', s)

print("=" * 80)
print("SESSION 12i: AGGRESSIVE ASSEMBLY + PROPER NOUN ANALYSIS")
print("=" * 80)

# 1. Build ALL overlaps with LOWER threshold
print("\n1. ALL OVERLAPS (min 2 codes = 4 digits)")
print("-" * 60)

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

print(f"  Total overlapping pairs: {len(overlaps)}")

# 2. Try EVERY starting book, greedy merge with threshold=2 codes
print("\n2. EXHAUSTIVE GREEDY MERGE (threshold=2 codes)")
print("-" * 60)

best_merged = ''
best_used = set()
best_start = -1
best_contained = set()

for start_idx in range(len(corrected)):
    merged = corrected[start_idx]
    used = {start_idx}

    changed = True
    while changed:
        changed = False
        best_bi = None
        best_ov = 0
        best_side = None
        best_new = ''

        for bi in range(len(corrected)):
            if bi in used: continue
            text = corrected[bi]

            # Right
            for k in range(min(len(merged), len(text)), 3, -2):
                if merged[-k:] == text[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'right'
                        best_new = text[k:]
                    break
            # Left
            for k in range(min(len(merged), len(text)), 3, -2):
                if text[-k:] == merged[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'left'
                        best_new = text[:-k]
                    break

        if best_bi is not None and best_ov >= 4:  # 2 codes = 4 digits
            used.add(best_bi)
            if best_side == 'right':
                merged += best_new
            else:
                merged = best_new + merged
            changed = True

    # Check containment
    contained = set()
    for bi in range(len(corrected)):
        if corrected[bi] in merged:
            contained.add(bi)

    if len(contained) > len(best_contained):
        best_merged = merged
        best_used = set(used)
        best_start = start_idx
        best_contained = set(contained)

print(f"  Best start: B{best_start:02d}")
print(f"  Books merged: {len(best_used)}/{len(corrected)}")
print(f"  Books contained: {len(best_contained)}/{len(corrected)}")
missing = sorted(set(range(len(corrected))) - best_contained)
print(f"  Missing: {missing}")

# 3. Now try to add missing books with LOWER threshold
print("\n3. FORCE-ADDING MISSING BOOKS (lower threshold)")
print("-" * 60)

merged2 = best_merged
added = set()
for threshold in [4, 3, 2]:  # Try decreasing thresholds
    changed = True
    while changed:
        changed = False
        best_bi = None
        best_ov = 0
        best_side = None
        best_new = ''

        for bi in missing:
            if bi in added: continue
            text = corrected[bi]

            # Right
            for k in range(min(len(merged2), len(text)), 1, -2):
                if merged2[-k:] == text[:k]:
                    if k >= threshold and k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'right'
                        best_new = text[k:]
                    break
            # Left
            for k in range(min(len(merged2), len(text)), 1, -2):
                if text[-k:] == merged2[:k]:
                    if k >= threshold and k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'left'
                        best_new = text[:-k]
                    break

        if best_bi is not None:
            added.add(best_bi)
            if best_side == 'right':
                merged2 += best_new
            else:
                merged2 = best_new + merged2
            print(f"  Added B{best_bi:02d} ({best_side}, {best_ov} digits overlap, threshold={threshold})")
            changed = True

# Final containment
contained2 = set()
for bi in range(len(corrected)):
    if corrected[bi] in merged2:
        contained2.add(bi)
print(f"\n  After force-add: {len(contained2)}/{len(corrected)} contained")
still_missing = sorted(set(range(len(corrected))) - contained2)
print(f"  Still missing: {still_missing}")

# 4. For TRULY missing books, what are they?
print("\n4. TRULY MISSING BOOKS ANALYSIS")
print("-" * 60)

for bi in still_missing[:20]:
    text = corrected[bi]
    decoded = collapse(decode_str(text))
    # Find best substring match anywhere in merged2
    best_match = 0
    best_pos = -1
    for start in range(0, len(merged2) - 3, 2):
        mlen = 0
        for k in range(0, min(len(text), len(merged2) - start), 2):
            if text[k:k+2] == merged2[start+k:start+k+2]:
                mlen += 2
            else:
                break
        if mlen > best_match:
            best_match = mlen
            best_pos = start
    pct = best_match * 100 / len(text) if len(text) > 0 else 0
    print(f"  B{bi:02d}: {len(text)//2} codes, best prefix match={best_match//2} codes ({pct:.0f}%)")
    print(f"    Text: {decoded[:60]}...")

# 5. Full decoded text with improved segmentation
print("\n5. FULL DECODED NARRATIVE")
print("-" * 60)

full_decoded = collapse(decode_str(merged2))
print(f"  Superstring: {len(merged2)//2} codes")
print(f"  Collapsed text: {len(full_decoded)} chars")
print()
for i in range(0, len(full_decoded), 70):
    print(f"  [{i:4d}] {full_decoded[i:i+70]}")

# 6. MANUAL segmentation of the proper nouns
print("\n6. PROPER NOUN DEEP ANALYSIS")
print("-" * 60)

proper_nouns = [
    'TAUTR', 'EILCHANHEARUCHTIG', 'EDETOTNIURGS',
    'HEDEMI', 'ADTHARSC', 'LABRNI', 'ENGCHD',
    'KELSEI', 'TIUMENGEMI', 'LABGZERAS', 'SCHWITEIONE',
    'WRLGTNELNRHELUIRUN', 'GEVMT', 'DGEDA', 'TEMDIA', 'UISEMIV'
]

for noun in proper_nouns:
    # Count occurrences in full decoded text
    count = full_decoded.count(noun)
    # Find context (10 chars before and after)
    positions = []
    pos = 0
    while True:
        idx = full_decoded.find(noun, pos)
        if idx == -1: break
        before = full_decoded[max(0,idx-15):idx]
        after = full_decoded[idx+len(noun):idx+len(noun)+15]
        positions.append((idx, before, after))
        pos = idx + 1

    if positions:
        print(f"\n  {noun} ({count}x):")
        for idx, before, after in positions:
            print(f"    [{idx:4d}] ...{before}|{noun}|{after}...")

    # Try reversing
    rev = noun[::-1]
    if rev in full_decoded:
        print(f"    ** REVERSED found: {rev}")

    # Try as German word parts
    # Check if it could be a compound word
    if len(noun) >= 8:
        # Try splitting at every position
        splits = []
        for sp in range(2, len(noun)-1):
            left = noun[:sp]
            right = noun[sp:]
            splits.append(f"{left}+{right}")
        print(f"    Possible splits: {', '.join(splits[:5])}...")

# 7. What if the mapping has specific errors? Check letter patterns
print("\n7. LETTER FREQUENCY IN CONTEXT")
print("-" * 60)

# Compare letter frequency of decoded text vs German
all_letters = Counter(full_decoded)
total = sum(all_letters.values())

expected = {
    'E': 17.4, 'N': 9.8, 'I': 7.6, 'S': 7.3, 'R': 7.0,
    'A': 6.5, 'T': 6.2, 'D': 5.1, 'H': 4.8, 'U': 4.3,
    'L': 3.4, 'C': 3.1, 'G': 3.0, 'M': 2.5, 'O': 2.5,
    'B': 1.9, 'W': 1.9, 'F': 1.7, 'K': 1.2, 'Z': 1.1,
    'V': 0.9, 'P': 0.8
}

print(f"  Letter frequency analysis (collapsed text, {total} chars):")
deviances = []
for letter in sorted(all_letters.keys()):
    actual = all_letters[letter] * 100 / total
    exp = expected.get(letter, 0)
    diff = actual - exp
    deviances.append((letter, actual, exp, diff))
    flag = ' <-- SWAP CANDIDATE' if abs(diff) > 2.5 else ''
    print(f"    {letter}: {actual:5.1f}% (exp {exp:.1f}%, diff {diff:+.1f}%){flag}")

# 8. Try swapping the most deviant letters
print("\n8. TARGETED LETTER SWAPS")
print("-" * 60)

# Most over-represented: I (+2.9%), most under: B, F, P
# What if some I codes should be B, F, or P?
i_codes = [c for c, l in mapping.items() if l == 'I']
print(f"  I codes ({len(i_codes)}): {i_codes}")

# For each I code, count its frequency
all_codes = [c for s in corrected for c in parse_codes(s)]
code_freq = Counter(all_codes)

for code in i_codes:
    freq = code_freq.get(code, 0)
    print(f"    Code {code} -> I: {freq}x")

# Try reassigning least-used I codes to B, F, or P
# Test each reassignment
NEG_INF = float('-inf')
german_words = [
    'KOENIG', 'GEIGET', 'SCHAUN', 'URALTE', 'FINDEN', 'DIESER',
    'NORDEN', 'SONNE', 'UNTER', 'NICHT', 'WERDE',
    'STEINEN', 'STEIN', 'DENEN', 'ERDE', 'VIEL', 'RUNE',
    'STEH', 'LIED', 'SEGEN', 'DORT', 'DENN',
    'GOLD', 'MOND', 'WELT', 'ENDE', 'REDE',
    'HUND', 'SEIN', 'WIRD', 'KLAR', 'ERST',
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
    'WARD', 'WART', 'BALD', 'BERG', 'BURG',
    'FEUER', 'FLAMME', 'BLUT', 'FLUCH', 'BRIEF',
    'PFAD', 'PFLICHT', 'PRACHT',
    'ER', 'ES', 'IN', 'SO', 'AN', 'IM',
    'DA', 'NU', 'IR', 'EZ', 'DO', 'OB',
    'DU', 'HAT', 'BIS',
    'UM', 'AM', 'AB', 'ZU', 'ALT', 'NEU', 'DIR', 'MAN',
    'BEI', 'FUR', 'VOR',
]
german_words = list(dict.fromkeys(german_words))

def count_words(text, words):
    count = 0
    for w in words:
        idx = 0
        while True:
            pos = text.find(w, idx)
            if pos == -1: break
            count += len(w)
            idx = pos + 1
    return count

baseline = count_words(full_decoded, german_words)
print(f"\n  Baseline word coverage: {baseline}")

# Test swapping each I code to B, F, P
improvements = []
for code in i_codes:
    for new_letter in ['B', 'F', 'P']:
        test_map = dict(mapping)
        test_map[code] = new_letter
        test_decoded = collapse(decode_str(merged2, test_map))
        score = count_words(test_decoded, german_words)
        if score > baseline:
            improvements.append((code, new_letter, score, score - baseline))

if improvements:
    improvements.sort(key=lambda x: -x[3])
    print(f"  Improvements found:")
    for code, letter, score, diff in improvements[:10]:
        print(f"    Code {code}: I -> {letter}: +{diff} coverage")
else:
    print("  No improvements found from I swaps")

# 9. Try to find Tibia-specific names in the decoded text
print("\n9. TIBIA LORE SEARCH IN DECODED TEXT")
print("-" * 60)

tibia_names = [
    # Places
    'EDRON', 'THAIS', 'CARLIN', 'VENORE', 'DARASHIA', 'KAZORDOON',
    'ANKRAHMUN', 'DREFIA', 'HELLGATE', 'MINTWALLIN', 'CYCLOPOLIS',
    'DEMONA', 'FIBULA', 'ROOKGAARD', 'SENJA', 'FOLDA', 'VEGA',
    'GHOSTLAND', 'BANUTA', 'GOROMA', 'FEYRIST',
    # NPCs/Characters
    'FERUMBRAS', 'ZATHROTH', 'FARDOS', 'UMAN', 'CRUNOR', 'KIROK',
    'BORETH', 'LYKAN', 'TIBIANUS', 'EXCALIBUG',
    'ORSHABAAL', 'MORGAROTH', 'GHAZBARAN', 'BAZIR', 'ASHFALOR',
    'NICHTDA', 'OLDRAK',
    # Monsters
    'BONELORD', 'BRAINDEATH', 'ELDER', 'DEMON', 'DRAGON',
    'WARLOCK', 'NECROMANCER', 'LICH', 'VAMPIRE',
    # Gods/Concepts
    'BANOR', 'BASTESH', 'FAFNAR', 'SUON', 'SULA',
    'THAIAN', 'CREATOR',
    # German versions
    'KOENIG', 'STEIN', 'RUNEN', 'DRACHE', 'DAEMON',
    'FLAMME', 'SONNE', 'MOND',
    # Old German Tibia
    'KNIGHTWATCH', 'STONEHOME', 'EXCALIBUR',
]

found_names = []
for name in tibia_names:
    if name in full_decoded:
        idx = full_decoded.find(name)
        before = full_decoded[max(0,idx-10):idx]
        after = full_decoded[idx+len(name):idx+len(name)+10]
        found_names.append((name, idx, before, after))
        print(f"  FOUND: {name} at [{idx}]: ...{before}|{name}|{after}...")

if not found_names:
    print("  No exact Tibia names found in decoded text")

# Also search for partial matches (3+ chars)
print("\n  Partial matches (4+ chars):")
for name in tibia_names:
    if len(name) < 4: continue
    for sublen in range(len(name), 3, -1):
        sub = name[:sublen]
        if sub in full_decoded and len(sub) >= 4:
            idx = full_decoded.find(sub)
            print(f"    {name} prefix '{sub}' at [{idx}]")
            break

# 10. What do the proper nouns look like if we DON'T collapse?
print("\n10. PROPER NOUNS WITHOUT COLLAPSE")
print("-" * 60)

uncollapsed = decode_str(merged2)
for noun in ['TAUTR', 'EILCHANHEARUCHTIG', 'EDETOTNIURGS', 'HEDEMI', 'ADTHARSC', 'LABRNI']:
    # Find noun in collapsed, map back to uncollapsed position
    idx = full_decoded.find(noun)
    if idx >= 0:
        # Rough mapping: for each char in collapsed, find corresponding uncollapsed
        # This is approximate
        ci = 0
        ui = 0
        while ci < idx and ui < len(uncollapsed):
            while ui + 1 < len(uncollapsed) and uncollapsed[ui+1] == uncollapsed[ui]:
                ui += 1
            ci += 1
            ui += 1
        # Extract uncollapsed region
        end_ci = ci + len(noun)
        end_ui = ui
        while ci < end_ci and end_ui < len(uncollapsed):
            while end_ui + 1 < len(uncollapsed) and uncollapsed[end_ui+1] == uncollapsed[end_ui]:
                end_ui += 1
            ci += 1
            end_ui += 1
        uncollapsed_noun = uncollapsed[ui:end_ui]
        print(f"  {noun} -> uncollapsed: {uncollapsed_noun}")

print("\n" + "=" * 80)
print("SESSION 12i COMPLETE")
print("=" * 80)
