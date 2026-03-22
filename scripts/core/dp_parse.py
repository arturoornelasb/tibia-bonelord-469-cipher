"""Dynamic programming word parser for decoded 469 text.
Uses Viterbi-style optimal word segmentation with comprehensive German dictionary."""
import json
from collections import Counter

with open('books.json', 'r') as f:
    books = json.load(f)

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

all_codes = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U',
    '00': 'H', '14': 'N', '72': 'R', '91': 'S', '15': 'I',
    '76': 'E', '52': 'S', '42': 'D', '46': 'I', '48': 'N',
    '57': 'H', '04': 'M', '12': 'S', '58': 'N',
    '78': 'T', '51': 'R', '35': 'A', '34': 'L',
    '01': 'E', '59': 'S', '41': 'E', '30': 'E',
    '94': 'H',
    '47': 'D', '13': 'N', '71': 'I', '63': 'D',
    '93': 'N', '28': 'D', '86': 'E', '43': 'U',
    '70': 'U', '65': 'I', '16': 'I', '36': 'W',
    '64': 'T', '89': 'A', '80': 'G', '97': 'G', '75': 'T',
    '08': 'R', '20': 'F', '96': 'L', '99': 'O', '55': 'R',
    '67': 'E', '27': 'E', '03': 'E', '09': 'E', '05': 'C', '53': 'N',
    '44': 'U', '62': 'B', '68': 'R',
    '23': 'S', '17': 'E', '29': 'E', '66': 'A', '49': 'E',
    '38': 'K', '77': 'Z',
    '22': 'K', '82': 'O', '73': 'N', '50': 'I', '84': 'G',
    '25': 'O', '83': 'V', '81': 'T', '24': 'I',
    '79': 'O', '10': 'R',
}

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# Comprehensive German dictionary — common words plus Tibia lore terms
# Words scored by length (longer = better match = higher score)
german_words = set([
    # Articles, pronouns, prepositions
    'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST',
    'WIR', 'ICH', 'SIE', 'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI', 'VOR', 'FUR',
    'TAG', 'ORT', 'TOD', 'OFT', 'NIE', 'ALT', 'NEU',
    'NACH', 'AUCH', 'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN',
    'DASS', 'WENN', 'DANN', 'DENN', 'ABER', 'ODER', 'WEIL',
    'EINE', 'DIES', 'HIER', 'DORT', 'WELT', 'ZEIT', 'TEIL',
    'WORT', 'NAME', 'GANZ', 'SEHR', 'VIEL', 'FORT', 'HOCH',
    'ERDE', 'GOTT', 'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN',
    'HELD', 'MACHT', 'KRAFT', 'GEIST', 'NACHT', 'LICHT', 'KRIEG',
    # Common verbs
    'HAT', 'WAR', 'HATTE', 'WURDE', 'KANN', 'SOLL', 'WILL', 'MUSS',
    'HABEN', 'WERDEN', 'KOMMEN', 'GEHEN', 'SEHEN', 'FINDEN',
    'KENNEN', 'WISSEN', 'MACHEN', 'SAGEN', 'GEBEN', 'NEHMEN',
    'STEHEN', 'LIEGEN', 'HALTEN', 'FALLEN', 'HELFEN', 'TRAGEN',
    'RUFEN', 'LESEN', 'SCHREIBEN', 'SPRECHEN', 'BRECHEN',
    # Common adjectives/adverbs
    'ALLE', 'ALLES', 'ALLEN', 'KEINE', 'KEINEN', 'VIELE',
    'GROSS', 'KLEIN', 'ERSTE', 'ERSTEN', 'LETZTE', 'LETZTEN',
    'ANDERE', 'ANDEREN', 'ANDERE',
    # Demonstratives, possessives
    'DIESE', 'DIESER', 'DIESES', 'DIESEM', 'DIESEN',
    'SEINE', 'SEINER', 'SEINEN', 'SEINES', 'SEINEM',
    'IHREN', 'IHREM', 'IHRES', 'IHRER',
    'EINEN', 'EINER', 'EINEM', 'EINES',
    # Spatial/directional
    'NORDEN', 'SUEDEN', 'OSTEN', 'WESTEN',
    'GEGEN', 'UNTER', 'DURCH', 'HINTER', 'UEBER', 'ZWISCHEN',
    'IMMER', 'WIEDER', 'SCHON', 'NICHT', 'NICHTS',
    # Tibia lore terms
    'RUNE', 'RUNEN', 'STEIN', 'STEINE', 'STEINEN', 'RUNENSTEIN',
    'ORT', 'ORTE', 'ORTEN', 'RUNEORT',
    'KOENIG', 'KRIEGER', 'MEISTER', 'HERREN',
    'URALTE', 'URALTEN', 'INSCHRIFT',
    'TEMPEL', 'TURM', 'HOEHLE',
    'GEBOREN', 'GESEHEN', 'GEFUNDEN', 'GESCHAFFEN', 'GESCHRIEBEN',
    'VERSCHIEDENE', 'VERSPRECHEN', 'VERSTEHEN',
    'GEHEIMNIS', 'BIBLIOTHEK', 'TAUSEND',
    'ANTWORT',
    # Additional common words
    'DU', 'OB', 'AM', 'IM',
    'VOM', 'ZUM', 'ZUR', 'BIS', 'ALS',
    'NUN', 'NOR', 'HIN',
    'ZWEI', 'DREI', 'VIER', 'FUENF', 'SECHS',
    'MEHR', 'WENIG', 'WENIGE',
    'TAGE', 'TAGEN', 'NACHT', 'NAECHTE',
    'LAND', 'WASSER', 'FEUER',
    'MACHT', 'MAECHTIGER', 'MAECHTIG',
    'LEBEN', 'STERBEN', 'ENDE',
    'KLAR', 'WAHR', 'RECHT',
    'TEILE', 'TEILEN',
    'WORTE', 'WORTEN',
    'SOFORT',
    'ZUSAMMEN',
    'DUNKEL', 'DUNKELHEIT',
    'ERDEN',
    'GESCHAFFEN',
    'MACHEN', 'GEMACHT',
    'HIMMEL',
    'STIMME', 'STIMMEN',
    'SCHNELL',
    'KAPITEL',
    'VERSCHIEDEN',
    'UEBER', 'HINAUS',
    'UEBERALL',
    # Additional verb forms
    'SAGT', 'SAGTE', 'SAGTEN',
    'GING', 'GINGEN', 'GEGANGEN',
    'KAM', 'KAMEN', 'GEKOMMEN',
    'FAND', 'FANDEN',
    'SAH', 'SAHEN',
    'NAHM', 'NAHMEN',
    'GAB', 'GABEN', 'GEGEBEN',
    'LIESS', 'LIESSEN',
    'BRACHTE', 'BRACHTEN',
    'WUSSTE', 'WUSSTEN',
    'KONNTE', 'KONNTEN',
    'SOLLTE', 'SOLLTEN',
    'WOLLTE', 'WOLLTEN',
    'MUSSTE', 'MUSSTEN',
    # Noun forms
    'STEINE', 'STEINEN', 'STEINES',
    'ORTES',
    'REICHES', 'REICH', 'REICHE', 'REICHEN',
    'VOLKES', 'VOLK', 'VOELKER',
    'KOENIGREICH', 'KOENIGREICHE',
    'SCHRIFT', 'SCHRIFTEN',
    'ZEICHEN',
    'WAHRHEIT',
    # Prepositions/conjunctions
    'FUER', 'OHNE', 'NEBEN',
    'BEVOR', 'NACHDEM', 'WAEHREND',
    'OBWOHL', 'JEDOCH', 'TROTZDEM',
    # Test words for the mystery patterns
    'RUNESTEIN', 'RUNENSTEIN',
    'TOTENREICH', 'TOTNIURG',  # Leave mystery term in case it IS a word
])

