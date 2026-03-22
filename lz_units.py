"""
Tibia 469 - LZ Decomposition + Transition Chain Analysis
==========================================================
Key insights from previous analysis:
- 1->9 is dominant (43.5% of digits before 9 are 1)
- MI decays to ~0.08 by k=4, suggesting 2-4 digit code units
- No alignment preference rules out fixed-width codes
- 3 almost never followed by 2, 3, 7, 8, 9

Approach: Use LZ78-like decomposition to discover the natural "words"
(repeating units) in the digit sequence.
"""

import json
from collections import Counter, defaultdict

with open("books.json", "r") as f:
    books = json.load(f)

all_text = "".join(books)

print("=" * 70)
print("LZ DECOMPOSITION + TRANSITION CHAIN ANALYSIS")
print("=" * 70)

# ============================================================
# 1. LZ78-LIKE DICTIONARY BUILDING
# ============================================================
print("\n" + "=" * 70)
print("1. LZ78 DICTIONARY (natural encoding units)")
print("=" * 70)

def lz78_decompose(text, max_dict_size=5000):
    """Build LZ78 dictionary from text."""
    dictionary = {"": 0}
    next_code = 1
    entries = []  # (phrase, code)

    i = 0
    while i < len(text):
        # Find longest match in dictionary
        w = ""
        while i < len(text) and w + text[i] in dictionary:
            w += text[i]
            i += 1

        if i < len(text):
            new_phrase = w + text[i]
            if next_code < max_dict_size:
                dictionary[new_phrase] = next_code
                next_code += 1
            entries.append((w, text[i]))
            i += 1
        else:
            entries.append((w, ""))

    return dictionary, entries

dictionary, entries = lz78_decompose(all_text)

# What are the most common dictionary entries?
print(f"\nDictionary size: {len(dictionary)}")
print(f"Number of LZ78 steps: {len(entries)}")

# Count how often each dictionary entry is used
# Actually, let's look at the dictionary entries by length
dict_by_length = defaultdict(list)
for phrase in dictionary:
    if phrase:  # skip empty
        dict_by_length[len(phrase)].append(phrase)

print(f"\nDictionary entries by length:")
for length in sorted(dict_by_length.keys()):
    count = len(dict_by_length[length])
    print(f"  Length {length}: {count} entries")
    if length <= 4:
        # Show most frequent in the text
        freqs = [(phrase, all_text.count(phrase)) for phrase in dict_by_length[length]]
        freqs.sort(key=lambda x: -x[1])
        for phrase, freq in freqs[:10]:
            print(f"    '{phrase}': appears {freq}x in text")

# ============================================================
# 2. GREEDY LONGEST MATCH TOKENIZATION
# ============================================================
print("\n" + "=" * 70)
print("2. GREEDY TOKENIZATION (longest match)")
print("=" * 70)

# Build a token dictionary from the most frequent substrings
# of length 1-5

def build_token_dict(text, min_freq=10, max_len=6):
    """Build a dictionary of frequent substrings."""
    tokens = {}
    for length in range(max_len, 0, -1):
        freq = Counter()
        for i in range(len(text) - length + 1):
            sub = text[i:i+length]
            freq[sub] += 1

        for sub, count in freq.items():
            if count >= min_freq and sub not in tokens:
                tokens[sub] = count

    return tokens

token_dict = build_token_dict(all_text, min_freq=20, max_len=6)
print(f"Token dictionary: {len(token_dict)} entries")

# Sort by length descending, then by frequency
sorted_tokens = sorted(token_dict.items(), key=lambda x: (-len(x[0]), -x[1]))

print(f"\nLongest frequent tokens (min 20 occurrences):")
for token, freq in sorted_tokens[:40]:
    print(f"  '{token}' ({len(token)} digits): {freq}x")

# Tokenize the text using greedy longest match
def greedy_tokenize(text, token_list):
    """Tokenize text using greedy longest match."""
    # Sort tokens by length descending
    sorted_t = sorted(token_list, key=len, reverse=True)

    tokens = []
    i = 0
    while i < len(text):
        matched = False
        for t in sorted_t:
            if text[i:i+len(t)] == t:
                tokens.append(t)
                i += len(t)
                matched = True
                break
        if not matched:
            tokens.append(text[i])
            i += 1

    return tokens

