# ECM2434 - Group Software Project

## About the project

This is the repository for our sustainability-based web application: **CarbonCommuter**!

CarbonCommuter is a free-to-use website that tracks carbon savings from students or staff on their commutes to/from campus. Users are then rewarded by encouraging competition and growing their profile, which in turn drives a sustainable outlook on the everyday activity that is a journey to/from the University.

### Team Members

- Sam Townley - [@SamLolo](https://github.com/SamLolo)
- Eleanor Forrest - [@emforrest](https://github.com/emforrest)
- Abi Hinton - [@abih4](https://github.com/abih4)
- Giulia Brown - [@giuliabrown](https://github.com/giuliabrown)
- Jack Skinner - [@Lonk2004](https://github.com/Lonk2004)
- Charles Symonds - [@Charles-Symonds-10](https://github.com/Charles-Symonds-10)

### Aims

The aim of this project was to build a game focused around sustainability. Our idea was to create an application that encouraged university students to travel sustainably and consider the carbon impact of their journeys! With an estimated 37,000+ students and staff on campus (\*), a small reduction in the number of journeys made by car to campus would lead to a significant reduction in the emissions of harmful CO2. To do this, we intent to positively reward users for each journey they make to/from campus that wasn't in a car (see [gamification](#gamificiation) for more info). On top of this, we'd like to point out the facilities on campus that students can make use of, such as bike racks and bus stops, to achieve this goal.

*(\*) Taken from 2022/23 statistics - reference: https://www.exeter.ac.uk/about/facts/facts/*

### Gamificiation

A big part of the project is focused around the principle of gamificiation. This involves encouraging users to keep re-engaging with the service through the use of "game-like" elements. Taking this onboard, we chose to promote competition amongst the users through the use of a leaderboard. By repeatedly uploading journeys, users could see their progress reflect real-time on the leaderboard, and compare their savings to that of their peers. Another similar element is groups. Groups can be created by anyone, allowing societies and departments to compete amongst the members within the group, through a seperate group leaderboard, as well as competing with other groups through the gloabal group leaderboard. This should promote collaboration, and keep users interested in the service by leveraging their commitment to their favourite society.

We also intend to give users the chance to show off their achievements through the use of public profiles. Here, users can earn badges from achievements, such as milestones in their total carbon savings, or uploading journeys for multiple days in a row. Badges have a rariety associated with them based on how many users own the badge, making them collectible. Users also have levels, determined by the number of times they've made a journey using a sustainable mode of transport. Each type: walking, cycling, by bus or by train; has an individual level, as well as an overall level associated with the user based on the total amount of journeys they've logged within the system. These are desgined to promote routine engagement with the application, encouring repeated daily uploads through badges, and sparking competition between students as to who has the higher level and better overall profile.

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

As part of the project, we are using a MySQL database hosted on Oracle Cloud. This allows us to synchronise our project database across all 6 developers. The application already has the connection details embedded, however for reference, they are as follows:

```text
Host: 129.153.205.30
Port: 3306
User: django
Pass: acf6Z4LeA85FF9gY!
```

If the application can't find a database connection, you can setup a local MySQL server by following the [MySQL installation guide](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/). Once running, create a schema using the following SQL command:

```sql
CREATE SCHEMA 'sustainabilitygame';
```

You will also need to carry out a migration before you can start the webserver using the following commands:

```shell
python manage.py makemigrations
python manage.py migrate
```

### Starting the webserver

First, make sure you've first activated the virtual environment:

```shell
#For Windows (cmd.exe):
env\Scripts\activate.bat
#For Windows (powershell)
env\Scripts\Activate.ps1
#For MacOS/Linux:
source env/bin/activate
```

Then, move inside the sustainabilityGame directory if you're not already, and use the following command to start the webserver:

```shell
cd sustainabilityGame
python manage.py runserver
```

Alternatively, you can use the included scripts to easily start the webserver in one click:

- For windows: [start_server.bat](start_server.bat)
- For MacOS/Linux: [start_server.sh](start_server.sh)