# Build word set for quick lookup
word_set = german_words

# DP parse: maximize total characters covered by words
def dp_parse(text):
    n = len(text)
    # dp[i] = (max_covered, backpointer)
    # max_covered = maximum characters covered by words in text[:i]
    dp = [(0, None)] * (n + 1)  # (score, (start, word))

    for i in range(1, n + 1):
        # Option 1: character i-1 is unmatched
        dp[i] = (dp[i-1][0], None)

        # Option 2: a word ends at position i
        max_word_len = min(i, 15)
        for wlen in range(2, max_word_len + 1):
            start = i - wlen
            candidate = text[start:i]
            if '?' in candidate:
                continue
            if candidate in word_set:
                # Score: previous + word length (prefer longer words)
                score = dp[start][0] + wlen
                if score > dp[i][0]:
                    dp[i] = (score, (start, candidate))

    # Backtrack
    tokens = []
    i = n
    while i > 0:
        if dp[i][1] is not None:
            start, word = dp[i][1]
            # Add unmatched chars between this word and the previous
            if i > start + len(word):
                gap = text[start + len(word):i]
                # This shouldn't happen in correct backtracking
                pass
            tokens.append(('WORD', word))
            # Check for gap before this word
            next_end = start
            # Collect unmatched chars up to start
            gap_start = next_end
            i = start
        else:
            tokens.append(('CHAR', text[i-1]))
            i -= 1

    tokens.reverse()

    # Merge consecutive CHAR tokens
    merged = []
    for kind, val in tokens:
        if kind == 'WORD':
            merged.append(val)
        else:
            if merged and merged[-1].islower():
                merged[-1] += val.lower()
            else:
                merged.append(val.lower())

    return merged, dp[n][0]

