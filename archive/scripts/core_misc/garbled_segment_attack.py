#!/usr/bin/env python3
"""
Garbled Segment Attack
========================
With v7 mapping, trace the raw codes of recurring garbled segments
and try to resolve them by testing letter substitutions.

Key garbled segments to attack:
- HECHLLT (appears in FACH/NACH HECHLLT - maybe HOCH/RECHT/etc?)
- NDCE (appears in DIE NDCE - what word?)
- UNENITGH (appears after LABGZERAS)
- LAUNRLRUNR (appears near NACH)
"""

import json, os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)

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

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

code_counts = Counter()
for bpairs in book_pairs:
    code_counts.update(bpairs)

# Decode all books
decoded_books = []
for bpairs in book_pairs:
    text = ''.join(v7.get(p, '?') for p in bpairs)
    decoded_books.append((text, bpairs))

print("=" * 70)
print("GARBLED SEGMENT ANALYSIS WITH V7 MAPPING")
print("=" * 70)

# Find recurring substrings that contain no recognized words
# Look at each decoded book and find segments in [] brackets

# First, let's find the raw codes for known garbled segments
def find_code_sequence(target_text, window=3):
    """Find the raw code sequences producing a given decoded text."""
    results = []
    for bidx, (text, bpairs) in enumerate(decoded_books):
        pos = 0
        while True:
            pos = text.find(target_text, pos)
            if pos == -1:
                break
            codes = bpairs[pos:pos+len(target_text)]
            # Get context
            ctx_start = max(0, pos - window)
            ctx_end = min(len(text), pos + len(target_text) + window)
            ctx = text[ctx_start:ctx_end]
            results.append({
                'book': bidx,
                'pos': pos,
                'codes': codes,
                'context': ctx,
            })
            pos += 1
    return results

# Key garbled segments to investigate
garbled = [
    "HECHLLT",     # appears after NACH/FACH
    "NDCE",        # appears in DIE ___
    "LAUNRLRUNR",  # appears near NACH
    "UNENITGH",    # appears after LABGZERAS
    "RHEIUIRUNN",  # appears with HWND
    "TEHWRIGTN",   # appears before EIN
    "NTEUTTUIG",   # appears in various
    "AUIENNR",     # appears after RUNE
    "GEIGET",      # appears in various
    "EILCHANHEARUCHTIG",  # full phrase
    "EDETOTNIURG",  # proper noun - let's verify codes
    "ADTHARSC",    # proper noun - verify
    "SCHWITEIO",   # proper noun - verify
    "TIUMENGEMI",  # proper noun - verify
]

for target in garbled:
    results = find_code_sequence(target)
    if results:
        print(f"\n{'=' * 50}")
        print(f"'{target}' ({len(results)} occurrences)")
        print(f"{'=' * 50}")

        # Show code sequences
        code_seqs = []
        for r in results[:5]:
            codes_str = ' '.join(r['codes'])
            ctx = r['context']
            print(f"  Book {r['book']:2d} pos {r['pos']:3d}: [{codes_str}]")
            print(f"    context: ...{ctx}...")
            code_seqs.append(tuple(r['codes']))

        # Check if code sequences are consistent
        unique_seqs = set(code_seqs)
        if len(unique_seqs) == 1:
            print(f"  >> CONSISTENT code sequence across all occurrences")
        else:
            print(f"  >> {len(unique_seqs)} different code sequences!")

        # For each position in the garbled segment, show what letter options exist
        if len(results) > 0:
            codes = results[0]['codes']
            print(f"\n  Position analysis:")
            for i, (char, code) in enumerate(zip(target, codes)):
                occ = code_counts.get(code, 0)
                print(f"    pos {i}: '{char}' <- code [{code}] ({occ} total occ, mapped as {v7.get(code, '?')})")

# ============================================================
# SPECIFIC ATTACK: HECHLLT -> what German word?
# ============================================================
print(f"\n{'=' * 70}")
print("ATTACK: HECHLLT -> ? (appears after NACH/FACH)")
print(f"{'=' * 70}")

