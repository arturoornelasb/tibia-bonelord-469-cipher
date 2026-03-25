#!/usr/bin/env python3
"""Session 10q: Phrase structure analysis + MHG deep vocabulary"""

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

all_col = [(i, collapse(decode(b))) for i, b in enumerate(books)]

print("=" * 80)
print("SESSION 10q: PHRASE STRUCTURE + MHG VOCABULARY EXPANSION")
print("=" * 80)

# 1. PHRASE ALIGNMENT - compare all books to find repeating segments
print("\n1. PHRASE STRUCTURE ACROSS ALL BOOKS")
print("-" * 60)

# Get all non-substring pieces
pieces = {}
for i, text in all_col:
    is_sub = False
    for j, other in all_col:
        if i != j and text in other:
            is_sub = True
            break
    if not is_sub:
        pieces[i] = text

# Find common substrings of length >= 8
print("  Common phrases (>= 8 chars, appearing in 3+ unique pieces):")
phrase_count = Counter()
for bi, text in pieces.items():
    seen = set()
    for length in range(8, min(30, len(text))):
        for start in range(len(text) - length + 1):
            sub = text[start:start+length]
            if sub not in seen:
                seen.add(sub)
                phrase_count[sub] += 1

# Filter to substrings appearing 3+ times that aren't substrings of longer hits
common = {s: c for s, c in phrase_count.items() if c >= 3}
# Remove substrings of longer common strings
maximal = {}
for s in sorted(common.keys(), key=len, reverse=True):
    is_sub = False
    for longer in maximal:
        if s in longer:
            is_sub = True
            break
    if not is_sub:
        maximal[s] = common[s]

for phrase, count in sorted(maximal.items(), key=lambda x: (-x[1], -len(x[0]))):
    if len(phrase) >= 8:
        print(f"    [{count}x] {phrase}")

# 2. SENTENCE STRUCTURE - the text has clear clauses
print("\n" + "=" * 60)
print("2. CLAUSE ANALYSIS")
print("=" * 60)

# The longest book seems to contain the full narrative
# Let's analyze the structure
by_len = sorted(pieces.items(), key=lambda x: len(x[1]), reverse=True)
longest_bi, longest = by_len[0]

print(f"  Longest piece: Book {longest_bi} ({len(longest)} chars)")
print(f"  Full text:")
for i in range(0, len(longest), 70):
    print(f"    {longest[i:i+70]}")

# 3. Try to identify clauses by known word positions
print("\n" + "=" * 60)
print("3. KNOWN WORD POSITIONS IN LONGEST BOOK")
print("=" * 60)

