# Importing required python modules.
import random
# Importing required custom modules.
from MoveNode import MoveNode

# Defines widely used global constants.
WHITE = True
BLACK = False


# Starts the definition of the class 'AI'.
class AI:
    # Defines the starting value for the attribute 'movesAnalysed'.
    movesAnalysed = 0

    def __init__(self, board, side, depth):
        # Initialising function of the 'AI' class. Creates and assigns given
        # values to the required attributes.
        self.board = board
        self.side = side
        self.depth = depth

    def generateMoveTree(self):
        # Function to generate the move tree. Goes through each possible legal
        # move and creates another 'MoveNode' object based off each move and
        # adds it to the array. It then goes through the array and makes each
        # move before from each node and goes through a recursive function
        # before returning the move tree list.
        moveTree = []
        for move in self.board.getAllMovesLegal(self.side):
            moveTree.append(MoveNode(move, [], None))
        for node in moveTree:
            self.board.makeMove(node.move)
            self.populateNodeChildren(node)
            self.board.undoLastMove()
        return moveTree

    def populateNodeChildren(self, node, debug=False):
        # A recursive function to carry on the population of the move tree
        # nodes. If there are no legal moves left and the only moves remaining
        # are checkmate moves or stalemate moves, it sets those specific
        # attributes to True or False respective of the outcome and returns as
        # the game is over after that move. Else, it goes through the recursion
        # of the doing the same thing with the next list of possible moves.
        # Whilst doing this it keeps track of the moves analysed so far as an
        # attribute of the 'AI' class.
        node.pointAdvantage = self.board.getPointAdvantageOfSide(self.side)
        node.depth = node.getDepth()
        if node.depth == self.depth:
            return
        side = self.board.currentSide
        legalMoves = self.board.getAllMovesLegal(side)
        if not legalMoves:
            if self.board.isCheckMate():
                node.move.checkmate = True
                return
            elif self.board.isStaleMate():
                node.move.stalemate = True
                node.pointAdvantage = 0
                return
            raise Exception()
        for move in legalMoves:
            self.movesAnalysed += 1
            node.children.append(MoveNode(move, [], node))
            self.board.makeMove(move)
            self.populateNodeChildren(node.children[-1])
            self.board.undoLastMove()

    def getOptimalPointAdvantageForNode(self, node):
        # A recursive function to determine the best point advantage possible
        # from any starting node path before returning it.
        if node.children:
            for child in node.children:
                child.pointAdvantage = \
                    self.getOptimalPointAdvantageForNode(child)
            if node.children[0].depth % 2 == 1:
                return max(node.children).pointAdvantage
            else:
                return min(node.children).pointAdvantage
        return node.pointAdvantage

    def getBestMove(self):
        # This function is the main function of the 'AI' class and kicks off
        # all the other functions. It runs the 'generateMoveTree' function,
        # it then finds the set of best moves from the move tree before
        # returning a random choice from the list.
        moveTree = self.generateMoveTree()
        bestMoves = self.bestMovesWithMoveTree(moveTree)
        randomBestMove = random.choice(bestMoves)
        randomBestMove.notation = randomBestMove.getNotation()
        return randomBestMove

    def bestMovesWithMoveTree(self, moveTree):
        # This function finds all the move paths from the move tree with the
        # highest point value by using the 'getOptimalPointAdvantageForNode'
        # function before returning the set of moves from each node.
        bestMoveNodes = []
        for moveNode in moveTree:
            moveNode.pointAdvantage = \
                self.getOptimalPointAdvantageForNode(moveNode)
            if not bestMoveNodes:
                bestMoveNodes.append(moveNode)
            elif moveNode > bestMoveNodes[0]:
                bestMoveNodes = [moveNode]
            elif moveNode == bestMoveNodes[0]:
                bestMoveNodes.append(moveNode)
        return [node.move for node in bestMoveNodes]
