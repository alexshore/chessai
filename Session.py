import os

import Database as DB
import Game
from termcolor import colored as c
from getpass import getpass


class Session():

    def __init__(self, isAdmin, firstName, username):
        self.isAdmin = isAdmin
        self.firstName = firstName
        self.username = username

    def consoleClear(self):
        os.system('cls')
        os.system('cls')

    def getInput(self):
        while True:
            try:
                return int(input('Option: ')[0])
            except:
                print('Invalid input. Enter a valid number only.\n')

    def printMainMenu(self):
        self.consoleClear()
        if self.isAdmin:
            print(f'Welcome, {self.firstName} - Admin priveleges enabled.\n')
            print('0 - Admin menu.\n')
        else:
            print(f'Welcome, {self.firstName}.\n')
        print('1 - Start a game.')
        print('2 - View your stats.')
        print('3 - Edit account settings.')
        print('4 - Log out.')
        return self.getInput()

    def startSession(self):
        while True:
            choice = self.printMainMenu()
            if choice == 4:
                return
            elif choice == 0 and self.isAdmin:
                self.adminMenu()
            elif choice == 2:
                DB.getStats(self.username)
            elif choice == 1:
                Game.main(self.username)
            elif choice == 3:
                self.accountMenu()
            elif choice == 5:
                self.testingMenu()
            else:
                getpass('Unable to parse input. Press enter to re-try.')

    def printAdminMenu(self):
        self.consoleClear()
        print('- Admin Menu. -\n')
        print('1 - View recent matches.')
        print('2 - Edit/View all users.')
        print('3 - Reset database.')
        print('0 - Back to main menu.')
        return self.getInput()

    def adminMenu(self):
        while True:
            adminChoice = self.printAdminMenu()
            if not adminChoice:
                return
            elif adminChoice == 1:
                DB.printRecentMatches()
            elif adminChoice == 2:
                self.adminUserMenu()
            elif adminChoice == 3:
                self.consoleClear()
                sure = input('Are you sure? (yN) ')
                if sure.lower() == 'y':
                    DB.bootDB()
                    getpass('Database rebooted. Press enter to continue.')
            else:
                getpass('Unable to parse input. Press enter to re-try.')

    def printTestingMenu(self):
        self.consoleClear()
        print('- Testing Menu. -\n')
        print('1 - Get recent matches.')
        print('0 - Back to main menu.')
        return self.getInput()

    def testingMenu(self):
        while True:
            testChoice = self.printTestingMenu()
            if not testChoice:
                return
            elif testChoice == 1:
                input(DB.getRecentMatches())

    def printAccountMenu(self):
        self.consoleClear()
        print('- Account Editing. -\n')
        print('1 - Change your password.')
        print('2 - View security info.')
        print('3 - Edit account info.')
        print('0 - Back to main menu.')
        return self.getInput()

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
            else:
                getpass('Unable to parse input. Press enter to re-try.')

    def printAdminUserMenu(self):
        self.consoleClear()
        print('- User Menu. -\n')
        print('1 - Add new user.')
        print('2 - Edit existing user.')
        print('3 - Search users.')
        print('0 - Back to admin menu.')
        return self.getInput()

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
                    DB.printUsers()
                    Username = input(
                        '\nWhich user would you like to edit? (case-sensitive) ')
                    if DB.checkUsernameExists(Username):
                        DB.editUser(True, Username)
                        break
                    else:
                        getpass('Invalid username. Press enter to try again.')
            elif menuChoice == 3:
                self.userSearchMenu()
            else:
                getpass('Unable to parse input. Press enter to re-try.')

    def printUserSearchMenu(self):
        self.consoleClear()
        print('- User search menu. -\n')
        print('1 - Search by username.')
        print('2 - Search by firstname.')
        print('3 - Search by lastname.')
        print('4 - Search by creation date.')
        print('5 - Search by account type.')
        print('0 - Back to user menu.')
        return self.getInput()

    def userSearchMenu(self):
        while True:
            searchChoice = self.printUserSearchMenu()
            if not searchChoice:
                return
            elif searchChoice == 1:
                DB.searchByUsername()
            elif searchChoice == 2:
                DB.searchByFirstname()
            elif searchChoice == 3:
                DB.searchByLastname()
            elif searchChoice == 4:
                DB.searchByDate()
            elif searchChoice == 5:
                DB.searchByAdmin()
            else:
                getpass('Invalid input. Press enter to re-try.')


if __name__ == '__main__':
    userSession = Session(True, 'Alex', 'ashore')
    userSession.startSession()
