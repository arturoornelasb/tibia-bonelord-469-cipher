"""
Tibia 469 - Score Knightmare Crib Solutions Against Book Text
==============================================================
We found 4,924 ways to split the Knightmare cipher into groups.
Now we apply each mapping to the books and score which produces
the most English-like (or German-like) text.

This is the key insight: many mappings are consistent with ONE
crib, but only the CORRECT mapping will produce coherent text
when applied to other data.
"""

import json
from collections import Counter, defaultdict

with open("books.json", "r") as f:
    books = json.load(f)

all_text = "".join(books)

# English bigram log-frequencies for scoring
COMMON_BIGRAMS = {
    'TH': 3.56, 'HE': 3.07, 'IN': 2.43, 'ER': 2.05, 'AN': 1.99,
    'RE': 1.85, 'ON': 1.76, 'AT': 1.49, 'EN': 1.45, 'ND': 1.35,
    'TI': 1.34, 'ES': 1.34, 'OR': 1.28, 'TE': 1.27, 'OF': 1.17,
    'ED': 1.17, 'IS': 1.13, 'IT': 1.12, 'AL': 1.09, 'AR': 1.07,
    'ST': 1.05, 'TO': 1.05, 'NT': 1.04, 'NG': 0.95, 'SE': 0.93,
    'HA': 0.93, 'AS': 0.87, 'OU': 0.87, 'IO': 0.83, 'LE': 0.83,
    'VE': 0.83, 'CO': 0.79, 'ME': 0.79, 'DE': 0.76, 'HI': 0.76,
    'RI': 0.73, 'RO': 0.73, 'IC': 0.70, 'NE': 0.69, 'EA': 0.69,
    'RA': 0.69, 'CE': 0.65, 'LI': 0.62, 'CH': 0.60, 'LL': 0.58,
    'BE': 0.58, 'MA': 0.57, 'SI': 0.55, 'OM': 0.55, 'UR': 0.54,
}

ENGLISH_FREQ = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0,
    'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3,
    'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4, 'W': 2.4,
    'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5,
    'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15, 'Q': 0.10,
    'Z': 0.07
}


def find_splits(cipher, plain, pos_c=0, pos_p=0, current_mapping=None, current_split=None):
    """Find all consistent ways to split cipher digits into groups matching plaintext letters."""
    if current_mapping is None:
        current_mapping = {}
    if current_split is None:
        current_split = []

    if pos_p == len(plain):
        if pos_c == len(cipher):
            return [(dict(current_mapping), list(current_split))]
        return []

    if pos_c >= len(cipher):
        return []

    results = []
    for width in [1, 2, 3]:
        if pos_c + width > len(cipher):
            continue
        code = cipher[pos_c:pos_c + width]
        letter = plain[pos_p]

        if code in current_mapping and current_mapping[code] != letter:
            continue

        new_mapping = dict(current_mapping)
        new_mapping[code] = letter
        new_split = current_split + [code]

        results.extend(find_splits(cipher, plain, pos_c + width, pos_p + 1,
                                   new_mapping, new_split))
    return results


def decode_variable(text, mapping):
    """Decode text using variable-length mapping. Greedy longest-match."""
    result = []
    i = 0
    unmapped = 0
    # Sort codes by length descending for greedy matching
    sorted_codes = sorted(mapping.keys(), key=len, reverse=True)

    while i < len(text):
        matched = False
        for code in sorted_codes:
            if text[i:i + len(code)] == code:
                result.append(mapping[code])
                i += len(code)
                matched = True
                break
        if not matched:
            result.append('?')
            i += 1
            unmapped += 1

    return "".join(result), unmapped


def score_text(text):
    """Score text by English-likeness."""
    text = text.upper()
    score = 0.0
    alpha = [c for c in text if c.isalpha()]
    if len(alpha) < 5:
        return -999999

    # Bigram scoring
    for i in range(len(text) - 1):
        bi = text[i:i + 2]
        if bi in COMMON_BIGRAMS:
            score += COMMON_BIGRAMS[bi]

    # Letter frequency match
    counts = Counter(alpha)
    total = len(alpha)
    for letter, expected in ENGLISH_FREQ.items():
        observed = counts.get(letter, 0) / total * 100
        score -= abs(observed - expected) * 0.5

    # Penalty for ? (unmapped characters)
    q_count = text.count('?')
    score -= q_count * 2

    return score


print("=" * 70)
print("SCORING KNIGHTMARE CRIB SOLUTIONS AGAINST BOOK TEXT")
print("=" * 70)

# Generate all solutions
cipher = "347867090871097664346600345"
plain = "BEAWITTHANBEAFOOL"

print(f"\nGenerating all consistent splits...")
solutions = find_splits(cipher, plain)
print(f"Found {len(solutions)} solutions")

