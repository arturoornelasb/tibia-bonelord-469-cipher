#!/usr/bin/env python3
"""Session 10h: KLAR confirmation, OEHSG/GETHK attack, sentence reading"""

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
print("SESSION 10h: KLAR CONFIRMATION & SENTENCE READING")
print("=" * 80)

# 1. KLAR (clear) - verify in context
print("\n1. KLAR VERIFICATION")
print("-" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'KLAR' in col:
        pos = col.index('KLAR')
        start = max(0, pos-15)
        end = min(len(col), pos+19)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# Check KLAR codes
print("\n  KLAR code analysis:")
for bi, book in enumerate(books):
    decoded = decode(book)
    col = collapse(decoded)
    if 'KLAR' in col:
        # Find raw position
        for ri in range(len(decoded)-3):
            if collapse(decoded[ri:ri+6]).startswith('KLAR'):
                codes = book[ri:ri+4]
                letters = [mapping.get(c, '?') for c in codes]
                print(f"    B{bi:02d}: {'-'.join(codes)} = {''.join(letters)}")
                break
        break

# 2. OEHSG pattern - what is this?
print("\n" + "=" * 60)
print("2. OEHSG ANALYSIS")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'OEHSG' in col:
        pos = col.index('OEHSG')
        start = max(0, pos-15)
        end = min(len(col), pos+20)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")
        break

# All OEHSG contexts
oehsg_contexts = set()
for bi, book in enumerate(books):
    col = collapse(decode(book))
    for m in re.finditer('OEHSG', col):
        pos = m.start()
        start = max(0, pos-10)
        end = min(len(col), pos+15)
        ctx = col[start:end]
        oehsg_contexts.add(ctx)

print(f"\n  {len(oehsg_contexts)} unique contexts:")
for ctx in sorted(oehsg_contexts)[:8]:
    print(f"    ...{ctx}...")

# OEHSG appears before "SEI GEVMT WIE TUN TAG"
# What comes before OEHSG?
print("\n  What precedes OEHSG:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'OEHSG' in col:
        pos = col.index('OEHSG')
        start = max(0, pos-25)
        ctx = col[start:pos+5]
        print(f"    B{bi:02d}: ...{ctx}")

# 3. GETHK analysis
print("\n" + "=" * 60)
print("3. GETHK ANALYSIS")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'GETHK' in col:
        pos = col.index('GETHK')
        start = max(0, pos-15)
        end = min(len(col), pos+20)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# 4. The TA ER pattern before OEHSG/GETHK
print("\n" + "=" * 60)
print("4. 'TA ER' PATTERN")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'TAER' in col:
        pos = col.index('TAER')
        start = max(0, pos-10)
        end = min(len(col), pos+25)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")
        if bi > 55:
            break

# 5. Deep reading: the longest assembled piece
print("\n" + "=" * 60)
print("5. MANUAL READING - LONGEST PIECE")
print("=" * 60)

# Get the longest unique collapsed text
all_col = [(i, collapse(decode(b))) for i, b in enumerate(books)]
# Find maximal pieces
maximal = {}
for i, text in all_col:
    is_sub = False
    for j, other in all_col:
        if i != j and text in other:
            is_sub = True
            break
    if not is_sub:
        maximal[i] = text

# Sort by length
by_len = sorted(maximal.items(), key=lambda x: len(x[1]), reverse=True)

# Take top 3
for idx, (bi, text) in enumerate(by_len[:3]):
    print(f"\n  --- Book {bi} ({len(text)} chars) ---")
    print(f"  Raw: {text}")

    # Manual word-by-word analysis
    known_words = {
        'AUNRSONGETRASES': 'title/epithet',
        'EILCHANHEARUCHTIG': 'adj?(all identical codes)',
        'EDETOTNIURGS': 'unknown compound',
        'EUGENDRTHENAEDEULGHLWUOEHSG': 'unknown long compound',
        'MIHIETUNCISN': 'unknown',
        'DNRHAUNRNVMHISDIZA': 'unknown(contains HAUN)',
        'SCHWITEIONE': 'unknown',
        'UNENITGHNE': 'unknown',
        'WRLGTNELNRHELUIRUNN': 'garbled core',
        'LABGZERAS': 'king name',
        'HEDEMI': 'place name',
        'KOENIG': 'king',
        'URALTE': 'ancient',
        'UTRUNR': 'utterance?',
        'KELSEI': 'MHG?',
        'GEIGET': 'plays/shows',
        'SCHAUN': 'behold(MHG)',
        'FINDEN': 'to find',
        'SEIDE': 'silk',
        'STEIN': 'stone',
        'NORDEN': 'north',
        'UNTER': 'under',
        'NICHT': 'not',
        'WERDE': 'become',
        'DENEN': 'to those',
        'ERDE': 'earth',
        'VIEL': 'much',
        'RUNE': 'rune',
        'STEH': 'stand',
        'LIED': 'song',
        'GOLD': 'gold',
        'MOND': 'moon',
        'WELT': 'world',
        'HUND': 'hound',
        'SEGEN': 'blessing',
        'DORT': 'there',
        'DENN': 'then',
        'ENDE': 'end',
        'REDE': 'speech',
        'SEIN': 'his/be',
        'WIRD': 'will',
        'KLAR': 'clear',
        'SONNE': 'sun',
        'TAG': 'day',
        'WEG': 'way',
        'DER': 'the(m)',
        'DEN': 'the(acc)',
        'DIE': 'the(f/pl)',
        'DAS': 'that/the(n)',
        'UND': 'and',
        'IST': 'is',
        'EIN': 'a/one',
        'SIE': 'they/she',
        'WIR': 'we',
        'VON': 'from',
        'MIT': 'with',
        'WIE': 'how/as',
        'SEI': 'be(subj)',
        'AUS': 'from/out',
        'ORT': 'place',
        'TUN': 'do',
        'NUR': 'only',
        'ER': 'he',
        'ES': 'it',
        'IN': 'in',
        'SO': 'so',
    }

    # Greedy match
    pos = 0
    reading = []
    while pos < len(text):
        matched = False
        for word in sorted(known_words.keys(), key=len, reverse=True):
            if text[pos:pos+len(word)] == word:
                reading.append(f"{word}({known_words[word]})")
                pos += len(word)
                matched = True
                break
        if not matched:
            unk_start = pos
            while pos < len(text):
                found = False
                for word in known_words:
                    if text[pos:pos+len(word)] == word:
                        found = True
                        break
                if found:
                    break
                pos += 1
            reading.append(f"[{text[unk_start:pos]}]")

    line = ' '.join(reading)
    for i in range(0, len(line), 80):
        print(f"  {line[i:i+80]}")

# 6. TAUTR - could this be TAUTR = TAUTER (more deaf/numb)?
print("\n" + "=" * 60)
print("6. TAUTR ANALYSIS")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'TAUTR' in col:
        pos = col.index('TAUTR')
        start = max(0, pos-20)
        end = min(len(col), pos+25)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")
        if bi > 55:
            break

print("\n  TAUTR hypotheses:")
print("    1. Proper noun (character name)")
print("    2. TAUTER = 'more deaf/numb' (comparative adj)")
print("    3. TAU + TR = 'dew' + ?")
print("    4. T + AUTR = ? + ?")

# 7. What is LABRNI?
print("\n" + "=" * 60)
print("7. LABRNI / LABRRNI ANALYSIS")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'LABR' in col:
        pos = col.index('LABR')
        start = max(0, pos-15)
        end = min(len(col), pos+20)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")
        if bi > 55:
            break

# Note: LABR appears in both LABRNI and LABGZERAS
# LABGZERAS is the king's name
# Could LABRNI be related?

# 8. CUIT and RLAUNR
print("\n" + "=" * 60)
print("8. CUIT / RLAUNR / SCUIT ANALYSIS")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'CUIT' in col:
        pos = col.index('CUIT')
        start = max(0, pos-15)
        end = min(len(col), pos+20)
        ctx = col[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

print("\n  CUIT/SCUIT in context:")
print("    Always: 'AUNRSONGETRASES CUIT RLAUNRS IST VMTEGE VIEL'")
print("    Or: 'AUNRSONGETRASES SCUIT RLAUNRS IST VMTEGE VIEL'")
print("    SCUIT could be MHG SCHUIT (protection/shield?)")
print("    RLAUNR codes: R-L-A-U-N-R (palindromic consonant frame!)")

# 9. What does the assembled narrative tell us?
print("\n" + "=" * 60)
print("9. NARRATIVE SUMMARY")
print("=" * 60)

# Based on all analysis, piece together the story
print("""
  RECONSTRUCTED NARRATIVE (partial):

  1. Opening: "ER TAUTR IST EILCHANHEARUCHTIG"
     = "He, TAUTR, is [mighty/famous?]"

  2. Purpose: "ER SO DAS TUN DIE..."
     = "He, so that the [something] do..."

  3. Action: "EINER SEIN EDETOTNIURGS"
     = "[One/his] EDETOTNIURGS [dead journey?]"

  4. Alliance: "ER LABRNI WIR UND IEM IN HEDEMI"
     = "He LABRNI, we and [him?] in HEDEMI"

  5. Setting: "DIE URALTE STEIN ENT ER ADTHARSC"
     = "The ancient stone [arose/??] ADTHARSC"

  6. Vision: "IST SCHAUN RU IN WISET"
     = "Is to behold [??] in WISET[=knowledge?]"

  7. Place: "TIUMENGEMI ORT ENGCHD"
     = "[community] place [of worship?]"

  8. Task: "KELSEI DEN DNRHAUNRNVMHISDIZA RUNE"
     = "[??] the DNRHAUN... rune"

  9. Action: "UNTER LAUS IN HIET DEN..."
     = "Under [??] in [heat?] the..."

  10. Mystery: "IST LRSZTHK WIR DAS EUGENDRTHENAEDEULGHLWUOEHSG"
      = "Is [??consonants??] we the [long unknown]..."

  11. Blessing: "SEI GEVMT WIE TUN TAG"
      = "Be formed/shaped as the day does"

  12. Finding: "STEH WRLGTNELNRHELUIRUNN HWND FINDEN"
      = "Stand [at garbled] hound find"

  13. Display: "ER GEIGET ES IN CHN"
      = "He plays/shows it in [??]"

  14. Colophon: "ENDE UTRUNR DENEN DER REDE KOENIG LABGZERAS
      UNENITGHNE AUNRSONGETRASES"
      = "End of utterance of those of the speech,
      King Labgzeras [title] AUNRSONGETRASES"

  KEY THEMES:
  - Ancient stone with runes in a place called HEDEMI
  - A king named LABGZERAS with a title
  - Finding a hound (HEL-hound?)
  - Forming/shaping as the day does
  - A garbled core sequence (possibly a magic incantation)
  - Standing before something and beholding it
""")

# 10. Word frequency ranked by narrative importance
print("=" * 60)
print("10. NARRATIVE VOCABULARY")
print("=" * 60)

important_words = [
    ('RUNE', 23, 'The text is about RUNES - magic inscriptions'),
    ('ERDE', 13, 'EARTH - elemental/geographical'),
    ('STEIN', 9, 'STONE - the ancient stone is central'),
    ('URALTE', 9, 'ANCIENT - describing the stone'),
    ('SCHAUN', 8, 'BEHOLD - MHG, seeing/beholding'),
    ('ORT', 10, 'PLACE - location references'),
    ('STEH', 7, 'STAND - standing before something'),
    ('GEIGET', 7, 'PLAYS/SHOWS - MHG musical/display verb'),
    ('HEDEMI', 7, 'PLACE NAME - where the stone is'),
    ('VIEL', 8, 'MUCH/MANY'),
    ('KOENIG', 6, 'KING - Labgzeras'),
    ('SEIDE', 6, 'SILK - material reference'),
    ('REDE', 6, 'SPEECH - formal proclamation'),
    ('FINDEN', 6, 'FIND - finding the hound'),
    ('TAG', 5, 'DAY'),
    ('HUND', 3, 'HOUND - OHG HWND'),
]

for word, count, note in important_words:
    print(f"  {word:15s} ({count:2d}x): {note}")

print("\n" + "=" * 80)
print("SESSION 10h COMPLETE")
print("=" * 80)
