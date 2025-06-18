from random import randint as R
from Files.combatant import Combatant
from Files.Combatants.Players.fighter import Fighter1Archer
from Files.Combatants.Monsters.oldgrowthHunter import OldgrowthHunter1
runs = 100000

hunter = OldgrowthHunter1()
p1 = Fighter1Archer()
p2 = Fighter1Archer()

combatants = [hunter, p1, p2]
winningTeam = []
for sim in range(runs):
    for combatant in combatants:
        combatant.Reset()
        combatant.initRoll = R(1,20)+combatant.initiative

    turnOrder = sorted(combatants, key=lambda c: c.initRoll, reverse=True)

    done = False
    while not done:
        for combatant in turnOrder:
            if done:break
            if combatant.hp <= 0:
                pass
            for i in range(combatant.numberOfAttacks):
                targets = list(sorted(list(filter(lambda c: c.hp>0 and c.team != combatant.team, turnOrder)), key=lambda c: c.hp))
                if(len(targets)==0):
                    for c in turnOrder:
                        c.endingHP+=[c.hp]
                        #print(c)
                    winningTeam += [combatant.team]
                    done = True
                    break
                targets[0].hp -= combatant.Attack(targets[0])
            for func in combatant.cleanUp:
                func()
            
#for c in combatants:
#    print(c.name+" "+str(sum(c.endingHP)/len(c.endingHP)))
print("\n".join(team+" "+str(100*len(list(filter(lambda y: y==team, winningTeam)))/runs)+"%" for team in set(winningTeam)))
