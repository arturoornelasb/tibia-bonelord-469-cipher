#!/usr/bin/env python3
"""
Session 19 Part 2: Validate and apply all cross-boundary anagram candidates.
Test each independently, then combine safe ones.
"""

import json, os, re
from collections import Counter, defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

DIGIT_SPLITS = {
    2: (45, '1'),    5: (265, '1'),   6: (12, '0'),    8: (137, '7'),
    10: (169, '0'),  11: (137, '0'),  12: (56, '1'),   13: (45, '0'),
    14: (98, '1'),   15: (98, '0'),   18: (4, '0'),    19: (52, '0'),
    20: (5, '1'),    22: (7, '1'),    23: (22, '4'),   24: (87, '8'),
    25: (0, '0'),    29: (53, '0'),   32: (137, '1'),  34: (101, '0'),
    36: (78, '0'),   39: (44, '0'),   42: (91, '2'),   43: (122, '0'),
    45: (15, '0'),   46: (0, '2'),    48: (126, '0'),  49: (97, '1'),
    50: (16, '6'),   52: (1, '0'),    53: (257, '1'),  54: (49, '1'),
    60: (73, '9'),   61: (93, '7'),   64: (60, '0'),   65: (114, '2'),
    68: (54, '0'),
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

book_pairs = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        split_pos, digit = DIGIT_SPLITS[bidx]
        book = book[:split_pos] + digit + book[split_pos:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

decoded_books = []
for bpairs in book_pairs:
    text = ''.join(v7.get(p, '?') for p in bpairs)
    decoded_books.append(text)

all_text = ''.join(decoded_books)

BASE_ANAGRAM_MAP = {
    'LABGZERAS': 'SALZBERG', 'SCHWITEIONE': 'WEICHSTEIN',
    'SCHWITEIO': 'WEICHSTEIN', 'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'EDETOTNIURG': 'GOTTDIENER', 'EDETOTNIURGS': 'GOTTDIENERS',
    'ADTHARSC': 'SCHARDT', 'TAUTR': 'TRAUT', 'EILCH': 'LEICH',
    'HEDEMI': 'HEIME', 'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG', 'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE', 'TEIGN': 'NEIGT', 'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER', 'SODGE': 'GODES', 'SNDTEII': 'DIENST',
    'IEB': 'BEI',
}

KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR', 'NU',
    'ABER', 'ALLE', 'ALLES', 'ALTE', 'ALTEN', 'ALTER', 'AUCH', 'BAND',
    'BERG', 'BURG', 'DENN', 'DIES', 'DIESE', 'DIESER', 'DIESEN',
    'DIESEM', 'DOCH', 'DORT', 'DREI', 'DURCH', 'EINE', 'EINEM',
    'EINEN', 'EINER', 'EINES', 'ENDE', 'ERDE', 'ERST', 'ERSTE',
    'FACH', 'FAND', 'FERN', 'FEST', 'FORT', 'GAR', 'GANZ', 'GEGEN',
    'GEIST', 'GOTT', 'GOLD', 'GRAB', 'GROSS', 'GRUFT', 'GUT',
    'HAND', 'HEIM', 'HELD', 'HERR', 'HIER', 'HOCH', 'IMMER',
    'KANN', 'KLAR', 'KRAFT', 'LAND', 'LANG', 'LICHT', 'MACHT',
    'MEHR', 'MUSS', 'NACH', 'NACHT', 'NAHM', 'NAME', 'NEU', 'NEUE',
    'NEUEN', 'NICHT', 'NIE', 'NOCH', 'ODER', 'ORT', 'ORTEN',
    'REDE', 'REDEN', 'REICH', 'RIEF', 'RUIN', 'RUNE', 'RUNEN',
    'SAND', 'SAGT', 'SCHAUN', 'SCHON', 'SEHR', 'SEID', 'SEIN',
    'SEINE', 'SEINEN', 'SEINER', 'SEINEM', 'SEINES',
    'SICH', 'SIND', 'SOHN', 'SOLL', 'STEH', 'STEIN', 'STEINE',
    'STEINEN', 'STERN', 'TAG', 'TAGE', 'TAGEN', 'TAT', 'TEIL',
    'TIEF', 'TOD', 'TURM', 'UNTER', 'URALTE', 'VIEL', 'VIER',
    'WAHR', 'WALD', 'WAND', 'WARD', 'WEIL', 'WELT', 'WENN', 'WERT',
    'WESEN', 'WILL', 'WIND', 'WIRD', 'WORT', 'WORTE', 'ZEIT',
    'ZEHN', 'ZORN',
    'FINDEN', 'GEBEN', 'GEHEN', 'HABEN', 'KOMMEN', 'LEBEN', 'LESEN',
    'NEHMEN', 'SAGEN', 'SEHEN', 'STEHEN', 'SUCHEN', 'WISSEN',
    'WISSET', 'RUFEN', 'WIEDER',
    'OEL', 'SCE', 'MINNE', 'MIN',
    'ODE', 'SER', 'GEN', 'INS',
    'GEIGET', 'BERUCHTIG', 'BERUCHTIGER',
    'MEERE', 'NEIGT', 'WISTEN', 'MANIER', 'HUND',
    'GODE', 'GODES', 'EIGENTUM', 'REDER',
    'THENAEUT', 'LABT', 'MORT', 'DIGE', 'WEGE',
    'KOENIGS', 'NAHE', 'NOT', 'NOTH', 'ZUR', 'OWI',
    'ENGE', 'SEIDEN', 'ALTES', 'DENN', 'BIS', 'NIE',
    'NUT', 'NUTZ', 'HEIL', 'NEID', 'TREU', 'TREUE',
    'SUN', 'DIENST', 'SANG', 'DINC', 'HULDE', 'NACH',
    'STEINE', 'LANT', 'HERRE', 'DIENEST',
    'GEBOT', 'SCHWUR', 'ORDEN', 'RICHTER', 'DUNKEL',
    'EHRE', 'EDELE', 'SCHULD', 'SEGEN', 'FLUCH', 'RACHE',
    'KOENIG', 'DASS', 'EDEL', 'ADEL',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME',
    'SCHARDT',
])

