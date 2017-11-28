from heuristics import Heuristic
from ways import load_map_from_csv
from ways import tools
from consts import Consts
from states import *
from problems import MapProblem
# Use the L2 aerial distance (in meters)
class L2DistanceHeuristic(Heuristic):
    def estimate(self, problem, state):
        coord1 = problem._roads[state.junctionIdx].coordinates
        coord2 = problem._roads[problem.target.junctionIdx].coordinates

        # TODO : Return the correct value (call the suitable function from ways.tools)
        return tools.compute_distance(coord1, coord2)


if __name__ == "__main__":
    roads = load_map_from_csv(Consts.getDataFilePath("israel.csv"))
    mp = MapProblem(roads, 50343, 5413)
    bs1 = BusState(342, [], [], [])
    test_obj = L2DistanceHeuristic()
    print("hey")
    print(test_obj.estimate(mp, bs1))
