#!/usr/bin/env python3
"""Quick test of NIT and TOT as new KNOWN words."""
import json, os
from collections import Counter

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
    'IEB': 'BEI',
    'TNEDAS': 'STANDE', 'NSCHAT': 'NACHTS', 'SANGE': 'SAGEN',
}

resolved = all_text
for anag in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
    resolved = resolved.replace(anag, ANAGRAM_MAP[anag])

KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR', 'NU', 'STANDE', 'NACHTS',
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
    'OEL', 'SCE', 'MINNE', 'MIN', 'ODE', 'SER', 'GEN', 'INS',
    'GEIGET', 'BERUCHTIG', 'BERUCHTIGER',
    'MEERE', 'NEIGT', 'WISTEN', 'MANIER', 'HUND',
    'GODE', 'GODES', 'EIGENTUM', 'REDER',
    'THENAEUT', 'LABT', 'MORT', 'DIGE', 'WEGE', 'KOENIGS',
    'NAHE', 'NOT', 'NOTH', 'ZUR', 'OWI', 'ENGE', 'SEIDEN',
    'ALTES', 'NUT', 'NUTZ', 'HEIL', 'NEID', 'TREU', 'TREUE',
    'SUN', 'DIENST', 'SANG', 'DINC', 'HULDE', 'LANT', 'HERRE',
    'DIENEST', 'GEBOT', 'SCHWUR', 'ORDEN', 'RICHTER', 'DUNKEL',
    'EHRE', 'EDELE', 'SCHULD', 'SEGEN', 'FLUCH', 'RACHE',
    'KOENIG', 'DASS', 'EDEL', 'ADEL',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME', 'SCHARDT',
])

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

total = sum(1 for c in resolved if c != '?')
_, baseline = dp_segment(resolved, KNOWN)
print(f"Baseline: {baseline}/{total} = {baseline/total*100:.1f}%")

# Test NIT
print(f"\n=== NIT (MHG 'not', variant of niht) ===")
test1 = set(KNOWN)
test1.add('NIT')
tokens1, cov1 = dp_segment(resolved, test1)
print(f"  +NIT: {cov1}/{total} = {cov1/total*100:.1f}% ({cov1-baseline:+d})")

# Show where NIT matches
for i, t in enumerate(tokens1):
    if t == 'NIT':
        before = tokens1[max(0,i-3):i]
        after = tokens1[i+1:min(len(tokens1),i+4)]
        print(f"  [{' '.join(before)}] NIT [{' '.join(after)}]")

# Test TOT
print(f"\n=== TOT (dead) ===")
test2 = set(KNOWN)
test2.add('TOT')
tokens2, cov2 = dp_segment(resolved, test2)
print(f"  +TOT: {cov2}/{total} = {cov2/total*100:.1f}% ({cov2-baseline:+d})")

for i, t in enumerate(tokens2):
    if t == 'TOT':
        before = tokens2[max(0,i-3):i]
        after = tokens2[i+1:min(len(tokens2),i+4)]
        print(f"  [{' '.join(before)}] TOT [{' '.join(after)}]")

# Test both together
print(f"\n=== NIT + TOT combined ===")
test3 = set(KNOWN)
test3.add('NIT')
test3.add('TOT')
_, cov3 = dp_segment(resolved, test3)
print(f"  +NIT+TOT: {cov3}/{total} = {cov3/total*100:.1f}% ({cov3-baseline:+d})")

# Also test: MIR (me, dative), IHR (her/their), MIT (with)
print(f"\n=== Additional MHG/German words ===")
candidates = [
    ('MIR', 'me (dative)'),
    ('IHR', 'her/their'),
    ('MIT', 'with'),
    ('IHN', 'him (accusative)'),
    ('MUT', 'courage'),
    ('RUH', 'rest/peace'),
    ('TAL', 'valley'),
    ('TOR', 'gate/fool'),
    ('WEG', 'way/path'),
    ('HOF', 'court'),
    ('RAT', 'counsel'),
    ('BALD', 'soon'),
    ('GEHT', 'goes'),
    ('SOLL', 'shall'),
    ('WOHL', 'well/indeed'),
    ('LEID', 'suffering'),
    ('EHREN', 'to honor'),
    ('STUND', 'hour (MHG)'),
    ('DAROB', 'thereupon'),
]

for word, desc in candidates:
    if word in KNOWN:
        continue
    test = set(KNOWN)
    test.add(word)
    _, cov = dp_segment(resolved, test)
    delta = cov - baseline
    if delta > 0:
        print(f"  {word} ({desc}): +{delta}")
        # Show first 2 contexts
        tokens_t, _ = dp_segment(resolved, test)
        count = 0
        for i, t in enumerate(tokens_t):
            if t == word:
                before = tokens_t[max(0,i-2):i]
                after = tokens_t[i+1:min(len(tokens_t),i+3)]
                print(f"    [{' '.join(before)}] {word} [{' '.join(after)}]")
                count += 1
                if count >= 2:
                    break

# Mass test: try ALL 3-letter combinations from A-Z
print(f"\n=== Mass 3-letter word scan ===")
big_gains = []
for a in 'ABCDEFGHIKLMNORSTUWZ':
    for b in 'ABCDEFGHIKLMNORSTUWZ':
        for c in 'ABCDEFGHIKLMNORSTUWZ':
            w = a + b + c
            if w in KNOWN:
                continue
            # Quick count: does it even appear?
            count = resolved.count(w)
            if count >= 3:
                test = set(KNOWN)
                test.add(w)
                _, cov = dp_segment(resolved, test)
                delta = cov - baseline
                if delta >= 6:  # At least +6 to be interesting
                    big_gains.append((w, delta, count))

big_gains.sort(key=lambda x: -x[1])
print(f"  3-letter words with +6 or more coverage:")
for w, delta, count in big_gains[:15]:
    print(f"  {w}: +{delta} ({count} appearances)")
