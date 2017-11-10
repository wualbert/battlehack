import battlecode
import time
import random

#Start a game
game = battlecode.Game('lmaowtf')

start = time.clock()

#define helper functions here
def nearest_glass_state(state, entity):
    nearest_statue = None
    nearest_dist = 10000
    for other_entity in state.get_entities(entity_type=battlecode.Entity.STATUE):
        if(entity == other_entity):
            continue
        dist = entity.location.adjacent_distance_to(other_entity.location)
        if(dist< nearest_dist):
            dist = nearest_dist
            nearest_statue = other_entity

    return nearest_statue

    ###Modifications###

def getEntityMap(state):
    """

    :param state: a game state
    :return: 2d array of [map.width][map.height] that stores entity objects, ownCount, enemyCount
    """
    enemyCount = 0
    ownCount = 0
    entityMap = [[None]*state.map.height]*state.map.width
    for entity in state.get_entities():
        entityMap[entity.location.x][entity.location.y] = entity
        if entity.is_thrower:
            if entity.team == state.my_team:
                ownCount+=1
            else:
                enemyCount+=1
    return entityMap, ownCount, enemyCount

def enemyPickup(selfRobot,near_entities):
    """
    Enemies that can be picked up
    :param selfRobot: your robot
    :param near_entities: entities around you
    :return:list of enemies that can be picked up in ascending HP
    """
    nearEnemies = []
    for nearEntity in near_entities:
        if selfRobot.can_pickup(nearEntity):
            if  nearEntity.team == state.my_team_id:
                nearEnemies.append(nearEntity)
    #sort enemies by HP
    nearEnemies.sort(key = lambda x: x.hp)
    return nearEnemies

def buildStatue(selfRobot, state):
    #check if there are statues in the sector
    selfSector = state.map.sector_at(selfRobot.location)
    if selfSector.team != state.my_team:
        buildDirections = []
        for direction in battlecode.Direction.directions():
            if selfRobot.can_build(direction):
                buildDirections.append(direction)
        return buildDirections
    return None

def get_goal_sectors(state):
    """ faskf """
    all_sectors = []
    for x in range(0, state.map.width, 5):
        for y in range(0, state.map.height, 5):
            this_sector  = state.map.sector_at(battlecode.Location(x,y))
            if(not state.my_team.id == this_sector.team.id):
                all_sectors.append(this_sector)
    #all sectors has non allied sectors
    return all_sectors


def find_closest_goals(state,robot, all_sectors):
    """

    :param state:
    :param robot:
    :param all_sectors:
    :return: Location object
    """
    min_loc = (0,0)
    min_dist = 500000
    for s in all_sectors:
        if(robot.location.distance_to(battlecode.Location(s.top_left[0]+2, s.top_left[1]-2)) < min_dist):
            min_loc = (s.top_left[0]+2,s.top_left[1]-2)
            min_dist = robot.location.distance_to(battlecode.Location(s.top_left[0]+2, s.top_left[1]-2))
    return battlecode.Location(min_loc)



def enemies_within_hitting_range(S):
    '''
    For a Stack that can throw, checks if there is an enemy R or T that can be hit from the current position
    returns a list of lists of [entity that can be hit, direction] or None
    '''
    res = []
    for other_entity in S.entities_within_euclidean_distance(7):
        if other_entity.team.id != state.my_team.id and other_entity.team.id != 0:
            otherX = other_entity.location()[0]
            otherY = other_entity.location()[1]
            throwerX = S.location()[0]
            throwerY = S.location()[1]
            deltaX = otherX - throwerX
            deltaY = otherY - throwerY
            if abs(otherX) == abs(otherY):
                ent_list = []
                ent_list.append(other_entity)
                if deltaX > 0 and deltaY == 0:
                    ent_list.append(battlecode.Direction.EAST)
                if deltaX > 0 and deltaY > 0:
                    ent_list.append(battlecode.Direction.NORTH_EAST)
                if deltaX == 0 and deltaY > 0:
                    ent_list.append(battlecode.Direction.NORTH)
                if deltaX < 0 and deltaY > 0:
                    ent_list.append(battlecode.Direction.NORTH_WEST)
                if deltaX < 0 and deltaY == 0:
                    ent_list.append(battlecode.Direction.WEST)
                if deltaX < 0 and deltaY < 0:
                    ent_list.append(battlecode.Direction.SOUTH_WEST)
                if deltaX == 0 and deltaY < 0:
                    ent_list.append(battlecode.Direction.SOUTH)
                if deltaX > 0 and deltaY < 0:
                    ent_list.append(battlecode.Direction.SOUTH_EAST)
                res.append(ent_list)
    if res:
        return res
    return None


def hit_an_enemy(S):
    '''
    Stack throws a robot into an enemy (the first in the list for now)
    '''
    available_enemies = enemies_within_hitting_range(S)
    if available_enemies != None and S.can_act():
        S.queue_throw(available_enemies[0][1])


for state in game.turns():
    # Your Code will run within this loop
    starttime = time.time()

    #get entity map
    entityMap, ownCount, enemyCount = getEntityMap(state)

    all_goal_sectors = get_goal_sectors(state)


    for entity in state.get_entities(team=state.my_team): 
        # This line gets all the bots on your team
        subtime = time.time()
        if subtime - starttime > 0.90:
            break

        ###Modifications###
        #get adjacent entities
        my_location = entity.location
        near_entities = list(entity.entities_within_euclidean_distance(1.9))
        near_entities = list(filter(lambda x: x.can_be_picked, near_entities))
        enemiesInRange = enemyPickup(entity, near_entities)
        #pick up enemies
        if enemiesInRange:
            print('picking up')
            entity.queue_pickup(enemiesInRange[0])
            entity.hit_an_enemy()

        #check for building statues
        buildDirections = buildStatue(entity,state)
        if buildDirections:
            entity.queue_build(buildDirections[0])

        # call if need to move
        closestGoal = find_closest_goals(state, entity, all_goal_sectors)

        #check if already at goal
        if entity.location != closestGoal:
            movementDirection = entity.location.direction_to(closestGoal)
            #check if the direction is movable
            if entity.can_move(movementDirection):
                entity.queue_move(movementDirection)
            elif entity.can_move(movementDirection.rotate_counter_clockwise_degrees(90)):
                entity.queue_move(movementDirection.rotate_counter_clockwise_degrees(90))
            elif entity.can_move(movementDirection.rotate_counter_clockwise_degrees(270)):
                entity.queue_move(movementDirection.rotate_counter_clockwise_degrees(270))




        ###End###
        #
        # for pickup_entity in near_entities:
        #     assert entity.location.is_adjacent(pickup_entity.location)
        #     if entity.can_pickup(pickup_entity):
        #         entity.queue_pickup(pickup_entity)
        #
        # statue = nearest_glass_state(state, entity)
        # if(statue != None):
        #     direction = entity.location.direction_to(statue.location)
        #     if entity.can_throw(direction):
        #         entity.queue_throw(direction)
        #
        # for direction in battlecode.Direction.directions():
        #     if entity.can_move(direction):
        #         entity.queue_move(direction)
        # if subtime - starttime > 0.055:
        #     break

end = time.clock()
print('clock time: '+str(end - start))
print('per round: '+str((end - start) / 1000))
