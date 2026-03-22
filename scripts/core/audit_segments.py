"""For each unrecognized segment, check if any single code reassignment
would create German words — this tests for misassigned codes."""
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

word_dict = set([
    'AB', 'AM', 'AN', 'DA', 'DU', 'ER', 'ES', 'IM', 'IN', 'JA', 'OB', 'SO',
    'UM', 'WO', 'ZU',
    'ALS', 'AUF', 'AUS', 'BEI', 'BIS', 'DAS', 'DEM', 'DEN', 'DER', 'DES',
    'DIE', 'DIR', 'EIN', 'FUR', 'GAB', 'GUT', 'HAT', 'HIN', 'ICH', 'IHM',
    'IHN', 'IST', 'KAM', 'MAN', 'MIT', 'NEU', 'NIE', 'NUN', 'NUR', 'ORT',
    'RAT', 'SAH', 'SEI', 'SIE', 'TAG', 'TAT', 'TOD', 'TUN', 'UND', 'VOM',
    'VON', 'VOR', 'WAR', 'WAS', 'WEG', 'WER', 'WIE', 'WIR', 'ZUM', 'ZUR',
    'ABER', 'ALLE', 'ALSO', 'AUCH', 'BERG', 'BURG', 'DACH', 'DANN', 'DASS',
    'DEIN', 'DENN', 'DIES', 'DOCH', 'DORT', 'DREI', 'EINE', 'ENDE', 'ERDE',
    'ERST', 'EUCH', 'FAND', 'FEST', 'FORT', 'GANZ', 'GOTT', 'HALB', 'HAND',
    'HAUS', 'HEIL', 'HELD', 'HERR', 'HIER', 'HOCH', 'JEDE', 'JENE', 'KAUM',
    'KEIN', 'KERN', 'LAND', 'LANG', 'MEHR', 'MEIN', 'MUSS', 'NACH', 'NAHE',
    'NAME', 'NOCH', 'ODER', 'OHNE', 'ORTE', 'RIEF', 'RUNE', 'SAGT', 'SANG',
    'SEHR', 'SEIN', 'SICH', 'SIND', 'SOHN', 'TEIL', 'TIEF', 'TURM', 'VIEL',
    'VOLK', 'WEIL', 'WEIT', 'WELT', 'WENN', 'WERT', 'WORT', 'WOHL', 'ZAHL',
    'ZEIT', 'ZWEI', 'FACH', 'FERN', 'HEIM', 'HEER', 'HERZ', 'KLAR', 'LAUT',
    'LEID', 'LIST', 'LUFT', 'NEIN', 'REDE', 'RUHE', 'SINN', 'SPUR', 'STEIL',
    'TAGE', 'WAND', 'WUND', 'ZEIG', 'ACHT', 'EDEL', 'LEER', 'RECHT', 'DRAN',
    'STEH', 'GEHE', 'SEHE', 'REDEN', 'GENUG', 'STARK',
    'ALLES', 'ALTER', 'ALTEN', 'BEIDE', 'BERGE', 'BOTEN', 'DAHER', 'DENEN',
    'DERER', 'DIESE', 'DURCH', 'EIGEN', 'EINEN', 'EINER', 'EINEM', 'EINES',
    'ERSTE', 'ETWAS', 'EWIGE', 'GANZE', 'GEGEN', 'GEHEN', 'GEIST', 'GEBEN',
    'GROSS', 'HABEN', 'HEISS', 'JEDER', 'JEDES', 'KEINE', 'KENNT', 'KRAFT',
    'LANDE', 'LANGE', 'LEBEN', 'LICHT', 'MACHT', 'NACHT', 'NEBEN', 'NICHT',
    'ORTEN', 'RUNEN', 'SAGEN', 'SAGTE', 'SEHEN', 'SEINE', 'STEHT', 'STEIN',
    'TAGEN', 'TEILE', 'TEILS', 'UNTER', 'VIELE', 'WEDER', 'WELCH', 'WERDE',
    'WESEN', 'IMMER', 'SUCHE', 'STEIL', 'EDLEN', 'KLARE', 'STEHE', 'SUCHT',
    'SEITE', 'SEIEN', 'SINNE', 'GEBET', 'HUNDE', 'GRUND',
    'ANDERE', 'DIESER', 'DIESES', 'DIESEM', 'DIESEN', 'DUNKEL', 'EIGENE',
    'ERSTEN', 'ERSTER', 'EWIGEN', 'FINDEN', 'FRAGEN', 'GEHEIM', 'GRENZE',
    'GROSSE', 'GRUPPE', 'HELFEN', 'HIMMEL', 'KOENIG', 'KOMMEN', 'KONNTE',
    'LANGEN', 'MACHEN', 'NICHTS', 'NORDEN', 'SEINES', 'SEINER', 'SEINEM',
    'SEINEN', 'STEINE', 'SUEDEN', 'TEMPEL', 'URALTE', 'WIEDER', 'WISSEN',
    'WOLLTE', 'ZEIGEN', 'ZEITEN', 'ANDERE', 'ANFANG', 'DIENEN',
    'ANDEREN', 'EIGENEN', 'FLIEHEN', 'GROSSEN', 'LETZTEN', 'STEINEN',
    'STIMMEN', 'URALTEN', 'WAHREND', 'WOLLTEN', 'MENSCHEN',
    'LABGZERAS', 'TOTNIURG', 'HEARUCHTIGER',
])

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

