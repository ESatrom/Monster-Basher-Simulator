from ....combatant import *
from typing import List

class GiantBoar(Combatant):
    def __init__(self, team:str):
        super().__init__("Giant Boar", 12, 42, 2, team, [Attack("Tusk", 5, MakeHit((2,6,3,DamageType.SLASHING))), Attack("Charge", 5, MakeHit((4,6,3,DamageType.SLASHING)))])
        self.relentless = 1
        self.charge = 1
        self.AddStats(17, 10, 16, 2, 7, 5)

    def Damage(self, damage:List[Damage] | Damage):
        super().Damage(damage)
        if sum(d.finalAmount for d in damage) <= 10 and self.hp <= sum(d.finalAmount for d in damage) and self.relentless:
            self.relentless -= 1
            self.hp = 1

    def Act(self, others):
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            if(self.charge):
                self.charge -= 1
                dam = self.AttackWith(targets[0], "Charge")
                if dam[0].sourceAmount >= 0:
                    if targets[0].RollSave(Stat.STRENGTH) < 13:
                        targets[0].GiveCondition(ConditionConstant.PRONE)
            else:
                self.AttackWith(targets[0], "Tusk")
