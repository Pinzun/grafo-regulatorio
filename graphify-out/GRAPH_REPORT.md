# Graph Report - grafo-regulatorio  (2026-11-26)

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
| Ley 20.701 de 2013 | completa | 0 | — |
| Ley 20.402 de 2009 | parcial | 0 | 8811969 |
| Ley 20.805 de 2015 | completa | 0 | — |
| Ley 21.194 de 2019 | completa | 0 | — |
| Ley 21.304 de 2021 | completa | 0 | — |
| Ley 21.806 de 2026 | completa | 0 | — |
| Ley 21.118 de 2018 | completa | 0 | — |
| Ley 20.698 de 2013 | completa | 0 | — |
| Ley 20.257 de 2008 | completa | 0 | — |
| Ley 20.999 de 2017 | completa | 0 | — |

> **Advertencia:** 1 norma(s) con cobertura parcial. Las respuestas sobre qué artículos modificó una ley pueden estar incompletas; los candidatos pendientes están en `datos/derivados/candidatos_por_fechaversion.csv` y la causa en `docs/diagnostico_truncamiento_bcn.md`.

## Cobertura de la historia por artículo

224 de 239 artículos del DFL 4 en el grafo tienen historia completa (todas las leyes posteriores al DFL 4 que la BCN anota en el artículo están en el grafo). Detalle de todo el DFL 4 en `datos/derivados/historia_articulos.csv`.

| Artículo | Leyes que faltan |
|---|---|
| 25 | 20220 |
| 34 bis | 20897 |
| 131 | 20928 |
| 132 | 20928 |
| 133 | 20220 |
| 146 | 20220 |
| 146 ter | 20220, 20720 |
| 149 | 20571 |
| 149 bis | 20571 |
| 149 quater | 20571 |
| 157 | 20928 |
| 184 | 20928 |
| 191 | 20928 |
| 193 | 21647 |
| 225 | 20928 |

Aristas por relación, estado y método: contiene/verificada/regla: 257; deroga/inferida/regla: 2; deroga/verificada/regla: 7; implementa/verificada/regla: 1; modifica/verificada/manual: 52; modifica/verificada/regla: 273

## Summary
- 277 nodes · 592 edges · 14 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.7)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…212-12
- Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 10-1…199 bis
- Ley 20.701 de 2013 + Ley 21.582 de 2023 | DFL 4 de 2006 (LGSE): arts. 11…98
- Ley 20.402 de 2009 | DFL 4 de 2006 (LGSE): arts. 9…220
- Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225
- Ley 20.805 de 2015 | DFL 4 de 2006 (LGSE): arts. 108…147
- Ley 21.304 de 2021 + Ley 21.806 de 2026 | DFL 4 de 2006 (LGSE): arts. 141…207-8
- Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…115
- Ley 21.194 de 2019 | DFL 4 de 2006 (LGSE): arts. 8 ter…193
- Ley 21.118 de 2018 + Ley 21.505 de 2022 | DFL 4 de 2006 (LGSE): arts. 72-2…149 ter
- Ley 21.472 de 2022 + Ley 21.667 de 2024 + Ley 21.833 de 2026 | DFL 4 de 2006 (LGSE): arts.
- Ley 20.257 de 2008 | DFL 4 de 2006 (LGSE): arts. 79…157
- Ley 20.698 de 2013 | DFL 4 de 2006 (LGSE): arts. 150 bis…174 bis
- Ley 20.999 de 2017 | DFL 4 de 2006 (LGSE): arts. 209…210

## God Nodes (most connected - your core abstractions)
1. `DFL 4 de 2006 (LGSE)` - 239 edges
2. `Ley 20.936 de 2016 — art. 1` - 127 edges
3. `Ley 21.804 de 2026 — art. único` - 58 edges
4. `Ley 20.402 de 2009 — art. 13` - 44 edges
5. `Ley 20.701 de 2013 — art. único` - 24 edges
6. `Ley 20.805 de 2015 — art. único` - 16 edges
7. `Ley 21.194 de 2019 — art. único` - 12 edges
8. `Ley 21.721 de 2024 — art. único` - 11 edges
9. `Ley 21.833 de 2026 — art. 1` - 9 edges
10. `Ley 21.505 de 2022 — art. único` - 8 edges

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

