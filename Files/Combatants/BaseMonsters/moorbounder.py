from random import randint as R
from ...combatant import Combatant, MakeHit

class Moorbounder(Combatant):
    def __init__(self, team):
        super().__init__("Moorbounder", 13, 30, lambda r: r+6, MakeHit(lambda: R(1,4)+R(1,4)+R(1,4)+R(1,4)+4), MakeHit(lambda: R(1,4)+R(1,4)+R(1,4)+R(1,4)+R(1,4)+R(1,4)+R(1,4)+R(1,4)+4), 2, team, 1)
