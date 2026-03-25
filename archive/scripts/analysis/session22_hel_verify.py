#!/usr/bin/env python3
"""
Session 22 Part 4: Deep verification of HEL as KNOWN word.
HEL = hell/bright (NHG) or hël (MHG: echoing/resounding).
+21 chars gain if added. Need to verify it's not a false positive.
"""

import json, os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

DIGIT_SPLITS = {
    2: (45, '1'), 5: (265, '1'), 6: (12, '0'), 8: (137, '7'),
    10: (169, '0'), 11: (137, '0'), 12: (56, '1'), 13: (45, '0'),
    14: (98, '1'), 15: (98, '0'), 18: (4, '0'), 19: (52, '0'),
    20: (5, '1'), 22: (7, '1'), 23: (22, '4'), 24: (87, '8'),
    25: (0, '0'), 29: (53, '0'), 32: (137, '1'), 34: (101, '0'),
    36: (78, '0'), 39: (44, '0'), 42: (91, '2'), 43: (122, '0'),
    45: (15, '0'), 46: (0, '2'), 48: (126, '0'), 49: (97, '1'),
    50: (16, '6'), 52: (1, '0'), 53: (257, '1'), 54: (49, '1'),
    60: (73, '9'), 61: (93, '7'), 64: (60, '0'), 65: (114, '2'),
    68: (54, '0'),
}

def ic_from_counts(counts, total):
    if total <= 1: return 0
    return sum(c*(c-1) for c in counts.values()) / (total*(total-1))

def get_offset(book):
    if len(book) < 10: return 0
    bp0 = [book[j:j+2] for j in range(0, len(book)-1, 2)]
    bp1 = [book[j:j+2] for j in range(1, len(book)-1, 2)]
    return 0 if ic_from_counts(Counter(bp0), len(bp0)) > ic_from_counts(Counter(bp1), len(bp1)) else 1

ANAGRAM_MAP = {
    'LABGZERAS': 'SALZBERG', 'SCHWITEIONE': 'WEICHSTEIN',
    'SCHWITEIO': 'WEICHSTEIN', 'AUNRSONGETRASES': 'ORANGENSTRASSE',
    'EDETOTNIURG': 'GOTTDIENER', 'EDETOTNIURGS': 'GOTTDIENERS',
    'ADTHARSC': 'SCHARDT', 'TAUTR': 'TRAUT', 'EILCH': 'LEICH',
    'HEDDEMI': 'HEIME', 'TIUMENGEMI': 'EIGENTUM',
    'HEARUCHTIG': 'BERUCHTIG', 'HEARUCHTIGER': 'BERUCHTIGER',
    'EILCHANHEARUCHTIG': 'LEICHANBERUCHTIG',
    'EILCHANHEARUCHTIGER': 'LEICHANBERUCHTIGER',
    'EEMRE': 'MEERE', 'TEIGN': 'NEIGT', 'WIISETN': 'WISTEN',
    'AUIENMR': 'MANIER', 'SODGE': 'GODES', 'SNDTEII': 'DIENST',
    'IEB': 'BEI', 'TNEDAS': 'STANDE', 'NSCHAT': 'NACHTS',
    'SANGE': 'SAGEN', 'GHNEE': 'GEHEN', 'THARSCR': 'SCHRAT',
    'ANSD': 'SAND', 'TTU': 'TUT', 'TERLAU': 'URALTE',
    'EUN': 'NEU', 'NIUR': 'RUIN', 'RUIIN': 'RUIN',
    'CHIS': 'SICH',
}

decoded_books = []
book_pairs_all = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs_all.append(pairs)
    decoded_books.append(''.join(v7.get(p, '?') for p in pairs))

processed = ''.join(decoded_books)
for old in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    processed = processed.replace(old, ANAGRAM_MAP[old])

# ================================================================
# Find ALL positions where HEL appears in processed text
# ================================================================
print("=" * 60)
print("ALL HEL (3-char) occurrences in processed text")
print("=" * 60)

pos = 0
hel_positions = []
while True:
    idx = processed.find('HEL', pos)
    if idx < 0: break
    ctx = processed[max(0,idx-10):idx+13]
    hel_positions.append(idx)

    # Check if inside a known longer word
    inside_word = None
    for w in ['HELD', 'HEIL', 'HELL', 'HELDEN', 'HECHLLT', 'HELUIRUNNHWND']:
        wpos = processed.find(w)
        while wpos >= 0:
            if wpos <= idx < wpos + len(w):
                inside_word = w
                break
            wpos = processed.find(w, wpos + 1)
        if inside_word:
            break

    label = f" (inside {inside_word})" if inside_word else ""
    print(f"  pos {idx}: ...{ctx}...{label}")
    pos = idx + 1

print(f"\n  Total HEL occurrences: {len(hel_positions)}")

# ================================================================
# Check: does adding HEL break any existing known words?
# ================================================================
print(f"\n{'='*60}")
print("Collision check: adding HEL to KNOWN")
print(f"{'='*60}")

KNOWN_BASE = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR', 'SIN',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN', 'TUT',
    'SAG', 'WAR', 'NU', 'STANDE', 'NACHTS', 'NIT', 'TOT', 'TER',
    'SICH', 'SIND', 'SOHN', 'SOLL', 'STEH', 'STEIN', 'STEINE',
    'STEINEN', 'OEL', 'SCE', 'MINNE', 'MIN', 'ODE', 'SER', 'GEN', 'INS',
    'GEIGET', 'BERUCHTIG', 'BERUCHTIGER', 'MEERE', 'NEIGT', 'WISTEN',
    'MANIER', 'GODE', 'GODES', 'EIGENTUM', 'REDER', 'THENAEUT',
    'KOENIG', 'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME', 'SCHARDT',
    'ENDE', 'ERDE', 'ERST', 'ERSTE', 'FACH', 'FINDEN', 'RUIN', 'RUNE',
    'RUNEN', 'SAND', 'SCHAUN', 'SAGEN', 'GEHEN', 'SCHRAT', 'URALTE',
    'DIENST', 'HELD', 'HEIL',
])

