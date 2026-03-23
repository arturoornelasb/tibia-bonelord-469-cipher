"""
Comprehensive attack on the Bonelord 469 cipher.
Multi-pronged approach:
1. Apply code 05=S hypothesis
2. Systematically test all unknown codes (74, 37, 40, 02, 33, 69)
3. Context analysis around each unknown code occurrence
4. DP word segmentation with expanded German dictionary
5. Produce best possible full decode
"""
import json
import os
from collections import Counter
from itertools import product

# Load books
data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)

# === MAPPING ===
# Tier 14 mapping (92 codes) - the established mapping
all_codes = {
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
    '09': 'E', '05': 'C', '53': 'N', '44': 'U', '62': 'B',
    '68': 'R', '23': 'S', '17': 'E', '29': 'E', '66': 'A',
    '49': 'E', '38': 'K', '77': 'Z', '22': 'K', '82': 'O',
    '73': 'N', '50': 'I', '84': 'G', '25': 'O', '83': 'V',
    '81': 'T', '24': 'I', '79': 'O', '10': 'R', '54': 'M',
    '98': 'T', '39': 'E', '87': 'W',
}

# === IC-BASED OFFSET DETECTION ===
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

# === SUPERSTRING ASSEMBLY ===
def find_overlap(a, b, min_len=4):
    max_overlap = min(len(a), len(b))
    for length in range(max_overlap, min_len - 1, -1):
        if length % 2 != 0:
            continue
        if a[-length:] == b[:length]:
            return length
    return 0

def build_superstring(book_list):
    """Build superstring from raw digit strings using greedy overlap."""
    n = len(book_list)
    # Check containment
    contained = set()
    for i in range(n):
        for j in range(n):
            if i != j and book_list[i] in book_list[j]:
                contained.add(i)

    unique_idx = [i for i in range(n) if i not in contained]
    unique = [book_list[i] for i in unique_idx]

    used = [False] * len(unique)
    fragments = []

    while True:
        unused = [i for i in range(len(unique)) if not used[i]]
        if not unused:
            break
        start = max(unused, key=lambda i: len(unique[i]))
        current = unique[start]
        used[start] = True

        changed = True
        while changed:
            changed = False
            best_ov, best_idx, best_dir = 0, -1, None
            for i in [x for x in range(len(unique)) if not used[x]]:
                ov_right = find_overlap(current, unique[i])
                ov_left = find_overlap(unique[i], current)
                if ov_right > best_ov:
                    best_ov, best_idx, best_dir = ov_right, i, 'right'
                if ov_left > best_ov:
                    best_ov, best_idx, best_dir = ov_left, i, 'left'
            if best_idx >= 0 and best_ov >= 4:
                if best_dir == 'right':
                    current = current + unique[best_idx][best_ov:]
                else:
                    current = unique[best_idx] + current[best_ov:]
                used[best_idx] = True
                changed = True

        fragments.append(current)

    return fragments

