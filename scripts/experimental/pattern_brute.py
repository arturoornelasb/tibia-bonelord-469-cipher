"""
Brute-force the key patterns by trying top candidate letters
for each unknown position, then scoring by German word matches.
"""
import json
from collections import Counter
from itertools import product

with open('books.json', 'r') as f:
    books = json.load(f)

# Known assignments
known = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U',
    '00': 'H', '14': 'N', '72': 'R', '91': 'S', '15': 'I',
    '76': 'E', '52': 'S', '42': 'D', '46': 'I', '48': 'N',
    '57': 'H', '04': 'M', '12': 'S', '58': 'N',
}

# German words for validation
german_words = set([
    'DER', 'DIE', 'DAS', 'UND', 'IST', 'EIN', 'EINE', 'EINEN', 'EINER',
    'DEN', 'DEM', 'DES', 'VON', 'HAT', 'AUF', 'MIT', 'SICH', 'SIND',
    'NICHT', 'STEIN', 'STEINE', 'STEINEN', 'RUNE', 'RUNEN',
    'DIESER', 'DIESE', 'DIESES', 'DIESEM', 'DIESEN',
    'NACH', 'NOCH', 'AUCH', 'ABER', 'ODER', 'ALLE', 'WENN', 'DANN',
    'WERDEN', 'WURDE', 'HABEN', 'HABE', 'KANN', 'WIRD',
    'SEIN', 'SEINE', 'SEINEN', 'SEINER', 'SEINES', 'SEINEM',
    'DURCH', 'GEGEN', 'UNTER', 'UEBER', 'HINTER', 'ZWISCHEN',
    'HIER', 'IHRE', 'IHREN', 'IHRER', 'IHREM',
    'SCHRIFT', 'SPRACHE', 'ZEICHEN', 'MACHT', 'KRAFT', 'GEIST',
    'LEBEN', 'LICHT', 'DUNKEL', 'FEUER', 'AUGE', 'AUGEN',
    'ANDERE', 'ANDEREN', 'ANDERER', 'ANDERES',
    'KONNTE', 'MUSSTE', 'SOLLTE', 'WOLLTE',
    'IMMER', 'WIEDER', 'SCHON', 'NICHTS',
    'KLEINEN', 'KLEINE', 'KLEINER', 'KLEINES',
    'ALTEN', 'ALTE', 'ALTER', 'ALTES',
    'NEUEN', 'NEUE', 'NEUER', 'NEUES',
    'GROSSEN', 'GROSSE', 'GROSSER', 'GROSSES',
    'ERSTEN', 'ERSTE', 'ERSTER', 'ERSTES',
    'LETZTEN', 'LETZTE', 'LETZTER', 'LETZTES',
    'URALTE', 'URALTEN', 'URALTER', 'URALTES',
    'GEMEINDE', 'FREUNDE', 'FEINDE',
    'RUNENSTEIN', 'RUNENSTEINEN', 'RUNENSTEINE',
    'SCHON', 'SEHR', 'JEDE', 'JEDER', 'JEDES', 'JEDEM', 'JEDEN',
    'WELT', 'ZEIT', 'TEIL', 'SEITE', 'STELLE', 'STELLEN',
    'INSCHRIFT', 'INSCHRIFTEN',
    'SCHREIBEN', 'LESEN', 'FINDEN', 'SEHEN', 'GEBEN',
    'EINIGE', 'EINIGEN', 'EINIGER',
    'WELCHE', 'WELCHEN', 'WELCHER', 'WELCHES',
    'SOLCHE', 'SOLCHEN', 'SOLCHER',
    'JENE', 'JENEN', 'JENER', 'JENES',
    # Tibia-related
    'BONELORD', 'BEHOLDER', 'HELLGATE', 'BIBLIOTHEK',
    'GEHEIMNIS', 'GEHEIME', 'GEHEIMEN',
    'MAGIC', 'MAGIE', 'ZAUBER', 'FLUCH',
    'MACHT', 'WISSEN', 'KENNEN', 'VERSTEHEN',
])

# Common German bigrams for scoring
german_bigrams = {
    'EN': 3.88, 'ER': 3.75, 'CH': 2.75, 'DE': 2.00, 'EI': 1.88,
    'ND': 1.88, 'TE': 1.67, 'IN': 1.65, 'IE': 1.64, 'GE': 1.43,
    'ES': 1.36, 'NE': 1.26, 'SE': 1.20, 'RE': 1.18, 'HE': 1.16,
    'AN': 1.14, 'UN': 1.14, 'ST': 1.13, 'BE': 1.06, 'DI': 0.98,
    'EM': 0.93, 'AU': 0.93, 'SC': 0.86, 'DA': 0.86, 'SI': 0.82,
    'LE': 0.82, 'IC': 0.81, 'TI': 0.73, 'AL': 0.71, 'HA': 0.71,
    'NG': 0.67, 'WE': 0.65, 'EL': 0.65, 'HI': 0.58, 'NS': 0.57,
    'NT': 0.56, 'IS': 0.55, 'HT': 0.54, 'MI': 0.52, 'IT': 0.50,
    'RI': 0.41, 'AB': 0.38, 'LI': 0.35, 'ED': 0.35, 'EG': 0.34,
    'NI': 0.33, 'ET': 0.33, 'IG': 0.32, 'AR': 0.31, 'RU': 0.30,
}

