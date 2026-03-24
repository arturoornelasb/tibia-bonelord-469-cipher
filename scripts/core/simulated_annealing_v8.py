#!/usr/bin/env python3
"""
Simulated Annealing Solver
============================
Explore the mapping space stochastically while respecting hard constraints
from confirmed anagrams. Uses combined score: word_coverage - freq_penalty.

Hard constraints: 43 locked codes from anagram evidence.
Search space: 55 unlocked codes, each can be any of 21 German letters.
"""

import json, os, random, math, copy
from collections import Counter

random.seed(42)

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
    'NIE', 'ALT', 'NEU', 'GAR', 'SEI', 'TUN', 'HER', 'GEN', 'WEG',
    'MIN', 'SER', 'ODE', 'INS', 'WAR', 'SAG', 'GIB',
    'ENDE', 'REDE', 'RUNE', 'WORT', 'NACH', 'AUCH',
    'NOCH', 'DOCH', 'SICH', 'SIND', 'SEIN', 'WARD', 'DASS', 'WENN',
    'DANN', 'DENN', 'ABER', 'ODER', 'WEIL', 'WIRD', 'EINE', 'DIES',
    'HIER', 'DORT', 'WELT', 'ZEIT', 'TEIL', 'NAME',
    'GANZ', 'SEHR', 'VIEL', 'FORT', 'HOCH', 'KLAR', 'ERDE', 'GOTT',
    'HERR', 'BURG', 'BERG', 'GOLD', 'SOHN', 'WAHR', 'HELD', 'FACH',
    'WIND', 'FAND', 'GING', 'NAHM', 'SAGT', 'KANN', 'SOLL', 'WILL',
    'MUSS', 'GIBT', 'RIEF', 'LAND', 'HAND', 'BAND', 'SAND', 'WAND',
    'MACHT', 'KRAFT', 'GEIST', 'NACHT', 'LICHT', 'REICH',
    'UNTER', 'DURCH', 'GEGEN', 'IMMER', 'NICHT', 'SCHON',
    'DIESE', 'SEINE', 'EINEN', 'EINER', 'EINEM', 'EINES',
    'URALTE', 'STEINEN', 'STEINE', 'STEIN', 'RUNEN', 'FINDEN',
    'STEHEN', 'GEHEN', 'KOMMEN', 'SAGEN', 'WISSEN',
    'ERSTE', 'KOENIG', 'RUIN', 'SCHAUN',
    'ORTE', 'ORTEN', 'WORTE', 'STEH', 'GEH',
    'ALLE', 'ALLES', 'VIELE', 'WIEDER', 'WISSET',
    'REDE', 'REDEN', 'WESEN', 'EHRE', 'GRAB', 'GRUFT',
    'ALTE', 'ALTEN', 'ALTER', 'NEUE', 'NEUEN',
    'DIESEN', 'DIESEM', 'DIESER', 'DIESES',
    'SEINER', 'SEINEN', 'SEINES', 'SEINEM',
    'EDEL', 'ADEL', 'OBEN', 'UNTEN',
    'TEIL', 'TEILE', 'TEILEN', 'SEITE', 'SEITEN',
    'TAGE', 'TAGEN', 'NEBEN', 'LEBEN', 'GEBEN',
    'HABEN', 'SEHEN', 'NEHMEN',
    'FEUER', 'WASSER', 'STERN', 'STERNE',
    'OEL', 'SCE', 'MINNE', 'HWND',
    'SANG', 'DING', 'RING',
    'SUCHE', 'SUCHEN', 'FRAGE',
    'FEST', 'TIEF', 'RECHT',
    'EIGEN', 'GEIGEN', 'ZEIGEN', 'REIGEN',
    'BEI', 'AUF', 'AUS',
    'OFFEN', 'GROSS', 'KLEIN',
    'NACHT', 'MORGEN', 'ABEND',
    'BRUDER', 'VATER', 'MUTTER', 'KIND',
    'MEISTER', 'RITTER', 'PRIESTER',
    'HELFEN', 'WERFEN', 'STERBEN', 'WERDEN',
    'TRAGEN', 'GRABEN', 'FALLEN',
    'LESEN', 'ESSEN',
    'SCHILD', 'HELM', 'SCHWERT',
    'SCHATZ', 'SEGEN', 'FLUCH', 'ZAUBER',
    'MAHNEN', 'WARNEN',
    'LABGZERAS', 'HEDEMI', 'ADTHARSC', 'TAUTR',
    'EDETOTNIURG', 'SCHWITEIONE',
    'TIUMENGEMI', 'UTRUNR', 'HEARUCHTIG',
    'HIHL', 'EILCH', 'ENGCHD', 'KELSEI',
    'AUNRSONGETRASES',
])

