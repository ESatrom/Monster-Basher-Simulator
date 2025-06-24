from ....combatant import Combatant, MakeHit, Attack, R

class Ogre(Combatant):
    def __init__(self, team):
        super().__init__("Ogre", 11, 59, 2, team, [
            Attack("Greatclub", lambda r: r+6, MakeHit(lambda: R(2,8)+4), MakeHit(lambda: R(4,8)+4))
            ,Attack("Javelin", lambda r: r+6, MakeHit(lambda: R(2,6)+4), MakeHit(lambda: R(4,6)+4))
        ])
        self.AddStats(19, 8, 16, 5, 7, 7)

    def Act(self, others): #Shrek has multiple options. Thankfully, if we're assuming everything is always in range, there's only one correct one
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            self.AttackWith(targets[0], self.attacks["Greatclub"])
