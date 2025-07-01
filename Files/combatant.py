from __future__ import annotations
from random import randint
from enum import Enum
from typing import Dict, List, Callable, Any, Tuple
import math
__all__ = ["Combatant", "Attack", "MakeHit", "Stat", "DamageType", "ConditionConstant", "R", "RechargeAbility", "Damage"]

def R(numDice:int, step:int) -> int:
    """
    rolls <numDice>d<step>
    
    :param int numDice: The number of dice to be rolled
    :param int step: The number of faces on each die to be rolled
    :return int: value of the rolled dice
    """
    return sum(randint(1,step) for i in range(numDice))

class Combatant:
    """A combatant, be it a PC, monster, etc"""
    def __init__(self, name:str, ac:int, hp:int, cr:float, team:str, attacks:List[Attack]):
        """
        :param str name: The combatant's name
        :param int ac: The combatant's armor class
        :param int hp: The combatant's maximum hp
        :param float cr: The combatant's approximate Challenge Rating (monsters) or Level (Player Characters)
        :param team: Team the combatant should fight for. Defaults to the combatant's name if None
        :type team: str or None
        :param List[Attack] attacks: List of attack options for the combatant. If only one is listed, it's used as the default for Attack().
        """
        if not isinstance(attacks,List):attacks = [attacks]        
        self.name:str = name
        """The combatant's name"""
        self.ac:int = ac
        """The combatant's Armor Class"""
        self.hp:int = hp
        """The combatant's current amount of Hit Points"""
        self.maxHp:int = hp
        """The combatant's maximum amount of Hit Points"""
        self.cr:float = cr
        """The combatant's approximate Level (Player Characters) or Challenge Rating (monsters)"""
        self.team:str = name if team is None else team
        """The team the combatant should fight for."""
        self.attacks:Dict[str,Attack] = {attack.name:attack for attack in attacks}
        """Dict of the combatant's attacks, indexed by attack names"""
        if len(attacks)==1: #If the creature has only 1 attack, set it as default
            self.multiattack:Attack = [attacks[0].name]
            """The combatant's default attack pattern. A list of attack names in usage order"""
        self.endingHP:List[int] = []
        """Array of ending health values to generate average end-of-combat hp."""
        self.cleanUp:List[Callable] = []
        """List of functions to execute at end of turn"""
        self.oldCleanUp:List[Callable] = []
        """List of functions to remove from cleanup"""
        #self.effects = {}
        self.damageTriggers:List[Callable[[List[Damage]],Any]] = []
        """List of functions to execute upon damage taken, taking in the damage taken and not caring what they return"""
        self.oldDamageTriggers:List[Callable[[List[Damage]],Any]] = []
        """List of functions to remove from damage triggers"""
        self.str:int = 10
        """The combatant's Strength score (1-20 normal range, 1-30 legendary/heroic/extreme/whatever)"""
        self.dex:int = 10
        """The combatant's Dexterity score (1-20 normal range, 1-30 legendary/heroic/extreme/whatever)"""
        self.con:int = 10
        """The combatant's Constitution score (1-20 normal range, 1-30 legendary/heroic/extreme/whatever)"""
        self.int:int = 10
        """The combatant's Intelligence score (1-20 normal range, 1-30 legendary/heroic/extreme/whatever)"""
        self.wis:int = 10
        """The combatant's Wisdom score (1-20 normal range, 1-30 legendary/heroic/extreme/whatever)"""
        self.cha:int = 10
        """The combatant's Charisma score (1-20 normal range, 1-30 legendary/heroic/extreme/whatever)"""
        self.saveProficiencies:List[Stat] = []
        """List of stats with which this combatant has save proficiencies. Multiple listings grant multiple stacks of their proficiency bonus."""
        self.conditions:List[Condition] = []
        """List of conditions currently present on the combatant"""
        self.vulnerabilities:List[DamageType] = []
        """List of damage types from which to take double damage"""
        self.resistances:List[DamageType] = []
        """List of damage types from which to take half damage"""
        self.immunities:List[DamageType] = []
        """List of damage types from which to take no damage"""
        self.conditionImmunities:List[ConditionConstant] = []
        """List of condition types to ignore"""
        self.advantageSource:List[str] = []
        """sources of advantage"""
        self.disadvantageSource:List[str] = []
        """sources of disadvantage"""
        
    def GetProf(self) -> int:
        """:return int: The combatants proficiency bonus based on approximate CR/Level"""
        return min(2,math.ceil(self.cr / 4)+1)
    
    def __str__(self):
        """Prints as combatant name and current HP"""
        return f"{self.name} ({self.hp}/{self.maxHp})"
    
    def AttackWith(self, target:Combatant, attack:str|Attack) -> List[Damage]:
        """
        Makes one attack with the provided option against the provided target, returning damage dealt
        
        :param Combatant target: the victim of our attack
        :param str attack: Name of the attack to use
        :return List[Damage]: The damage dealt
        """
        if isinstance(attack,str):attack = self.attacks[attack]
        x:int = R(1,20)
        adv:bool = self.AttacksAdvantage() or target.AttackedAdvantage()
        dis:bool = self.AttacksDisadvantage() or target.AttackedDisadvantage()
        if dis and not adv: x = min(x,R(1,20))
        elif adv: x = max(x,R(1,20))
        if x==1:return [Damage(0)] #fumble
        if x==20:return attack.Crit(target) #natural crit
        if attack.Modifier(x)>target.ac: #hit
            if target.AttackedCrit(): #paralysis crit
                return attack.Crit(target)
            else: #normal damage
                return attack.Hit(target)
        return [Damage(0)] #miss

    def Damage(self, damage:List[Damage]|Damage):
        """
        Causes this combatant to take the specified damage
        
        :param List[Damage] damage: The damage to take
        """
        if not isinstance(damage,List):damage:List[Damage] = [damage]
        for i in range(len(damage)):
            if damage[i] in self.vulnerabilities:
                damage[i].Multiply(2)
            if damage[i] in self.resistances:
                damage[i].Multiply(1/2)
            if damage[i] in self.immunities:
                damage[i].Multiply(0)
        
        self.hp -= sum(d.finalAmount for d in damage)
        for trigger in self.damageTriggers:trigger(damage)
        for trigger in self.oldDamageTriggers:
            try:self.damageTriggers.remove(trigger)
            except:pass

    def CleanUp(self):
        """Performs all end-of-turn cleanup functions assigned to this combatant"""
        for func in self.cleanUp:
            func()
        for func in self.oldCleanUp:
            try:self.cleanUp.remove(func)
            except:pass
        self.oldCleanUp = []
    
    def Act(self, others:List[Combatant]):
        """
        How the combatant behaves on its turn
        
        :param List[Combatant] others: Other combatants in the fight, be they friend or foe
        """
        if not isinstance(others,List):others = [others]
        for atk in self.multiattack:
            targets:List[Combatant] = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                self.AttackWith(targets[0], atk)

    def TakeTurn(self, others:List[Combatant]):
        """
        Don't override this, override Act.
        
        Takes its turn, first getting up from prone if possible, then taking its actions unless incapacitated, then executing cleanup functions
        
        :param List[Combatant] others: Other combatants in the fight, be they friend or foe
        """
        if not isinstance(others,List):others = [others]
        if self.GetSpeed():
            self.RemoveCondition(ConditionConstant.PRONE)
        if not self.PassTurn():
            self.Act(others)
        self.CleanUp()
        
    def AddRecharge(self, rechargeAbilities:List[RechargeAbility]):
        """Gives the combatant one or more Recharge Abilities"""
        if not isinstance(rechargeAbilities,List):rechargeAbilities = [rechargeAbilities]
        self.rechargeAbilities:List[RechargeAbility] = {recharge.name:recharge for recharge in rechargeAbilities}
        """List of the combatant's recharge abilities"""
        def RollRecharge():
            """Function to attempt recharging all recharge abilities at cleanup"""
            for ability in self.rechargeAbilities.values():
                for i in range(ability.rolls):
                    if ability.charges < ability.maxCharges:
                        if R(1,6)>=ability.DC:
                            ability.charges+=1
        if not RollRecharge in self.cleanUp:
            self.cleanUp+=[RollRecharge]

    def AddConcentration(self):
        """Configures a creature to be able to maintain concentration"""
        self.concentration:Callable|False = False
        def concentrationCheck(damage:List[Damage]):
            amount = sum(d.finalAmount for d in damage)
            if R(1,20)+self.con<max(10,int(amount/2)):#con save
                if self.concentration:self.concentration()
        self.damageTriggers += [concentrationCheck]

    def AddStats(self, str:int, dex:int, con:int, int:int, wis:int, cha:int):
        """
        Sets a combatant's stats.
        
        :param int str: The combatant's Strength score
        :param int dex: The combatant's Dexterity score
        :param int con: The combatant's Constitution score
        :param int int: The combatant's Intelligence score
        :param int wis: The combatant's Wisdom score
        :param int cha: The combatant's Charisma score
        """
        self.str = str
        self.dex = dex
        self.con = con
        self.int = int
        self.wis = wis
        self.cha = cha

    def AddSaveProf(self, stat:Stat):
        """Gives the combatant proficiency (stackable) in the given stat"""
        self.saveProficiencies += [stat]

    def GetMod(self, stat:Stat) -> int:
        """Gets the combatant's modifier for a given stat (floor((stat-10)/2))"""
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

    def HasCondition(self, condition:ConditionConstant) -> bool|int:
        """
        :param ConditionConstant condition: condition to check for
        :return bool|int: Whether or not the condition is present, or the number of stacks present
        """
        if condition in self.conditionImmunities:return False
        return sum(c.stacks for c in self.conditions if c.condition == condition)

    def GiveCondition(self, condition:ConditionConstant, source:str|None=None, stacks:int|None=1):
        """
        :param ConditionConstant condition: condition to give
        :param str source: source of the condition (ie - "sleeping pills")
        """
        self.conditions += [Condition(condition, source, stacks)]

    def RemoveCondition(self, condition:ConditionConstant|None, source:str|None=None):
        """
        :param ConditionConstant condition: The condition to remove, or None to match all
        :param str source: The source of conditions to remove, or None to match all
        """
        self.conditions = [c for c in self.conditions if (c.condition == condition or condition is None) and (c.source == source or source is None)]
        
    def AttacksDisadvantage(self) -> bool:
        """Whether this combatant's attacks should be at disadvantage"""
        result = self.HasCondition(ConditionConstant.BLINDED) or self.HasCondition(ConditionConstant.FRIGHTENED) or self.HasCondition(ConditionConstant.POISONED) or self.HasCondition(ConditionConstant.PRONE) or self.HasCondition(ConditionConstant.RESTRAINED)
        result |= self.HasCondition(ConditionConstant.EXHAUSTION) >= 3
        result |= len(self.disadvantageSource)>0
        return result

    def AttacksAdvantage(self) -> bool:
        """Whether this combatant's attacks should be at advantage"""
        result = self.HasCondition(ConditionConstant.INVISIBLE)
        result |= len(self.advantageSource)>0
        return result
        
    def AttackedAdvantage(self) -> bool:
        """Whether attacks against this combatant should be at advantage"""
        result = self.HasCondition(ConditionConstant.BLINDED) or self.HasCondition(ConditionConstant.PRONE) or self.HasCondition(ConditionConstant.RESTRAINED) or self.HasCondition(ConditionConstant.PARALYZED) or self.HasCondition(ConditionConstant.PETRIFIED) or self.HasCondition(ConditionConstant.STUNNED) or self.HasCondition(ConditionConstant.UNCONSCIOUS)
        return result
    
    def AttackedCrit(self) -> bool:
        """Whether attacks against this combatant should auto-crit"""
        result = self.HasCondition(ConditionConstant.PARALYZED) or self.HasCondition(ConditionConstant.UNCONSCIOUS)
        return result

    def AttackedDisadvantage(self) -> bool:
        """Whether attacks against this combatant should be at disadvantage"""
        result = self.HasCondition(ConditionConstant.INVISIBLE)
        return result
    
    def PassTurn(self) -> bool:
        """Whether this combatant should pass its turn (has no actions available)"""
        result = self.HasCondition(ConditionConstant.INCAPACITATED) or self.HasCondition(ConditionConstant.PARALYZED) or self.HasCondition(ConditionConstant.PETRIFIED) or self.HasCondition(ConditionConstant.STUNNED) or self.HasCondition(ConditionConstant.UNCONSCIOUS)
        return result
        
    def Roll(self, stat:Stat, advantage:bool=False, disadvantage:bool=False) -> int:
        """Makes a roll with the given stat, optionally with advantage or disadvantage"""
        if advantage and not disadvantage:return max(R(1,20),R(1,20))+self.GetMod(stat)
        elif disadvantage:return min(R(1,20),R(1,20))+self.GetMod(stat)
        else:return R(1,20)+self.GetMod(stat)
    
    def RollSave(self, stat:Stat, advantage:bool=False, disadvantage:bool=False) -> int:
        """Makes a saving throw with the given stat, optionally with advantage or disadvantage"""
        return self.Roll(stat, advantage, disadvantage) + self.GetProf() * self.saveProficiencies.count(stat)
    
    def GetSpeed(self) -> int:
        """The current speed of the creature in feet, or 1 cuz I'm not actually dealing with mobility yet"""
        return 0 if self.HasCondition(ConditionConstant.GRAPPLED) or self.HasCondition(ConditionConstant.PARALYZED) or self.HasCondition(ConditionConstant.PETRIFIED) or self.HasCondition(ConditionConstant.RESTRAINED) or self.HasCondition(ConditionConstant.STUNNED) or self.HasCondition(ConditionConstant.UNCONSCIOUS) else 1

