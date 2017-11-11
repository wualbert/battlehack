
################ BASIL ###################3

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
            point_to_check = battlecode.Location(x + dy, y+dy)
            that_sector = state.map.sector_at(point_to_check)
            if(that_sector.team.id == state.my_team_id):
                continue
            center = get_centroid(sector_to_move_to)


            ents = state.get_entities(location = battlecode.Location((x + dx/5, y+dy/5)))
            if(len(ents) > 0): #other ents in location to move?
                continue

            dir_to_move = robot.location.direction_to(center)
            robot.queue_move(dir_to_move)
            return



