"""
Constraint-based cracking: focus on recurring patterns that MUST be German words.
Use the 16 confirmed codes plus linguistic constraints to determine more codes.

Key recurring patterns to crack:
1. Pre-STEIN: codes 95,61,51,35,34,78,01 -> E,U,?,?,?,?,? followed by STEIN
2. DIERELGERGENNERNNDE: codes 45,21,76,52,19,72,78,30,46,48,76,51,59,56,46,11,41,45,19
3. Post-STEIN: codes 19,93,64,67,24,31,42,78
"""
import json
from collections import Counter
from itertools import product

with open('books.json', 'r') as f:
    books = json.load(f)

with open('best_mapping.json', 'r') as f:
    mapping = json.load(f)

confirmed = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U',
}

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

# Get all pairs per book
book_data = []
for i, book in enumerate(books):
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_data.append((off, pairs))

all_pairs = []
for _, pairs in book_data:
    all_pairs.extend(pairs)
pair_counts = Counter(all_pairs)

print("=" * 70, flush=True)
print("1. ANALYZE PRE-STEIN CONTEXT IN DETAIL", flush=True)
print("=" * 70, flush=True)

# Find all STEIN occurrences and their full context
stein_contexts = []
for bi, (off, pairs) in enumerate(book_data):
    for pi in range(len(pairs) - 4):
        if (pairs[pi] == '92' and pairs[pi+1] == '88' and
            pairs[pi+2] == '95' and pairs[pi+3] == '21' and
            pairs[pi+4] == '60'):
            # Get 15 pairs before and 15 after
            before = pairs[max(0, pi-15):pi]
            after = pairs[pi+5:min(len(pairs), pi+20)]
            stein_contexts.append((bi, pi, before, after))

print(f"Found {len(stein_contexts)} STEIN occurrences", flush=True)

# Show the consistent pre-STEIN codes
for bi, pi, before, after in stein_contexts[:5]:
    before_decoded = ''.join(confirmed.get(p, f'({p})') for p in before)
    after_decoded = ''.join(confirmed.get(p, f'({p})') for p in after)
    print(f"\n  Book {bi} at pair {pi}:", flush=True)
    print(f"    Before: {before}", flush=True)
    print(f"    Before decoded: {before_decoded}", flush=True)
    print(f"    After:  {after}", flush=True)
    print(f"    After decoded:  {after_decoded}", flush=True)

# The consistent pre-STEIN pattern is: ...,95,61,51,35,34,78,01,92,88,95,21,60
# = E, U, [51], [35], [34], [78], [01], S, T, E, I, N
# What 7-letter pattern fits: E U ? ? ? ? ? S T E I N ?

# Let me check what comes BEFORE the E,U
print(f"\n\nPre-EU codes (before 95,61):", flush=True)
pre_eu_codes = Counter()
for bi, pi, before, after in stein_contexts:
    if pi >= 9:
        # Go further back
        _, all_p = book_data[bi]
        pre = all_p[max(0, pi-9):pi-7]  # 2 codes before the 95,61
    if len(before) >= 9:
        for k in range(len(before) - 7):
            pre_eu_codes[before[k]] += 1
        # The 2 codes right before 95,61
        if len(before) >= 8:
            print(f"  Book {bi}: ...{before[-9:-7]} then {before[-7:]} STEIN", flush=True)

# What are the exact pre-STEIN codes?
print(f"\n\nCodes immediately before STEIN (7 positions):", flush=True)
pre_stein_counter = [Counter() for _ in range(7)]
for bi, pi, before, after in stein_contexts:
    if len(before) >= 7:
        for k in range(7):
            pre_stein_counter[k][before[-(7-k)]] += 1

for k in range(7):
    code = pre_stein_counter[k].most_common(1)[0] if pre_stein_counter[k] else ('??', 0)
    fixed = "FIXED" if code[0] in confirmed else "free"
    decoded = confirmed.get(code[0], '?')
    print(f"  Position -{7-k}: code {code[0]} ({code[1]}/{len(stein_contexts)} times) -> {decoded} ({fixed})", flush=True)

# Even further back
print(f"\n\nCodes at positions -15 to -8 before STEIN:", flush=True)
far_pre_stein = [Counter() for _ in range(8)]
for bi, pi, before, after in stein_contexts:
    if len(before) >= 15:
        for k in range(8):
            far_pre_stein[k][before[-(15-k)]] += 1

for k in range(8):
    mc = far_pre_stein[k].most_common(3)
    print(f"  Position -{15-k}: {mc}", flush=True)


print(f"\n\n{'='*70}", flush=True)
print("2. ANALYZE POST-STEIN CONTEXT", flush=True)
print("=" * 70, flush=True)

post_stein_counter = [Counter() for _ in range(15)]
for bi, pi, before, after in stein_contexts:
    for k in range(min(15, len(after))):
        post_stein_counter[k][after[k]] += 1

for k in range(15):
    mc = post_stein_counter[k].most_common(3)
    if mc:
        fixed = "FIXED" if mc[0][0] in confirmed else "free"
        decoded = confirmed.get(mc[0][0], '?')
        print(f"  Position +{k}: {mc} -> dominant={decoded} ({fixed})", flush=True)


