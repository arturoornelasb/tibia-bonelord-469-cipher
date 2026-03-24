#!/usr/bin/env python3
"""
Constraint-Based Solver V8
===========================
Use confirmed anagram constraints + simulated annealing to find a better mapping.

Hard constraints (codes locked):
  LABGZERAS    = SALZBERG+A  -> codes locked for S,A,L,Z,B,E,R,G
  SCHWITEIONE  = WEICHSTEIN+O -> codes locked for S,C,H,W,I,T,E,O,N
  AUNRSONGETRASES = ORANGENSTRASSE+U -> codes locked for O,R,A,N,G,E,N,S,T,R,A,S,S,E,U

Strategy:
  1. Identify which codes are "locked" by anagram constraints
  2. For remaining codes, try targeted swaps
  3. Score = word_coverage + freq_fitness + bigram_quality
  4. Focus on fixing garbled segments (HECHLLT, NDCE, RHEIUIRUNN)
"""

import json, os, random, math
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

with open(os.path.join(data_dir, 'books.json'), 'r') as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'mapping_v7.json'), 'r') as f:
    v7 = json.load(f)

GERMAN_WORDS = set([
    'SO', 'DA', 'JA', 'ZU', 'AN', 'IN', 'UM', 'ES', 'ER', 'WO',
    'DU', 'OB', 'AM', 'IM', 'AB', 'OH',
    'DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN', 'UND', 'IST',
    'WIR', 'ICH', 'SIE', 'MAN', 'WER', 'WIE', 'WAS', 'NUR', 'GUT',
    'MIT', 'VON', 'HAT', 'AUF', 'AUS', 'BEI', 'VOR', 'FUR', 'VOM',
    'ZUM', 'ZUR', 'BIS', 'ALS', 'NUN', 'HIN', 'TAG', 'ORT', 'TOD',
    'OFT', 'NIE', 'ALT', 'NEU', 'GAR', 'NET', 'ODE', 'SEI', 'TUN',
    'MAL', 'RAT', 'RUF', 'MUT', 'HUT', 'NOT', 'ROT', 'TAT', 'HER',
    'GEN', 'WEG', 'INS', 'WAR', 'SAG', 'GIB', 'MIN', 'SER',
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
    'REDE', 'REDEN', 'WESEN', 'EHRE', 'TREUE', 'GRAB', 'GRUFT',
    'ALTE', 'ALTEN', 'ALTER', 'NEUE', 'NEUEN',
    'DUNKLE', 'DUNKLEN', 'OBEN', 'UNTEN',
    'DIESEN', 'DIESEM', 'DIESER', 'DIESES',
    'SEINER', 'SEINEN', 'SEINES', 'SEINEM',
    'NORDEN', 'SUEDEN', 'OSTEN', 'WESTEN',
    'EDEL', 'ADEL', 'HARSCH', 'SCHAR',
    'TEIL', 'TEILE', 'TEILEN', 'SEITE', 'SEITEN',
    'TAGE', 'TAGEN', 'NEBEN', 'LEBEN', 'GEBEN',
    'SAGTE', 'WURDE', 'WAREN', 'HATTE',
    'HABEN', 'SEHEN', 'NEHMEN',
    'FEUER', 'WASSER', 'HOLZ', 'EISEN',
    'STERN', 'STERNE', 'MOND', 'SONNE',
    'BLUT', 'BEIN', 'HERZ', 'LEIB', 'HAUPT',
    'FLUCHT', 'FURCHT', 'ZORN', 'STOLZ', 'SCHULD',
    'FRIEDE', 'FRIEDEN', 'FREUND', 'FEIND',
    'TURM', 'MAUER', 'STRASSE',
    'DORF', 'STADT', 'SCHLOSS', 'TEMPEL',
    'WALD', 'WIESE', 'FLUSS', 'MEER', 'INSEL',
    'SAGE', 'LEGENDE',
    'ACHT', 'NEUN', 'ZEHN', 'DREI', 'VIER',
    'SECHS', 'SIEBEN', 'ZWEI', 'EINS',
    'SANG', 'BRING', 'RING', 'DING', 'KLING',
    'SUCHE', 'SUCHEN', 'FRAGE', 'FRAGEN',
    'TIEF', 'FEST', 'KALT', 'WARM', 'LANG', 'KURZ',
    'GROSS', 'KLEIN', 'BREIT', 'SCHMAL',
    'OFFEN', 'GESCHLOSSEN', 'LEER', 'VOLL',
    'RECHT', 'SCHLECHT', 'ECHT', 'FALSCH',
    'STAHL', 'SILBER', 'KUPFER',
    'GRUEN', 'BLAU', 'WEISS', 'SCHWARZ',
    'NACHT', 'MORGEN', 'ABEND', 'MITTAG',
    'BRUDER', 'SCHWESTER', 'VATER', 'MUTTER',
    'SOHN', 'TOCHTER', 'KIND', 'KINDER',
    'MEISTER', 'RITTER', 'PRIESTER', 'BAUER',
    'KAUFEN', 'LAUFEN', 'RUFEN', 'SCHLAFEN',
    'WERFEN', 'HELFEN', 'STERBEN', 'WERDEN',
    'TRAGEN', 'GRABEN', 'FAHREN', 'FALLEN',
    'LESEN', 'ESSEN', 'VERGESSEN', 'MESSEN',
    'BETEN', 'REDEN', 'TRETEN',
    'STUNDE', 'MONAT', 'SOMMER', 'WINTER',
    'FRUEH', 'SPAET',
    'WACHE', 'WACHEN', 'HUETEN', 'SCHUETZEN',
    'SCHILD', 'HELM', 'RUESTUNG',
    'WAFFE', 'DOLCH', 'BOGEN', 'PFEIL',
    'SCHATZ', 'BEUTE', 'RAUB',
    'GEBET', 'FLUCH', 'SEGEN', 'ZAUBER',
    'MACHT', 'KRAFT', 'STAERKE',
    'SCHULD', 'SUENDE', 'STRAFE',
    'EHREN', 'LOBEN', 'PREISEN',
    'MAHNEN', 'WARNEN', 'DROHEN',
    'OEL', 'SCE', 'MINNE',
    'HWND', 'HIHL', 'EILCH', 'TAUTR',
    'HEARUCHTIG', 'HEARUCHTIGER',
    'LABGZERAS', 'HEDEMI', 'ADTHARSC',
    'TOTNIURG', 'EDETOTNIURG',
    'SCHWITEIONE', 'SCHWITEIO',
    'TIUMENGEMI', 'LABRNI', 'UTRUNR',
    'AUNRSONGETRASES', 'ENGCHD', 'KELSEI', 'GEVMT',
])

