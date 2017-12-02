from heuristics import Heuristic

from problems import MapProblem
from astar import AStar
from heuristics import L2DistanceHeuristic


# TODO : Done
class TSPCustomHeuristic(Heuristic):
    roads = None
    map_astar = None

    # TODO : Done
    def __init__(self, roads):
        super().__init__()
        self.roads = roads
        self.map_astar = AStar(L2DistanceHeuristic(), shouldCache=True)

    # Estimate heuristically the minimal cost from the given state to the problem's goal
    def estimate(self, problem, state):
        max_distance = 0
        for order_i in state.waitingOrders:
            source = order_i[0]
            for order_j in state.waitingOrders:
                target = order_j[1]
                orders_problem = MapProblem(self.roads, source, target)
                _, orders_distance, _, _ = self.map_astar.run(orders_problem)

                if orders_distance > max_distance:
                    max_distance = orders_distance
        return max_distance
