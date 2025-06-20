from ....combatant import Combatant, MakeHit, R, Attack

class SharkbodyAbomination(Combatant):
    def __init__(self, team):
        super().__init__("Sharkbody Abomination", 12, 45, 1, team, [Attack("Bite",lambda r: r+6, MakeHit(lambda: R(2,8)+4), MakeHit(lambda: R(4,8)+4))])

    def Act(self, others):
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp if c.hp == c.maxHp else c.hp * .75))
        if len(targets)>0:
            if targets[0].hp == targets[0].maxHp:
                self.Attack(targets[0])
            else: #Blood Frenzy advantage
                x = R(1,20)
                if not len(self.poisoned)>0: x = min(x,R(1,20))
                if x==1:return 0 #fumble
                if x==20:return self.attack.Crit(targets[0]) #natural crit
                if self.attack.Modifier(x)>targets[0].ac: #hit
                    if targets[0].paralyzed: #paralysis crit
                        return self.attack.Crit(targets[0])
                    else: #normal damage
                        return self.attack.Hit(targets[0])
                return 0 #miss
