"""
Session 10 - Attack the garbled core: WRLGTNELNRHELUIRUNN
This 19-char sequence between STEH and HWND appears 8+ times.
Strategy:
1. Extract exact code sequence and all contexts
2. Try MHG/OHG segmentation with expanded vocabulary
3. Look for embedded words at every offset
4. Analyze code repetition patterns for morpheme boundaries
5. Try reversals, anagram decomposition
6. Cross-reference with Tibia lore
"""
import json, re
from collections import Counter

with open('data/books.json') as f:
    raw_books = json.load(f)
with open('data/final_mapping_v4.json') as f:
    mapping = json.load(f)

def parse_codes(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]

books = [parse_codes(b) for b in raw_books]

rev = {}
for code, letter in mapping.items():
    rev.setdefault(letter, []).append(code)

def decode(codes):
    return ''.join(mapping.get(c, '?') for c in codes)

def collapse(text):
    if not text: return text
    r = [text[0]]
    for c in text[1:]:
        if c != r[-1]: r.append(c)
    return ''.join(r)

print("=" * 80)
print("SESSION 10: ATTACKING THE GARBLED CORE")
print("=" * 80)

# ============================================================
# 1. Find all occurrences of STEH...HWND pattern
# ============================================================
print("\n1. ALL STEH...HWND OCCURRENCES")
print("-" * 60)

steh_hwnd_contexts = []
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    # Look for STEH followed by HWND within 30 chars
    for idx in range(len(decoded) - 4):
        if decoded[idx:idx+4] == 'STEH':
            rest = decoded[idx+4:idx+35]
            hwnd_pos = rest.find('HWND')
            if hwnd_pos >= 0:
                garbled = rest[:hwnd_pos]
                full = decoded[idx:idx+4+hwnd_pos+4]
                codes_here = book_codes[idx:idx+4+hwnd_pos+4]
                steh_hwnd_contexts.append((bi, idx, garbled, full, codes_here))

print(f"  Found {len(steh_hwnd_contexts)} STEH...HWND patterns")
for bi, idx, garbled, full, codes in steh_hwnd_contexts[:10]:
    print(f"  Book {bi:2d} pos {idx:3d}: {full}")
    print(f"    garbled core: '{garbled}' ({len(garbled)} chars)")

# Get the canonical garbled core
if steh_hwnd_contexts:
    garbled_cores = Counter(ctx[2] for ctx in steh_hwnd_contexts)
    print(f"\n  Unique garbled cores: {len(garbled_cores)}")
    for core, cnt in garbled_cores.most_common(5):
        print(f"    x{cnt}: '{core}' ({len(core)} chars)")

# ============================================================
# 2. Code-level analysis of the garbled core
# ============================================================
print(f"\n{'='*60}")
print("2. CODE-LEVEL ANALYSIS")
print("=" * 60)

# Get the most common garbled core's codes
if steh_hwnd_contexts:
    # Take first occurrence
    bi0, idx0, garbled0, full0, codes0 = steh_hwnd_contexts[0]
    # Extract just the garbled part codes (after STEH, before HWND)
    steh_len = 4
    garbled_codes = codes0[steh_len:steh_len+len(garbled0)]

    print(f"\n  Garbled: {garbled0}")
    print(f"  Length: {len(garbled0)} chars")
    print(f"  Codes: {garbled_codes}")
    print(f"\n  Position-by-position:")
    for j, c in enumerate(garbled_codes):
        letter = mapping.get(c, '?')
        # Count how many total uses this code has
        total = sum(1 for b in books for x in b if x == c)
        print(f"    pos {j:2d}: code {c:2s} = {letter} (used {total}x total)")

    # Look for repeating code subsequences
    print(f"\n  Repeating code patterns (length 2-5):")
    for plen in range(2, 6):
        patterns = Counter()
        for i in range(len(garbled_codes) - plen + 1):
            sub = tuple(garbled_codes[i:i+plen])
            patterns[sub] += 1
        repeats = {k: v for k, v in patterns.items() if v > 1}
        if repeats:
            for pat, cnt in sorted(repeats.items(), key=lambda x: -x[1]):
                decoded_pat = ''.join(mapping.get(c, '?') for c in pat)
                print(f"      {pat} = '{decoded_pat}' x{cnt}")