class Condition:
    def __init__(self, condition:ConditionConstant, source:str, stacks:int=1):
        """
        :param ConditionConstant condition: id of condition
        :param str source: source of this condition (ie "Sleep")
        :param int stacks: number of stacks of this condition
        """
        self.condition:ConditionConstant = condition
        """Id of this condition"""
        self.source:str = source
        """Source this condition came from"""
        self.stacks:int = stacks
        """Number of stacks of this condition - probably only used for exhaustion"""
    
class ConditionConstant(Enum):
    BLINDED = 1
    """Can't See | Attacks by disadvantage | Attacks against advantage"""
    CHARMED = 2
    """Can't harm charmer | Adv social checks by charmer"""
    DEAFENED = 3
    """Can't hear"""
    EXHAUSTION = 4
    """1: Disadvantage abilities | 2: Speed halved | 3: Disadvantage attacks & saves | 4: HP Max halved | 5: Speed = 0 | 6: Death"""
    FRIGHTENED = 5
    """Disadvantage Attacks & Abilities while source in LoS | Can't willingly move closer to source"""
    GRAPPLED = 6
    """Speed = 0"""
    INCAPACITATED = 7
    """Can't take actions/reactions/bonus actions"""
    INVISIBLE = 8
    """Invisible | Attacks by Advantage | Attacks against Disadvantage"""
    PARALYZED = 9
    """Incapacitated | Speed = 0 | Can't speak | Fails Str/Dex saves | Attacks against advantage | Attacks within 5ft crit"""
    PETRIFIED = 10
    """Stone | Incapacitated | Speed = 0 | Can't speak | Unaware | Attacks against advantage | Fails Str/Dex saves | Resistance all damage | Immune to new Poison and Disease, suspend current"""
    POISONED = 11
    """Disadvantage Attacks/Abilities"""
    PRONE = 12
    """Disadvantage Attacks | Attacks within 5ft advantage, others disadvantage"""
    RESTRAINED = 13
    """Speed = 0 | Attacks by disadvantage | Attacks against advantage | disadvantage Dex saves"""
    STUNNED = 14
    """Incapacitated | Speed = 0 | Speak falteringly | Fails Str/Dex saves | Attacks against advantage"""
    UNCONSCIOUS = 15
    """Incapacitated | Speed = 0 | Can't speak | Unaware | Prone | Fails Str/Dex saves | Attacks against advantage | Attacks within 5ft crit"""

