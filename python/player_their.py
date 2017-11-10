import battlecode
import time
import random

#Start a game
game = battlecode.Game('testplayer')

start = time.clock()
"""
def enemies_within_hitting_range(S):
    '''
    For a Stack that can throw, checks if there is an enemy R or T that can be hit from the current position
    returns a list of lists of [entity that can be hit, direction] or None
    '''
    res = []
    for other_entity in S.entities_within_euclidean_distance(7):
        if other_entity.team.id != state.my_team and other_entity.team.id != 0:
            otherX = other_entity.location()[0]
            otherY = other_entity.location()[1]
            if abs(otherX) == abs(otherY):
                ent_list = []
                ent_list.append(other_entity)
                if otherX > 0 and otherY = 0:
                    ent_list.append(Direction.EAST)
                if otherX > 0 and otherY > 0:
                    ent_list.append(Direction.SOUTH_EAST)
                if otherX = 0 and otherY > 0:
                    ent_list.append(Direction.SOUTH)
                if otherX < 0 and otherY > 0:
                    ent_list.append(Direction.SOUTH_WEST)
                if otherX < 0 and otherY = 0:
                    ent_list.append(Direction.WEST)
                if otherX < 0 and otherY < 0:
                    ent_list.append(Direction.NORTH_WEST)
                if otherX = 0 and otherY < 0:
                    ent_list.append(Direction.NORTH)
                if otherX > 0 and otherY < 0:
                    ent_list.append(Direction.NORTH_EAST)
                res.append(ent_list)
    if res != []
        return res
    return None

def hit_an_enemy(S):
    '''
    Stack throws a robot into an enemy (the first in the list for now)
    '''
    available_enemies = enemies_within_hitting_range(S)
    if available_enemies != None and S.can_act():
        S.queue_throw(available_enemies[0][1])
        
        
 """               
            
    
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

for state in game.turns():
    # Your Code will run within this loop
    for entity in state.get_entities(team=state.my_team): 
        if(state.turn % 100 == 0):
            for direction in battlecode.Direction.directions():
                if entity.can_build(direction):
                    entity.queue_build(direction)

        my_location = entity.location
        near_entites = entity.entities_within_euclidean_distance(1.9)
        near_entites = list(filter(lambda x: x.can_be_picked, near_entites))

        for pickup_entity in near_entites:
            assert entity.location.is_adjacent(pickup_entity.location)
            if entity.can_pickup(pickup_entity):
                entity.queue_pickup(pickup_entity)

        statue = nearest_glass_state(state, entity)
        if(statue != None):
            direction = entity.location.direction_to(statue.location)
            if entity.can_throw(direction):
                entity.queue_throw(direction)

        for direction in battlecode.Direction.directions():
            if entity.can_move(direction):
                entity.queue_move(direction)

end = time.clock()
print('clock time: '+str(end - start))
print('per round: '+str((end - start) / 1000))
