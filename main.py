from Files.combatant import R
from Files.Combatants.Players.fighter import *
from Files.Combatants.Monsters.all import *
from Files.Combatants.BaseMonsters.all import *



runs = 100000

sets = [    
    [FlyingSnake]
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
            combatant.initRoll = R(1,20)+combatant.initiative
        
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