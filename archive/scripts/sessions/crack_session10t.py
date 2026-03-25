#!/usr/bin/env python3
"""Session 10t: Full narrative segmentation with MHG vocabulary + MINHE discovery"""

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

NEG_INF = float('-inf')

# EXPANDED MHG word list including MINHE discovery
german_words = [
    # Known proper nouns / compound words (preserved as units)
    'EILCHANHEARUCHTIG', 'EDETOTNIURGS', 'WRLGTNELNRHELUIRUNN',
    'TIUMENGEMI', 'SCHWITEIONE', 'LABGZERAS', 'HEDEMI', 'TAUTR',
    'LABRNI', 'ADTHARSC', 'ENGCHD', 'KELSEI',
    # Confirmed German words
    'KOENIG', 'GEIGET', 'SCHAUN', 'URALTE', 'FINDEN', 'DIESER',
    'NORDEN', 'SONNE', 'UNTER', 'NICHT', 'WERDE',
    'STEIN', 'DENEN', 'ERDE', 'VIEL', 'RUNE',
    'STEH', 'LIED', 'SEGEN', 'DORT', 'DENN',
    'GOLD', 'MOND', 'WELT', 'ENDE', 'REDE',
    'HUND', 'SEIN', 'WIRD', 'KLAR', 'ERST',
    'HWND', 'WISET', 'OWI',
    'EINEN', 'EINER', 'SEINE', 'SEIDE',
    'TAG', 'WEG', 'DER', 'DEN', 'DIE', 'DAS',
    'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON',
    'MIT', 'WIE', 'SEI', 'AUS', 'ORT', 'TUN',
    'NUR', 'SUN', 'TOT', 'GAR', 'ACH', 'ZUM',
    'HIN', 'HER', 'ALS', 'AUCH', 'RUND', 'GEH',
    'NACH', 'IENE', 'NOCH', 'ALLE', 'WOHL',
    # NEW: MHG additions from 10s analysis
    'MINHE',      # MHG "minne" (love) - confirmed pattern!
    'HEIT',       # -heit suffix
    'TUOT',       # MHG tun-3sg "does"
    'MUOT',       # MHG "muot" (courage/spirit)
    'GUOT',       # MHG "guot" (good)
    'HUOT',       # MHG "huot" (hat/guard)
    'MICHEL',     # MHG "michel" (great)
    'EDEL',       # noble
    'RITTER',     # knight
    'MEISTER',    # master
    'GEIST',      # spirit
    'KRAFT',      # force
    'RECHT',      # right
    'NACHT',      # night
    'MACHT',      # power
    'LEBEN',      # life
    'GEBEN',      # give
    'NEHMEN',     # take
    'LIEBE',      # love (NHG)
    'FEUER',      # fire
    'WASSER',     # water
    'LICHT',      # light
    'WEISE',      # wise
    'HELD',       # hero
    'HERR',       # lord
    'LAND',       # land
    'GEHEN',      # go
    'SEHEN',      # see
    'WARD',       # became
    'WART',       # waited
    'SOLCH',      # such
    'SELB',       # self
    'ABER',       # but
    'ODER',       # or
    'WENN',       # when
    'DANN',       # then
    'WEIL',       # because
    'HIER',       # here
    'SICH',       # self
    'SIND',       # are
    'SEHR',       # very
    'BURG',       # fortress
    'BERG',       # mountain
    'WALD',       # forest
    'FELD',       # field
    # MHG-specific words to try
    'HIEZ',       # MHG "called" (heißen past)
    'NIHT',       # MHG "nicht" variant
    'VROUWE',     # MHG "lady"
    'SWERT',      # MHG "sword"
    'MAGET',      # MHG "maiden"
    'TUGENDE',    # MHG "virtues"
    'LIGEN',      # MHG "lie" (liegen)
    'GESINDE',    # MHG "retinue"
    'HERRE',      # MHG "lord"
    'RICHE',      # MHG "kingdom/rich"
    'LANDE',      # MHG "lands"
    'TAGE',       # MHG "days"
    'WEGE',       # MHG "ways"
    'STUNDE',     # hour
    'STIMME',     # voice
    'STERNE',     # stars
    'SCHIN',      # MHG "shine"
    'TUGEND',     # virtue
    'SORGE',      # worry
    'FREUDE',     # joy
    'MINNE',      # MHG love (collapsed version)
    'SELE',       # MHG "soul"
    'ERE',        # MHG "honor"
    'SCHEIN',     # shine
    'STEIN',      # already have it
    'TREUE',      # loyalty
    'WISE',       # wise/manner
    'HUOTE',      # MHG "guarding"
    'DIENST',     # service
    'HERZE',      # MHG "heart"
    'OUGE',       # MHG "eye"
    'SINNE',      # MHG "senses"
    'ALTE',       # old
    'IUNGE',      # MHG "young"
    'GROZ',       # MHG "great"
    'GENUOC',     # MHG "enough"
    'MANIG',      # MHG "many"
    'NIEMAN',     # MHG "nobody"
    'ALLER',      # of all
    'IMMER',      # always
    'NIMER',      # MHG "nevermore"
    'ALSE',       # MHG "as"
    'ALSO',       # so
    # Short common MHG
    'ER', 'ES', 'IN', 'SO', 'AN', 'IM', 'OB',
    'AE', 'IR', 'SI', 'EZ', 'NU', 'DA', 'DO',
    'WA', 'WO', 'IE',
    # MHG prepositions/conjunctions
    'VOR', 'NACH', 'BEI', 'ZUO',
    'OBER', 'UBER', 'WIDER',
    'DURCH', 'GEGEN',
    # Verb forms
    'HAT', 'WAS', 'KAN', 'SOL', 'WIL',
    'SAGEN', 'TRAGEN', 'SCHLAGEN',
    'STEN', 'GEN', 'LAN', 'TAN',
]

