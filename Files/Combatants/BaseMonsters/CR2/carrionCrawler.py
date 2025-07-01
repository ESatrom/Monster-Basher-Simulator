from ....combatant import *

class CarrionCrawler(Combatant):
    def __init__(self, team:str):
        super().__init__("Carrion Crawler", 13, 51, 2, team, [Attack("Bite", 4, MakeHit((2,4,2,DamageType.PIERCING))), Attack("Tentacles", 8, MakeHit((1,4,2,DamageType.POISON)))])
        self.AddStats(14, 13, 16, 1, 12, 5)

    def Act(self, others):
        for atk in ["Tentacles", "Bite"]:
            targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
            if len(targets)>0:
                if atk == "Tentacles" and targets[0].HasCondition(ConditionConstant.PARALYZED) and len(t for t in targets if not t.HasCondition(ConditionConstant.PARALYZED)):
                    target = list(filter(lambda t: not t.HasCondition(ConditionConstant.PARALYZED), targets))[0]
                    dmg = self.AttackWith(target, atk)[0] #If a kill is unlikely, prioritize poisoning over takedown
                    if dmg.sourceAmount > 0: #damage dealt, that's a hit, roll to poison
                        if target.RollSave(Stat.CONSTITUTION) < 13: #DC 13 con save
                            target.GiveCondition(ConditionConstant.PARALYZED, "Tentacles")
                            def clean():
                                if target.RollSave(Stat.CONSTITUTION) >= 13: #DC 13 con save
                                    target.RemoveCondition(ConditionConstant.PARALYZED, "Tentacles")
                                    target.oldCleanUp += [clean]
                            target.cleanUp += [clean]
                else:
                    self.AttackWith(targets[0], atk)