class Stat(Enum):
    STRENGTH = 1
    DEXTERITY = 2
    CONSTITUTION = 3
    INTELLIGENCE = 4
    WISDOM = 5
    CHARISMA = 6

class RechargeAbility:
    def __init__(self, name:str, charges:int, rolls:int, DC:int):
        """
        :param str name: Name of ability
        :param int charges: Max charges of ability
        :param int rolls: Number of rolls to regain charges at the start of each turn
        :param int DC: Min d6 roll to regain a charge
        """
        self.name:str = name
        """Name of this ability"""
        self.charges:int = charges
        """Current number of charges for this abilit"""
        self.maxCharges:int = charges
        """Max number of charges for this ability"""
        self.rolls:int = rolls
        """Number of d6s to roll each turn to try regaining charges"""
        self.DC:int = DC
        """Min roll on a d6 to regain a charge"""

class Attack:
    def __init__(self, name:str, modifier:Callable[[int],int]|int, hit:Tuple[Callable[[Combatant],List[Damage]],Callable[[Combatant],List[Damage]]]):
        """
        :param str name: Name of the attack
        :param ((int)->int)|int modifier: Function taking a roll returning that roll plus modifier, or a flat modifier
        :param Tuple[(Combatant)->List[Damage],(Combatant)->List[Damage]] hit: A pair of functions each taking a combatant, then hitting (or critting for the second) the combatant, then returning damage dealt
        """
        self.name = name
        """Name of the attack"""
        self.modifier:Callable[[int],int]
        """Modifier lambda, give it your roll, it gives you roll plus mods"""
        if isinstance(modifier,int):
            self.modifier = lambda r: r+modifier 
        else:
            self.modifier = modifier
        self.hit:Callable[[Combatant],List[Damage]] = hit[0]
        """Function to call when making a normal hit (not crit) against another creature, returns damage dealt"""
        self.crit:Callable[[Combatant],List[Damage]] = hit[1]
        """Function to call when making a crit against another creature, returns damage dealt"""
        
    def Modifier(self, roll:int) -> int:
        """Modifier lambda, give it your roll, it gives you roll plus mods"""
        return self.modifier(roll)
    def Hit(self, target:Combatant) -> List[Damage]:
        """Function to call when making a normal hit (not crit) against another creature, returns damage dealt"""
        return self.hit(target)
    def Crit(self, target:Combatant) -> List[Damage]:
        """Function to call when making a crit against another creature, returns damage dealt"""
        return self.crit(target)

