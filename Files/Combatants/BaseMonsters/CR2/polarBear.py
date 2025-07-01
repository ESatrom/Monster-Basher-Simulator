from ....combatant import *

class PolarBear(Combatant):
    def __init__(self, team:str):
        super().__init__("Polar Bear", 12, 42, 2, team, [Attack("Bite", 7, MakeHit((1,8,5,DamageType.PIERCING))), Attack("Claws", 7, MakeHit((2,6,5,DamageType.PIERCING)))])
        self.AddStats(20, 10, 16, 2, 13, 7)
        self.multiattack = ["Claws", "Bite"]
