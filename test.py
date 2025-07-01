from Files.combatant import R
from Files.Combatants.Players.fighter import *
from Files.Combatants.Monsters.all import *
from Files.Combatants.BaseMonsters.all import *



runs = 100
# Populate sets with every single combatant in a single match-up. This can be run to ensure there are no errors in combatant code.
sets = [
    [FlyingSnake, Fighter1Duelist],
    [AnimatedArmor, Fighter1Duelist],
    [BrassDragonWyrmling, Fighter1Duelist],
    [BrownBear, Fighter1Duelist],
    [EvilMage, Fighter1Duelist],
    [Ghoul, Fighter1Duelist],
    [Moorbounder, Fighter1Duelist],
    [Ogrillon, Fighter1Duelist],
    [Quickling, Fighter1Duelist],
    [Allosaurus, Fighter1Duelist],
    [BlackDragonWyrmling, Fighter1Duelist],
    [CarrionCrawler, Fighter1Duelist],
    [Ettercap, Fighter1Duelist],
    [Gargoyle, Fighter1Duelist],
    [GiantBoar, Fighter1Duelist],
    [Ogre, Fighter1Duelist],
    [PolarBear, Fighter1Duelist],
    [SharkbodyAbomination, Fighter1Duelist],
    [SpinedDevil, Fighter1Duelist],
    [Ankylosaurus, Fighter1Duelist],
    [OldgrowthHunter1, Fighter1Duelist],
    [OldgrowthHunter2Slow, Fighter1Duelist],
    [OldgrowthHunter2Fast, Fighter1Duelist],
    [OldgrowthHunter2Fastest, Fighter1Duelist],
    [OldgrowthShaman3, Fighter1Duelist],
    [Fighter1Archer, Fighter1Duelist],
    [Fighter1Flow, Fighter1Duelist],
    [Fighter1Mauler, Fighter1Duelist],
    [Fighter2Archer, Fighter1Duelist],
    [Fighter2Duelist, Fighter1Duelist],
    [Fighter2Flow, Fighter1Duelist],
    [Fighter2Mauler, Fighter1Duelist],
    [Ettercap, OldgrowthHunter1],
    [CarrionCrawler, OldgrowthHunter1],
    [EvilMage, OldgrowthHunter1]
]

for s in sets:
    classes = []
    for team in s:
        if isinstance(team, list):
            if isinstance(team[0],str):
                for i in range(2,len(team)):
                    classes += [[team[i], team[1]]]
            else:
                for i in range(len(team)):
                    classes += [[team[i], None]]
        else:
            classes += [[team, None]]
            
    winningTeam = []
    playerDown = 0
    for sim in range(runs):
        combatants = [c[0](c[1]) for c in classes]
        for combatant in combatants:
            combatant.initRoll = R(1,20)+combatant.dex
        
        if sim==1:print(" VS ".join(', '.join(sorted(x.name for x in combatants if x.team == team)) for team in set(c.team for c in combatants)))

        turnOrder = sorted(combatants, key=lambda c: c.initRoll, reverse=True)

        done = False
        while not done:
            for combatant in turnOrder:
                if done:break
                if combatant.hp <= 0:continue
                combatant.TakeTurn(turnOrder)
                if len(set([c.team for c in turnOrder if c.hp > 0])) < 2:
                    done = True
                
        for c in combatants:c.endingHP+=[c.hp]
        try:winningTeam += [list(filter(lambda c: c.hp > 0,turnOrder))[0].team]
        except:winningTeam += ["pyrhic"]
        if len(list(filter(lambda c: c.team=="Players" and c.hp <=0, turnOrder))):
            playerDown += 1
                
    #for c in combatants:
    #    print(c.name+" "+str(sum(c.endingHP)/len(c.endingHP)))
    print("\n".join(sorted("\t"+team+" "+str(100*len(list(filter(lambda y: y==team, winningTeam)))/runs)+"%" for team in set(winningTeam))))
    if playerDown > 0:
        print("\tPlayer Downed: "+str(playerDown/runs*100)+"%")