class DamageType(Enum):
    ACID = 1
    BLUDGEONING = 2
    COLD = 3
    FIRE = 4
    FORCE = 5
    LIGHTNING = 6
    NECROTIC = 7
    PIERCING = 8
    POISON = 9
    PSYCHIC = 10
    RADIANT = 11
    SLASHING = 12
    THUNDER = 13
    
class Damage:
    def __init__(self, amount:int, damageType:DamageType|None=None):
        """
        :param int amount: Amount of damage to be dealt before any reductions
        :param DamageType damageType: The type of damage to be dealt
        """
        if amount > 0 and damageType is None:raise Exception
        self.sourceAmount:int = amount
        """The initial amount of damage dealt, should not be modified"""
        self.finalAmount:int = amount
        """The final amount of damage taken, after all modifications (vulnerability, resistance, immunity, uncanny dodge, etc)"""
        self.damageType:DamageType = damageType
        """The type of this damage"""
    
    def Add(self, amount:int) -> int:
        """Adds the provided amount to and returns final amount"""
        self.finalAmount += amount
        return self.finalAmount
    
    def Multiply(self, amount:int) -> int:
        """Multiplies the provided amount to and returns final amount"""
        self.finalAmount *= amount
        self.finalAmount = int(self.finalAmount)
        return self.finalAmount
        

