#!/usr/bin/env python3
"""Session 12a: Expanded MHG word list + proper noun Tibia cross-reference + new approaches"""

import json, re
from collections import Counter, defaultdict

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]
books = [parse_codes(b) for b in raw_books]
def decode(book, m=None):
    if m is None: m = mapping
    return ''.join(m.get(c, '?') for c in book)
def collapse(s):
    return re.sub(r'(.)\1+', r'\1', s)

NEG_INF = float('-inf')

# MASSIVELY expanded MHG/OHG word list
# Adding words found in corpus analysis + standard MHG vocabulary
german_words = [
    # === PROPER NOUNS (from narrative) ===
    'EILCHANHEARUCHTIG', 'EDETOTNIURGS', 'WRLGTNELNRHELUIRUNN',
    'TIUMENGEMI', 'SCHWITEIONE', 'LABGZERAS', 'HEDEMI', 'TAUTR',
    'LABRNI', 'ADTHARSC', 'ENGCHD', 'KELSEI',

    # === CONFIRMED UNKNOWN WORDS (recurring, likely MHG) ===
    'NGETRAS', 'GEVMT', 'DGEDA', 'TEMDIA', 'UISEMIV',
    'TEIGN', 'CHN', 'SCE',

    # === STANDARD GERMAN (already in list) ===
    'KOENIG', 'GEIGET', 'SCHAUN', 'URALTE', 'FINDEN', 'DIESER',
    'NORDEN', 'SONNE', 'UNTER', 'NICHT', 'WERDE',
    'STEINEN', 'STEIN', 'DENEN', 'ERDE', 'VIEL', 'RUNE',
    'STEH', 'LIED', 'SEGEN', 'DORT', 'DENN',
    'GOLD', 'MOND', 'WELT', 'ENDE', 'REDE',
    'HUND', 'SEIN', 'WIRD', 'KLAR', 'ERST',
    'HWND', 'WISET', 'OWI', 'MINHE',
    'EINEN', 'EINER', 'SEINE', 'SEIDE',
    'TAG', 'WEG', 'DER', 'DEN', 'DIE', 'DAS',
    'UND', 'IST', 'EIN', 'SIE', 'WIR', 'VON',
    'MIT', 'WIE', 'SEI', 'AUS', 'ORT', 'TUN',
    'NUR', 'SUN', 'TOT', 'GAR', 'ACH', 'ZUM',
    'HIN', 'HER', 'ALS', 'AUCH', 'RUND', 'GEH',
    'NACH', 'IENE', 'NOCH', 'ALLE', 'WOHL',
    'HIER', 'SICH', 'SIND', 'SEHR',
    'ABER', 'ODER', 'WENN', 'DANN',
    'ALTE', 'EDEL', 'HELD', 'LAND',
    'WARD', 'WART',
    'ER', 'ES', 'IN', 'SO', 'AN', 'IM',
    'DA', 'NU', 'IR', 'EZ', 'DO', 'OB', 'IE',
    'TER', 'HIET',

    # === NEW: MHG words found in corpus (session 10z) ===
    'DU', 'HAT', 'BIS', 'SINE',  # DU(10x), HAT(4x), BIS(2x), SINE(3x)

    # === NEW: More MHG/OHG vocabulary ===
    # Common MHG verbs
    'SAGEN', 'HABEN', 'KOMEN', 'GEBEN', 'NEMEN', 'SEHEN',
    'WISEN', 'LESEN', 'REDEN', 'LEBEN', 'GEHEN', 'TRAGEN',
    'LIGEN', 'SITEN', 'BITEN', 'LEGEN', 'SETEN', 'RITEN',
    'VINDEN', 'BINDEN', 'SINGEN', 'RINGEN',
    'DISEN', 'WILEN', 'NIDEN',
    'SAG', 'GAB', 'NAM', 'SAH', 'LAS', 'BAT', 'LAG',
    'SPRACH', 'SPRICHT',

    # MHG nouns
    'HERR', 'FRAU', 'VROUWE', 'RITTER', 'KNECHT',
    'BURC', 'BURG', 'STAT', 'STEINE',
    'WASSER', 'FEUER', 'LUFT',
    'NACHT', 'MORGEN', 'ABEND',
    'KRAFT', 'MACHT', 'EHRE', 'MINNE',
    'LIEBE', 'LEBEN', 'STERBEN', 'LEIDEN',
    'VOLC', 'VOLK',
    'DEGEN', 'RECKE', 'WIGANT',
    'SWERT', 'SCHILD', 'HELM',
    'HERRE', 'VROWE',
    'MERE', 'MAERE',
    'HERZE', 'SELE',
    'TUGEND', 'TRIUWE', 'ERE',
    'DINC', 'DING',

    # MHG adjectives
    'EDELE', 'GROZE', 'KLEINE', 'GUOT', 'SCHOEN',
    'HOHES', 'TIEFES', 'ALTES', 'NEUES',
    'STARK', 'WEISE',

    # MHG pronouns/articles
    'DISE', 'DIRRE', 'DISER', 'DISEM',
    'JENER', 'MICH', 'DICH', 'SICH',
    'UNSER', 'EUER', 'IREM',
    'IREN', 'IRER',
    'MEIN', 'DEIN',

    # MHG prepositions/conjunctions/adverbs
    'UBER', 'UEBER', 'WIDER', 'GEGEN', 'DURCH', 'ZWISCHEN',
    'BEVOR', 'WARUM', 'WOHIN', 'WOHER',
    'DARUM', 'DARIN', 'DAVON', 'DABEI',
    'HINAUS', 'HEREIN', 'DARAUF',
    'ALSO', 'IEDOCH', 'NIMMER', 'IMMER',
    'BEIDE', 'MANCH', 'SOLCH',
    'WEDER', 'DEREN', 'DESSEN',
    'DOCH', 'EBEN', 'GANZ',
    'BALD', 'SCHON',

    # Tibia-specific vocabulary
    'DRACHE', 'DRACHEN', 'ZWERGE', 'ELFEN',
    'RUNEN', 'ZAUBER', 'MAGIE',
    'DUNKEL', 'LICHT', 'SCHATTEN',
    'TIEFE', 'HOEHE', 'TURM',
    'ALTAR', 'TEMPEL', 'GRAB',
    'FLUCH', 'BANN', 'SCHWUR',
    'KRIEG', 'KAMPF', 'SIEG',
    'SEELE', 'GEIST', 'WESEN',
    'MACHT', 'ORDEN', 'GILDE',

    # Short common words
    'UM', 'AM', 'AB', 'BI', 'ZU',
    'VOR', 'MAN', 'GUT', 'NEU', 'ALT',
    'ROT', 'WAS', 'WER', 'WEN', 'WEM',
    'IHR', 'IHN', 'DIR', 'MIR', 'UNS',

    # MHG common phrases parts
    'SELE', 'HEIL', 'WEHE',
    'EWIG', 'TIEF', 'WEIT', 'LANG',
    'BOSE', 'BOES', 'GRIM',

    # More verb forms
    'GILT', 'GALT', 'GING', 'GETAN',
    'WARD', 'WART', 'WARS', 'WURD',
    'HIEZ', 'LIEZ', 'SACH',
    'SOLT', 'WOLT', 'MUOZ',

    # OHG/archaic
    'DHER', 'DHAZ', 'DHES',
    'FONA', 'ENTI', 'EDHO',
    'WIHAN', 'HEILAG',

    # Number words
    'DREI', 'VIER', 'ACHT', 'NEUN', 'ZEHN',
    'ZWEI',

    # Genitive/possessive forms
    'EINES', 'IHRES', 'MEINES', 'DEINES',
    'SEINES', 'UNSERES',

    # Definite articles all forms
    'DIESE', 'EINEM', 'JEDE', 'JEDEM',
]

