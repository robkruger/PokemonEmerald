from enum import Enum


class BattleState(Enum):
    START = 0
    WAITING = 1,
    FRIENDLY_TURN = 2
    ENEMY_TURN = 3
