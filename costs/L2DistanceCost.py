from cost import Cost
from ways import load_map_from_csv
from ways import tools
from consts import Consts
from states import *

class L2DistanceCost(Cost):
    roads = None

    def __init__(self, roads):
        self.roads = roads

    # Returns the L2 aerial distance between two states
    def compute(self, fromState, toState):
        coord1 = self.roads[fromState.junctionIdx].coordinates
        coord2 = self.roads[toState.junctionIdx].coordinates

        # TODO : Done
        return tools.compute_distance(coord1, coord2)


if __name__ == "__main__":
    roads = load_map_from_csv(Consts.getDataFilePath("israel.csv"))
    bs = BusState(34, [(54980, 3423), (5325, 2435)], [], [])
    bs1 = BusState(342, [], [], [])
    testobj = L2DistanceCost(roads)
    print("hey")
    print(testobj.compute(bs, bs1))
