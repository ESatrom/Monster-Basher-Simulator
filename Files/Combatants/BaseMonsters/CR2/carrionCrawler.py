from ....combatant import Combatant, MakeHit, R, Attack

class CarrionCrawler(Combatant):
    def __init__(self, team):
        super().__init__("Carrion Crawler", 13, 51, 2, team, [Attack("Bite",lambda r: r+4, MakeHit(lambda: R(2,4)+2), MakeHit(lambda: R(4,4)+2)), Attack("Tentacles",lambda r: r+8, MakeHit(lambda: R(1,4)+2), MakeHit(lambda: R(2,4)+2))])
        self.AddStats(14, 13, 16, 1, 12, 5)

    def Act(self, others):
        for atk in ["Tentacles", "Bite"]:
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                if atk == "Tentacles" and len(targets[0].paralyzed) > 0 and len(t for t in targets if len(t.paralyzed) == 0):
                    target = list(filter(lambda t: len(t.paralyzed)==0))[0]
                    dmg = self.AttackWith(target, self.attacks[atk]) #If a kill is unlikely, prioritize poisoning over takedown
                    if dmg > 0: #damage dealt, that's a hit, roll to poison
                        if R(1,20)+target.con < 13: #DC 13 con save
                            target.paralyzed.add("Carrion Crawler Tentacles")
                            def clean():
                                if R(1,20)+target.con >= 13: #DC 13 con save
                                    try:target.paralyzed.remove("Carrion Crawler Tentacles")
                                    except:pass
                                    target.oldCleanUp += [clean]
                            target.cleanUp += [clean]
                else:
                    self.AttackWith(targets[0], self.attacks[atk])