#!/usr/bin/env python3
"""Session 10z: Smart word boundary detection + expanded MHG vocabulary + Tibia lore"""

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

rev_map = defaultdict(list)
for code, letter in mapping.items():
    rev_map[letter].append(code)

print("=" * 80)
print("SESSION 10z: WORD BOUNDARIES + EXPANDED MHG + TIBIA LORE")
print("=" * 80)

# 1. Detect cross-code doubles (word boundaries hidden by collapse)
print("\n1. CROSS-CODE DOUBLES (WORD BOUNDARY MARKERS)")
print("-" * 60)

# When two DIFFERENT codes for the SAME letter appear consecutively,
# collapse hides the boundary. Find these cases.
cross_doubles = Counter()
boundary_contexts = defaultdict(list)

for bi, book in enumerate(books):
    decoded_raw = decode(book)
    for ci in range(len(book) - 1):
        code1 = book[ci]
        code2 = book[ci + 1]
        letter1 = mapping.get(code1, '?')
        letter2 = mapping.get(code2, '?')
        if letter1 == letter2 and code1 != code2:
            # Cross-code double! This is likely a word boundary
            cross_doubles[(letter1, code1, code2)] += 1
            # Context: get surrounding collapsed text
            start = max(0, ci - 5)
            end = min(len(book), ci + 7)
            ctx_decoded = decode(book[start:end])
            ctx_collapsed = collapse(ctx_decoded)
            # Mark boundary position
            before = collapse(decode(book[start:ci+1]))
            after = collapse(decode(book[ci+1:end]))
            boundary_contexts[(letter1, code1, code2)].append(
                (bi, f"...{before}|{after}...")
            )

print(f"  Total cross-code double types: {len(cross_doubles)}")
print(f"\n  Cross-code doubles by letter:")
by_letter = defaultdict(list)
for (letter, c1, c2), count in cross_doubles.most_common():
    by_letter[letter].append((c1, c2, count))
for letter in sorted(by_letter.keys()):
    pairs = by_letter[letter]
    total = sum(c for _, _, c in pairs)
    print(f"    {letter}: {total} total boundaries ({len(pairs)} code pairs)")
    for c1, c2, count in pairs[:3]:
        ctxs = boundary_contexts[(letter, c1, c2)][:2]
        ctx_str = ', '.join(ctx for _, ctx in ctxs)
        print(f"      {c1}+{c2} x{count}: {ctx_str}")

# 2. Smart decode that preserves cross-code boundaries
print("\n\n2. SMART DECODE WITH BOUNDARY MARKERS")
print("-" * 60)

def smart_decode(book):
    """Decode with | markers where cross-code doubles create hidden boundaries"""
    result = []
    for ci in range(len(book)):
        letter = mapping.get(book[ci], '?')
        if ci > 0:
            prev_letter = mapping.get(book[ci-1], '?')
            if letter == prev_letter:
                if book[ci] != book[ci-1]:
                    # Different code, same letter = likely word boundary
                    result.append('|')
                    result.append(letter)
                else:
                    # Same code, same letter = just a doubled letter (collapse it)
                    pass
            else:
                result.append(letter)
        else:
            result.append(letter)
    return ''.join(result)

# Show a few examples
for bi in [5, 9, 69, 0, 47]:
    smart = smart_decode(books[bi])
    normal = collapse(decode(books[bi]))
    print(f"\n  B{bi:02d} normal:  {normal[:80]}")
    print(f"  B{bi:02d} smart:   {smart[:80]}")
    # Count boundaries added
    boundaries = smart.count('|')
    print(f"  B{bi:02d} hidden boundaries: {boundaries}")

# 3. Expanded MHG word list analysis
print("\n\n3. EXPANDED VOCABULARY SEARCH")
print("-" * 60)

# All texts for pattern mining
all_collapsed = [collapse(decode(b)) for b in books]

# Combine into mega-text for substring search
mega = ''.join(all_collapsed)

# Search for common MHG words in the mega text
mhg_candidates = [
    # Common MHG function words
    'DU', 'WAN', 'MUOZ', 'SAH', 'LIEZ', 'SPRACH', 'DOCH',
    'WART', 'WOHL', 'SOLCH', 'SELB', 'DISE', 'WELCH',
    'GROZ', 'GUT', 'HAT', 'WAS', 'BIS', 'UBER', 'MAN',
    'MAG', 'LANT', 'HERR', 'WORT', 'STAT',
    # Possible Tibia names
    'BROG', 'CRUNOR', 'FERUMBRAS', 'ZATHROTH', 'UMAN',
    'FARDOS', 'TIBIANUS', 'BANOR', 'KIROK', 'UTHUN',
    'URTHUN', 'SUON', 'NOODLES',
    # More OHG/MHG
    'SINE', 'MINE', 'DINE', 'ANDER', 'BEID', 'JENER',
    'BEGAN', 'WAGEN', 'TRAGEN', 'SAGEN', 'KLAGEN',
    'GEBEN', 'LESEN', 'SEHEN', 'RUFEN', 'HEILEN',
    # Endings
    'HEIT', 'KEIT', 'SCHAFT', 'LICH', 'UNGE',
    # Prepositions
    'GEGEN', 'ZWISCHEN', 'NEBEN', 'HINTER',
]

