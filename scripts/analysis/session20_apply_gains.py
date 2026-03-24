#!/usr/bin/env python3
"""
Session 20 Part 4: Apply confirmed gains and hunt for more words.

Confirmed:
- TER: +15 (MHG article "of the", 9x in STEINEN TER SCHARDT)
- Code 96 stays L (changing to I breaks EILCH->LEICH anagram)

New investigations:
1. Verify SIN/SET gains from extended word test
2. Investigate HEDDEMI as different anagram or compound
3. Find more MHG words in garbled zones
4. Look at the {T} EIN pattern (very frequent)
5. Scan for new cross-boundary anagrams with TER added
"""

import json, os
from collections import Counter, defaultdict

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

book_pairs = []
decoded_books = []
for bidx, book in enumerate(books):
    if bidx in DIGIT_SPLITS:
        p, d = DIGIT_SPLITS[bidx]
        book = book[:p] + d + book[p:]
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)
    decoded_books.append(''.join(v7.get(p, '?') for p in pairs))

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
    'IEB': 'BEI', 'TNEDAS': 'STANDE', 'NSCHAT': 'NACHTS',
    'SANGE': 'SAGEN', 'GHNEE': 'GEHEN',
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
    'SAG', 'WAR', 'NU', 'STANDE', 'NACHTS', 'NIT', 'TOT',
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

def dp_count(text, wordset):
    n = len(text)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            if text[start:i] in wordset:
                dp[i] = max(dp[i], dp[start] + wlen)
    return dp[n]

total = sum(1 for c in resolved if c != '?')
baseline = dp_count(resolved, KNOWN)
print(f"Baseline: {baseline}/{total} = {baseline/total*100:.1f}%")

# ================================================================
# 1. VERIFY SIN AND SET
# ================================================================
print(f"\n{'=' * 80}")
print("1. VERIFY SIN AND SET CANDIDATES")
print("=" * 80)

# Test SIN
test = set(KNOWN)
test.add('TER')  # confirmed
test.add('SIN')
sin_cov = dp_count(resolved, test)
print(f"\n  +TER+SIN: {sin_cov}/{total} = {sin_cov/total*100:.1f}%")

# Show SIN contexts
tokens_ter, _ = dp_segment(resolved, set(KNOWN) | {'TER', 'SIN'})
print(f"\n  SIN contexts in segmented text:")
for i, t in enumerate(tokens_ter):
    if t == 'SIN':
        ctx = ' '.join(tokens_ter[max(0,i-3):min(len(tokens_ter),i+4)])
        print(f"    {ctx}")

# SIN in MHG = "his" (possessive, dialect variant of SIN/SIN)
# But SIN could also just be a substring match that hurts longer words

# Test SET
test2 = set(KNOWN)
test2.add('TER')
test2.add('SET')
set_cov = dp_count(resolved, test2)
print(f"\n  +TER+SET: {set_cov}/{total} = {set_cov/total*100:.1f}%")

# Show SET contexts
tokens_set, _ = dp_segment(resolved, set(KNOWN) | {'TER', 'SET'})
print(f"\n  SET contexts:")
for i, t in enumerate(tokens_set):
    if t == 'SET':
        ctx = ' '.join(tokens_set[max(0,i-3):min(len(tokens_set),i+4)])
        print(f"    {ctx}")

# ================================================================
# 2. HEDDEMI DEEPER ANALYSIS
# ================================================================
print(f"\n{'=' * 80}")
print("2. HEDDEMI ANALYSIS")
print("=" * 80)

# The sequence is always: MIN + HEDDEMI + DIE URALTE
# What if HEDDEMI is actually MIN's ending + something?
# Full context: ...IMMINHEDDEMIDIEURALTE...
# Parse options:
# A) IM MIN HED DEM I DIE URALTE (current)
# B) IM MINHEDDEMI DIE URALTE (MIN + HEDDEMI as one block)
# C) IM MIN HEDDEM I DIE URALTE (HEDDEM as the garbled block)

