from ....combatant import Combatant, Attack, MakeHit, R, Stat

class EvilMage(Combatant):
    def __init__(self, team):
        super().__init__("Evil Mage", 12, 22, 1, team, [Attack("Shocking Grasp", lambda r: r+5, MakeHit(lambda: R(1,8)), MakeHit(lambda: R(2,8))), Attack("Quarterstaff", lambda r: r+1, MakeHit(lambda: R(1,8)-1), MakeHit(lambda: R(2,8)-1))])
        self.AddConcentration()
        self.ones = 4
        self.twos = 3
        self.AddStats(9, 14, 11, 17, 12, 11)
        self.AddSaveProf(Stat.INTELLIGENCE)
        self.AddSaveProf(Stat.WISDOM)

    def MagicMissileDart(self, target):
        target.Damage(R(1,4)+1)

    def MagicMissile(self, darts, targets):
        missiles = darts
        for t in targets:
            if missiles > 0 and t.hp > 0:
                x = min(missiles, int(t.hp/3.5))
                missiles -= x
                for i in range(x):self.MagicMissileDart(t)
        for m in range(missiles):
            self.MagicMissileDart(targets[0])
            
    def HoldPerson(self, target):
        if R(1,20)+target.wis < 13: #Wis save
            target.paralyzed.add("Hold Person")
            def clean():
                if R(1,20)+1 >= 13:
                    try:target.paralyzed.remove("Hold Person")
                    except:pass
                    target.oldCleanUp += [clean]
                    self.concentration = False
            target.cleanUp += [clean]
            def clearConc():
                try:target.paralyzed.remove("Hold Person")
                except:pass
                try:target.cleanUp.remove(clean)
                except:pass
                self.concentration = False
            self.concentration = clearConc
    
    def Act(self, others):
        targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != self.team, others)), key=lambda c: c.hp))
        if len(targets)>0:
            if len(targets[0].paralyzed)<1 and self.twos > 0:
                if targets[0].hp <= int(3.5*3) and self.ones > 0:
                    self.ones -= 1
                    self.MagicMissile(3, targets)
                elif targets[0].hp <= int(3.5*4):
                    self.twos -= 1
                    self.MagicMissile(4, targets)
                else:
                    self.twos -= 1
                    self.HoldPerson(targets[0])
            else:
                if self.ones > 0:
                    self.ones -= 1
                    self.MagicMissile(3, targets)
                elif self.twos > 0:
                    self.twos -= 1
                    self.MagicMissile(4, targets)
                else:
                    self.AttackWith(targets[0], self.attacks["Shocking Grasp"])