print(f"\n\n{'='*70}", flush=True)
print("3. CRACK THE RECURRING 19-PAIR PATTERN", flush=True)
print("=" * 70, flush=True)

# The pattern from DIERELGERGENNERNNDE
# Codes: 45,21,76,52,19,72,78,30,46,48,76,51,59,56,46,11,41,45,19
target_codes = ['45','21','76','52','19','72','78','30','46','48','76','51','59','56','46','11','41','45','19']
print(f"Target code sequence: {target_codes}", flush=True)

# Show confirmed vs free
for i, c in enumerate(target_codes):
    if c in confirmed:
        print(f"  [{i}] {c} -> {confirmed[c]} (FIXED)", flush=True)
    else:
        print(f"  [{i}] {c} -> ? (free)", flush=True)

# The pattern with confirmed codes filled in:
# 45=D, 21=I, 76=?, 52=?, 19=E, 72=?, 78=?, 30=?, 46=?, 48=?, 76=?, 51=?, 59=?, 56=E, 46=?, 11=N, 41=?, 45=D, 19=E
pattern = []
free_positions = []
for i, c in enumerate(target_codes):
    if c in confirmed:
        pattern.append(confirmed[c])
    else:
        pattern.append('?')
        if c not in [target_codes[j] for j in range(i) if target_codes[j] not in confirmed]:
            free_positions.append((i, c))

print(f"\nPattern: {''.join(pattern)}", flush=True)
print(f"Free codes in pattern: {[(c, [i for i,tc in enumerate(target_codes) if tc == c]) for _, c in free_positions]}", flush=True)

# Find what comes before and after this pattern in each book
print(f"\n\nFull context around the recurring pattern:", flush=True)
for bi, (off, pairs) in enumerate(book_data):
    decoded = ''.join(confirmed.get(p, '?') for p in pairs)
    # Search for the target code sequence
    for pi in range(len(pairs) - len(target_codes) + 1):
        if pairs[pi:pi+len(target_codes)] == target_codes:
            ctx_start = max(0, pi - 5)
            ctx_end = min(len(pairs), pi + len(target_codes) + 5)
            ctx_pairs = pairs[ctx_start:ctx_end]
            ctx_decoded = ''.join(confirmed.get(p, '?') for p in ctx_pairs)
            print(f"  Book {bi} pos {pi}: {ctx_decoded}", flush=True)
            if bi > 8:
                break
    else:
        continue
    if bi > 8:
        break


print(f"\n\n{'='*70}", flush=True)
print("4. FREQUENCY-CONSTRAINED CODE ENUMERATION", flush=True)
print("=" * 70, flush=True)

# How many codes should each letter have?
# Based on German frequencies and 98 unique codes:
german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
    'Q': 0.001
}

total_pairs = sum(pair_counts.values())
print(f"Total pair occurrences: {total_pairs}", flush=True)
print(f"Unique codes: {len(pair_counts)}", flush=True)

# Expected number of codes per letter
print(f"\nExpected code count per letter (98 codes total):", flush=True)
for letter in sorted(german_freq, key=lambda l: -german_freq[l]):
    expected_codes = german_freq[letter] * 98
    # How many confirmed codes does this letter have?
    confirmed_count = sum(1 for c, l in confirmed.items() if l == letter)
    print(f"  {letter}: ~{expected_codes:.1f} codes (have {confirmed_count} confirmed)", flush=True)


print(f"\n\n{'='*70}", flush=True)
print("5. BIGRAM ANALYSIS OF CONFIRMED PAIRS", flush=True)
print("=" * 70, flush=True)

# For each free code, what confirmed codes appear before/after it?
# This gives us bigram constraints
free_codes_set = set(pair_counts.keys()) - set(confirmed.keys())
print(f"Free codes: {len(free_codes_set)}", flush=True)

# Build bigram contexts for free codes
code_left_context = {}  # free_code -> Counter of (confirmed_code, letter) before it
code_right_context = {}  # free_code -> Counter of (confirmed_code, letter) after it

for _, pairs in book_data:
    for i in range(len(pairs) - 1):
        c1, c2 = pairs[i], pairs[i+1]
        if c2 in free_codes_set and c1 in confirmed:
            if c2 not in code_left_context:
                code_left_context[c2] = Counter()
            code_left_context[c2][confirmed[c1]] += 1
        if c1 in free_codes_set and c2 in confirmed:
            if c1 not in code_right_context:
                code_right_context[c1] = Counter()
            code_right_context[c1][confirmed[c2]] += 1

# German bigram frequencies (most common)
common_bigrams = {
    'EN', 'ER', 'CH', 'DE', 'EI', 'ND', 'TE', 'IN', 'IE', 'GE',
    'ES', 'NE', 'SE', 'RE', 'HE', 'AN', 'UN', 'ST', 'BE', 'DI',
    'EM', 'AU', 'SS', 'SC', 'DA', 'SI', 'LE', 'IC', 'TI', 'AL',
    'HA', 'NG', 'WE', 'EL', 'HI', 'NS', 'NT', 'IS', 'HT', 'MI'
}

