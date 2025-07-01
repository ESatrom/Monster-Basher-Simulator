from ....combatant import *

class Ogrillon(Combatant):
    def __init__(self, team:str):
        super().__init__("Half-Ogre (Ogrillon)", 12, 30, 1, team, [
            Attack("Battleaxe (1 hand)", 5, MakeHit((2,8,3,DamageType.SLASHING)))
            ,Attack("Battleaxe (2 hands)", 5, MakeHit((2,10,3,DamageType.SLASHING)))
            ,Attack("Javelin", 5, MakeHit((2,6,3,DamageType.PIERCING)))
        ])
        self.AddStats(17, 10, 14, 7, 9, 10)
        self.multiattack = ["Battleaxe (2 hands)"] #The ogrillon has multiple options. Thankfully, if we're assuming everything is always in range, there's only one correct one
