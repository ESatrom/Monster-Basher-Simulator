from ....combatant import *

class Gargoyle(Combatant):
    def __init__(self, team:str):
        super().__init__("Gargoyle", 15, 52, 2, team, [Attack("Bite", 4, MakeHit((1,6,2,DamageType.PIERCING))), Attack("Claws", 4, MakeHit((1,6,2,DamageType.SLASHING)))])
        self.AddStats(15, 11, 16, 6, 11, 7)
        self.multiattack = ["Claws", "Bite"]
        self.resistances += [DamageType.BLUDGEONING, DamageType.PIERCING, DamageType.SLASHING]
        self.immunities += [DamageType.POISON]
        self.conditionImmunities += [ConditionConstant.EXHAUSTION, ConditionConstant.PETRIFIED, ConditionConstant.POISONED]
        
    def Damage(self, damage):
        #TODO Full damage for phys not magical or adamantine
        # for d in damage:
        #     if d.damageType in (DamageType.PIERCING, DamageType.BLUDGEONING, DamageType.SLASHING) and magic or adaamntine:
        #         d.Multiply(2)
        return super().Damage(damage)
