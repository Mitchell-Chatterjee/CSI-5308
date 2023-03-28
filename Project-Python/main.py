import igraph as ig
from Ring import Node, Direction


def run_experiments():
    # Let's generate a couple nodes to start and make sure we can graph them properly
    node_1 = Node(3, None, None)
    node_2 = Node(2, None, None)

    # Now let's link up the nodes
    node_1.left, node_1.right = node_2, node_2
    node_2.left, node_2.right = node_1, node_1

    # Now let's ensure they give the correct edges
    print(f"Node 1 edge left: {node_1.get_edge(Direction.LEFT)}")
    print(f"Node 2 edge right: {node_2.get_edge(Direction.RIGHT)}")


if __name__ == '__main__':
    run_experiments()
