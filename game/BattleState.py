from enum import Enum


class BattleState(Enum):
    START = 0
    WAITING = 1
    START_TURNS = 2
    FRIENDLY_TURN = 3
    ENEMY_TURN = 4
