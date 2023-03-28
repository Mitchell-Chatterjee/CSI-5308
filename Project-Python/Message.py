class Message:
    def __init__(self, value: int, stage: int, counter: int):
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