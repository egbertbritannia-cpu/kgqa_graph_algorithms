def dfs_path(graph, source, target):
    """
    Finds a path using Depth-First Search (not necessarily shortest).

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

    visited = set()
    nodes_visited = 0
    result = {'path': None}

    def _dfs(current, path):
        nonlocal nodes_visited
        visited.add(current)
        nodes_visited += 1

        if current == target:
            result['path'] = list(path)
            return True

        for neighbor in graph.successors(current):
            if neighbor not in visited:
                path.append(neighbor)
                if _dfs(neighbor, path):
                    return True
                path.pop()

        return False

    _dfs(source, [source])

    if result['path'] is None:
        return {'path': None, 'cost': float('inf'), 'nodes_visited': nodes_visited}

    cost = _path_cost(graph, result['path'])
    return {'path': result['path'], 'cost': cost, 'nodes_visited': nodes_visited}


def _path_cost(graph, path):
    total = 0.0
    for i in range(len(path) - 1):
        edge_data = graph.get_edge_data(path[i], path[i + 1])
        total += edge_data.get('weight', 1.0)
    return total
