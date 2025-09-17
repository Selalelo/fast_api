from graphviz import Digraph

# Create a directed graph
dot = Digraph(comment="FastAPI Data Flow", format="png")
dot.attr(rankdir="LR", size="8")

# Nodes
dot.node("A", "Client\n(Sends JSON)")
dot.node("B", "FastAPI\n(Parses + Validates)")
dot.node("C", "Pydantic Model\n(Post object)")
dot.node("D", "Convert to dict\n(.model_dump()/.dict())")
dot.node("E", "SQLAlchemy Model\n(models.Post(**dict))")
dot.node("F", "Database\n(Postgres, etc.)")

# Edges
dot.edge("A", "B", label="Raw JSON")
dot.edge("B", "C", label="Validated Data")
dot.edge("C", "D", label="Optional step\n(when creating)")
dot.edge("D", "E", label="Keyword args")
dot.edge("E", "F", label="INSERT / UPDATE")

# Save inside current working directory instead of /mnt/data
file_path = "fastapi_data_flow"
dot.render(file_path, cleanup=True)

file_path + ".png"