german_words = list(dict.fromkeys(german_words))
word_scores = {w: len(w) * 3 for w in german_words}
all_words = sorted(word_scores.keys(), key=len, reverse=True)

print("=" * 80)
print("SESSION 12a: EXPANDED WORD LIST + PROPER NOUN ANALYSIS")
print("=" * 80)
print(f"\n  Word list size: {len(all_words)} words")

# Decode all books
all_collapsed = [collapse(decode(b)) for b in books]

# 1. Coverage with expanded word list
def dp_segment(text):
    n = len(text)
    if n == 0: return [], 0, 0
    dp = [NEG_INF] * (n + 1)
    back = [None] * (n + 1)
    dp[0] = 0
    for i in range(n):
        if dp[i] == NEG_INF: continue
        ns = dp[i] - 1
        if ns > dp[i+1]:
            dp[i+1] = ns
            back[i+1] = ('unk', i)
        for word in all_words:
            wl = len(word)
            if i + wl <= n and text[i:i+wl] == word:
                ns = dp[i] + word_scores.get(word, wl)
                if ns > dp[i+wl]:
                    dp[i+wl] = ns
                    back[i+wl] = ('word', i, word)
    pos = n
    parts = []
    covered = 0
    while pos > 0:
        info = back[pos]
        if info is None:
            parts.append(('?', text[pos-1:pos]))
            pos -= 1
        elif info[0] == 'unk':
            parts.append(('?', text[info[1]:pos]))
            pos = info[1]
        elif info[0] == 'word':
            parts.append(('W', info[2]))
            covered += len(info[2])
            pos = info[1]
    parts.reverse()
    return parts, covered, n

