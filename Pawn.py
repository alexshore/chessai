# Importing required custom modules.
from Bishop import Bishop
from Coordinate import Coordinate as C
from Knight import Knight
from Move import Move
from Piece import Piece
from Queen import Queen
from Rook import Rook

# Defines widely used global constants.
WHITE = True
BLACK = False


# Starts the definition of the class 'Pawn' using inheritence.
class Pawn(Piece):
    # Defines the string representation and the piece value.
    stringRep = 'p'
    value = 1

    def __init__(self, board, side, position, movesMade=0):
        # Initialising function of the 'Pawn' class. Creates and assigns
        # given values to the required attributes. Does this through both
        # regular variable assignment and also through inheritance.
        super(Pawn, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        # Function run to yield a group of all possible legal and illegal
        # 'Move' objects to the calling function. Does this by running through
        # a list of movements and testing for valid moves before yielding them.
        # Also handles the promotion of pieces and the ability for a piece to
        # move two spaces forward on its first move.
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
