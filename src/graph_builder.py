import networkx as nx

def build_full_graph(triples):
    """
    Builds a directed graph from CSO triples.
    Applies node merging for relatedEquivalent.
    Assigns weights: superTopicOf (1.0), contributesTo (1.5).
    """
    G = nx.DiGraph()
    weights = {
        'superTopicOf': 1.0,
        'contributesTo': 1.5
    }
    
    # First pass: build alias map for relatedEquivalent
    alias_map = {}
    for subj, pred, obj in triples:
        if pred == 'relatedEquivalent':
            # Map object to subject (subject becomes canonical)
            if obj not in alias_map:
                alias_map[obj] = subj

    def get_canonical(node):
        # Resolve to root canonical to handle transitive equivalents
        curr = node
        visited = set()
        while curr in alias_map and curr not in visited:
            visited.add(curr)
            curr = alias_map[curr]
        return curr
        
    # Second pass: add nodes and edges
    for subj, pred, obj in triples:
        if pred == 'relatedEquivalent':
            continue
            
        c_subj = get_canonical(subj)
        c_obj = get_canonical(obj)
        
        if c_subj == c_obj:
            continue
            
        if not G.has_node(c_subj):
            G.add_node(c_subj, label=c_subj.replace("_", " ").title())
        if not G.has_node(c_obj):
            G.add_node(c_obj, label=c_obj.replace("_", " ").title())
            
        if pred == 'superTopicOf':
            G.add_edge(c_subj, c_obj, type=pred, weight=weights['superTopicOf'], label="is parent of")
        elif pred == 'contributesTo':
            G.add_edge(c_subj, c_obj, type=pred, weight=weights['contributesTo'], label="contributes to")
            
    return G

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.data_loader import load_cso_triples
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_file = os.path.join(base_dir, "data", "raw", "CSO.3.5.csv")
    
    if os.path.exists(test_file):
        print("Loading triples...")
        triples = load_cso_triples(test_file)
        print("Building graph...")
        G = build_full_graph(triples)
        print(f"Graph built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
