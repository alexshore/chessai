import sqlite3, os, datetime as dt, re
from getpass import *

def consoleClear():
    os.system('cls')
    os.system('cls')

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

def addInitUser():
    date = dt.datetime.today().strftime('%d/%m/%Y')
    temp = ['ashore', 'pw', True, 'Alex', 'Shore', date, 1, 'echo']
    command("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", temp[0], temp[1], temp[2], temp[3],
                                                                    temp[4], temp[5], temp[6], temp[7])
    temp = ['jfrost', 'pw', False, 'James', 'Frost', date, 1, 'honey']
    command("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", temp[0], temp[1], temp[2], temp[3],
                                                                    temp[4], temp[5], temp[6], temp[7])

def addNewUser(username, password, isAdmin, firstName, surName, date, SID, answer):
    command("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", username, password, isAdmin, firstName,
                                                                    surName, date, SID, answer)
def checkUsernameExists(Username):
    valid = command("SELECT Users.Username FROM Users WHERE Users.Username = ?", Username)
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

def printAllUsers():
    users = getAllUsers()
    print('+' + '-' * 15 + '+' + '-' * 13 + '+' + '-' * 17 + '+' + '-' * 13 + '+')
    print(f"|{'Username':>14} |{'Firstname':>12} |{'Surname':>16} |{'Created':>12} |")
    print('+' + '-' * 15 + '+' + '-' * 13 + '+' + '-' * 17 + '+' + '-' * 13 + '+')
    for user in users:
        print(f"|{user[0]:>14} |{user[1]:>12} |{user[2]:>16} |{user[3]:>12} |")
    print('+' + '-' * 15 + '+' + '-' * 13 + '+' + '-' * 17 + '+' + '-' * 13 + '+')

def getAllUsers():
    data = command("""
SELECT Users.Username,
Users.FirstName,
Users.SurName,
Users.created
FROM Users""")
    return data

def printUserDetails(Username):
    Username, Password, isAdmin, FirstName, SurName, Created = getUserDetails(Username)
    connector ='+' + '-' * 15 + '+' + '-' * 19 + '+' + '-' * 10 + \
               '+' + '-' * 13 + '+' + '-' * 17 + '+' + '-' * 13 + '+'
    print(connector)
    print(f"|{'Username':>14} |{'Password':>18} |{'isAdmin':>9} " + \
          f"|{'FirstName':>12} |{'SurName':>16} |{'Created':>12} |")
    print(connector)
    print(f"|{Username:>14} |{Password:>18} |{isAdmin:>9} " + \
          f"|{FirstName:>12} |{SurName:>16} |{Created:>12} |")
    print(connector + '\n')

def editUser(isAdmin, Username):
    while True:
        consoleClear()
        printUserDetails(Username)
        fieldChange = input('\nWhich field would you like to change (case-sensitive): ')
        consoleClear()
        NewItem = None
        if fieldChange == 'Username' and isAdmin:
            NewItem = getUsername()
        elif fieldChange == 'Password':
            NewItem = getPassword()
        elif fieldChange == 'isAdmin':
            NewItem = getEditableAdmin() if isAdmin else getIsAdmin()
        elif fieldChange == 'FirstName':
            NewItem = input('Firstname: ')
        elif fieldChange == 'SurName':
            NewItem = input('Surname: ')
        elif fieldChange == 'Created' and isAdmin:
            NewItem = getEditableDate()
        else:
            retry = input('Invalid field entered. Re-enter? (yN) ')
            if retry.lower() != 'y':
                input('Returning to menu. Press enter to continue.')
                break
        if NewItem:
            try:
                editUserField(fieldChange, NewItem, Username)
                print(f'{fieldChange} changed to {NewItem} for {Username}.')
                input('Press enter to continue.')
                break
            except:
                input('Something went wrong. Press enter to try again.')

def editUserField(Field, NewItem, Username):
    command("UPDATE Users SET {} = ? WHERE Username = ?".format(Field), NewItem, Username)

def getUserDetails(Username):
    return command("SELECT * FROM Users WHERE Users.Username = ?", Username)[0][:6]

def checkPasswordMatch(Username):
    while True:
        Password = getpass()
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
            return isAdmin, FirstName, Username
        else:
            tryAgain = input('Invalid username/password. Retry? (yN) ')
            if tryAgain.lower() != 'y':
                return

def getUsername():
    while True:
        consoleClear()
        Username = input('Username: ')
        if not checkUsernameExists(Username):
            return Username
        else:
            print('Username already in use, try another.\n')

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
            Password = getpass()
            if checkPasswordValidity(Password):
                break
        confirmationPass = getpass('Please confirm password: ')
        if confirmationPass == Password:
            return Password
        else:
            consoleClear()
            print('Passwords don\'t match. Try again.\n')

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
            input('Correct code, setting as admin. Press enter to continue.')
            return True
        tryAgain = input('\nIncorrect code. Try again? (yN) ')
        if tryAgain.lower() != 'y':
            return False

def getEditableDate():
    consoleClear()
    while True:
        try:
            Year = input('What year was this account created: ')
            Month = input('What month was this account created: ')
            Day = input('What day was this account created: ')
            date = dt.date(Year, Month, Day)
        except:
            input('Invalid time entered. Press enter to try again.')
    return date.strftime('%d/%m%Y')

def getCurrentDate():
    return dt.datetime.today().strftime('%d/%m/%Y')

def getSecurity():
    consoleClear()
    data = getSecurityQuestions()
    while True:
        print('Security Questions:')
        for i in range(len(data)):
            print('{} - {}'.format(data[i][0], data[i][1]))
        SID = int(input('Option: ')[0])
        if SID not in [i for i in range(1, len(data))]:
            print('\nInvalid choice. Try again.')
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
    addNewUser(Username, Password, isAdmin, Firstname, Surname, date, SID, Answer)

def forgotPassword():
    while True:
        consoleClear()
        print('- Password recovery -\n')
        Username = input('Username: ')
        if checkUsernameExists(Username):
            print(getQuestion(Username))
            while True:
                Answer = input('Answer: ')
                if Answer == getAnswer(Username):
                    input('You may now enter a new password. Press enter to continue.')
                    newPassword = getPassword()
                    setPass(Username, newPassword)
                    input('Your password has been changed. Press enter to continue.')
                    return
                else:
                    retry = input('Invalid answer. Try again? (yN) ')
                    if retry.lower() != 'y':
                        return
        else:
            retry = input('Invalid username. Try again? (yN) ')
            if retry.lower() != 'y':
                return

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
