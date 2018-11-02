from random import *

import Database as DB


def fabricate(n):
    for i in range(n):
        username = choice(DB.getAllUsernames())[0]
        won = True if randint(0, 1) else False
        side = choice(['WHITE', 'BLACK'])
        depth = randint(2, 4)
        moves = randint(30, 50)
        piecesLeft = randint(8, 20)
        endPointAdvantage = randint(-10, 30) if won else randint(-30, 10)
        DB.addMatch(username, won, side, depth, moves,
                    piecesLeft, endPointAdvantage)


if __name__ == '__main__':
    fabricate(100)