# Context: "NACH HECHLLT" or "FACH HECHLLT"
# Could be: HOCH_LT? RECHT? SCHLECHT?
# Let's look at the codes
results = find_code_sequence("HECHLLT")
if results:
    codes_seq = results[0]['codes']
    print(f"  Codes: {' '.join(codes_seq)}")
    print(f"  Letters: {' '.join(v7.get(c, '?') for c in codes_seq)}")

    # The issue: which codes might be wrong?
    # H E C H L L T
    # If we look at "NACH HECHLL T", the T at end might be part of next word
    # Or "NACH_HECHLLT" could be a compound

    # Let's check what appears BEFORE and AFTER this segment
    for r in results[:5]:
        text = decoded_books[r['book']][0]
        ctx_start = max(0, r['pos'] - 15)
        ctx_end = min(len(text), r['pos'] + len("HECHLLT") + 15)
        print(f"  Book {r['book']:2d}: ...{text[ctx_start:ctx_end]}...")

# ============================================================
# SPECIFIC ATTACK: Try to resolve NDCE
# ============================================================
print(f"\n{'=' * 70}")
print("ATTACK: NDCE -> ? (appears in 'DIE NDCE')")
print(f"{'=' * 70}")

results = find_code_sequence("NDCE")
if results:
    codes_seq = results[0]['codes']
    print(f"  Codes: {' '.join(codes_seq)}")

    for r in results[:5]:
        text = decoded_books[r['book']][0]
        ctx_start = max(0, r['pos'] - 15)
        ctx_end = min(len(text), r['pos'] + len("NDCE") + 15)
        print(f"  Book {r['book']:2d}: ...{text[ctx_start:ctx_end]}...")

# ============================================================
# ATTACK: Look at AUNRSONGETRASES codes to check for anagram
# ============================================================
print(f"\n{'=' * 70}")
print("PROPER NOUN VERIFICATION")
print(f"{'=' * 70}")

proper_nouns = [
    "AUNRSONGETRASES",
    "LABGZERAS",
    "TIUMENGEMI",
    "SCHWITEIONE",
    "EDETOTNIURG",
    "EILCH",
    "HEARUCHTIG",
    "ADTHARSC",
    "TAUTR",
    "HEDEMI",
    "TOTNIURG",
    "UTRUNR",
    "HIHL",
]

for noun in proper_nouns:
    results = find_code_sequence(noun)
    if results:
        codes_seq = results[0]['codes']
        print(f"\n  {noun} ({len(results)}x): [{' '.join(codes_seq)}]")
        # Show sorted letters for anagram analysis
        sorted_letters = ''.join(sorted(noun))
        print(f"    Sorted: {sorted_letters}")

# ============================================================
# NEW ANAGRAM ATTACK on previously unknown proper nouns
# ============================================================
print(f"\n{'=' * 70}")
print("NEW ANAGRAM ANALYSIS")
print(f"{'=' * 70}")