# ============================================================
# FOCUSED ANALYSIS: problematic strings and their raw codes
# ============================================================

# Key unrecognized strings and the books where they appear
targets = [
    'HIENUSTEHWILGTNELN',    # appears in many books
    'LUIRUNNHWND',           # 8 books
    'AUNRSONGETRASES',       # 11 books
    'TUIGAA',                # appears in context
    'TAUTRI',                # near HEARUCHTIGER
    'HECHL',                 # in FACHHECHL
    'OELCO',                 # unknown
    'THARSC',                # near IST SCHAUN
    'TEIAD',                 # near URALTE
    'IIIWII',                # triple I + W + double I
    'SCHAUN',                # near IST
    'GETRASES',              # in AUNRSONGETRASES
]

print("=" * 100)
print("RAW CODE ANALYSIS of unrecognized segments")
print("=" * 100)

for target in targets:
    found = []
    for idx, bpairs in enumerate(book_pairs):
        text = ''.join(all_codes.get(p, '?') for p in bpairs)
        pos = text.find(target)
        if pos == -1:
            continue
        raw_codes = bpairs[pos:pos+len(target)]
        found.append((idx, raw_codes))

    if not found:
        print(f"\n  '{target}': NOT FOUND in any book")
        continue

    print(f"\n  '{target}' ({len(found)} books):")
    # Show all instances with their raw codes
    for idx, raw_codes in found[:3]:  # show up to 3
        code_str = ' '.join(raw_codes)
        print(f"    Bk{idx:2d}: {code_str}")

    # Now test: for each position in the target, what if that code was a different letter?
    # Use the first instance's codes as reference
    ref_codes = found[0][1]
    print(f"    Testing single-code reassignments:")

    for pos_in_target in range(len(ref_codes)):
        code = ref_codes[pos_in_target]
        current_letter = all_codes.get(code, '?')
        best_hits = []

        for test_letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if test_letter == current_letter:
                continue
            # Replace this position's letter
            test_target = list(target)
            test_target[pos_in_target] = test_letter
            test_str = ''.join(test_target)

            # Check if any words form across this position
            hits = []
            for wlen in range(2, min(15, len(test_str) + 1)):
                for ws in range(max(0, pos_in_target - wlen + 1),
                               min(len(test_str) - wlen + 1, pos_in_target + 1)):
                    cand = test_str[ws:ws+wlen]
                    if cand in word_dict:
                        hits.append(cand)

            if hits:
                best_hits.append((test_letter, hits))

        if best_hits:
            # Sort by max word length found
            best_hits.sort(key=lambda x: -max(len(w) for w in x[1]))
            top3 = best_hits[:3]
            for letter, hits in top3:
                print(f"      pos {pos_in_target} (code {code}={current_letter}->{letter}): {', '.join(hits)}")

