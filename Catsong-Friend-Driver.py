import random
from types import CellType
import numpy as np 
import copy


from pyswip import Prolog
prolog = Prolog()
prolog.consult('SJY-Agent.pl')
 

def generate_world():
    # Initializing walls
    r0c0 = r0c1 = r0c2 = r0c3 = r0c4 = r0c5 = r1c0 = r2c0 = r3c0 = r4c0 = r5c0 \
    = r6c0 = r6c1 = r6c2 = r6c3 = r6c4 = r6c5 = r5c5 = r4c5 = r3c5 = r2c5 = r1c5 = np.array([
        ['#','#','#'],
        ['#','#','#'],
        ['#','#','#']
    ])

    # Initializing cells
    r1c1 =  np.array([['.', '.', '.'],
                    [' ', '?', ' '],
                    ['.', '.', '.']])

    r1c2=r1c1.copy()
    r1c3=r1c1.copy()
    r1c4=r1c1.copy()
    r2c1=r1c1.copy()
    r2c2=r1c1.copy()
    r2c3=r1c1.copy()
    r2c4=r1c1.copy()
    r3c1=r1c1.copy()
    r3c2=r1c1.copy()
    r3c3=r1c1.copy()
    r3c4=r1c1.copy()
    r4c1=r1c1.copy()
    r4c2=r1c1.copy()
    r4c3=r1c1.copy()
    r4c4=r1c1.copy()
    r5c1=r1c1.copy()
    r5c2=r1c1.copy()
    r5c3=r1c1.copy()
    r5c4=r1c1.copy()


    wumpus_world = np.array([
    [r0c0,r0c1,r0c2,r0c3,r0c4,r0c5],
    [r1c0,r1c1,r1c2,r1c3,r1c4,r1c5],
    [r2c0,r2c1,r2c2,r2c3,r2c4,r2c5],
    [r3c0,r3c1,r3c2,r3c3,r3c4,r3c5],
    [r4c0,r4c1,r4c2,r4c3,r4c4,r4c5],
    [r5c0,r5c1,r5c2,r5c3,r5c4,r5c5],
    [r6c0,r6c1,r6c2,r6c3,r6c4,r6c5],
    ])


    #Spawn agent
    startY = random.randint(1,5)
    startX = random.randint(1,4)
    dir = random.randint(1,4)
    if(dir == 1):
        (wumpus_world[startY][startX])[1][1] = '^'
        dir = 'rnorth'
    elif(dir == 2):
        (wumpus_world[startY][startX])[1][1] = '>'
        dir = 'reast'
    elif(dir == 3):
        (wumpus_world[startY][startX])[1][1] = 'v'
        dir = 'rsouth'
    else:
        (wumpus_world[startY][startX])[1][1] = '<'
        dir = 'rwest'
    # (wumpus_world[startY][startX])[0][0] = '%'




    #Spawn 3 Confundus Portals
    for i in range(3):
        row = random.randint(1,5)
        col = random.randint(1,4)
        while((wumpus_world[row][col])[1][1]!='?'):
            row = random.randint(1,5)
            col = random.randint(1,4)
            
        (wumpus_world[row][col])[1][0] = (wumpus_world[row][col])[1][2] = '-'
        wumpus_world[row][col][1][1] = 'O'
        wumpus_world[row][col][0][0] = '%'
        #above portal
        if(row!=1):
            (wumpus_world[row-1][col])[0][2] = 'T'
        #below portal
        if(row!=5):
            (wumpus_world[row+1][col])[0][2] = 'T'
        #left of portal
        if(col!=1):
            (wumpus_world[row][col-1])[0][2] = 'T'
        #right of portal
        if(col!=4):
            (wumpus_world[row][col+1])[0][2] = 'T'


    #Spawn Wumpus 
    global wumpus_dead 
    wumpus_dead = False
    numwumpus = 1
    for i in range(numwumpus):
        row = random.randint(1,5)
        col = random.randint(1,4)
        while((wumpus_world[row][col])[1][1]!='?'):
            row = random.randint(1,5)
            col = random.randint(1,4)
        (wumpus_world[row][col])[1][0] = (wumpus_world[row][col])[1][2] = '-'
        (wumpus_world[row][col])[1][1] = 'W'

        #above wumpus
        if(row!=1):
            (wumpus_world[row-1][col])[0][1] = '='
        #below wumpus
        if(row!=5):
            (wumpus_world[row+1][col])[0][1] = '='
        #left of wumpus
        if(col!=1):
            (wumpus_world[row][col-1])[0][1] = '='
        #right of wumpus
        if(col!=4):
            (wumpus_world[row][col+1])[0][1] = '='

    #Spawn coin 
    numcoins = 3
    for i in range(numcoins):
        row = random.randint(1,5)
        col = random.randint(1,4)
        while((wumpus_world[row][col])[1][1]!='?'):
            row = random.randint(1,5)
            col = random.randint(1,4)
        (wumpus_world[row][col])[1][0] = (wumpus_world[row][col])[1][2] = '-'
        (wumpus_world[row][col])[2][0] = '*'



    return wumpus_world, dir, startY, startX

