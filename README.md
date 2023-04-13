# Warden-Web-Wizards-JIMS

## Steps for Setting Up Python Virtual Environment
- Python environments are isolated spaces where you can install and manage Python packages independently of the system Python installation. In other words, a Python environment allows you to have multiple versions of Python and their associated packages installed on the same machine, without conflicts.


2. Check that you have Python 3 installed by running python3 --version. If you don't have Python 3 installed, you can download it from the official website: https://www.python.org/downloads/mac-osx/.
  - Note : The module we need is venv which is a built-in module with python3.

3. Create a new virtual environment by running `python3 -m venv </path/to/new/virtual/environment>`. Replace `</path/to/new/virtual/environment>` with the path where you want to create your virtual environment. Take note of this path as you will need it to activate your environment

1. First, ensure that the venv module is installed on your machine by running the command python3 -m venv --help in your terminal.
2. To create a new virtual environment, navigate to the directory where you want to create the environment and run the command `python3 -m venv <path/to/new/virtual/environment> `. Replace `<path/to/new/virtual/environment>` with the path where you want to create the environment.
  - NOTE : This step it may not needed as I have already created the env within this branch assuming it is the one you are cloning.
3. To activate the virtual environment, run the command ` source <path/to/new/virtual/environment>/bin/activate `. This command will activate the virtual environment and show its name in your terminal prompt.
4. Once activated, you can now run Python code within the virtual environment. Packages installed while working within this environment will be isolated from your global Python installation, preventing any potential conflicts with different versions of the same package or different project dependencies.
5. You can now install any necessary packages or dependencies using pip. For instance, you can run ` pip install <package-name> `to install a package.
6. To standardize libraries and ensure everyone is using the same package versions, add any required or desired packages to  ` <path/to/new/virtual/environment>/requirements.txt` by simply entering the package name.
7. In the terminal, run the command ` pip3 install -r <path/to/new/virtual/environment>/requirements.txt `. This command will install all packages listed in the requirements file you specified.
8. Once you're done working within the virtual environment (done working on the project), you can deactivate it by running the command deactivate in your terminal.

## Making migrations
- Models are the Python classes that define the structure and behavior of your database tables. When you make changes to your models, such as adding, modifying, or deleting fields, Django needs to know how to update the database schema to reflect those changes. This is where migrations come in.

- When every you make changes to you models make sure you make migraitons and migrate using the following steps

1. Within the terminal navigate to the main project folder

2. Run the following command `python3 ./src/jims_project/manage.py makemigrations`

3. Run the following command `python3 ./src/jims_project/manage.py migrate`

## Steps for running server
1. Within the terminal navigate to the main project folder

2. Run the following command `python3 ./src/jims_project/manage.py runserver`

## Extra notes 
- The 'main_dev' database in azure is the current database that the app is connected to

- To change the database that the application is connec