# German expected letter frequencies
GERMAN_FREQ = {
    'E': 17.40, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
    'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
    'L': 3.44, 'C': 3.06, 'G': 3.01, 'M': 2.53, 'O': 2.51,
    'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
    'P': 0.79,
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

book_pairs = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_pairs.append(pairs)

code_counts = Counter()
for bpairs in book_pairs:
    code_counts.update(bpairs)
total_codes = sum(code_counts.values())

# ============================================================
# PHASE 1: Identify locked codes from confirmed anagrams
# ============================================================
print("=" * 70)
print("PHASE 1: ANAGRAM-LOCKED CODES")
print("=" * 70)

# Find code sequences for confirmed proper nouns
def find_codes_for_text(target):
    """Find the consistent code sequence for a decoded text string."""
    for bpairs in book_pairs:
        text = ''.join(v7.get(p, '?') for p in bpairs)
        pos = text.find(target)
        if pos >= 0:
            return bpairs[pos:pos+len(target)]
    return None

# LABGZERAS = SALZBERG + A
labg_codes = find_codes_for_text("LABGZERAS")
# SCHWITEIONE = WEICHSTEIN + O
schw_codes = find_codes_for_text("SCHWITEIONE")
# AUNRSONGETRASES = ORANGENSTRASSE + U
aunr_codes = find_codes_for_text("AUNRSONGETRASES")
# FINDEN = FINDEN (very common, high confidence)
find_codes = find_codes_for_text("FINDEN")

locked_codes = set()
locked_assignments = {}

for name, codes, text in [
    ("LABGZERAS", labg_codes, "LABGZERAS"),
    ("SCHWITEIONE", schw_codes, "SCHWITEIONE"),
    ("AUNRSONGETRASES", aunr_codes, "AUNRSONGETRASES"),
    ("FINDEN", find_codes, "FINDEN"),
]:
    if codes:
        print(f"\n  {name} = {text}")
        print(f"    Codes: {' '.join(codes)}")
        for i, (code, letter) in enumerate(zip(codes, text)):
            current = v7.get(code, '?')
            locked_codes.add(code)
            locked_assignments[code] = current
            marker = " (SAME)" if current == letter else f" -> anagram letter {letter}"
            print(f"    [{code}]={current}{marker}")

# Also lock high-confidence common words: DER, DIE, DAS, EIN, UND, IST, etc.
common_phrases = ["DIE URALTE STEINEN", "KOENIG", "NACH", "STEH", "GEH", "ERDE", "ICH"]
for phrase in common_phrases:
    codes = find_codes_for_text(phrase)
    if codes:
        for code in codes:
            locked_codes.add(code)
            locked_assignments[code] = v7.get(code, '?')

print(f"\n  Total locked codes: {len(locked_codes)}/{len(v7)}")
unlocked = [c for c in v7 if c not in locked_codes]
print(f"  Unlocked codes: {len(unlocked)}")
for c in sorted(unlocked, key=lambda x: int(x)):
    print(f"    [{c}]={v7[c]} ({code_counts.get(c, 0)} occ)")

# ============================================================
# PHASE 2: Score function
# ============================================================

def dp_parse(text, word_set):
    n = len(text)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i-1]
        for wlen in range(2, min(i, 20) + 1):
            start = i - wlen
            cand = text[start:i]
            if '?' not in cand and cand in word_set:
                score = dp[start] + wlen
                if score > dp[i]:
                    dp[i] = score
    return dp[n]

