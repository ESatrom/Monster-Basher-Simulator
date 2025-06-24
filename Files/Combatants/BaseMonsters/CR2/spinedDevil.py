from ....combatant import Combatant, MakeHit, Attack, R

class SpinedDevil(Combatant):
    def __init__(self, team):
        super().__init__("Spined Devil", 13, 22, 2, team, [
            Attack("Bite", lambda r: r+2, MakeHit(lambda: R(2,4)), MakeHit(lambda: R(4,4)))
            ,Attack("Fork", lambda r: r+2, MakeHit(lambda: R(1,6)), MakeHit(lambda: R(2,6)))
            ,Attack("Tail Spine", lambda r: r+4, MakeHit(lambda: R(1,4)+2), MakeHit(lambda: R(2,4)))
        ])
        self.spines = 12
        self.AddStats(10, 15, 12, 11, 14, 8)

    def Damage(self, amount):
        return super().Damage(int(amount/2))

    def Act(self, others): #Multiattack (special, 2)
        for atk in ["Bite", "Fork"]:
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                if self.spines > 0:
                    self.AttackWith(targets[0], self.attacks["Tail Spine"])
                    self.spines -= 1
                else:
                    self.AttackWith(targets[0], self.attacks[atk])