# ============================================================
# 3. MHG/OHG expanded vocabulary scan
# ============================================================
print(f"\n{'='*60}")
print("3. EXPANDED MHG/OHG VOCABULARY SCAN")
print("=" * 60)

# Extended Middle High German / Old High German word list
mhg_words = {
    # Common MHG words not in modern German
    'wol': 'well/indeed', 'daz': 'that', 'ouch': 'also',
    'siner': 'his', 'ir': 'their/her', 'min': 'my',
    'niht': 'not', 'niut': 'nothing', 'als': 'as',
    'vil': 'very', 'wart': 'became', 'wer': 'who',
    'vrowe': 'lady', 'ritter': 'knight', 'kunic': 'king',
    'swert': 'sword', 'helm': 'helmet', 'schilt': 'shield',
    'burc': 'castle', 'lant': 'land', 'stat': 'city',
    'stein': 'stone', 'alt': 'old', 'elt': 'old (comp)',
    'gros': 'great', 'gut': 'good', 'heil': 'salvation',
    'heilig': 'holy', 'erde': 'earth', 'himel': 'heaven',
    'tot': 'death', 'leben': 'life', 'zit': 'time',
    'naht': 'night', 'tac': 'day', 'gelt': 'money',
    'ere': 'honor', 'tugent': 'virtue', 'leit': 'suffering',
    'minne': 'love', 'muot': 'courage', 'craft': 'power',
    'list': 'cunning', 'wunder': 'wonder', 'wunne': 'joy',
    'run': 'rune', 'rune': 'rune', 'runen': 'runes',
    # Verbs in MHG
    'sol': 'shall', 'wil': 'wants', 'mac': 'may',
    'tuon': 'to do', 'gan': 'to go', 'sten': 'to stand',
    'liegen': 'to lie', 'sagen': 'to say', 'weln': 'to choose',
    'heizen': 'to be called', 'wizzen': 'to know',
    'vinden': 'to find', 'binden': 'to bind',
    'winden': 'to wind', 'riten': 'to ride',
    'striten': 'to fight', 'sniden': 'to cut',
    'schinen': 'to shine', 'legen': 'to lay',
    'setzen': 'to set', 'nemen': 'to take',
    'geben': 'to give', 'sehen': 'to see',
    'lesen': 'to read', 'sprechen': 'to speak',
    'helfen': 'to help', 'sterben': 'to die',
    'werfen': 'to throw', 'werden': 'to become',
    'tragen': 'to carry', 'graben': 'to dig',
    'schaffen': 'to create', 'halten': 'to hold',
    # OHG specific
    'wini': 'friend (OHG)', 'runa': 'rune/secret (OHG)',
    'runstab': 'rune-staff', 'hrunen': 'to whisper/rune',
    'lune': 'shelter', 'elni': 'foreign',
    'welt': 'world', 'elt': 'age',
    # Prepositions/particles
    'hin': 'thither', 'her': 'hither',
    'neln': 'not at all?', 'elne': 'foreign',
    'gelt': 'tribute', 'hel': 'hell/bright',
    'heln': 'to conceal', 'heler': 'concealer',
    'helung': 'concealment',
    'helu': 'concealing', 'helui': '?concealing-?',
    'werg': 'tow/hemp', 'werk': 'work',
    'elt': 'world/age', 'eltern': 'parents',
    'neln': '?', 'nel': '?',
    'iru': 'their (OHG dat)', 'irun': 'their (OHG)',
    'gel': 'yellow', 'geln': 'to yell',
    'teln': 'to share/deal', 'ellu': 'all (OHG)',
    # More MHG vocabulary
    'urliuge': 'war', 'urluge': 'war',
    'helden': 'heroes', 'helt': 'hero',
    'ritter': 'knight', 'riter': 'knight (MHG)',
    'herr': 'lord', 'herre': 'lord (MHG)',
    'knecht': 'servant', 'kneht': 'servant (MHG)',
    'gir': 'greedy', 'girheit': 'greed',
    'nit': 'envy', 'niid': 'envy (MHG)',
    'lig': 'lie', 'ligen': 'to lie',
    'hel': 'bright/Hell', 'helle': 'Hell (MHG)',
    # Words with W-R-L-G-T-N-E that could form in our garbled section
    'welt': 'world', 'welten': 'worlds',
    'gelten': 'to pay/be worth', 'gelt': 'money',
    'eln': 'ell (measure)', 'elne': 'foreign',
    'nel': '?reversed len?',
    'reh': 'deer', 'reht': 'right/law',
    'gern': 'gladly', 'gerne': 'gladly (MHG)',
    'lern': 'learn', 'lernen': 'to learn',
    'gelt': 'tribute', 'gelte': 'vessel',
    'wer': 'who', 'wern': 'to defend',
    'nern': 'to save', 'nerung': 'salvation',
    'elui': '?', 'eluirun': '?',
    'irn': 'their (OHG gen pl)', 'iren': 'their',
    # Tibia-relevant
    'drache': 'dragon', 'wurm': 'worm/dragon',
    'trol': 'troll', 'ork': 'orc',
    'geist': 'spirit', 'geister': 'spirits',
    'knochen': 'bones', 'knoch': 'bone',
    'herr': 'lord', 'meister': 'master',
    'ruine': 'ruin', 'turm': 'tower',
    'gruft': 'crypt', 'hort': 'treasure/hoard',
}

