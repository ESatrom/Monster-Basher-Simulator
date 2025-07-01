from ....combatant import *

class AnimatedArmor(Combatant):
    def __init__(self, team:str):
        super().__init__("Animated Armor", 18, 33, 1, team, Attack("Slam", 4, MakeHit((1,6,2,DamageType.BLUDGEONING))))
        self.AddStats(14, 11, 13, 1, 3, 1)
        self.multiattack = ["Slam","Slam"]
        self.immunities += [DamageType.POISON, DamageType.PSYCHIC]
        self.conditionImmunities += [ConditionConstant.BLINDED, ConditionConstant.CHARMED, ConditionConstant.DEAFENED, ConditionConstant.EXHAUSTION, ConditionConstant.FRIGHTENED, ConditionConstant.PARALYZED, ConditionConstant.PETRIFIED, ConditionConstant.POISONED]
