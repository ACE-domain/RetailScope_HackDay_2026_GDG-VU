# Graph Report - RetailScope_HackDay_2026_GDG-VU  (2026-10-22)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 15 nodes · 15 edges · 4 communities (0 shown, 4 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `569adf68`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_audit
- vercel.json
- read_root

## God Nodes (most connected - your core abstractions)
1. `run_audit()` - 5 edges
2. `read_root()` - 2 edges
3. `builds` - 1 edges
4. `routes` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (4 total, 4 thin omitted)

## Knowledge Gaps
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_audit()` connect `run_audit` to `index.py`?**
  _High betweenness centrality (0.214) - this node is a cross-community bridge._
- **Why does `read_root()` connect `read_root` to `index.py`?**
  _High betweenness centrality (0.110) - this node is a cross-community bridge._