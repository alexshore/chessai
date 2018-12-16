from Bishop import Bishop
from Coordinate import Coordinate as C
from King import King
from Knight import Knight
from Move import Move
from Pawn import Pawn
from Piece import Piece
from Queen import Queen
from Rook import Rook
from termcolor import colored

WHITE = True
BLACK = False


class Board:
    def __init__(self, rookTest=False, queenTest=False, bishopTest=False, knightTest=False,
                 pawnTest=False, takeTest=False, castle=False, promotion=False):

        self.pieces = []
        self.history = []
        self.points = 0
        self.currentSide = WHITE
        self.movesMade = 0

        if not pawnTest and not rookTest and not queenTest and not bishopTest \
                and not knightTest and not castle and not takeTest and not promotion:
            self.pieces.extend([Rook(self, BLACK, C(0, 7)),
                                Knight(self, BLACK, C(1, 7)),
                                Bishop(self, BLACK, C(2, 7)),
                                King(self, BLACK, C(3, 7)),
                                Queen(self, BLACK, C(4, 7)),
                                Bishop(self, BLACK, C(5, 7)),
                                Knight(self, BLACK, C(6, 7)),
                                Rook(self, BLACK, C(7, 7))])
            for x in range(8):
                self.pieces.append(Pawn(self, BLACK, C(x, 6)))
                self.pieces.append(Pawn(self, WHITE, C(x, 1)))
            self.pieces.extend([Rook(self, WHITE, C(0, 0)),
                                Knight(self, WHITE, C(1, 0)),
                                Bishop(self, WHITE, C(2, 0)),
                                King(self, WHITE, C(3, 0)),
                                Queen(self, WHITE, C(4, 0)),
                                Bishop(self, WHITE, C(5, 0)),
                                Knight(self, WHITE, C(6, 0)),
                                Rook(self, WHITE, C(7, 0))])

        elif pawnTest:
            pawnToMove = Pawn(self, WHITE, C(2, 1))
            pawnToMove.movesMade = 0
            pawnToPromote = Pawn(self, WHITE, C(2, 6))
            pawnToPromote.movesMade = 4
            pieceToTake = Rook(self, BLACK, C(1, 7))
            whiteKing = King(self, WHITE, C(4, 0))
            blackKing = King(self, BLACK, C(4, 7))
            self.pieces.extend(
                [pawnToMove, pawnToPromote, whiteKing, pieceToTake, blackKing])

        elif rookTest:
            whiteRook = Rook(self, WHITE, C(4, 4))
            whiteKing = King(self, WHITE, C(3, 0))
            blackKing = King(self, BLACK, C(3, 7))
            self.pieces.extend([whiteRook, whiteKing, blackKing])

        elif queenTest:
            whiteQueen = Queen(self, WHITE, C(2, 2))
            whiteKing = King(self, WHITE, C(4, 0))
            blackQueen = Queen(self, BLACK, C(3, 6))
            blackKing = King(self, BLACK, C(3, 7))
            self.pieces.extend([whiteQueen, whiteKing, blackQueen, blackKing])

        elif bishopTest:
            whiteBishop = Bishop(self, WHITE, C(4, 4))
            whiteKing = King(self, WHITE, C(3, 0))
            blackKing = King(self, BLACK, C(3, 7))
            self.pieces.extend([whiteBishop, whiteKing, blackKing])

        elif knightTest:
            whiteKnight = Knight(self, WHITE, C(4, 4))
            whiteKing = King(self, WHITE, C(3, 0))
            blackKing = King(self, BLACK, C(3, 7))
            self.pieces.extend([whiteKnight, whiteKing, blackKing])

        elif promotion:
            pawnToPromote = Pawn(self, WHITE, C(1, 6))
            pawnToPromote.movesMade = 1
            kingWhite = King(self, WHITE, C(4, 0))
            kingBlack = King(self, BLACK, C(3, 2))
            self.pieces.extend([pawnToPromote, kingWhite, kingBlack])

        elif takeTest:
            pawnToTake = Pawn(self, BLACK, C(4, 4))
            whiteQueen = Queen(self, WHITE, C(2, 4))
            whiteBishop = Bishop(self, WHITE, C(2, 2))
            whiteRook = Rook(self, WHITE, C(4, 2))
            whiteKing = King(self, WHITE, C(1, 0))
            blackKing = King(self, BLACK, C(1, 7))
            self.pieces.extend(
                [pawnToTake,
                 whiteQueen,
                 whiteBishop,
                 whiteRook,
                 whiteKing,
                 blackKing])

        elif castle:
            kingWhite = King(self, WHITE, C(3, 0))
            kingBlack = King(self, BLACK, C(4, 7))
            kingSideRook = Rook(self, WHITE, C(0, 0))
            queenSideRook = Rook(self, WHITE, C(7, 0))
            self.pieces.extend(
                [kingWhite, kingBlack, kingSideRook, queenSideRook])

    def __str__(self):
        return self.wrapStringRep(self.makeStringRep(self.pieces))

    def undoLastMove(self):
        lastMove, pieceTaken = self.history.pop()

        if lastMove.castle:
            king = lastMove.piece
            rook = lastMove.specialMovePiece

            self.movePieceToPosition(king, lastMove.oldPos)
            self.movePieceToPosition(rook, lastMove.rookMove.oldPos)

            king.movesMade -= 1
            rook.movesMade -= 1

        elif lastMove.promotion:
            pawnPromoted = lastMove.piece
            promotedPiece = self.pieceAtPosition(lastMove.newPos)
            if pieceTaken:
                if pieceTaken.side == WHITE:
                    self.points += pieceTaken.value
                if pieceTaken.side == BLACK:
                    self.points -= pieceTaken.value
                self.addPieceToPosition(pieceTaken, lastMove.newPos)
                self.pieces.append(pieceTaken)
            self.pieces.remove(promotedPiece)
            self.pieces.append(pawnPromoted)
            if pawnPromoted.side == WHITE:
                self.points -= promotedPiece.value - 1
            elif pawnPromoted.side == BLACK:
                self.points += promotedPiece.value - 1
            pawnPromoted.movesMade -= 1

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
                if pieceToTake and pieceToTake.stringRep == 'K':
                    return True
        return False

    def isStaleMate(self):
        if len(self.getAllMovesLegal(self.currentSide)) == 0:
            for move in self.getAllMovesUnfiltered(not self.currentSide):
                pieceToTake = move.pieceToCapture
                if pieceToTake and pieceToTake.stringRep == 'K':
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
                    # pieceRep = piece.stringRep
                else:
                    pieceRep = colored('-', 'white')
                stringRep += pieceRep + ' '
            stringRep += '\n'
        stringRep = stringRep.strip()
        return stringRep

    def wrapStringRep(self, stringRep):
        sRep = '\n'.join(
            ['   a b c d e f g h   ', ' ' * 21] +
            ['%d  %s  %d' % (8 - r, s.strip(), 8 - r)
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

    def movePieceToPosition(self, piece, pos):
        piece.position = pos

    def addPieceToPosition(self, piece, pos):
        piece.position = pos

    def makeMove(self, move):
        self.addMoveToHistory(move)
        if move.castle:
            kingToMove = move.piece
            rookToMove = move.specialMovePiece
            self.movePieceToPosition(kingToMove, move.newPos)
            self.movePieceToPosition(rookToMove, move.rookMove.newPos)
            kingToMove.movesMade += 1
            rookToMove.movesMade += 1

        elif move.promotion:
            self.pieces.remove(move.piece)
            if move.pieceToCapture:
                self.pieces.remove(move.pieceToCapture)
            self.pieces.append(move.specialMovePiece)

            if move.piece.side == WHITE:
                self.points += move.specialMovePiece.value - 1
            if move.piece.side == BLACK:
                self.points -= move.specialMovePiece.value - 1

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

    def getAllMovesUnfiltered(self, side, includeKing=True):
        unfilteredMoves = []
        self.pieces.sort()
        for piece in self.pieces:
            if piece.side == side:
                if includeKing or piece.stringRep != 'K':
                    for move in piece.getPossibleMoves():
                        unfilteredMoves.append(move)
        return unfilteredMoves

    def testIfLegalBoard(self, side):
        for move in self.getAllMovesUnfiltered(side):
            pieceToTake = move.pieceToCapture
            if pieceToTake and pieceToTake.stringRep == 'K':
                return False
        return True

    def moveIsLegal(self, move):
        side = move.piece.side
        self.makeMove(move)
        isLegal = self.testIfLegalBoard(not side)
        self.undoLastMove()
        return isLegal

    def getAllMovesLegal(self, side):
        unfilteredMoves = list(self.getAllMovesUnfiltered(side))
        legalMoves = []
        for move in unfilteredMoves:
            if self.moveIsLegal(move):
                legalMoves.append(move)
        return legalMoves