# Remove duplicates
german_words = list(dict.fromkeys(german_words))
word_scores = {w: len(w) * 3 for w in german_words}
all_words = sorted(word_scores.keys(), key=len, reverse=True)

def dp_segment_full(text):
    """DP segmentation returning word boundaries"""
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
    # Backtrack
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

print("=" * 80)
print("SESSION 10t: FULL NARRATIVE WITH MHG VOCABULARY")
print("=" * 80)

# 1. Full segmented narrative
print("\n1. FULL NARRATIVE SEGMENTATION")
print("-" * 60)

total_covered = 0
total_chars = 0

for bi, book in enumerate(books):
    col = collapse(decode(book))
    parts, covered, n = dp_segment_full(col)
    total_covered += covered
    total_chars += n

    # Format: WORD [unknown] WORD WORD [unknown] ...
    formatted = ''
    for ptype, ptext in parts:
        if ptype == 'W':
            formatted += ptext + ' '
        else:
            formatted += '[' + ptext + '] '

    print(f"\n  B{bi:02d} ({covered}/{n}={covered*100//n if n else 0}%):")
    print(f"    {formatted.strip()}")

print(f"\n  TOTAL COVERAGE: {total_covered}/{total_chars} = {total_covered*100/total_chars:.1f}%")

# 2. Focus on unknown segments with surrounding context
print("\n\n" + "=" * 60)
print("2. UNKNOWN SEGMENTS IN CONTEXT")
print("=" * 60)

# Collect all unknown segments with their left/right word neighbors
unk_contexts = defaultdict(list)
for bi, book in enumerate(books):
    col = collapse(decode(book))
    parts, _, _ = dp_segment_full(col)
    for pi, (ptype, ptext) in enumerate(parts):
        if ptype == '?' and len(ptext) >= 2:
            left = ''
            right = ''
            for j in range(pi-1, -1, -1):
                if parts[j][0] == 'W':
                    left = parts[j][1]
                    break
            for j in range(pi+1, len(parts)):
                if parts[j][0] == 'W':
                    right = parts[j][1]
                    break
            unk_contexts[ptext].append((bi, left, right))

# Show most common unknowns with all contexts
print("\n  Unknown segments with word neighbors (3+ occurrences):")
for unk, contexts in sorted(unk_contexts.items(), key=lambda x: len(x[1]), reverse=True):
    if len(contexts) < 3: continue
    print(f"\n  '{unk}' x{len(contexts)}:")
    seen = set()
    for bi, left, right in contexts:
        key = (left, right)
        if key not in seen:
            seen.add(key)
            print(f"    {left:15s} [{unk}] {right}")

# 3. MINHE verification
print("\n\n" + "=" * 60)
print("3. MINHE (MINNE) VERIFICATION")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'MINHE' in col:
        idx = col.index('MINHE')
        ctx = col[max(0,idx-15):idx+20]
        print(f"  B{bi:02d}: ...{ctx}...")

# How many books contain MINHE?
minhe_books = sum(1 for book in books if 'MINHE' in collapse(decode(book)))
print(f"\n  MINHE appears in {minhe_books} books")

