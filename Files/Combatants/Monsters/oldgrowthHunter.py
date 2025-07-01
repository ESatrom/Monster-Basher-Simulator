from ...combatant import *

class OldgrowthHunter1(Combatant):
    def __init__(self, team:str):
        super().__init__("Oldgrowth Hunter (CR 1)", 16, 27, 1, team, Attack("Bone Dart", lambda r: r+R(1,4)+5, MakeHit((1,4,3,DamageType.PIERCING))))
        self.AddRecharge([RechargeAbility("Poison Dart", 1, 1, 5),RechargeAbility("Bone Dart", 6, 2, 5)])
        self.AddStats(14, 16, 15, 10, 10, 10)
        self.AddSaveProf(Stat.DEXTERITY)
        self.AddSaveProf(Stat.STRENGTH)
        
    def RollSave(self, stat, advantage=False, disadvantage=False):
        return super().RollSave(stat, advantage, disadvantage) + R(1,4)

    def BoneDart(self, target:Combatant):
        if self.rechargeAbilities["Bone Dart"].charges>0:
            self.AttackWith(target, "Bone Dart")
            self.rechargeAbilities["Bone Dart"].charges -= 1

    def PoisonDart(self, target:Combatant):
        if self.rechargeAbilities["Bone Dart"].charges>0:
            if self.AttackWith(target, "Bone Dart")[0].sourceAmount>0: #damage was dealt = we scored a hit
                if target.RollSave(Stat.CONSTITUTION)<12: #2 seems like a reasonable con save modifier
                    target.GiveCondition(ConditionConstant.POISONED, "Poison Dart")
                    def ClearPoison():
                        target.RemoveCondition(ConditionConstant.POISONED, "Poison Dart")
                        target.oldCleanUp += [ClearPoison]
                    target.cleanUp += [ClearPoison]
            self.rechargeAbilities["Bone Dart"].charges -= 1
            self.rechargeAbilities["Poison Dart"].charges -= 1
                
    def Act(self, others):
        for i in range(2): #Multiattack (2)
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                if not targets[0].HasCondition(ConditionConstant.POISONED) and self.rechargeAbilities["Poison Dart"].charges>0:
                    self.PoisonDart(targets[0])
                else:
                    self.BoneDart(targets[0])

class OldgrowthHunter2Slow(OldgrowthHunter1):
    def __init__(self, team:str):
        super().__init__(team)
        self.name = "Oldgrowth Hunter (CR2, slow)"
        self.cr = 2
        self.ac = 16
        self.maxHp = 42
        self.rechargeAbilities["Bone Dart"].maxCharges = 8
        self.AddStats(14, 16, 15, 10, 10, 10)
        self.AddSaveProf(Stat.DEXTERITY)
        self.AddSaveProf(Stat.STRENGTH)

class OldgrowthHunter2Fast(OldgrowthHunter1):
    def __init__(self, team:str):
        super().__init__(team)
        self.name = "Oldgrowth Hunter (CR2, Fast)"
        self.cr = 2
        self.ac = 16
        self.maxHp = 36
        self.rechargeAbilities["Bone Dart"].maxCharges = 8
        self.AddStats(14, 17, 13, 10, 10, 10)
        self.AddSaveProf(Stat.DEXTERITY)
        self.AddSaveProf(Stat.STRENGTH)
                
    def Act(self, others):
        for i in range(3): #Multiattack (3)
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                if not targets[0].HasCondition(ConditionConstant.POISONED) and self.rechargeAbilities["Poison Dart"].charges>0:
                    self.PoisonDart(targets[0])
                else:
                    self.BoneDart(targets[0])

class OldgrowthHunter2Fastest(OldgrowthHunter1):
    def __init__(self, team:str):
        super().__init__(team)
        self.name = "Oldgrowth Hunter (CR2, Fastest)"
        self.cr = 2
        self.ac = 16
        self.maxHp = 28
        self.rechargeAbilities["Bone Dart"].rolls = 3
        self.rechargeAbilities["Bone Dart"].maxCharges = 8
        self.AddStats(14, 16, 14, 10, 10, 10)
        self.AddSaveProf(Stat.DEXTERITY)
        self.AddSaveProf(Stat.STRENGTH)
                
    def Act(self, others):
        for i in range(3): #Multiattack (3)
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                if not targets[0].HasCondition(ConditionConstant.POISONED) and self.rechargeAbilities["Poison Dart"].charges>0:
                    self.PoisonDart(targets[0])
                else:
                    self.BoneDart(targets[0])
