### CSE20 FINAL PROJECT

'''
title: CSE20 Final Project
author: James Ma
date-created: June 14, 2021
'''

import sys
import sqlite3
import pathlib

FILENAME = "Reservation_and_walk_in list.db"

FIRST_RUN = True
if (pathlib.Path.cwd() / FILENAME).exists():
    FIRST_RUN = False


CONNECTION = sqlite3.connect(FILENAME)
CURSOR = CONNECTION.cursor()

# --- SUBROUTINES --- #
def startingScreen():
    '''
    Starting text for the program
    :return: Starting text
    '''
    print('''
Welcome to the reservation organizer!
Organizing you to success!
    ''')

def checkInt(NUM):
    '''
    Verifies whether the number is an integer
    :param NUM: (int) Integer to be verified
    :return: (int)
    '''
    if NUM.isnumeric():
        NUM = int(NUM)
        return NUM
    else:
        print("Please enter a number.")
        NEW_NUM = input(">")
        return checkInt(NEW_NUM)

def askRepeat():
    '''
    Choose whether to end the program
    :return: (bool)
    '''
    REPEAT = input("Use Program Again? Y/n: ")
    if REPEAT == "n" or REPEAT == "N" or REPEAT == "no":
        return False
    else:
        return True


### INPUTS
def startMenu():
    '''
    user selects option
    :return: (int) column to search
    '''
    print('''
1. Reservation
2. Walk-in
3. Delete
    ''')
    CHOICE = input(" > ")
    CHOICE = checkInt(CHOICE)
    if CHOICE > 0 and CHOICE < 4:
        return CHOICE
    else:
        print("Please enter a valid number in the menu.")
        return startMenu()


def reservationSelection():
    '''
    user selects which reservation option to go to
    :return: (str)
    '''
    print('''
1. Add reservation
2. View reservations
3. Edit Reservation
4. Exit Program
    ''')
    CHOICE = checkInt(input("> "))
    if CHOICE > 0 and CHOICE < 5:
        if CHOICE == 1:
            RESERVATIONCHOICE = "ADDR"
        if CHOICE == 2:
            RESERVATIONCHOICE = "VIEWR"
        if CHOICE == 3:
            RESERVATIONCHOICE = "EDITR"
        if CHOICE == 4:
            RESERVATIONCHOICE = "Exit"
        return RESERVATIONCHOICE
    else:
        print("Please enter valid number in the menu.")
        return reservationSelection()

def walkInSelection():
    '''
    user selects which walk-in option to go to
    :return: (str)
    '''
    print('''
1. Add Walk-in
2. View Walk-in's
3. Edit Walk-in
4. Exit Program
    ''')
    CHOICE = checkInt(input("> "))
    if CHOICE > 0 and CHOICE < 5:
        if CHOICE == 1:
            WALKINCHOICE = "ADDW"
        if CHOICE == 2:
            WALKINCHOICE = "VIEWW"
        if CHOICE == 3:
            WALKINCHOICE = "EDITW"
        if CHOICE == 4:
            WALKINCHOICE = "Exit"
        return WALKINCHOICE
    else:
        print("Please enter valid number in the menu.")
        return walkInSelection()

def deleteSelection():
    '''
    user selects which delete option to go to
    :return: (str)
    '''
    print('''
1. Reservation
2. Walk-In
3. Exit Program
    ''')
    CHOICE = checkInt(input("> "))
    if CHOICE > 0 and CHOICE < 4:
        if CHOICE == 1:
            DELETECHOICE = "DELETER"
        if CHOICE == 2:
            DELETECHOICE = "DELETEW"
        if CHOICE == 3:
            DELETECHOICE = "Exit"
        return DELETECHOICE
    else:
        print("Please enter valid number in the menu.")
        return deleteSelection()


def addReservation(RESERVATIONCHOICE):
    '''
    User enters reservation information
    :return: (None)
    '''
    global CURSOR, CONNECTION
    if RESERVATIONCHOICE == "ADDR":
        # Inputs
        FIRST_NAME = input("First Name: ")
        LAST_NAME = input("Last Name: ")
        PHONE = input("Phone number: ")
        DATE = input("Date: ")
        TIME = input("Time: ")
        SECTION = input("Requested Section: ")
        # PROCESSING
        if FIRST_NAME == "" or LAST_NAME == "":
            print("Not enough information given")
            return addReservation(RESERVATIONCHOICE)
        else:
            CURSOR.execute('''
                INSERT INTO
                    reservation(
                        first_name,
                        last_name,
                        phone,
                        date,
                        time,
                        section
                        )
                    VALUES (
                        ?, ?, ?, ?, ?, ?
                        )
                ;''', (FIRST_NAME, LAST_NAME, PHONE, DATE, TIME, SECTION))
        CONNECTION.commit()
        print(f"{FIRST_NAME} {LAST_NAME} successfully added to reservation list!")