# === GERMAN DICTIONARY ===
german_words = set([
    # 2-letter
    'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO', 'DU', 'OB', 'AM', 'IM',
    # 3-letter
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST', 'WIR', 'ICH', 'SIE',
    'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT', 'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI',
    'VOR', 'FUR', 'TAG', 'ORT', 'TOD', 'OFT', 'NIE', 'ALT', 'NEU', 'VOM', 'ZUM', 'ZUR',
    'BIS', 'ALS', 'NUN', 'HIN', 'TUN', 'TUT', 'SAH', 'GAB', 'KAM', 'WAR', 'SEI', 'HAB',
    'RUF', 'RAT', 'TAT',
    # 4-letter
    'NACH', 'AUCH', 'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN', 'DASS', 'WENN', 'DANN',
    'DENN', 'ABER', 'ODER', 'WEIL', 'EINE', 'DIES', 'HIER', 'DORT', 'WELT', 'ZEIT',
    'TEIL', 'WORT', 'NAME', 'GANZ', 'SEHR', 'VIEL', 'FORT', 'HOCH', 'ERDE', 'GOTT',
    'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN', 'HELD', 'ZWEI', 'DREI', 'VIER', 'MEHR',
    'LAND', 'FEST', 'REDE', 'TAGE', 'RUHE', 'FERN', 'FREI', 'WAHR', 'VOLK', 'KLAR',
    'TIEF', 'STEG', 'WAND', 'RAND', 'RUND', 'GALT', 'BAND', 'WALD', 'GRAB', 'MORD',
    'BUCH', 'WEGE', 'SPUR', 'RUNE', 'ENDE', 'HAUS', 'NAHM', 'GING', 'WOHL', 'DRAN',
    'LANG', 'KEIN', 'OHNE', 'ALLE', 'IHRE', 'WARD', 'BEIM', 'KAUM', 'DRUM', 'KALT',
    'HALB', 'BALD', 'LAUT', 'ERST', 'RAUM', 'MUSS', 'WILL', 'SOLL', 'KANN', 'DARF',
    'STEIN', 'ORTEN',  # 5-letter but important
    # 5-letter
    'NICHT', 'DIESE', 'UNTER', 'DURCH', 'GEGEN', 'IMMER', 'REDEN', 'SAGTE', 'STEIL',
    'FINDE', 'ORTE', 'KRAFT', 'GEIST', 'NACHT', 'LICHT', 'KRIEG', 'MACHT', 'STEIN',
    'RUNEN', 'HATTE', 'WURDE', 'GROSS', 'KLEIN', 'ERSTE', 'ALLES', 'ALLEN', 'KEINE',
    'VIELE', 'SCHON', 'KOMMT', 'FEHLT', 'STEHT', 'LIEGT', 'REDEN', 'FERNE', 'STEHE',
    'GEBEN', 'GEBET', 'SENDE', 'SAGEN', 'TATEN', 'STIMM', 'STATT', 'PLATZ', 'JEDEN',
    'JEDER', 'JEDES', 'JEDEM', 'KEINE', 'KAMEN', 'FANDEN', 'JENEN', 'HEISST',
    'WOHER', 'WOHIN', 'WORIN', 'WORAN', 'DARAUS', 'WORTE', 'WORTEN', 'SEITE',
    'EINES', 'EINEM', 'EINER', 'EINEN', 'STEIL', 'IHREN', 'STEIG', 'FINDET',
    # 6-letter
    'KOENIG', 'STEINE', 'URALTE', 'FINDEN', 'HATTEN', 'WERDEN', 'KOMMEN', 'GEHEN',
    'SEHEN', 'KENNEN', 'WISSEN', 'MACHEN', 'NEHMEN', 'STEHEN', 'LIEGEN', 'HALTEN',
    'FALLEN', 'HELFEN', 'TRAGEN', 'ANDERE', 'DIESEM', 'DIESEN', 'DIESER', 'DIESES',
    'SEINEN', 'SEINER', 'SEINES', 'SEINEM', 'HINTER', 'WIEDER', 'NICHTS', 'DUNKEL',
    'NORDEN', 'SUEDEN', 'OSTEN', 'WESTEN', 'STIMME', 'HIMMEL', 'ANFANG', 'SPRACH',
    'STEINEN', 'GEGEBEN', 'DARAUF', 'DARAUS', 'FELSEN', 'GRABEN', 'TEMPEL',
    'ZEICHEN', 'REICHE', 'WELCHE', 'WELCHER', 'MANCHES', 'MANCHE', 'SOLCHE',
    'INSELN', 'SPRUCH', 'SPRACHE', 'GEHEIM', 'KRIEGER',
    # 7-letter
    'STEINEN', 'URALTEN', 'KRIEGER', 'MEISTER', 'ANDEREN', 'ZWISCHEN',
    'GEFUNDEN', 'GEBOREN', 'GESEHEN', 'GESCHAFFEN', 'SCHREIBEN', 'SPRECHEN',
    'BRECHEN', 'WAHRHEIT', 'KAPITEL', 'SCHNELL', 'VERSCHIEDENE', 'INSCHRIFT',
    'SCHRIFT', 'SCHRIFTEN', 'KOENIGIN', 'KOENIGREICH', 'ZUSAMMEN', 'DARUEBER',
    'VERSCHIEDEN', 'VERSPRECHEN', 'VERSTEHEN', 'GEHEIMNIS', 'MAECHTIGER',
    'ZURUECK', 'VERFLUCHT',
    # Verb forms important for this text
    'SAGT', 'SAGTE', 'SAGTEN', 'GING', 'GINGEN', 'GEGANGEN', 'FAND', 'FANDEN',
    'SAH', 'SAHEN', 'NAHM', 'NAHMEN', 'GAB', 'GABEN', 'LIESS', 'LIESSEN',
    'BRACHTE', 'BRACHTEN', 'WUSSTE', 'WUSSTEN', 'KONNTE', 'KONNTEN',
    'SOLLTE', 'SOLLTEN', 'WOLLTE', 'WOLLTEN', 'MUSSTE', 'MUSSTEN',
    # Noun forms relevant to the narrative
    'REICH', 'REICHE', 'REICHEN', 'REICHES', 'VOLKES', 'KOENIGREICHE',
    'SCHRIFT', 'SCHRIFTEN', 'TAGEN', 'NAECHTE', 'WASSER', 'FEUER',
    'LEBEN', 'STERBEN', 'ERDEN', 'ENDEN', 'ENDER', 'SENDEN', 'SENDER',
    'WENDIG', 'WENIGE', 'TEILE', 'TEILEN', 'SOFORT', 'WORTE',
    # Archaic/medieval German
    'DERER', 'DESSEN', 'DENEN', 'WELCH', 'SOLCH', 'MANCH', 'JENE', 'JENER',
    'JENES', 'JENEN', 'JENEM', 'DAHER', 'DAHIN', 'DARUM', 'DAVON', 'DARAN',
    'DABEI', 'HIERZU', 'WOZU', 'WOFUER',
    'VERFLUCHTEN', 'ZERSTOERT', 'VERNICHTET', 'ERSCHAFFEN', 'VERBORGEN',
    'GESTORBEN', 'ERRICHTET', 'VERFALLEN', 'VERGESSEN',
    # Compound word components
    'RUNE', 'RUNEN', 'RUNENSTEIN', 'RUNEORT',
    'STEIN', 'STEINE', 'STEINEN', 'STEINES',
    'GRAB', 'GRABEN', 'GRAEBER',
    'TURM', 'TUERME', 'HOEHLE',
    'MAUER', 'MAUERN',
    'SPRUCH', 'SPRUECHE',
    'SCHATZ', 'SCHAETZE',
    'STAB', 'STAEBE',
    # P-words (testing 74=P hypothesis)
    'PLATZ', 'PLATZE', 'PLATZEN',
    'PREIS', 'PREISE',
    'SPRACH', 'SPRECHEN', 'GESPROCHEN',
    'SPRICHT', 'SPRACHE', 'SPRACHEN',
    'KAMPF', 'KAEMPFE', 'KAEMPFEN',
    'OPFER', 'EMPFANG',
    'TEMPEL', 'GRUPPE',
    'BEISPIEL', 'HAUPT', 'HAUPTSTADT',
    'PROPHEZEIT', 'PROPHEZEIUNG',
    # J-words (testing 37=J hypothesis)
    'JETZT', 'JENE', 'JENER', 'JENES', 'JENEN', 'JENEM',
    'JEDER', 'JEDES', 'JEDEM', 'JEDEN', 'JEDOCH',
    'JAHR', 'JAHRE', 'JAHREN', 'JAHRHUNDERT',
    'JAGD', 'JEMAND', 'JENSEITS',
])

