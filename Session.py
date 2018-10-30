import os

import Database as DB
import Game
from termcolor import colored as c


class Session():

    def __init__(self, isAdmin, firstName, username):
        self.isAdmin = isAdmin
        self.firstName = firstName
        self.username = username

    def consoleClear(self):
        os.system('cls')
        os.system('cls')

    def printMainMenu(self):
        self.consoleClear()
        if self.isAdmin:
            print(f'Welcome, {self.firstName} - Admin priveleges enabled.\n')
            print('A - Admin menu.')
        else:
            print(f'Welcome, {self.firstName}.\n')
        print('S - Start a game.')
        print('V - View your stats.')
        print('E - Edit account settings.')
        print('T - Test functions.')
        print('L - Log out.')
        return input('Option: ')[0].lower()

    def startSession(self):
        while True:
            choice = self.printMainMenu()
            if choice == 'l':
                return
            elif choice == 'a' and self.isAdmin:
                self.adminMenu()
            elif choice == 's':
                Game.main()
            elif choice == 'e':
                self.accountMenu()
            elif choice == 't':
                self.testing()
            else:
                getpass('Unable to parse input. Press enter to try again.')

    def printAdminMenu(self):
        self.consoleClear()
        print('- Admin Menu. -\n')
        print('1 - Edit/View all matches.')
        print('2 - Edit/View all users.')
        print('3 - Reset database.')
        print('0 - Back to main menu.')
        return int(input('Option: ')[0])

    def adminMenu(self):
        while True:
            adminChoice = self.printAdminMenu()
            if not adminChoice:
                return
            elif adminChoice == 1:
                print('match view thing')
            elif adminChoice == 2:
                self.adminUserMenu()
            elif adminChoice == 3:
                self.consoleClear()
                sure = input('Are you sure? (yN) ')
                if sure.lower() == 'y':
                    DB.bootDB()
                    getpass('Database rebooted. Press enter to continue.')

    def printTestMenu(self):
        self.consoleClear()
        print('- Testing. -\n')
        print('1 - getPiecesByUser')
        print('2 - getStats')
        print('0 - Return.')
        return int(input('Option: ')[0])

    def testing(self):
        while True:
            testChoice = self.printTestMenu()
            if not testChoice:
                return
            elif testChoice == 1:
                input(DB.getPiecesByUser(self.username))
            elif testChoice == 2:
                DB.getStats(self.username)

    def printAccountMenu(self):
        self.consoleClear()
        print('- Account editing. -\n')
        print('1 - Change your password.')
        print('2 - View security info.')
        print('3 - Edit account info.')
        print('0 - Back to main menu.')
        return int(input('Option: ')[0])

    def accountMenu(self):
        while True:
            menuChoice = self.printAccountMenu()
            if not menuChoice:
                return
            elif menuChoice == 1:
                DB.changePassword(self.username)
            elif menuChoice == 2:
                DB.viewSecurity(self.username)
            elif menuChoice == 3:
                DB.editUser(self.isAdmin, self.username)

    def printAdminUserMenu(self):
        self.consoleClear()
        print('- User Menu. -\n')
        print('1 - Add new user.')
        print('2 - Edit existing user.')
        print('3 - Search users.')
        print('0 - Back to admin menu.')
        return int(input('Option: ')[0])

    def adminUserMenu(self):
        while True:
            menuChoice = self.printAdminUserMenu()
            if not menuChoice:
                return
            elif menuChoice == 1:
                DB.createAccount()
            elif menuChoice == 2:
                while True:
                    self.consoleClear()
                    DB.printAllUsers()
                    Username = input(
                        '\nWhich user would you like to edit? (case-sensitive) ')
                    if DB.checkUsernameExists(Username):
                        DB.editUser(True, Username)
                        break
                    else:
                        getpass('Invalid username. Press enter to try again.')
            elif menuChoice == 3:
                DB.printAllUsers()


if __name__ == '__main__':
    userSession = Session(True, 'Alex', 'ashore')
    userSession.startSession()