def addWalkIn(WALKINCHOICE):
    '''
    User enters walk-in information
    :return: (None)
    '''
    global CURSOR, CONNECTION
    if WALKINCHOICE == "ADDW":
        FIRST_NAME = input("First Name: ")
        LAST_NAME = input("Last Name: ")
        PHONE = input("Phone number: ")
        TIME = input("Time: ")
        if FIRST_NAME == "" or LAST_NAME == "":
            print("Not enough information given")
            return addWalkIn(WALKINCHOICE)
        else:
            CURSOR.execute('''
                INSERT INTO
                    walkin(
                        first_name,
                        last_name,
                        phone,
                        time
                        )
                    VALUES (
                        ?, ?, ?, ?
                        )
                ;''', (FIRST_NAME, LAST_NAME, PHONE, TIME))
        CONNECTION.commit()
        print(f"{FIRST_NAME} {LAST_NAME} successfully added to the Walk In list!")

def chooseReservation():
    '''
    ask the user to select which reservation to edit
    :return: (int) reservation selection
    '''
    global CURSOR
    if RESERVATIONCHOICE == "EDITR":
        RESERVATION = CURSOR.execute('''
            SELECT
                id,
                first_name,
                last_name,
                phone,
                date,
                time,
                section
            FROM
                reservation
            ORDER BY
                first_name
        ;''').fetchall()

        print("Please select a reservation")
        for i in range(len(RESERVATION)):
            print(f"{i+1}. {RESERVATION[i][1]} {RESERVATION[i][2]}")

        SELECTION = checkInt(input("> "))-1
        RESERVATIONSELECTION = RESERVATION[SELECTION][0]
        return RESERVATIONSELECTION

def chooseWalkIn():
    '''
    ask the user to select which walk-in to edit
    :return: (int) walk-in selection
    '''
    global CURSOR
    if WALKINCHOICE == "EDITW":
        WALKIN = CURSOR.execute('''
            SELECT
                id,
                first_name,
                last_name,
                phone,
                time
            FROM
                walkin
            ORDER BY
                time
        ;''').fetchall()

        print("Please select a walk-in")
        for i in range(len(WALKIN)):
            print(f"{i+1}. {WALKIN[i][1]} {WALKIN[i][2]}")

        SELECTION = checkInt(input("> "))-1
        WALKINSLSECTION = WALKIN[SELECTION][0]
        return WALKINSLSECTION

def chooseDeleteReservation():
    '''
    ask the user to select which reservation to delete
    :return: (int) delete reservation selection
    '''
    global CURSOR
    if DELETECHOICE == "DELETER":
        RESERVATIONDELETE = CURSOR.execute('''
            SELECT
                id,
                first_name,
                last_name,
                phone,
                date,
                time,
                section
            FROM
                reservation
            ORDER BY
                first_name
        ;''').fetchall()

        print("Please select a reservation")
        for i in range(len(RESERVATIONDELETE)):
            print(f"{i+1}. {RESERVATIONDELETE[i][1]} {RESERVATIONDELETE[i][2]}")

        SELECTION = checkInt(input("> "))-1
        RESERVATIONSELECTION = RESERVATIONDELETE[SELECTION][0]
        return RESERVATIONSELECTION


def chooseDeleteWalkIn():
    '''
    ask the user to select which walk-in to delete
    :return: (int) delete walk-in selection
    '''
    global CURSOR
    if DELETECHOICE == "DELETEW":
        WALKINDELETE = CURSOR.execute('''
            SELECT
                id,
                first_name,
                last_name,
                phone,
                time
            FROM
                walkin
            ORDER BY
                first_name
        ;''').fetchall()

        print("Please select a reservation")
        for i in range(len(WALKINDELETE)):
            print(f"{i+1}. {WALKINDELETE[i][1]} {WALKINDELETE[i][2]}")

        SELECTION = checkInt(input("> "))-1
        WALKINSELECTION = WALKINDELETE[SELECTION][0]
        return WALKINSELECTION


