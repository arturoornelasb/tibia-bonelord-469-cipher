#!/usr/bin/env python3
"""Session 12j: Code-level proper noun forensics + targeted mapping repair"""

import json, re
from collections import Counter, defaultdict
from itertools import product

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
    codes = parse_codes(s)
    return ''.join(m.get(c, '?') for c in codes)
def collapse(s):
    return re.sub(r'(.)\1+', r'\1', s)

print("=" * 80)
print("SESSION 12j: CODE-LEVEL FORENSICS")
print("=" * 80)

# Build the superstring (reuse best approach from 12i)
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

best_merged = ''
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
            for k in range(min(len(merged), len(text)), 3, -2):
                if merged[-k:] == text[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'right'
                        best_new = text[k:]
                    break
            for k in range(min(len(merged), len(text)), 3, -2):
                if text[-k:] == merged[:k]:
                    if k > best_ov:
                        best_ov = k
                        best_bi = bi
                        best_side = 'left'
                        best_new = text[:-k]
                    break
        if best_bi is not None and best_ov >= 4:
            used.add(best_bi)
            if best_side == 'right':
                merged += best_new
            else:
                merged = best_new + merged
            changed = True
    contained = set()
    for bi in range(len(corrected)):
        if corrected[bi] in merged:
            contained.add(bi)
    if len(contained) > len(best_contained):
        best_merged = merged
        best_contained = set(contained)

super_codes = parse_codes(best_merged)
super_decoded = ''.join(mapping.get(c, '?') for c in super_codes)
super_collapsed = collapse(super_decoded)

print(f"\n  Superstring: {len(super_codes)} codes, {len(super_collapsed)} collapsed chars")

# 1. Map proper nouns to their raw codes
print("\n1. PROPER NOUNS -> RAW CODES")
print("-" * 60)

# Find the codes for each proper noun by searching in the collapsed text
# and mapping back to code positions
def find_codes_for_text(target, collapsed, decoded, codes):
    """Find the raw codes that produce a given collapsed text substring"""
    idx = collapsed.find(target)
    if idx == -1:
        return None, -1

    # Map collapsed position to decoded position
    ci = 0
    di = 0
    while ci < idx and di < len(decoded):
        while di + 1 < len(decoded) and decoded[di+1] == decoded[di]:
            di += 1
        ci += 1
        di += 1

    start_di = di
    ci_end = ci + len(target)
    while ci < ci_end and di < len(decoded):
        while di + 1 < len(decoded) and decoded[di+1] == decoded[di]:
            di += 1
        ci += 1
        di += 1
    end_di = di

    # Each decoded char = 1 code
    return codes[start_di:end_di], start_di

nouns = ['TAUTR', 'EILCHANHEARUCHTIG', 'EDETOTNIURGS', 'HEDEMI',
         'ADTHARSC', 'LABRNI', 'ENGCHD', 'KELSEI', 'TIUMENGEMI',
         'SCHWITEIONE', 'WRLGTNELNRHELUIRUN', 'GEVMT']

# Also check for LABGZERAS in individual books since it might not be in main superstring
for noun in nouns:
    noun_codes, pos = find_codes_for_text(noun, super_collapsed, super_decoded, super_codes)
    if noun_codes:
        decoded_check = ''.join(mapping.get(c, '?') for c in noun_codes)
        collapsed_check = collapse(decoded_check)
        print(f"\n  {noun} (at decoded pos {pos}):")
        print(f"    Codes: {' '.join(noun_codes)}")
        print(f"    Decoded: {decoded_check}")
        print(f"    Collapsed: {collapsed_check}")

        # Show code frequencies
        code_freqs = Counter(c for s in corrected for c in parse_codes(s))
        for c in noun_codes:
            letter = mapping.get(c, '?')
            freq = code_freqs.get(c, 0)
            # Check if this code is "confirmed" (appears in known word contexts)
            print(f"      {c}->{letter} ({freq}x)")

# 2. Look for LABGZERAS in individual books
print("\n2. LABGZERAS SEARCH")
print("-" * 60)

for bi in range(len(corrected)):
    decoded = collapse(decode_str(corrected[bi]))
    if 'LABGZERAS' in decoded:
        idx = decoded.find('LABGZERAS')
        codes = parse_codes(corrected[bi])
        noun_codes, pos = find_codes_for_text('LABGZERAS', decoded,
                                              decode_str(corrected[bi]), codes)
        print(f"  Found in B{bi:02d} at pos {pos}")
        if noun_codes:
            print(f"    Codes: {' '.join(noun_codes)}")
            decoded_check = ''.join(mapping.get(c, '?') for c in noun_codes)
            print(f"    Decoded: {decoded_check}")
        before = decoded[max(0,idx-15):idx]
        after = decoded[idx+9:idx+24]
        print(f"    Context: ...{before}|LABGZERAS|{after}...")

# 3. For each unreadable noun, try ALL possible letter assignments
print("\n3. TARGETED CODE REASSIGNMENT TESTS")
print("-" * 60)

# Get all codes that appear in the corpus
all_codes_list = [c for s in corrected for c in parse_codes(s)]
code_freq = Counter(all_codes_list)
all_letters = 'ABCDEFGHIKLMNOPRSTUVWZ'

# For WRLGTNELNRHELUIRUN - this is the most suspicious sequence
# Let's see what codes produce it
wrl_codes, wrl_pos = find_codes_for_text('WRLGTNELNRHELUIRUN', super_collapsed, super_decoded, super_codes)
if wrl_codes:
    print(f"\n  WRLGTNELNRHELUIRUN codes: {' '.join(wrl_codes)}")
    # Try reassigning each code to see what makes the most sense
    # For each code in this noun that maps to an unusual consonant cluster,
    # try all other letters
    best_readings = []
    for ci, code in enumerate(wrl_codes):
        original = mapping.get(code, '?')
        for new_letter in all_letters:
            if new_letter == original: continue
            test = list(wrl_codes)
            # Build test string with this one code changed
            test_decoded = ''
            for tc in test:
                if tc == code:
                    test_decoded += new_letter
                else:
                    test_decoded += mapping.get(tc, '?')
            test_collapsed = collapse(test_decoded)
            # Score: count recognizable substrings
            score = 0
            test_words = ['WUNDER', 'UNTER', 'RUNE', 'RUNEN', 'HELD', 'HELDEN',
                         'ERDE', 'NORDEN', 'STERN', 'GOTT', 'LICHT', 'NACHT',
                         'FINDEN', 'STEHEN', 'GEGEN', 'DURCH', 'DUNKEL',
                         'KRAFT', 'MACHT', 'RECHT', 'SCHLECHT', 'SCHEIN',
                         'STEIN', 'BEIN', 'REIN', 'KLEIN', 'FEIN',
                         'WELT', 'GELD', 'FELD', 'ZELT',
                         'BERG', 'BURG', 'TURM', 'WURM']
            for w in test_words:
                if w in test_collapsed:
                    score += len(w)
            if score > 0:
                best_readings.append((code, original, new_letter, test_collapsed, score))

    if best_readings:
        best_readings.sort(key=lambda x: -x[4])
        print(f"  Readings with recognizable words:")
        for code, orig, new, text, score in best_readings[:10]:
            print(f"    {code}: {orig}->{new}: {text} (score={score})")
    else:
        print(f"  No single-code change produces recognizable words")

# 4. Try PAIR swaps for the most suspicious codes
print("\n4. SYSTEMATIC PAIR REASSIGNMENT")
print("-" * 60)

# The "unconfirmed" codes - those that don't appear in ANY known word context
# Build set of confirmed codes
known_words_codes = set()
german_words = [
    'KOENIG', 'SCHAUN', 'URALTE', 'FINDEN', 'DIESER',
    'STEINEN', 'STEIN', 'ERDE', 'RUNE', 'STEH', 'SEGEN',
    'GOLD', 'MOND', 'WELT', 'ENDE', 'SEIN', 'WIRD',
    'EINEN', 'EINER', 'SEINE',
    'TAG', 'WEG', 'DER', 'DEN', 'DIE', 'DAS',
    'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON',
    'MIT', 'WIE', 'SEI', 'AUS', 'ORT', 'TUN',
    'NUR', 'HIER', 'SICH', 'SIND',
    'ABER', 'ODER', 'WENN', 'DANN',
    'ALTE', 'EDEL', 'HELD', 'LAND',
    'ER', 'ES', 'IN', 'SO', 'AN', 'IM',
    'DA', 'DU', 'HAT', 'BIS',
    'UM', 'AM', 'AB', 'ZU',
]

# For each known word, find all instances in the superstring and mark codes as confirmed
for word in german_words:
    for bi in range(len(corrected)):
        decoded = collapse(decode_str(corrected[bi]))
        idx = 0
        while True:
            pos = decoded.find(word, idx)
            if pos == -1: break
            # Find which codes correspond to this word
            word_codes_found, _ = find_codes_for_text(word, decoded,
                decode_str(corrected[bi]), parse_codes(corrected[bi]))
            if word_codes_found:
                for c in word_codes_found:
                    known_words_codes.add(c)
            idx = pos + 1

all_used_codes = set(code_freq.keys())
unconfirmed = sorted(all_used_codes - known_words_codes)
print(f"  Confirmed codes: {len(known_words_codes)}")
print(f"  Unconfirmed codes: {len(unconfirmed)}")
print(f"  Unconfirmed: {unconfirmed}")

# Show what letters the unconfirmed codes map to
unconf_by_letter = defaultdict(list)
for c in unconfirmed:
    letter = mapping.get(c, '?')
    unconf_by_letter[letter].append((c, code_freq.get(c, 0)))

print(f"\n  Unconfirmed codes by letter:")
for letter in sorted(unconf_by_letter.keys()):
    codes = unconf_by_letter[letter]
    codes_str = ', '.join(f'{c}({f}x)' for c, f in codes)
    print(f"    {letter}: {codes_str}")

# 5. Try swapping each unconfirmed code to every other letter
print("\n5. UNCONFIRMED CODE REASSIGNMENT SCAN")
print("-" * 60)

# Use the full corpus for testing
all_collapsed = [collapse(decode_str(s)) for s in corrected]
full_text = ''.join(all_collapsed)

# Expanded word list for scoring
score_words = [
    'KOENIG', 'SCHAUN', 'URALTE', 'FINDEN', 'DIESER', 'NORDEN', 'SONNE',
    'UNTER', 'NICHT', 'WERDE', 'STEINEN', 'STEIN', 'DENEN', 'ERDE',
    'VIEL', 'RUNE', 'STEH', 'LIED', 'SEGEN', 'DORT', 'DENN',
    'GOLD', 'MOND', 'WELT', 'ENDE', 'REDE', 'HUND', 'SEIN', 'WIRD',
    'EINEN', 'EINER', 'SEINE', 'TAG', 'WEG', 'DER', 'DEN', 'DIE', 'DAS',
    'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON', 'MIT', 'WIE', 'SEI', 'AUS',
    'ORT', 'TUN', 'NUR', 'HIN', 'HER', 'ALS', 'AUCH', 'RUND', 'GEH',
    'NACH', 'NOCH', 'ALLE', 'WOHL', 'HIER', 'SICH', 'SIND', 'SEHR',
    'ABER', 'ODER', 'WENN', 'DANN', 'ALTE', 'EDEL', 'HELD', 'LAND',
    'WARD', 'WART', 'ER', 'ES', 'IN', 'SO', 'AN', 'IM', 'DA', 'DU',
    'HAT', 'BIS', 'UM', 'AM', 'AB', 'ZU', 'ALT', 'NEU', 'DIR', 'MAN',
    'BEI', 'FUR', 'VOR', 'BALD', 'BERG', 'BURG', 'BLUT', 'FEUER',
    'FLAMME', 'FLUCH', 'BRIEF', 'PFAD', 'NACHT', 'LICHT', 'KRAFT',
    'MACHT', 'DUNKEL', 'STERN', 'GOTT', 'DRACHE', 'DAEMON',
    'RUNEN', 'EHRE', 'STEINE', 'GEHEN', 'SEHEN', 'NEHMEN',
    'GEBEN', 'LEBEN', 'STERBEN', 'WERDEN', 'HABEN', 'MACHEN',
    'SAGEN', 'FRAGEN', 'SUCHEN', 'TRAGEN', 'SCHLAGEN',
]
score_words = list(dict.fromkeys(score_words))

def score_text(text):
    total = 0
    for w in score_words:
        idx = 0
        while True:
            pos = text.find(w, idx)
            if pos == -1: break
            total += len(w)
            idx = pos + 1
    return total

baseline_score = score_text(full_text)
print(f"  Baseline score: {baseline_score}")

improvements = []
for code in unconfirmed:
    original = mapping.get(code, '?')
    freq = code_freq.get(code, 0)
    if freq < 3: continue  # Skip very rare codes

    for new_letter in all_letters:
        if new_letter == original: continue
        test_map = dict(mapping)
        test_map[code] = new_letter
        test_text = ''.join(collapse(decode_str(s, test_map)) for s in corrected)
        test_score = score_text(test_text)
        if test_score > baseline_score:
            improvements.append((code, original, new_letter, freq, test_score - baseline_score))

improvements.sort(key=lambda x: -x[4])
if improvements:
    print(f"\n  Improvements found ({len(improvements)}):")
    for code, orig, new, freq, gain in improvements[:15]:
        print(f"    Code {code}: {orig}->{new} ({freq}x): +{gain}")
else:
    print("  No improvements found")

# 6. Try PAIR reassignments of top unconfirmed codes
print("\n6. TOP PAIR REASSIGNMENTS")
print("-" * 60)

# Try pairs of unconfirmed codes (only high-frequency ones)
high_freq_unconf = [c for c in unconfirmed if code_freq.get(c, 0) >= 10]
print(f"  High-frequency unconfirmed: {high_freq_unconf}")

pair_improvements = []
for i in range(len(high_freq_unconf)):
    for j in range(i+1, len(high_freq_unconf)):
        c1 = high_freq_unconf[i]
        c2 = high_freq_unconf[j]
        o1 = mapping.get(c1, '?')
        o2 = mapping.get(c2, '?')

        # Try swapping their letters
        test_map = dict(mapping)
        test_map[c1] = o2
        test_map[c2] = o1
        test_text = ''.join(collapse(decode_str(s, test_map)) for s in corrected)
        test_score = score_text(test_text)
        if test_score > baseline_score + 3:
            pair_improvements.append((c1, c2, o1, o2, test_score - baseline_score))

pair_improvements.sort(key=lambda x: -x[4])
if pair_improvements:
    print(f"\n  Pair swap improvements:")
    for c1, c2, o1, o2, gain in pair_improvements[:10]:
        print(f"    Swap {c1}({o1}) <-> {c2}({o2}): +{gain}")
else:
    print("  No pair swap improvements > 3")

# 7. Context analysis of proper nouns
print("\n7. NARRATIVE CONTEXT ANALYSIS")
print("-" * 60)

# Read the full narrative more carefully with manual word boundaries
text = super_collapsed
print(f"\n  Manual reading of the narrative ({len(text)} chars):\n")

# Try to identify word boundaries by looking for known words and
# splitting the remaining text
segments = []
pos = 0
while pos < len(text):
    best_word = None
    best_len = 0
    for w in sorted(score_words, key=len, reverse=True):
        if text[pos:pos+len(w)] == w and len(w) > best_len:
            best_word = w
            best_len = len(w)
    if best_word:
        segments.append(('W', best_word))
        pos += best_len
    else:
        # Accumulate unknown chars
        if segments and segments[-1][0] == '?':
            segments[-1] = ('?', segments[-1][1] + text[pos])
        else:
            segments.append(('?', text[pos]))
        pos += 1

# Print with word boundaries
line = ''
for stype, stext in segments:
    if stype == 'W':
        token = stext
    else:
        token = f'[{stext}]'
    if len(line) + len(token) + 1 > 75:
        print(f"    {line}")
        line = token + ' '
    else:
        line += token + ' '
if line.strip():
    print(f"    {line}")

# 8. Summary of all proper nouns with their raw code patterns
print("\n8. PROPER NOUN RAW CODE PATTERNS")
print("-" * 60)

# Reverse mapping: letter -> list of codes
rev_map = defaultdict(list)
for code, letter in mapping.items():
    rev_map[letter].append(code)

for noun in nouns:
    noun_codes, pos = find_codes_for_text(noun, super_collapsed, super_decoded, super_codes)
    if not noun_codes: continue

    # Show the code pattern
    pattern = []
    for c in noun_codes:
        letter = mapping.get(c, '?')
        alternatives = rev_map[letter]
        # Is this the most common code for this letter?
        alt_freqs = [(ac, code_freq.get(ac, 0)) for ac in alternatives]
        alt_freqs.sort(key=lambda x: -x[1])
        most_common = alt_freqs[0][0] if alt_freqs else c
        marker = '*' if c != most_common else ''
        pattern.append(f"{c}{marker}")

    print(f"\n  {noun}:")
    print(f"    Codes: {' '.join(pattern)}")
    print(f"    (* = not the most common code for this letter)")

print("\n" + "=" * 80)
print("SESSION 12j COMPLETE")
print("=" * 80)
