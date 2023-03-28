import igraph as ig
from Ring import Node, Direction, Ring


def run_experiments():
    # Let's generate a couple nodes to start and make sure we can graph them properly
    node_1 = Node(1, None, None)
    node_2 = Node(2, None, None)
    node_3 = Node(3, None, None)

    # Now let's link up the nodes in a ring
    ring = Ring([node_1, node_2, node_3], Direction.RIGHT)

    # Now let's ensure they give the correct edges
    print(f"Node 1 edge left: {node_1.get_edge(Direction.LEFT)}")
    print(f"Node 2 edge right: {node_2.get_edge(Direction.RIGHT)}")

    # Print all edges in order
    edges = [elem.get_edge(Direction.RIGHT) for elem in ring.nodes]
    print(edges)


if __name__ == '__main__':
    run_experiments()