# === DP WORD PARSER ===
def dp_parse(text, word_set):
    """Viterbi-style DP segmentation. Returns (words, score, coverage)."""
    n = len(text)
    # dp[i] = (best_score, best_split_point) for text[:i]
    dp = [(0, -1)] * (n + 1)

    for i in range(1, n + 1):
        dp[i] = dp[i-1]  # default: skip this char
        for wlen in range(2, min(i, 20) + 1):
            word = text[i-wlen:i]
            if word in word_set:
                # Score: longer words worth more (quadratic bonus)
                score = wlen * wlen
                new_score = dp[i-wlen][0] + score
                if new_score > dp[i][0]:
                    dp[i] = (new_score, i - wlen)

    # Backtrack to find words
    words = []
    pos = n
    while pos > 0:
        prev = dp[pos][1]
        if prev >= 0 and prev != pos - 1:
            # Check if it's actually a word
            w = text[prev:pos]
            if w in word_set:
                words.append((prev, w))
                pos = prev
                continue
        pos -= 1

    words.reverse()
    total_covered = sum(len(w) for _, w in words)
    return words, dp[n][0], total_covered

# === DECODE FUNCTION ===
def decode_pairs(pairs, mapping):
    """Decode a list of 2-digit code pairs using the given mapping."""
    result = []
    for p in pairs:
        letter = mapping.get(p)
        if letter:
            result.append(letter)
        else:
            result.append('?')
    return ''.join(result)