total_chars = sum(len(t) for t in all_collapsed)
total_cov = 0
book_results = []
for bi in range(len(all_collapsed)):
    parts, cov, tot = dp_segment(all_collapsed[bi])
    pct = cov * 100 / tot if tot > 0 else 0
    total_cov += cov
    book_results.append((bi, pct, tot, parts))

old_pct = 57.6  # from session 11c
new_pct = total_cov * 100 / total_chars
print(f"\n1. COVERAGE COMPARISON")
print("-" * 60)
print(f"  Previous word list: {old_pct:.1f}%")
print(f"  Expanded word list: {new_pct:.1f}% ({new_pct - old_pct:+.1f}%)")

# 2. Show new words that were found
print(f"\n2. NEWLY MATCHED WORDS")
print("-" * 60)

new_words_added = [
    'DU', 'HAT', 'BIS', 'SINE', 'SAGEN', 'HABEN', 'KOMEN', 'GEBEN',
    'NEMEN', 'SEHEN', 'WISEN', 'LESEN', 'REDEN', 'LEBEN', 'GEHEN',
    'TRAGEN', 'LIGEN', 'SITEN', 'BITEN', 'LEGEN', 'SETEN', 'RITEN',
    'VINDEN', 'BINDEN', 'SINGEN', 'RINGEN', 'DISEN', 'WILEN', 'NIDEN',
    'SAG', 'GAB', 'NAM', 'SAH', 'LAS', 'BAT', 'LAG',
    'SPRACH', 'SPRICHT',
    'HERR', 'FRAU', 'VROUWE', 'RITTER', 'KNECHT',
    'BURC', 'BURG', 'STAT', 'STEINE',
    'WASSER', 'FEUER', 'LUFT',
    'NACHT', 'MORGEN', 'ABEND',
    'KRAFT', 'MACHT', 'EHRE', 'MINNE',
    'LIEBE', 'LEBEN', 'STERBEN', 'LEIDEN',
    'VOLC', 'VOLK',
    'UM', 'AM', 'AB', 'BI', 'ZU',
    'VOR', 'MAN', 'GUT', 'NEU', 'ALT',
    'ROT', 'WAS', 'WER', 'WEN', 'WEM',
    'IHR', 'IHN', 'DIR', 'MIR', 'UNS',
    'DOCH', 'EBEN', 'GANZ', 'BALD', 'SCHON',
    'EWIG', 'TIEF', 'WEIT', 'LANG',
    'DREI', 'VIER', 'ACHT', 'NEUN', 'ZEHN', 'ZWEI',
    'MEIN', 'DEIN', 'DISE', 'MICH', 'DICH',
    'GILT', 'GALT', 'GING', 'GETAN', 'WARS', 'WURD',
    'HIEZ', 'LIEZ', 'SACH', 'SOLT', 'WOLT', 'MUOZ',
    'HEIL', 'WEHE', 'SELE',
    'SEELE', 'GEIST', 'WESEN', 'ORDEN',
    'ALTAR', 'TEMPEL', 'GRAB', 'TURM',
    'FLUCH', 'BANN', 'SCHWUR',
    'RUNEN', 'ZAUBER', 'MAGIE',
    'DUNKEL', 'LICHT', 'SCHATTEN',
    'DRACHE', 'DRACHEN',
]

