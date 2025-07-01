from ....combatant import *

class Quickling(Combatant):
    def __init__(self, team:str):
        super().__init__("Quickling", 16, 10, 1, team, Attack("Dagger", 8, MakeHit((1,4,6,DamageType.PIERCING))))
        #Increased AC to simulate Blurred Movement.
        self.AddStats(4, 23, 13, 10, 12, 7)
        self.multiattack = ["Dagger","Dagger","Dagger"]
        
    def AttackedDisadvantage(self):
        result = super().AttackedDisadvantage()
        result |= self.GetSpeed() > 0
        return result
