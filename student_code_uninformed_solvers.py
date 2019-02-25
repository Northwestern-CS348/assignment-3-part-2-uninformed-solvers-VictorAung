
from collections import deque
from solver import *


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here



        # save current state
        currState = self.currentState

        # if there are next moves, we should expand the node and mark down parents and children
        for mov in self.gm.getMovables():
            self.gm.makeMove(mov)
            nextState = GameState(self.gm.getGameState(), self.currentState.depth + 1, mov)
            currState.children.append(nextState)
            nextState.parent = currState
            self.gm.reverseMove(mov)

        # check child if it has not been visited
        for child in currState.children:
            if child not in self.visited:
                self.currentState = child
                self.visited[child] = True
                self.gm.makeMove(child.requiredMovable)
                break

        if self.victoryCondition == self.currentState.state:
            return True
        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = deque()
        self.counter = 0

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        #queue up state
        for move in self.gm.getMovables():
            self.gm.makeMove(move)
            newState = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
            newState.parent = self.currentState
            self.gm.reverseMove(move)
            self.currentState.children.append(newState)
            self.queue.append(newState)

        #go to root
        while self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        #change counter
        while self.queue[self.counter] in self.visited:
            self.counter += 1

        newList = list()
        while self.queue[self.counter].parent:
            newList.append(self.queue[self.counter].requiredMovable)
            self.queue[self.counter] = self.queue[self.counter].parent

        while len(newList) != 0:
            self.gm.makeMove(newList.pop())
            for child in self.currentState.children:
                if child.state == self.gm.getGameState():
                    self.visited[child] = True
                    self.currentState = child

        if self.currentState.state == self.victoryCondition:
            return True
        return False
