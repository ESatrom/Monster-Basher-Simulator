from ....combatant import Combatant, MakeHit, R, Attack

class Quickling(Combatant):
    def __init__(self, team):
        super().__init__("Quickling", 16+6, 10, 6, team, [Attack("Dagger",lambda r: r+8, MakeHit(lambda: R(1,4)+6), MakeHit(lambda: R(2,4)+6))])
        #Increased AC to simulate Blurred Movement.
    def Act(self, others):
        for i in range(3): #Multiattack (3)
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                self.Attack(targets[0])