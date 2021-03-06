# Importing required python modules.
import datetime as dt
import os
import re
import sqlite3
from getpass import *
from random import *
from statistics import mean, mode

import numpy as np
from faker import Faker

from termcolor import colored


def consoleClear():
    # A simple function designed to clear the console screen when called.
    os.system('cls')


def resetMatches():
    # A function to pass an SQL statement to delete all records from the
    # 'Matches' table in the DB.
    command("DELETE FROM Matches")


def command(code, *args):
    # A generic function used to send SQL commands to the database and also
    # extract data from the database if the command requires it.
    with sqlite3.connect('Chess.db') as conn:
        db = conn.cursor()
        if not args:
            db.execute(code)
        else:
            db.execute(code, args)
        data = db.fetchall()
        return data


def createMatches():
    # A function to pass an SQL statement creating the 'Matches' table to the
    # 'command' function.
    sql = """CREATE TABLE IF NOT EXISTS Matches
(MatchID INTEGER,
Username TEXT,
DateOfGame TEXT,
Won INTEGER,
Side REAL,
AIDepth INTEGER,
Moves INTEGER,
PiecesLeft INTEGER,
PointAdvantage INTEGER,
PRIMARY KEY(MatchID)
FOREIGN KEY(Username) REFERENCES Users(Username))"""
    command(sql)


def createUsers():
    # A function to pass an SQL statement creating the 'Users' table to the
    # 'command' function.
    sql = """CREATE TABLE IF NOT EXISTS Users
(Username TEXT,
Password TEXT,
isAdmin INTEGER,
FirstName TEXT,
SurName TEXT,
Created TEXT,
SecurityID INTEGER,
Answer TEXT,
PRIMARY KEY(Username)
FOREIGN KEY(SecurityID) REFERENCES Security(SecurityID))"""
    command(sql)


def createSecurity():
    # A function to pass an SQL statement creating the 'Security' table to the
    # 'command' function.
    sql = """CREATE TABLE IF NOT EXISTS Security
(SecurityID INTEGER,
Question TEXT,
PRIMARY KEY(SecurityID))"""
    command(sql)


def fabricate(n):
    fake = Faker()
    dates = [fake.date_this_year(
        before_today=True, after_today=False) for x in range(n)]
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
        addTestMatch(username, date, won, side, depth,
                     moves, piecesLeft, endPointAdvantage)


def addTestMatch(username, date, won, side, depth,
                 moves, piecesLeft, endPointAdvantage):
    command("""
INSERT INTO Matches(Username,
DateOfGame,
Won,
Side,
AIDepth,
Moves,
PiecesLeft,
PointAdvantage)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            username, date, won, side, depth,
            moves, piecesLeft, endPointAdvantage)


def addMatch(username, won, side, depth,
             moves, piecesLeft, endPointAdvantage):
    # Function to pass an SQL statement to insert a new record into the
    # 'Matches' table into specific named fields.
    date = dt.datetime.today().strftime('%d/%m/%Y')
    command("""
INSERT INTO Matches(Username,
DateOfGame,
Won,
Side,
AIDepth,
Moves,
PiecesLeft,
PointAdvantage)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            username, date, won, side, depth,
            moves, piecesLeft, endPointAdvantage)


def resetUser(Username):
    # Function to pass an SQL statement to the database designed to delete
    # all records from the 'Matches' table where the 'Username' is equal to
    # a given value.
    command("DELETE FROM Matches WHERE Username = ?", Username)


def tryResetUser(Username):
    # Function to instigate the resetting of a user's matches by asking for
    # two sets of confirmation data.
    if checkPasswordMatch(Username):
        while True:
            confirm = input(
                'Finally, enter your username to confirm reset: ')
            if confirm == Username:
                resetUser(Username)
                getpass(
                    'User stats have been reset. Press enter to return.')


def deleteUser(Username):
    # Function to pass an SQL statement to the database designed to delete
    # all records from the 'Users' table where the 'Username' is equal to
    # a given value.
    command("DELETE FROM Users WHERE Username = ?", Username)


def tryDeleteUser(Username):
    # Function to instigate the resetting of a user's matches and deletion of
    # a user's account by asking for two sets of confirmation data.
    if checkPasswordMatch(Username):
        while True:
            consoleClear()
            confirm = input(
                'Finally, enter your username to confirm deletion: ')
            if confirm == Username:
                resetUser(Username)
                deleteUser(Username)
                getpass(
                    'User has been deleted. Press enter to return.')
                return True


