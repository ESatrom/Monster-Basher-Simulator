from random import randint
from enum import Enum
import math

def R(numDice, step):
    """rolls <numDice>d<step>"""
    return sum(randint(1,step) for i in range(numDice))

class Combatant:
    """A combatant, be it a PC, monster, etc"""
    def __init__(self, name, ac, hp, cr, team, attacks):
        self.name = name
        self.ac = ac
        self.hp = hp
        self.maxHp = hp
        self.cr = cr
        def GetProf(self):return min(2,math.ceil(self.cr / 4)+1)
        self.team = name if team is None else team
        if len(attacks)==1: #If the creature has only 1 attack, set it as default
            self.attack = attacks[0]
        elif len(attacks)>1: #If it has more than one, log all of them
            self.attacks = {attack.name:attack for attack in attacks}
        self.endingHP = [] #Array of ending health values to generate average end-of-combat hp.
        self.cleanUp = [] #List of functions to execute at end of turn
        self.oldCleanUp = [] #List of functions to remove from cleanup
        self.poisoned = set() #List of sources of the poisoned condition
        self.paralyzed = set() #List of sources of the paralyzed condition (note, `Unconscious` is treated as paralyzed ("On Damage")
        self.effects = {}
        self.damageTriggers = []
        self.str = 10
        self.dex = 10
        self.con = 10
        self.int = 10
        self.wis = 10
        self.cha = 10
        self.saveProficiencies = []
        
    def __str__(self):
        return f"{self.name} ({self.hp}/{self.maxHp})"
    
    def Attack(self, target):
        """Performs a single attack against the provided target. Attempts to use the default attack which will fail for monsters with multiple options"""
        return self.AttackWith(target, self.attack)
    
    def AttackWith(self, target, attack):
        """Performs a single attack against the provided target using the provided attack option."""
        x = R(1,20)
        if len(self.poisoned)>0 and not len(target.paralyzed)>0: x = min(x,R(1,20))
        elif len(target.paralyzed)>0: x = max(x,R(1,20))
        if x==1:return 0 #fumble
        if x==20:return attack.Crit(target) #natural crit
        if attack.Modifier(x)>target.ac: #hit
            if target.paralyzed: #paralysis crit
                return attack.Crit(target)
            else: #normal damage
                return attack.Hit(target)
        return 0 #miss

    def Damage(self, amount):
        """Causes this combatant to take the specified amount of damage"""
        self.hp -= amount
        for trigger in self.damageTriggers:trigger(amount)
        try:self.paralyzed.remove("On Damage") #generally used for asleep creatures
        except:pass

    def CleanUp(self):
        """Performs all end-of-turn cleanup functions assigned to this combatant"""
        for func in self.cleanUp:
            func()
        for func in self.oldCleanUp:
            try:self.cleanUp.remove(func)
            except:pass
        self.oldCleanUp = []
    
    def Act(self, others):
        """How the combatant behaves on its turn"""
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            self.Attack(targets[0])

    def TakeTurn(self, others):
        """Don't override this, override Act"""
        if not self.paralyzed:
            self.Act(others)
        self.CleanUp()
        
    def AddRecharge(self, rechargeAbilities):
        self.rechargeAbilities = {recharge.name:recharge for recharge in rechargeAbilities}
        def RollRecharge():
            for ability in self.rechargeAbilities.values():
                for i in range(ability.rolls):
                    if ability.charges < ability.maxCharges:
                        if R(1,6)>=ability.DC:
                            ability.charges+=1
        if not RollRecharge in self.cleanUp:
            self.cleanUp+=[RollRecharge]

    def AddConcentration(self):
        self.concentration = False
        def concentrationCheck(amount):
            if R(1,20)+self.con<max(10,int(amount/2)):#con save
                if self.concentration:self.concentration()
        self.damageTriggers += [concentrationCheck]
        pass

    def AddStats(self, str, dex, con, int, wis, cha):
        self.str = str
        self.dex = dex
        self.con = con
        self.int = int
        self.wis = wis
        self.cha = cha

    def AddSaveProf(self, stat):
        self.saveProficiencies += [stat]

    def GetMod(self, stat):
        match stat:
            case Stat.STRENGTH:
                return (self.str-10)//2
            case Stat.CONSTITUTION:
                return (self.con-10)//2
            case Stat.DEXTERITY:
                return (self.dex-10)//2
            case Stat.INTELLIGENCE:
                return (self.int-10)//2
            case Stat.WISDOM:
                return (self.wis-10)//2
            case Stat.CHARISMA:
                return (self.cha-10)//2

    def Roll(self, stat, advantage=False, disadvantage=False):
        if advantage and not disadvantage:return max(R(1,20),R(1,20))+self.GetMod(stat)
        elif disadvantage:return min(R(1,20),R(1,20))+self.GetMod(stat)
        else:return R(1,20)+self.GetMod(stat)
    
    def RollSave(self, stat, advantage=False, disadvantage=False):
        return self.Roll(stat, advantage, disadvantage) + self.GetProf() * self.saveProficiencies.count(stat)

class Stat(Enum):
    STRENGTH = 1
    DEXTERITY = 2
    CONSTITUTION = 3
    INTELLIGENCE = 4
    WISDOM = 5
    CHARISMA = 6

class RechargeAbility:
    def __init__(self, name, charges, rolls, DC):
        self.name = name
        self.charges = charges
        self.maxCharges = charges
        self.rolls = rolls
        self.DC = DC

class Attack:
    def __init__(self, name, modifier, hit, crit):
        self.name = name
        self.Modifier = modifier
        self.Hit = hit
        self.Crit = crit

def MakeHit(DamageLambda):
    def Hit(target):
        dam = DamageLambda()
        target.Damage(dam)
        return dam
    return Hit
