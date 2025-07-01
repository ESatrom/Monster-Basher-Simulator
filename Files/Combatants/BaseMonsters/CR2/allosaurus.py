from ....combatant import *

class Allosaurus(Combatant):
    def __init__(self, team:str):
        super().__init__("Allosaurus", 12, 42, 2, team, [Attack("Bite", 6, MakeHit((2,10,4,DamageType.PIERCING))), Attack("Claw", 6, MakeHit((2,8,4,DamageType.SLASHING)))])
        self.AddStats(19, 13, 17, 2, 12, 5)
        self.pounce = 1

    def Act(self, others):
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            if self.pounce:
                self.pounce = 0
                hit = self.AttackWith(targets[0], "Claw")[0].sourceAmount
                if hit:
                    targets[0].GiveCondition(ConditionConstant.PRONE, None)
                    if targets[0].HasCondition(ConditionConstant.PRONE):
                        self.AttackWith(targets[0], "Bite")
            else:
                self.AttackWith(targets[0], "Bite")