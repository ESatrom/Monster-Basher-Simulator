from random import randint as R

class Combatant:
    def __init__(self, name, ac, hp, ModifierLambda, HitLambda, CritLambda, initiative, team, numberOfAttacks):
        self.name = name
        self.ac = ac
        self.hp = hp
        self.maxHp = hp
        self.modifier = ModifierLambda
        self.hit = HitLambda
        self.crit = CritLambda
        self.Attack = MakeAttackFunc(self.modifier, self.hit, self.crit)
        self.initiative = initiative
        self.numberOfAttacks = numberOfAttacks
        self.team = team
        self.initRoll = 0
        self.endingHP = []
        self.cleanUp = []
    def __str__(self):
        return f"{self.name} ({self.hp}/{self.maxHp})"
    def Reset(self):
        self.hp = self.maxHp

class RechargeCombatant(Combatant):
    def __init__(self, name, ac, hp, ModifierLambda, HitLambda, CritLambda, initiative, team, numberOfAttacks, rechargeCharges, rechargeRolls, rechargeDC):
        Combatant.__init__(self, name, ac, hp, ModifierLambda, HitLambda, CritLambda, initiative, team, numberOfAttacks)
        self.recharge = rechargeCharges
        self.rechargeCharges = rechargeCharges
        self.rechargeRolls = rechargeRolls
        self.rechargeDC = rechargeDC
        def RollRecharge():
            for i in range(self.rechargeRolls):
                if self.recharge < self.rechargeCharges:
                    if(R(1,6)>=self.rechargeDC):
                        self.recharge+=1
        self.cleanUp+=[RollRecharge]
    def Reset(self):
        Combatant.Reset(self)
        self.recharge = self.rechargeCharges

    
def MakeAttackFunc(ModifierLambda,Hit,Crit):
    def NewFunc(target):
        x = R(1,20)
        if x==1:return 0
        if x==20:return Crit(target)
        if ModifierLambda(x)>target.ac:return Hit(target)
        return 0
    return NewFunc

def MakeHit(DamageLambda):
    def Hit(target):
        dam = DamageLambda()
        target.hp -= dam
        return dam
    return Hit
