#!/usr/bin/env python3
"""
Find the Missing B, F, P Codes
================================
German text MUST have B (~1.89%), F (~1.66%), P (~0.79%).
Currently: B=0.34% (1 code), F=0.45% (1 code), P=0.00% (0 codes).

Strategy: For each over-represented letter (I, D, E, N), check if
any of its codes produce GERMAN WORDS with B/F/P when changed.

The key insight: if a code is currently mapped as I but should be B,
then everywhere it appears in the text, the neighbors should form
valid German bigrams with B (not I).

Uses German bigram fitness scoring instead of DP word coverage.
"""

import json, os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)

# German bigram log-probabilities (relative, higher = more common)
# Based on standard German text analysis
BIGRAM_SCORE = {}
# Very common bigrams (score 3)
for bg in ['EN', 'ER', 'CH', 'DE', 'EI', 'ND', 'TE', 'IN', 'IE', 'GE',
           'ES', 'NE', 'UN', 'ST', 'RE', 'HE', 'AN', 'BE', 'SE', 'HA',
           'AU', 'NG', 'DI', 'LE', 'IC', 'DA', 'SS', 'SC', 'SI', 'SO']:
    BIGRAM_SCORE[bg] = 3
# Common bigrams (score 2)
for bg in ['TI', 'EL', 'AL', 'AR', 'MA', 'WE', 'UR', 'UE', 'MI', 'AB',
           'LI', 'NI', 'OR', 'ME', 'RI', 'ZU', 'DO', 'WI', 'DU', 'AG',
           'NA', 'RA', 'US', 'ET', 'EM', 'HI', 'EE', 'ON', 'TA', 'ED',
           'IT', 'FU', 'FA', 'FE', 'FI', 'FL', 'FR', 'BA', 'BI', 'BL',
           'BR', 'BU', 'PF', 'PL', 'PR', 'PA', 'PE', 'PI']:
    BIGRAM_SCORE[bg] = 2
# Less common but valid (score 1)
for bg in ['FO', 'BO', 'PO', 'BU', 'FU', 'PU', 'AF', 'EF', 'IF', 'OF',
           'UF', 'AB', 'EB', 'IB', 'OB', 'UB', 'AP', 'EP', 'IP', 'OP',
           'UP', 'FB', 'BF', 'LB', 'LF', 'LP', 'MB', 'MF', 'MP',
           'NB', 'NF', 'NP', 'RB', 'RF', 'RP', 'SB', 'SF', 'SP']:
    BIGRAM_SCORE[bg] = 1

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
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

code_counts = Counter()
for bpairs in book_pairs:
    code_counts.update(bpairs)

def bigram_fitness(mapping, code, letter):
    """Score how well a code fits as a given letter based on surrounding bigrams."""
    total_score = 0
    total_positions = 0
    for bpairs in book_pairs:
        for i, p in enumerate(bpairs):
            if p == code:
                total_positions += 1
                # Check left bigram
                if i > 0:
                    prev = mapping.get(bpairs[i-1], '?')
                    if prev != '?':
                        bg = prev + letter
                        total_score += BIGRAM_SCORE.get(bg, 0)
                # Check right bigram
                if i < len(bpairs) - 1:
                    nxt = mapping.get(bpairs[i+1], '?')
                    if nxt != '?':
                        bg = letter + nxt
                        total_score += BIGRAM_SCORE.get(bg, 0)
    avg = total_score / max(total_positions, 1)
    return avg, total_positions

print("=" * 70)
print("FINDING MISSING B, F, P CODES")
print("=" * 70)

# For each code mapped to an over-represented letter,
# compare bigram fitness of current assignment vs B/F/P
over_codes = []
for code, letter in v7.items():
    if letter in ('I', 'D', 'E', 'N') and code_counts.get(code, 0) >= 10:
        over_codes.append((code, letter))

print(f"\nTesting {len(over_codes)} codes from over-represented letters (I, D, E, N)")
print(f"Checking if they fit better as B, F, or P\n")

candidates = []
for code, current in sorted(over_codes, key=lambda x: code_counts.get(x[0], 0)):
    occ = code_counts.get(code, 0)
    current_fit, positions = bigram_fitness(v7, code, current)

    for target in ['B', 'F', 'P']:
        target_fit, _ = bigram_fitness(v7, code, target)

        if target_fit > current_fit * 0.5 and target_fit >= 1.0:
            candidates.append({
                'code': code,
                'current': current,
                'target': target,
                'current_fit': current_fit,
                'target_fit': target_fit,
                'occ': occ,
                'ratio': target_fit / max(current_fit, 0.01),
            })

# Sort by target fitness
candidates.sort(key=lambda x: -x['target_fit'])

print(f"{'Code':>5} {'Cur':>4} {'Tgt':>4} {'Occ':>5} {'CurFit':>7} {'TgtFit':>7} {'Ratio':>6}")
print("-" * 50)
for c in candidates[:30]:
    marker = " ***" if c['ratio'] > 0.8 else ""
    print(f"  [{c['code']:>2}] {c['current']:>4} {c['target']:>4} {c['occ']:>5} "
          f"{c['current_fit']:>6.2f} {c['target_fit']:>6.2f} {c['ratio']:>5.2f}{marker}")

