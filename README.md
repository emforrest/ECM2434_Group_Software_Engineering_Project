# ECM2434 - Group Software Project

## About the project

The aim of this project was to build a game focused around sustainability. Our idea was to create an application that encouraged university to travel sustainably and consider the carbon impact of their journeys!

## Running the application

### Pre-requisites

- ![Python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54) Designed for [Python 3.11](https://www.python.org/downloads/).
- ![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=flat-square&logo=mysql&logoColor=white) Uses a MySQL database running v3.0.36, which can be installed [here](https://dev.mysql.com/downloads/mysql/).

### Setting up the virtual environment

To setup a virtual enviroment, you will need to use the [`virtualenv`](https://pypi.org/project/virtualenv/) package. First, make sure that it's installed:
```shell
pip install virtualenv
```
Once it's installed, navigate to the directory containing the source code, and create the virtual environment:
```shell
python -m venv env
```
To install the required packages for the files, activate the virtual environment and install from the provided [`requirements.txt`](requirements.txt) file:
```shell
#For Windows (cmd.exe):
env\Scripts\activate.bat
#For Windows (powershell)
env\Scripts\Activate.ps1
#For MacOS/Linux:
source env/bin/activate

#Once activated, you should see (env) before the command prompt
pip install -r requirements.txt
```

### Starting the webserver

First, make sure you've first activated the virtual environment:
*(If using an IDE, it will typically active the virtual environment for you)*
```shell
#For Windows (cmd.exe):
env\Scripts\activate.bat
#For Windows (powershell)
env\Scripts\Activate.ps1
#For MacOS/Linux:
source env/bin/activate
```
Then, use the following command to start the webserver:
```shell
python manage.py runserver
```