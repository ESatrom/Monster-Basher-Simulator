from ...combatant import Combatant, MakeHit, R, Attack

class Fighter1(Combatant):
    def __init__(self, name, ac, hp, initiative, team, attacks):
        super().__init__(name, ac, hp, initiative, team, attacks)
        self.level = 1
    def Reset(self):
        self.secondWind = 1
        return super().Reset()
    def Act(self, others):
        if self.secondWind and self.maxHp - self.hp >= 5 + self.level:
            self.secondWind -= 1
            self.hp += R(1,10)+self.level
            self.hp = min(self.hp, self.maxHp)
        return super().Act(others)

class Fighter2(Fighter1):
    def __init__(self, name, ac, hp, initiative, team, attacks):
        super().__init__(name, ac, hp, initiative, team, attacks)
        self.level = 2
        self.surge = 1
    def Reset(self):
        self.surge = 1
        return super().Reset()
    def Act(self, others):
        if self.surge:
            self.surge -= 1
            self.Attack(others)
        super().Act(others)

class Fighter1Archer(Fighter1):
    def __init__(self, team):
        super().__init__("Lvl1 Fighter (Archer)", 15, 12, 3, team, [Attack("Longbow", lambda r: r+7, MakeHit(lambda: R(1,8)+3), MakeHit(lambda: R(2,8)+3))])

class Fighter2Archer(Fighter2):
    def __init__(self, team):
        super().__init__("Lvl2 Fighter (Archer)", 15, 20, 3, team, [Attack("Longbow", lambda r: r+7, MakeHit(lambda: R(1,8)+3), MakeHit(lambda: R(2,8)+3))])

class Fighter1Duelist(Fighter1):
    def __init__(self, team):
        super().__init__("Lvl1 Fighter (Duelist)", 18, 12, 3, team, [Attack("Rapier", lambda r: r+5, MakeHit(lambda: R(1,8)+5), MakeHit(lambda: R(2,8)+5))])

class Fighter2Duelist(Fighter2):
    def __init__(self, team):
        super().__init__("Lvl2 Fighter (Duelist)", 18, 20, 3, team, [Attack("Rapier", lambda r: r+5, MakeHit(lambda: R(1,8)+5), MakeHit(lambda: R(2,8)+5))])

class Fighter1Mauler(Fighter1):
    def Reroll12(self, numDice, step):
        initialRoll = [R(1,step) for i in range(numDice)]
        return sum(R(1,step) if r < 3 else r for r in initialRoll)
    def __init__(self, team):
        super().__init__("Lvl1 Fighter (Great Weapons)", 16, 12, 1, team, [Attack("Maul", lambda r: r+5, MakeHit(lambda: self.Reroll12(2,6)+3), MakeHit(lambda: self.Reroll12(4,6)+3))])

class Fighter2Mauler(Fighter2):
    def Reroll12(self, low, high):
        x = R(low, high)
        return x if x > 2 else R(low, high)
    def __init__(self, team):
        super().__init__("Lvl2 Fighter (Great Weapons)", 16, 20, 1, team, [Attack("Maul", lambda r: r+5, MakeHit(lambda: self.Reroll12(2,6)+3), MakeHit(lambda: self.Reroll12(4,6)+3))])