def dp_count(text, wordset):
    n = len(text)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if cand in wordset:
                score = dp[start] + wlen
                if score > dp[i]:
                    dp[i] = score
    return dp[n]

def dp_segment(text, wordset):
    n = len(text)
    dp = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], None)
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if cand in wordset:
                score = dp[start][0] + wlen
                if score > dp[i][0]:
                    dp[i] = (score, (start, cand))
    tokens = []
    i = n
    while i > 0:
        if dp[i][1] is not None:
            start, word = dp[i][1]
            tokens.append(('W', word))
            i = start
        else:
            tokens.append(('C', text[i-1]))
            i -= 1
    tokens.reverse()
    result = []
    for kind, val in tokens:
        if kind == 'W':
            result.append(val)
        else:
            if result and result[-1].startswith('{'):
                result[-1] = result[-1][:-1] + val + '}'
            else:
                result.append('{' + val + '}')
    return result, dp[n][0]

def sorted_letters(s):
    return ''.join(sorted(s))

# Baseline
resolved_base = all_text
for anag in sorted(BASE_ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved_base = resolved_base.replace(anag, BASE_ANAGRAM_MAP[anag])
total = sum(1 for c in resolved_base if c != '?')
baseline = dp_count(resolved_base, KNOWN)
print(f"BASELINE: {baseline}/{total} = {baseline/total*100:.1f}%")
print()

# ================================================================
# TEST EACH CANDIDATE INDEPENDENTLY
# ================================================================
print("=" * 80)
print("INDEPENDENT CANDIDATE TESTING")
print("=" * 80)

candidates = [
    # (anagram_from, anagram_to, new_known_words, description)
    ('TNEDAS', 'STANDE', ['STANDE'], 'MHG subjunctive: he stood/would stand'),
    ('NSCHAT', 'NACHTS', ['NACHTS'], 'at night (genitive)'),
    ('SANGE', 'SAGEN', [], 'to say / legends (already in KNOWN)'),
    ('ANSD', 'SAND', [], 'sand (already in KNOWN)'),
]

for anag_from, anag_to, new_words, desc in candidates:
    test_map = dict(BASE_ANAGRAM_MAP)
    test_map[anag_from] = anag_to
    test_known = set(KNOWN)
    for w in new_words:
        test_known.add(w)

    test_resolved = all_text
    for anag in sorted(test_map.keys(), key=len, reverse=True):
        test_resolved = test_resolved.replace(anag, test_map[anag])

    cov = dp_count(test_resolved, test_known)
    delta = cov - baseline
    occ = resolved_base.count(anag_from)

    # Verify anagram
    is_anagram = sorted_letters(anag_from) == sorted_letters(anag_to)

    print(f"\n  {anag_from} -> {anag_to} ({desc})")
    print(f"    Anagram: {'EXACT' if is_anagram else 'NO'} ({sorted_letters(anag_from)} vs {sorted_letters(anag_to)})")
    print(f"    Occurrences: {occ}x")
    print(f"    Coverage: {cov}/{total} = {cov/total*100:.1f}% ({delta:+d})")

    # Show all contexts
    if occ <= 5:
        for i in range(len(test_resolved)):
            if test_resolved[i:i+len(anag_to)] == anag_to:
                # Make sure this wasn't already there in base
                if resolved_base[i:i+len(anag_to)] != anag_to:
                    start = max(0, i-15)
                    end = min(len(test_resolved), i+len(anag_to)+15)
                    ctx = test_resolved[start:end]
                    # DP-segment the context
                    tokens, _ = dp_segment(ctx, test_known)
                    print(f"    Context: {' '.join(tokens)}")

# ================================================================
# VALIDATE ANSD -> SAND more carefully
# ================================================================
print(f"\n{'=' * 80}")
print("DETAILED ANSD -> SAND VALIDATION")
print("=" * 80)

# Find all ANSD in resolved text and show full phrase context
for i in range(len(resolved_base)):
    if resolved_base[i:i+4] == 'ANSD':
        start = max(0, i-25)
        end = min(len(resolved_base), i+30)
        ctx = resolved_base[start:end]
        tokens, _ = dp_segment(ctx, KNOWN)
        print(f"\n  Position {i}:")
        print(f"    Raw: ...{ctx}...")
        print(f"    Parsed: {' '.join(tokens)}")

# Check if SAND makes narrative sense in all positions
# "DIENST ORT AN{SD} IM MIN HED" -> "DIENST ORT SAND IM MIN HED"
# = "service place sand in my [?]" - sand as landscape feature
# vs "service place at [?] in my [?]" - AN + unknown SD

# ================================================================
# VALIDATE SANGE -> SAGEN more carefully
# ================================================================
print(f"\n{'=' * 80}")
print("DETAILED SANGE -> SAGEN VALIDATION")
print("=" * 80)

for i in range(len(resolved_base)):
    if resolved_base[i:i+5] == 'SANGE':
        start = max(0, i-20)
        end = min(len(resolved_base), i+25)
        ctx = resolved_base[start:end]
        tokens, _ = dp_segment(ctx, KNOWN)
        print(f"\n  Position {i}:")
        print(f"    Raw: ...{ctx}...")
        print(f"    Parsed: {' '.join(tokens)}")
        # If we replace SANGE with SAGEN:
        ctx2 = resolved_base[start:i] + 'SAGEN' + resolved_base[i+5:end]
        tokens2, _ = dp_segment(ctx2, KNOWN)
        print(f"    With SAGEN: {' '.join(tokens2)}")

# ================================================================
# LOOK AT LARGE GARBLED BLOCK: WRLGTNELNRHELUIRUNNHWND
# ================================================================
print(f"\n{'=' * 80}")
print("LARGE GARBLED BLOCK ANALYSIS: WRLGTNELNRHELUIRUNNHWND")
print("=" * 80)

block = 'WRLGTNELNRHELUIRUNNHWND'
print(f"  Block: {block} ({len(block)} chars)")
print(f"  Letter counts: {dict(Counter(block))}")

# This appears between "IM NU STEH" and "FINDEN NEIGT DAS"
# Could contain multiple words. Let's try substrings.

# Check if any substrings are known words or anagrams
print(f"\n  Looking for known words inside (sliding window):")
for wlen in range(3, min(12, len(block)+1)):
    for start in range(len(block) - wlen + 1):
        sub = block[start:start+wlen]
        if sub in KNOWN:
            print(f"    [{start}:{start+wlen}] {sub}")

# Check substrings against anagram index
print(f"\n  Looking for anagram substrings (4+ chars):")
all_words_extended = KNOWN | set([
    'STANDE', 'NACHTS', 'TURM', 'HELD', 'HELFEN', 'WUNDER',
    'NORDEN', 'SUEDEN', 'WESTEN', 'OSTEN', 'RITTER', 'KNECHT',
    'HERREN', 'HULDEN', 'VINDEN', 'STIMME', 'GEWALT', 'GENADE',
    'BRUNNEN', 'LINDEN', 'THURM', 'UNTOT', 'UNTOTE',
    'DRUIDE', 'WACHTER', 'KIRCHE', 'KLOSTER', 'KRYPTA',
    'INSCHRIFT', 'ZEICHEN', 'SCHWERT', 'SCHILD', 'LANZE',
    'RITUAL', 'ZAUBER', 'GEBEIN', 'LEICHE', 'RUHE', 'KRIEG',
    'EWIGE', 'EWIGEN', 'HUNGER', 'GLUECK', 'PFLICHT',
])

anagram_idx = defaultdict(list)
for w in all_words_extended:
    anagram_idx[sorted_letters(w)].append(w)

for wlen in range(4, min(10, len(block)+1)):
    for start in range(len(block) - wlen + 1):
        sub = block[start:start+wlen]
        key = sorted_letters(sub)
        matches = anagram_idx.get(key, [])
        if matches:
            rest = block[:start] + '|' + block[start+wlen:]
            print(f"    [{start}:{start+wlen}] {sub} = {matches}  (rest: {rest})")

# Also check: the block consistently precedes FINDEN
# Could it be a phrase? "WRLGTNELN RHELUIRUNN HWND"
# HWND was identified before as potentially HUND (dog/hound)
# Let's check if HWND = HUND with W->U already applied
# Actually W and U map differently in v7. HWND appears at the end.
# In the block: ...HWND, followed by FINDEN = "find"
# "HUND FINDEN" = "find [the] dog/hound" ??
# HWND sorted = DHNW. HUND sorted = DHNU. Not a match (W vs U).
# Unless W=U in some context... but that's a code mapping change.

# Check blocks ending in HWND
hwnd_count = resolved_base.count('HWND')
print(f"\n  HWND appears {hwnd_count}x in text")
# Always followed by FINDEN?
for i in range(len(resolved_base)):
    if resolved_base[i:i+4] == 'HWND':
        after = resolved_base[i+4:i+14]
        print(f"    HWND + '{after}'")

# ================================================================
# INVESTIGATE DIER -> DREI (three)
# ================================================================
print(f"\n{'=' * 80}")
print("DIER -> DREI VALIDATION")
print("=" * 80)

for i in range(len(resolved_base)):
    if resolved_base[i:i+4] == 'DIER':
        start = max(0, i-20)
        end = min(len(resolved_base), i+25)
        ctx = resolved_base[start:end]
        tokens, _ = dp_segment(ctx, KNOWN)
        print(f"\n  Position {i}:")
        print(f"    Parsed: {' '.join(tokens)}")
        # With DREI:
        ctx2 = resolved_base[start:i] + 'DREI' + resolved_base[i+4:end]
        tokens2, _ = dp_segment(ctx2, KNOWN)
        print(f"    With DREI: {' '.join(tokens2)}")

# ================================================================
# COMBINED: ALL SAFE CANDIDATES
# ================================================================
print(f"\n{'=' * 80}")
print("COMBINED SAFE CANDIDATES")
print("=" * 80)

# Safe = confirmed exact anagrams with clear narrative support
safe_anagrams = dict(BASE_ANAGRAM_MAP)
safe_anagrams['TNEDAS'] = 'STANDE'   # exact, 4x, MHG subjunctive

safe_known = set(KNOWN)
safe_known.add('STANDE')

safe_resolved = all_text
for anag in sorted(safe_anagrams.keys(), key=len, reverse=True):
    safe_resolved = safe_resolved.replace(anag, safe_anagrams[anag])

safe_cov = dp_count(safe_resolved, safe_known)
print(f"  Baseline:      {baseline}/{total} = {baseline/total*100:.1f}%")
print(f"  +STANDE only:  {safe_cov}/{total} = {safe_cov/total*100:.1f}% ({safe_cov-baseline:+d})")

# Now add NSCHAT->NACHTS (also exact anagram, good context)
safe2_anagrams = dict(safe_anagrams)
safe2_anagrams['NSCHAT'] = 'NACHTS'
safe2_known = set(safe_known)
safe2_known.add('NACHTS')

safe2_resolved = all_text
for anag in sorted(safe2_anagrams.keys(), key=len, reverse=True):
    safe2_resolved = safe2_resolved.replace(anag, safe2_anagrams[anag])

safe2_cov = dp_count(safe2_resolved, safe2_known)
print(f"  +NACHTS:       {safe2_cov}/{total} = {safe2_cov/total*100:.1f}% ({safe2_cov-baseline:+d})")

# Add SANGE->SAGEN (exact anagram, SAGEN already in KNOWN)
safe3_anagrams = dict(safe2_anagrams)
safe3_anagrams['SANGE'] = 'SAGEN'
safe3_known = set(safe2_known)

safe3_resolved = all_text
for anag in sorted(safe3_anagrams.keys(), key=len, reverse=True):
    safe3_resolved = safe3_resolved.replace(anag, safe3_anagrams[anag])

safe3_cov = dp_count(safe3_resolved, safe3_known)
print(f"  +SAGEN:        {safe3_cov}/{total} = {safe3_cov/total*100:.1f}% ({safe3_cov-baseline:+d})")

# Add ANSD->SAND (exact anagram, SAND already in KNOWN)
safe4_anagrams = dict(safe3_anagrams)
safe4_anagrams['ANSD'] = 'SAND'
safe4_known = set(safe3_known)

safe4_resolved = all_text
for anag in sorted(safe4_anagrams.keys(), key=len, reverse=True):
    safe4_resolved = safe4_resolved.replace(anag, safe4_anagrams[anag])

safe4_cov = dp_count(safe4_resolved, safe4_known)
print(f"  +SAND:         {safe4_cov}/{total} = {safe4_cov/total*100:.1f}% ({safe4_cov-baseline:+d})")

# Show segmented text for combined
tokens_final, _ = dp_segment(safe4_resolved, safe4_known)
# Count remaining garbled
garbled_chars = sum(len(t)-2 for t in tokens_final if t.startswith('{'))
matched_chars = safe4_cov
print(f"\n  Final: {matched_chars} matched, {garbled_chars} garbled, {total} total")

# ================================================================
# INVESTIGATE: "TNED" (5th occurrence, NOT followed by AS)
# ================================================================
print(f"\n{'=' * 80}")
print("TNED WITHOUT AS")
print("=" * 80)

# TNED appears 5 times but TNEDAS only 4 times
# The 5th TNED is in "ALS TNED ENDE E WEICHSTEIN"
for i in range(len(resolved_base)):
    if resolved_base[i:i+4] == 'TNED':
        following = resolved_base[i+4:i+20]
        if not following.startswith('AS'):
            start = max(0, i-20)
            end = min(len(resolved_base), i+30)
            ctx = resolved_base[start:end]
            tokens, _ = dp_segment(ctx, KNOWN)
            print(f"  Position {i}: ...{ctx}...")
            print(f"  Parsed: {' '.join(tokens)}")
            # What is TNEDENDE?
            print(f"  TNED sorted: {sorted_letters('TNED')}")
            print(f"  TNEDE sorted: {sorted_letters('TNEDE')}")
            print(f"  TNEDENDE sorted: {sorted_letters('TNEDENDE')}")
            # STENDE? DENTE? ENDENT?
            # Check: TNEDE = TENDE? DENET?
            # DENT sorted = DENT. TEND sorted = DENT. DENT = dent? Not German.
            # But what about: TNED + ENDE = TNEDENDE
            # Could be STENDENDE? ENTDENDE?
            # Actually: "ALS TNED ENDE E WEICHSTEIN"
            # If TNED = DENT (MHG?) or just garbled fragment
            # More likely: the text here has different word boundaries
            # "ALSTNED" = ALS + TNED. TNED isn't matched.
            # "ALSTNE" + D + "ENDE" = could be "ALS STANDE" minus the last A?
            # TNED has letters D,E,N,T. Missing A and S to form STANDE.
            # Not the same pattern as TNEDAS.

# ================================================================
# CHECK: What if some {E} blocks are actually valid words in context?
# ================================================================
print(f"\n{'=' * 80}")
print("SINGLE-LETTER {E} ANALYSIS")
print("=" * 80)

# {E} appears 38 times. It's the most common single-letter garbled.
# Could E be a valid MHG particle/exclamation?
# In MHG: 'e' can mean 'before' (temporal, = ehe) or be a prefix
# Adding 'E' as a known word would match 38 occurrences = +38 chars!
# But that's dangerous - E is so common it might overfit

# Test impact
test_known_e = set(KNOWN)
test_known_e.add('E')
cov_e = dp_count(resolved_base, test_known_e)
print(f"  Adding E as known word: {cov_e}/{total} = {cov_e/total*100:.1f}% ({cov_e-baseline:+d})")

# Check: how does E interact with DP? E is 1 char, below the min word length of 2
# Wait... the DP checks wlen range(2, ...). So E (1 char) would NOT be matched!
# Let me verify:
print(f"  (Note: DP minimum word length is 2, so single-char 'E' won't match)")
print(f"  Need to modify DP to allow 1-char words, but that's risky)")

# What about EE, OE, EI as MHG words?
# EE = MHG "ehe" (before) sometimes written "e" or "ee"
# OE = not standard
# EI = egg (but also exclamation in MHG)
for w in ['EE', 'OE', 'EI', 'OI', 'NU']:
    count = resolved_base.count(w)
    print(f"  '{w}' in text: {count}x (already known: {w in KNOWN})")

# ================================================================
# FINAL ANALYSIS: NARRATIVE STRUCTURE AFTER IMPROVEMENTS
# ================================================================
print(f"\n{'=' * 80}")
print("NARRATIVE WITH ALL IMPROVEMENTS")
print("=" * 80)

# Use safe3 (STANDE + NACHTS + SAGEN, skip SAND for now)
final_anagrams = dict(safe3_anagrams)
final_known = set(safe3_known)

final_resolved = all_text
for anag in sorted(final_anagrams.keys(), key=len, reverse=True):
    final_resolved = final_resolved.replace(anag, final_anagrams[anag])

tokens_final, cov_final = dp_segment(final_resolved, final_known)
print(f"  Coverage: {cov_final}/{total} = {cov_final/total*100:.1f}%")
print(f"\n  First 150 tokens:")
print(f"  {' '.join(tokens_final[:150])}")

# Count how many unique garbled blocks remain
garbled_remaining = Counter()
for t in tokens_final:
    if t.startswith('{'):
        garbled_remaining[t] += 1
print(f"\n  Unique garbled blocks: {len(garbled_remaining)}")
print(f"  Total garbled tokens: {sum(garbled_remaining.values())}")
print(f"\n  Most common garbled blocks:")
for block, count in garbled_remaining.most_common(20):
    print(f"    {count:3d}x {block}")
