from ....combatant import *
from typing import List
from random import shuffle

class BrassDragonWyrmling(Combatant):
    def __init__(self, team:str):
        super().__init__("Brass Dragon Wyrmling", 16, 16, 1, team, Attack("Bite", 4, MakeHit((1,10,2,DamageType.PIERCING))))
        self.AddRecharge([RechargeAbility("Breath Weapons", 1, 1, 5)])
        self.AddStats(15, 10, 13, 10, 11, 13)
        self.AddSaveProf(Stat.DEXTERITY)
        self.AddSaveProf(Stat.CONSTITUTION)
        self.AddSaveProf(Stat.WISDOM)
        self.AddSaveProf(Stat.CHARISMA)
        self.immunities += [DamageType.FIRE]

    def FireBreath(self, targets:List[Combatant]):
        """Sprays fire over 2 targets in the list"""
        self.rechargeAbilities["Breath Weapons"].charges -= 1
        shuffle(targets)
        roll = R(4,6)
        for t in targets[:2]:
            dam = Damage(roll, DamageType.FIRE)
            if t.RollSave(Stat.DEXTERITY)>=11:
                dam.Multiply(1/2)
            t.Damage([dam])
    
    def SleepBreath(self, targets:List[Combatant]):
        """Exhales a draft of sleep-inducing fog over 2 targets in the list"""
        self.rechargeAbilities["Breath Weapons"].charges -= 1
        shuffle(targets)
        for t in targets[:2]:
            if t.RollSave(Stat.CONSTITUTION)<11:#Con save
                t.GiveCondition(ConditionConstant.UNCONSCIOUS, "Sleep Breath")
                def clean():
                    t.RemoveCondition(ConditionConstant.UNCONSCIOUS, "Sleep Breath")
                    t.oldDamageTriggers += [clean]
                t.damageTriggers += clean

    def Act(self, others:List[Combatant]):
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            if self.rechargeAbilities["Breath Weapons"].charges:
                self.FireBreath(targets)
            else:
                self.AttackWith(targets[0], "Bite")