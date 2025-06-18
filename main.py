from random import randint as R
from Files.Combatants.Players.fighter import Fighter1Archer, Fighter1Duelist, Fighter1Mauler, Fighter2Archer
from Files.Combatants.Monsters.oldgrowthHunter import OldgrowthHunter1
from Files.Combatants.BaseMonsters.ogrillon import Ogrillon
from Files.Combatants.BaseMonsters.moorbounder import Moorbounder
from Files.Combatants.BaseMonsters.animatedArmor import AnimatedArmor
runs = 100000

hunter = Moorbounder("Moorbounder")
p1 = OldgrowthHunter1("Oldgrowth")
#p2 = Fighter1Mauler()

combatants = [hunter, p1]
winningTeam = []
playerDown = 0
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
            combatant.TakeTurn(turnOrder)
            if len(set([c.team for c in turnOrder if c.hp > 0])) < 2:
                done = True
            
    
    winningTeam += [list(filter(lambda c: c.hp > 0,turnOrder))[0].team]
    if len(list(filter(lambda c: c.team=="Players" and c.hp <=0, turnOrder))):
        playerDown += 1
            
#for c in combatants:
#    print(c.name+" "+str(sum(c.endingHP)/len(c.endingHP)))
print("\n".join(sorted(team+" "+str(100*len(list(filter(lambda y: y==team, winningTeam)))/runs)+"%" for team in set(winningTeam))))
print(str(playerDown/runs*100)+"%")