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


def load_roles_from_csv(filename):
    roles_set = set()
    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            roles_set.add(row['role'])
    return roles_set


class Persons:
    def __init__(self):
        self.person_data = []

    def add_person(self, person_data):
        self.person_data.append(person_data)


class Login:
    def __init__(self):
        self.login_data = []
        self.database_instance = database_instance

    def add_login(self, person_id, username, password, role):
        login_entry = {"person_id": person_id, "username": username, "password": password, "role": role}
        self.login_data.append(login_entry)
        self.database_instance.insert_data('login_table', login_entry)


def initializing():
    person_table = Persons()
    persons_data = CsvReader().read_csv('persons.csv')

    for person in persons_data:
        person_table.add_person(person)

    login_table_instance = Login()
    login_data = CsvReader().read_csv('login.csv')

    for login_entry in login_data:
        person_id = login_entry['ID']
        username = login_entry['username']
        password = login_entry['password']
        role = login_entry['role']

        login_table_instance.add_login(person_id, username, password, role)

    return person_table, login_table_instance


def login(logins_table):
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        for entry in logins_table.login_data:
            if entry['username'] == username and entry['password'] == password:
                result = [entry['person_id'], entry['role']]
                print(f"Login successful! Welcome User ID: {result[0]}, Role: {result[1]}")
                return result

        print("----------------------------------------------------")
        print("Invalid login user ID or password. Please try again.")
        print("----------------------------------------------------")

        attempts += 1
    print("<< Too many unsuccessful login attempts. Exiting the program. >>")
    exit_program()


def exit_program():
    sys.exit()


class AdvisorPendingRequest:
    def __init__(self, project_id, to_be_advisor, response=None, response_data=None):
        self.project_id = project_id
        self.to_be_advisor = to_be_advisor
        self.response = response
        self.response_data = response_data


class MemberPendingRequest:
    def __init__(self, project_id, to_be_member, response=None, response_data=None):
        self.project_id = project_id
        self.to_be_member = to_be_member
        self.response = response
        self.response_data = response_data


class Project:
    def __init__(self, projects_csv_path='project.csv'):
        self.projects = self.load_projects_from_csv(projects_csv_path)

    def load_projects_from_csv(self, filename):
        projects = []
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                projects.append(row)
        return projects

    def get_project(self, project_id):
        for project in self.projects:
            if project.get('projectID') == str(project_id):
                return project

        return None


