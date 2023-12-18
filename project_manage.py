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
    logins_data = CsvReader().read_csv('login.csv')

    for login_entry in logins_data:
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
                print("------------------------------------------------------")
                print(f"Login successful! Welcome User ID: {result[0]}, Role: {result[1]}")
                print("------------------------------------------------------")
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
    def __init__(self, project_id, advisor_id, status='Pending', responses=None, response_data=None):
        self.project_id = project_id
        self.advisor_id = advisor_id
        self.responses = responses
        self.status = status
        self.response_data = response_data


class MemberPendingRequest:
    def __init__(self, project_id, to_be_member, responses=None, response_data=None):
        self.project_id = project_id
        self.to_be_member = to_be_member
        self.responses = responses
        self.response_data = response_data

        self.first_name = None
        self.last_name = None
        self.member_id = to_be_member
        self.status = 'Pending'


class Project:
    VALID_STATUSES = {'Pending', 'Approved', 'Completed', 'Cancelled'}

    def __init__(self, projects_csv_path='project.csv'):
        self.projects_csv_path = projects_csv_path
        self.projects = self.load_projects_from_csv()

    def load_projects_from_csv(self):
        projects = []
        try:
            with open(self.projects_csv_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    projects.append(row)
        except FileNotFoundError:
            print(f"File '{self.projects_csv_path}' not found.")
        except Exception as e:
            print(f"Error loading project data from '{self.projects_csv_path}': {e}")
        return projects

    def get_project(self, project_id):
        for project in self.projects:
            if project.get('projectID') == str(project_id):
                return project
        return None

    def modify_project_details(self, project_id, new_title, new_status):
        for project in self.projects:
            if project['projectID'] == str(project_id):
                project['projectName'] = new_title
                project['status'] = new_status
                print(f"Project details modified successfully.")
                self.save_projects_to_csv()  # Save changes to CSV
                return

        print(f"Project with ID {project_id} not found.")

    def save_projects_to_csv(self, filename='project.csv'):
        with open(filename, 'w', newline='') as file:
            fieldnames = ['projectID', 'projectName', 'leadID', 'member1', 'member2', 'advisorName', 'status',
                          'comment']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for project in self.projects:
                writer.writerow({
                    'projectID': project['projectID'],
                    'projectName': project['projectName'],
                    'leadID': project['leadID'],
                    'member1': project['member1'],
                    'member2': project['member2'],
                    'advisorName': project['advisorName'],
                    'status': project['status'],
                    'comment': project.get('comment', ''),  # Retrieve the comment or set an empty string
                })


class Admin:
    def __init__(self):
        self.person_database_instance = Database()
        self.login_database_instance = Database()

    def update_login_data(self):
        person_id = input("Enter person ID: ")
        column_to_update = input("Enter the column to update (username, password, or role): ")
        new_value = input(f"Enter the new value for {column_to_update}: ")

        # Check if 'login' table exists
        if 'login' not in self.login_database_instance.tables:
            # If 'login' table does not exist, create it with the appropriate columns
            columns = ['ID', 'username', 'password', 'role']
            self.login_database_instance.create_table('login', columns)

        # Create a condition to find the row to update
        condition = {'ID': person_id}

        # Create the new data to update the specified column
        data_to_update = {column_to_update: new_value}

        # Update the 'login' table with the modified data
        self.login_database_instance.update_table('login', condition, data_to_update)

        self.save_login_to_csv('login.csv')

        print("Login data updated successfully.")

    def update_persons_data(self):
        person_id = input("Enter person ID: ")

        # Create a condition to find the row to update
        condition = {'ID': person_id}

        # Prompt user for the column to update
        column_to_update = input("Enter the column to update (first, last, or type): ").lower()

        # Prompt user for the new value
        new_value = input(f"Enter the new value for {column_to_update}: ")

        # Create the new data to update the specified column
        data_to_update = {column_to_update: new_value}

        # Update the 'persons' table with the modified data
        self.person_database_instance.update_table('persons', condition, data_to_update)

        self.save_persons_to_csv('persons.csv')

        print("Persons data updated successfully.")

    def manage_database(self):  # Add this method
        print("------------------------------------------------------")
        print("Admin is managing the database.")
        action = input("Do you want to update data? : ").lower()
        if action == 'yes':
            print("Admin is updating the database.")
            file_choice = input("Enter the file to modify (persons.csv or login.csv): ").lower()

            if file_choice == 'persons.csv':
                self.update_persons_data()
            elif file_choice == 'login.csv':
                self.update_login_data()
            else:
                print("Invalid file choice. Exiting.")
        elif action == 'no':
            print("Admin is not updating the database. Exiting.")

    def save_login_to_csv(self, filename='login.csv'):
        with open(filename, 'w', newline='') as file:
            fieldnames = ['ID', 'username', 'password', 'role']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Check if 'login' table exists and has data
            logins_data = self.login_database_instance.tables.get('login', [])
            if logins_data:
                writer.writeheader()
                for row in login_data:
                    writer.writerow({
                        'ID': row['ID'],
                        'username': row['username'],
                        'password': row['password'],
                        'role': row['role'],
                    })

    def save_persons_to_csv(self, filename='persons.csv'):
        with open(filename, 'w', newline='') as file:
            fieldnames = ['ID', 'first', 'last', 'type']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Check if 'persons' table exists and has data
            persons_data = self.person_database_instance.tables.get('persons', [])
            if persons_data:
                writer.writeheader()
                for row in persons_data:
                    writer.writerow({
                        'ID': row.get('ID', ''),
                        'first': row.get('first', ''),
                        'last': row.get('last', ''),
                        'type': row.get('type', ''),
                    })


class Student:
    def __init__(self, logins_data):
        self.project_manager = Project()
        self.logins_data = logins_data

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
            print(f"Lead ID: {project_details.get('leadID', 'not available')}")

            # Print 'advisorName' if present
            advisor_name = project_details.get('advisorName')
            if advisor_name is not None:
                print(f"Advisor: {advisor_name}")

            # Print 'member1' if present
            member1 = project_details.get('member1')
            if member1 is not None:
                print(f"Member1: {member1}")

            # Print 'member2' if present
            member2 = project_details.get('member2')
            if member2 is not None:
                print(f"Member2: {member2}")

            # Print 'status' if present
            status = project_details.get('status')
            if status is not None:
                print(f"Status: {status}")

            print("----------")
        else:
            print(f"Project with ID {project_id} not found.")

    def modify_project_details(self, project_id, new_title, new_status):
        self.project_manager.modify_project_details(project_id, new_title, new_status)

    @staticmethod
    def is_only_student(student_id):
        lead_ids = ['Lionel.M', '9898118']
        member_ids = ['5662557', 'Manuel.N', 'Robert.L', '5687866']
        return student_id not in lead_ids or student_id not in member_ids

    def perform_activities(self, student_id):
        if self.is_only_student(student_id):
            print("You are not allowed to perform activities for the leader or member role")

    @staticmethod
    def save_member_request_to_csv(request):
        try:
            with open('member_pending_request.csv', 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['ID', 'status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerow({
                    'ID': request.member_id,
                    'status': request.status
                })

                print("Request saved to 'member_pending_request.csv' successfully.")
        except Exception as e:
            print(f"Error saving request to 'member_pending_request.csv': {e}")

    @staticmethod
    def read_member_data_from_id(member_id):
        members_data = CsvReader().read_csv('members.csv')
        for members in members_data:
            if members.get('ID') == member_id:
                return {'firstName': members.get('firstName', 'Unknown'),
                        'lastName': members.get('lastName', 'Unknown')}

        return None

    @staticmethod
    def save_advisor_request_to_csv(request):
        try:
            with open('advisor_pending_request.csv', 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['ID', 'status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerow({
                    'ID': request.advisor_id,
                    'status': request.status
                })

                print("Advisor request saved to 'advisor_pending_request.csv' successfully.")
        except Exception as e:
            print(f"Error saving advisor request to 'advisor_pending_request.csv': {e}")


class Lead(Student):
    def __init__(self, logins_data):
        super().__init__(logins_data)

    @staticmethod
    def is_lead(student_id):
        lead_ids = ['Lionel.M', '9898118']
        return student_id in lead_ids

    def get_lead_id(self):
        username = input("Enter your username: ")
        for entry in self.logins_data:
            if entry['username'] == username and entry['role'] == 'lead':
                return entry.get('lead_id', None)
        print("Lead ID not found for the given username and role.")
        return None

    def modify_project_details(self, project_id, new_title, new_status):
        self.project_manager.modify_project_details(project_id, new_title, new_status)

    @staticmethod
    def add_members_to_project(project_id, student_instance):
        members = input("Enter member IDs (comma-separated): ").split(',')
        for member_id in members:
            request = MemberPendingRequest(project_id, member_id, responses=None, response_data=None)
            student_instance.save_member_request_to_csv(request)

    def perform_lead_activities(self, project_id, student_id):
        if self.is_lead(student_id):
            while True:
                print("1. View Project Details")
                print("2. Modify Project Details")
                print("3. Send Advisor Requests")
                print("4. Send Member Requests")
                print("5. Exit")

                choice = input("Enter your choice (1-5): ")

                if choice == '1':
                    self.view_project_details(project_id)
                elif choice == '2':
                    new_title = input("Enter the new project title: ")
                    new_status = input("Enter the new project status: ")
                    self.modify_project_details(project_id, new_title, new_status)
                elif choice == '3':
                    self.send_advisor_requests(project_id, self)
                elif choice == '4':
                    self.add_members_to_project(project_id, self)
                elif choice == '5':
                    exit_program()
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")
        else:
            print("You are not allowed to perform activities for the leader role")

    @staticmethod
    def send_advisor_requests(project_id, student_instance):
        advisor_ids = input("Enter advisor IDs (comma-separated): ").split(',')

        for advisor_id in advisor_ids:
            request = AdvisorPendingRequest(project_id, advisor_id)
            student_instance.save_advisor_request_to_csv(request)

    def submit_final_project_report(self):
        project_id = input("Enter the project ID: ")
        lead_id = self.get_lead_id()
        project = self.project_manager.get_project(project_id)
        if project and project['Lead'] == lead_id:
            print("Final project report submitted.")
        else:
            print("Project not found or you are not the lead of the project.")


class Member(Student):
    def __init__(self, users_id, projects_manager):
        super().__init__(login_data)
        self.users_id = users_id
        self.projects_manager = projects_manager

    def view_project_details(self, project_id):
        project_details = self.project_manager.get_project(project_id)
        print("----------")
        print("View Project Details:")
        if project_details:
            print(f"Project ID: {project_details.get('projectID', 'not available')}")
            print(f"Title: {project_details.get('projectName', 'not available')}")
            print(f"Lead ID: {project_details.get('leadID', 'not available')}")

            # Print 'advisorName' if present
            advisor_name = project_details.get('advisorName')
            if advisor_name is not None:
                print(f"Advisor: {advisor_name}")

            # Print 'member1' if present
            member1 = project_details.get('member1')
            if member1 is not None:
                print(f"Member1: {member1}")

            # Print 'member2' if present
            member2 = project_details.get('member2')
            if member2 is not None:
                print(f"Member2: {member2}")

            # Print 'status' if present
            status = project_details.get('status')
            if status is not None:
                print(f"Status: {status}")

            print("----------")
        else:
            print(f"Project with ID {project_id} not found.")

    def modify_project_details(self, project_id, new_title, new_status):
        self.project_manager.modify_project_details(project_id, new_title, new_status)

    @staticmethod
    def is_project_member(student_id):
        member_ids = ['5662557', 'Manuel.N', 'Robert.L', '5687866']
        return student_id in member_ids

    def perform_member_activities(self, project_id, student_id):
        if self.is_project_member(student_id):
            while True:
                print("1. View Project Details")
                print("2. Modify Project Details")
                print("3. Exit")

                choice = input("Enter your choice (1-3): ")

                if choice == '1':
                    self.view_project_details(project_id)
                elif choice == '2':
                    new_title = input("Enter the new project title: ")
                    new_status = input("Enter the new project status: ")
                    self.modify_project_details(project_id, new_title, new_status)
                elif choice == '3':
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 3.")
        else:
            print("You are not a member of this project")

    @staticmethod
    def print_project_details(project_details):
        print(f"Project ID: {project_details.get('ProjectID', 'not available')}")
        print(f"Title: {project_details.get('Title', 'not available')}")
        print(f"Lead: {project_details.get('Lead', 'not available')}")
        print(f"Advisor: {project_details.get('Advisor', 'not available')}")
        print(f"Status: {project_details.get('Status', 'not available')}")
        print("----------")


class Faculty:
    def __init__(self, projects_manager):
        self.projects_manager = projects_manager
        self.advisor_requests = self.load_advisor_requests_from_csv('advisor_pending_request.csv')

    def load_advisor_requests_from_csv(self, filename):
        requests = []
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                request = AdvisorRequest(
                    project_id=row['ID'],  # Use 'project_id' instead of 'ID'
                    status=row['status']
                )
                requests.append(request)
        return requests

    def see_advisor_requests(self):
        print("Advisor Requests:")
        for request in self.advisor_requests:
            print(f"Project ID: {request.project_id}, Status: {request.status}")

    def deny_advisor_role(self, project_id):
        request = self.find_advisor_request(project_id)
        if request:
            self.advisor_requests.remove(request)
            print(f"Denying advisor request for Project {project_id}")
        else:
            return None

    def save_advisor_requests_to_csv(self, filename='advisor_pending_request.csv'):
        with open(filename, 'w', newline='') as file:
            fieldnames = ['ID', 'status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for request in self.advisor_requests:
                writer.writerow({
                    'ID': request.project_id,
                    'status': request.status
                })

    def send_advisor_response(self, project_id, responses):
        request = self.find_advisor_request(project_id)
        if request:
            if responses.lower() == 'accept':
                request.status = 'accepted'
                print(f"Accepting advisor request for Project {project_id}.")
            elif responses.lower() == 'deny':
                request.status = 'denied'
                print(f"Denying advisor request for Project {project_id}.")
            else:
                print("Invalid response. Please enter 'accept' or 'deny'.")
            self.save_advisor_requests_to_csv('advisor_pending_request.csv')
        else:
            return None

    def see_all_projects(self):
        print("All Projects:")
        for project in self.projects_manager.projects:
            print(f"Project ID: {project['projectID']}")
            print(f"Title: {project['projectName']}")
            print(f"Lead: {project['leadID']}")
            print(f"Advisor: {project['advisorName']}")
            print(f"Status: {project['status']}")
            print("----------")

    def evaluate_projects(self):
        print("Evaluating Projects:")
        for project in self.projects_manager.projects:
            self.print_project_details(project)
            evaluation = input("Enter your evaluation for this project: ")
            project['comment'] = evaluation  # Add the comment to the project
            print(f"Evaluation for Project {project['projectID']} - {project['projectName']} recorded.")
            print("----------")

        self.projects_manager.save_projects_to_csv('project.csv')

    @staticmethod
    def print_project_details(project):
        print(f"Project ID: {project['projectID']}")
        print(f"Title: {project['projectName']}")
        print(f"Lead: {project['leadID']}")
        print(f"Advisor: {project['advisorName']}")
        print(f"Status: {project['status']}")
        print("----------")

    def find_advisor_request(self, project_id):
        for request in self.advisor_requests:
            if request.project_id == project_id:
                return request
        return None


class AdvisorRequest:
    def __init__(self, project_id, status):
        self.project_id = project_id
        self.status = status


class Advisor(Faculty):
    def __init__(self, projects_manager):
        super().__init__(projects_manager)
        self.advisor_requests = self.load_advisor_requests_from_csv('advisor_pending_request.csv')

    def load_advisor_requests_from_csv(self, filename):
        requests = []
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                request = AdvisorRequest(
                    project_id=row['ID'],  # Use 'project_id' instead of 'ID'
                    status=row['status']
                )
                requests.append(request)
        return requests

    def save_advisor_requests_to_csv(self, filename='advisor_pending_request.csv'):
        with open(filename, 'w', newline='') as file:
            fieldnames = ['ID', 'status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for request in self.advisor_requests:
                writer.writerow({
                    'ID': request.project_id,
                    'status': request.status
                })

    def find_advisor_request(self, project_id):
        for request in self.advisor_requests:
            if request.project_id == project_id:
                return request
        return None

    def accept_or_deny_advisor_request(self, project_id, responses):
        request = self.find_advisor_request(project_id)
        if request:
            if responses.lower() == 'accept':
                # Perform actions for accepting the request
                request.status = 'accepted'
                print(f"Accepting advisor request for Project {project_id}.")

                # Update project status in project_manager
                project = self.projects_manager.get_project(project_id)
                if project:
                    project['status'] = 'Approved'
                else:
                    print(f"Project with ID {project_id} not found in the project manager.")
            elif responses.lower() == 'deny':
                # Perform actions for denying the request
                request.status = 'denied'
                print(f"Denying advisor request for Project {project_id}.")
            else:
                print("Invalid response. Please enter 'accept' or 'deny'.")

    def approve_project(self, project_id):
        project = self.projects_manager.get_project(project_id)
        if project:
            # Perform actions for approving the project
            print(f"Approving Project {project_id} - {project['projectName']}")
        else:
            print("Project not found.")

    def see_all_projects(self):
        print("All Projects:")
        for project in self.projects_manager.projects:
            print(f"Project ID: {project['projectID']}")
            print(f"Title: {project['projectName']}")
            print(f"Lead: {project['leadID']}")
            print(f"Advisor: {project['advisorName']}")
            print(f"Status: {project['status']}")
            print("----------")

    def evaluate_projects(self):
        print("Evaluating Projects:")
        for project in self.projects_manager.projects:
            print(f"Evaluating Project {project['projectID']} - {project['projectName']}")
            evaluation = input("Enter your evaluation for this project: ")
            project['comment'] = evaluation  # Add the comment to the project
            print(f"Evaluation for Project {project['projectID']} - {project['projectName']} recorded.")
            print("----------")
        # Save the updated projects to 'project.csv'
        self.projects_manager.save_projects_to_csv('project.csv')


# Instantiate the Database class for both person and login databases
person_database = Database()
login_database = Database()

# Create instances of the Admin, Login, Persons, and other relevant classes
login_instance = Login()
persons_instance = Persons()
login_data = {}
leader_instance = Lead(login_data)


# Initialize tables and data
persons_table, login_table = initializing()

# Instantiate the Project Manager and Faculty instances
project_manager = Project('project.csv')

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
            admin = Admin()
            admin.manage_database()
            admin.save_login_to_csv('login.csv')
            admin.save_persons_to_csv('persons.csv')
        elif user_role.lower() == 'student' and user_id:
            print("Student activities")
            student = Student(login_table)
            student.perform_activities(project_id_to_use)
        elif user_role.lower() == 'leader' and user_id:
            print("Lead activities")
            lead = Lead(login_data)  # Assuming login_data is defined
            lead.perform_lead_activities(project_id_to_use, user_id)
            lead.send_advisor_requests(project_id_to_use, leader_instance)
            lead.submit_final_project_report()
        elif user_role.lower() == 'member' and user_id:
            print("Member activities")
            member = Member(user_id, project_manager)
            project_id_to_use = 1
            member.perform_member_activities(project_id_to_use, user_id)
        elif user_role.lower() == 'faculty' and user_id:
            print("Faculty activities")
            faculty = Faculty(project_manager)
            faculty.see_advisor_requests()
            faculty.deny_advisor_role(project_id_to_deny)
            faculty.see_all_projects()
            faculty.evaluate_projects()
        elif user_role.lower() == 'advisor' and user_id:
            print("Advisor activities")
            advisor = Advisor(project_manager)
            advisor.see_advisor_requests()

            response = input("Do you want to be the advisor for Project? (accept/deny): ")

            if response.lower() in ['accept', 'deny']:
                advisor.accept_or_deny_advisor_request(project_id_to_deny, response.lower())
                advisor.see_all_projects()
                advisor.evaluate_projects()
                advisor.approve_project(project_id_to_use)
            else:
                print("Invalid response. Please enter 'accept' or 'deny'.")
    else:
        print("Invalid role. Please check your user data.")
else:
    print("Login failed. Please check your credentials.")

# Once everything is done, make a call to the exit function
exit_program()