def MakeHit(damage:List[Tuple[int,int,int,DamageType]]) -> Tuple[Callable[[Combatant],List[Damage]],Callable[[Combatant],List[Damage]]]:
    """
    Makes a default hit function (Deal damage and return it, crits double dice not mods) for the provided damage lambda.
    
    :param List[Tuple[int,int,int,DamageType]] damage: A list of damage sources described as follows:
    :param int damageParam1: Number of dice to roll
    :param int damageParam2: Step of dice to roll, ignored if param1 is zero or None
    :param int damageParam3: Flat modifier, may be None
    :param DamageType damageParam4: The type of damage to be dealt
    """
    if not isinstance(damage,List):damage = [damage]
    damage = [
        [
            0 if d[0] is None or d[1] is None or d[1] == 0 else d[0],
            0 if d[1] is None else d[1],
            0 if d[2] is None else d[2],
            d[3]
        ]
        for d in damage]
    def Hit(target:Combatant) -> int:
        dam:List[Damage] = [Damage(R(d[0],d[1])+d[2], d[3]) for d in damage]
        target.Damage(dam)
        return dam
    def Crit(target:Combatant) -> int:
        dam:List[Damage] = [Damage(R(d[0]*2,d[1])+d[2], d[3]) for d in damage]
        target.Damage(dam)
        return dam
    return (Hit,Crit)
