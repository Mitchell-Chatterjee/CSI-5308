from Ring import Node, Direction, Ring
from Algorithms import MinMax, MinMaxPlus
import random


def generate_random_ring(size):
    temp = [i for i in range(1, size+1)]
    random.shuffle(temp)
    nodes = [Node(value, None, None) for value in temp]

    return nodes


def run_experiments():
    # Let's generate a couple nodes to start and make sure we can graph them properly
    nodes = generate_random_ring(10)

    # Now let's link up the nodes in a ring
    ring = Ring(nodes, Direction.RIGHT)

    # Print all edges in order
    print([elem.get_edge(Direction.RIGHT) for elem in ring.nodes])

    # Get both algorithms
    min_max = MinMax()
    min_max_plus = MinMaxPlus()

    # Let's test out sending a message between two nodes
    nodes = ring.nodes
    node_1, node_2, node_3 = nodes[1], nodes[2], nodes[3]
    node_1.send(message=node_1.value, direction=Direction.RIGHT)
    node_2.act(direction=Direction.RIGHT, algorithm=min_max)
    print(f"Node 1 value: {node_1.value}")
    print(f"Node 3 buffer: {node_3.message_buffer}")

    # Time to visualize the graph
    # ring.visualize()


if __name__ == '__main__':
    run_experiments()
