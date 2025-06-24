from ...combatant import Combatant, MakeHit, R, Attack, Stat

class Fighter1(Combatant):
    def __init__(self, name, ac, hp, level, team, attacks):
        super().__init__(name, ac, hp, level, team, attacks)
        self.secondWind = 1
        self.AddSaveProf(Stat.STRENGTH)
        self.AddSaveProf(Stat.CONSTITUTION)
        
    def Act(self, others):
        if self.secondWind and self.maxHp - self.hp >= 5 + self.cr:
            self.secondWind -= 1
            self.hp += R(1,10)+self.cr
            self.hp = min(self.hp, self.maxHp)
        return super().Act(others)

class Fighter2(Fighter1):
    def __init__(self, name, ac, hp, level, team, attacks):
        super().__init__(name, ac, hp, level, team, attacks)
        self.surge = 1
    def Act(self, others):
        if self.surge:
            self.surge -= 1
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                self.Attack(targets[0])
        super().Act(others)

class Fighter1Archer(Fighter1):
    def __init__(self, team):
        super().__init__("Lvl1 Fighter (Archer)", 15, 12, 1, team, [Attack("Longbow", lambda r: r+7, MakeHit(lambda: R(1,8)+3), MakeHit(lambda: R(2,8)+3))])
        self.AddStats(12, 16, 14, 10, 14, 10)

class Fighter2Archer(Fighter2):
    def __init__(self, team):
        super().__init__("Lvl2 Fighter (Archer)", 15, 20, 2, team, [Attack("Longbow", lambda r: r+7, MakeHit(lambda: R(1,8)+3), MakeHit(lambda: R(2,8)+3))])
        self.AddStats(12, 16, 14, 10, 14, 10)

class Fighter1Duelist(Fighter1):
    def __init__(self, team):
        super().__init__("Lvl1 Fighter (Duelist)", 18, 12, 1, team, [Attack("Rapier", lambda r: r+5, MakeHit(lambda: R(1,8)+5), MakeHit(lambda: R(2,8)+5))])
        self.AddStats(12, 16, 14, 10, 14, 10)

class Fighter2Duelist(Fighter2):
    def __init__(self, team):
        super().__init__("Lvl2 Fighter (Duelist)", 18, 20, 2, team, [Attack("Rapier", lambda r: r+5, MakeHit(lambda: R(1,8)+5), MakeHit(lambda: R(2,8)+5))])
        self.AddStats(12, 16, 14, 10, 14, 10)

class Fighter1Mauler(Fighter1):
    def Reroll12(self, numDice, step):
        initialRoll = [R(1,step) for i in range(numDice)]
        return sum(R(1,step) if r < 3 else r for r in initialRoll)
    def __init__(self, team):
        super().__init__("Lvl1 Fighter (Great Weapons)", 16, 13, 1, team, [Attack("Maul", lambda r: r+5, MakeHit(lambda: self.Reroll12(2,6)+3), MakeHit(lambda: self.Reroll12(4,6)+3))])
        self.AddStats(16, 10, 16, 10, 14, 10)

class Fighter2Mauler(Fighter2):
    def Reroll12(self, low, high):
        x = R(low, high)
        return x if x > 2 else R(low, high)
    def __init__(self, team):
        super().__init__("Lvl2 Fighter (Great Weapons)", 16, 22, 2, team, [Attack("Maul", lambda r: r+5, MakeHit(lambda: self.Reroll12(2,6)+3), MakeHit(lambda: self.Reroll12(4,6)+3))])

class Fighter1Flow(Fighter1):
    def __init__(self, team):
        super().__init__("Lvl1 Fighter (Flow)", 16, 12, 1, team, [Attack("Shortsword", lambda r: r+5, MakeHit(lambda: R(1,6)+3), MakeHit(lambda: R(2,6)+3))])
        self.AddStats(10, 16, 14, 10, 14, 12)
    def Act(self, others):
        attacks = 1
        if self.secondWind and self.maxHp - self.hp >= 5 + self.cr:
            self.secondWind -= 1
            self.hp += R(1,10)+self.cr
            self.hp = min(self.hp, self.maxHp)
        else:
            attacks += 1
        for i in range(attacks): #BA Stab
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                self.Attack(targets[0])

class Fighter2Flow(Fighter2):
    def __init__(self, team):
        super().__init__("Lvl2 Fighter (Flow)", 16, 20, 2, team, [Attack("Longbow", lambda r: r+5, MakeHit(lambda: R(1,6)+3), MakeHit(lambda: R(2,6)+3))])
        self.AddStats(10, 16, 14, 10, 14, 12)
    def Act(self, others):
        if self.surge:
            self.surge -= 1
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                self.Attack(targets[0])
        attacks = 1
        if self.secondWind and self.maxHp - self.hp >= 5 + self.cr:
            self.secondWind -= 1
            self.hp += R(1,10)+self.cr
            self.hp = min(self.hp, self.maxHp)
        else:
            attacks += 1
        for i in range(attacks): #BA Stab
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                self.Attack(targets[0])