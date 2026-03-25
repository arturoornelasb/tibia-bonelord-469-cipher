#!/usr/bin/env python3
"""Session 30: Cross-boundary absorption attack.

For each garbled block in the DP output, try absorbing it into adjacent
known words to form longer known words. Also handle the UNR problem
with context-specific ANAGRAM_MAP entries.
"""
import json, os, re
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json')) as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json')) as f:
    books = json.load(f)

# Load pipeline
src = open(os.path.join(script_dir, '..', 'core', 'narrative_v3_clean.py')).read()
code_end = src.index("\n# ============================================================\n# RECONSTRUCT")
exec(src[:code_end])

# Get the resolved text (after ANAGRAM_MAP, before DP)
all_text = ''.join(decoded_books)
resolved_text = all_text
for anagram in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved_text = resolved_text.replace(anagram, ANAGRAM_MAP[anagram])

tokens, covered = dp_segment(resolved_text)
total_known = sum(1 for c in resolved_text if c != '?')
print(f"Baseline: {covered}/{total_known} = {covered/total_known*100:.1f}%\n")

# ============================================================
# STRATEGY 1: UNR context-specific fix
# ============================================================
print("=" * 70)
print("STRATEGY 1: UNR CONTEXT FIX")
print("=" * 70)

# Check what precedes UNR in the DECODED text (before ANAGRAM_MAP)
# UNR appears as literal UNR in decoded text. We need to find unique
# context strings that DON'T overlap with UIRUNNHWND

# Find all UNR positions in decoded text (before anagram)
unr_positions = []
for i in range(len(all_text) - 2):
    if all_text[i:i+3] == 'UNR':
        # Check if this is part of UIRUNNHWND (which gets converted to WINDUNRUH)
        # UIRUNNHWND contains UNR at positions 4-6 (0-indexed: UIR[UNR]HWND... wait no)
        # Let me find the actual context
        ctx_start = max(0, i-15)
        ctx_end = min(len(all_text), i+18)
        ctx = all_text[ctx_start:ctx_end]
        # Check if this is inside UIRUNNHWND
        is_in_windunruh = False
        for j in range(max(0, i-10), i):
            if all_text[j:j+10] == 'UIRUNNHWND':
                if j <= i < j + 10:
                    is_in_windunruh = True
                    break
            if all_text[j:j+12] == 'SIUIRUNNHWND':
                if j <= i < j + 12:
                    is_in_windunruh = True
                    break
        unr_positions.append((i, is_in_windunruh, ctx))
        print(f"  pos {i}: windunruh={is_in_windunruh}  ...{ctx}...")

standalone_unr = [(i, ctx) for i, inside, ctx in unr_positions if not inside]
print(f"\n  Standalone UNR: {len(standalone_unr)}")
print(f"  Inside WINDUNRUH: {len(unr_positions) - len(standalone_unr)}")

# For each standalone UNR, find the 5-char context before and after
print("\n  Standalone UNR contexts (pre-ANAGRAM decoded text):")
for i, ctx in standalone_unr:
    before = all_text[max(0,i-8):i]
    after = all_text[i+3:min(len(all_text),i+11)]
    print(f"    ...{before}[UNR]{after}...")
    # Check if we can make a longer ANAGRAM_MAP key
    # Try 5, 6, 7, 8 char keys centered on UNR
    for klen in range(5, 12):
        for kstart in range(max(0, i - klen + 3), i + 1):
            key = all_text[kstart:kstart+klen]
            if 'UNR' not in key:
                continue
            # Make replacement: swap UNR -> NUR in the key
            unr_pos_in_key = key.index('UNR')
            replacement = key[:unr_pos_in_key] + 'NUR' + key[unr_pos_in_key+3:]
            # Check if this key is unique enough (appears the right number of times)
            count_in_text = all_text.count(key)
            if count_in_text >= 1:
                # Test if the replacement improves things
                pass  # Will test below

# Try the simplest fix: ODTREUUNR -> ODTREUNUR (context: "OD TREU UNR" -> "OD TREU NUR")
# But first check if all standalone UNR share a common prefix

