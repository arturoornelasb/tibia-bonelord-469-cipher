"""
Session 9 - Attack I overrepresentation.
I is at 10.4% vs expected 7.6% (+2.8%).
If ~50 of I's ~588 occurrences are actually B or F, that would fix the frequency gap.
Strategy: Find I codes that create valid German words when changed to B or F.
"""
import json, re
from collections import Counter

with open('data/books.json') as f:
    raw_books = json.load(f)
with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]

books = [parse_codes(b) for b in raw_books]

rev = {}
for code, letter in mapping.items():
    rev.setdefault(letter, []).append(code)

def decode(codes):
    return ''.join(mapping.get(c, '?') for c in codes)

print("=" * 80)
print("ATTACK ON I OVERREPRESENTATION")
print("=" * 80)

# I codes and their frequencies
i_codes = rev.get('I', [])
print(f"\nI codes: {i_codes}")
code_counts = {}
for ic in i_codes:
    count = sum(1 for b in books for c in b if c == ic)
    code_counts[ic] = count
    print(f"  Code {ic}: {count} occurrences")

total_i = sum(code_counts.values())
print(f"  Total I: {total_i}")

# Expected I count at 7.6% of total
total_codes = sum(len(b) for b in books)
expected_i = int(total_codes * 0.076)
excess = total_i - expected_i
print(f"  Expected at 7.6%: {expected_i}")
print(f"  Excess: {excess} (~{excess} codes might be B or F)")

# ============================================================
# For each I code, test what happens if we change it to B or F
# ============================================================
print("\n" + "=" * 80)
print("TESTING EACH I CODE AS B AND F")
print("=" * 80)

german_words_3plus = {
    'ab', 'aber', 'als', 'alt', 'alte', 'alten', 'alter', 'altes',
    'am', 'an', 'auf', 'aus',
    'bald', 'baum', 'bei', 'berg', 'bis', 'blut', 'boden', 'brief',
    'da', 'das', 'dass', 'dem', 'den', 'denen', 'der', 'des',
    'die', 'dies', 'dieser', 'dir', 'doch', 'durch',
    'eben', 'eigen', 'ein', 'eine', 'einem', 'einen', 'einer',
    'ende', 'er', 'erde', 'erst', 'erste', 'ersten', 'es',
    'fach', 'fall', 'fand', 'fels', 'fest', 'finden', 'fing',
    'fort', 'frei', 'fuer',
    'gab', 'ganz', 'gar', 'geben', 'gehen', 'geh', 'gen', 'gern',
    'grab', 'gruen', 'grund', 'gut',
    'hab', 'haben', 'halb', 'hat', 'haus', 'heb', 'heben',
    'her', 'hier', 'hin', 'hob',
    'ich', 'ihm', 'ihn', 'in', 'ins', 'ist',
    'klar', 'koenig',
    'lab', 'lauf', 'leben', 'lob',
    'nach', 'neben', 'net', 'neu', 'nicht', 'nie', 'noch', 'nun', 'nur',
    'ob', 'ode', 'oben', 'oder', 'oft', 'ort', 'orte',
    'rede', 'rief', 'ruf', 'ruin', 'rune', 'runen',
    'schaff', 'schaun', 'schuf', 'see', 'seid', 'sei', 'sein', 'seine',
    'ser', 'sie', 'so', 'stab', 'steh', 'stein', 'steine', 'steinen',
    'rief', 'ruf', 'brief',
    'tab', 'tag', 'teil', 'tief', 'tot', 'tun',
    'ub', 'ueber', 'um', 'und', 'uns', 'unter', 'uralte', 'uralten',
    'viel', 'volk', 'von', 'vor',
    'wald', 'weg', 'weil', 'welt', 'wir', 'wind', 'wisset', 'wohl', 'wort',
    # Words with B/F that would be especially interesting
    'aber', 'auf', 'befand', 'befinden', 'befall', 'befehl',
    'berg', 'blick', 'boden', 'bote', 'brach', 'brief',
    'darf', 'darauf', 'duerfen',
    'fand', 'fern', 'feucht', 'feuer', 'fluch', 'flug', 'fluss',
    'folge', 'fragen', 'fremd', 'fuehren', 'fuerst', 'fuss',
    'gab', 'gebot', 'gebirge', 'gebiet', 'geboren',
    'graben', 'grub', 'grab',
    'halb', 'heben', 'herbei', 'herauf',
    'kampf', 'kraft', 'krieg',
    'lauf', 'laufen', 'lob', 'leben',
    'neben', 'oben', 'ob',
    'rief', 'ruf', 'rufen',
    'schaffen', 'scharf', 'schiff', 'schlaf',
    'stab', 'stufe', 'strafe',
    'tief', 'tiefe', 'treffen', 'treff',
    'ufer', 'uebel',
    'verb', 'verbot', 'verfiel', 'vorbei',
    'waffe', 'weib', 'wolf',
}

