# Importing required custom modules.
from Move import Move

# Starts the definition of the class 'MoveNode'.
class MoveNode:

    def __init__(self, move, children, parent):
        # Initialising function of the 'MoveNode' class. Creates and assigns
        # given values to the required attributes.
        self.move = move
        self.children = children
        self.parent = parent
        pointAdvantage = None
        depth = 1

    def __str__(self):
        # Custom function that generates a printable string for whenever
        # something tries to print the object. It compiles several pieces of
        # info about the 'MoveNode' object and formats them together before
        # returning the string.
        stringRep = 'Move: {}'.format(self.move) + \
                    ' - Point Advantage: {}'.format(self.pointAdvantage) + \
                    ' - Checkmate: {}'.format(self.move.checkmate)
        stringRep += '\n'

        for child in self.children:
            stringRep += ' ' * self.getDepth() * 4
            stringRep += str(child)

        return stringRep

    def __gt__(self, other):
        # Custom function to determine whether a specific 'MovdNode' object is
        # worth more in value than another given object. Then returns a
        # boolean value.
        if self.move.checkMate and not other.move.checkMate:
            return True
        if not self.move.checkMate and other.move.checkMate:
            return False
        if self.move.checkMate and other.move.checkMate:
            return False
        return self.pointAdvantage > other.pointAdvantage

    def __lt__(self, other):
        # Custom function to determine whether a specific 'MovdNode' object is
        # worth less  in value than another given object. Then returns a
        # boolean value.
        if self.move.checkMate and not other.move.checkMate:
            return False
        if not self.move.checkMate and other.move.checkMate:
            return True
        if self.move.staleMate and other.move.staleMate:
            return False
        return self.pointAdvantage < other.pointAdvantage

    def __eq__(self, other):
        # Custom function to determine whether a specific 'MovdNode' object is
        # equal in value another given object. Then returns a boolean value.
        if self.move.checkMate and other.move.checkMate:
            return True
        return self.pointAdvantage == other.pointAdvantage

    def getDepth(self):
        # Simple function to find out how deep a node is from the top of the
        # move tree before returning the value.
        depth = 1
        highestNode = self
        while True:
            if highestNode.parent is not None:
                highestNode = highestNode.parent
                depth += 1
            else:
                return depth
