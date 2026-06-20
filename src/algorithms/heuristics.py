"""Heuristic functions for A* search."""


def depth_heuristic(graph, current_node, target_node, base_weight=1.0):
    """Estimate distance using the difference in ontology depth.

    The pruned CSO graph stores a ``depth`` value on each node. Concepts at very
    different depths are likely farther apart in the hierarchy, so A* can use
    this value as a simple guide.
    """
    current_depth = graph.nodes[current_node].get("depth", 0)
    target_depth = graph.nodes[target_node].get("depth", 0)
    return abs(current_depth - target_depth) * base_weight


def null_heuristic(graph, current_node, target_node):
    """Return zero so A* behaves like Dijkstra."""
    return 0.0


def bind_depth_heuristic(graph, base_weight=1.0):
    """Adapt ``depth_heuristic`` to the two-argument API used by astar_path."""

    def heuristic(current_node, target_node):
        return depth_heuristic(graph, current_node, target_node, base_weight)

    return heuristic
