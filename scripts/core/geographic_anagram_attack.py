#!/usr/bin/env python3
"""
Geographic Anagram Attack on Bonelord 469 Proper Nouns
======================================================
Hypothesis: CipSoft (based in Regensburg, Bavaria) uses anagrams of real
German/Austrian/Swiss geographic names for proper nouns in the 469 cipher.

Known CipSoft anagram pattern:
  Vladruc = Dracula, Dallheim = Heimdall, Banor = Baron

Key finding from deep_anagram_attack.py:
  LABGZERAS ~ SALZBERG (near-exact anagram!)

This script:
1. Verifies LABGZERAS = SALZBERG letter-by-letter
2. Tests ALL proper nouns against comprehensive geographic name database
3. Traces raw codes for each proper noun to identify potential mapping errors
4. Tests compound geographic splits (e.g., SCHWITEIONE = STEINWEICH? WIESENTEICH?)
"""

import json, os, sys
from collections import Counter
from itertools import permutations

# ============================================================
# PROPER NOUNS FROM THE CIPHER
# ============================================================
PROPER_NOUNS = {
    "LABGZERAS":       (8, "KOENIG LABGZERAS - king's name"),
    "HEDEMI":          (11, "place - DIE URALTE STEINEN ... HEDEMI"),
    "ADTHARSC":        (6, "entity/place at the stones"),
    "SCHWITEIONE":     (10, "possibly bonelord race/place name"),
    "TIUMENGEMI":      (2, "ORT TIUMENGEMI = place name"),
    "ENGCHD":          (7, "ORT ENGCHD = place name"),
    "KELSEI":          (3, "after ENGCHD, possibly place/person"),
    "TAUTR":           (8, "HIER TAUTR IST = here TAUTR is"),
    "EILCHANHEARUCHTIG": (8, "title/adjective"),
    "EDETOTNIURGS":    (8, "attribute, contains TOTNIURG"),
    "TOTNIURG":        (8, "reversed = GRUINTOT"),
    "LABRNI":          (8, "person/place, shares LAB- with LABGZERAS"),
    "AUNRSONGETRASES": (11, "most common unrecognized"),
    "UTRUNR":          (5, "ENDE UTRUNR = end of utterance"),
    "GEVMT":           (7, "SEI GEVMT WIE = be GE-VMT as"),
}