print("  MHG candidates found in corpus:")
for word in mhg_candidates:
    count = 0
    for text in all_collapsed:
        count += text.count(word)
    if count > 0:
        # Show context
        for text in all_collapsed:
            idx = text.find(word)
            if idx >= 0:
                ctx = text[max(0,idx-6):idx+len(word)+6]
                print(f"    {word} x{count}: ...{ctx}...")
                break

# 4. Analyze the low-coverage unknown regions
print("\n\n4. LOW-COVERAGE REGIONS ANALYSIS")
print("-" * 60)

NEG_INF = float('-inf')
german_words = [
    'EILCHANHEARUCHTIG', 'EDETOTNIURGS', 'WRLGTNELNRHELUIRUNN',
    'TIUMENGEMI', 'SCHWITEIONE', 'LABGZERAS', 'HEDEMI', 'TAUTR',
    'LABRNI', 'ADTHARSC', 'ENGCHD', 'KELSEI',
    'KOENIG', 'GEIGET', 'SCHAUN', 'URALTE', 'FINDEN', 'DIESER',
    'NORDEN', 'SONNE', 'UNTER', 'NICHT', 'WERDE',
    'STEINEN', 'STEIN', 'DENEN', 'ERDE', 'VIEL', 'RUNE',
    'STEH', 'LIED', 'SEGEN', 'DORT', 'DENN',
    'GOLD', 'MOND', 'WELT', 'ENDE', 'REDE',
    'HUND', 'SEIN', 'WIRD', 'KLAR', 'ERST',
    'HWND', 'WISET', 'OWI', 'MINHE',
    'EINEN', 'EINER', 'SEINE', 'SEIDE',
    # New additions from search
    'GROZ', 'GUT', 'HAT', 'WAS', 'MAN', 'STAT',
    'SOLCH', 'SELB', 'DOCH', 'WOHL',
    'TAG', 'WEG', 'DER', 'DEN', 'DIE', 'DAS',
    'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON',
    'MIT', 'WIE', 'SEI', 'AUS', 'ORT', 'TUN',
    'NUR', 'SUN', 'TOT', 'GAR', 'ACH', 'ZUM',
    'HIN', 'HER', 'ALS', 'AUCH', 'RUND', 'GEH',
    'NACH', 'IENE', 'NOCH', 'ALLE', 'WOHL',
    'HIER', 'SICH', 'SIND', 'SEHR',
    'ABER', 'ODER', 'WENN', 'DANN',
    'ALTE', 'EDEL', 'HELD', 'LAND',
    'WARD', 'WART',
    'ER', 'ES', 'IN', 'SO', 'AN', 'IM',
    'DA', 'NU', 'IR', 'EZ', 'DO', 'OB', 'IE',
    'TER', 'HIET', 'NGETRAS', 'GEVMT', 'DGEDA',
    'TEMDIA', 'UISEMIV', 'TEIGN', 'CHN', 'SCE',
]

german_words = list(dict.fromkeys(german_words))
word_scores = {w: len(w) * 3 for w in german_words}
all_words = sorted(word_scores.keys(), key=len, reverse=True)

def dp_segment_full(text):
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
        for word in all_words:
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

# Extract all unknown sequences with context
print("  Collecting consecutive unknown regions...")
unknown_regions = Counter()
for bi in range(len(all_collapsed)):
    text = all_collapsed[bi]
    parts, _, _ = dp_segment_full(text)
    # Find consecutive unknowns
    i = 0
    while i < len(parts):
        if parts[i][0] == '?':
            # Collect consecutive unknowns
            unk_str = ''
            j = i
            while j < len(parts) and parts[j][0] == '?':
                unk_str += parts[j][1]
                j += 1
            if len(unk_str) >= 3:
                # Get surrounding context
                before_word = ''
                if i > 0 and parts[i-1][0] == 'W':
                    before_word = parts[i-1][1]
                after_word = ''
                if j < len(parts) and parts[j][0] == 'W':
                    after_word = parts[j][1]
                key = f"{before_word}...[{unk_str}]...{after_word}"
                unknown_regions[key] += 1
            i = j
        else:
            i += 1

