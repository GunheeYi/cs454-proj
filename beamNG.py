
from config import BNG_HOME, BNG_USER
from beamngpy import BeamNGpy, Scenario, Vehicle, Road
from beamngpy.beamngcommon import set_up_simple_logging
from beamngpy.sensors import Damage
import math

def dist(tup1,tup2):
    ax=tup1[0]
    bx=tup2[0]
    '''ax,ay=tup1[0],tup1[1]
    bx,by=tup2[0],tup2[1]'''
    return abs(ax-bx)

def run(port, car_name, debug=False):
    if debug:
        set_up_simple_logging()
    result={}
    result['speed'] = 0.0
    result['intensity']=math.inf
    result['distance']=math.inf

    try:
        with BeamNGpy('localhost', port, home=BNG_HOME, user=BNG_USER) as bng:
            scenario = Scenario('tig', f'test_scenario')
            ground_level = -28.0
            road_nodes = [
                    (-100, 0, ground_level, 8),
                    (  0, 0, ground_level, 8),
                    (+100, 0, ground_level, 8)
                ]
            road = Road('tig_road_rubber_sticky', rid='straight_road')
            road.nodes.extend(road_nodes)
            scenario.add_road(road)
            direction_of_the_road = (0, 0, 1, -1)

            # Vehicle to move
            ego_position = (-40.0, -2.0, ground_level)
            ego_vehicle = Vehicle('ego', model=car_name, licence='ego', partConfig=f"vehicles/{car_name}/etk856tc_M.pc")
            damage=Damage()
            ego_vehicle.attach_sensor('damage', damage)
            scenario.add_vehicle(ego_vehicle, pos=ego_position, rot=None, rot_quat=direction_of_the_road)

            # Obstacle
            parked_car_position = (0.0, -2.0, ground_level)
            parked_vehicle = Vehicle('parked', model='etk800', licence='parked', color="red")
            scenario.add_vehicle(parked_vehicle, pos=parked_car_position, rot=None, rot_quat=direction_of_the_road)

            # Load all stuffs into BeamNG
            bng.set_steps_per_second(60)    #60 fps
            bng.set_deterministic()
            scenario.make(bng) 

            # Start scenario
            bng.load_scenario(scenario)
            bng.switch_vehicle(ego_vehicle) # Change camera
            bng.start_scenario()

            ## Throttle until obstacle is detected.
            ego_vehicle.control(throttle=0.8)
            no_problem = True
            for i in range(10000000):
                sensors = bng.poll_sensors(ego_vehicle)
                ego_pos = sensors['state']['pos']
                ego_vel = sensors['state']['vel'][0]
                if i==20 and ego_vel < 0.1:
                    no_problem = False
                    break

                if(((dist(ego_pos, parked_car_position)-5)/ego_vel**2) <= 0.055):
                    ## If brake not applied, they will collide. Start braking
                    break
            
            if no_problem:
                ego_vehicle.control(throttle=0,brake=1.0)
                past_speed = None
                while True:
                    sensors = bng.poll_sensors(ego_vehicle)
                    ego_pos = sensors['state']['pos']
                    ego_vel = sensors['state']['vel'][0]
                    ego_damage = sensors['damage']['damage'] 
                    if ego_damage > 0:
                        result['distance']=dist(ego_pos, parked_car_position)
                        result['speed'] = past_speed
                        result['intensity'] = ego_damage
                        break
                    
                    past_speed = ego_vel

                    if ego_vel <= 1e-10:
                        result['speed'] = 0
                        result['intensity'] = ego_damage
                        result['distance'] = dist(ego_pos, parked_car_position)
                        break
    except ConnectionResetError as e:
        if (debug):
            print(e)
    finally:
        if (debug):
            print(result)
        return result
        
# print(run())

if __name__ == "__main__":
    run(64256, 'car0', debug=True)