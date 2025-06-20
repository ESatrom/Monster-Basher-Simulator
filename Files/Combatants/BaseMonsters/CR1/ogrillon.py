from ....combatant import Combatant, MakeHit, Attack, R

class Ogrillon(Combatant):
    def __init__(self, team):
        super().__init__("Half-Ogre (Ogrillon)", 12, 30, 0, team, [
            Attack("Battleaxe (1 hand)", lambda r: r+5, MakeHit(lambda: R(2,8)+3), MakeHit(lambda: R(4,8)+3))
            ,Attack("Battleaxe (2 hands)", lambda r: r+5, MakeHit(lambda: R(2,10)+3), MakeHit(lambda: R(4,10)+3))
            ,Attack("Javelin", lambda r: r+5, MakeHit(lambda: R(2,6)+3), MakeHit(lambda: R(4,6)+3))
        ])

    def Act(self, others): #The ogrillon has multiple options. Thankfully, if we're assuming everything is always in range, there's only one correct one
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            self.AttackWith(targets[0], self.attacks["Battleaxe (2 hands)"])
