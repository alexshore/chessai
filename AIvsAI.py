import os
import random
from getpass import *

import Database as DB
from AI import AI
from Bishop import Bishop
from Board import Board
from Coordinate import Coordinate as C
from InputParser import InputParser
from King import King
from Knight import Knight
from Move import Move
from Pawn import Pawn
from Piece import Piece
from Queen import Queen
from Rook import Rook

WHITE = True
BLACK = False


def consoleClear():
    os.system('cls')
    os.system('cls')


def recordMatch(username, board, side, won, ai):
    DB.addMatch(username, won, 'WHITE' if side else 'BLACK',
                ai.depth, board.movesMade, len(board.pieces),
                board.getPointAdvantageOfSide(side))


def askForPlayerSide():
    playerInput = input(
        'What side would you like to play as [wB]? ').lower()
    if 'w' in playerInput:
        print('You will play as white.')
        return WHITE
    else:
        print('You will play as black.')
        return BLACK


def askForAIDepth():
    depthInput = 2
    try:
        depthInput = int(input('How deep should the AI look for moves?\n'
                               + '-WARNING- values above 3 will be slow.\n'
                               + 'Leave blank for default: '))
    except:
        print('Invalid input, defaulting to 2.')
    return depthInput


def listMoves(board, parser, pawns):
    consoleClear()
    moves = parser.getLegalMovesWithNotation(board.currentSide)
    movesWithPiece = [[]]
    pieceRep = ''
    for move in moves:
        columnHead = move.piece.stringRep + \
            ' - {}'.format(move.positionToHumanCoord(move.oldPos))
        if (pawns or move.piece.stringRep != 'p') and [columnHead, move.piece] not in movesWithPiece[0]:
            movesWithPiece.append([])
            movesWithPiece[0].append([columnHead, move.piece])
    for piece in range(len(movesWithPiece[0])):
        for move in moves:
            if move.piece == movesWithPiece[0][piece][1]:
                movesWithPiece[piece + 1].append(move.notation)
    maxLen = 0
    for i in range(1, len(movesWithPiece)):
        length = len(movesWithPiece[i])
        maxLen = length if length > maxLen else maxLen
    for i in range(1, len(movesWithPiece)):
        if len(movesWithPiece[i]) < maxLen:
            for j in range(len(movesWithPiece[i]), maxLen):
                movesWithPiece[i].append('')
    columnHeader = "|"
    connector = '+'
    for i in range(len(movesWithPiece[0])):
        columnHeader += '{:>7} |'.format(movesWithPiece[0][i][0])
        connector += '-' * 8 + '+'
    print(connector + '\n' + columnHeader + '\n' + connector)
    rows = []
    for i in range(len(movesWithPiece[1])):
        rows.append([])
    for i in range(1, len(movesWithPiece)):
        for row in range(len(movesWithPiece[i])):
            rows[row].append(movesWithPiece[i][row])
    for i in range(len(rows)):
        row = "|"
        for each in range(len(rows[i])):
            row += "{:>7} |".format(rows[i][each])
        print(row)
    print(connector + '\n')
    getpass('Press enter to continue.')


def printMakeMove(move, board):
    print()
    print('Making move: {}'.format(move.notation))
    board.makeMove(move)


def getRandomMove(board, parser):
    legalMoves = board.getAllMovesLegal(board.currentSide)
    randomMove = random.choice(legalMoves)
    return randomMove


def printPointAdvantage(board):
    print('Currently, the point difference is: '
          + str(board.getPointAdvantageOfSide(board.currentSide)))


def undoLastTwoMoves(board):
    if len(board.history) >= 2:
        board.undoLastMove()
        board.undoLastMove()


def makeMove(move, board):
    print()
    print("Making move : " + move.notation)
    board.makeMove(move)


def printCommandOptions():
    consoleClear()
    print('- Options. -\n')
    undoOption = 'u - undo last move'
    printMovesOption = 'l - show all moves w/out pawns'
    printAllMovesOption = 'll - show all moves'
    randomMoveOption = 'r - make a random move'
    quitOption = 'quit - resign'
    moveOption = 'a3a5, c3xa5, 0-0, b7b8=R - make the move'
    options = [undoOption, printMovesOption, printAllMovesOption,
               randomMoveOption, quitOption, moveOption, '', ]
    print('\n'.join(options))
    getpass('Press enter to continue.')


def startGame(board, firstAI, otherAI):
    while True:
        counter = 1
        consoleClear()
        print(board)
        print()
        if board.isCheckMate():
            if board.currentSide == firstAI.side:
                print('Checkmate, firstAI won!')
            else:
                print('Checkmate, otherAI won!')
            input()
            break
        if board.isStaleMate():
            print('Stalemate...')
            return
        if board.currentSide == firstAI.side:
            print('FirstAI thinking...')
            move = firstAI.getBestMove(False)
            move.notation = move.getNotation()
            makeMove(move, board)
            if board.currentSide == firstAI.side:
                board.currentSide == otherAI.side
        elif board.currentSide == otherAI.side:
            print('AI thinking...')
            move = otherAI.getBestMove(False)
            move.notation = move.getNotation()
            makeMove(move, board)
            if board.currentSide == otherAI.side:
                board.currentSide == firstAI.side


def main():
    consoleClear()
    board = Board()
    print()
    firstAI = AI(board, False, 2)
    otherAI = AI(board, True, 2)
    startGame(board, firstAI, otherAI)


if __name__ == '__main__':
    main()
