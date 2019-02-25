from game_master import GameMaster
from read import *
from util import *


class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        p1 = []
        p2 = []
        p3 = []
        for fact in self.kb.facts:
            if fact.statement.predicate == 'on':
                disk = fact.statement.terms[0].term.element
                num = int(disk[-1:])
                if fact.statement.terms[1].term.element == 'peg1':
                    p1.append(num)
                if fact.statement.terms[1].term.element == 'peg2':
                    p2.append(num)
                if fact.statement.terms[1].term.element == 'peg3':
                    p3.append(num)
        p1.sort()
        p2.sort()
        p3.sort()
        return tuple(p1), tuple(p2), tuple(p3)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """

        if self.isMovableLegal(movable_statement):
            movableQuery = self.produceMovableQuery()
            matchCheck = match(movable_statement, movableQuery.statement)
            if matchCheck:
                disc1 = matchCheck.bindings[0].constant
                pInitial = matchCheck.bindings[1].constant
                pTarget = matchCheck.bindings[2].constant
                self.kb.kb_retract(parse_input('fact: (top ' + disc1.element + ' ' + pInitial.element + ')'))
                self.kb.kb_retract(parse_input('fact: (on ' + disc1.element + ' ' + pInitial.element + ')'))

                aboveCheck = self.kb.kb_ask(parse_input('fact: (above ' + disc1.element + ' ?x)'))
                if aboveCheck:
                    oldBottom = aboveCheck[0].bindings_dict['?x']
                    self.kb.kb_retract(parse_input('fact: (above ' + disc1.element + ' ' + oldBottom + ')'))
                    self.kb.kb_assert(parse_input('fact: (top ' + oldBottom + ' ' + pInitial.element + ')'))

                else:
                    self.kb.kb_assert(parse_input('fact: (empty ' + pInitial.element + ')'))

                emptyCheck = self.kb.kb_ask(parse_input('fact: (empty ' + pTarget.element + ')'))
                if emptyCheck:
                    self.kb.kb_retract(parse_input('fact: (empty ' + pTarget.element + ')'))
                    self.kb.kb_assert(parse_input('fact: (on ' + disc1.element + ' ' + pTarget.element + ')'))
                    self.kb.kb_assert(parse_input('fact: (top ' + disc1.element + ' ' + pTarget.element + ')'))

                else:
                    currTop = self.kb.kb_ask(parse_input('fact: (top ?x ' + pTarget.element + ')'))
                    oldTop = currTop[0].bindings_dict['?x']
                    self.kb.kb_retract(parse_input('fact: (top ' + oldTop + ' ' + pTarget.element + ')'))
                    self.kb.kb_assert(parse_input('fact: (above ' + disc1.element + ' ' + oldTop))
                    self.kb.kb_assert(parse_input('fact: (on ' + disc1.element + ' ' + pTarget.element + ')'))
                    self.kb.kb_assert(parse_input('fact: (top ' + disc1.element + ' ' + pTarget.element))

        else:
            pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))


class Puzzle8Game(GameMaster):
    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        row1 = [0, 0, 0]
        row2 = [0, 0, 0]
        row3 = [0, 0, 0]
        for fact in self.kb.facts:
            if fact.statement.predicate == 'pos':
                ele = fact.statement.terms[0].term.element
                num = ele[-1:]
                if num != 'y':
                    num = int(num)
                else:
                    num = -1
                col = int(fact.statement.terms[1].term.element[-1:])
                if fact.statement.terms[2].term.element == 'pos1':
                    row1[col - 1] = num
                if fact.statement.terms[2].term.element == 'pos2':
                    row2[col - 1] = num
                if fact.statement.terms[2].term.element == 'pos3':
                    row3[col - 1] = num
        return tuple(row1), tuple(row2), tuple(row3)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if self.isMovableLegal(movable_statement):
            ele = movable_statement.terms[0].term.element
            col = movable_statement.terms[1].term.element
            row = movable_statement.terms[2].term.element
            col1 = movable_statement.terms[3].term.element
            row1 = movable_statement.terms[4].term.element
            oldFact = parse_input('fact: (pos ' + ele + ' ' + col + ' ' + row + ')')
            newFact = parse_input('fact: (pos ' + ele + ' ' + col1 + ' ' + row1 + ')')
            oldFact1 = parse_input('fact: (pos empty ' + col1 + ' ' + row1 + ')')
            newFact1 = parse_input('fact: (pos empty ' + col + ' ' + row + ')')
            self.kb.kb_retract(oldFact)
            self.kb.kb_retract(oldFact1)
            self.kb.kb_assert(newFact)
            self.kb.kb_assert(newFact1)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
