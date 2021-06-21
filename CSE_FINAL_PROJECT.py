### CSE20 FINAL PROJECT

'''
title: CSE20 Final Project
author: James Ma
date-created: June 14, 2021
'''

import sys
import sqlite3
import pathlib

DB_FILENAME = "Reservation_and_walk_in list.db"

FIRST_RUN = True
if (pathlib.Path.cwd() / DB_FILENAME).exists():
    FIRST_RUN = False

CONNECTION = sqlite3.connect(DB_FILENAME)
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
    :param NUM: (int) Value to be verified
    :return: (int)
    '''
    if NUM.isnumeric():
        NUM = int(NUM)
        return NUM
    else:
        print("Please enter a number.")
        NEW_NUM = input(">")
        return checkInt(NEW_NUM)

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
2. View Walk-in's and who is next in line
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
    User enters reservation information
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

def getReservationID():
    '''
    ask the user to select which reservation
    :return: (int) Contact ID (Primary Key)
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

        INDEX = int(input("> "))
        CONTACT_ID = RESERVATION[INDEX][0]
        return CONTACT_ID

def getWalkinID():
    '''
    ask the user to select which reservation
    :return: (int) Contact ID (Primary Key)
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

        INDEX = int(input("> "))
        CONTACT_ID = WALKIN[INDEX][0]
        return CONTACT_ID


def editReservation(RINFO, RESERVATIONCHOICE):
    '''
    User updates contact information
    :param INFO: (int)
    :return: (None)
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
                INFO = ?
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
            NEW_INFO.appened(TIME)
        if SECTION == "":
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
                section = ?
            WHERE
                id = ?
        ;''', NEW_INFO)

        CONNECTION.commit()
        print(f"{NEW_INFO[0]} {NEW_INFO[1]} was successfully updated!")

def editWalkin(WINFO, WALKINCHOICE):
    '''
    User updates contact information
    :param INFO: (int)
    :return: (None)
    '''

    global CURSOR, CONNECTION
    if WALKINCHOICE == "EDITW":

        WALKIN = CURSOR.execute('''
            SELECT
                first_name,
                last_name,
                phone,
                date,
                section
            FROM
                walkin
            WHERE
                INFO = ?
        ;''', [WINFO]).fetchone()

        print("Leave field blank for no changes")
        FIRST_NAME = input(f"First Name({WALKIN[0]}): ")
        LAST_NAME = input(f"Last Name ({WALKIN[1]}): ")
        PHONE = input(f"Phone ({WALKIN[2]}): ")
        TIME = input(f"Time ({WALKIN[3]}): ")

        NEW_INFO = []
        if FIRST_NAME == "":
            NEW_INFO.append(WALKIN[0])
        else:
            NEW_INFO.append(FIRST_NAME)
        if LAST_NAME == "":
            NEW_INFO.append(WALKIN[1])
        else:
            NEW_INFO.append(LAST_NAME)
        if PHONE == "":
            NEW_INFO.append(WALKIN[2])
        else:
            NEW_INFO.append(PHONE)
        if TIME == "":
            NEW_INFO.append(WALKIN[3])
        else:
            NEW_INFO.append(TIME)

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
        ;''', NEW_INFO)

        CONNECTION.commit()
        print(f"{NEW_INFO[0]} {NEW_INFO[1]} was successfully updated!")


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
    create the contacts table if it is the first run.
    :return: (None)
    '''
    global CURSOR, CONNECTION

    CURSOR.execute('''
        CREATE TABLE walkin(
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ;''')

    CONNECTION.commit()

def exitReservation(RESERVATIONCHOICE):
    if RESERVATIONCHOICE == "Exit":
        print("Have a nice day!")
        sys.exit()

def exitWalkin(WALKINCHOICE):
    if WALKINCHOICE == "Exit":
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
                first_name,
                last_name,
                phone,
                date,
                time,
                section
            FROM
                reservation
            ORDER BY
                date
                time
        ;''').fetchall()

        for i in range(len(RESERVATIONS)):
            print(f"{RESERVATIONS}")

def dispWalkIn(WALKINCHOICE):
    '''
    Displays all reservations starting with date
    :return: (None)
    '''
    if WALKINCHOICE == "VIEWW":
        WALKIN = CURSOR.execute('''
            SELECT
                first_name,
                last_name,
                phone,
                time
            FROM
                walkin
            ORDER BY
                time
        ;''').fetchall()

        for i in range(len(WALKIN)):
            print(f"{WALKIN}")


### --- MAIN PROGRAM CODE --- ###
if __name__ == "__main__":
    while True:
        startingScreen()
        OPTION = startMenu()
        if FIRST_RUN:
            walkinTable()
            reservationTable()
        if OPTION == 1:
            RESERVATIONCHOICE = reservationSelection()
            addReservation(RESERVATIONCHOICE)
            dispReservations(RESERVATIONCHOICE)
            RINFO = getReservationID()
            editReservation(RINFO,RESERVATIONCHOICE)
            exitReservation(RESERVATIONCHOICE)
        if OPTION == 2:
            WALKINCHOICE = walkInSelection()
            addWalkIn(WALKINCHOICE)
            dispWalkIn(WALKINCHOICE)
            WINFO = getWalkinID()
            editWalkin(WINFO, WALKINCHOICE)
            exitWalkin(WALKINCHOICE)


        if OPTION == 3:
            pass