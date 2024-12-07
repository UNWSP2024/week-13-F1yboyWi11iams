import sqlite3
from random import choice

MIN_CHOICE = 1
MAX_CHOICE = 5
CREATE = 1
READ = 2
UPDATE = 3
DELETE = 4
EXIT = 5

def main():
    choice = 0
    while choice != EXIT:
        display_menu()
        choice = get_menu_choice()

        if choice == CREATE:
            create()
        elif choice == READ:
            read()
        elif choice == UPDATE:
            update()
        elif choice == DELETE:
            delete()

def display_menu():
    print('\n----- Entries Menu -----')
    print('1. Create a new item')
    print('2. Read an item')
    print('3. Update an item')
    print('4. Delete an item')
    print('5. Exit the program')

def get_menu_choice():
    choice = int(input('Enter your choice: '))

    while choice < MIN_CHOICE or choice > MAX_CHOICE:
        print(f'Valid choices are {MIN_CHOICE} through {MAX_CHOICE}.')
        choice = int(input('Enter your choice: '))

    return choice

def create():
    print('Create New Item')
    name = input('Item Name: ')
    number = input('Phone Number: ')
    insert_row(name, number)

def read():
    name = input('Enter an item name to search for: ')
    num_found = display_item(name)
    print(f'{num_found} row(s) found.')

def update():
    read()

    selected_id = int(input('Select a Caller ID: '))

    name = input('Enter the new Caller name: ')
    number = input('Enter the new number: ')

    num_updated = update_row(selected_id, name, number)

def delete():
    read()

    selected_id = int(input('Select a Caller ID to delete: '))

    sure = input("Are you sure you want to delete this contact? (y/n): ")
    if sure.lower() == 'y':
        num_deleted = delete_row(selected_id)
        print(f'{num_deleted} row(s) deleted.')

def insert_row(name, number):
    conn = None
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        cur.execute('''INSERT INTO Entries (ItemName, Number)
        VALUES (?, ?)''',
                    (name, number))
        conn.commit()
    except sqlite3.Error as err:
        print('Database Error', err)
    finally:
        if conn != None:
            conn.close()

def display_item(name):
    conn = None
    results = []
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        cur.execute('''SELECT * FROM Entries
        WHERE lower(ItemName) == ?''',
                    (name.lower(),))
        results = cur.fetchall()

        for row in results:
            print(f'ID: {row[0]:<3} Name: {row[1]:<15} '
                  f'Number: {row[2]:<6}')
    except sqlite3.Error as err:
        print('Database Error', err)
    finally:
        if conn != None:
            conn.close()
    return len(results)

def update_row(id, name, number):
    conn = None
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        cur.execute('''UPDATE Entries
        SET Itemname = ?, Number = ?
        WHERE CallerID == ?''',
                    (name, number, id))
        conn.commit()
        num_updated = cur.rowcount
    except sqlite3.Error as err:
        print('Database Error', err)
    finally:
        if conn != None:
            conn.close()

    return num_updated

def delete_row(id):
    conn = None
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        cur.execute('''DELETE FROM Entries
        WHERE ItemID == ?''',
                    (id,))
        conn.commit()
        num_deleted = cur.rowcount
    except sqlite3.Error as err:
        print('Database Error', err)
    finally:
        if conn != None:
            conn.close()

    return num_deleted

if __name__ == '__main__':
    main()