impossible_bigrams = {
    'QX', 'XQ', 'QZ', 'ZQ', 'QJ', 'JQ', 'XJ', 'JX',
}

# For codes with strong bigram context, infer likely letter
print(f"\nFree codes with strong confirmed-neighbor context:", flush=True)
for code in sorted(free_codes_set, key=lambda c: -pair_counts.get(c, 0)):
    freq = pair_counts.get(code, 0)
    if freq < 5:
        continue
    left = code_left_context.get(code, Counter())
    right = code_right_context.get(code, Counter())

    if left or right:
        # For each candidate letter, count how many valid bigrams it forms
        scores = {}
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            good = 0
            bad = 0
            for l_letter, l_count in left.items():
                bg = l_letter + letter
                if bg in common_bigrams:
                    good += l_count * 2
                elif bg in impossible_bigrams:
                    bad += l_count * 10
            for r_letter, r_count in right.items():
                bg = letter + r_letter
                if bg in common_bigrams:
                    good += r_count * 2
                elif bg in impossible_bigrams:
                    bad += r_count * 10
            scores[letter] = good - bad

        best = sorted(scores.items(), key=lambda x: -x[1])[:5]
        left_top = left.most_common(3)
        right_top = right.most_common(3)

        if best[0][1] > 10:  # Only show if strong signal
            print(f"\n  Code {code} (freq={freq}):", flush=True)
            print(f"    Left context:  {left_top}", flush=True)
            print(f"    Right context: {right_top}", flush=True)
            print(f"    Best letters:  {best}", flush=True)


print(f"\n\n{'='*70}", flush=True)
print("6. WHAT IS 'E U [51] [35] [34] [78] [01] STEIN'?", flush=True)
print("=" * 70, flush=True)

# Codes: 51, 35, 34, 78, 01
# These 5 codes make up positions 3-7 before STEIN
# Full: E U [51] [35] [34] [78] [01] S T E I N

# What are the frequencies of these codes?
for c in ['51', '35', '34', '78', '01']:
    freq = pair_counts.get(c, 0)
    pct = freq / total_pairs * 100
    left = code_left_context.get(c, Counter())
    right = code_right_context.get(c, Counter())
    print(f"  Code {c}: freq={freq} ({pct:.2f}%), left={left.most_common(3)}, right={right.most_common(3)}", flush=True)

# The pre-STEIN pattern is E,U,a,b,c,d,e where a=51, b=35, c=34, d=78, e=01
# And then S,T,E,I,N follows
# German words: What 12-letter German word/phrase fits _EU?????STEIN_?

# Consider:
# FEUERSTEIN (flint) = F,E,U,E,R,S,T,E,I,N - 10 letters
# That would need one extra code before 95 to be F
# And 51=E, 35=R, and then 34,78,01 need to be something...
# Wait: F,E,U,E,R,S,T,E,I,N
# If the F is BEFORE the 95:
#   [F_code],95=E,61=U,51=E,35=R,STEIN -> but that's only 4 free codes, not 5

# ABENTEUERSTEIN? Too long
# Let me think... what if there's a word boundary?
# ...E | U[51][35][34] | [78][01]STEIN

# German "und" patterns:
# ...E UND STEIN? That's E, U, N, D, S, T, E, I, N
# 51=N, 35=D -> UND then 34,78,01 before STEIN

# UND ...STEIN patterns:
# UND GESTEIN (and rock)?  That would be U,N,D,G,E,S,T,E,I,N  34=G,78=E,01=?
# But we have 95=E already, so 78=E is possible (homophonic)
# UND GESTEIN: 61=U,51=N,35=D,34=G,78=E,01=S  ... but then the S would be before STEIN codes
# Actually the next codes are 92=S, so 01 can't be S (duplicate)

# Wait, let me reconsider the actual sequence:
# 95, 61, 51, 35, 34, 78, 01, 92, 88, 95, 21, 60
# E,  U,  ?,  ?,  ?,  ?,  ?,  S,  T,  E,  I,  N

# If 51=N, 35=D → "E U N D ? ? ? STEIN"
# What 3-letter word + STEIN? DARSTEIN? No.
# DES STEIN? "E UND ES STEIN" = E,U,N,D,E,S,STEIN
# But that needs 34=E,78=S and 01 is left over before 92=S

# Hmm. Let me try: what if there's no word at all?
# In Tibia lore, maybe this is a specific word/name?

# Let me try all plausible German segments:
print(f"\nTrying German phrase patterns for E U _ _ _ _ _ S T E I N:", flush=True)

