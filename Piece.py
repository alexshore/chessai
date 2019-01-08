# Importing required custom modules.
from Coordinate import Coordinate as C
from Move import Move

# Defines widely used global constants.
WHITE = True
BLACK = False


# Starts the definition of the class 'Piece'.
class Piece:

    def __init__(self, board, side, position, movesMade=0):
        # Initialising function of the 'InputParser' class. Creates and assigns
        # given values to the required attributes.
        self.board = board
        self.side = side
        self.position = position
        movesMade = 0

    def __str__(self):
        # Custom function that generates a printable string for whenever
        # something tries to print the object. It compiles several pieces of
        # info about the 'Piece' object and formats them together before
        # returning the string.
        if self.side == WHITE:
            sideString = 'White'
        else:
            sideString = 'Black'
        return 'Type: {}'.format(type(self).__name__) + \
               ' - Position: {}'.format(self.position) + \
               ' - Side: {}'.format(sideString) + \
               ' - Value: {}'.format(self.value) + \
               ' - Moves Made: {}'.format(self.movesMade)

    def __eq__(self, other):
        # Custom function that returns a boolean value depending on whether
        # certain attributes of two objects are the same as each other.
        if self.board == other.board and \
                self.side == other.side and \
                self.position == other.position and \
                self.__class__ == other.__class__:
            return True
        return False

    def __lt__(self, other):
        # Custom function to determine whether a specific 'Piece' object is
        # worth less than another given object. Then returns a boolean value.
        if self.stringRep == 'p':
            return True
        elif self.stringRep == 'K':
            return False
        elif self.stringRep == 'Q':
            return True if other.stringRep == 'K' else False
        elif self.stringRep == 'R':
            return True if other.stringRep in ['K', 'Q'] else False
        elif self.stringRep == 'B':
            return True if other.stringRep in ['K', 'Q', 'R'] else False
        elif self.stringRep == 'N':
            return True if other.stringRep in ['K', 'Q', 'R', 'B'] else False

    def movesInDirectionFromPos(self, pos, direction, side):
        # Function to yield a group of all possible legal and illegal 'Move'
        # objects from a given 'direction' 'Coordinate' objects to the calling
        # function. Returns either when it finds a move to take a piece or
        # after it has finished looping through the algorithm.
        for distance in range(1, 8):
            movement = C(distance * direction[0], distance * direction[1])
            newPos = pos + movement
            if self.board.isValidPos(newPos):
                pieceAtNewPos = self.board.pieceAtPosition(newPos)
                if pieceAtNewPos is None:
                    yield Move(self, newPos)
                elif pieceAtNewPos is not None:
                    if pieceAtNewPos.side != side:
                        yield Move(self, newPos, pieceToCapture=pieceAtNewPos)
                    return
