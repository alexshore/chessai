from Coordinate import Coordinate as C
from Move import Move

WHITE = True
BLACK = False
X = 0
Y = 1


class Piece:

    def __init__(self, board, side, position, movesMade=0):
        self.board = board
        self.side = side
        self.position = position
        movesMade = 0

    def __str__(self):
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
        if self.board == other.board and \
                self.side == other.side and \
                self.position == other.position and \
                self.__class__ == other.__class__:
            return True
        return False

    def __lt__(self, other):
        if self.stringRep == 'p' and other.stringRep in ['K', 'Q', 'R', 'B', 'N']:
            return True
        elif self.stringRep == 'K' and other.stringRep in ['Q', 'R', 'B', 'N', 'p']:
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

    def copy(self):
        cpy = self.__class__(self.board, self.side, self.position, movesMade=self.movesMade)
        return cpy
