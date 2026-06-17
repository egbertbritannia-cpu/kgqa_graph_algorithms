import heapq

def dijkstra_path(graph, source, target):
    """
    Finds the lowest-cost path using Dijkstra's algorithm.
    Edge weights: superTopicOf=1.0, contributesTo=1.5.

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

    # dist[node] = best known cost to reach node
    dist = {source: 0.0}
    # prev[node] = previous node on best path
    prev = {source: None}
    # min-heap: (cost, node)
    heap = [(0.0, source)]
    visited = set()
    nodes_visited = 0

    while heap:
        cost, current = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)
        nodes_visited += 1

        if current == target:
            path = _reconstruct_path(prev, source, target)
            return {'path': path, 'cost': cost, 'nodes_visited': nodes_visited}

        for neighbor in graph.successors(current):
            if neighbor in visited:
                continue
            edge_data = graph.get_edge_data(current, neighbor)
            weight = edge_data.get('weight', 1.0)
            new_cost = cost + weight

            if new_cost < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_cost
                prev[neighbor] = current
                heapq.heappush(heap, (new_cost, neighbor))

    return {'path': None, 'cost': float('inf'), 'nodes_visited': nodes_visited}


def _reconstruct_path(prev, source, target):
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()
    return path if path[0] == source else None
