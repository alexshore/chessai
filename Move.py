# Starts the definition of the class 'Move'.
class Move:

    def __init__(self, piece, newPos, pieceToCapture=None):
        # Initialising function of the 'Move' class. Creates and assigns
        # given values to the required attributes.
        self.check = False
        self.checkMate = False
        self.staleMate = False
        self.kingSideCastle = False
        self.queenSideCastle = False
        self.castle = False
        self.promotion = False

        self.piece = piece
        self.oldPos = piece.position
        self.newPos = newPos
        self.pieceToCapture = pieceToCapture
        self.specialMovePiece = None
        self.rookMove = None

        self.notation = self.getNotation()

    def getNotation(self):
        # Function designed generate a unique move generation string for a
        # given move object. String is based upon start and end coordinates
        # of a move and may have extra notation characters added depending
        # on what type of move it is. The only exception is castling moves
        # which have their own unique notationself.
        # After it generates the notation it returns the notation.
        notation = ''
        if self.queenSideCastle:
            return '0-0-0'
        if self.kingSideCastle:
            return '0-0'
        newPosNotation = self.positionToHumanCoord(self.newPos)
        oldPosNotation = self.positionToHumanCoord(self.oldPos)
        captureNotation = 'x' if self.pieceToCapture else ''
        promotionNotation = '={}'.format(self.specialMovePiece.stringRep) \
                            if self.specialMovePiece else ''
        notation += oldPosNotation + captureNotation + newPosNotation + promotionNotation
        return notation

    def positionToHumanCoord(self, pos):
        # Function to take in a 'Coordinate' object and translate it to a
        # 'human readable' coordinate string before returning it.
        transTable = str.maketrans('01234567', 'abcdefgh')
        notation = str(pos[0]).translate(transTable) + str(pos[1] + 1)
        return notation

    def __str__(self):
        # Custom function that generates a printable string for whenever
        # something tries to print the object. It compiles several pieces of
        # info about the 'Move' object and formats them together before
        # returning the string.
        displayString = 'Old Pos: {}'.format(self.oldPos) + \
                        'New Pos: {}'.format(self.newPos)
        if self.notation:
            displayString += 'Notation: {}'.format(self.notation)
        return displayString

    def __eq__(self, other):
        # Custom function that returns a boolean value depending on whether
        # certain attributes of two objects are the same as each other.
        if self.oldPos == other.oldPos and \
           self.newPos == other.newPos and \
           self.specialMovePiece == other.specialMovePiece:
            if not self.specialMovePiece:
                return True
            if self.specialMovePiece and \
               self.specialMovepiece == other.specialMovePiece:
                return True
            else:
                return False
        else:
            return False

    def __hash__(self):
        # Custom function to run a hashing function on a tuple of two given
        # 'Coordinate' objects.
        return hash((self.oldPos, self.newPos))

    def reverse(self):
        # Generates and returns another 'Move' object.
        return Move(self.piece, self.piece.position,
                    pieceToCapture=self.pieceToCapture)
