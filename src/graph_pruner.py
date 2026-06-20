import networkx as nx
import json
import os
import argparse

def extract_subgraph(full_graph, root_node, max_depth=5):
    """
    Extracts a subgraph starting from root_node using BFS.
    Only follows 'superTopicOf' edges to build the core hierarchy.
    """
    if root_node not in full_graph:
        # Let's try to find it by replacing spaces with underscores
        root_node_alt = root_node.replace(" ", "_").lower()
        if root_node_alt in full_graph:
            root_node = root_node_alt
        else:
            raise ValueError(f"Root node '{root_node}' not found in the graph.")
        
    subgraph_nodes = {root_node}
    queue = [(root_node, 0)]
    node_depths = {root_node: 0}
    
    while queue:
        current, depth = queue.pop(0)
        
        if depth < max_depth:
            # Look at children via 'superTopicOf'
            for neighbor in full_graph.successors(current):
                edge_data = full_graph.get_edge_data(current, neighbor)
                if edge_data['type'] == 'superTopicOf':
                    if neighbor not in subgraph_nodes:
                        subgraph_nodes.add(neighbor)
                        # We store the minimum depth
                        node_depths[neighbor] = depth + 1
                        queue.append((neighbor, depth + 1))
                        
    # Create the subgraph
    # nx.subgraph keeps all edges (including 'contributesTo') between the nodes in subgraph_nodes
    H = full_graph.subgraph(subgraph_nodes).copy()
    
    # Assign depths and root info
    for node in H.nodes():
        H.nodes[node]['depth'] = node_depths.get(node, -1)
        H.nodes[node]['branch'] = root_node
        
    # Calculate degree inside subgraph
    for node in H.nodes():
        H.nodes[node]['degree'] = H.degree(node)
        
    return H

def save_subgraph(graph, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data = nx.node_link_data(graph)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def build_and_save_subgraph(input_file, output_file, root, max_depth):
    """Build the full CSO graph, prune it from one root, and save the result."""
    from src.data_loader import load_cso_triples
    from src.graph_builder import build_full_graph

    print(f"Loading triples from {input_file}...")
    triples = load_cso_triples(input_file)

    print("Building full graph...")
    full_graph = build_full_graph(triples)

    print(f"Extracting subgraph from root '{root}' with max depth {max_depth}...")
    subgraph = extract_subgraph(full_graph, root, max_depth)

    print(
        f"Subgraph extracted: {subgraph.number_of_nodes()} nodes, "
        f"{subgraph.number_of_edges()} edges."
    )
    print(f"Saving to {output_file}...")
    save_subgraph(subgraph, output_file)
    print("Done.")


def parse_args():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_input = os.path.join(base_dir, "data", "raw", "CSO.3.5.csv")
    default_output = os.path.join(base_dir, "data", "processed", "subgraph_data_mining.json")

    parser = argparse.ArgumentParser(description="Prune a CSO graph into a smaller subgraph.")
    parser.add_argument("--input", default=default_input, help="Path to the raw CSO CSV file.")
    parser.add_argument("--output", default=default_output, help="Path for the pruned graph JSON.")
    parser.add_argument("--root", default="data_mining", help="Root concept, e.g. artificial_intelligence.")
    parser.add_argument("--max-depth", type=int, default=5, help="Maximum hierarchy depth to follow.")
    return parser.parse_args()


if __name__ == "__main__":
    import sys
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_dir)

    args = parse_args()
    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}")
    else:
        try:
            build_and_save_subgraph(args.input, args.output, args.root, args.max_depth)
        except Exception as error:
            print(f"Error: {error}")
