from ....combatant import Combatant, MakeHit, Attack, R

class AnimatedArmor(Combatant):
    def __init__(self, team):
        super().__init__("Animated Armor", 18, 33, 0, team, [Attack("Slam", lambda r: r+4, MakeHit(lambda: R(1,6)+2), MakeHit(lambda: R(2,6)+2))])

    def Act(self, others):
        for i in range(2): #Multiattack (2)
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                self.Attack(targets[0])