## Communities (14 total, 0 thin omitted)

### Community 0 - "DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…212-12"
Cohesion: 0.03
Nodes (63): DFL 4 de 2006 (LGSE), DFL 4 de 2006 (LGSE) — art. 100, DFL 4 de 2006 (LGSE) — art. 101, DFL 4 de 2006 (LGSE) — art. 103, DFL 4 de 2006 (LGSE) — art. 104, DFL 4 de 2006 (LGSE) — art. 105, DFL 4 de 2006 (LGSE) — art. 106, DFL 4 de 2006 (LGSE) — art. 107 (+55 more)

### Community 1 - "Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 10-1…199 bis"
Cohesion: 0.04
Nodes (48): Ley 21.804 de 2026, Ley 21.804 de 2026 — art. único, DFL 4 de 2006 (LGSE) — art. 10-1, DFL 4 de 2006 (LGSE) — art. 10-2, DFL 4 de 2006 (LGSE) — art. 10-3, DFL 4 de 2006 (LGSE) — art. 10-4, DFL 4 de 2006 (LGSE) — art. 10-5, DFL 4 de 2006 (LGSE) — art. 10-6 (+40 more)

### Community 2 - "Ley 20.701 de 2013 + Ley 21.582 de 2023 | DFL 4 de 2006 (LGSE): arts. 11…98"
Cohesion: 0.07
Nodes (31): Ley 20.701 de 2013, Ley 20.701 de 2013 — art. único, Ley 21.582 de 2023, Ley 21.582 de 2023 — art. 10, DFL 4 de 2006 (LGSE) — art. 11, DFL 4 de 2006 (LGSE) — art. 19, DFL 4 de 2006 (LGSE) — art. 20, DFL 4 de 2006 (LGSE) — art. 21 (+23 more)

### Community 3 - "Ley 20.402 de 2009 | DFL 4 de 2006 (LGSE): arts. 9…220"
Cohesion: 0.07
Nodes (28): Ley 20.402 de 2009, Ley 20.402 de 2009 — art. 13, DFL 4 de 2006 (LGSE) — art. 112, DFL 4 de 2006 (LGSE) — art. 137, DFL 4 de 2006 (LGSE) — art. 146, DFL 4 de 2006 (LGSE) — art. 150, DFL 4 de 2006 (LGSE) — art. 151, DFL 4 de 2006 (LGSE) — art. 152 (+20 more)

### Community 4 - "Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225"
Cohesion: 0.10
Nodes (20): Ley 20.936 de 2016, Ley 20.936 de 2016 — art. 1, DFL 4 de 2006 (LGSE) — art. 109, DFL 4 de 2006 (LGSE) — art. 128, DFL 4 de 2006 (LGSE) — art. 150 ter, DFL 4 de 2006 (LGSE) — art. 155, DFL 4 de 2006 (LGSE) — art. 158, DFL 4 de 2006 (LGSE) — art. 160 (+12 more)

### Community 5 - "Ley 20.805 de 2015 | DFL 4 de 2006 (LGSE): arts. 108…147"
Cohesion: 0.12
Nodes (16): Ley 20.805 de 2015, Ley 20.805 de 2015 — art. único, DFL 4 de 2006 (LGSE) — art. 108, DFL 4 de 2006 (LGSE) — art. 131, DFL 4 de 2006 (LGSE) — art. 131 bis, DFL 4 de 2006 (LGSE) — art. 131 ter, DFL 4 de 2006 (LGSE) — art. 132, DFL 4 de 2006 (LGSE) — art. 133 (+8 more)