# ============================================================
# DEEP ANALYSIS of top B/F/P candidates
# ============================================================
print(f"\n{'=' * 70}")
print("DETAILED CONTEXT FOR TOP CANDIDATES")
print(f"{'=' * 70}")

# Show actual context for top candidates
for c in candidates[:10]:
    code = c['code']
    target = c['target']
    occ = c['occ']
    current = c['current']

    print(f"\n  [{code}] {current}->{target} ({occ} occ, ratio={c['ratio']:.2f}):")

    # Show every context where this code appears
    examples = []
    for bpairs in book_pairs:
        for i, p in enumerate(bpairs):
            if p == code:
                ctx_start = max(0, i - 5)
                ctx_end = min(len(bpairs), i + 6)
                ctx_codes = bpairs[ctx_start:ctx_end]

                # Decode with current mapping
                current_text = ''
                for j, cp in enumerate(ctx_codes):
                    if cp == code:
                        current_text += f'[{current}]'
                    else:
                        current_text += v7.get(cp, '?')

                # Decode with target letter
                target_text = ''
                for j, cp in enumerate(ctx_codes):
                    if cp == code:
                        target_text += f'[{target}]'
                    else:
                        target_text += v7.get(cp, '?')

                examples.append((current_text, target_text))

    # Show unique contexts
    seen = set()
    for curr, tgt in examples[:8]:
        key = curr
        if key not in seen:
            seen.add(key)
            print(f"    {curr}")
            print(f"    {tgt}")

# ============================================================
# GERMAN WORD TEST: which codes create German words as B/F/P?
# ============================================================
print(f"\n{'=' * 70}")
print("GERMAN WORD EMERGENCE TEST")
print("Testing: does changing X->B/F/P create recognizable German words?")
print(f"{'=' * 70}")

GERMAN_WORDS = set([
    'AB', 'OB', 'BEI', 'BIS', 'BAU', 'BAD', 'BIN', 'BOG',
    'ABER', 'BALD', 'BAND', 'BAUM', 'BERG', 'BEIN', 'BEST',
    'BIER', 'BILD', 'BLAU', 'BLUT', 'BOGEN', 'BOTE', 'BREIT',
    'BRIEF', 'BROT', 'BRUST', 'BUCH', 'BURG', 'BUSCH',
    'GEBEN', 'HABEN', 'LEBEN', 'LIEBEN', 'GRABEN', 'TREIBEN',
    'GLAUBE', 'LIEBE', 'GRUBE', 'STUBE', 'FARBE', 'NARBE',
    'HERB', 'DERB', 'GRAB', 'STAB', 'STAUB',
    # F words
    'FUR', 'FAR', 'FEL', 'FER', 'FIN',
    'FALL', 'FAND', 'FAST', 'FEIN', 'FELD', 'FERN', 'FEST',
    'FEHL', 'FEIER', 'FEIND', 'FEUER', 'FIEL', 'FINDEN',
    'FLUCHT', 'FLUCH', 'FLUG', 'FLUSS', 'FOLGE', 'FORT',
    'FRAGE', 'FRAU', 'FREI', 'FREMD', 'FREUDE', 'FREUND',
    'FRIEDE', 'FRIEDEN', 'FRUCHT', 'FRUEH', 'FUEHREN',
    'FUERST', 'FURCHT', 'FUSS',
    'RUFEN', 'SCHAFFEN', 'STRAFEN', 'TREFFEN', 'HELFEN',
    'TIEF', 'BRIEF', 'SCHLAF', 'GRAF', 'DARF',
    'AUF', 'AUF', 'LAUF', 'KAUF',
    # P words
    'PAAR', 'PAKT', 'PLATZ', 'PREIS', 'PFAD', 'PFEIL',
    'PFLICHT', 'PFLEGE', 'PFORTE', 'PRIESTER',
    'OPFER', 'KAMPF', 'KOPF', 'TOPF', 'HAUPT',
    'SPRUCH', 'SPRACHE', 'SPRUNG',
])

# For each candidate, check if changing creates any German words in context
for c in candidates[:15]:
    code = c['code']
    target = c['target']
    current = c['current']

    # Build modified mapping
    test_map = dict(v7)
    test_map[code] = target

    # Find all 3-6 letter sequences containing this code
    word_hits = Counter()
    for bpairs in book_pairs:
        text_new = ''.join(test_map.get(p, '?') for p in bpairs)
        text_old = ''.join(v7.get(p, '?') for p in bpairs)

        # Find positions where the code appears
        for i, p in enumerate(bpairs):
            if p == code:
                # Check windows of size 2-8 centered on position i
                for wstart in range(max(0, i-5), i+1):
                    for wend in range(i+1, min(len(bpairs), i+6)+1):
                        word = text_new[wstart:wend]
                        if word.upper() in GERMAN_WORDS and target in word.upper():
                            word_hits[word.upper()] += 1

    if word_hits:
        print(f"\n  [{code}] {current}->{target}: German words found!")
        for word, count in word_hits.most_common(10):
            print(f"    {word} ({count}x)")
