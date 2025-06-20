from ....combatant import Combatant, MakeHit, R, Attack

class Ettercap(Combatant):
    def __init__(self, team):
        super().__init__("Ettercap", 13, 44, 2, team, [Attack("Bite",lambda r: r+4, MakeHit(lambda: R(1,8)+R(1,8)+2), MakeHit(lambda: R(2,8)+R(2,8)+2)), Attack("Claws",lambda r: r+4, MakeHit(lambda: R(2,4)+2), MakeHit(lambda: R(4,4)+2))])
        self.AddSaves(2, 2, 1, -2, 1, -1)

    def Act(self, others):
        for atk in ["Claws", "Bite"]:
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                if atk == "Bite" and len(targets[0].poisoned) > 0 and len(t for t in targets if len(t.poisoned) == 0) and not targets[0].hp < 11:
                    target = list(filter(lambda t: len(t.poisoned)==0))[0]
                    dmg = self.AttackWith(target, self.attacks[atk]) #If a kill is unlikely, prioritize poisoning over takedown
                    if dmg > 0: #damage dealt, that's a hit, roll to poison
                        if R(1,20)+target.con < 11: #DC 11 con save
                            target.poisoned.add("Ettercap Bite")
                            def clean():
                                if R(1,20)+target.con >= 11: #DC 11 con save
                                    try:target.poisoned.remove("Ettercap Bite")
                                    except:pass
                                    target.oldCleanUp += [clean]
                            target.cleanUp += [clean]
                else:
                    self.AttackWith(targets[0], self.attacks[atk])