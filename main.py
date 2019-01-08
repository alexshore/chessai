# Importing required python modules.
import datetime as dt
import os
import re
from getpass import getpass
# Importing required custom modules.
import Database as DB
from Session import Session


def consoleClear():
    os.system('cls')
    os.system('cls')


def accountMenu():
    consoleClear()
    print('- Log-in Menu. -\n')
    print('1 - Log in.')
    print('2 - Create account.')
    print('3 - Forgotten password.')
    print('0 - Quit.')
    while True:
        try:
            return int(input('Option: ')[0])
        except:
            print('Invalid input. Enter a valid number only.\n')


def main():
    while True:
        menuChoice = accountMenu()
        if menuChoice == 1:
            data = [DB.logIn()]
            if data[0]:
                userSession = Session(data[0][1], data[0][2], data[0][3])
                userSession.startSession()
        elif menuChoice == 2:
            DB.createAccount()
            input('\nUser created. You may now login. Press enter to continue.')
        elif menuChoice == 3:
            DB.forgotPassword()
        elif not menuChoice:
            return
        else:
            print('Unable to parse input.')


if __name__ == '__main__':
    main()
