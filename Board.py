# Importing required custom modules.
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

# Defines widely used global constants.
WHITE = True
BLACK = False


# Starts the definition of the class 'Board'.
class Board:

    def __init__(self):
        # The initialising function of the 'Board' class. Assigns all of the
        # attributes their starting values before creating all of the pieces
        # needed for the game.
        self.pieces = []
        self.history = []
        self.points = 0
        self.currentSide = WHITE
        self.movesMade = 0

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
                            Rook(self, WHITE, C(7, 0)),
                            Rook(self, BLACK, C(0, 7)),
                            Knight(self, BLACK, C(1, 7)),
                            Bishop(self, BLACK, C(2, 7)),
                            King(self, BLACK, C(3, 7)),
                            Queen(self, BLACK, C(4, 7)),
                            Bishop(self, BLACK, C(5, 7)),
                            Knight(self, BLACK, C(6, 7)),
                            Rook(self, BLACK, C(7, 7))])

    def __str__(self):
        # Calls a couple functions to create a wrapped representation of the
        # board in its current state. Then gets returned to a print statement.
        return self.wrapStringRep(self.makeStringRep(self.pieces))

    def undoLastMove(self):
        # This function handles the undoing of the last move. It extracts data
        # about the move from the history attribute and then runs through one
        # of the three following algorithms dependent on whether the move is a
        # special move or not. It then changes the side of the board.
        lastMove, pieceTaken = self.history.pop()

        # If the last move was a castling move, this handles that specific case.
        if lastMove.castle:
            king = lastMove.piece
            rook = lastMove.specialMovePiece

            self.movePieceToPosition(king, lastMove.oldPos)
            self.movePieceToPosition(rook, lastMove.rookMove.oldPos)

            king.movesMade -= 1
            rook.movesMade -= 1

        # If the last move was a pawn promotion, this fixes that specific case.
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

        # This handles all of the other cases where nothing special happened.
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
        # Checks whether any of the opposite sides pieces can take the king
        # on this next turn. If yes then returns True, else False. Essentially,
        # it is just checking for checkmate to end the game.
        if len(self.getAllMovesLegal(self.currentSide)) == 0:
            for move in self.getAllMovesUnfiltered(not self.currentSide):
                pieceToTake = move.pieceToCapture
                if pieceToTake and pieceToTake.stringRep == 'K':
                    return True
        return False

    def isStaleMate(self):
        # Checks whether any of the opposite sides pieces can take the king
        # on this next turn. If yes then returns False, else if there are no
        # moves to take the king it returns True which ends the game on a
        # stalemate status. Finally if there are still possible moves on the
        # player's side, it returns False and the game carries on.
        if len(self.getAllMovesLegal(self.currentSide)) == 0:
            for move in self.getAllMovesUnfiltered(not self.currentSide):
                pieceToTake = move.pieceToCapture
                if pieceToTake and pieceToTake.stringRep == 'K':
                    return False
            return True
        return False

    def makeStringRep(self, pieces):
        # This creates the raw printable board before it is passed to the
        # wrapping function. It goes through each 'spot' on the board and
        # depending on whether there is a piece assigned to said 'spot',
        # it will either add a simple white '-' or else add either a red
        # or a blue letter depending on the type of the piece.
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
        # This wraps the board representation thats created in the previous
        # function. It separates the lines of the representation and returns
        # them with some fancy formatting.
        sRep = '\n'.join(
            ['   a b c d e f g h   ', ' ' * 21] +
            ['%d  %s  %d' % (8 - r, s.strip(), 8 - r)
               for r, s in enumerate(stringRep.split('\n'))] +
            [' ' * 21, '   a b c d e f g h   ']
        ).rstrip()
        return sRep

    def isValidPos(self, pos):
        # Simply checks a given coordinate to make sure it is within the
        # bounds of the board, i.e. 8x8.
        if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7:
            return True
        else:
            return False

    def pieceAtPosition(self, pos, debug=False):
        # Loops through each piece and references its position against
        # a given position.
        for piece in self.pieces:
            if piece.position == pos:
                return piece

    def movePieceToPosition(self, piece, pos):
        # Changes the position attribute of a given piece to a given coordinate.
        piece.position = pos

    def addPieceToPosition(self, piece, pos):
        # Changes the position attribute of a given piece to a given coordinate.
        piece.position = pos

    def makeMove(self, move):
        # This procedure adds the move to be made to the history attribute then
        # enacts the given move upon the board dependent on the specificity of
        # the move e.g. whether it is a regular non-special move, a castling
        # move or a promotion move. It then changes the side of the board.
        self.addMoveToHistory(move)
        # This if statement handles the case of a castling move.
        if move.castle:
            kingToMove = move.piece
            rookToMove = move.specialMovePiece
            self.movePieceToPosition(kingToMove, move.newPos)
            self.movePieceToPosition(rookToMove, move.rookMove.newPos)
            kingToMove.movesMade += 1
            rookToMove.movesMade += 1

        # This if statement handles the case of a pawn promotion.
        elif move.promotion:
            self.pieces.remove(move.piece)
            if move.pieceToCapture:
                self.pieces.remove(move.pieceToCapture)
            self.pieces.append(move.specialMovePiece)

            if move.piece.side == WHITE:
                self.points += move.specialMovePiece.value - 1
            if move.piece.side == BLACK:
                self.points -= move.specialMovePiece.value - 1

        # This handles all the other types of moves.
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
        # Adds the entire object of the move along with the piece taken by said
        # move to the history attribute.
        pieceTaken = move.pieceToCapture
        if pieceTaken:
            self.history.append([move, pieceTaken])
        else:
            self.history.append([move, None])

    def getPointValueOfSide(self, side):
        # Loops through all remaining pieces of a specific side and adds up
        # the points of said pieces before returning the value.
        points = 0
        for piece in self.pieces:
            if piece.side == side:
                points += piece.value
        return points

    def getPointAdvantageOfSide(self, side):
        # Gets the point value of both sides and subtracts the opposite sides
        # points from the players points and returns it.
        pointAdvantage = self.getPointValueOfSide(side) - \
            self.getPointValueOfSide(not side)
        return pointAdvantage

    def getAllMovesUnfiltered(self, side, includeKing=True):
        # Runs through each piece in the pieces array attribute of the board
        # and then creates a list of each possible move that the current pieces
        # can make before returning the list.
        unfilteredMoves = []
        self.pieces.sort()
        for piece in self.pieces:
            if piece.side == side:
                if includeKing or piece.stringRep != 'K':
                    for move in piece.getPossibleMoves():
                        unfilteredMoves.append(move)
        return unfilteredMoves

    def testIfLegalBoard(self, side):
        # Checks if any of the moves of a given side have a piece to capture
        # and whether that piece is a 'King' or not. If there are no pieces
        # that can take the king. It returns True which indicates a legal board.
        # Else it returns False which indicates an illegal board.
        for move in self.getAllMovesUnfiltered(side):
            pieceToTake = move.pieceToCapture
            if pieceToTake and pieceToTake.stringRep == 'K':
                return False
        return True

    def moveIsLegal(self, move):
        # Makes a given move, then checks if the board is legal after said move,
        # it then returns the boolean isLegal value after undoing the made move.
        side = move.piece.side
        self.makeMove(move)
        isLegal = self.testIfLegalBoard(not side)
        self.undoLastMove()
        return isLegal

    def getAllMovesLegal(self, side):
        # Retrieves a list of all moves of a given side then creates a list of
        # all possible legal moves the player can make before returning the list.
        unfilteredMoves = list(self.getAllMovesUnfiltered(side))
        legalMoves = []
        for move in unfilteredMoves:
            if self.moveIsLegal(move):
                legalMoves.append(move)
        return legalMoves
