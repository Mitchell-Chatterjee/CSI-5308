from State import State
from abc import ABC, abstractmethod
from Message import Message, ElectMessage, NotifyMessage, WakeUpMessage


class Algorithm(ABC):
    @abstractmethod
    def act(self, node_state: State, node_value: int, node_stage: int, incoming_message: Message):
        """
        This value should likely return the node_state, new node value and the message to send.
        :param node_state: The state of the current node. Defeated or Active.
        :param node_value: The value of the current node.
        :param node_stage: The stage that the current node is in.
        :param incoming_message: The incoming message in the message buffer.
        :return: (State, int, Message) --> (node_state, node_value, outgoing_message)
        """
        pass


class MinMax(Algorithm):

    def process_message(self, node_state: State, node_value: int, incoming_message: ElectMessage):
        if incoming_message.stage % 2 == 0 and incoming_message.value > node_value:
            # Here the message sent will contain our own value
            return State.CANDIDATE, incoming_message.value, new_message(incoming_message)
        elif incoming_message.stage % 2 == 1 and incoming_message.value < node_value:
            # Here again the message will contain our own value
            return State.CANDIDATE, incoming_message.value, new_message(incoming_message)
        # Otherwise the node will become defeated and the message will not continue any further
        return State.DEFEATED, node_value, None

    def asleep_act(self, node_state: State, node_value: int, incoming_message: Message):
        # In the general case we become defeated and forward the message
        return State.DEFEATED, node_value, incoming_message

    def originator_act(self, node_state: State, node_value: int, incoming_message: Message):
        # If the node state is an originator then we begin the message chain.
        return State.CANDIDATE, node_value, ElectMessage(node_value, 1, 0)

    def candidate_act(self, node_state: State, node_value: int, incoming_message: ElectMessage):
        if node_value == incoming_message.value:
            # In this case we have been elected
            return State.LEADER, node_value, None
        # General case we process the message
        return self.process_message(node_state, node_value, incoming_message)

    def defeated_act(self, node_state: State, node_value: int, incoming_message: Message):
        # Simply forward the message
        return node_state, node_value, incoming_message

    def act(self, node_state: State, node_value: int, node_stage: int, incoming_message: Message):
        if node_state == State.ORIGINATOR:
            return self.originator_act(node_state, node_value, incoming_message)
        elif node_state == State.ASLEEP:
            return self.asleep_act(node_state, node_value, incoming_message)
        elif node_state == State.CANDIDATE:
            return self.candidate_act(node_state, node_value, incoming_message)
        elif node_state == State.DEFEATED:
            return self.defeated_act(node_state, node_value, incoming_message)


class MinMaxPlus(Algorithm):
    def process_message(self, node_state: State, node_value: int, incoming_message: ElectMessage):
        if incoming_message.stage % 2 == 0 and incoming_message.value > node_value:
            # Here the message sent will contain our own value
            return State.CANDIDATE, incoming_message.value, new_message(incoming_message)
        elif incoming_message.stage % 2 == 1 and incoming_message.value < node_value:
            # Here again the message will contain our own value
            return State.CANDIDATE, incoming_message.value, new_message(incoming_message)
        elif incoming_message.counter == 0:
            # This handles the case where the counter becomes 0 at a Candidate that it would otherwise defeat
            return State.CANDIDATE, incoming_message.value, new_message(incoming_message)
        # Otherwise the node will become defeated and the message will not continue any further
        return State.DEFEATED, node_value, None

    def asleep_act(self, node_state: State, node_value: int, incoming_message: Message):
        # In the general case we become defeated and forward the message
        return State.DEFEATED, node_value, forwarded_message(incoming_message)

    def originator_act(self, node_state: State, node_value: int, incoming_message: Message):
        # If the node state is an originator then we begin the message chain.
        return State.CANDIDATE, node_value, ElectMessage(node_value, 1, 0)

    def candidate_act(self, node_state: State, node_value: int, node_stage: int, incoming_message: ElectMessage):
        # In this case we have been elected
        if node_value == incoming_message.value:
            return State.LEADER, node_value, None

        # In this case, the candidate will become defeated if it is receiving a message from the next step
        if node_stage < incoming_message.stage:
            return State.DEFEATED, node_value, forwarded_message(incoming_message)

        # General case we process the message
        return self.process_message(node_state, node_value, incoming_message)

    def defeated_act(self, node_state: State, node_value: int, node_stage: int, incoming_message: Message):
        if isinstance(incoming_message, ElectMessage):
            # This case handles when the node is defeated and the counter reaches 0 in an even stage
            if incoming_message.counter == 0:
                return State.CANDIDATE, incoming_message.value, new_message(incoming_message)
            # This is the case that handles rule 4
            elif node_stage % 2 == 0 and incoming_message.stage == node_stage + 1 \
                    and incoming_message.value < node_value:
                return State.CANDIDATE, incoming_message.value, new_message(incoming_message)

        # Simply forward the message, otherwise.
        return node_state, node_value, forwarded_message(incoming_message)

    def act(self, node_state: State, node_value: int, node_stage: int, incoming_message: Message):
        # Reduce message counter if we are in an even stage
        if isinstance(incoming_message, ElectMessage) and incoming_message.stage % 2 == 0:
            incoming_message.counter -= 1

        if node_state == State.ORIGINATOR:
            return self.originator_act(node_state, node_value, incoming_message)
        elif node_state == State.ASLEEP:
            return self.asleep_act(node_state, node_value, incoming_message)
        elif node_state == State.CANDIDATE:
            return self.candidate_act(node_state, node_value, node_stage, incoming_message)
        elif node_state == State.DEFEATED:
            return self.defeated_act(node_state, node_value, node_stage, incoming_message)


def fibonacci_number(index):
    """
    This function will simply give us the i-th fibonacci number.
    If the index is larger than our value, we will extend the list.
    Note: Could also just do this using Binet's formula, but due to rounding errors we don't risk it.
    :param index: The value of the index we wish to get.
    :return: The fibonacci number at the given index.
    """
    # Our seed Fibonacci numbers.
    sequence = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]

    # We will extend the series if it is not long enough.
    while index > len(sequence) - 1:
        sequence.append(sequence[len(sequence) - 1] + sequence[len(sequence) - 2])

    return sequence[index]


def forwarded_message(incoming_message: ElectMessage):
    """
    Here we need only decrease the counter if it exists
    :param incoming_message:
    :return:
    """
    if incoming_message.stage % 2 == 0:
        incoming_message.counter -= 1
    return incoming_message


def new_message(incoming_message: ElectMessage):
    """
    Here we need to update the value in the message, update the stage and decrease the counter.
    :param incoming_message:
    :return:
    """
    incoming_message.stage += 1

    # Update the counter to the i-th fibonacci number if we are in an even stage.
    incoming_message.counter = fibonacci_number(incoming_message.stage) if incoming_message.stage % 2 == 0 else -1

    return incoming_message
