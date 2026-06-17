import csv
import os

def parse_uri(uri):
    """
    Extracts the meaningful part from a CSO URI.
    Example: https://cso.kmi.open.ac.uk/topics/machine_learning -> machine_learning
    """
    if "cso.kmi.open.ac.uk/topics/" in uri:
        return uri.split("/")[-1].strip("<>\"'")
    if "cso.kmi.open.ac.uk/schema/cso#" in uri:
        return uri.split("#")[-1].strip("<>\"'")
    # Fallback for raw strings
    return uri.strip("<>\"'")

def load_cso_triples(file_path):
    """
    Loads CSO triples from a CSV file.
    Only keeps relevant predicates: superTopicOf, contributesTo, relatedEquivalent.
    """
    triples = []
    relevant_predicates = {'superTopicOf', 'contributesTo', 'relatedEquivalent'}
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSO file not found: {file_path}")
        
    with open(file_path, 'r', encoding='utf-8') as f:
        # Some CSVs might be tab separated or comma separated
        # We will try comma first, if it fails, try other ways or manual splitting
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 3:
                # Try simple splitting by space if it's N-Triples disguised as CSV
                parts = line.strip().split()
                if len(parts) < 3:
                    continue
            
            # Simple heuristic for extracting subject, predicate, object
            subject = parse_uri(parts[0])
            predicate = parse_uri(parts[1])
            # The object might contain commas, so we join the rest
            obj = parse_uri(",".join(parts[2:]))
            
            # Remove any trailing dot from N-Triples format
            if obj.endswith('.'):
                obj = obj[:-1].strip()
            
            if predicate in relevant_predicates:
                triples.append((subject, predicate, obj))
                
    return triples

if __name__ == "__main__":
    # Test the loader
    import sys
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_file = os.path.join(base_dir, "data", "raw", "CSO.3.5.csv")
    if os.path.exists(test_file):
        triples = load_cso_triples(test_file)
        print(f"Loaded {len(triples)} triples.")
        print("Sample triples:", triples[:5])
    else:
        print(f"File not found: {test_file}")
