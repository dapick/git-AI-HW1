import abc


class Problem(metaclass=abc.ABCMeta):
    initialState = None

    def __init__(self, initialState):
        self.initialState = initialState

    @abc.abstractmethod
    def _calculateCost(self, fromState, toState):
        raise NotImplementedError

    @abc.abstractmethod
    # Return the successors of a given state
    def expand(self, state):
        raise NotImplementedError

    # Return the successors with a cost for each successor (operator)
    def expandWithCosts(self, state, costComputer=None):
        successors = self.expand(state)

        if costComputer is None:
            for s in successors:
                yield s, self._calculateCost(state, s)
        else:
            for s in successors:
                yield s, costComputer.compute(state, s)

    @abc.abstractmethod
    def isGoal(self, state):
        raise NotImplementedError


from states import MapState


class MapProblem(Problem):
    target = None
    _roads = None

    def __init__(self, roads, source, target):
        self._roads = roads
        I = MapState(source, roads[source].coordinates)
        super().__init__(I)

        self.target = MapState(target, roads[target].coordinates)

    def __hash__(self):
        return hash((self.initialState, self.target))

    def __eq__(self, other):
        return (self.initialState, self.target) == (other.initialState, other.target)

    def _calculateCost(self, fromState, toState):
        for l in self._roads[fromState.junctionIdx].links:
            if l.target == toState.junctionIdx:
                return l.distance

        raise ValueError

    def expand(self, state):
        for l in self._roads[state.junctionIdx].links:
            yield MapState(l.target, self._roads[l.target].coordinates)

    def isGoal(self, state):
        return state.junctionIdx == self.target.junctionIdx


from states import BusState


class BusProblem(Problem):
    orders = None

    def __init__(self, startingPoint: int, orders: list):
        self.orders = orders

        I = BusState(startingPoint, self.orders.copy(), [], [])
        super().__init__(I)

    def isGoal(self, state):
        return state.isGoal()

    def _calculateCost(self, fromState, toState):
        raise NotImplementedError

    # Return all the successors of a given state
    def expand(self, state):
        for order in state.waitingOrders:
            yield self._getNewStateAtLoc(state, order[0])

        for order in state.ordersOnBus:
            yield self._getNewStateAtLoc(state, order[1])

    # Get the new state created after going from one state to a new location (on map)
    def _getNewStateAtLoc(self, previousState, newLoc):
        # TODO : Done
        newWaiting = []
        newOnBus = []
        newFinished = []
        for order in previousState.waitingOrders:
            if order[0] == newLoc:  # Reach to a source point of an order which waited
                newOnBus.append(order)  # Add a new order to the bus
            else:
                newWaiting.append(order)  # Keep the orders in wait
        for order in previousState.ordersOnBus:
            if order[1] == newLoc:  # Reach to a target point of an order which was on the bus
                newFinished.append(order)  # Update that finished an order
            else:
                newOnBus.append(order)  # Keep the order in the bus
        newFinished.extend(previousState.finishedOrders)  # Keep orders which were finished before
        return BusState(newLoc, newWaiting, newOnBus, newFinished)

    @staticmethod
    def load(filepath):
        with open(filepath, "r") as f:
            startingPoint = int(f.readline())
            ordersNum = int(f.readline())

            orders = [None] * ordersNum

            for i in range(ordersNum):
                order = f.readline().split("\t")
                orders[i] = (int(order[0]), int(order[1]))

        return BusProblem(startingPoint, orders)


""" Tests """


if __name__ == "__main__":
    bp = BusProblem(34, [(54980, 3423), (5325, 2435)])
    bs = BusState(34, [(54980, 3423), (5325, 2435)], [], [])
    bs1 = bp._getNewStateAtLoc(bs, 5325)
    bs1 = bp._getNewStateAtLoc(bs1, 2435)
    bs1 = bp._getNewStateAtLoc(bs1, 54980)
    if not bs1.isGoal():
        print("OK")
    bs1 = bp._getNewStateAtLoc(bs1, 3423)
    if bs1.isGoal():
        print("OK")