# Check if DIE MINHE pattern is consistent
print("\n  DIE MINHE pattern check:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'MINHE' in col:
        idx = col.index('MINHE')
        before = col[max(0,idx-5):idx]
        print(f"    B{bi:02d}: before MINHE = '{before}'")

# 4. Attack GEVMT - most common unknown (7x)
print("\n\n" + "=" * 60)
print("4. ATTACK: GEVMT (7x)")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'GEVMT' in col:
        idx = col.index('GEVMT')
        ctx = col[max(0,idx-12):idx+15]
        # Get raw codes
        decoded = decode(book)
        for ri in range(len(decoded)):
            sub = decoded[ri:ri+10]
            if collapse(sub).startswith('GEVMT'):
                raw_codes = book[ri:ri+8]
                raw_letters = [mapping.get(c, '?') for c in raw_codes[:8]]
                print(f"  B{bi:02d}: ...{ctx}...")
                print(f"    codes: {raw_codes[:8]}")
                print(f"    letters: {' '.join(f'{c}={l}' for c, l in zip(raw_codes[:8], raw_letters))}")
                break

# What letters does GEVMT consist of?
print("\n  GEVMT = G-E-V-M-T")
print("  Could be: GE-VMT or GEV-MT")
print("  'ge-' is common German prefix (past participle)")
print("  'VMT' = ??? 'vmt' is not a German root")
print("  Could V be wrong? If V→F: GEFMT? Still odd.")
print("  If V→U: GEUMT? GE-UMT? Still odd.")

# But wait - VMTEGE also appears
print("\n  Related: VMTEGE also appears")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'VMTEGE' in col:
        idx = col.index('VMTEGE')
        ctx = col[max(0,idx-10):idx+15]
        print(f"    B{bi:02d}: ...{ctx}...")

# 5. Attack NGETRAS (7x)
print("\n\n" + "=" * 60)
print("5. ATTACK: NGETRAS (7x)")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    pos = 0
    while True:
        idx = col.find('NGETRAS', pos)
        if idx < 0: break
        ctx = col[max(0,idx-10):idx+15]
        print(f"  B{bi:02d}: ...{ctx}...")
        pos = idx + 1
        break  # one per book

# Could be N-GETRAS = ? + GETRAS
# Or NGE-TRAS = ? + TRAS
# TRAGEN = to carry; GETRAGEN = carried
# But NGETRAS doesn't match GETRAGEN
print("  NGETRAS: possibly 'N GE TRAS' or 'NGE TRAS'")
print("  TRAGEN (carry) -> GE-TRAGEN (carried)?")
print("  TRAS could be from MHG 'tratz' (defiance)")

# 6. Attack DGEDA (6x)
print("\n\n" + "=" * 60)
print("6. ATTACK: DGEDA (6x)")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'DGEDA' in col:
        idx = col.index('DGEDA')
        ctx = col[max(0,idx-10):idx+15]
        decoded = decode(book)
        for ri in range(len(decoded)):
            sub = decoded[ri:ri+10]
            if collapse(sub).startswith('DGEDA'):
                raw_codes = book[ri:ri+8]
                raw_letters = [mapping.get(c, '?') for c in raw_codes[:8]]
                print(f"  B{bi:02d}: ...{ctx}...")
                print(f"    codes: {raw_codes[:8]}, letters: {raw_letters[:8]}")
                break
        break

print("  DGEDA: D-G-E-D-A")
print("  Could be: D GEDA or DGE DA")
print("  GEDANKE (thought) starts with GEDA!")
print("  So: [D] GEDA[NKE] or [UND] GEDA[NKE]")

# Verify: does GEDANKE or GEDAN appear?
print("\n  Checking for GEDAN* pattern:")
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'GEDAN' in col:
        idx = col.index('GEDAN')
        ctx = col[max(0,idx-5):idx+15]
        print(f"    B{bi:02d}: ...{ctx}...")

# 7. Attack SCE (6x)
print("\n\n" + "=" * 60)
print("7. ATTACK: SCE (6x)")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    pos = 0
    while True:
        idx = col.find('SCE', pos)
        if idx < 0: break
        # Make sure it's not part of SCHAUN etc
        ctx = col[max(0,idx-10):idx+10]
        if 'SCH' not in col[idx:idx+4]:  # Not SCH digraph
            print(f"  B{bi:02d}: ...{ctx}...")
        pos = idx + 1

print("  SCE = S-C-E")
print("  In MHG: 'sce' not a common sequence")
print("  Could be word boundary: S + CE or SC + E")
print("  'schaz' (treasure) starts SCH not SC")

# 8. Attack CHN (7x)
print("\n\n" + "=" * 60)
print("8. ATTACK: CHN (7x)")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    pos = 0
    while True:
        idx = col.find('CHN', pos)
        if idx < 0: break
        ctx = col[max(0,idx-10):idx+12]
        print(f"  B{bi:02d}: ...{ctx}...")
        pos = idx + 1
        break

print("  CHN: common in German after vowel (ZEICHEN, REICHEN, etc)")
print("  Could be end of -CHEN (diminutive) + N")

# 9. Coverage with expanded vocabulary
print("\n\n" + "=" * 60)
print("9. COVERAGE SUMMARY")
print("=" * 60)
print(f"  Total coverage: {total_covered}/{total_chars} = {total_covered*100/total_chars:.1f}%")
print(f"  Words in dictionary: {len(german_words)}")

# Count word frequencies in segmentation
word_freq = Counter()
for bi, book in enumerate(books):
    col = collapse(decode(book))
    parts, _, _ = dp_segment_full(col)
    for ptype, ptext in parts:
        if ptype == 'W':
            word_freq[ptext] += 1

print(f"\n  Top 30 words by frequency:")
for w, c in word_freq.most_common(30):
    print(f"    {w:20s} x{c}")

print("\n" + "=" * 80)
print("SESSION 10t COMPLETE")
print("=" * 80)
