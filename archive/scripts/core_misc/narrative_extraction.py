#!/usr/bin/env python3
"""
Narrative Extraction with V7 Mapping
=====================================
Extract the continuous narrative by concatenating decoded text
from all books in order, segmenting into words, and attempting
a coherent German translation.
"""

import json, os
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)

GERMAN_WORDS = set([
    'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO',
    'DU', 'OB', 'AM', 'IM', 'AB',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST',
    'WIR', 'ICH', 'SIE', 'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI', 'VOR', 'FUR', 'VOM',
    'ZUM', 'ZUR', 'BIS', 'ALS', 'NUN', 'HIN', 'TAG', 'ORT', 'TOD',
    'OFT', 'NIE', 'ALT', 'NEU', 'GAR', 'NET', 'ODE', 'SEI', 'TUN',
    'MAL', 'RAT', 'RUF', 'MUT', 'HUT', 'NOT', 'ROT', 'TAT',
    'ENDE', 'REDE', 'RUNE', 'WORT', 'NACH', 'AUCH',
    'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN', 'WARD', 'DASS', 'WENN',
    'DANN', 'DENN', 'ABER', 'ODER', 'WEIL', 'WIRD', 'EINE', 'DIES',
    'HIER', 'DORT', 'WELT', 'ZEIT', 'TEIL', 'SEID', 'WORT', 'NAME',
    'GANZ', 'SEHR', 'VIEL', 'FORT', 'HOCH', 'KLAR', 'ERDE', 'GOTT',
    'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN', 'WAHR', 'HELD', 'FACH',
    'WIND', 'FAND', 'GING', 'NAHM', 'SAGT', 'KANN', 'SOLL', 'WILL',
    'MUSS', 'GIBT', 'RIEF', 'LAND', 'HAND', 'BAND', 'SAND', 'WAND',
    'MACHT', 'KRAFT', 'GEIST', 'NACHT', 'LICHT', 'KRIEG', 'REICH',
    'UNTER', 'DURCH', 'GEGEN', 'IMMER', 'NICHT', 'SCHON',
    'DIESE', 'SEINE', 'EINEN', 'EINER', 'EINEM', 'EINES',
    'URALTE', 'STEINEN', 'STEINE', 'STEIN', 'RUNEN', 'FINDEN',
    'STEHEN', 'GEHEN', 'KOMMEN', 'SAGEN', 'WISSEN',
    'ERSTE', 'ANDEREN', 'KOENIG', 'SCHAUN', 'RUIN',
    'ORTE', 'ORTEN', 'WORTE', 'STEH', 'GEH',
    'ALLE', 'ALLES', 'VIELE', 'WIEDER', 'WISSET',
    'SPRACH', 'GESCHAH', 'GEFUNDEN', 'GEBOREN', 'GESTORBEN',
    'ZWISCHEN', 'HEILIG', 'DUNKEL', 'SCHWERT',
    'STIMME', 'ZEICHEN', 'HIMMEL', 'SEELE', 'GEHEIMNIS',
    'MIN', 'SER', 'GEN', 'WEG', 'INS', 'HER',
    'SEI', 'LIES', 'SAG', 'GIB', 'WAR', 'GAR',
    'REDE', 'REDEN', 'WESEN', 'EHRE', 'TREUE', 'GRAB', 'GRUFT',
    'ALTE', 'ALTEN', 'ALTER', 'NEUE', 'NEUEN',
    'DUNKLE', 'DUNKLEN',
    'HWND', 'OEL', 'SCE', 'MINNE', 'RUCHTIG',
    'HEARUCHTIG', 'HEARUCHTIGER',
    'LABGZERAS', 'HEDEMI', 'ADTHARSC', 'TAUTR',
    'TOTNIURG', 'TOTNIURGS', 'EDETOTNIURG', 'EDETOTNIURGS',
    'SCHWITEIONE', 'SCHWITEIO', 'ENGCHD', 'KELSEI',
    'TIUMENGEMI', 'LABRNI', 'UTRUNR', 'GEVMT',
    'AUNRSONGETRASES', 'EILCH', 'EILCHANHEARUCHTIG',
    'DIESEN', 'DIESEM', 'DIESER', 'DIESES',
    'SEINER', 'SEINEN', 'SEINES', 'SEINEM',
    'NORDEN', 'SUEDEN', 'OSTEN', 'WESTEN',
    'RUNEORT', 'RUNENSTEIN',
    'EDEL', 'ADEL', 'HARSCH', 'SCHAR',
    'HIHL', 'SANG',
    'TEIL', 'TEILE', 'TEILEN', 'SEITE', 'SEITEN',
    'TAGE', 'TAGEN', 'NEBEN',
    'SAGTE', 'WURDE', 'WAREN', 'HATTE',
    'HABEN', 'LEBEN', 'SEHEN', 'NEHMEN', 'GEBEN',
    'FEUER', 'WASSER', 'STEIN', 'HOLZ', 'EISEN',
    'STERN', 'STERNE', 'MOND', 'SONNE',
    'BLUT', 'BEIN', 'HERZ', 'LEIB', 'HAUPT',
    'FLUCHT', 'FURCHT', 'ZORN', 'STOLZ', 'SCHULD',
    'FRIEDE', 'FRIEDEN', 'FREUND', 'FEIND',
    'TURM', 'MAUER', 'STRASSE',
    'DORF', 'STADT', 'SCHLOSS', 'TEMPEL',
    'WALD', 'WIESE', 'FLUSS', 'MEER', 'INSEL',
    'SAGE', 'SAGEN', 'LEGENDE',
    'ACHT', 'NEUN', 'ZEHN', 'DREI', 'VIER',
    'SECHS', 'SIEBEN', 'ZWEI', 'EINS',
])

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

