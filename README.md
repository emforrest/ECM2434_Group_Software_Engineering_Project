# ECM2434 - Group Software Project

## About the project

The aim of this project was to build a game focused around sustainability. Our idea was to create an application that encouraged university to travel sustainably and consider the carbon impact of their journeys! The application, named **CarbonCommuter**, changes an ordinary commute to university into one that matters. Every journey is a chance to increase a users score, and that put them one step closer to rewards and new badges.

### Team Members

- Sam Townley - [@SamLolo](https://github.com/SamLolo)
- Eleanor Forrest - [@emforrest](https://github.com/emforrest)
- Abi Hinton - [@abih4](https://github.com/abih4)
- Giulia Brown - [@giuliabrown](https://github.com/giuliabrown)
- Jack Skinner - [@Lonk2004](https://github.com/Lonk2004)
- Charles Symonds - [@Charles-Symonds-10](https://github.com/Charles-Symonds-10)

## Running the application

### Technical Specification

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://pypi.org/project/Django/)
[![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)](https://dev.mysql.com/downloads/mysql/)
[![Oracle](https://img.shields.io/badge/Oracle-F80000?style=for-the-badge&logo=oracle&logoColor=white)](https://www.oracle.com/cloud/)
[![Trello](https://img.shields.io/badge/Trello-%23026AA7.svg?style=for-the-badge&logo=Trello&logoColor=white)](https://trello.com/b/yyfAlINB/the-ceiling-fans)

- Designed for [Python 3.11](https://www.python.org/downloads/) with [Django v5.0.2](https://pypi.org/project/Django/).
- Uses a MySQL database running v3.0.36, which can be installed [here](https://dev.mysql.com/downloads/mysql/).
- Set up with a MySQL server running on an [Oracle Cloud](https://www.oracle.com/cloud/) instance.
- Project planning and tracking done via a [Kanban board](https://trello.com/b/yyfAlINB/the-ceiling-fans) hosted on Trello.

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

### Handling the database connection

As part of the project, we are using a MySQL database hosted on Oracle Cloud. This allows us to synchronise our project database across all 6 developers. The application already has the connection details, however for reference, they are as follows:

```text
Host: 129.146.140.114
Port: 3306
User: django
Pass: acf6Z4LeA85FF9gY!
```

If the application can't find a database connection, you can setup a local MySQL server by following the [MySQL installation guide](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/). Once running, you can use our provided [GroupSoftDevDataBase.sql](database/GroupSoftDevDataBase.sql) file to create the database and necessary tables. You will also need to run `python manage.py migrate` before starting the webserver!

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