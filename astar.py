import numpy as np
import sys


class AStar:
    cost = None
    heuristic = None
    _cache = None
    shouldCache = None

    def __init__(self, heuristic, cost=None, shouldCache=False):
        self.heuristic = heuristic
        self.shouldCache = shouldCache
        self.cost = cost

        # Handles the cache. No reason to change this code.
        if self.shouldCache:
            self._cache = {}

    # Get's from the cache. No reason to change this code.
    def _getFromCache(self, problem):
        if self.shouldCache:
            return self._cache.get(problem)

        return None

    # Get's from the cache. No reason to change this code.
    def _storeInCache(self, problem, value):
        if not self.shouldCache:
            return

        self._cache[problem] = value

    # Run A*
    def run(self, problem):
        # Check if we already have this problem in the cache.
        # No reason to change this code.
        source = problem.initialState
        if self.shouldCache:
            res = self._getFromCache(problem)

            if res is not None:
                return res

        # Initializes the required sets
        closed_set = []  # The list of nodes already evaluated.
        parents = {}  # The map of navigated nodes.

        # Save the g_score and f_score for the open nodes
        g_score = {source: 0}
        open_set = {source: self.heuristic.estimate(problem, problem.initialState)}

        developed = 0  # Number of times we called succ

        # Tips:
        # - To get the successor states of a state with their costs, use: problem.expandWithCosts(state, self.cost)
        # - You should break your code into methods (two such stubs are written below)
        # - Don't forget to cache your result between returning it - TODO
        while open_set:
            next_state = self._get_open_state_with_lowest_f_score(open_set)
            del open_set[next_state]
            closed_set.append(next_state)
            if problem.isGoal(next_state):
                retVal=(self._reconstruct_path(parents, next_state),
                        self._calculate_path_cost(parents, g_score, next_state),
                        self.heuristic.estimate(problem, problem.initialState),
                        developed)
                self._storeInCache(problem,retVal)
                return retVal
            developed += 1
            for succ_state, succ_state_cost in problem.expandWithCosts(next_state, self.cost):
                new_g = g_score[next_state] + succ_state_cost
                if succ_state in open_set:  # Checks if the son node was already in OPEN
                    if new_g < g_score[succ_state]:  # Checks if found a better path for the node
                        g_score[succ_state] = new_g
                        parents[succ_state] = next_state
                        open_set[succ_state] = g_score[succ_state] + self.heuristic.estimate(problem, succ_state)
                else:
                    if succ_state in closed_set:  # Checks if the son node was already in CLOSED
                        if new_g < g_score[succ_state]:  # Checks if found a better path for the node
                            g_score[succ_state] = new_g
                            parents[succ_state] = next_state
                            closed_set.remove(succ_state)
                            open_set[succ_state] = g_score[succ_state] + self.heuristic.estimate(problem, succ_state)
                    else:  # Found a new node
                        g_score[succ_state] = new_g
                        parents[succ_state] = next_state
                        open_set[succ_state] = g_score[succ_state] + \
                                               self.heuristic.estimate(problem, succ_state)

    @staticmethod
    def _get_open_state_with_lowest_f_score(open_set: dict):
        min_f = float("inf")
        min_state_f = 0
        for state, state_f_value in open_set.items():
            if state_f_value < min_f:
                min_f = state_f_value
                min_state_f = state
        return min_state_f

    # Reconstruct the path from a given goal by its parent and so on
    @staticmethod
    def _reconstruct_path(parents: dict, goal) -> list:
        path_list = []
        while goal:
            path_list.insert(0, goal)
            goal = parents.get(goal)
        return path_list

    @staticmethod
    def _calculate_path_cost(parents: dict, g_score: dict, goal) -> int:
        path_cost = 0
        #while goal:
            #path_cost += g_score[goal]
            #goal = parents.get(goal)
        return g_score[goal]