print(f"  Unique unknown regions (>= 3 chars): {len(unknown_regions)}")
print(f"\n  Most common unknown regions:")
for region, count in unknown_regions.most_common(25):
    print(f"    x{count}: {region}")

# 5. Study the N-gram patterns in unknown regions
print("\n\n5. UNKNOWN REGION N-GRAMS")
print("-" * 60)

# Collect ALL unknown text
all_unk_text = ''
for bi in range(len(all_collapsed)):
    text = all_collapsed[bi]
    parts, _, _ = dp_segment_full(text)
    for ptype, ptext in parts:
        if ptype == '?':
            all_unk_text += ptext

unk_bigrams = Counter()
unk_trigrams = Counter()
for i in range(len(all_unk_text) - 1):
    unk_bigrams[all_unk_text[i:i+2]] += 1
for i in range(len(all_unk_text) - 2):
    unk_trigrams[all_unk_text[i:i+3]] += 1

print(f"  Total unknown chars: {len(all_unk_text)}")
print(f"\n  Top bigrams in unknown text:")
for bg, c in unk_bigrams.most_common(15):
    print(f"    {bg} x{c}")
print(f"\n  Top trigrams in unknown text:")
for tg, c in unk_trigrams.most_common(15):
    print(f"    {tg} x{c}")

# 6. Look at the SMART decode for boundary insights
print("\n\n6. SMART DECODE WORD RECOVERY")
print("-" * 60)

# Use smart decode to find words that span boundaries
smart_texts = [smart_decode(b) for b in books]

# Some words that might be hidden by collapsed doubles:
# If we have ...D|D... this could be end_D + start_D
# Like "UND DER" collapsing to "UNDER" - wait no, the boundary would show

# Check: does smart decode reveal new words?
for bi in range(len(books)):
    smart = smart_texts[bi]
    # Remove | markers to get searchable text
    clean = smart.replace('|', '')
    normal = all_collapsed[bi]
    if clean != normal:
        # Smart decode has different text! The | markers split what collapse merged
        diffs = []
        for i in range(min(len(clean), len(normal))):
            if i < len(clean) and i < len(normal) and clean[i] != normal[i]:
                diffs.append(i)
        if diffs:
            print(f"  B{bi:02d} DIFFERS from collapsed: {len(diffs)} positions")

# Actually, clean should equal normal. The | just marks boundaries.
# Let me re-approach: find words that SPAN a | boundary
print("\n  Words found by splitting at boundaries:")
new_words_found = Counter()
for bi in range(len(books)):
    smart = smart_texts[bi]
    # Split at | to get segments
    segments = smart.split('|')
    # Try joining adjacent segments
    for i in range(len(segments) - 1):
        combined = segments[i] + segments[i+1]
        # Does this contain a known word that isn't in the normal segmentation?
        for word in all_words:
            if word in combined:
                # But is it in the original collapsed text?
                normal = all_collapsed[bi]
                if word not in normal:
                    new_words_found[word] += 1
                    if new_words_found[word] <= 2:
                        print(f"    B{bi:02d}: {word} found in smart '{combined[:30]}' but NOT in normal!")

if not new_words_found:
    print("    No new words revealed by boundary analysis")

# 7. What are single-letter unknowns between known words?
print("\n\n7. SINGLE-LETTER UNKNOWNS IN CONTEXT")
print("-" * 60)

single_contexts = Counter()
for bi in range(len(all_collapsed)):
    text = all_collapsed[bi]
    parts, _, _ = dp_segment_full(text)
    for i in range(1, len(parts) - 1):
        if parts[i][0] == '?' and len(parts[i][1]) == 1:
            before = parts[i-1][1] if parts[i-1][0] == 'W' else f'[{parts[i-1][1]}]'
            after = parts[i+1][1] if parts[i+1][0] == 'W' else f'[{parts[i+1][1]}]'
            single_contexts[f"{before} [{parts[i][1]}] {after}"] += 1

print(f"  Unique single-letter-in-context patterns: {len(single_contexts)}")
print(f"\n  Most common:")
for ctx, count in single_contexts.most_common(20):
    print(f"    x{count}: {ctx}")

# 8. Tibia lore cross-reference
print("\n\n8. TIBIA LORE CROSS-REFERENCE")
print("-" * 60)