def editReservation(RINFO, RESERVATIONCHOICE):
    '''
    User updates the reservation information
    :param RINFO: (int) Chosen reservation to edit
    :param RESERVATIONCHOICE: (int) Chosen reservation option
    :return: (none)
    '''

    global CURSOR, CONNECTION
    if RESERVATIONCHOICE == "EDITR":

        RESERVATION = CURSOR.execute('''
            SELECT
                first_name,
                last_name,
                phone,
                date,
                time,
                section
            FROM
                reservation
            WHERE
                id = ?
        ;''', [RINFO]).fetchone()

        print("Leave field blank for no changes")
        FIRST_NAME = input(f"First Name({RESERVATION[0]}): ")
        LAST_NAME = input(f"Last Name ({RESERVATION[1]}): ")
        PHONE = input(f"Phone ({RESERVATION[2]}): ")
        DATE = input(f"Date ({RESERVATION[3]}): ")
        TIME = input(f"Time ({RESERVATION[4]}): ")
        SECTION = input(f"Requested Section ({RESERVATION[5]}): ")

        NEW_INFO = []
        if FIRST_NAME == "":
            NEW_INFO.append(RESERVATION[0])
        else:
            NEW_INFO.append(FIRST_NAME)
        if LAST_NAME == "":
            NEW_INFO.append(RESERVATION[1])
        else:
            NEW_INFO.append(LAST_NAME)
        if PHONE == "":
            NEW_INFO.append(RESERVATION[2])
        else:
            NEW_INFO.append(PHONE)
        if DATE == "":
            NEW_INFO.append(RESERVATION[3])
        else:
            NEW_INFO.append(DATE)
        if TIME == "":
            NEW_INFO.append(RESERVATION[4])
        else:
            NEW_INFO.append(TIME)
        if SECTION == "":
            NEW_INFO.append(RESERVATION[5])
        else:
            NEW_INFO.append(SECTION)
        NEW_INFO.append(RINFO)


        CURSOR.execute('''
            UPDATE
                reservation
            SET
                first_name = ?,
                last_name = ?,
                phone = ?,
                date = ?,
                time = ?,
                section = ?
            WHERE
                id = ?
        ;''', NEW_INFO)

        CONNECTION.commit()
        print(f"{NEW_INFO[0]} {NEW_INFO[1]} was successfully updated!")

def editWalkin(WINFO, WALKINCHOICE):
    '''
    User updates the walk-in information
    :param WINFO: (int) Chosen walk-in to edit
    :param WALKINCHOICE: (int) Chosen walk-in option
    :return: (none)
    '''
    global CURSOR, CONNECTION
    if WALKINCHOICE == "EDITW":

        WALKIN = CURSOR.execute('''
            SELECT
                first_name,
                last_name,
                phone,
                time
            FROM
                walkin
            WHERE
                id = ?
        ;''', [WINFO]).fetchone()

        print("Leave field blank for no changes")
        FIRST_NAME = input(f"First Name({WALKIN[0]}): ")
        LAST_NAME = input(f"Last Name ({WALKIN[1]}): ")
        PHONE = input(f"Phone ({WALKIN[2]}): ")
        TIME = input(f"Time ({WALKIN[3]}): ")

        INFO = []
        if FIRST_NAME == "":
            INFO.append(WALKIN[0])
        else:
            INFO.append(FIRST_NAME)
        if LAST_NAME == "":
            INFO.append(WALKIN[1])
        else:
            INFO.append(LAST_NAME)
        if PHONE == "":
            INFO.append(WALKIN[2])
        else:
            INFO.append(PHONE)
        if TIME == "":
            INFO.append(WALKIN[3])
        else:
            INFO.append(TIME)
        INFO.append(WINFO)

        CURSOR.execute('''
            UPDATE
                walkin
            SET
                first_name = ?,
                last_name = ?,
                phone = ?,
                time = ?
            WHERE
                id = ?
        ;''', INFO)

        CONNECTION.commit()
        print(f"{INFO[0]} {INFO[1]} was successfully updated!")


### PROCESSING

def reservationTable():
    '''
    creates reservation table if first run
    :return: (None)
    '''
    global CURSOR, CONNECTION

    CURSOR.execute('''
        CREATE TABLE
            reservation(
                id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                phone TEXT NOT NULL, 
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                section TEXT
            )
    ;''')

    CONNECTION.commit()

def walkinTable():
    '''
    creates walk-in table if first run
    :return: (None)
    '''
    global CURSOR, CONNECTION

    CURSOR.execute('''
        CREATE TABLE 
            walkin(
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ;''')

    CONNECTION.commit()


