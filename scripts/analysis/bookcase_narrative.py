#!/usr/bin/env python3
"""
Decode the Hellgate Library narrative in BOOKCASE ORDER.
Compare to index order - does the physical arrangement reveal a different story?
Also check if books within the same bookcase chain/overlap.
"""
import json, os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'bookcase_mapping.json'), 'r') as f:
    bc_map = json.load(f)

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
    'IEB': 'BEI',  # NEW: exact anagram, 3x
}

KNOWN = set([
    'AB', 'AM', 'AN', 'ALS', 'AUF', 'AUS', 'BEI', 'DA', 'DAS', 'DEM',
    'DEN', 'DER', 'DES', 'DIE', 'DU', 'ER', 'ES', 'IM', 'IN', 'IST',
    'JA', 'MAN', 'OB', 'SO', 'UM', 'UND', 'VON', 'VOR', 'WO', 'ZU',
    'EIN', 'ICH', 'SIE', 'WER', 'WIE', 'WAS', 'WIR',
    'GEH', 'GIB', 'HAT', 'HIN', 'HER', 'NUN', 'NUR', 'SEI', 'TUN',
    'SAG', 'WAR', 'ODE', 'SER', 'GEN', 'INS', 'MIN', 'OEL', 'SCE',
    'NU',  # MHG: now (same as NUN)
    'ABER', 'ALLE', 'ALLES', 'ALTE', 'ALTEN', 'ALTER', 'AUCH', 'BAND',
    'BERG', 'BURG', 'DENN', 'DIES', 'DOCH', 'DORT', 'DREI', 'DURCH',
    'EINE', 'EINEM', 'EINEN', 'EINER', 'EINES', 'ENDE', 'ERDE', 'ERST',
    'ERSTE', 'FACH', 'FAND', 'FERN', 'FEST', 'FORT', 'GAR', 'GANZ',
    'GEGEN', 'GEIST', 'GOTT', 'GOLD', 'GRAB', 'GROSS', 'GRUFT', 'GUT',
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
    'ZEHN', 'ZORN', 'FINDEN', 'GEBEN', 'GEHEN', 'HABEN', 'KOMMEN',
    'LEBEN', 'LESEN', 'NEHMEN', 'SAGEN', 'SEHEN', 'STEHEN', 'SUCHEN',
    'WISSEN', 'WISSET', 'RUFEN', 'WIEDER', 'GEIGET', 'BERUCHTIG',
    'BERUCHTIGER', 'MEERE', 'NEIGT', 'WISTEN', 'MANIER', 'HUND',
    'GODE', 'GODES', 'EIGENTUM', 'REDER', 'THENAEUT', 'LABT', 'MORT',
    'DIGE', 'WEGE', 'KOENIGS', 'NAHE', 'NOT', 'NOTH', 'ZUR', 'OWI',
    'ENGE', 'SEIDEN', 'ALTES', 'BIS', 'NUT', 'NUTZ', 'HEIL', 'NEID',
    'TREU', 'TREUE', 'SUN', 'DIENST', 'SANG', 'DINC', 'HULDE',
    'LANT', 'HERRE', 'DIENEST', 'GEBOT', 'SCHWUR', 'ORDEN',
    'RICHTER', 'DUNKEL', 'EHRE', 'EDELE', 'SCHULD', 'SEGEN',
    'FLUCH', 'RACHE', 'KOENIG', 'DASS', 'EDEL', 'ADEL',
    'SALZBERG', 'WEICHSTEIN', 'ORANGENSTRASSE',
    'GOTTDIENER', 'GOTTDIENERS', 'TRAUT', 'LEICH', 'HEIME', 'SCHARDT',
])

def dp_segment(text):
    n = len(text)
    dp = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], None)
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            if text[start:i] in KNOWN:
                score = dp[start][0] + wlen
                if score > dp[i][0]:
                    dp[i] = (score, (start, text[start:i]))
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

