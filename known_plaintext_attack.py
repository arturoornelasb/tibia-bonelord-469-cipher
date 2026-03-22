"""
Tibia 469 - Known Plaintext Attack
====================================
Using NPC dialogues with suspected translations as "cribs"
to derive the cipher key.

Known/suspected mappings:
- Knightmare: "3478 67 090871 097664 3466 00 0345" = "BE A WIT THAN BE A FOOL"
- If we trust the spacing, we can map digit groups to words
"""

import json
from collections import Counter, defaultdict

with open("books.json", "r") as f:
    books = json.load(f)

all_text = "".join(books)

print("=" * 70)
print("TIBIA 469 - KNOWN PLAINTEXT ATTACK")
print("=" * 70)

# ============================================================
# 1. KNIGHTMARE CRIB ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("1. KNIGHTMARE CRIB: '3478 67 090871 097664 3466 00 0345'")
print("   PLAINTEXT:        'BE   A  WIT    THAN   BE   A  FOOL'")
print("=" * 70)

# If we trust the spacing:
# 3478   = BE
# 67     = A
# 090871 = WIT (3 letters, 6 digits -> 2 digits per letter)
# 097664 = THAN (4 letters, 6 digits -> mixed?)
# 3466   = BE (2 letters, 4 digits -> 2 digits per letter, BUT 3478=BE above!)
# 00     = A (1 letter, 2 digits -> but 67=A above!)
# 0345   = FOOL (4 letters, 4 digits -> 1 digit per letter?)

# This is inconsistent! 3478=BE but also 3466=BE, and 67=A but also 00=A
# This strongly suggests HOMOPHONIC cipher (multiple ciphertexts per letter)

print("\nMapping analysis (assuming 2-digit pairs):")
print()

# If 2-digit pairs: 3478 = B,E => 34=B, 78=E
# 67 = A => need padding? or 1-digit mapping?
# 090871 = W,I,T => 09=W, 08=I, 71=T
# 097664 = T,H,A,N => 09=T? conflict with W!
# Or: 0=padding, 97664 doesn't split evenly

# Alternative: what if spacing is the delimiter and the
# number-to-letter mapping is more complex?

print("--- Hypothesis A: Pure 2-digit pairs ---")
# 3478 -> 34,78 -> B,E  (works: 2 pairs = 2 letters)
# 67 -> one pair, one letter = A
# 090871 -> 09,08,71 -> W,I,T (3 pairs = 3 letters)
# 097664 -> 09,76,64 -> T,H,A,N (3 pairs for 4 letters - DOESN'T WORK)
#   unless: 0,97,66,4 or 09,76,6,4 (variable width?)

print("  3478 = BE:  34->B, 78->E")
print("  67   = A:   67->A")
print("  090871 = WIT:  09->W, 08->I, 71->T")
print("  097664 = THAN: 09->T?, 76->H?, 64->A?, leftover '6'?")
print("  PROBLEM: 09 maps to both W and T!")
print()

print("--- Hypothesis B: Variable-length with 0 as spacer ---")
# What if 0 is a word separator within groups?
# 090871 = [0]9[0]871 = 9=W, 871=IT?
# That's more complex

# Alternative spacing interpretation:
# "3478 67 090871 097664 3466 00 0345"
# What if the original is: "34 78 67 09 08 71 09 76 64 34 66 00 03 45"
# And spaces in NPC text are just formatting?

print("--- Hypothesis C: All pairs, ignore NPC spacing ---")
mapping_c = {}
plaintext = "BEAWITTHANBEA FOOL"
# But we don't know where "A FOOL" splits vs "AFOOL"
# Let's try: "BE A WIT THAN BE A FOOL"
# Remove spaces: "BEAWITTHANBEAFOOL" = 17 letters
# Cipher without spaces: "34786709087109766434660003 45" = hmm

