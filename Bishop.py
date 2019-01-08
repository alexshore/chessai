# Importing required custom modules.
from Coordinate import Coordinate as C
from Piece import Piece

# Defines widely used global constants.
WHITE = True
BLACK = False


# Starts the definition of the class 'Bishop' using inheritence.
class Bishop(Piece):
    # Defines the string representation and the piece value.
    stringRep = 'B'
    value = 3

    def __init__(self, board, side, position, movesMade=0):
        # Initialising function of the 'Bishop' class. Creates and assigns
        # given values to the required attributes. Does this through both
        # regular variable assignment and also through inheritance.
        super(Bishop, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        # Function run to yield a group of all possible legal and illegal
        # 'Move' objects to the calling function. Does this by providing a list
        # of directions to the 'movesInDirectionFromPos' function which then
        # returns the moves to be yielded.
        pos = self.position
        directions = [C(1, 1), C(-1, -1),
                      C(-1, 1), C(1, -1)]
        for direction in directions:
            for move in self.movesInDirectionFromPos(pos, direction,
                                                     self.side):
                yield move