def find_anagram_matches(word, dict_words, max_diff=1):
    """Find dictionary words that are anagrams or near-anagrams."""
    word_sorted = sorted(word.lower())
    matches = []
    for dw in dict_words:
        dw_sorted = sorted(dw.lower())
        # Check if one is a sub-multiset of the other + up to max_diff extras
        from collections import Counter as C
        wc = C(word.lower())
        dc = C(dw.lower())
        # Symmetric difference
        all_letters = set(wc.keys()) | set(dc.keys())
        diff = sum(abs(wc.get(l, 0) - dc.get(l, 0)) for l in all_letters)
        if diff <= max_diff * 2 and len(dw) >= len(word) - max_diff:
            matches.append((dw, diff // 2))
    return matches

# German words/names to test against
geo_names = [
    'REGENSBURG', 'SALZBURG', 'NUERNBERG', 'HEIDELBERG', 'FREIBURG',
    'AUGSBURG', 'WUERZBURG', 'BAMBERG', 'PASSAU', 'INGOLSTADT',
    'KELHEIM', 'LANDSHUT', 'STRAUBING', 'DEGGENDORF', 'CHAM',
    'AMBERG', 'WEIDEN', 'SCHWANDORF', 'TIRSCHENREUTH',
    'BERLIN', 'MUENCHEN', 'HAMBURG', 'KOELN', 'FRANKFURT',
    'STUTTGART', 'DUESSELDORF', 'DORTMUND', 'ESSEN', 'BREMEN',
    'DRESDEN', 'LEIPZIG', 'HANNOVER', 'KASSEL', 'ERFURT',
    'ROSTOCK', 'LUEBECK', 'MAGDEBURG', 'BRAUNSCHWEIG',
    'AACHEN', 'TRIER', 'MAINZ', 'WORMS', 'SPEYER',
    'WEICHSTEIN', 'SALZBERG', 'BACHSTADT', 'DRACHSTADT',
]

# German common words that could be anagrams
german_words = [
    'SONNENAUFGANG', 'SONNENUNTERGANG', 'MORGENSTERN',
    'ABENDSTERN', 'SONNENGOTT', 'ERDGEIST', 'BERGGEIST',
    'STEINMETZ', 'GOLDSCHMIED', 'WAFFENSCHMIED',
    'RUNENMEISTER', 'GRABSTAETTE', 'TOTENSTILLE',
    'GEISTERSTADT', 'NEBELREICH', 'SCHATTENREICH',
    'UNTERWELT', 'DRACHENHORT', 'KOENIGREICH',
    'RITTERTUM', 'PRIESTERTUM', 'ZAUBERSPRUCH',
    'STERNENLICHT', 'MONDLICHT', 'SONNENLICHT',
    'SCHWARZERTURM', 'STEINTURM', 'RUNDTURM',
    'BURGHERR', 'BURGFRAULEIN', 'RITTERSCHLAG',
    'KOENIGSTHRON', 'DRACHENTOD', 'HELDENTAT',
    'GOTTESGERICHT', 'TOTENGERICHT', 'SEELENGERICHT',
    'GRABESRUHE', 'TODESRUHE', 'EWIGERSCHLAF',
]

for noun in ['AUNRSONGETRASES', 'EDETOTNIURG', 'TIUMENGEMI',
             'UTRUNR', 'HIHL', 'EILCH', 'ENGCHD', 'KELSEI',
             'GEVMT', 'LABRNI', 'HEDEMI', 'TAUTR']:
    matches = find_anagram_matches(noun, geo_names + german_words, max_diff=1)
    if matches:
        print(f"\n  {noun}:")
        for match, diff in sorted(matches, key=lambda x: x[1]):
            print(f"    -> {match} (diff={diff})")

# ============================================================
# FOCUS: AUNRSONGETRASES (15 chars, recurring)
# ============================================================
print(f"\n{'=' * 70}")
print("DEEP ANALYSIS: AUNRSONGETRASES")
print(f"{'=' * 70}")

results = find_code_sequence("AUNRSONGETRASES")
if results:
    codes = results[0]['codes']
    print(f"  Codes: {' '.join(codes)}")
    print(f"  Letters: {' '.join(v7.get(c, '?') for c in codes)}")
    print(f"  Sorted letters: {''.join(sorted('AUNRSONGETRASES'))}")
    print(f"  Letter counts: {dict(Counter('AUNRSONGETRASES'))}")

    # This is 15 chars. Could it be a compound?
    # AUNR + SONGETRASES?
    # AUNRS + ONGETRASES?
    # Let's look for sub-anagrams
    text = 'AUNRSONGETRASES'
    for split in range(3, len(text)-2):
        part1 = text[:split]
        part2 = text[split:]
        # Check part1 and part2 against short German words
        for gw in ['RUNE', 'RUNEN', 'STEIN', 'STEINE', 'STERN', 'STERNE',
                    'UNTER', 'ORTEN', 'OSTEN', 'NORDEN', 'SORGE', 'SORGEN',
                    'GARTEN', 'STRASSE', 'GRENZE', 'SONNEN', 'REGEN',
                    'GEGEN', 'SAGEN', 'TRAGEN', 'GRABEN', 'RATSEN',
                    'SONNT', 'RASEN', 'ROSEN', 'NASE', 'NASEN',
                    'STRANG', 'GESANG', 'ORANGE', 'ORGANE', 'ORGAN']:
            s1 = sorted(part1.lower())
            s2 = sorted(gw.lower())
            if s1 == s2:
                print(f"    Split at {split}: '{part1}' = anagram of '{gw}' | '{part2}'")
            s1 = sorted(part2.lower())
            if s1 == s2:
                print(f"    Split at {split}: '{part1}' | '{part2}' = anagram of '{gw}'")

    # Full anagram: 15 letters A,A,E,E,G,N,N,O,R,R,S,S,S,T,U
    # That's a LOT of S's (3). Could be: SONNENAUFGANGS? No, wrong letters.
    # STRASSENGRUNO? No.
    # Let's try: AUSGANGSTORNES? SONNENSTRAUGE?
    # GRATSONUNESSES?
    # Let's think: STRASSEN + ORGAN = STRASSENORGAN? Close but wrong letters.
    # AUGE + RSTSONNESS? No.
    # What about UNTERGANGSROSE? ROSENUNTERGANS?
    # Letters: A A E E G N N O R R S S S T U
    # SONNENUTERGARSS? UNTERGANGSROSES?
    # UNTERGANGS = U,N,T,E,R,G,A,N,G,S (10 letters, but we only have 1 G!)
    # Hmm... SONNENSTRASSE = S,O,N,N,E,N,S,T,R,A,S,S,E (13 letters, 3N but we have 2N)
    # Wait: SONNENSTRASSGE? No, too many letters.
    # RUNENSTRASSES? R,U,N,E,N,S,T,R,A,S,S,E,S (13 letters)
    # Our letters: A,A,E,E,G,N,N,O,R,R,S,S,S,T,U (15 letters)
    # So: RUNENSTRASSES + leftover O,A,G,R = RUNENSTRASSES + OAGR?
    # Or: GENOSSENSTRASSE? No, wrong letters.
    # Interesting: ORANGENESTERNS? Close but not right.

    # CipSoft pattern: exact anagram + 1 extra letter
    # So it should be 14 chars + 1 extra
    # 14-char German words/compounds are rare but possible

    # Actually, could it be two words?
    print(f"\n  Testing two-word splits:")
    letters = sorted('AUNRSONGETRASES'.lower())
    for gw1 in ['runen', 'stein', 'steine', 'strasse', 'stern', 'sterne',
                 'sorge', 'sorgen', 'garten', 'regen', 'segen', 'gegen',
                 'osten', 'norden', 'westen', 'sueden', 'grotte', 'turm',
                 'toren', 'tor', 'rose', 'rosen', 'natur', 'organ',
                 'grossen', 'strassen', 'sonne', 'sonnen']:
        remaining = list(letters)
        valid = True
        for c in gw1:
            if c in remaining:
                remaining.remove(c)
            else:
                valid = False
                break
        if valid:
            rem_str = ''.join(sorted(remaining))
            # Check if remaining matches a word
            for gw2 in ['strasse', 'strassen', 'garten', 'rosen', 'stern',
                        'stein', 'steine', 'organ', 'grotte', 'segen',
                        'sorgen', 'torsen', 'turm', 'essen', 'regen',
                        'sonne', 'osten', 'natur', 'nase', 'rasen',
                        'sorge', 'trage', 'trages', 'sager', 'arsen',
                        'orange', 'gestorben', 'ertragen']:
                if sorted(gw2) == sorted(rem_str) or sorted(gw2) == sorted(remaining[:-1]):
                    extra = ''
                    if len(remaining) > len(gw2):
                        extra_letters = list(remaining)
                        for c in gw2:
                            extra_letters.remove(c)
                        extra = f" +{''.join(extra_letters)}"
                    print(f"    {gw1.upper()} + {gw2.upper()}{extra}")
