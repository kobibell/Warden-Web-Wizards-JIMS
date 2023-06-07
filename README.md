# Warden-Web-Wizards-JIMS

## Background

This project was undertaken as part of our Software Engineering course, with the objective of developing a comprehensive solution for the San Diego Sheriff's Office. Our task was to analyze and create an application based on hypothetical problem scenarios provided by a client.

The primary goal of this project was to design and implement a robust Jail Information Management System (JIMS) to address the existing shortcomings in computer support for detention facilities. We carefully examined the requirements in various functional areas, including booking, inventory management, inmate cash account management, user management, and abstraction.

## Installation Guide

### Cloning the Project
1. Open your terminal and navigate to the directory where you wish to clone the project.
2. Run `git clone https://github.com/<username>/<repository>.git` to clone the repository. `Replace <username>/<repository>.git` with the URL of this GitHub repository.

### Setting Up the Project Environment
To maintain package versions and prevent potential conflicts, we suggest creating a Python virtual environment for this project.

1. Navigate to the directory where you wish to create the virtual environment.
2. Use the command `python3 -m venv <path/to/new/virtual/environment>` to establish a new virtual environment. Substitute `<path/to/new/virtual/environment>` with the preferred path for the environment.
3. To activate the virtual environment, run `source <path/to/new/virtual/environment>/bin/activate`.
4. Install the project requirements with `pip3 install requirements.txt` command.


### Running the Server

1. Navigate to the main project folder in the terminal.
2. Use `python3 ./src/jims_project/manage.py runserver` to start the server.

### Logging in
The following credentials can be used initially to login:
- Email : guest@gmail.com
- Password : guest

## Developer Guide

### Database Managment
This application utilizes Django's in-built support for various databases. Originally connected to the 'main_dev' Azure database, the application now uses a local SQLite database to curtail additional costs. The code for the previous database connection remains intact for reference purposes, even though the database is inactive.

To modify the database settings:

1. Go to the settings.py file at `./src/jims_project/jims_project`.
2. Locate the `DATABASES` configuration dictionary where the default connection is defined. The `ENGINE` configuration signifies the Python import path to your database engine, which is how Django communicates with your database. The `NAME` configuration is your database's name.

Remember to run migrations every time you create a new database or alter your models. Refer to the Making Migrations section for more information.

### Making migrations
- Models are the Python classes that define the structure and behavior of your database tables. When you make changes to your models, such as adding, modifying, or deleting fields, Django needs to know how to update the database schema to reflect those changes. To ensure the database reflects the changes to your models, you must create migrations and then apply them.

To generate migrations:

1. Open the terminal and go to the main project directory.
2. Use `python3 ./src/jims_project/manage.py makemigrations` to prepare migration files based on the changes you've made to your models.
3. Apply these changes to the database with `python3 ./src/jims_project/manage.py migrate`.

### Running Tests
The project uses coverage.py as a tool for measuring code coverage of Python programs. It monitors your program, noting which parts of the code have been executed, then analyzes the source to identify code that could have been executed but was not. This is a great tool to ensure that your tests are thorough.

To run tests and generate coverage reports:

1. Navigate to the main project directory in the terminal.
2. Run all test cases in the 'jims_app' with the command `coverage run --source='.' manage.py test jims_app`.
3. Generate a coverage report showing the code coverage for each file and the total coverage with `coverage report`.
4. Create a detailed interactive HTML report using `coverage html` and view it in your web browser by opening the index.html file from the html

Remember that while high coverage is a good goal, 100% coverage does not guarantee that your program is free of bugs. Always aim to write meaningful tests that effectively validate the functionality of your program.



