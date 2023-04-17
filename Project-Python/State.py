from enum import Enum


class State(Enum):
    ASLEEP = "Asleep"
    CANDIDATE = "Candidate"
    DEFEATED = "Defeated"
    LEADER = "Leader"
    ORIGINATOR = "Originator"