# ============================================================
# FIND RECURRING PHRASES (multi-book consensus)
# ============================================================
print("=" * 70)
print("NARRATIVE FLOW ANALYSIS WITH V7 MAPPING")
print("=" * 70)

# Decode all books
all_decoded = []
for idx, book in enumerate(books):
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    text = ''.join(v7.get(p, '?') for p in pairs)
    tokens, covered = dp_parse(text)
    known = sum(1 for c in text if c != '?')
    pct = covered / max(known, 1) * 100
    all_decoded.append({
        'idx': idx,
        'text': text,
        'parsed': ' '.join(tokens),
        'pct': pct,
        'length': len(pairs),
    })

# Sort by coverage
all_decoded.sort(key=lambda x: -x['pct'])

# Find the most common phrases across books
# Extract all recognized word sequences
phrase_counter = Counter()
for d in all_decoded:
    tokens, _ = dp_parse(d['text'])
    # Extract sequences of consecutive words
    words = []
    for t in tokens:
        if t.startswith('['):
            if len(words) >= 2:
                phrase = ' '.join(words)
                phrase_counter[phrase] += 1
            words = []
        else:
            words.append(t)
    if len(words) >= 2:
        phrase = ' '.join(words)
        phrase_counter[phrase] += 1

print("\n--- MOST COMMON RECOGNIZED PHRASES ---")
for phrase, count in phrase_counter.most_common(30):
    if count >= 2 and len(phrase) > 10:
        print(f"  {count}x: {phrase}")

# ============================================================
# EXTRACT LONGEST NARRATIVE SEGMENTS
# ============================================================
print(f"\n{'=' * 70}")
print("LONGEST RECOGNIZED NARRATIVE SEGMENTS")
print(f"{'=' * 70}")

all_segments = []
for d in all_decoded:
    tokens, _ = dp_parse(d['text'])
    current_seg = []
    for t in tokens:
        if not t.startswith('['):
            current_seg.append(t)
        else:
            if len(current_seg) >= 3:
                all_segments.append((' '.join(current_seg), d['idx']))
            current_seg = []
    if len(current_seg) >= 3:
        all_segments.append((' '.join(current_seg), d['idx']))

all_segments.sort(key=lambda x: -len(x[0]))
seen = set()
print()
for seg, bidx in all_segments[:30]:
    if seg not in seen:
        seen.add(seg)
        print(f"  Book {bidx:2d}: {seg}")

# ============================================================
# RECONSTRUCT FULL NARRATIVE (ordered by highest coverage)
# ============================================================
print(f"\n{'=' * 70}")
print("FULL NARRATIVE RECONSTRUCTION (books >60% coverage)")
print(f"{'=' * 70}")

for d in sorted(all_decoded, key=lambda x: x['idx']):
    if d['pct'] >= 60 and d['length'] >= 30:
        print(f"\nBook {d['idx']:2d} ({d['pct']:.0f}%):")
        print(f"  {d['parsed']}")

# ============================================================
# AGGREGATE TRANSLATION ATTEMPT
# ============================================================
print(f"\n{'=' * 70}")
print("AGGREGATE TRANSLATION ATTEMPT")
print(f"{'=' * 70}")

