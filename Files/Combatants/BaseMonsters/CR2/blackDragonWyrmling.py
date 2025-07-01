from ....combatant import *
from random import shuffle
from typing import List

class BlackDragonWyrmling(Combatant):
    def __init__(self, team:str):
        super().__init__("Black Dragon Wyrmling", 17, 33, 2, team, Attack("Bite", 4, MakeHit([(1,10,2,DamageType.PIERCING),(1,4,0,DamageType.ACID)])))
        self.AddRecharge([RechargeAbility("Breath Weapons", 1, 1, 5)])
        self.AddStats(15, 14, 13, 10, 11, 13)
        self.AddSaveProf(Stat.DEXTERITY)
        self.AddSaveProf(Stat.CONSTITUTION)
        self.AddSaveProf(Stat.WISDOM)
        self.AddSaveProf(Stat.CHARISMA)
        self.immunities += [DamageType.ACID]
        
    def AcidBreath(self, targets:List[Combatant]):
        """Sprays acid on 2 targets"""
        self.rechargeAbilities["Breath Weapons"].charges -= 1
        shuffle(targets)
        roll = R(5,8)
        for t in targets[:2]:
            dam = Damage(roll, DamageType.ACID)
            if t.RollSave(Stat.DEXTERITY)>=11:#Dex save
                dam.Multiply(1/2)
            t.Damage(dam)

    def Act(self, others:List[Combatant]):
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            if self.rechargeAbilities["Breath Weapons"].charges:
                self.AcidBreath(targets)
            else:
                self.AttackWith(targets[0], "Bite")