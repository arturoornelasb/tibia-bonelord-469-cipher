"""
Investigate anomalous patterns: IIIWII, proper noun structures,
I-code inflation, and potential secondary cipher layer.
"""
import json
import os
from collections import Counter

data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

# Full mapping
mapping = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U', '00': 'H', '14': 'N', '72': 'R',
    '91': 'S', '15': 'I', '76': 'E', '52': 'S', '42': 'D',
    '46': 'I', '48': 'N', '57': 'H', '04': 'M', '12': 'S',
    '58': 'N', '78': 'T', '51': 'R', '35': 'A', '34': 'L',
    '01': 'E', '59': 'S', '41': 'E', '30': 'E', '94': 'H',
    '47': 'D', '13': 'N', '71': 'I', '63': 'D', '93': 'N',
    '28': 'D', '86': 'E', '43': 'U', '70': 'U', '65': 'I',
    '16': 'I', '36': 'W', '64': 'T', '89': 'A', '80': 'G',
    '97': 'G', '75': 'T', '08': 'R', '20': 'F', '96': 'L',
    '99': 'O', '55': 'R', '67': 'E', '27': 'E', '03': 'E',
    '09': 'E', '05': 'S', '53': 'N', '44': 'U', '62': 'B',
    '68': 'R', '23': 'S', '17': 'E', '29': 'E', '66': 'A',
    '49': 'E', '38': 'K', '77': 'Z', '22': 'K', '82': 'O',
    '73': 'N', '50': 'I', '84': 'G', '25': 'O', '83': 'V',
    '81': 'T', '24': 'I', '79': 'O', '10': 'R', '54': 'M',
    '98': 'T', '39': 'E', '87': 'W',
    '74': 'E', '37': 'E', '40': 'M', '02': 'D', '69': 'E',
}

i_codes = ['21', '15', '46', '71', '65', '16', '50', '24']

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

def decode_book_raw(book):
    """Decode keeping code pairs visible."""
    offset = get_offset(book)
    pairs = [book[j:j+2] for j in range(offset, len(book)-1, 2)]
    return pairs

def decode_book(book):
    offset = get_offset(book)
    pairs = [book[j:j+2] for j in range(offset, len(book)-1, 2)]
    return ''.join(mapping.get(p, '?') for p in pairs)

# ============================================================
# 1. IIIWII PATTERN
# ============================================================
print("=" * 80)
print("1. IIIWII PATTERN ANALYSIS")
print("=" * 80)

for i, book in enumerate(books):
    dec = decode_book(book)
    if 'IIIWII' in dec:
        pos = dec.find('IIIWII')
        ctx = dec[max(0, pos-10):pos+20]

        # Get the raw code pairs at this position
        pairs = decode_book_raw(book)
        offset = get_offset(book)
        # Find which pairs produce the IIIWII
        pair_start = pos  # Each pair produces one char
        relevant_pairs = pairs[max(0, pos-5):pos+12]

        print(f"\n  Book {i}: ...{ctx}...")
        print(f"    Code pairs: {' '.join(relevant_pairs)}")
        print(f"    Letters:    {' '.join(mapping.get(p, '?') for p in relevant_pairs)}")

# Find ALL sequences of 3+ consecutive I's
print("\n\n--- All III+ sequences ---")
for i, book in enumerate(books):
    dec = decode_book(book)
    j = 0
    while j < len(dec):
        if dec[j] == 'I':
            run_start = j
            while j < len(dec) and dec[j] == 'I':
                j += 1
            run_len = j - run_start
            if run_len >= 3:
                ctx = dec[max(0, run_start-5):j+5]
                pairs = decode_book_raw(book)
                i_pairs = pairs[run_start:j]
                print(f"  Book {i}: {'I'*run_len} at pos {run_start} — ...{ctx}... — codes: {' '.join(i_pairs)}")
        else:
            j += 1

# ============================================================
# 2. I-CODE DISTRIBUTION
# ============================================================
print(f"\n\n{'='*80}")
print("2. I-CODE FREQUENCY ANALYSIS")
print(f"{'='*80}")

