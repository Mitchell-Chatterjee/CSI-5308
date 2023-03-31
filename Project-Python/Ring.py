from enum import Enum
import igraph as ig
import matplotlib.pyplot as plt
from State import State
from Algorithms import Algorithm
from threading import Thread


class Direction(Enum):
    LEFT = False
    RIGHT = True


class Node:
    def __init__(self, value: int, left, right):
        self._value = value
        self._left = left
        self._right = right
        self._state = State.ASLEEP
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

    @state.setter
    def state(self, state):
        self._state = state

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

    def act(self, direction: Direction, algorithm: Algorithm):
        """
        This method is used in the general case. When we are executing a turn for a specific node.
        :return: (done)
        """
        # Make a special exception for the originator case
        if self._state == State.ORIGINATOR:
            state, value, message = \
                algorithm.act(node_state=self._state, node_value=self._value, incoming_message=None)
            # Update the parameters
            self._state = state
            self._value = value
            self.send(message, direction)

        while len(self._message_buffer) > 0 or self._state == State.ORIGINATOR:
            # Iterate through the message buffer until it's empty.
            state, value, message = \
                algorithm.act(node_state=self._state, node_value=self._value,
                              incoming_message=self._message_buffer.pop(0))

            # Update the parameters
            self._state = state
            self._value = value

            # In this case we have elected a leader
            if self._state == State.LEADER:
                return True

            # Otherwise we continue with the general case and send a message. If the message isn't none
            if message is not None:
                self.send(message, direction)
        # We return False in the general case as we are not done yet.
        return False


class Ring:
    def __init__(self, nodes: [Node], direction: Direction, algorithm):
        self._nodes = nodes
        self._direction = direction
        self._algorithm = algorithm
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
        for i in range(0, len(self._nodes) - 1):
            self._nodes[i].right = self._nodes[i + 1]
            self._nodes[i + 1].left = self._nodes[i]

        # String up the last node to the first node and vice versa
        self._nodes[-1].right = self._nodes[0]
        self._nodes[0].left = self._nodes[-1]

    def leader_election(self):
        done = False

        # TODO: Remove this
        # For now the first node will automatically become an Originator
        self._nodes[0].state = State.ORIGINATOR

        # Each thread will begin at an originator and follow its message around the ring until
        # No more messages are being sent from this node

        # Create a pool of threads for each originator
        thread_pool = [
            Thread(target=Ring.thread_act, args=(self, node, self._direction, self._algorithm, ))
            for node in self._nodes if node.state == State.ORIGINATOR
        ]

        # Starting all the threads
        # map(lambda thread: thread.start(), thread_pool)
        for thread in thread_pool:
            thread.start()

        # Joining all the threads
        # map(lambda thread: thread.join, thread_pool)
        for thread in thread_pool:
            thread.join()

        # leader_node = [node for node in self._nodes if node.state == State.LEADER][0]
        # print(f"We have elected a leader: {leader_node.value}")

    def thread_act(self, node: Node, direction: Direction, algorithm: Algorithm):
        """
        This thread will follow the message as far as it can go and then the thread will die.
        :param node:
        :param direction:
        :param algorithm:
        :return:
        """
        print(f"Worker thread with value {node.value}")
        node.act(direction, algorithm)
        return None

    def visualize(self):
        # Time to visualize the graph
        ig.config['plotting.backend'] = 'matplotlib'
        g = ig.Graph(edges=[elem.get_edge(Direction.RIGHT) for elem in self._nodes])
        layout = g.layout(layout='auto')
        ig.plot(g)
        plt.show()
