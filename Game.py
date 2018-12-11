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
from termcolor import colored as colour

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
        columnHead = f"{colour(move.piece.stringRep, 'green')} at " + \
                     f"{colour(move.positionToHumanCoord(move.oldPos), 'cyan')}"
        if (pawns or move.piece.stringRep != 'p') and \
                [columnHead, move.piece] not in movesWithPiece[0]:
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
        columnHeader += f" {movesWithPiece[0][i][0]:>8} |"
        connector += '-' * 9 + '+'
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
            row += f"{rows[i][each]:>8} |"
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


def startGame(board, playerSide, ai, username):
    parser = InputParser(board, playerSide)
    while True:
        consoleClear()
        print(board)
        print()
        if board.isCheckMate():
            if board.currentSide == playerSide:
                print('Checkmate, you lost.')
                win = False
            else:
                print('Checkmate! You won!')
                win = True
            recordMatch(username, board, playerSide, win, ai)
            return
        if board.isStaleMate():
            print('Stalemate...')
            return
        if board.currentSide == playerSide:
            printPointAdvantage(board)
            move = None
            command = input('It\'s your move. '
                            'Type \'?\' for options: ').lower()
            if command == '?':
                printCommandOptions()
                continue
            elif command == 'l':
                listMoves(board, parser, False)
                continue
            elif command == 'll':
                listMoves(board, parser, True)
                continue
            elif command == 'u':
                undoLastTwoMoves(board)
                continue
            elif command == 'r':
                move = getRandomMove(board, parser)
            elif command == 'quit':
                return
            else:
                move = parser.parse(command)
            if move:
                makeMove(move, board)
            else:
                print('Couldn\'t parse input, enter a valid command or move.')
        elif board.currentSide == ai.side:
            print('AI thinking...')
            move = ai.getBestMove()
            move.notation = move.getNotation()
            makeMove(move, board)
            getpass('\nPress enter to continue.')
            if board.currentSide == ai.side:
                board.currentSide = playerSide


def main(username):
    consoleClear()
    board = Board()
    playerSide = askForPlayerSide()
    print()
    aiDepth = askForAIDepth()
    opponentAI = AI(board, not playerSide, aiDepth)
    startGame(board, playerSide, opponentAI, username)


if __name__ == '__main__':
    main('ashore')