# Count how often each I-code appears
i_code_counts = Counter()
for book in books:
    pairs = decode_book_raw(book)
    for p in pairs:
        if p in i_codes:
            i_code_counts[p] += 1

print("\nI-code frequencies:")
for code, count in sorted(i_code_counts.items(), key=lambda x: -x[1]):
    print(f"  Code {code}: {count} times")

print(f"\nTotal I occurrences: {sum(i_code_counts.values())}")
print(f"Expected (7.5% of ~5600): ~420")
print(f"Excess I's: {sum(i_code_counts.values()) - 420}")

# Check which I-codes appear in the IIIWII pattern
print("\nI-codes in IIIWII sections:")
for i, book in enumerate(books):
    dec = decode_book(book)
    if 'IIIWII' in dec:
        pos = dec.find('IIIWII')
        pairs = decode_book_raw(book)
        iii_pairs = pairs[pos:pos+3]
        wii_pairs = pairs[pos+4:pos+6]
        print(f"  Book {i}: III = {iii_pairs}, W = {pairs[pos+3]}, II = {wii_pairs}")

# ============================================================
# 3. UNRECOGNIZED SEGMENTS ANALYSIS
# ============================================================
print(f"\n\n{'='*80}")
print("3. MOST COMMON UNRECOGNIZED SEGMENTS")
print(f"{'='*80}")

# Extract unrecognized segments from all books
WORDS = set("""
a ab aber alle allem allen aller alles als also alt alte altem alten alter altes am an andere
ans auch auf aus bei beim bis da dabei damit dann das dass dem den denen denn
der deren des dessen die dies diese diesem diesen dieser dieses dir doch dort durch
ein eine einem einen einer einige einst em en ende er erde erst erste es etwas
fach fand finden fuer ganz gar geh geheim gehen gegen gibt ging gross gut
hab habe haben hat her hier hin ich ihm ihn ihr ihre ihrem ihren ihrer im in ins ist
ja jede jeden jeder jedes klar koenig koenige koenigen koenigs kommen kam
lang lage nach nacht neu neue neuen nicht nichts noch nun nur ob oder ohne ort orte orten
rede reden ruin rune runen runeort see sehr sei seid sein seine seinem seinen seiner seit
sie sind so soll steil stein steine steinen teil teile teilen tun
ueber um und uns unter uralte uralten viel vom von vor wahr war was wasser weg weil
wir wird wissen wo wohl wort zeichen zeit zu zum zur zwei zwischen
schwiteio tharsc totniurg hearuchtiger aunrsongetrases labgzeras labge
finden dass dieser dieses fach nach aus dass tun ab des geh erde enden nu
min gem steil heer koenigs tag tage nacht orte orten erste schau
""".split())

segment_counts = Counter()
for i, book in enumerate(books):
    dec = decode_book(book)
    # Simple word removal to find unrecognized parts
    remaining = dec.lower()
    for length in range(max(len(w) for w in WORDS), 1, -1):
        for word in WORDS:
            if len(word) == length:
                remaining = remaining.replace(word, ' ' * len(word))

    # Extract remaining segments
    current = ''
    for ch in remaining:
        if ch != ' ':
            current += ch
        else:
            if len(current) >= 3:
                segment_counts[current.upper()] += 1
            current = ''
    if len(current) >= 3:
        segment_counts[current.upper()] += 1

print("\nMost common unrecognized segments (3+ chars):")
for seg, count in segment_counts.most_common(30):
    print(f"  {seg}: {count}x")

# ============================================================
# 4. PROPER NOUN REVERSE ANALYSIS
# ============================================================
print(f"\n\n{'='*80}")
print("4. PROPER NOUN ANAGRAM/REVERSE CHECK")
print(f"{'='*80}")

# Check if proper nouns are anagrammed German words
import itertools

def check_anagrams(word, max_len=8):
    """Check if the letters can form German words."""
    letters = sorted(word.lower())
    results = []
    # Check subsets
    for length in range(3, min(len(word)+1, max_len+1)):
        for combo in set(itertools.combinations(letters, length)):
            test = ''.join(combo)
            if test in WORDS:
                results.append(test.upper())
    return list(set(results))

