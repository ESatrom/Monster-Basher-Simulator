from ...combatant import *
from typing import List

class OldgrowthShaman3(Combatant):
    def __init__(self, team:str):
        super().__init__("Oldgrowth Shaman (CR 3)", 15, 44, 3, team, [Attack("Bone Dart", lambda r: r+R(1,4)+4, MakeHit((1,4,2,DamageType.PIERCING))), Attack("Black Bolt", lambda r: r+R(1,4)+5, MakeHit((4,6,0,DamageType.NECROTIC))), Attack("Mark", lambda r: r+R(1,4)+5, MakeHit((1,4,0,DamageType.PIERCING)))])
        self.AddConcentration()
        self.AddRecharge([RechargeAbility("Poison Dart", 1, 1, 5)])
        self.drain = 1
        self.virulentMark = 2
        self.AddStats(12, 14, 13, 10, 10, 16)
        self.AddSaveProf(Stat.WISDOM)
        self.AddSaveProf(Stat.CHARISMA)
        
    def RollSave(self, stat, advantage=False, disadvantage=False):
        return super().RollSave(stat, advantage, disadvantage) + R(1,4)
        
    def PoisonDart(self, target:Combatant):
        if self.AttackWith(target, "Bone Dart")[0].sourceAmount>0: #damage was dealt = we scored a hit
            if target.RollSave(Stat.CONSTITUTION)<12: #2 seems like a reasonable con save modifier
                target.GiveCondition(ConditionConstant.POISONED, "Poison Dart")
                def ClearPoison():
                    target.RemoveCondition(ConditionConstant.POISONED, "Poison Dart")
                    target.oldCleanUp += [ClearPoison]
                target.cleanUp += [ClearPoison]
        self.rechargeAbilities["Poison Dart"].charges -= 1

    def Drain(self, target:Combatant):
        self.drain -= 1
        stacks:int = 1
        if target.RollSave(Stat.WISDOM) < 13: #Wis save
            stacks = 2
        target.GiveCondition(ConditionConstant.EXHAUSTION, "Drain", stacks)
        def clean():
            target.GiveCondition(ConditionConstant.EXHAUSTION, "Drain", stacks)
            if target.HasCondition(ConditionConstant.EXHAUSTION) >= 6:
                target.hp = 0
                self.concentration = False
                target.oldCleanUp += [clean]
        target.cleanUp += [clean]
        def clearConc():
            target.RemoveCondition(ConditionConstant.EXHAUSTION, "Drain")
            try:target.cleanUp.remove(clean)
            except:pass
            self.concentration = False
        self.concentration = clearConc
    
    def VirulentMark(self, target:Combatant):
        self.virulentMark -= 1
        if self.AttackWith(target, "Mark")[0].sourceAmount > 0: #Hit, attempt inflict
            if target.RollSave(Stat.CONSTITUTION) <13: #DC 13 Con save
                target.GiveCondition(ConditionConstant.POISONED, "Virulent Mark")

    def Act(self, others:List[Combatant]):
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            avoidDrained = [t for t in targets if not t.HasCondition(ConditionConstant.EXHAUSTION)]
            if len(avoidDrained)>0:targets = avoidDrained
            if self.drain > 0 and (targets[-1].hp > 3 * 14 or (targets[-1].hp > 14 and sum(t.hp for t in targets) > 3 * 14)):
                self.Drain(targets[-1])
            elif not targets[-1].HasCondition(ConditionConstant.POISONED) and targets[-1].hp > 14*2 and self.virulentMark>0:
                self.VirulentMark(targets[-1])
            else:
                self.AttackWith(targets[0], self.attacks["Black Bolt"])

