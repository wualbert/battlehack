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

# def getEntityMap(state):
#     """
#
#     :param state: a game state
#     :return: 2d array of [map.width][map.height] that stores entity objects, ownRobotCount, enemyCount, enemyRobotList
#     """
#     enemyRobotCount = 0
#     ownRobotCount = 0
#     enemyRobotList = []
#     enemyStatueList =[]
#     entityMap = [[None]*state.map.height]*state.map.width
#     for entity in state.get_entities():
#         entityMap[entity.location.x][entity.location.y] = entity
#         if entity.is_thrower:
#             if entity.team.id == state.my_team.id:
#                 ownRobotCount+=1
#             else:
#                 enemyRobotCount+=1
#                 enemyRobotList.append(entity)
#         elif entity.is_statue:
#             if entity.team.id != state.my_team.id:
#                 enemyStatueList.append(entity)
#     print("ownteam", ownRobotCount,"enemy", enemyRobotCount)
#     return entityMap, ownRobotCount, enemyRobotCount, enemyRobotList, enemyStatueList

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
            if  nearEntity.team.id != state.my_team.id:
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



def enemies_within_hitting_range(S, state):

    '''
    For a Stack that can throw, checks if there is an enemy R or T that can be hit from the current position
    returns a list of lists of [entity that can be hit, direction] or None
    '''
    res = []
    for other_entity in S.entities_within_euclidean_distance(3):
        if other_entity.team.id != state.my_team.id and other_entity.team.id != 0:
#        if other_entity.team.id != state.my_team.id and other_entity.team.id != 0:
            otherX = other_entity.location.x
            otherY = other_entity.location.y
            throwerX = S.location.x
            throwerY = S.location.y
            deltaX = otherX - throwerX
            deltaY = otherY - throwerY
            if abs(otherX) == abs(otherY):
                ent_list = []
                ent_list.append(other_entity)
                ent_list.append(battlecode.Direction.from_delta(deltaX, deltaY))
                #
                # if deltaX > 0 and deltaY == 0:
                #     ent_list.append(battlecode.EAST)
                # if deltaX > 0 and deltaY > 0:
                #     ent_list.append(battlecode.NORTH_EAST)
                # if deltaX == 0 and deltaY > 0:
                #     ent_list.append(battlecode.NORTH)
                # if deltaX < 0 and deltaY > 0:
                #     ent_list.append(battlecode.NORTH_WEST)
                # if deltaX < 0 and deltaY == 0:
                #     ent_list.append(battlecode.WEST)
                # if deltaX < 0 and deltaY < 0:
                #     ent_list.append(battlecode.SOUTH_WEST)
                # if deltaX == 0 and deltaY < 0:
                #     ent_list.append(battlecode.SOUTH)
                # if deltaX > 0 and deltaY < 0:
                #     ent_list.append(battlecode.SOUTH_EAST)
                res.append(ent_list)
    if res:
        return res
    return None


def hit_an_enemy(S, state):
    '''
    Stack throws a robot into an enemy (the first in the list for now)
    '''
    available_enemies = enemies_within_hitting_range(S,state)
    if available_enemies:
        if S.can_throw(available_enemies[0][1]):
            S.queue_throw(available_enemies[0][1])

def building_spots(thrower, state):
    '''
    thrower: a robot
    state: current state of the game
    for a given thrower, analyzes a sector configuration and
    builds a new statue if:
    - A sector is neutral without enemy statue or is owned by enemy
    - Can build on one of the adjacent tiles

    returns: a list of possible building directions
    '''
    sector_dictionary = ownStatuesInSectors(state)
    current_location = thrower.location
    MiniMap = state.map
    current_sector = MiniMap.sector_at(current_location)
    sector_id = current_sector.team.id
    condition = True
    #
    # for entity in current_sector.entities_in_sector():
    #     if entity.type == 'statue':
    #         condition = False
            
    # neutral_without_statue = (sector_id ==0) and condition

    building_spots = []

    for possible_direction in battlecode.Direction.directions():
        building_location = current_location.adjacent_location_in_direction(possible_direction)
        building_sector = MiniMap.sector_at(building_location)
        building_sector_id = building_sector.team.id
        if building_sector_id != state.my_team.id and sector_dictionary[building_sector.top_left] and thrower.can_build(possible_direction):
            building_spots.append(possible_direction)

    return building_spots

