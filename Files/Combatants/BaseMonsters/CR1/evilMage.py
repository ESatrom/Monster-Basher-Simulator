from ....combatant import *
from typing import List

class EvilMage(Combatant):
    def __init__(self, team:str):
        super().__init__("Evil Mage", 12, 22, 1, team, [Attack("Shocking Grasp", 5, MakeHit((1,8,0,DamageType.LIGHTNING))), Attack("Quarterstaff", 1, MakeHit((1,8,-1,DamageType.BLUDGEONING)))])
        self.AddConcentration()
        self.ones = 4
        self.twos = 3
        self.AddStats(9, 14, 11, 17, 12, 11)
        self.AddSaveProf(Stat.INTELLIGENCE)
        self.AddSaveProf(Stat.WISDOM)

    def MagicMissileDart(self, target:Combatant):
        target.Damage(Damage(R(1,4)+1,DamageType.FORCE))

    def MagicMissile(self, darts:int, targets:List[Combatant]):
        """Distributes <darts> darts of magic missile between the targets, attempting to kill as many as possible with average damage"""
        missiles = darts
        for t in targets:
            if missiles > 0 and t.hp > 0:
                x = min(missiles, int(t.hp/3.5))
                missiles -= x
                for i in range(x):self.MagicMissileDart(t)
        for m in range(missiles):
            self.MagicMissileDart(targets[0])
            
    def HoldPerson(self, target:Combatant):
        if target.RollSave(Stat.WISDOM) < 13: #Wis save
            target.GiveCondition(ConditionConstant.PARALYZED, "Hold Person")
            def clean():
                if target.RollSave(Stat.WISDOM) >= 13:
                    target.RemoveCondition(ConditionConstant.PARALYZED, "Hold Person")
                    target.oldCleanUp += [clean]
                    self.concentration = False
            target.cleanUp += [clean]
            def clearConc():
                target.RemoveCondition(ConditionConstant.PARALYZED, "Hold Person")
                try:target.cleanUp.remove(clean)
                except:pass
                self.concentration = False
            self.concentration = clearConc
    
    def Act(self, others:List[Combatant]):
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            if not targets[0].HasCondition(ConditionConstant.PARALYZED) and self.twos > 0:
                if targets[0].hp <= int(3.5*3) and self.ones > 0:
                    self.ones -= 1
                    self.MagicMissile(3, targets)
                elif targets[0].hp <= int(3.5*4):
                    self.twos -= 1
                    self.MagicMissile(4, targets)
                else:
                    self.twos -= 1
                    self.HoldPerson(targets[0])
            else:
                if self.ones > 0:
                    self.ones -= 1
                    self.MagicMissile(3, targets)
                elif self.twos > 0:
                    self.twos -= 1
                    self.MagicMissile(4, targets)
                else:
                    self.AttackWith(targets[0], "Shocking Grasp")