# === BUILD SUPERSTRING ===
print("=" * 80)
print("COMPREHENSIVE ATTACK ON THE BONELORD 469 CIPHER")
print("=" * 80)

print("\n[1] Building raw-digit superstring...")
fragments = build_superstring(books)
fragments.sort(key=len, reverse=True)
print(f"    {len(fragments)} fragments assembled")
for i, f in enumerate(fragments[:5]):
    print(f"    Fragment {i}: {len(f)} digits ({len(f)//2} codes)")

# Use the main fragment for analysis
main_raw = fragments[0]
print(f"\n    Main fragment: {len(main_raw)} digits = {len(main_raw)//2} code pairs")

# Decode the main fragment
main_offset = get_offset(main_raw)
main_pairs = [main_raw[j:j+2] for j in range(main_offset, len(main_raw)-1, 2)]
print(f"    Offset: {main_offset}, Pairs: {len(main_pairs)}")

# === ANALYZE UNKNOWN CODES ===
print("\n" + "=" * 80)
print("[2] UNKNOWN CODE ANALYSIS")
print("=" * 80)

# Count all unknown codes across all books
all_pairs_flat = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    all_pairs_flat.extend(pairs)

unknown_counter = Counter()
for p in all_pairs_flat:
    if p not in all_codes:
        unknown_counter[p] += 1

print(f"\nTotal pairs across all books: {len(all_pairs_flat)}")
print(f"Unknown codes:")
for code, cnt in unknown_counter.most_common():
    pct = cnt / len(all_pairs_flat) * 100
    print(f"  Code {code}: {cnt} occurrences ({pct:.2f}%)")

# Also count in the main superstring
unknown_in_main = Counter()
for p in main_pairs:
    if p not in all_codes:
        unknown_in_main[p] += 1

print(f"\nIn main superstring ({len(main_pairs)} pairs):")
for code, cnt in unknown_in_main.most_common():
    print(f"  Code {code}: {cnt}")

# === CONTEXT ANALYSIS FOR EACH UNKNOWN CODE ===
print("\n" + "=" * 80)
print("[3] CONTEXT ANALYSIS (letters surrounding each unknown code)")
print("=" * 80)

def get_context(pairs, mapping, target_code, window=5):
    """Get decoded context around each occurrence of target_code."""
    contexts = []
    for i, p in enumerate(pairs):
        if p == target_code:
            before = []
            after = []
            for j in range(max(0, i-window), i):
                before.append(mapping.get(pairs[j], '?'))
            for j in range(i+1, min(len(pairs), i+window+1)):
                after.append(mapping.get(pairs[j], '?'))
            contexts.append((''.join(before), ''.join(after), i))
    return contexts

for code, cnt in unknown_counter.most_common():
    if cnt == 0:
        continue
    print(f"\n--- Code {code} ({cnt} occurrences) ---")
    contexts = get_context(main_pairs, all_codes, code)
    for before, after, pos in contexts[:15]:
        print(f"  pos {pos:4d}: ...{before}[{code}]{after}...")

# === TEST 05=S HYPOTHESIS ===
print("\n" + "=" * 80)
print("[4] TESTING CODE 05=S HYPOTHESIS")
print("=" * 80)

mapping_05C = dict(all_codes)  # current: 05=C
mapping_05S = dict(all_codes)
mapping_05S['05'] = 'S'

decoded_05C = decode_pairs(main_pairs, mapping_05C)
decoded_05S = decode_pairs(main_pairs, mapping_05S)

words_C, score_C, cov_C = dp_parse(decoded_05C, german_words)
words_S, score_S, cov_S = dp_parse(decoded_05S, german_words)

print(f"\n05=C: {len(words_C)} words, score={score_C}, coverage={cov_C}/{len(decoded_05C)} ({cov_C/len(decoded_05C)*100:.1f}%)")
print(f"05=S: {len(words_S)} words, score={score_S}, coverage={cov_S}/{len(decoded_05S)} ({cov_S/len(decoded_05S)*100:.1f}%)")
print(f"Delta: {len(words_S)-len(words_C):+d} words, {score_S-score_C:+d} score, {cov_S-cov_C:+d} chars")

