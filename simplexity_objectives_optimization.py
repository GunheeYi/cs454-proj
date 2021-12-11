from parameters import applyParameters
from beamNG import run

from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution

class BeamNGProblem(FloatProblem):

    def __init__(self, q):
        super(BeamNGProblem, self).__init__()
        self.number_of_variables = 7
        self.number_of_objectives = 3
        self.number_of_constraints = 0

        self.obj_direction = [self.MINIMIZE, self.MINIMIZE, self.MINIMIZE]
        self.obj_labels = ['f(1)', 'f(2)', 'f(3)']

        self.original = [7000, 0.14, 44, 1, 3000, 1550,  0.325]
        self.lower_bound = [6000, 0.1, 30, 0.8, 2500, 1250, 0.3]
        self.upper_bound = [8000, 0.18, 60, 1.2, 3500, 1850, 0.35]
        self._q = q

        FloatSolution.lower_bound = self.lower_bound
        FloatSolution.upper_bound = self.upper_bound

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        port, car_name = self._q.get()
        Vars = solution.variables

        X = list(map(lambda _: float('%.3f' % _), Vars[:self.number_of_variables]))

        change_ratio_max = 0
        changed_parameter_count = 0

        for i in range(self.number_of_variables):
            original = self.original[i]
            deviation = abs(X[i] - original)
            width = self.upper_bound[i] - self.lower_bound[i]
            change_precision = deviation / width
            change_ratio = deviation / original
            

            # precision A
            if (width >= 1000):
                beta = 0.005
            elif (width >= 100):
                beta = 0.01
            elif (width >= 1):
                beta = 0.02
            else:
                beta = 0.04

            # precision B
            '''if (width >= 1000):
                beta = 0.01
            elif (width >= 100):
                beta = 0.02
            elif (width >= 1):
                beta = 0.04
            else:
                beta = 0.08'''

            if change_precision < beta: X[i] = original
            else: changed_parameter_count += 1

            change_ratio_max = max(change_ratio_max, change_ratio)
        
        parameters = dict()
        parameters['maxRPM'] = X[0]
        parameters['engineInertia'] = X[1]
        parameters['engineBrakeTorque'] = X[2]
        parameters['nodeWeightMul'] = X[3]
        parameters['brakeMulF'] = X[4]
        parameters['brakeMulR'] = X[5]
        parameters['wheelRadius'] = X[6]

        applyParameters(parameters, car_name)

        result = run(port, car_name)

        distance = result["distance"]
        speed = result["speed"]

        if result["speed"] != 0:
            distance = 0.0

        solution.objectives[0] = float('%.5f' % change_ratio_max)  # min maximum para change
        solution.objectives[1] = float('%.5f' % (distance - speed))  # distance - speed
        solution.objectives[2] = changed_parameter_count  # changed para num

        self._q.put((port, car_name))
        return solution

    def get_name(self):
        return 'BeamNGProblem'
