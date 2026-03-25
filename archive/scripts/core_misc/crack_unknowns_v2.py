"""
Crack the unknown codes by analyzing context across ALL books.
Focus on codes 74 (19x), 37 (8x), 40 (7x), 02 (4x).
"""
import json
import os
from collections import Counter

data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

# Tier 14 mapping with 05=S applied
mapping = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U', '00': 'H', '14': 'N', '72': 'R',
    '91': 'S', '15': 'I', '76': 'E', '52': 'S', '42': 'D',
    '46': 'I', '48': 'N', '57': 'H', '04': 'M', '12': 'S',
    '58': 'N', '78': 'T', '51': 'R', '35': 'A', '34': 'L',
    '01': 'E', '59': 'S', '41': 'E', '30': 'E', '94': 'H',
    '47': 'D', '13': 'N', '71': 'I', '63': 'D', '93': 'N',
    '28': 'D', '86': 'E', '43': 'U', '70': 'U', '65': 'I',
    '16': 'I', '36': 'W', '64': 'T', '89': 'A', '80': 'G',
    '97': 'G', '75': 'T', '08': 'R', '20': 'F', '96': 'L',
    '99': 'O', '55': 'R', '67': 'E', '27': 'E', '03': 'E',
    '09': 'E', '05': 'S', '53': 'N', '44': 'U', '62': 'B',
    '68': 'R', '23': 'S', '17': 'E', '29': 'E', '66': 'A',
    '49': 'E', '38': 'K', '77': 'Z', '22': 'K', '82': 'O',
    '73': 'N', '50': 'I', '84': 'G', '25': 'O', '83': 'V',
    '81': 'T', '24': 'I', '79': 'O', '10': 'R', '54': 'M',
    '98': 'T', '39': 'E', '87': 'W',
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

# Decode all books
all_decoded_texts = []
all_pairs_by_book = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    all_pairs_by_book.append(pairs)
    decoded = ''.join(mapping.get(p, f'[{p}]') for p in pairs)
    all_decoded_texts.append(decoded)

# Concatenate ALL decoded text for analysis
full_pairs = []
for pairs in all_pairs_by_book:
    full_pairs.extend(pairs)

full_decoded = ''.join(mapping.get(p, f'[{p}]') for p in full_pairs)

print(f"Total pairs across all books: {len(full_pairs)}")
print(f"Total decoded length: {len(full_decoded)} chars (incl brackets for unknowns)")

# === CONTEXT ANALYSIS: ALL OCCURRENCES ===
unknown_codes = ['74', '37', '40', '02', '33', '69']

