# Graph Report - .  (2026-06-18)

## Corpus Check
- Corpus is ~18,732 words - fits in a single context window. You may not need a graph.

## Summary
- 20 nodes · 31 edges · 3 communities
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_SMP Negeri 1 Bogor Admissions|SMP Negeri 1 Bogor Admissions]]
- [[_COMMUNITY_SMP Negeri 3 Bogor Admissions|SMP Negeri 3 Bogor Admissions]]
- [[_COMMUNITY_Cross-School Prestasi Pathways|Cross-School Prestasi Pathways]]

## God Nodes (most connected - your core abstractions)
1. `SMP NEGERI 1 BOGOR` - 10 edges
2. `SMP NEGERI 3 BOGOR` - 10 edges
3. `Jalur Afirmasi (SMPN 1)` - 3 edges
4. `Jalur Domisili (SMPN 1)` - 3 edges
5. `Jalur Mutasi (SMPN 1)` - 3 edges
6. `Jalur Prestasi (SMPN 1)` - 3 edges
7. `Jalur Afirmasi (SMPN 3)` - 3 edges
8. `Jalur Domisili (SMPN 3)` - 3 edges
9. `Jalur Mutasi (SMPN 3)` - 3 edges
10. `Jalur Prestasi (SMPN 3)` - 3 edges

## Surprising Connections (you probably didn't know these)
- `SMP NEGERI 1 BOGOR` --semantically_similar_to--> `SMP NEGERI 3 BOGOR`  [INFERRED] [semantically similar]
  raw/smpn1_overview.md → raw/smpn3_overview.md
- `Jalur Afirmasi (SMPN 1)` --semantically_similar_to--> `Jalur Afirmasi (SMPN 3)`  [INFERRED] [semantically similar]
  raw/smpn1_overview.md → raw/smpn3_overview.md
- `Jalur Domisili (SMPN 1)` --semantically_similar_to--> `Jalur Domisili (SMPN 3)`  [INFERRED] [semantically similar]
  raw/smpn1_overview.md → raw/smpn3_overview.md
- `Jalur Mutasi (SMPN 1)` --semantically_similar_to--> `Jalur Mutasi (SMPN 3)`  [INFERRED] [semantically similar]
  raw/smpn1_overview.md → raw/smpn3_overview.md
- `Jalur Prestasi Document (SMPN 1)` --references--> `SMP NEGERI 1 BOGOR`  [EXTRACTED]
  raw/smpn1_pathway_prestasi.md → raw/smpn1_overview.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **SMPN 1 Bogor Admission System** — raw_smpn1_overview_smp_negeri_1_bogor, raw_smpn1_overview_pathway_afirmasi, raw_smpn1_overview_pathway_domisili, raw_smpn1_overview_pathway_mutasi, raw_smpn1_overview_pathway_prestasi [EXTRACTED 1.00]
- **SMPN 3 Bogor Admission System** — raw_smpn3_overview_smp_negeri_3_bogor, raw_smpn3_overview_pathway_afirmasi, raw_smpn3_overview_pathway_domisili, raw_smpn3_overview_pathway_mutasi, raw_smpn3_overview_pathway_prestasi [EXTRACTED 1.00]

## Communities (3 total, 0 thin omitted)

### Community 0 - "SMP Negeri 1 Bogor Admissions"
Cohesion: 0.36
Nodes (8): SMP NEGERI 1 BOGOR Overview Document, Jalur Afirmasi (SMPN 1), Jalur Domisili (SMPN 1), Jalur Mutasi (SMPN 1), SMP NEGERI 1 BOGOR, Jalur Afirmasi Document (SMPN 1), Jalur Domisili Document (SMPN 1), Jalur Mutasi Document (SMPN 1)

### Community 1 - "SMP Negeri 3 Bogor Admissions"
Cohesion: 0.36
Nodes (8): SMP NEGERI 3 BOGOR Overview Document, Jalur Afirmasi (SMPN 3), Jalur Domisili (SMPN 3), Jalur Mutasi (SMPN 3), SMP NEGERI 3 BOGOR, Jalur Afirmasi Document (SMPN 3), Jalur Domisili Document (SMPN 3), Jalur Mutasi Document (SMPN 3)

### Community 2 - "Cross-School Prestasi Pathways"
Cohesion: 0.50
Nodes (4): Jalur Prestasi (SMPN 1), Jalur Prestasi Document (SMPN 1), Jalur Prestasi (SMPN 3), Jalur Prestasi Document (SMPN 3)

## Knowledge Gaps
- **2 isolated node(s):** `SMP NEGERI 1 BOGOR Overview Document`, `SMP NEGERI 3 BOGOR Overview Document`
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SMP NEGERI 1 BOGOR` connect `SMP Negeri 1 Bogor Admissions` to `SMP Negeri 3 Bogor Admissions`, `Cross-School Prestasi Pathways`?**
  _High betweenness centrality (0.550) - this node is a cross-community bridge._
- **Why does `SMP NEGERI 3 BOGOR` connect `SMP Negeri 3 Bogor Admissions` to `SMP Negeri 1 Bogor Admissions`, `Cross-School Prestasi Pathways`?**
  _High betweenness centrality (0.550) - this node is a cross-community bridge._
- **Why does `Jalur Afirmasi (SMPN 1)` connect `SMP Negeri 1 Bogor Admissions` to `SMP Negeri 3 Bogor Admissions`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **What connects `SMP NEGERI 1 BOGOR Overview Document`, `SMP NEGERI 3 BOGOR Overview Document` to the rest of the system?**
  _2 weakly-connected nodes found - possible documentation gaps or missing edges._