def checkPageNo(page, pages):
    # Function to return either a boolean 'False' value or an integer
    # depending on whether it is within a certain range or not.
    try:
        page = int(page[0])
        if page > pages or page < 1:
            return False
        else:
            return page
    except:
        return False


def getMatchesByField(Field, Search, x=0, y=0, z=-1):
    # Function to pass an SQL statement to extract either all of the matches
    # from the 'Matches' table or all of the matches where a specific field
    # value matches a given search value before returning a small selection
    # from the list and also the integer length of the returning data.
    if not Field:
        data = command("SELECT * FROM Matches")
    else:
        data = command("""
SELECT *
FROM Matches
WHERE {} = ?""".format(Field), Search)
    return data[x:y:z], len(data)


def viewMatches(Field, Search=None):
    # A function to handle all but the actual printing of a selection of
    # matches retrieved from the 'getMatchesByField' function after being
    # given a field and a search value. Creates and applies a makeshift
    # 'page' system also for the viewer to be able to navigate  given
    # results easily.
    page = 1
    while True:
        matches, len = getMatchesByField(
            Field, Search, ((page - 1) * -10) - 1, (page * -10) - 1)
        if not matches:
            getpass('\nNo matches found from that search. ' +
                    'Press enter return.')
            break
        else:
            pages = int(len / 10 if len % 10 == 0 else (len // 10) + 1)
            printMatches(matches[::-1])
            print(f'Currently on page {page}/{pages}.')
            newPage = input(
                'Enter new page no. or leave blank to return: ')
            if newPage:
                correct = checkPageNo(newPage, pages)
                if correct:
                    page = correct
            else:
                break


def printMatches(matches):
    # A function that when given a list of data, prints said list with the
    # use of large amounts of string formatting to create a table.
    consoleClear()
    connector = '+'
    for i in [14, 12, 7, 7, 9, 7, 12, 16]:
        connector += '-' * i + '+'
    header = f"|{'Username':>13} |{'DateOfGame':>11} |{'Won':>6} " + \
             f"|{'Side':>6} |{'AIDepth':>8} |{'Moves':>6} " + \
             f"|{'PiecesLeft':>11} |{'PointAdvantage':>15} |\n"
    print(connector + '\n' + header + connector)
    for match in matches[::-1]:
        print(f"|{match[1]:>13} |{match[2]:>11} |"
              + f"{'True' if match[3] else 'False':>6} |"
              + f"{match[4]:>6} |{match[5]:>8} |{match[6]:>6} |"
              + f"{match[7]:>11} |{match[8]:>15} |")
    print(connector)


def viewAllMatches():
    # A function to call the 'viewMatches' function with the required argument
    # so that it returns all matches rather than just those specified by a
    # given field and search value.
    viewMatches(False)


def viewMatchesByUser():
    # A function to take in a string from the user, check if it exists as a
    # 'Username' in the database and then run the 'viewMatches' function and
    # return with any records in the 'Matches' table that match the 'Username'.
    while True:
        consoleClear()
        Search = input('Search for matches by username: ').lower()
        if checkUsernameExists(Search):
            break
        else:
            getpass(
                '\nNo matches found from that search. Press enter return.')
            return
    viewMatches('Username', Search)


def viewMatchesByDate():
    # A function to retrieve a date as a string and run the 'viewMatches'
    # function and return with any records in the 'Matches' table that match
    # the given 'DateOfGame'.
    Search = getEditableDate()
    viewMatches('DateOfGame', Search)


def addInitUser():
    command("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            'as', 'p', 1, 'Alex', 'Shore', getCurrentDate(), 1, 'echo')
    command("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            'jf', 'p', 1, 'James', 'Frost', getCurrentDate(), 1, 'honey')


def addNewUser(username, password, isAdmin,
               firstName, surName, date, SID, answer):
    # Function to pass an SQL statement to insert a new record into the
    # 'Users' table into specific named fields.
    command("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            username, password, isAdmin, firstName,
            surName, date, SID, answer)


def getUsersByField(Field, Search, x=0, y=0, z=1):
    # Function to pass an SQL statement to extract either all of the matches
    # from the 'Users' table or all of the matches where a specific field
    # value matches a given search value before returning a small selection
    # from the list and also the integer length of the returning data.
    if not Field:
        data = command("SELECT * FROM Users ORDER BY SurName")
    else:
        data = command("""
SELECT *
FROM Users
WHERE {} = ?
ORDER BY SurName""".format(Field), Search)
    return data[x:y:z], len(data)


def viewUsers(Field, Search=None):
    # A function to handle all but the actual printing of a selection of
    # users retrieved from the 'getUsersByField' function after being
    # given a field and a search value. Creates and applies a makeshift
    # 'page' system also for the viewer to be able to navigate  given
    # results easily.
    page = 1
    while True:
        users, len = getUsersByField(
            Field, Search, (page - 1) * 10, page * 10)
        if not users:
            getpass(
                'No users found from that search. Press enter to return')
            break
        else:
            pages = int(len / 10 if len % 10 == 0 else (len // 10) + 1)
            printUsers(users)
            print(f'Currently on page {page}/{pages}.')
            newPage = input(
                'Enter new page no. or leave blank to return: ')
            if newPage:
                correct = checkPageNo(newPage, pages)
                if correct:
                    page = correct
            else:
                break


def printUsers(users):
    # A function that when given a list of data, prints said list with the
    # use of large amounts of string formatting to create a table.
    consoleClear()
    connector = '+'
    for i in [14, 13, 17, 9, 12]:
        connector += '-' * i + '+'
    header = f"|{'Username':>13} |{'Firstname':>12} " + \
             f"|{'Surname':>16} |{'isAdmin':>8} |{'Created':>11} |\n"
    print(connector + '\n' + header + connector)
    for user in users:
        print(
            f"|{user[0]:>13} |{user[3]:>12} |{user[4]:>16} |"
            + f"{'True' if user[2] else 'False':>8} |{user[5]:>11} |")
    print(connector)


def viewAllUsers():
    # A function to call the 'viewUsers' function with the required argument
    # so that it returns all matches rather than just those specified by a
    # given field and search value.
    viewUsers(False)


def searchByUsername():
    # A function to take in a string from the user to act as a search
    # parameter. Gets passed to the 'viewUsers' function to find a record,
    # if there is one, that matches the given string in the 'Username' field.
    consoleClear()
    Search = input('Enter username to search for: ').lower()
    viewUsers('Username', Search)


def searchByFirstname():
    # A function to take in a string from the user to act as a search
    # parameter. Gets passed to the 'viewUsers' function to find any record(s),
    # if there is one, that matches the given string in the 'FirstName' field.
    consoleClear()
    Search = input('Enter firstname to search for: ').lower()
    viewUsers('FirstName', Search)


def searchByLastname():
    # A function to take in a string from the user to act as a search
    # parameter. Gets passed to the 'viewUsers' function to find any record(s),
    # if there is one, that matches the given string in the 'SurName' field.
    consoleClear()
    Search = input('Enter lastname to search for: ').lower()
    viewUsers('SurName', Search)


def searchByDate():
    # A function to retrieve a date as a string and run the 'viewUsers'
    # function to print any of the records in the 'Users' table that match
    # the given 'Created' date.
    consoleClear()
    Search = getEditableDate()
    viewUsers('Created', Search)


def searchByAdmin():
    # A function to take in an integer input from the user to reference a
    # state of admin within the table. Runs the 'viewUsers' function to print
    # any of the records in the 'Users' table that match the state.
    consoleClear()
    print('- Account types. -\n')
    print('0 - Regular account.')
    print('1 - Admin account.')
    Search = int(input('Option: ')[0])
    viewUsers('isAdmin', Search)


def checkUsernameExists(Username):
    # Function to pass an SQL statement to the database to verify whether
    # any user exists with the name that is already passed to the function
    # before returning a boolean value depending on whether it finds any
    # such matching thing.
    valid = command("""
SELECT Users.Username
FROM Users
WHERE Users.Username = ?""", Username)
    return True if valid else False


def getSecurityQuestions():
    # Function to retrieve and return all data from the 'Security' table
    # in the database through passing an SQL statement to the database.
    return command("SELECT * FROM Security")


def setPass(Username, Password):
    # Function to update a given record's 'Password' field with a newly
    # given replacement string.
    command("""
UPDATE Users
SET Password = ?
WHERE Username = ?""", Password, Username)


def getQuestion(Username):
    # Function to retrieve and return the 'Security.Question' from the
    # 'Security' where the given 'Username' matches that of a record in the
    # table through passing a querying SQL statement to the database.
    return command("""
SELECT Security.Question
FROM Security
INNER JOIN Users ON (Security.SecurityID = Users.SecurityID)
WHERE Users.Username = ?""", Username)[0][0]


def getAnswer(Username):
    # Function to retrieve and return the value in the 'Answer' string
    # pertaining to to a given username matching in the 'User' table through
    # the use of passing an SQL statement to the database.
    return command("""
SELECT Users.Answer
FROM Users
WHERE Users.Username = ?""", Username)[0][0]


def getSessionDetails(Username):
    # Function to retrieve and return the values stored in the fields
    # 'isAdmin', 'FirstName' and 'Username' from the 'Users' table where
    # an already passed in 'Username' parameter matches the same entry in
    # the database through the use of passing an SQL statement to the database.
    return command("""
SELECT Users.isAdmin,
Users.FirstName,
Users.Username
FROM Users
WHERE Users.Username = ?""", Username)[0]


def checkLogInData(Username, Password):
    # Function to retrieve and return the values stored in the field
    # 'Username' from the 'Users' table where already passed in 'Username'
    # and 'Password' parameters match the same entry in the database through
    # the use of passing an SQL statement to the database.
    return command("""
SELECT Users.Username
FROM Users
WHERE Users.Username = ?
AND Users.Password = ?
""", Username, Password)


def getAllUsers():
    # Function to retrieve and return the values stored in the fields
    # 'Username', 'FirstName', 'SurName', 'isAdmin' and 'Created' from the
    # 'Users' table in an array alphabetically ordered by the 'SurName' field
    # through the use of passing an SQL statement to the database.
    return command("""
SELECT Users.Username,
Users.FirstName,
Users.SurName,
Users.isAdmin,
Users.Created
FROM Users ORDER BY Users.SurName""")


def getAllUsernames():
    # Function to retrieve and return all values stored in the 'Username' field
    # in the 'Users' table and returns them in an array through the use of
    # passing an SQL statement to the database.
    return command("""
SELECT Users.Username
FROM Users""")


def printUserDetails(Username):
    # Function to retrieve contents for 6 variables from the function
    # 'getUserDetails' by passing it an already passed in 'Username' variable
    # and then to print the 6 retrieved variables in a nicely formatted way
    # for the user.
    Username, Password, isAdmin, FirstName, SurName, Created = \
        getUserDetails(Username)
    print('- Account Details -\n')
    print(f"{'Username:':<20}" + f'{Username:>20}')
    print(f"{'Password:':<20}" + f'{Password:>20}')
    print(f"{'isAdmin:':<20}" + f'{isAdmin:>20}')
    print(f"{'Created:':<20}" + f'{Created:>20}')
    print('\n- Personal Details -\n')
    print(f"{'FirstName:':<20}" + f'{FirstName:>20}')
    print(f"{'SurName:':<20}" + f'{SurName:>20}')


def editUser(isAdmin, Username, currentUser):
    # A function to, in short, either edit a specific user's details and return
    # to the previous menu or just to print said details and return without
    # changing anything. The process is as follows: firstly, the function
    # prints out the details relating to the given 'Username' parameter.
    # Secondly, the user enters a string that references a field to change.
    # Then, the program checks that if that string actually exists as a
    # changeable field name, it gets the user to input the new updated item
    # for the field. Finally, it prints a statement telling the user what has
    # changed from previous to now.
    while True:
        consoleClear()
        printUserDetails(Username)
        print('\nInput is case sensitive.')
        print('Enter \'x\' to return.')
        fieldChange = input('Field to change? ')
        consoleClear()
        newItem = None
        if fieldChange.lower() == 'x':
            return True
        elif fieldChange == 'Username':
            print('Due to complications in code, this is unchangeable.')
            getpass('Press enter to continue.')
        elif fieldChange == 'Password':
            newItem = getPassword()
        elif fieldChange == 'isAdmin':
            newItem = getIsAdmin()
        elif fieldChange == 'FirstName':
            newItem = input('Firstname: ')
        elif fieldChange == 'SurName':
            newItem = input('Surname: ')
        elif fieldChange == 'Created' and isAdmin:
            newItem = getEditableDate()
        elif fieldChange == 'Created':
            print('Sorry, this can only be changed by an admin.')
            getpass('Press enter to continue.')
        else:
            retry = input('Invalid field entered. Retry? (yN) ')
            if retry.lower() != 'y':
                getpass('Returning to menu. Press enter to continue.')
                return True
        if newItem or newItem == 0:
            try:
                oldItem = getUserField(fieldChange, Username)
                editUserField(fieldChange, newItem, Username)
                if fieldChange == 'isAdmin' and currentUser == Username:
                    if newItem != oldItem:
                        print(
                            '\nYou had admin your status changed from ' +
                            f"{'true' if oldItem else 'false'} to " +
                            f"{'true' if newItem else 'false'}.\n")
                        getpass('Press enter to logout.')
                        return False
                    else:
                        print(
                            f'\nYour admin status was left unchanged.\n')
                        getpass('Press enter to continue.')
                        return True
                if newItem != oldItem:
                    print(
                        f'\n{fieldChange} changed from {oldItem} to' +
                        f' {newItem} for user \'{Username}\'.\n')
                    getpass('Press enter to logout.')
                    return False
                else:
                    print(
                        f'\n{fieldChange} was left ' +
                        'unchanged for user \'{Username}\'.\n')
            except:
                getpass('Something went wrong. Press enter to try again.')


def editUserField(Field, newItem, Username):
    # Function to pass an SQL statement to the database to update a specific
    # field within a record where the 'Username' field in the 'Users' table
    # matches the given passed parameter.
    command("""
UPDATE Users
SET {} = ?
WHERE Users.Username = ?""".format(
            Field), newItem, Username)


def getUserField(Field, Username):
    # Function to pass an SQL statement to the database to select and return
    # a specific field within the database where 'Username' field in the
    # 'Users' table matches the given passed parameter.
    return command("""
SELECT Users.{}
FROM Users
WHERE Users.Username = ?""".format(Field), Username)[0][0]


def getUserDetails(Username):
    # Function to pass an SQL statement to the database to select and return
    # the first five attributes of a record within the datbase where the
    # 'Username' field of the record in the 'Users' table matches the given
    # passed parameter.
    return command("""
SELECT *
FROM Users
WHERE Users.Username = ?""", Username)[0][:6]


def viewSecurity(Username):
    # Function to pass an SQl statement to the database to select and return
    # the 'Security.Question' and 'User.Answer' field values from the
    # 'Security' and 'Users' tables respectively where the 'Username' field of
    # the record matches the given passed parameter through the use of a joined
    # table search. It then prints the data collected in a table for the user
    # to view. The user then has a choice of whether to change their security
    # data or not. If they say yes, then it runs the function 'getSecurity' to
    # allow the user to enter in new security details and once it has these
    # details runs the function 'editUserField' twice to update the database
    # with the users newly entered data.
    consoleClear()
    data = command("""
SELECT Security.Question,
Users.Answer
FROM Users
INNER JOIN Security ON(Users.SecurityID = Security.SecurityID)
WHERE Users.Username = ?""", Username)[0]
    connector = '+' + '-' * 46 + '+' + '-' * 21 + '+'
    header = f"|{'Question':>45} |{'Answer':>20} |"
    print(connector + '\n' + header + '\n' + connector)
    print(f'|{data[0]:>45} |{data[1]:>20} |\n' + connector)
    while True:
        edit = input('\nWould you like to edit data? (yN) ')
        if edit.lower() == 'y':
            SID, Answer = getSecurity()
            editUserField('SecurityID', SID, Username)
            editUserField('Answer', Answer, Username)
        break


def changePassword(Username):
    # A simple function to act as the connecting function between three other
    # functions. First runs an IF statement to evaluate a 'boolean-returning'
    # function that is passed a 'Username' string variable that essentially
    # just checks for a given password matching the one in the database with
    # the same 'Username' string in its record.
    if checkPasswordMatch(Username):
        newPassword = getPassword()
        setPass(Username, newPassword)


def checkPasswordMatch(Username):
    # A function that is passed a 'Username' string and asks for an entry from
    # the user asking for their current 'Password' before checking both the
    # 'Username' and 'Password' string variables against the 'Users' table in
    # the database through passing an SQL statement to retrieve the 'Username'
    # field in any records in the 'Users' table where the 'Username' field and
    # the 'Password' field match those passed into it. If there is a match, it
    # returns 'True', else 'False'.
    while True:
        consoleClear()
        Password = getpass('Current password: ')
        data = command("""
SELECT Users.Username
FROM Users
WHERE Users.Username = ?
AND Users.Password = ?
""", Username, Password)
        if data:
            return True
        else:
            retry = input('\nInvalid password. Retry? (yN) ')
            if retry.lower() != 'y':
                return False


def logIn():
    # A more complex function to allow the user to 'Log in'. Is very similar to
    # the function 'checkPasswordMatch' in that it checks a 'Username' and
    # 'Password' input against the 'Users' table in the same way by retrieving
    # the 'Username' field in any records in the 'Users' table where there is a
    # match. If there is a match, the program runs another function called
    # 'getSessionDetails' whose purpose is already explained previously before
    # returning the data it gets from 'getSessionDetails' along with a boolean
    # denoting whether to continue trying to log in or not. If however, it does
    # not find a match, it allows the user to choose to try re-entering their
    # data and either exits or loops back around depending on what the user
    # enters.
    while True:
        consoleClear()
        Username = input('Username: ').lower()
        Password = getpass('Password: ')
        data = command("""
SELECT Users.Username
FROM Users
WHERE Users.Username = ?
AND Users.Password = ?
""", Username, Password)
        if data:
            sessionData = getSessionDetails(data[0][0])
            Username, FirstName = sessionData[2], sessionData[1]
            isAdmin = sessionData[0]
            return True, isAdmin, FirstName, Username
        else:
            tryAgain = input(
                'Invalid username/password. Retry? (yN) ')
            if tryAgain.lower() != 'y':
                return False


def getUsername():
    # A function to take in an input from the user to act as a 'Username'
    # string variable which then gets checks for existence within the database
    # as an already in-use record. If the 'Username' does not exist within the
    # database 'Users' table, or the length of the username is not between six
    # and 12 characters the user has to try another string to use.
    while True:
        consoleClear()
        Username = input('Username: ').lower()
        if checkUsernameExists(Username):
            getpass(
                'Username already in use. Press enter to try again.')
        elif len(Username) > 12 or len(Username) < 6:
            getpass(
                'Username has to be between 6 and 12 characters long.')
        else:
            return Username


def checkPasswordValidity(Password):
    # A function to be passed a 'Password' parameter that is then checked by
    # numerous security measures to make sure that the users 'Password' is
    # deemed strong enough to be secure. The function does this through the use
    # of regular expression. If it deems the 'Password' to be strong enough, it
    # returns the boolean value 'True', else it returns 'None'.
    if len(Password) < 8:
        print('Password was too short. Try again.\n')
    elif len(Password) > 16:
        print('Password was too long. Try again.\n')
    elif not re.search('[a-z]', Password):
        print('Password needs lowercase characters. Try again.\n')
    elif not re.search('[A-Z]', Password):
        print('Password needs uppercase characters. Try again.\n')
    elif not re.search('[0-9]', Password):
        print('Password needs at least one number. Try again.\n')
    elif re.search('\s', Password):
        print('Password can\'t contain spaces. Try again.\n')
    else:
        return True


def getPassword():
    # A function to print out a list of rules for the user to follow when
    # entering in their new 'Password' for their 'account' in the system and to
    # then take in a new 'Password' string variable before checking the
    # validity of the given 'Password' from the user. If this returns 'True',
    # it breaks out of the loop before asking the user to enter in their
    # 'Password' again to make sure the user entered it correctly to their own
    # liking the first time. If the confirmation variable matches the original,
    # then the original is passed back to the calling function, else it loops
    # back to the beginning of the function.
    while True:
        consoleClear()
        print('Password must be between 8-16 characters long.')
        print('Password must contain lowercase and uppercase.')
        print('Password must contain at least one number.')
        print('Password must not contain spaces.\n')
        while True:
            Password = getpass('New password: ')
            if checkPasswordValidity(Password):
                break
        confirmationPass = getpass('Please confirm new password: ')
        if confirmationPass == Password:
            return Password
        else:
            consoleClear()
            getpass(
                'Passwords don\'t match. Press enter to try again.\n')


def getIsAdmin():
    # A function to ask the user whether or not they would like their 'account'
    # to have an 'isAdmin' status of true or false. If the user tries to get
    # their account to have an 'isAdmin' status of true by selecting 'y' then
    # the function will ask for a 'Permission code' to check that the user has
    # the ability to become an admin. If the users entered code matches the one
    # in the code, they are made an admin through the function returning a
    # value with inherent truthiness, else, it asks if they would like to
    # retry entering in the correct code or be content with their 'account' not
    # having an 'isAdmin' status of 'True' and then either loops back to the
    # user entering in a new code or returns with a value of no truthiness.
    consoleClear()
    adminAttempt = input('Set this account as admin? (yN) ')
    if adminAttempt.lower() != 'y':
        return 0
    while True:
        adminPass = getpass('\nPermission code: ')
        if adminPass == 'lifegoeson-noahandthewhale':
            return 1
        tryAgain = input('\nIncorrect code. Try again? (yN) ')
        if tryAgain.lower() != 'y':
            return 0
        consoleClear()


def getEditableDate():
    # A function take in three integer values from the user and to run them
    # through the imported 'datetime.date' function to create a 'date' object
    # that is then passed back to the calling function if it succeeds with
    # an edited string version of the 'date' object.
    consoleClear()
    while True:
        try:
            Day = int(input('Enter day: '))
            Month = int(input('Enter month: '))
            Year = int(input('Enter year: '))
            newDate = dt.date(Year, Month, Day)
            break
        except:
            getpass('Invalid date entered. Press enter to try again.')
    return newDate.strftime('%d/%m/%Y')


def getCurrentDate():
    # A simple function to return the date today in the format 'DD/MM/YYYY' by
    # the use of the 'datetime.datetime.today' function along with the
    # '<date>.strftime' function.
    return dt.datetime.today().strftime('%d/%m/%Y')


def getSecurity():
    # A simple function to retrieve data from the 'getSecurityQuestions'
    # function before printing out said data in a nice format whiles asking the
    # user to select a favourable question to act as their 'Security' question
    # before asking the user to enter in their 'Answer' and returning both of
    # these pieces of data.
    data = getSecurityQuestions()
    while True:
        consoleClear()
        print('Security Questions:')
        for i in range(len(data)):
            print(f'{data[i][0]} - {data[i][1]}')
        SID = int(input('Option: ')[0])
        if SID not in range(1, len(data) + 1):
            getpass('\nInvalid choice. Press enter to try again.')
        else:
            break
    Answer = input('Enter answer: ').lower()
    return SID, Answer


def getPersonalDetails():
    # A simple function to allow the user to enter in two string variables
    # named 'Firstname' and 'Surname' before returning these variables.
    consoleClear()
    Firstname = input('Set firstname as: ').lower()
    Surname = input('Set surname as: ').lower()
    return Firstname, Surname


def createAccount():
    # A connecting function to start off the user account creation process and
    # call all of the functions required for the process to have all the needed
    # data to create the account.
    consoleClear()
    print('- Account creation: -\n')
    start = input('\nEnter \'x\' to exit. Continue? (yN) ')
    if start.lower() == 'y':
        Username = getUsername()
        Password = getPassword()
        isAdmin = getIsAdmin()
        Firstname, Surname = getPersonalDetails()
        date = getCurrentDate()
        SID, Answer = getSecurity()
        addNewUser(Username, Password, isAdmin,
                   Firstname, Surname, date, SID, Answer)
    else:
        return


def forgotPassword():
    # A more complex function to go through the 'Password recovery' system.
    # Takes in an input from the user to act as a 'Username' string variable.
    # This gets referenced against the 'Users' table in the database to check
    # if a user exists with that 'Username' value. If a user does exist it runs
    # another function to extract the security question related to that user
    # before asking the user to input an answer to said question. If the answer
    # that the user inputs is seen to be correct in the database it then kicks
    # off the 'getPassword' function to retrieve a new password for the user
    # before setting it in the database and returning. If any of these steps
    # fails the function asks the user if they would like to retry, if they
    # choose to retry it loops back, else it returns out of the function back
    # to the calling function.
    while True:
        consoleClear()
        print('- Password recovery -\n')
        Username = input('Username: ')
        if checkUsernameExists(Username):
            print(getQuestion(Username))
            while True:
                Answer = getpass('Answer: ').lower()
                if Answer == getAnswer(Username):
                    getpass(
                        'You may now enter a new password. ' +
                        'Press enter to continue.')
                    newPassword = getPassword()
                    setPass(Username, newPassword)
                    getpass(
                        'Your password has been changed. ' +
                        'Press enter to continue.')
                    return
                else:
                    retry = input('Invalid answer. Try again? (yN) ')
                    if retry.lower() != 'y':
                        return
        else:
            retry = input('Invalid username. Try again? (yN) ')
            if retry.lower() != 'y':
                return


def getPlayedByUser(Username):
    # A simple function to retrieve from the database all records from the
    # 'Matches' table where the 'Username' field matches the given passed
    # parameter through the use of passing an SQL statement to the database
    # before returning the length of the retrieved data.
    return len(command("""
SELECT *
FROM Matches
WHERE Username = ?""", Username))


def getWinsByUser(Username):
    # A simple function to retrieve from the database all records from the
    # 'Matches' table where the 'Username' field matches the given passed
    # parameter as well as the value stored in the 'Won' field being equal to
    # '1' through the use of passing an SQL statement to the database
    # before returning the length of the retrieved data.
    return len(command("""
SELECT *
FROM Matches
WHERE Username = ?
AND Won = 1""", Username))


def getWinRateByUser(Username):
    # A simple function to either return a value representing percentage win
    # rate if the user is found to have any matches played, else to return
    # an 'NA' string.
    if getPlayedByUser(Username):
        return str(int(round(getWinsByUser(Username) /
                             getPlayedByUser(Username) * 100, 0))) + '%'
    return 'NA'


def getListStats(list):
    # A simple function get passed a list of integers and return a list of
    # three values; the largest value in the list, the minimum value in the
    # list and the integer mean value rounded to zero decimal places.
    return [max(list), min(list), int(round(mean(list), 0))]


def getFieldByUser(Field, Username):
    # A function to get passed a field to retrieve from and a search term
    # 'Username' to use to retrieve data and return it after passing the data
    # in a list to the function 'getListStats'.
    data = command("""
SELECT {}
FROM Matches
WHERE Username = ?""".format(Field), Username)
    return getListStats([n[0] for n in data])


def getPiecesByUser(Username):
    # A connecting function to check if the user referenced by the passed
    # 'Username' string variable has played any 'Matches'. If yes, then to
    # return with the value returned by the called function 'getFieldByUser'
    # with the field 'PiecesLeft' and the same 'Username' variable. Else,
    # returns a list consisting of the string 'NA' three times.
    if getPlayedByUser(Username):
        return getFieldByUser('PiecesLeft', Username)
    return ['NA' for n in range(3)]


def getPointsByUser(Username):
    # A connecting function to check if the user referenced by the passed
    # 'Username' string variable has played any 'Matches'. If yes, then to
    # return with the value returned by the called function 'getPointsByUser'
    # with the field 'PointAdvantage' and the same 'Username' variable. Else,
    # returns a list consisting of the string 'NA' three times.
    if getPlayedByUser(Username):
        return getFieldByUser('PointAdvantage', Username)
    return ['NA' for n in range(3)]


def getMovesByUser(Username):
    # A connecting function to check if the user referenced by the passed
    # 'Username' string variable has played any 'Matches'. If yes, then to
    # return with the value returned by the called function 'getPlayedByUser'
    # with the field 'Moves' and the same 'Username' variable. Else,
    # returns a list consisting of the string 'NA' three times.
    if getPlayedByUser(Username):
        return getFieldByUser('Moves', Username)
    return ['NA' for n in range(3)]


def getLastGameDate(Username):
    # A connecting function to check if the user referenced by the passed
    # 'Username' string variable has played any 'Matches'. If yes, then to
    # retrieve and return the last item from the data returned from passing an
    # SQL statement to the database to return a list containing all data under
    # the 'DateOfGame' field in the 'Matches' table where the 'Username'
    # matches that given to the function. Else, returns the string 'NA'.
    if getPlayedByUser(Username):
        return command("""
SELECT DateOfGame
FROM Matches
WHERE Username = ?""", Username)[-1][0]
    return 'NA'


def getAIDepthByUser(Username):
    # A connecting function to check if the user referenced by the passed
    # 'Username' string variable has played any 'Matches'. If yes, then to
    # retrieve and return the last ten items from the data returned from
    # passing an SQL statement to the database to return a list containing all
    # data under the 'AIDepth' field in the 'Matches' table where the
    # 'Username' matches that given to the function. Else, returns the string
    # 'NA'.
    if getPlayedByUser(Username):
        data = command("""
SELECT AIDepth
FROM Matches
WHERE Username = ?""", Username)[:-10]
        return mode([n[0] for n in data])
    return 'NA'


def getUsersStats():
    consoleClear()
    username = input('See stats of which user? ').lower()
    if checkUsernameExists(username):
        getStats(username)
    else:
        getpass(
            'Sorry, that user does not exist. Press enter to return.')


def getStats(Username):
    printStats([getPlayedByUser(Username),
                getWinsByUser(Username),
                getWinRateByUser(Username),
                getPiecesByUser(Username),
                getPointsByUser(Username),
                getMovesByUser(Username),
                getLastGameDate(Username),
                getAIDepthByUser(Username)], Username)


def printStats(stats, username):
    consoleClear()
    print(f'- Base stats ({username}) -\n')
    print(f"{'Total matches played: ':<30}" + f'{stats[0]:>10}')
    print(f"{'Total match wins: ':<30}" + f'{stats[1]:>10}')
    print(f"{'Percentage win rate: ':<30}" + f'{stats[2]:>10}')
    print(f"{'Common AI depth (recent): ':<30}" + f'{stats[7]:>10}')
    print(f"{'Last played game: ':<30}" + f'{stats[6]:>10}')
    print('\n- More stats (most / least / average). -\n')
    print(f"{'Pieces left:':<20}" +
          f'{stats[3][0]:>4} /{stats[3][1]:>4} /{stats[3][2]:>4}')
    print(f"{'Point advantage:':<20}" +
          f'{stats[4][0]:>4} /{stats[4][1]:>4} /{stats[4][2]:>4}')
    print(f"{'Moves made:':<20}" +
          f'{stats[5][0]:>4} /{stats[5][1]:>4} /{stats[5][2]:>4}\n')
    getpass('Press enter to continue:')
