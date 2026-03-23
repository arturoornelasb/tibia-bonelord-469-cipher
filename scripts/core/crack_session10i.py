#!/usr/bin/env python3
"""Session 10i: German dictionary mining + MHG word finder"""

import json, re
from collections import Counter, defaultdict

with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)
with open('data/books.json') as f:
    raw_books = json.load(f)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]
books = [parse_codes(b) for b in raw_books]
def decode(book):
    return ''.join(mapping.get(c, '?') for c in book)
def collapse(s):
    return re.sub(r'(.)\1+', r'\1', s)

print("=" * 80)
print("SESSION 10i: DICTIONARY MINING & MHG WORD FINDER")
print("=" * 80)

# Comprehensive German word list (modern + MHG + OHG)
german_dict = set([
    # Common modern German words (3-8 chars)
    'ACH', 'ALS', 'ALT', 'ARM', 'ART', 'AUF', 'AUS',
    'BAD', 'BEI', 'BIS', 'BOG', 'DAM',
    'DAS', 'DEM', 'DEN', 'DER', 'DIE', 'DIR', 'DOM',
    'EHE', 'EIS', 'END', 'ERD', 'ERZ',
    'FEL', 'FER', 'FIN', 'FOR',
    'GAR', 'GEN', 'GIB', 'GUT',
    'HAT', 'HER', 'HIN', 'HOF',
    'IHM', 'IHN', 'IHR', 'IRR',
    'KAM', 'KIN', 'KON',
    'LAS', 'LOS',
    'MAG', 'MAL', 'MAN', 'MIR', 'MUT',
    'NAH', 'NIE', 'NOR', 'NOT', 'NUN', 'NUR',
    'OFT',
    'RAT', 'RUF', 'RUH',
    'SAH', 'TAL', 'TAT', 'TOR', 'TOT', 'TUR',
    'UHR', 'UMS', 'UNS',
    'VOR',
    'WAR', 'WAS', 'WEM', 'WEN', 'WER', 'WIE', 'WOL',
    'ZUM', 'ZUR', 'ZWO',
    # 4-letter
    'ABER', 'ALLE', 'ALSO', 'AUCH', 'BAND', 'BAUM', 'BERG',
    'BILD', 'BLUT', 'BURG', 'CHER', 'DEIN', 'DICH', 'DIES',
    'DOCH', 'DREI', 'DRIN', 'EBEN', 'EDEL', 'EDLE', 'EHER',
    'EILE', 'ERDE', 'ERST', 'EUCH', 'EUER',
    'FELD', 'FEST', 'FERN', 'FIEL', 'FORT', 'FREI',
    'GANZ', 'GERN', 'GIER', 'GLAS', 'GOLD', 'GOTT', 'GRAB',
    'HALB', 'HALT', 'HAND', 'HAUS', 'HEIL', 'HELD', 'HERR',
    'HOCH', 'HORN', 'HUND',
    'IRGD',
    'KALT', 'KERN', 'KIND', 'KLAR', 'KNIE', 'KORN', 'KURZ',
    'LAND', 'LANG', 'LAUT', 'LEER', 'LEID', 'LIED', 'LUFT',
    'MEIN', 'MILD', 'MOND', 'MORD', 'MUND', 'NACHT',
    'NAME', 'NOCH', 'NORD', 'OBEN', 'OFEN', 'OHNE',
    'PLAT', 'RING', 'REIN', 'RIEF', 'ROSS', 'RUND', 'RUHE',
    'SAAL', 'SAND', 'SEHR', 'SEIT', 'SICH', 'SIND', 'SOLL',
    'SOHN', 'STAMM', 'STAR', 'TIEF', 'TIER', 'TODE',
    'TREU', 'TRUG', 'WALD', 'WAND', 'WEIL', 'WEIN', 'WEIS',
    'WELT', 'WENN', 'WERT', 'WILL', 'WOHL', 'WOLF', 'WORT',
    'WUND', 'WURM', 'ZAHL', 'ZEIT', 'ZORN', 'ZWEI',
    # 5-letter
    'ABEND', 'ADLER', 'ALLES', 'ALTER', 'ANDER', 'ANTIG',
    'BEGAN', 'BEIDE', 'BERGE', 'BITTE', 'BLICK', 'BODEN',
    'BREIT', 'BRUST', 'DAVON', 'DEINE', 'DELLE', 'DENEN',
    'DIESE', 'DURCH', 'DUNST', 'DUNKEL',
    'EHREN', 'EIGEN', 'EILIG', 'EINEN', 'EINER', 'ENGEL',
    'EWIGE',
    'FEIND', 'FEUER', 'FLUCH', 'FREMD', 'FRIEDE',
    'GEBEN', 'GEGEN', 'GEIST', 'GNADE', 'GRAVE', 'GREIS',
    'HABEN', 'HAUPT', 'HEISS', 'HERZE',
    'IMMER', 'INNEN', 'JEDER', 'JENEN', 'KAMPF', 'KEINE',
    'KLANG', 'KNABE', 'KRAFT', 'KRONE', 'KUNST',
    'LANDE', 'LANGE', 'LESEN', 'LEUTE', 'LICHT', 'LIEBE',
    'MACHT', 'MEIDE', 'MITTE', 'MOEGE', 'NACHT',
    'NEUEN', 'NICHT', 'NORDEN', 'OSTEN',
    'RECHT', 'REDEN', 'REISE', 'RIESE', 'RUFEN',
    'SAGEN', 'SCHON', 'SEELE', 'SEGEN', 'SEIDE', 'SEINE',
    'SONNE', 'SORGE', 'STAND', 'STARK', 'STEIN', 'STERN',
    'STIRN', 'STOLZ', 'STURM', 'SUCHE', 'SUNDE',
    'TAGEN', 'TIEFE', 'TOTEN', 'TRAUM', 'TREUE', 'TUGEND',
    'TURME',
    'UNTER', 'VATER', 'VIELE', 'VORNE',
    'WEISE', 'WERDE', 'WESEN', 'WIDER', 'WILLE', 'WIRST',
    'WONNE', 'WURDE', 'WURZEL',
    'ZEIGE', 'ZEIGT',
    # 6+ letter
    'ANDERE', 'ANFANG', 'ARBEIT',
    'BEGINN', 'BEREIT', 'BLUMEN',
    'DAREIN', 'DARAUF', 'DIENEN', 'DIESER', 'DUNKEL',
    'EINMAL', 'ENDLOS', 'ERSTER',
    'FINDEN', 'FLIEHE', 'FREUDE', 'FRIEDE', 'FUERST',
    'GAUKEL', 'GEHEIM', 'GEIGER', 'GEIGET', 'GELEIT', 'GENUG',
    'GESANG', 'GLEICH', 'GNADEN', 'GROSSE', 'GRUENE',
    'HAUFEN', 'HALTEN', 'HEILEN', 'HEILIG', 'HERREN', 'HIMMEL',
    'HOFFEN', 'HUETER',
    'KAMMER', 'KOENIG', 'KRIEGE', 'KOMMEN',
    'LANGEN', 'LEIDEN', 'LODERN',
    'MORGEN', 'MEINEM', 'MEINEN', 'MEINER',
    'NORDEN', 'NICHTS', 'NIMMER',
    'ORDNEN', 'RAETSEL',
    'SACHEN', 'SCHAUN', 'SEELEN', 'SELBER', 'SICHER',
    'SINGEN', 'SOLCHE', 'STEHEN', 'STELLE', 'STIMME',
    'SUENDE', 'SUCHEN',
    'TIEFEN', 'TREIBE', 'TUGEND', 'URALTE', 'URWALD',
    'VERGEH', 'WAHREN', 'WANDEL', 'WASSER', 'WEIDEN',
    'WEILEN', 'WERDEN', 'WISSET', 'WOLLEN', 'WUNDER',
    'ZEITEN', 'ZURUEK', 'ZWISCHEN',
    # MHG specific
    'DITZ', 'HAUN', 'RUNE', 'STEH', 'SCHAUN',
    'WISSET', 'GEIGEN', 'GEIGET', 'KELSEI',
    'REDE', 'SEIDE', 'HWND',
    'ORT', 'WEG', 'TAG', 'EIL',
    'GEN', 'HER', 'HIN', 'VOR',
    # MHG verbs
    'TUON', 'LAZEN', 'WESEN', 'WIZZEN',
    'HABEN', 'WERDEN', 'SAGEN',
    # Potential MHG words
    'TION', 'UNGE', 'HEIT', 'LICH', 'CHEN',
    'LEIN', 'ISCH', 'HAFT',
])