text = longest
known_words = [
    ('EILCHANHEARUCHTIG', 'PROP-ADJ'),
    ('EDETOTNIURGS', 'PROP-NOUN'),
    ('WRLGTNELNRHELUIRUNN', 'PROP-NOUN'),
    ('DNRHAUNRNVMHISDIZA', 'PROP-NOUN'),
    ('AUNRSONGETRASES', 'PROP-NOUN'),
    ('EUGENDRTHENAEDEULGHLWUOEHSG', 'PROP-NOUN'),
    ('TIUMENGEMI', 'NOUN'),
    ('SCHWITEIONE', 'PROP-NOUN'),
    ('LABGZERAS', 'PROP-NOUN'),
    ('UNENITGHNE', 'PROP-NOUN'),
    ('ADTHARSC', 'PROP-NOUN'),
    ('ENGCHD', 'PROP-NOUN'),
    ('HEDEMI', 'PROP-NOUN'),
    ('KELSEI', 'PROP-NOUN'),
    ('TAUTR', 'PROP-NOUN'),
    ('DIESER', 'DET'), ('FINDEN', 'VERB'), ('SCHAUN', 'VERB'),
    ('GEIGET', 'VERB'), ('URALTE', 'ADJ'),
    ('KOENIG', 'NOUN'), ('STEIN', 'NOUN'), ('RUNE', 'NOUN'),
    ('ERDE', 'NOUN'), ('SEGEN', 'NOUN'), ('REDE', 'NOUN'),
    ('GOLD', 'NOUN'), ('MOND', 'NOUN'), ('SONNE', 'NOUN'),
    ('WELT', 'NOUN'), ('HUND', 'NOUN'), ('HWND', 'NOUN'),
    ('STEH', 'VERB'), ('WIRD', 'VERB'), ('WERDE', 'VERB'),
    ('LIED', 'NOUN'), ('SEIDE', 'NOUN'),
    ('SEINE', 'POSS'), ('SEIN', 'POSS'), ('EINEN', 'DET'),
    ('EINER', 'DET'), ('KLAR', 'ADJ'), ('ERST', 'ADV'),
    ('DENEN', 'PRON'), ('UNTER', 'PREP'), ('NICHT', 'NEG'),
    ('NORDEN', 'NOUN'), ('VIEL', 'ADJ'),
    ('STEIEN', 'NOUN'), ('VMTEGE', 'NOUN'),
    ('EMPOR', 'ADV'), ('ENDE', 'NOUN'), ('OWI', 'INTERJ'),
    ('DORT', 'ADV'), ('DENN', 'CONJ'),
    ('AUCH', 'ADV'), ('RUND', 'ADJ'),
    ('DAS', 'DET'), ('DER', 'DET'), ('DIE', 'DET'), ('DEN', 'DET'),
    ('UND', 'CONJ'), ('IST', 'VERB'), ('EIN', 'DET'),
    ('SIE', 'PRON'), ('WIR', 'PRON'), ('VON', 'PREP'),
    ('MIT', 'PREP'), ('WIE', 'CONJ'), ('SEI', 'VERB'),
    ('AUS', 'PREP'), ('ORT', 'NOUN'), ('TUN', 'VERB'),
    ('NUR', 'ADV'), ('SUN', 'NOUN'), ('TOT', 'ADJ'),
    ('GAR', 'ADV'), ('ACH', 'INTERJ'), ('ZUM', 'PREP'),
    ('HIN', 'ADV'), ('HER', 'ADV'), ('ALS', 'CONJ'),
    ('GEH', 'VERB'),
    ('ER', 'PRON'), ('ES', 'PRON'), ('IN', 'PREP'), ('SO', 'ADV'),
]

# Find positions
positions = []
for word, pos_tag in known_words:
    idx = text.find(word)
    if idx >= 0:
        positions.append((idx, idx+len(word), word, pos_tag))

positions.sort()

# Show annotated text
print(f"\n  Annotated narrative:")
last_end = 0
clauses = []
current = []
for start, end, word, tag in positions:
    if start >= last_end:
        gap = text[last_end:start]
        if gap:
            current.append(f'[{gap}]')
        current.append(f'{word}({tag})')
        last_end = end
    elif start > positions[0][0]:  # Overlap - skip
        pass

remaining = text[last_end:]
if remaining:
    current.append(f'[{remaining}]')

annotated = ' '.join(current)
for i in range(0, len(annotated), 78):
    print(f"    {annotated[i:i+78]}")

# 4. MHG expanded vocabulary
print("\n" + "=" * 60)
print("4. MHG EXPANDED VOCABULARY SEARCH")
print("=" * 60)

