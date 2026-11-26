# Graph Report - grafo-regulatorio  (2026-11-25)

## Corpus Check
- Grafo generado por adaptador determinista (scripts/csv_a_graphify.py), sin extracción LLM.

## Summary
- 46 nodes · 84 edges · 3 communities
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.7)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…84
- Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…85
- Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…91 bis

## God Nodes (most connected - your core abstractions)
1. `DFL 4 de 2006 (LGSE)` - 40 edges
2. `Ley 20.936 de 2016 — art. 1` - 38 edges
3. `Ley 21.721 de 2024 — art. único` - 5 edges
4. `DFL 4 de 2006 (LGSE) — art. 77` - 3 edges
5. `DFL 4 de 2006 (LGSE) — art. 91 bis` - 3 edges
6. `DFL 4 de 2006 (LGSE) — art. 7` - 2 edges
7. `DFL 4 de 2006 (LGSE) — art. 8 bis` - 2 edges
8. `DFL 4 de 2006 (LGSE) — art. 72-1` - 2 edges
9. `DFL 4 de 2006 (LGSE) — art. 72-2` - 2 edges
10. `DFL 4 de 2006 (LGSE) — art. 72-3` - 2 edges

## Surprising Connections (you probably didn't know these)
- `DFL 4 de 2006 (LGSE)` --contiene--> `DFL 4 de 2006 (LGSE) — art. 7`  [EXTRACTED]
  ontologia/nodos_normas.csv → ontologia/nodos_articulos.csv
- `DFL 4 de 2006 (LGSE)` --contiene--> `DFL 4 de 2006 (LGSE) — art. 72-15`  [EXTRACTED]
  ontologia/nodos_normas.csv → ontologia/nodos_articulos.csv
- `DFL 4 de 2006 (LGSE)` --contiene--> `DFL 4 de 2006 (LGSE) — art. 72-16`  [EXTRACTED]
  ontologia/nodos_normas.csv → ontologia/nodos_articulos.csv
- `DFL 4 de 2006 (LGSE)` --contiene--> `DFL 4 de 2006 (LGSE) — art. 72-2`  [EXTRACTED]
  ontologia/nodos_normas.csv → ontologia/nodos_articulos.csv
- `DFL 4 de 2006 (LGSE)` --contiene--> `DFL 4 de 2006 (LGSE) — art. 72-21`  [EXTRACTED]
  ontologia/nodos_normas.csv → ontologia/nodos_articulos.csv

## Communities (3 total, 0 thin omitted)

### Community 0 - "DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…84"
Cohesion: 0.10
Nodes (21): DFL 4 de 2006 (LGSE), DFL 4 de 2006 (LGSE) — art. 72-1, DFL 4 de 2006 (LGSE) — art. 72-10, DFL 4 de 2006 (LGSE) — art. 72-11, DFL 4 de 2006 (LGSE) — art. 72-12, DFL 4 de 2006 (LGSE) — art. 72-13, DFL 4 de 2006 (LGSE) — art. 72-14, DFL 4 de 2006 (LGSE) — art. 72-17 (+13 more)

### Community 1 - "Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…85"
Cohesion: 0.11
Nodes (18): Ley 20.936 de 2016, Ley 20.936 de 2016 — art. 1, DFL 4 de 2006 (LGSE) — art. 7, DFL 4 de 2006 (LGSE) — art. 72-15, DFL 4 de 2006 (LGSE) — art. 72-16, DFL 4 de 2006 (LGSE) — art. 72-2, DFL 4 de 2006 (LGSE) — art. 72-21, DFL 4 de 2006 (LGSE) — art. 72-22 (+10 more)

### Community 2 - "Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…91 bis"
Cohesion: 0.29
Nodes (7): Ley 21.721 de 2024, Ley 21.721 de 2024 — art. único, DFL 4 de 2006 (LGSE) — art. 77, DFL 4 de 2006 (LGSE) — art. 87, DFL 4 de 2006 (LGSE) — art. 91, DFL 4 de 2006 (LGSE) — art. 91 bis, Res. 156 exenta de 2025

## Knowledge Gaps
- **3 isolated node(s):** `Ley 20.936 de 2016`, `Ley 21.721 de 2024`, `Res. 156 exenta de 2025`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 3 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Ley 20.936 de 2016 — art. 1` connect `Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…85` to `DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…84`, `Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…91 bis`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `Ley 20.936 de 2016 — art. 1` (e.g. with `DFL 4 de 2006 (LGSE) — art. 73` and `DFL 4 de 2006 (LGSE) — art. 74`) actually correct?**
  _`Ley 20.936 de 2016 — art. 1` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Ley 20.936 de 2016`, `Ley 21.721 de 2024`, `Res. 156 exenta de 2025` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…84` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._
- **Should `Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…85` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._