# Check what comes IMMEDIATELY before UNR in all standalone cases
prefixes = set()
for i, ctx in standalone_unr:
    prefix = all_text[max(0,i-4):i]
    prefixes.add(prefix)
print(f"\n  Unique 4-char prefixes before standalone UNR: {prefixes}")

# ============================================================
# Try adding ANAGRAM_MAP entries for standalone UNR contexts
# ============================================================
print("\n  Testing context-specific UNR->NUR ANAGRAM_MAP entries:")

# Get all possible keys containing UNR
potential_entries = {}
for i, ctx in standalone_unr:
    # Try keys of length 5-12 that contain UNR
    for klen in range(4, 15):
        kstart = max(0, i - (klen - 3))
        for ks in range(kstart, i + 1):
            if ks + klen > len(all_text):
                continue
            key = all_text[ks:ks+klen]
            if 'UNR' not in key:
                continue
            # Skip if key is inside UIRUNNHWND
            if 'UIRUNNH' in key or 'IRUNNHW' in key:
                continue
            unr_idx = key.index('UNR')
            repl = key[:unr_idx] + 'NUR' + key[unr_idx+3:]
            if key not in potential_entries:
                potential_entries[key] = (repl, 0)
            potential_entries[key] = (repl, potential_entries[key][1] + 1)

# Test each potential entry
def dp_score(text, known_set):
    n = len(text)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        for wlen in range(2, min(i, 20) + 1):
            s = i - wlen
            if text[s:i] in known_set:
                dp[i] = max(dp[i], dp[s] + wlen)
    return dp[n]

best_entries = []
for key, (repl, count) in sorted(potential_entries.items(), key=lambda x: -x[1][1]):
    # Test: apply this entry on top of existing ANAGRAM_MAP
    test_text = all_text
    # Apply existing ANAGRAM_MAP + this new entry, longest first
    all_entries = dict(ANAGRAM_MAP)
    all_entries[key] = repl
    for a in sorted(all_entries.keys(), key=len, reverse=True):
        test_text = test_text.replace(a, all_entries[a])
    test_total = sum(1 for c in test_text if c != '?')
    test_cov = dp_score(test_text, KNOWN)
    delta = test_cov - covered
    if delta > 0:
        best_entries.append((delta, key, repl, all_text.count(key)))
        if delta >= 3:
            print(f"    +{delta}: '{key}' -> '{repl}'  ({all_text.count(key)}x in decoded)")

best_entries.sort(key=lambda x: -x[0])
if best_entries:
    print(f"\n  Best UNR fix: +{best_entries[0][0]} chars via '{best_entries[0][1]}' -> '{best_entries[0][2]}'")
else:
    print("  No UNR fix found")

# ============================================================
# STRATEGY 2: Cross-boundary absorption for 2-char blocks
# ============================================================
print("\n" + "=" * 70)
print("STRATEGY 2: CROSS-BOUNDARY ABSORPTION (2-char blocks)")
print("=" * 70)

# For each 2-char garbled block, check if combining with adjacent word
# creates a new known word
absorptions = []
for i, tok in enumerate(tokens):
    if not tok.startswith('{') or len(tok) != 4:  # {XY} = 4 chars
        continue
    block = tok[1:-1]
    if len(block) != 2:
        continue

    prev_word = tokens[i-1] if i > 0 and not tokens[i-1].startswith('{') else None
    next_word = tokens[i+1] if i < len(tokens)-1 and not tokens[i+1].startswith('{') else None

    # Try absorbing block into previous word (block goes to end)
    if prev_word:
        combined = prev_word + block
        if combined in KNOWN:
            absorptions.append(('suffix', block, prev_word, combined, i))
        # Also try with swap
        for c1, c2 in [('I','E'), ('E','I'), ('I','L'), ('L','I')]:
            swapped = combined.replace(c1, c2, 1)
            if swapped in KNOWN and swapped != combined:
                absorptions.append(('suffix+swap', block, prev_word, swapped, i))

    # Try absorbing block into next word (block goes to start)
    if next_word:
        combined = block + next_word
        if combined in KNOWN:
            absorptions.append(('prefix', block, next_word, combined, i))
        for c1, c2 in [('I','E'), ('E','I'), ('I','L'), ('L','I')]:
            swapped = combined.replace(c1, c2, 1)
            if swapped in KNOWN and swapped != combined:
                absorptions.append(('prefix+swap', block, next_word, swapped, i))

    # Try: block IS a word (check 2-char words not in KNOWN)
    # Already min_wlen=2 so 2-char garbled means it's not in KNOWN
    # Check common 2-char German words
    if block in {'DE', 'HI', 'ST', 'ND', 'TE', 'RT', 'HE', 'UR'}:
        pass  # These might be parts of words

