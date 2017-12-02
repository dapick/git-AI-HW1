from . import GreedySolver
import numpy as np

class GreedyStochasticSolver(GreedySolver):
    _TEMPERATURE_DECAY_FACTOR = None
    _INITIAL_TEMPERATURE = None
    _N = None

    def __init__(self, roads, astar, scorer, initialTemperature, temperatureDecayFactor, topNumToConsider):
        super().__init__(roads, astar, scorer)

        self._INITIAL_TEMPERATURE = initialTemperature
        self._TEMPERATURE_DECAY_FACTOR = temperatureDecayFactor
        self._N = topNumToConsider

    def _getSuccessorsProbabilities(self, currState, successors):
        scores=[self._scorer.compute(currState, target) for target in successors]
        dict_scores_with_index = zip(scores,range(len(successors)))
        sortedValues=sorted(dict_scores_with_index,key=lambda x:x[0])
        X = np.array(list([ x[0] for x in filter(lambda x: x[0] , sortedValues[:self._N])]))
        sortedValues=[ [0,x[1]] for x in sortedValues]
        X = X / np.amin(X)
        Y = np.sum(np.power(X, -1 / self.T))
        X = np.power(X, -1 / self.T)
        X =X/Y
        for i in range(len(X)):
            sortedValues[i][0]=X[i]
        sortedValues=[x[0] for x in sorted(sortedValues,key=lambda x:x[1])]
        P=np.array(sortedValues)

        # Initialize an all-zeros vector for the distribution
        #P = np.zeros((len(successors),))

        # TODO: Fill the distribution in P as explained in the instructions.
        # TODO : No changes in the rest of the code are needed

        # Update the temperature
        self.T *= self._TEMPERATURE_DECAY_FACTOR

        return P

    # Find the next state to develop
    def _getNextState(self, problem, currState):
        successors = list(problem.expand(currState))
        P = self._getSuccessorsProbabilities(currState, successors)
        # TODO : Choose the next state stochastically according to the calculated distribution.
        # You should look for a suitable function in numpy.random.
        a=len(successors)
        nextIdx =  np.random.choice(len(successors),1,p=P)[0]
        return successors[nextIdx]

    # Override the base solve method to initialize the temperature
    def solve(self, initialState):
        self.T = self._INITIAL_TEMPERATURE
        return super().solve(initialState)