# Filter: only keep solutions where single-digit codes exist
# (the variable-length theory is most promising)
print(f"\nFiltering solutions...")

# Score each solution against a sample of book text
# Use merged chain as the test text for better signal
sample = all_text[:2000]

print(f"Scoring {len(solutions)} solutions against first 2000 digits...")
print(f"(this may take a moment)\n")

scored = []
for idx, (mapping, split) in enumerate(solutions):
    decoded, unmapped = decode_variable(sample, mapping)
    s = score_text(decoded)
    scored.append((s, idx, mapping, split, decoded, unmapped))

# Sort by score descending
scored.sort(key=lambda x: -x[0])

print(f"{'Rank':>4} {'Score':>8} {'Unmapped':>8} | Mapping Summary")
print("-" * 80)

for rank, (score, idx, mapping, split, decoded, unmapped) in enumerate(scored[:30]):
    # Summarize mapping
    inv = defaultdict(list)
    for code, letter in sorted(mapping.items()):
        inv[letter].append(code)
    map_str = " ".join(f"{l}={','.join(codes)}" for l, codes in sorted(inv.items()))
    print(f"  {rank + 1:3d}  {score:8.1f}  {unmapped:6d}   | {map_str[:60]}")

# Show decoded text for top 5
print("\n" + "=" * 70)
print("TOP 5 SOLUTIONS - DECODED TEXT")
print("=" * 70)

for rank in range(min(5, len(scored))):
    score, idx, mapping, split, decoded, unmapped = scored[rank]
    print(f"\n--- Rank {rank + 1} (score: {score:.1f}, unmapped: {unmapped}) ---")

    # Show mapping
    inv = defaultdict(list)
    for code, letter in sorted(mapping.items()):
        inv[letter].append(code)
    print(f"  Mapping:")
    for letter in sorted(inv.keys()):
        codes = inv[letter]
        print(f"    {letter}: {', '.join(codes)}")

    print(f"\n  Decoded (first 300 chars):")
    print(f"    {decoded[:300]}")

    # Decode NPC dialogues
    print(f"\n  NPC Dialogues:")
    for name, text in [("Greeting 1", "485611800364197"),
                       ("Greeting 2", "78572611857643646724"),
                       ("Chayenne 1", "114514519485611451908304576512282177")]:
        d, u = decode_variable(text, mapping)
        print(f"    {name}: {d}")

    # Decode individual books
    print(f"\n  Books (first 60 chars):")
    for bi in range(5):
        d, u = decode_variable(books[bi], mapping)
        print(f"    Book {bi + 1}: {d[:60]}")

# ============================================================
# Try adding the bonelord greeting as a second crib
# ============================================================
print("\n" + "=" * 70)
print("EXTENDED CRIB: COMBINING KNIGHTMARE + GREETING")
print("=" * 70)

# The Wrinkled Bonelord says "485611800364197" as greeting
# If this means "GREETINGS" (9 letters, 15 digits = 1.67 digits/letter)
# or "WELCOME" (7 letters, 15 digits = 2.14)
# or another word

# For each top Knightmare solution, check if the greeting
# can consistently decode to a common word

print("\nFor top 10 Knightmare solutions, trying greeting words...")

greeting = "485611800364197"
greeting_candidates = [
    "GREETINGS", "WELCOME", "HELLO", "HELLOWORLD",
    "GREETINGSSS", "IAMLIBRARIAN", "WHATDOYOUWANT",
    "CANYOUHELP", "GREETINGSS", "AHGREETINGS",
    "WELCOMEGUEST", "LIBRARYOPEN"
]

for rank in range(min(10, len(scored))):
    score, idx, mapping, split, decoded, unmapped = scored[rank]

    print(f"\n  Rank {rank + 1} Knightmare solution:")

    # First, decode greeting with existing mapping
    g_decoded, g_unmapped = decode_variable(greeting, mapping)
    print(f"    Greeting decoded with Knightmare key: '{g_decoded}' (unmapped: {g_unmapped})")

    # Try extending the mapping with greeting candidates
    for word in greeting_candidates:
        if len(word) < 5 or len(word) > 15:
            continue
        extended_solutions = find_splits(greeting, word)
        for ext_mapping, ext_split in extended_solutions[:3]:
            # Check consistency with Knightmare mapping
            consistent = True
            for code, letter in ext_mapping.items():
                if code in mapping and mapping[code] != letter:
                    consistent = False
                    break
            if consistent:
                # Merge mappings
                merged = dict(mapping)
                merged.update(ext_mapping)
                # Score the merged mapping
                d, u = decode_variable(sample, merged)
                s = score_text(d)
                if s > score * 0.8:  # At least 80% as good
                    print(f"    + Greeting='{word}': score={s:.1f}, merged codes: {len(merged)}")
                    # Show the decoded text
                    print(f"      Text: {d[:100]}")

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