# Use tokens of length >= 3 with freq >= 30
long_tokens = [t for t, f in token_dict.items() if len(t) >= 3 and f >= 30]
print(f"\nTokenizing with {len(long_tokens)} tokens (length >= 3, freq >= 30)")

tokens = greedy_tokenize(all_text, long_tokens)
print(f"Total tokens: {len(tokens)}")
print(f"Compression ratio: {len(all_text)} digits -> {len(tokens)} tokens = {len(all_text)/len(tokens):.2f}x")

token_freq_final = Counter(tokens)
print(f"\nTop 30 tokens after greedy tokenization:")
for token, count in token_freq_final.most_common(30):
    print(f"  '{token}' ({len(token)} digits): {count}x")

# Average token length
avg_token = sum(len(t) for t in tokens) / len(tokens)
print(f"\nAverage token length: {avg_token:.2f} digits")

# ============================================================
# 3. TRANSITION CHAIN CODES
# ============================================================
print("\n" + "=" * 70)
print("3. DOMINANT TRANSITION CHAINS")
print("=" * 70)

# From the transition analysis:
# 1->9 (23.4%), 9->5 (19.8%), 5->1 (25.9%) -> CYCLE: 1-9-5-1
# 2->1 (35.0%), 4->5 (25.4%), 7->2 (25.4%), 3->4 (27.8%)
# 8->0 (18.0%), 0->4 (19.2%), 6->4 (23.7%)

# The dominant cycle is 1->9->5->1
# This means "195", "951", "519" should be very common
print("\nDominant cycle 1-9-5:")
for seq in ['19', '95', '51', '195', '519', '951', '1951', '9519', '5195']:
    count = all_text.count(seq)
    print(f"  '{seq}': {count}x")

# The chain 3->4->5->1->9
print("\nChain 3-4-5-1-9:")
for seq in ['34', '45', '51', '19', '345', '451', '519', '3451', '4519', '34519']:
    count = all_text.count(seq)
    print(f"  '{seq}': {count}x")

# The chain 7->2->1->9
print("\nChain 7-2-1-9:")
for seq in ['72', '21', '19', '721', '219', '7219', '72189']:
    count = all_text.count(seq)
    print(f"  '{seq}': {count}x")

# The chain 8->0->4->5->1->9
print("\nChain 8-0-4-5-1-9:")
for seq in ['80', '04', '45', '804', '045', '8045', '80451']:
    count = all_text.count(seq)
    print(f"  '{seq}': {count}x")

# ============================================================
# 4. BYTE-PAIR ENCODING (BPE) APPROACH
# ============================================================
print("\n" + "=" * 70)
print("4. BYTE-PAIR ENCODING (iterative pair merging)")
print("=" * 70)

def bpe_decompose(text, num_merges=50):
    """Apply BPE to find natural groupings."""
    # Start with individual digits as tokens
    tokens = list(text)
    merge_history = []

    for step in range(num_merges):
        # Count adjacent pairs
        pair_freq = Counter()
        for i in range(len(tokens) - 1):
            pair_freq[(tokens[i], tokens[i+1])] += 1

        if not pair_freq:
            break

        # Find most frequent pair
        best_pair, best_count = pair_freq.most_common(1)[0]
        merged = best_pair[0] + best_pair[1]

        merge_history.append((best_pair, best_count, merged))

        # Merge this pair everywhere
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and tokens[i] == best_pair[0] and tokens[i+1] == best_pair[1]:
                new_tokens.append(merged)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1

        tokens = new_tokens

    return tokens, merge_history

print("\nRunning BPE (50 merges)...")
bpe_tokens, merge_history = bpe_decompose(all_text, 50)

print(f"\nMerge history (first 50 pairs merged):")
for i, (pair, count, merged) in enumerate(merge_history):
    print(f"  Step {i+1:2d}: '{pair[0]}' + '{pair[1]}' -> '{merged}' (appears {count}x)")

print(f"\nAfter 50 merges: {len(bpe_tokens)} tokens")
print(f"Token vocabulary: {len(set(bpe_tokens))} unique tokens")

# Token frequency
bpe_freq = Counter(bpe_tokens)
print(f"\nTop 30 BPE tokens:")
for token, count in bpe_freq.most_common(30):
    print(f"  '{token}' ({len(token)} digits): {count}x")

