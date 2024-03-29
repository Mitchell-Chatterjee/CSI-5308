import copy
from enum import Enum

from Message import Message
from State import State
from Algorithms import Algorithm
from threading import Thread
from random import sample
import igraph as ig
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from functools import partial


class Direction(Enum):
    LEFT = "Left"
    RIGHT = "Right"


class Node:
    def __init__(self, value: int, left, right):
        self._value = value
        self._left = left
        self._right = right
        self._state = State.ASLEEP
        self._stage = 0
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
        :return: (continue) --> (bool) This is a boolean value indicating whether we should continue on this thread.
        """
        while len(self._message_buffer) > 0 or self._state == State.ORIGINATOR:
            # Iterate through the message buffer until it's empty.
            state, value, message = \
                algorithm.act(node_state=self._state, node_value=self._value, node_stage=self._stage,
                              incoming_message=None if self._state == State.ORIGINATOR
                              else self._message_buffer.pop(0))

            # Update the parameters
            self._state = state
            self._value = value

            # Otherwise we continue with the general case and send a message. If the message isn't none.
            if message is not None:
                self._stage = message.stage
                self.send(message, direction)
                return True
        # We return False if we do not send a message.
        return False


class Ring:
    def __init__(self, nodes: [Node], direction: Direction, algorithm, number_of_originators):
        self._nodes = nodes
        self._direction = direction
        self._algorithm = algorithm
        # This value will maintain the total number of messages we send
        self._messages = 0
        # Create the ring
        self.create_ring(number_of_originators=number_of_originators)

        # The following are used for animation
        # This will hold the sequence of labels for the animation. Seed it with the starting values.
        self._stage_list = [[copy.deepcopy(node) for node in self._nodes]]
        # List of messages that we will display in the animation
        self._message_list = ["Initial state"]
        # Index used for creating the animation at the end
        self._stage_index = 0
        # The dictionary containing the colours
        self._colour_dict = {State.CANDIDATE: "green", State.ORIGINATOR: "green", State.LEADER: "red",
                             State.ASLEEP: "grey", State.DEFEATED: "grey"}

    @property
    def nodes(self):
        return self._nodes

    @property
    def direction(self):
        return self._direction

    @property
    def stage_list(self):
        return self._stage_list

    @direction.setter
    def direction(self, direction):
        self._direction = direction

    def create_ring(self, number_of_originators):
        """
        This function will string up the nodes in order to form a ring. From left to right.
        :return: Returns the same list of nodes, that can then be used for running algorithms.
        """
        if number_of_originators > len(self._nodes):
            raise Exception("Number of originators is greater than the length of the list.")

        # The originators are chosen at random
        for node in sample(self._nodes, number_of_originators):
            node.state = State.ORIGINATOR

        # Connect each node to the one to their right and vice versa
        for i in range(0, len(self._nodes) - 1):
            self._nodes[i].right = self._nodes[i + 1]
            self._nodes[i + 1].left = self._nodes[i]

        # String up the last node to the first node and vice versa
        self._nodes[-1].right = self._nodes[0]
        self._nodes[0].left = self._nodes[-1]

    def leader_election(self):
        """
        Each thread will begin at an originator and follow its message around the ring until
        No more messages are being sent from this node
        :return: The leader and the number of messages for this algorithm
        """

        # Create a pool of threads for each originator
        thread_pool = [
            Thread(target=Ring.thread_act, args=(self, node, self._direction, self._algorithm, ))
            for node in self._nodes if node.state == State.ORIGINATOR
        ]

        # Starting all the threads
        for thread in thread_pool:
            thread.start()

        # Joining all the threads
        for thread in thread_pool:
            thread.join()

        leader_node = [node for node in self._nodes if node.state == State.LEADER][0]
        return leader_node.value, self._messages

    def thread_act(self, node: Node, direction: Direction, algorithm: Algorithm):
        """
        Each thread will begin at an originator and follow its message around the ring until
        No more messages are being sent from this node
        :param node: The node we begin at. An originator.
        :param direction: The direction to send messages.
        :param algorithm: The algorithm we are using.
        :return: None
        """
        # We will continue until we are told to stop. As we are no longer forwarding messages.
        while node.act(direction, algorithm):
            node = node.right if direction == Direction.RIGHT else node.left
            self._messages += 1

            # Make a deepcopy of each node, so we can reference it later for animation
            self._stage_list.append([copy.deepcopy(node) for node in self._nodes])

            # Append the message here
            if len(node.message_buffer) == 0:
                self._message_list.append(f"The node {node.value} has received no message")
            else:
                message: Message = node.message_buffer[-1]
                self._message_list.append(f"The node {node.value} has received the message {message.value}")
        # Append the final stage and message
        self._stage_list.append([copy.deepcopy(node) for node in self._nodes])
        self._message_list.append(f"The node {node.value} has received no message")

        return

    def update_graph(self, ax, g, layout, frame):
        # Remove plot elements from the previous frame
        ax.clear()

        # Fix limits (unless you want a zoom-out effect)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)

        # Set the colours for this stage and increase the stage index
        vertex_labels = [node.value for node in self._stage_list[self._stage_index]]

        # Only move the to the next stage if we have moved to the next frame
        if self._stage_index < frame:
            self._stage_index += 1

        vertex_colours = [self._colour_dict[node.state] for node in self._stage_list[self._stage_index]]

        # Add a caption for what's happening right now
        # ax.text(2, 6, r'an equation: $E=mc^2$', fontsize=15)
        # ax.text(3, 8, f"Send message {self._stage_index}", style='italic',
        #         bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
        ax.set_title(self._message_list[self._stage_index])
        ig.plot(g, target=ax, vertex_label=vertex_labels, vertex_color=vertex_colours)

        return ax.get_children()

    def visualize(self, animation_speed):
        g = ig.Graph.Ring(len(self._nodes), directed=False)
        layout = g.layout_circle()
        fig, ax = plt.subplots()
        ani = animation.FuncAnimation(fig, partial(self.update_graph, ax, g, layout), len(self._stage_list),
                                      interval=animation_speed, blit=False)
        writergif = animation.PillowWriter(fps=1)
        ani.save(f'animation_{type(self._algorithm).__name__}.gif', writer=writergif)
