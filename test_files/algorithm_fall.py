world = [
    [[1,1,False], [1,1,False], [1,1,False], [1,1,False], [1,1,False]],
    [[1,1,False], [1,1,False], [1,1,False], [1,1,False], [1,1,False]],
    [[1,1,False], [0,0,False], [1,1,False], [0,0,False], [1,1,False]],
    [[1,1,False], [0,0,False], [0,0,False], [0,0,False], [1,1,False]],
    [[1,1,False], [1,1,False], [1,1,False], [1,1,False], [1,1,False]]
]

strengh_factors = {0:0,
                   1:0.3,
                   2:0.5}

def world_print(world):
    for row in world:
        print(row)


def check_falling(world):
    world_width = len(world[0])
    for row in world[:-1]:
        for column in row:
            column[1] = 0
    for column in world[world_width - 1]:
        column[1] = 1
        column[2] = False
    for layer in range(len(world) - 1, 0, -1):
        column = 0
        for block in world[layer]:
            base_strength = block[0]
            if block[1] == 0:
                block[2] = True
            else:
                #check left
                factor = block[1]
                for i in range(3):
                    if column - i >= 0:
                        higher_block = world[layer - 1][column - i]
                        if higher_block[0] != 0:
                            higher_block[1] += factor
                            if higher_block[1] > 1:
                                higher_block[1] = 1
                            factor *= strengh_factors[higher_block[0]]
                        else:
                            break
                    else:
                        break
                #check right
                factor = block[1]
                for i in range(3):
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