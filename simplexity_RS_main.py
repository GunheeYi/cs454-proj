__author__ = 'Simplexity-Kaiou Yin'

from simplexity_objectives_optimization import BeamNGProblem
from jmetal.algorithm.multiobjective.random_search import RandomSearch
from jmetal.util.solution import print_function_values_to_file, print_variables_to_file
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.core.quality_indicator import HyperVolume
from queue import Queue
from config import BNG_USER
from pathlib import Path
import shutil

if __name__ == '__main__':
    CAR_NAME = "car1"
    car_path = f"{BNG_USER}/0.23/mods/unpacked/cs454_mod/vehicles/" + CAR_NAME
    if (not Path(car_path).exists()):
        shutil.copytree('./etk800_sample', car_path)
    portDirQueue = Queue()
    portDirQueue.put((64255, CAR_NAME))
    problem = BeamNGProblem(portDirQueue)

    max_evaluations = 1680

    algorithm = RandomSearch(
        problem=problem,
        termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
    )

    algorithm.run()
    front = algorithm.get_result()

    from jmetal.lab.visualization import Plot

    # Save results to file
    print_function_values_to_file(front, 'FUN.' + algorithm.label)
    print_variables_to_file(front, 'VAR.' + algorithm.label)

    print(f'Algorithm: ${algorithm.get_name()}')
    print(f'Problem: ${problem.get_name()}')
    print(f'Computing time: ${algorithm.total_computing_time}')