# What is HEDDEM as a word/anagram?
# HEDDEM sorted: DDEHM (5 unique letters, 6 total: D,D,E,H,M)
# Could be: no common German word
# What about HEDD + EMI? or HE + DDEM + I?

# More important: the full 7-letter block HEDDEMI
# If we treat the extra D as a +2 pattern: HEIME + DD -> HEDDEMI?
# Or treat it as +1: what 6-letter word has letters D,D,E,H,I,M (minus one)?
#   Remove D: DEHIM -> HEIME (5 letters, but we need 6)
#   Hmm, that doesn't work.

# What if code 45 at position 3 is wrong? Let's check what happens
# if we try every letter at that position
print(f"\n  HEDDEMI with code at pos 3 changed (currently D=code 45):")
# HEDDEMI = H E D [?] E M I
for alt in 'ABCDEFGHIKLMNORSTUWZ':
    alt_word = 'HED' + alt + 'EMI'
    # Check if this minus any one letter = known anagram target
    for skip in range(7):
        reduced = alt_word[:skip] + alt_word[skip+1:]
        reduced_sorted = ''.join(sorted(reduced))
        for target in ['HEIME', 'HEIM', 'HEIME', 'MEDHI', 'DHEIM']:
            target_sorted = ''.join(sorted(target))
            if reduced_sorted == target_sorted and len(reduced) == len(target):
                print(f"    D->{alt}: {alt_word} - skip[{skip}]='{alt_word[skip]}' -> {reduced} = anagram of {target}")

# Actually, let me try: what if the full block including neighbors is the anagram?
# Context: IMMINHEDDEMIDIEURALTE
# We know: IM, MIN, DEM, DIE, URALTE are all words
# The garbled chars are: HED + I + (the T that follows STEINEN)
# What if we look at MINHEDDEMI as a whole?
print(f"\n  MINHEDDEMI (10 letters, sorted: {''.join(sorted('MINHEDDEMI'))}):")
# Sorted: DDEEHIIMMN
# Any 10-letter anagram? Too long for brute force.
# But what about known patterns?
# MINHEIME = 8 letters? No, we have 10.
# HEIMEDINM = no
# What if it's MIN + HEIDE + DMI?
# HEIDE (heath) = H,E,I,D,E. Remaining: M,D,I,M,N
# MIN+HEIDE+DM? DM is garbage.

# Try: HEDDEM = anagram of some word
# HEDDEM sorted: DDEHM
# German words: HEMMD (hindered)? No, that's HEMMTE
# What about: the position 3 D is actually the second letter of a NEW word?
# MIN HE DDEM I DIE? HE is not useful. DDEM is not a word.

# What about treating this as: MIN + HED + DEM + I
# Where HED is MHG for "head" (Haupt)? No, MHG "head" = houbet
# Or HED is a dialectal form? In some dialects HEID/HEDE = heath

# Try DAHEIM (at home)
# DAHEIM sorted: ADEHIM (6 letters)
# HEDDEMI has: DDEEHIM (7 letters) = DAHEIM + ED? ADHEIMD + E?
# Not quite. DAHEIM = A,D,E,H,I,M. We have D,D,E,E,H,I,M. Extra D and E, missing A.

# What about adding HEDDEMI directly as a resolved form?
# HEDDEMI -> DAHEIME? (MHG plural of "at home")
# DAHEIME = D,A,H,E,I,M,E = 7 letters. Sorted: ADEEHIM
# HEDDEMI sorted: DDEEHIM
# Diff: A vs D. Not a match.

# DEIDHEM? DHEIMED? Not words.

# Let me try: what words have letters D,D,E,H,M + 1 extra from {E,I}?
# With E extra: DDEHME -> no German word
# With I extra: DDEHMI -> no German word

# Conclusion: HEDDEMI remains unsolved. The extra D prevents HEDEMI->HEIME from matching.
# It's likely either a proper noun or a word we haven't identified yet.
print(f"  HEDDEMI remains unsolved. May be a cipher artifact or unknown word.")

# ================================================================
# 3. {T} EIN PATTERN (very frequent)
# ================================================================
print(f"\n{'=' * 80}")
print("3. {{T}} EIN PATTERN")
print("=" * 80)

