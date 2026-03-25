"""
Raw-digit superstring assembly.
Assemble at the raw digit level (before decoding) for better overlaps.
The decoded-level assembly fragments excessively because different homophones
for the same letter don't overlap. Raw digits are exact, so overlaps are unambiguous.
"""
import json

with open('books.json', 'r') as f:
    books = json.load(f)

# All books are even-length digit strings (2-digit codes)
print(f"Total books: {len(books)}")
for i, b in enumerate(books):
    print(f"  Bk{i}: {len(b)} digits ({len(b)//2} codes)")

# Find longest suffix-prefix overlap between two digit strings
def find_overlap(a, b, min_len=4):
    """Find longest suffix of a that matches prefix of b. Min 4 digits (2 codes)."""
    max_overlap = min(len(a), len(b))
    for length in range(max_overlap, min_len - 1, -1):
        if length % 2 != 0:  # only even-length overlaps (complete code pairs)
            continue
        if a[-length:] == b[:length]:
            return length
    return 0

# Greedy overlap assembly
# Step 1: Find all pairwise overlaps
print("\n=== Finding all pairwise overlaps ===")
n = len(books)
overlaps = {}
for i in range(n):
    for j in range(n):
        if i == j:
            continue
        ov = find_overlap(books[i], books[j])
        if ov > 0:
            overlaps[(i, j)] = ov

# Sort by overlap length descending
sorted_overlaps = sorted(overlaps.items(), key=lambda x: -x[1])
print(f"Total overlapping pairs: {len(sorted_overlaps)}")
print("\nTop 20 overlaps:")
for (i, j), ov in sorted_overlaps[:20]:
    print(f"  Bk{i} -> Bk{j}: {ov} digits ({ov//2} codes)")

# Step 2: Check for exact duplicates and containment
print("\n=== Checking containment ===")
contained = set()
for i in range(n):
    for j in range(n):
        if i != j and books[i] in books[j]:
            print(f"  Bk{i} ({len(books[i])} digits) is contained in Bk{j} ({len(books[j])} digits)")
            contained.add(i)

print(f"\n{len(contained)} books are contained in other books")

# Step 3: Greedy superstring assembly
# Remove contained books first
unique_indices = [i for i in range(n) if i not in contained]
unique_books = [books[i] for i in unique_indices]
print(f"\n{len(unique_books)} unique (non-contained) books remain")

# Build superstring(s) by greedily joining
used = [False] * len(unique_books)
fragments = []

while True:
    # Find unused books
    unused = [i for i in range(len(unique_books)) if not used[i]]
    if not unused:
        break

    # Start with the longest unused book
    start_idx = max(unused, key=lambda i: len(unique_books[i]))
    current = unique_books[start_idx]
    used[start_idx] = True
    chain = [unique_indices[start_idx]]

    # Extend right
    changed = True
    while changed:
        changed = False
        best_ov = 0
        best_j = -1
        for j in range(len(unique_books)):
            if used[j]:
                continue
            ov = find_overlap(current, unique_books[j])
            if ov > best_ov:
                best_ov = ov
                best_j = j
        if best_j >= 0 and best_ov >= 4:
            current = current + unique_books[best_j][best_ov:]
            used[best_j] = True
            chain.append(unique_indices[best_j])
            changed = True

    # Extend left
    changed = True
    while changed:
        changed = False
        best_ov = 0
        best_j = -1
        for j in range(len(unique_books)):
            if used[j]:
                continue
            ov = find_overlap(unique_books[j], current)
            if ov > best_ov:
                best_ov = ov
                best_j = j
        if best_j >= 0 and best_ov >= 4:
            current = unique_books[best_j][:len(unique_books[best_j]) - best_ov] + current
            used[best_j] = True
            chain.insert(0, unique_indices[best_j])
            changed = True

    fragments.append((current, chain))

print(f"\n=== Assembled {len(fragments)} superstring fragments ===")
total_digits = 0
for idx, (frag, chain) in enumerate(fragments):
    codes = len(frag) // 2
    total_digits += len(frag)
    print(f"\nFragment {idx}: {len(frag)} digits ({codes} codes), assembled from {len(chain)} books")
    print(f"  Books: {chain}")
    # Show first and last 40 digits
    if len(frag) <= 80:
        print(f"  Raw: {frag}")
    else:
        print(f"  Start: {frag[:80]}...")
        print(f"  End:   ...{frag[-80:]}")

print(f"\nTotal assembled: {total_digits} digits ({total_digits//2} codes)")