if steh_hwnd_contexts:
    garbled = steh_hwnd_contexts[0][2].upper()
    collapsed = collapse(garbled)

    print(f"\n  Garbled: {garbled}")
    print(f"  Collapsed: {collapsed}")

    # Try finding MHG words at every offset
    print(f"\n  MHG/OHG words found within garbled core:")
    found_words = []
    for wlen in range(2, min(len(garbled)+1, 12)):
        for start in range(len(garbled) - wlen + 1):
            substr = garbled[start:start+wlen].lower()
            if substr in mhg_words:
                meaning = mhg_words[substr]
                found_words.append((start, wlen, substr, meaning))
                print(f"    pos {start}-{start+wlen}: {substr.upper()} = {meaning}")

    # Also try on collapsed version
    print(f"\n  In collapsed version ({collapsed}):")
    for wlen in range(2, min(len(collapsed)+1, 12)):
        for start in range(len(collapsed) - wlen + 1):
            substr = collapsed[start:start+wlen].lower()
            if substr in mhg_words:
                meaning = mhg_words[substr]
                print(f"    pos {start}-{start+wlen}: {substr.upper()} = {meaning}")

# ============================================================
# 4. Try every possible 2-word split
# ============================================================
print(f"\n{'='*60}")
print("4. SYSTEMATIC SEGMENTATION ATTEMPTS")
print("=" * 60)

