from ...combatant import Combatant, R, RechargeAbility, Attack, MakeHit, Stat

class OldgrowthShaman3(Combatant):
    def __init__(self, team):
        super().__init__("Oldgrowth Shaman (CR 3)", 15, 44, 3, team, [Attack("Bone Dart", lambda r: r+R(1,4)+4, MakeHit(lambda: R(1,4)+2), MakeHit(lambda: R(2,4)+2)), Attack("Black Bolt", lambda r: r+R(1,4)+5, MakeHit(lambda: R(4,6)), MakeHit(lambda: R(8,6))), Attack("Mark", lambda r: r+R(1,4)+5, MakeHit(lambda: R(1,4)), MakeHit(lambda: R(2,4)))])
        self.AddConcentration()
        self.AddRecharge([RechargeAbility("Poison Dart", 1, 1, 5)])
        self.drain = 1
        self.virulentMark = 2
        self.AddStats(12, 14, 13, 10, 10, 16)
        self.AddSaveProf(Stat.WISDOM)
        self.AddSaveProf(Stat.CHARISMA)
        
    def PoisonDart(self, target):
        if self.AttackWith(target, self.attacks["Bone Dart"])>0: #damage was dealt = we scored a hit
            if R(1,20)+target.con<12: #2 seems like a reasonable con save modifier
                target.poisoned.add("Oldgrowth Poison Dart")
                def ClearPoison():
                    try:target.poisoned.remove("Oldgrowth Poison Dart")
                    except:pass
                    target.oldCleanUp += [ClearPoison]
                target.cleanUp += [ClearPoison]
        self.rechargeAbilities["Poison Dart"].charges -= 1

    def Drain(self, target):
        self.drain -= 1
        if R(1,20)+target.wis < 13: #Wis save
            target.effects["exhaustion"] = 2
            def clean():
                target.effects["exhaustion"] += 2
                if target.effects["exhaustion"] >= 6:
                    target.hp = 0
                    del target.effects["exhaustion"]
                    self.concentration = False
                    target.oldCleanUp += [clean]
            target.cleanUp += [clean]
            def clearConc():
                try:del target.effects["exhaustion"]
                except:pass
                try:target.cleanUp.remove(clean)
                except:pass
                self.concentration = False
            self.concentration = clearConc
    
    def VirulentMark(self, target):
        self.virulentMark -= 1
        if self.AttackWith(target, self.attacks["Mark"]) > 0: #Hit, attempt inflict
            if R(1,20)+target.con <13: #DC 13 Con save
                target.poisoned.add("Virulent Mark")
        pass

    def Act(self, others):
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            ts = [t for t in targets if "exhaustion" in t.effects]
            avoidDrained = [t for t in targets if not ("exhaustion" in t.effects and t.effects["exhaustion"] > 0)]
            if len(avoidDrained)>0:targets = avoidDrained
            if self.drain > 0 and (targets[-1].hp > 3 * 14 or (targets[-1].hp > 14 and sum(t.hp for t in targets) > 3 * 14)):
                self.Drain(targets[-1])
            elif len(targets[-1].poisoned)<1 and targets[-1].hp > 14*2 and self.virulentMark>0:
                self.VirulentMark(targets[-1])
            else:
                self.AttackWith(targets[0], self.attacks["Black Bolt"])

