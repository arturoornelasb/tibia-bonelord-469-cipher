#!/usr/bin/env python3
"""Session 10e: Code verification and missing letter hunt (P, J)"""

import json, re
from collections import Counter, defaultdict

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]
books = [parse_codes(b) for b in raw_books]

# Reverse mapping: letter -> codes
letter_codes = defaultdict(list)
for code, letter in mapping.items():
    letter_codes[letter].append(code)

print("=" * 80)
print("SESSION 10e: CODE VERIFICATION & MISSING LETTER HUNT")
print("=" * 80)

# 1. Code counts per letter
print("\n1. CODES PER LETTER")
print("-" * 60)
for letter in sorted(letter_codes.keys()):
    codes = sorted(letter_codes[letter])
    print(f"  {letter}: {len(codes)} codes -> {codes}")
print(f"  Total codes: {len(mapping)}")
print(f"  Missing letters: P, J, Q, X, Y")

# 2. Confirmed words and which codes they validate
print("\n2. CODE CONFIRMATION BY KNOWN WORDS")
print("-" * 60)

confirmed_words = {
    'DER': [['45','19','08'], ['45','19','55'], ['42','86','08']],
    'DEN': [['45','19','48'], ['42','56','11'], ['45','19','11']],
    'DIE': [['42','15','86'], ['47','16','03']],
    'DAS': [['42','89','12'], ['28','85','91']],
    'UND': [['61','71','28'], ['44','71','47'], ['43','53','45']],
    'IST': [['65','12','81'], ['50','23','88'], ['16','91','64']],
    'EIN': [['03','50','14'], ['86','16','11'], ['19','46','71']],
    'SEIN': [['05','86','16','11'], ['91','29','15','48']],
    'SIE': [['59','46','67'], ['52','65','01']],
    'WIR': [['87','65','08'], ['33','21','72'], ['36','15','51']],
    'ER': [['86','51'], ['76','08'], ['17','24']],
    'ES': [['67','05'], ['03','12'], ['01','52']],
    'IN': [['46','71'], ['50','14'], ['65','53']],
    'VON': [['83','82','11'], ['83','25','14']],
    'MIT': [['04','50','64'], ['40','46','81']],
    'WIE': [['36','16','67'], ['33','15','01']],
    'SEI': [['05','29','46'], ['91','86','21']],
    'AUS': [['89','44','52'], ['85','43','91']],
    'NICHT': [['14','50','18','94','64']],
    'KOENIG': [['22','82','17','73','50','84']],
    'VIEL': [['83','46','86','96'], ['83','15','01','34']],
    'RUNE': [['72','61','53','01'], ['51','43','14','86']],
    'ERDE': [['86','51','28','49'], ['17','08','42','03']],
    'TAG': [['78','31','97'], ['64','85','80']],
    'WEG': [['33','29','97'], ['87','27','80']],
    'REDE': [['08','30','45','76'], ['51','03','42','17']],
    'ENDE': [['86','53','47','67'], ['17','71','45','01']],
    'UNTER': [['43','53','64','86','51'], ['61','14','78','17','24']],
    'GEIGET': [['97','29','21','97','27','81'], ['80','03','50','80','26','64']],
    'DENEN': [['45','19','48','56','11'], ['42','86','14','01','53']],
    'WERDE': [['36','86','24','42','86']],
    'STEIN': [['05','64','29','15','48']],
    'SEIDE': [['05','86','16','42','86']],
    'HUND': [['57','43','14','28'], ['94','61','71','45']],
    'STEH': [['05','64','76','57'], ['91','81','30','94']],
    'GOLD': [['84','82','96','42']],
    'SEGEN': [['05','49','97','17','71']],
    'NORDEN': [['53','82','51','45','17','71']],
    'DORT': [['28','99','55','64']],
    'WELT': [['33','29','96','81']],
    'LIED': [['34','15','86','45']],
    'SONNE': [['23','99','11','11','19']],
    'MOND': [['04','99','48','28']],
    'DENN': [['45','86','71','11']],
    'KELSEI': [['22','30','34','91','86','21']],
}

# Track which codes are confirmed
confirmed_codes = defaultdict(set)  # letter -> set of confirmed codes
code_words = defaultdict(list)  # code -> list of words confirming it

for word, variants in confirmed_words.items():
    for variant in variants:
        for i, code in enumerate(variant):
            letter = word[i]
            confirmed_codes[letter].add(code)
            code_words[code].append(f"{word}[{i}]")