cipher_nospaces = "347867090871097664346600345"
plain_nospaces = "BEAWITTHANBEAFOOL"
print(f"  Cipher (no spaces): {cipher_nospaces} ({len(cipher_nospaces)} digits)")
print(f"  Plain  (no spaces): {plain_nospaces} ({len(plain_nospaces)} letters)")
print(f"  Ratio: {len(cipher_nospaces)/len(plain_nospaces):.2f} digits per letter")

# 26 digits for 17 letters = 1.53 digits per letter
# This is between 1 and 2, suggesting VARIABLE-LENGTH encoding

# Let's try all possible ways to split 26 digits into 17 groups of 1-2 digits
print("\n--- Trying all valid 1-2 digit splits for Knightmare ---")

def find_splits(cipher, plain, pos_c=0, pos_p=0, current_mapping=None, current_split=None):
    """Find all ways to split cipher into groups matching plaintext."""
    if current_mapping is None:
        current_mapping = {}
    if current_split is None:
        current_split = []

    if pos_p == len(plain):
        if pos_c == len(cipher):
            # Check consistency: no cipher code maps to two different letters
            # (but a letter CAN map to multiple codes - homophonic)
            return [(dict(current_mapping), list(current_split))]
        return []

    if pos_c >= len(cipher):
        return []

    results = []
    for width in [1, 2, 3]:  # Try 1, 2, or 3 digit codes
        if pos_c + width > len(cipher):
            continue
        code = cipher[pos_c:pos_c+width]
        letter = plain[pos_p]

        # Check consistency: this code can't already map to a different letter
        if code in current_mapping and current_mapping[code] != letter:
            continue

        new_mapping = dict(current_mapping)
        new_mapping[code] = letter
        new_split = current_split + [code]

        results.extend(find_splits(cipher, plain, pos_c + width, pos_p + 1,
                                    new_mapping, new_split))

    return results

print(f"\n  Searching for consistent mappings...")
print(f"  (this checks all ways to split '{cipher_nospaces}' into groups that map to '{plain_nospaces}')")
print(f"  Allowing 1, 2, or 3 digit codes...")

solutions = find_splits(cipher_nospaces, plain_nospaces)
print(f"\n  Found {len(solutions)} consistent solutions!")

if solutions:
    print(f"\n  Showing first 20 solutions:")
    for i, (mapping, split) in enumerate(solutions[:20]):
        split_str = " ".join(f"{s}={plain_nospaces[j]}" for j, s in enumerate(split))
        print(f"    {i+1}. {split_str}")
        # Show the mapping
        code_to_letter = defaultdict(set)
        for code, letter in mapping.items():
            code_to_letter[code].add(letter)
        conflicts = {c: letters for c, letters in code_to_letter.items() if len(letters) > 1}
        if conflicts:
            print(f"       CONFLICTS: {conflicts}")

# ============================================================
# 2. WRINKLED BONELORD GREETING CRIB
# ============================================================
print("\n" + "=" * 70)
print("2. WRINKLED BONELORD GREETING")
print("=" * 70)

# Greeting: "485611800364197"
# This appears in Book 31 at position 11
# What could this mean? If bonelord says this as greeting,
# in English it might be "GREETINGS" or "WELCOME" or "HELLO"

# Also: "78572611857643646724" appears in 6 books
# This is the second greeting line

greeting1 = "485611800364197"
greeting2 = "78572611857643646724"

print(f"\nGreeting 1: {greeting1} ({len(greeting1)} digits)")
print(f"Greeting 2: {greeting2} ({len(greeting2)} digits)")

# Try common greetings
for word in ["HELLO", "GREETINGS", "WELCOME", "HAIL", "SALUTATIONS"]:
    ratio = len(greeting1) / len(word)
    print(f"  '{greeting1}' as '{word}': {ratio:.2f} digits/letter")

print()
for word in ["WELCOME VISITOR", "WHAT DO YOU WANT", "I AM THE LIBRARIAN", "GREETINGS MORTAL"]:
    plain = word.replace(" ", "")
    ratio = len(greeting2) / len(plain)
    print(f"  '{greeting2}' as '{word}': {ratio:.2f} digits/letter")

