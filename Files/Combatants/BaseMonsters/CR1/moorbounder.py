from ....combatant import *

class Moorbounder(Combatant):
    def __init__(self, team:str):
        super().__init__("Moorbounder", 13, 30, 1, team, Attack("Claws", 6, MakeHit((4,4,4,DamageType.SLASHING))))
        self.AddStats(18, 14, 14, 2, 13, 5)
