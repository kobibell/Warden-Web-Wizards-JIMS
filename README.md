# Warden-Web-Wizards-JIMS

## Steps for Setting Up Python Virtual Environment

1. Open the Terminal app or Command Prompt depending on your machine (found in the Applications/Utilities folder).

2. Check that you have Python 3 installed by running python3 --version. If you don't have Python 3 installed, you can download it from the official website: https://www.python.org/downloads/mac-osx/.
  - Note : The module we need is venv which is a built-in module with python3.

3. Create a new virtual environment by running `python3 -m venv </path/to/new/virtual/environment>`. Replace `</path/to/new/virtual/environment>` with the path where you want to create your virtual environment. Take note of this path as you will need it to activate your environment

1. First, ensure that the venv module is installed on your machine by running the command python3 -m venv --help in your terminal.
2. To create a new virtual environment, navigate to the directory where you want to create the environment and run the command `python3 -m venv <path/to/new/virtual/environment> `. Replace `<path/to/new/virtual/environment>` with the path where you want to create the environment.
  - NOTE : This step it may not needed as I have already created the env within this branch assuming it is the one you are cloning.
3. To activate the virtual environment, run the command ` source <path/to/new/virtual/environment>/bin/activate `. This command will activate the virtual environment and show its name in your terminal prompt.
4. Once activated, you can now run Python code within the virtual environment. Packages installed while working within this environment will be isolated from your global Python installation, preventing any potential conflicts with different versions of the same package or different project dependencies.

4. Activate the virtual environment by running `source </path/to/new/virtual/environment>/bin/activate`. You should see the name of your virtual environment in the prompt, indicating that it's active.
 - Note : For windows run `C:<\path\to\new\virtual\environment>\Scripts\activate.bat` instead.

5. You can now install any necessary packages or dependencies using pip. For instance, you can run `pip3 install <package-name>`to install a package.

6. To standardize libraries and ensure everyone is using the same package versions, add any required or desired packages to `<path/to/project>/requirements.txt` by simply entering the package name.

7. In the terminal, and with your venv activated, run the command `pip3 install -r <path/to/project>/requirements.txt`. This command will install all packages listed in the requirements file you specified.

8. You can now work with all the packages needed for the project without affecting your global environment or other projects

8. Once you're done working within the virtual environment (done working on the project), you can deactivate it by running the command deactivate in your terminal.

## Steps for running server (locally for now)
1. Within the terminal navigate to the main project folder

2. Run the following command `python3 ./src/jims_project/manage.py runserver`

## Extra notes 
- The 'jims_app' database in azure is the current database that the app is connected to