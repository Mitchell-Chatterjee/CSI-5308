from enum import Enum


class Stage(Enum):
    EVEN = True
    ODD = False


class Message:
    def __init__(self, value: int, stage: Stage, counter: int):
        self._value = value
        self._stage = stage
        self._counter = counter

    @property
    def value(self):
        return self._value

    @property
    def stage(self):
        return self._stage

    @property
    def counter(self):
        return self._counter

    @value.setter
    def value(self, value):
        self._value = value

    @stage.setter
    def stage(self, stage):
        self._stage = stage

    @counter.setter
    def counter(self, counter):
        self._counter = counter
