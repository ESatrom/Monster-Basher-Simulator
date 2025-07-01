from ....combatant import *

class Ettercap(Combatant):
    def __init__(self, team:str):
        super().__init__("Ettercap", 13, 44, 2, team, [Attack("Bite", 4, MakeHit([(1,8,2,DamageType.PIERCING),(1,8,0,DamageType.POISON)])), Attack("Claws", 4, MakeHit((2,4,2,DamageType.SLASHING)))])
        self.AddStats(14, 15, 13, 7, 12, 8)

    def Act(self, others):
        for atk in ["Claws", "Bite"]:
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                if atk == "Bite" and targets[0].HasCondition(ConditionConstant.POISONED) and len(t for t in targets if not t.HasCondition(ConditionConstant.POISONED)) > 0 and not targets[0].hp < 11:
                    target = list(filter(lambda t: not t.HasCondition(ConditionConstant.POISONED), targets))[0]
                    dmg = self.AttackWith(target, atk) #If a kill is unlikely, prioritize poisoning over takedown
                    if sum(d.sourceAmount for d in dmg) > 0: #damage dealt, that's a hit, roll to poison
                        if target.RollSave(Stat.CONSTITUTION) < 11: #DC 11 con save
                            target.GiveCondition(ConditionConstant.POISONED, "Bite")
                            def clean():
                                if target.RollSave(Stat.CONSTITUTION) >= 11: #DC 11 con save
                                    target.RemoveCondition(ConditionConstant.POISONED, "Bite")
                                    target.oldCleanUp += [clean]
                            target.cleanUp += [clean]
                else:
                    self.AttackWith(targets[0], atk)