# Garbled segments to search
garbled_segments = [
    'EILCHANHEARUCHTIG',
    'EDETOTNIURGS',
    'EUGENDRTHENAEDEULGHLWUOEHSG',
    'MIHIETUNCISN',
    'TIUMENGEMI',
    'WRLGTNELNRHELUIRUNN',
    'DNRHAUNRNVMHISDIZA',
    'AUNRSONGETRASES',
    'SCHWITEIONE',
    'UNENITGHNE',
    'ADTHARSC',
    'ADTHAUMR',
    'OIAITOE',
    'NMHSO',
    'OEHSG',
    'URIHWNRS',
    'DGEDA',
    'LRSZTHK',
    'ENGCHD',
    'TEMDIA',
    'NESRER',
    'RSIC',
    'TUNR',
    'WISETEIS',
]

print("\n1. DICTIONARY SCAN OF GARBLED SEGMENTS")
print("-" * 60)

for segment in garbled_segments:
    hits = []
    for length in range(3, min(len(segment)+1, 9)):
        for start in range(len(segment) - length + 1):
            substr = segment[start:start+length]
            if substr in german_dict:
                hits.append((start, length, substr))

    if hits:
        # Remove substrings (keep longest at each position)
        best = {}
        for start, length, word in hits:
            if start not in best or length > best[start][0]:
                best[start] = (length, word)

        print(f"\n  {segment}:")
        for start in sorted(best.keys()):
            length, word = best[start]
            before = segment[:start]
            after = segment[start+length:]
            print(f"    pos {start}: [{word}] ({before}|{word}|{after})")

