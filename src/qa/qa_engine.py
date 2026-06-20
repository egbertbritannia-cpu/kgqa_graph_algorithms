"""End-to-end orchestration for explainable KGQA."""

import time

import networkx as nx

from src.algorithms import astar_path, bfs_path, dfs_path, dijkstra_path
from src.algorithms.heuristics import bind_depth_heuristic
from src.qa.path_verbalizer import format_path, verbalize_path
from src.qa.query_parser import RuleBasedQueryParser


class KGQAEngine:
    """Parse a question, run a graph algorithm, and verbalize the result."""

    def __init__(self, graph, parser=None):
        self.graph = graph
        self.parser = parser or RuleBasedQueryParser()

    @classmethod
    def from_json(cls, graph_path):
        """Load a NetworkX node-link JSON graph and create an engine."""
        graph = nx.node_link_graph(_load_json(graph_path))
        return cls(graph)

    def answer(self, question, algorithm="dijkstra"):
        """Answer a relationship question with an explainable path."""
        parsed = self.parser.parse(question)
        source = self._resolve_node(parsed["source"])
        target = self._resolve_node(parsed["target"])

        started = time.perf_counter()
        result = self._run_algorithm(algorithm, source, target)
        direction = "forward"

        # Directed CSO edges run from broader topic to narrower topic. If the
        # user asks in the opposite order, try the reverse direction as a
        # practical fallback while keeping the explanation honest.
        if not result["path"]:
            reverse_result = self._run_algorithm(algorithm, target, source)
            if reverse_result["path"]:
                result = reverse_result
                direction = "reverse"

        elapsed_ms = (time.perf_counter() - started) * 1000
        path = result["path"]

        return {
            "question": question,
            "source": source,
            "target": target,
            "algorithm": algorithm.lower(),
            "direction": direction,
            "answer": verbalize_path(self.graph, path),
            "path": path,
            "path_text": format_path(self.graph, path),
            "cost": result["cost"],
            "nodes_visited": result["nodes_visited"],
            "time_ms": elapsed_ms,
        }

    def _run_algorithm(self, algorithm, source, target):
        algorithm = algorithm.lower()

        if algorithm == "bfs":
            return bfs_path(self.graph, source, target)
        if algorithm == "dfs":
            return dfs_path(self.graph, source, target)
        if algorithm == "dijkstra":
            return dijkstra_path(self.graph, source, target)
        if algorithm in {"astar", "a*"}:
            heuristic = bind_depth_heuristic(self.graph)
            return astar_path(self.graph, source, target, heuristic=heuristic)

        raise ValueError("Algorithm must be one of: bfs, dfs, dijkstra, astar.")

    def _resolve_node(self, node_id):
        """Find a node by ID, then by stored label if needed."""
        if node_id in self.graph:
            return node_id

        for node, data in self.graph.nodes(data=True):
            label_id = data.get("label", "").strip().lower().replace(" ", "_")
            if label_id == node_id:
                return node

        raise ValueError(f"Concept '{node_id}' was not found in the graph.")


def _load_json(graph_path):
    import json

    with open(graph_path, "r", encoding="utf-8") as file:
        return json.load(file)
