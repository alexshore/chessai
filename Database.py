import datetime as dt
import os
import re
import sqlite3
from getpass import *
from statistics import mean, mode


def consoleClear():
    os.system('cls')
    os.system('cls')


def resetMatches():
    command("DELETE FROM Matches")


def command(code, *args):
    with sqlite3.connect('Chess.db') as conn:
        db = conn.cursor()
        if not args:
            db.execute(code)
        else:
            db.execute(code, args)
        data = db.fetchall()
        return data


def createTable(sql):
    with sqlite3.connect('Chess.db') as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()


def createMatches():
    sql = """CREATE TABLE IF NOT EXISTS Matches
(MatchID integer,
Username text,
AIDepth integer,
DateOfGame date,
Won boolean,
Side text,
Moves integer,
PRIMARY KEY(MatchID)
FOREIGN KEY(Username) REFERENCES Users(Username))"""
    command(sql)


def createUsers():
    sql = """CREATE TABLE IF NOT EXISTS Users
(Username text,
Password text,
isAdmin boolean,
FirstName text,
SurName text,
Created date,
SecurityID integer,
Answer text,
PRIMARY KEY(Username)
FOREIGN KEY(SecurityID) REFERENCES Security(SecurityID))"""
    command(sql)


def createSecurity():
    sql = """CREATE TABLE IF NOT EXISTS Security
(SecurityID integer,
Question text,
PRIMARY KEY(SecurityID))"""
    command(sql)