def pickUpCoin(curY, curX, wumpus_world,coinCount):
    if( wumpus_world[curY][curX][2][0] == '*'):
        wumpus_world[curY][curX][2][0] = '.'
        print("You picked up a coin!")
        coinCount+=1
    return wumpus_world,coinCount

    
def shoot(curY, curX, dir, wumpus_world):
    global wumpus_dead
    #check if agent has arrow
    if(bool(list(prolog.query("hasArrow")))):
        if (dir == 'rnorth'):
            for i in range(1,curY):
                if(wumpus_world[i][curX][1][1] == 'W'):
                    wumpus_dead = True
                    L[5] = "on" #Wumpus scream
                    L[1] = "off" #Stench gone
                    wumpus_world[i][curX][1][1] = '?'
                    wumpus_world[i][curX][1][0] = wumpus_world[i][curX][1][2] = ' '
                    #remove stench around wumpus (absolute map)
                    #above wumpus
                    if(i!=1):
                        (wumpus_world[i-1][curX])[0][1] = '.'
                    #below wumpus
                    if(i!=5):
                        (wumpus_world[i+1][curX])[0][1] = '.'
                    #left of wumpus
                    if(curX!=1):
                        (wumpus_world[i][curX-1])[0][1] = '.'
                    #right of wumpus
                    if(curX!=4):
                        (wumpus_world[i][curX+1])[0][1] = '.'

        elif (dir == 'rsouth'):
            for i in range(curY+1,6):
                if(wumpus_world[i][curX][1][1] == 'W'):
                    wumpus_dead = True
                    L[5] = "on" #Wumpus scream
                    L[1] = "off" #Stench gone
                    wumpus_world[i][curX][1][1] = '?'
                    wumpus_world[i][curX][1][0] = wumpus_world[i][curX][1][2] = ' '
                    #remove stench around wumpus (absolute map)
                    #above wumpus
                    if(i!=1):
                        (wumpus_world[i-1][curX])[0][1] = '.'
                    #below wumpus
                    if(i!=5):
                        (wumpus_world[i+1][curX])[0][1] = '.'
                    #left of wumpus
                    if(curX!=1):
                        (wumpus_world[i][curX-1])[0][1] = '.'
                    #right of wumpus
                    if(curX!=4):
                        (wumpus_world[i][curX+1])[0][1] = '.'

        elif (dir == 'reast'):
            for i in range(curX+1,5):
                if(wumpus_world[curY][i][1][1] == 'W'):
                    wumpus_dead = True
                    L[5] = "on" #Wumpus scream
                    L[1] = "off" #Stench gone
                    wumpus_world[curY][i][1][1] = '?'
                    wumpus_world[curY][i][1][0] = wumpus_world[curY][i][1][2] = ' '
                    #remove stench around wumpus (absolute map)
                    #above wumpus
                    if(curY!=1):
                        (wumpus_world[curY-1][i])[0][1] = '.'
                    #below wumpus
                    if(curY!=5):
                        (wumpus_world[curY+1][i])[0][1] = '.'
                    #left of wumpus
                    if(i!=1):
                        (wumpus_world[curY][i-1])[0][1] = '.'
                    #right of wumpus
                    if(i!=4):
                        (wumpus_world[curY][i+1])[0][1] = '.'
        #rwest
        else:
            for i in range(curX-1,0,-1):
                if(wumpus_world[curY][i][1][1] == 'W'):
                    wumpus_dead = True
                    L[5] = "on" #Wumpus scream
                    L[1] = "off" #Stench gone
                    wumpus_world[curY][i][1][1] = '?'
                    wumpus_world[curY][i][1][0] = wumpus_world[curY][i][1][2] = ' '
                    #remove stench around wumpus (absolute map)
                    #above wumpus
                    if(curY!=1):
                        (wumpus_world[curY-1][i])[0][1] = '.'
                    #below wumpus
                    if(curY!=5):
                        (wumpus_world[curY+1][i])[0][1] = '.'
                    #left of wumpus
                    if(i!=1):
                        (wumpus_world[curY][i-1])[0][1] = '.'
                    #right of wumpus
                    if(i!=4):
                        (wumpus_world[curY][i+1])[0][1] = '.'

        if(wumpus_dead):
            print("Wumpus is killed!")
        else: 
            print("Wumpus is still alive!")

    else:
        print("There are no more arrows!")

    return wumpus_world

