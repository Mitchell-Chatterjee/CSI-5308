from enum import Enum
from abc import ABC


class Message(ABC):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return self._value


class ElectMessage(Message):
    def __init__(self, value: int, stage: int, counter: int):
        self._stage = stage
        self._counter = counter
        super().__init__(value)

    @property
    def stage(self):
        return self._stage

    @property
    def counter(self):
        return self._counter

    @stage.setter
    def stage(self, stage):
        self._stage = stage

    @counter.setter
    def counter(self, counter):
        self._counter = counter


class NotifyMessage(Message):
    def __init__(self, value: None):
        super().__init__(value)


class WakeUpMessage(Message):
    def __init__(self, value):
        super().__init__(value)