def evaluate_mapping(mapping):
    """Score a mapping: word coverage + frequency fitness."""
    # Decode all books
    total_chars = 0
    total_covered = 0
    letter_counts = Counter()

    for bpairs in book_pairs:
        text = ''.join(mapping.get(p, '?') for p in bpairs)
        known = sum(1 for c in text if c != '?')
        covered = dp_parse(text, GERMAN_WORDS)
        total_chars += known
        total_covered += covered
        letter_counts.update(c for c in text if c != '?')

    coverage = total_covered / max(total_chars, 1) * 100

    # Frequency fitness
    total_letters = sum(letter_counts.values())
    freq_score = 0
    for letter, expected_pct in GERMAN_FREQ.items():
        actual_pct = letter_counts.get(letter, 0) / total_letters * 100
        freq_score += abs(actual_pct - expected_pct)

    # Combined score (higher = better)
    # coverage is ~58%, freq_score is ~18 (lower = better)
    combined = coverage - freq_score * 0.3

    return coverage, freq_score, combined

# ============================================================
# PHASE 3: Targeted single-code swaps on unlocked codes
# ============================================================
print(f"\n{'=' * 70}")
print("PHASE 3: TARGETED SINGLE-CODE SWAPS")
print("=" * 70)

base_cov, base_freq, base_combined = evaluate_mapping(v7)
print(f"\n  V7 baseline: coverage={base_cov:.2f}%, freq={base_freq:.2f}, combined={base_combined:.2f}")

LETTERS = list('ABCDEFGHIKLMNOPRSTUWZ')
improvements = []

for code in unlocked:
    current_letter = v7[code]
    for target_letter in LETTERS:
        if target_letter == current_letter:
            continue
        # Test swap
        test_map = dict(v7)
        test_map[code] = target_letter
        cov, freq, combined = evaluate_mapping(test_map)

        if combined > base_combined + 0.05:
            improvements.append({
                'code': code,
                'from': current_letter,
                'to': target_letter,
                'cov': cov,
                'freq': freq,
                'combined': combined,
                'delta': combined - base_combined,
            })

improvements.sort(key=lambda x: -x['delta'])

if improvements:
    print(f"\n  Found {len(improvements)} improving swaps:")
    print(f"  {'Code':>5} {'From':>5} {'To':>5} {'Cov%':>7} {'Freq':>7} {'Comb':>7} {'Delta':>7}")
    print(f"  {'-'*50}")
    for imp in improvements[:20]:
        print(f"    [{imp['code']:>2}] {imp['from']:>5} {imp['to']:>5} "
              f"{imp['cov']:>6.2f} {imp['freq']:>6.2f} {imp['combined']:>6.2f} {imp['delta']:>+6.3f}")
else:
    print("  No single-code improvements found among unlocked codes.")

# ============================================================
# PHASE 4: Test pairs of swaps among top improvements
# ============================================================
print(f"\n{'=' * 70}")
print("PHASE 4: PAIRWISE SWAP COMBINATIONS")
print("=" * 70)