# ============================================================
# GEOGRAPHIC NAME DATABASE
# CipSoft is in Regensburg, Bavaria. Focus on:
# - Bavarian cities/towns/regions
# - Austrian cities (especially near border: Salzburg, Linz, etc.)
# - Swiss German cities
# - Major German cities and historic places
# - Medieval German place names
# ============================================================
GEOGRAPHIC_NAMES = [
    # Bavaria (CipSoft's home)
    "REGENSBURG", "NUERNBERG", "MUENCHEN", "AUGSBURG", "WUERZBURG",
    "BAMBERG", "BAYREUTH", "PASSAU", "INGOLSTADT", "LANDSHUT",
    "STRAUBING", "DEGGENDORF", "KELHEIM", "AMBERG", "SCHWANDORF",
    "CHAM", "REGEN", "FREYUNG", "TIRSCHENREUTH", "NEUMARKT",
    "SULZBACH", "NABBURG", "WEIDEN", "OBERVIECHTACH",
    "ABENSBERG", "NEUSTADT", "VILSHOFEN", "GRAFENAU",
    "EICHSTAETT", "SCHWABACH", "FUERTH", "ERLANGEN",
    "ROTHENBURG", "DINKELSBUEHL", "NOERDLINGEN",

    # Austrian cities (Salzburg especially relevant!)
    "SALZBURG", "SALZBERG", "WIEN", "LINZ", "GRAZ", "INNSBRUCK",
    "KLAGENFURT", "VILLACH", "WELS", "STEYR", "DORNBIRN",
    "FELDKIRCH", "BREGENZ", "HALLEIN", "HALLSTATT", "SALZKAMMERGUT",
    "BERCHTESGADEN", "REICHENHALL",

    # Major German cities
    "BERLIN", "HAMBURG", "KOELN", "FRANKFURT", "STUTTGART",
    "DUESSELDORF", "DORTMUND", "ESSEN", "LEIPZIG", "DRESDEN",
    "HANNOVER", "BREMEN", "MAGDEBURG", "LUEBECK", "ROSTOCK",
    "AACHEN", "MAINZ", "TRIER", "HEIDELBERG", "FREIBURG",
    "KONSTANZ", "ULMER",

    # Swiss German cities
    "ZUERICH", "BERN", "BASEL", "LUZERN", "WINTERTHUR",
    "SCHAFFHAUSEN", "THUN", "CHUR",

    # Medieval/historic place components
    "STEINBERG", "STEINREICH", "STEINHEIM", "STEINACH",
    "GOLDBERG", "SILBERBERG", "EISENBERG", "KUPFERBERG",
    "SCHWARZBERG", "WEISSENBERG", "GRUENBERG",
    "BERGHEIM", "BURGHEIM", "WALDHEIM", "SEEHEIM",
    "KIRCHBERG", "LICHTENBERG", "ROSENBERG", "GRAFENBERG",
    "FALKENSTEIN", "ALTENSTEIN", "NEUENSTEIN", "ECKSTEIN",
    "DRACHENFELS", "RABENSTEIN", "LOEWENSTEIN",

    # Rivers and geographic features
    "DONAU", "RHEIN", "ELBE", "MAIN", "ISAR", "INN",
    "SALZACH", "NAAB", "REGEN", "ALTMUEHL",

    # Regions
    "BAYERN", "FRANKEN", "SCHWABEN", "OBERPFALZ",
    "NIEDERBAYERN", "OBERBAYERN", "MITTELFRANKEN",
    "SACHSEN", "THUERINGEN", "HESSEN", "WESTFALEN",
    "SCHLESIEN", "BOEHMEN", "MAEHREN", "KAERNTEN",
    "TIROL", "STEIERMARK", "VORARLBERG",

    # Medieval compounds
    "HEILIGENSTADT", "KOENIGSBERG", "KOENIGSTEIN",
    "KAISERSLAUTERN", "REICHENBACH", "REICHENBERG",
    "FRIEDBERG", "LANDSBERG", "WASSERBURG",
    "ALTDORF", "NEUDORF", "KIRCHDORF",
    "GRAFENWOERTH", "MARKTREDWITZ",

    # Mythological/legendary places from German lore
    "NIBELHEIM", "WALHALL", "MIDGARD", "ASGARD",
    "NIFLHEIM", "MUSPELHEIM", "SCHWARZWALD",

    # Common German place-name elements (for compound matching)
    "BERG", "BURG", "HEIM", "DORF", "STADT", "STEIN",
    "FELD", "WALD", "SEE", "BACH", "AU", "BRUCH",
    "HAUSEN", "HOFEN", "KIRCHEN", "MUEHLE",
    "BRUECK", "GRABEN", "GRUND", "THAL",
    "FURT", "HAVEN", "HAFEN", "WERTH", "WERDER",
]

# Add without umlauts
expanded_geo = set()
for name in GEOGRAPHIC_NAMES:
    expanded_geo.add(name)
    expanded_geo.add(name.replace("UE", "U").replace("OE", "O").replace("AE", "A"))
    # Also try with AE/OE/UE as single letters would appear in cipher
    expanded_geo.add(name.replace("UE", "U").replace("OE", "O").replace("AE", "E"))

GEOGRAPHIC_SET = expanded_geo

# ============================================================
# ANALYSIS FUNCTIONS
# ============================================================

