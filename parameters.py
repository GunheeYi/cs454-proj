DIR_VEHICLES = "."
NAME_VEHICLE = "barstow"
DIR_CONFIG = DIR_VEHICLES + "/" + NAME_VEHICLE + "/vehicles/" + NAME_VEHICLE + "/"

def applyParameters(parameters):

    # parameters = {
    #     'maxRPM': 6000,
    #     'engineInertia': 0.3,
    #     'engineBrakeTorque': 60,
    #     'engineNodeWeightMul': 1.2,
    #     'brakeMulF': 2200,
    #     'brakeMulR': 1000,
    #     'bodyNodeWeightMul': 1.2,
    #     'wheelRadius': 0.4
    # }

    JBEAM_ENGINE = DIR_CONFIG+'barstow_engine_v8.jbeam'
    JBEAM_BRAKES = DIR_CONFIG+'barstow_brakes_.jbeam'
    JBEAM_BODY = DIR_CONFIG+'barstow_body.jbeam'
    JBEAM_FTIRE = DIR_CONFIG+'tires_F_14x6_biasply.jbeam'
    JBEAM_RTIRE = DIR_CONFIG+'tires_R_14x6_biasply.jbeam'

    with open(JBEAM_ENGINE, 'r') as f:
        t = f.readlines()
        t[45] = '        "maxRPM":{},\n'.format(parameters['maxRPM'])
        t[47] = '        "inertia":{},\n'.format(parameters['engineInertia'])
        t[49] = '        "engineBrakeTorque":{},\n'.format(parameters['engineBrakeTorque'])
        t[196] = "         {{\"nodeWeight\":{}}},\n".format(29.5*parameters['engineNodeWeightMul'])
        t[212] = '         ["em1r", -0.23, -1.3, 0.5, {{"nodeWeight":{}}}],\n'.format(3*parameters['engineNodeWeightMul'])
        t[213] = '         ["em1l", 0.23, -1.3, 0.5, {{"nodeWeight":{}}}],\n'.format(3*parameters['engineNodeWeightMul'])
    with open(JBEAM_ENGINE, 'w') as f:
        for l in t: f.write(l)

    with open(JBEAM_BRAKES, 'r') as f:
        t = f.readlines()
        t[26] = '        {{"brakeTorque":"$=$brakestrength*{}"}},\n'.format(parameters['brakeMulF'])
        t[65] = '        {{"brakeTorque":"$=$brakestrength*{}"}},\n'.format(parameters['brakeMulR'])
    with open(JBEAM_BRAKES, 'w') as f:
        for l in t: f.write(l)

    with open(JBEAM_BODY, 'r') as f:
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
    with open(JBEAM_BODY, 'w') as f:
        for l in t: f.write(l)

    with open(JBEAM_FTIRE, 'r') as f:
        t = f.readlines()
        t[103] = '        {{"radius":{}}},\n'.format(parameters['wheelRadius'])
    with open(JBEAM_FTIRE, 'w') as f:
        for l in t: f.write(l)

    with open(JBEAM_RTIRE, 'r') as f:
        t = f.readlines()
        t[103] = '        {{"radius":{}}},\n'.format(parameters['wheelRadius'])
    with open(JBEAM_RTIRE, 'w') as f:
        for l in t: f.write(l)