print("\n  Confirmed vs unconfirmed codes per letter:")
for letter in sorted(letter_codes.keys()):
    all_codes = set(letter_codes[letter])
    confirmed = confirmed_codes.get(letter, set())
    unconfirmed = all_codes - confirmed
    status = "ALL CONFIRMED" if not unconfirmed else f"UNCONFIRMED: {sorted(unconfirmed)}"
    print(f"  {letter}: {len(all_codes)} total, {len(confirmed)} confirmed, {status}")

# 3. Count frequency of each unconfirmed code
print("\n3. UNCONFIRMED CODE FREQUENCIES")
print("-" * 60)
all_code_counts = Counter()
for book in books:
    all_code_counts.update(book)

unconfirmed = []
for letter in sorted(letter_codes.keys()):
    all_codes = set(letter_codes[letter])
    confirmed = confirmed_codes.get(letter, set())
    for code in sorted(all_codes - confirmed):
        count = all_code_counts[code]
        unconfirmed.append((code, letter, count))
        print(f"  Code {code} (assigned={letter}): {count} occurrences")

# 4. Context analysis for high-frequency unconfirmed codes
print("\n4. CONTEXT FOR UNCONFIRMED CODES")
print("-" * 60)

# Sort by frequency
unconfirmed.sort(key=lambda x: -x[2])
total_codes = sum(all_code_counts.values())

for code, assigned_letter, count in unconfirmed[:15]:
    pct = count / total_codes * 100
    print(f"\n  Code {code} (assigned={assigned_letter}, {count}x, {pct:.1f}%):")

    # Show contexts: 3 codes before and after
    contexts = []
    for bi, book in enumerate(books):
        for ci, c in enumerate(book):
            if c == code:
                start = max(0, ci-4)
                end = min(len(book), ci+5)
                ctx_codes = book[start:end]
                ctx_letters = [mapping.get(cc, '?') for cc in ctx_codes]
                pos_in_ctx = ci - start
                ctx_str = ''.join(ctx_letters)
                # Mark the target position
                before = ''.join(ctx_letters[:pos_in_ctx])
                after = ''.join(ctx_letters[pos_in_ctx+1:])
                contexts.append(f"  B{bi:02d}: {before}[{assigned_letter}]{after}")

    # Show up to 5 unique contexts
    seen = set()
    shown = 0
    for ctx in contexts:
        if ctx not in seen and shown < 5:
            print(f"    {ctx}")
            seen.add(ctx)
            shown += 1
    if len(seen) > 5:
        print(f"    ... and {len(seen)-5} more unique contexts")

# 5. Missing letter hypothesis testing
print("\n" + "=" * 60)
print("5. MISSING LETTER HYPOTHESIS TESTING")
print("=" * 60)

# For each unconfirmed code, test if reassigning to P or J improves readability
# by checking surrounding context

# German words containing P (common in MHG too):
p_words = ['SPRECHEN', 'PFERD', 'PFAD', 'PLAGE', 'PEIN', 'PRACHT',
           'PREIS', 'PREDIGEN', 'PRIESTER', 'PALAST', 'PARADIES',
           'SPIEL', 'SPEER', 'SPUR', 'SPRUCH', 'SPAT', 'SPEISE']

# German words containing J:
j_words = ['JA', 'JEDER', 'JENE', 'JUNG', 'JAMMER', 'JAGEN', 'JAHR']

# For each unconfirmed code, collect all bigrams (code before/after)
print("\n  Testing P hypothesis:")
for code, assigned_letter, count in unconfirmed[:15]:
    if count < 5:
        continue
    # Get all contexts where swapping to P creates recognizable patterns
    p_matches = []
    for bi, book in enumerate(books):
        for ci, c in enumerate(book):
            if c == code:
                # Get 3-letter window with P substituted
                for window_size in [2, 3, 4, 5]:
                    for offset in range(window_size):
                        start = ci - offset
                        end = start + window_size
                        if start < 0 or end > len(book):
                            continue
                        window_letters = []
                        for wi in range(start, end):
                            if wi == ci:
                                window_letters.append('P')
                            else:
                                window_letters.append(mapping.get(book[wi], '?'))
                        word = ''.join(window_letters)
                        # Check against P-words
                        for pw in p_words:
                            if word in pw:
                                p_matches.append(f"B{bi}: {word} (in {pw})")
    if p_matches:
        print(f"\n  Code {code} (currently={assigned_letter}): P matches!")
        for m in sorted(set(p_matches))[:5]:
            print(f"    {m}")