# Additional MHG words to search for
mhg_words = [
    # Verbs
    'WISEN', 'WISET', 'VINDEN', 'STEHEN', 'REDEN', 'SAGEN', 'GEBEN',
    'NEMEN', 'KOMEN', 'LEGEN', 'TRAGEN', 'FUEREN', 'RUOFEN',
    'SINGEN', 'SPRECHEN', 'STERBEN', 'HELFEN', 'WERDEN',
    'HEIZEN', 'NENNEN', 'SENDEN', 'WONEN',
    # Nouns
    'MEISTER', 'RITTER', 'HERRE', 'VROUWE', 'KNECHT', 'TUGEND',
    'MINNE', 'WUNDER', 'HELDEN', 'LAND', 'BURG', 'STAT',
    'VOLC', 'DIET', 'ORDEN', 'GESELLE', 'BRUODER',
    'KRAFT', 'MACHT', 'KUNST', 'GEIST', 'LEIB', 'HERZ',
    'SEELE', 'STIMME', 'WORT', 'BUCH', 'BRIEF',
    # Adjectives
    'EDEL', 'HOCH', 'GROSS', 'LANG', 'STARK', 'RECHT',
    'HEILIG', 'TIEF', 'WERT', 'GUOT', 'BOESE',
    'SCHOENE', 'REINE', 'ALTE', 'NEWE',
    # Pronouns/Articles
    'DISE', 'IENE', 'ANDER', 'SELBE', 'IEDER',
    # Prepositions/Conjunctions
    'NACH', 'UBER', 'DURCH', 'GEGEN', 'ZWISCHEN',
    'WENN', 'WEIL', 'ODER', 'ABER', 'NOCH', 'SCHON',
    # Numbers
    'ZWEI', 'DREI', 'VIER', 'FUNF', 'SECHS', 'SIBEN',
    # Adverbs
    'IMMER', 'IMER', 'NIMMER', 'WIDER', 'GERNE',
    'NIHT', 'WOHL', 'BALDE', 'SERE',
    # MHG-specific forms
    'WISSET', 'WISENT', 'KUNIC', 'KUNEC',
    'WERLT', 'HANT', 'GRUNT', 'SLANGE', 'WISE',
    'UMBE', 'MITTE', 'INNE', 'OBEN', 'UNTEN',
]

found_new = []
for word in mhg_words:
    for bi, col in all_col:
        if word in col:
            pos = col.index(word)
            start = max(0, pos-5)
            end = min(len(col), pos+len(word)+5)
            ctx = col[start:end]
            found_new.append((word, bi, ctx))
            break

print("  New MHG words found:")
for word, bi, ctx in found_new:
    if word not in ['ERDE', 'RUNE', 'STEIN', 'KOENIG', 'GOLD', 'MOND',
                    'SONNE', 'WELT', 'HUND', 'LIED', 'SEGEN',
                    'SEIN', 'DER', 'DIE', 'DAS', 'ENDE', 'UND',
                    'IST', 'NICHT', 'UNTER', 'ODER', 'NOCH',
                    'AUCH', 'ERST', 'WIRD', 'WERDE', 'REDE',
                    'SEINE', 'FINDEN', 'SCHAUN', 'DIESER',
                    'NORDEN', 'STEH', 'DORT', 'DENN', 'VIEL',
                    'KLAR', 'AUS', 'MIT', 'WIR', 'HER', 'HIN',
                    'NUR', 'ALS', 'WIE', 'GAR', 'ACH']:
        print(f"    {word:15s} B{bi:02d}: ...{ctx}...")

# 5. Attack unknown segments individually
print("\n" + "=" * 60)
print("5. INDIVIDUAL SEGMENT ATTACK")
print("=" * 60)

# NHI - appears at start: "[NHI] ER TAUTR IST..."
# Could be an interjection or title
print("\n  NHI analysis:")
for bi, col in all_col:
    if col.startswith('NHI') or 'NHIER' in col:
        print(f"    B{bi:02d}: {col[:30]}...")
        break

# NHI could be: N + HI (well/here) or NH + I
# In MHG: "nu" = now. If NHI = NU + HI... but U != H
# Or: NHI = name/title?
# Context: "NHI ER TAUTR IST" = "NHI he TAUTR is"
# Sounds like: "[name/title] he TAUTR is..."
# Could NHI be a title? Like a garbled form?

# IEM analysis - "UND IEM IN HEDEMI"
print("\n  IEM analysis:")
for bi, col in all_col:
    if 'UNDIEM' in col or 'IENUNDIEM' in col:
        pos = col.find('IEM')
        start = max(0, pos-8)
        end = min(len(col), pos+12)
        print(f"    B{bi:02d}: ...{col[start:end]}...")
        break

# RUI - "SCHAUN RUI IN WISET"
print("\n  RUI analysis:")
for bi, col in all_col:
    if 'RUI' in col:
        pos = col.index('RUI')
        start = max(0, pos-8)
        end = min(len(col), pos+15)
        print(f"    B{bi:02d}: ...{col[start:end]}...")
        break

