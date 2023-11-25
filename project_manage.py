import sys

from database import Database
import csv

database_instance = Database()


class CsvReader:
    @staticmethod
    def read_csv(filename):
        data = []
        with open(filename, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(dict(row))
        return data


class Persons:
    def __init__(self):
        self.person_data = []

    def add_person(self, person_data):
        self.person_data.append(person_data)


class Login:
    def __init__(self):
        self.login_data = []

    def add_login(self, person_id, username, password, user_role):
        login_entry = {"person_id": person_id, "username": username, "password": password, "role": user_role}
        self.login_data.append(login_entry)

    def __str__(self):
        return ""


def initializing():
    persons_table = Persons()
    persons_data = CsvReader().read_csv('persons.csv')
    for person in persons_data:
        persons_table.add_person(person)

    login_table_instance = Login()
    login_data = CsvReader().read_csv('login.csv')

    for login_entry in login_data:
        person_id = login_entry['person_id']
        username = login_entry['username']
        password = login_entry['password']
        user_role = login_entry['role']

        login_table_instance.add_login(person_id, username, password, user_role)

    return login_table_instance


def login(logins_table):
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        for entry in logins_table.login_data:
            if entry['username'] == username and entry['password'] == password:
                result = [entry['person_id'], entry['role']]
                print(f"Login successful! User ID: {result[0]}, Role: {result[1]}")
                return result

        print("Invalid login user ID or password. Please try again.")
        attempts += 1
    print("Too many unsuccessful login attempts. Exiting the program.")
    exit_program()


def exit_program():
    sys.exit()


# Make calls to the initializing and login functions defined above
login_table = initializing()
val = login(login_table)

if val:
    if val[1] == 'admin':
        print("Admin activities")
    elif val[1] == 'student':
        print("Student activities")
    elif val[1] == 'member':
        print("Member activities")
    elif val[1] == 'lead':
        print("Lead activities")
    elif val[1] == 'faculty':
        print("Faculty activities")
    elif val[1] == 'advisor':
        print("Advisor activities")
# Once everything is done, make a call to the exit function
exit_program()
