# Importing required custom modules.
from Coordinate import Coordinate as C
from Move import Move
from Piece import Piece

# Defines widely used global constants.
WHITE = True
BLACK = False


# Starts the definition of the class 'Knight' using inheritence.
class Knight(Piece):
    # Defines the string representation and the piece value.
    stringRep = 'N'
    value = 3

    def __init__(self, board, side, position, movesMade=0):
        # Initialising function of the 'Bishop' class. Creates and assigns
        # given values to the required attributes. Does this through both
        # regular variable assignment and also through inheritance.
        super(Knight, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        # Function run to yield a group of all possible legal and illegal
        # 'Move' objects to the calling function. Does this by running through
        # a list of movements and testing for valid moves before yielding them.
        board = self.board
        pos = self.position
        movements = [C(2, 1), C(2, -1), C(-2, 1), C(-2, -1),
                     C(1, 2), C(1, -2), C(-1, 2), C(-1, -2)]
        for movement in movements:
            newPos = pos + movement
            if board.isValidPos(newPos):
                pieceAtNewPos = board.pieceAtPosition(newPos)
                if pieceAtNewPos is None:
                    yield Move(self, newPos)
                elif pieceAtNewPos.side != self.side:
                    yield Move(self, newPos, pieceToCapture=pieceAtNewPos)
