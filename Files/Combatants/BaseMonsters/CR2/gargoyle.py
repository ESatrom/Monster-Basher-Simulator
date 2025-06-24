from ....combatant import Combatant, MakeHit, R, Attack

class Gargoyle(Combatant):
    def __init__(self, team):
        super().__init__("Gargoyle", 15, 52, 2, team, [Attack("Bite",lambda r: r+4, MakeHit(lambda: R(1,6)+2), MakeHit(lambda: R(2,6)+2)), Attack("Claws",lambda r: r+4, MakeHit(lambda: R(1,6)+2), MakeHit(lambda: R(2,6)+2))])
        self.AddStats(15, 11, 16, 6, 11, 7)

    def Damage(self, amount):
        return super().Damage(int(amount/2))

    def Act(self, others):
        for atk in ["Claws", "Bite"]:
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                self.AttackWith(targets[0], self.attacks[atk])