# ============================================================
# SPECIFIC DEEP-DIVE: AUNRSONGETRASES
# ============================================================
print(f"\n{'='*100}")
print("DEEP DIVE: AUNRSONGETRASES — most common unrecognized phrase (11 books)")
print("=" * 100)

for idx, bpairs in enumerate(book_pairs):
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    pos = text.find('AUNRSONGETRASES')
    if pos == -1:
        continue
    # Get wide context
    start = max(0, pos - 15)
    end = min(len(bpairs), pos + 15 + 15)
    context_pairs = bpairs[start:end]
    context_text = ''.join(all_codes.get(p, '?') for p in context_pairs)
    rel_pos = pos - start
    marked = context_text[:rel_pos] + '[' + context_text[rel_pos:rel_pos+15] + ']' + context_text[rel_pos+15:]
    codes_str = ' '.join(context_pairs)
    print(f"  Bk{idx:2d}: {marked}")
    print(f"         {codes_str}")

# What are the raw codes for AUNRSONGETRASES?
print(f"\n  Raw codes for AUNRSONGETRASES:")
for idx, bpairs in enumerate(book_pairs):
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    pos = text.find('AUNRSONGETRASES')
    if pos == -1:
        continue
    raw = bpairs[pos:pos+15]
    print(f"    Bk{idx:2d}: {' '.join(raw)}")
    # Try all possible word boundaries
    break  # Just need one since they should all be same codes

# Manual word boundary attempts
print(f"\n  Word boundary hypotheses for AUNRSONGETRASES:")
hyps = [
    'A UNR SON GETRASES',
    'AUN R SON GET RASES',
    'AU NR SONNE TRASES',
    'A UN R SONGE TRASES',
    'AUNR SON GE TRASES',
    'AUNR SONGE T RASES',
    'AUNR SONGETRASES',
    'A UNR SONGE TRASES',
]
for h in hyps:
    words = h.split()
    german = [w for w in words if w in word_dict]
    print(f"    {h:35s} -> German: {german}")

# ============================================================
# DEEP DIVE: LUIRUNNHWND
# ============================================================
print(f"\n{'='*100}")
print("DEEP DIVE: LUIRUNNHWND — appears in 8 books")
print("=" * 100)

for idx, bpairs in enumerate(book_pairs):
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    pos = text.find('LUIRUNNHWND')
    if pos == -1:
        continue
    start = max(0, pos - 10)
    end = min(len(bpairs), pos + 11 + 10)
    context_pairs = bpairs[start:end]
    context_text = ''.join(all_codes.get(p, '?') for p in context_pairs)
    rel_pos = pos - start
    marked = context_text[:rel_pos] + '[' + context_text[rel_pos:rel_pos+11] + ']' + context_text[rel_pos+11:]
    print(f"  Bk{idx:2d}: {marked}")
    print(f"         {' '.join(context_pairs)}")
    break

print(f"\n  Word boundary hypotheses for LUIRUNNHWND:")
hyps = [
    'LUI RUNN HWND',
    'LUIRUNN HWND',
    'L UIRUNN HWND',
    'LUI RUN NHWND',
    'LUIR UNN HWND',
    'LU IRUNN HWND',
]
for h in hyps:
    words = h.split()
    german = [w for w in words if w in word_dict]
    print(f"    {h:25s} -> German: {german}")

