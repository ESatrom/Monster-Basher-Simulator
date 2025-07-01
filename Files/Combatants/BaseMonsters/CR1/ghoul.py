from ....combatant import *

class Ghoul(Combatant):
    def __init__(self, team:str):
        super().__init__("Ghoul", 12, 22, 1, team, [Attack("Bite", 2, MakeHit((2,6,2,DamageType.PIERCING))), Attack("Claws", 4, MakeHit((2,4,2,DamageType.SLASHING)))])
        self.AddStats(13, 15, 10, 7, 10, 6)
        self.immunities += [DamageType.POISON]
        self.conditionImmunities += [ConditionConstant.CHARMED, ConditionConstant.EXHAUSTION, ConditionConstant.POISONED]
        
    def Act(self, others):
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            if targets[0].HasCondition(ConditionConstant.PARALYZED): #Bite Paralyzed targets (higher damage worth worse to hit if paralyzed, not otherwise)
                self.AttackWith(targets[0], "Bite")
            else: #Otherwise claw them up, inflict paralysis
                if self.AttackWith(targets[0], "Claws")[0].sourceAmount > 0: #on damage dealt (hit), inflict paralysis
                    if targets[0].RollSave(Stat.CONSTITUTION) < 10: #DC 10 con save
                        targets[0].GiveCondition(ConditionConstant.PARALYZED, "Claws")
                        def clean():
                            if targets[0].RollSave(Stat.CONSTITUTION) >= 10: #DC 10 con save
                                targets[0].RemoveCondition(ConditionConstant.PARALYZED, "Claws")
                                targets[0].oldCleanUp += [clean]
                        targets[0].cleanUp += [clean]