# Now decode the assembled fragments
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

def decode(digit_string):
    result = []
    for i in range(0, len(digit_string), 2):
        code = digit_string[i:i+2]
        if code in all_codes:
            result.append(all_codes[code])
        else:
            result.append('?')
    return ''.join(result)

print("\n=== Decoded Fragments ===")
for idx, (frag, chain) in enumerate(fragments):
    decoded = decode(frag)
    print(f"\nFragment {idx} ({len(decoded)} chars, {len(chain)} books):")
    # Print in 80-char lines
    for start in range(0, len(decoded), 80):
        print(f"  {decoded[start:start+80]}")

# Compare with decoded-level assembly
print("\n=== Comparison with decoded-level assembly ===")
# Decode each book individually
decoded_books = [decode(b) for b in books]

# Check: do the raw fragments decode to the same thing?
# Count unique characters, unknown codes
for idx, (frag, chain) in enumerate(fragments):
    decoded = decode(frag)
    unknowns = decoded.count('?')
    print(f"Fragment {idx}: {len(decoded)} chars, {unknowns} unknowns ({100*unknowns/len(decoded):.1f}%)")

# Verify all books are accounted for
all_used_books = set()
for frag, chain in fragments:
    all_used_books.update(chain)
all_used_books.update(contained)
missing = set(range(n)) - all_used_books
print(f"\nBooks accounted for: {len(all_used_books)}/{n}")
if missing:
    print(f"Missing books: {missing}")

# Now do DP word segmentation on each fragment
print("\n\n=== DP Word Segmentation on Raw-Assembled Fragments ===")

german_words = set()
basic = [
    'DER','DIE','DAS','EIN','EINE','UND','IN','IST','ES','ICH','DU','ER','SIE','WIR',
    'IHR','NICHT','AUCH','AUF','AN','MIT','AUS','VON','ZU','BEI','NACH','HIER','DA',
    'NOCH','NUR','ABER','WAS','WER','WIE','SO','DOCH','KEIN','KEINE','MEIN','DEIN',
    'SEIN','SEINE','DIESER','DIESE','JEDER','JEDE','ALLE','ODER','WENN','DASS',
    'WEIL','DENN','OB','ALS','BIS','FUER','UEBER','UNTER','NEBEN','VOR','HINTER',
    'ZWISCHEN','DURCH','OHNE','GEGEN','SCHON','SEHR','MEHR','AM','IM','ZUM','ZUR',
    'DEN','DEM','DES','EINEN','EINEM','EINES',
    'HABEN','SEIN','WERDEN','KOENNEN','MUESSEN','SOLLEN','WOLLEN','DUERFEN',
    'MACHEN','GEHEN','KOMMEN','SEHEN','STEHEN','FINDEN','GEBEN','NEHMEN',
    'LASSEN','HALTEN','SAGEN','SPRECHEN','BRINGEN','LESEN','SCHREIBEN',
    'HEISSEN','KENNEN','DENKEN','WISSEN','LEBEN','LIEGEN','BLEIBEN',
    'RUFEN','SETZEN','STELLEN','TRAGEN','ZIEHEN','SCHLAGEN','FALLEN',
    'LAUFEN','FAHREN','ESSEN','TRINKEN','SCHLAFEN','STERBEN','BEGINNEN',
    'FANGEN','KOENIG','RUNE','RUNEN','STEIN','STEINE','STEINEN',
    'URALTE','URALTEN','URALTER','ENDE','ENDEN','ENDLICH',
    'GROSS','KLEINE','ALTEN','NEUEN','GUTEN',
    'ORT','REDE','REDEN','TEIL','TEILE','TEILEN',
    'FACH','STEIL','TUN','TUNS',
    'TAG','NACHT','WELT','ZEIT','MANN','FRAU','KIND','HAUS',
    'LAND','STADT','WALD','BERG','FLUSS','SEE','MEER',
    'FEUER','WASSER','ERDE','LUFT','LICHT','DUNKEL',
    'KRIEG','KAMPF','SCHWERT','SCHILD','MAGIE','ZAUBER',
    'GEIST','SEELE','TOD','LEBEN','MACHT','KRAFT',
    'DRACHE','DAEMON','RITTER','HELD','MEISTER',
    'GOLD','SILBER','EISEN','STAHL',
    'ALT','NEU','GUT','SCHLECHT','STARK','SCHWACH',
    'WAHR','FALSCH','RECHT','TIEF','HOCH','LANG','KURZ',
    'SCHAUN','SCHAUEN','ZEIGEN','SEHEN',
    'AB','EI','RE','GE',
    'MINH','TOTNIURG','HEARUCHTIGER','LABGZERAS','THARSC',
    'DIES','DIESER','DIESES','DIESEM',
    'NIMM','NIMMER','IMMER','GESTERN','MORGEN','HEUTE',
    'OBEN','UNTEN','LINKS','RECHTS','INNEN','AUSSEN',
    'FREUND','FEIND','BRUDER','SCHWESTER','VATER','MUTTER',
    'EHRE','RUHM','TREUE','MUT','FURCHT',
    'ENGEL','TEUFEL','GOTT','GOETTER',
    'SONNE','MOND','STERN','STERNE',
    'BLUT','BEIN','HERZ','AUGE','HAND',
    'ZEICHEN','SCHRIFT','BUCH','WORT','WORTE','SPRUCH',
    'STEIN','MAUER','TOR','TUER','WEG','STRASSE',
    'DUNKELHEIT','FINSTERNIS',
    'EWIGE','EWIGEN','EWIGKEIT',
    'HEILIG','HEILIGE','HEILIGEN',
    'GEHEIM','GEHEIMNIS',
    'VERBORGEN','VERBORGENE','VERBORGENEN',
    'VERGESSEN','VERGESSENE','VERGESSENEN',
    'ZERSTOEREN','ERSCHAFFEN','ERWACHEN',
    'PROPHEZEIUNG','LEGENDE','SAGE',
    'UNTOTE','UNTOTEN','UNTOTER',
    'ELEMENTAR','ELEMENT','ELEMENTE',
    'RITUAL','OPFER','ALTAR',
    'HOEHLE','TIEFE','ABGRUND',
    'FLUCH','SEGEN','BANN',
    'TRUHE','SCHAETZ','SCHAETZE',
    'WAECHTER','HUETER',
    'PORTAL','PASSAGE','EINGANG',
    'INSCHRIFT','GRAVUR',
    'KNOCHEN','SCHAEDEL','GEBEIN',
    'NORDEN','SUEDEN','OSTEN','WESTEN',
    'ERSTER','ERSTE','ERSTEN','ZWEITE','DRITTE',
    'HUNDERT','TAUSEND',
    'SE','EN','ER','EI','EE', 'NE',
    'TIER', 'TIERE', 'TIEREN',
    'EICHE', 'SACHE', 'SACHEN',
    'REISE', 'REISEN',
    'STUNDE', 'STUNDEN',
    'DIENST',
    'MEINEN', 'MEINER',
    'SEINER', 'SEINES',
    'IHREN', 'IHREM', 'IHRER',
    'UNSERE', 'UNSEREN', 'UNSEREM',
]
for w in basic:
    german_words.add(w)
    if len(w) >= 4:
        german_words.add(w[:len(w)-1])  # stem without last letter

