"""
Apply high-confidence bigram-derived code assignments and decode.
Focus on assignments where the bigram evidence is overwhelming.
"""
import json
from collections import Counter

with open('books.json', 'r') as f:
    books = json.load(f)

confirmed = {
    '92': 'S', '88': 'T', '95': 'E', '21': 'I', '60': 'N',
    '56': 'E', '11': 'N', '45': 'D', '19': 'E',
    '26': 'E', '90': 'N', '31': 'A', '18': 'C', '06': 'H',
    '85': 'A', '61': 'U',
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

book_data = []
for book in books:
    off = get_offset(book)
    pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
    book_data.append((off, pairs))

all_pairs = []
for _, pairs in book_data:
    all_pairs.extend(pairs)
pair_counts = Counter(all_pairs)
total_pairs = sum(pair_counts.values())

# Build bigram evidence from confirmed codes
code_left = {}
code_right = {}
for _, pairs in book_data:
    for i in range(len(pairs) - 1):
        c1, c2 = pairs[i], pairs[i+1]
        if c2 not in confirmed and c1 in confirmed:
            code_left.setdefault(c2, Counter())[confirmed[c1]] += 1
        if c1 not in confirmed and c2 in confirmed:
            code_right.setdefault(c1, Counter())[confirmed[c2]] += 1

# Also build code-to-code bigrams for free codes
code_code_bigram = Counter()
for _, pairs in book_data:
    for i in range(len(pairs) - 1):
        code_code_bigram[(pairs[i], pairs[i+1])] += 1

print("=" * 70, flush=True)
print("HIGH-CONFIDENCE BIGRAM ASSIGNMENTS", flush=True)
print("=" * 70, flush=True)

# Tier 1: overwhelming evidence (single dominant bigram >80% of contexts)
tier1 = {}

# 00: left=C(56) out of freq=92. CH is THE German digraph.
# 56/92 = 60.9% of all occurrences follow C
tier1['00'] = ('H', 'CH bigram: C->00 56 times out of 92 total')

# 14: left=U(59) out of freq=106. UN is ubiquitous.
# 59/106 = 55.7% follow U
tier1['14'] = ('N', 'UN bigram: U->14 59 times out of 106 total')

# 72: left=E(40), right=U(41). ERx40 + RUx41 = massive evidence for R.
# Also A->72(10)=AR, T->72(9)=TR. All perfect R bigrams.
tier1['72'] = ('R', 'ER/RU/AR/TR bigrams: E>72x40, 72>Ux41')

# 91: right=C(51) out of freq=82. ?C in German: SC, IC, EC.
# 51/82 = 62% precede C. Given freq 82, this is S or I.
# Also: left=E(26)->E?->C pattern: ESC or EIC.
# German: EISCH, ESCHE, ESCH common -> 91=S very likely (SCH pattern)
# Also: 91 left=E(26), N(6), T(2) -> ES(26), NS(6), TS(2). All great S bigrams!
tier1['91'] = ('S', '91->Cx51 (SCH), E->91x26 (ES), N->91x6 (NS)')

# 15: left=D(12), E(6), S(1); right=E(31), A(5), C(1)
# D->15->E: DIE if 15=I! IE is top-5 German bigram.
# 31/77 = 40% precede E. DI(12) = common.
# But also SI(1)-> Hmm, let's check more:
# In the pre-STEIN context, 15 is at position -8 (8/10 times)
# Context: 42->15->95(E) -> 42,15,E. If 15=I -> ?IE (common!)
tier1['15'] = ('I', 'D->15(12)->E(31): DIE pattern, IE top bigram')

print(f"\nTier 1 assignments (strong bigram evidence):", flush=True)
for code, (letter, reason) in sorted(tier1.items()):
    freq = pair_counts.get(code, 0)
    print(f"  {code} -> {letter} (freq={freq}): {reason}", flush=True)

# Tier 2: good evidence, slightly less certain
tier2 = {}

# 76: left=D(21), A(15), I(13). DE(21), AE(15?), IE(13) all valid.
# But AE is rare in modern German. Unless word boundary: ...A | E...
# DE(21) and IE(13) are very strong.
# In 19-pair pattern: D,I,76 -> if 76=E -> DIE (perfect!)
# And [48],76,[51] at position 9-11: if 76=E -> ?EN pattern
tier2['76'] = ('E', 'DI->76->?: DIE pattern; D->76x21, I->76x13')

# 52: right=E(58) out of 126. 46% precede E.
# In DIESE hypothesis: 52=S. SE is common.
# But also: right=A(1), U(1) -> SA, SU less diagnostic
# If 76=E, then the 19-pair pattern has I,76=E,52,E = I,E,S,E = IESE (DIESE!)
# So this supports 52=S
tier2['52'] = ('S', 'In DIESE: I,E,52,E; 52->Ex58 (SE common)')

# 80: left=N(47) out of 79. 59% follow N!
# German N+?: ND(very common), NS, NG, NT, NE, NI, NA, NZ, NK, NR
# right=H(9), E(6), C(4) -> ?H, ?E, ?C
# If 80=D: ND(top bigram!) and DH(rare), DE(good), DC(rare)
# If 80=G: NG(common) and GH(rare), GE(common!), GC(no)
# If 80=S: NS(common) and SH(no), SE(common), SC(good)
# If 80=T: NT(common) and TH(rare in German), TE(good), TC(no)
# Hard to choose. N->80 is clear but the right context mixes things.
# Let's defer this one.

# 97: left=I(38) out of 58. 65% follow I!
# IS, IC, IE, IN, IG, IT all common.
# right=A(5), I(2), S(1)
# If 97=S: IS(very common, IST) and SA, SI both OK
# If 97=E: IE(very common) and EA, EI both OK
# If 97=N: IN(very common) and NA, NI both OK
# If 97=C: IC(common, NICHT) and CA(ok)
# Hard to distinguish. But IS->IST is a very common word.
# Also 97 appears right after STEIN in 1 occurrence. Let's defer.

# 48: right=E(35) out of 73. 48% precede E.
# left=E(11) -> E,48,E pattern.
# NE, RE, IE, SE all have E on left. If 48=N: ENE is common in German.
# Also in the 19-pair pattern: [46],48,[76=E] -> ?NE if 48=N? Or ?48,E
# Let's check: 48->E(35), 48->D(12). ND and NE are both very common for N!
# But 48 has left=E(11). EN is the #1 German bigram!
# So E->48->E gives ENE (common in ..ENEN, ..IENE, etc.)
# And E->48->D gives END (as in ENDE!)
tier2['48'] = ('N', 'E->48->E(35)/D(12): ENE/END patterns; left E(11)=EN')

# 57: left=C(11), H(9).
# C->57: CE (common: MACHEN->CE), or if 57=H -> CH (but 00=H already for CH!)
# H->57: HE (common), HI, HA, HT...
# If 57=H: CH(11) duplicates the CH pattern we gave to 00. Possible in homophonic.
# If 57=T: CT(unusual), HT(very common! NICHT, ACHT...)
# If 57=E: CE(common), HE(very common!)
# Right context: 57->E(18), 57->S(1).
# If 57=H: HE(18) is very common. HS not so much.
# If 57=T: TE(18) is common.
# If 57=E: EE(18) - rare in German.
# 57=H is supported by HE(18) and CH(11). H expects ~5 codes.
# 00=H and 57=H would give H two codes with total freq 92+102=194.
# German H frequency: 4.8% -> expected 0.048*5597=269. Two codes at 194 is short.
# 06=H(confirmed) at freq... let me check. Actually 06 is confirmed H with what freq?
# We'd need to check, but 3 H codes (06, 00, 57) is reasonable for ~4.7 codes expected.
tier2['57'] = ('H', 'C->57(11)+H->57(9): CH/HH; 57->E(18)=HE all common')

# 42: left=N(26), A(9) out of 56. N->42(46%!) and A->42(16%)
# NS, ND, NG, NT all common.
# right=C(8), E(1)
# If 42=D: ND(26 very common!), AD(9 ok), DC(8 uncommon in German)
# If 42=G: NG(26 common!), AG(9 common), GC(rare)
# If 42=S: NS(26 common), AS(9 ok), SC(8 good for SCH)
# If 42=T: NT(26 common), AT(9 ok), TC(rare)
# DC, GC, TC are all rare. SC is good (SCH).
# ND(26) is the strongest candidate. Let's check code 42 in context:
# In pre-STEIN: position -9 is 42 (8/10 times), followed by 15=I
# If 42=D: DI is common! If 42=G: GI is uncommon. If 42=S: SI is ok.
# N->42->I: NDI (in INDING?), NGI (rare), NSI (rare)
# NDI is most common.
tier2['42'] = ('D', 'N->42(26)=ND, A->42(9)=AD, 42->I(via 15)=DI')

# 34: right=A(29) out of 107. 27% precede A.
# left=E(4), D(1).
# If 34=N: NA(29 common), EN(4 top bigram!), DN(rare)
# If 34=D: DA(29 common), ED(4 ok), DD(rare)
# If 34=H: HA(29 common), EH(4 ok), DH(rare)
# If 34=L: LA(29 common), EL(4 common), DL(rare)
# Hard to distinguish just from bigrams. Let's check frequency:
# 34 has freq 107. N expects ~9.6 codes, D expects ~5 codes, H expects ~4.7
# N: 60,11,90 confirmed (3 codes). 14 tier1=N (4 codes). If 51=N and 34=N -> 6 N-codes.
# That's about 6/9.6 ≈ 63% of expected N-codes.
# With freq 107, code 34 has high count consistent with common letter.

# 04: left=E(13), D(5). Right=I(28) out of 58. 48% precede I!
# If 04=M: MI(28 common), EM(13 very common), DM(rare)
# If 04=S: SI(28 ok), ES(13 common), DS(rare)
# If 04=N: NI(28 common), EN(13 top bigram!), DN(rare)
# If 04=L: LI(28 ok), EL(13 common), DL(rare)
# EM and MI suggest M! But EN and NI also work for N.
# Code 04 freq=58. M expects ~2.5 codes. E->04->I at 13+28 = strong.
# If 04=M: total M count would be ~58 for one code. M expected: 0.025*5597=140.
# Need ~2-3 M codes at ~47-70 each. 04=M at 58 is reasonable.

tier2['04'] = ('M', 'E->04(13)=EM, 04->I(28)=MI both common German bigrams')

# 46: left=E(17), N(6), H(1); right=N(15), T(7), E(3)
# If 46=I: EI(17 very common!), NI(6 common), HI(1 ok)
#          IN(15 very common!), IT(7 common), IE(3 common)
# This is extremely strong evidence for I!
# EI and IN are both top-10 German bigrams.
tier2['46'] = ('I', 'E->46(17)=EI, N->46(6)=NI; 46->N(15)=IN, 46->T(7)=IT')

# 12: left=E(9), U(3), I(3); right=T(30), N(7), A(6)
# If 12=S: ES(9), US(3), IS(3); ST(30 very common!), SN(7 rare), SA(6 ok)
# ST(30) is the #1 signal. And ES(9), US(3), IS(3) all good S bigrams.
# SN is rare though. Unless word boundary: ...S | N...
# If 12=H: EH(9), UH(3), IH(3 very rare); HT(30 rare), HN(7 rare), HA(6)
# If 12=C: EC(9), UC(3), IC(3); CT(30 no), CN(7 no)
# 12=S is by far the best. ST(30) is massive evidence.
tier2['12'] = ('S', '12->T(30)=ST!, E->12(9)=ES, U->12(3)=US, I->12(3)=IS')

# 58: left=I(20), H(6); right=D(12), N(5), E(3)
# If 58=C: IC(20 common, NICHT!), HC(6 rare in German)
#          CD(12 no), CN(5 no) -> right context doesn't fit C
# If 58=N: IN(20 very common!), HN(6 rare)
#          ND(12 common), NN(5 ok), NE(3 common)
# If 58=E: IE(20 very common!), HE(6 common)
#          ED(12 ok), EN(5 top bigram), EE(3 rare)
# If 58=S: IS(20 common), HS(6 rare)
#          SD(12 rare), SN(5 rare) -> bad right context
# IN(20)+ND(12) or IE(20)+ED(12)?
# I->58(20) is strong. 58->D(12) favors N (ND) over E (ED, uncommon).
# Also H->58(6): HN is rare, HE is common -> 58=E slightly favored by left H.
# But overall, I->58 + 58->D -> IN+ND = 58=N is strongest.
# Hmm but that conflicts with having too many N codes...
# Let me check: confirmed N: 60,11,90 (3). tier1 N: 14 (4). tier2 N: 48 (5).
# If 58=N: 6 N-codes. Expected ~9.6. Still room.
# If 58=E: confirmed E: 95,56,19,26 (4). tier2 E: 76 (5). If 58=E: 6 E-codes.
# Expected ~16 E-codes. Still lots of room.
# Let me check the 19-pair pattern. Code 58 doesn't appear in it.
# Let me lean towards N for now based on IN+ND being stronger than IE+ED.
tier2['58'] = ('N', 'I->58(20)=IN, 58->D(12)=ND both top bigrams')

print(f"\nTier 2 assignments (good bigram evidence):", flush=True)
for code, (letter, reason) in sorted(tier2.items()):
    freq = pair_counts.get(code, 0)
    print(f"  {code} -> {letter} (freq={freq}): {reason}", flush=True)

# Build combined mapping
mapping = dict(confirmed)
for code, (letter, _) in tier1.items():
    mapping[code] = letter
for code, (letter, _) in tier2.items():
    mapping[code] = letter

print(f"\n\n{'='*70}", flush=True)
print("DECODE WITH BIGRAM-DERIVED MAPPING", flush=True)
print("=" * 70, flush=True)

# Check letter frequencies with this mapping
letter_freq = Counter()
for pair, count in pair_counts.items():
    if pair in mapping:
        letter_freq[mapping[pair]] += count

print(f"\nLetter frequencies ({sum(letter_freq.values())}/{total_pairs} pairs mapped):", flush=True)
german_freq = {
    'E': 0.164, 'N': 0.098, 'I': 0.076, 'S': 0.073, 'R': 0.070,
    'A': 0.065, 'T': 0.062, 'D': 0.051, 'H': 0.048, 'U': 0.042,
    'L': 0.034, 'C': 0.031, 'G': 0.030, 'M': 0.025, 'O': 0.025,
    'B': 0.019, 'W': 0.019, 'F': 0.017, 'K': 0.012, 'Z': 0.011,
    'P': 0.008, 'V': 0.007, 'J': 0.003, 'Y': 0.001, 'X': 0.001,
    'Q': 0.001
}
mapped_total = sum(letter_freq.values())
for letter in sorted(german_freq, key=lambda l: -german_freq[l]):
    obs = letter_freq.get(letter, 0) / mapped_total * 100 if mapped_total > 0 else 0
    exp = german_freq[letter] * 100
    codes = [c for c, l in mapping.items() if l == letter]
    delta = obs - exp
    flag = " <<<" if abs(delta) > 2.0 else ""
    print(f"  {letter}: {obs:5.1f}% (exp {exp:.1f}%, delta {delta:+.1f}%) codes={codes}{flag}", flush=True)

# Decode books
print(f"\n\n{'='*70}", flush=True)
print("DECODED BOOKS (longest first)", flush=True)
print("=" * 70, flush=True)

book_decoded = []
for i, (off, pairs) in enumerate(book_data):
    decoded = ''.join(mapping.get(p, '?') for p in pairs)
    book_decoded.append((i, decoded, off))

book_decoded.sort(key=lambda x: -len(x[1]))
for idx, decoded, off in book_decoded[:15]:
    print(f"\n  Book {idx} (off={off}, {len(decoded)} letters):", flush=True)
    for j in range(0, len(decoded), 80):
        print(f"    {decoded[j:j+80]}", flush=True)

# Count German words
german_words = [
    'RUNENSTEIN', 'RUNENSTEINEN', 'STEINEN', 'STEINE',
    'NICHT', 'EINER', 'EINEN', 'DIESE', 'DIESER',
    'WERDEN', 'WURDE', 'WAREN', 'HABEN',
    'STEIN', 'RUNE', 'RUNEN', 'AUCH',
    'NACH', 'NOCH', 'WENN', 'DANN',
    'ABER', 'ODER', 'ALLE', 'WELT',
    'SICH', 'SIND', 'DASS',
    'ENDE', 'HABE', 'KANN', 'WIRD',
    'DER', 'DIE', 'DAS', 'UND',
    'IST', 'EIN', 'DEN', 'DEM',
    'VON', 'HAT', 'AUF', 'MIT',
    'DES', 'SIE', 'ICH', 'AUS',
    'BEI', 'WIR', 'NUR', 'EINE',
    'NICHT', 'SEIN', 'HIER', 'IHRE',
    'JEDE', 'JEDER', 'VIELE', 'MEHR',
    'DURCH', 'GEGEN', 'UNTER', 'UEBER',
    'SCHRIFT', 'SPRACHE', 'ZEICHEN',
    'BONELORD', 'BONELORDS',
    'AUGE', 'AUGEN', 'FEUER',
    'DUNKEL', 'LICHT', 'LEBEN',
    'MACHT', 'KRAFT', 'GEIST',
]

full_text = ''.join(d for _, d, _ in book_decoded)
print(f"\n\n{'='*70}", flush=True)
print("GERMAN WORD HITS", flush=True)
print("=" * 70, flush=True)

for word in sorted(german_words, key=lambda w: -len(w)):
    c = full_text.count(word)
    if c > 0:
        print(f"  '{word}': {c} times", flush=True)

# Focus on the 19-pair pattern
print(f"\n\n{'='*70}", flush=True)
print("19-PAIR RECURRING PATTERN DECODED", flush=True)
print("=" * 70, flush=True)

target_codes = ['45','21','76','52','19','72','78','30','46','48','76','51','59','56','46','11','41','45','19']
decoded_pattern = ''.join(mapping.get(c, '?') for c in target_codes)
print(f"  Codes: {target_codes}", flush=True)
print(f"  Decoded: {decoded_pattern}", flush=True)

# Pre-STEIN decoded
pre_stein = ['15','95','61','51','35','34','78','01']
pre_decoded = ''.join(mapping.get(c, '?') for c in pre_stein)
print(f"\n  Pre-STEIN codes: {pre_stein}", flush=True)
print(f"  Pre-STEIN decoded: {pre_decoded}", flush=True)

# Full STEIN context
full_stein = ['42','15','95','61','51','35','34','78','01','92','88','95','21','60','19','93','64','67','24','31','42','78']
full_decoded = ''.join(mapping.get(c, '?') for c in full_stein)
print(f"\n  Full STEIN context: {full_stein}", flush=True)
print(f"  Full decoded: {full_decoded}", flush=True)

# Even further back
far_context = ['74','45','45','19','04','50','42','15','95','61','51','35','34','78','01','92','88','95','21','60','19','93','64','67','24','31','42','78','94','31','51','91','18','65','12']
far_decoded = ''.join(mapping.get(c, '?') for c in far_context)
print(f"\n  Extended context: {far_context}", flush=True)
print(f"  Extended decoded: {far_decoded}", flush=True)

print(f"\n\n{'='*70}", flush=True)
print("DONE", flush=True)
print("=" * 70, flush=True)
