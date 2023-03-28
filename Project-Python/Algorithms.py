from Ring import State
from abc import ABC, abstractmethod
from Message import Message, Stage


class Algorithm(ABC):
    @abstractmethod
    def act(self, node_state: int, node_value: int, incoming_message: Message):
        """
        This value should likely return the node_state, new node value and the message to send.
        :param node_state: The state of the current node. Defeated or Active.
        :param node_value: The value of the current node.
        :param incoming_message: The incoming message in the message buffer.
        :return: (State, int, any) --> (node_state, node_value, outgoing_message)
        """
        pass


class MinMax(Algorithm):
    def act(self, node_state: State, node_value: int, incoming_message: Message):
        if node_state == State.ACTIVE and incoming_message.stage == Stage.EVEN:
            if incoming_message.value > node_value:
                # Here the message sent will contain our own value
                return State.ACTIVE, node_value, new_message(incoming_message)
        elif node_state == State.ACTIVE and incoming_message.stage == Stage.ODD:
            if incoming_message.value < node_value:
                # Here again the message will contain our own value
                return State.ACTIVE, node_value, new_message(incoming_message)
        # If the node is already passive then we will simply forward the message
        return State.DEFEATED, node_value, forwarded_message(incoming_message)


class MinMaxPlus(Algorithm):
    def act(self, node_state: int, node_value: int, incoming_message: Message):
        # TODO: Implement this
        return NotImplemented


def forwarded_message(incoming_message: Message):
    """
    Here we need only decrease the counter if it exists
    :param incoming_message:
    :return:
    """
    if incoming_message.stage == Stage.EVEN:
        incoming_message.counter -= 1
    return incoming_message


def new_message(incoming_message: Message, node_value: int):
    """
    Here we need to update the value in the message, update the stage and decrease the counter.
    :param incoming_message:
    :param node_value:
    :return:
    """
    incoming_message.value = node_value
    incoming_message.stage = Stage.EVEN if incoming_message.stage == Stage.ODD else Stage.ODD

    # TODO: Fix this to use the Fibonacci sequence
    # Note that we update the counter either way, but it doesn't really matter as we won't check it in the odd stages
    # of MinMaxPlus.
    incoming_message.counter = 0

    return incoming_message