# Get unique codes from top improvements
top_swaps = improvements[:15] if improvements else []
pair_results = []

for i in range(len(top_swaps)):
    for j in range(i+1, len(top_swaps)):
        s1, s2 = top_swaps[i], top_swaps[j]
        if s1['code'] == s2['code']:
            continue
        test_map = dict(v7)
        test_map[s1['code']] = s1['to']
        test_map[s2['code']] = s2['to']
        cov, freq, combined = evaluate_mapping(test_map)
        if combined > base_combined + 0.1:
            pair_results.append({
                'swaps': [(s1['code'], s1['from'], s1['to']),
                          (s2['code'], s2['from'], s2['to'])],
                'cov': cov, 'freq': freq, 'combined': combined,
                'delta': combined - base_combined,
            })

pair_results.sort(key=lambda x: -x['delta'])
if pair_results:
    print(f"\n  Top pair combinations:")
    for pr in pair_results[:10]:
        swaps_str = ' + '.join(f"[{s[0]}]{s[1]}->{s[2]}" for s in pr['swaps'])
        print(f"    {swaps_str}: cov={pr['cov']:.2f}% freq={pr['freq']:.2f} "
              f"combined={pr['combined']:.2f} delta={pr['delta']:+.3f}")

# ============================================================
# PHASE 5: Garbled Segment Cracking
# ============================================================
print(f"\n{'=' * 70}")
print("PHASE 5: GARBLED SEGMENT CRACKING")
print("=" * 70)

def find_segment_codes(target):
    """Find code sequence and all contexts for a garbled segment."""
    results = []
    for bidx, bpairs in enumerate(book_pairs):
        text = ''.join(v7.get(p, '?') for p in bpairs)
        pos = 0
        while True:
            pos = text.find(target, pos)
            if pos < 0: break
            codes = bpairs[pos:pos+len(target)]
            ctx_s = max(0, pos - 15)
            ctx_e = min(len(text), pos + len(target) + 15)
            results.append({
                'book': bidx, 'pos': pos,
                'codes': codes, 'context': text[ctx_s:ctx_e]
            })
            pos += 1
    return results

# For each garbled segment, try every possible 1-code substitution
# and check if the result contains German words
garbled_targets = [
    ("HECHLLT", "after NACH/FACH"),
    ("NDCE", "in DIE NDCE"),
    ("RHEIUIRUNN", "with HWND"),
    ("LAUNRLRUNR", "near NACH"),
    ("TEHWRIGTN", "before EIN"),
    ("NTEUTTUIG", "various"),
    ("UNENITGH", "after LABGZERAS"),
    ("GEIGET", "various"),
]

# Extended word list for garbled segment matching
EXTENDED_WORDS = GERMAN_WORDS | set([
    'GESCHLECHT', 'RECHT', 'KNECHT', 'ECHT', 'SCHLECHT',
    'MACHT', 'NACHT', 'ACHT', 'TRACHT', 'PRACHT',
    'GEFECHT', 'PFLICHT', 'LICHT', 'SICHT', 'BERICHT',
    'GERICHT', 'GEDICHT', 'GEWICHT', 'ZUCHT', 'SUCHT',
    'FRUCHT', 'FLUCHT', 'FURCHT', 'BUCHT',
    'NICHTS', 'RECHTS', 'NACHTS',
    'KRAFT', 'SCHRIFT', 'VERNUNFT', 'ANKUNFT', 'ZUKUNFT',
    'EINHERRUFEN', 'ZUSAMMEN', 'RICHTUNG', 'ORDNUNG',
    'ANFUEHRUNG', 'BERATUNG', 'BEDEUTUNG', 'ERRETTUNG',
    'BELEHRUNG', 'ERHELLUNG', 'STELLUNG', 'HALTUNG',
    'WOHNUNG', 'RECHNUNG', 'ZEICHNUNG', 'WANDLUNG',
    'HANDLUNG', 'ERZAEHLUNG', 'FORSCHUNG', 'MISCHUNG',
    'HOFFNUNG', 'WARNUNG', 'MAHNUNG', 'REINIGUNG',
    'HEILIGUNG', 'KREUZIGUNG',
    'RITTER', 'BITTER', 'MUTTER', 'BUTTER', 'WETTER',
    'BRUDER', 'KINDER', 'FELDER', 'WAELDER', 'LAENDER',
    'MAENNER', 'FRAUEN', 'KRIEGER', 'JAEGER', 'WANDERER',
    'SCHENKEN', 'DENKEN', 'LENKEN', 'TRINKEN', 'SINKEN',
    'RINGEN', 'SINGEN', 'BRINGEN', 'SPRINGEN', 'KLINGEN',
    'SCHWINGEN', 'DRINGEN', 'ZWINGEN',
    'ERKENNEN', 'BEKENNEN', 'NENNEN', 'BRENNEN', 'RENNEN',
    'HERR', 'HERRSCHAFT', 'HERRLICH', 'HERRSCHER',
    'GEWALTIG', 'MAECHTIG', 'PRAECHTIG', 'EINTRAECHTIG',
    'BEDAECHTIG', 'ANDAECHTIG', 'NACHDRUECKLICH',
    'HEILIG', 'EWIG', 'WENIG', 'FERTIG', 'RICHTIG',
    'WICHTIG', 'MUTIG', 'GUELTIG', 'SCHULDIG',
    'LEBENDIG', 'ELEND', 'FREMD', 'BEREIT',
    'EHRFUERCHTIG', 'UEBERMAECHTIG',
    'SCHREIBEN', 'TREIBEN', 'BLEIBEN',
    'GLEICHEN', 'REICHEN', 'WEICHEN', 'STREICHEN',
    'NACHHER', 'VORHER', 'NACHRICHT', 'VORSICHT',
    'RITTERLICH', 'KOENIGLICH', 'KAISERLICH',
    'NATUERLICH', 'SICHERLICH', 'WAHRLICH',
])

