#!/usr/bin/env python3
"""Session 10j: DIESER discovery, re-segmentation, new word integration"""

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
    return re.sub(r'(.)\\1+', r'\\1', s)

all_col = [(i, collapse(decode(b))) for i, b in enumerate(books)]

print("=" * 80)
print("SESSION 10j: DIESER DISCOVERY & RE-SEGMENTATION")
print("=" * 80)

# 1. DIESER code-level verification
print("\n1. DIESER CODE-LEVEL VERIFICATION")
print("-" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'DIESER' in col:
        pos = col.index('DIESER')
        # Find raw position
        decoded = decode(book)
        for ri in range(len(decoded)):
            if collapse(decoded[ri:ri+12]).startswith('DIESER'):
                codes = book[ri:ri+6]
                letters = [mapping.get(c, '?') for c in codes]
                ctx_start = max(0, pos-10)
                ctx_end = min(len(col), pos+16)
                ctx = col[ctx_start:ctx_end]
                print(f"  B{bi:02d}: {'-'.join(codes)} = {''.join(letters)} in ...{ctx}...")
                break
        if bi > 30:
            break

# 2. DIESER vs DIE-S-ER: which segmentation is correct?
print("\n" + "=" * 60)
print("2. DIESER CONTEXT ANALYSIS")
print("=" * 60)

for bi, col in all_col:
    if 'DIESER' in col:
        pos = col.index('DIESER')
        start = max(0, pos-20)
        end = min(len(col), pos+30)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")
        if bi > 35:
            break

# Check what comes after DIESER
print("\n  What follows DIESER:")
after_dieser = Counter()
for bi, col in all_col:
    for m in re.finditer('DIESER', col):
        after = col[m.end():m.end()+15]
        after_dieser[after[:8]] += 1
        print(f"    B{bi:02d}: DIESER + '{after[:15]}'")
        break

# 3. SICH analysis
print("\n" + "=" * 60)
print("3. SICH (reflexive pronoun) ANALYSIS")
print("=" * 60)

for bi, col in all_col:
    if 'SICH' in col:
        pos = col.index('SICH')
        start = max(0, pos-15)
        end = min(len(col), pos+20)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# 4. ERST (first) analysis
print("\n" + "=" * 60)
print("4. ERST (first) ANALYSIS")
print("=" * 60)

for bi, col in all_col:
    if 'ERST' in col:
        pos = col.index('ERST')
        start = max(0, pos-15)
        end = min(len(col), pos+20)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# 5. AUCH analysis
print("\n" + "=" * 60)
print("5. AUCH (also) ANALYSIS")
print("=" * 60)

for bi, col in all_col:
    if 'AUCH' in col:
        pos = col.index('AUCH')
        start = max(0, pos-15)
        end = min(len(col), pos+20)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# 6. ENT- prefix analysis
print("\n" + "=" * 60)
print("6. ENT- PREFIX ANALYSIS")
print("=" * 60)

for bi, col in all_col:
    for m in re.finditer(r'ENT[A-Z]', col):
        pos = m.start()
        start = max(0, pos-10)
        end = min(len(col), pos+20)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")
        break

# 7. SUN = OHG SUNNA analysis
print("\n" + "=" * 60)
print("7. SUN (OHG SUNNA = sun) ANALYSIS")
print("=" * 60)

sun_count = 0
for bi, col in all_col:
    # SUN but not SUNT, SUNG, etc - look for SUN followed by non-N
    for m in re.finditer(r'SUN(?!N)', col):
        pos = m.start()
        start = max(0, pos-10)
        end = min(len(col), pos+15)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")
        sun_count += 1
        if sun_count > 10:
            break
    if sun_count > 10:
        break

# Also check SONNE
print("\n  SONNE occurrences:")
for bi, col in all_col:
    if 'SONNE' in col:
        pos = col.index('SONNE')
        start = max(0, pos-10)
        end = min(len(col), pos+15)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# 8. RE-SEGMENTATION with expanded word list
print("\n" + "=" * 60)
print("8. RE-SEGMENTED NARRATIVE")
print("=" * 60)

# Expanded word list with new discoveries
expanded_words = [
    # Very long / proper
    'AUNRSONGETRASES', 'UNENITGHNE', 'EILCHANHEARUCHTIG',
    'EDETOTNIURGS', 'DNRHAUNRNVMHISDIZA',
    'EUGENDRTHENAEDEULGHLWUOEHSG', 'WRLGTNELNRHELUIRUNN',
    'MIHIETUNCISN', 'TIUMENGEMI', 'SCHWITEIONE',
    # NEW: demonstrative
    'DIESER', 'DIESE', 'DIESES',
    # Proper nouns
    'LABGZERAS', 'HEDEMI', 'TAUTR', 'LABRNI', 'ADTHARSC',
    'ADTHAUMR', 'ODEGAREN', 'RLAUNR', 'GALRN',
    # MHG / archaic / newly found
    'KOENIG', 'UTRUNR', 'GEIGET', 'KELSEI', 'SCHAUN',
    'URALTE', 'WISSET', 'FINDEN', 'SEIDE', 'HWND',
    'GEVMT', 'VMTEGE',
    # NEW: common German
    'DIESER', 'EINEN', 'EINER', 'SEINE', 'SICH',
    'NORDEN', 'SONNE', 'UNTER', 'NICHT', 'WERDE',
    'STEIN', 'DENEN', 'ERDE', 'VIEL', 'RUNE',
    'STEH', 'LIED', 'SEGEN', 'DORT', 'DENN',
    'GOLD', 'MOND', 'WELT', 'ENDE', 'REDE',
    'HUND', 'SEIN', 'WIRD', 'KLAR', 'ERST',
    'AUCH', 'RUND',
    # Standard short
    'TAG', 'WEG', 'DER', 'DEN', 'DIE', 'DAS',
    'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON',
    'MIT', 'WIE', 'SEI', 'AUS', 'ORT', 'TUN',
    'NUR', 'SUN', 'TOT', 'GAR', 'ACH', 'ZUM',
    'HIN', 'HER', 'DIR', 'ALS',
    'ER', 'ES', 'IN', 'SO', 'IM',
]
# Remove duplicates, keep longest first
expanded_words = sorted(set(expanded_words), key=len, reverse=True)

# Get longest unique piece
pieces = {}
for i, text in all_col:
    is_sub = False
    for j, other in all_col:
        if i != j and text in other:
            is_sub = True
            break
    if not is_sub:
        pieces[i] = text

by_len = sorted(pieces.items(), key=lambda x: len(x[1]), reverse=True)

# Segment top 3
for idx, (bi, text) in enumerate(by_len[:3]):
    print(f"\n  --- Book {bi} ({len(text)} chars) ---")
    pos = 0
    words = []
    while pos < len(text):
        matched = False
        for word in expanded_words:
            if text[pos:pos+len(word)] == word:
                words.append(word)
                pos += len(word)
                matched = True
                break
        if not matched:
            unk_start = pos
            while pos < len(text):
                found = False
                for word in expanded_words:
                    if text[pos:pos+len(word)] == word:
                        found = True
                        break
                if found:
                    break
                pos += 1
            words.append(f"[{text[unk_start:pos]}]")

    line = ' '.join(words)
    for i in range(0, len(line), 78):
        print(f"    {line[i:i+78]}")

# 9. Focus: what is "T" between DIESER and EINER?
print("\n" + "=" * 60)
print("9. THE 'T' BETWEEN DIESER AND EINER")
print("=" * 60)

# Look at code-level for DIESERTEINER
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'DIESERTEINER' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if collapse(decoded[ri:ri+20]).startswith('DIESERTEINER'):
                # Show codes for DIESERTEINER
                codes = book[ri:ri+12]
                letters = [mapping.get(c, '?') for c in codes]
                print(f"  B{bi:02d}: codes {'-'.join(codes)}")
                print(f"         letters {''.join(letters)}")
                # The T could be doubled in raw
                print(f"         raw: {decoded[ri:ri+20]}")
                break
        break

# 10. What is after EINER SEIN?
print("\n" + "=" * 60)
print("10. 'EINER SEIN' -> EDETOTNIURGS ANALYSIS")
print("=" * 60)

# EDETOTNIURGS contains TOT (dead)
# Could be: EDE + TOT + NIURGS
# Or: EDET + OT + NIURGS
# MHG EDEL = noble, EDELING = nobleman
# EDETOT could be "noble dead" or "death of the noble"
# NIURGS - could contain NIURG = ?
# What about: E-DE-TOT-NI-URGS?
# Or EDET = ?
# URGS could be related to URGISCHT/URSPRUNG?

print("  EDETOTNIURGS hypotheses:")
print("    1. EDE-TOT-NIURGS  (EDE + dead + ?)")
print("    2. EDET-OT-NIURGS  (? + ? + ?)")
print("    3. EDEL-TOT-NIURGS (noble-dead-? but L->missing)")
print("    4. E-DE-TOT-NI-URGS (? the dead not ?)")
print()

# Check code-level for EDETOTNIURGS
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'EDETOTNIURGS' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if collapse(decoded[ri:ri+20]).startswith('EDETOT'):
                codes = book[ri:ri+12]
                letters = [mapping.get(c, '?') for c in codes]
                print(f"  B{bi:02d} raw codes: {' '.join(codes)}")
                print(f"  B{bi:02d} raw letters: {''.join(letters)}")
                print(f"  B{bi:02d} raw decoded: {decoded[ri:ri+20]}")
                break
        break

# 11. ADTHARSC - proper noun or compound?
print("\n" + "=" * 60)
print("11. ADTHARSC / ADTHAUMR DEEP ANALYSIS")
print("=" * 60)

for bi, col in all_col:
    if 'ADTHAR' in col or 'ADTHAU' in col:
        # Full context
        for pattern in ['ADTHAR', 'ADTHAU']:
            if pattern in col:
                pos = col.index(pattern)
                start = max(0, pos-20)
                end = min(len(col), pos+25)
                ctx = col[start:end]
                print(f"  B{bi:02d}: ...{ctx}...")

# Check if ADTHARSC and ADTHAUMR share prefix codes
print("\n  Code-level comparison:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    decoded = decode(book)
    for pattern in ['ADTHARSC', 'ADTHAUMR']:
        if pattern in col:
            for ri in range(len(decoded)):
                if collapse(decoded[ri:ri+15]).startswith(pattern):
                    codes = book[ri:ri+8]
                    letters = [mapping.get(c, '?') for c in codes]
                    print(f"    B{bi:02d} {pattern}: {' '.join(codes)} = {''.join(letters)}")
                    break
            break

# 12. Complete vocabulary count
print("\n" + "=" * 60)
print("12. COMPLETE VOCABULARY SUMMARY")
print("=" * 60)

# Categorize all known words
confirmed = {
    'Articles/Pronouns': ['DER', 'DEN', 'DIE', 'DAS', 'EIN', 'EINER',
                          'EINEN', 'ER', 'ES', 'SIE', 'WIR', 'DIESER',
                          'DIESE', 'SEIN', 'SEINE', 'DENEN', 'SICH'],
    'Verbs': ['IST', 'TUN', 'STEH', 'WIRD', 'WERDE', 'FINDEN', 'GEIGET',
              'SCHAUN', 'SEI'],
    'Nouns': ['RUNE', 'STEIN', 'ERDE', 'ORT', 'TAG', 'WEG', 'SONNE', 'SUN',
              'MOND', 'WELT', 'GOLD', 'SEIDE', 'LIED', 'SEGEN', 'HUND',
              'HWND', 'KOENIG', 'REDE', 'ENDE', 'NORDEN', 'TOT'],
    'Adjectives/Adverbs': ['URALTE', 'VIEL', 'KLAR', 'NICHT', 'NUR', 'DORT',
                           'DENN', 'SO', 'WIE', 'AUCH', 'ERST', 'GAR',
                           'HIN', 'HER', 'AUS', 'UNTER'],
    'Prepositions': ['IN', 'VON', 'MIT', 'ALS', 'ZUM'],
    'Conjunctions': ['UND'],
    'Proper nouns': ['LABGZERAS', 'HEDEMI', 'TAUTR', 'LABRNI',
                     'AUNRSONGETRASES', 'UNENITGHNE', 'ADTHARSC',
                     'ADTHAUMR', 'ODEGAREN', 'RLAUNR'],
    'MHG/archaic': ['UTRUNR', 'KELSEI', 'GEVMT', 'VMTEGE', 'WISSET'],
    'Unknown compounds': ['EILCHANHEARUCHTIG', 'EDETOTNIURGS',
                          'EUGENDRTHENAEDEULGHLWUOEHSG',
                          'DNRHAUNRNVMHISDIZA', 'MIHIETUNCISN',
                          'TIUMENGEMI', 'SCHWITEIONE',
                          'WRLGTNELNRHELUIRUNN'],
}

total = 0
for cat, words in confirmed.items():
    print(f"\n  {cat} ({len(words)}):")
    for w in sorted(words):
        count = sum(1 for _, text in all_col if w in text)
        print(f"    {w:20s} ({count:2d}x)")
        total += 1

print(f"\n  TOTAL VOCABULARY: {total} items")

# 13. Improved narrative reading
print("\n" + "=" * 60)
print("13. IMPROVED NARRATIVE READING")
print("=" * 60)

# Use the longest book for the full narrative
longest_bi, longest_text = by_len[0]

# Better translation attempt
translations = {
    'ER': 'he', 'TAUTR': '[TAUTR]', 'IST': 'is',
    'EILCHANHEARUCHTIG': '[EILCHANHEARUCHTIG=famous?]',
    'SO': 'so', 'DAS': 'that', 'TUN': 'do',
    'DIESER': 'this_one', 'EINER': 'one', 'SEIN': 'his',
    'EDETOTNIURGS': '[EDE-dead-NIURGS]', 'LABRNI': '[LABRNI]',
    'WIR': 'we', 'UND': 'and', 'IN': 'in', 'HEDEMI': '[HEDEMI]',
    'DIE': 'the', 'URALTE': 'ancient', 'STEIN': 'stone',
    'ADTHARSC': '[ADTHARSC]', 'SCHAUN': 'behold',
    'WISSET': 'know_ye', 'KELSEI': '[KELSEI]', 'DEN': 'the',
    'DNRHAUNRNVMHISDIZA': '[DNR-HAUN-RN-VM-HIS-DIZA]',
    'RUNE': 'rune', 'ORT': 'place', 'UNTER': 'under',
    'STEH': 'stand', 'WRLGTNELNRHELUIRUNN': '[WRLGT...]',
    'HWND': 'hound', 'FINDEN': 'find', 'GEIGET': 'shows',
    'ES': 'it', 'VIEL': 'much', 'KLAR': 'clear',
    'SONNE': 'sun', 'SUN': 'sun(OHG)', 'TAG': 'day',
    'GOLD': 'gold', 'MOND': 'moon', 'ERDE': 'earth',
    'SEI': 'be', 'GEVMT': 'formed', 'WIE': 'as/how',
    'ENDE': 'end', 'UTRUNR': 'utterance', 'DENEN': 'those',
    'DER': 'the', 'REDE': 'speech', 'KOENIG': 'king',
    'LABGZERAS': '[LABGZERAS]', 'UNENITGHNE': '[UNENITGHNE]',
    'AUNRSONGETRASES': '[AUNRSONGETRASES]',
    'MIT': 'with', 'VON': 'from', 'AUS': 'from/out',
    'NUR': 'only', 'NICHT': 'not', 'AUCH': 'also',
    'WERDE': 'become', 'WIRD': 'will', 'ERST': 'first',
    'SEIDE': 'silk', 'SEGEN': 'blessing', 'HUND': 'hound',
    'LIED': 'song', 'WELT': 'world', 'NORDEN': 'north',
    'DORT': 'there', 'WEG': 'way', 'EIN': 'a/one',
    'SIE': 'they/she', 'DENN': 'then', 'SICH': 'self',
}

# Segment and translate
pos = 0
segments = []
while pos < len(longest_text):
    matched = False
    for word in expanded_words:
        if longest_text[pos:pos+len(word)] == word:
            trans = translations.get(word, word)
            segments.append(f"{word}={trans}")
            pos += len(word)
            matched = True
            break
    if not matched:
        unk_start = pos
        while pos < len(longest_text):
            found = False
            for word in expanded_words:
                if longest_text[pos:pos+len(word)] == word:
                    found = True
                    break
            if found:
                break
            pos += 1
        segments.append(f"[{longest_text[unk_start:pos]}]")

# Print in readable chunks
line = ' | '.join(segments)
for i in range(0, len(line), 80):
    print(f"  {line[i:i+80]}")

print("\n" + "=" * 80)
print("SESSION 10j COMPLETE")
print("=" * 80)
