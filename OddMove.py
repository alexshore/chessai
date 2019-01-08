class Move:

    def __init__(self, piece, newPos, pieceToCapture=None):
        self.check = False
        self.checkMate = False
        self.staleMate = False
        self.kingSideCastle = False
        self.queenSideCastle = False
        self.castle = False
        self.suicide = False
        self.cripple = False
        self.northPiece = None
        self.southPiece = None
        self.eastPiece = None
        self.westPiece = None
        self.whip = False
        self.waitTimeDecrease = False
        self.piece = piece
        self.oldPos = piece.position
        self.newPos = newPos
        self.specialPos = None
        self.pieceToCapture = pieceToCapture
        self.specialMovePiece = None
        self.rookMove = None

        self.notation = self.getNotation()

    def getNotation(self):
        notation = ''

        if self.queenSideCastle:
            return '0-0-0'

        if self.kingSideCastle:
            return '0-0'

        newPosNotation = self.positionToHumanCoord(self.newPos if not \
                                        self.specialPos else self.specialPos)
        oldPosNotation = self.positionToHumanCoord(self.oldPos)
        captureNotation = 'x' if self.pieceToCapture else ''
        promotionNotation = '={}'.format(self.specialMovePiece.stringRep) \
                            if self.specialMovePiece else ''
        notation += oldPosNotation + captureNotation + newPosNotation + promotionNotation

        return notation

    def positionToHumanCoord(self, pos):
        transTable = str.maketrans('01234567', 'abcdefgh')
        notation = str(pos[0]).translate(transTable) + str(pos[1] + 1)
        return notation

    def __str__(self):
        self.notation = self.getNotation()
        displayString = 'Old Pos: {}'.format(self.oldPos) + \
                        'New Pos: {}'.format(self.newPos)
        if self.notation:
            displayString += 'Notation: {}'.format(self.notation)
        return displayString

    def __eq__(self, other):
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
        return hash((self.oldPos, self.newPos))

    def reverse(self):
        return Move(self.piece, self.piece.position,
                    pieceToCapture=self.pieceToCapture)
