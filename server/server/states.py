#!/usr/bin/env python3

from enum import Enum, auto, unique

@unique
class GlobalState(Enum):
    Uninitialized = auto()
    WaitingForActionOne = auto()
    WaitingForActionEvery = auto()

class ServerState:
    def __init__(self, global_state : GlobalState, **args):
        self.state = global_state
        self.args = {**args}