for target in unknown_codes:
    occurrences = []
    for bi, pairs in enumerate(all_pairs_by_book):
        for pi, p in enumerate(pairs):
            if p == target:
                # Get wide context (10 pairs each side)
                ctx_before_pairs = pairs[max(0, pi-10):pi]
                ctx_after_pairs = pairs[pi+1:min(len(pairs), pi+11)]
                before = ''.join(mapping.get(x, f'[{x}]') for x in ctx_before_pairs)
                after = ''.join(mapping.get(x, f'[{x}]') for x in ctx_after_pairs)

                # Get immediate neighbors (1 pair each side)
                prev_letter = mapping.get(pairs[pi-1], '?') if pi > 0 else '^'
                next_letter = mapping.get(pairs[pi+1], '?') if pi < len(pairs)-1 else '$'

                occurrences.append({
                    'book': bi, 'pos': pi,
                    'before': before, 'after': after,
                    'prev': prev_letter, 'next': next_letter,
                    'prev_code': pairs[pi-1] if pi > 0 else None,
                    'next_code': pairs[pi+1] if pi < len(pairs)-1 else None,
                })

    if not occurrences:
        continue

    print(f"\n{'='*70}")
    print(f"CODE {target}: {len(occurrences)} occurrences")
    print(f"{'='*70}")

    # Show all contexts
    for i, occ in enumerate(occurrences):
        print(f"  [{i+1:2d}] Book {occ['book']:2d} pos {occ['pos']:3d}: "
              f"...{occ['before']}[{target}]{occ['after']}...")

    # Analyze what letters come BEFORE this code
    prev_counts = Counter(occ['prev'] for occ in occurrences)
    next_counts = Counter(occ['next'] for occ in occurrences)
    print(f"\n  Letters BEFORE code {target}: {dict(prev_counts)}")
    print(f"  Letters AFTER  code {target}: {dict(next_counts)}")

    # What bigrams would each letter create?
    print(f"\n  Bigram analysis for each possible letter:")
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        prev_bigrams = Counter()
        next_bigrams = Counter()
        for occ in occurrences:
            if occ['prev'] not in ('?', '^', '['):
                prev_bigrams[occ['prev'] + letter] += 1
            if occ['next'] not in ('?', '$', '['):
                next_bigrams[letter + occ['next']] += 1

        # Score German bigram plausibility
        german_common_bigrams = {
            'EN': 10, 'ER': 9, 'CH': 9, 'DE': 8, 'EI': 8, 'ND': 8,
            'TE': 8, 'IN': 8, 'IE': 8, 'GE': 8, 'ES': 7, 'NE': 7,
            'UN': 7, 'ST': 7, 'RE': 7, 'HE': 7, 'AN': 7, 'BE': 6,
            'SE': 6, 'DI': 6, 'DA': 6, 'AU': 6, 'AL': 6, 'LE': 6,
            'SC': 6, 'RA': 5, 'EL': 5, 'NG': 5, 'IC': 5, 'TI': 5,
            'VE': 5, 'OR': 5, 'HA': 5, 'ME': 5, 'WE': 5, 'IS': 5,
            'AR': 5, 'NS': 5, 'IT': 5, 'RI': 5, 'LI': 5, 'AB': 4,
            'ON': 4, 'ET': 4, 'SI': 4, 'HI': 4, 'EM': 4, 'AS': 4,
            'IG': 4, 'ZU': 4, 'MI': 4, 'NI': 4, 'RU': 4, 'KE': 4,
            'GR': 4, 'KO': 4, 'VO': 4, 'FE': 3, 'RO': 3, 'AG': 3,
            'UR': 3, 'MA': 3, 'TU': 3, 'GA': 3, 'WA': 3, 'WI': 3,
            'SO': 3, 'US': 3, 'AT': 3, 'OD': 3, 'ED': 3, 'TR': 3,
            'NT': 3, 'DU': 3, 'LA': 3, 'FU': 3, 'BR': 3, 'SP': 3,
            'PR': 3, 'PF': 3, 'PL': 3, 'JE': 3, 'JA': 3, 'AE': 3,
            'OE': 3, 'UE': 3, 'EU': 3, 'EE': 2, 'SS': 2, 'FF': 2,
            'LL': 2, 'MM': 2, 'NN': 2, 'TT': 2, 'RR': 2, 'PP': 2,
            'CK': 4, 'EH': 4, 'AH': 3, 'UH': 2, 'OH': 2, 'IH': 2,
        }

        score = 0
        for bi, cnt in list(prev_bigrams.items()) + list(next_bigrams.items()):
            score += german_common_bigrams.get(bi, -1) * cnt

        if score > 0:
            all_bigrams = dict(prev_bigrams)
            all_bigrams.update({f"_{k}": v for k, v in next_bigrams.items()})
            print(f"    {letter}: score={score:3d}  "
                  f"prev_bi={dict(prev_bigrams)}  next_bi={dict(next_bigrams)}")

# === SPECIFIC HYPOTHESES ===
print(f"\n{'='*70}")
print("SPECIFIC HYPOTHESES TO TEST")
print(f"{'='*70}")

# Test specific words that might contain unknowns
# Look for German words in decoded text around unknowns
hypotheses = [
    ('74', 'P', "P is missing from mapping, freq 0.34% matches P=0.79% (rough)"),
    ('74', 'E', "Another E code (most common letter, already has 17 codes)"),
    ('37', 'J', "J is missing, freq 0.14% near J=0.27%"),
    ('37', 'P', "Maybe P split across two codes"),
    ('40', 'P', "Could be P instead"),
    ('40', 'J', "Could be J"),
    ('02', 'Y', "Very rare, freq matches Y=0.04%"),
    ('02', 'X', "Very rare, freq matches X=0.03%"),
]