# Show words unique to 05=S
words_C_set = set(w for _, w in words_C)
words_S_set = set(w for _, w in words_S)
new_words = words_S_set - words_C_set
lost_words = words_C_set - words_S_set
if new_words:
    print(f"\nNew words gained with 05=S: {sorted(new_words)}")
if lost_words:
    print(f"Words lost with 05=S: {sorted(lost_words)}")

# Show contexts where 05 appears
print("\nContexts with 05=S applied:")
for i, p in enumerate(main_pairs):
    if p == '05':
        before = decode_pairs(main_pairs[max(0,i-6):i], mapping_05S)
        after = decode_pairs(main_pairs[i+1:min(len(main_pairs),i+7)], mapping_05S)
        print(f"  pos {i}: ...{before}[S]{after}...")

# === USE 05=S AS BASE ===
base_mapping = dict(all_codes)
base_mapping['05'] = 'S'  # Apply the hypothesis

# === SYSTEMATIC TEST OF UNKNOWN CODES ===
print("\n" + "=" * 80)
print("[5] SYSTEMATIC TESTING OF UNKNOWN CODES")
print("=" * 80)

# German letter frequencies for reference
german_freq = {
    'E': 16.93, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
    'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
    'L': 3.44, 'C': 3.06, 'G': 3.01, 'M': 2.53, 'O': 2.51,
    'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
    'P': 0.79, 'V': 0.67, 'J': 0.27, 'Y': 0.04, 'X': 0.03, 'Q': 0.02,
}

# Letters to test for each unknown code
test_letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

# German bigram frequencies (top pairs)
good_bigrams = set([
    'EN', 'ER', 'CH', 'DE', 'EI', 'ND', 'TE', 'IN', 'IE', 'GE',
    'ES', 'NE', 'UN', 'ST', 'RE', 'HE', 'AN', 'BE', 'SE', 'DI',
    'DA', 'AU', 'AL', 'LE', 'SC', 'RA', 'EL', 'NG', 'IC', 'TI',
    'VE', 'OR', 'HA', 'ME', 'WE', 'IS', 'AR', 'NS', 'IT', 'RI',
    'LI', 'SS', 'AB', 'ON', 'ET', 'SI', 'HI', 'EM', 'AS', 'IG',
    'ZU', 'MI', 'NI', 'RU', 'KE', 'GR', 'KO', 'VO', 'FE', 'RO',
    'AG', 'UR', 'MA', 'TU', 'GA', 'WA', 'WI', 'SO', 'US', 'AT',
    'OD', 'ED', 'TR', 'NT', 'DU', 'LA', 'FU', 'BR', 'SP', 'PR',
    'PF', 'PL', 'JE', 'JA',
])

# Bad bigrams (very unlikely in German)
bad_bigrams = set([
    'QQ', 'XX', 'YY', 'QX', 'XQ', 'QZ', 'ZQ', 'BX', 'XB',
    'QA', 'QE', 'QI', 'QO', 'CQ', 'QP', 'PQ',
])

def bigram_score(text):
    """Score text by quality of bigrams."""
    score = 0
    for i in range(len(text) - 1):
        bi = text[i:i+2]
        if '?' in bi:
            continue
        if bi in good_bigrams:
            score += 2
        elif bi in bad_bigrams:
            score -= 5
    return score

