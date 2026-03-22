"""
Investigate:
1. C overrepresentation (7.29x in unrecognized segments)
2. ENDE frequency (26 times in 3185 chars — unusually high?)
3. Whether reassigning C codes to other letters improves coverage
"""
import json
from collections import Counter

with open('books.json', 'r') as f:
    books = json.load(f)

all_codes = {
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
    '09': 'E', '05': 'C', '53': 'N', '44': 'U', '62': 'B',
    '68': 'R', '23': 'S', '17': 'E', '29': 'E', '66': 'A',
    '49': 'E', '38': 'K', '77': 'Z', '22': 'K', '82': 'O',
    '73': 'N', '50': 'I', '84': 'G', '25': 'O', '83': 'V',
    '81': 'T', '24': 'I', '79': 'O', '10': 'R', '54': 'M',
    '98': 'T', '39': 'E', '87': 'W',
}

def decode(digit_string, code_map=None):
    if code_map is None:
        code_map = all_codes
    result = []
    for i in range(0, len(digit_string), 2):
        code = digit_string[i:i+2]
        if code in code_map:
            result.append(code_map[code])
        else:
            result.append('?')
    return ''.join(result)

def get_codes(digit_string):
    codes = []
    for i in range(0, len(digit_string), 2):
        codes.append(digit_string[i:i+2])
    return codes

# Build superstring from raw digits (simplified — just concatenate unique books)
# For context analysis, decode all books individually
decoded_books = [decode(b) for b in books]
full_text = ''.join(decoded_books)

print("=== PART 1: C CODE ANALYSIS ===\n")

# C codes are 05 and 18
c_codes = ['05', '18']
print("C is encoded by codes: 05 and 18\n")

# Count occurrences of each C code
c05_count = 0
c18_count = 0
for b in books:
    codes = get_codes(b)
    c05_count += codes.count('05')
    c18_count += codes.count('18')

print(f"Code 05 (C): {c05_count} occurrences")
print(f"Code 18 (C): {c18_count} occurrences")
print(f"Total C:     {c05_count + c18_count} occurrences")

# For each C occurrence, show its context (3 codes before/after)
print("\n--- All C occurrences with context ---")
for book_idx, b in enumerate(books):
    codes = get_codes(b)
    decoded = decode(b)
    for pos, code in enumerate(codes):
        if code in c_codes:
            # Get context window
            start = max(0, pos - 4)
            end = min(len(codes), pos + 5)
            context_codes = codes[start:end]
            context_decoded = decoded[start:end]

            # Mark the C position
            marker = ' ' * (pos - start) + '^'

            # What comes before and after C?
            before = decoded[pos-1] if pos > 0 else '-'
            after = decoded[pos+1] if pos+1 < len(decoded) else '-'
            bigram_before = before + 'C'
            bigram_after = 'C' + after

            print(f"  Bk{book_idx:2d} pos{pos:3d}: ...{context_decoded}... "
                  f"(code {code}) [{bigram_before}|{bigram_after}]")

# Count bigrams involving C
print("\n--- C bigrams ---")
c_bigrams_before = Counter()
c_bigrams_after = Counter()
c_trigrams = Counter()

for b in books:
    decoded = decode(b)
    for i, ch in enumerate(decoded):
        if ch == 'C':
            if i > 0:
                c_bigrams_before[decoded[i-1] + 'C'] += 1
            if i < len(decoded) - 1:
                c_bigrams_after['C' + decoded[i+1]] += 1
            if i > 0 and i < len(decoded) - 1:
                c_trigrams[decoded[i-1] + 'C' + decoded[i+1]] += 1

print("\nBigrams ending in C:")
for bigram, count in c_bigrams_before.most_common():
    print(f"  {bigram}: {count}")

print("\nBigrams starting with C:")
for bigram, count in c_bigrams_after.most_common():
    print(f"  {bigram}: {count}")

print("\nTrigrams with C in center:")
for trigram, count in c_trigrams.most_common():
    german_note = ""
    if trigram in ('SCH', 'ACH', 'ICH', 'OCH', 'UCH', 'ECH'):
        german_note = " <-- valid German"
    elif trigram in ('SCE', 'SCA', 'SCO', 'SCI'):
        german_note = " <-- NOT German (SC_ without H)"
    elif trigram in ('CHA', 'CHE', 'CHI', 'CHO', 'CHU', 'CHT', 'CHS', 'CHR', 'CHL', 'CHN', 'CHW'):
        german_note = " <-- valid German CH_"
    elif trigram.startswith('CK'):
        german_note = " <-- valid German CK"
    elif trigram.startswith('CO') or trigram.startswith('CE') or trigram.startswith('CA') or trigram.startswith('CI'):
        german_note = " <-- Latin/foreign C_ (not native German)"
    print(f"  {trigram}: {count}{german_note}")