# {T} EIN appears after "DIES ER" many times
# Full pattern: "ER SO DASS TUN DIES ER {T} EIN ER SEIN GOTTDIENER"
# What if T is part of a word with EIN? TEIN? Not useful.
# Or T is the end of the previous word: "DIES ERT"? Not useful.
# "ER T EIN" = "he [T] one" = "er [T] ein"
# What if T = a number particle? TEN?
# Actually in German "ERTEINER" = "ER T EINER" or "ER TEINER"?
# What if {T} is just a garbled conjunction or article?

# Let's see all contexts
tokens_base, _ = dp_segment(resolved, KNOWN)
t_ein_contexts = []
for i, t in enumerate(tokens_base):
    if t == '{T}' and i+1 < len(tokens_base) and tokens_base[i+1] == 'EIN':
        before = tokens_base[max(0,i-2):i]
        after = tokens_base[i+2:min(len(tokens_base),i+5)]
        t_ein_contexts.append((' '.join(before), ' '.join(after)))

print(f"\n  {{T}} EIN occurrences: {len(t_ein_contexts)}")
for before, after in t_ein_contexts:
    print(f"    ...{before} {{T}} EIN {after}...")

# The T between "ER" and "EIN" is very common
# ERTEINER = ER T EIN ER  or ERTE + INER?
# In MHG, could be: ERTEILET (divided)?
# What if we read it as: "ER TEIN ER" where TEIN = MHG word?
# TEIN doesn't exist in MHG.
# Or: "ERT EIN ER" where ERT = MHG?
# ERT = not a word.

# The most common full phrase: "DIES ER {T} EIN ER SEIN GOTTDIENER"
# = "dies er [t] ein er sein Gottdiener"
# = "this he [t] a/one he his God's-servant"
# What if T = ward/was? No, WAR is already there.
# What if the raw text is actually "DIESERTEINERSEINGOTTDIENER"?
# = "DIESER T EINER SEIN GOTTDIENER"
# DIESER = "this" (pronoun). Wait, DIESER is already in KNOWN!

# Let me check: does "DIESER" appear at these positions?
print(f"\n  Checking if DIESER matches at these positions:")
# The text at these positions is: ...DIESERTEINERSEINGOTTDIENER...
# DP is choosing: DIES + ER + T + EIN + ER + SEIN = 4+2+0+3+2+4 = 15 matched
# But DIESER + T + EIN + ER + SEIN = 6+0+3+2+4 = 15 matched too (same!)
# The DP picks the first maximum, which depends on scanning direction.

# Actually: DIES(4) + ER(2) = 6 chars matched in first 6.
# DIESER(6) = 6 chars matched in first 6. Same score!
# So DP might pick either one. The {T} is left over either way.

# What about: "DIESER TEIN ER SEIN" vs "DIES ER T EIN ER SEIN"?
# In both cases, T is unmatched. Unless we add TEIN or OT or something.

# ================================================================
# 4. MASS 3-LETTER MHG WORD SCAN
# ================================================================
print(f"\n{'=' * 80}")
print("4. MASS 3-LETTER WORD SCAN (MHG + German)")
print("=" * 80)

# Comprehensive list of German/MHG 3-letter words
THREE_LETTER = [
    'ACH', 'AGE', 'ART', 'BAD', 'BAT', 'BOT', 'DAM', 'DAN',
    'EIS', 'ERZ', 'FEL', 'GEL', 'HOF', 'HUT', 'IRR', 'KUR',
    'LOS', 'MAG', 'MAT', 'MET', 'MIR', 'MIT', 'MUT', 'NET',
    'NIE', 'OFT', 'RAT', 'ROT', 'RUF', 'RUH', 'SIT', 'TAL',
    'TOR', 'TUG', 'VIL', 'VOR', 'WAN', 'WEH', 'WIS', 'WOL',
    'ZAL', 'ZIT',
    # MHG specific
    'AVE', 'BAS', 'DIT', 'DAZ', 'DOC', 'EHT', 'GIN', 'GIE',
    'HAZ', 'HUS', 'IER', 'LAN', 'LIP', 'MER', 'NIU', 'OUC',
    'OUZ', 'SAM', 'SIC', 'SOL', 'TUO', 'VIE', 'VUR', 'WAT',
    'WEL', 'WIL', 'WIS', 'ZUO',
]

