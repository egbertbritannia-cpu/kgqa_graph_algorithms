# Applying Graph Algorithms to Knowledge Graph Construction for Academic Question-Answering Systems

**Mentor:** Nguyễn Thanh Điền  
**Members:**
- Quách Thế Dương (SE203060)
- Hoàng Đức Tài (SE201718)
- Phạm Văn Đức Duy (SE194521)

## 📌 Research Overview
This research focuses on applying classical graph algorithms (BFS, DFS, Dijkstra, A*) to organize and query a knowledge graph of academic concepts. The goal is to support concept-level question answering in an explainable manner, where the retrieved path between concepts serves as both the answer and its logical explanation.

**Keywords:** Knowledge Graph, Graph Algorithms, Data Retrieval, Semantic Reasoning, Shortest Path, Concept Question Answering.

## 🎯 Objectives
1. **Knowledge Graph Construction:** Model academic concepts and their semantic relationships into a machine-actionable structure.
2. **Multi-hop Reasoning:** Implement and evaluate classical graph algorithms (BFS, DFS, Dijkstra, A*) to measure distances and trace explicit relationships between concepts.
3. **Explainable QA Framework:** Develop a transparent concept-level question-answering system using shortest paths.

## 🛠 Approach & Methodology
1. **Data Collection:** Extract concepts and relationships from a narrowly scoped academic domain.
2. **Algorithm Implementation:** Develop Python-based modules for graph traversal and shortest-path calculation.
3. **Question-Answering Module:** Translate user queries into node-to-node pathfinding tasks and verbalize the results.
4. **Evaluation:** Compare the performance of algorithms in terms of execution time and path relevance.

## 📂 Project Structure
- `src/`: Core logic and Python modules for graph algorithms and the QA system.
- `data/`: Datasets, raw concept data, and graph database exports.
- `notebooks/`: Jupyter notebooks for data analysis, exploration, and algorithm testing.
- `docs/`: Additional documentation and project reports.