print("\n\n=== PART 2: TEST C REASSIGNMENT ===\n")

# What if code 05 or 18 is NOT C but something else?
# Test all 26 letters for each C code

german_words = set()
basic = [
    'DER','DIE','DAS','EIN','EINE','UND','IN','IST','ES','ICH','DU','ER','SIE','WIR',
    'IHR','NICHT','AUCH','AUF','AN','MIT','AUS','VON','ZU','BEI','NACH','HIER','DA',
    'NOCH','NUR','ABER','WAS','WER','WIE','SO','DOCH','KEIN','KEINE','MEIN','DEIN',
    'SEIN','SEINE','DIESER','DIESE','JEDER','JEDE','ALLE','ODER','WENN','DASS',
    'WEIL','DENN','OB','ALS','BIS','FUER','UEBER','UNTER','NEBEN','VOR','HINTER',
    'ZWISCHEN','DURCH','OHNE','GEGEN','SCHON','SEHR','MEHR','AM','IM','ZUM','ZUR',
    'DEN','DEM','DES','EINEN','EINEM','EINES','HABEN','SEIN','WERDEN','KOENNEN',
    'MACHEN','GEHEN','KOMMEN','SEHEN','STEHEN','FINDEN','GEBEN','NEHMEN',
    'LASSEN','HALTEN','SAGEN','SPRECHEN','BRINGEN','LESEN','SCHREIBEN',
    'HEISSEN','KENNEN','DENKEN','WISSEN','LEBEN','LIEGEN','BLEIBEN',
    'RUFEN','SETZEN','STELLEN','TRAGEN','ZIEHEN','SCHLAGEN','FALLEN',
    'LAUFEN','FAHREN','ESSEN','TRINKEN','SCHLAFEN','STERBEN','BEGINNEN',
    'FANGEN','KOENIG','RUNE','RUNEN','STEIN','STEINE','STEINEN',
    'URALTE','URALTEN','URALTER','ENDE','ENDEN','ENDLICH',
    'ORT','REDE','REDEN','TEIL','TEILE','TEILEN',
    'FACH','STEIL','TUN','TAG','NACHT','WELT','ZEIT',
    'FEUER','WASSER','ERDE','LUFT','LICHT','DUNKEL',
    'KRIEG','KAMPF','SCHWERT','SCHILD','MAGIE','ZAUBER',
    'GEIST','SEELE','TOD','LEBEN','MACHT','KRAFT',
    'GOLD','SILBER','EISEN','STAHL','SCHAUN','SCHAUEN',
    'AB','EI','RE','GE','SE','EN','NE','ER','ES',
    'MINH','TOTNIURG','HEARUCHTIGER','LABGZERAS','THARSC',
    'DIES','DIESER','DIESES','DIESEM','STEH','STEHEN',
    'NIMM','IMMER','OBEN','UNTEN','RECHTS','LINKS',
    'EHRE','RUHM','TREUE','MUT','BEIN','HERZ','AUGE','HAND',
    'STEIN','MAUER','TOR','WEG','ZEICHEN','SCHRIFT','WORT',
    'HEILIG','HEILIGE','GEHEIM','RITUAL','OPFER','ALTAR',
    'FLUCH','SEGEN','BANN','PORTAL','EINGANG',
    'NORDEN','SUEDEN','OSTEN','WESTEN',
    'ERSTER','ERSTE','ERSTEN','ZWEITE','DRITTE',
    'HUNDERT','TAUSEND',
    'REISE','REISEN','STUNDE','STUNDEN','DIENST',
    'MEINEN','MEINER','SEINER','SEINES',
    'UNSERE','UNSEREN',
    'AUCH','WEG','GANZ','GROSS','KLEIN',
    'NACH','NOCH','DOCH','SCHON',
    'RECHT','SCHLECHT','STARK','SCHWACH',
    'TIEF','HOCH','LANG','KURZ',
    'FREUND','FEIND','BRUDER','VATER','MUTTER',
    'SONNE','MOND','STERN','BLUT',
]
for w in basic:
    german_words.add(w)

def count_word_hits(text, wordset, min_len=2):
    hits = 0
    for wlen in range(min_len, min(len(text), 20) + 1):
        for start in range(len(text) - wlen + 1):
            word = text[start:start+wlen]
            if word in wordset:
                hits += 1
    return hits

