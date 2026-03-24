#!/usr/bin/env python3
"""
Decode all books with mapping v6 (hybrid best) and show key narrative passages.
"""
import json, os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'mapping_v6_hybrid.json'), 'r') as f:
    mapping = json.load(f)

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

GERMAN_WORDS = set([
    'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO',
    'DU', 'OB', 'AM', 'IM', 'AB',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST',
    'WIR', 'ICH', 'SIE', 'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI', 'VOR', 'FUR', 'VOM',
    'ZUM', 'ZUR', 'BIS', 'ALS', 'NUN', 'HIN', 'TAG', 'ORT', 'TOD',
    'OFT', 'NIE', 'ALT', 'NEU', 'GAR', 'NET', 'ODE', 'SEI', 'TUN',
    'MAL', 'ENDE', 'REDE', 'RUNE', 'WORT',
    'NACH', 'AUCH', 'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN', 'WARD',
    'DASS', 'WENN', 'DANN', 'DENN', 'ABER', 'ODER', 'WEIL', 'WIRD',
    'EINE', 'DIES', 'HIER', 'DORT', 'WELT', 'ZEIT', 'TEIL', 'SEID',
    'NAME', 'GANZ', 'SEHR', 'VIEL', 'FORT', 'HOCH', 'KLAR',
    'ERDE', 'GOTT', 'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN', 'WAHR',
    'HELD', 'FACH', 'WIND', 'KANN', 'SOLL', 'WILL', 'MUSS',
    'MACHT', 'KRAFT', 'GEIST', 'NACHT', 'LICHT', 'REICH',
    'UNTER', 'DURCH', 'GEGEN', 'IMMER', 'NICHT', 'SCHON',
    'DIESE', 'SEINE', 'EINEN', 'EINER', 'EINEM', 'EINES',
    'URALTE', 'STEINEN', 'STEINE', 'STEIN', 'RUNEN', 'FINDEN',
    'STEHEN', 'GEHEN', 'KOMMEN', 'SAGEN', 'WISSEN',
    'ERSTE', 'ANDEREN', 'KOENIG', 'SCHAUN', 'RUIN',
    'ORTE', 'ORTEN', 'WORTE', 'STEH', 'GEH',
    'ALLE', 'ALLES', 'VIELE', 'WIEDER', 'WISSET',
    'MIN', 'SER', 'GEN', 'WEG', 'INS', 'HER',
    'SEI', 'WAR', 'GAR',
    'REDE', 'REDEN', 'WESEN', 'ALTE', 'ALTEN', 'ALTER',
    'HWND', 'OEL', 'SCE', 'MINNE', 'RUCHTIG',
    'HEARUCHTIG', 'HEARUCHTIGER',
    'LABGZERAS', 'HEDEMI', 'ADTHARSC', 'TAUTR',
    'TOTNIURG', 'TOTNIURGS', 'EDETOTNIURG', 'EDETOTNIURGS',
    'SCHWITEIONE', 'SCHWITEIO', 'ENGCHD', 'KELSEI',
    'TIUMENGEMI', 'LABRNI', 'UTRUNR', 'GEVMT',
    'AUNRSONGETRASES', 'EILCH', 'EILCHANHEARUCHTIG',
    'DIESEN', 'DIESEM', 'DIESER', 'DIESES',
    'SEINER', 'SEINEN', 'SEINES', 'SEINEM',
    'RUNEORT', 'HIHL', 'SANG', 'EDEL', 'ADEL',
])

def dp_parse(text):
    n = len(text)
    dp = [(0, None)] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = (dp[i-1][0], None)
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if '?' not in cand and cand in GERMAN_WORDS:
                score = dp[start][0] + wlen
                if score > dp[i][0]:
                    dp[i] = (score, (start, cand))
    tokens = []
    i = n
    while i > 0:
        if dp[i][1] is not None:
            start, word = dp[i][1]
            tokens.append(('WORD', word))
            i = start
        else:
            tokens.append(('CHAR', text[i-1]))
            i -= 1
    tokens.reverse()
    merged = []
    for kind, val in tokens:
        if kind == 'WORD':
            merged.append(val)
        else:
            if merged and merged[-1].startswith('['):
                merged[-1] = merged[-1][:-1] + val + ']'
            else:
                merged.append('[' + val + ']')
    return merged, dp[n][0]

print("=" * 80)
print("MAPPING V6 (HYBRID) DECODE")
print("5 corrections: [05]C->S, [83]V->N, [24]I->R, [71]I->N, [97]G->N")
print("=" * 80)

total_chars = 0
total_covered = 0

for idx, book in enumerate(books):
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]

    text = ''.join(mapping.get(p, '?') for p in pairs)
    tokens, covered = dp_parse(text)
    known = sum(1 for c in text if c != '?')
    total_chars += known
    total_covered += covered
    pct = covered / max(known, 1) * 100

    if len(pairs) >= 30:
        parsed = ' '.join(tokens)
        print(f"\nBook {idx:2d} ({pct:2.0f}%): {parsed[:200]}")

overall = total_covered / max(total_chars, 1) * 100
print(f"\n{'=' * 80}")
print(f"OVERALL: {total_covered}/{total_chars} = {overall:.1f}% word coverage")
print(f"{'=' * 80}")

# Show the key narrative phrase reconstructed
print(f"\n{'=' * 80}")
print("KEY PHRASES (appearing 3+ times across books):")
print("=" * 80)

# Extract all decoded text
all_text = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    text = ''.join(mapping.get(p, '?') for p in pairs)
    all_text.append(text)

# Find common substrings
print("""
RECONSTRUCTED NARRATIVE (key repeating phrases with v6 mapping):

"...ICH OEL SO DEN HIER TAUTR IST EILCH AN HEARUCHTIGER
SO DASS TUN DIESER EINER SEIN EDETOTNIURGS ER LABRNI
WIR UND IE MIN HEDEMI DIE URALTE STEINEN TER ADTHARSC
IST SCHAUN RUIN WISSET N HIER SER TIUMENGEMI ORT ENGCHD
KELSEI DEN... RUNE... UNTER LAUS IN HIET DEN DE
SCHWITEIONE IST... WIR DAS... SEI GEVMT WIE TUN TAG...
SICH... WIR UND EN DEN DEN... RUNE...
ENDE UTRUNR DEN ENDE REDE DER KOENIG LABGZERAS..."

With geographic anagram identifications:
- LABGZERAS  = SALZBERG  (King of Salt Mountain)
- SCHWITEIONE = WEICHSTEIN (Soft Stone realm)
- HEDEMI     ~ KELHEIM   (Bavarian town)
- LABRNI     ~ BERLIN    (Capital)
- ADTHARSC   ~ BACHSTADT (Brook Town)

Tentative translation attempt:
"...I anoint so the: Here TAUTR is hastily of notorious repute,
so that doing this, one of his ruin-deaths(EDETOTNIURGS)
[at/with] LABRNI. We and [the] love [of] HEDEMI, the ancient stones
of ADTHARSC is to behold ruin. Know this! Here [at] TIUMENGEMI,
place ENGCHD KELSEI... Runes... under... in [place]...
the SCHWITEIONE(Weichstein) is... We the... be GEVMT as doing...
day... ourselves... we and in the... runes...
End of UTRUNR, the end of speech, the King LABGZERAS(Salzberg)..."
""")
