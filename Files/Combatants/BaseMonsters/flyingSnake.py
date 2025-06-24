from ...combatant import Combatant, MakeHit, R, Attack

class FlyingSnake(Combatant):
    def __init__(self, team):
        super().__init__("Flying Snake", 14, 5, 1/8, team, [Attack("Bite",lambda r: r+6, MakeHit(lambda: 1+R(3,4)), MakeHit(lambda: 1+R(6,4)))])
        self.AddStats(4, 18, 11, 2, 12, 5)