# 2. Full text scan for all dictionary words
print("\n" + "=" * 60)
print("2. FULL TEXT DICTIONARY COVERAGE")
print("=" * 60)

# Get all unique text
all_text = ''
for book in books:
    col = collapse(decode(book))
    if col not in all_text:
        all_text += col

# Find all dictionary words in the full text
word_counts = Counter()
for word in german_dict:
    if len(word) >= 3:
        count = all_text.count(word)
        if count > 0:
            word_counts[word] = count

print(f"\n  Words found in text (top 40):")
for word, count in word_counts.most_common(40):
    print(f"    {word:12s} ({count:3d}x)")

# 3. NEW word candidates (not in our confirmed list)
print("\n" + "=" * 60)
print("3. NEW WORD CANDIDATES")
print("=" * 60)

confirmed_set = {
    'DER', 'DIE', 'DAS', 'DEN', 'DENEN', 'EIN', 'ER', 'ES', 'SIE',
    'WIR', 'IST', 'UND', 'IN', 'VON', 'MIT', 'AUS', 'SO', 'WIE',
    'SEI', 'SEIN', 'NICHT', 'ORT', 'TUN', 'STEIN', 'ERDE', 'RUNE',
    'VIEL', 'KOENIG', 'GEIGET', 'STEH', 'SCHAUN', 'REDE', 'ENDE',
    'URALTE', 'UNTER', 'FINDEN', 'TAG', 'WEG', 'HUND', 'SEIDE',
    'GOLD', 'MOND', 'SONNE', 'WELT', 'LIED', 'SEGEN', 'DORT',
    'DENN', 'WIRD', 'WERDE', 'KLAR', 'NORDEN', 'KELSEI',
    'GEN', 'HER', 'HIN', 'NUR',
}

new_words = []
for word, count in word_counts.most_common(100):
    if word not in confirmed_set and count >= 2:
        # Check if it appears at word boundaries (after/before known words)
        new_words.append((word, count))

print(f"\n  New word candidates (>=2 occurrences, not already confirmed):")
for word, count in new_words[:30]:
    # Show one context
    for bi, book in enumerate(books):
        col = collapse(decode(book))
        if word in col:
            pos = col.index(word)
            start = max(0, pos-10)
            end = min(len(col), pos+len(word)+10)
            ctx = col[start:end]
            print(f"    {word:10s} ({count:2d}x): ...{ctx}...")
            break

# 4. Trigram analysis of unknown segments
print("\n" + "=" * 60)
print("4. COMMON TRIGRAMS IN UNKNOWNS")
print("=" * 60)

# Collect all unknown segments from the text
unknown_text = ''
for bi, book in enumerate(books):
    col = collapse(decode(book))
    # Remove known words to get unknown residue
    residue = col
    for word in sorted(confirmed_set, key=len, reverse=True):
        residue = residue.replace(word, ' ')
    unknown_text += residue.replace(' ', '')

trigram_counts = Counter()
for i in range(len(unknown_text)-2):
    tri = unknown_text[i:i+3]
    if '?' not in tri:
        trigram_counts[tri] += 1

print(f"\n  Top 20 trigrams in unknown text:")
for tri, count in trigram_counts.most_common(20):
    # Check if this trigram is a German word fragment
    matches = [w for w in german_dict if tri in w]
    match_str = ', '.join(matches[:3]) if matches else '(no matches)'
    print(f"    {tri}: {count:3d}x -> {match_str}")

# 5. DIES/DIESER test
print("\n" + "=" * 60)
print("5. DIES/DIESER IN TEXT")
print("=" * 60)

