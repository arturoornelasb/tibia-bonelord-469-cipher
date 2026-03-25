#!/usr/bin/env python3
"""Session 10f: Full narrative assembly and deep reading"""

import json, re
from collections import Counter, defaultdict

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]
books = [parse_codes(b) for b in raw_books]

def decode(book):
    return ''.join(mapping.get(c, '?') for c in book)

def collapse(s):
    return re.sub(r'(.)\1+', r'\1', s)

print("=" * 80)
print("SESSION 10f: FULL NARRATIVE ASSEMBLY")
print("=" * 80)

# 1. Decode all books and find longest unique pieces
all_decoded = [(i, decode(b)) for i, b in enumerate(books)]
all_collapsed = [(i, collapse(d)) for i, d in all_decoded]

# Remove exact duplicates
unique = {}
for i, text in all_collapsed:
    if text not in unique.values():
        unique[i] = text

# Remove substrings (keep only maximal pieces)
maximal = {}
for i, text in unique.items():
    is_sub = False
    for j, other in unique.items():
        if i != j and text in other:
            is_sub = True
            break
    if not is_sub:
        maximal[i] = text

print(f"\n  Total books: {len(books)}")
print(f"  Unique content: {len(unique)}")
print(f"  Maximal (non-substring): {len(maximal)}")

# 2. Greedy superstring assembly
print("\n" + "=" * 60)
print("2. SUPERSTRING ASSEMBLY")
print("=" * 60)

pieces = list(maximal.values())

def find_overlap(a, b, min_overlap=5):
    """Find max overlap where end of a matches start of b"""
    max_ov = min(len(a), len(b))
    for ov in range(max_ov, min_overlap-1, -1):
        if a[-ov:] == b[:ov]:
            return ov
    return 0

# Greedy merge: find pair with largest overlap, merge, repeat
iteration = 0
while len(pieces) > 1:
    best_ov = 0
    best_i, best_j = -1, -1
    best_merged = ""

    for i in range(len(pieces)):
        for j in range(len(pieces)):
            if i == j:
                continue
            ov = find_overlap(pieces[i], pieces[j])
            if ov > best_ov:
                best_ov = ov
                best_i, best_j = i, j
                best_merged = pieces[i] + pieces[j][ov:]

    if best_ov < 5:
        break

    # Remove j first (higher index), then i
    new_pieces = []
    for k in range(len(pieces)):
        if k != best_i and k != best_j:
            new_pieces.append(pieces[k])
    new_pieces.append(best_merged)
    pieces = new_pieces
    iteration += 1

print(f"\n  Assembly iterations: {iteration}")
print(f"  Remaining pieces: {len(pieces)}")

# Sort by length
pieces.sort(key=len, reverse=True)

# 3. Show assembled narrative with word boundaries
print("\n" + "=" * 60)
print("3. ASSEMBLED NARRATIVE")
print("=" * 60)

# Comprehensive German word list for segmentation
german_words = [
    # Long words first
    'AUNRSONGETRASES', 'UNENITGHNE', 'KOENIG', 'LABGZERAS',
    'EILCHANHEARUCHTIG', 'EDETOTNIURGS',
    'DNRHAUNRNVMHISDIZA',
    'MIHIETUNCISN', 'TIUMENGEMI',
    'SCHWITEIONE', 'EUGENDRTHENAEDEULGHLWUOEHSG',
    'WRLGTNELNRHELUIRUNN',
    # MHG / archaic
    'UTRUNR', 'GEIGET', 'KELSEI', 'SCHAUN', 'SEIDE',
    'URALTE', 'WISSET',
    # Standard German
    'NORDEN', 'SONNE', 'UNTER', 'NICHT', 'WERDE', 'STEIN',
    'DENEN', 'ERDE', 'VIEL', 'RUNE', 'STEH', 'LIED',
    'SEGEN', 'DORT', 'DENN', 'GOLD', 'MOND', 'WELT',
    'ENDE', 'REDE', 'HUND', 'SEIN', 'WIRD', 'ODER',
    'GEHT', 'TAG', 'WEG', 'DER', 'DEN', 'DIE', 'DAS',
    'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON', 'MIT',
    'WIE', 'SEI', 'AUS', 'ORT', 'TUN', 'NUR',
    'ER', 'ES', 'IN', 'SO',
]

