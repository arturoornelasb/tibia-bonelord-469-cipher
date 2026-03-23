"""
Narrative Translation: Manual sentence-level analysis of best decoded passages.
Accepts 24=R (strong evidence). Tests 71 cautiously.
Attempts to identify word boundaries and translate continuous German.
"""
import json
import os
import re
from collections import Counter

data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'final_mapping_v2.json'), 'r') as f:
    base_mapping = json.load(f)

# Apply 24=R (confirmed by deep_crack_v2: creates UNTER, ER ALS, ER AM NEU)
mapping = dict(base_mapping)
mapping['24'] = 'R'
mapping['33'] = 'W'
# 71 stays I for now (N makes N even more inflated: 11.9% vs 9.8% expected)

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    ic0 = ic_from_counts(Counter(bp0), len(bp0))
    ic1 = ic_from_counts(Counter(bp1), len(bp1))
    return 0 if ic0 > ic1 else 1

def decode_book(book, m):
    offset = get_offset(book)
    pairs = [book[j:j+2] for j in range(offset, len(book)-1, 2)]
    return ''.join(m.get(p, '?') for p in pairs)

def get_pairs(book):
    offset = get_offset(book)
    return [book[j:j+2] for j in range(offset, len(book)-1, 2)]

# ============================================================
# 1. SENTENCE-LEVEL ANALYSIS OF BEST PASSAGE (Book 5, 9, etc.)
# ============================================================
print("=" * 80)
print("1. SENTENCE-LEVEL TRANSLATION OF MAIN NARRATIVE")
print("=" * 80)

# Book 5 is the most informative (136 chars, highest readable content)
# Let's decode it with detailed code-by-code annotation
for target_book in [5, 9, 2, 27, 11, 32, 48, 53]:
    dec = decode_book(books[target_book], mapping)
    pairs = get_pairs(books[target_book])

    print(f"\n--- Book {target_book} ({len(dec)} chars) ---")
    print(f"  Decoded: {dec}")

    # Manual word boundary attempt
    # Mark known words
    text = dec
    boundaries = []

    # Long words first
    known = [
        'AUNRSONGETRASES', 'HEARUCHTIGER', 'SCHWITEIO', 'LABGZERAS', 'TOTNIURG',
        'THARSC', 'RUNEORT', 'STEINEN', 'STEINE', 'URALTE', 'URALTEN',
        'DIESER', 'SEINER', 'SEINEN', 'SEINEM', 'SEINE', 'SEIN',
        'KOENIG', 'KOENIGS', 'ORTEN', 'ERSTE', 'STEIL',
        'EINER', 'EINEN', 'EINEM', 'EINE', 'DENEN', 'DENN',
        'FINDEN', 'GEBEN', 'GEGEN', 'ENDEN', 'UNTER',
        'NICHT', 'ERDE', 'ENDE', 'REDE', 'RUNE', 'RUNEN',
        'DASS', 'DIES', 'HIER', 'NACH', 'AUCH', 'WEIL',
        'FACH', 'SEID', 'TEIL', 'WORT', 'LAND',
        'ABER', 'ALLE', 'ALSO', 'NOCH', 'SCHAU',
        'WIR', 'UND', 'DIE', 'DER', 'DAS', 'DEM', 'DEN', 'DES',
        'AUS', 'SEE', 'NEU', 'ORT', 'GAR', 'NUN', 'TOT', 'TAG',
        'WAR', 'WAS', 'WER', 'WIE', 'WEG', 'TUN',
        'ICH', 'IHR', 'IHN', 'IHM',
        'GEH', 'HAT', 'HIN', 'IST',
        'VON', 'VOR', 'VOM', 'FUR',
        'ZUM', 'ZUR', 'EIN', 'MIN', 'GEM',
        'ER', 'ES', 'SO', 'DA', 'AN', 'AM', 'IM', 'IN', 'AB', 'ZU',
        'DE', 'EN', 'UM', 'OB', 'NU',
    ]

    # Greedy forward match
    pos = 0
    parsed = []
    while pos < len(text):
        best_match = None
        for word in sorted(known, key=len, reverse=True):
            if text[pos:pos+len(word)] == word:
                best_match = word
                break
        if best_match:
            parsed.append(best_match)
            pos += len(best_match)
        else:
            # Collect unrecognized chars until next match
            unrec_start = pos
            pos += 1
            while pos < len(text):
                found = False
                for word in sorted(known, key=len, reverse=True):
                    if text[pos:pos+len(word)] == word:
                        found = True
                        break
                if found:
                    break
                pos += 1
            parsed.append(f"[{text[unrec_start:pos]}]")

    print(f"  Parsed: {' '.join(parsed)}")

