from parameters import applyParameters
from beamNG import run

from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution

class BeamNGProblem(FloatProblem):

    def __init__(self):
        super(BeamNGProblem, self).__init__()
        self.number_of_variables = 8
        self.number_of_objectives = 3
        self.number_of_constraints = 0

        self.obj_direction = [self.MINIMIZE, self.MINIMIZE, self.MINIMIZE]
        self.obj_labels = ['f(1)', 'f(2)', 'f(3)']

        self.original = [5000, 0.2, 50, 1, 2000, 950, 1, 0.325]
        self.lower_bound = [4000, 0.1, 40, 0.8, 1600, 800, 0.8, 0.28]
        self.upper_bound = [6000, 0.3, 60, 1.2, 2400, 1100, 1.2, 0.35]

        FloatSolution.lower_bound = self.lower_bound
        FloatSolution.upper_bound = self.upper_bound

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        Vars = solution.variables
        print(Vars)

        X = list(map(lambda _: float('%.3f' % _), Vars[:self.number_of_variables]))

        change_ratio_max = 0
        changed_parameter_count = 0

        for i in range(self.number_of_variables):
            original = self.original[i]
            deviation = abs(X[i] - original)
            width = self.upper_bound[i] - self.lower_bound[i]
            change_precision = deviation / width
            change_ratio = deviation / original

            if change_precision < 0.04: X[i] = original
            else: changed_parameter_count += 1

            change_ratio_max = max(change_ratio_max, change_ratio)

        parameters = dict()
        parameters['maxRPM'] = X[0]
        parameters['engineInertia'] = X[1]
        parameters['engineBrakeTorque'] = X[2]
        parameters['engineNodeWeightMul'] = X[3]
        parameters['brakeMulF'] = X[4]
        parameters['brakeMulR'] = X[5]
        parameters['bodyNodeWeightMul'] = X[6]
        parameters['wheelRadius'] = X[7]

        applyParameters(parameters)

        result = run()

        print(result)

        if "distance" in result.keys():
            distance = result["distance"]
        else:
            distance = 0.0

        if "speed" in result.keys():
            speed = result["speed"]
            distance = 0.0
        else:
            speed = 0.0

        print("distance: %f" % distance)
        print("speed: %f" % speed)

        solution.objectives[0] = float('%.3f' % change_ratio_max)  # min maximum para change
        solution.objectives[1] = float('%.3f' % (distance - speed))  # distance - speed
        solution.objectives[2] = changed_parameter_count  # changed para num

        return solution

    def get_name(self):
        return 'BeamNGProblem'
