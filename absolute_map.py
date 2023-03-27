import random

def set_absolute_map(map):
    # Set 3 Random Confundus Portals
    i = 0
    while (i < 3):
        confundus_row = random.randint(1,5)
        confundus_column = random.randint(1,4)
        
        # Find empty cell
        if (map[confundus_row][confundus_column][1][0] != '-'):
            map[confundus_row][confundus_column][1][0] = '-'
            map[confundus_row][confundus_column][1][1] = 'O'
            map[confundus_row][confundus_column][1][2] = '-'
            i = i + 1

    # Set 1 Random Wumpus
    i = 0
    while (i < 1):
        wumpus_row = random.randint(1,5)
        wumpus_column = random.randint(1,4)
        
        # Find empty cell
        if (map[wumpus_row][wumpus_column][1][0] != '-'):
            map[wumpus_row][wumpus_column][1][0] = '-'
            map[wumpus_row][wumpus_column][1][1] = 'W'
            map[wumpus_row][wumpus_column][1][2] = '-'
            i = i + 1

    # Set Random Coins
    i = 0
    while (i < 5):
        coin_row = random.randint(1,5)
        coin_column = random.randint(1,4)
        
        # Find empty cell
        if (map[coin_row][coin_column][1][0] != '-'):
            map[coin_row][coin_column][1][0] = '-'
            map[coin_row][coin_column][1][2] = '-'
            map[coin_row][coin_column][2][0] = '*'
            i = i + 1

    # Set Indications
    for i in range(1,6):
        for j in range(1,5):
            # Adjacent cells
            up_cell = map[i-1][j]
            down_cell = map[i+1][j]
            left_cell = map[i][j-1]
            right_cell = map[i][j+1]
            
            # Set stench indicators (Symbol 2)
            if (up_cell[1][1] == 'W' or down_cell[1][1] == 'W' or left_cell[1][1] == 'W' or right_cell[1][1] == 'W'):
                map[i][j][0][1] = '='
            
            # Set tingle indicators (Symbol 3)
            if (up_cell[1][1] == 'O' or down_cell[1][1] == 'O' or left_cell[1][1] == 'O' or right_cell[1][1] == 'O'):
                map[i][j][0][2] = 'T'

    return map

def insert_agent(map):
    i = 0
    while (i < 1):
        agent_row = random.randint(1,5)
        agent_column = random.randint(1,4)
        agent_direction = random.randint(1,4) # 1 = north, 2 = west, 3 = east, 4 = south

        if (map[agent_row][agent_column][1][0] != '-'):
            agent_abs_cell = map[agent_row][agent_column]

            if agent_direction == 1:
                agent_abs_cell[1][1] = '∧'
            elif agent_direction == 2:
                agent_abs_cell[1][1] = '<'
            elif agent_direction == 3:
                agent_abs_cell[1][1] = '>'
            else:
                agent_abs_cell[1][1] = '∨'

            agent_abs_cell[1][0] = '-'
            agent_abs_cell[1][2] = '-'

            i += 1
    
    return agent_abs_cell, agent_row, agent_column, agent_direction

    

    

    

    