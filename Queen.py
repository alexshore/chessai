# Importing required custom modules.
from Coordinate import Coordinate as C
from Piece import Piece

# Defines widely used global constants.
WHITE = True
BLACK = False


# Starts the definition of the class 'Queen' using inheritence.
class Queen(Piece):
    # Defines the string representation and the piece value.
    stringRep = 'Q'
    value = 9

    def __init__(self, board, side, position, movesMade=0):
        # Initialising function of the 'Queen' class. Creates and assigns
        # given values to the required attributes. Does this through both
        # regular variable assignment and also through inheritance.
        super(Queen, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        # Function run to yield a group of all possibly legal and illegal
        # moves to the calling function. Does this by providing a list of
        # directions to the 'movesInDirectionFromPos' function which then
        # returns the moves to be yielded.
        pos = self.position
        directions = [C(0, 1), C(0, -1), C(1, 0), C(-1, 0),
                      C(1, 1), C(1, -1), C(-1, 1), C(-1, -1)]
        for direction in directions:
            for move in self.movesInDirectionFromPos(pos, direction,
                                                     self.side):
                yield move
