import empty_map
import absolute_map
import copy

# Prolog stuff
from pyswip import Prolog
 
prolog = Prolog()
prolog.consult('SJY-agent.pl')

def print_map(map):
    for i in range(0,len(map)):
        for j in map[i]:
            print(j[0], end="\t")
        print()
        for j in map[i]:
            print(j[1], end="\t")
        print()
        for j in map[i]:
            print(j[2], end="\t")

        print("\n")

empty_map = empty_map.create_empty_map()

abs_map_without_agent = absolute_map.set_absolute_map(empty_map)

map = copy.deepcopy(abs_map_without_agent)

# Insert agent
agent_abs_cell, agent_row, agent_column, agent_direction = absolute_map.insert_agent(map)

wall_cell = [['#','#','#'],
                ['#','#','#'],
                ['#','#','#']]

# Empty map of 2k+1 by 2k+1
def create_map(k):
    map_size = (2*k)+1
    map = []
    
    for i in range(0,map_size):
        map.append([])
        
        for j in range(0,map_size):
            map[i].append([
                ['.','.','.'],
                [' ','?',' '],
                ['.','.','.']
            ])
    
    return map

def agent_sense(agent_abs_cell):
    global bump_indicator
    global confounded_indicator
    global scream_indicator
    global agent_alive
    
    # If wumpus
    if agent_abs_cell[1][1] == 'W':
        agent_alive = False
    
    # Confounded, Stench, Tingle, Glitter, Bump, Scream.
    confounded = 'off'
    stench = 'off'
    tingle = 'off'
    glitter = 'off'
    bump = 'off'
    scream = 'off'

    confounded2 = 'C'
    stench2 = 'S'
    tingle2 = 'T'
    glitter2 = 'G'
    bump2 = 'B'
    scream2 = 'S'
    
    # If wall
    if agent_abs_cell[0][0] == '#':
        bump = 'on'
        bump2 = 'Bump'
        bump_indicator = True
    
    # If Confundus Portal
    if agent_abs_cell[1][1] == 'O':
        confounded = 'on'
        confounded2 = 'Confounded'
        confounded_indicator = True
    
    if (confounded_indicator):
        confounded = 'on'
        
    # If stench
    if agent_abs_cell[0][1] == '=':
        stench = 'on'
        stench2 = 'Stench'
    
    # If tingle
    if agent_abs_cell[0][2] == 'T':
        tingle = 'on'
        tingle2 = 'Tingle'
        
    # If glitter (Coin found)
    if agent_abs_cell[2][0] == '*':
        # Remove coin in absolute map
        agent_abs_cell[2][0] = '.'
        agent_abs_cell[1][0] = ' '
        agent_abs_cell[1][2] = ' '

        glitter = 'on'
        glitter2 = 'Glitter'

    if (scream_indicator):
        scream = 'on'
        scream2 = 'Scream'
        
    L = "[" + confounded + "," + stench + "," + tingle + "," + glitter + "," + bump + "," + scream + "]"

    print(f"{confounded2}-{stench2}-{tingle2}-{glitter2}-{bump2}-{scream2}")
        
    return L

def update_agent_abs_cell(action):
    global agent_row
    global agent_column
    global agent_direction
    global scream_indicator
    # 1 = north
    # 2 = west
    # 3 = east
    # 4 = south
    
    if (action == 'moveforward'):   
        if (agent_direction == 1):
            agent_row = agent_row - 1
            agent_column = agent_column 
        elif (agent_direction == 2):
            agent_row = agent_row
            agent_column = agent_column - 1
        elif (agent_direction == 3):
            agent_row = agent_row
            agent_column = agent_column + 1
        else:
            agent_row = agent_row + 1
            agent_column = agent_column
    elif (action == 'movebackward'):
        if (agent_direction == 1):
            agent_row = agent_row + 1
            agent_column = agent_column 
        elif (agent_direction == 2):
            agent_row = agent_row
            agent_column = agent_column + 1
        elif (agent_direction == 3):
            agent_row = agent_row
            agent_column = agent_column - 1
        else:
            agent_row = agent_row - 1
            agent_column = agent_column
    elif (action == 'turnleft'):
        if (agent_direction == 1):
            agent_direction = 2
        elif (agent_direction == 2):
            agent_direction = 4
        elif (agent_direction == 3):
            agent_direction = 1
        else:
            agent_direction = 3
    elif (action == 'turnright'):
        if (agent_direction == 1):
            agent_direction = 3
        elif (agent_direction == 2):
            agent_direction = 1
        elif (agent_direction == 3):
            agent_direction = 4
        else:
            agent_direction = 2
    elif (action == 'shoot'):
        if (agent_direction == 1):
            for i in range(1,agent_row):
                if (map[i][agent_column][1][1] == 'W'):
                    scream_indicator = True
                    remove_wumpus()
        elif (agent_direction == 2):
            for i in range(1,agent_column):
                if (map[agent_row][i][1][1] == 'W'):
                    scream_indicator = True
                    remove_wumpus()
        elif (agent_direction == 3):
            for i in range(agent_column+1,6):
                if (map[agent_row][i][1][1] == 'W'):
                    scream_indicator = True
                    remove_wumpus()
        else:
            for i in range(agent_row+1,6):
                if (map[i][agent_column][1][1] == 'W'):
                    scream_indicator = True
                    remove_wumpus()
            
    agent_abs_cell = map[agent_row][agent_column]
    
    return agent_abs_cell