def letter_diff(word1, word2):
    """Precise letter difference between two words (multiset symmetric difference / 2)."""
    c1 = Counter(word1.upper())
    c2 = Counter(word2.upper())
    all_letters = set(list(c1.keys()) + list(c2.keys()))
    total_diff = sum(abs(c1.get(l, 0) - c2.get(l, 0)) for l in all_letters)
    extra_in_1 = {l: c1.get(l, 0) - c2.get(l, 0) for l in all_letters if c1.get(l, 0) > c2.get(l, 0)}
    missing_in_1 = {l: c2.get(l, 0) - c1.get(l, 0) for l in all_letters if c2.get(l, 0) > c1.get(l, 0)}
    return total_diff, extra_in_1, missing_in_1

def find_geographic_matches(noun, max_diff=3):
    """Find geographic names that are anagrams or near-anagrams of noun."""
    results = []
    noun_upper = noun.upper()
    noun_len = len(noun_upper)

    for geo in GEOGRAPHIC_SET:
        # Allow length difference up to max_diff
        if abs(len(geo) - noun_len) > max_diff:
            continue

        total_diff, extra, missing = letter_diff(noun_upper, geo)
        effective_diff = total_diff // 2  # substitutions

        if effective_diff <= max_diff:
            results.append({
                'geo': geo,
                'diff': effective_diff,
                'raw_diff': total_diff,
                'extra_in_noun': extra,
                'missing_in_noun': missing,
                'len_diff': len(geo) - noun_len,
            })

    return sorted(results, key=lambda x: (x['diff'], abs(x['len_diff'])))