for target, desc in garbled_targets:
    results = find_segment_codes(target)
    if not results:
        continue

    codes = results[0]['codes']
    print(f"\n  '{target}' ({len(results)}x, {desc})")
    print(f"    Codes: {' '.join(codes)}")
    print(f"    Context: {results[0]['context']}")

    # Try changing each code to every letter
    best_fixes = []
    for pos_idx in range(len(codes)):
        code = codes[pos_idx]
        if code in locked_codes:
            continue
        original = v7.get(code, '?')

        for letter in LETTERS:
            if letter == original:
                continue

            # Build the new decoded segment
            new_text = ''
            for k, c in enumerate(codes):
                if k == pos_idx:
                    new_text += letter
                else:
                    new_text += v7.get(c, '?')

            # Check for German words in extended context
            # Look at segment + surrounding context
            for r in results[:1]:
                bpairs = book_pairs[r['book']]
                ctx_s = max(0, r['pos'] - 5)
                ctx_e = min(len(bpairs), r['pos'] + len(target) + 5)
                ctx_codes = bpairs[ctx_s:ctx_e]

                full_text = ''
                for k, c in enumerate(ctx_codes):
                    rel_pos = k - (r['pos'] - ctx_s)
                    if 0 <= rel_pos < len(codes) and rel_pos == pos_idx:
                        full_text += letter
                    else:
                        full_text += v7.get(c, '?')

                # Find all German words in full_text
                found_words = set()
                for wlen in range(2, min(len(full_text), 20) + 1):
                    for start in range(len(full_text) - wlen + 1):
                        candidate = full_text[start:start+wlen]
                        if candidate in EXTENDED_WORDS:
                            found_words.add(candidate)

                if found_words:
                    # Compute word length coverage for this context
                    word_cov = dp_parse(full_text, EXTENDED_WORDS)
                    base_word_cov = dp_parse(
                        ''.join(v7.get(c, '?') for c in ctx_codes),
                        EXTENDED_WORDS
                    )

                    if word_cov > base_word_cov:
                        best_fixes.append({
                            'pos': pos_idx,
                            'code': code,
                            'from': original,
                            'to': letter,
                            'new_text': new_text,
                            'full_ctx': full_text,
                            'words': found_words,
                            'word_cov': word_cov,
                            'base_cov': base_word_cov,
                            'gain': word_cov - base_word_cov,
                        })

    # Sort by coverage gain
    best_fixes.sort(key=lambda x: -x['gain'])

    if best_fixes:
        print(f"    TOP FIXES:")
        seen_texts = set()
        for fix in best_fixes[:8]:
            if fix['new_text'] in seen_texts:
                continue
            seen_texts.add(fix['new_text'])
            words_str = ', '.join(sorted(fix['words'], key=lambda x: -len(x))[:5])
            print(f"      [{fix['code']}]{fix['from']}->{fix['to']}: "
                  f"'{fix['new_text']}' (gain={fix['gain']}, words: {words_str})")
    else:
        print(f"    No single-code fixes found.")