def dp_parse(text, wordset, min_word_len=2):
    n = len(text)
    dp = [0] * (n + 1)
    parent = [None] * (n + 1)

    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        parent[i] = i - 1

        for wlen in range(min_word_len, min(i, 25) + 1):
            start = i - wlen
            word = text[start:i]
            if word in wordset:
                score = dp[start] + wlen * wlen  # favor longer words
                if score > dp[i]:
                    dp[i] = score
                    parent[i] = start

    # Backtrack
    words = []
    pos = n
    while pos > 0:
        prev = parent[pos]
        seg = text[prev:pos]
        if seg in wordset:
            words.append((prev, seg))
        pos = prev
    words.reverse()

    covered = sum(len(w) for _, w in words)
    return words, covered

# Parse each fragment
for idx, (frag, chain) in enumerate(fragments):
    decoded = decode(frag)
    if len(decoded) < 5:
        continue
    words, covered = dp_parse(decoded, german_words)
    pct = 100 * covered / len(decoded) if decoded else 0
    print(f"\nFragment {idx} ({len(decoded)} chars): {pct:.1f}% coverage, {len(words)} words")
    if len(decoded) <= 300:
        # Annotate: uppercase = recognized, lowercase = unrecognized
        annotated = list(decoded.lower())
        for pos, word in words:
            for k in range(len(word)):
                annotated[pos + k] = word[k]  # uppercase
        print(f"  {''.join(annotated)}")

    # Show top words
    from collections import Counter
    wc = Counter(w for _, w in words)
    top = wc.most_common(15)
    if top:
        print(f"  Top words: {', '.join(f'{w}:{c}' for w,c in top)}")
