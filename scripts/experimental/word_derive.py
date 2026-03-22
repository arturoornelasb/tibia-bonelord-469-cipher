"""
Word-pattern derivation: find unknown codes that complete German words
when surrounded by known codes.
"""
import json
from collections import Counter, defaultdict

with open('books.json', 'r') as f:
    books = json.load(f)

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

fixed = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U',
    '00': 'H', '14': 'N', '72': 'R', '91': 'S', '15': 'I',
    '76': 'E', '52': 'S', '42': 'D', '46': 'I', '48': 'N',
    '57': 'H', '04': 'M', '12': 'S', '58': 'N',
    '78': 'T', '51': 'R', '35': 'A', '34': 'L',
    '01': 'E', '59': 'S', '41': 'E', '30': 'E',
    '94': 'H',
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# German word patterns of length 3-8 with one wildcard position
german_words = [
    # 3-letter
    'DER', 'DIE', 'DAS', 'UND', 'IST', 'EIN', 'DEN', 'DEM', 'DES',
    'VON', 'HAT', 'AUF', 'MIT', 'SIE', 'ICH', 'AUS', 'WIR', 'BEI',
    'NUR', 'WER', 'MAN', 'IHN', 'IHR', 'WAS', 'OFT', 'NUN',
    'ALS', 'ODE', 'UNS', 'TAG', 'WIE', 'GUT',
    # 4-letter
    'SICH', 'SIND', 'DASS', 'EINE', 'SEIN', 'HIER', 'IHRE',
    'NACH', 'NOCH', 'AUCH', 'ABER', 'ODER', 'ALLE', 'WENN', 'DANN',
    'WELT', 'ZEIT', 'TEIL', 'JEDE', 'GIBT', 'KEIN', 'NEIN',
    'VIEL', 'WOHL', 'GANZ', 'LANG', 'GROSS', 'HAUS', 'VOLK',
    'GOTT', 'MUSS', 'SOLL', 'WILL', 'DORT', 'SEHR',
    'LAND', 'WALD', 'BERG', 'NACHT', 'BUCH', 'RUNE', 'LAUT',
    'WORT', 'NAME', 'FORM', 'ERDE', 'WIND', 'LEHR',
    # 5-letter
    'NICHT', 'EINER', 'EINEN', 'DIESE', 'JEDER', 'JEDES', 'ALTEN',
    'STEINE', 'RUNEN', 'STEIN', 'SEINE', 'IMMER', 'SCHON',
    'UNTER', 'DURCH', 'GEGEN', 'HINTER',
    'HATTE', 'HABEN', 'WURDE', 'WAREN', 'MACHT', 'KRAFT',
    'ERSTE', 'NEUEN', 'NEUER', 'ALLES', 'IHREN', 'IHREM',
    'MEINE', 'DEINEN', 'HEISST', 'BITTE', 'DINGE',
    'LICHT', 'DUNKEL', 'FEUER', 'WASSER', 'MAGIE',
    'GEBEN', 'LESEN', 'SEHEN', 'REDEN', 'ZEIGT',
    'GROSS', 'KLEIN', 'FREMD', 'LIEBE',
    'NACHT', 'GEIST', 'SEELE', 'HERZ',
    'WISSEN', 'KONNTE', 'MUSSTE', 'SOLLTE', 'WOLLTE',
    # 6-letter
    'DIESER', 'DIESES', 'DIESEM', 'DIESEN',
    'STEINEN', 'URALTE', 'URALTEN', 'URALTER',
    'ANDERE', 'ANDEREN', 'ANDERER',
    'KLEINE', 'KLEINEN', 'GROSSER',
    'NICHTS', 'WERDEN', 'WIEDER', 'EINIGE',
    'SCHRIFT', 'SPRACHE', 'ZEICHEN',
    'KOENNEN', 'MUESSTEN',
    'FREUNDE', 'FEINDE',
    'UNSERE', 'UNSERER', 'UNSEREM',
    # 7+ letter
    'ZWISCHEN', 'INSCHRIFT', 'INSCHRIFTEN',
    'GEHEIMNIS', 'GEHEIME', 'GEHEIMEN',
    'RUNENSTEIN', 'RUNENSTEINE', 'RUNENSTEINEN',
    'BIBLIOTHEK',
    'SCHREIBEN', 'GESCHRIEBEN',
    'VERSTEHEN', 'VERSTANDEN',
    'VERSCHIEDENE', 'VERSCHIEDENEN',
    'EINANDER',
]

# For each word, generate all possible patterns with 1 unknown
# then check if the pattern appears in the text
print("=" * 70)
print("WORD-PATTERN MATCHING")
print("=" * 70)

# Build code-letter pairs for fast lookup
pair_counts = Counter()
for pairs in book_pairs:
    pair_counts.update(pairs)

# For each book, find windows of 3-12 pairs
# where exactly 1 pair is unknown and the rest match a German word
word_evidence = defaultdict(lambda: defaultdict(int))  # code -> letter -> count