def bigram_score(text):
    score = 0
    for i in range(len(text)-1):
        bg = text[i:i+2]
        if bg in german_bigrams:
            score += german_bigrams[bg]
    return score

def word_matches(text):
    matches = []
    for word in german_words:
        if word in text:
            matches.append(word)
    return matches

# ============================================
# PATTERN 1: 19-pair recurring pattern
# ============================================
print("=" * 70)
print("PATTERN 1: 19-PAIR RECURRING (13 books)")
print("=" * 70)

pattern1_codes = ['45','21','76','52','19','72','78','30','46','48','76','51','59','56','46','11','41','45','19']
# Known: D  I  E  S  E  R  ?   ?  I  N  E  ?   ?  E  I  N  ?  D  E
# Unknowns at positions 6,7,11,12,16 (0-indexed)

# Top candidates from bigram analysis:
candidates_78 = ['E', 'I', 'U', 'A', 'C']  # position 6
candidates_30 = ['E', 'H', 'N', 'D', 'S']  # position 7
candidates_51 = ['E', 'N', 'I', 'S', 'G']  # position 11
candidates_59 = ['N', 'I', 'S', 'T', 'D']  # position 12
candidates_41 = ['E', 'D', 'N', 'G', 'S']  # position 16

best_score = -1
best_text = ''
best_combo = None
results = []

for c78, c30, c51, c59, c41 in product(candidates_78, candidates_30, candidates_51, candidates_59, candidates_41):
    text = f'D I E S E R {c78} {c30} I N E {c51} {c59} E I N {c41} D E'.replace(' ', '')
    bs = bigram_score(text)
    words = word_matches(text)
    word_len_score = sum(len(w) for w in words)
    total = bs + word_len_score * 2
    results.append((total, bs, words, text, c78, c30, c51, c59, c41))

results.sort(key=lambda x: -x[0])
print("\nTop 20 solutions for 19-pair pattern:")
for i, (total, bs, words, text, c78, c30, c51, c59, c41) in enumerate(results[:20]):
    print(f"  {i+1}. {text}  (score={total:.1f}, bigrams={bs:.1f})")
    print(f"     78={c78}, 30={c30}, 51={c51}, 59={c59}, 41={c41}")
    print(f"     Words: {words}")
    print()


# ============================================
# PATTERN 2: Pre-STEIN context
# ============================================
print("\n" + "=" * 70)
print("PATTERN 2: PRE-STEIN CONTEXT")
print("=" * 70)

# Extended: [74],D,D,E,M,[50],D,I,E,U,[51],[35],[34],[78],[01],S,T,E,I,N
# Then: E,[93],[64],[67],[24],A,D,[78],[94],A,[51],S,C,[65],S

# Focus on: EU[51][35][34][78][01]STEIN
pre_codes = ['61','51','35','34','78','01']
# Known: U, ?, ?, ?, ?, ?

candidates_pre = {
    '51': ['E', 'N', 'I', 'S', 'G', 'R'],
    '35': ['I', 'N', 'A', 'E', 'R', 'L'],
    '34': ['D', 'E', 'N', 'H', 'I', 'L', 'T'],
    '78': ['E', 'I', 'U', 'A', 'T'],
    '01': ['E', 'I', 'S', 'N', 'H'],
}

best_results = []
for c51 in candidates_pre['51']:
    for c35 in candidates_pre['35']:
        for c34 in candidates_pre['34']:
            for c78 in candidates_pre['78']:
                for c01 in candidates_pre['01']:
                    text = f'U{c51}{c35}{c34}{c78}{c01}STEIN'
                    bs = bigram_score(text)
                    words = word_matches(text)
                    word_len_score = sum(len(w) for w in words)
                    total = bs + word_len_score * 2
                    best_results.append((total, bs, words, text, c51, c35, c34, c78, c01))

best_results.sort(key=lambda x: -x[0])
print("\nTop 20 solutions for pre-STEIN (U?????STEIN):")
for i, (total, bs, words, text, c51, c35, c34, c78, c01) in enumerate(best_results[:20]):
    print(f"  {i+1}. {text}  (score={total:.1f}, bigrams={bs:.1f})")
    print(f"     51={c51}, 35={c35}, 34={c34}, 78={c78}, 01={c01}")
    print(f"     Words: {words}")
    print()