print("\n  Testing J hypothesis:")
for code, assigned_letter, count in unconfirmed[:15]:
    if count < 5:
        continue
    j_matches = []
    for bi, book in enumerate(books):
        for ci, c in enumerate(book):
            if c == code:
                for window_size in [2, 3, 4]:
                    for offset in range(window_size):
                        start = ci - offset
                        end = start + window_size
                        if start < 0 or end > len(book):
                            continue
                        window_letters = []
                        for wi in range(start, end):
                            if wi == ci:
                                window_letters.append('J')
                            else:
                                window_letters.append(mapping.get(book[wi], '?'))
                        word = ''.join(window_letters)
                        for jw in j_words:
                            if word in jw:
                                j_matches.append(f"B{bi}: {word} (in {jw})")
    if j_matches:
        print(f"\n  Code {code} (currently={assigned_letter}): J matches!")
        for m in sorted(set(j_matches))[:5]:
            print(f"    {m}")

# 6. Deeper look at OWI
print("\n" + "=" * 60)
print("6. OWI DEEP ANALYSIS")
print("=" * 60)

for bi, book in enumerate(books):
    decoded = ''.join(mapping.get(c, '?') for c in book)
    positions = [m.start() for m in re.finditer('OWI', decoded)]
    for pos in positions:
        start = max(0, pos-15)
        end = min(len(decoded), pos+18)
        ctx = decoded[start:end]
        print(f"  B{bi:02d} pos {pos}: ...{ctx}...")

# 7. DGEDA - could it be a verb? GE- prefix + DA
print("\n" + "=" * 60)
print("7. DGEDA ANALYSIS")
print("=" * 60)

# If first D is end of previous word: ...D + GEDA
# GEDA could be MHG past participle GE-DA (done/given?)
# Or GE-DAT, GE-DACHT with missing letters?
for bi, book in enumerate(books):
    decoded = ''.join(mapping.get(c, '?') for c in book)
    positions = [m.start() for m in re.finditer('DGEDA', decoded)]
    for pos in positions[:3]:
        start = max(0, pos-20)
        end = min(len(decoded), pos+25)
        ctx = decoded[start:end]
        # Also show with collapsed doubles
        collapsed = re.sub(r'(.)\1+', r'\1', ctx)
        print(f"  B{bi:02d}: raw={ctx}")
        print(f"        col={collapsed}")

# 8. Full narrative: assemble all unique pieces and read them
print("\n" + "=" * 60)
print("8. FULL TEXT - ALL BOOKS DECODED")
print("=" * 60)

# Decode all books, collapse doubles, show unique content
all_decoded = []
for bi, book in enumerate(books):
    decoded = ''.join(mapping.get(c, '?') for c in book)
    collapsed = re.sub(r'(.)\1+', r'\1', decoded)
    all_decoded.append(collapsed)

# Find truly unique content (not substring of another)
unique_texts = []
for i, text in enumerate(all_decoded):
    is_sub = False
    for j, other in enumerate(all_decoded):
        if i != j and text in other:
            is_sub = True
            break
    if not is_sub:
        unique_texts.append((i, text))

print(f"\n  {len(unique_texts)} unique (non-substring) books")
print(f"  Showing first 10 with manual segmentation hints:")

# Known word list for segmentation
known = ['KOENIG', 'LABGZERAS', 'DENEN', 'REDE', 'ENDE', 'UTRUNR',
         'GEIGET', 'STEIN', 'GOLD', 'SONNE', 'MOND', 'NORDEN',
         'ERDE', 'VIEL', 'RUNE', 'UNTER', 'NICHT', 'WELT',
         'WERDE', 'SEIN', 'STEH', 'LIED', 'SEIDE', 'HUND',
         'SEGEN', 'DORT', 'DENN', 'KELSEI', 'AUNRSONGETRASES',
         'WEG', 'TAG', 'DER', 'DEN', 'DIE', 'DAS', 'UND',
         'IST', 'EIN', 'SIE', 'WIR', 'VON', 'MIT', 'WIE',
         'SEI', 'AUS', 'ER', 'ES', 'IN']

for idx, (bi, text) in enumerate(unique_texts[:10]):
    print(f"\n  Book {bi} ({len(text)} chars):")
    # Highlight known words
    marked = text
    for w in sorted(known, key=len, reverse=True):
        marked = marked.replace(w, f' {w} ')
    # Clean up spaces
    marked = re.sub(r'\s+', ' ', marked).strip()
    # Wrap at 70 chars
    for i in range(0, len(marked), 70):
        print(f"    {marked[i:i+70]}")