for pi, piece in enumerate(pieces):
    print(f"\n  --- Piece {pi+1} ({len(piece)} chars) ---")

    # Try to insert word boundaries using known words
    # Simple greedy left-to-right matching
    pos = 0
    words = []
    while pos < len(piece):
        matched = False
        # Try longest match first
        for word in sorted(german_words, key=len, reverse=True):
            if piece[pos:pos+len(word)] == word:
                words.append(word)
                pos += len(word)
                matched = True
                break
        if not matched:
            # Collect unknown characters
            unknown_start = pos
            while pos < len(piece):
                found = False
                for word in german_words:
                    if piece[pos:pos+len(word)] == word:
                        found = True
                        break
                if found:
                    break
                pos += 1
            words.append(f"[{piece[unknown_start:pos]}]")

    # Print with word boundaries
    line = ' '.join(words)
    for i in range(0, len(line), 75):
        print(f"    {line[i:i+75]}")

# 4. Focused narrative interpretation
print("\n" + "=" * 60)
print("4. NARRATIVE INTERPRETATION")
print("=" * 60)

# Key phrases found
phrases = {
    'DIE URALTE STEIN': 'the ancient stone',
    'KOENIG LABGZERAS': 'King Labgzeras',
    'DENEN DER REDE': 'of those of the speech/proclamation',
    'ER GEIGET ES': 'he plays/shows it',
    'ENDE UTRUNR': 'end of utterance',
    'RUNE': 'rune(s)',
    'ORT': 'place',
    'WIR': 'we',
    'SEIN': 'his/to be',
    'IST': 'is',
    'VIEL': 'much/many',
    'SEI GEVMT WIE': 'be GE-VMT as',
    'TUN DIE': 'do the',
    'ER SO DAS': 'he so that',
    'IN DEN': 'in the',
}

print("\n  Confirmed phrases and meanings:")
for phrase, meaning in phrases.items():
    print(f"    {phrase:30s} = {meaning}")

# 5. What is ADTHARSC?
print("\n" + "=" * 60)
print("5. ADTHARSC / ADTHAUMR ANALYSIS")
print("=" * 60)

for i, text in all_collapsed:
    for pattern in ['ADTHAR', 'ADTHAU']:
        if pattern in text:
            pos = text.index(pattern)
            start = max(0, pos-10)
            end = min(len(text), pos+25)
            ctx = text[start:end]
            print(f"  B{i:02d}: ...{ctx}...")

# 6. SCHAUN analysis (MHG schauen = to look)
print("\n" + "=" * 60)
print("6. SCHAUN/SCHAUNR CONTEXT")
print("=" * 60)

for i, text in all_collapsed:
    if 'SCHAUN' in text:
        pos = text.index('SCHAUN')
        start = max(0, pos-15)
        end = min(len(text), pos+20)
        ctx = text[start:end]
        print(f"  B{i:02d}: ...{ctx}...")

# 7. Code 20 (F?) deeper analysis
print("\n" + "=" * 60)
print("7. CODE 20 (assigned=F) DEEP ANALYSIS")
print("=" * 60)

print(f"  Occurrences: 16")
contexts_20 = []
for bi, book in enumerate(books):
    decoded_raw = decode(book)
    col = collapse(decoded_raw)
    for ci, c in enumerate(book):
        if c == '20':
            start = max(0, ci-5)
            end = min(len(book), ci+6)
            ctx_raw = ''.join(mapping.get(book[x], '?') for x in range(start, end))
            pos_in = ci - start
            before = ctx_raw[:pos_in]
            after = ctx_raw[pos_in+1:]
            contexts_20.append((bi, before, after))
            print(f"  B{bi:02d}: {before}[F]{after}")

# Test: what if code 20 = P?
print("\n  If code 20 = P:")
for bi, before, after in contexts_20:
    full = before + 'P' + after
    print(f"  B{bi:02d}: {full}")

# Test: what if code 20 = J?
print("\n  If code 20 = J:")
for bi, before, after in contexts_20:
    full = before + 'J' + after
    print(f"  B{bi:02d}: {full}")

# 8. GALRN analysis (appears in Book 7)
print("\n" + "=" * 60)
print("8. PROPER NOUN CANDIDATES")
print("=" * 60)