for word in german_words:
    wlen = len(word)
    if wlen < 3 or wlen > 12:
        continue

    # For each position that could be unknown
    for unk_pos in range(wlen):
        target_letter = word[unk_pos]
        known_letters = [(i, word[i]) for i in range(wlen) if i != unk_pos]

        # Search in all books
        for pairs in book_pairs:
            for start in range(len(pairs) - wlen + 1):
                window = pairs[start:start + wlen]

                # Check: exactly position unk_pos should be unknown,
                # all others should be fixed and match the word
                match = True
                unk_code = None
                for i, expected_letter in known_letters:
                    code = window[i]
                    if code not in fixed or fixed[code] != expected_letter:
                        match = False
                        break
                if not match:
                    continue

                # Check that the unknown position IS actually unknown
                unk_code = window[unk_pos]
                if unk_code in fixed:
                    # Already known — verify it matches
                    if fixed[unk_code] == target_letter:
                        continue  # Already confirmed, skip
                    else:
                        continue  # Contradicts known assignment

                # Found a match! Code unk_code should be target_letter
                word_evidence[unk_code][target_letter] += 1

# Report results
print(f"\nWord-based evidence for unknown codes:")
print(f"{'Code':<6} {'Letter':<8} {'Hits':<6} {'Words found':<40}")
print("-" * 70)

# Collect all evidence
all_evidence = []
for code in sorted(word_evidence.keys(), key=lambda c: -sum(word_evidence[c].values())):
    for letter, count in sorted(word_evidence[code].items(), key=lambda x: -x[1]):
        if count >= 2:  # at least 2 independent matches
            all_evidence.append((code, letter, count))

# Show top evidence
for code, letter, count in sorted(all_evidence, key=lambda x: -x[2])[:60]:
    # Find which words match
    matching_words = []
    for word in german_words:
        for unk_pos in range(len(word)):
            if word[unk_pos] != letter:
                continue
            known_letters = [(i, word[i]) for i in range(len(word)) if i != unk_pos]
            for pairs in book_pairs:
                for start in range(len(pairs) - len(word) + 1):
                    window = pairs[start:start + len(word)]
                    match = True
                    for i, exp in known_letters:
                        if window[i] not in fixed or fixed[window[i]] != exp:
                            match = False
                            break
                    if match and window[unk_pos] == code:
                        if word not in matching_words:
                            matching_words.append(word)
                        break
                if word in matching_words:
                    break

    freq = pair_counts.get(code, 0)
    print(f"  {code:<6} {letter:<8} {count:<6} (freq={freq}) words: {matching_words[:8]}")


# Summarize: for each unknown code, what's the best letter?
print(f"\n{'='*70}")
print("BEST WORD-BASED ASSIGNMENT PER CODE")
print("=" * 70)

code_best = {}
for code in word_evidence:
    letters = word_evidence[code]
    if not letters:
        continue
    best_letter = max(letters, key=letters.get)
    best_count = letters[best_letter]
    second = sorted(letters.items(), key=lambda x: -x[1])
    second_info = f", 2nd: {second[1][0]}:{second[1][1]}" if len(second) > 1 else ""

    if best_count >= 3:
        freq = pair_counts.get(code, 0)
        ratio = best_count / sum(letters.values())
        code_best[code] = (best_letter, best_count, ratio)
        print(f"  {code}: {best_letter} ({best_count} hits, {ratio:.0%} of evidence, freq={freq}){second_info}")


# Cross-check with frequency needs
print(f"\n{'='*70}")
print("PROPOSED TIER 4 ASSIGNMENTS (word + bigram combined)")
print("=" * 70)

german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
}

total_pairs = sum(pair_counts.values())

# Calculate how much more each letter needs
letter_assigned = Counter()
for c, l in fixed.items():
    letter_assigned[l] += pair_counts.get(c, 0)

print(f"\nIf we assign codes by word evidence (top letter, >=5 hits, >=60% ratio):")
proposed = {}
for code, (letter, count, ratio) in sorted(code_best.items(), key=lambda x: -x[1][1]):
    if count >= 5 and ratio >= 0.60:
        proposed[code] = letter
        letter_assigned[letter] += pair_counts.get(code, 0)
        print(f"  {code} = {letter} ({count} hits, {ratio:.0%})")

print(f"\nResulting letter frequencies:")
for l in sorted(german_freq, key=lambda l: -german_freq[l]):
    obs = letter_assigned.get(l, 0) / total_pairs * 100
    exp = german_freq[l] * 100
    diff = obs - exp
    n_fixed = sum(1 for c in fixed if fixed[c] == l)
    n_proposed = sum(1 for c in proposed if proposed[c] == l)
    if obs > 0 or exp > 1:
        marker = "!!" if abs(diff) > 2 else ""
        print(f"  {l}: {obs:.1f}% (exp {exp:.1f}%, diff {diff:+.1f}%) [{n_fixed} fixed + {n_proposed} new] {marker}")

print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