for code, letter, reason in hypotheses:
    test_map = dict(mapping)
    test_map[code] = letter

    # Decode ALL books with this hypothesis
    total_word_hits = 0
    german_words_big = set([
        'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO', 'DU', 'OB', 'AM', 'IM',
        'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST', 'WIR', 'ICH', 'SIE',
        'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT', 'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI',
        'VOR', 'TAG', 'ORT', 'TOD', 'NIE', 'ALT', 'NEU', 'VOM', 'ZUM', 'ZUR', 'BIS', 'ALS',
        'NUN', 'HIN', 'TUN', 'TUT', 'SEI', 'RAT', 'TAT', 'SAH', 'GAB', 'KAM', 'WAR',
        'NACH', 'AUCH', 'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN', 'DASS', 'WENN', 'DANN',
        'DENN', 'ABER', 'ODER', 'WEIL', 'EINE', 'DIES', 'HIER', 'DORT', 'WELT', 'ZEIT',
        'TEIL', 'WORT', 'NAME', 'GANZ', 'SEHR', 'VIEL', 'FORT', 'HOCH', 'ERDE', 'GOTT',
        'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN', 'HELD', 'ZWEI', 'DREI', 'VIER', 'MEHR',
        'LAND', 'FEST', 'REDE', 'TAGE', 'FREI', 'WAHR', 'VOLK', 'WALD', 'GRAB', 'RUNE',
        'ENDE', 'HAUS', 'NAHM', 'GING', 'LANG', 'KEIN', 'OHNE', 'ALLE', 'WARD', 'BALD',
        'LAUT', 'ERST', 'MUSS', 'WILL', 'SOLL', 'KANN', 'BUCH', 'WEGE', 'SPUR',
        'NICHT', 'DIESE', 'UNTER', 'DURCH', 'GEGEN', 'IMMER', 'KRAFT', 'GEIST', 'NACHT',
        'LICHT', 'KRIEG', 'MACHT', 'STEIN', 'RUNEN', 'HATTE', 'WURDE', 'GROSS', 'KLEIN',
        'ERSTE', 'ALLES', 'KEINE', 'VIELE', 'SCHON', 'STEIL', 'ORTE', 'GEBEN',
        'SENDE', 'SAGEN', 'STATT', 'PLATZ', 'JEDER', 'JEDES', 'JEDEN', 'JEDEM',
        'JETZT', 'WOHER', 'WOHIN', 'WORTE', 'SEITE', 'EINES', 'EINEM', 'EINER', 'EINEN',
        'IHREN', 'STEIG', 'FINDE', 'REDEN', 'FERNE', 'SAGTE',
        'KOENIG', 'STEINE', 'URALTE', 'FINDEN', 'HATTEN', 'WERDEN', 'KOMMEN',
        'SEHEN', 'KENNEN', 'WISSEN', 'MACHEN', 'NEHMEN', 'STEHEN', 'LIEGEN', 'HALTEN',
        'FALLEN', 'ANDERE', 'DIESEM', 'DIESEN', 'DIESER', 'DIESES', 'SEINEN', 'SEINER',
        'HINTER', 'WIEDER', 'NICHTS', 'DUNKEL', 'STIMME', 'HIMMEL', 'ANFANG', 'SPRACH',
        'DARAUF', 'FELSEN', 'TEMPEL', 'ZEICHEN', 'REICHE', 'WELCHE', 'SPRUCH', 'SPRACHE',
        'KRIEGER', 'GEFUNDEN', 'GEBOREN', 'GESEHEN', 'GESCHAFFEN', 'SPRECHEN',
        'WAHRHEIT', 'SCHRIFT', 'VERSCHIEDENE', 'INSCHRIFT',
        'STEINEN', 'URALTEN', 'MEISTER', 'ANDEREN', 'ZWISCHEN',
        'KOENIGREICH', 'ZUSAMMEN', 'GEHEIMNIS',
        'SAGT', 'SAGTEN', 'GEGANGEN', 'FANDEN', 'SAHEN', 'NAHMEN', 'GABEN',
        'KONNTE', 'KONNTEN', 'SOLLTE', 'WOLLTE', 'MUSSTE',
        'REICH', 'REICHEN', 'VOLKES', 'TAGEN', 'WASSER', 'FEUER',
        'LEBEN', 'STERBEN', 'ENDEN', 'TEILE', 'TEILEN', 'SOFORT',
        'SPRACHEN', 'KAMPF', 'OPFER', 'HAUPT', 'GRUPPE',
        'JENE', 'JENER', 'JENES', 'JENEN', 'JEDOCH', 'JENSEITS',
        'JAHR', 'JAHRE', 'JAHREN', 'RUNEORT', 'RUNENSTEIN',
        'ORTEN', 'RUNESTEIN',
    ])

    # Look for recognizable words in each book decoded with this hypothesis
    for pairs in all_pairs_by_book:
        decoded = ''.join(test_map.get(p, '?') for p in pairs)
        for w in german_words_big:
            total_word_hits += decoded.count(w)

    # Baseline
    baseline_hits = 0
    for pairs in all_pairs_by_book:
        decoded = ''.join(mapping.get(p, '?') for p in pairs)
        for w in german_words_big:
            baseline_hits += decoded.count(w)

    delta = total_word_hits - baseline_hits
    print(f"\n  {code}={letter}: {total_word_hits} word hits (baseline: {baseline_hits}, delta: {delta:+d})")
    print(f"    Reason: {reason}")

    # Show affected contexts
    for bi, pairs in enumerate(all_pairs_by_book):
        for pi, p in enumerate(pairs):
            if p == code:
                ctx_pairs = pairs[max(0, pi-5):min(len(pairs), pi+6)]
                ctx = ''.join(test_map.get(x, '?') for x in ctx_pairs)
                pos_in_ctx = sum(1 for x in pairs[max(0,pi-5):pi])
                print(f"    Bk{bi:2d} pos{pi:3d}: {ctx}")

