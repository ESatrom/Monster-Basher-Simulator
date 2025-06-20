from ....combatant import Combatant, Attack, MakeHit, R, RechargeAbility
from random import shuffle

class BlackDragonWyrmling(Combatant):
    def __init__(self, team):
        super().__init__("Black Dragon Wyrmling", 17, 33, 2, team, [Attack("Bite", lambda r: r+4, MakeHit(lambda: R(1,10)+R(1,4)+2), MakeHit(lambda: R(2,10)+2))])
        self.AddRecharge([RechargeAbility("Breath Weapons", 1, 1, 5)])
        self.AddSaves(2, 4, 3, 0, 2, 3)
    def AcidBreath(self, targets):
        self.rechargeAbilities["Breath Weapons"].charges -= 1
        shuffle(targets)
        dam = R(5,8)
        for t in targets[:2]:
            if R(1,20)+t.dex<11:#Dex save
                t.Damage(dam)
            else:
                t.Damage(int(dam/2))

    def Act(self, others):
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            if self.rechargeAbilities["Breath Weapons"].charges:
                self.AcidBreath(targets)
            else:
                self.Attack(targets[0])