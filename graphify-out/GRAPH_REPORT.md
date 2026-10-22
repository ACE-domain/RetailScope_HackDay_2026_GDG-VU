# Graph Report - RetailScope_HackDay_2026_GDG-VU  (2026-10-22)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 24 nodes · 19 edges · 8 communities (1 shown, 7 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `00d85a14`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- index.py
- run_audit
- vercel.json
- read_root
- openai
- pydantic
- python-multipart
- uvicorn

## God Nodes (most connected - your core abstractions)
1. `run_audit()` - 5 edges
2. `RetailScope` - 4 edges
3. `read_root()` - 2 edges
4. `builds` - 1 edges
5. `routes` - 1 edges
6. `fastapi` - 1 edges
7. `Gemma 4` - 1 edges
8. `Google Gemini` - 1 edges
9. `Graphify` - 1 edges
10. `openai` - 0 edges

## Surprising Connections (you probably didn't know these)
- `RetailScope` --references--> `fastapi`  [INFERRED]
  README.md → requirements.txt

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **RetailScope Technology Stack** — readme_gemma_4, readme_google_gemini, readme_graphify, requirements_fastapi [EXTRACTED 0.90]

## Communities (8 total, 7 thin omitted)

### Community 2 - "vercel.json"
Cohesion: 0.40
Nodes (5): Gemma 4, Google Gemini, Graphify, RetailScope, fastapi

## Knowledge Gaps
- **8 isolated node(s):** `fastapi`, `Gemma 4`, `Google Gemini`, `Graphify`, `openai` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 17 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_audit()` connect `run_audit` to `index.py`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **What connects `fastapi`, `Gemma 4`, `Google Gemini` to the rest of the system?**
  _8 weakly-connected nodes found - possible documentation gaps or missing edges._