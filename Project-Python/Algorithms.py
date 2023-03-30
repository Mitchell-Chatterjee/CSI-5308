from State import State
from abc import ABC, abstractmethod
from Message import Message, Stage, ElectMessage, NotifyMessage, WakeUpMessage


class Algorithm(ABC):
    @abstractmethod
    def act(self, node_state: State, node_value: int, incoming_message: Message):
        """
        This value should likely return the node_state, new node value and the message to send.
        :param node_state: The state of the current node. Defeated or Active.
        :param node_value: The value of the current node.
        :param incoming_message: The incoming message in the message buffer.
        :return: (State, int, any) --> (node_state, node_value, outgoing_message)
        """
        pass


class MinMax(Algorithm):

    def process_message(self, node_state: State, node_value: int, incoming_message: ElectMessage):
        if incoming_message.stage == Stage.EVEN and incoming_message.value > node_value:
            # Here the message sent will contain our own value
            return State.CANDIDATE, incoming_message.value, new_message(incoming_message, incoming_message.value)
        elif incoming_message.stage == Stage.ODD and incoming_message.value < node_value:
            # Here again the message will contain our own value
            return State.CANDIDATE, incoming_message.value, new_message(incoming_message, incoming_message.value)
        # Otherwise the node will become defeated and the message will not continue any further
        return State.DEFEATED, node_value, None

    def asleep_act(self, node_state: State, node_value: int, incoming_message: Message):
        # If the node state is an originator then we begin the message chain.
        if node_state == State.ORIGINATOR:
            return State.CANDIDATE, node_value, ElectMessage(node_value, Stage.ODD, 0)
        # In the general case we become defeated and forward the message
        return State.DEFEATED, node_value, incoming_message

    def candidate_act(self, node_state: State, node_value: int, incoming_message: Message):
        if node_value == incoming_message.value:
            # In this case we have been elected
            return State.LEADER, node_value, None
        # General case we process the message
        return self.process_message(node_state, node_value, incoming_message)

    def defeated_act(self, node_state: State, node_value: int, incoming_message: Message):
        # Simply forward the message
        return node_state, node_value, incoming_message

    def act(self, node_state: State, node_value: int, incoming_message: Message):
        if node_state == State.ASLEEP or node_state == State.ORIGINATOR:
            return self.asleep_act(node_state, node_value, incoming_message)
        elif node_state == State.CANDIDATE:
            return self.candidate_act(node_state, node_value, incoming_message)
        elif node_state == State.DEFEATED:
            return self.defeated_act(node_state, node_value, incoming_message)


class MinMaxPlus(Algorithm):
    def act(self, node_state: State, node_value: int, incoming_message: Message):
        # TODO: Implement this
        return NotImplemented


def forwarded_message(incoming_message: ElectMessage):
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
