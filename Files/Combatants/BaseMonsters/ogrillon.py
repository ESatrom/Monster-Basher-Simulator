from random import randint as R
from ...combatant import Combatant, MakeHit

class Ogrillon(Combatant):
    def __init__(self, team):
        super().__init__("Half-Ogre (Ogrillon)", 12, 30, lambda r: r+5, MakeHit(lambda: R(1,10)+R(1,10)+3), MakeHit(lambda: R(1,10)+R(1,10)+R(1,10)+R(1,10)+3), 0, team, 1)