# The core repeating narrative, pieced together from highest-coverage books
print("""
Based on books with >75% coverage, the narrative reconstructs as:

SECTION 1 - The Anointing (Books 46, 51, 53):
  "...ES ER SCE AUS E ODE DU N IN DENN AN GEN SS IN HIHL
   DIE NDCE FACH HECHLLT ICH OEL SO DEN HIER..."

   Partial: "...he/it [SCE] from [?] or you [?] then at [GEN=?]
   [SS=?] in HIHL the [NDCE] [FACH] [HECHLLT]
   I anoint so the here..."

SECTION 2 - The Notorious One (Books 2, 5, 9, 22, 46, 48):
  "TAUTR IST EILCH AN HEARUCHTIG ER SO DASS TUN
   DIES ER T EIN ER SEIN EDETOTNIURGS"

   Translation: "TAUTR is EILCH(hastily) of-notorious-repute,
   he so that do(ing) this he [?] one, he his
   EDETOTNIURGS(death-ruin-fortress)"

SECTION 3 - The Ancient Stones (Books 0, 5, 9, 58, 69):
  "ER LABRNI WIR UOD IM MIN HEDEMI DIE URALTE STEINEN
   TER ADTHARSC IST SCHAUN RUIN"

   Translation: "he LABRNI(Berlin) we [?] in-the love(MINNE)
   HEDEMI(Kelheim) the ancient stones [of] ADTHARSC(Bachstadt)
   is to-behold ruin"

SECTION 4 - The Rune Places (Books 11, 18, 32, 43, 58):
  "ODE GAR EO RUNE ORT NDT ER AM NEU DENN
   DTEII ORT AN UD IM MIN HEDEMI DIE URALTE STEINE"

   Translation: "or(ODE) very [?] rune place [NDT] he
   at(AM) new(NEU) then(DENN) [?] place at [?]
   in-the love HEDEMI the ancient stones"

SECTION 5 - The King's Speech (Books 1, 10, 19, 27, 31, 35, 57, 63, 66):
  "ODE UTRUNR DEN ENDE REDE R KOENIG LABGZERAS
   UNENITGHNEE AUNRSONGETRASES"

   Translation: "or UTRUNR(Rundturm?) the end speech [of]
   King LABGZERAS(Salzberg=Salt Mountain)
   [?] AUNRSONGETRASES(Orangenstrasse?)"

SECTION 6 - Schwiteione (Books 8, 23, 24, 37):
  "ENDE E SCHWITEIONE GAR NUN ENDE"
  "DAS WIR NSCHA ER ALTE II ORTE"

   Translation: "End [of] SCHWITEIONE(Weichstein=Soft Stone)
   very/indeed(GAR) now end"
   "that we [?] he old [?] places"

PROPER NOUNS IDENTIFIED:
  LABGZERAS    = SALZBERG    (Salt Mountain - anagram +A)
  SCHWITEIONE  = WEICHSTEIN  (Soft Stone - anagram +O)
  HEDEMI       ~ KELHEIM     (Bavarian town near CipSoft/Regensburg)
  LABRNI       ~ BERLIN      (Capital)
  ADTHARSC     ~ BACHSTADT   (Brook Town)
  TIUMENGEMI   ~ EIGENTUM    (Property/Possession)
  EDETOTNIURG  = ?TOTENGRUDE (Death Pit? - anagram attempt)
  UTRUNR       ~ RUNDTURM    (Round Tower)
  AUNRSONGETRASES = ?ORANGENSTRASSE+S (Orange Street)
  HIHL         = ? (proper noun, appears with RUNE)
  EILCH        = ? (hastily? or proper noun)
  TAUTR        = ? (proper noun)
  HEARUCHTIG   = HERAUSCHTIG = "notorious" (Middle High German)
  ENGCHD       = ? (proper noun)
  KELSEI       = ? (proper noun)
""")

# ============================================================
# STATISTICS
# ============================================================
total_books = len(all_decoded)
high_cov = sum(1 for d in all_decoded if d['pct'] >= 70)
med_cov = sum(1 for d in all_decoded if 50 <= d['pct'] < 70)
low_cov = sum(1 for d in all_decoded if d['pct'] < 50)

total_chars = sum(d['length'] for d in all_decoded)
avg_cov = sum(d['pct'] * d['length'] for d in all_decoded) / total_chars

print(f"\n{'=' * 70}")
print("STATISTICS")
print(f"{'=' * 70}")
print(f"  Total books decoded: {total_books}")
print(f"  Books >70% coverage: {high_cov}")
print(f"  Books 50-70% coverage: {med_cov}")
print(f"  Books <50% coverage: {low_cov}")
print(f"  Weighted average coverage: {avg_cov:.1f}%")
print(f"  Total decoded characters: {total_chars}")
print(f"  Codes mapped: {len(v7)}/98 unique codes in data")
