from enum import Enum


class Direction(Enum):
    LEFT = False
    RIGHT = True


class Node:
    def __init__(self, value: int, left, right):
        self._value = value
        self._left = left
        self._right = right

    @property
    def value(self):
        return self._value

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @left.setter
    def left(self, node):
        self._left = node

    @right.setter
    def right(self, node):
        self._right = node

    def get_edge(self, direction: Enum):
        """
        This function will return the edge with itself and the neighbour in the specified direction.
        :param direction: Left or Right
        :return: A list containing the edge in the specified direction
        """
        # TODO: Check this enum
        if direction is Direction.LEFT:
            return [self._value, self._left.value]
        return [self._value, self._right.value]


class Ring:
    def __init__(self, nodes: [Node], direction: Direction):
        self._nodes = nodes
        self._direction = direction

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