# Update relative map using KB
def update_relative_map(k):
    global bump_indicator
    global confounded_indicator
    
    for X in range(-k,k+1):
        for Y in range(-k,k+1):
            X_Coord = -Y + k
            Y_Coord = X + k
            
            check_wall = bool(list(prolog.query("wall("+ str(X) +","+ str(Y) +")")))
            if (check_wall):
                relative_map[X_Coord][Y_Coord] = wall_cell
            
            check_stench = bool(list(prolog.query("stench("+ str(X) +","+ str(Y) +")")))
            if (check_stench):
                relative_map[X_Coord][Y_Coord][0][1] = '='
                
            check_wumpus = bool(list(prolog.query("wumpus("+ str(X) +","+ str(Y) +")")))
            if (check_wumpus):
                relative_map[X_Coord][Y_Coord][1][1] = 'W'

            check_tingle = bool(list(prolog.query("tingle("+ str(X) +","+ str(Y) +")")))
            if (check_tingle):
                relative_map[X_Coord][Y_Coord][0][2] = 'T'
                
            check_confundus = bool(list(prolog.query("confundus("+ str(X) +","+ str(Y) +")")))
            if (check_confundus):
                relative_map[X_Coord][Y_Coord][1][1] = 'O'
            
            if (check_wumpus and check_confundus):
                relative_map[X_Coord][Y_Coord][1][1] = 'U'
            
            check_glitter = bool(list(prolog.query("glitter("+ str(X) +","+ str(Y) +")")))
            if (check_glitter):
                relative_map[X_Coord][Y_Coord][2][0] = '*'
                
            check_safe = bool(list(prolog.query("safe("+ str(X) +","+ str(Y) +")")))
            check_visited = bool(list(prolog.query("visited("+ str(X) +","+ str(Y) +")")))
            if (check_safe == True and check_visited == False):
                relative_map[X_Coord][Y_Coord][1][1] = 's'
            if (check_safe == True and check_visited == True):
                relative_map[X_Coord][Y_Coord][1][1] = 'S'
                
            check_agent = bool(list(prolog.query("current("+ str(X) +","+ str(Y) +",Z)")))
            if (check_agent):
                # Get orientation
                agent_dir = list(prolog.query("current("+ str(X) +","+ str(Y) +",Orientation)"))[0]['Orientation']
                
                if agent_dir == 'rnorth':
                    relative_map[X_Coord][Y_Coord][1][1] = '∧'
                elif agent_dir == 'rwest':
                    relative_map[X_Coord][Y_Coord][1][1] = '<'
                elif agent_dir == 'reast':
                    relative_map[X_Coord][Y_Coord][1][1] = '>'
                else:
                    relative_map[X_Coord][Y_Coord][1][1] = '∨'
                    
                relative_map[X_Coord][Y_Coord][1][0] = '-'
                relative_map[X_Coord][Y_Coord][1][2] = '-'
                
                if (bump_indicator):
                    relative_map[X_Coord][Y_Coord][2][1] = 'B'
                else:
                    relative_map[X_Coord][Y_Coord][2][1] = '.'
                    
                if (confounded_indicator):
                    relative_map[X_Coord][Y_Coord][0][0] = '%'
                else:
                    relative_map[X_Coord][Y_Coord][0][0] = '.'
                
                if (scream_indicator):
                    relative_map[X_Coord][Y_Coord][2][2] = '@'
                else:
                    relative_map[X_Coord][Y_Coord][2][2] = '.'