# Average token length after BPE
avg_bpe = sum(len(t) for t in bpe_tokens) / len(bpe_tokens)
print(f"\nAverage BPE token length: {avg_bpe:.2f} digits")

# ============================================================
# 5. TESTING IF BPE TOKENS COULD BE LETTERS
# ============================================================
print("\n" + "=" * 70)
print("5. BPE TOKEN ANALYSIS: COULD TOKENS BE LETTERS?")
print("=" * 70)

# In English, we'd expect ~26 tokens (letters) + maybe space
# After BPE, how many tokens account for most of the text?

cumulative = 0
total_bpe = len(bpe_tokens)
print("\nCumulative coverage by top N tokens:")
for i, (token, count) in enumerate(bpe_freq.most_common()):
    cumulative += count
    pct = cumulative / total_bpe * 100
    if (i + 1) in [5, 10, 15, 20, 25, 26, 30, 40, 50, 75, 100]:
        print(f"  Top {i+1:3d} tokens: {pct:5.1f}% of text ({cumulative}/{total_bpe})")

# Map top-N BPE tokens to English letters by frequency
ENGLISH_FREQ_ORDER = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

print("\n--- If top 26 BPE tokens = English letters (by frequency) ---")
bpe_mapping = {}
for i, (token, count) in enumerate(bpe_freq.most_common(26)):
    letter = ENGLISH_FREQ_ORDER[i]
    bpe_mapping[token] = letter
    print(f"  '{token}' ({count}x) = {letter} ({count/total_bpe*100:.1f}%)")

# Decode with this mapping
decoded_tokens = []
for token in bpe_tokens:
    if token in bpe_mapping:
        decoded_tokens.append(bpe_mapping[token])
    else:
        decoded_tokens.append('?')

decoded_bpe = "".join(decoded_tokens)
print(f"\nDecoded text (first 300 chars):")
print(f"  {decoded_bpe[:300]}")

# Check for common English words
common_words = ['THE', 'AND', 'OF', 'TO', 'IN', 'IS', 'IT', 'FOR', 'THAT',
                'WAS', 'ON', 'ARE', 'AS', 'WITH', 'HIS', 'THEY', 'AT', 'BE',
                'THIS', 'HAVE', 'FROM', 'OR', 'HAD', 'BY', 'HOT', 'BUT',
                'SOME', 'WHAT', 'THERE', 'WE', 'CAN', 'OUT', 'OTHER', 'ALL']

found_words = 0
for word in common_words:
    count = decoded_bpe.count(word)
    if count > 0:
        found_words += 1
        print(f"  Found '{word}': {count}x")

print(f"\n  English words found: {found_words}/{len(common_words)}")

# ============================================================
# 6. GERMAN FREQUENCY ORDER BPE MAPPING
# ============================================================
print("\n" + "=" * 70)
print("6. GERMAN FREQUENCY ORDER BPE MAPPING")
print("=" * 70)

GERMAN_FREQ_ORDER = 'ENISRATDHULCGMOBWFKZPVJYXQ'

bpe_mapping_de = {}
for i, (token, count) in enumerate(bpe_freq.most_common(26)):
    letter = GERMAN_FREQ_ORDER[i]
    bpe_mapping_de[token] = letter

decoded_de = []
for token in bpe_tokens:
    if token in bpe_mapping_de:
        decoded_de.append(bpe_mapping_de[token])
    else:
        decoded_de.append('?')

decoded_de_text = "".join(decoded_de)
print(f"\nGerman-mapped (first 300 chars):")
print(f"  {decoded_de_text[:300]}")

german_words = ['DER', 'DIE', 'UND', 'DEN', 'DAS', 'IST', 'EIN', 'AUF',
                'DES', 'MIT', 'ICH', 'SIE', 'VON', 'ZUR', 'HAT', 'WIR',
                'FUR', 'VOR', 'ZUM', 'BEI', 'MAN', 'NUR', 'WAS', 'ORT',
                'AUS', 'ALS', 'WER', 'DAR', 'NICHT', 'SICH', 'EINE',
                'UBER', 'NOCH', 'NACH', 'KEIN', 'MUSS']

found_de = 0
for word in german_words:
    count = decoded_de_text.count(word)
    if count > 0:
        found_de += 1
        print(f"  Found '{word}': {count}x")

