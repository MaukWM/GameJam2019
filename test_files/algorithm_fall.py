from models.tiles.air_tile import Air

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
        for cell in row:
            cell.stability = 0
    for cell in world[world_width - 1]:           #behalve de onderste laag
        cell.stability = 1
        cell.should_fall = False
    for layer in range(len(world) - 1, 0, -1):      #ga de lagen langs van onder naar poven
        cell = 0
        for block in world[layer]:
            if block.stability < 0.1:                       #deze 0.1 geeft aan wanneer iets breekt, TODO: veranderen in andere value
                block.stability = 0
                block.should_fall = True
            else:
                #check left
                factor = block[1]
                for i in range(3):                                      #2 blokjes aan de linkerkant updaten
                    if cell - i >= 0:
                        higher_block = world[layer - 1][cell - i]
                        if not isinstance(higher_block, Air):                        #als die geen lucht is, ga dan door met de functie
                            higher_block.stability += factor
                            if higher_block.stability > 1:                     #max van kracht is 1
                                higher_block.stability = 1
                            factor *= higher_block.strength  #hoe verder je van de pillar ben, dan wordt het effect van de pillar minder
                        else:
                            break
                    else:
                        break
                #check right
                factor = block.stability
                for i in range(3):                                      #zelfde als links
                    if cell + i < world_width:
                        higher_block = world[layer - 1][cell + i]
                        if not isinstance(higher_block, Air):
                            higher_block.stability += factor
                            if higher_block.stability > 1:
                                higher_block.stability = 1
                            factor *= higher_block.strength
                        else:
                            break
                    else:
                        break
            cell += 1
    world_print(world)

check_falling(world)