if steh_hwnd_contexts:
    garbled = steh_hwnd_contexts[0][2].upper()

    # German word set (expanded with MHG)
    all_words = set()
    for w in mhg_words:
        all_words.add(w.upper())
    # Add common modern German
    modern_de = [
        'AB', 'ABER', 'ALS', 'ALT', 'ALTE', 'ALTEN', 'AM', 'AN', 'AUF', 'AUS',
        'BEI', 'BIS', 'DA', 'DAS', 'DEM', 'DEN', 'DER', 'DES', 'DIE', 'DIES',
        'DIESER', 'DIR', 'DURCH', 'EIN', 'EINE', 'EINEM', 'EINEN', 'EINER',
        'ER', 'ERST', 'ERSTE', 'ES', 'FACH', 'FINDEN', 'FORT', 'GAR', 'GEH',
        'HAT', 'HIER', 'ICH', 'IHN', 'IHR', 'IN', 'IST', 'KOENIG', 'NACH',
        'NEU', 'NUN', 'ODE', 'ORT', 'RUIN', 'RUNE', 'RUNEN', 'SCHAUN',
        'SEE', 'SEI', 'SEID', 'SEIN', 'SEINE', 'SIE', 'SO', 'STEH', 'STEIN',
        'STEINE', 'TAG', 'TUN', 'UND', 'UNTER', 'URALTE', 'VIEL', 'VON',
        'WEG', 'WER', 'WIR', 'WISSET', 'WOHL',
        # Additional words
        'WELT', 'GELT', 'HELD', 'HELDEN', 'ERDE', 'LEID', 'NEID',
        'WILD', 'LEER', 'GERN', 'FERN', 'KERN', 'STERN', 'TURN',
        'WUNNE', 'WUNDER', 'HEIL', 'TEIL', 'WEIL',
        'NUR', 'NICHT', 'NOCH', 'EWIG', 'NEU',
        'WIRT', 'WIRT', 'LEHRE', 'LEHRER', 'HELFER',
        'ELF', 'ELFEN', 'GEIST', 'HEER', 'HELLE',
        'LUFT', 'LUGE', 'TRUG', 'TRUGEN', 'GELTEN',
        'IRRE', 'IRR', 'IRN', 'IRUN',
    ]
    for w in modern_de:
        all_words.add(w)

    print(f"\n  Trying to segment: {garbled}")

    # DP segmentation
    n = len(garbled)
    # dp[i] = (best_coverage, list_of_words)
    dp = [(0, []) for _ in range(n+1)]
    for i in range(1, n+1):
        # Default: skip this char
        dp[i] = (dp[i-1][0], dp[i-1][1] + [garbled[i-1]])
        # Try all words ending at position i
        for wlen in range(2, min(i+1, 16)):
            candidate = garbled[i-wlen:i]
            if candidate in all_words:
                prev_coverage = dp[i-wlen][0]
                new_coverage = prev_coverage + wlen
                if new_coverage > dp[i][0]:
                    dp[i] = (new_coverage, dp[i-wlen][1] + [f'[{candidate}]'])

    final_coverage = dp[n][0]
    final_words = dp[n][1]
    print(f"  Best DP coverage: {final_coverage}/{n} chars ({100*final_coverage/n:.1f}%)")
    print(f"  Segmentation: {' '.join(final_words)}")

    # Also try on collapsed
    collapsed = collapse(garbled)
    n2 = len(collapsed)
    dp2 = [(0, []) for _ in range(n2+1)]
    for i in range(1, n2+1):
        dp2[i] = (dp2[i-1][0], dp2[i-1][1] + [collapsed[i-1]])
        for wlen in range(2, min(i+1, 16)):
            candidate = collapsed[i-wlen:i]
            if candidate in all_words:
                prev_coverage = dp2[i-wlen][0]
                new_coverage = prev_coverage + wlen
                if new_coverage > dp2[i][0]:
                    dp2[i] = (new_coverage, dp2[i-wlen][1] + [f'[{candidate}]'])

    print(f"\n  Collapsed: {collapsed}")
    print(f"  Best DP coverage: {dp2[n2][0]}/{n2} ({100*dp2[n2][0]/n2:.1f}%)")
    print(f"  Segmentation: {' '.join(dp2[n2][1])}")

# ============================================================
# 5. Reversed reading (TOTNIURG precedent)
# ============================================================
print(f"\n{'='*60}")
print("5. REVERSED READING")
print("=" * 60)