### Community 6 - "Ley 21.304 de 2021 + Ley 21.806 de 2026 | DFL 4 de 2006 (LGSE): arts. 141…207-8"
Cohesion: 0.14
Nodes (14): Ley 21.304 de 2021, Ley 21.304 de 2021 — art. único, Ley 21.806 de 2026, Ley 21.806 de 2026 — art. 101, DFL 4 de 2006 (LGSE) — art. 141, DFL 4 de 2006 (LGSE) — art. 207-1, DFL 4 de 2006 (LGSE) — art. 207-2, DFL 4 de 2006 (LGSE) — art. 207-2 bis (+6 more)

### Community 7 - "Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…115"
Cohesion: 0.15
Nodes (13): Ley 21.721 de 2024, Ley 21.721 de 2024 — art. único, DFL 4 de 2006 (LGSE) — art. 102, DFL 4 de 2006 (LGSE) — art. 114, DFL 4 de 2006 (LGSE) — art. 115, DFL 4 de 2006 (LGSE) — art. 77, DFL 4 de 2006 (LGSE) — art. 87, DFL 4 de 2006 (LGSE) — art. 91 (+5 more)

### Community 8 - "Ley 21.194 de 2019 | DFL 4 de 2006 (LGSE): arts. 8 ter…193"
Cohesion: 0.17
Nodes (12): Ley 21.194 de 2019, Ley 21.194 de 2019 — art. único, DFL 4 de 2006 (LGSE) — art. 182, DFL 4 de 2006 (LGSE) — art. 182 bis, DFL 4 de 2006 (LGSE) — art. 183, DFL 4 de 2006 (LGSE) — art. 183 bis, DFL 4 de 2006 (LGSE) — art. 185, DFL 4 de 2006 (LGSE) — art. 187 (+4 more)

### Community 9 - "Ley 21.118 de 2018 + Ley 21.505 de 2022 | DFL 4 de 2006 (LGSE): arts. 72-2…149 ter"
Cohesion: 0.22
Nodes (10): Ley 21.118 de 2018, Ley 21.118 de 2018 — art. único, Ley 21.505 de 2022, Ley 21.505 de 2022 — art. único, DFL 4 de 2006 (LGSE) — art. 149, DFL 4 de 2006 (LGSE) — art. 149 bis, DFL 4 de 2006 (LGSE) — art. 149 ter, DFL 4 de 2006 (LGSE) — art. 72-17 (+2 more)

### Community 10 - "Ley 21.472 de 2022 + Ley 21.667 de 2024 + Ley 21.833 de 2026 | DFL 4 de 2006 (LGSE): arts."
Cohesion: 0.24
Nodes (10): Ley 21.472 de 2022, Ley 21.472 de 2022 — art. 1, Ley 21.667 de 2024, Ley 21.667 de 2024 — art. primero, Ley 21.833 de 2026, Ley 21.833 de 2026 — art. 1, DFL 4 de 2006 (LGSE) — art. 183 ter, DFL 4 de 2006 (LGSE) — art. 212-13 (+2 more)

### Community 11 - "Ley 20.257 de 2008 | DFL 4 de 2006 (LGSE): arts. 79…157"
Cohesion: 0.50
Nodes (4): Ley 20.257 de 2008, Ley 20.257 de 2008 — art. único, DFL 4 de 2006 (LGSE) — art. 157, DFL 4 de 2006 (LGSE) — art. 79

### Community 12 - "Ley 20.698 de 2013 | DFL 4 de 2006 (LGSE): arts. 150 bis…174 bis"
Cohesion: 0.50
Nodes (4): Ley 20.698 de 2013, Ley 20.698 de 2013 — art. 1, DFL 4 de 2006 (LGSE) — art. 150 bis, DFL 4 de 2006 (LGSE) — art. 174 bis

