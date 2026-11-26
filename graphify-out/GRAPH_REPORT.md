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
| Ley 20.928 de 2016 | completa | 0 | — |
| Ley 20.220 de 2007 | completa | 0 | — |
| Ley 20.571 de 2012 | completa | 0 | — |
| Ley 20.273 de 2008 | completa | 0 | — |
| Ley 20.720 de 2014 | completa | 0 | — |
| Ley 20.897 de 2016 | completa | 0 | — |
| Ley 21.076 de 2018 | completa | 0 | — |
| Ley 21.657 de 2024 | completa | 0 | — |
| Ley 21.647 de 2023 | completa | 0 | — |

> **Advertencia:** 1 norma(s) con cobertura parcial. Las respuestas sobre qué artículos modificó una ley pueden estar incompletas; los candidatos pendientes están en `datos/derivados/candidatos_por_fechaversion.csv` y la causa en `docs/diagnostico_truncamiento_bcn.md`.

## Cobertura de la historia por artículo

244 de 244 artículos del DFL 4 en el grafo tienen historia completa (todas las leyes posteriores al DFL 4 que la BCN anota en el artículo están en el grafo). Detalle de todo el DFL 4 en `datos/derivados/historia_articulos.csv`.

Aristas por relación, estado y método: contiene/verificada/regla: 271; deroga/inferida/regla: 2; deroga/verificada/regla: 7; implementa/verificada/regla: 1; modifica/verificada/manual: 52; modifica/verificada/regla: 297

## Summary
- 300 nodes · 630 edges · 17 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.7)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…223
- Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 10-1…199 bis
- Ley 20.701 de 2013 + Ley 20.897 de 2016 + Ley 21.582 de 2023 | DFL 4 de 2006 (LGSE): arts.
- Ley 20.402 de 2009 | DFL 4 de 2006 (LGSE): arts. 9…220
- Ley 21.304 de 2021 + Ley 21.472 de 2022 + Ley 21.667 de 2024 + Ley 21.806 de 2026 + Ley 21
- Ley 20.220 de 2007 + Ley 20.805 de 2015 | DFL 4 de 2006 (LGSE): arts. 27…147
- Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225
- Ley 21.194 de 2019 + Ley 21.647 de 2023 | DFL 4 de 2006 (LGSE): arts. 8 ter…193
- Ley 20.571 de 2012 + Ley 21.118 de 2018 + Ley 21.505 de 2022 | DFL 4 de 2006 (LGSE): arts.
- Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…115
- Ley 20.257 de 2008 + Ley 20.698 de 2013 | DFL 4 de 2006 (LGSE): arts. 79…174 bis
- Ley 20.273 de 2008 | DFL 4 de 2006 (LGSE): arts. 213…214
- Ley 20.928 de 2016 | DFL 4 de 2006 (LGSE): arts. 157…191
- Ley 20.999 de 2017 | DFL 4 de 2006 (LGSE): arts. 209…210
- Ley 20.720 de 2014 | Ley 20.720 de 2014: art. 391
- Ley 21.076 de 2018 | Ley 21.076 de 2018: art. único
- Ley 21.657 de 2024 | Ley 21.657 de 2024: art. único

## God Nodes (most connected - your core abstractions)
1. `DFL 4 de 2006 (LGSE)` - 244 edges
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

## Communities (17 total, 0 thin omitted)

### Community 0 - "DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…223"
Cohesion: 0.03
Nodes (62): DFL 4 de 2006 (LGSE), DFL 4 de 2006 (LGSE) — art. 100, DFL 4 de 2006 (LGSE) — art. 101, DFL 4 de 2006 (LGSE) — art. 103, DFL 4 de 2006 (LGSE) — art. 104, DFL 4 de 2006 (LGSE) — art. 105, DFL 4 de 2006 (LGSE) — art. 106, DFL 4 de 2006 (LGSE) — art. 107 (+54 more)