# ============================================================
# 2. FOCUS ON RECURRING UNRECOGNIZED SEGMENTS
# ============================================================
print(f"\n\n{'='*80}")
print("2. RECURRING UNKNOWN SEGMENTS: WHAT ARE THEY?")
print(f"{'='*80}")

unknowns = {
    'HED': 'appears in MINHEDDEM - could be "HED" = archaic for "had"?',
    'TAUTRI': 'appears after HIER - "HIER TAUTRI STEIL" - TAU+TRI? TAUT+RI?',
    'UTRUNR': 'appears in ENDEUTRUNR - "ENDE UTRUNR" or "EN DEUTRUNR"?',
    'HECHLLT': 'HECHL = hackle? HECHLL = ?',
    'HIHLDI': 'HIH+LDI? HIHL+DI?',
    'TEIGN': 'TEIG+N? TEIGN = dough?',
    'SCE': 'SC+E? part of THARSC E?',
    'NRUI': 'NRU+I? follows SCHAU',
    'OEL': 'OEL = oil? "ICHOELSODE" = ICH OEL SO DE?',
    'NDTEII': 'ND+TEII? appears in context of ORT',
    'AEUT': 'AE+UT? appears before ERALS',
    'WIISETN': 'WIIS+ETN? follows IIIWII/IINWII pattern',
    'LGTNELGZ': 'LGT+NELGZ? precedes ERAS (= LABGZERAS?)',
    'NSCHA': 'N+SCHA? SCHAU variant?',
    'NDGE': 'ND+GE? common German prefix',
    'GEVM': 'GE+VM? GEV+M?',
    'IEOWI': 'I+EOWI? appears in SIEOWI context',
    'DUNLN': 'DUN+LN? DUNL+N?',
}

for seg, analysis in unknowns.items():
    # Find all contexts
    contexts = []
    for i, book in enumerate(books):
        dec = decode_book(book, mapping)
        pos = 0
        while True:
            p = dec.find(seg, pos)
            if p == -1: break
            ctx = dec[max(0,p-8):min(len(dec), p+len(seg)+8)]
            contexts.append(f"Bk{i}:{ctx}")
            pos = p + 1
    print(f"\n  {seg} ({len(contexts)}x): {analysis}")
    for ctx in contexts[:3]:
        print(f"    {ctx}")

# ============================================================
# 3. TEST: WHAT IF 'CH' IN DECODED TEXT IS ACTUALLY WRONG?
# ============================================================
print(f"\n\n{'='*80}")
print("3. CODE 18 (=C) INVESTIGATION")
print(f"{'='*80}")

# C appears 124 times (2.2%). German C is 2.7%.
# But C almost always appears before H in German (CH digraph)
# Let's check: does code 18 always precede an H-code?
c_contexts = []
for i, book in enumerate(books):
    pairs = get_pairs(book)
    for k, p in enumerate(pairs):
        if p == '18':
            before = mapping.get(pairs[k-1], '?') if k > 0 else '^'
            after = mapping.get(pairs[k+1], '?') if k < len(pairs)-1 else '$'
            c_contexts.append((before, after))

print(f"\n  Code 18 (C) contexts: {len(c_contexts)} occurrences")
after_counts = Counter(after for _, after in c_contexts)
print(f"  Letter after C: {dict(after_counts.most_common(10))}")
before_counts = Counter(before for before, _ in c_contexts)
print(f"  Letter before C: {dict(before_counts.most_common(10))}")

ch_count = sum(1 for _, a in c_contexts if a == 'H')
print(f"  C followed by H: {ch_count}/{len(c_contexts)} ({ch_count/len(c_contexts)*100:.0f}%)")
print(f"  C NOT followed by H: {len(c_contexts) - ch_count}")

# ============================================================
# 4. LOOK FOR P - MISSING LETTER
# ============================================================
print(f"\n\n{'='*80}")
print("4. MISSING LETTER P (0.67% expected = ~37 occurrences)")
print(f"{'='*80}")