# Remove already-known
three_to_test = [w for w in THREE_LETTER if w not in KNOWN]

test_known_base = set(KNOWN) | {'TER'}
base_cov = dp_count(resolved, test_known_base)
print(f"\n  Base (KNOWN + TER): {base_cov}/{total} = {base_cov/total*100:.1f}%")

gains = []
for word in three_to_test:
    test = set(test_known_base)
    test.add(word)
    cov = dp_count(resolved, test)
    delta = cov - base_cov
    if delta > 0:
        gains.append((word, delta, cov))

gains.sort(key=lambda x: -x[1])
for word, delta, cov in gains:
    print(f"    +{word}: {cov}/{total} = {cov/total*100:.1f}% ({delta:+d})")

# Verify each gaining word makes narrative sense
print(f"\n  Contexts of gaining words:")
for word, delta, _ in gains[:10]:
    test = set(test_known_base) | {word}
    tokens_test, _ = dp_segment(resolved, test)
    for i, t in enumerate(tokens_test):
        if t == word:
            ctx = ' '.join(tokens_test[max(0,i-3):min(len(tokens_test),i+4)])
            print(f"    {word}: {ctx}")
            break

# ================================================================
# 5. MASS 4-5 LETTER WORD SCAN
# ================================================================
print(f"\n{'=' * 80}")
print("5. MASS 4-5 LETTER WORD SCAN")
print("=" * 80)

FOUR_FIVE = [
    # 4-letter German/MHG
    'ARME', 'BALD', 'BETT', 'BILD', 'BUCH', 'DANK', 'EWIG',
    'FEHL', 'FREI', 'FUHR', 'GANG', 'GAST', 'GIFT', 'GRAF',
    'GRAU', 'HEER', 'HERZ', 'HIRT', 'HULD', 'KERN', 'LAUT',
    'LEER', 'MEID', 'MILD', 'MORD', 'MUET', 'MUNT', 'NAHT',
    'OBEN', 'PFAD', 'RAUM', 'RITT', 'RUHE', 'SAAT', 'SAEH',
    'SEHN', 'SINN', 'SOLN', 'TREU', 'TUOT', 'TURN', 'WACH',
    'WAHR', 'WERK', 'ZAHL', 'ZIEL',
    # 5-letter German/MHG
    'ANTLITZ', 'BLICK', 'BRAUCH', 'BRUST', 'DEGEN', 'EIGEN',
    'EILEN', 'ENGEL', 'FEIND', 'FOLGE', 'FREMD', 'FRIEDE',
    'GLAUB', 'GRUBE', 'HAUPT', 'HEIDE', 'JENEM', 'KAMPF',
    'KNABE', 'KREUZ', 'LEHRE', 'LEUTE', 'LIEBE', 'MEIDE',
    'MUTIG', 'OPFER', 'PFERD', 'RECHT', 'SEELE', 'STATT',
    'STILL', 'SUCHE', 'TOTEN', 'TREIB', 'TROTZ', 'TUGEND',
    'WACHE', 'WEISE', 'WOLLT',
    # MHG-specific longer words
    'GUOTE', 'LANDE', 'LIUTE', 'MAGET', 'MEIDE', 'MUOZE',
    'SCHILT', 'SINNE', 'STRIT', 'SWERT', 'TIURE', 'VOLKE',
    'VROWE', 'WUNNE', 'EDELEN',
    # Common German words that might match garbled patterns
    'ANDER', 'BEVOR', 'DABEI', 'DARIN', 'DAVON', 'EBENSO',
    'EINST', 'HERAB', 'HINAB', 'JENER', 'JENEM', 'JENES',
    'MITTEN', 'NEBEN', 'OFFEN', 'RECHT', 'GLEICH',
    'GESETZ', 'GESICHT',
]

