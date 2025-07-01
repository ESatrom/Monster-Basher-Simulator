from ...combatant import *

class FlyingSnake(Combatant):
    def __init__(self, team:str):
        super().__init__("Flying Snake", 14, 5, 1/8, team, Attack("Bite", 6, MakeHit([(0,0,1,DamageType.PIERCING),(3,4,0,DamageType.POISON)])))
        self.AddStats(4, 18, 11, 2, 12, 5)