# Known Tibia elements that might match our proper nouns
tibia_entities = {
    'TAUTR': ['TAUTR is described as EILCHANHEARUCHTIG',
              'Could be related to Tibia god/hero'],
    'EILCHANHEARUCHTIG': ['17 chars, decomposed: EILCHAN-HEA-RUCHTIG',
                          '-RUCHTIG = MHG famous/renowned',
                          'EILCHAN could be proper noun element'],
    'EDETOTNIURGS': ['Belongs to TAUTR (SEIN = his)',
                     'Could be title, place, or attribute'],
    'HEDEMI': ['Place with URALTE STEINEN (ancient stones)',
               'Contains ADTHARSC'],
    'ADTHARSC': ['Associated with STEINEN TER (stones the)',
                 'Could be place or entity name'],
    'LABRNI': ['Appears after ER (he/it)',
               'Could be place name'],
    'ENGCHD': ['Near KELSEI and TIUMENGEMI',
               'Followed by ORT (place)'],
    'KELSEI': ['Near ENGCHD',
               'Contains EZ EL US ED = MHG words?'],
    'TIUMENGEMI': ['Contains MENGE (crowd/many)?',
                   'TIU = MHG "the" (fem)?'],
    'LABGZERAS': ['With KOENIG (king)',
                  'Name of a king or kingdom?'],
    'SCHWITEIONE': ['IST = is',
                    'Attribute or state?'],
}

for name, notes in tibia_entities.items():
    count = sum(1 for t in all_collapsed if name in t)
    print(f"\n  {name} (in {count} books):")
    for note in notes:
        print(f"    - {note}")
    # Show all contexts
    for bi, text in enumerate(all_collapsed):
        if name in text:
            idx = text.index(name)
            ctx = text[max(0,idx-10):idx+len(name)+10]
            print(f"    B{bi:02d}: ...{ctx}...")
            if bi > 3 and count > 5:
                print(f"    ... and {count - 4} more")
                break

# 9. The recurring phrase: SEI GEVMT WIE TUN R TAG R SIC
print("\n\n9. THE RECURRING FORMULA")
print("-" * 60)

formula = 'SEIGEVMTWIETUN'
formula_count = sum(1 for t in all_collapsed if formula in t)
print(f"  '{formula}...' appears in {formula_count} books")

# What follows after TAG?
print("\n  Full formula with everything after TAG:")
for bi, text in enumerate(all_collapsed):
    if formula in text:
        idx = text.index(formula)
        after = text[idx:]
        print(f"    B{bi:02d}: {after[:60]}")

# 10. Summary: readable narrative attempt
print("\n\n10. BEST NARRATIVE READING")
print("-" * 60)
print("  Using B05 (94.7% coverage) as anchor text:")
print()

text = all_collapsed[5]  # B05
parts, _, _ = dp_segment_full(text)
# Format with spaces between words, brackets for unknowns
formatted = ''
for ptype, ptext in parts:
    if ptype == 'W':
        formatted += ptext + ' '
    else:
        formatted += f'[{ptext}] '

# Print wrapped
for i in range(0, len(formatted), 70):
    print(f"    {formatted[i:i+70]}")

# Also attempt translation of known words
print("\n  Partial translation attempt:")
translations = {
    'HIER': 'here', 'TAUTR': '(name:Tautr)', 'IST': 'is',
    'EILCHANHEARUCHTIG': '(famous/renowned)',
    'ER': 'he', 'SO': 'so/thus', 'DAS': 'that', 'TUN': 'do',
    'DIESER': 'this', 'EINER': 'one/a', 'SEIN': 'his',
    'EDETOTNIURGS': '(name/title)',
    'LABRNI': '(name:Labrni)', 'WIR': 'we', 'UND': 'and',
    'IE': 'ever/the', 'IN': 'in', 'HEDEMI': '(place:Hedemi)',
    'DIE': 'the', 'URALTE': 'ancient', 'STEINEN': 'stones',
    'TER': 'the(MHG)', 'ADTHARSC': '(name:Adtharsc)',
    'SCHAUN': 'look/see', 'WISET': 'know(ye)',
    'TIUMENGEMI': '(name/word)', 'ORT': 'place',
    'ENGCHD': '(name:Engchd)', 'KELSEI': '(name:Kelsei)',
    'DEN': 'the(acc)', 'RUNE': 'rune', 'UNTER': 'under',
    'AUS': 'out/from', 'HIET': 'called(past)',
    'ENDE': 'end', 'SCHWITEIONE': '(word/name)',
    'WIRD': 'becomes', 'SEI': 'be(imp)', 'GEVMT': '(word)',
    'WIE': 'as/how', 'TAG': 'day', 'SICH': 'self',
    'MINHE': '(word:love?)', 'AUCH': 'also',
}

translated = ''
for ptype, ptext in parts:
    if ptype == 'W':
        tr = translations.get(ptext, ptext.lower())
        translated += tr + ' '
    else:
        translated += f'[{ptext}] '

for i in range(0, len(translated), 70):
    print(f"    {translated[i:i+70]}")

print("\n" + "=" * 80)
print("SESSION 10z COMPLETE")
print("=" * 80)
