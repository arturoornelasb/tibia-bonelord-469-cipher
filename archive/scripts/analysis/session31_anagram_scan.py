#!/usr/bin/env python3
"""
Session 31: Scan garbled blocks for German word anagrams with swap tolerance.
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)

# Large German/MHG word list for anagram matching
GERMAN_WORDS = set()
for w in [
    'ABER', 'ACHT', 'ADEL', 'ALLE', 'ALSO', 'ALTE', 'ALTEN', 'ALTER', 'ALTES',
    'AMEN', 'ANDERE', 'ANGEL', 'ANGST', 'ARBEIT', 'ARME', 'ARMEN', 'ART',
    'AUCH', 'AUGE', 'AUGEN', 'AUS',
    'BAND', 'BERG', 'BERGE', 'BETEN', 'BETT', 'BILD', 'BITTE', 'BLUT',
    'BODEN', 'BOTE', 'BREIT', 'BRINGEN', 'BRUDER', 'BURG', 'BUSSE',
    'DANK', 'DANN', 'DARIN', 'DENN', 'DICH', 'DIENST', 'DING', 'DINGE',
    'DORT', 'DREI', 'DUNKEL', 'DURCH',
    'EDEL', 'EHRE', 'EHREN', 'EIGEN', 'EINST', 'ENDE', 'ERDE', 'ERDEN',
    'ERST', 'ERSTE', 'ERSTEN', 'EUCH', 'EUER', 'EWIG', 'EWIGE',
    'FESTE', 'FEUER', 'FINDEN', 'FLUCH', 'FLUCHT', 'FREI', 'FREUDE',
    'FRIEDE', 'FUERST', 'FUHR', 'FUER',
    'GARTEN', 'GAST', 'GEBET', 'GEBOT', 'GEGEN', 'GEHEN', 'GEIST',
    'GELD', 'GERICHT', 'GERN', 'GNADE', 'GOLD', 'GOTT', 'GOTTES',
    'GRAB', 'GRABEN', 'GREIS', 'GRIM', 'GRIMM', 'GROSS', 'GROSSE',
    'GRUEN', 'GRUND', 'GUT', 'GUTE', 'GUTEN', 'GUTER',
    'HALB', 'HALTE', 'HALTEN', 'HAND', 'HAUS', 'HEER', 'HEIL', 'HEILIG',
    'HEIM', 'HEIME', 'HEISS', 'HELD', 'HELDEN', 'HELDIN', 'HERR',
    'HERREN', 'HERZ', 'HERZE', 'HEUTE', 'HIER', 'HIMMEL', 'HOCH',
    'HUETER', 'HULD',
    'IMMER', 'INNEN',
    'JEDER', 'JENE', 'JENER', 'JUNG', 'JUNGE',
    'KAMPF', 'KEIN', 'KEINE', 'KEINER', 'KENNEN', 'KIND', 'KINDER',
    'KIRCHE', 'KLAGE', 'KLAR', 'KLEID', 'KLEIN', 'KOENIG', 'KRAFT',
    'KRIEG', 'KRONE', 'KUNST',
    'LAGE', 'LAND', 'LANG', 'LANGE', 'LANGEN', 'LANGER', 'LASS',
    'LASSEN', 'LAST', 'LAUT', 'LEBEN', 'LEGEN', 'LEHRE', 'LEID',
    'LEIDE', 'LEUTE', 'LICHT', 'LIEBE', 'LIEGEN', 'LIED', 'LIST',
    'LOHN', 'LOSE', 'LOSEN',
    'MACHT', 'MAGEN', 'MANN', 'MEER', 'MEIN', 'MEINE', 'MEINEN',
    'MEISTER', 'MENSCH', 'MILDE', 'MINE', 'MORGEN', 'MUOT', 'MUSS',
    'MUSSE', 'MUT', 'MUTTER',
    'NACH', 'NACHT', 'NACHTS', 'NAHE', 'NAME', 'NAMEN', 'NEHMEN',
    'NEID', 'NEIN', 'NENNEN', 'NEST', 'NEUE', 'NEUEN', 'NEUER',
    'NEUES', 'NICHT', 'NICHTS', 'NIMMT', 'NOCH', 'NORD', 'NOT', 'NOTH',
    'OBEN', 'ODER', 'OHNE',
    'PFLICHT', 'PLATZ', 'PREIS',
    'RACHE', 'RAT', 'RAUM', 'RECHT', 'RECHTE', 'REDE', 'REDEN',
    'REICH', 'REICHE', 'REICHEN', 'REIN', 'REISE', 'RETTER',
    'RICHTER', 'RING', 'RITTER', 'RUHM', 'RUHE', 'RUIN', 'RUNE',
    'RUNEN',
    'SACHE', 'SAGE', 'SAGEN', 'SAND', 'SANG', 'SCHAR', 'SCHATTEN',
    'SCHATZ', 'SCHLACHT', 'SCHLAG', 'SCHLECHT', 'SCHLOSS', 'SCHULD',
    'SCHUTZ', 'SCHWERT', 'SCHWUR', 'SEELE', 'SEGEN', 'SEID', 'SEIN',
    'SEINE', 'SEINEN', 'SEINER', 'SEIT', 'SICHER', 'SIEG', 'SIEGEL',
    'SINN', 'SITTE', 'SOLL', 'SOHN', 'SONDER', 'SORGE', 'SORGEN',
    'SPRECHEN', 'STAAT', 'STADT', 'STAERKE', 'STAMM', 'STAND', 'STARK',
    'STATT', 'STEHEN', 'STEIN', 'STEINE', 'STELLE', 'STILLE', 'STIMME',
    'STOLZ', 'STRAFE', 'STREIT', 'STUNDE',
    'TAT', 'TATEN', 'TEIL', 'TEILE', 'TEILEN', 'TIEFE', 'TIER',
    'TOD', 'TODE', 'TORE', 'TRAGEN', 'TRAUM', 'TREIBEN', 'TRETE',
    'TRETEN', 'TREU', 'TREUE', 'TROST', 'TRUTZ', 'TUN', 'TUER',
    'TUGEND',
    'UEBEL', 'UEBER', 'UNRECHT', 'UNTER', 'URTEIL',
    'VATER', 'VIEL', 'VIELE', 'VOLK',
    'WACHE', 'WAGE', 'WAGEN', 'WAHL', 'WAHR', 'WALD', 'WAND',
    'WARTE', 'WARTEN', 'WASSER', 'WEGE', 'WEGEN', 'WEHR', 'WEIB',
    'WEIL', 'WEISE', 'WEISEN', 'WELT', 'WENIG', 'WENN', 'WERK',
    'WERT', 'WESEN', 'WIDER', 'WILLE', 'WISSEN', 'WOHL', 'WOLF',
    'WORT', 'WORTE', 'WUNDER', 'WUERDE',
    'ZAHL', 'ZEICHEN', 'ZEIT', 'ZEITEN', 'ZORN', 'ZUCHT', 'ZWEI',
    # MHG specific
    'HERRE', 'VROUWE', 'MINNE', 'HUOTE', 'MUOZE', 'KUENE', 'TRIUWE',
    'SWAERE', 'LEIT', 'LIUTE', 'TUGENDE', 'GOTES', 'ELLIU',
    'WERLDE', 'SELE', 'KRIUZE', 'HOEHE',
    'DESTE', 'DETTE', 'DRITE', 'DRITTE',
    # Verbs (MHG/NHG)
    'GEBEN', 'HABEN', 'HALTEN', 'KOMMEN', 'LASSEN', 'MACHEN', 'RUFEN',
    'SAGEN', 'SCHREIBEN', 'SEHEN', 'SETZEN', 'STEHEN', 'SUCHEN',
    'TRAGEN', 'WISSEN', 'WOLLEN', 'ZEIGEN',
    'DIENT', 'STEHT', 'GEHT', 'KOMMT', 'NIMMT', 'GIBT', 'HAELT',
    'TRITT', 'WIRKT', 'HEISST', 'LIEGT', 'SITZT', 'BLEIBT',
    'WURDE', 'WAREN', 'HATTE', 'SAGTE', 'NAHM', 'GING', 'SOLL',
]:
    GERMAN_WORDS.add(w)

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
    2: (34, '0'), 5: (265, '1'), 6: (20, '0'), 8: (137, '7'),
    10: (277, '2'), 11: (137, '0'), 12: (0, '0'), 13: (55, '0'),
    14: (98, '1'), 15: (98, '0'), 18: (4, '0'), 19: (52, '0'),
    20: (5, '1'), 22: (7, '1'), 23: (14, '0'), 24: (47, '8'),
    25: (0, '0'), 29: (151, '1'), 32: (137, '1'), 34: (101, '0'),
    36: (78, '0'), 39: (44, '0'), 42: (91, '2'), 43: (26, '1'),
    45: (23, '7'), 46: (0, '2'), 48: (127, '0'), 49: (97, '1'),
    50: (136, '2'), 52: (0, '4'), 53: (248, '2'), 54: (49, '1'),
    60: (73, '9'), 61: (93, '7'), 64: (58, '4'), 65: (94, '0'),
    68: (4, '0'),
}

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
core_path = os.path.join(script_dir, '..', 'core', 'narrative_v3_clean.py')
with open(core_path, 'r') as f:
    core_source = f.read()
map_start = core_source.index('ANAGRAM_MAP = {')
map_end = core_source.index('\n}', map_start) + 2
exec(core_source[map_start:map_end])
known_start = core_source.index('KNOWN = set([')
known_end = core_source.index('])', known_start) + 2
exec(core_source[known_start:known_end])

resolved_text = all_text
for anagram in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved_text = resolved_text.replace(anagram, ANAGRAM_MAP[anagram])
resolved_text = resolved_text.replace('TREUUNR', 'TREUNUR')

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

tokens, covered = dp_segment(resolved_text, KNOWN)
total = sum(1 for c in resolved_text if c != '?')
print(f"Current: {covered}/{total} = {covered/total*100:.2f}%")

# Check each garbled block for anagram matches
print("\n=== GARBLED BLOCKS -> GERMAN WORD ANAGRAMS ===")
seen = set()
for i, tok in enumerate(tokens):
    if not tok.startswith('{'):
        continue
    block = tok[1:-1]
    if '?' in block or len(block) < 3 or block in seen:
        continue
    seen.add(block)

    block_counter = Counter(block)

    matches = []
    for word in GERMAN_WORDS:
        if len(word) != len(block):
            continue
        # Check exact anagram
        if sorted(word) == sorted(block):
            matches.append((word, 0, 'exact'))
            continue
        # Check with I<->E, I<->L swaps
        word_counter = Counter(word)
        swaps = 0
        possible = True
        temp = dict(block_counter)
        for letter, count in word_counter.items():
            have = temp.get(letter, 0)
            if have >= count:
                temp[letter] = have - count
            else:
                deficit = count - have
                if letter == 'E' and temp.get('I', 0) >= deficit:
                    temp['I'] -= deficit
                    swaps += deficit
                elif letter == 'I' and temp.get('E', 0) >= deficit:
                    temp['E'] -= deficit
                    swaps += deficit
                elif letter == 'L' and temp.get('I', 0) >= deficit:
                    temp['I'] -= deficit
                    swaps += deficit
                elif letter == 'I' and temp.get('L', 0) >= deficit:
                    temp['L'] -= deficit
                    swaps += deficit
                else:
                    possible = False
                    break
        if possible and swaps <= 2 and sum(temp.values()) == 0:
            matches.append((word, swaps, 'swap'))

    if matches:
        ctx_l = ' '.join(tokens[max(0, i-3):i])
        ctx_r = ' '.join(tokens[i+1:min(len(tokens), i+4)])
        print(f"\n  {{{block}}} ({len(block)} chars)")
        print(f"    ctx: ...{ctx_l[-40:]} [{block}] {ctx_r[:40]}...")
        for word, swaps, kind in matches:
            print(f"    -> {word} ({kind}, {swaps} swaps)")

# Also check EETTR specifically (known good candidate)
print("\n=== CONFIRMED FIXUPS ===")
print(f"  EETTR -> TRETE (unique in resolved text, +5 chars)")
count = resolved_text.count('EETTR')
pos = resolved_text.find('EETTR')
print(f"    Occurrences: {count}")
print(f"    Context: ...{resolved_text[pos-15:pos+20]}...")

# Now look for raw-text anagram opportunities
# Find stretches of raw text NOT covered by any ANAGRAM_MAP entry
print("\n=== UNRESOLVED RAW TEXT STRETCHES (>= 5 chars) ===")
# Mark which positions are covered by ANAGRAM_MAP
raw_covered = [False] * len(all_text)
for anagram in ANAGRAM_MAP:
    start = 0
    while True:
        pos = all_text.find(anagram, start)
        if pos < 0:
            break
        for j in range(pos, pos + len(anagram)):
            raw_covered[j] = True
        start = pos + 1

# Find uncovered stretches
stretches = []
i = 0
while i < len(all_text):
    if not raw_covered[i] and all_text[i] != '?':
        j = i
        while j < len(all_text) and not raw_covered[j] and all_text[j] != '?':
            j += 1
        stretch = all_text[i:j]
        if len(stretch) >= 5:
            stretches.append((i, stretch))
        i = j
    else:
        i += 1

# Show top stretches
for pos, stretch in sorted(stretches, key=lambda x: -len(x[1]))[:15]:
    ctx_before = all_text[max(0, pos-10):pos]
    ctx_after = all_text[pos+len(stretch):pos+len(stretch)+10]
    print(f"  [{len(stretch):3d}ch @ {pos}] {ctx_before}|{stretch}|{ctx_after}")
