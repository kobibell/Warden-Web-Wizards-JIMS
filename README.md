# Warden-Web-Wizards-JIMS

### Steps for Setting Up Python Virtual Environment (venv)


1. First, ensure that the venv module is installed on your machine by running the command python3 -m venv --help in your terminal.
2. To create a new virtual environment, navigate to the directory where you want to create the environment and run the command `python3 -m venv <path/to/new/virtual/environment> `. Replace <path/to/new/virtual/environment> with the path where you want to create the environment.
  - NOTE : This set it not needed as I already created the env within this branch which you should clone
3. To activate the virtual environment, run the command ` source <path/to/new/virtual/environment>/bin/activate `. This command will activate the virtual environment and show its name in your terminal prompt.
4. Once activated, you can now run Python code within the virtual environment. Packages installed while working within this environment will be isolated from your global Python installation, preventing any potential conflicts with different versions of the same package or different project dependencies.
5. You can now install any necessary packages or dependencies using pip. For instance, you can run pip install <package-name> to install a package.
6. To standardize libraries and ensure everyone is using the same package versions, add any required or desired packages to <path/to/new/virtual/environment>/requirements.txt by simply entering the package name.
7. In the terminal, run the command ` pip3 install -r <path/to/new/virtual/environment>/requirements.txt `. This command will install all packages listed in the requirements file you specified.
8. Once you're done working within the virtual environment (done working on the project), you can deactivate it by running the command deactivate in your terminal.
