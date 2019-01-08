from Coordinate import Coordinate as C
from OddMove import Move
from OddPieces import (AbusiveFather, AngryFeminist, Helicopter, NeckBeard,
                       Piece, PornAddict, SuicideBomber, TikTokFan)
from termcolor import colored

WHITE = True
BLACK = False


class Board:
    def __init__(self, bomberTest=False, helicopterTest=False,
                 feministTest=False, tikTokTest=0, addictTest=False,
                 beardTest=False, fatherTest=True, slowTest=False):
        self.pieces = []
        self.history = []
        self.points = 0
        self.currentSide = WHITE
        self.movesMade = 0

        if not bomberTest and not helicopterTest and \
                not feministTest and not tikTokTest and \
                not addictTest and not beardTest and \
                not fatherTest and not slowTest:
            self.pieces.extend([SuicideBomber(self, BLACK, C(0, 7)),
                                AbusiveFather(self, BLACK, C(2, 7)),
                                AngryFeminist(self, BLACK, C(3, 7)),
                                Helicopter(self, BLACK, C(4, 7)),
                                PornAddict(self, BLACK, C(5, 7)),
                                SuicideBomber(self, BLACK, C(7, 7))])
            for x in range(8):
                self.pieces.append(TikTokFan(self, BLACK, C(x, 6)))
                self.pieces.append(TikTokFan(self, WHITE, C(x, 1)))
            self.pieces.extend([SuicideBomber(self, WHITE, C(0, 0)),
                                PornAddict(self, WHITE, C(2, 0)),
                                AngryFeminist(self, WHITE, C(3, 0)),
                                Helicopter(self, WHITE, C(4, 0)),
                                AbusiveFather(self, WHITE, C(5, 0)),
                                SuicideBomber(self, WHITE, C(7, 0))])
        elif feministTest and not slowTest:
            self.pieces.extend([AngryFeminist(self, WHITE, C(3, 0)),
                                AngryFeminist(self, BLACK, C(3, 7))])
        elif fatherTest and not slowTest:
            self.pieces.extend([AngryFeminist(self, WHITE, C(3, 0)),
                                AngryFeminist(self, BLACK, C(3, 7)),
                                AbusiveFather(self, WHITE, C(3, 1)),
                                TikTokFan(self, BLACK, C(4, 3)),
                                TikTokFan(self, BLACK, C(2, 3))])
        if slowTest:
            if feministTest:
                self.pieces.extend([AngryFeminist(self, WHITE, C(3, 0)),
                                    AngryFeminist(self, BLACK, C(3, 7))])
            if bomberTest:
                self.pieces.extend([SuicideBomber(self, WHITE, C(0, 0)),
                                    SuicideBomber(self, BLACK, C(7, 7))])
            if helicopterTest:
                self.pieces.extend([Helicopter(self, WHITE, C(4, 0)),
                                    Helicopter(self, BLACK, C(4, 7))])
            if fatherTest:
                self.pieces.extend([AbusiveFather(self, WHITE, C(2, 0)),
                                    AbusiveFather(self, BLACK, C(2, 7))])
            if tikTokTest:
                for i in range(tikTokTest):
                    self.pieces.extend([TikTokFan(self, WHITE, C(i, 1)),
                                        TikTokFan(self, BLACK, C(7-i, 6))])


    def __str__(self):
        return self.wrapStringRep(self.makeStringRep(self.pieces))

    def makeMove(self, move):
        for piece in self.pieces:
            if piece.stringRep == 'A' and piece.side == self.currentSide and piece.waitTime != 0:
                piece.waitTime -= 1
                if piece.side:
                    move.whiteTimeDecrease = True
                else:
                    move.blackTimeDecrease = True
        self.addMoveToHistory(move)
        if move.cripple:
            pieceToMove = move.piece
            pieceToTake = move.pieceToCapture
            if move.northPiece:
                self.pieces.remove(move.northPiece)
            if move.southPiece:
                self.pieces.remove(move.southPiece)
            if move.westPiece:
                self.pieces.remove(move.westPiece)
            if move.eastPiece:
                self.pieces.remove(move.eastPiece)
            self.pieces.remove(pieceToMove)
            self.pieces.remove(pieceToTake)

        elif move.suicide:
            pieceToMove = move.piece
            pieceToTake = move.pieceToCapture
            if move.specialMovePiece:
                self.pieces.remove(specialMovePiece)
            self.pieces.remove(pieceToMove)
            self.pieces.remove(pieceToTake)

        elif move.whip:
            pieceToMove = move.piece
            pieceToTake = move.pieceToCapture
            self.pieces.remove(pieceToTake)
            pieceToMove.movesMade += 1
            pieceToMove.waitTime += 2

        else:
            pieceToMove = move.piece
            pieceToTake = move.pieceToCapture
            if pieceToTake:
                if pieceToTake.side == WHITE:
                    self.points -= pieceToTake.value
                if pieceToTake.side == BLACK:
                    self.points += pieceToTake.value
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

    def undoLastMove(self):
        lastMove, pieceTaken = self.history.pop()
        if lastMove.waitTimeDecrease:
            for piece in self.pieces:
                if piece.stringRep == 'A' and piece.side != self.currentSide:
                    piece.waitTime += 1
        if lastMove.whip:
            self.addPieceToPosition(pieceTaken, lastMove.specialPos)
            if pieceTaken.side == WHITE:
                self.points += pieceTaken.value
            if pieceTaken.side == BLACK:
                self.points -= pieceTaken.value
            self.pieces.append(pieceTaken)
            lastMove.piece.movesMade -= 1
            lastMove.piece.waitTime = 0

        elif lastMove.suicide:
            piece = lastMove.piece
            self.pieces.append(piece)
            if lastMove.specialMovePiece:
                self.pieces.append(lastMove.specialMovePiece)
            if lastMove.pieceToCapture:
                self.pieces.append(lastMove.pieceToCapture)

        elif lastMove.cripple:
            piece = lastMove.piece
            self.addPieceToPosition(piece, lastMove.oldPos)
            if lastMove.northPiece:
                self.pieces.remove(self.pieceAtPosition(lastMove.northPiece.position))
                self.pieces.append(lastMove.northPiece)
            elif lastMove.southPiece:
                self.pieces.remove(self.pieceAtPosition(lastMove.southPiece.position))
                self.pieces.append(lastMove.southPiece)
            elif lastMove.eastPiece:
                self.pieces.remove(self.pieceAtPosition(lastMove.eastPiece.position))
                self.pieces.append(lastMove.eastPiece)
            elif lastMove.westPiece:
                self.pieces.remove(self.pieceAtPosition(lastMove.westPiece.position))
                self.pieces.append(lastMove.westPiece)

        else:
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
            [' ' * 21, '   a b c d e f g h   ']
        ).rstrip()
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
            pieceAtPos = self.pieceAtPosition(pos + movement)
            if pieceAtPos:
                if pieceAtPos.stringRep == 'F' and pieceAtPos.side != side:
                    return False
        return True

    def scanForTikTok(self, side, pos):
        movements = [C(1, 0), C(-1, 0)]
        i = 0
        for movement in movements:
            try:
                pieceAtPos = self.pieceAtPosition(pos + movement)
            except:
                print(pos)
                print(f'pos type: {type(pos)}, mov type: {type(movement)}')
            if pieceAtPos:
                if pieceAtPos.stringRep == 't' and pieceAtPos.side == side:
                    i += 1
        return i + 1

    def movePieceToPosition(self, piece, pos):
        piece.position = pos

    def addPieceToPosition(self, piece, pos):
        piece.position = pos

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

    def getAllMovesUnfiltered(self, side):
        unfilteredMoves = []
        for piece in self.pieces:
            if piece.side == side:
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
        if move.piece.stringRep != 'A':
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