# Decode each book
decoded = {}
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        split_pos, digit = DIGIT_SPLITS[bidx]
        book = book[:split_pos] + digit + book[split_pos:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    text = ''.join(v7.get(p, '?') for p in pairs)
    # Apply anagram resolution
    for ana in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
        text = text.replace(ana, ANAGRAM_MAP[ana])
    decoded[bidx] = text

# ================================================================
# CHECK BOOK CHAINING WITHIN BOOKCASES
# ================================================================
print("=" * 90)
print("BOOK OVERLAP/CHAINING ANALYSIS WITHIN BOOKCASES")
print("=" * 90)

# Group by bookcase
from collections import OrderedDict
bc_groups = OrderedDict()
for entry in bc_map:
    bc = entry['bookcase']
    if bc not in bc_groups:
        bc_groups[bc] = []
    bc_groups[bc].append(entry)

for bc, entries in bc_groups.items():
    if len(entries) < 2:
        continue
    indices = [e['books_json_index'] for e in sorted(entries, key=lambda x: x['library_number'])]

    print(f"\n{bc}: books {indices}")
    for i in range(len(indices) - 1):
        b1 = books[indices[i]]
        b2 = books[indices[i+1]]

        # Check if end of b1 overlaps with start of b2
        best_overlap = 0
        for olen in range(10, min(len(b1), len(b2)) + 1):
            if b1[-olen:] == b2[:olen]:
                best_overlap = olen

        # Also check the other direction
        best_reverse = 0
        for olen in range(10, min(len(b1), len(b2)) + 1):
            if b2[-olen:] == b1[:olen]:
                best_reverse = olen

        if best_overlap > 0:
            print(f"  [{indices[i]}] -> [{indices[i+1]}]: overlap {best_overlap} chars (b1_end = b2_start)")
        elif best_reverse > 0:
            print(f"  [{indices[i+1]}] -> [{indices[i]}]: overlap {best_reverse} chars (b2_end = b1_start)")
        else:
            # Check any overlap (not just end/start)
            found = False
            for olen in range(min(50, min(len(b1), len(b2))), 9, -1):
                for offset in range(len(b1) - olen + 1):
                    seg = b1[offset:offset+olen]
                    if seg in b2:
                        print(f"  [{indices[i]}] & [{indices[i+1]}]: shared substring {olen} chars at b1[{offset}]")
                        found = True
                        break
                if found:
                    break
            if not found:
                print(f"  [{indices[i]}] & [{indices[i+1]}]: NO overlap found")

# ================================================================
# NARRATIVE IN BOOKCASE ORDER
# ================================================================
print(f"\n{'=' * 90}")
print("NARRATIVE DECODED IN BOOKCASE ORDER")
print("=" * 90)

bookcase_order = []
for bc, entries in bc_groups.items():
    sorted_entries = sorted(entries, key=lambda x: x['library_number'])
    bookcase_order.extend(sorted_entries)

# Remove duplicate (book 61 appears twice)
seen_indices = set()
unique_order = []
for entry in bookcase_order:
    idx = entry['books_json_index']
    if idx not in seen_indices:
        seen_indices.add(idx)
        unique_order.append(entry)

total_text_bc = ''
for entry in unique_order:
    idx = entry['books_json_index']
    text = decoded[idx]
    total_text_bc += text

total_known_bc = sum(1 for c in total_text_bc if c != '?')
tokens_bc, covered_bc = dp_segment(total_text_bc)
pct_bc = covered_bc / max(total_known_bc, 1) * 100

print(f"\nBookcase order coverage: {covered_bc}/{total_known_bc} = {pct_bc:.1f}%")

# Show per-bookcase narrative
for bc, entries in bc_groups.items():
    sorted_entries = sorted(entries, key=lambda x: x['library_number'])
    indices = [e['books_json_index'] for e in sorted_entries]

    # Concatenate books in this bookcase
    bc_text = ''
    for idx in indices:
        bc_text += decoded[idx]

    if len(bc_text) < 10:
        continue

    total_k = sum(1 for c in bc_text if c != '?')
    toks, cov = dp_segment(bc_text)
    pct = cov / max(total_k, 1) * 100

    print(f"\n{'─' * 70}")
    print(f"  {bc} | Books: {indices} | Coverage: {pct:.0f}%")
    print(f"{'─' * 70}")
    # Show segmented text, wrap at ~80 chars
    seg_text = ' '.join(toks)
    while seg_text:
        if len(seg_text) <= 80:
            print(f"    {seg_text}")
            break
        # Find a good break point
        bp = seg_text.rfind(' ', 0, 80)
        if bp <= 0:
            bp = 80
        print(f"    {seg_text[:bp]}")
        seg_text = seg_text[bp+1:]

# ================================================================
# COMPARE: INDEX ORDER vs BOOKCASE ORDER
# ================================================================
print(f"\n{'=' * 90}")
print("COMPARISON: INDEX ORDER vs BOOKCASE ORDER")
print("=" * 90)

# Index order
total_text_idx = ''
for idx in range(len(books)):
    total_text_idx += decoded[idx]

total_known_idx = sum(1 for c in total_text_idx if c != '?')
tokens_idx, covered_idx = dp_segment(total_text_idx)
pct_idx = covered_idx / max(total_known_idx, 1) * 100

print(f"  Index order coverage:    {covered_idx}/{total_known_idx} = {pct_idx:.1f}%")
print(f"  Bookcase order coverage: {covered_bc}/{total_known_bc} = {pct_bc:.1f}%")
print(f"  Difference: {covered_bc - covered_idx:+d} chars")

# Show the first 500 chars of each for comparison
print(f"\nFirst 500 chars of INDEX order text:")
idx_preview = ' '.join(tokens_idx)[:500]
print(f"  {idx_preview}")

print(f"\nFirst 500 chars of BOOKCASE order text:")
bc_preview = ' '.join(tokens_bc)[:500]
print(f"  {bc_preview}")
