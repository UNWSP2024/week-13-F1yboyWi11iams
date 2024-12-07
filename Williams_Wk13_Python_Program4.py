import sqlite3

MIN_CHOICE = 1
MAX_CHOICE = 5
CREATE = 1
READ = 2
UPDATE = 3
DELETE = 4
EXIT = 5


def main():
    # Connect to the database.
    conn = sqlite3.connect('phonebook.db')

    # Get a database cursor.
    cur = conn.cursor()

    # Add the Cities table.
    add_entries_table(cur)

    # Add rows to the Cities table.
    add_entries(cur)

    # Commit the changes.
    conn.commit()

    # Display the cities.
    display_entries(cur)

    # Close the connection.
    conn.close()


# The add_cities_table adds the Cities table to the database.
def add_entries_table(cur):
    # If the table already exists, drop it.
    cur.execute('DROP TABLE IF EXISTS Entries')

    # Create the table.
    cur.execute('''CREATE TABLE Entries (CallerID INTEGER PRIMARY KEY NOT NULL,
                                        CallerName TEXT,
                                        CallerNumber REAL)''')


# The add_cities function adds 20 rows to the Entries table.
def add_entries(cur):
    entries = [(1, 'Tokyo', 38001000),
               (2, 'Delhi', 25703168),
               (3, 'Shanghai', 23740778),
               (4, 'Sao Paulo', 21066245),
               (5, 'Mumbai', 21042538),
               (6, 'Mexico City', 20998543),
               (7, 'Beijing', 20383994),
               (8, 'Osaka', 20237645),
               (9, 'Cairo', 18771769),
               (10, 'New York', 18593220),
               (11, 'Dhaka', 17598228),
               (12, 'Karachi', 16617644),
               (13, 'Buenos Aires', 15180176),
               (14, 'Kolkata', 14864919),
               (15, 'Istanbul', 14163989),
               (16, 'Chongqing', 13331579),
               (17, 'Lagos', 13122829),
               (18, 'Manila', 12946263),
               (19, 'Rio de Janeiro', 12902306),
               (20, 'Guangzhou', 12458130)]

    for entry in entries:
        cur.execute('''INSERT INTO Entries (CallerID, CallerName, CallerNumber)
                       VALUES (?, ?, ?)''', (entry[0], entry[1], entry[2]))


# The display_cities function displays the contents of
# the Cities table.
def display_entries(cur):
    print('Contents of phonebook.db/Entries table:')
    cur.execute('SELECT * FROM Entries')
    results = cur.fetchall()
    for row in results:
        print(f'{row[0]:<3}{row[1]:20}{row[2]:,.0f}')

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
    print('Create New Contact')
    name = input('Contact Name: ')
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
        num_deleted = delete_entry(selected_id)
        print(f'{num_deleted} row(s) deleted.')

def insert_row(name, number):
    conn = None
    try:
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        cur.execute('''INSERT INTO Entries (CallerName, CallerNumber)
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
        WHERE lower(CallerName) == ?''',
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
        SET CallerName = ?, CallerNumber = ?
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
        WHERE CallerID == ?''',
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