# Test: what if code 05 is letter X instead of C?
print("Testing code 05 (currently C) as each letter:")
base_hits = count_word_hits(full_text, german_words)
print(f"  Baseline (C): {base_hits} word hits\n")

results_05 = []
for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    test_codes = dict(all_codes)
    test_codes['05'] = letter
    test_text = ''.join(decode(b, test_codes) for b in books)
    hits = count_word_hits(test_text, german_words)
    delta = hits - base_hits
    results_05.append((letter, hits, delta))
    if abs(delta) > 2:
        print(f"  05={letter}: {hits} hits (delta {delta:+d})")

print("\nTesting code 18 (currently C) as each letter:")
results_18 = []
for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    test_codes = dict(all_codes)
    test_codes['18'] = letter
    test_text = ''.join(decode(b, test_codes) for b in books)
    hits = count_word_hits(test_text, german_words)
    delta = hits - base_hits
    results_18.append((letter, hits, delta))
    if abs(delta) > 2:
        print(f"  18={letter}: {hits} hits (delta {delta:+d})")

# Best alternatives
print("\nBest alternatives for code 05:")
for letter, hits, delta in sorted(results_05, key=lambda x: -x[1])[:5]:
    print(f"  {letter}: {hits} ({delta:+d})")

print("\nBest alternatives for code 18:")
for letter, hits, delta in sorted(results_18, key=lambda x: -x[1])[:5]:
    print(f"  {letter}: {hits} ({delta:+d})")


print("\n\n=== PART 3: ENDE INVESTIGATION ===\n")

# Find all ENDE occurrences and their contexts
print("All ENDE occurrences in decoded text:\n")
ende_contexts = []
for book_idx, b in enumerate(books):
    decoded = decode(b)
    pos = 0
    while True:
        pos = decoded.find('ENDE', pos)
        if pos < 0:
            break
        # Get context (10 chars before/after)
        start = max(0, pos - 10)
        end = min(len(decoded), pos + 14)
        context = decoded[start:end]
        # Mark ENDE position
        marker_start = pos - start
        marked = context[:marker_start] + '[' + context[marker_start:marker_start+4] + ']' + context[marker_start+4:]

        # What are the raw codes for this ENDE?
        code_start = pos * 2
        ende_raw = b[code_start:code_start+8]  # 4 codes = 8 digits

        ende_contexts.append((book_idx, pos, marked, ende_raw))
        pos += 1

print(f"Total ENDE occurrences: {len(ende_contexts)}\n")

# Group by what comes before/after
before_ende = Counter()
after_ende = Counter()
for book_idx, pos, ctx, raw in ende_contexts:
    decoded = decode(books[book_idx])
    if pos > 0:
        before_ende[decoded[pos-1]] += 1
    if pos + 4 < len(decoded):
        after_ende[decoded[pos+4]] += 1
    print(f"  Bk{book_idx:2d} pos{pos:3d}: {ctx}  raw={raw}")

print(f"\nLetter before ENDE: {dict(before_ende.most_common())}")
print(f"Letter after ENDE:  {dict(after_ende.most_common())}")

# Check: is ENDE always the word "Ende" or part of longer words?
print("\nENDE as part of longer sequences:")
for book_idx, pos, ctx, raw in ende_contexts:
    decoded = decode(books[book_idx])
    # Try to identify if it's a standalone word or part of compound
    before = decoded[max(0,pos-5):pos]
    after = decoded[pos+4:min(len(decoded),pos+9)]

    # Check common patterns
    full = before + 'ENDE' + after
    patterns = []
    if pos >= 1 and decoded[pos-1:pos+4] == 'SENDE':
        patterns.append('SENDE (sending?)')
    if pos >= 2 and decoded[pos-2:pos+4] == 'ENDEN':
        patterns.append('ENDEN (ends)')
    if pos + 4 < len(decoded) and decoded[pos:pos+5] in ('ENDEN', 'ENDER', 'ENDES'):
        patterns.append(decoded[pos:pos+5])
    if pos >= 1 and decoded[pos-1:pos+4] == 'WENDE':
        patterns.append('WENDE (turn)')
    if pos >= 2 and decoded[pos-2:pos+4] in ('BLENDE', 'SPENDE'):
        patterns.append(decoded[pos-2:pos+4])
    if pos + 5 <= len(decoded) and decoded[pos:pos+6] == 'ENDERE':
        patterns.append('ENDERE (other?)')

    if patterns:
        print(f"  Bk{book_idx:2d} pos{pos:3d}: {', '.join(patterns)} in context: {ctx}")

