import os
import pymysql
from urllib.request import urlopen


## Hard Coded Secrets This is bad. INSECURE DESIGN  
## Security Misconfiguration: admin account hard coded aswell as Host name
## This leads to a compromised admin account. 
db_config = {
    'host': 'mydatabase.com',
    'user': 'admin',
    'password': 'secret123'
}

## Improper Input Validation
## Looks like a possible lack of sanitization and error handling aswell. 
## ^ Security Misconfiguration

def get_user_input():
    user_input = input('Enter your name: ')
    return user_input

## Command Injection as we are calling OS.System
## Insufficient Logging, I would include a log for what it is trying to do here. 
def send_email(to, subject, body):
    os.system(f'echo {body} | mail -s "{subject}" {to}')


## Insecure Design, in this case API
## Possible data exposure with the basic http request. 
## Lack of validation or error handling: Security Misconfiguration
def get_data():
    url = 'http://insecure-api.com/get-data'
    data = urlopen(url).read().decode()
    return data

## This is suseptible to an SQL Injection attack if we don't handle validation here or in the get data function.  
## Security Misconfiguration: Lack of validation or error handling
## Insufficient Logging, I would include a log for what it is trying to do here. 
def save_to_db(data):
    query = f"INSERT INTO mytable (column1, column2) VALUES ('{data}', 'Another Value')"
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

## I don't know if you want stuff on this. I would like logging in here. 
## more so to tell us user IP/Credentials/Inputs/API response
if __name__ == '__main__': 
    user_input = get_user_input()
    data = get_data() 
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
