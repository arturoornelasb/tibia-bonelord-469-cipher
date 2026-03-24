#!/usr/bin/env python3
"""
Session 18: Deep investigation of code 20 (F→N candidate).
Key question: Is code 20 really F, or is it N?

In MHG (Middle High German), many NHG F-words use V instead:
  NHG finden → MHG vinden
  NHG fern → MHG verre
  NHG fluch → MHG vluoch
  NHG fort → MHG vort
  NHG fach → NHG/MHG fach (compartment)

If the text is MHG, F should be rare. Let's check every occurrence of code 20.
"""
import json, os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

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

ANAGRAM_MAP = {
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
}

# Build book data
book_data = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        split_pos, digit = DIGIT_SPLITS[bidx]
        book = book[:split_pos] + digit + book[split_pos:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    text = ''.join(v7.get(p, '?') for p in pairs)
    book_data.append({'pairs': pairs, 'text': text})

print("=" * 80)
print("ALL OCCURRENCES OF CODE 20 (currently F)")
print("=" * 80)

total_code20 = 0
contexts = []
for bidx, bd in enumerate(book_data):
    for pos, pair in enumerate(bd['pairs']):
        if pair == '20':
            total_code20 += 1
            ctx_start = max(0, pos-8)
            ctx_end = min(len(bd['text']), pos+9)
            ctx = bd['text'][ctx_start:ctx_end]
            t_pos = pos - ctx_start

            # Apply anagram resolution to context for readability
            raw_ctx = bd['text'][max(0,pos-12):min(len(bd['text']),pos+13)]
            resolved_ctx = raw_ctx
            for ana in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
                resolved_ctx = resolved_ctx.replace(ana, ANAGRAM_MAP[ana])

            marker = ctx[:t_pos] + '[' + ctx[t_pos] + ']' + ctx[t_pos+1:]
            contexts.append((bidx, pos, marker, resolved_ctx))

print(f"\nTotal occurrences: {total_code20}")
print(f"\nAll occurrences with context (F=current, N=if changed):")
for bidx, pos, ctx, resolved in contexts:
    f_text = ctx
    n_text = ctx.replace('[F]', '[N]')
    print(f"  Book {bidx:2d} pos {pos:3d}: F: ...{f_text}...")
    print(f"                       N: ...{n_text}...")
    print()

# Key analysis: for each F occurrence, what word is it part of?
print("=" * 80)
print("WORD-LEVEL ANALYSIS: What word does each F/N belong to?")
print("=" * 80)

for bidx, pos, ctx, resolved in contexts:
    text = book_data[bidx]['text']
    # Get surrounding chars for word identification
    start = pos
    while start > 0 and text[start-1].isalpha() and text[start-1] != '?':
        start -= 1
    end = pos + 1
    while end < len(text) and text[end].isalpha() and text[end] != '?':
        end += 1

    word_with_f = text[start:end]
    word_with_n = word_with_f[:pos-start] + 'N' + word_with_f[pos-start+1:]

    # Check word boundaries - what recognized words are nearby?
    before = text[max(0,pos-15):pos]
    after = text[pos+1:min(len(text),pos+16)]

    # Specific word pattern checks
    f_words_found = []
    n_words_found = []

    # Check 3-8 char windows around the F position
    for wstart in range(max(0, pos-7), pos+1):
        for wend in range(pos+1, min(len(text), pos+8)):
            f_word = text[wstart:wend]
            n_word = f_word[:pos-wstart] + 'N' + f_word[pos-wstart+1:]

            KNOWN_CHECK = {'FACH', 'FAND', 'FERN', 'FEST', 'FORT', 'FINDEN',
                          'FLUCH', 'KRAFT', 'TIEF', 'RIEF', 'GRUFT',
                          'NACH', 'NACHT', 'NAME', 'NEIN', 'NICHT', 'NINDEN',
                          'NEUEN', 'HAND', 'WAND', 'SAND', 'LAND', 'BAND',
                          'SANG', 'SANG', 'DEN', 'NUN', 'NOTH', 'FINDEN',
                          'RUFEN', 'IN', 'AN', 'SEGEN', 'GEGEN'}
            if f_word in KNOWN_CHECK:
                f_words_found.append(f_word)
            if n_word in KNOWN_CHECK:
                n_words_found.append(n_word)

    print(f"  Book {bidx:2d} pos {pos:3d}: local='{word_with_f}' -> '{word_with_n}'")
    if f_words_found:
        print(f"    F-words found: {f_words_found}")
    if n_words_found:
        print(f"    N-words found: {n_words_found}")

# Summary analysis
print(f"\n{'=' * 80}")
print("SUMMARY: Code 20 = F vs N")
print("=" * 80)
print(f"""
Code 20 appears {total_code20} times total.

If F: German text has F-words like FACH, FINDEN, FERN
  - FACH (compartment) appears in "DIE NDCE FACH HECHLLT"
  - FINDEN (to find) appears in "FINDEN NEIGT DAS ES"
  - FERN (far) appears in "FINDEN D FERN DAS ES"
  - NLNDEF remains garbled

If N:
  - FACH -> NACH (after/towards) - "DIE NDCE NACH HECHLLT"
  - FINDEN -> NINDEN - BUT DP can still match: N+IN+DEN = 5/6 chars
  - FERN -> NERN - loses FERN
  - NLNDEF -> NLNDEN - DP can match DEN within it
  - Net coverage change: +11 chars

MHG argument for N:
  - In MHG, F is very rare. Most NHG F-words use V:
    vinden, verre, vluoch, vort, vrouwe, vuoz
  - FACH could remain as F (it's one of the few true F-words)
  - But MHG does use F in some words: fach, feuer

MHG argument for F:
  - FINDEN is a very strong contextual match
  - FERN is a strong contextual match
  - Having NO F-code means 0 F's in the text

Verdict: F appears more likely despite +11 gain from N.
The gain comes from coincidental short-word matches, not from
coherent narrative improvement.
""")

# Also check: does code 90 (N) ever appear where we'd expect F?
print("=" * 80)
print("CODE 90 (currently N) - does it ever look like it should be something else?")
print("=" * 80)

total_code90 = 0
code90_contexts = []
for bidx, bd in enumerate(book_data):
    for pos, pair in enumerate(bd['pairs']):
        if pair == '90':
            total_code90 += 1
            ctx_start = max(0, pos-6)
            ctx_end = min(len(bd['text']), pos+7)
            ctx = bd['text'][ctx_start:ctx_end]
            t_pos = pos - ctx_start
            marker = ctx[:t_pos] + '[' + ctx[t_pos] + ']' + ctx[t_pos+1:]
            code90_contexts.append((bidx, pos, marker))

print(f"\nCode 90 appears {total_code90} times:")
for bidx, pos, ctx in code90_contexts[:25]:
    n_ctx = ctx
    o_ctx = ctx.replace('[N]', '[O]')
    print(f"  Book {bidx:2d}: N: {n_ctx}  |  O: {o_ctx}")
