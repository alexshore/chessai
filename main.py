from Session import Session
from getpass import getpass
import re, os, Database as DB, datetime as dt

def consoleClear():
    os.system('cls')
    os.system('cls')

def accountMenu():
    consoleClear()
    print('- Log-in Menu. -\n')
    print('1 - Log in.')
    print('2 - Create account.')
    print('3 - Forgotten password.')
    print('4 - Reboot DB.')
    print('0 - Quit.')
    return int(input('Option: ')[0])

def main():
    while True:
        menuChoice = accountMenu()
        if menuChoice == 1:
            data = []
            data.append(DB.logIn())
            print(data)
            if data:
                userSession = Session(data[0][0], data[0][1], data[0][2])
                userSession.startSession()
        elif menuChoice == 2:
            DB.createAccount()
            input('User created. You may now login. Press enter to continue.')
        elif menuChoice == 3:
            DB.forgotPassword()
        elif menuChoice == 4:
            DB.bootDB()
            input('Database reset. Press enter to continue.')
        elif not menuChoice:
            return
        else:
            print('Unable to parse input.')

if __name__ == '__main__':
    main()