class Admin:
    def __init__(self, person_database_instance, login_database_instance):
        self.person_database_instance = person_database_instance
        self.login_database_instance = login_database_instance

    def manage_database(self):
        print("Admin is managing the database.")
        # Assuming create_table and insert_data methods are available in both instances
        self.person_database_instance.create_table('new_table', ['column1', 'column2'])
        self.person_database_instance.insert_data('new_table', {'column1': 'value1', 'column2': 'value2'})

    def update_tables(self):
        print("Admin is updating tables.")

        # Assuming you have a method to read data from the CSV file
        person_data = self.read_data_from_csv('persons.csv')  # Update the CSV file name

        if person_data is None:
            print("Error reading data from 'persons.csv'.")
            return

        for row in person_data:
            if 'ProjectID' in row:
                project_id = row['ProjectID']
                leader = input("Enter lead for Project {}: ".format(project_id))
                advisor = input("Enter advisor for Project {}: ".format(project_id))

                row['Lead'] = leader
                row['Advisor'] = advisor

        # Assuming you have a method to write data to the database
        self.write_data_to_database('persons', person_data)

    # Add a method to read data from the CSV file
    @staticmethod
    def read_data_from_csv(file_path):
        data = []
        try:
            with open(file_path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    data.append(dict(row))
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
        return data

    @staticmethod
    def delete_data(project_id):
        print(f"Admin is deleting data for Project {project_id}.")
        # Implement the logic to delete data based on project_id in both databases
        # For example: self.person_database_instance.delete_data('persons', {'ProjectID': project_id})
        #              self.login_database_instance.delete_data('login', {'ProjectID': project_id})

    def read_data_from_database(self, table_name):
        return self.person_database_instance.get_table(table_name)  # Update the table name

    def write_data_to_database(self, table_name, data):
        self.person_database_instance.update_table(table_name, data)  # Update the table name


class Student:
    def __init__(self, login_data):
        self.project_manager = Project()
        self.login_data = login_data

    def load_project_data_from_csv(self, filename='project.csv'):
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                self.project_manager.project_table = [dict(row) for row in reader]

            print(f"Project data loaded from '{filename}' successfully.")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"Error loading project data from '{filename}': {e}")

    def view_project_details(self, project_id):
        project_details = self.project_manager.get_project(project_id)
        print("----------")
        print("View Project Details:")
        if project_details:
            print(f"Project ID: {project_details.get('projectID', 'not available')}")
            print(f"Title: {project_details.get('projectName', 'not available')}")
            print(f"Lead: {project_details.get('leadID', 'not available')}")
            # Add other attributes as needed
            print("----------")
        else:
            print(f"Project with ID {project_id} not found.")

    def modify_project_details(self, project_id, new_title, new_status):
        self.project_manager.modify_project_details(project_id, new_title, new_status)
        print("Project details modified successfully.")

    def view_member_requests(self, project_id):
        member_requests = self.project_manager.get_member_requests(project_id)
        print("View Member Requests:")
        for request in member_requests:
            print(f"Request ID: {request['RequestID']}")
            print(f"Student ID: {request['StudentID']}")
            print("----------")

    def perform_activities(self, project_id, student_id):
        while True:
            print("1. View Project Details")
            print("2. Modify Project Details")
            print("3. View Member Requests")
            print("4. Send Member Requests")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.view_project_details(project_id)
            elif choice == '2':
                self.modify_project_details(project_id)
            elif choice == '3':
                self.view_member_requests(project_id)
            elif choice == '4':
                # ... (implement send_member_request logic)
                pass
            elif choice == '5':
                exit_program()
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

    def send_member_request(self, project_id, project_title, lead_id):
        # Implement logic to send member requests based on the provided information
        # This might involve updating the project database or sending notifications
        print(f"Request sent to {lead_id} for project '{project_title}' with ID {project_id}.")


class Lead:
    def __init__(self, login_data):
        self.project_manager = Project()
        self.login_data = login_data

    # def create_project_and_become_lead(self, project_title, student_id):
    #     # Deny all existing member requests
    #     for request in self.project_manager.member_request:
    #         if request.project_id not in self.project_manager.project_table:
    #             self.project_manager.member_request.remove(request)
    #             print(f"Existing member request for Project {request.project_id} denied.")
    #
    #     # Create a new project
    #     self.project_manager.create_project(project_title, student_id)
    #
    #     # Add the student as the lead
    #     project_id = len(self.project_manager.project_table)
    #     project = self.project_manager.get_project(project_id)
    #     project['Lead'] = student_id
    #     print(f"New project created: {project_title}. {student_id} is the lead.")
    #
    #     # Update project data in the CSV file
    #     self.update_project_csv(project_id, project_title, student_id)
    #
    # def update_project_csv(self, project_id, project_title, student_id):
    #     # Assuming you have a method to read data from the CSV file
    #     project_data = self.read_data_from_csv('project.csv')
    #
    #     if project_data is None:
    #         print("Error reading data from 'project.csv'.")
    #         return
    #
    #     # Update the project name and lead ID
    #     for entry in project_data:
    #         if 'ProjectID' in entry and entry['ProjectID'] == str(project_id):
    #             entry['Title'] = project_title
    #             entry['Lead'] = student_id
    #
    #     # Assuming you have a method to write data to the CSV file
    #     self.write_data_to_csv('project.csv', project_data)
    #     print("Updated Project Data:", project_data)

    def get_lead_id(self):
        username = input("Enter your username: ")
        for entry in self.login_data:
            if entry['username'] == username and entry['role'] == 'lead':
                return entry.get('lead_id', None)
        print("Lead ID not found for the given username and role.")
        return None

    def add_members_to_project(self):
        project_id = input("Enter the project ID: ")
        members = input("Enter member IDs (comma-separated): ").split(',')
        self.project_manager.add_members_to_project(project_id, members)

    def see_and_modify_project_details(self):
        project_id = input("Enter the project ID: ")
        lead_id = self.get_lead_id()
        project = self.project_manager.get_project(project_id)

        if project and project['Lead'] == lead_id:
            print("Current Project Details:")
            print(f"Project ID: {project['ProjectID']}")
            print(f"Title: {project['Title']}")
            print(f"Lead: {project['Lead']}")
            print(f"Advisor: {project['Advisor']}")
            print(f"Status: {project['Status']}")
            print("----------")

            # Your logic to modify project details goes here
            new_title = input("Enter the new project title: ")
            new_status = input("Enter the new project status: ")
            self.project_manager.modify_project_details(project_id, new_title, new_status)
        else:
            print("Project not found or you are not the lead of the project.")

    def send_request_messages_to_advisors(self):
        project_id = input("Enter the project ID: ")
        advisor_ids = input("Enter advisor IDs (comma-separated): ").split(',')
        self.project_manager.send_request_messages_to_advisors(project_id, advisor_ids)

    def submit_final_project_report(self):
        project_id = input("Enter the project ID: ")
        lead_id = self.get_lead_id()
        project = self.project_manager.get_project(project_id)
        if project and project['Lead'] == lead_id:
            # Your logic to submit the final project report goes here
            print("Final project report submitted.")
        else:
            print("Project not found or you are not the lead of the project.")