# ============================================================
# PHASE 6: Multi-code garbled segment attack
# ============================================================
print(f"\n{'=' * 70}")
print("PHASE 6: MULTI-CODE GARBLED FIXES (2 simultaneous changes)")
print("=" * 70)

for target, desc in garbled_targets[:4]:  # Focus on top 4
    results = find_segment_codes(target)
    if not results:
        continue

    codes = results[0]['codes']
    changeable = [(i, codes[i]) for i in range(len(codes)) if codes[i] not in locked_codes]

    if len(changeable) < 2:
        continue

    print(f"\n  '{target}' - testing 2-code changes:")

    best_multi = []
    for ci in range(len(changeable)):
        for cj in range(ci+1, len(changeable)):
            pos_i, code_i = changeable[ci]
            pos_j, code_j = changeable[cj]

            for li in LETTERS:
                if li == v7.get(code_i, '?'):
                    continue
                for lj in LETTERS:
                    if lj == v7.get(code_j, '?'):
                        continue

                    # Build new text
                    new_text = ''
                    for k, c in enumerate(codes):
                        if k == pos_i:
                            new_text += li
                        elif k == pos_j:
                            new_text += lj
                        else:
                            new_text += v7.get(c, '?')

                    # Check for long German words
                    found_words = set()
                    for wlen in range(3, min(len(new_text), 20) + 1):
                        for start in range(len(new_text) - wlen + 1):
                            candidate = new_text[start:start+wlen]
                            if candidate in EXTENDED_WORDS:
                                found_words.add(candidate)

                    if found_words:
                        total_word_len = sum(len(w) for w in found_words)
                        if total_word_len >= 4:
                            best_multi.append({
                                'changes': [(code_i, v7.get(code_i, '?'), li, pos_i),
                                            (code_j, v7.get(code_j, '?'), lj, pos_j)],
                                'new_text': new_text,
                                'words': found_words,
                                'total_word_len': total_word_len,
                            })

    best_multi.sort(key=lambda x: -x['total_word_len'])

    if best_multi:
        seen = set()
        count = 0
        for bm in best_multi:
            if bm['new_text'] in seen:
                continue
            seen.add(bm['new_text'])
            changes_str = ' + '.join(f"[{c[0]}]{c[1]}->{c[2]}" for c in bm['changes'])
            words_str = ', '.join(sorted(bm['words'], key=lambda x: -len(x))[:5])
            print(f"    {changes_str}: '{bm['new_text']}' -> {words_str}")
            count += 1
            if count >= 10:
                break

# ============================================================
# PHASE 7: Check best improvement globally
# ============================================================
print(f"\n{'=' * 70}")
print("PHASE 7: GLOBAL IMPACT ASSESSMENT")
print("=" * 70)

# If we found improvements, apply the best and show decoded text
if improvements:
    best = improvements[0]
    test_map = dict(v7)
    test_map[best['code']] = best['to']

    print(f"\n  Best single swap: [{best['code']}] {best['from']}->{best['to']}")
    print(f"  Coverage: {best['cov']:.2f}% (was {base_cov:.2f}%)")
    print(f"  Freq score: {best['freq']:.2f} (was {base_freq:.2f})")

    # Show affected text samples
    print(f"\n  Text changes:")
    for bidx, bpairs in enumerate(book_pairs[:10]):
        text_old = ''.join(v7.get(p, '?') for p in bpairs)
        text_new = ''.join(test_map.get(p, '?') for p in bpairs)
        if text_old != text_new:
            # Find differences
            for i in range(len(text_old)):
                if text_old[i] != text_new[i]:
                    ctx_s = max(0, i - 10)
                    ctx_e = min(len(text_old), i + 10)
                    print(f"    Book {bidx}: ...{text_old[ctx_s:ctx_e]}... -> ...{text_new[ctx_s:ctx_e]}...")
                    break

# Summary
print(f"\n{'=' * 70}")
print("SUMMARY")
print("=" * 70)
print(f"  V7 baseline: coverage={base_cov:.2f}%, freq_score={base_freq:.2f}")
print(f"  Locked codes (from anagrams): {len(locked_codes)}")
print(f"  Unlocked codes: {len(unlocked)}")
print(f"  Single-code improvements found: {len(improvements)}")
print(f"  Pair improvements found: {len(pair_results)}")