# ============================================================
# 3. CHAYENNE'S DIALOGUE CRIB
# ============================================================
print("\n" + "=" * 70)
print("3. CHAYENNE'S DIALOGUE")
print("=" * 70)

# Chayenne (dev): "114514519485611451908304576512282177 :) 6612527570584 xD"
# The smiley faces suggest these are two separate encoded phrases
# followed by emoticons

chayenne1 = "114514519485611451908304576512282177"
chayenne2 = "6612527570584"

print(f"\nPhrase 1: {chayenne1} ({len(chayenne1)} digits)")
print(f"Phrase 2: {chayenne2} ({len(chayenne2)} digits)")
print(f"  (followed by ':)' and 'xD' respectively)")

# Phrase 1 appears in 11 books! It's a very common sequence
# This is embedded in a larger repeating pattern

# Let's see what's around it in the books
print("\nContext of Chayenne phrase 1 in books:")
for i, book in enumerate(books):
    pos = book.find(chayenne1)
    if pos != -1:
        before = book[max(0,pos-20):pos]
        after = book[pos+len(chayenne1):pos+len(chayenne1)+20]
        print(f"  Book {i+1}: ...{before}[{chayenne1}]{after}...")
        break  # Just show first

# ============================================================
# 4. APPLY KNIGHTMARE SOLUTIONS TO BOOKS
# ============================================================
print("\n" + "=" * 70)
print("4. APPLYING BEST KNIGHTMARE SOLUTIONS TO BOOKS")
print("=" * 70)

if solutions:
    # Take the first few solutions and try them on book text
    for sol_idx, (mapping, split) in enumerate(solutions[:5]):
        print(f"\n--- Solution {sol_idx+1} ---")
        print(f"  Mapping: {dict(sorted(mapping.items()))}")

        # Try to decode first book using this mapping
        # Need to figure out the grouping for the book text too
        # For now, try all possible pair widths based on the mapping
        widths_used = set(len(k) for k in mapping.keys())
        print(f"  Code widths used: {widths_used}")

        if widths_used == {2}:
            # Pure 2-digit mapping - easy to apply
            book_text = books[0]
            decoded = ""
            for j in range(0, len(book_text) - 1, 2):
                pair = book_text[j:j+2]
                if pair in mapping:
                    decoded += mapping[pair]
                else:
                    decoded += "?"
            print(f"  Book 1 (pairs): {decoded[:80]}")

# ============================================================
# 5. FREQUENCY-GUIDED KNOWN PLAINTEXT
# ============================================================
print("\n" + "=" * 70)
print("5. IF 2-DIGIT PAIRS: FREQUENCY vs ENGLISH LETTER FREQUENCY")
print("=" * 70)

# Get pair frequencies
pairs = [all_text[i:i+2] for i in range(0, len(all_text)-1, 2)]
pair_freq = Counter(pairs)
total = len(pairs)

# Sort pairs by frequency
sorted_pairs = sorted(pair_freq.items(), key=lambda x: -x[1])
pair_pcts = [(p, c/total*100) for p, c in sorted_pairs]

# English letter frequency sorted
eng_sorted = sorted(ENGLISH_FREQ.items(), key=lambda x: -x[1])

ENGLISH_FREQ = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0,
    'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3,
    'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4, 'W': 2.4,
    'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5,
    'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
    'Z': 0.07
}
eng_sorted = sorted(ENGLISH_FREQ.items(), key=lambda x: -x[1])

# In a homophonic cipher with ~100 symbols for 26 letters,
# each letter gets ~freq/100*total_pairs symbols
# E (12.7%) needs ~12-13 pair codes
# T (9.1%) needs ~9 pair codes
# etc.

print("\nExpected pair allocation in homophonic cipher:")
print(f"{'Letter':>6} {'Eng%':>5} {'ExpPairs':>8} | Candidate pairs (by freq)")
print("-" * 70)