for bi, book in enumerate(books):
    col = collapse(decode(book))
    for pattern in ['DIES', 'DIESER']:
        if pattern in col:
            pos = col.index(pattern)
            start = max(0, pos-10)
            end = min(len(col), pos+len(pattern)+10)
            ctx = col[start:end]
            print(f"  B{bi:02d}: {pattern} in ...{ctx}...")
            break

# 6. Check for EDEL (noble) in EDETOTNIURGS
print("\n" + "=" * 60)
print("6. EDEL CHECK IN EDETOTNIURGS")
print("=" * 60)

# EDETOTNIURGS: if EDE = EDEL with L dropped... no, that doesn't work
# But: EDEL appears elsewhere?
for bi, book in enumerate(books):
    col = collapse(decode(book))
    if 'EDEL' in col:
        pos = col.index('EDEL')
        start = max(0, pos-10)
        end = min(len(col), pos+14)
        ctx = col[start:end]
        print(f"  B{bi:02d}: EDEL in ...{ctx}...")

print("\n  EDETOTNIURGS decomposition:")
print("    E-DE-TOT-N-I-URGS")
print("    EDE-TOT-NI-URGS")
print("    EDET-OT-NI-URGS")
print("    If TOT=dead: 'EDE-dead-NIURGS'")
print("    If NIURG=? NIUR=nur(only)? NIURG+S?")

# 7. Search for ALSO, NOCH, DOCH, EBEN, ERST, GANZ
print("\n" + "=" * 60)
print("7. COMMON GERMAN WORDS SEARCH")
print("=" * 60)

search = ['ALSO', 'NOCH', 'DOCH', 'EBEN', 'ERST', 'GANZ', 'GERN',
          'HALB', 'HALT', 'HOCH', 'KURZ', 'LANG', 'MEIN', 'OBEN',
          'OHNE', 'REIN', 'WOHL', 'ALLE', 'EWIG', 'FERN', 'FEST',
          'FREI', 'GROSS', 'HEISS', 'KALT', 'EDEL', 'STOLZ',
          'WILD', 'WAHR', 'STARK', 'REICH', 'EIGEN', 'HEILIG',
          'ALLES', 'DIESER', 'DIESE', 'SOLCH', 'JEDER', 'JENE',
          'EUER', 'DEIN', 'UNSER', 'DEREN', 'WELCH',
          'SOLL', 'KANN', 'MUSS', 'DARF', 'WILL',
          'WARD', 'WART', 'WURD',
          'GOTT', 'HERR', 'HELD', 'FEIND', 'FREUND',
          'MACHT', 'KRAFT', 'GEIST', 'SEELE',
          'HIMMEL', 'HOELLE', 'LEBEN', 'STERB',
          'SUCHE', 'WEISE', 'DEUT', 'WICH', 'TRUG', 'BRACH',
          'LICHT', 'NACHT', 'FEUER', 'WASSER',
          'SUN', 'SUNNE', 'MANE', 'STERRE',
          ]

found = []
for word in search:
    for bi, book in enumerate(books):
        col = collapse(decode(book))
        if word in col:
            pos = col.index(word)
            start = max(0, pos-8)
            end = min(len(col), pos+len(word)+8)
            ctx = col[start:end]
            count = sum(collapse(decode(b)).count(word) for b in books)
            found.append((word, count, bi, ctx))
            break

for word, count, bi, ctx in sorted(found, key=lambda x: -x[1]):
    if count >= 2:
        print(f"  {word:10s} ({count:2d}x): B{bi:02d} ...{ctx}...")

# 8. TION/UNGE/HEIT suffixes
print("\n" + "=" * 60)
print("8. GERMAN SUFFIX SEARCH")
print("=" * 60)

suffixes = ['TION', 'UNGE', 'HEIT', 'KEIT', 'LICH', 'ISCH', 'HAFT',
            'LING', 'CHEN', 'LEIN', 'TUNG', 'SCHAFT', 'ERIN', 'NISS']

for suffix in suffixes:
    count = sum(collapse(decode(b)).count(suffix) for b in books)
    if count > 0:
        for bi, book in enumerate(books):
            col = collapse(decode(book))
            if suffix in col:
                pos = col.index(suffix)
                start = max(0, pos-8)
                end = min(len(col), pos+len(suffix)+4)
                ctx = col[start:end]
                print(f"  -{suffix} ({count:2d}x): B{bi:02d} ...{ctx}...")
                break

print("\n" + "=" * 80)
print("SESSION 10i COMPLETE")
print("=" * 80)
