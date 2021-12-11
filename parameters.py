from config import BNG_USER
import glob
import json

def applyParameters(parameters, car_name):
    DIR_CONFIG = f"{BNG_USER}/0.23/mods/unpacked/cs454_mod/vehicles/{car_name}"
    DIR_REF = "./etk800_sample"

    # Write weight first
    for file in glob.glob(f"{DIR_REF}/*.jbeam"):
        filename = file.split('\\')[-1]
        with open(file) as f:
            data = json.load(f)
        for key in data:
            if ('nodes' in data[key]):
                node = data[key]['nodes']
                for i, x in enumerate(node):
                    if isinstance(x, dict) and "nodeWeight" in x:
                        data[key]['nodes'][i]["nodeWeight"] *= parameters['nodeWeightMul']
                    elif isinstance(x,list):
                        for j, y in enumerate(x):
                            if (isinstance(y, dict) and "nodeWeight"in y):
                                data[key]['nodes'][i][j]["nodeWeight"] *= parameters['nodeWeightMul']
        with open(f"{DIR_CONFIG}/{filename}", 'w') as f:
            json.dump(data, f)
    
    with open(f"{DIR_CONFIG}/etk_engine_i6_3.0_petrol.jbeam") as f:
        data = json.load(f)
    data["etk_engine_i6"]["mainEngine"]["maxRPM"] = int(parameters['maxRPM'])   # 7000
    data["etk_engine_i6"]["mainEngine"]["inertia"] = parameters['engineInertia']    # 0.14
    data["etk_engine_i6"]["mainEngine"]["engineBrakeTorque"] = parameters['engineBrakeTorque'] #44
    with open(f"{DIR_CONFIG}/etk_engine_i6_3.0_petrol.jbeam", 'w') as f:
        json.dump(data, f)
    
    with open(f"{DIR_CONFIG}/etk800_brakes.jbeam") as f:
        data = json.load(f)
    data["etk800_brake_F"]["pressureWheels"][1]["brakeTorque"] = f"$=$brakestrength*{parameters['brakeMulF']}" # 3000
    data["etk800_brake_R"]["pressureWheels"][1]["brakeTorque"] = f"$=$brakestrength*{parameters['brakeMulR']}" # 1550
    with open(f"{DIR_CONFIG}/etk800_brakes.jbeam", 'w') as f:
        json.dump(data, f)

    with open(f"{DIR_CONFIG}/tires_R_18x9_sport.jbeam") as f:
        data = json.load(f)
    data["tire_R_245_40_18_sport"]["pressureWheels"][8]["radius"] = parameters['wheelRadius']   # 0.325
    with open(f"{DIR_CONFIG}/tires_R_18x9_sport.jbeam", 'w') as f:
        json.dump(data, f)
    
    with open(f"{DIR_CONFIG}/tires_F_18x9_sport.jbeam") as f:
        data = json.load(f)
    data["tire_F_245_40_18_sport"]["pressureWheels"][8]["radius"] = parameters['wheelRadius']   # 0.325
    with open(f"{DIR_CONFIG}/tires_F_18x9_sport.jbeam", 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    parameters = dict()
    parameters['maxRPM'] = 7000
    parameters['engineInertia'] = 0.14
    parameters['engineBrakeTorque'] = 44
    parameters['nodeWeightMul'] = 1
    parameters['brakeMulF'] = 3000
    parameters['brakeMulR'] = 1550
    parameters['wheelRadius'] = 0.325

    # confirm valid car name
    applyParameters(parameters, 'car0')