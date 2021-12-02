
from config import BNG_HOME, BNG_USER
from beamngpy import BeamNGpy, Scenario, Vehicle, Road
from beamngpy.sensors import Electrics, Damage, State
import time
import json


def dist(tup1,tup2):
    ax,ay=tup1[0],tup1[1]
    bx,by=tup2[0],tup2[1]
    return ((ax-bx)**2+(ay-by)**2)**0.5
def run():
    
    with BeamNGpy('localhost', 64256, home=BNG_HOME, user=BNG_USER) as bng:
        scenario = Scenario('tig', 'test_scenario')
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
        ego_position = (-70.0, -2.0, ground_level)
        ego_vehicle = Vehicle('ego', model='barstow_forEdit', licence='ego', partConfig="vehicles/barstow_forEdit/291m.pc")
        

        electrics = Electrics()
        damage=Damage()
        # with open(f"{BNG_USER}\\0.23\\mods\\unpacked\\barstow_modified\\vehicles\\barstow_forEdit\\291m.pc", 'r') as json_file:
        #     ego_vehicle.set_part_config(json.load(json_file))
        
        ego_vehicle.attach_sensor('electrics', electrics)
        ego_vehicle.attach_sensor('damage', damage)
        # ego_vehicle.attach_sensor('electrics', electrics)
        # ego_vehicle.attach_sensor('damage', damage)
        scenario.add_vehicle(ego_vehicle, pos=ego_position, rot=None, rot_quat=direction_of_the_road)

        # Obstacle
        parked_car_position = (0.0, -2.0, ground_level)
        parked_vehicle = Vehicle('parked', model='etk800', licence='parked', color="red")
        scenario.add_vehicle(parked_vehicle, pos=parked_car_position, rot=None, rot_quat=direction_of_the_road)

        # Load all stuffs into BeamNG
    
        bng.set_steps_per_second(60)    #60 fps
        bng.set_deterministic()
        scenario.make(bng)
        bng.load_scenario(scenario)
        bng.switch_vehicle(ego_vehicle) # Change camera
        bng.start_scenario()
        result={}
        #while True:
            #print(scenario._get_vehicles_list())
            ## Throttle until obstacle is detected.
        ego_vehicle.control(throttle=0.8)
        while True:
            #time.sleep(.01)
            sensors = bng.poll_sensors(ego_vehicle)
            bng.poll_sensors(parked_vehicle)
            ego_vehicle.update_vehicle()
            parked_vehicle.update_vehicle()
            if(dist(ego_vehicle.state['pos'],parked_vehicle.state['pos'])<19):
                ## Obstacle is detected
                print("brake!")
                break
            #if i % 10 == 0:
            print(ego_vehicle.state['vel'])
                #print(sensors)
            
            if ego_vehicle.state['vel'][0] >= 13.9:
                ego_vehicle.control(throttle=0.07)
            elif ego_vehicle.state['vel'][0] >= 13.8:
                ego_vehicle.control(throttle=0.08)
            elif ego_vehicle.state['vel'][0] >= 13.6:
                ego_vehicle.control(throttle=0.082)
            elif ego_vehicle.state['vel'][0] >= 13.2:
                ego_vehicle.control(throttle=0.1)
            else:
                ego_vehicle.control(throttle=0.8)
            
        
        ## Input breaks
        ego_vehicle.control(throttle=0,brake=1.0)
        past_speed = None
        while True:
            #time.sleep(0.1)
            sensors = bng.poll_sensors(ego_vehicle)
            bng.poll_sensors(parked_vehicle)
            ego_vehicle.control(throttle=0, brake=1.0)
            ego_vehicle.update_vehicle()
            parked_vehicle.update_vehicle()

            if sensors['damage']['damage'] > 0:
                result['speed'] = past_speed
                result['intensity']=sensors['damage']['damage']
                result['distance']=dist(ego_vehicle.state['pos'],parked_vehicle.state['pos'])
                break
            past_speed = ego_vehicle.state['vel'][0]

            if ego_vehicle.state['vel'][0] <= 1e-10:
                result['speed'] = 0
                result['intensity']=sensors['damage']['damage']
                result['distance']=dist(ego_vehicle.state['pos'],parked_vehicle.state['pos'])
                break

        ## Record the intensity and final distance
        bng.stop_scenario()
        return result
            #bng.stop_scenario()
            #scenario.make(bng)
            
            # bng.stop_scenario()
            # # scenario.remove_vehicle(ego_vehicle)
            # # scenario.add_vehicle(ego_vehicle)
            # # bng.load_scenario(scenario)
            # new_scenario = scenario = Scenario('tig', 'test_scenario')
            # new_scenario.add_road(road)
            # ego_vehicle = Vehicle('ego', model='barstow_forEdit', licence='ego', color="white")
            # #ego_vehicle.attach_sensor('state', state)
            # ego_vehicle.attach_sensor('electrics', electrics)
            # ego_vehicle.attach_sensor('damage', damage)
            

            # new_scenario.add_vehicle(ego_vehicle, pos=ego_position, rot=None, rot_quat=direction_of_the_road)

            # new_scenario.add_vehicle(parked_vehicle, pos=parked_car_position, rot=None, rot_quat=direction_of_the_road)
            # new_scenario.make(bng)
            # bng.load_scenario(new_scenario)
            # bng.start_scenario()

            # scenario.restart()
            # bng.restart_scenario()
            # bng.switch_vehicle(ego_vehicle)

            

            #bng.load_scenario(scenario)
            
            
            
            #bng.despawn_vehicle(ego_vehicle)
            #ego_vehicle = Vehicle('ego', model='barstow_forEdit', licence='ego', color="black")
            #bng.spawn_vehicle(ego_vehicle, pos = ego_position, rot = None, rot_quat=direction_of_the_road)
        
run()