# === REVERSE/ANAGRAM ANALYSIS OF PROPER NOUNS ===
print(f"\n{'='*70}")
print("PROPER NOUN ANALYSIS")
print(f"{'='*70}")

nouns = {
    'LABGZERAS': 'King mentioned in the text',
    'TOTNIURG': 'Appears after KOENIG',
    'SCHWITEIO': 'Appears 10 times, always same encoding',
    'HEARUCHTIGER': 'Place or descriptor (followed by SO DASS)',
    'THARSC': 'Appears after STEINEN',
    'AUNRSONGETRASES': 'Most common unrecognized phrase (11 books)',
}

for noun, desc in nouns.items():
    reversed_n = noun[::-1]
    print(f"\n  {noun}:")
    print(f"    Description: {desc}")
    print(f"    Reversed: {reversed_n}")

    # Check if reversed contains German words
    for w in ['GOTT', 'GRAL', 'BERG', 'BURG', 'LAND', 'STEIN', 'RUINE', 'GRAB',
              'STERN', 'TURN', 'TURM', 'WELT', 'ERDE', 'GRUN', 'TOTEN', 'SARG',
              'GRANT', 'TRUG', 'NATUR', 'GRUEN', 'RUIN', 'REST', 'SARGE']:
        if w in noun or w in reversed_n:
            print(f"    Contains '{w}' in {'original' if w in noun else 'reversed'}")

    # Try splitting into German word components
    print(f"    Possible splits:")
    for split_pos in range(2, len(noun)-1):
        part1 = noun[:split_pos]
        part2 = noun[split_pos:]
        # Check if either part is a German word
        short_dict = {'TOT', 'DER', 'DIE', 'DAS', 'EIN', 'UND', 'IST', 'WIR',
                       'ICH', 'SIE', 'MAN', 'AUS', 'VOR', 'NACH', 'AUCH', 'NOCH',
                       'STEIN', 'RUNE', 'SCHWI', 'ERDE', 'LAND', 'BERG', 'BURG',
                       'GRAB', 'GOTT', 'HERR', 'HELD', 'GOLD', 'SOHN', 'VOLK',
                       'REICH', 'MACHT', 'KRAFT', 'GEIST', 'NACHT', 'LICHT', 'KRIEG',
                       'LAB', 'SERA', 'THAR', 'TEIO', 'NIURG', 'HEARUCHT',
                       'SCHW', 'IGER', 'TIGER', 'SONGE', 'RASES', 'AUNR',
                       'AU', 'NR', 'SON', 'GET', 'RAS', 'SCHWI', 'GZER',
                       'HOER', 'CHER', 'IURE', 'GRUN'}
        note = ''
        if part1 in short_dict or part2 in short_dict:
            note = ' <---'
        if len(part1) >= 3 and len(part2) >= 3:
            print(f"      {part1} + {part2}{note}")

# === CHECK WITH 05=C vs 05=S on AFFECTED WORDS ===
print(f"\n{'='*70}")
print("05=C vs 05=S: DETAILED COMPARISON")
print(f"{'='*70}")

for bi, pairs in enumerate(all_pairs_by_book):
    for pi, p in enumerate(pairs):
        if p == '05':
            # Show wide context with both mappings
            ctx_pairs = pairs[max(0,pi-8):min(len(pairs), pi+9)]
            ctx_C = ''.join(mapping.get(x, '?') if x != '05' else 'C' for x in ctx_pairs)
            ctx_S = ''.join(mapping.get(x, '?') if x != '05' else 'S' for x in ctx_pairs)
            print(f"  Bk{bi:2d} pos{pi:3d}:")
            print(f"    05=C: {ctx_C}")
            print(f"    05=S: {ctx_S}")

            # Check for CH pattern (if next pair is H)
            if pi < len(pairs) - 1:
                next_p = pairs[pi+1]
                next_l = mapping.get(next_p, '?')
                if next_l == 'H':
                    print(f"    *** FOLLOWED BY H: CH vs SH ***")
