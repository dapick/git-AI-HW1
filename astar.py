
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
        closed_set = {source: 0}  # The dict of nodes already evaluated. The g is the value
        parents = {}  # The map of navigated nodes.

        # Save the g_score and f_score for the open nodes
        open_set = {source: (self.heuristic.estimate(problem, problem.initialState), 0)}

        developed = 0  # Number of times we called succ

        # Tips:
        # - You should break your code into methods (two such stubs are written below)
        while open_set:
            next_state_tuple = self._get_open_state_with_lowest_f_score(open_set)
            next_state = next_state_tuple[0]
            closed_set[next_state] = next_state_tuple[1]
            del open_set[next_state]

            if problem.isGoal(next_state):
                new_cache_value = (self._reconstruct_path(parents, next_state),
                                   closed_set[next_state],
                                   self.heuristic.estimate(problem, problem.initialState),
                                   developed)
                self._storeInCache(problem, new_cache_value)
                return new_cache_value

            developed += 1
            for succ_state, succ_state_cost in problem.expandWithCosts(next_state, self.cost):
                new_g = closed_set[next_state] + succ_state_cost
                if succ_state in open_set:  # Checks if the son node was already in OPEN
                    if new_g < open_set[succ_state][1]:  # Checks if found a better path for the node
                        parents[succ_state] = next_state
                        open_set[succ_state] = (new_g + self.heuristic.estimate(problem, succ_state), new_g)
                else:
                    if succ_state in closed_set:  # Checks if the son node was already in CLOSED
                        if new_g < closed_set[succ_state]:  # Checks if found a better path for the node
                            parents[succ_state] = next_state
                            closed_set.pop(succ_state)
                            open_set[succ_state] = (new_g + self.heuristic.estimate(problem, succ_state), new_g)
                    else:  # Found a new node
                        parents[succ_state] = next_state
                        open_set[succ_state] = (new_g + self.heuristic.estimate(problem, succ_state), new_g)

    # Returns the state with the lowest f from OPEN
    @staticmethod
    def _get_open_state_with_lowest_f_score(open_set: dict):
        min_f = float("inf")
        min_state = 0
        min_state_g = 0
        for state, values in open_set.items():
            if values[0] < min_f:
                min_f = values[0]
                min_state = state
                min_state_g = values[1]
        return min_state, min_state_g

    # Reconstruct the path from a given goal by its parent and so on
    @staticmethod
    def _reconstruct_path(parents: dict, goal) -> list:
        path_list = []
        while goal:
            path_list.insert(0, goal)
            goal = parents.get(goal)
        return path_list
