import sqlite3

connection = sqlite3.connect('database.db')

with connection:
    connection.execute("""CREATE TABLE IF NOT EXISTS employees (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        HiredDate TEXT NOT NULL,
                        Name TEXT NOT NULL,
                        Surname TEXT NOT NULL,
                        PhoneNumber TEXT UNIQUE NOT NULL,
                        Email TEXT UNIQUE NOT NULL,
                        Address TEXT NOT NULL,
                        Position TEXT NOT NULL,
                        BadgeID TEXT UNIQUE NOT NULL,
                        Password TEXT UNIQUE NOT NULL);""")

    connection.execute("""CREATE TABLE IF NOT EXISTS employees_pics (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name TEXT NOT NULL,
                        Picture BLOB NOT NULL);""")


def insert_data(values):
    print(values)
    with connection:
        data_execute = connection.execute("""INSERT OR IGNORE INTO employees (HiredDate, Name, Surname, PhoneNumber, Email, Address, Position, BadgeID, Password) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""", values)


def show_employees():
    employees = connection.execute('SELECT * FROM employees;')
    columns = [description[0] for description in employees.description]

    return employees, columns

def show_employee_id(ide):
    employee = connection.execute('SELECT Name, Surname, HiredDate, PhoneNumber, Email, Address, Position, BadgeID FROM employees WHERE ID = ?;', (ide,))
    columns = [description[0] for description in employee.description]
    return employee, columns

def get_pic_data(employee_id):
    with connection:
        pic_data = connection.execute('SELECT * FROM employees_pics INNER JOIN employees ON employees.ID = employees_pics.ID WHERE employees.ID = ?;', (employee_id,))
        name_surname = connection.execute('SELECT Name, Surname FROM employees WHERE ID = ?', (employee_id,))

    for i in pic_data.fetchall():
        pic_data = i

    for i in name_surname.fetchall():
        name_surname = i

    with open(f'New_Pictures/{name_surname[1]}_{name_surname[0]}.gif', 'wb') as picture:
        picture.write(pic_data[2])

def store_pic_data(name, pic_path):
    with open(pic_path, 'rb') as pic:
        pic_data = pic.read()

    with connection:
        data_execute = connection.execute('INSERT OR IGNORE INTO employees_pics (Name, Picture) VALUES (?, ?);', (name, pic_data))


def get_badge_ids():
    return connection.execute('SELECT BadgeID FROM employees;')


def get_display_data():
    with connection:
        names = connection.execute('SELECT Name, Surname, BadgeID, Position FROM employees;')
        return names

def test():
    # store picture
    with open('icon.png', 'rb') as picture:
        pic_details = picture.read()

    with connection:
        connection.execute('INSERT INTO employees_pics (Name, Picture) VALUES (?, ?)', ('Picture', pic_details,))
