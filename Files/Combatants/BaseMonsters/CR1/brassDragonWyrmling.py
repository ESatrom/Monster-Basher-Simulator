from ....combatant import Combatant, Attack, MakeHit, R, RechargeAbility
from random import shuffle

class BrassDragonWyrmling(Combatant):
    def __init__(self, team):
        super().__init__("Brass Dragon Wyrmling", 16, 16, 3, team, [Attack("Bite", lambda r: r+4, MakeHit(lambda: R(1,10)+2), MakeHit(lambda: R(2,10)+2))])
        self.AddRecharge([RechargeAbility("Breath Weapons", 1, 1, 5)])

    def FireBreath(self, targets):
        self.rechargeAbilities["Breath Weapons"].charges -= 1
        shuffle(targets)
        dam = R(4,6)
        for t in targets[:2]:
            if R(1,20)+2<11:#Dex save
                t.Damage(dam)
            else:
                t.Damage(int(dam/2))
            
    
    def SleepBreath(self, targets):
        self.rechargeAbilities["Breath Weapons"].charges -= 1
        shuffle(targets)
        for t in targets[:2]:
            if R(1,20)+2<11:#Con save
                t.paralyzed.add("On Damage")

    def Act(self, others):
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            if self.rechargeAbilities["Breath Weapons"].charges:
                self.FireBreath(targets)
            else:
                self.Attack(targets[0])