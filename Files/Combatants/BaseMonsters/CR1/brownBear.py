from ....combatant import *

class BrownBear(Combatant):
    def __init__(self, team:str):
        super().__init__("Brown Bear", 11, 34, 1, team, [Attack("Bite", 6, MakeHit((1,8,4,DamageType.PIERCING))), Attack("Claws", 6, MakeHit((2,6,4,DamageType.SLASHING)))])
        self.AddStats(19, 10, 16, 2, 13, 7)
        self.multiattack = ["Claws", "Bite"]
