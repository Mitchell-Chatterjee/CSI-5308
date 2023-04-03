from Ring import Node, Direction, Ring
from Algorithms import MinMax, MinMaxPlus
from State import State
import random


def generate_random_ring(size):
    temp = [i for i in range(1, size+1)]
    random.shuffle(temp)
    nodes = [Node(value, None, None) for value in temp]

    return nodes


def run_experiments():
    # Let's generate a couple nodes to start and make sure we can graph them properly
    nodes = generate_random_ring(10)

    # Get both algorithms
    min_max = MinMax()
    min_max_plus = MinMaxPlus()

    # Now let's link up the nodes in a ring
    ring = Ring(nodes, Direction.RIGHT, min_max_plus)

    # Print all edges in order
    print([elem.get_edge(Direction.RIGHT) for elem in ring.nodes])

    # Now let's test out leader election in the ring
    ring.leader_election(number_of_originators=2)

    # Time to visualize the graph
    # ring.visualize()


if __name__ == '__main__':
    run_experiments()
