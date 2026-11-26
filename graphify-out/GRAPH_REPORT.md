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

Aristas por relación, estado y método: contiene/verificada/regla: 129; implementa/verificada/regla: 1; modifica/verificada/manual: 52; modifica/verificada/regla: 84

## Summary
- 133 nodes · 266 edges · 3 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…223
- Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225
- Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…115

## God Nodes (most connected - your core abstractions)
1. `DFL 4 de 2006 (LGSE)` - 127 edges
2. `Ley 20.936 de 2016 — art. 1` - 127 edges
3. `Ley 21.721 de 2024 — art. único` - 11 edges
4. `DFL 4 de 2006 (LGSE) — art. 77` - 3 edges
5. `DFL 4 de 2006 (LGSE) — art. 87` - 3 edges
6. `DFL 4 de 2006 (LGSE) — art. 91` - 3 edges
7. `DFL 4 de 2006 (LGSE) — art. 91 bis` - 3 edges
8. `DFL 4 de 2006 (LGSE) — art. 95` - 3 edges
9. `DFL 4 de 2006 (LGSE) — art. 96` - 3 edges
10. `DFL 4 de 2006 (LGSE) — art. 99` - 3 edges

## Surprising Connections (you probably didn't know these)
- `DFL 4 de 2006 (LGSE)` --contiene--> `DFL 4 de 2006 (LGSE) — art. 106`  [EXTRACTED]
  ontologia/nodos_normas.csv → ontologia/nodos_articulos.csv
- `DFL 4 de 2006 (LGSE)` --contiene--> `DFL 4 de 2006 (LGSE) — art. 108`  [EXTRACTED]
  ontologia/nodos_normas.csv → ontologia/nodos_articulos.csv
- `DFL 4 de 2006 (LGSE)` --contiene--> `DFL 4 de 2006 (LGSE) — art. 121`  [EXTRACTED]
  ontologia/nodos_normas.csv → ontologia/nodos_articulos.csv
- `DFL 4 de 2006 (LGSE)` --contiene--> `DFL 4 de 2006 (LGSE) — art. 122`  [EXTRACTED]
  ontologia/nodos_normas.csv → ontologia/nodos_articulos.csv
- `DFL 4 de 2006 (LGSE)` --contiene--> `DFL 4 de 2006 (LGSE) — art. 128`  [EXTRACTED]
  ontologia/nodos_normas.csv → ontologia/nodos_articulos.csv

## Communities (3 total, 0 thin omitted)

### Community 0 - "DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…223"
Cohesion: 0.02
Nodes (87): DFL 4 de 2006 (LGSE), DFL 4 de 2006 (LGSE) — art. 100, DFL 4 de 2006 (LGSE) — art. 101, DFL 4 de 2006 (LGSE) — art. 103, DFL 4 de 2006 (LGSE) — art. 104, DFL 4 de 2006 (LGSE) — art. 105, DFL 4 de 2006 (LGSE) — art. 107, DFL 4 de 2006 (LGSE) — art. 109 (+79 more)

### Community 1 - "Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225"
Cohesion: 0.06
Nodes (33): Ley 20.936 de 2016, Ley 20.936 de 2016 — art. 1, DFL 4 de 2006 (LGSE) — art. 106, DFL 4 de 2006 (LGSE) — art. 108, DFL 4 de 2006 (LGSE) — art. 121, DFL 4 de 2006 (LGSE) — art. 122, DFL 4 de 2006 (LGSE) — art. 128, DFL 4 de 2006 (LGSE) — art. 135 quinquies (+25 more)

### Community 2 - "Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…115"
Cohesion: 0.15
Nodes (13): Ley 21.721 de 2024, Ley 21.721 de 2024 — art. único, DFL 4 de 2006 (LGSE) — art. 102, DFL 4 de 2006 (LGSE) — art. 114, DFL 4 de 2006 (LGSE) — art. 115, DFL 4 de 2006 (LGSE) — art. 77, DFL 4 de 2006 (LGSE) — art. 87, DFL 4 de 2006 (LGSE) — art. 91 (+5 more)

## Knowledge Gaps
- **3 isolated node(s):** `Ley 20.936 de 2016`, `Ley 21.721 de 2024`, `Res. 156 exenta de 2025`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 3 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Ley 20.936 de 2016 — art. 1` connect `Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225` to `DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…223`, `Ley 21.721 de 2024 + Res. 156 exenta de 2025 | DFL 4 de 2006 (LGSE): arts. 77…115`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **What connects `Ley 20.936 de 2016`, `Ley 21.721 de 2024`, `Res. 156 exenta de 2025` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `DFL 4 de 2006 (LGSE) | DFL 4 de 2006 (LGSE): arts. 8 bis…223` be split into smaller, more focused modules?**
  _Cohesion score 0.022988505747126436 - nodes in this community are weakly interconnected._
- **Should `Ley 20.936 de 2016 | DFL 4 de 2006 (LGSE): arts. 7…225` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._