# Apply to the longest books
print("=" * 80)
print("DYNAMIC PROGRAMMING WORD PARSE — Optimal German word segmentation")
print("=" * 80)

total_chars = 0
total_covered = 0
word_counts = Counter()

for idx, bpairs in enumerate(book_pairs):
    if len(bpairs) < 60:
        continue

    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    tokens, covered = dp_parse(text)
    known = sum(1 for c in text if c != '?')
    total_chars += known
    total_covered += covered

    # Count words
    for t in tokens:
        if t.isupper() and len(t) >= 3:
            word_counts[t] += 1

    parsed = ' '.join(tokens)

    print(f"\nBook {idx} ({len(bpairs)} pairs, {covered}/{known} chars in words = {covered/max(known,1)*100:.0f}%):")
    for j in range(0, len(parsed), 120):
        print(f"  {parsed[j:j+120]}")

print(f"\n{'='*80}")
print(f"TOTAL: {total_covered}/{total_chars} chars in words = {total_covered/max(total_chars,1)*100:.1f}%")
print(f"{'='*80}")

print(f"\nTop 40 words found:")
for word, count in word_counts.most_common(40):
    print(f"  {word}: {count}")

# Focus on the HEARUCHTIG context
print(f"\n{'='*80}")
print("CONTEXT ANALYSIS: What surrounds HEARUCHTIG?")
print("=" * 80)

# Get the full text around HEARUCHTIG with best word parse
for idx, bpairs in enumerate(book_pairs):
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    pos = text.find('HEARUCHTIG')
    if pos == -1:
        continue

    # Get wide context
    ctx_start = max(0, pos - 30)
    ctx_end = min(len(text), pos + 40)
    ctx = text[ctx_start:ctx_end]

    tokens, _ = dp_parse(ctx)
    parsed = ' '.join(tokens)
    print(f"\n  Bk{idx}: {parsed}")
    break  # One example is enough since they're all identical

# Analyze the AUNRSON pattern
print(f"\n{'='*80}")
print("CONTEXT ANALYSIS: What surrounds GETRASES?")
print("=" * 80)

for idx, bpairs in enumerate(book_pairs):
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    pos = text.find('GETRASE')
    if pos == -1:
        continue
    ctx_start = max(0, pos - 30)
    ctx_end = min(len(text), pos + 30)
    ctx = text[ctx_start:ctx_end]
    tokens, _ = dp_parse(ctx)
    parsed = ' '.join(tokens)
    print(f"\n  Bk{idx}: {parsed}")
    if idx > 25:
        break

# Analyze the TOTNIURG context
print(f"\n{'='*80}")
print("CONTEXT ANALYSIS: What surrounds TOTNIURG?")
print("=" * 80)

for idx, bpairs in enumerate(book_pairs):
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    pos = text.find('TOTNIURG')
    if pos == -1:
        continue
    ctx_start = max(0, pos - 30)
    ctx_end = min(len(text), pos + 30)
    ctx = text[ctx_start:ctx_end]
    tokens, _ = dp_parse(ctx)
    parsed = ' '.join(tokens)
    print(f"\n  Bk{idx}: {parsed}")
    if idx > 30:
        break
