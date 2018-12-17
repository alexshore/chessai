from Coordinate import Coordinate as C
from OddMove import Move

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
    value = 10

    def __init__(self, board, side, position, movesMade=0):
        super(Helicopter, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        board = self.board
        pos = self.position
        movements = []
        for x in range(-3, 4):
            for y in range(-3, 4):
                if not (x == 0 and y == 0):
                    movements.append(C(x, y))
        print(movements)
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
                pieceAtNewPos = board.pieceAtPosition(newPos)
                if pieceAtNewPos and pieceAtNewPos.stringRep == 'H':
                    return movement


class TikTokFan(Piece):

    stringRep = 't'
    value = 1

    def __init__(self, board, side, position,  movesMade=0):
        super(TikTokFan, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        board = self.board
        pos = self.position
        yInc = board.scanForTikTok(self.side, pos)
        movement = C(0, yInc) if self.side == WHITE else C(0, -1 * yInc)
        finalPos = pos + movement
        if self.board.isValidPos(finalPos) and board.notInFeministRange(self.side, pos):
            if not self.board.pieceAtPosition(finalPos):
                yield Move(self, finalPos)
        movements = [C(1, 0), C(-1, 0)]
        for movement in movements:
            newPos = pos + movement
            if self.board.isValidPos(newPos):
                pieceToTake = self.board.pieceAtPosition(newPos)
                if pieceToTake and pieceToTake.side != self.side:
                    yield Move(self, newPos, pieceToCapture=pieceToTake)


class NeckBeard(Piece):

    stringRep = 'N'
    value = 5

    def __init__(self, board, side, position, movesMade=0):
        super(NeckBeard, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        pass


class PornAddict(Piece):

    stringRep = 'P'
    value = 3

    def __init__(self, board, side, position, movesMade=0):
        super(PornAddict, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        board = self.board
        pos = self.position
        side = self.side
        movements = [C(1, 0), C(-1, 0)]
        for movement in movements:
            newPos = pos + movement
            if board.isValidPos(newPos) and board.notInFeministRange(side, newPos):
                pieceAtNewPos = board.pieceAtPosition(newPos)
                if not pieceAtNewPos:
                    yield Move(self, newPos)
                elif pieceAtNewPos.side != self.side:
                    yield Move(self, newPos, pieceToCapture=pieceAtNewPos)
        movements = [C(1, 1), C(-1, 1)] \
                     if self.side == WHITE else \
                    [C(1, -1), C(-1, -1)]
        for movement in movements:
            newPos = pos + movement
            if board.isValidPos(newPos) and board.notInFeministRange(side, newPos):
                pieceAtNewPos = board.pieceAtPosition(newPos)
                if pieceAtNewPos is None:
                    yield Move(self, newPos)
                    nextPos = newPos + movement
                    if board.isValidPos(nextPos) and board.notInFeministRange(side, nextPos):
                        pieceAtNewPos = board.pieceAtPosition(nextPos)
                        if pieceAtNewPos is None:
                            yield Move(self, nextPos)
                        elif pieceAtNewPos.side != side:
                            yield Move(self, nextPos, pieceToCapture=pieceAtNewPos)
                elif pieceAtNewPos.side != side:
                    yield Move(self, newPos, pieceToCapture=pieceAtNewPos)


class AbusiveFather(Piece):

    stringRep = 'A'
    value = 3

    def __init__(self, board, side, position, movesMade=0, waitTime=0):
        super(AbusiveFather, self).__init__(board, side, position)
        self.movesMade = movesMade
        self.waitTime = waitTime

    def getPossibleMoves(self):
        pos = self.position
        board = self.board
        side = self.side
        directions = [C(1, 1), C(-1, -1),
                      C(-1, 1), C(1, -1)]
        for direction in directions:
            for dist in range(1, 8):
                movement = C(direction[0] * dist, direction[1] * dist)
                newPos = pos + movement
                if board.isValidPos(newPos) and board.notInFeministRange(self.side, newPos):
                    pieceAtNewPos = self.board.pieceAtPosition(newPos)
                    if not pieceAtNewPos:
                        yield Move(self, newPos)
                    else:
                        break
                else:
                    break
        movements = [C(2, 0), C(2, 1), C(2, 2), C(2, -1), C(2, -2), C(-2, 0), C(-2, 1), C(-2, 2),
                     C(-2, -1), C(-2, -2), C(-1, -2), C(0, -2), C(1, -2), C(-1, 2), C(0, 2), C(1, 2)]
        for movement in movements:
            newPos = pos + movement
            if board.isValidPos(newPos) and board.notInFeministRange(self.side, newPos):
                pieceAtNewPos = board.pieceAtPosition(newPos)
                if pieceAtNewPos and pieceAtNewPos.side == side and self.waitTime != 0:
                    move = Move(self, pos, pieceToCapture=pieceAtNewPos)
                    move.whip = True
                    yield move


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
                     if self.side else \
                    [C(0, -1), C(1, 0), C(-1, 0)]
        for movement in movements:
            newPos = pos + movement
            if board.isValidPos(newPos) and board.notInFeministRange(self.side, newPos):
                pieceAtNewPos = board.pieceAtPosition(newPos)
                if not pieceAtNewPos:
                    yield Move(self, newPos)
                elif pieceAtNewPos.side != self.side:
                    move = Move(self, newPos, pieceToCapture=pieceAtNewPos)
                    move.cripple = True
                    for cripplePos in [C(0, 1), C(1, 0), C(-1, 0), C(0, -1)]:
                        pieceAtCripplePos = self.pieceAtPosition(
                            newPos + cripplePos)
                        if pieceAtCripplePos:
                            if pieceAtCripplePos.side != self.side and \
                                    pieceAtCripplePos.stringRep not in ['H', 't']:
                                if cripplePos == C(0, 1):
                                    move.northPiece = pieceAtCripplePos
                                elif cripplePos == C(1, 0):
                                    move.eastPiece = pieceAtCripplePos
                                elif cripplePos == C(-1, 0):
                                    move.westPiece = pieceAtCripplePos
                                elif cripplePos == C(0, -1):
                                    move.southPiece = pieceAtCripplePos
                    yield move