if steh_hwnd_contexts:
    garbled = steh_hwnd_contexts[0][2].upper()
    reversed_g = garbled[::-1]
    collapsed_rev = collapse(reversed_g)

    print(f"  Original: {garbled}")
    print(f"  Reversed: {reversed_g}")
    print(f"  Rev collapsed: {collapsed_rev}")

    # Scan reversed for words
    print(f"\n  Words in reversed:")
    for wlen in range(3, min(len(reversed_g)+1, 12)):
        for start in range(len(reversed_g) - wlen + 1):
            substr = reversed_g[start:start+wlen]
            if substr in all_words:
                print(f"    pos {start}-{start+wlen}: {substr}")

    # Same for collapsed reversed
    print(f"\n  Words in collapsed reversed:")
    for wlen in range(3, min(len(collapsed_rev)+1, 12)):
        for start in range(len(collapsed_rev) - wlen + 1):
            substr = collapsed_rev[start:start+wlen]
            if substr in all_words:
                print(f"    pos {start}-{start+wlen}: {substr}")

# ============================================================
# 6. Check wider context around STEH...HWND
# ============================================================
print(f"\n{'='*60}")
print("6. WIDER CONTEXT ANALYSIS")
print("=" * 60)

if steh_hwnd_contexts:
    for bi, idx, garbled, full, codes in steh_hwnd_contexts[:5]:
        decoded_book = decode(books[bi])
        # Get 20 chars before and after
        ctx_before = decoded_book[max(0,idx-20):idx]
        ctx_after = decoded_book[idx+len(full):min(len(decoded_book),idx+len(full)+20)]
        print(f"\n  Book {bi}:")
        print(f"    ...{ctx_before} | STEH {garbled} HWND | {ctx_after}...")

# ============================================================
# 7. All other major garbled sequences
# ============================================================
print(f"\n{'='*60}")
print("7. ALL MAJOR GARBLED SEQUENCES")
print("=" * 60)

# Find all segments of 6+ chars that contain no German words
# Assemble full text first
all_decoded = []
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    all_decoded.append(decoded)

# Count longest unidentified runs in each book
garbled_segments = []
for bi, decoded in enumerate(all_decoded):
    # Simple: find runs of 6+ chars that are all caps with no spaces
    # (everything is caps in our decoded text)
    # Instead, let's find what segments DON'T contain common short words
    text = decoded
    # Mark positions covered by known words
    covered = [False] * len(text)
    known_words_short = ['DER', 'DIE', 'DAS', 'DEN', 'DEM', 'DES', 'EIN',
                         'UND', 'IST', 'ICH', 'SIE', 'WIR', 'ER', 'ES',
                         'AN', 'IN', 'SO', 'AUS', 'VON', 'NACH',
                         'SEIN', 'SEINE', 'HIER', 'DIES', 'DIESER',
                         'STEH', 'STEIN', 'STEINE', 'STEINEN',
                         'FINDEN', 'URALTE', 'KOENIG', 'WISSET',
                         'SCHAUN', 'RUIN', 'RUNE', 'RUNEN',
                         'FACH', 'ORT', 'SEE', 'TUN', 'NUN',
                         'ERDE', 'VIEL', 'TEIL', 'ALT', 'NEU',
                         'GAR', 'AUCH', 'NOCH', 'ERST', 'ERSTE',
                         'HAT', 'TAG', 'WEG', 'BIS',
                         'SEID', 'WIND', 'HECHLT', 'OEL',
                         'HWND', 'THARSC', 'LABGZERAS', 'TOTNIURG',
                         'SCHWITEIO', 'HEARUCHTIGER', 'TAUTR', 'EILCH',
                         'HIHL', 'LABRRNI', 'MINHEDDEM', 'MINHEDEM',
                         'AUNRSONGETRASES', 'RUNEORT']
    for word in known_words_short:
        start = 0
        while True:
            idx = text.find(word, start)
            if idx == -1:
                break
            for p in range(idx, idx+len(word)):
                covered[p] = True
            start = idx + 1

    # Find uncovered runs of 6+
    run_start = None
    for i in range(len(covered)):
        if not covered[i]:
            if run_start is None:
                run_start = i
        else:
            if run_start is not None:
                run_len = i - run_start
                if run_len >= 6:
                    segment = text[run_start:i]
                    garbled_segments.append((bi, run_start, segment))
                run_start = None
    if run_start is not None:
        run_len = len(covered) - run_start
        if run_len >= 6:
            garbled_segments.append((bi, run_start, text[run_start:]))