### Community 13 - "Ley 20.999 de 2017 | DFL 4 de 2006 (LGSE): arts. 209…210"
Cohesion: 0.50
Nodes (4): Ley 20.999 de 2017, Ley 20.999 de 2017 — art. 2, DFL 4 de 2006 (LGSE) — art. 209, DFL 4 de 2006 (LGSE) — art. 210

## Knowledge Gaps
- **19 isolated node(s):** `Ley 20.936 de 2016`, `Ley 21.721 de 2024`, `Res. 156 exenta de 2025`, `Ley 21.804 de 2026`, `Ley 21.505 de 2022` (+14 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 19 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Ley 20.936 de 2016 — art. 1` connect `Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225` to `DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…212-12`, `Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 10-1…199 bis`, `Ley 20.701 de 2013 + Ley 21.582 de 2023 | DFL 4 de 2006 (LGSE): arts. 11…98`, `Ley 20.402 de 2009 | DFL 4 de 2006 (LGSE): arts. 9…220`, `Ley 20.805 de 2015 | DFL 4 de 2006 (LGSE): arts. 108…147`, `Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…115`, `Ley 21.118 de 2018 + Ley 21.505 de 2022 | DFL 4 de 2006 (LGSE): arts. 72-2…149 ter`, `Ley 21.472 de 2022 + Ley 21.667 de 2024 + Ley 21.833 de 2026 | DFL 4 de 2006 (LGSE): arts.`, `Ley 20.257 de 2008 | DFL 4 de 2006 (LGSE): arts. 79…157`, `Ley 20.698 de 2013 | DFL 4 de 2006 (LGSE): arts. 150 bis…174 bis`, `Ley 20.999 de 2017 | DFL 4 de 2006 (LGSE): arts. 209…210`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **What connects `Ley 20.936 de 2016`, `Ley 21.721 de 2024`, `Res. 156 exenta de 2025` to the rest of the system?**
  _19 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…212-12` be split into smaller, more focused modules?**
  _Cohesion score 0.031746031746031744 - nodes in this community are weakly interconnected._
- **Why does `Ley 21.804 de 2026 — art. único` connect `Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 10-1…199 bis` to `Ley 20.402 de 2009 | DFL 4 de 2006 (LGSE): arts. 9…220`, `Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225`, `Ley 20.805 de 2015 | DFL 4 de 2006 (LGSE): arts. 108…147`, `Ley 21.194 de 2019 | DFL 4 de 2006 (LGSE): arts. 8 ter…193`, `Ley 21.118 de 2018 + Ley 21.505 de 2022 | DFL 4 de 2006 (LGSE): arts. 72-2…149 ter`, `Ley 20.257 de 2008 | DFL 4 de 2006 (LGSE): arts. 79…157`, `Ley 20.698 de 2013 | DFL 4 de 2006 (LGSE): arts. 150 bis…174 bis`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Should `Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 10-1…199 bis` be split into smaller, more focused modules?**
  _Cohesion score 0.041666666666666664 - nodes in this community are weakly interconnected._
- **Why does `Ley 20.402 de 2009 — art. 13` connect `Ley 20.402 de 2009 | DFL 4 de 2006 (LGSE): arts. 9…220` to `Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 10-1…199 bis`, `Ley 20.701 de 2013 + Ley 21.582 de 2023 | DFL 4 de 2006 (LGSE): arts. 11…98`, `Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225`, `Ley 20.805 de 2015 | DFL 4 de 2006 (LGSE): arts. 108…147`, `Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…115`, `Ley 21.194 de 2019 | DFL 4 de 2006 (LGSE): arts. 8 ter…193`, `Ley 20.999 de 2017 | DFL 4 de 2006 (LGSE): arts. 209…210`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Should `Ley 20.701 de 2013 + Ley 21.582 de 2023 | DFL 4 de 2006 (LGSE): arts. 11…98` be split into smaller, more focused modules?**
  _Cohesion score 0.06881720430107527 - nodes in this community are weakly interconnected._