print(f"\n  German words found: {found_de}/{len(german_words)}")

# ============================================================
# 7. NPC DIALOGUE BPE ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("7. NPC DIALOGUE BPE TOKENIZATION")
print("=" * 70)

npc_texts = {
    "Knightmare": "347867090871097664346600345",
    "Greeting 1": "485611800364197",
    "Greeting 2": "78572611857643646724",
    "Chayenne":   "114514519485611451908304576512282177",
}

for name, npc_text in npc_texts.items():
    # Tokenize with BPE vocabulary
    npc_bpe, _ = bpe_decompose(npc_text, 50)

    # Map to English
    decoded_npc_en = "".join(bpe_mapping.get(t, '?') for t in npc_bpe)
    decoded_npc_de = "".join(bpe_mapping_de.get(t, '?') for t in npc_bpe)

    print(f"\n  {name}: '{npc_text}'")
    print(f"    BPE tokens: {npc_bpe}")
    print(f"    English map: {decoded_npc_en}")
    print(f"    German map:  {decoded_npc_de}")

# ============================================================
# 8. LOOKING FOR "THE" (most common English word)
# ============================================================
print("\n" + "=" * 70)
print("8. SEARCHING FOR 'THE' - MOST COMMON ENGLISH WORD")
print("=" * 70)

# 'THE' should appear ~7% of all words in English text
# If the text is ~6216 unique digits encoding ~3885 letters (~1.6 d/l)
# That's roughly 777 words (avg 5 letters/word)
# 'THE' should appear ~54 times

# What 3-token (or 3-BPE-unit) sequence appears most often?
token_trigrams = Counter()
for i in range(len(bpe_tokens) - 2):
    token_trigrams[(bpe_tokens[i], bpe_tokens[i+1], bpe_tokens[i+2])] += 1

print("\nMost common 3-token sequences (potential 'THE', 'AND', etc.):")
for trigram, count in token_trigrams.most_common(20):
    combined = "".join(trigram)
    print(f"  {trigram} -> '{combined}' ({len(combined)} digits): {count}x")

# 2-token sequences (potential 'OF', 'TO', 'IN', etc.)
token_bigrams = Counter()
for i in range(len(bpe_tokens) - 1):
    token_bigrams[(bpe_tokens[i], bpe_tokens[i+1])] += 1

print("\nMost common 2-token sequences:")
for bigram, count in token_bigrams.most_common(20):
    combined = "".join(bigram)
    print(f"  {bigram} -> '{combined}' ({len(combined)} digits): {count}x")

# ============================================================
# 9. COMPRESSION RATIO AS LANGUAGE INDICATOR
# ============================================================
print("\n" + "=" * 70)
print("9. COMPRESSION CHARACTERISTICS")
print("=" * 70)

# Generate random digit strings of same length and compare compression
import random
random.seed(42)

# Original text compression (using BPE as proxy)
orig_ratio = len(all_text) / len(bpe_tokens)

# Random text compression
random_text = "".join(str(random.randint(0, 9)) for _ in range(len(all_text)))
random_bpe, _ = bpe_decompose(random_text, 50)
random_ratio = len(random_text) / len(random_bpe)

# English-frequency biased random
eng_weights = [7.59, 16.59, 8.39, 5.78, 11.28, 12.94, 10.08, 8.51, 9.92, 8.92]
total_w = sum(eng_weights)
eng_probs = [w/total_w for w in eng_weights]
biased_text = "".join(str(random.choices(range(10), weights=eng_probs, k=1)[0])
                       for _ in range(len(all_text)))
biased_bpe, _ = bpe_decompose(biased_text, 50)
biased_ratio = len(biased_text) / len(biased_bpe)

print(f"\n  BPE compression ratios (50 merges):")
print(f"    Original 469 text:    {orig_ratio:.3f}x")
print(f"    Uniform random:       {random_ratio:.3f}x")
print(f"    Frequency-biased random: {biased_ratio:.3f}x")
print(f"\n  Original compresses {'better' if orig_ratio > biased_ratio else 'worse'} "
      f"than frequency-biased random")
print(f"  This {'suggests' if orig_ratio > biased_ratio * 1.1 else 'does not strongly suggest'} "
      f"additional structure beyond frequency bias")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