# SCE - "ER SCE AUS"
print("\n  SCE analysis:")
print("  ER SCE AUS = 'he SCE from/out'")
print("  Possible: ERSCHE(INT) = appears -> ER SCHE AUS?")
print("  But SCE != SCHE (missing H)")
# Check raw codes for SCE
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'ERSCEA' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if 'RSCE' in collapse(decoded[ri:ri+8]):
                codes = book[ri:ri+6]
                letters = [mapping.get(c, '?') for c in codes]
                print(f"    B{bi:02d} codes: {' '.join(codes)} = {''.join(letters)}")
                break
        break

# CHN - "IN CHN ES"
print("\n  CHN analysis:")
print("  Context: 'GEIGET ES IN CHN ES R ER SCE AUS'")
print("  = 'shows it in CHN ... he SCE from'")
print("  CHN could be proper noun (place)")
# Check raw
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'INCHNES' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if 'NCHNE' in collapse(decoded[ri:ri+10]):
                codes = book[ri:ri+7]
                letters = [mapping.get(c, '?') for c in codes]
                print(f"    B{bi:02d} codes: {' '.join(codes)} = {''.join(letters)}")
                break
        break

# 6. TEIGN - the persistent mystery
print("\n" + "=" * 60)
print("6. TEIGN DEEP ANALYSIS")
print("=" * 60)

# Context: "FINDEN TEIGN DAS ES DER ERSTE"
# TEIGN between FINDEN and DAS
# Could TEIGN be a verb? Adjective?
# In MHG: ZEIGEN = to show (but we have T not Z)
# TEIG = dough? TEIGEN = to knead?
# Or: T + EIGN = ? + own/proper?
# EIGEN = own. TE + IGN?

print("  TEIGN contexts:")
for bi, col in all_col:
    if 'TEIGN' in col:
        pos = col.index('TEIGN')
        start = max(0, pos-10)
        end = min(len(col), pos+20)
        print(f"    B{bi:02d}: ...{col[start:end]}...")
        if bi > 30:
            break

