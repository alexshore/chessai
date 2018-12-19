import os
import random
from getpass import *

import Database as DB
from Coordinate import Coordinate as C
from OddBoard import Board
from OddMove import Move
from OddParser import InputParser
from OddPieces import (AbusiveFather, AngryFeminist, Helicopter, NeckBeard,
                       Piece, PornAddict, SuicideBomber, TikTokFan)
from termcolor import colored as colour

WHITE = True
BLACK = False


def consoleClear():
    os.system('cls')
    os.system('cls')


def askForPlayerSide():
    playerInput = input(
        'What side would you like to play as [wB]? ').lower()
    if 'w' in playerInput:
        print('You will play as white.')
        return WHITE
    else:
        print('You will play as black.')
        return BLACK


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
    print('Currently, the point difference is: ' +
          str(board.getPointAdvantageOfSide(board.currentSide)))

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
    printMovesOption = 'l - show all moves w/out pawns'
    printAllMovesOption = 'll - show all moves'
    quitOption = 'quit - resign'
    moveOption = 'a3a5, c3xa5, 0-0, b7b8=R - make the move'
    options = [printMovesOption, printAllMovesOption,
               quitOption, moveOption, '', ]
    print('\n'.join(options))
    getpass('Press enter to continue.')


def printWaitTime(board):
    for piece in board.pieces:
        if piece.stringRep == 'A':
            getpass(f'father wait time: {piece.waitTime}')


def startGame(board):
    whiteParser = InputParser(board, WHITE)
    blackParser = InputParser(board, BLACK)
    while True:
        consoleClear()
        print(board)
        print()
        if board.isCheckMate():
            if board.currentSide:
                print('Checkmate,  lost.')
            else:
                print('Checkmate! You won!')
        if board.isStaleMate():
            print('Stalemate...')
            return
        if board.currentSide:
            printPointAdvantage(board)
            move = None
            command = input('It\'s your move, white boy. '
                            'Type \'?\' for options: ').lower()
            if command == '?':
                printCommandOptions()
                continue
            elif command == 'l':
                listMoves(board, whiteParser, False)
                continue
            elif command == 'u':
                undoLastTwoMoves(board)
                continue
            elif command == 'test':
                printWaitTime(board)
                continue
            elif command == 'll':
                listMoves(board, whiteParser, True)
                continue
            elif command == 'quit':
                return
            else:
                move = whiteParser.parse(command)
            if move:
                makeMove(move, board)
            else:
                getpass('Invalid input. Try again.')
        elif not board.currentSide:
            printPointAdvantage(board)
            move = None
            command = input('It\'s your move, black man. '
                            'Type \'?\' for options: ').lower()
            if command == '?':
                printCommandOptions()
                continue
            elif command == 'l':
                listMoves(board, blackParser, False)
                continue
            elif command == 'll':
                listMoves(board, blackParser, True)
                continue
            elif command == 'test':
                printWaitTime(board)
                continue
            elif command == 'quit':
                return
            else:
                move = blackParser.parse(command)
            if move:
                makeMove(move, board)
            else:
                getpass('Invalid input. Try again.')


def main():
    consoleClear()
    board = Board()
    startGame(board)


if __name__ == '__main__':
    main()
