"""Turn graph paths into human-readable explanations."""


def verbalize_path(graph, path):
    """Create a concise English explanation for a path.

    Args:
        graph: A NetworkX DiGraph with typed edges.
        path: A list of node IDs, for example ["data_mining", "decision_tree"].

    Returns:
        A readable explanation string.
    """
    if not path:
        return "No explanation path was found."

    if len(path) == 1:
        return f"{_label(graph, path[0])} is the same concept as the requested target."

    sentences = []
    for source, target in zip(path, path[1:]):
        edge = graph.get_edge_data(source, target, default={})
        relation_type = edge.get("type", "relatedTo")
        sentences.append(_verbalize_edge(graph, source, target, relation_type))

    return " ".join(sentences)


def format_path(graph, path):
    """Return a compact arrow representation of the path."""
    if not path:
        return "(no path)"
    return " -> ".join(_label(graph, node) for node in path)


def _verbalize_edge(graph, source, target, relation_type):
    source_label = _label(graph, source)
    target_label = _label(graph, target)

    if relation_type == "superTopicOf":
        return f"{source_label} is a broader topic that includes {target_label}."
    if relation_type == "contributesTo":
        return f"{source_label} contributes to {target_label}."

    return f"{source_label} is related to {target_label}."


def _label(graph, node):
    """Prefer the stored display label, then fall back to a readable node ID."""
    return graph.nodes[node].get("label", node.replace("_", " ").title())
