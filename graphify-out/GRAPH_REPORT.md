# Graph Report - grafo-regulatorio  (2026-11-25)

## Corpus Check
- Grafo generado por adaptador determinista (scripts/csv_a_graphify.py), sin extracción LLM.

## Cobertura de las normas

| Norma | Cobertura | Modificaciones pendientes | Artículos truncados (idParte) |
|---|---|---|---|
| DFL 4 de 2006 (LGSE) | completa | 0 | — |
| Ley 20.936 de 2016 | completa | 0 | — |
| Ley 21.721 de 2024 | completa | 0 | — |
| Res. 156 exenta de 2025 | completa | 0 | — |
| Ley 21.804 de 2026 | completa | 0 | — |
| Ley 21.505 de 2022 | completa | 0 | — |
| Ley 21.582 de 2023 | completa | 0 | — |
| Ley 21.833 de 2026 | completa | 0 | — |
| Ley 21.472 de 2022 | completa | 0 | — |
| Ley 21.667 de 2024 | completa | 0 | — |

## Cobertura de la historia por artículo

153 de 181 artículos del DFL 4 en el grafo tienen historia completa (todas las leyes posteriores al DFL 4 que la BCN anota en el artículo están en el grafo). Detalle de todo el DFL 4 en `datos/derivados/historia_articulos.csv`.

| Artículo | Leyes que faltan |
|---|---|
| 8 ter | 21194 |
| 20 | 20701 |
| 29 | 20701 |
| 39 | 20701 |
| 133 | 20220, 20805, 21806 |
| 134 | 20805 |
| 135 quinquies | 20805 |
| 135 ter | 20805 |
| 146 ter | 20220, 20720 |
| 147 | 20402, 20805 |
| 149 | 20571 |
| 149 bis | 20571, 21118 |
| 149 quater | 20571 |
| 149 ter | 21118 |
| 150 bis | 20257, 20698 |
| 150 ter | 20698 |
| 157 | 20257, 20805, 20928 |
| 163 | 20402 |
| 170 | 20402 |
| 178 | 20402 |
| 183 | 21194 |
| 184 | 20402, 20928 |
| 191 | 20928 |
| 207-2 | 21304 |
| 210 | 20999 |
| 211 | 20402 |
| 212 | 20402 |
| 225 | 20928, 21194 |

Aristas por relación, estado y método: contiene/verificada/regla: 189; deroga/verificada/regla: 7; implementa/verificada/regla: 1; modifica/verificada/manual: 52; modifica/verificada/regla: 160

## Summary
- 199 nodes · 409 edges · 7 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…223
- Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 8 ter…199 bis
- Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225
- Ley 21.472 de 2022 + Ley 21.667 de 2024 + Ley 21.833 de 2026 | DFL 4 de 2006 (LGSE): arts.
- Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…115
- Ley 21.582 de 2023 | DFL 4 de 2006 (LGSE): arts. 20…98
- Ley 21.505 de 2022 | DFL 4 de 2006 (LGSE): arts. 72-2…149 ter

## God Nodes (most connected - your core abstractions)
1. `DFL 4 de 2006 (LGSE)` - 181 edges
2. `Ley 20.936 de 2016 — art. 1` - 127 edges
3. `Ley 21.804 de 2026 — art. único` - 58 edges
4. `Ley 21.721 de 2024 — art. único` - 11 edges
5. `Ley 21.833 de 2026 — art. 1` - 9 edges
6. `Ley 21.505 de 2022 — art. único` - 8 edges
7. `Ley 21.582 de 2023 — art. 10` - 8 edges
8. `DFL 4 de 2006 (LGSE) — art. 212-13` - 5 edges
9. `DFL 4 de 2006 (LGSE) — art. 157` - 4 edges
10. `DFL 4 de 2006 (LGSE) — art. 163` - 4 edges

## Surprising Connections (you probably didn't know these)
- `DFL 4 de 2006 (LGSE)` --contiene--> `DFL 4 de 2006 (LGSE) — art. 10-1`  [EXTRACTED]
  ontologia/nodos_normas.csv → ontologia/nodos_articulos.csv
- `DFL 4 de 2006 (LGSE)` --contiene--> `DFL 4 de 2006 (LGSE) — art. 10-2`  [EXTRACTED]
  ontologia/nodos_normas.csv → ontologia/nodos_articulos.csv
- `DFL 4 de 2006 (LGSE)` --contiene--> `DFL 4 de 2006 (LGSE) — art. 10-3`  [EXTRACTED]
  ontologia/nodos_normas.csv → ontologia/nodos_articulos.csv
- `DFL 4 de 2006 (LGSE)` --contiene--> `DFL 4 de 2006 (LGSE) — art. 10-4`  [EXTRACTED]
  ontologia/nodos_normas.csv → ontologia/nodos_articulos.csv
- `DFL 4 de 2006 (LGSE)` --contiene--> `DFL 4 de 2006 (LGSE) — art. 10-5`  [EXTRACTED]
  ontologia/nodos_normas.csv → ontologia/nodos_articulos.csv

## Communities (7 total, 0 thin omitted)

### Community 0 - "DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…223"
Cohesion: 0.03
Nodes (73): DFL 4 de 2006 (LGSE), DFL 4 de 2006 (LGSE) — art. 100, DFL 4 de 2006 (LGSE) — art. 103, DFL 4 de 2006 (LGSE) — art. 104, DFL 4 de 2006 (LGSE) — art. 105, DFL 4 de 2006 (LGSE) — art. 106, DFL 4 de 2006 (LGSE) — art. 107, DFL 4 de 2006 (LGSE) — art. 108 (+65 more)