four_five_to_test = [w for w in FOUR_FIVE if w not in KNOWN]

gains45 = []
for word in four_five_to_test:
    test = set(test_known_base)
    test.add(word)
    cov = dp_count(resolved, test)
    delta = cov - base_cov
    if delta > 0:
        gains45.append((word, delta, cov))

gains45.sort(key=lambda x: -x[1])
for word, delta, cov in gains45[:15]:
    print(f"    +{word}: {cov}/{total} = {cov/total*100:.1f}% ({delta:+d})")

# ================================================================
# 6. CUMULATIVE GAINS
# ================================================================
print(f"\n{'=' * 80}")
print("6. CUMULATIVE GAINS ASSESSMENT")
print("=" * 80)

all_candidates = []
# TER is confirmed
all_candidates.append(('TER', 'MHG article (of the)'))
# Add any 3-letter gains > 2
for word, delta, _ in gains:
    if delta >= 2:
        all_candidates.append((word, f'3-letter, +{delta}'))
# Add any 4-5 letter gains > 2
for word, delta, _ in gains45:
    if delta >= 2:
        all_candidates.append((word, f'4-5 letter, +{delta}'))

print(f"\n  All candidates with gain >= 2:")
test_cum = set(KNOWN)
prev_cov = baseline
for word, desc in all_candidates:
    test_cum.add(word)
    cov = dp_count(resolved, test_cum)
    marginal = cov - prev_cov
    print(f"    +{word:12s} ({desc:25s}): {cov}/{total} = {cov/total*100:.1f}% (+{marginal} marginal)")
    prev_cov = cov

print(f"\n  TOTAL: {prev_cov}/{total} = {prev_cov/total*100:.1f}% ({prev_cov-baseline:+d} from baseline)")

# ================================================================
# 7. NEW CROSS-BOUNDARY ANAGRAMS WITH TER CONTEXT
# ================================================================
print(f"\n{'=' * 80}")
print("7. NEW CROSS-BOUNDARY ANAGRAM SCAN")
print("=" * 80)

# With TER added, resegment and scan boundaries
tokens_new, cov_new = dp_segment(resolved, test_cum)

# Find all garbled+word and word+garbled boundaries
boundary_candidates = []
for i, t in enumerate(tokens_new):
    if t.startswith('{'):
        content = t[1:-1]
        if len(content) > 6: continue  # skip huge blocks
        # garbled + next word
        if i + 1 < len(tokens_new) and not tokens_new[i+1].startswith('{'):
            combined = content + tokens_new[i+1]
            combined_sorted = ''.join(sorted(combined))
            # Test against an expanded word list
            for candidate in list(test_cum):
                if len(candidate) == len(combined):
                    if ''.join(sorted(candidate)) == combined_sorted:
                        boundary_candidates.append((f'{{{content}}}+{tokens_new[i+1]}', candidate, 'exact'))
                elif len(candidate) == len(combined) - 1:
                    # +1 pattern
                    for skip in range(len(combined)):
                        reduced = combined[:skip] + combined[skip+1:]
                        if ''.join(sorted(reduced)) == ''.join(sorted(candidate)):
                            boundary_candidates.append((f'{{{content}}}+{tokens_new[i+1]}', candidate, f'+1 (skip {combined[skip]})'))
                            break
        # prev word + garbled
        if i > 0 and not tokens_new[i-1].startswith('{'):
            combined = tokens_new[i-1] + content
            combined_sorted = ''.join(sorted(combined))
            for candidate in list(test_cum):
                if len(candidate) == len(combined):
                    if ''.join(sorted(candidate)) == combined_sorted:
                        boundary_candidates.append((f'{tokens_new[i-1]}+{{{content}}}', candidate, 'exact'))

# Show unique candidates
seen = set()
for source, target, method in boundary_candidates:
    key = (source, target)
    if key not in seen:
        seen.add(key)
        print(f"  {source} -> {target} ({method})")

print(f"\n  Done.")