# Pattern: E U a b c d e S T E I N
# Where a=code51, b=code35, c=code34, d=code78, e=code01
# Possibilities:
candidates = [
    # word boundary between E and U
    ("E UNTERSТEIN", "E UNTERSTEIN", {'51':'N', '35':'T', '34':'E', '78':'R', '01':'S'}),  # no, 01=S conflicts with 92=S... actually homophonic is OK
    # Compound: EU + NACHTSTEIN
    ("EU NACHTSTEIN", "", {'51':'N', '35':'A', '34':'C', '78':'H', '01':'T'}),  # but 18=C confirmed
    # Phrase: EUCH ... STEIN
    # UND STEIN with preceding text
    ("...E UND GESTEIN", "", {'51':'N', '35':'D', '34':'G', '78':'E', '01':'S'}),
    # FEUERSTEIN: need F before E
    # RUNENSTEINEN: R,U,N,E,N,S,T,E,I,N,E,N  - 12 letters!
    # E,U,[N],[E],[N],[S],[T],S,T,E,I,N  - but that's EUNENST-STEIN which makes no sense
    # Actually: R-U-N-E-N-S-T-E-I-N-E-N
    # If the E before is actually part of previous word, and U starts RUNENSTEINEN:
    # Nope, R would need to come before U
]

# Actually - RUNENSTEINEN is 12 letters: R,U,N,E,N,S,T,E,I,N,E,N
# Our sequence from EU onward: U,a,b,c,d,e,S,T,E,I,N = 11 positions starting from U
# RUNENSTEINEN starting from U: U,N,E,N,S,T,E,I,N,E,N = 11 letters
# Match: 51=N, 35=E, 34=N, 78=S, 01=T
# Then after STEIN: the next codes should be E,N
# Let's check: RUNENSTEINEN: ...S,T,E,I,N,E,N
# Our STEIN = 92,88,95,21,60 = S,T,E,I,N
# Then next should be E,N
# From trace: after STEIN, codes are 19,93,... and 19=E(confirmed), 93=?
# If 93=N then we get RUNENSTEINEN!

# Check if this is consistent
print(f"\n  Hypothesis: RUNENSTEINEN", flush=True)
print(f"  R,U,N,E,N,S,T,E,I,N,E,N", flush=True)
print(f"  The 'R' would be from the code before 95(E)", flush=True)
print(f"  Mapping: 51=N, 35=E, 34=N, 78=S, 01=T", flush=True)
print(f"  Post-STEIN: 19=E(confirmed!), 93 should be N", flush=True)

# Check: is code before 95 consistent across STEIN occurrences?
pre_95_code = Counter()
for bi, pi, before, after in stein_contexts:
    if len(before) >= 8:
        pre_95_code[before[-8]] += 1

print(f"\n  Code at position -8 (should be R for RUNENSTEINEN): {pre_95_code.most_common(5)}", flush=True)

# Check what 93 currently maps to
print(f"  Code 93 frequency: {pair_counts.get('93', 0)}", flush=True)
print(f"  Code 93 right context: {code_right_context.get('93', Counter()).most_common(5)}", flush=True)
print(f"  Code 93 left context: {code_left_context.get('93', Counter()).most_common(5)}", flush=True)

# Also check: 51 appears elsewhere - if 51=N, does it form good bigrams?
# And 35=E, 34=N etc.
print(f"\n  Checking RUNENSTEINEN hypothesis consistency:", flush=True)
hypothesis = {'51': 'N', '35': 'E', '34': 'N', '78': 'S', '01': 'T', '93': 'N'}
for c, l in hypothesis.items():
    freq = pair_counts.get(c, 0)
    left = code_left_context.get(c, Counter())
    right = code_right_context.get(c, Counter())
    left_str = ', '.join(f'{ll}{l}({n})' for ll, n in left.most_common(5))
    right_str = ', '.join(f'{l}{rl}({n})' for rl, n in right.most_common(5))
    print(f"  Code {c} -> {l} (freq {freq}): left bigrams: {left_str}", flush=True)
    print(f"         right bigrams: {right_str}", flush=True)


print(f"\n\n{'='*70}", flush=True)
print("7. WHAT DOES DIERELGERGENNERNNDE BECOME?", flush=True)
print("=" * 70, flush=True)

# Pattern codes: 45,21,76,52,19,72,78,30,46,48,76,51,59,56,46,11,41,45,19
# With confirmed: D,I,?,?,E,?,?,?,?,?,?,?,?,E,?,N,?,D,E
# With RUNENSTEINEN hypothesis (51=N, 78=S):
#                  D,I,?,?,E,?,S,?,?,?,?,N,?,E,?,N,?,D,E

# Free codes in this pattern: 76, 52, 72, 30, 46, 48, 59, 41
# 76 appears twice (positions 2 and 10)

hypo_map = dict(confirmed)
for c, l in hypothesis.items():
    hypo_map[c] = l

pattern_decoded = ''.join(hypo_map.get(c, '?') for c in target_codes)
print(f"Pattern with hypothesis: {pattern_decoded}", flush=True)
print(f"Free codes remaining: 76, 52, 72, 30, 46, 48, 59, 41", flush=True)

# This 19-char pattern appears in 13 books, so it's a real phrase
# DI??E?S???N?EN?NDE  -- what German phrase is this?
# With ? filled in it should be readable German

