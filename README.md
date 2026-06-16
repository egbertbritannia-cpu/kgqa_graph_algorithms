# Applying Graph Algorithms to Knowledge Graph Construction for Academic Question-Answering Systems

## Research Overview
In the era of information explosion, storing and exploiting data efficiently has become increasingly important. This research focuses on applying classical graph algorithms to organize and query a knowledge graph of academic concepts, aiming to support concept-level question answering in an explainable manner.

**Keywords**: Knowledge Graph, Graph Algorithms, Data Retrieval, Semantic Reasoning, Shortest Path, Concept Question Answering.

## Team Members
- Nguyễn Thanh Điền (Mentor)
- Quách Thế Dương (SE203060)
- Hoàng Đức Tài (SE201718)
- Phạm Văn Đức Duy (SE194521)

## Objectives
1. Construct a domain-specific knowledge graph by modeling academic concepts and their semantic relationships.
2. Implement and evaluate classical graph algorithms (BFS, DFS, Dijkstra, A*) to support multi-hop reasoning.
3. Develop a transparent concept-level question-answering framework utilizing the shortest paths to serve as both the answer and logical explanation.

## Project Structure
- `data/`: Contains the collected concept data and knowledge graph structure.
- `src/`: Core Python modules for graph construction, algorithms (BFS, DFS, Dijkstra, A*), and QA logic.
- `notebooks/`: Jupyter notebooks for data analysis and algorithm evaluation.
- `docs/`: Additional documentation and research reports.

## Methodology
1. **Data Collection & Graph Construction**: Extract concepts and relationships from an academic domain and structure them as nodes and typed edges.
2. **Algorithm Implementation**: Implement traversal methods (BFS, DFS) to trace relationships and shortest-path algorithms (Dijkstra, A*) to measure concept distances.
3. **Question-Answering Module**: Translate user queries into pathfinding tasks and verbalize the retrieved path.
4. **Evaluation**: Compare execution time and path relevance of the algorithms.