# P is missing from the mapping. At 0.67%, we'd expect ~37 P's in 5600 chars.
# Could one of the codes currently assigned to another letter actually be P?
# Most likely candidates: low-frequency codes assigned to high-frequency letters
# That seem to create bad contexts

# Check all codes with <50 occurrences that might be P
code_counts = Counter()
for book in books:
    pairs = get_pairs(book)
    for p in pairs:
        code_counts[p] += 1

print("\nCodes with 15-50 occurrences (P-range frequency):")
for code, count in sorted(code_counts.items(), key=lambda x: x[1]):
    if 15 <= count <= 50:
        current_letter = mapping.get(code, '?')
        # Test as P
        test_m = dict(mapping)
        test_m[code] = 'P'
        # Check contexts
        p_contexts = []
        for book in books:
            pairs = get_pairs(book)
            dec_base = ''.join(mapping.get(p2, '?') for p2 in pairs)
            dec_test = ''.join(test_m.get(p2, '?') for p2 in pairs)
            for k, p2 in enumerate(pairs):
                if p2 == code:
                    ctx_base = dec_base[max(0,k-3):k+4]
                    ctx_test = dec_test[max(0,k-3):k+4]
                    p_contexts.append(f"{ctx_base}=>{ctx_test}")

        # Look for German words with P
        p_words_found = 0
        for ctx in p_contexts:
            after = ctx.split('=>')[1] if '=>' in ctx else ''
            for pw in ['SPR', 'PER', 'PEL', 'OPF', 'UPT', 'AMP', 'IMP', 'UMP']:
                if pw in after.upper():
                    p_words_found += 1

        if p_words_found > 0 or count < 30:
            print(f"  Code {code} ({count}x, currently {current_letter}): P-word hits: {p_words_found}")
            for ctx in p_contexts[:3]:
                print(f"    {ctx}")

# ============================================================
# 5. COMPLETE TRANSLATION ATTEMPT
# ============================================================
print(f"\n\n{'='*80}")
print("5. COMPLETE NARRATIVE TRANSLATION")
print(f"{'='*80}")

# Build superstring from all books
decoded_all = []
seen = set()
for book in books:
    dec = decode_book(book, mapping)
    if dec not in seen:
        decoded_all.append(dec)
        seen.add(dec)

# Greedy overlap assembly
def find_best_overlap(fragments):
    best_score = 0
    best_i = best_j = -1
    best_merged = ''
    for i in range(len(fragments)):
        for j in range(len(fragments)):
            if i == j: continue
            a, b = fragments[i], fragments[j]
            max_ov = min(len(a), len(b))
            for ov in range(max_ov, 0, -1):
                if a[-ov:] == b[:ov]:
                    if ov > best_score:
                        best_score = ov
                        best_i, best_j = i, j
                        best_merged = a + b[ov:]
                    break
    return best_score, best_i, best_j, best_merged

frags = list(decoded_all)
while len(frags) > 1:
    score, i, j, merged = find_best_overlap(frags)
    if score < 4:
        break
    frags = [f for k, f in enumerate(frags) if k != i and k != j] + [merged]

# Find the largest fragment
main_frag = max(frags, key=len)
print(f"\nMain narrative ({len(main_frag)} chars):")

# Parse into sentences
known_words = [
    'AUNRSONGETRASES', 'HEARUCHTIGER', 'SCHWITEIO', 'LABGZERAS', 'TOTNIURG',
    'THARSC', 'RUNEORT', 'STEINEN', 'STEINE', 'URALTE', 'URALTEN',
    'DIESER', 'SEINER', 'SEINEN', 'SEINEM', 'SEINE', 'SEIN',
    'KOENIG', 'KOENIGS', 'ORTEN', 'ORTE', 'ERSTE', 'STEIL',
    'EINER', 'EINEN', 'EINEM', 'EINE', 'DENEN', 'DENN',
    'FINDEN', 'GEBEN', 'GEGEN', 'ENDEN', 'UNTER', 'NACHT',
    'NICHT', 'ERDE', 'ENDE', 'REDE', 'RUNE', 'RUNEN',
    'DASS', 'DIES', 'HIER', 'NACH', 'AUCH', 'WEIL', 'DREI',
    'FACH', 'SEID', 'TEIL', 'WORT', 'LAND', 'LANDE', 'HEER',
    'ABER', 'ALLE', 'ALSO', 'NOCH', 'SCHAU', 'GRAB',
    'DEIN', 'DEINE', 'DEINEM', 'DEINEN',
    'WIR', 'UND', 'DIE', 'DER', 'DAS', 'DEM', 'DEN', 'DES',
    'AUS', 'SEE', 'NEU', 'ORT', 'GAR', 'NUN', 'TOT', 'TAG',
    'WAR', 'WAS', 'WER', 'WIE', 'WEG', 'TUN', 'NUR', 'ALT',
    'ICH', 'IHR', 'IHN', 'IHM', 'DIR',
    'GEH', 'HAT', 'HIN', 'IST', 'HIE',
    'VON', 'VOR', 'VOM',
    'ZUM', 'ZUR', 'EIN', 'MIN', 'GEM',
    'ER', 'ES', 'SO', 'DA', 'AN', 'AM', 'IM', 'IN', 'AB', 'ZU',
    'DE', 'EN', 'UM', 'OB', 'NU',
]