# Count unique segments
segment_counts = Counter(s[2] for s in garbled_segments)
print(f"\n  Total garbled segments (6+ chars): {len(garbled_segments)}")
print(f"  Unique: {len(segment_counts)}")
print(f"\n  Most common garbled segments:")
for seg, cnt in segment_counts.most_common(20):
    collapsed_seg = collapse(seg)
    print(f"    x{cnt:2d} ({len(seg):2d} chars): {seg}")
    if collapsed_seg != seg:
        print(f"         collapsed: {collapsed_seg}")

# ============================================================
# 8. VMTEGE pattern deep analysis
# ============================================================
print(f"\n{'='*60}")
print("8. VMTEGE DEEP ANALYSIS")
print("=" * 60)

vmt_contexts = []
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('VMT')
    if idx != -1:
        ctx_start = max(0, idx-10)
        ctx_end = min(len(decoded), idx+15)
        codes_here = book_codes[idx:idx+3]
        vmt_contexts.append((bi, idx, decoded[ctx_start:ctx_end], codes_here))

print(f"\n  VMT occurrences: {len(vmt_contexts)}")
for bi, idx, ctx, codes in vmt_contexts[:8]:
    print(f"    Book {bi:2d}: ...{ctx}...")

if vmt_contexts:
    # All VMT code sequences
    vmt_code_seqs = Counter(tuple(c[3]) for c in vmt_contexts)
    print(f"\n  VMT code patterns:")
    for seq, cnt in vmt_code_seqs.most_common():
        print(f"    {list(seq)} x{cnt}")

# What letters do V, M, T map from?
print(f"\n  V codes: {rev.get('V', [])}")
print(f"  M codes: {rev.get('M', [])}")
print(f"  T codes: {rev.get('T', [])}")

# What if VMT is actually a MHG word?
# In MHG: "vermeit" = avoided, "vermaht" = betrothed
# VER-MIT = "with-?"
# Or: V = F in MHG (v was pronounced /f/)
# FMT? Still nothing
# What about VMT as abbreviation?
# In medieval German, tildes/macrons over letters indicated abbreviation
# VM could be VER- (very common MHG prefix)
# VMT = VERMT = VERMIT? VERMEHT? VERMAHT?
print(f"\n  MHG hypothesis:")
print(f"    If V=/f/: FMT = ?")
print(f"    If VM=VER: VERT = ?")
print(f"    VERMEIT (avoided) = VER-MEIT?")
print(f"    VMTEGE: VM-TEGE = VER-TAGE? (days)")
print(f"    VMTEGE: V-MT-EGE = F-MT-EGE?")
print(f"    VMTEGE with collapsed: VMTEGE (no doubles)")

# Check what follows VMT in all cases
print(f"\n  VMT + following context:")
for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('VMTEGE')
    if idx != -1:
        ctx = decoded[idx:idx+12]
        codes = book_codes[idx:idx+12]
        print(f"    Book {bi}: {ctx}")
        for j, c in enumerate(codes[:8]):
            letter = mapping.get(c, '?')
            print(f"      pos {j}: {c} = {letter}")
        break

# ============================================================
# 9. DNRHAUNRN deep analysis
# ============================================================
print(f"\n{'='*60}")
print("9. DNRHAUNRN ANALYSIS")
print("=" * 60)

