from Coordinate import Coordinate as C
from Move import Move
from Piece import Piece

WHITE = True
BLACK = False


class King(Piece):
    stringRep = 'K'
    value = 100

    def __init__(self, board, side, position, movesMade=0):
        super(King, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        pos = self.position
        movements = [C(0, 1), C(0, -1), C(1, 0), C(-1, 0),
                     C(1, 1), C(1, -1), C(-1, 1), C(-1, -1)]
        for movement in movements:
            newPos = pos + movement
            if self.board.isValidPos(newPos):
                pieceAtNewPos = self.board.pieceAtPosition(newPos)
                if self.board.pieceAtPosition(newPos) is None:
                    yield Move(self, newPos)
                elif pieceAtNewPos.side != self.side:
                    yield Move(self, newPos, pieceToCapture=pieceAtNewPos)

        if self.movesMade == 0:  # CASTLING, HIGHLY WIP
            inCheck = False
            kingSideCastleBlocked = False
            queenSideCastleBlocked = False
            kingSideCastleCheck = False
            queenSideCastleCheck = False
            kingSideRookMoved = True
            queenSideRookMoved = True

            kingSideCastlePositions = [self.position - C(1, 0),
                                       self.position - C(2, 0)]
            for position in kingSideCastlePositions:
                if self.board.pieceAtPosition(position):
                    kingSideCastleBlocked = True

            queenSideCastlePositions = [self.position + C(1, 0),
                                        self.position + C(2, 0),
                                        self.position + C(3, 0)]
            for position in queenSideCastlePositions:
                if self.board.pieceAtPosition(position):
                    queenSideCastleBlocked = True

            if kingSideCastleBlocked and queenSideCastleBlocked:
                return

            opponentMoves = self.board.getAllMovesUnfiltered(not self.side,
                                                             includeKing=False)

            for move in opponentMoves:
                if move.newPos == self.position:
                    inCheck = True
                    break
                if move.newPos == self.position - C(1, 0) or \
                        move.newPos == self.position - C(2, 0):
                    kingSideCastleCheck = True
                if move.newPos == self.position + C(1, 0) or \
                        move.newPos == self.position + C(2, 0):
                    queenSideCastleCheck = True

            kingSideRookPos = self.position - C(3, 0)
            kingSideRook = self.board.pieceAtPosition(kingSideRookPos) \
                if self.board.isValidPos(kingSideRookPos) else None
            if kingSideRook and \
                    kingSideRook.stringRep == 'R' and \
                    kingSideRook.movesMade == 0:
                kingSideRookMoved = False

            queenSideRookPos = self.position + C(4, 0)
            queenSideRook = self.board.pieceAtPosition(queenSideRookPos) \
                if self.board.isValidPos(kingSideRookPos) else None
            if queenSideRook and \
                    queenSideRook.stringRep == 'R' and \
                    queenSideRook.movesMade == 0:
                queenSideRookMoved = False

            if not inCheck:
                if not kingSideCastleBlocked and \
                        not kingSideCastleCheck and \
                        not kingSideRookMoved:
                    move = Move(self, self.position - C(2, 0))
                    move.specialMovePiece = self.board.pieceAtPosition(
                        kingSideRookPos)
                    rookMove = Move(move.specialMovePiece,
                                    self.position - C(1, 0))
                    move.kingSideCastle = True
                    move.rookMove = rookMove
                    yield move
                if not queenSideCastleBlocked and \
                        not queenSideCastleCheck and \
                        not queenSideRookMoved:
                    move = Move(self, self.position + C(2, 0))
                    move.specialMovePiece = self.board.pieceAtPosition(
                        queenSideRookPos)
                    rookMove = Move(move.specialMovePiece,
                                    self.position + C(1, 0))
                    move.queenSideCastle = True
                    move.rookMove = rookMove
                    yield move