for test_letter in ['B', 'F']:
    print(f"\n{'='*60}")
    print(f"  TESTING I -> {test_letter}")
    print(f"{'='*60}")

    for ic in sorted(i_codes, key=lambda x: -code_counts[x]):
        count = code_counts[ic]
        if count < 5:
            continue  # Skip very rare codes

        # For each book, replace this I code with test_letter and check for new words
        new_words_found = []
        for bi, book_codes in enumerate(books):
            original = decode(book_codes)
            # Replace this specific code
            modified = []
            for c in book_codes:
                if c == ic:
                    modified.append(test_letter)
                else:
                    modified.append(mapping.get(c, '?'))
            modified_text = ''.join(modified)

            # Find all 3+ char words in modified that weren't in original
            for wlen in range(3, 12):
                for pos in range(len(modified_text) - wlen + 1):
                    candidate = modified_text[pos:pos+wlen].lower()
                    if candidate in german_words_3plus:
                        # Check if this word existed in the original
                        orig_at_pos = original[pos:pos+wlen].lower()
                        if orig_at_pos != candidate:
                            # New word created by the change!
                            context_start = max(0, pos-5)
                            context_end = min(len(modified_text), pos+wlen+5)
                            new_words_found.append((
                                bi, candidate, pos,
                                original[context_start:context_end],
                                modified_text[context_start:context_end]
                            ))

        # Deduplicate by word
        word_counter = Counter(w[1] for w in new_words_found)
        if word_counter:
            print(f"\n  Code {ic} (I, {count}x) -> {test_letter}:")
            unique_words = {}
            for bi, word, pos, orig_ctx, mod_ctx in new_words_found:
                if word not in unique_words:
                    unique_words[word] = (bi, pos, orig_ctx, mod_ctx)

            for word, (bi, pos, orig_ctx, mod_ctx) in sorted(unique_words.items(),
                                                              key=lambda x: -word_counter[x[0]]):
                cnt = word_counter[word]
                print(f"    {word:12s} x{cnt:2d}  orig:'{orig_ctx}' -> mod:'{mod_ctx}'")

            # How many I occurrences would this affect?
            total_affected = count
            print(f"    -> Would change {total_affected} I's to {test_letter}")

# ============================================================
# Also test: which I code has the worst bigram profile?
# ============================================================
print(f"\n{'='*80}")
print("BIGRAM ANALYSIS PER I CODE")
print(f"{'='*80}")

# For each I code, what letters precede and follow it?
for ic in sorted(i_codes, key=lambda x: -code_counts[x]):
    count = code_counts[ic]
    if count < 5:
        continue

    before = Counter()
    after = Counter()
    for book_codes in books:
        decoded = decode(book_codes)
        for pos, c in enumerate(book_codes):
            if c == ic:
                if pos > 0:
                    before[decoded[pos-1]] += 1
                if pos < len(decoded) - 1:
                    after[decoded[pos+1]] += 1

    print(f"\n  Code {ic} (I, {count}x):")
    print(f"    Before: {dict(before.most_common(8))}")
    print(f"    After:  {dict(after.most_common(8))}")

    # Check for unusual bigrams that wouldn't be expected for I
    # In German, common I-bigrams: EI, IE, IN, IS, IT, IG, IC, DI, MI, NI
    # Unusual: BI (uncommon), FI (uncommon), OI (very rare), UI (very rare)
    unusual_before = {k: v for k, v in before.items() if k in 'OUAW'}
    unusual_after = {k: v for k, v in after.items() if k in 'OUAW'}
    if unusual_before or unusual_after:
        print(f"    UNUSUAL before: {unusual_before}")
        print(f"    UNUSUAL after:  {unusual_after}")

print("\n" + "=" * 80)
print("DONE")
print("=" * 80)
