from ....combatant import Combatant, MakeHit, Attack, R

class Moorbounder(Combatant):
    def __init__(self, team):
        super().__init__("Moorbounder", 13, 30, 1, team, [Attack("Claws", lambda r: r+6, MakeHit(lambda: R(4,4)+4), MakeHit(lambda: R(8,4)+4))])
        self.AddStats(18, 14, 14, 2, 13, 5)