# Count how often each new word appears in the corpus
found_new = Counter()
for w in set(new_words_added):
    for text in all_collapsed:
        found_new[w] += text.count(w)

found_new = {w: c for w, c in found_new.items() if c > 0}
for w, c in sorted(found_new.items(), key=lambda x: -x[1]):
    print(f"  {w}: {c}x")

# 3. Remaining unknowns after expansion
print(f"\n3. REMAINING UNKNOWN SEGMENTS")
print("-" * 60)

all_unknowns = Counter()
for bi, pct, tot, parts in book_results:
    for ptype, ptext in parts:
        if ptype == '?':
            all_unknowns[ptext] += 1

print(f"  Total unique unknowns: {len(all_unknowns)}")
print(f"\n  Multi-char unknowns (>=2 chars, >=2 occurrences):")
for unk, count in all_unknowns.most_common(50):
    if len(unk) >= 2 and count >= 2:
        print(f"    '{unk}' x{count}")

# 4. Show best-decoded books with new word list
print(f"\n4. TOP 10 BOOKS BY COVERAGE")
print("-" * 60)
book_results.sort(key=lambda x: x[1], reverse=True)
for bi, pct, tot, parts in book_results[:10]:
    formatted = ''
    for ptype, ptext in parts:
        if ptype == 'W':
            formatted += ptext + ' '
        else:
            formatted += f'[{ptext}]'
    print(f"  B{bi:02d} ({pct:.1f}%): {formatted[:120]}")

# 5. Full narrative of best book
print(f"\n5. BEST BOOK FULL NARRATIVE")
print("-" * 60)
best_bi, best_pct, best_tot, best_parts = book_results[0]
print(f"  Book {best_bi} ({best_pct:.1f}% coverage):\n")
line = ''
line_num = 1
for ptype, ptext in best_parts:
    if ptype == 'W':
        word = ptext
    else:
        word = f'[{ptext}]'
    if len(line) + len(word) + 1 > 70:
        print(f"    {line_num:3d}| {line}")
        line = word + ' '
        line_num += 1
    else:
        line += word + ' '
if line.strip():
    print(f"    {line_num:3d}| {line}")

# 6. Pattern mining: look for recurring multi-char unknowns that might be words
print(f"\n6. PATTERN MINING: RECURRING UNKNOWN SEQUENCES")
print("-" * 60)

# Extract all unknown runs of 3+ chars that appear 2+ times
unk_runs = Counter()
for text in all_collapsed:
    parts, _, _ = dp_segment(text)
    # Merge consecutive unknowns
    merged = []
    for ptype, ptext in parts:
        if ptype == '?' and merged and merged[-1][0] == '?':
            merged[-1] = ('?', merged[-1][1] + ptext)
        else:
            merged.append((ptype, ptext))
    for ptype, ptext in merged:
        if ptype == '?' and len(ptext) >= 3:
            unk_runs[ptext] += 1

print(f"  Unknown runs >=3 chars, appearing >=2 times:")
for run, count in unk_runs.most_common(30):
    if count >= 2:
        # Show context (what comes before and after)
        contexts = []
        for text in all_collapsed:
            idx = text.find(run)
            if idx >= 0:
                before = text[max(0,idx-10):idx]
                after = text[idx+len(run):idx+len(run)+10]
                contexts.append(f"...{before}[{run}]{after}...")
                if len(contexts) >= 2:
                    break
        print(f"  '{run}' x{count}")
        for ctx in contexts:
            print(f"      {ctx}")