for kind, block, word, combined, idx in absorptions:
    ctx = ' '.join(tokens[max(0,idx-2):idx+3])
    print(f"  {kind}: {block} + {word} -> {combined}  (context: {ctx})")

# ============================================================
# STRATEGY 3: New words from single-letter absorption
# ============================================================
print("\n" + "=" * 70)
print("STRATEGY 3: SINGLE-LETTER ABSORPTIONS")
print("=" * 70)

single_absorptions = []
for i, tok in enumerate(tokens):
    if not tok.startswith('{') or len(tok) != 3:  # {X} = 3 chars
        continue
    letter = tok[1]

    prev_word = tokens[i-1] if i > 0 and not tokens[i-1].startswith('{') else None
    next_word = tokens[i+1] if i < len(tokens)-1 and not tokens[i+1].startswith('{') else None

    # Absorb into previous word
    if prev_word:
        combined = prev_word + letter
        if combined in KNOWN and len(combined) > len(prev_word):
            single_absorptions.append(('suffix', letter, prev_word, combined, i))

    # Absorb into next word
    if next_word:
        combined = letter + next_word
        if combined in KNOWN and len(combined) > len(next_word):
            single_absorptions.append(('prefix', letter, next_word, combined, i))

# Count how many times each absorption pattern appears
pattern_counts = Counter()
for kind, letter, word, combined, idx in single_absorptions:
    pattern_counts[(kind, letter, word, combined)] += 1

for (kind, letter, word, combined), count in pattern_counts.most_common(30):
    print(f"  {count}x {kind}: {letter} + {word} -> {combined}")

# ============================================================
# STRATEGY 4: ANAGRAM_MAP entries for decoded-text patterns
# ============================================================
print("\n" + "=" * 70)
print("STRATEGY 4: NEW ANAGRAM_MAP FROM DECODED TEXT PATTERNS")
print("=" * 70)

# Find recurring patterns in decoded text that aren't handled
# Focus on the ND pattern: "ORT ND TER" (6x)
# In resolved text, this appears as ORTNDTER
# ND could be UND (and) with missing U, or part of a longer word
print("  ND pattern analysis:")
nd_positions = []
for i in range(len(resolved_text) - 1):
    if resolved_text[i:i+2] == 'ND':
        before = resolved_text[max(0,i-6):i]
        after = resolved_text[i+2:min(len(resolved_text),i+8)]
        nd_positions.append((i, before, after))

# Check garbled ND contexts specifically
for i, tok in enumerate(tokens):
    if tok == '{ND}':
        ctx = ' '.join(tokens[max(0,i-3):min(len(tokens),i+4)])
        print(f"    {ctx}")

# DE pattern: "NEU DE DIENST" (5x)
print("\n  DE pattern analysis:")
for i, tok in enumerate(tokens):
    if tok == '{DE}':
        ctx = ' '.join(tokens[max(0,i-3):min(len(tokens),i+4)])
        print(f"    {ctx}")

# CHTIG: "ORANGENSTRASSE CHTIG ER"
print("\n  CHTIG analysis:")
for i, tok in enumerate(tokens):
    if tok == '{CHTIG}':
        ctx = ' '.join(tokens[max(0,i-3):min(len(tokens),i+4)])
        print(f"    {ctx}")
        # This is clearly BERUCHTIG with BERU consumed
        # Check: in decoded text, what is before CHTIG?
        # Find position in resolved text
        pos = resolved_text.find('CHTIG')
        if pos > 0:
            print(f"    Resolved text before: ...{resolved_text[max(0,pos-20):pos+10]}...")