### Community 1 - "Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 10-1…199 bis"
Cohesion: 0.04
Nodes (47): Ley 21.804 de 2026, Ley 21.804 de 2026 — art. único, DFL 4 de 2006 (LGSE) — art. 10-1, DFL 4 de 2006 (LGSE) — art. 10-2, DFL 4 de 2006 (LGSE) — art. 10-3, DFL 4 de 2006 (LGSE) — art. 10-4, DFL 4 de 2006 (LGSE) — art. 10-5, DFL 4 de 2006 (LGSE) — art. 10-6 (+39 more)

### Community 2 - "Ley 20.701 de 2013 + Ley 20.897 de 2016 + Ley 21.582 de 2023 | DFL 4 de 2006 (LGSE): arts."
Cohesion: 0.07
Nodes (32): Ley 20.701 de 2013, Ley 20.701 de 2013 — art. único, Ley 20.897 de 2016, Ley 20.897 de 2016 — art. 2, Ley 21.582 de 2023, Ley 21.582 de 2023 — art. 10, DFL 4 de 2006 (LGSE) — art. 11, DFL 4 de 2006 (LGSE) — art. 19 (+24 more)

### Community 3 - "Ley 20.402 de 2009 | DFL 4 de 2006 (LGSE): arts. 9…220"
Cohesion: 0.07
Nodes (28): Ley 20.402 de 2009, Ley 20.402 de 2009 — art. 13, DFL 4 de 2006 (LGSE) — art. 112, DFL 4 de 2006 (LGSE) — art. 137, DFL 4 de 2006 (LGSE) — art. 146, DFL 4 de 2006 (LGSE) — art. 150, DFL 4 de 2006 (LGSE) — art. 151, DFL 4 de 2006 (LGSE) — art. 152 (+20 more)

### Community 4 - "Ley 21.304 de 2021 + Ley 21.472 de 2022 + Ley 21.667 de 2024 + Ley 21.806 de 2026 + Ley 21"
Cohesion: 0.09
Nodes (24): Ley 21.304 de 2021, Ley 21.304 de 2021 — art. único, Ley 21.472 de 2022, Ley 21.472 de 2022 — art. 1, Ley 21.667 de 2024, Ley 21.667 de 2024 — art. primero, Ley 21.806 de 2026, Ley 21.806 de 2026 — art. 101 (+16 more)

### Community 5 - "Ley 20.220 de 2007 + Ley 20.805 de 2015 | DFL 4 de 2006 (LGSE): arts. 27…147"
Cohesion: 0.11
Nodes (20): Ley 20.220 de 2007, Ley 20.220 de 2007 — art. único, Ley 20.805 de 2015, Ley 20.805 de 2015 — art. único, DFL 4 de 2006 (LGSE) — art. 108, DFL 4 de 2006 (LGSE) — art. 131, DFL 4 de 2006 (LGSE) — art. 131 bis, DFL 4 de 2006 (LGSE) — art. 131 ter (+12 more)

### Community 6 - "Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225"
Cohesion: 0.11
Nodes (19): Ley 20.936 de 2016, Ley 20.936 de 2016 — art. 1, DFL 4 de 2006 (LGSE) — art. 109, DFL 4 de 2006 (LGSE) — art. 128, DFL 4 de 2006 (LGSE) — art. 150 ter, DFL 4 de 2006 (LGSE) — art. 155, DFL 4 de 2006 (LGSE) — art. 158, DFL 4 de 2006 (LGSE) — art. 160 (+11 more)

### Community 7 - "Ley 21.194 de 2019 + Ley 21.647 de 2023 | DFL 4 de 2006 (LGSE): arts. 8 ter…193"
Cohesion: 0.14
Nodes (14): Ley 21.194 de 2019, Ley 21.194 de 2019 — art. único, Ley 21.647 de 2023, Ley 21.647 de 2023 — art. 88, DFL 4 de 2006 (LGSE) — art. 182, DFL 4 de 2006 (LGSE) — art. 182 bis, DFL 4 de 2006 (LGSE) — art. 183, DFL 4 de 2006 (LGSE) — art. 183 bis (+6 more)