class Member:
    def __init__(self, user_id, project_manager):
        self.user_id = user_id
        self.project_manager = project_manager

    def view_project_details(self, project_id):
        project_details = self.project_manager.get_project(project_id)

        if project_details:
            print("View Project Details:")
            # Check if 'ProjectID' key exists in the dictionary
            if 'ProjectID' in project_details:
                print(f"Project ID: {project_details['ProjectID']}")
            else:
                print("Project ID not available.")

            # Similarly, check for other keys
            if 'Title' in project_details:
                print(f"Title: {project_details['Title']}")
            else:
                print("Title not available.")

            if 'Lead' in project_details:
                print(f"Lead: {project_details['Lead']}")
            else:
                print("Lead not available.")

            if 'Advisor' in project_details:
                print(f"Advisor: {project_details['Advisor']}")
            else:
                print("Advisor not available.")

            if 'Status' in project_details:
                print(f"Status: {project_details['Status']}")
            else:
                print("Status not available.")

            print("----------")
        else:
            print(f"Project with ID {project_id} not found.")

    def modify_project_details(self, project_id, new_title=None, new_status=None):
        project = self.project_manager.get_project(project_id)
        if project and self.user_id in [project.get('Lead'), project.get('Member1'), project.get('Member2')]:
            if new_title:
                project['Title'] = new_title
            if new_status:
                project['Status'] = new_status
            print(f"Project details modified successfully.")
        else:
            print("Either the project does not exist or you do not have the permission to modify it.")


class Faculty:
    def __init__(self, project_manager):
        self.project_manager = project_manager
        self.advisor_requests = []

    def see_advisor_requests(self):
        print("Advisor Requests:")
        for request in self.advisor_requests:
            print(f"Project ID: {request.project_id}, Request From: {request.to_be_advisor}")

    def deny_advisor_request(self, project_id, faculty_id):
        request = self.find_advisor_request(project_id, faculty_id)
        if request:
            self.advisor_requests.remove(request)
            print(f"Denying advisor request for Project {project_id} from Faculty {faculty_id}.")
        else:
            print("Advisor request not found.")

    def see_all_projects(self):
        print("All Projects:")
        for project in self.project_manager.project_table:
            print(f"Project ID: {project['ProjectID']}")
            print(f"Title: {project['Title']}")
            print(f"Lead: {project['Lead']}")
            print(f"Advisor: {project['Advisor']}")
            print(f"Status: {project['Status']}")
            print("----------")

    def evaluate_projects(self):
        print("Evaluating Projects:")
        for project in self.project_manager.project_table:
            # Your evaluation logic goes here
            # You can print, store evaluations, or perform any specific actions based on your requirements
            print(f"Evaluating Project {project['ProjectID']} - {project['Title']}")

    def find_advisor_request(self, project_id, faculty_id):
        for request in self.advisor_requests:
            if request.project_id == project_id and request.to_be_advisor == faculty_id:
                return request
        return None