### Community 1 - "Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 8 ter…199 bis"
Cohesion: 0.04
Nodes (53): Ley 21.804 de 2026, Ley 21.804 de 2026 — art. único, DFL 4 de 2006 (LGSE) — art. 10-1, DFL 4 de 2006 (LGSE) — art. 10-2, DFL 4 de 2006 (LGSE) — art. 10-3, DFL 4 de 2006 (LGSE) — art. 10-4, DFL 4 de 2006 (LGSE) — art. 10-5, DFL 4 de 2006 (LGSE) — art. 10-6 (+45 more)

### Community 2 - "Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225"
Cohesion: 0.07
Nodes (30): Ley 20.936 de 2016, Ley 20.936 de 2016 — art. 1, DFL 4 de 2006 (LGSE) — art. 101, DFL 4 de 2006 (LGSE) — art. 111, DFL 4 de 2006 (LGSE) — art. 116, DFL 4 de 2006 (LGSE) — art. 118, DFL 4 de 2006 (LGSE) — art. 119, DFL 4 de 2006 (LGSE) — art. 128 (+22 more)

### Community 3 - "Ley 21.472 de 2022 + Ley 21.667 de 2024 + Ley 21.833 de 2026 | DFL 4 de 2006 (LGSE): arts."
Cohesion: 0.18
Nodes (13): Ley 21.472 de 2022, Ley 21.472 de 2022 — art. 1, Ley 21.667 de 2024, Ley 21.667 de 2024 — art. primero, Ley 21.833 de 2026, Ley 21.833 de 2026 — art. 1, DFL 4 de 2006 (LGSE) — art. 163, DFL 4 de 2006 (LGSE) — art. 183 (+5 more)

### Community 4 - "Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…115"
Cohesion: 0.15
Nodes (13): Ley 21.721 de 2024, Ley 21.721 de 2024 — art. único, DFL 4 de 2006 (LGSE) — art. 102, DFL 4 de 2006 (LGSE) — art. 114, DFL 4 de 2006 (LGSE) — art. 115, DFL 4 de 2006 (LGSE) — art. 77, DFL 4 de 2006 (LGSE) — art. 87, DFL 4 de 2006 (LGSE) — art. 91 (+5 more)

### Community 5 - "Ley 21.582 de 2023 | DFL 4 de 2006 (LGSE): arts. 20…98"
Cohesion: 0.22
Nodes (9): Ley 21.582 de 2023, Ley 21.582 de 2023 — art. 10, DFL 4 de 2006 (LGSE) — art. 20, DFL 4 de 2006 (LGSE) — art. 23, DFL 4 de 2006 (LGSE) — art. 29, DFL 4 de 2006 (LGSE) — art. 39, DFL 4 de 2006 (LGSE) — art. 62, DFL 4 de 2006 (LGSE) — art. 97 (+1 more)

### Community 6 - "Ley 21.505 de 2022 | DFL 4 de 2006 (LGSE): arts. 72-2…149 ter"
Cohesion: 0.25
Nodes (8): Ley 21.505 de 2022, Ley 21.505 de 2022 — art. único, DFL 4 de 2006 (LGSE) — art. 149, DFL 4 de 2006 (LGSE) — art. 149 bis, DFL 4 de 2006 (LGSE) — art. 149 ter, DFL 4 de 2006 (LGSE) — art. 72-17, DFL 4 de 2006 (LGSE) — art. 72-18, DFL 4 de 2006 (LGSE) — art. 72-2

## Knowledge Gaps
- **9 isolated node(s):** `Ley 20.936 de 2016`, `Ley 21.721 de 2024`, `Res. 156 exenta de 2025`, `Ley 21.804 de 2026`, `Ley 21.505 de 2022` (+4 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 9 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Ley 20.936 de 2016 — art. 1` connect `Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225` to `DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…223`, `Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 8 ter…199 bis`, `Ley 21.472 de 2022 + Ley 21.667 de 2024 + Ley 21.833 de 2026 | DFL 4 de 2006 (LGSE): arts.`, `Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…115`, `Ley 21.582 de 2023 | DFL 4 de 2006 (LGSE): arts. 20…98`, `Ley 21.505 de 2022 | DFL 4 de 2006 (LGSE): arts. 72-2…149 ter`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **What connects `Ley 20.936 de 2016`, `Ley 21.721 de 2024`, `Res. 156 exenta de 2025` to the rest of the system?**
  _9 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…223` be split into smaller, more focused modules?**
  _Cohesion score 0.0273972602739726 - nodes in this community are weakly interconnected._
- **Why does `Ley 21.804 de 2026 — art. único` connect `Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 8 ter…199 bis` to `Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225`, `Ley 21.472 de 2022 + Ley 21.667 de 2024 + Ley 21.833 de 2026 | DFL 4 de 2006 (LGSE): arts.`, `Ley 21.505 de 2022 | DFL 4 de 2006 (LGSE): arts. 72-2…149 ter`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Should `Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 8 ter…199 bis` be split into smaller, more focused modules?**
  _Cohesion score 0.03773584905660377 - nodes in this community are weakly interconnected._
- **Should `Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225` be split into smaller, more focused modules?**
  _Cohesion score 0.06666666666666667 - nodes in this community are weakly interconnected._