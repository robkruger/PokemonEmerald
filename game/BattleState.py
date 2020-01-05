from enum import Enum


class BattleState(Enum):
    WAITING = 0,
    FRIENDLY_TURN = 1
    ENEMY_TURN = 2