def deleteReservation(DELETECHOICE, RINFO):
    '''
    Deletes reservation from reservation table
    :param DELETECHOICE: (int) chosen delete option
    :param RINFO: (int) chosen reservation to delete
    :return: (none)
    '''

    global CURSOR, CONNECTION
    if DELETECHOICE == "DELETER":
        DELETER = CURSOR.execute('''
            SELECT
                first_name,
                last_name,
                phone,
                date,
                time,
                section
            FROM
                reservation
            WHERE
                id = ?
        ;''', [RINFO]).fetchone()

        CURSOR.execute('''
            DELETE FROM
                reservation
            WHERE
                id = ?
        ;''', [RINFO])

        CONNECTION.commit()

        print("Successfully Deleted!")


def deleteWalkIn(DELETECHOICE, WINFO):
    '''
    Deletes walk-in from walkin table
    :param DELETECHOICE: (int) chosen delete option
    :param WINFO: (int) chosen walk-in to delete
    :return: (none)
    '''
    global CURSOR, CONNECTION
    if DELETECHOICE == "DELETEW":
        DELETEW = CURSOR.execute('''
            SELECT
                first_name,
                last_name,
                phone,
                time
            FROM
                walkin
            WHERE
                id = ?
        ;''', [WINFO]).fetchone()

        CURSOR.execute('''
            DELETE FROM
                walkin
            WHERE
                id = ?
        ;''', [WINFO])

        CONNECTION.commit()

        print("Successfully Deleted!")

def exitReservation(RESERVATIONCHOICE):
    '''
    Exits program for reservation option
    :param RESERVATIONCHOICE: (int) chosen reservation option
    :return: (none)
    '''
    if RESERVATIONCHOICE == "Exit":
        print("Have a nice day!")
        sys.exit()

def exitWalkin(WALKINCHOICE):
    '''
    Exits program for walk-in option
    :param WALKINCHOICE: (int) chosen walk-in option
    :return: (none)
    '''
    if WALKINCHOICE == "Exit":
        print("Have a nice day!")
        sys.exit()

def exitDelete(DELETECHOICE):
    '''
    Edits program for delete option
    :param DELETECHOICE: (int) chosen delete option
    :return: (none)
    '''
    if DELETECHOICE == "Exit":
        print("Have a nice day!")
        sys.exit()

### OUTPUTS

def dispReservations(RESERVATIONCHOICE):
    '''
    Displays all reservations starting with date
    :return: (None)
    '''
    if RESERVATIONCHOICE == "VIEWR":
        RESERVATIONS = CURSOR.execute('''
            SELECT
                date,
                first_name,
                last_name,
                phone,
                time,
                section
            FROM
                reservation
            ORDER BY
                date
        ;''').fetchall()
        for item in RESERVATIONS:
            print(*item, sep= ', ')

def dispWalkIn(WALKINCHOICE):
    '''
    Displays all walk-ins starting with time
    :return: (None)
    '''
    if WALKINCHOICE == "VIEWW":
        WALKIN = CURSOR.execute('''
            SELECT
                time,
                first_name,
                last_name,
                phone
            FROM
                walkin
            ORDER BY
                time
        ;''').fetchall()
        for item in WALKIN:
            print(*item, sep= ', ')


### --- MAIN PROGRAM CODE --- ###
if __name__ == "__main__":
    startingScreen()
    if FIRST_RUN:
        reservationTable()
        walkinTable()
    while True:
        OPTION = startMenu()
        if OPTION == 1:
            RESERVATIONCHOICE = reservationSelection()
            addReservation(RESERVATIONCHOICE)
            dispReservations(RESERVATIONCHOICE)
            RINFO = chooseReservation()
            editReservation(RINFO, RESERVATIONCHOICE)
            exitReservation(RESERVATIONCHOICE)
            if not askRepeat():
                print("Have a nice day!")
                sys.exit()
        if OPTION == 2:
            WALKINCHOICE = walkInSelection()
            addWalkIn(WALKINCHOICE)
            dispWalkIn(WALKINCHOICE)
            WINFO = chooseWalkIn()
            editWalkin(WINFO, WALKINCHOICE)
            exitWalkin(WALKINCHOICE)
            if not askRepeat():
                print("Have a nice day!")
                sys.exit()
        if OPTION == 3:
            DELETECHOICE = deleteSelection()
            RINFO = chooseDeleteReservation()
            deleteReservation(DELETECHOICE, RINFO)
            WINFO = chooseDeleteWalkIn()
            deleteWalkIn(DELETECHOICE, WINFO)
            exitDelete(DELETECHOICE)
            if not askRepeat():
                print("Have a nice day!")
                sys.exit()