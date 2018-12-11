import random

from MoveNode import MoveNode

WHITE = True
BLACK = False


class AI:
    depth = 1
    board = None
    side = None
    movesAnalysed = 0

    def __init__(self, board, side, depth):
        self.board = board
        self.side = side
        self.depth = depth

    def generateMoveTree(self):
        moveTree = []
        for move in self.board.getAllMovesLegal(self.side):
            moveTree.append(MoveNode(move, [], None))

        for node in moveTree:
            self.board.makeMove(node.move)
            self.populateNodeChildren(node)
            self.board.undoLastMove()
        return moveTree

    def populateNodeChildren(self, node, debug=False):
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
        moveTree = self.generateMoveTree()
        bestMoves = self.bestMovesWithMoveTree(moveTree)
        randomBestMove = random.choice(bestMoves)
        randomBestMove.notation = randomBestMove.getNotation()
        return randomBestMove

    def bestMovesWithMoveTree(self, moveTree):
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
