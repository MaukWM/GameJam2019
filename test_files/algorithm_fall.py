world = [
    [[2,1,False], [1,1,False], [1,1,False], [1,1,False], [1,1,False]],
    [[2,1,False], [1,1,False], [1,1,False], [1,1,False], [1,1,False]],
    [[2,1,False], [0,0,False], [1,1,False], [0,0,False], [1,1,False]],
    [[2,1,False], [0,0,False], [0,0,False], [0,0,False], [1,1,False]],
    [[2,1,False], [1,1,False], [1,1,False], [1,1,False], [1,1,False]]
]

strengh_factors = {0:0,
                   1:0.1,
                   2:0.5}

def world_print(world):
    for row in world:
        print(row)


def check_falling(world):
    world_width = len(world[0])
    for row in world[:-1]:                          #zet alle sterktes naar 0 dat je opnieuw kan berekenen
        for column in row:
            column[1] = 0
    for column in world[world_width - 1]:           #behalve de onderste laag
        column[1] = 1
        column[2] = False
    for layer in range(len(world) - 1, 0, -1):      #ga de lagen langs van onder naar poven
        column = 0
        for block in world[layer]:
            if block[1] < 0.1:                       #deze 0.1 geeft aan wanneer iets breekt, TODO: veranderen in andere value
                block[1] = 0
                block[2] = True
            else:
                #check left
                factor = block[1]
                for i in range(3):                                      #2 blokjes aan de linkerkant updaten
                    if column - i >= 0:
                        higher_block = world[layer - 1][column - i]
                        if higher_block[0] != 0:                        #als die geen lucht is, ga dan door met de functie
                            higher_block[1] += factor
                            if higher_block[1] > 1:                     #max van kracht is 1
                                higher_block[1] = 1
                            factor *= strengh_factors[higher_block[0]]  #hoe verder je van de pillar ben, dan wordt het effect van de pillar minder
                        else:
                            break
                    else:
                        break
                #check right
                factor = block[1]
                for i in range(3):                                      #zelfde als links
                    if column + i < world_width:
                        higher_block = world[layer - 1][column + i]
                        if higher_block[0] != 0:
                            higher_block[1] += factor
                            if higher_block[1] > 1:
                                higher_block[1] = 1
                            factor *= strengh_factors[higher_block[0]]
                        else:
                            break
                    else:
                        break
            column += 1
    world_print(world)

check_falling(world)