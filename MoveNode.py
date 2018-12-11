from Move import Move


class MoveNode:

    def __init__(self, move, children, parent):
        self.move = move
        self.children = children
        self.parent = parent
        pointAdvantage = None
        depth = 1

    def __str__(self):
        stringRep = 'Move: {}'.format(self.move) + \
                    ' - Point Advantage: {}'.format(self.pointAdvantage) + \
                    ' - Checkmate: {}'.format(self.move.checkmate)
        stringRep += '\n'

        for child in self.children:
            stringRep += ' ' * self.getDepth() * 4
            stringRep += str(child)

        return stringRep

    def __gt__(self, other):
        if self.move.checkMate and not other.move.checkMate:
            return True
        if not self.move.checkMate and other.move.checkMate:
            return False
        if self.move.checkMate and other.move.checkMate:
            return False
        return self.pointAdvantage > other.pointAdvantage

    def __lt__(self, other):
        if self.move.checkMate and not other.move.checkMate:
            return False
        if not self.move.checkMate and other.move.checkMate:
            return True
        if self.move.staleMate and other.move.staleMate:
            return False
        return self.pointAdvantage < other.pointAdvantage

    def __eq__(self, other):
        if self.move.checkMate and other.move.checkMate:
            return True
        return self.pointAdvantage == other.pointAdvantage

    def getDepth(self):
        depth = 1
        highestNode = self
        while True:
            if highestNode.parent is not None:
                highestNode = highestNode.parent
                depth += 1
            else:
                return depth
