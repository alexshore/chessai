import os

import Database as DB
import Game
from termcolor import colored as c
from getpass import getpass


class Session:

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
            print('9 - Admin menu.\n')
        else:
            print(f'Welcome, {self.firstName}.\n')
        print('1 - Start a game.')
        print('2 - View your stats.')
        print('3 - Edit account settings.')
        print('0 - Log out.')
        return self.getInput()

    def startSession(self):
        while True:
            choice = self.printMainMenu()
            if not choice:
                return
            elif choice == 9 and self.isAdmin:
                if not self.adminMenu():
                    return
            elif choice == 1:
                Game.main(self.username)
            elif choice == 2:
                DB.getStats(self.username)
            elif choice == 3:
                if not self.accountMenu():
                    return
            elif choice == 5:
                self.testingMenu()
            else:
                getpass('Unable to parse input. Press enter to re-try.')

    def printAdminMenu(self):
        self.consoleClear()
        print('- Admin Menu. -\n')
        print('1 - Matches menu.')
        print('2 - Users menu.')
        print('3 - View stats.')
        print('0 - Back to main menu.')
        return self.getInput()

    def adminMenu(self):
        while True:
            adminChoice = self.printAdminMenu()
            if not adminChoice:
                return True
            elif adminChoice == 1:
                self.adminMatchesMenu()
            elif adminChoice == 2:
                if not self.adminUserMenu():
                    return False
            elif adminChoice == 3:
                DB.getUsersStats()
            else:
                getpass('Unable to parse input. Press enter to re-try.')

    def printAdminMatchesMenu(self):
        self.consoleClear()
        print('- Matches Menu. \n')
        print('1 - View all matches.')
        print('2 - View matches by username.')
        print('3 - View matches by date of match.')
        print('4 - Reset matches.')
        print('0 - Back to admin menu.')
        return self.getInput()

    def adminMatchesMenu(self):
        while True:
            matchChoice = self.printAdminMatchesMenu()
            if not matchChoice:
                return
            elif matchChoice == 1:
                DB.viewAllMatches()
            elif matchChoice == 2:
                DB.viewMatchesByUser()
            elif matchChoice == 3:
                DB.viewMatchesByDate()
            elif matchChoice == 4:
                DB.resetMatches()

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
        print('\n8 - Reset account.')
        print('9 - Delete account.\n')
        print('0 - Back to main menu.')
        return self.getInput()

    def accountMenu(self):
        while True:
            menuChoice = self.printAccountMenu()
            if not menuChoice:
                return True
            elif menuChoice == 1:
                DB.changePassword(self.username)
            elif menuChoice == 2:
                DB.viewSecurity(self.username)
            elif menuChoice == 3:
                if not DB.editUser(self.isAdmin, self.username, self.username):
                    return False
            elif menuChoice == 8:
                DB.tryResetUser(self.username)
            elif menuChoice == 9:
                if DB.tryDeleteUser(self.username):
                    return False
            else:
                getpass('Unable to parse input. Press enter to re-try.')

    def printAdminUserMenu(self):
        self.consoleClear()
        print('- User Menu. -\n')
        print('1 - View all users.')
        print('2 - Search all users.')
        print('3 - Add a new user.')
        print('4 - Edit a user.')
        print('0 - Back to admin menu.')
        return self.getInput()

    def adminUserMenu(self):
        while True:
            menuChoice = self.printAdminUserMenu()
            if not menuChoice:
                return
            elif menuChoice == 1:
                DB.viewAllUsers()
            elif menuChoice == 2:
                self.userSearchMenu()
            elif menuChoice == 3:
                DB.createAccount()
            elif menuChoice == 4:
                while True:
                    self.consoleClear()
                    Username = input(
                        'Which user would you like to edit? (Username) ')
                    if DB.checkUsernameExists(Username):
                        if not DB.editUser(True, Username, self.username):
                            return False
                    else:
                        getpass('Invalid username. Press enter to continue.')
                        break
            elif menuChoice == 3:
                self.userSearchMenu()
            else:
                getpass('Unable to parse input. Press enter to re-try.')

    def printUserSearchMenu(self):
        self.consoleClear()
        print('Search by:\n')
        print('1 - Username.')
        print('2 - Firstname.')
        print('3 - Lastname.')
        print('4 - Creation date.')
        print('5 - Account type.')
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