### Community 8 - "Ley 20.571 de 2012 + Ley 21.118 de 2018 + Ley 21.505 de 2022 | DFL 4 de 2006 (LGSE): arts."
Cohesion: 0.19
Nodes (13): Ley 20.571 de 2012, Ley 20.571 de 2012 — art. único, Ley 21.118 de 2018, Ley 21.118 de 2018 — art. único, Ley 21.505 de 2022, Ley 21.505 de 2022 — art. único, DFL 4 de 2006 (LGSE) — art. 149, DFL 4 de 2006 (LGSE) — art. 149 bis (+5 more)

### Community 9 - "Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…115"
Cohesion: 0.15
Nodes (13): Ley 21.721 de 2024, Ley 21.721 de 2024 — art. único, DFL 4 de 2006 (LGSE) — art. 102, DFL 4 de 2006 (LGSE) — art. 114, DFL 4 de 2006 (LGSE) — art. 115, DFL 4 de 2006 (LGSE) — art. 77, DFL 4 de 2006 (LGSE) — art. 87, DFL 4 de 2006 (LGSE) — art. 91 (+5 more)

### Community 10 - "Ley 20.257 de 2008 + Ley 20.698 de 2013 | DFL 4 de 2006 (LGSE): arts. 79…174 bis"
Cohesion: 0.29
Nodes (7): Ley 20.257 de 2008, Ley 20.257 de 2008 — art. único, Ley 20.698 de 2013, Ley 20.698 de 2013 — art. 1, DFL 4 de 2006 (LGSE) — art. 150 bis, DFL 4 de 2006 (LGSE) — art. 174 bis, DFL 4 de 2006 (LGSE) — art. 79

### Community 11 - "Ley 20.273 de 2008 | DFL 4 de 2006 (LGSE): arts. 213…214"
Cohesion: 0.50
Nodes (4): Ley 20.273 de 2008, Ley 20.273 de 2008 — art. 2, DFL 4 de 2006 (LGSE) — art. 213, DFL 4 de 2006 (LGSE) — art. 214

### Community 12 - "Ley 20.928 de 2016 | DFL 4 de 2006 (LGSE): arts. 157…191"
Cohesion: 0.50
Nodes (4): Ley 20.928 de 2016, Ley 20.928 de 2016 — art. único, DFL 4 de 2006 (LGSE) — art. 157, DFL 4 de 2006 (LGSE) — art. 191

### Community 13 - "Ley 20.999 de 2017 | DFL 4 de 2006 (LGSE): arts. 209…210"
Cohesion: 0.50
Nodes (4): Ley 20.999 de 2017, Ley 20.999 de 2017 — art. 2, DFL 4 de 2006 (LGSE) — art. 209, DFL 4 de 2006 (LGSE) — art. 210

### Community 14 - "Ley 20.720 de 2014 | Ley 20.720 de 2014: art. 391"
Cohesion: 0.67
Nodes (3): Ley 20.720 de 2014, Ley 20.720 de 2014 — art. 391, DFL 4 de 2006 (LGSE) — art. 146 ter

### Community 15 - "Ley 21.076 de 2018 | Ley 21.076 de 2018: art. único"
Cohesion: 0.67
Nodes (3): Ley 21.076 de 2018, Ley 21.076 de 2018 — art. único, DFL 4 de 2006 (LGSE) — art. 139 bis

### Community 16 - "Ley 21.657 de 2024 | Ley 21.657 de 2024: art. único"
Cohesion: 0.67
Nodes (3): Ley 21.657 de 2024, Ley 21.657 de 2024 — art. único, DFL 4 de 2006 (LGSE) — art. 191 bis