# Frequency of each free code in pattern:
for c in ['76', '52', '72', '30', '46', '48', '59', '41']:
    freq = pair_counts.get(c, 0)
    left = code_left_context.get(c, Counter())
    right = code_right_context.get(c, Counter())
    print(f"  Code {c} (freq {freq}): left={left.most_common(3)}, right={right.most_common(3)}", flush=True)

# Try to read it as German:
# D I [76] [52] E [72] S [30] [46] [48] [76] N [59] E [46] N [41] D E
# Pattern: DI_?E_S__?_N_E_N_DE
# What if it's: "DIE [52]E[72]S[30][46][48][76]N[59]E[46]N[41]DE"
# Or: "DIESES ..." wait
# DI[76][52]E → could be DIESE (this) if 76=E, 52=S → DIESE
# Then: DIESE [72]S[30][46][48] [76=E]N[59]E[46]N[41]DE

# If 76=E, 52=S:
# D,I,E,S,E,?,S,?,?,?,E,N,?,E,?,N,?,D,E
# DIESE?S???EN?E?N?DE
# What is: "DIESER [S30][46][48]EN[59]E[46]N[41]DE"?

# Wait: "DIESER" = D,I,E,S,E,R → 72=R!
# Then: DIESER S[30][46][48]EN[59]E[46]N[41]DE
# = DIESES[30][46][48]EN?E?N?DE  no wait...
# = D,I,E,S,E,R,S,?,?,?,E,N,?,E,?,N,?,D,E
# DIESERS???EN?E?N?DE
# Hmm DIESERS isn't German. But DIESER followed by S...
# Could be word boundary: DIESER S[30][46][48]EN[59]E[46]N[41]DE

# Actually I miscounted. Let me be careful:
# Position 0: 45=D
# Position 1: 21=I
# Position 2: 76=?
# Position 3: 52=?
# Position 4: 19=E
# Position 5: 72=?
# Position 6: 78=S (from hypothesis)
# Position 7: 30=?
# Position 8: 46=?
# Position 9: 48=?
# Position 10: 76=? (same as pos 2!)
# Position 11: 51=N (from hypothesis)
# Position 12: 59=?
# Position 13: 56=E (confirmed)
# Position 14: 46=? (same as pos 8!)
# Position 15: 11=N (confirmed)
# Position 16: 41=?
# Position 17: 45=D (confirmed)
# Position 18: 19=E (confirmed)

# So: D I [76] [52] E [72] S [30] [46] [48] [76] N [59] E [46] N [41] D E
# Note: 76 appears at positions 2 and 10 (same letter)
# 46 appears at positions 8 and 14 (same letter)

# If DIESE: pos 0-4 = D,I,E,S,E → 76=E, 52=S
# Then pos 10: 76=E (consistent!)
# Then: D,I,E,S,E,[72],S,[30],[46],[48],E,N,[59],E,[46],N,[41],D,E

# If 72=R → DIESER (pos 0-5)
# DIESER S [30] [46] [48] E N [59] E [46] N [41] D E
# If this is "DIESER STEINEN DE..." → S[30][46][48]EN = STEINEN?
# STEINEN = S,T,E,I,N,E,N
# We have S, [30], [46], [48], E, N
# So S,[30],[46],[48] must be S,T,E,I and then EN
# 30=T, 46=E, 48=I
# Check: STEINEN would be positions 6-12: S,T,E,I,E,N,?
# Wait: S(78),T(30),E(46),I(48),E(76=E),N(51=N) = STEIEN...
# That's 6 letters: STEIEN - not quite STEINEN
# STEINEN = S,T,E,I,N,E,N = 7 letters
# We have positions 6-12: S,[30],[46],[48],[76],[51],[59]
# = S, 30=T, 46=E, 48=I, 76=E, 51=N, 59=?
# If 59=E: STEIENE... no
# If the word is STEINEN (S,T,E,I,N,E,N) and 51=N:
# S,T,E,I,N,E,N → 78,30,46,48,51=N... but position 10 is 76=E not 51=N
# Hmm, that doesn't match.

# Let me recount:
# Pos 6: 78=S
# Pos 7: 30=?
# Pos 8: 46=?
# Pos 9: 48=?
# Pos 10: 76=E (if DIESE hypothesis)
# Pos 11: 51=N (hypothesis)
# So pos 6-11: S, [30], [46], [48], E, N

# For this to be "STEINEN":
# S, T, E, I, N, E, N  (7 letters)
# But we only have 6 positions (6-11) before 59 at pos 12
# S,[30],[46],[48],E,N = 6 letters
# This would be "S[30][46][48]EN"
# If 30=T, 46=E, 48=I → "STEIEN" (not a word)
# If 30=T, 46=I, 48=E → "STIEEN" (not a word)

# Hmm. Let me reconsider. What if 76 ≠ E?

# Alternative: What if this is "DI[76][52]E[72]..." and 76,52 are different letters?
# Let me try to enumerate short German words starting with DI:
# DIE, DIES, DIESE, DIESER, DICH, DIR, DING, DIENEN
# If "DIE" = D,I,E → position 2 (76) = E
# Then pos 3 (52) starts a new word/continues