# 9. ENGCHD - the consonant cluster
print("\n" + "=" * 60)
print("9. ENGCHD CONTEXT - ORT (PLACE) CONNECTION")
print("=" * 60)

for bi, book in enumerate(books):
    decoded = ''.join(mapping.get(c, '?') for c in book)
    collapsed = re.sub(r'(.)\1+', r'\1', decoded)
    if 'ENGCHD' in collapsed:
        pos = collapsed.index('ENGCHD')
        start = max(0, pos-25)
        end = min(len(collapsed), pos+31)
        ctx = collapsed[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# 10. VMTEGE - the persistent mystery
print("\n" + "=" * 60)
print("10. VMTEGE FULL CONTEXT")
print("=" * 60)

for bi, book in enumerate(books):
    decoded = ''.join(mapping.get(c, '?') for c in book)
    collapsed = re.sub(r'(.)\1+', r'\1', decoded)
    if 'VMT' in collapsed:
        pos = collapsed.index('VMT')
        start = max(0, pos-30)
        end = min(len(collapsed), pos+35)
        ctx = collapsed[start:end]
        print(f"  B{bi:02d}: ...{ctx}...")

# 11. The SC = SCH hypothesis
print("\n" + "=" * 60)
print("11. SC OCCURRENCES (possible SCH)")
print("=" * 60)

for bi, book in enumerate(books):
    decoded = ''.join(mapping.get(c, '?') for c in book)
    collapsed = re.sub(r'(.)\1+', r'\1', decoded)
    # Find SC not followed by H
    for m in re.finditer(r'SC(?!H)', collapsed):
        pos = m.start()
        start = max(0, pos-10)
        end = min(len(collapsed), pos+15)
        ctx = collapsed[start:end]
        print(f"  B{bi:02d} pos {pos}: ...{ctx}...")

# 12. Code 60: is it really N?
print("\n" + "=" * 60)
print("12. CODE 60 VERIFICATION")
print("=" * 60)
print(f"  Code 60 assigned: {mapping['60']}")
print(f"  Occurrences: {all_code_counts['60']}")

# Show all contexts for code 60
contexts_60 = []
for bi, book in enumerate(books):
    for ci, c in enumerate(book):
        if c == '60':
            start = max(0, ci-3)
            end = min(len(book), ci+4)
            ctx = ''.join(mapping.get(book[x], '?') for x in range(start, end))
            pos_in = ci - start
            contexts_60.append(f"  B{bi:02d}: {ctx} (code 60 at pos {pos_in})")

seen = set()
for ctx in contexts_60:
    if ctx not in seen:
        print(f"    {ctx}")
        seen.add(ctx)
    if len(seen) >= 10:
        print(f"    ... {len(contexts_60) - 10} more")
        break

# 13. Summary of letter distribution
print("\n" + "=" * 60)
print("13. LETTER FREQUENCY ANALYSIS")
print("=" * 60)

letter_counts = Counter()
for book in books:
    for c in book:
        if c in mapping:
            letter_counts[mapping[c]] += 1

total_letters = sum(letter_counts.values())
# Expected German frequencies
expected = {'E':17.4, 'N':9.8, 'I':7.6, 'S':7.3, 'R':7.0, 'T':6.2,
            'A':6.5, 'D':5.1, 'H':4.8, 'U':4.2, 'L':3.4, 'G':3.0,
            'O':2.5, 'M':2.5, 'B':1.9, 'W':1.9, 'Z':1.1, 'K':1.2,
            'V':0.8, 'F':1.7, 'C':0.3, 'P':0.7, 'J':0.3}

print(f"  {'Letter':>6} {'Count':>6} {'Actual%':>8} {'Expected%':>10} {'Diff':>6} {'Codes':>6}")
for letter, count in sorted(letter_counts.items(), key=lambda x: -x[1]):
    actual_pct = count / total_letters * 100
    exp_pct = expected.get(letter, 0)
    diff = actual_pct - exp_pct
    n_codes = len(letter_codes[letter])
    flag = " <<<" if abs(diff) > 1.5 else ""
    print(f"  {letter:>6} {count:>6} {actual_pct:>7.1f}% {exp_pct:>9.1f}% {diff:>+5.1f}% {n_codes:>5}{flag}")

print(f"\n  P expected: {expected['P']:.1f}% = ~{int(total_letters * expected['P']/100)} chars")
print(f"  J expected: {expected['J']:.1f}% = ~{int(total_letters * expected['J']/100)} chars")

print("\n" + "=" * 80)
print("SESSION 10e COMPLETE")
print("=" * 80)
