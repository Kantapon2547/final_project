# Final Project for 2023's 219114/115 Programming I

## Project Files
- database.py (update)
- project_manage.py (update)
- persons.csv
- login.csv
- project.csv (update)
- member_pending_request.csv (update)
- advisor_pending_request.csv (update)
- README.md (update)
- TODO.md
- Proposal.md

## Role Actions Table in project_manage.py

| Role    | Action                           | Methods/Classes Involved                | Completion Percentage |
|---------|----------------------------------|-----------------------------------------|-----------------------|
| Admin   | Manage Database                  | `Admin.manage_database()`               | 90%                   |
| Student | Perform Activities               | `Student.perform_activities()`          | 100%                  |
| Lead    | Perform Lead Activities           | `Lead.perform_lead_activities()`        | 90%                   |
| Member  | Perform Member Activities         | `Member.perform_member_activities()`    | 100%                  |
| Faculty | See Advisor Requests              | `Faculty.see_advisor_requests()`        | 100%                  |
| Advisor | See Advisor Requests, Accept/Deny Requests | `Advisor.see_advisor_requests()`, `Advisor.accept_or_deny_advisor_request()` | 100%                  |

## Project Overview
This project involves the implementation of a collaborative project management system. The system encompasses various roles such as Admin, Student, Lead, Member, Faculty, and Advisor, each having specific actions and functionalities. Below is a brief overview of the key files and functionalities:

### database.py (Update)
- Database class: Manages data storage and retrieval, including tables for persons and logins.
- CsvReader class: Reads data from CSV files.
- Table class: Represents a table with insert and update capabilities.

### project_manage.py (Update)
- CsvReader: Reads data from CSV files.
- Persons and Login: Classes for managing person and login data.
- Admin: Admin-specific functionalities, including updating person and login data.
- Student, Lead, Member, Faculty, Advisor: Classes representing different roles with specific actions.
- Project: Manages project-related data, including loading, modifying, and saving to CSV.
- AdvisorRequest: Represents a request from a student to an advisor.

### CSV Files
- persons.csv: Contains information about individuals.
- login.csv: Holds login credentials and roles.
- project.csv: Stores project-related information.
- member_pending_request.csv: Tracks pending member requests.
- advisor_pending_request.csv: Stores pending advisor requests.

## Other Files
- README.md (Update): This file providing an overview of the project and its components.
- TODO.md: Contains tasks and features to be implemented in the future.
- Proposal.md: A document outlining the initial project proposal.

## Role-Specific Functionalities

### Admin
- Manages the database, including updating person and login data.
- Can view and update data in the persons and login tables.

### Student
- Performs activities based on the student's role.
- Views and modifies project details.

### Lead
- Performs lead activities such as viewing and modifying project details.
- Sends advisor requests and manages members in the project.

### Member
- Performs member-specific activities such as viewing and modifying project details.

### Faculty
- Sees advisor requests, denies advisor roles, and evaluates projects.

### Advisor
- Sees advisor requests, accepts or denies advisor requests, and approves projects.

## Instructions for Running the Program
1. Run `database.py` to initialize the database and read data from CSV files.
2. Run `project_manage.py` to execute role-specific functionalities based on user input.
3. Follow on-screen instructions for each role and action.
