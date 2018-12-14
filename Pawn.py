from Bishop import Bishop
from Coordinate import Coordinate as C
from Knight import Knight
from Move import Move
from Piece import Piece
from Queen import Queen
from Rook import Rook

WHITE = True
BLACK = False


class Pawn(Piece):
    stringRep = 'p'
    value = 1

    def __init__(self, board, side, position, movesMade=0):
        super(Pawn, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        pos = self.position

        movement = C(0, 1) if self.side == WHITE else C(0, -1)
        advanceOnePos = pos + movement
        if self.board.isValidPos(advanceOnePos):
            if self.board.pieceAtPosition(advanceOnePos) is None:
                col = advanceOnePos[1]
                if col in [7, 0]:
                    piecesForPromotion = \
                        [Rook(self.board, self.side, advanceOnePos),
                         Knight(self.board, self.side, advanceOnePos),
                         Bishop(self.board, self.side, advanceOnePos),
                         Queen(self.board, self.side, advanceOnePos)]
                    for piece in piecesForPromotion:
                        move = Move(self, advanceOnePos)
                        move.promotion = True
                        piece.movesMade = self.movesMade
                        move.specialMovePiece = piece
                        yield move
                else:
                    yield Move(self, advanceOnePos)

        if self.movesMade == 0:
            advanceTwoPos = pos + movement + movement
            if self.board.isValidPos(advanceTwoPos):
                if self.board.pieceAtPosition(advanceTwoPos) is None and \
                        self.board.pieceAtPosition(advanceOnePos) is None:
                    yield Move(self, advanceTwoPos)

        movements = [C(1, 1), C(-1, 1)
                     ] if self.side == WHITE else [C(1, -1), C(-1, -1)]
        for movement in movements:
            newPos = self.position + movement
            if self.board.isValidPos(newPos):
                pieceToTake = self.board.pieceAtPosition(newPos)
                if pieceToTake and pieceToTake.side != self.side:
                    col = newPos[1]
                    if col in [7, 0]:
                        piecesForPromotion = \
                            [Rook(self.board, self.side, newPos),
                             Knight(self.board, self.side, newPos),
                             Bishop(self.board, self.side, newPos),
                             Queen(self.board, self.side, newPos)]
                        for piece in piecesForPromotion:
                            move = Move(
                                self, newPos, pieceToCapture=pieceToTake)
                            move.promotion = True
                            move.specialMovePiece = piece
                            yield move
                    else:
                        yield Move(self, newPos, pieceToCapture=pieceToTake)
