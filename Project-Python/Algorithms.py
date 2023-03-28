from Ring import State
from abc import ABC, abstractmethod
from Message import Message


class Algorithm(ABC):
    @abstractmethod
    def act(self, node_state, node_value, incoming_message):
        """
        This value should likely return the node_state, new node value and the message to send.
        :param node_state: The state of the current node. Defeated or Active.
        :param node_value: The value of the current node.
        :param incoming_message: The incoming message in the message buffer.
        :return: (State, int, any) --> (node_state, node_value, outgoing_message)
        """
        pass


class MinMax(Algorithm):
    def act(self, node_state, node_value, incoming_message):
        # TODO: Implement this
        return NotImplemented


class MinMaxPlus(Algorithm):
    def act(self, node_state, node_value, incoming_message):
        # TODO: Implement this
        return NotImplemented