def absMove(move,curY,curX,dir,offset,wumpus_world):
    reborn = False
    if(move == "moveforward"):
        if(dir == 'rnorth'):
            if(wumpus_world[curY-1][curX][1][1] != '#'):
                wumpus_world[curY][curX][1][1] = '?'
                curY -= 1
                if(wumpus_world[curY][curX][1][1] == 'O' or wumpus_world[curY][curX][0][0] == '%'):
                    tempX,tempY = curX, curY
                    wumpus_world,curY,curX,dir= confundus(curY,curX,wumpus_world)
                    offset = 1
                    return curY,curX,tempY,tempX,dir,offset,wumpus_world,reborn
                elif(wumpus_world[curY][curX][1][1] == 'W'):
                    list(prolog.query("reborn"))
                    wumpus_world, dir, startY, startX, offset,relmapE,L = start_game()
                    tempX,tempY = curX, curY
                    reborn = True
                    print("You have died\nGame has restarted!")
                    return startY,startX,tempY,tempX,dir,offset,wumpus_world,reborn
                    

                wumpus_world[curY][curX][1][1] = '^'
            else:
                tempY,tempX = curY,curX
                return (curY, curX,tempY-1,tempX,dir,offset,wumpus_world,reborn)
        elif(dir == 'rsouth'):
            if(wumpus_world[curY+1][curX][1][1] != '#'):
                wumpus_world[curY][curX][1][1] = '?'
                curY += 1
                if(wumpus_world[curY][curX][1][1] == 'O' or wumpus_world[curY][curX][0][0] == '%'):
                    tempX,tempY = curX, curY
                    wumpus_world,curY,curX,dir= confundus(curY,curX,wumpus_world)
                    offset = 1
                    return curY,curX,tempY,tempX,dir,offset,wumpus_world,reborn
                elif(wumpus_world[curY][curX][1][1] == 'W'):
                    list(prolog.query("reborn"))
                    wumpus_world, dir, startY, startX, offset,relmapE,L = start_game()
                    tempX,tempY = curX, curY
                    reborn = True
                    print("You have died\nGame has restarted!")
                    return startY,startX,tempY,tempX,dir,offset,wumpus_world,reborn

                wumpus_world[curY][curX][1][1] = 'v'
            else:
                tempY,tempX = curY,curX
                return (curY, curX,tempY+1,tempX,dir,offset,wumpus_world,reborn)
        elif(dir == 'reast'):
            if(wumpus_world[curY][curX+1][1][1] != '#'):
                wumpus_world[curY][curX][1][1] = '?'
                curX += 1
                if(wumpus_world[curY][curX][1][1] == 'O' or wumpus_world[curY][curX][0][0] == '%'):
                    tempX,tempY = curX, curY
                    wumpus_world,curY,curX,dir= confundus(curY,curX,wumpus_world)
                    offset = 1
                    return curY,curX,tempY,tempX,dir,offset,wumpus_world,reborn
                elif(wumpus_world[curY][curX][1][1] == 'W'):
                    list(prolog.query("reborn"))
                    wumpus_world, dir, startY, startX, offset,relmapE,L = start_game()
                    tempX,tempY = curX, curY
                    reborn = True
                    print("You have died\nGame has restarted!")
                    return startY,startX,tempY,tempX,dir,offset,wumpus_world,reborn
                wumpus_world[curY][curX][1][1] = '>'
            else:
                tempY,tempX = curY,curX
                return (curY, curX,tempY,tempX+1,dir,offset,wumpus_world,reborn)
        elif(dir == 'rwest'):
            if(wumpus_world[curY][curX-1][1][1] != '#'):
                wumpus_world[curY][curX][1][1] = '?'
                curX -= 1
                if(wumpus_world[curY][curX][1][1] == 'O' or wumpus_world[curY][curX][0][0] == '%'):
                    tempX,tempY = curX, curY
                    wumpus_world,curY,curX,dir= confundus(curY,curX,wumpus_world)
                    # wumpus_world[curY][curX][1][1] = '<'
                    offset = 1
                    return curY,curX,tempY,tempX,dir,offset,wumpus_world,reborn
                elif(wumpus_world[curY][curX][1][1] == 'W'):
                    list(prolog.query("reborn"))
                    wumpus_world, dir, startY, startX, offset,relmapE ,L= start_game()
                    tempX,tempY = curX, curY
                    reborn = True
                    print("You have died\nGame has restarted!")

                    return startY,startX,tempY,tempX,dir,offset,wumpus_world,reborn

                wumpus_world[curY][curX][1][1] = '<'
            else:
                tempY,tempX = curY,curX
                return (curY, curX,tempY,tempX-1,dir,offset,wumpus_world,reborn)
    elif(move == "turnleft"):
        if(dir == 'rnorth'):
            dir = 'rwest'
            wumpus_world[curY][curX][1][1] = '<'
        elif(dir == 'rsouth'):
            dir = 'reast'
            wumpus_world[curY][curX][1][1] = '>'
        elif(dir == 'reast'):
            dir = 'rnorth'
            wumpus_world[curY][curX][1][1] = '^'
        elif(dir == 'rwest'):
            dir = 'rsouth'
            wumpus_world[curY][curX][1][1] = 'v'
    elif(move == "turnright"):
        if(dir == 'rnorth'):
            dir = 'reast'
            wumpus_world[curY][curX][1][1] = '>'
        elif(dir == 'rsouth'):
            dir = 'rwest'
            wumpus_world[curY][curX][1][1] = '<'
        elif(dir == 'reast'):
            dir = 'rsouth'
            wumpus_world[curY][curX][1][1] = 'v'
        elif(dir == 'rwest'):
            dir = 'rnorth'
            wumpus_world[curY][curX][1][1] = '^'        
    tempY,tempX = curY,curX
    return(curY,curX,tempY,tempX,dir,offset,wumpus_world,reborn)