# If 76=E: D,I,E,[52],E,[72],S,...
# What is [52]E[72]S?
# If 52=S, 72=R → "SERS" (part of DIESER?)
# DIESE,R,S... = "DIESERS" - no
# Unless word boundary: DIESE + RS... = DIE SERS? No.

# Let me step back. If I assume 76=E and look at the FULL decoded pattern:
# D,I,E,[52],E,[72],S,[30],[46],[48],E,N,[59],E,[46],N,[41],D,E
# = DIE[52]E[72]S[30][46][48]EN[59]E[46]N[41]DE

# What if it's: DIE [52]E[72]STEINE[46]N[41]DE
# Where [30][46][48]EN = EINEN? → 30=I, 46=N, 48=E, but 46=N conflicts with 76=E at pos 8...
# Wait: 46 appears at pos 8 and 14. If 46=N:
# D,I,E,[52],E,[72],S,[30],N,[48],E,N,[59],E,N,N,[41],D,E
# = DIE[52]E[72]S[30]N[48]EN[59]ENN[41]DE

# This is getting complicated. Let me try a different approach -
# enumerate all possible assignments for these 8 free codes that make
# valid German text.

print(f"\n\nSystematic analysis:", flush=True)
print(f"If 76=E (from DIESE pattern):", flush=True)
print(f"  D I E [52] E [72] S [30] [46] [48] E N [59] E [46] N [41] D E", flush=True)
print(f"\nIf 76=E AND 52=S AND 72=R (from DIESER):", flush=True)
print(f"  D I E S E R S [30] [46] [48] E N [59] E [46] N [41] D E", flush=True)
print(f"  = DIESER + S[30][46][48]EN[59]E[46]N[41]DE", flush=True)

# DIESER + STEINENDE?
# DIESER STEINENDE = this stone-end
# S[30][46][48]EN[59]E[46]N[41]DE
# STEINENDE = S,T,E,I,N,E,N,D,E
# S, [30], [46], [48], E, N, [59], E, [46], N, [41], D, E
# That's 13 positions for 9 letters... doesn't work.

# DIESER S[30][46][48]EN [59]E[46]N[41]DE
# What if [30][46][48] = TEI → STEIEN? No.
# What if the S is end of DIESER and new word starts at 30?
# DIESERS [30][46][48]EN[59]E[46]N[41]DE
# No, DIESERS isn't German.

# Let me try: is it "DIESER [word1] [word2] DE" ?
# Where S at pos 6 starts word1?

# Actually, there are NO SPACES in this cipher. It's continuous text.
# German compound words and sentences run together.
# So "DIESER" followed by what?

# Common German patterns after DIESER:
# DIESER STEIN = DIESERSTEIN (this stone)
# But that would need: pos 6-10 = S,T,E,I,N
# = 78=S, 30=T, 46=E, 48=I, 76=N??
# But we said 76=E! Contradiction.

# So either 76≠E or the word isn't DIESER.

# What if 76=S? Then: DIS...
# D,I,S,[52],E,[72],S,[30],[46],[48],S,N,[59],E,[46],N,[41],D,E
# That's weird - 3 S's from the same code.

# What if 76=R? DI R [52] E [72] S [30] [46] [48] R N [59] E [46] N [41] D E
# = DIR[52]E[72]S[30][46][48]RN[59]E[46]N[41]DE
# DIR = "to you" in German. Then: [52]E[72]S...

# I think I need to let the computer try more systematically.
# Let me test all 26 options for code 76 and see which ones
# make the pattern look most like German.

print(f"\n\nTrying all letters for code 76:", flush=True)
for letter_76 in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    partial = f"DI{letter_76}?E?S????{letter_76}N?E?N?DE"
    # Check if DI+letter_76 starts a German word
    di_starts = ['DIE', 'DIC', 'DIN', 'DIR']
    if f'DI{letter_76}' in [w[:3] for w in di_starts]:
        print(f"  76={letter_76}: {partial} <- starts German word", flush=True)


print(f"\n\n{'='*70}", flush=True)
print("8. TRY ALTERNATIVE: WHAT IF PRE-STEIN IS 'UND FEUERSTEIN'?", flush=True)
print("=" * 70, flush=True)

# FEUERSTEIN = F,E,U,E,R,S,T,E,I,N = 10 letters
# Our sequence from pos -7: E,U,[51],[35],[34],[78],[01],S,T,E,I,N
# = 12 positions
# FEUERSTEIN only has 10 letters starting from F
# If we take EU: E,U,[51],[35],[34],[78],[01] = 7 positions
# FEUERSTEIN starting from EU: E,U,E,R,S,T = 6 letters ... only 6 from EU
# Actually FEUERSTEIN: F-E-U-E-R-S-T-E-I-N
# Starting from E: E-U-E-R-S-T-E-I-N = 9 letters for 12 positions. No.

