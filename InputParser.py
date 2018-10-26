import re


class InputParser:

    def __init__(self, board, side):
        self.board = board
        self.side = side

    def parse(self, humanInput):
        if re.compile('[a-z][1-8]x*[a-z][1-8]=[qbnr]').match(humanInput):
            newInput = humanInput[:-1] + humanInput[-1].upper()
        elif re.compile('[a-z][1-8]x*[a-z][1-8]').match(humanInput):
            newInput = humanInput
        else:
            newInput = humanInput
        for move in self.getLegalMovesWithNotation(self.side):
            if move.notation == newInput:
                return move

    def getLegalMovesWithNotation(self, side):
        moves = []
        for legalMove in self.board.getAllMovesLegal(side):
            legalMove.notation = legalMove.getNotation()
            moves.append(legalMove)
        return moves