# Show main fragment with word boundaries
pos = 0
output_parts = []
while pos < len(main_frag):
    best_match = None
    for word in sorted(known_words, key=len, reverse=True):
        if main_frag[pos:pos+len(word)] == word:
            best_match = word
            break
    if best_match:
        output_parts.append(best_match)
        pos += len(best_match)
    else:
        unrec_start = pos
        pos += 1
        while pos < len(main_frag):
            found = False
            for word in sorted(known_words, key=len, reverse=True):
                if main_frag[pos:pos+len(word)] == word:
                    found = True
                    break
            if found:
                break
            pos += 1
        output_parts.append(f"[{main_frag[unrec_start:pos]}]")

# Print in readable chunks
line = ''
for part in output_parts:
    if len(line) + len(part) + 1 > 75:
        print(f"    {line}")
        line = part
    else:
        if line:
            line += ' ' + part
        else:
            line = part
if line:
    print(f"    {line}")

# ============================================================
# 6. TRANSLATION OF CLEAREST PASSAGES
# ============================================================
print(f"\n\n{'='*80}")
print("6. GERMAN TRANSLATION OF CLEAREST PASSAGES")
print(f"{'='*80}")

passages = [
    ("Book 5, main passage",
     "HIER TAUTRI STEIL AN HEARUCHTIGER SO DASS TUN DIESER EINER SEINE DE TOTNIURG SEE RL AB RRNI WIR UND IE MIN HED DEM I DIE URALTE STEINEN T ER AD THARSC IST SCHAU",
     "Here [tautri=?] steep at Hearuchtiger, so that do this one his [deed] Totniurg Lake [rl] away [rrni] we and [ie] [min-hed-dem] the ancient stones [t] he at Tharsc is - look!"),
    ("Books 1/27, king passage",
     "ENDE UTRUNR DENEN DE REDE R KOENIG LABGZERAS UN EN ITGHNEE AUNRSONGETRASES",
     "End [utrunr] those of the speech of King Labgzeras [un] [en] [itghnee] Aunrsongetrases"),
    ("Book 11, rune-place passage",
     "DE GAR EN RUNEORT ND ER AM NEU DES ND TEII ORT AN DIE MIN HED DEM I DIE URALTE STEINE",
     "Indeed [gar=indeed] at rune-place [nd] he at new of-the [nd-teii] place at the [minheddem] the ancient stones"),
    ("Book 53, full passage",
     "AUS ENDE DUNLN DE FS AN GEVM MIN HIHL DIE NDCE FACH HECHLLT ICH OEL SO DEN HIER TAUTRI STEIL AN HEARUCHTIGER SO DASS TUN DIESER EINER SEINE DE TOTNIURG SEE RL AB",
     "From end [dunln] the [fs] at [gevm] [min] [hihl] the [ndce] fold [hechllt] I [oel] so the here [tautri] steep at Hearuchtiger so that do this one his [deed] Totniurg Lake [rl] away"),
    ("Book 48, after Totniurg",
     "HEARUCHTIGER SO DASS TUN DIESER EINER SEINE DE TOTNIURG S DA U EN NT ER LAUNRL RUNR NACH HECHL",
     "Hearuchtiger so that do this one his [deed] Totniurg [s] there [u-en-nt] he [launrl-runr] after/towards [hechl]"),
    ("Book 18, location passage",
     "HIER SER TI UM EN GEM I ORTEN GAR RUNE DD UNTER LAUS IN HIE",
     "Here [ser-ti] around at gem-i places indeed rune [dd] beneath [laus] in here"),
]