# What if it's "UND FEUERSTEIN"?
# The E before is end of previous word.
# U,N,D,F,E,U,E,R,S,T,E,I,N  ... 13 letters for 12 positions. Close!
# Wait: 61=U, 51=N, 35=D → UND, then 34=F, 78=E, 01=U
# Then: UNDFEU + STEIN
# But that gives "UNDFEUSTEIN" which isn't a word either.
# FEUERSTEIN = F,E,U,E,R,S,T,E,I,N
# Positions: [34]=F,[78]=E,[01]=U... then next should be E,R but next is 92=S
# So 01=U, then S,T,E,I,N → no E,R in between. Doesn't work.

# Back to RUNENSTEINEN:
# R-U-N-E-N-S-T-E-I-N-E-N = 12 letters
# [R_code]-95-61-51-35-34-78-01-92-88-95-21-60-19-93
# R, E,U,N,E,N,S,T,S,T,E,I,N,E,?
# Wait that has S,T twice! The 78=S,01=T is followed by 92=S,88=T
# RUNENSTEIN has only one S,T: R,U,N,E,N,S,T,E,I,N
# So: [R]-E-U-[N]-[E]-[N]-[S]-[T]-S-T-E-I-N
# That's: R,E,U,N,E,N,S,T then S,T,E,I,N
# = RUNENSTSTEIN?? That has NSTST which is wrong.

# OK so the RUNENSTEINEN hypothesis has a problem.
# 78=S and 01=T means the sequence before 92=S, 88=T would be ...,S,T,S,T,...
# That's STST which is not in RUNENSTEINEN.

print("RUNENSTEINEN hypothesis problem:", flush=True)
print("  Sequence: ..., 78, 01, 92, 88, ...", flush=True)
print("  If 78=S, 01=T: ...S, T, S, T, ... = STST in the middle", flush=True)
print("  RUNENSTEINEN only has one ST: R-U-N-E-N-S-T-E-I-N-E-N", flush=True)
print("  So 78 and 01 CANNOT both map to S and T respectively!", flush=True)

# Let me reconsider. The 7 free codes before STEIN: 51, 35, 34, 78, 01
# Plus 92=S and 88=T are the STEIN codes.
# So the pre-STEIN text is: E, U, [51], [35], [34], [78], [01]
# And this is followed DIRECTLY by S(92), T(88), E(95), I(21), N(60)

# For RUNENSTEINEN to work:
# ..., R, U, N, E, N, S, T, E, I, N, E, N
# The S,T in RUNENSTEINEN would have to be 92,88 (the STEIN codes)
# So the pre-STEIN codes map to: R, U, N, E, N
# But we have 7 codes before STEIN: E, U, [51], [35], [34], [78], [01]
# RUNENST: R,U,N,E,N needs only 5 slots (R,U,N,E,N)
# But we have E(95), U(61), [51], [35], [34], [78], [01] = 7 codes
# That's 7 letters for "RUNEN" (5 letters) + the leading E from code 95

# So it could be: [word ending in E], RUNENSTEINEN
# Where: 61=U, 51=N, 35=E, 34=N and [78],[01] are extra
# But that's only 4 letters (UNEN) not matching RUNEN

# Let me be more careful:
# E(95) = last letter of previous word
# Then RUNENSTEINEN: R,U,N,E,N,S,T,E,I,N,E,N
# = 12 letters mapped to: [R_code],61,51,35,34,78,01,92,88,95,21,60,[E_code],[N_code]
# R=unknown code before 95
# U=61 ✓
# N=51
# E=35
# N=34
# S=78
# T=01
# S=92 ✓ wait, but RUNENSTEINEN has S,T,E,I,N,E,N = only one S
# Position mapping:
# R  U  N  E  N  S  T  E  I  N  E  N
# ?  61 51 35 34 78 01 92 88 95 21 60
#                         ^S  ^T  ^E  ^I  ^N
# Wait that doesn't work. RUNENSTEINEN = R,U,N,E,N,S,T,E,I,N,E,N
# That's 12 letters. The codes from 61 to 60 are:
# 61, 51, 35, 34, 78, 01, 92, 88, 95, 21, 60 = 11 codes
# Plus the R before = 12 total. So:
# R=code_before_95, U=61, N=51, E=35, N=34, S=78, T=01, E=92?, T=88?
# No! 92=S(confirmed) and 88=T(confirmed)!
# RUNENSTEINEN position 8 is E, maps to code 92=S. Contradiction!

print(f"\nRUNENSTEINEN full mapping check:", flush=True)
print(f"  R  U  N  E  N  S  T  E  I  N  E  N", flush=True)
print(f"  ?  61 51 35 34 78 01 92 88 95 21 60", flush=True)
print(f"  But RUNENSTEINEN[7]=E needs code 92, and 92=S(confirmed). CONTRADICTION!", flush=True)
print(f"  RUNENSTEINEN does NOT fit this code sequence.", flush=True)

# So what DOES fit? We need a 12-letter word/phrase where:
# Position 0: any letter (unknown code before 95)
# Position 1: E (code 95, confirmed)
# Position 2: U (code 61, confirmed)
# Positions 3-7: five unknown letters
# Position 8: S (code 92, confirmed)
# Position 9: T (code 88, confirmed)
# Position 10: E (code 95, confirmed)
# Position 11: I (code 21, confirmed)
# Position 12: N (code 60, confirmed)

