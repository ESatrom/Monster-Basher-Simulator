from ....combatant import Combatant, MakeHit, R, Attack

class Allosaurus(Combatant):
    def __init__(self, team):
        super().__init__("Allosaurus", 12, 42, 0, team, [Attack("Bite",lambda r: r+6, MakeHit(lambda: R(2,10)+4), MakeHit(lambda: R(4,10)+4)), Attack("Claw",lambda r: r+6, MakeHit(lambda: R(1,8)+4), MakeHit(lambda: R(2,8)+4))])
        self.AddSaves(4, 1, 3, -4, 1, -3)

    def Act(self, others):
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            self.AttackWith(targets[0], self.attacks["Bite"])