# ============================================
# PATTERN 3: Full extended context
# ============================================
print("\n" + "=" * 70)
print("PATTERN 3: FULL EXTENDED STEIN CONTEXT")
print("=" * 70)

# [74],D,D,E,M,[50],D,I,E,U,[51],[35],[34],[78],[01],S,T,E,I,N,E,[93],[64],[67],[24],A,D,[78],[94],A,[51],S,C,[65],S
# Extra unknowns: 74, 50, 93, 64, 67, 24, 94, 65

# Let me add best candidates for these too
candidates_74 = ['E', 'N', 'T']  # H->74(58%), top=E(ND pattern)
candidates_50 = ['N', 'E', 'I']  # M->50(31%), 50->D(29%)
candidates_93 = ['N', 'I', 'S']  # E->93(100%), 93->64(100%)
candidates_64 = ['E', 'T', 'D', 'S']
candidates_67 = ['E', 'D', 'S', 'T']
candidates_24 = ['D', 'H', 'N']  # weak evidence
candidates_94 = ['H', 'D', 'N']  # C->94(28%) => CH strong
candidates_65 = ['E', 'I', 'T']  # H->65(68%)

# This is too many combinations. Let me fix some:
# 78=E (strongest evidence), 94=H (CH pattern), 41=E
# Then vary the rest

# Check with 78=E, 94=H, 41=E:
print("With 78=E, 94=H (from C->94=CH), 41=E:")
print()

for c51 in ['E', 'N', 'I', 'S', 'G', 'R']:
    for c35 in ['I', 'N', 'A', 'E', 'R']:
        for c34 in ['D', 'E', 'N', 'H', 'L', 'T']:
            for c01 in ['E', 'I', 'S', 'N']:
                text = f'U{c51}{c35}{c34}E{c01}STEIN'
                bs = bigram_score(text)
                words = word_matches(text)
                word_len_score = sum(len(w) for w in words)

                # Also check 19-pair with same codes
                for c30 in ['E', 'H', 'N', 'D', 'S']:
                    for c59 in ['N', 'I', 'S', 'T']:
                        text19 = f'DIESERE{c30}INE{c51}{c59}EINEДЕ'.replace('Д', 'D')
                        text19 = f'DIESERE{c30}INE{c51}{c59}EINEDE'
                        bs19 = bigram_score(text19)
                        words19 = word_matches(text19)
                        wl19 = sum(len(w) for w in words19)

                        combined = bs + word_len_score * 2 + bs19 + wl19 * 2
                        if combined > 50:  # threshold
                            pass  # too many to print

# Simpler: just do pre-STEIN with 78=E fixed
print("Pre-STEIN with 78=E fixed:")
best = []
for c51 in ['E', 'N', 'I', 'S', 'G', 'R']:
    for c35 in ['I', 'N', 'A', 'E', 'R', 'L']:
        for c34 in ['D', 'E', 'N', 'H', 'I', 'L', 'T']:
            for c01 in ['E', 'I', 'S', 'N', 'H']:
                text = f'U{c51}{c35}{c34}E{c01}STEIN'
                bs = bigram_score(text)
                words = word_matches(text)
                wl = sum(len(w) for w in words)
                total = bs + wl * 3
                best.append((total, text, c51, c35, c34, c01, words))

best.sort(key=lambda x: -x[0])
for i, (total, text, c51, c35, c34, c01, words) in enumerate(best[:15]):
    print(f"  {i+1}. {text}  (score={total:.1f}, 51={c51} 35={c35} 34={c34} 01={c01})")
    print(f"     Words: {words}")


# ============================================
# PATTERN 4: Post-STEIN with 78=E, 94=H
# ============================================
print(f"\n\n{'='*70}")
print("PATTERN 4: POST-STEIN CONTEXT")
print("=" * 70)
# STEINE,[93],[64],[67],[24],A,D,E,H,A,[51],S,C,[65],S

# With 94=H:
for c93 in ['N', 'I', 'S', 'M', 'L']:
    for c64 in ['E', 'T', 'D', 'S', 'G']:
        for c67 in ['E', 'D', 'S', 'T', 'R']:
            for c24 in ['D', 'H', 'N', 'L', 'M']:
                for c51 in ['E', 'N', 'I', 'S', 'G', 'R']:
                    for c65 in ['E', 'I', 'T', 'A']:
                        text = f'STEINE{c93}{c64}{c67}{c24}ADEHA{c51}SC{c65}S'
                        words = word_matches(text)
                        wl = sum(len(w) for w in words)
                        if wl >= 10:  # only interesting results
                            bs = bigram_score(text)
                            total = bs + wl * 3
                            print(f"  {text}  score={total:.1f} 93={c93} 64={c64} 67={c67} 24={c24} 51={c51} 65={c65}")
                            print(f"    Words: {words}")


print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