class Advisor:
    def __init__(self, project_manager):
        self.project_manager = project_manager
        self.advisor_requests = []

    def see_advisor_requests(self):
        print("Advisor Requests:")
        for request in self.advisor_requests:
            print(f"Project ID: {request.project_id}, Request From: {request.to_be_advisor}")

    def accept_advisor_request(self, project_id, faculty_id):
        request = self.find_advisor_request(project_id, faculty_id)
        if request:
            # You can add more logic here if needed
            self.advisor_requests.remove(request)
            print(f"Accepting advisor request for Project {project_id} from Faculty {faculty_id}.")
        else:
            print("Advisor request not found.")

    def deny_advisor_request(self, project_id, faculty_id):
        request = self.find_advisor_request(project_id, faculty_id)
        if request:
            # You can add more logic here if needed
            self.advisor_requests.remove(request)
            print(f"Denying advisor request for Project {project_id} from Faculty {faculty_id}.")
        else:
            print("Advisor request not found.")

    def see_all_projects(self):
        print("All Projects:")
        for project in self.project_manager.project_table:
            print(f"Project ID: {project['ProjectID']}")
            print(f"Title: {project['Title']}")
            print(f"Lead: {project['Lead']}")
            print(f"Advisor: {project['Advisor']}")
            print(f"Status: {project['Status']}")
            print("----------")

    def evaluate_projects(self):
        print("Evaluating Projects:")
        for project in self.project_manager.project_table:
            # Your evaluation logic goes here
            # You can print, store evaluations, or perform any specific actions based on your requirements
            print(f"Evaluating Project {project['ProjectID']} - {project['Title']}")

    def approve_project(self, project_id):
        project = self.project_manager.get_project(project_id)
        if project:
            # Your approval logic goes here
            # You can update the project status or perform any other relevant actions
            print(f"Approving Project {project_id} - {project['Title']}")
        else:
            print("Project not found.")

    def find_advisor_request(self, project_id, faculty_id):
        for request in self.advisor_requests:
            if request.project_id == project_id and request.to_be_advisor == faculty_id:
                return request
        return None

# Instantiate the Database class for both person and login databases
person_database = Database()
login_database = Database()

# Create instances of the Admin, Login, Persons, and other relevant classes
admin_instance = Admin(person_database, login_database)
login_instance = Login()
persons_instance = Persons()
# ... Instantiate other classes

# Initialize tables and data
persons_table, login_table = initializing()

# Instantiate the Project Manager and Faculty instances
project_manager = Project('project.csv')
faculty_instance = Faculty(project_manager)
advisor_instance = Advisor(project_manager)

# Make calls to the initializing and login functions defined above
project_id_to_use = 1
project_id_to_modify = 2
project_id_to_deny = 3
val = login(login_table)

if val:
    user_id, user_role = val

    roles_from_csv = load_roles_from_csv('login.csv')

    if user_role in roles_from_csv:
        if user_role.lower() == 'admin':
            print("Admin activities")
            admin_instance.manage_database()
            admin_instance.update_tables()
        elif user_role.lower() == 'student' and user_id:
            print("Student activities")
            student = Student(login_table)
            student.perform_activities(project_id_to_use, user_id)
            project_id_to_view = 1
            student.view_project_details(project_id_to_view)

        elif user_role.lower() == 'member':
            print("Member activities")
            member_instance = Member(user_id, project_manager)
            member_instance.view_project_details()
            member_instance.modify_project_details(project_id_to_modify, new_title="New Title", new_status="New Status")
        elif user_role.lower() == 'lead':
            print("Lead activities")
            lead = Lead()
        elif user_role.lower() == 'faculty':
            print("Faculty activities")
            faculty_instance.see_advisor_requests()
            faculty_instance.deny_advisor_request(project_id_to_deny, 'advisor_id_here')
            faculty_instance.see_all_projects()
            faculty_instance.evaluate_projects()
        elif user_role.lower() == 'advisor':
            print("Advisor activities")
            advisor_instance.see_advisor_requests()
            advisor_instance.accept_advisor_request(project_id_to_use, 'faculty_id_here')
            advisor_instance.deny_advisor_request(project_id_to_deny, 'faculty_id_here')
            advisor_instance.see_all_projects()
            advisor_instance.evaluate_projects()
            advisor_instance.approve_project(project_id_to_use)
    else:
        print("Invalid role. Please check your user data.")
else:
    print("Login failed. Please check your credentials.")

# Once everything is done, make a call to the exit function
exit_program()