def ownStatuesInSectors(state):
    sectorDict = dict()
    for entity in state.get_entities(entity_type = 'statue', team = state.my_team):
        sector = state.map.sector_at(entity.location).top_left
        if sector not in sectorDict:
            sectorDict[sector]=1
        else:
            sectorDict[sector]+=1
    return sectorDict


def build_a_tower(thrower, state):
    if building_spots(thrower, state):
        thrower.queue_build(building_spots[0])
        

def get_centroid(sector):
    """given a sector returns its centroid as a location"""
    tl = sector.top_left
    return battlecode.Location(tl[0] + 2, tl[1] - 2 )

def move(state, robot):
    """
    Moves a robot to a nearby goal sector that avoiding hedges
    """
    x = robot.location.x
    y = robot.location.y
    sector_to_move_to = state.map.sector_at(robot.location)
    H = state.map.height
    W = state.map.width
    for dx in [-5, 0 ,5]:
        for dy in [-5, 0, 5]:
            if(not (0 <= x +dx < W and 0<= y + dy <H)):
                continue
            point_to_check = battlecode.Location(x + dx, y+dy)
            that_sector = state.map.sector_at(point_to_check)
            if(that_sector.team.id == state.my_team_id):
                continue
            sector_to_move_to = that_sector
            center = get_centroid(sector_to_move_to)

            if(robot.location == center):
                return
            dir_to_move = robot.location.direction_to(center)
            if not robot.can_move(dir_to_move):
                continue
            robot.queue_move(dir_to_move)
            return

def aggresiveKill(state):
    enemyEntities = list(state.get_entities(entity_type='thrower',team=state.other_team))
    enemyEntities.extend(list(state.get_entities(entity_type='statue',team=state.other_team)))
    for enemyEntity in enemyEntities:
        enemyX = enemyEntity.location.x
        enemyY = enemyEntity.location.y
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx == 0 and dy == 0:
                    continue
                thrown = False
                for k in range(1,8):
                    if thrown:
                        break
                    checkLocation = battlecode.Location(enemyX+dx*k, enemyY+dy*k)
                    if state.map.location_on_map(checkLocation):
                        ownEntity = list(state.get_entities(location=checkLocation))
                        if not ownEntity:
                            continue
                        ownEntity = ownEntity[0]
                        pickupCandidates = ownEntity.entities_within_euclidean_distance(distance=1.9)
                        for pickup in pickupCandidates:
                            if ownEntity.can_pickup(pickup):
                                ownEntity.queue_pickup(pickup)
                                if ownEntity.can_throw(battlecode.Direction(-dx,-dy)):
                                    ownEntity.queue_throw(battlecode.Direction(-dx,-dy))
                                    thrown = True
                                    break
    return

def brawl(state):
    enemyStatues = list(state.get_entities(entity_type='statue', team=state.other_team))

    for enemyStatue in enemyStatues:
        enemyX = enemyStatue.location.x
        enemyY = enemyStatue.location.y
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx == 0 and dy == 0:
                    continue
                thrown = False
                for k in range(1,8):
                    if thrown:
                        break
                    checkLocation = battlecode.Location(enemyX+dx*k, enemyY+dy*k)
                    if state.map.location_on_map(checkLocation):
                        ownEntity = list(state.get_entities(location=checkLocation))
                        if not ownEntity:
                            continue
                        ownEntity = ownEntity[0]
                        pickupCandidates = ownEntity.entities_within_euclidean_distance(distance=1.9)
                        for pickup in pickupCandidates:
                            if ownEntity.can_pickup(pickup):
                                ownEntity.queue_pickup(pickup)
                                if ownEntity.can_throw(battlecode.Direction(-dx,-dy)):
                                    ownEntity.queue_throw(battlecode.Direction(-dx,-dy))
                                    thrown = True
                                    break

    enemyEntities = list(state.get_entities(entity_type='thrower',team=state.other_team))
    for enemyStatue in enemyEntities:
        candidates = enemyStatue.entities_within_euclidean_distance(1.9)
        for candidate in candidates:
            if candidate.is_thrower and candidate.team == state.my_team and not (candidate.is_holding and candidate.is_held):
                if candidate.can_pickup(enemyStatue):
                    candidate.queue_pickup(enemyStatue)
                    for direction in battlecode.Direction.all():
                        if candidate.can_throw(direction):
                            candidate.queue_throw(direction)
    return

