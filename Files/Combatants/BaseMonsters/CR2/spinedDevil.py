from ....combatant import *

class SpinedDevil(Combatant):
    def __init__(self, team:str):
        super().__init__("Spined Devil", 13, 22, 2, team, [
            Attack("Bite", 2, MakeHit((2,4,0,DamageType.SLASHING)))
            ,Attack("Fork", 2, MakeHit((1,6,0,DamageType.PIERCING)))
            ,Attack("Tail Spine", 4, MakeHit([(1,4,2,DamageType.PIERCING),(1,6,0,DamageType.FIRE)]))
        ])
        self.spines = 12
        self.AddStats(10, 15, 12, 11, 14, 8)
        self.resistances += [DamageType.COLD, DamageType.BLUDGEONING, DamageType.PIERCING, DamageType.SLASHING]
        self.immunities += [DamageType.FIRE, DamageType.POISON]
        self.conditionImmunities += [ConditionConstant.POISONED]

    def Damage(self, damage):
        #TODO Full damage for phys not magical or adamantine
        # for d in damage:
        #     if d.damageType in (DamageType.PIERCING, DamageType.BLUDGEONING, DamageType.SLASHING) and magic or adaamntine:
        #         d.Multiply(2)
        return super().Damage(damage)


    def Act(self, others): #Multiattack (special, 2)
        for atk in ["Bite", "Fork"]:
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                if self.spines > 0:
                    self.AttackWith(targets[0], self.attacks["Tail Spine"])
                    self.spines -= 1
                else:
                    self.AttackWith(targets[0], atk)
