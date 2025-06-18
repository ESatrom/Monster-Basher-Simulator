from random import randint as R
from ...combatant import RechargeCombatant, MakeAttackFunc

class OldgrowthHunter1(RechargeCombatant):
    def __init__(self):
        RechargeCombatant.__init__(self, "OldgrowthHunter1", 16, 16, lambda r: r+R(1,4)+5, None, None, 3, "Oldgrowth", 2, 1, 1, 5)
        def HunterStrike(DamageLambda):
            def Hit(target):
                if(self.recharge and target.hp >= int(sum([DamageLambda()/32 in range(32)]))):
                    self.recharge -= 1
                    def DisadvantageAttack(t2):
                        x = min(R(1,20),R(1,20))
                        if x==1:return 0
                        if x==20:return target.crit(t2)
                        if target.modifier(x)>t2.ac:return target.hit(t2)
                        return 0
                    def ResetAttack():
                        target.Attack = MakeAttackFunc(target.modifier, target.hit, target.crit)
                        target.cleanUp.remove(ResetAttack)
                    if(R(1,20)+2<12):
                        target.cleanUp += [ResetAttack]
                        target.Attack = DisadvantageAttack
                dam = DamageLambda()
                target.hp -= dam
                return dam
            return Hit
        self.hit = HunterStrike(lambda: R(1,4)+3)
        self.crit = HunterStrike(lambda: R(1,4)+R(1,4)+3)
        self.Attack = MakeAttackFunc(self.modifier, self.hit, self.crit)
        