def remove_wumpus():
    for i in range(1,6):
        for j in range(1,5):
            if (map[i][j][1][1] == 'W'):
                map[i][j][1][0] = ' '
                map[i][j][1][1] = '?'
                map[i][j][1][2] = ' '

            if (map[i][j][0][1] == '='):
                map[i][j][0][1] = '.'

# Initial k is 1, which means initial map will be 3x3
k = 1
relative_map = create_map(k)
bump_indicator = False
scream_indicator = False
confounded_indicator = True
agent_alive = True
coins_collected = 0
iteration = 0

# Print absolute map
print("====================================== Absolute Map ======================================\n")
print_map(map)

# First iteration
print(f"====================================== Iteration {iteration} ======================================\n")

# Get agent current relative position from prolog
agent_relative_pos = list(prolog.query("current(X,Y,Orientation)"))
print(f"Agent relative position is: ({agent_relative_pos[0]['X']},{agent_relative_pos[0]['Y']}), facing {agent_relative_pos[0]['Orientation']}.")

# Sense and update KB
L = agent_sense(agent_abs_cell)
list(prolog.query("reposition("+ L +")"))

# Update relative map according to KB
update_relative_map(k)

print_map(relative_map)

# Explore shenanigans 
explore_actions = list(prolog.query("explore(L)"))
print("Explore:", explore_actions)

while(True):
    if (bool(list(prolog.query("explore(L)")))):
        iteration += 1
        print(f"====================================== Iteration {iteration} ======================================\n")
        for next_action in explore_actions[0]['L']:
            if (next_action == 'moveforward'):
                print("Agent moves forward.")
                list(prolog.query("moveforward."))
            elif (next_action == 'turnleft'):
                print("Agent turns left.")
                list(prolog.query("turnleft."))
            elif (next_action == 'turnright'):
                print("Agent turns right.")
                list(prolog.query("turnright."))
            elif (next_action == 'pickup'):
                print("Agent picks up the coin.")
                list(prolog.query("pickup."))
                coins_collected += 1
            elif (next_action == 'shoot'):
                print("Agent attempts to shoot.")
                list(prolog.query("shoot."))

            confounded_indicator = False

            # Get absolute cell first
            agent_abs_cell = update_agent_abs_cell(next_action)

            # Sense this absolute cell, get L
            L = agent_sense(agent_abs_cell)

            if (agent_alive == False):
                print("The agent encountered the Wumpus, hence the game restarts.")
                map = copy.deepcopy(abs_map_without_agent)
                agent_abs_cell, agent_row, agent_column, agent_direction = absolute_map.insert_agent(map)

                # Print new map
                print("New absolute map")
                print_map(map)

                L = agent_sense(agent_abs_cell)
                list(prolog.query("reborn."))
                list(prolog.query("reposition("+ L +")"))

                iteration = 0
                k = 1

            if (bump_indicator):
                agent_abs_cell = update_agent_abs_cell('movebackward')

            # Query move(A,L)
            list(prolog.query("move("+ next_action +","+ L +")"))

            # Get agent current position from prolog
            agent_relative_pos = list(prolog.query("current(X,Y,Orientation)"))
            print(f"Agent relative position is: ({agent_relative_pos[0]['X']},{agent_relative_pos[0]['Y']}), facing {agent_relative_pos[0]['Orientation']}")

            if (confounded_indicator):
                map = copy.deepcopy(abs_map_without_agent)
                # Relocate agent to another safe location in map
                agent_abs_cell, agent_row, agent_column, agent_direction = absolute_map.insert_agent(map)
                # Print new map
                print("New absolute map")
                print_map(map)

                L = agent_sense(agent_abs_cell)
                list(prolog.query("reposition("+ L +")"))

                k = 1

            # Check if map needs to be expanded
            grid_x =  agent_relative_pos[0]['X'] + k
            grid_y = agent_relative_pos[0]['Y'] + k
            if (grid_x == 0 or grid_y == 0 or grid_x == 2*k or grid_y == 2*k):
                k = k + 1

            relative_map = create_map(k)

            # Update relative map according to KB
            update_relative_map(k)
            print_map(relative_map)
            
            bump_indicator = False
            scream_indicator = False

        explore_actions = list(prolog.query("explore(L)"))
        print("Explore:", explore_actions)

        print()
        print()
        print()
        print()
        print()
    else:
        print(f"Number of coins collected by agent: {coins_collected}")
        break