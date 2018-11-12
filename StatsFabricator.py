import datetime as dt
from random import *

import numpy as np
from faker import Faker

import Database as DB


def fabricate(n):
    fake = Faker()
    dates = [fake.date_this_year(before_today=True, after_today=False) for x in range(n)]
    dates.sort()
    for i in range(n):
        username = choice(DB.getAllUsernames())[0]
        date = dates[i].strftime('%d/%m/%Y')
        won = True if randint(0, 1) else False
        side = choice(['WHITE', 'BLACK'])
        depth = int(triangular(2, 4, 2))
        moves = int(triangular(25, 55, 36))
        piecesLeft = int(triangular(8, 22, 13))
        endPointAdvantage = int(triangular(8, 33, 23)) if won else int(
            triangular(-37, 8, -17))
        DB.addTestMatch(username, date, won, side, depth,
                        moves, piecesLeft, endPointAdvantage)


if __name__ == '__main__':
    fabricate(1000)
