#!/usr/bin/env python3
"""Generate Hellgate Library guide: bookcase -> book -> decoded text + translations."""
import json, os, sys

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')

# Load data
with open(os.path.join(data_dir, 'mapping_v7.json')) as f:
    v7 = json.load(f)
with open(os.path.join(data_dir, 'books.json')) as f:
    books = json.load(f)
with open(os.path.join(data_dir, 'bookcase_mapping.json')) as f:
    bookcase_map = json.load(f)

# Load pipeline (decode + segment)
src = open(os.path.join(script_dir, '..', 'core', 'narrative_v3_clean.py')).read()
code_end = src.index("\n# ============================================================\n# RECONSTRUCT")
exec(src[:code_end])

# Per-book resolved text — apply ANAGRAM_MAP per-book independently
# (ANAGRAM_MAP changes text length, so concatenated boundaries are invalid)
per_book_resolved = []
for text in decoded_books:
    rt = text
    for anagram in sorted(ANAGRAM_MAP.keys(), key=len, reverse=True):
        rt = rt.replace(anagram, ANAGRAM_MAP[anagram])
    rt = rt.replace('TREUUNR', 'TREUNUR')
    per_book_resolved.append(rt)

# Per-book segmentation
per_book_segmented = []
per_book_coverage = []
for bidx, rt in enumerate(per_book_resolved):
    total = sum(1 for c in rt if c != '?')
    if total == 0:
        per_book_segmented.append('')
        per_book_coverage.append(0)
        continue
    tokens, cov = dp_segment(rt)
    seg = ' '.join(tokens)
    pct = cov / total * 100
    per_book_segmented.append(seg)
    per_book_coverage.append(pct)

# Group by bookcase
from collections import OrderedDict
bookcases = OrderedDict()
for entry in bookcase_map:
    bc = entry['bookcase']
    if bc not in bookcases:
        bookcases[bc] = []
    bookcases[bc].append(entry)

# Get raw cipher text per book
def get_cipher_text(bidx):
    return books[bidx] if bidx < len(books) else ''

# Output
output_path = os.path.join(script_dir, '..', '..', 'docs', 'hellgate_library_guide.md')
with open(output_path, 'w', encoding='utf-8') as out:
    out.write("# Hellgate Library — Complete Book Guide\n\n")
    out.write("**Location:** Underground beneath Ab'Dendriel (Shadow Caves → Hellgate, Key 3012)\n")
    out.write("**Total Books:** 71 (across 40 bookcases)\n")
    out.write("**Cipher:** Homophonic substitution, 98 two-digit codes → 22 German letters\n")
    out.write("**Overall Decode:** 94.4% word coverage (100% letter-level)\n")
    out.write("**Generated:** 2026-03-24 from pipeline v7 (30 sessions)\n\n")
    out.write("---\n\n")
    out.write("## How to Read This Guide\n\n")
    out.write("- **Title:** The 10-digit number shown as the book's name in-game\n")
    out.write("- **Cipher Text:** The full digit sequence (the raw content of the book)\n")
    out.write("- **Decoded German:** Letters decoded from the cipher, segmented into words\n")
    out.write("- **{XYZ}** = garbled blocks (letters are correct but word boundaries unresolved)\n")
    out.write("- **Coverage %** = percentage of characters matching known German/MHG words\n\n")
    out.write("---\n\n")

    for bc_name, bc_books in bookcases.items():
        out.write(f"## {bc_name}\n\n")

        for entry in bc_books:
            lib_num = entry['library_number']
            bidx = entry['books_json_index']
            label = entry['label_10digit']
            clen = entry['content_length']

            cipher = get_cipher_text(bidx)
            seg = per_book_segmented[bidx] if bidx < len(per_book_segmented) else ''
            pct = per_book_coverage[bidx] if bidx < len(per_book_coverage) else 0

            out.write(f"### Book #{lib_num} — \"{label}\"\n\n")
            out.write(f"**Bookcase:** {bc_name} | **Length:** {clen} digits | **Coverage:** {pct:.0f}%\n\n")

            # Cipher text (wrap at 80)
            out.write("**Cipher Text:**\n```\n")
            for i in range(0, len(cipher), 80):
                out.write(cipher[i:i+80] + "\n")
            out.write("```\n\n")

            # Decoded German
            out.write("**Decoded German:**\n")
            out.write(f"> {seg}\n\n")

            out.write("---\n\n")

    # Summary table
    out.write("## Summary Table\n\n")
    out.write("| # | Title | Bookcase | Digits | Coverage | First Words |\n")
    out.write("|---|-------|----------|--------|----------|-------------|\n")
    for entry in bookcase_map:
        lib_num = entry['library_number']
        bidx = entry['books_json_index']
        label = entry['label_10digit']
        clen = entry['content_length']
        bc = entry['bookcase']
        pct = per_book_coverage[bidx] if bidx < len(per_book_coverage) else 0
        seg = per_book_segmented[bidx] if bidx < len(per_book_segmented) else ''
        # First ~50 chars of decoded
        preview = seg[:60].rstrip()
        if len(seg) > 60:
            preview += "..."
        out.write(f"| {lib_num} | {label} | {bc} | {clen} | {pct:.0f}% | {preview} |\n")

    out.write(f"\n---\n\n*Generated from `scripts/core/narrative_v3_clean.py` (mapping v7, 94.4% coverage).*\n")

print(f"Written to {output_path}")
print(f"Total books: {len(bookcase_map)}")
print(f"Bookcases: {len(bookcases)}")
