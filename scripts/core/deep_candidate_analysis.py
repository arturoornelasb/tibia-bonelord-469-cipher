#!/usr/bin/env python3
"""
Deep Candidate Analysis
========================
Investigate the most promising code reassignment candidates from the
constraint solver. For each candidate, show ALL contexts where the
code appears and evaluate whether the change makes sense globally.

Top candidates to investigate:
1. [29] E -> B/F/P (freq improvement, same coverage)
2. [13] A -> W (best combined improvement)
3. [41] E -> O (coverage + freq improvement)
4. [55] R -> M (freq improvement)
5. [10] R -> F (freq improvement)
6. [81] T -> N (would make GEIGET -> GEIGEN)
"""

import json, os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)

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

# ============================================================
# For each candidate, show every context where the code appears
# ============================================================
candidates = [
    ('29', 'E', ['B', 'F', 'P'], "freq improvement, E over-represented"),
    ('13', 'A', ['W'], "best combined improvement from v8 solver"),
    ('41', 'E', ['O'], "coverage+freq improvement"),
    ('55', 'R', ['M'], "freq improvement, R slightly over"),
    ('10', 'R', ['F'], "would add a needed F code"),
    ('81', 'T', ['N'], "would make GEIGET->GEIGEN"),
    ('02', 'D', ['B', 'F', 'P'], "would add needed B/F/P"),
]