# ============================================================
# DEEP DIVE: HIENUSTEHWILGT
# ============================================================
print(f"\n{'='*100}")
print("DEEP DIVE: HIENUSTEHWILGT — long unrecognized segment")
print("=" * 100)

for idx, bpairs in enumerate(book_pairs):
    text = ''.join(all_codes.get(p, '?') for p in bpairs)
    pos = text.find('HIENUSTEHWILGT')
    if pos == -1:
        continue
    start = max(0, pos - 8)
    end = min(len(bpairs), pos + 14 + 8)
    context_pairs = bpairs[start:end]
    context_text = ''.join(all_codes.get(p, '?') for p in context_pairs)
    rel_pos = pos - start
    marked = context_text[:rel_pos] + '[' + context_text[rel_pos:rel_pos+14] + ']' + context_text[rel_pos+14:]
    print(f"  Bk{idx:2d}: {marked}")
    print(f"         {' '.join(context_pairs)}")
    break

print(f"\n  Hypotheses:")
hyps = [
    'HIEN USTEH WILGT',
    'HI EN USTEH WILGT',
    'HIEN U STEH WILGT',
    'HIE NUSTEH WILGT',
    'HIEN USTEHW ILGT',
    'H IEN US TEH WILGT',
]
for h in hyps:
    words = h.split()
    german = [w for w in words if w in word_dict]
    print(f"    {h:25s} -> German: {german}")

# ============================================================
# CHECK: Could any codes be WRONG? Test code frequency vs expected
# ============================================================
print(f"\n{'='*100}")
print("FREQUENCY AUDIT — codes that appear in unrecognized text disproportionately")
print("=" * 100)

# For each code, count how often it appears in recognized vs unrecognized segments
# Using the main fragment from comprehensive_decode

# Get the main superstring
texts_decoded = []
for bpairs in book_pairs:
    texts_decoded.append(''.join(all_codes.get(p, '?') for p in bpairs))

# Use Bk9 as a representative
bk9 = texts_decoded[9]
from collections import defaultdict

# DP parse of Bk9
n = len(bk9)
dp = [(0, -1, None)] * (n + 1)
for i in range(1, n + 1):
    dp[i] = (dp[i-1][0], i-1, None)
    for wlen in range(2, min(20, i + 1)):
        start = i - wlen
        candidate = bk9[start:i]
        if '?' not in candidate and candidate in word_dict:
            new_covered = dp[start][0] + wlen
            if new_covered > dp[i][0]:
                dp[i] = (new_covered, start, candidate)

words_found = []
pos = n
while pos > 0:
    _, prev, word = dp[pos]
    if word:
        words_found.append((prev, word))
        pos = prev
    else:
        pos = prev
words_found.reverse()

covered = [False] * n
for start, word in words_found:
    for j in range(start, start + len(word)):
        covered[j] = True

# Count letters in covered vs uncovered
covered_letters = Counter()
uncovered_letters = Counter()
for i in range(n):
    if bk9[i] == '?':
        continue
    if covered[i]:
        covered_letters[bk9[i]] += 1
    else:
        uncovered_letters[bk9[i]] += 1

print(f"  Bk9: covered={sum(covered_letters.values())}, uncovered={sum(uncovered_letters.values())}")
print(f"\n  Letters overrepresented in uncovered segments (suspicious):")
total_covered = sum(covered_letters.values())
total_uncovered = sum(uncovered_letters.values())
for letter in sorted(set(list(covered_letters.keys()) + list(uncovered_letters.keys()))):
    cov_pct = covered_letters[letter] / total_covered * 100 if total_covered else 0
    unc_pct = uncovered_letters[letter] / total_uncovered * 100 if total_uncovered else 0
    ratio = unc_pct / cov_pct if cov_pct > 0 else float('inf')
    if ratio > 1.5 or ratio < 0.5:
        print(f"    {letter}: covered={cov_pct:.1f}%, uncovered={unc_pct:.1f}%, ratio={ratio:.2f}")