# Test each unknown code with each possible letter
for code, cnt in unknown_counter.most_common():
    if cnt == 0:
        continue

    print(f"\n{'='*60}")
    print(f"Testing code {code} ({cnt} occurrences)")
    print(f"{'='*60}")

    # Expected frequency
    code_pct = cnt / len(all_pairs_flat) * 100
    print(f"Frequency: {code_pct:.2f}%")
    print(f"Best frequency matches:")
    freq_matches = sorted(german_freq.items(), key=lambda x: abs(x[1] - code_pct))[:5]
    for letter, freq in freq_matches:
        print(f"  {letter}: {freq:.2f}% (delta: {abs(freq-code_pct):.2f}%)")

    results = []
    for letter in test_letters:
        test_map = dict(base_mapping)
        test_map[code] = letter
        decoded = decode_pairs(main_pairs, test_map)

        # Score 1: DP word parse
        words, dp_score, coverage = dp_parse(decoded, german_words)

        # Score 2: Bigram quality
        bi_score = bigram_score(decoded)

        # Combined score
        combined = dp_score + bi_score

        results.append((letter, len(words), dp_score, bi_score, combined, coverage, words))

    # Sort by combined score
    results.sort(key=lambda x: -x[4])

    # Baseline (without this code assigned)
    baseline_decoded = decode_pairs(main_pairs, base_mapping)
    baseline_words, baseline_dp, baseline_cov = dp_parse(baseline_decoded, german_words)
    baseline_bi = bigram_score(baseline_decoded)

    print(f"\nBaseline (code {code}=?): {len(baseline_words)} words, dp={baseline_dp}, bi={baseline_bi}, cov={baseline_cov}")
    print(f"\nTop 10 letter assignments:")
    print(f"{'Letter':>6} {'Words':>6} {'DP':>6} {'Bigram':>7} {'Combined':>9} {'Coverage':>9} {'Delta':>7}")
    for letter, nw, dps, bis, comb, cov, _ in results[:10]:
        delta = comb - (baseline_dp + baseline_bi)
        print(f"  {letter:>4}  {nw:>5}  {dps:>5}  {bis:>6}  {comb:>8}  {cov:>8}  {delta:>+6}")

    # Show context with best assignment
    best_letter = results[0][0]
    best_words = results[0][6]
    print(f"\nBest: {code}={best_letter}")
    print(f"New words with {code}={best_letter}:")
    best_word_set = set(w for _, w in best_words)
    base_word_set = set(w for _, w in baseline_words)
    new_w = best_word_set - base_word_set
    for w in sorted(new_w):
        print(f"  {w}")

# === BEST COMBINED ASSIGNMENT ===
print("\n" + "=" * 80)
print("[6] OPTIMIZED COMBINED ASSIGNMENT")
print("=" * 80)

# Get the best letter for each unknown code individually
best_individual = {}
for code, cnt in unknown_counter.most_common():
    if cnt < 2:  # Skip codes with only 1 occurrence
        continue

    best_score = -999999
    best_letter = '?'
    for letter in test_letters:
        test_map = dict(base_mapping)
        test_map[code] = letter
        decoded = decode_pairs(main_pairs, test_map)
        words, dp_score, coverage = dp_parse(decoded, german_words)
        bi_score = bigram_score(decoded)
        combined = dp_score + bi_score
        if combined > best_score:
            best_score = combined
            best_letter = letter
    best_individual[code] = best_letter

print("\nBest individual assignments:")
for code, letter in sorted(best_individual.items()):
    print(f"  Code {code} = {letter}")

# Apply all best assignments together
final_mapping = dict(base_mapping)
for code, letter in best_individual.items():
    final_mapping[code] = letter
# Also assign single-occurrence codes their best letter
for code, cnt in unknown_counter.most_common():
    if cnt == 1 and code not in final_mapping:
        best_score = -999999
        best_letter = '?'
        for letter in test_letters:
            test_map = dict(final_mapping)
            test_map[code] = letter
            decoded = decode_pairs(main_pairs, test_map)
            words, dp_score, coverage = dp_parse(decoded, german_words)
            bi_score = bigram_score(decoded)
            combined = dp_score + bi_score
            if combined > best_score:
                best_score = combined
                best_letter = letter
        final_mapping[code] = best_letter

print(f"\nFinal mapping: {len(final_mapping)} codes assigned")

# === FULL DECODE ===
print("\n" + "=" * 80)
print("[7] FULL DECODED TEXT (main fragment)")
print("=" * 80)

final_decoded = decode_pairs(main_pairs, final_mapping)
words, score, coverage = dp_parse(final_decoded, german_words)

print(f"\nTotal length: {len(final_decoded)} characters")
print(f"Words found: {len(words)}")
print(f"Coverage: {coverage}/{len(final_decoded)} ({coverage/len(final_decoded)*100:.1f}%)")
print(f"DP score: {score}")

# Print with word boundaries marked
print(f"\n--- Decoded text with word boundaries ---")
# Mark word positions
word_starts = set()
word_ends = set()
for pos, w in words:
    word_starts.add(pos)
    word_ends.add(pos + len(w))

