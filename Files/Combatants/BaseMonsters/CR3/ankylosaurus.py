from ....combatant import *
from typing import List

class Ankylosaurus(Combatant):
    def __init__(self, team:str):
        super().__init__("Ankylosaurus", 15, 68, 3, team, Attack("Tail", 7, MakeHit((4,6,4,DamageType.BLUDGEONING))))
        self.AddStats(19, 11, 15, 2, 12, 5)
    def Act(self, others):
        if not isinstance(others,List):others = [others]
        targets:List[Combatant] = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            dam = self.AttackWith(targets[0], "Tail")
            if dam[0].sourceAmount > 0:
                if targets[0].RollSave(Stat.STRENGTH) < 14:
                    targets[0].GiveCondition(ConditionConstant.PRONE)