# Check if ENDE is always encoded the same way
print("\nENDE raw code patterns:")
ende_raw_patterns = Counter()
for _, _, _, raw in ende_contexts:
    # raw is 8 digits = 4 codes
    codes = [raw[i:i+2] for i in range(0, 8, 2)]
    pattern = '-'.join(codes)
    ende_raw_patterns[pattern] += 1

for pattern, count in ende_raw_patterns.most_common():
    codes = pattern.split('-')
    decoded = ''.join(all_codes.get(c, '?') for c in codes)
    print(f"  {pattern} -> {decoded}: {count}x")


print("\n\n=== PART 4: SCHWI/SCHWITEIO INVESTIGATION ===\n")

# I noticed SCHWITEIO appears multiple times. Let's investigate.
for book_idx, b in enumerate(books):
    decoded = decode(b)
    if 'SCHWI' in decoded:
        pos = decoded.find('SCHWI')
        start = max(0, pos - 10)
        end = min(len(decoded), pos + 20)
        context = decoded[start:end]

        # Get raw codes
        code_start = pos * 2
        code_end = min(len(b), (pos + 15) * 2)
        raw = b[code_start:code_end]
        raw_codes = [raw[i:i+2] for i in range(0, len(raw), 2)]

        print(f"  Bk{book_idx:2d}: ...{context}...")
        print(f"         raw: {' '.join(raw_codes)}")


print("\n\n=== PART 5: CO vs CH ANALYSIS ===\n")

# In German, C almost never appears alone — it's always CH, SCH, CK, or in foreign words
# Check how many times C appears in non-German patterns
c_pattern_counts = {'CH': 0, 'SCH': 0, 'CK': 0, 'CO': 0, 'CE': 0, 'CA': 0, 'CI': 0, 'CS': 0, 'other_C': 0}

for b in books:
    decoded = decode(b)
    i = 0
    while i < len(decoded):
        if decoded[i] == 'C':
            # Check what follows
            after = decoded[i+1] if i+1 < len(decoded) else ''
            before = decoded[i-1] if i > 0 else ''

            if before == 'S' and after == 'H':
                c_pattern_counts['SCH'] += 1
            elif after == 'H':
                c_pattern_counts['CH'] += 1
            elif after == 'K':
                c_pattern_counts['CK'] += 1
            elif after == 'O':
                c_pattern_counts['CO'] += 1
            elif after == 'E':
                c_pattern_counts['CE'] += 1
            elif after == 'A':
                c_pattern_counts['CA'] += 1
            elif after == 'I':
                c_pattern_counts['CI'] += 1
            elif after == 'S':
                c_pattern_counts['CS'] += 1
            else:
                c_pattern_counts['other_C'] += 1
                print(f"  Unusual C context: Bk decoded[{i-2}:{i+3}] = ...{decoded[max(0,i-2):i+3]}...")
        i += 1

print("C pattern distribution:")
for pat, count in sorted(c_pattern_counts.items(), key=lambda x: -x[1]):
    german = "valid" if pat in ('CH', 'SCH', 'CK') else "NON-standard in German"
    print(f"  {pat}: {count} ({german})")

# Specifically: where does CO appear?
print("\n\nAll CO occurrences:")
for book_idx, b in enumerate(books):
    decoded = decode(b)
    pos = 0
    while True:
        pos = decoded.find('CO', pos)
        if pos < 0:
            break
        start = max(0, pos - 6)
        end = min(len(decoded), pos + 8)
        raw_start = pos * 2
        raw_codes = [b[raw_start+i:raw_start+i+2] for i in range(0, 4, 2)]
        print(f"  Bk{book_idx:2d} pos{pos:3d}: ...{decoded[start:end]}...  codes: {raw_codes}")
        pos += 1

# Specifically: where does CE appear?
print("\nAll CE occurrences:")
for book_idx, b in enumerate(books):
    decoded = decode(b)
    pos = 0
    while True:
        pos = decoded.find('CE', pos)
        if pos < 0:
            break
        start = max(0, pos - 6)
        end = min(len(decoded), pos + 8)
        raw_start = pos * 2
        raw_codes = [b[raw_start+i:raw_start+i+2] for i in range(0, 4, 2)]
        print(f"  Bk{book_idx:2d} pos{pos:3d}: ...{decoded[start:end]}...  codes: {raw_codes}")
        pos += 1