# Print in chunks of 80 chars with word markers
chunk_size = 80
for start in range(0, len(final_decoded), chunk_size):
    chunk = final_decoded[start:start+chunk_size]
    # Build word-boundary line
    boundary = ''
    for i in range(start, min(start + chunk_size, len(final_decoded))):
        if i in word_starts:
            boundary += '|'
        elif i in word_ends:
            boundary += '|'
        else:
            boundary += ' '
    print(f"  {start:4d}: {chunk}")
    # Find words in this chunk
    chunk_words = [(p-start, w) for p, w in words if start <= p < start + chunk_size]
    if chunk_words:
        word_line = ' ' * 8
        for p, w in chunk_words:
            word_line += f"[{w}]"
            padding = p + len(w) - len(word_line) + 8
            if padding > 0:
                word_line += ' ' * padding
        # Just list the words
        wlist = ' '.join(w for _, w in chunk_words)
        print(f"        -> {wlist}")

# === WORD FREQUENCY ===
print(f"\n--- Most common words ---")
word_counter = Counter(w for _, w in words)
for w, cnt in word_counter.most_common(30):
    print(f"  {w}: {cnt}")

# === DECODE ALL FRAGMENTS ===
print(f"\n" + "=" * 80)
print("[8] ALL FRAGMENTS DECODED")
print("=" * 80)

for fi, frag in enumerate(fragments):
    foff = get_offset(frag)
    fpairs = [frag[j:j+2] for j in range(foff, len(frag)-1, 2)]
    fdecoded = decode_pairs(fpairs, final_mapping)
    fwords, fscore, fcov = dp_parse(fdecoded, german_words)
    print(f"\nFragment {fi} ({len(fdecoded)} chars, {len(fwords)} words, {fcov/len(fdecoded)*100:.0f}% coverage):")
    print(f"  {fdecoded[:200]}...")
    if fwords:
        print(f"  Words: {' '.join(w for _, w in fwords[:20])}")

# === NARRATIVE EXTRACTION ===
print(f"\n" + "=" * 80)
print("[9] NARRATIVE ANALYSIS")
print("=" * 80)

# Look for key patterns in the decoded text
patterns = [
    'KOENIG', 'STEIN', 'STEINE', 'STEINEN', 'URALTE', 'RUNE', 'RUNEN',
    'ENDE', 'REDE', 'FINDEN', 'HIER', 'DORT', 'REICH', 'MACHT',
    'KRIEGER', 'MEISTER', 'NACHT', 'LICHT', 'DUNKEL', 'GEIST',
    'SPRACH', 'SAGTE', 'SCHRIFT', 'ZEICHEN', 'GRAB', 'TURM',
    'TEMPEL', 'WASSER', 'FEUER', 'ERDE', 'HIMMEL', 'GOTT',
    'KAMPF', 'KRIEG', 'VOLK', 'LAND', 'PLATZ', 'JETZT',
    'SCHWITEIO', 'LABGZERAS', 'TOTNIURG', 'HEARUCHTIGER',
]

print("\nKey pattern occurrences:")
for pattern in patterns:
    count = final_decoded.count(pattern)
    if count > 0:
        print(f"  {pattern}: {count} times")
        # Show context for first 3
        idx = 0
        shown = 0
        while shown < 3 and idx < len(final_decoded):
            pos = final_decoded.find(pattern, idx)
            if pos < 0:
                break
            ctx_start = max(0, pos - 10)
            ctx_end = min(len(final_decoded), pos + len(pattern) + 10)
            ctx = final_decoded[ctx_start:ctx_end]
            marker = '.' * (pos - ctx_start) + pattern + '.' * (ctx_end - pos - len(pattern))
            print(f"    pos {pos}: ...{ctx}...")
            idx = pos + 1
            shown += 1

# === MAPPING COMPARISON ===
print(f"\n" + "=" * 80)
print("[10] FINAL MAPPING CHANGES")
print("=" * 80)

print("\nChanges from original Tier 14 mapping:")
for code in sorted(final_mapping.keys()):
    orig = all_codes.get(code)
    new = final_mapping[code]
    if orig is None:
        print(f"  Code {code}: ? -> {new} (NEW)")
    elif orig != new:
        print(f"  Code {code}: {orig} -> {new} (CHANGED)")

# Save the final mapping
output_path = os.path.join(data_dir, 'final_mapping.json')
with open(output_path, 'w') as f:
    json.dump(final_mapping, f, indent=2, sort_keys=True)
print(f"\nFinal mapping saved to {output_path}")