GERMAN_FREQ = {
    'E': 17.40, 'N': 9.78, 'I': 7.55, 'S': 7.27, 'R': 7.00,
    'A': 6.51, 'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35,
    'L': 3.44, 'C': 3.06, 'G': 3.01, 'M': 2.53, 'O': 2.51,
    'B': 1.89, 'W': 1.89, 'F': 1.66, 'K': 1.21, 'Z': 1.13,
    'P': 0.79,
}

LETTERS = list(GERMAN_FREQ.keys())

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

# Locked codes from anagram constraints
def find_codes_for_text(target, mapping):
    for bpairs in book_pairs:
        text = ''.join(mapping.get(p, '?') for p in bpairs)
        pos = text.find(target)
        if pos >= 0:
            return bpairs[pos:pos+len(target)]
    return None

locked_codes = set()
for phrase in ['LABGZERAS', 'SCHWITEIONE', 'AUNRSONGETRASES', 'FINDEN',
               'DIE URALTE STEINEN', 'KOENIG', 'NACH', 'STEH', 'GEH',
               'ERDE', 'ICH', 'SCHAUN', 'RUIN', 'DASS']:
    # Find in the text and mark those codes
    for bpairs in book_pairs:
        text = ''.join(v7.get(p, '?') for p in bpairs)
        pos = text.find(phrase.replace(' ', ''))
        if pos >= 0:
            for code in bpairs[pos:pos+len(phrase.replace(' ', ''))]:
                locked_codes.add(code)
            break

unlocked = [c for c in v7 if c not in locked_codes]
print(f"Locked: {len(locked_codes)}, Unlocked: {len(unlocked)}")

# Pre-decode books for speed (cache the parts that don't change)
def decode_fast(mapping):
    """Fast decode all books and compute score."""
    total_chars = 0
    total_covered = 0
    letter_counts = Counter()

    for bpairs in book_pairs:
        text = ''.join(mapping.get(p, '?') for p in bpairs)
        known = sum(1 for c in text if c != '?')
        total_chars += known

        # DP word coverage (simplified for speed)
        n = len(text)
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i-1]
            for wlen in range(2, min(i, 16) + 1):
                start = i - wlen
                cand = text[start:i]
                if '?' not in cand and cand in GERMAN_WORDS:
                    if dp[start] + wlen > dp[i]:
                        dp[i] = dp[start] + wlen
        total_covered += dp[n]
        letter_counts.update(c for c in text if c != '?')

    coverage = total_covered / max(total_chars, 1) * 100
    total_letters = sum(letter_counts.values())
    freq_score = sum(abs(letter_counts.get(l, 0) / total_letters * 100 - GERMAN_FREQ[l])
                     for l in GERMAN_FREQ)

    return coverage - freq_score * 0.25

# Initial score
base_score = decode_fast(v7)
print(f"V7 baseline score: {base_score:.4f}")

# ============================================================
# SIMULATED ANNEALING
# ============================================================
best_mapping = dict(v7)
best_score = base_score
current_mapping = dict(v7)
current_score = base_score

T_start = 2.0
T_end = 0.01
n_steps = 8000  # Total iterations
cooling_rate = (T_end / T_start) ** (1.0 / n_steps)

accepted = 0
improved = 0

print(f"\nRunning SA: {n_steps} steps, T: {T_start} -> {T_end}")

T = T_start
for step in range(n_steps):
    # Pick random unlocked code
    code = random.choice(unlocked)
    old_letter = current_mapping[code]

    # Pick random new letter (different from current)
    new_letter = random.choice([l for l in LETTERS if l != old_letter])

    # Apply change
    current_mapping[code] = new_letter
    new_score = decode_fast(current_mapping)

    delta = new_score - current_score

    # Accept or reject
    if delta > 0 or random.random() < math.exp(delta / T):
        current_score = new_score
        accepted += 1
        if new_score > best_score:
            best_score = new_score
            best_mapping = dict(current_mapping)
            improved += 1
    else:
        current_mapping[code] = old_letter  # Revert

    T *= cooling_rate

    if (step + 1) % 1000 == 0:
        print(f"  Step {step+1:5d}: T={T:.4f}, current={current_score:.4f}, "
              f"best={best_score:.4f}, accepted={accepted}, improved={improved}")