## Knowledge Gaps
- **28 isolated node(s):** `Ley 20.936 de 2016`, `Ley 21.721 de 2024`, `Res. 156 exenta de 2025`, `Ley 21.804 de 2026`, `Ley 21.505 de 2022` (+23 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 28 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Ley 20.936 de 2016 — art. 1` connect `Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225` to `DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…223`, `Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 10-1…199 bis`, `Ley 20.701 de 2013 + Ley 20.897 de 2016 + Ley 21.582 de 2023 | DFL 4 de 2006 (LGSE): arts.`, `Ley 20.402 de 2009 | DFL 4 de 2006 (LGSE): arts. 9…220`, `Ley 21.304 de 2021 + Ley 21.472 de 2022 + Ley 21.667 de 2024 + Ley 21.806 de 2026 + Ley 21`, `Ley 20.220 de 2007 + Ley 20.805 de 2015 | DFL 4 de 2006 (LGSE): arts. 27…147`, `Ley 20.571 de 2012 + Ley 21.118 de 2018 + Ley 21.505 de 2022 | DFL 4 de 2006 (LGSE): arts.`, `Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…115`, `Ley 20.257 de 2008 + Ley 20.698 de 2013 | DFL 4 de 2006 (LGSE): arts. 79…174 bis`, `Ley 20.928 de 2016 | DFL 4 de 2006 (LGSE): arts. 157…191`, `Ley 20.999 de 2017 | DFL 4 de 2006 (LGSE): arts. 209…210`, `Ley 20.720 de 2014 | Ley 20.720 de 2014: art. 391`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **What connects `Ley 20.936 de 2016`, `Ley 21.721 de 2024`, `Res. 156 exenta de 2025` to the rest of the system?**
  _28 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…223` be split into smaller, more focused modules?**
  _Cohesion score 0.03225806451612903 - nodes in this community are weakly interconnected._
- **Why does `Ley 21.804 de 2026 — art. único` connect `Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 10-1…199 bis` to `Ley 20.402 de 2009 | DFL 4 de 2006 (LGSE): arts. 9…220`, `Ley 20.220 de 2007 + Ley 20.805 de 2015 | DFL 4 de 2006 (LGSE): arts. 27…147`, `Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225`, `Ley 21.194 de 2019 + Ley 21.647 de 2023 | DFL 4 de 2006 (LGSE): arts. 8 ter…193`, `Ley 20.571 de 2012 + Ley 21.118 de 2018 + Ley 21.505 de 2022 | DFL 4 de 2006 (LGSE): arts.`, `Ley 20.257 de 2008 + Ley 20.698 de 2013 | DFL 4 de 2006 (LGSE): arts. 79…174 bis`, `Ley 20.928 de 2016 | DFL 4 de 2006 (LGSE): arts. 157…191`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Should `Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 10-1…199 bis` be split into smaller, more focused modules?**
  _Cohesion score 0.0425531914893617 - nodes in this community are weakly interconnected._
- **Why does `Ley 20.402 de 2009 — art. 13` connect `Ley 20.402 de 2009 | DFL 4 de 2006 (LGSE): arts. 9…220` to `Ley 21.804 de 2026 | DFL 4 de 2006 (LGSE): arts. 10-1…199 bis`, `Ley 20.701 de 2013 + Ley 20.897 de 2016 + Ley 21.582 de 2023 | DFL 4 de 2006 (LGSE): arts.`, `Ley 20.220 de 2007 + Ley 20.805 de 2015 | DFL 4 de 2006 (LGSE): arts. 27…147`, `Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225`, `Ley 21.194 de 2019 + Ley 21.647 de 2023 | DFL 4 de 2006 (LGSE): arts. 8 ter…193`, `Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…115`, `Ley 20.999 de 2017 | DFL 4 de 2006 (LGSE): arts. 209…210`?**
  _High betweenness centrality (0.000) - this node is a cross-community bridge._
- **Should `Ley 20.701 de 2013 + Ley 20.897 de 2016 + Ley 21.582 de 2023 | DFL 4 de 2006 (LGSE): arts.` be split into smaller, more focused modules?**
  _Cohesion score 0.06653225806451613 - nodes in this community are weakly interconnected._