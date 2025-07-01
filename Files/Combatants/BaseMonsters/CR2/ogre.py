from ....combatant import *

class Ogre(Combatant):
    def __init__(self, team:str):
        super().__init__("Ogre", 11, 59, 2, team, [
            Attack("Greatclub", 6, MakeHit((2,8,4,DamageType.BLUDGEONING)))
            ,Attack("Javelin", 6, MakeHit((2,6,4,DamageType.PIERCING)))
        ])
        self.AddStats(19, 8, 16, 5, 7, 7)
        self.multiattack = ["Greatclub"] #Shrek has multiple options. Thankfully, if we're assuming everything is always in range, there's only one correct one