print(f"\nSA complete.")
print(f"  Best score: {best_score:.4f} (baseline: {base_score:.4f})")
print(f"  Delta: {best_score - base_score:+.4f}")
print(f"  Accepted: {accepted}/{n_steps}")
print(f"  Improved: {improved}")

# Show changes from V7
changes = []
for code in sorted(v7.keys(), key=int):
    if v7[code] != best_mapping.get(code, v7[code]):
        changes.append((code, v7[code], best_mapping[code], code_counts.get(code, 0)))

if changes:
    print(f"\n  Changes from V7:")
    for code, old, new, occ in changes:
        locked_str = " (LOCKED!)" if code in locked_codes else ""
        print(f"    [{code}] {old} -> {new} ({occ} occ){locked_str}")

    # Show text differences for a sample book
    print(f"\n  Text comparison (Book 2):")
    bpairs = book_pairs[2]
    text_old = ''.join(v7.get(p, '?') for p in bpairs)
    text_new = ''.join(best_mapping.get(p, '?') for p in bpairs)
    print(f"    V7:  {text_old}")
    print(f"    SA:  {text_new}")
else:
    print("\n  No changes from V7 -- mapping is at local optimum!")

# ============================================================
# SECOND RUN: More aggressive (higher temp, more steps)
# ============================================================
print(f"\n{'=' * 70}")
print("SECOND SA RUN (aggressive)")
print(f"{'=' * 70}")

random.seed(123)
best_mapping2 = dict(v7)
best_score2 = base_score
current_mapping2 = dict(v7)
current_score2 = base_score

T_start2 = 5.0
n_steps2 = 15000
cooling_rate2 = (T_end / T_start2) ** (1.0 / n_steps2)

accepted2 = 0
improved2 = 0
T = T_start2

for step in range(n_steps2):
    # Occasionally try swapping two codes (more dramatic change)
    if random.random() < 0.1 and len(unlocked) >= 2:
        # Swap two unlocked codes
        c1, c2 = random.sample(unlocked, 2)
        old1, old2 = current_mapping2[c1], current_mapping2[c2]
        current_mapping2[c1] = old2
        current_mapping2[c2] = old1
        new_score = decode_fast(current_mapping2)
        delta = new_score - current_score2
        if delta > 0 or random.random() < math.exp(delta / T):
            current_score2 = new_score
            accepted2 += 1
            if new_score > best_score2:
                best_score2 = new_score
                best_mapping2 = dict(current_mapping2)
                improved2 += 1
        else:
            current_mapping2[c1] = old1
            current_mapping2[c2] = old2
    else:
        code = random.choice(unlocked)
        old_letter = current_mapping2[code]
        new_letter = random.choice([l for l in LETTERS if l != old_letter])
        current_mapping2[code] = new_letter
        new_score = decode_fast(current_mapping2)
        delta = new_score - current_score2
        if delta > 0 or random.random() < math.exp(delta / T):
            current_score2 = new_score
            accepted2 += 1
            if new_score > best_score2:
                best_score2 = new_score
                best_mapping2 = dict(current_mapping2)
                improved2 += 1
        else:
            current_mapping2[code] = old_letter

    T *= cooling_rate2

    if (step + 1) % 3000 == 0:
        print(f"  Step {step+1:5d}: T={T:.4f}, current={current_score2:.4f}, "
              f"best={best_score2:.4f}")

print(f"\nAggressive SA complete.")
print(f"  Best score: {best_score2:.4f} (baseline: {base_score:.4f})")
print(f"  Delta: {best_score2 - base_score:+.4f}")

changes2 = []
for code in sorted(v7.keys(), key=int):
    if v7[code] != best_mapping2.get(code, v7[code]):
        changes2.append((code, v7[code], best_mapping2[code], code_counts.get(code, 0)))

if changes2:
    print(f"\n  Changes from V7:")
    for code, old, new, occ in changes2:
        print(f"    [{code}] {old} -> {new} ({occ} occ)")

    # Show a sample
    bpairs = book_pairs[5]
    text_old = ''.join(v7.get(p, '?') for p in bpairs)
    text_new = ''.join(best_mapping2.get(p, '?') for p in bpairs)
    print(f"\n  Book 5 V7: {text_old[:80]}...")
    print(f"  Book 5 SA: {text_new[:80]}...")
else:
    print("\n  No changes -- V7 is a true local optimum under this scoring!")