def confundus(startY,startX,wumpus_world):
    row = random.randint(1,5)
    col = random.randint(1,4)
    while((wumpus_world[row][col])[1][1]!='?'):
        row = random.randint(1,5)
        col = random.randint(1,4)

    wumpus_world[startY][startX][1][1]='O'
    startY = row
    startX = col

    (wumpus_world[row][col])[1][0] = (wumpus_world[row][col])[1][2] = '-'
    dir = random.randint(1,4)
    if(dir == 1):
        (wumpus_world[startY][startX])[1][1] = '^'
        dir = "rnorth"
    elif(dir == 2):
        (wumpus_world[startY][startX])[1][1] = '>'
        dir = "reast"
    elif(dir == 3):
        (wumpus_world[startY][startX])[1][1] = 'v'
        dir = "rsouth"
    else:
        (wumpus_world[startY][startX])[1][1] = '<'
        dir = "rwest"
    return wumpus_world,startY,startX,dir

def relativemap_expand(offset):
    a0b0 =  np.array([['.', '.', '.'],
                [' ', '?', ' '],
                ['.', '.', '.']])
    row = (2*offset) + 1
    col = (2*offset) + 1
    arr = []
    farr = []
    for i in range(row):
        arr1 = copy.deepcopy(arr)
        farr.append(arr1)
        for j in range(col):
            grid = copy.deepcopy(a0b0)
            farr[i].append(grid)
    return farr