def enemyCentroid(state):
    xSum = 0
    ySum = 0
    enemyEntities = state.get_entities(team=state.other_team)
    count = 0
    for enemyEntity in enemyEntities:
        xSum += enemyEntity.location.x
        ySum += enemyEntity.location.y
        count +=1
    return (xSum/count, ySum/count)

def targetWalk(entity, target):
    """

    :param entity:
    :param target: (x,y)
    :return:
    """
    currentX, currentY = entity.location.x,entity.location.y
    norm = ((target[0]-currentX)**2+(target[1]-currentY)**2)**0.5

    if norm == 0:
        return
    targetDirection = battlecode.Direction.from_delta((target[0]-currentX)/norm, (target[1]-currentY)/norm)


    if entity.can_move(targetDirection):
        entity.queue_move(targetDirection)
        moved = True
    #turn if blocked
    elif entity.can_move(targetDirection.rotate_counter_clockwise_degrees(45)):
        entity.queue_move(targetDirection.rotate_counter_clockwise_degrees(45))
        moved = True

    elif entity.can_move(targetDirection.rotate_counter_clockwise_degrees(315)):
        entity.queue_move(targetDirection.rotate_counter_clockwise_degrees(315))
        moved = True
    elif entity.can_move(targetDirection.rotate_counter_clockwise_degrees(90)):
        entity.queue_move(targetDirection.rotate_counter_clockwise_degrees(90))
        moved = True

    elif entity.can_move(targetDirection.rotate_counter_clockwise_degrees(270)):
        entity.queue_move(targetDirection.rotate_counter_clockwise_degrees(270))
        moved = True

for state in game.turns():
    # Your Code will run within this loop
    starttime = time.time()
    #get entity map
    brawling = False
    entityMap = state.get_entities()
    ownCount = len(list(state.get_entities(entity_type='thrower', team=state.my_team)))
    enemyCount = len(list(state.get_entities(entity_type='thrower', team=state.other_team)))
    if float(ownCount)/float(enemyCount+1) >= 3:
        brawl(state)
        brawling = True
    all_goal_sectors = get_goal_sectors(state)
    moveTarget = enemyCentroid(state)
    ownStatueInSectors = ownStatuesInSectors(state)
    for entity in state.get_entities(entity_type='thrower',team=state.my_team):
        moved = False
        # This line gets all the bots on your team
        entityStartTime = time.time()
        #get adjacent entities
        my_location = entity.location
        near_entities = list(entity.entities_within_euclidean_distance(1.9))
        near_entities = list(filter(lambda x: x.can_be_picked, near_entities))
        enemiesInRange = enemyPickup(entity, near_entities)
        #pick up enemies
        if enemiesInRange:
            entity.queue_pickup(enemiesInRange[0])
            hit_an_enemy(entity, state)


        if not brawling:
            #check for building statues
            buildDirections = building_spots(entity, state)
            if buildDirections:
                entity.queue_build(buildDirections[0])

        targetWalk(entity, moveTarget)
        #
        # # move(state,entity)
        # # call if need to move
        # closestGoal = find_closest_goals(state, entity, all_goal_sectors)
        #
        # #check if already at goal
        # if entity.location != closestGoal:
        #     movementDirection = entity.location.direction_to(closestGoal)
        #     #check if the direction is movable
        #     if entity.can_move(movementDirection):
        #         entity.queue_move(movementDirection)
        #         moved = True
        #     #turn if blocked
        #     elif entity.can_move(movementDirection.rotate_counter_clockwise_degrees(90)):
        #         entity.queue_move(movementDirection.rotate_counter_clockwise_degrees(90))
        #         moved = True
        #
        #     elif entity.can_move(movementDirection.rotate_counter_clockwise_degrees(270)):
        #         entity.queue_move(movementDirection.rotate_counter_clockwise_degrees(270))
        #         moved = True
        #
        # if not moved:
        #     x = random.randint(-1,1)
        #     y = random.randint(-1,1)
        #     if not (x == 0 and y == 0):
        #         direction = battlecode.Direction(x,y)
        #         if entity.can_move(direction):
        #             entity.queue_move(direction)

    endTime = time.time()
    print(endTime-starttime)
        # if time.time() - starttime + 2*entityTimeDiff > 0.1:
        #     print('terminating')
        #     break
end = time.clock()
print('clock time: '+str(end - start))
print('per round: '+str((end - start) / 1000))
