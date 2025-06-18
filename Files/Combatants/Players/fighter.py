from random import randint as R
from ...combatant import Combatant, MakeHit

class Fighter1(Combatant):
    def __init__(self, name, ac, hp, ModifierLambda, HitLambda, CritLambda, initiative, team, numberOfAttacks):
        super().__init__(name, ac, hp, ModifierLambda, HitLambda, CritLambda, initiative, team, numberOfAttacks)
        self.level = 1
    def Reset(self):
        self.secondWind = 1
        return super().Reset()
    def TakeTurn(self, others):
        if(self.secondWind and self.maxHp - self.hp >= 5 + self.level):
            self.secondWind -= 1
            self.hp += R(1,10)+self.level
            self.hp = min(self.hp, self.maxHp)
        return super().TakeTurn(others)

class Fighter2(Fighter1):
    def __init__(self, name, ac, hp, ModifierLambda, HitLambda, CritLambda, initiative, team, numberOfAttacks):
        super().__init__(name, ac, hp, ModifierLambda, HitLambda, CritLambda, initiative, team, numberOfAttacks)
        self.level = 2
        self.surge = 1
    def Reset(self):
        self.surge = 1
        return super().Reset()
    def TakeTurn(self, others):
        if(self.surge):
            self.surge -= 1
            self.AttackAction(others)
        super().TakeTurn(others)

class Fighter1Archer(Fighter1):
    def __init__(self):
        super().__init__("Archer1", 15, 12, lambda r: r+7, MakeHit(lambda: R(1,8)+3), MakeHit(lambda: R(1,8)+R(1,8)+3), 3, "Players", 1)

class Fighter2Archer(Fighter2):
    def __init__(self):
        super().__init__("Archer2", 15, 20, lambda r: r+7, MakeHit(lambda: R(1,8)+3), MakeHit(lambda: R(1,8)+R(1,8)+3), 3, "Players", 1)