def population(map, confunded):
    length = len(map)
    for i in range(length):
        for j in range(length):
            initial = len(map)//2 ##relative_position(0,0) 5x5 -> initial = 2
            offset = initial ## initial = 2
            y = i
            x = j
            p = str((y - offset)*-1)
            q = str(x- offset)
            if(bool(list(prolog.query("stench("+q+","+p+")")))):
                map[y][x][0][1] = "="
                # print("Coordinates of stench is", y,x )

            if(bool(list(prolog.query("tingle("+q+","+p+")")))):
                map[y][x][0][2] = "T"
                # print("Coordinates of tingle is", y,x )
            if(bool(list(prolog.query("glitter("+q+","+p+")")))):
                map[y][x][2][0] = "*"
            if(bool(list(prolog.query("wumpus("+q+","+p+")")))):
                # print("Coordinates of wumpus is", y,x )
                map[y][x][1][1] = "W"
                map[y][x][1][0] = map[y][x][1][2] = "-"
            if(bool(list(prolog.query("confundus("+q+","+p+")")))):
                # print("Coordinates of confundus is", y,x )
                if(map[y][x][1][1] == "W"):
                    map[y][x][1][1] = "U"
                else:
                    map[y][x][1][1] = "O"
                map[y][x][1][0] = map[y][x][1][2] = "-"
            if(bool(list(prolog.query("wall("+q+","+p+")")))):
                for a in range(3):
                    for b in range(3):
                        map[y][x][a][b] = "#"
            if(bool(list(prolog.query("safe("+q+","+p+")")))):
                if(bool(list(prolog.query("visited("+q+","+p+")")))):
                    map[y][x][1][1] = "S"
                else:
                    map[y][x][1][1] = "s"

            if(bool(list(prolog.query("current("+q+","+p+",rnorth)")))):
                # print("Prolog position is at ",q,p)
                # print("Python position is at ",i,j)
                map[y][x][1][1] = "^"
                map[y][x][1][0] = map[y][x][1][2] = "-"
                if(confunded):
                    map[y][x][0][0] = "%"
            elif(bool(list(prolog.query("current("+q+","+p+",rsouth)")))):
                map[y][x][1][1] = "v"
                map[y][x][1][0] = map[y][x][1][2] = "-"
                if(confunded):
                    map[y][x][0][0] = "%"
            elif(bool(list(prolog.query("current("+q+","+p+",reast)")))):
                map[y][x][1][1] = ">"
                map[y][x][1][0] = map[y][x][1][2] = "-"
                if(confunded):
                    map[y][x][0][0] = "%"
            elif(bool(list(prolog.query("current("+q+","+p+",rwest)")))):
                map[y][x][1][1] = "<"
                map[y][x][1][0] = map[y][x][1][2] = "-"
                if(confunded):
                    map[y][x][0][0] = "%"
    return map


def print_map(map):
    for i in range(0,len(map)):
        for j in map[i]:
            print("  ".join(j[0]), end = '    ')
        print()
        for j in map[i]:
            print("  ".join(j[1]), end = '    ')
        print()
        for j in map[i]:
            print("  ".join(j[2]), end = '    ')
        print("\n")

def check_edge(map,y,x):
    offset = len(map)//2 + 1
    edgeMax = len(map) - offset
    edgeMin = -edgeMax
    if(y == edgeMax or y == edgeMin or x == edgeMax or x == edgeMin):
        return True
    else:
        return False
    
def start_sense(startY,startX,wumpus_world):
    L = ["on"]
    if(wumpus_world[startY][startX][0][1] == "="):
        L.append("on")
    else:
        L.append("off")
    if(wumpus_world[startY][startX][0][2] == "T"):
        L.append("on")
    else:
        L.append("off")
    for i in range(3):
        L.append("off")
    return L

def input_sense(y,x,wumpus_world,confunded):
    # print(y,x,"abspos in input sense")
    if(confunded):
        L = ["on"]
    else:
        L = []
        if(wumpus_world[y][x][0][0] == "%"): #Confunded
            L.append("on")
        else:
            L.append("off")
    if(wumpus_world[y][x][0][1] == "="): #Stench indicator  
        L.append("on")
    else:
        L.append("off")
    if(wumpus_world[y][x][0][2] == "T"): #Tingle indicator
        L.append("on")  
    else:
        L.append("off")
    if(wumpus_world[y][x][2][0] == "*"): #Glitter indicator
        L.append("on")
    else:
        L.append("off")
    if(wumpus_world[y][x][2][1] == "#"): #Bump indicator 
        L.append("on")
    else:
        L.append("off")
    L.append("off") 
    return L

def print_full_senses(L):
    if(L[0] == "on"): #Counfounded indicator
        print("Confounded -", end = ' ')
    else:
        print("C -", end = ' ')

    if(L[1] == "on"): #Stench indicator
        print("Stench -", end = ' ')
    else:
        print("St -", end = ' ')

    if(L[2] == "on"): #Tingle indicator
        print("Tingle -", end = ' ')
    else:
        print("T -", end = ' ')

    if(L[3] == "on"): #Glitter indicator
        print("Glitter -", end = ' ')
    else:
        print("G -", end = ' ')

    if(L[4] == "on"): #Bump indicator
        print("Bump -", end = ' ')
    else:
        print("B -", end = ' ')

    if(L[5] == "on"): #Scream indicator
        print("Scream", end = ' ')
    else:
        print("Sc", end = ' ')
    
    print("")

