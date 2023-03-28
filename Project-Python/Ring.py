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

