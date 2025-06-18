from random import randint as R
from ...combatant import Combatant, MakeHit

class Fighter1Archer(Combatant):
    def __init__(self):
        Combatant.__init__(self, "Archer1", 15, 12, lambda r: r+7, MakeHit(lambda: R(1,8)+3), MakeHit(lambda: R(1,8)+R(1,8)+3), 3, "Players", 1)