# So: ?EU?????STEIN
# 13-letter pattern with ? at positions 0, 3, 4, 5, 6, 7

# German words/phrases ending in STEIN:
# FEUERSTEIN: F-E-U-E-R-STEIN = FEUERSTEIN → ?=nothing before F
# But position 0 is the code before 95, which exists. Let me check if ALL occurrences
# have the same code at position 0.

print(f"\n\nChecking code at position before E(95) in pre-STEIN:", flush=True)
pre_E_code = Counter()
for bi, pi, before, after in stein_contexts:
    if pi >= 8:
        _, all_p = book_data[bi]
        pre_code = all_p[pi - 8]
        pre_E_code[pre_code] += 1

print(f"  Code before the E: {pre_E_code.most_common(10)}", flush=True)

# Check if FEUERSTEIN works:
# F,E,U,E,R,S,T,E,I,N = 10 letters
# Code_before=F, 95=E, 61=U, 51=E, 35=R, STEIN = 92,88,95,21,60
# That leaves 34, 78, 01 unmapped! We have 7 codes between U and STEIN
# but FEUERSTEIN only needs 2 (E,R) between U and STEIN
# So FEUERSTEIN doesn't fit either.

# What 7-letter segment fits between U and STEIN?
# ?EU[7 letters]STEIN  where the E before is code 95
# The 7 letters come from codes 51, 35, 34, 78, 01 + ???
# Wait no: codes between 61(U) and 92(S) are exactly: 51, 35, 34, 78, 01
# That's 5 codes = 5 letters.
# So the full sequence is: [code_before],E,U,[5 letters],S,T,E,I,N
# = 13 characters total: ?EU?????STEIN

# For FEUERSTEIN(10): F,E,U,E,R,S,T,E,I,N
# Between U and S: E,R = only 2 letters. We need 5. NO.

# For "GRUNDSTEIN"(10): G,R,U,N,D,S,T,E,I,N
# ?,E,U is positions 0,1,2 but GRUNDSTEIN[0:3] = G,R,U
# Position 1 should be R but it's E. NO.

# For "NÄCHSTEN STEIN"... no umlauts in this cipher probably.

# What has EU_____S pattern?
# EUCH (you) = E,U,C,H → only 2 letters after U
# EUER (your) = E,U,E,R → only 2
# EUROPA = E,U,R,O,P,A → 4 after U, need 5

# Could it be two words? ?EU + ????STEIN?
# Or: ?E + U????STEIN?  (word boundary between E and U)
# UNTERSTEIN? U,N,T,E,R,S,T,E,I,N = 10 letters
# U=61, N=51, T=35, E=34, R=78, S=01... then STEIN
# Check: 01=S? No, 01 would precede 92=S giving SS. Possible in German (UNTERSS...?)
# Actually no, UNTERSTEIN: U,N,T,E,R + STEIN
# 61=U, 51=N, 35=T, 34=E, 78=R, then 01=? before 92=S
# We need 5 codes (51,35,34,78,01) for NTERS (if UNTERSTEIN without the U)
# Actually UNTERSTEIN = U,N,T,E,R,S,T,E,I,N
# After U: N,T,E,R = 4 letters, but 01 makes 5 codes for 4 letters. Doesn't fit.

# Hmm. We need EXACTLY 5 letters between U and S.
# ?-E-U-?-?-?-?-?-S-T-E-I-N
# Words: ???EU?????STEIN
# Where 95=E and 61=U are confirmed.

# ABENTEUERSTEIN? A-B-E-N-T-E-U-E-R-S-T-E-I-N = 14 letters
# If the code_before=N, then: N,E,U,E,R,S,T,E,I,N
# But that's only 10 letters (from N onward), and between U and S: E,R = 2. No.

# Actually wait:
# ?-E-U-a-b-c-d-e-S-T-E-I-N  where a=51, b=35, c=34, d=78, e=01
# What if: word boundary after U?
# ...EU + abcde + STEIN
# 5 letters + STEIN = 10-letter compound? Or two words?
# Common German words: NACHT(5), KRAFT(5), LICHT(5), SCHRI(5)
# NACHTSTEIN? Doesn't exist.
# LICHTSTEIN? Not common.
# What about: SCHRIFTSTEIN? S,C,H,R,I,F,T,S,T,E,I,N = 12 letters (too many)

# Or maybe it IS two separate words and STEIN is common.
# abcde = 5 letters forming end of one word + start of STEIN
# e.g., "...EUCH NICHT STEIN" = E,U,C,H,N,I,C,H,T... no, too many letters

# This is hard to crack manually. Let me instead check what's CONSISTENT
# across all occurrences and try a more computational approach.

print(f"\n\n{'='*70}", flush=True)
print("DONE - NEED COMPUTATIONAL APPROACH", flush=True)
print("=" * 70, flush=True)
