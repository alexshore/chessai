# Importing required custom modules.
from Coordinate import Coordinate as C
from Move import Move
from Piece import Piece

# Defines widely used global constants.
WHITE = True
BLACK = False


# Starts the definition of the class 'King' using inheritence.
class King(Piece):
    # Defines the string representation and the piece value.
    stringRep = 'K'
    value = 100

    def __init__(self, board, side, position, movesMade=0):
        # Initialising function of the 'King' class. Creates and assigns
        # given values to the required attributes. Does this through both
        # regular variable assignment and also through inheritance.
        super(King, self).__init__(board, side, position)
        self.movesMade = movesMade

    def getPossibleMoves(self):
        # Function run to yield a group of all possible legal and illegal
        # 'Move' objects to the calling function. Does this by running through
        # a list of movements and testing for valid moves before yielding them.
        # Also goes through another special algorithm to test if it can also
        # perform another special type of move, a 'castle'.
        pos = self.position
        movements = [C(0, 1), C(-1, -1), C(1, 0), C(-1, 0),
                     C(1, 1), C(1, -1), C(-1, 1), C(0, -1)]
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
                    move.castle = True
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
                    move.castle = True
                    yield move
