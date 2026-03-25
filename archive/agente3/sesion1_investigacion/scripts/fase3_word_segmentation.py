"""
fase3_word_segmentation.py — Segmentación por libros pares.

Basado en la técnica del video Expedientes Tibianos X:
- Los 9 pares de libros con contenido compartido revelan fronteras de palabras.
- Las sub-secuencias que se repiten intactas entre libros son "unidades" (palabras/frases).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils_469 import load_books, load_mapping, digits_to_pairs, decode_pairs
from collections import defaultdict

def find_overlapping_pairs(books, min_overlap=10):
    """Encuentra pares de libros con sub-secuencias compartidas."""
    pairs = []
    for i in range(len(books)):
        for j in range(i+1, len(books)):
            overlap = longest_common_substring(books[i], books[j])
            if overlap >= min_overlap:
                pairs.append((i, j, overlap))
    pairs.sort(key=lambda x: -x[2])
    return pairs

def longest_common_substring(s1, s2):
    """Encuentra la longitud del substring común más largo."""
    m, n = len(s1), len(s2)
    # Rolling hash approach for efficiency
    max_len = 0
    for length in range(min(m, n), 0, -1):
        s1_subs = {s1[i:i+length] for i in range(m - length + 1)}
        for j in range(n - length + 1):
            if s2[j:j+length] in s1_subs:
                return length
        if max_len > 0:
            break
    return max_len

def find_all_shared_substrings(book1, book2, min_len=6):
    """Encuentra todas las sub-secuencias compartidas entre dos libros."""
    shared = []
    # Use suffix-based approach
    for length in range(min(len(book1), len(book2)), min_len-1, -1):
        subs1 = {}
        for i in range(len(book1) - length + 1):
            s = book1[i:i+length]
            subs1[s] = i
        for j in range(len(book2) - length + 1):
            s = book2[j:j+length]
            if s in subs1:
                # Check not already covered by a longer match
                already_covered = False
                for (s2, _, _, _) in shared:
                    if s in s2:
                        already_covered = True
                        break
                if not already_covered:
                    shared.append((s, subs1[s], j, length))
        if shared:
            break  # We found matches at this length, don't need shorter
    return shared

def find_repeating_units(books, min_len=4, max_len=40):
    """
    Encuentra sub-secuencias que se repiten en múltiples libros.
    Estas son candidatas a "palabras" en el lenguaje 469.
    """
    # Concatenar todo y buscar n-gramas frecuentes
    all_text = "".join(books)
    
    units = {}
    for length in range(max_len, min_len-1, -2):  # step by 2 (digit pairs)
        for i in range(len(all_text) - length + 1):
            sub = all_text[i:i+length]
            if sub not in units:
                # Contar en cuántos libros aparece
                book_count = sum(1 for b in books if sub in b)
                if book_count >= 2:
                    total_count = all_text.count(sub)
                    units[sub] = {
                        'sequence': sub,
                        'length': length,
                        'books': book_count,
                        'total': total_count
                    }
    
    # Filtrar: eliminar sub-secuencias que son parte de otras más largas
    filtered = {}
    sorted_units = sorted(units.items(), key=lambda x: -x[1]['length'])
    for seq, info in sorted_units:
        is_sub = False
        for existing_seq in filtered:
            if seq in existing_seq and seq != existing_seq:
                is_sub = True
                break
        if not is_sub:
            filtered[seq] = info
    
    return filtered

def main():
    print("=" * 60)
    print("  FASE 3: SEGMENTACION POR LIBROS PARES")
    print("=" * 60)
    
    mapping = load_mapping(4)
    books = load_books()
    
    print(f"\nCargados {len(books)} libros")
    print(f"Longitudes: min={min(len(b) for b in books)}, max={max(len(b) for b in books)}, "
          f"media={sum(len(b) for b in books)/len(books):.0f}")
    
    # Paso 1: Encontrar sub-secuencias compartidas frecuentes
    print(f"\n--- Buscando unidades repetidas (4-30 digitos, en 2+ libros) ---")
    units = find_repeating_units(books, min_len=4, max_len=30)
    
    # Filtrar solo las que tienen longitud par (pueden ser pares de dígitos)
    even_units = {k: v for k, v in units.items() if v['length'] % 2 == 0}
    
    # Ordenar por frecuencia * longitud
    ranked = sorted(even_units.items(), key=lambda x: -(x[1]['books'] * x[1]['length']))
    
    print(f"\nTop 40 unidades repetidas:")
    print(f"{'Secuencia':<35} {'Len':<5} {'Libros':<7} {'Total':<7} {'Decodificado':<20}")
    print(f"{'-'*74}")
    
    for seq, info in ranked[:40]:
        decoded = decode_pairs(digits_to_pairs(seq, 0), mapping)
        # Also try offset 1
        decoded1 = decode_pairs(digits_to_pairs(seq, 1), mapping)
        # Pick better one
        unk0 = decoded.count('?')
        unk1 = decoded1.count('?')
        best = decoded if unk0 <= unk1 else f"(o1){decoded1}"
        
        seq_display = seq[:32] + "..." if len(seq) > 32 else seq
        print(f"  {seq_display:<33} {info['length']:<5} {info['books']:<7} {info['total']:<7} {best:<20}")
    
    # Paso 2: Identificar libros que son substrings de otros
    print(f"\n--- Libros contenidos dentro de otros ---")
    containment = []
    for i in range(len(books)):
        for j in range(len(books)):
            if i != j and books[i] in books[j] and len(books[i]) < len(books[j]):
                containment.append((i, j, len(books[i])))
    
    print(f"  {len(containment)} relaciones de contencion encontradas")
    for child, parent, length in sorted(containment, key=lambda x: -x[2])[:15]:
        print(f"  Libro {child} ({length} dig) esta contenido en Libro {parent} ({len(books[parent])} dig)")
    
    # Paso 3: Encontrar pares con máximo solapamiento (suffix-prefix)
    print(f"\n--- Solapamientos suffix-prefix (>= 10 digitos) ---")
    overlaps = []
    for i in range(len(books)):
        for j in range(len(books)):
            if i == j:
                continue
            # Check if suffix of book[i] matches prefix of book[j]
            max_ov = min(len(books[i]), len(books[j]))
            for ov_len in range(max_ov, 9, -1):
                if books[i][-ov_len:] == books[j][:ov_len]:
                    overlaps.append((i, j, ov_len))
                    break
    
    overlaps.sort(key=lambda x: -x[2])
    print(f"  {len(overlaps)} solapamientos encontrados")
    for src, dst, ov_len in overlaps[:20]:
        decoded_ov = decode_pairs(digits_to_pairs(books[src][-ov_len:], 0), mapping)
        print(f"  Libro {src:>2} -> Libro {dst:>2}: {ov_len:>3} digitos = \"{decoded_ov[:30]}\"")
    
    # Paso 4: Construir cadenas
    print(f"\n--- Cadenas reconstruidas ---")
    # Build chains from overlaps
    adj = defaultdict(list)
    for src, dst, ov_len in overlaps:
        adj[src].append((dst, ov_len))
    
    visited = set()
    chains = []
    
    # Find chain starts (books that are targets of no overlap or start new chains)
    targets = {dst for _, dst, _ in overlaps}
    sources = {src for src, _, _ in overlaps}
    starts = sources - targets  # Books that are sources but not targets
    
    for start in sorted(starts):
        if start in visited:
            continue
        chain = [start]
        visited.add(start)
        current = start
        while current in adj:
            # Pick the longest overlap
            options = [(dst, ov) for dst, ov in adj[current] if dst not in visited]
            if not options:
                break
            next_book, ov = max(options, key=lambda x: x[1])
            chain.append(next_book)
            visited.add(next_book)
            current = next_book
        if len(chain) >= 2:
            chains.append(chain)
    
    for i, chain in enumerate(sorted(chains, key=lambda x: -len(x))):
        chain_str = " -> ".join(str(b) for b in chain)
        total_len = sum(len(books[b]) for b in chain)
        print(f"  Cadena {i}: [{len(chain)} libros, ~{total_len} dig] {chain_str}")
    
    isolated = set(range(len(books))) - visited
    print(f"\n  Libros aislados: {len(isolated)} ({', '.join(str(b) for b in sorted(isolated))})")
    
    # Paso 5: Glosario de "palabras 469"
    print(f"\n--- Glosario de 'palabras 469' (unidades de 4-12 digitos en 5+ libros) ---")
    word_candidates = {k: v for k, v in even_units.items() 
                       if v['books'] >= 5 and 4 <= v['length'] <= 12}
    
    print(f"{'Codigo469':<14} {'Decodificado':<10} {'Libros':<7} {'Total':<7}")
    print(f"{'-'*38}")
    for seq, info in sorted(word_candidates.items(), key=lambda x: -x[1]['books']):
        decoded = decode_pairs(digits_to_pairs(seq, 0), mapping)
        print(f"  {seq:<12}   {decoded:<10} {info['books']:<7} {info['total']:<7}")

if __name__ == "__main__":
    main()
