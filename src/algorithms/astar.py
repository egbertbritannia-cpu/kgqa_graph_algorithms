import heapq

def astar_path(graph, source, target, heuristic=None):
    """
    Finds the lowest-cost path using A* Search.

    A* extends Dijkstra by adding a heuristic h(node) that estimates
    the remaining cost from node to target, guiding the search faster.

    f(n) = g(n) + h(n)
      g(n): actual cost from source to n
      h(n): estimated cost from n to target (must be admissible: never overestimate)

    Args:
        graph    : NetworkX DiGraph
        source   : starting node
        target   : goal node
        heuristic: callable(node, target) -> float
                   Defaults to h=0 (equivalent to Dijkstra) when None.

    Returns:
        dict with keys:
            'path'          : list of node names from source to target, or None if not found
            'cost'          : total edge weight along the path
            'nodes_visited' : number of nodes popped from the priority queue
    """
    if source not in graph:
        raise ValueError(f"Source node '{source}' not found in graph.")
    if target not in graph:
        raise ValueError(f"Target node '{target}' not found in graph.")
    if source == target:
        return {'path': [source], 'cost': 0.0, 'nodes_visited': 1}

    if heuristic is None:
        heuristic = lambda node, tgt: 0.0

    # g[node] = actual cost from source to node
    g = {source: 0.0}
    # prev[node] = previous node on best path
    prev = {source: None}
    # min-heap: (f_score, node)
    heap = [(heuristic(source, target), source)]
    visited = set()
    nodes_visited = 0

    while heap:
        f, current = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)
        nodes_visited += 1

        if current == target:
            path = _reconstruct_path(prev, source, target)
            return {'path': path, 'cost': g[target], 'nodes_visited': nodes_visited}

        for neighbor in graph.successors(current):
            if neighbor in visited:
                continue
            edge_data = graph.get_edge_data(current, neighbor)
            weight = edge_data.get('weight', 1.0)
            tentative_g = g[current] + weight

            if tentative_g < g.get(neighbor, float('inf')):
                g[neighbor] = tentative_g
                prev[neighbor] = current
                f_score = tentative_g + heuristic(neighbor, target)
                heapq.heappush(heap, (f_score, neighbor))

    return {'path': None, 'cost': float('inf'), 'nodes_visited': nodes_visited}


def _reconstruct_path(prev, source, target):
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()
    return path if path[0] == source else None
