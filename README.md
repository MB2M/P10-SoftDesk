# P10-SoftDesk
    
*This repository hosts a project to achieve during my training OpenClassRooms.com*

This script was created on Python 3.9 and use the Django framework in its 3.1.5 version.
It also use django rest framework v3.12.2

The purpose of this repository is to deliver an api for an issue tracking system.

You can use external request or website UI to explore data.

## Installation

Download the files in the directories of your choice

### 1) Create a Virtual Environment :
 
Go to the directory where you downloaded files and run this command on your terminal:

    python3 -m venv env
    
Then, initialize it :
 
- On Windows, run:

        env\Scripts\activate.bat
    
- On Unix or MacOS, run:

        source env/bin/activate
        
For more information, refer to the python.org documentation :

<https://docs.python.org/3/tutorial/venv.html>
    
### 2) Install the requirements

Still on you terminal, with the environment activated, run the following command to install the required libraries
    
    pip install -r requirements

### 3) Start the server

Go to the litreview/ repository and start the server using command:

    python manage.py runserver

Server is now running on

    http://127.0.0.1:8000/
    
### 4) Create an account:

In order to use the API, you have to create an account using a POST request or django rest framework UI:

<http://127.0.0.1:8000/api/signup/>

Those fields are required:
+first_name
+last-name
+email
+password

### 5) Connect to the API

From UI, go to <http://127.0.0.1:8000/api/api-auth/login/>

Sending a POST request to <http://127.0.0.1:8000/api/token/> with fields 'email' and 'password'
--> You will receive a token you have to send in every request <--


### 6) Refer to the API docs

Api documentation is available here:

<https://documenter.getpostman.com/view/6875164/TzCS6RsC>


