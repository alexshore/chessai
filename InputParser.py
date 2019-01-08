# Importing required python modules.
import re


# Starts the definition of the class 'InputParser'.
class InputParser:

    def __init__(self, board, side):
        # Initialising function of the 'InputParser' class. Creates and assigns
        # given values to the required attributes.
        self.board = board
        self.side = side

    def parse(self, humanInput):
        # Parsing function. Takes in a human input of a move notation before
        # comparing it to the notation of all of the other moves that have
        # been worked out up to this point. It then returns a move if one such
        # move exists.
        newInput = None
        if re.compile('[a-z][1-8]x*[a-z][1-8]=[qbnr]').match(humanInput):
            newInput = humanInput[:-1] + humanInput[-1].upper()
        elif re.compile('[a-z][1-8]x*[a-z][1-8]').match(humanInput):
            newInput = humanInput
        elif re.compile('0[/-0/]*').match(humanInput):
            newInput = humanInput
        for move in self.getLegalMovesWithNotation(self.side):
            if move.notation == newInput:
                return move

    def getLegalMovesWithNotation(self, side):
        # Retrieves a list of all possible legal moves before assigning each
        # move its notation.
        moves = []
        for legalMove in self.board.getAllMovesLegal(side):
            legalMove.notation = legalMove.getNotation()
            moves.append(legalMove)
        return moves