pair_idx = 0
homophonic_key = {}
for letter, freq in eng_sorted:
    # How many pairs should this letter get?
    num_pairs = max(1, round(freq / 100 * len(pair_freq)))
    candidate_pairs = [p for p, _ in pair_pcts[pair_idx:pair_idx+num_pairs]]
    for p in candidate_pairs:
        homophonic_key[p] = letter
    pair_idx += num_pairs
    cand_str = ", ".join(candidate_pairs[:6])
    if len(candidate_pairs) > 6:
        cand_str += f"... (+{len(candidate_pairs)-6} more)"
    print(f"  {letter:>4}  {freq:5.1f}  {num_pairs:>5}    | {cand_str}")

# Apply this frequency-based mapping to books
print("\n--- Frequency-based decode of first 5 books ---")
for i in range(5):
    book_pairs = [books[i][j:j+2] for j in range(0, len(books[i])-1, 2)]
    decoded = "".join(homophonic_key.get(p, '?') for p in book_pairs)
    print(f"  Book {i+1}: {decoded[:80]}")

# Apply to NPC dialogues
print("\n--- Frequency-based decode of NPC dialogues ---")
for name, text in [("Knightmare", "347867090871097664346600345"),
                   ("Greeting 1", "485611800364197"),
                   ("Greeting 2", "78572611857643646724"),
                   ("Chayenne 1", chayenne1),
                   ("Chayenne 2", chayenne2)]:
    d_pairs = [text[j:j+2] for j in range(0, len(text)-1, 2)]
    decoded = "".join(homophonic_key.get(p, '?') for p in d_pairs)
    print(f"  {name:>12}: {decoded}")

# ============================================================
# 6. WHAT IF IT'S GERMAN? (CipSoft is German)
# ============================================================
print("\n" + "=" * 70)
print("6. GERMAN LANGUAGE FREQUENCY COMPARISON")
print("=" * 70)

GERMAN_FREQ = {
    'E': 16.4, 'N': 9.8, 'I': 7.6, 'S': 7.3, 'R': 7.0,
    'A': 6.5, 'T': 6.2, 'D': 5.1, 'H': 4.8, 'U': 4.3,
    'L': 3.4, 'C': 3.1, 'G': 3.0, 'M': 2.5, 'O': 2.5,
    'B': 1.9, 'W': 1.9, 'F': 1.7, 'K': 1.4, 'Z': 1.1,
    'P': 0.8, 'V': 0.7, 'J': 0.3, 'Y': 0.04, 'X': 0.03,
    'Q': 0.02
}

# Compare IC to German
# German IC ~ 0.0762 (higher than English 0.0667)
print("If the plaintext is GERMAN:")
print(f"  German IC ~ 0.0762 (vs English ~ 0.0667)")
print(f"  German has higher E frequency (16.4% vs 12.7%)")
print(f"  Our most frequent pair '19' appears 3.92%")
print(f"  If E needs ~16 codes: top 16 pairs should represent E")
print(f"  Sum of top 16 pair frequencies: {sum(c for _, c in pair_pcts[:16]):.1f}%")

# German frequency-based mapping
print("\n--- German frequency-based decode of Knightmare ---")
ger_sorted = sorted(GERMAN_FREQ.items(), key=lambda x: -x[1])
pair_idx = 0
german_key = {}
for letter, freq in ger_sorted:
    num_pairs = max(1, round(freq / 100 * len(pair_freq)))
    candidate_pairs = [p for p, _ in pair_pcts[pair_idx:pair_idx+num_pairs]]
    for p in candidate_pairs:
        german_key[p] = letter
    pair_idx += num_pairs

knightmare_pairs = ["34", "78", "67", "09", "08", "71", "09", "76", "64", "34", "66", "00", "03", "45"]
decoded_eng = "".join(homophonic_key.get(p, '?') for p in knightmare_pairs)
decoded_ger = "".join(german_key.get(p, '?') for p in knightmare_pairs)
print(f"  English freq decode: {decoded_eng}")
print(f"  German freq decode:  {decoded_ger}")
print(f"  Expected:            BE A WIT THAN BE A FOOL")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
