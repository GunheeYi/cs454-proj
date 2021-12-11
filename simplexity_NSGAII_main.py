__author__ = 'Simplexity-Kaiou Yin'

from simplexity_objectives_optimization import BeamNGProblem
from jmetal.algorithm.multiobjective import NSGAII
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.util.solution import print_function_values_to_file, print_variables_to_file
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.evaluator import MultiprocessEvaluator, SequentialEvaluator
from multiprocessing import Manager
from pathlib import Path
from config import BNG_USER
import shutil

if __name__ == '__main__':
    num_processes = 1
    Path(f"{BNG_USER}/0.23/mods/unpacked/cs454_mod/vehicles").mkdir(parents=True, exist_ok=True)
    for i in range(num_processes):
        car_path = f"{BNG_USER}/0.23/mods/unpacked/cs454_mod/vehicles/car{i}"
        if (not Path(car_path).exists()):
            shutil.copytree('./etk800_sample', car_path)
    
    m = Manager()
    portDirQueue = m.Queue()
    [portDirQueue.put((64256+i, f"car{i}")) for i in range(num_processes)]
    print("Initialization done.")
    problem = BeamNGProblem(portDirQueue)

    algorithm = NSGAII(
        problem=problem,
        population_size=30,
        offspring_population_size=30,
        mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
        crossover=SBXCrossover(probability=1, distribution_index=20),
        termination_criterion=StoppingByEvaluations(max_evaluations=1680),
        population_evaluator = SequentialEvaluator() if (num_processes == 1) else MultiprocessEvaluator(processes=num_processes)
    )

    algorithm.run()

    from jmetal.util.solution import get_non_dominated_solutions, print_function_values_to_file, \
        print_variables_to_file
    from jmetal.lab.visualization import Plot

    front = get_non_dominated_solutions(algorithm.get_result())

    # Save results to file
    print_function_values_to_file(front, 'FUN.' + algorithm.label)
    print_variables_to_file(front, 'VAR.' + algorithm.label)

    print(f'Algorithm: ${algorithm.get_name()}')
    print(f'Problem: ${problem.get_name()}')
    print(f'Computing time: ${algorithm.total_computing_time}')

    plot_front = Plot(title='Pareto Front',
                      axis_labels=['min maximum parameter change', 'min distance - speed', 'min changed para num'])
    plot_front.plot(front, label='Three Objectives', filename='Pareto Front', format='png')
