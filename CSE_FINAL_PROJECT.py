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
Welcome to the reservation organizer
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



def reservationSelectionl():
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
    if CHOICE > 0 and CHOICE < 4:
        if CHOICE == 1:
            RESERVATIONCHOICE = "ADDR"
        if CHOICE == 2:
            RESERVATIONCHOICE = "VIEWR"
        if CHOICE == 3:
            RESERVATIONCHOICE = "EXITR"
        if CHOICE == 4:
            RESERVATIONCHOICE = "Exit"
        return RESERVATIONCHOICE
    else:
        print("Please enter valid number in the menu.")
        return

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
    if CHOICE > 0 and CHOICE < 4:
        if CHOICE == 1:
            RESERVATIONCHOICE = "ADDW"
        if CHOICE == 2:
            RESERVATIONCHOICE = "VIEWW"
        if CHOICE == 3:
            RESERVATIONCHOICE = "EDITW"
        if CHOICE == 4:
            RESERVATIONCHOICE = "Exit"
        return RESERVATIONCHOICE
    else:
        print("Please enter valid number in the menu.")
        return

def addReservation():
    '''
    User enters reservation information
    :return: (None)
    '''
    global CURSOR, CONNECTION
    # Inputs
    FIRST_NAME = input("First Name: ")
    LAST_NAME = input("Last Name: ")
    PHONE = input("Phone number: ")
    DATE = input("Date: ")
    SECTION = input("Requested Section?: ")
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
                    section,
                    )
                VALUES (
                    ?, ?, ?, ?
                    )
            ;''', (FIRST_NAME, LAST_NAME, PHONE, DATE, SECTION))

    # Output
    CONNECTION.commit()
    print(f"{FIRST_NAME} {LAST_NAME} successfully added to reservation list!")


### PROCESSING

def reservationTable():
    '''
    creates reservation table if first run
    :return: (None)
    '''
    global CURSOR, CONNECTION

    CURSOR.execute('''
        CREATE TABLE reservation(
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT NOT NULL, 
            date TEXT NOT NULL,
            section TEXT
        )
    ;''')

    CONNECTION.commit()

def walkinTable():


### OUTPUTS



### --- MAIN PROGRAM CODE --- ###
if __name__ == "__main__":
