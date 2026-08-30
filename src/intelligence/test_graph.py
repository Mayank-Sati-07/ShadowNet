from src.intelligence.graph_loader import load_person_graph


graph = load_person_graph()

print()
print("Graph information")
print("------------------")

print(
    "Nodes:",
    graph.number_of_nodes()
)

print(
    "Edges:",
    graph.number_of_edges()
)