def start_game():
    wumpus_world, dir, startY, startX = generate_world()
    L = start_sense(startY,startX,wumpus_world)
    offset = 1
    list(prolog.query("reposition("+str(L)+")"))
    relmap = relativemap_expand(offset)
    relmapE = population(relmap, True)
    print("================================================================\n")
    a = "ABSOLUTE MAP";
    print(a.rjust(37, ' '))
    print("================================================================\n")

    print_map(wumpus_world)
    print("================================================================\n")
    a = "RELATIVE MAP";
    print(a.rjust(37, ' '))
    print("================================================================\n")

    print_map(relmapE)
    # q = list(prolog.query("safe(X,Y)"))
    # print("Safe is", q)
    return wumpus_world, dir, startY, startX, offset,relmapE,L
# senses L[confounded, stench, tingle, glitter, bump, scream]

print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
a = "Welcome to Wumpus World";
print(a.rjust(95, ' '))
print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
print("Rules of Wumpus World:")
print("If there are no more safe and unvisited grids to visit, end the game.")
print("Game will end back at spawn point")
wumpus_world, dir, startY, startX, offset,relmapE,L = start_game()
print_full_senses(L)
action = ""
pos = ""
confunded = False
count = 0
coinCount = 0
while(True):
    count +=1
    print("Iteration: ",count)
    L = ["off","off","off","off","off","off"]
    q = list(prolog.query("explore(L)"))

    if(q[0]['L'] == []):
        if(count==1):
            print("Spawned with no safe grids to traverse to. Please run program again")
        else:
            # print("Number of coins collected : ",coinCount)
            print("Visited all possible safe grids")
            print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
            a = "End of Wumpus World";
            print(a.rjust(95, ' '))
            print("///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
        break

    else:
        g=q[0]["L"]
        print("List of actions to take: ",g)
        for z in g:
            action = z
            print("Executing: ",action)

            startY,startX,tempY,tempX,dir,offset,wumpus_world,reborn = absMove(action,startY,startX,dir,offset,wumpus_world)
            
            # print(startY,startX)
            if(reborn):
                continue
            if(action == "moveforward"):
                list(prolog.query("moveforward"))
                pos = list(prolog.query("current(X,Y,Z)"))
                y = pos[0]["Y"]
                x = pos[0]["X"]                
                L = input_sense(tempY,tempX,wumpus_world,confunded)
                # print(L,"before confund")
                # q = list(prolog.query("confundus(X,Y)"))
                # print("Portal is", q)
                list(prolog.query("move(moveforward,"+str(L)+")"))
                if(L[0] == "on"):
                    confunded = True
                    L = input_sense(startY,startX,wumpus_world,confunded)
                    # print(L,"after confund")
                    list(prolog.query("reposition("+str(L)+")"))
                confunded = False
                pos = list(prolog.query("current(X,Y,Z)"))
                y = pos[0]["Y"]
                x = pos[0]["X"]
                # print(x,y,"relpos")
                check = check_edge(relmapE,y,x)
                # print(check,"checkedge")
                if(check == True):
                    offset+=1
            elif(action == "pickup"):
                L = input_sense(tempY,tempX,wumpus_world,confunded)
                list(prolog.query("move(pickup,"+str(L)+")"))
                wumpus_world,coinCount = pickUpCoin(startY, startX, wumpus_world,coinCount)
                print(wumpus_world[startY][startX][2][0])
            elif(action == "turnleft"):
                L = input_sense(tempY,tempX,wumpus_world,confunded)
                list(prolog.query("turnleft"))
                pos = list(prolog.query("current(X,Y,Z)"))
            elif(action == "turnright"):
                L = input_sense(tempY,tempX,wumpus_world,confunded)
                list(prolog.query("turnright"))
                pos = list(prolog.query("current(X,Y,Z)"))
            elif(action == "s"):
                L = input_sense(tempY,tempX,wumpus_world,confunded)
                wumpus_world = shoot(startY, startX, dir, wumpus_world)
                list(prolog.query("move(shoot,"+str(L)+")"))


        relmap = relativemap_expand(offset)
        relmapE = population(relmap, False)
        print("================================================================\n")
        a = "ABSOLUTE MAP";
        print(a.rjust(37, ' '))
        print("================================================================\n")

        print_map(wumpus_world)
        print("================================================================\n")
        a = "RELATIVE MAP";
        print(a.rjust(37, ' '))
        print("================================================================\n")

        print_map(relmapE)
        print_full_senses(L)
 