# 7. Try reading unknown segments as potential German words
# with letter substitution guesses
print(f"\n7. UNKNOWN -> GERMAN WORD HYPOTHESES")
print("-" * 60)

# Focus on frequent unknowns
top_unknowns = [unk for unk, c in unk_runs.most_common(20) if c >= 2 and len(unk) >= 3]

for unk in top_unknowns:
    # Check if any standard German words could match with 1-2 letter changes
    potential = []
    for w in ['BRUDER', 'VATER', 'MUTTER', 'SCHWESTER', 'TOCHTER',
              'MEISTER', 'KOENIG', 'RITTER', 'KRIEGER', 'JAEGER',
              'DRACHE', 'SCHLANGE', 'DAEMON', 'GEISTER',
              'GERADE', 'GEWESEN', 'GESEHEN', 'GEMACHT', 'GESAGT',
              'SOLCHE', 'WELCHE', 'MANCHER', 'JEDER', 'KEINER',
              'GETRAGEN', 'GEFUNDEN', 'GEBUNDEN', 'GESUNGEN',
              'WUNDER', 'DONNER', 'BLITZ', 'STURM', 'HIMMEL',
              'STERBEN', 'WANDERN', 'FLIEGEN', 'REISEN',
              'DUNKEL', 'FINSTER', 'GRAUSAM', 'HEILIG',
              'VERGESSEN', 'VERSPRECHEN', 'VERSTEHEN', 'ENTDECKEN',
              'EWIGKEIT', 'FREIHEIT', 'WAHRHEIT', 'WEISHEIT',
              'SCHICKSAL', 'ABENTEUER', 'GEHEIMNIS',
              'EDELSTEIN', 'SILBER', 'EISEN', 'KUPFER',
              # MHG-specific
              'VROUWE', 'SWERT', 'MINNE', 'TRIUWE', 'STAETE',
              'AVENTIURE', 'RECKE', 'DEGEN', 'WIGANT',
              'NIBELUNGEN', 'KRIEMHILD', 'SIEGFRIED',
              ]:
        if len(w) == len(unk):
            diffs = sum(1 for a, b in zip(unk, w) if a != b)
            if diffs <= 2:
                potential.append((w, diffs))
    if potential:
        print(f"  {unk} (len={len(unk)}):")
        for w, d in sorted(potential, key=lambda x: x[1]):
            print(f"    -> {w} ({d} diff{'s' if d > 1 else ''})")

# 8. Analyze the narrative structure
print(f"\n8. NARRATIVE STRUCTURE ANALYSIS")
print("-" * 60)

# Find the most common word sequences (bigrams)
bigrams = Counter()
for text in all_collapsed:
    parts, _, _ = dp_segment(text)
    words = [ptext for ptype, ptext in parts if ptype == 'W']
    for i in range(len(words) - 1):
        bigrams[(words[i], words[i+1])] += 1

print(f"  Most common word pairs:")
for (w1, w2), count in bigrams.most_common(30):
    if count >= 2:
        print(f"    {w1} {w2} ({count}x)")

# 9. Summary
print(f"\n9. COVERAGE SUMMARY")
print("-" * 60)
print(f"  Words in list: {len(all_words)}")
print(f"  Total corpus: {total_chars} chars")
print(f"  Total covered: {total_cov} chars ({new_pct:.1f}%)")
print(f"  Books >90%: {sum(1 for _,p,_,_ in book_results if p >= 90)}")
print(f"  Books >80%: {sum(1 for _,p,_,_ in book_results if p >= 80)}")
print(f"  Books >70%: {sum(1 for _,p,_,_ in book_results if p >= 70)}")
print(f"  Books >50%: {sum(1 for _,p,_,_ in book_results if p >= 50)}")

print("\n" + "=" * 80)
print("SESSION 12a COMPLETE")
print("=" * 80)