def find_compound_geo_matches(noun, max_diff=2):
    """Try splitting noun into compound of geographic elements."""
    noun = noun.upper()
    n = len(noun)
    results = []

    # Geographic elements for compound matching
    elements = [
        "BERG", "BURG", "HEIM", "DORF", "STADT", "STEIN", "FELD",
        "WALD", "SEE", "BACH", "AU", "HAUSEN", "KIRCH", "KIRCHEN",
        "BRUECK", "GRABEN", "THAL", "TAL", "FURT", "HAVEN", "WERTH",
        "GOLD", "SILBER", "EISEN", "SALZ", "WASSER", "SCHWARZ", "WEISS",
        "GRUEN", "ROT", "ROSEN", "FALKEN", "LOEWEN", "DRACHEN",
        "LICHT", "NACHT", "SCHATTEN", "WEIN", "ICH", "SCHW", "EI",
        "REICH", "WEIT", "WIES", "WIESE", "TEICH", "WEICH", "EICHE",
    ]

    # Try 2-part splits
    for i in range(2, n - 1):
        p1 = noun[:i]
        p2 = noun[i:]

        for e1 in elements:
            d1, _, _ = letter_diff(p1, e1)
            if d1 <= max_diff * 2 and abs(len(p1) - len(e1)) <= max_diff:
                for e2 in elements:
                    d2, _, _ = letter_diff(p2, e2)
                    if d2 <= max_diff * 2 and abs(len(p2) - len(e2)) <= max_diff:
                        total = d1 // 2 + d2 // 2
                        if total <= max_diff:
                            results.append((f"{e1}+{e2}", total, i))

    # Try as rearranged compound: anagram of "element1+element2"
    for e1 in elements:
        for e2 in elements:
            compound = e1 + e2
            td, extra, missing = letter_diff(noun, compound)
            if td // 2 <= max_diff and abs(len(noun) - len(compound)) <= max_diff:
                results.append((f"{e1}{e2} (anagram)", td // 2, -1))

    return sorted(set((r[0], r[1]) for r in results), key=lambda x: x[1])

def trace_raw_codes(noun_text, mapping, books_data):
    """Find the raw digit codes that produce a given text in the decoded books."""
    # Build reverse mapping for decoding
    inv_map = {v: [] for v in set(mapping.values())}
    for code, letter in mapping.items():
        inv_map[letter].append(code)

    occurrences = []
    for book_idx, book in enumerate(books_data):
        # Try both offsets
        for off in [0, 1]:
            pairs = [book[j:j+2] for j in range(off, len(book)-1, 2)]
            decoded = ''.join(mapping.get(p, '?') for p in pairs)

            pos = 0
            while True:
                pos = decoded.find(noun_text, pos)
                if pos == -1:
                    break
                raw_codes = pairs[pos:pos + len(noun_text)]
                occurrences.append({
                    'book': book_idx,
                    'offset': off,
                    'position': pos,
                    'codes': raw_codes,
                    'decoded': ''.join(mapping.get(c, '?') for c in raw_codes),
                })
                pos += 1

    return occurrences

# ============================================================
# MAIN ANALYSIS
# ============================================================

def main():
    # Load data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', '..', 'data')

    with open(os.path.join(data_dir, 'books.json'), 'r') as f:
        books = json.load(f)
    with open(os.path.join(data_dir, 'final_mapping_v4.json'), 'r') as f:
        mapping = json.load(f)

    print("=" * 70)
    print("GEOGRAPHIC ANAGRAM ATTACK ON BONELORD 469 PROPER NOUNS")
    print("=" * 70)

    # ============================================================
    # 1. VERIFY LABGZERAS = SALZBERG
    # ============================================================
    print("\n" + "=" * 70)
    print("1. LABGZERAS vs SALZBERG - Detailed Verification")
    print("=" * 70)

    lab = "LABGZERAS"
    sal = "SALZBERG"

    c_lab = Counter(lab)
    c_sal = Counter(sal)

    print(f"\n  LABGZERAS ({len(lab)} letters): {dict(sorted(c_lab.items()))}")
    print(f"  SALZBERG  ({len(sal)} letters): {dict(sorted(c_sal.items()))}")

    total_diff, extra, missing = letter_diff(lab, sal)
    print(f"\n  Total letter difference: {total_diff}")
    print(f"  Extra in LABGZERAS:  {extra}")
    print(f"  Missing in LABGZERAS: {missing}")
    print(f"  Effective substitutions needed: {total_diff // 2}")

    if extra:
        print(f"\n  -> LABGZERAS has extra letter(s): {extra}")
        print(f"  -> If we remove the extra A: L_BGZERAS = SALZBERG (exact!)")
        print(f"  -> This means one code currently mapped to A might be wrong,")
        print(f"     OR CipSoft added a letter (like Ferumbras vs Ambrosius)")

    # Trace raw codes for LABGZERAS
    print(f"\n  Raw code occurrences of LABGZERAS:")
    occurrences = trace_raw_codes("LABGZERAS", mapping, books)
    code_patterns = set()
    for occ in occurrences:
        codes_str = ' '.join(occ['codes'])
        code_patterns.add(codes_str)
        print(f"    Book {occ['book']:2d} off={occ['offset']}: [{codes_str}] -> {occ['decoded']}")

    if not occurrences:
        # Try partial: just "LABGZER" or "BGZERAS"
        print("  (No exact match found. Looking for LABGZER and BGZERAS...)")
        for partial in ["LABGZER", "BGZERAS", "ABGZERA", "LABGZE"]:
            occs = trace_raw_codes(partial, mapping, books)
            if occs:
                print(f"    Found '{partial}' in {len(occs)} locations")
                for occ in occs[:3]:
                    print(f"      Book {occ['book']:2d}: [{' '.join(occ['codes'])}]")

    # Check which codes map to A (the extra letter)
    a_codes = [c for c, l in mapping.items() if l == 'A']
    print(f"\n  Codes currently mapped to A: {a_codes}")
    print(f"  If any of these in LABGZERAS position is wrong,")
    print(f"  the real name might be SALZBERG (exact anagram)")

    # ============================================================
    # 2. SYSTEMATIC GEOGRAPHIC MATCH FOR ALL PROPER NOUNS
    # ============================================================
    print("\n" + "=" * 70)
    print("2. GEOGRAPHIC MATCHES FOR ALL PROPER NOUNS")
    print("=" * 70)

    for noun, (freq, context) in sorted(PROPER_NOUNS.items()):
        print(f"\n  --- {noun} (freq={freq}) ---")
        print(f"  Context: {context}")
        print(f"  Letters ({len(noun)}): {dict(sorted(Counter(noun).items()))}")

        matches = find_geographic_matches(noun, max_diff=3)
        if matches:
            print(f"  Geographic matches (best first):")
            for m in matches[:8]:
                marker = " *** EXACT" if m['diff'] == 0 else ""
                marker = " ** NEAR-EXACT" if m['diff'] == 1 and not marker else marker
                print(f"    {m['geo']:20s} diff={m['diff']} "
                      f"extra={m['extra_in_noun']} missing={m['missing_in_noun']}{marker}")
        else:
            print(f"  No geographic matches within 3 letter diff")

        # Also try reversed
        reversed_noun = noun[::-1]
        rev_matches = find_geographic_matches(reversed_noun, max_diff=2)
        if rev_matches:
            print(f"  Reversed ({reversed_noun}) matches:")
            for m in rev_matches[:3]:
                print(f"    {m['geo']:20s} diff={m['diff']}")

        # Try compound geographic splits
        compounds = find_compound_geo_matches(noun, max_diff=1)
        if compounds:
            print(f"  Compound geographic matches:")
            for name, diff in compounds[:5]:
                print(f"    {name:25s} diff={diff}")

    # ============================================================
    # 3. SPECIAL ANALYSIS: SCHWITEIONE
    # ============================================================
    print("\n" + "=" * 70)
    print("3. DEEP ANALYSIS: SCHWITEIONE")
    print("=" * 70)

    schw = "SCHWITEIONE"
    print(f"\n  Letters ({len(schw)}): {dict(sorted(Counter(schw).items()))}")

    # Test specific hypotheses
    candidates = [
        "STEINREICH", "STEINWEICH", "WIESENTEICH", "EICHENWEIST",
        "SCHWEINEOIT", "WEISSTEINOCH", "STEINWEICHO",
        "WEICHENSTEIN", "EICHENSTEIN", "WIESENSTEIN",
        "EINOETSCHWI", "SCHWITZIONE",
    ]

    print(f"\n  Specific hypothesis tests:")
    for cand in candidates:
        td, extra, missing = letter_diff(schw, cand)
        if td <= 6:
            print(f"    {cand:20s} diff={td//2} extra={extra} missing={missing}")

    # Brute force: what anagrams of SCHWITEIONE make sense?
    # Test all geographic compounds
    prefixes = ["STEIN", "SCHW", "WEISS", "EICH", "WIES", "TEICH", "WEICH", "WEIT", "SCHWEIT"]
    suffixes = ["HEIM", "BERG", "STEIN", "EIONE", "IONE", "ONE", "ENE", "EICH"]

    print(f"\n  Compound element test:")
    for p in prefixes:
        remainder = list(Counter(schw) - Counter(p))
        if len(remainder) >= 0 and all(v >= 0 for v in (Counter(schw) - Counter(p)).values()):
            rem_letters = Counter(schw) - Counter(p)
            rem_str = ''.join(sorted(rem_letters.elements()))
            if rem_str:
                print(f"    {p} + [{rem_str}] (len={len(rem_str)})")
                # Check if remainder is close to any geographic suffix
                for s in suffixes + list(GEOGRAPHIC_SET):
                    if abs(len(s) - len(rem_str)) <= 1:
                        td, _, _ = letter_diff(rem_str, s)
                        if td <= 2:
                            print(f"      -> {p}+{s} (rem diff={td//2})")

    # ============================================================
    # 4. SPECIAL ANALYSIS: HEDEMI
    # ============================================================
    print("\n" + "=" * 70)
    print("4. DEEP ANALYSIS: HEDEMI (place with uralte Steinen)")
    print("=" * 70)

    hed = "HEDEMI"
    print(f"\n  Letters ({len(hed)}): {dict(sorted(Counter(hed).items()))}")

    # HEDEMI could be an anagram of a -HEIM name (very common in Germany!)
    # H, E, D, E, M, I -> HEIM + DE? or DHEIM + E?
    heim_test = Counter("HEDEMI") - Counter("HEIM")
    if all(v >= 0 for v in heim_test.values()):
        rem = ''.join(sorted(heim_test.elements()))
        print(f"  HEDEMI contains HEIM! Remainder: [{rem}]")
        print(f"  -> HEDEMI could be anagram of {rem}HEIM or HEIM{rem}")
        # DE + HEIM = DEHEIM? Not a real place but...
        # Actually: DI + HEIM? DHEIM + EI?
        # What about DIEHEM? HEIMED?

    # Try all -HEIM places
    heim_places = [g for g in GEOGRAPHIC_SET if "HEIM" in g]
    print(f"\n  -HEIM places tested:")
    for place in sorted(heim_places):
        td, extra, missing = letter_diff(hed, place)
        if td <= 6:
            print(f"    {place:20s} diff={td//2} extra={extra} missing={missing}")

    # ============================================================
    # 5. SPECIAL ANALYSIS: ADTHARSC
    # ============================================================
    print("\n" + "=" * 70)
    print("5. DEEP ANALYSIS: ADTHARSC")
    print("=" * 70)

    adt = "ADTHARSC"
    print(f"\n  Letters ({len(adt)}): {dict(sorted(Counter(adt).items()))}")

    # ADTHARSC could contain HARSCH (harsh) or DRACH (dragon)
    # A, D, T, H, A, R, S, C -> DRACHST + A? SCHARD + AT? STADTARCH?
    for test in ["HARSCH", "DRACH", "SCHAR", "THARSC", "RACHT", "DRACHST"]:
        rem = Counter(adt) - Counter(test)
        if all(v >= 0 for v in rem.values()):
            rem_str = ''.join(sorted(rem.elements()))
            print(f"  Contains {test}, remainder: [{rem_str}]")

    # ADTHARSC reversed = CSRAHTA+D -> test as anagram
    rev_adt = adt[::-1]
    print(f"\n  Reversed: {rev_adt}")

    # Test against city names
    for test in ["DRACHST", "DARSTADT", "HARSTADT", "STADTAHR", "RACHSTAD",
                  "KARSTADT", "DRACH", "HARSCH"]:
        td, extra, missing = letter_diff(adt, test)
        if td <= 4:
            print(f"    {test:20s} diff={td//2} extra={extra} missing={missing}")

    # ============================================================
    # 6. SPECIAL ANALYSIS: TIUMENGEMI
    # ============================================================
    print("\n" + "=" * 70)
    print("6. DEEP ANALYSIS: TIUMENGEMI (ORT = place)")
    print("=" * 70)

    tiu = "TIUMENGEMI"
    print(f"\n  Letters ({len(tiu)}): {dict(sorted(Counter(tiu).items()))}")

    # TIUMENGEMI has: E(2), G(1), I(2), M(2), N(1), T(1), U(1)
    # Could be: EIGENTUM + MI? GEMEINTUM?
    for test in ["EIGENTUM", "GEMEINT", "GEMEINTU", "MEINGUT", "GUTMEINEN",
                  "MEINUNGEN", "STIMMUNG", "TUMMELING", "GEMENGTUI"]:
        td, extra, missing = letter_diff(tiu, test)
        if td <= 4:
            print(f"    {test:20s} diff={td//2} extra={extra} missing={missing}")

    # Compound test
    for prefix in ["GE", "TI", "TIU", "MEIN", "STEIN", "TUMEN", "MINE"]:
        rem = Counter(tiu) - Counter(prefix)
        if all(v >= 0 for v in rem.values()):
            rem_str = ''.join(sorted(rem.elements()))
            print(f"  Prefix {prefix}, remainder [{rem_str}]")

    # ============================================================
    # 7. SPECIAL ANALYSIS: ENGCHD
    # ============================================================
    print("\n" + "=" * 70)
    print("7. DEEP ANALYSIS: ENGCHD (ORT = place)")
    print("=" * 70)

    eng = "ENGCHD"
    print(f"\n  Letters ({len(eng)}): {dict(sorted(Counter(eng).items()))}")

    # Only 6 letters, no vowels except hidden in CH?
    # E, N, G, C, H, D - looks garbled, maybe wrong mapping?
    # If CH = one sound, then E + N + G + [CH] + D
    # ENGD + CH -> anagram? GDCHEN?

    # Could be a short city: GENF? No, wrong letters.
    # GENDCH? DECHNG?
    # What if one consonant is wrong? E.g., D should be I -> ENGCHI?
    # Or what about ENOCH + GD?

    for test in ["GENF", "GENDCH", "DECHNG", "DECHEN", "ENCHED",
                  "ECHGDN", "GNECHD"]:
        td, extra, missing = letter_diff(eng, test)
        if td <= 4:
            print(f"    {test:20s} diff={td//2} extra={extra} missing={missing}")

    print(f"\n  NOTE: ENGCHD has only 1 vowel (E). This is suspicious.")
    print(f"  Possible that some consonant codes are wrong here.")
    print(f"  If D->A: ENGCHA, if G->I: ENICHD, if H->I: ENGCID")

    # ============================================================
    # 8. THEMATIC CONSISTENCY CHECK
    # ============================================================
    print("\n" + "=" * 70)
    print("8. THEMATIC CONSISTENCY: Do matches tell a story?")
    print("=" * 70)

    print("""
  If LABGZERAS = SALZBERG (salt mountain), then the narrative is:
    "KOENIG LABGZERAS" = "King of Salzberg/Salzburg"

  Salzburg connection makes sense because:
  - CipSoft is in Regensburg, ~250km from Salzburg
  - Salzburg has ancient Celtic salt mines (SALZ = salt)
  - "URALTE STEINEN" (ancient stones) fits salt mining caves
  - "RUNEORT" (rune place) could be ancient inscriptions in mines
  - Salt mines have preserved medieval/ancient artifacts

  If SCHWITEIONE = STEINREICH/STEINWEICH:
  - STEINREICH = "rich in stones" or "stone realm"
  - Fits perfectly with "URALTE STEINEN" theme

  If HEDEMI contains HEIM (home):
  - A homeland/settlement name
  - "DIE URALTE STEINEN ... HEDEMI" = the ancient stones of [Home-place]

  The text would be about:
  - A king (LABGZERAS/SALZBERG) ruling a stone/salt realm
  - Ancient stone inscriptions (URALTE STEINEN, RUNEORT)
  - A mysterious place (HEDEMI) with these ancient stones
  - The TOTNIURG (reversed = ruin+death) as a threat/curse
""")

    # ============================================================
    # 9. SUMMARY OF BEST MATCHES
    # ============================================================
    print("\n" + "=" * 70)
    print("9. SUMMARY: BEST GEOGRAPHIC MATCHES")
    print("=" * 70)

    for noun, (freq, context) in sorted(PROPER_NOUNS.items(), key=lambda x: -x[1][0]):
        matches = find_geographic_matches(noun, max_diff=2)
        best = matches[0] if matches else None
        if best:
            marker = "***" if best['diff'] == 0 else "**" if best['diff'] == 1 else "*"
            print(f"  {noun:20s} -> {best['geo']:20s} (diff={best['diff']}) {marker}")
        else:
            print(f"  {noun:20s} -> (no match within 2)")

if __name__ == "__main__":
    main()