def addMatch(username, won, side, depth, moves, piecesLeft, endPointAdvantage):
    date = dt.datetime.today().strftime('%d/%m/%Y')
    command("""
INSERT INTO Matches(Username, DateOfGame, Won, Side, AIDepth, Moves, PiecesLeft, PointAdvantage) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            username, date, won, side, depth, moves, piecesLeft, endPointAdvantage)


def checkPageNo(page, pages):
    if not page:
        return


def getMatches(x=0, y=0, z=-1):
    return command("SELECT * FROM Matches")[x:y:z], len(command("SELECT * FROM Matches"))


def viewAllMatches():
    page = 4
    while True:
        matches, len = getMatches(((page - 1) * -10) - 1, (page * -10) - 1)
        pages = len / 10 if len % 10 == 0 else (len // 10 ) + 1
        printMatches(matches[::-1])
        print(f'Currently on page {page}/{pages}.')
        page = input('New page (Leave blank to return to menu): ')[0]
        correct = checkPageNo(page, pages)


def printMatches(matches):
    connector = '+'
    for i in [14, 12, 7, 7, 9, 7, 12, 16]:
        connector += '-' * i + '+'
    header = f"|{'Username':>13} |{'DateOfGame':>11} |{'Won':>6} " + \
             f"|{'Side':>6} |{'AIDepth':>8} |{'Moves':>6} " + \
             f"|{'PiecesLeft':>11} |{'PointAdvantage':>15} |\n"
    print(connector + '\n' + header + connector)
    for match in matches[::-1]:
        print(f"|{match[1]:>13} |{match[2]:>11} |{'True' if match[3] else 'False':>6} "
              + f'|{match[4]:>6} |{match[5]:>8} |{match[6]:>6} |{match[7]:>11} |{match[8]:>15} |')
    print(connector)


def addInitUser():
    date = dt.datetime.today().strftime('%d/%m/%Y')
    temp = ['ashore', 'pw', True, 'Alex', 'Shore', date, 1, 'echo']
    command("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7])
    temp = ['jfrost', 'pw', False, 'James', 'Frost', date, 1, 'honey']
    command("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", temp[0], temp[1], temp[2], temp[3],
            temp[4], temp[5], temp[6], temp[7])


def addNewUser(username, password, isAdmin, firstName, surName, date, SID, answer):
    command("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", username, password, isAdmin, firstName,
            surName, date, SID, answer)


def searchByField(Field, Search):
    return command("""
SELECT Users.Username,
Users.FirstName,
Users.SurName,
Users.isAdmin,
Users.Created
FROM Users WHERE {} = ?""".format(Field), Search)


def searchByUsername():
    consoleClear()
    Search = input('Enter username to search for: ')
    data = searchByField('Username', Search)
    if data:
        printUsers(data)
    else:
        getpass('No user(s) found. Press enter to return to menu.')


def searchByFirstname():
    consoleClear()
    Search = input('Enter firstname to search for: ')
    data = searchByField('FirstName', Search)
    if data:
        printUsers(data)
    else:
        getpass('No user(s) found. Press enter to return to menu.')


def searchByLastname():
    consoleClear()
    Search = input('Enter lastname to search for: ')
    data = searchByField('SurName', Search)
    if data:
        printUsers(data)
    else:
        getpass('No user(s) found. Press enter to return to menu.')


def searchByDate():
    consoleClear()
    Search = getEditableDate()
    data = searchByField('Created', Search)
    if data:
        printUsers(data)
    else:
        getpass('No user(s) found. Press enter to return to menu.')


def searchByAdmin():
    consoleClear()
    print('- Account types. -\n')
    print('0 - Regular account.')
    print('1 - Admin account.')
    Search = int(input('Option: ')[0])
    data = searchByField('isAdmin', Search)
    if data:
        printUsers(data)
    else:
        getpass('No user(s) found. Press enter to return to menu.')


def checkUsernameExists(Username):
    valid = command(
        "SELECT Users.Username FROM Users WHERE Users.Username = ?", Username)
    return True if valid else False


def getSecurityQuestions():
    return command("SELECT * FROM Security")


def setPass(Username, Password):
    command("UPDATE Users SET Password = ? WHERE Username = ?", Password, Username)


def getQuestion(Username):
    return command("""
SELECT Security.Question
FROM Security
INNER JOIN Users ON (Security.SecurityID = Users.SecurityID)
WHERE Users.Username = ?""", Username)[0][0]


def getAnswer(Username):
    return command("""
SELECT Users.Answer
FROM Users
WHERE Users.Username = ?""", Username)[0][0]


def getSessionDetails(Username):
    data = command("""
SELECT Users.isAdmin,
Users.FirstName,
Users.Username
FROM Users
WHERE Users.Username = ?""", Username)
    return data[0]


def checkLogInData(Username, Password):
    data = command("""
SELECT Users.Username
FROM Users
WHERE Users.Username = ?
AND Users.Password = ?
""", Username, Password)
    return data


def printUsers(users):
    consoleClear()
    connector = '+' + '-' * 14 + '+' + '-' * 13 + '+' + '-' * 17 + '+' + '-' * 9  + '+' + '-' * 12 + '+'
    print(connector)
    print(f"|{'Username':>13} |{'Firstname':>12} |{'Surname':>16} |{'isAdmin':>8} |{'Created':>11} |")
    print(connector)
    for user in users:
        print(
            f"|{user[0]:>13} |{user[1]:>12} |{user[2]:>16} |" + \
            f"{'True' if user[3] else 'False':>8} |{user[4]:>11} |")
    print(connector)
    getpass('\nPress enter to continue.')

def getAllUsers():
    printUsers(command("""
SELECT Users.Username,
Users.FirstName,
Users.SurName,
Users.isAdmin,
Users.Created
FROM Users"""))


def getAllUsernames():
    data=command("""
SELECT Users.Username
FROM Users""")
    return data


def printUserDetails(Username):
    Username, Password, isAdmin, FirstName, SurName, Created=getUserDetails(
        Username)
    connector = '+' + '-' * 15 + '+' + '-' * 19 + '+' + '-' * 10 + \
        '+' + '-' * 13 + '+' + '-' * 17 + '+' + '-' * 13 + '+'
    print(connector)
    print(f"|{'Username':>14} |{'Password':>18} |{'isAdmin':>9} " +
          f"|{'FirstName':>12} |{'SurName':>16} |{'Created':>12} |")
    print(connector)
    print(f"|{Username:>14} |{Password:>18} |{isAdmin:>9} " +
          f"|{FirstName:>12} |{SurName:>16} |{Created:>12} |")
    print(connector + '\n')


def editUser(isAdmin, Username):
    while True:
        consoleClear()
        printUserDetails(Username)
        fieldChange = input(
            '\nWhich field would you like to change (case-sensitive). Enter \'x\' to return: ')
        consoleClear()
        newItem = None
        if fieldChange.lower() == 'x':
            return
        elif fieldChange == 'Username':
            print('Due to complications in code, this is unchangeable.')
        elif fieldChange == 'Password':
            newItem = getPassword()
        elif fieldChange == 'isAdmin':
            newItem = getEditableAdmin() if isAdmin else getIsAdmin()
        elif fieldChange == 'FirstName':
            newItem = input('Firstname: ')
        elif fieldChange == 'SurName':
            newItem = input('Surname: ')
        elif fieldChange == 'Created' and isAdmin:
            newItem = getEditableDate()
        else:
            retry = input('Invalid field entered. Re-enter? (yN) ')
            if retry.lower() != 'y':
                getpass('Returning to menu. Press enter to continue.')
                break
        if newItem:
            try:
                editUserField(fieldChange, newItem, Username)
                print(
                    f'{fieldChange} changed from {getUserField(fieldChange, Username)} to {newItem} for user \'{Username}\'.')
                getpass('Press enter to continue.')
                break
            except:
                getpass('Something went wrong. Press enter to try again.')


def editUserField(Field, newItem, Username):
    command("UPDATE Users SET {} = ? WHERE Users.Username = ?".format(
        Field), newItem, Username)


def getUserField(Field, Username):
    return command("SELECT Users.{} FROM Users WHERE Users.Username = ?".format(Field), Username)[0][0]


def getUserDetails(Username):
    return command("SELECT * FROM Users WHERE Users.Username = ?", Username)[0][:6]


def viewSecurity(Username):
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
    if checkPasswordMatch(Username):
        newPassword = getPassword()
        setPass(Username, newPassword)


def checkPasswordMatch(Username):
    while True:
        Password = getpass('Old password: ')
        data = command("""
SELECT Users.Username
FROM Users
WHERE Users.Username = ?
AND Users.Password = ?
""", Username, Password)
        if data:
            return True
        else:
            retry = input('Invalid password. Retry? (yN) ')
            if retry.lower() != 'y':
                return False


def logIn():
    while True:
        consoleClear()
        Username = input('Username: ')
        Password = getpass('Password: ')
        data = command("""
SELECT Users.Username
FROM Users
WHERE Users.Username = ?
AND Users.Password = ?
""", Username, Password)
        if data:
            sessionData = getSessionDetails(data[0][0])
            Username, FirstName, isAdmin = sessionData[2], sessionData[1], sessionData[0]
            return True, isAdmin, FirstName, Username
        else:
            tryAgain = input('Invalid username/password. Retry? (yN) ')
            if tryAgain.lower() != 'y':
                return False


def getUsername():
    while True:
        consoleClear()
        Username = input('Username: ')
        if checkUsernameExists(Username):
            getpass('Username already in use. Press enter to try again.')
        elif len(Username) > 12 or len(Username) < 6:
            getpass('Username has to be between 6 and 12 characters long.')
        else:
            return Username


def checkPasswordValidity(Password):
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
    consoleClear()
    while True:
        print('Password must be between 8-16 characters long.')
        print('Password must contain lowercase and uppercase.')
        print('Password must contain at least one number.')
        print('Password must not contain spaces.\n')
        while True:
            Password = getpass('Password: ')
            if checkPasswordValidity(Password):
                break
        confirmationPass = getpass('Please confirm password: ')
        if confirmationPass == Password:
            return Password
        else:
            consoleClear()
            getpass('Passwords don\'t match. Press enter to try again.\n')


def getEditableAdmin():
    consoleClear()
    adminAttempt = input('Set this account as admin? (yN) ')
    return True if adminAttempt.lower() == 'y' else False


def getIsAdmin():
    consoleClear()
    adminAttempt = input('Set this account as admin? (yN) ')
    if adminAttempt.lower() != 'y':
        return False
    while True:
        adminPass = getpass('\nPermission code: ')
        if adminPass == 'yo dawg':
            getpass('Correct code, setting as admin. Press enter to continue.')
            return True
        tryAgain = input('\nIncorrect code. Try again? (yN) ')
        if tryAgain.lower() != 'y':
            return False


def getEditableDate():
    consoleClear()
    while True:
        try:
            Year = int(input('What year was account created: '))
            Month = int(input('What month was account created: '))
            Day = int(input('What day was account created: '))
            newDate = dt.date(Year, Month, Day)
            break
        except:
            getpass('Invalid time entered. Press enter to try again.')

    print(newDate.strftime('%d/%m/%Y'))
    return newDate.strftime('%d/%m/%Y')


def getCurrentDate():
    return dt.datetime.today().strftime('%d/%m/%Y')


def getSecurity():
    data = getSecurityQuestions()
    while True:
        consoleClear()
        print('Security Questions:')
        for i in range(len(data)):
            print('{} - {}'.format(data[i][0], data[i][1]))
        SID = int(input('Option: ')[0])
        if SID not in [i + 1 for i in range(len(data))]:
            getpass('\nInvalid choice. Press enter to try again.')
        else:
            break
    Answer = input('Enter answer: ')
    return SID, Answer


def getPersonalDetails():
    consoleClear()
    Firstname = input('Firstname: ')
    Surname = input('Surname: ')
    return Firstname, Surname


def createAccount():
    consoleClear()
    print('- Account creation: -\n')
    Username = getUsername()
    Password = getPassword()
    isAdmin = getIsAdmin()
    Firstname, Surname = getPersonalDetails()
    date = getCurrentDate()
    SID, Answer = getSecurity()
    addNewUser(Username, Password, isAdmin,
               Firstname, Surname, date, SID, Answer)


def forgotPassword():
    while True:
        consoleClear()
        print('- Password recovery -\n')
        Username = input('Username: ')
        if checkUsernameExists(Username):
            print(getQuestion(Username))
            while True:
                Answer = getpass('Answer: ')
                if Answer == getAnswer(Username):
                    getpass(
                        'You may now enter a new password. Press enter to continue.')
                    newPassword = getPassword()
                    setPass(Username, newPassword)
                    getpass(
                        'Your password has been changed. Press enter to continue.')
                    return
                else:
                    retry = input('Invalid answer. Try again? (yN) ')
                    if retry.lower() != 'y':
                        return
        else:
            retry = input('Invalid username. Try again? (yN) ')
            if retry.lower() != 'y':
                return


def getMatchesByUser(Username):
    data = command("SELECT * FROM Matches WHERE Username = ?", Username)
    return len(data)


def getWinsByUser(Username):
    data = command(
        "SELECT * FROM Matches WHERE Username = ? AND Won = 1", Username)
    return len(data)


def getWinRateByUser(Username):
    if getMatchesByUser(Username):
        return int(round(getWinsByUser(Username) / getMatchesByUser(Username) * 100, 0))
    return 'N/A'


def getListStats(list):
    return [max(list), min(list), int(round(mean(list), 0))]


def getFieldByUser(Field, Username):
    data = command(
        "SELECT {} FROM Matches WHERE Username = ?".format(Field), Username)
    list = [n[0] for n in data]
    return getListStats(list)


def getPiecesByUser(Username):
    if getMatchesByUser(Username):
        return getFieldByUser('PiecesLeft', Username)
    return ['N/A' for n in range(3)]


def getPointsByUser(Username):
    if getMatchesByUser(Username):
        return getFieldByUser('PointAdvantage', Username)
    return ['N/A' for n in range(3)]


def getMovesByUser(Username):
    if getMatchesByUser(Username):
        return getFieldByUser('Moves', Username)
    return ['N/A' for n in range(3)]


def getLastGameDate(Username):
    if getMatchesByUser(Username):
        return command("SELECT DateOfGame FROM Matches WHERE Username = ?", Username)[-1][0]
    return 'N/A'

def getAIDepthByUser(Username):
    if getMatchesByUser(Username):
        data = command(
            "SELECT AIDepth FROM Matches WHERE Username = ?", Username)[:-10]
        return mode([n[0] for n in data])
    return 'N/A'

def getStats(Username):
    printStats([getMatchesByUser(Username),
                getWinsByUser(Username),
                getWinRateByUser(Username),
                getPiecesByUser(Username),
                getPointsByUser(Username),
                getMovesByUser(Username),
                getLastGameDate(Username),
                getAIDepthByUser(Username)])


def printStats(stats):
    consoleClear()
    print('- Base stats. -\n')
    print(f"{'Total matches played: ':<30}" + f'{stats[0]:>10}')
    print(f"{'Total match wins: ':<30}" + f'{stats[1]:>10}')
    print(f"{'Percentage win rate: ':<30}" + f'{stats[2]:>10}')
    print(f"{'Common AI depth (recent): ':<30}" + f'{stats[7]:>10}')
    print(f"{'Last played game: ':<30}" + f'{stats[6]:>10}\n')
    print('- More stats (most-least-average). -\n')
    print(f"{'Pieces left:':<20}" +
          f'{stats[3][0]:^3}/{stats[3][1]:^3}/{stats[3][2]:>3}')
    print(f"{'Point advantage:':<20}" +
          f'{stats[4][0]:^3}/{stats[4][1]:^3}/{stats[4][2]:>3}')
    print(f"{'Moves made: ':<20}" +
          f'{stats[5][0]:^3}/{stats[5][1]:^3}/{stats[5][2]:>3}\n')
    getpass('Press enter to continue:')


def bootDB():
    dump()
    addInitUser()


def dump():
    command("DELETE FROM Users")


def menu():
    print('Options:\n')
    print('C - Create tables.')
    print('D - Dump data.')
    print('B - Boot database.')
    print('Q - Quit.')
    menuChoice = input('Enter your choice: ')
    return menuChoice


def main():
    while True:
        choice = menu()
        print()
        if choice.lower() == 'c':
            addInitUser()
        elif choice.lower() == 'd':
            dump()
        elif choice.lower() == 'b':
            bootDB()
        elif choice.lower() == 'q':
            return


if __name__ == '__main__':
    main()