for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('DNRHAUNRN')
    if idx != -1:
        ctx_start = max(0, idx-10)
        ctx_end = min(len(decoded), idx+25)
        codes_here = book_codes[idx:idx+9]
        print(f"  Book {bi}: ...{decoded[ctx_start:ctx_end]}...")
        print(f"  Codes: {codes_here}")
        for j, c in enumerate(codes_here):
            letter = mapping.get(c, '?')
            total = sum(1 for b in books for x in b if x == c)
            print(f"    pos {j}: code {c} = {letter} ({total}x total)")

        # Possible readings:
        # DNR + HAUNRN
        # D + NR + HAUN + RN
        # DN + R + HAUN + RN
        collapsed = collapse('DNRHAUNRN')
        print(f"\n  Collapsed: {collapsed}")

        # MHG: HAUN = hauwen (to strike/chop)
        # HAUNRN could be a gerund/noun form
        # DNR could be DENER/DINER (servant MHG)
        # Or "DEN RHAUNRN" = "den [r]Hau[e]n[r]n"
        # In MHG: plural of "hau" could be "houwen"
        print(f"\n  Possible splits:")
        print(f"    D + NR + HAUN + RN = '[d] [nr] strike [rn]'")
        print(f"    DNR + HAUN + RN = '[dnr] strike [rn]'")
        print(f"    DN + RHAUNRN = '[dn] + ?")
        break

# ============================================================
# 10. LHLADIZ analysis
# ============================================================
print(f"\n{'='*60}")
print("10. LHLADIZ ANALYSIS")
print("=" * 60)

for bi, book_codes in enumerate(books):
    decoded = decode(book_codes)
    idx = decoded.find('LHLADIZ')
    if idx != -1:
        ctx_start = max(0, idx-10)
        ctx_end = min(len(decoded), idx+15)
        codes_here = book_codes[idx:idx+7]
        print(f"  Book {bi}: ...{decoded[ctx_start:ctx_end]}...")
        print(f"  Codes: {codes_here}")
        for j, c in enumerate(codes_here):
            print(f"    pos {j}: code {c} = {mapping.get(c,'?')}")

        collapsed = collapse('LHLADIZ')
        reversed_v = 'LHLADIZ'[::-1]
        print(f"  Collapsed: {collapsed}")
        print(f"  Reversed: {reversed_v}")
        # ZIDALHL reversed -- ZIDAL? Not obvious
        # LHL + ADIZ?
        # L + HLADIZ? HLADIZ reversed = ZIDALH
        # Could this be a Slavic/Gothic name?
        # HL is an OHG cluster: HLAFORD -> lord
        # HLAD = OHG for "to load"?
        break

# ============================================================
# 11. Check if garbled sections share code patterns across books
# ============================================================
print(f"\n{'='*60}")
print("11. CROSS-BOOK CODE PATTERN MATCHING")
print("=" * 60)

# For each garbled segment that appears in multiple books,
# verify that the CODES are identical (not just the letters)
# This would confirm they're not coincidental letter matches
multi_segments = [(seg, cnt) for seg, cnt in segment_counts.items() if cnt >= 3]
print(f"\n  Segments appearing 3+ times: {len(multi_segments)}")

for seg, cnt in sorted(multi_segments, key=lambda x: -x[1])[:10]:
    # Find code sequences for each occurrence
    code_seqs = []
    for bi, start, s in garbled_segments:
        if s == seg:
            code_seq = tuple(books[bi][start:start+len(seg)])
            code_seqs.append((bi, code_seq))
    unique_code_seqs = set(cs[1] for cs in code_seqs)
    print(f"\n  '{seg}' x{cnt} ({len(seg)} chars):")
    print(f"    Unique code sequences: {len(unique_code_seqs)}")
    if len(unique_code_seqs) <= 3:
        for cs in unique_code_seqs:
            matching_books = [bi for bi, seq in code_seqs if seq == cs]
            print(f"      {list(cs)} (books: {matching_books})")

print(f"\n{'='*80}")
print("DONE - SESSION 10 GARBLED CORE ATTACK")
print("=" * 80)
