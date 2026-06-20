# Explainable KGQA with Classical Graph Algorithms

This project supports the paper **"Applying Graph Algorithms to Knowledge Graph
Construction for Academic Question-Answering Systems"**.

The goal is to build a lightweight end-to-end KGQA prototype where a user
question is converted into a graph pathfinding task. The returned path is used
as both the answer and the explanation.

## Research Scope

- Knowledge source: Computer Science Ontology (CSO)
- Graph library: NetworkX
- Core algorithms: BFS, DFS, Dijkstra, and A*
- QA type: concept-level relationship questions
- Main output: an explainable path between academic concepts

This version intentionally avoids LLMs, embeddings, and heavy NLP models so the
paper can isolate the behavior of classical graph algorithms. LLMs or knowledge
graph embeddings can be proposed later as future extensions.

## Project Structure

```text
kgqa_graph_algorithms/
├── main.py                     # End-to-end CLI QA demo
├── test_run.py                 # Algorithm comparison on one sample query
├── src/
│   ├── data_loader.py          # Load CSO triples
│   ├── graph_builder.py        # Build a NetworkX graph
│   ├── graph_pruner.py         # Extract a smaller subgraph from one root
│   ├── algorithms/             # BFS, DFS, Dijkstra, A*, heuristics
│   └── qa/                     # Query parser, QA engine, path verbalizer
├── data/
│   ├── raw/                    # Local CSO data, ignored by git
│   └── processed/              # Local pruned graphs, ignored by git
└── docs/study_materials/        # Research notes and study documents
```

## Run the End-to-End Demo

Use the local virtual environment:

```bash
.\.venv\Scripts\python.exe main.py --question "How is Data Mining related to Random Forests?" --algorithm dijkstra
```

Expected path:

```text
Data Mining -> Decision Tree -> Random Forests
```

You can also run the interactive CLI:

```bash
.\.venv\Scripts\python.exe main.py
```

Supported algorithms:

```text
bfs, dfs, dijkstra, astar
```

## Build a Pruned Subgraph

The current test graph uses `data_mining`, but the root can be changed for
experiments. In the local CSO file, `artificial_intelligence` exists, while the
exact node ID `data_science` was not found; use `data_mining` as the closest
data-oriented root unless a different CSO version contains `data_science`.

```bash
.\.venv\Scripts\python.exe src\graph_pruner.py --root artificial_intelligence --max-depth 4 --output data\processed\subgraph_ai.json
```

Then run QA on that graph:

```bash
.\.venv\Scripts\python.exe main.py --graph data\processed\subgraph_ai.json --question "How is Machine Learning related to Deep Learning?" --algorithm astar
```

## Compare Algorithms

```bash
.\.venv\Scripts\python.exe test_run.py
```

This prints the path, cost, runtime, and number of visited nodes for BFS, DFS,
Dijkstra, and A*. It also verifies the custom Dijkstra result against NetworkX.

## Paper-Oriented Notes

- BFS is useful for the shortest path by hop count.
- DFS is useful for exploration but does not guarantee the shortest path.
- Dijkstra is useful for weighted semantic distance.
- A* uses a simple depth-based heuristic to reduce search effort while keeping
  the reasoning process explainable.
- The path verbalizer turns graph edges into readable English explanations.
