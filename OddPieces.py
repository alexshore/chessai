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
        return f'Type: {type(self).__name__}' + \
               f' - Position: {self.position}' + \
               f' - Side: {sideString}' + \
               f' - Value: {self.value}' + \
               f' - Moves Made: {self.movesMade}'

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
        cpy = self.__class__(self.board, self.side,
                             self.position, movesMade=self.movesMade)
        return cpy


class Helicopter(Piece):

    stringRep = 'H'
    value = 5

    def __init__(self, board, side, position, movesMade=0):
        super(Helicopter, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        board = self.board
        pos = self.positionToHumanCoord
        movements = []
        for x in range(-3, 4):
            for y in range(-3, 4):
                if not (x == 0 and y == 0):
                    movements.append(C(x, y))

        for movement in movements:
            newPos = pos + movement
            if board.isValidPos(newPos) and board.notInFeministRange(self.side, newPos):
                pieceAtNewPos = self.board.pieceAtPosition(newPos)
                if pieceAtNewPos is None:
                    yield Move(self, newPos)
                elif pieceAtNewPos.side != self.side and (abs(movement[0]) != 3 and abs(movement[1]) != 3):
                    yield Move(self, newPos, pieceToCapture=pieceAtNewPos)


class AngryFeminist(Piece):

    stringRep = 'F'
    value = 50

    def __init__(self, board, side, position,  movesMade=0):
        super(AngryFeminist, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        board = self.board
        pos = self.position
        specialMove = self.helicopterPosCheck()
        movements = [C(0, 1), C(-1, -1), C(1, 0), C(-1, 0),
                     C(1, 1), C(1, -1), C(-1, 1), C(0, -1)]
        if specialMove == C(0, 1):
            movements.extend([C(0, 2), C(-1, 2), C(1, 2)])
            movements.remove(C(0, 1))
        elif specialMove == C(0, -1):
            movements.extend([C(0, -2), C(-1, -2), C(1, -2)])
            movements.remove(C(0, -1))
        elif specialMove == C(1, 0):
            movements.extend([C(2, 0), C(2, 1), C(2, -1)])
            movements.remove(C(1, 0))
        elif specialMove == C(-1, 0):
            movements.extend([C(-2, 0), C(-2, 1), C(-2, -1)])
            movements.remove(C(-1, 0))
        for movement in movements:
            newPos = pos + movement
            if board.isValidPos(newPos):
                pieceAtNewPos = board.pieceAtPosition(newPos)
                if pieceAtNewPos is None:
                    yield Move(self, newPos)
                elif pieceAtNewPos.side != self.side:
                    yield Move(self, newPos, pieceToCapture=pieceAtNewPos)

    def helicopterPosCheck(self):
        board = self.board
        pos = self.position
        movements = [C(0, 1), C(0, -1), C(1, 0), C(-1, 0)]
        for movement in movements:
            newPos = pos + movement
            if board.isValidPos(newPos):
                pieceAtNewPos = Board.pieceAtPosition(newPos)
                if pieceAtNewPos and pieceAtNewPos.stringRep == 'H':
                    return movement

class Mech(Piece):
    pass

class PornAddictedTeen(Piece):

    stringRep = 'P'
    value = 1

    def __init__(self, board, side, position, movesMade=0):
        super(PornAddictedTeen, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        pass

class SuicideBomber(Piece):

    stringRep = 'S'
    value = 5

    def __init__(self, board, side, position, movesMade=0):
        super(SuicideBomber, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        board = self.board
        pos = self.position
        movements = [C(0, 1), C(1, 0), C(-1, 0)] \
                     if self.side else movements = \
                    [C(0, -1), C(1, 0), C(-1, 0)]
        for movement in movements:
            newPos = pos + movement
            if board.isValidPos(newPos) and board.notInFeministRange(self.side, newPos):
                pieceAtNewPos = board.pieceAtPosition(newPos)
                if not pieceAtNewPos:
                    yield Move(self, newPos)
                elif pieceAtNewPos.side != self.side:
                    yield Move(self, newPos, pieceToCapture=pieceAtNewPos, cripple=True)
