from ....combatant import Combatant, MakeHit, R, Attack

class GiantBoar(Combatant):
    def __init__(self, team):
        super().__init__("Giant Boar", 12, 42, 0, team, [Attack("Tusk",lambda r: r+5, MakeHit(lambda: R(2,6)+3), MakeHit(lambda: R(4,6)+3)), Attack("Charge",lambda r: r+5, MakeHit(lambda: R(4,6)+3), MakeHit(lambda: R(8,6)+3))])
        self.relentless = 1
        self.charge = 1
        self.AddSaves(3, 0, 3, -4, -2, -3)

    def Damage(self, amount):
        if amount <= 10 and self.hp <= amount and self.relentless:
            self.relentless -= 1
            return super().Damage(self.hp - 1)
        return super().Damage(amount)

    def Act(self, others):
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            if(self.charge):
                self.charge -= 1
                self.AttackWith(targets[0], self.attacks["Charge"])
            else:
                self.AttackWith(targets[0], self.attacks["Tusk"])
