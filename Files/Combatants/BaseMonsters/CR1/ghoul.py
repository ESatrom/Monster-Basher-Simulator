from ....combatant import Combatant, Attack, MakeHit, R

class Ghoul(Combatant):
    def __init__(self, team):
        super().__init__("Ghoul", 12, 22, 2, team, [Attack("Bite", lambda r: r+2, MakeHit(lambda: R(2,6)+2), MakeHit(lambda: R(4,6)+2)), Attack("Claws", lambda r: r+4, MakeHit(lambda: R(2,4)+2), MakeHit(lambda: R(4,4)+2))])
        self.AddSaves(1, 2, 0, -2, 0, -2)
        
    def Act(self, others):
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            if len(targets[0].paralyzed)>0: #Bite Paralyzed targets (higher damage worth worse to hit if paralyzed, not otherwise)
                self.AttackWith(targets[0], self.attacks["Bite"])
            else: #Otherwise claw them up, inflict paralysis
                if self.AttackWith(targets[0], self.attacks["Claws"]) > 0: #on damage dealt (hit), inflict paralysis
                    if R(1,20)+targets[0].con < 10: #DC 10 con save
                        targets[0].paralyzed.add("Ghoul Fever")
                        def clean():
                            if R(1,20)+targets[0].con >= 10: #DC 10 con save
                                try:targets[0].paralyzed.remove("Ghoul Fever")
                                except:pass
                                targets[0].oldCleanUp += [clean]
                        targets[0].cleanUp += [clean]