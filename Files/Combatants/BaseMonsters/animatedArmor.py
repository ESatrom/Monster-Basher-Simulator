from random import randint as R
from ...combatant import Combatant, MakeHit

class AnimatedArmor(Combatant):
    def __init__(self, team):
        super().__init__("Animated Armor", 18, 33, lambda r: r+4, MakeHit(lambda: R(1,6)+2), MakeHit(lambda: R(1,6)+2), 0, team, 2)
