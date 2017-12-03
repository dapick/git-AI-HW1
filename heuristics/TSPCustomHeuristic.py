from heuristics import Heuristic

from problems import MapProblem
from astar import AStar
from heuristics import L2DistanceHeuristic


# TODO : Done
class TSPCustomHeuristic(Heuristic):
    roads = None
    map_astar = None

    # TODO : Done
    def __init__(self, roads, initial_state):
        super().__init__()
        self.roads = roads
        self.map_astar = AStar(L2DistanceHeuristic(), shouldCache=True)

    # Estimate heuristically the minimal cost from the given state to the problem's goal
    def estimate(self, problem, state):
        max_distance = 0
        for order in state.waitingOrders:
            orders_problem = MapProblem(self.roads, order[0], order[1])
            _, orders_distance, _, _ = self.map_astar.run(orders_problem)

            if orders_distance > max_distance:
                max_distance = orders_distance
        return max_distance