def dp_segment(text, known_set):
    n = len(text)
    dp = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], None)
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if cand in known_set:
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

# Compare word-by-word what changes
tokens_no_hel, cov_no_hel = dp_segment(processed, KNOWN_BASE)
tokens_hel, cov_hel = dp_segment(processed, KNOWN_BASE | {'HEL'})

print(f"  Without HEL: {cov_no_hel} covered")
print(f"  With HEL:    {cov_hel} covered (+{cov_hel - cov_no_hel})")

# Find exactly which tokens changed
print(f"\n  Token differences:")
# Align tokens and find differences
i_no = 0
i_yes = 0
pos_no = 0
pos_yes = 0
changes = []
while i_no < len(tokens_no_hel) and i_yes < len(tokens_hel):
    t_no = tokens_no_hel[i_no]
    t_yes = tokens_hel[i_yes]

    len_no = len(t_no.strip('{}'))
    len_yes = len(t_yes.strip('{}'))

    if pos_no == pos_yes and t_no != t_yes:
        # Found a difference - collect tokens until positions re-sync
        diff_start = pos_no
        old_tokens = []
        new_tokens = []
        while i_no < len(tokens_no_hel) and i_yes < len(tokens_hel):
            t_no = tokens_no_hel[i_no]
            t_yes = tokens_hel[i_yes]
            len_no = len(t_no.strip('{}'))
            len_yes = len(t_yes.strip('{}'))

            old_tokens.append(t_no)
            new_tokens.append(t_yes)
            pos_no += len_no
            pos_yes += len_yes
            i_no += 1
            i_yes += 1

            if pos_no == pos_yes:
                break

        changes.append((' '.join(old_tokens), ' '.join(new_tokens)))
    else:
        pos_no += len_no
        pos_yes += len_yes
        i_no += 1
        i_yes += 1

for old, new in changes[:15]:
    print(f"    OLD: {old}")
    print(f"    NEW: {new}")
    print()

# ================================================================
# Key question: does HEL inside WRLGTNELNRHELUIRUNNHWND make sense?
# ================================================================
print(f"{'='*60}")
print("WRLGTNELNRHELUIRUNNHWND decomposition with HEL")
print(f"{'='*60}")

block = 'WRLGTNELNRHELUIRUNNHWND'
print(f"  Full block: {block} (23 chars)")
print(f"  With HEL: WRLGTNELNR + HEL + UIRUNNHWND")
print(f"  WRLGTNELNR (10 chars): sorted = {''.join(sorted('WRLGTNELNR'))}")
print(f"  UIRUNNHWND (10 chars): sorted = {''.join(sorted('UIRUNNHWND'))}")

# Check raw codes for this block
all_pairs = []
for bpairs in book_pairs_all:
    all_pairs.extend(bpairs)

raw_decoded = ''.join(v7.get(p, '?') for p in all_pairs)

# Find WRLGTNELNRHELUIRUNNHWND in raw decoded text (before anagrams)
pos = 0
print(f"\n  Raw code sequences for this block:")
while True:
    idx = raw_decoded.find(block, pos)
    if idx < 0: break
    # Get the codes that produce this block
    # Each char comes from one pair. Map back to pairs.
    # Position in raw_decoded = index of pair
    codes = all_pairs[idx:idx+len(block)]
    print(f"    pos {idx}: codes = {codes}")

    # Split at HEL position (chars 10-12)
    pre_codes = codes[:10]
    hel_codes = codes[10:13]
    post_codes = codes[13:]
    print(f"      WRLGTNELNR: {pre_codes}")
    print(f"      HEL:        {hel_codes}")
    print(f"      UIRUNNHWND: {post_codes}")

    # Are the HEL codes typical H, E, L codes?
    h_codes_all = [p for p in set(all_pairs) if v7.get(p) == 'H']
    e_codes_all = [p for p in set(all_pairs) if v7.get(p) == 'E']
    l_codes_all = [p for p in set(all_pairs) if v7.get(p) == 'L']
    print(f"      H codes in mapping: {sorted(h_codes_all)}")
    print(f"      E codes in mapping: {sorted(e_codes_all)}")
    print(f"      L codes in mapping: {sorted(l_codes_all)}")
    print(f"      HEL codes {hel_codes[0]}={v7.get(hel_codes[0],'?')}, {hel_codes[1]}={v7.get(hel_codes[1],'?')}, {hel_codes[2]}={v7.get(hel_codes[2],'?')}")
    pos = idx + 1

# ================================================================
# Check if HECHLLT also contains HEL
# ================================================================
print(f"\n{'='*60}")
print("HECHLLT - does it contain HEL?")
print(f"{'='*60}")

# HECHLLT has H-E-C-H-L-L-T
# Contains HE at start and potential HEL? No - HECHLLT starts with H-E-C
# not H-E-L
print(f"  HECHLLT: H-E-C-H-L-L-T")
print(f"  No HEL substring (C comes before L)")

# But HECHLLNRHELUIRUNNHWND appears in some places
# This is HECHLLT merged with NRHELUIRUNNHWND
pos = 0
print(f"\n  Checking HECHLL+NRHELUIRUNNHWND:")
while True:
    idx = processed.find('HECHLL', pos)
    if idx < 0: break
    after = processed[idx:idx+30]
    print(f"    pos {idx}: {after}")
    pos = idx + 1

print(f"\nDone.")
