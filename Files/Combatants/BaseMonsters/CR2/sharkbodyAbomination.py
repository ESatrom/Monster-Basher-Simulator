from ....combatant import *

class SharkbodyAbomination(Combatant):
    def __init__(self, team:str):
        super().__init__("Sharkbody Abomination", 12, 45, 2, team, Attack("Bite", 6, MakeHit((2,8,4,DamageType.PIERCING))))
        self.AddStats(18, 13, 15, 1, 10, 4)

    def AttackWith(self, target, attack):
        if target.hp < target.maxHp:
            self.advantageSource += ["Blood Frenzy"]
        damage = super().AttackWith(target, attack)
        if "Blood Frenzy" in self.advantageSource:
            self.advantageSource.remove("Blood Frenzy")
        return damage
    
    def Act(self, others):
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp if c.hp == c.maxHp else c.hp * .75))
        if len(targets)>0:
            self.AttackWith(targets[0], "Bite")
