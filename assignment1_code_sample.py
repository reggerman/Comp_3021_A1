from email.mime.text import MIMEText
import os
import smtplib
import pymysql
from urllib.request import urlopen

import requests


## Hard Coded Secrets This is bad. INSECURE DESIGN  
## Security Misconfiguration: admin account hard coded aswell as Host name
## This leads to a compromised admin account. 

""" 
db_config = {
    'host': 'mydatabase.com',
    'user': 'admin',
    'password': 'secret123'
} """

db_config = {
    'host': os.getenv('Host'),
    'user': os.getenv('User'),
    'password': os.getenv('Password')
}

"""
Doing the above (env variables) is a method of secrets management, it solves the insecure design of hardcoded 
credentials, another way to do this is from a file and importing the module containing credentials. 
I personally have used env so that is how the example is. 
"""

## Improper Input Validation
## Looks like a possible lack of sanitization and error handling aswell. 
## ^ Security Misconfiguration

""" def get_user_input():
    user_input = input('Enter your name: ')
    return user_input 
"""

def get_user_input():
    user_input = input('Enter your name: ')
    if not all(x.isalpha() or x.isspace() for x in user_input):
        raise ValueError("Invalid Input")
    
    return user_input 

"""
One of the many ways you can check to see if the response is only alphabet or spaces, this eliminates special characters 
which in this case only gets us user name, not the biggest deal but cannot be overlooked since it is an input. 
"""


## Command Injection as we are calling OS.System
## Insufficient Logging, I would include a log for what it is trying to do here. 


"""
def send_email(to, subject, body):
    os.system(f'echo {body} | mail -s "{subject}" {to}')"""

def send_email(to, subject, body):

    logger.info("Email Initiliazing")

    msg = MIMEText(body)

    msg['Subject'] = subject
    msg['From'] = "noreply@company.com"
    msg['you'] = to

    s = smtplib.SMTP('localhost')
    s.sendmail(msg["From"], msg["you"], msg.as_string())

    logger.info("Email Sent with {msg}")

"""
Removes system and with the previous sanitizations we don't need to worry about it that much. I would also 
add logging. 
"""

## Insecure Design, in this case API
## Possible data exposure with the basic http request. 
## Lack of validation or error handling: Security Misconfiguration

""" def get_data():
    url = 'http://insecure-api.com/get-data'
    data = urlopen(url).read().decode()
    return data
 """

def get_data():
    url = 'https://secure-api.com/get-data'
    data = requests.get(url,timeout=5,verify=True)
    return data
"""
uses requests for timeout for both connect and read, and verify for ssl encryption/certification check.
"""

## This is suseptible to an SQL Injection attack if we don't handle validation here or in the get data function.  
## Security Misconfiguration: Lack of validation or error handling
## Insufficient Logging, I would include a log for what it is trying to do here. 
""" 
def save_to_db(data):
    query = f"INSERT INTO mytable (column1, column2) VALUES ('{data}', 'Another Value')"
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
 """
def save_to_db(data):
    query = f"INSERT INTO mytable (column1, column2) VALUES (%s , %s)"

    try: 
        with pymysql.connect(**db_config) as connection: 
            logger.info("Database Connection Established")
            with connection.cursor() as cursor:

                cursor.execute(query,(data, 'second value'))
                connection.commit()
                logger.info("Transaction committed successfully")
    except pymysql.MySQLError as e:
        logger.error("Database Error: {e}")

"""
try except helps with error handling, logging added, a template for the query to counter act injection. the with statements should gracefully close 
connection and cursor once it leaves the block.
"""
## I don't know if you want stuff on this. I would like logging in here. 
## more so to tell us user IP/Credentials/Inputs/API response
if __name__ == '__main__': 
    user_input = get_user_input()
    data = get_data() 
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
