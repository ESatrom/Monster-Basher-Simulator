from ...combatant import Combatant, R, RechargeAbility, Attack, MakeHit

class OldgrowthHunter1(Combatant):
    def __init__(self, team):
        super().__init__("Oldgrowth Hunter (CR 1)", 16, 27, 3, team, [Attack("Bone Dart", lambda r: r+R(1,4)+5, MakeHit(lambda: R(1,4)+3), MakeHit(lambda: R(2,4)+3))])
        self.AddRecharge([RechargeAbility("Poison Dart", 1, 1, 5),RechargeAbility("Bone Dart", 6, 2, 5)])
        self.AddSaves(4, 5, 4, 2, 2, 2)

    def BoneDart(self, target):
        if self.rechargeAbilities["Bone Dart"].charges>0:
            self.Attack(target)
            self.rechargeAbilities["Bone Dart"].charges -= 1

    def PoisonDart(self, target):
        if self.rechargeAbilities["Bone Dart"].charges>0:
            if self.Attack(target)>0: #damage was dealt = we scored a hit
                if R(1,20)+target.con<12: #2 seems like a reasonable con save modifier
                    target.poisoned.add("Oldgrowth Poison Dart")
                    def ClearPoison():
                        try:target.poisoned.remove("Oldgrowth Poison Dart")
                        except:pass
                        target.oldCleanUp += [ClearPoison]
                    target.cleanUp += [ClearPoison]
            self.rechargeAbilities["Bone Dart"].charges -= 1
            self.rechargeAbilities["Poison Dart"].charges -= 1
                
    def Act(self, others):
        for i in range(2): #Multiattack (2)
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                if len(targets[0].poisoned)<1 and self.rechargeAbilities["Poison Dart"].charges>0:
                    self.PoisonDart(targets[0])
                else:
                    self.BoneDart(targets[0])

class OldgrowthHunter2Slow(OldgrowthHunter1):
    def __init__(self, team):
        super().__init__(team)
        self.name = "Oldgrowth Hunter (CR2, slow)"
        self.ac = 16
        self.maxHp = 42
        self.rechargeAbilities["Bone Dart"].maxCharges = 8
        self.AddSaves(4, 5, 4, 2, 2, 2)

class OldgrowthHunter2Fast(OldgrowthHunter1):
    def __init__(self, team):
        super().__init__(team)
        self.name = "Oldgrowth Hunter (CR2, Fast)"
        self.ac = 16
        self.maxHp = 36
        self.rechargeAbilities["Bone Dart"].maxCharges = 8
        self.AddSaves(4, 5, 3, 2, 2, 2)
                
    def Act(self, others):
        for i in range(3): #Multiattack (3)
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                if len(targets[0].poisoned)<1 and self.rechargeAbilities["Poison Dart"].charges>0:
                    self.PoisonDart(targets[0])
                else:
                    self.BoneDart(targets[0])

class OldgrowthHunter2Fastest(OldgrowthHunter1):
    def __init__(self, team):
        super().__init__(team)
        self.name = "Oldgrowth Hunter (CR2, Fastest)"
        self.ac = 16
        self.maxHp = 28
        self.rechargeAbilities["Bone Dart"].rolls = 3
        self.rechargeAbilities["Bone Dart"].maxCharges = 8
        self.AddSaves(4, 5, 4, 2, 2, 2)
                
    def Act(self, others):
        for i in range(3): #Multiattack (3)
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                if len(targets[0].poisoned)<1 and self.rechargeAbilities["Poison Dart"].charges>0:
                    self.PoisonDart(targets[0])
                else:
                    self.BoneDart(targets[0])
