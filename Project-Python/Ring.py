from enum import Enum
import igraph as ig
import matplotlib.pyplot as plt
from Message import Message


class Direction(Enum):
    LEFT = False
    RIGHT = True


class State(Enum):
    ACTIVE = True
    DEFEATED = False


class Node:
    def __init__(self, value: int, left, right):
        self._value = value
        self._left = left
        self._right = right
        self._state = State.ACTIVE
        self._stage = 0
        # TODO: Make this thread safe
        self._message_buffer = []

    @property
    def value(self):
        return self._value

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def state(self):
        return self._state

    @property
    def stage(self):
        return self._stage

    @property
    def message_buffer(self):
        return self._message_buffer

    @left.setter
    def left(self, node):
        self._left = node

    @right.setter
    def right(self, node):
        self._right = node

    @stage.setter
    def stage(self, stage):
        self._stage = stage

    def get_edge(self, direction: Direction):
        """
        This function will return the edge with itself and the neighbour in the specified direction.
        :param direction: Left or Right
        :return: A list containing the edge in the specified direction
        """
        if direction is Direction.LEFT:
            return [self._left.value, self._value]
        return [self._value, self._right.value]

    def send(self, message, direction: Direction):
        """
        This method will send a message to the node in the specified direction.
        :param message: The message to be sent to the next node.
        :param direction: Left or Right.
        :return: None
        """
        node = self._right if direction == Direction.RIGHT else self._left
        node.message_buffer.append(message)

        return None

    def act(self, direction: Direction, algorithm):
        """
        This method is used in the general case. When we are executing a turn for a specific node.
        :return: None
        """
        if len(self._message_buffer) > 0:
            # This is where we will consider the incoming term
            # TODO: Continue work from here
            state, value, message = algorithm.act(self._state, self._value, self._message_buffer.pop(0))

            self._state = state
            self._value = value
            self.send(message, direction)
        return None


class Ring:
    def __init__(self, nodes: [Node], direction: Direction):
        self._nodes = nodes
        self._direction = direction
        # Create the ring
        self.create_ring()

    @property
    def nodes(self):
        return self._nodes

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction

    def create_ring(self):
        """
        This function will string up the nodes in order to form a ring. From left to right.
        :return: Returns the same list of nodes, that can then be used for running algorithms.
        """
        # Connect each node to the one to their right and vice versa
        for i in range(0, len(self._nodes)-1):
            self._nodes[i].right = self._nodes[i+1]
            self._nodes[i+1].left = self._nodes[i]

        # String up the last node to the first node and vice versa
        self._nodes[-1].right = self._nodes[0]
        self._nodes[0].left = self._nodes[-1]

    def visualize(self):
        # Time to visualize the graph
        ig.config['plotting.backend'] = 'matplotlib'
        g = ig.Graph(edges=[elem.get_edge(Direction.RIGHT) for elem in self._nodes])
        layout = g.layout(layout='auto')
        ig.plot(g)
        plt.show()