# Check raw codes
print("\n  TEIGN raw codes:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'TEIGN' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if 'TEIGN' in collapse(decoded[ri:ri+8]):
                codes = book[ri:ri+5]
                letters = [mapping.get(c, '?') for c in codes]
                print(f"    B{bi:02d}: {' '.join(codes)} = {''.join(letters)}")
                break
        break

# 7. NTENTUIGA / TUIGA analysis
print("\n" + "=" * 60)
print("7. NTENTUIGA / TUIGA")
print("=" * 60)

# Context: "ERDE NGE ENDEN TENTUIGA ER GEIGET ES"
# ERDE = earth, NGE = ?, ENDEN = to end,
# TENTUIGA = ? ER GEIGET ES = he shows it
# Could TENTUIGA be a name?
# TEN + TUIGA? Or TENT + UIGA?
# With genuine doubles: ENTENNTTUIGAA -> ENDEN TT UIGAA
# The TT is genuine: end of ENDENT and start of TUIGAA
# So: ENDENT + TUIGAA? ENDEN + T + TUIGAA?
# TUIGAA with genuine AA: real doubled A

print("  Full context with raw doubles:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'NTENTUIGA' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            test = collapse(decoded[ri:ri+20])
            if 'NTENTUIGA' in test:
                raw = decoded[ri:ri+15]
                codes = book[ri:ri+15]
                print(f"    B{bi:02d} raw: {raw}")
                print(f"    codes: {' '.join(codes)}")
                break
        break

# 8. LUSED / LUSEDHER
print("\n" + "=" * 60)
print("8. LUSED / LUSEDHER ANALYSIS")
print("=" * 60)

for bi, col in all_col:
    if 'LUSED' in col:
        pos = col.index('LUSED')
        start = max(0, pos-10)
        end = min(len(col), pos+20)
        print(f"  B{bi:02d}: ...{col[start:end]}...")
        break

# LUSED HER = ? here
# ERLOESUNG = salvation? No, LUSED
# GELUST = pleasure -> GELUSED = pleasured?
# Or: LUST + ED? Or LUSE + D?

# 9. EZEELUSED pattern (appears in several books)
print("\n" + "=" * 60)
print("9. EZEELUSED PATTERN")
print("=" * 60)

for bi, col in all_col:
    if 'ELUSED' in col or 'ZELUSED' in col:
        pos = col.find('LUSED')
        start = max(0, pos-12)
        end = min(len(col), pos+15)
        print(f"  B{bi:02d}: ...{col[start:end]}...")

# Raw codes for EZEELUSED
print("\n  Raw codes:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'ZELUSED' in col:
        decoded = decode(book)
        for ri in range(len(decoded)):
            if 'ZEELUSE' in decoded[ri:ri+10]:
                codes = book[ri:ri+8]
                raw = decoded[ri:ri+10]
                print(f"    B{bi:02d}: {raw} = codes {' '.join(codes)}")
                break
        break

# 10. Book structure summary
print("\n" + "=" * 60)
print("10. NARRATIVE STRUCTURE SUMMARY")
print("=" * 60)

# From the analysis, the narrative structure appears to be:
# Multiple books contain overlapping fragments of the same text
# The full text describes:
print("""
  RECONSTRUCTED NARRATIVE ORDER (best guess):

  CLAUSE 1: [NHI] ER TAUTR IST EILCHANHEARUCHTIG
            "[NHI] he TAUTR is [adjective ending in -IG]"
            = A character named TAUTR who has quality EILCHANHEARUCHTIG

  CLAUSE 2: ER SO DAS TUN DIESER [T] EINER SEIN EDETOTNIURGS
            "he so that do/deed this [T] one his EDETOTNIURGS"
            = He does something involving EDETOTNIURGS

  CLAUSE 3: ER LABRNI WIR UND IEM IN HEDEMI
            "he LABRNI we and IEM in HEDEMI"
            = Something involving place HEDEMI

  CLAUSE 4: DIE URALTE STEIN EINEN [T] ER ADTHARSC
            "the ancient stone a/one [T] he ADTHARSC"
            = The ancient stone, and ADTHARSC

  CLAUSE 5: IST SCHAUN RUI IN WISET [EIS?]
            "is see/look RUI in shows [ice?]"

  CLAUSE 6: NHI ER [S] ER TIUMENGEMI ORT ENGCHD
            "[NHI] he [S] he community place ENGCHD"
            = Reference to community of ENGCHD

  CLAUSE 7: KELSEI DEN DNRHAUNRNVMHISDIZA
            "KELSEI the DNRHAUNRNVMHISDIZA"

  CLAUSE 8: RUNE [D] UNTER LAUS IN HIET DEN ENDE SCHWITEIONE
            "rune [D] under ... in HIET the end SCHWITEIONE"

  CLAUSE 9: MI SEIN NDGE DAS SIE OWI RUNE AU IEN
            "MI his [NDGE] that she OWI rune on/from ..."

  CLAUSE 10: ERDE NGE ENDEN TENTUIGA ER GEIGET ES
             "earth [NGE] end TENTUIGA he shows it"

  CLAUSE 11: IN CHN ES R ER SCE AUS ENDE UTRUNR
             "in CHN ... he SCE from end UTRUNR"

  CLAUSE 12: DENEN DER ERDE DER KOENIG LABGZERAS
             "those the earth the king LABGZERAS"

  CLAUSE 13: UNENITGHNE AUNRSONGETRASES
             "UNENITGHNE AUNRSONGETRASES"
""")

# 11. Check if shorter books provide word boundary clues
print("=" * 60)
print("11. SHORTEST BOOKS - WORD BOUNDARY CLUES")
print("=" * 60)

by_len_short = sorted(all_col, key=lambda x: len(x[1]))
for bi, text in by_len_short[:10]:
    if len(text) > 5:
        print(f"  B{bi:02d} ({len(text):3d}): {text}")

print("\n" + "=" * 80)
print("SESSION 10q COMPLETE")
print("=" * 80)