for title, text, translation in passages:
    print(f"\n  {title}:")
    print(f"    German:  {text}")
    print(f"    English: {translation}")

# ============================================================
# 7. CONSISTENT REPEATED PATTERNS (POTENTIAL WORDS)
# ============================================================
print(f"\n\n{'='*80}")
print("7. CONSISTENT CODE SEQUENCES (REPEATED EXACT SAME CODES)")
print(f"{'='*80}")

# Find sequences of 3+ code pairs that repeat across multiple books
# These are likely words
from collections import defaultdict

ngram_books = defaultdict(set)
for i, book in enumerate(books):
    pairs = get_pairs(book)
    for n in range(3, 8):
        for k in range(len(pairs) - n + 1):
            seq = tuple(pairs[k:k+n])
            ngram_books[seq].add(i)

# Filter to sequences appearing in 3+ books
print("\nCode sequences appearing in 3+ books (likely words):")
multi_book = [(seq, books_set) for seq, books_set in ngram_books.items()
              if len(books_set) >= 3]
multi_book.sort(key=lambda x: -len(x[1]))

seen_decoded = set()
for seq, books_set in multi_book[:40]:
    decoded_seq = ''.join(mapping.get(c, '?') for c in seq)
    if decoded_seq in seen_decoded:
        continue
    seen_decoded.add(decoded_seq)
    codes_str = '-'.join(seq)
    print(f"  {decoded_seq:20s} (codes: {codes_str}) in {len(books_set)} books")

# ============================================================
# 8. WHAT COULD MINHEDDEM BE?
# ============================================================
print(f"\n\n{'='*80}")
print("8. MINHEDDEM ANALYSIS (appears ~11 times)")
print(f"{'='*80}")

# MINHEDDEM codes
for i, book in enumerate(books):
    dec = decode_book(book, mapping)
    if 'MINHED' in dec:
        pos = dec.find('MINHED')
        ctx = dec[max(0,pos-5):min(len(dec), pos+20)]
        pairs = get_pairs(book)
        code_ctx = pairs[max(0,pos-2):min(len(pairs), pos+12)]
        print(f"  Book {i}: ...{ctx}...")
        print(f"    Codes: {' '.join(code_ctx)}")

print("\n  Possible readings of MINHEDDEM:")
print("    MIN HED DEM = [min] [hed] the (dative)")
print("    MINHE DDEM = ? ?")
print("    M IN HED DEM = M in [hed] the")
print("    If HED = archaic German 'het' (had/was called): 'MIN HET DEM' = 'to the called/designated'")
print("    If HED = Middle High German 'heit' variant: 'MIN HEIT DEM' = 'greatness of the'")
print("    Codes for HED: check if D might be wrong...")

# Check what codes make up HEDDEM
for i, book in enumerate(books):
    dec = decode_book(book, mapping)
    if 'HEDDEM' in dec:
        pos = dec.find('HEDDEM')
        pairs = get_pairs(book)
        heddem_pairs = pairs[pos:pos+6]
        print(f"  Book {i}: HEDDEM codes = {' '.join(heddem_pairs)}")
        break

# ============================================================
# 9. CODE 69 VERIFICATION (tentatively E)
# ============================================================
print(f"\n\n{'='*80}")
print("9. CODE 69 VERIFICATION")
print(f"{'='*80}")

# Code 69 was tentatively assigned E. Verify.
code69_count = 0
for book in books:
    pairs = get_pairs(book)
    code69_count += pairs.count('69')
print(f"  Code 69 occurs {code69_count} times")

# Test all letters for code 69
for letter in 'EISNRADTHUGOMWCLFBZKVP':
    test_m = dict(mapping)
    test_m['69'] = letter
    total = 0
    for book in books:
        dec = decode_book(book, test_m)
        # Quick coverage
        text = dec.lower()
        for w in sorted(known_words, key=len, reverse=True):
            wl = w.lower()
            text = text.replace(wl, ' ' * len(wl))
        cov = sum(1 for c in text if c == ' ')
        total += cov
    if letter == mapping.get('69', '?'):
        print(f"  69={letter}: {total} (CURRENT)")
    elif total > 0:
        print(f"  69={letter}: {total}")