nouns = ['TOTNIURG', 'SCHWITEIO', 'THARSC', 'LABGZERAS', 'AUNRSONGETRASES']

for noun in nouns:
    rev = noun[::-1]
    print(f"\n  {noun}:")
    print(f"    Reversed: {rev}")

    # Check substrings of reversed form
    for length in range(3, len(rev) + 1):
        for start in range(len(rev) - length + 1):
            sub = rev[start:start + length].lower()
            if sub in WORDS:
                print(f"    Reversed contains: '{sub.upper()}' (pos {start}-{start+length})")

    # Check contained words (forward)
    for length in range(3, len(noun) + 1):
        for start in range(len(noun) - length + 1):
            sub = noun[start:start + length].lower()
            if sub in WORDS:
                print(f"    Forward contains: '{sub.upper()}' (pos {start}-{start+length})")

# ============================================================
# 5. SPECIFIC SEQUENCE: EILABRRNI
# ============================================================
print(f"\n\n{'='*80}")
print("5. EILABRRNI PATTERN (after TOTNIURG)")
print(f"{'='*80}")

# This sequence appears multiple times after TOTNIURG
for i, book in enumerate(books):
    dec = decode_book(book)
    if 'EILAB' in dec:
        pos = dec.find('EILAB')
        ctx = dec[max(0, pos-15):pos+20]
        pairs = decode_book_raw(book)
        relevant = pairs[max(0, pos-5):pos+15]
        print(f"  Book {i}: ...{ctx}...")
        print(f"    Pairs: {' '.join(relevant)}")

# Check if EILABRRNI reversed = INRRBALIE
print(f"\n  EILABRRNI reversed: {'EILABRRNI'[::-1]}")
print(f"  ILABRR reversed: {'ILABRR'[::-1]}")
# Check LABR — could this be related to LABYRINTH?
print(f"  LABR... LABYRINTH?")
print(f"  ILAB reversed: {'ILAB'[::-1]}")
print(f"  BALI?")

# ============================================================
# 6. CODE 33 - THE MISSED ONE
# ============================================================
print(f"\n\n{'='*80}")
print("6. CODE 33 (1 occurrence, UNMAPPED)")
print(f"{'='*80}")

for i, book in enumerate(books):
    pairs = decode_book_raw(book)
    if '33' in pairs:
        pos = pairs.index('33')
        ctx_pairs = pairs[max(0, pos-8):pos+9]
        ctx_decoded = ''.join(mapping.get(p, f'[{p}]') for p in ctx_pairs)
        print(f"  Book {i}: position {pos}")
        print(f"    Pairs: {' '.join(ctx_pairs)}")
        print(f"    Decoded: {ctx_decoded}")

        # Try each letter
        for letter in 'ENSIRDATHUGOKMWCLFBZVPJQXY':
            test = ctx_decoded.replace('[33]', letter)
            print(f"    33={letter}: {test}")

# ============================================================
# 7. FULL NARRATIVE ATTEMPT — MANUAL SENTENCE PARSING
# ============================================================
print(f"\n\n{'='*80}")
print("7. FULL NARRATIVE — MANUAL SENTENCE PARSING")
print(f"{'='*80}")

# Get the most informative books (those with highest coverage)
best_books = []
for i, book in enumerate(books):
    dec = decode_book(book)
    # Count recognized words
    text = dec.lower()
    word_count = 0
    for word in sorted(WORDS, key=len, reverse=True):
        while word in text:
            word_count += 1
            text = text.replace(word, ' ' * len(word), 1)
    best_books.append((i, dec, word_count))

best_books.sort(key=lambda x: -x[2])

print("\nNarrative from top 10 most readable books:\n")
seen_passages = set()
for i, dec, wc in best_books[:15]:
    # Extract the readable portions
    if dec[:30] not in seen_passages:
        print(f"  Book {i} ({len(dec)} chars, {wc} words):")
        print(f"    {dec}")
        print()
        seen_passages.add(dec[:30])
