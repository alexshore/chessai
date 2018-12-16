from Coordinate import Coordinate as C
from OddMove import Move
from OddPieces import (AbusiveFather, Feminist, Helicopter, PornAddict,
                       SuicideBomber, Piece)
from termcolor import colored

WHITE = True
BLACK = False


class Board:
    def __init__(self, helicopterTest=False, feministTest=False, addictTest=False,
                 fatherTest=False, blankTest=False, otherTest=False):

        self.pieces = []
        self.history = []
        self.points = 0
        self.currentSide = WHITE
        self.movesMade = 0

        if not helicopterTest and not feministTest and not addictTest and not fatherTest  \
                and not blankTest and not otherTest:
            self.pieces.extend([SuicideBomber(self, WHITE, C(0, 0)),
                                AbusiveFather(self, WHITE, C(1, 0)),
                                Helicopter(self, WHITE, C(3, 0)),
                                Feminist(self, WHITE, C(4, 0)),
                                PornAddict(self, WHITE, C(6, 0)),
                                SuicideBomber(self, WHITE, C(7, 0))])
            self.pieces.extend([SuicideBomber(self, BLACK, C(0, 7)),
                                PornAddict(self, BLACK, C(1, 7)),
                                Helicopter(self, BLACK, C(3, 7)),
                                Feminist(self, BLACK, C(4, 7)),
                                AbusiveFather(self, BLACK, C(6, 7)),
                                SuicideBomber(self, BLACK, C(7, 7))])

    def __str__(self):
        return self.wrapStringRep(self.makeStringRep(self.pieces))

    def undoLastMove(self):
        lastMove, pieceTaken = self.history.pop()
        pieceToMoveBack = lastMove.piece
        self.movePieceToPosition(pieceToMoveBack, lastMove.oldPos)
        if pieceTaken:
            if pieceTaken.side == WHITE:
                self.points += pieceTaken.value
            if pieceTaken.side == BLACK:
                self.points -= pieceTaken.value
            self.addPieceToPosition(pieceTaken, lastMove.newPos)
            self.pieces.append(pieceTaken)
        pieceToMoveBack.movesMade -= 1
        self.movesMade -= 1
        self.currentSide = not self.currentSide

    def isCheckMate(self):
        if len(self.getAllMovesLegal(self.currentSide)) == 0:
            for move in self.getAllMovesUnfiltered(not self.currentSide):
                pieceToTake = move.pieceToCapture
                if pieceToTake and pieceToTake.stringRep == 'F':
                    return True
        return False

    def isStaleMate(self):
        if len(self.getAllMovesLegal(self.currentSide)) == 0:
            for move in self.getAllMovesUnfiltered(not self.currentSide):
                pieceToTake = move.pieceToCapture
                if pieceToTake and pieceToTake.stringRep == 'F':
                    return False
            return True
        return False

    def makeStringRep(self, pieces):
        stringRep = ''
        for y in range(7, -1, -1):
            for x in range(8):
                piece = None
                for p in pieces:
                    if p.position == C(x, y):
                        piece = p
                        break
                if piece:
                    side = piece.side
                    color = 'cyan' if side == WHITE else 'red'
                    pieceRep = colored(piece.stringRep, color)
                else:
                    pieceRep = colored('-', 'white')
                stringRep += pieceRep + ' '
            stringRep += '\n'
        stringRep = stringRep.strip()
        return stringRep

    def wrapStringRep(self, stringRep):
        sRep = '\n'.join(
            ['   a b c d e f g h   ', ' ' * 21]
            + ['%d  %s  %d' % (8 - r, s.strip(), 8 - r)
             for r, s in enumerate(stringRep.split('\n'))] +
            [' ' * 21, '   a b c d e f g h   ']).rstrip()
        return sRep

    def isValidPos(self, pos):
        if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7:
            return True
        else:
            return False

    def pieceAtPosition(self, pos, debug=False):
        for piece in self.pieces:
            if piece.position == pos:
                return piece

    def notInFeministRange(self, side, pos):
        movements = [C(0, 1), C(-1, -1), C(1, 0), C(-1, 0),
                     C(1, 1), C(1, -1), C(-1, 1), C(0, -1)]
        for movement in movements:
            pieceAtRange = self.pieceAtPosition(pos + movement)
            if pieceAtRange and pieceAtRange.stringRep == 'F' and pieceAtRange.side != side:
                return False
        return True

    def movePieceToPosition(self, piece, pos):
        piece.position = pos

    def addPieceToPosition(self, piece, pos):
        piece.position = pos

    def makeMove(self, move):
        self.addMoveToHistory(move)

        if move.cripple:
            pieceToMove = move.piece
            pieceToTake = move.pieceToCapture
            newPos = move.newPos
            for cripplePos in [C(0, 1), C(1, 0), C(-1, 0), C(0, -1)]:
                pieceAtCripplePos = self.pieceAtPosition(newPos + cripplePos)
                if pieceAtCripplePos and pieceAtCripplePos.side != self.side:
                    self.pieces.remove(pieceAtCripplePos)
                    if pieceToTake.stringRep != 'S':
                        self.pieces.append(PornAddict(
                            self, self.side, newPos + cripplePos))
            self.pieces.remove(pieceToMove)
            self.pieces.remove(pieceToTake)

        else:
            pieceToMove = move.piece
            pieceToTake = move.pieceToCapture
            if pieceToTake:
                if pieceToTake.side == WHITE:
                    self.points -= pieceToTake.value
                if pieceToTake.side == BLACK:
                    self.points += pieceToTake.value
                if pieceToTake.stringRep == 'S':
                    self.pieces.remove(pieceToMove)
                self.pieces.remove(pieceToTake)
            self.movePieceToPosition(pieceToMove, move.newPos)
            pieceToMove.movesMade += 1
        self.movesMade += 1
        self.currentSide = not self.currentSide

    def addMoveToHistory(self, move):
        pieceTaken = move.pieceToCapture
        if pieceTaken:
            self.history.append([move, pieceTaken])
        else:
            self.history.append([move, None])

    def getPointValueOfSide(self, side):
        points = 0
        for piece in self.pieces:
            if piece.side == side:
                points += piece.value
        return points

    def getPointAdvantageOfSide(self, side):
        pointAdvantage = self.getPointValueOfSide(side) - \
            self.getPointValueOfSide(not side)
        return pointAdvantage

    def getAllMovesUnfiltered(self, side, includeFeminist=True):
        unfilteredMoves = []
        self.pieces.sort()
        for piece in self.pieces:
            if piece.side == side:
                if includeFeminist or piece.stringRep != 'F':
                    for move in piece.getPossibleMoves():
                        unfilteredMoves.append(move)
        return unfilteredMoves

    def testIfLegalBoard(self, side):
        for move in self.getAllMovesUnfiltered(side):
            pieceToTake = move.pieceToCapture
            if pieceToTake and pieceToTake.stringRep == 'F':
                return False
        return True

    def moveIsLegal(self, move):
        side = move.piece.side
        if move.piece.stringRep != 'S' and move.piece.pieceToCapture.stringRep != 'S':
            self.makeMove(move)
            isLegal = self.testIfLegalBoard(not side)
            self.undoLastMove()
            return isLegal
        else:
            return True

    def getAllMovesLegal(self, side):
        unfilteredMoves = list(self.getAllMovesUnfiltered(side))
        legalMoves = []
        for move in unfilteredMoves:
            if self.moveIsLegal(move):
                legalMoves.append(move)
        return legalMoves
