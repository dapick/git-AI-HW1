from consts import Consts
from astar import AStar
from ways import load_map_from_csv
from busSolvers import GreedyBestFirstSolver, GreedyStochasticSolver
from problems import BusProblem
from costs import L2DistanceCost
from heuristics import L2DistanceHeuristic
import numpy as np
from scipy import stats

REPEATS = 150

# Load the files
roads = load_map_from_csv(Consts.getDataFilePath("israel.csv"))
prob = BusProblem.load(Consts.getDataFilePath("HAIFA_100.in"))

mapAstar = AStar(L2DistanceHeuristic(), shouldCache=True)

scorer = L2DistanceCost(roads)

# Run the greedy solver
pickingPath = GreedyBestFirstSolver(roads, mapAstar, scorer).solve(prob)
greedyDistance = pickingPath.getDistance() / 1000
print("Greedy solution: {:.2f}km".format(greedyDistance))

# Run the stochastic solver #REPATS times
solver = GreedyStochasticSolver(roads, mapAstar, scorer,
                                Consts.STOCH_INITIAL_TEMPERATURE,
                                Consts.STOCH_TEMPERATURE_DECAY_FUNCTION,
                                Consts.STOCH_TOP_SCORES_TO_CONSIDER)
results = np.zeros((REPEATS,))
print("Stochastic repeats:")
for i in range(REPEATS):
    print("{}..".format(i+1), end=" ", flush=True)
    results[i] = solver.solve(prob).getDistance() / 1000

print("\nDone!")

# TODO : Part1 - Plot the diagram required in the instructions
from matplotlib import pyplot as plt
X=np.array(range(REPEATS))
Y=np.array([np.amin(results[:i+1]) for i in range(REPEATS)])
plt.plot(X,Y)
plt.grid(True)
plt.show(block=False)
plt.plot(X,greedyDistance)
plt.waitforbuttonpress()
# TODO : Part2 - Remove the exit and perform the t-test
avg_of_samples=np.sum(results)/150
print("{} avg of samples ".format(avg_of_samples))
deviation_samples=np.sqrt(np.sum(np.power(avg_of_samples-results,2))/150)
print("{} deviation of samples ".format(deviation_samples))
another_value_no_idea,p_value=stats.ttest_1samp(results,greedyDistance)
print(another_value_no_idea)
print(p_value)
