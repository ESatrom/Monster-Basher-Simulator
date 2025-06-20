from ....combatant import Combatant, MakeHit, R, Attack

class BrownBear(Combatant):
    def __init__(self, team):
        super().__init__("Brown Bear", 11, 34, 0, team, [Attack("Bite",lambda r: r+6, MakeHit(lambda: R(1,8)+4), MakeHit(lambda: R(2,8)+4)), Attack("Claws",lambda r: r+6, MakeHit(lambda: R(2,6)+4), MakeHit(lambda: R(4,6)+4))])
        self.AddSaves(4, 0, 3, -4, 1, -2)

    def Act(self, others):
        for atk in ["Claws", "Bite"]:
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                self.AttackWith(targets[0], self.attacks[atk])