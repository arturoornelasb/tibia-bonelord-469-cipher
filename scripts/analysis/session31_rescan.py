#!/usr/bin/env python3
"""Session 31: Rescan garbled blocks after DIGIT_SPLIT optimization."""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)

core_path = os.path.join(script_dir, '..', 'core', 'narrative_v3_clean.py')
with open(core_path, 'r') as f:
    core_source = f.read()
map_start = core_source.index('ANAGRAM_MAP = {')
map_end = core_source.index('\n}', map_start) + 2
exec(core_source[map_start:map_end])
known_start = core_source.index('KNOWN = set([')
known_end = core_source.index('])', known_start) + 2
exec(core_source[known_start:known_end])
ds_start = core_source.index('DIGIT_SPLITS = {')
ds_end = core_source.index('\n}', ds_start) + 2
exec(core_source[ds_start:ds_end])

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

decoded_books = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        split_pos, digit = DIGIT_SPLITS[bidx]
        book = book[:split_pos] + digit + book[split_pos:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    text = ''.join(v7.get(p, '?') for p in pairs)
    decoded_books.append(text)

all_text = ''.join(decoded_books)
resolved = all_text
for anagram in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved = resolved.replace(anagram, ANAGRAM_MAP[anagram])
resolved = resolved.replace('TREUUNR', 'TREUNUR')
resolved = resolved.replace('EETTR', 'TRETE')

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

tokens, covered = dp_segment(resolved, KNOWN)
total = sum(1 for c in resolved if c != '?')

# German word list
GERMAN = {
    'ABER', 'ACHT', 'ADEL', 'ALLE', 'ALSO', 'ALTE', 'ALTEN', 'ALTER',
    'AMEN', 'ANGST', 'ARME', 'ART', 'AUCH', 'AUS', 'BAND', 'BERG',
    'BETT', 'BILD', 'BLUT', 'BOTE', 'BREIT', 'BRUDER', 'BURG',
    'DANK', 'DANN', 'DENN', 'DICH', 'DIENST', 'DING', 'DORT', 'DREI',
    'DURCH', 'EDEL', 'EHRE', 'EHREN', 'EIGEN', 'EINST', 'ENDE', 'ERDE',
    'ERST', 'ERSTE', 'EUCH', 'EWIG', 'FESTE', 'FEUER', 'FINDEN', 'FLUCH',
    'FREI', 'FRIEDE', 'GARTEN', 'GAST', 'GEBET', 'GEBOT', 'GEGEN', 'GEHEN',
    'GEIST', 'GELD', 'GERN', 'GNADE', 'GOLD', 'GOTT', 'GOTTES', 'GRAB',
    'GREIS', 'GROSS', 'GRUND', 'GUT', 'GUTE', 'HALB', 'HALTE', 'HALTEN',
    'HAND', 'HAUS', 'HEER', 'HEIL', 'HEILIG', 'HEIM', 'HEISS', 'HELD',
    'HERR', 'HERZ', 'HIER', 'HIMMEL', 'HOCH', 'HULD', 'IMMER',
    'JEDER', 'JENE', 'JUNG', 'KAMPF', 'KEIN', 'KIND', 'KIRCHE', 'KLAGE',
    'KLAR', 'KLEID', 'KLEIN', 'KOENIG', 'KRAFT', 'KRIEG', 'KRONE', 'KUNST',
    'LAND', 'LANG', 'LANGE', 'LASS', 'LAST', 'LAUT', 'LEBEN', 'LEHRE',
    'LEID', 'LEUTE', 'LICHT', 'LIEBE', 'LIED', 'LIST', 'LOHN', 'MACHT',
    'MANN', 'MEER', 'MEIN', 'MEISTER', 'MENSCH', 'MILDE', 'MORGEN', 'MUT',
    'NACH', 'NACHT', 'NACHTS', 'NAME', 'NAMEN', 'NEID', 'NEIN', 'NEST',
    'NEUE', 'NICHT', 'NICHTS', 'NIMMT', 'NOCH', 'NORD', 'NOT',
    'OBEN', 'ODER', 'OHNE', 'PFLICHT', 'PREIS', 'RACHE', 'RAT', 'RAUM',
    'RECHT', 'REDE', 'REICH', 'REIN', 'REISE', 'RETTER', 'RICHTER', 'RING',
    'RITTER', 'RUHM', 'RUHE', 'RUIN', 'RUNE', 'RUNEN', 'SACHE', 'SAGE',
    'SAGEN', 'SAND', 'SANG', 'SCHAR', 'SCHATZ', 'SCHLAG', 'SCHULD',
    'SCHWERT', 'SCHWUR', 'SEELE', 'SEGEN', 'SEID', 'SEIN', 'SEINE', 'SEIT',
    'SIEG', 'SINN', 'SITTE', 'SOLL', 'SOHN', 'SORGE', 'STADT', 'STAMM',
    'STAND', 'STARK', 'STATT', 'STEHEN', 'STEIN', 'STEINE', 'STELLE',
    'STILLE', 'STOLZ', 'STRAFE', 'STREIT', 'STUNDE', 'TAT', 'TEIL', 'TIEFE',
    'TOD', 'TORE', 'TRAGEN', 'TRAUM', 'TRETE', 'TRETEN', 'TREU', 'TREUE',
    'TROST', 'TUN', 'TUGEND', 'UEBEL', 'UEBER', 'UNTER', 'URTEIL',
    'VATER', 'VIEL', 'VOLK', 'WACHE', 'WAGE', 'WAGEN', 'WAHL', 'WAHR',
    'WALD', 'WAND', 'WARTEN', 'WASSER', 'WEGE', 'WEHR', 'WEIL', 'WEISE',
    'WELT', 'WENIG', 'WENN', 'WERK', 'WERT', 'WESEN', 'WIDER', 'WILLE',
    'WISSEN', 'WOHL', 'WOLF', 'WORT', 'WORTE', 'WUNDER', 'ZAHL', 'ZEICHEN',
    'ZEIT', 'ZORN', 'ZUCHT', 'ZWEI',
    'HERRE', 'MINNE', 'LEIT', 'LIUTE', 'GOTES', 'SELE', 'DRITTE',
    'DIENT', 'STEHT', 'GEHT', 'KOMMT', 'NIMMT', 'GIBT', 'TRITT',
}

# Check all garbled 3-6 char blocks for anagram matches
seen = set()
fixups = []
for i, tok in enumerate(tokens):
    if not tok.startswith('{'):
        continue
    block = tok[1:-1]
    if '?' in block or len(block) < 3 or len(block) > 8 or block in seen:
        continue
    seen.add(block)

    block_counter = Counter(block)
    for word in GERMAN:
        if len(word) != len(block):
            continue
        # Exact anagram
        if sorted(word) == sorted(block):
            count = resolved.count(block)
            ctx_l = ' '.join(tokens[max(0, i-3):i])
            ctx_r = ' '.join(tokens[i+1:min(len(tokens), i+4)])
            fixups.append((block, word, 'exact', 0, ctx_l, ctx_r, count))
            break
        # Swap check
        word_c = Counter(word)
        swaps = 0
        possible = True
        temp = dict(block_counter)
        for letter, cnt in word_c.items():
            have = temp.get(letter, 0)
            if have >= cnt:
                temp[letter] = have - cnt
            else:
                deficit = cnt - have
                swapped = False
                for src, dst in [('I', 'E'), ('E', 'I'), ('I', 'L'), ('L', 'I')]:
                    if letter == dst and temp.get(src, 0) >= deficit:
                        temp[src] -= deficit
                        swaps += deficit
                        swapped = True
                        break
                if not swapped:
                    possible = False
                    break
        if possible and swaps <= 2 and sum(temp.values()) == 0:
            count = resolved.count(block)
            ctx_l = ' '.join(tokens[max(0, i-3):i])
            ctx_r = ' '.join(tokens[i+1:min(len(tokens), i+4)])
            fixups.append((block, word, 'swap', swaps, ctx_l, ctx_r, count))
            break

print(f"Coverage: {covered}/{total} = {covered/total*100:.2f}%")
print(f"\nGarbled blocks matching German words (3+ chars):")
for block, word, kind, sw, ctx_l, ctx_r, count in fixups:
    safe = "(UNIQUE)" if count == 1 else f"({count}x)"
    print(f"  {block} -> {word} ({kind}, {sw} swaps) {safe}")
    print(f"    ctx: ...{ctx_l[-35:]} [{block}] {ctx_r[:35]}...")

# Also show all remaining garbled blocks by size
garbled_counts = Counter()
for tok in tokens:
    if tok.startswith('{') and '?' not in tok[1:-1]:
        garbled_counts[len(tok[1:-1])] += 1

print(f"\nGarbled block size distribution:")
for size in sorted(garbled_counts):
    print(f"  {size}-char blocks: {garbled_counts[size]}")
total_garbled = sum(len(tok[1:-1]) for tok in tokens if tok.startswith('{') and '?' not in tok[1:-1])
total_blocks = sum(1 for tok in tokens if tok.startswith('{') and '?' not in tok[1:-1])
print(f"\nTotal: {total_blocks} blocks, {total_garbled} chars")
print(f"Gap to 100%: {total - covered} chars ({(total-covered)/total*100:.1f}%)")