for code, current, targets, reason in candidates:
    occ = code_counts.get(code, 0)
    print(f"\n{'=' * 70}")
    print(f"CODE [{code}] = {current} ({occ} occurrences)")
    print(f"Testing: {', '.join(targets)} | Reason: {reason}")
    print(f"{'=' * 70}")

    # Collect all contexts
    contexts = []
    for bidx, bpairs in enumerate(book_pairs):
        for i, p in enumerate(bpairs):
            if p == code:
                # Get wide context
                ctx_s = max(0, i - 6)
                ctx_e = min(len(bpairs), i + 7)
                ctx_codes = bpairs[ctx_s:ctx_e]
                pos_in_ctx = i - ctx_s

                text_current = ''
                for j, c in enumerate(ctx_codes):
                    letter = v7.get(c, '?')
                    if j == pos_in_ctx:
                        text_current += f'[{letter}]'
                    else:
                        text_current += letter

                texts_target = {}
                for tgt in targets:
                    text_t = ''
                    for j, c in enumerate(ctx_codes):
                        if j == pos_in_ctx:
                            text_t += f'[{tgt}]'
                        else:
                            text_t += v7.get(c, '?')
                    texts_target[tgt] = text_t

                contexts.append({
                    'book': bidx,
                    'pos': i,
                    'current': text_current,
                    'targets': texts_target,
                })

    # Show all contexts (limit to 15 for readability)
    for ctx in contexts[:15]:
        print(f"\n  Book {ctx['book']:2d} pos {ctx['pos']:3d}: {ctx['current']}")
        for tgt in targets:
            print(f"    {tgt}: {ctx['targets'][tgt]}")

    if len(contexts) > 15:
        print(f"\n  ... and {len(contexts) - 15} more occurrences")

    # ============================================================
    # Word participation analysis
    # ============================================================
    GERMAN_WORDS = set([
        'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO',
        'DU', 'OB', 'AM', 'IM', 'AB',
        'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST',
        'WIR', 'ICH', 'SIE', 'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT',
        'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI', 'VOR', 'FUR', 'VOM',
        'ZUM', 'ZUR', 'BIS', 'ALS', 'NUN', 'HIN', 'TAG', 'ORT', 'TOD',
        'NIE', 'ALT', 'NEU', 'GAR', 'SEI', 'TUN', 'HER', 'GEN', 'WEG',
        'ENDE', 'REDE', 'RUNE', 'WORT', 'NACH', 'AUCH',
        'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN', 'WARD', 'DASS', 'WENN',
        'DANN', 'DENN', 'ABER', 'ODER', 'WEIL', 'WIRD', 'EINE', 'DIES',
        'HIER', 'DORT', 'WELT', 'ZEIT', 'TEIL', 'WORT', 'NAME',
        'GANZ', 'SEHR', 'VIEL', 'FORT', 'HOCH', 'KLAR', 'ERDE', 'GOTT',
        'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN', 'WAHR', 'HELD', 'FACH',
        'WIND', 'FAND', 'GING', 'NAHM', 'SAGT', 'KANN', 'SOLL', 'WILL',
        'MUSS', 'GIBT', 'RIEF', 'LAND', 'HAND', 'BAND', 'SAND', 'WAND',
        'MACHT', 'KRAFT', 'GEIST', 'NACHT', 'LICHT', 'REICH',
        'UNTER', 'DURCH', 'GEGEN', 'IMMER', 'NICHT', 'SCHON',
        'DIESE', 'SEINE', 'EINEN', 'EINER', 'EINEM', 'EINES',
        'URALTE', 'STEINEN', 'STEINE', 'STEIN', 'RUNEN', 'FINDEN',
        'STEHEN', 'GEHEN', 'KOMMEN', 'SAGEN', 'WISSEN',
        'ERSTE', 'KOENIG', 'RUIN',
        'ORTE', 'ORTEN', 'WORTE', 'STEH', 'GEH',
        'ALLE', 'ALLES', 'VIELE', 'WIEDER', 'WISSET',
        'REDE', 'REDEN', 'WESEN', 'EHRE', 'GRAB', 'GRUFT',
        'ALTE', 'ALTEN', 'ALTER', 'NEUE', 'NEUEN',
        'DIESEN', 'DIESEM', 'DIESER', 'DIESES',
        'SEINER', 'SEINEN', 'SEINES', 'SEINEM',
        'EDEL', 'ADEL',
        'TEIL', 'TEILE', 'TEILEN', 'SEITE', 'SEITEN',
        'TAGE', 'TAGEN', 'NEBEN', 'LEBEN', 'GEBEN',
        'HABEN', 'SEHEN', 'NEHMEN',
        'FEUER', 'WASSER', 'STERN', 'STERNE',
        'OEL', 'SCE', 'MINNE', 'HWND',
        'LABGZERAS', 'HEDEMI', 'ADTHARSC', 'TAUTR',
        'EDETOTNIURG', 'SCHWITEIONE', 'AUNRSONGETRASES',
        'TIUMENGEMI', 'UTRUNR', 'HEARUCHTIG',
        'HIHL', 'EILCH', 'ENGCHD', 'KELSEI',
        'SANG', 'BRING', 'DING', 'RING',
        'SUCHE', 'SUCHEN', 'FRAGE', 'FRAGEN',
        'FEST', 'TIEF', 'RECHT', 'SCHLECHT',
        'GEIGEN', 'REIGEN', 'ZEIGEN', 'STEIGEN',
        'NEIGEN', 'SCHWEIGEN', 'EIGEN',
        'BEI', 'AUF', 'AUS', 'FUR',
        'BRIEF', 'STRAFE', 'KAMPF',
        'OBEN', 'UNTEN', 'INNEN', 'AUSSEN',
        'ABER', 'DENN', 'WEIL', 'ODER',
    ])

    # For each target, count how many contexts produce German words
    for tgt in targets:
        words_found_count = 0
        words_found = Counter()
        for ctx in contexts:
            # Check the target text for German words containing the changed position
            text = ctx['targets'][tgt].replace('[', '').replace(']', '')
            for wlen in range(2, min(len(text), 15) + 1):
                for start in range(len(text) - wlen + 1):
                    cand = text[start:start+wlen]
                    if cand in GERMAN_WORDS and tgt in cand:
                        words_found[cand] += 1

        current_words = Counter()
        for ctx in contexts:
            text = ctx['current'].replace('[', '').replace(']', '')
            for wlen in range(2, min(len(text), 15) + 1):
                for start in range(len(text) - wlen + 1):
                    cand = text[start:start+wlen]
                    if cand in GERMAN_WORDS and current in cand:
                        current_words[cand] += 1

        print(f"\n  As [{code}]={tgt}: words containing '{tgt}': {dict(words_found.most_common(10))}")
        print(f"  As [{code}]={current}: words containing '{current}': {dict(current_words.most_common(10))}")

