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

#PART 1
from matplotlib import pyplot as plt
#plot the minimum value for i first iterations
X=np.array(range(REPEATS))
Y=np.array([np.amin(results[:i+1]) for i in range(REPEATS)])
plt.title("Minimum distance as a function of repeats")
plt.xlabel('REPEATS')
plt.ylabel('Minimum Distance')
plt.plot(X,Y, label= "Greedy Stochastic")
plt.grid(True)
plt.show(block=False)
#plot the greedy distance value
greedyDistance_value_line=np.array([greedyDistance]*150)
plt.plot(X,greedyDistance_value_line, label= "Greedy")
plt.legend(bbox_to_anchor=(1, 1),
               bbox_transform=plt.gcf().transFigure)
plt.waitforbuttonpress()

#PART 2
avg_of_samples=np.sum(results)/150
print("{} avg of samples ".format(avg_of_samples))
deviation_samples=np.sqrt(np.sum(np.power(avg_of_samples-results,2))/150)
print("{} deviation of samples ".format(deviation_samples))
_,p_value=stats.ttest_1samp(results,greedyDistance)
print("{} p value",p_value)
