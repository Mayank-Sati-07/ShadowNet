from src.graph.create_constraints import create_constraints
from src.graph.load_nodes import load_all_nodes
from src.graph.load_relationships import load_all_relationships


def main():

    print("=" * 70)
    print("ShadowNet KNOWLEDGE GRAPH INGESTION")
    print("=" * 70)

    print("\n[1/3] Creating constraints...")
    create_constraints()

    print("\n[2/3] Loading nodes...")
    load_all_nodes()

    print("\n[3/3] Loading relationships...")
    load_all_relationships()

    print("\n" + "=" * 70)
    print("[OK] ShadowNet GRAPH INGESTION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()