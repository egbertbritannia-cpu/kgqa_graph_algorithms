from collections import deque

def bfs_path(graph, source, target):
    """
    Finds the shortest path by hop count using Breadth-First Search.

    Returns:
        dict with keys:
            'path'          : list of node names from source to target, or None if not found
            'cost'          : total edge weight along the path
            'nodes_visited' : number of nodes explored during search
    """
    if source not in graph:
        raise ValueError(f"Source node '{source}' not found in graph.")
    if target not in graph:
        raise ValueError(f"Target node '{target}' not found in graph.")
    if source == target:
        return {'path': [source], 'cost': 0.0, 'nodes_visited': 1}

    visited = {source}
    # Each queue entry: (current_node, path_so_far)
    queue = deque([(source, [source])])
    nodes_visited = 1

    while queue:
        current, path = queue.popleft()

        for neighbor in graph.successors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                nodes_visited += 1
                new_path = path + [neighbor]

                if neighbor == target:
                    cost = _path_cost(graph, new_path)
                    return {'path': new_path, 'cost': cost, 'nodes_visited': nodes_visited}

                queue.append((neighbor, new_path))

    return {'path': None, 'cost': float('inf'), 'nodes_visited': nodes_visited}


def _path_cost(graph, path):
    total = 0.0
    for i in range(len(path) - 1):
        edge_data = graph.get_edge_data(path[i], path[i + 1])
        total += edge_data.get('weight', 1.0)
    return total
