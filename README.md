# Warden-Web-Wizards-JIMS

### Steps for Setting Up Python Virtual Environment

1. Make sure that `venv` is installed on your machine by running the command `python3 -m venv --help` in your terminal.
2. Clone repository (or pull code) from GitHub that contains a Python ‘venv’ (note : this branch 
3. Navigate to the directory where the repository is cloned and open it in your code editor of choice
5. Activate the virtual environment by running the command `source /path/to/new/virtual/environment/bin/activate`. This will activate the virtual environment, and you should see its name in your terminal prompt.
6. You can now run the Python code within the virtual environment.
    - You will use packages defined by the environment based on the project.
    - This means that any packages or dependencies you install while working within the virtual environment will be isolated from your global Python installation. This is useful if you're working on multiple projects with different dependencies or if you want to avoid conflicts between different versions of the same package.
    - You can now install any necessary packages or dependencies within the virtual environment using `pip`. For example, you can run `pip install <package-name>` to install a package.
8. To standardize libraries and make sure we are all using the same package, add any required or desired packages into  '/path/to/new/virtual/environment/requirements' by just entering the package name
9. Within the terimal run the command 'pip3 install -r ./env/requirements.txt'
  -This will install all of the packages inside the requirements text that were specified
7. When you're finished working within the virtual environment, you can deactivate it by running the command `deactivate` in your terminal.