# Look for words that appear capitalized / after articles
proper_candidates = ['GALRN', 'LABRNI', 'LABRRNI', 'TAUTR', 'HEDEMI',
                     'AMNEUD', 'ODEGAREN', 'WISETEIS', 'TUNR',
                     'VEUMS', 'RSIC', 'CUIT', 'RLAUNR']

for name in proper_candidates:
    count = sum(1 for _, text in all_collapsed if name in text)
    if count > 0:
        # Show one context
        for i, text in all_collapsed:
            if name in text:
                pos = text.index(name)
                start = max(0, pos-12)
                end = min(len(text), pos+len(name)+12)
                ctx = text[start:end]
                print(f"  {name:18s} ({count}x): ...{ctx}...")
                break

# 9. The GE- prefix pattern (past participles)
print("\n" + "=" * 60)
print("9. GE- PREFIX PATTERNS (past participles)")
print("=" * 60)

for i, text in all_collapsed:
    for m in re.finditer(r'GE[A-Z]{2,8}', text):
        word = m.group()
        if word not in ['GEIGET', 'GENDEN', 'GEGEN']:
            pos = m.start()
            start = max(0, pos-8)
            end = min(len(text), pos+len(word)+8)
            ctx = text[start:end]
            print(f"  B{i:02d}: {word:15s} in ...{ctx}...")

# 10. ER + verb patterns (he + verb)
print("\n" + "=" * 60)
print("10. 'ER [verb]' PATTERNS")
print("=" * 60)

for i, text in all_collapsed:
    for m in re.finditer(r'ER[A-Z]{2,10}', text):
        after_er = m.group()[2:]
        if after_er in ['DEN', 'DE', 'GEIGET']:
            continue
        pos = m.start()
        start = max(0, pos-5)
        end = min(len(text), pos+len(m.group())+5)
        ctx = text[start:end]
        # Only show first 2 per book
        print(f"  B{i:02d}: ER + {after_er:12s} in ...{ctx}...")
        break

# 11. The IST + [word] pattern (is + adjective/noun)
print("\n" + "=" * 60)
print("11. 'IST [word]' PATTERNS")
print("=" * 60)

seen_ist = set()
for i, text in all_collapsed:
    for m in re.finditer(r'IST([A-Z]{2,15})', text):
        after = m.group(1)
        if after not in seen_ist:
            seen_ist.add(after)
            pos = m.start()
            start = max(0, pos-5)
            end = min(len(text), m.end()+5)
            ctx = text[start:end]
            print(f"  B{i:02d}: IST + {after:18s} in ...{ctx}...")

# 12. Tibia lore cross-reference
print("\n" + "=" * 60)
print("12. TIBIA LORE CROSS-REFERENCE")
print("=" * 60)

tibia_terms = {
    'STEIN': 'stone - many magical stones in Tibia',
    'RUNE': 'rune - magic runes are core Tibia items',
    'KOENIG': 'king - various Tibia kings and kingdoms',
    'GOLD': 'gold - currency and valuable in Tibia',
    'ERDE': 'earth - one of 4 elements in Tibia',
    'SONNE': 'sun - appears in Tibia cosmology',
    'MOND': 'moon - appears in Tibia cosmology',
    'NORDEN': 'north - directional, Tibia geography',
    'HUND': 'hound/dog - creatures in Tibia',
    'SEIDE': 'silk - crafting material in Tibia',
    'STEH': 'stand - bonelords "stand" in Hellgate',
    'URALTE': 'ancient - "uralte" artifacts in Tibia',
    'LIED': 'song - various songs/poems in Tibia lore',
    'WELT': 'world - Tibia is set in the world of Tibia',
    'SEGEN': 'blessing - priestly/divine concept',
    'DORT': 'there - location reference',
}

print("\n  Tibia-relevant vocabulary found:")
for word, note in sorted(tibia_terms.items()):
    count = sum(text.count(word) for _, text in all_collapsed)
    print(f"    {word:12s} ({count:2d}x): {note}")

# Potential Tibia proper nouns
print("\n  Potential Tibia proper nouns:")
print("    LABGZERAS    : King name (in cipher)")
print("    AUNRSONGETRASES: title/epithet of the king?")
print("    HELLGATE     : Location where bonelord books are found")
print("    BONELORD     : Creatures that 'wrote' these texts")

print("\n" + "=" * 80)
print("SESSION 10f COMPLETE")
print("=" * 80)