# ============================================================
# SPECIAL: Deep GEIGET -> GEIGEN analysis
# ============================================================
print(f"\n{'=' * 70}")
print("SPECIAL ANALYSIS: GEIGET -> GEIGEN")
print("If [81] T->N, does GEIGEN (violins) make sense in context?")
print(f"{'=' * 70}")

# Find GEIGET in context
for bidx, bpairs in enumerate(book_pairs):
    text = ''.join(v7.get(p, '?') for p in bpairs)
    pos = text.find('GEIGET')
    if pos >= 0:
        ctx_s = max(0, pos - 20)
        ctx_e = min(len(text), pos + 26)
        ctx = text[ctx_s:ctx_e]
        # Show with T and with N
        test_map = dict(v7)
        test_map['81'] = 'N'
        text_n = ''.join(test_map.get(p, '?') for p in bpairs)
        ctx_n = text_n[ctx_s:ctx_e]
        print(f"\n  Book {bidx}:")
        print(f"    T: ...{ctx}...")
        print(f"    N: ...{ctx_n}...")

# Show ALL contexts where [81] appears (all 30 occurrences)
print(f"\n  ALL [{81}]=T contexts:")
count = 0
for bidx, bpairs in enumerate(book_pairs):
    for i, p in enumerate(bpairs):
        if p == '81':
            ctx_s = max(0, i - 4)
            ctx_e = min(len(bpairs), i + 5)
            text_t = ''
            text_n = ''
            for j, c in enumerate(bpairs[ctx_s:ctx_e]):
                if c == '81':
                    text_t += '[T]'
                    text_n += '[N]'
                else:
                    text_t += v7.get(c, '?')
                    text_n += v7.get(c, '?')
            print(f"    Book {bidx:2d}: {text_t}  |  {text_n}")
            count += 1
print(f"    Total: {count} occurrences")

# ============================================================
# SPECIAL: [10] R->F analysis (would give a much-needed F code)
# ============================================================
print(f"\n{'=' * 70}")
print("SPECIAL: [10] R->F (would add needed F code, only 13 occ)")
print(f"{'=' * 70}")

for bidx, bpairs in enumerate(book_pairs):
    for i, p in enumerate(bpairs):
        if p == '10':
            ctx_s = max(0, i - 5)
            ctx_e = min(len(bpairs), i + 6)
            text_r = ''
            text_f = ''
            for j, c in enumerate(bpairs[ctx_s:ctx_e]):
                if c == '10':
                    text_r += '[R]'
                    text_f += '[F]'
                else:
                    text_r += v7.get(c, '?')
                    text_f += v7.get(c, '?')
            print(f"  Book {bidx:2d}: {text_r}  |  {text_f}")

# ============================================================
# SPECIAL: [02] D->B/F/P analysis (only 4 occ, low-risk)
# ============================================================
print(f"\n{'=' * 70}")
print("SPECIAL: [02] D->B or F or P (only 4 occ, very low risk)")
print(f"{'=' * 70}")

for bidx, bpairs in enumerate(book_pairs):
    for i, p in enumerate(bpairs):
        if p == '02':
            ctx_s = max(0, i - 6)
            ctx_e = min(len(bpairs), i + 7)
            texts = {}
            for letter in ['D', 'B', 'F', 'P']:
                text = ''
                for j, c in enumerate(bpairs[ctx_s:ctx_e]):
                    if c == '02':
                        text += f'[{letter}]'
                    else:
                        text += v7.get(c, '?')
                texts[letter] = text
            print(f"  Book {bidx:2d}:")
            for letter in ['D', 'B', 'F', 'P']:
                print(f"    {letter}: {texts[letter]}")
