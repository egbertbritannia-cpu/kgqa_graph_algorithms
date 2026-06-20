"""Command-line demo for the explainable KGQA system."""

import argparse
import os

from src.qa import KGQAEngine


DEFAULT_GRAPH = os.path.join("data", "processed", "subgraph_data_science.json")


def main():
    args = _parse_args()

    if not os.path.exists(args.graph):
        raise FileNotFoundError(
            f"Graph file not found: {args.graph}. Build a pruned graph first with src/graph_pruner.py."
        )

    engine = KGQAEngine.from_json(args.graph)

    if args.question:
        _print_answer(engine.answer(args.question, args.algorithm))
        return

    print("Explainable KGQA demo. Type 'exit' to stop.")
    while True:
        question = input("\nQuestion: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue

        try:
            _print_answer(engine.answer(question, args.algorithm))
        except ValueError as error:
            print(f"Error: {error}")


def _parse_args():
    parser = argparse.ArgumentParser(description="Explainable KGQA over a CSO subgraph.")
    parser.add_argument("--graph", default=DEFAULT_GRAPH, help="Path to a pruned graph JSON file.")
    parser.add_argument(
        "--algorithm",
        default="dijkstra",
        choices=["bfs", "dfs", "dijkstra", "astar"],
        help="Graph algorithm used to retrieve the explanation path.",
    )
    parser.add_argument("--question", help="Run one question and exit.")
    return parser.parse_args()


def _print_answer(result):
    print("\nAnswer")
    print(result["answer"])
    print("\nPath")
    print(result["path_text"])
    print("\nMetadata")
    print(f"Algorithm: {result['algorithm']}")
    print(f"Direction: {result['direction']}")
    print(f"Cost: {result['cost']}")
    print(f"Nodes visited: {result['nodes_visited']}")
    print(f"Time: {result['time_ms']:.3f} ms")


if __name__ == "__main__":
    main()
