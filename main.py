import os
import zipfile

def zipDirectory(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')) )


# provide parameters as key-value pairs in dictionary 'parameters'
def applyParameters(parameters):

    # # (parameters) = (changed value) # (original value)

    # # barstow_engine_v8.jbeam
    # maxRPM = 6000 # 5000
    # engineInertia = 0.3 # 0.2
    # engineBrakeTorque = 60 # 50
    # engineNodeWeightMul = 1.2 # multiplier; original weights given by exact value but divided into three parts (29.5+3+3)
    # # barstow_brakes.jbeam
    # brakeMulF = 2200 # 2000
    # brakeMulR = 1000 # 950
    # #barstow_body.jbeam
    # bodyNodeWeightMul = 1.2
    # #common
    # wheelRadius = 0.4 # 0.325

    with open('./barstow/vehicles/barstow/barstow_engine_v8.jbeam', 'r') as f:
        t = f.readlines()
        t[45] = '        "maxRPM":{},\n'.format(parameters['maxRPM'])
        t[47] = '        "inertia":{},\n'.format(parameters['engineInertia'])
        t[49] = '        "engineBrakeTorque":{},\n'.format(parameters['engineBrakeTorque'])
        t[196] = "         {{\"nodeWeight\":{}}},\n".format(29.5*parameters['engineNodeWeightMul'])
        t[212] = '         ["em1r", -0.23, -1.3, 0.5, {{"nodeWeight":{}}}],\n'.format(3*parameters['engineNodeWeightMul'])
        t[213] = '         ["em1l", 0.23, -1.3, 0.5, {{"nodeWeight":{}}}],\n'.format(3*parameters['engineNodeWeightMul'])
    with open('./barstow/vehicles/barstow/barstow_engine_v8.jbeam', 'w') as f:
        for l in t: f.write(l)

    with open('./barstow/vehicles/barstow/barstow_brakes.jbeam', 'r') as f:
        t = f.readlines()
        t[26] = '        {{"brakeTorque":"$=$brakestrength*{}"}},\n'.format(parameters['brakeMulF'])
        t[65] = '        {{"brakeTorque":"$=$brakestrength*{}"}},\n'.format(parameters['brakeMulR'])
    with open('./barstow/vehicles/barstow/barstow_brakes.jbeam', 'w') as f:
        for l in t: f.write(l)

    with open('./barstow/vehicles/barstow/barstow_body.jbeam', 'r') as f:
        t = f.readlines()
        t[87] = '        {{"nodeWeight":{}}},\n'.format(1.78*parameters['bodyNodeWeightMul'])
        t[94] = '        {{"nodeWeight":{}}},\n'.format(3.56*parameters['bodyNodeWeightMul'])
        t[131] = '         {{"nodeWeight":{}}},\n'.format(4.9*parameters['bodyNodeWeightMul'])
        t[161] = '         {{"nodeWeight":{}}},\n'.format(5.5*parameters['bodyNodeWeightMul'])
        t[168] = '         {{"nodeWeight":{}}},\n'.format(4.0*parameters['bodyNodeWeightMul'])
        t[181] = '         {{"nodeWeight":{}}},\n'.format(4.0*parameters['bodyNodeWeightMul'])
        t[200] = '         {{"nodeWeight":{}}},\n'.format(3.56*parameters['bodyNodeWeightMul'])
        t[217] = '         {{"nodeWeight":{}}},\n'.format(2.1*parameters['bodyNodeWeightMul'])
        t[258] = '         {{"nodeWeight":{}}},\n'.format(2.3*parameters['bodyNodeWeightMul'])
        t[276] = '         {{"nodeWeight":{}}},\n'.format(1.9*parameters['bodyNodeWeightMul'])
        t[287] = '         {{"nodeWeight":{}}},\n'.format(1.4*parameters['bodyNodeWeightMul'])
        t[297] = '         {{"nodeWeight":{}}},\n'.format(2.3*parameters['bodyNodeWeightMul'])
        t[302] = '         ["r1", 0.0, -0.02, 1.34, {{"nodeWeight":{},"group":["gps","barstow_windshield","barstow_roof"]}}],\n'.format(1.6*parameters['bodyNodeWeightMul'])
        t[306] = '         ["r2", 0.0, 0.37, 1.35, {{"nodeWeight":{}}}],\n'.format(1.6*parameters['bodyNodeWeightMul'])
        t[310] = '         ["r3", 0.0, 0.75, 1.32, {{"nodeWeight":{}}}],\n'.format(1.6*parameters['bodyNodeWeightMul'])
        t[315] = '         ["r4", 0.0, 1.27, 1.24, {{"nodeWeight":{}}}],\n'.format(1.6*parameters['bodyNodeWeightMul'])
        t[319] = '         {{"nodeWeight":{}}},\n'.format(2.7*parameters['bodyNodeWeightMul'])
        t[326] = '         {{"nodeWeight":{}}},\n'.format(0.89*parameters['bodyNodeWeightMul'])
    with open('./barstow/vehicles/barstow/barstow_body.jbeam', 'w') as f:
        for l in t: f.write(l)

    with open('./common/vehicles/common/tires/tires_14/tires_14x6/tires_F_14x6_biasply.jbeam', 'r') as f:
        t = f.readlines()
        t[103] = '        {{"radius":{}}},\n'.format(parameters['wheelRadius'])
    with open('./common/vehicles/common/tires/tires_14/tires_14x6/tires_F_14x6_biasply.jbeam', 'w') as f:
        for l in t: f.write(l)

    with open('./common/vehicles/common/tires/tires_14/tires_14x6/tires_R_14x6_biasply.jbeam', 'r') as f:
        t = f.readlines()
        t[103] = '        {{"radius":{}}},\n'.format(parameters['wheelRadius'])
    with open('./common/vehicles/common/tires/tires_14/tires_14x6/tires_R_14x6_biasply.jbeam', 'w') as f:
        for l in t: f.write(l)


    ## Zip the results; now only for directory 'barstow'.
    # zipf = zipfile.ZipFile('barstow.zip', 'w', zipfile.ZIP_DEFLATED)
    # zipDirectory('barstow/', zipf)
    # zipf.close()
    # zipf = zipfile.ZipFile('common.zip', 'w', zipfile.ZIP_DEFLATED)
    # zipDirectory('common/', zipf)
    # zipf.close()







## Regular expression approach: failed..

# import json
# import re

# with open('./barstow/vehicles/barstow/barstow_engine_v8.jbeam') as f:
#     # j = json.loads(f.read())
#     t = f.read()
#     t = re.sub(r"(\d) +(\d)", r"\1, \2", t)
#     t = re.sub(r" *\/\/.*", "", t)
#     t = re.sub(r"\/\*[a-zA-Z0-9\[\]\", \n]*\*\/", "", t)
#     t = t.replace("true", "True")
#     t = t.replace("false", "False")
#     # print(t[0:10000])

#     j = eval(t)
#     print(j["barstow_engine_v8_291"])