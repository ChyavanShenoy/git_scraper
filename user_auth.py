import sqlite3
from passlib.hash import pbkdf2_sha256
from datetime import datetime

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_user_data_table = "CREATE TABLE IF NOT EXISTS users (username text, password text)"
create_user_login_logs_table = "CREATE TABLE IF NOT EXISTS user_login_logs (username text, login_time text, success text, action text)"
create_user_repo_table = "CREATE TABLE IF NOT EXISTS user_repos (username text, repo_name text, repo_url text, repo_description text)"
for table in [create_user_data_table, create_user_login_logs_table, create_user_repo_table]:
    connection.execute(table)
connection.commit()


def encrypt_password(password):
    # encrypt password
    # return encrypted password
    hash = pbkdf2_sha256.hash(password)
    return hash


def check_user_exist(username):
    cursor.execute('SELECT * FROM users WHERE username=:un', {'un': username})
    if cursor.fetchone() is not None:
        return True
    else:
        return False


def verify_password(username, password):
    cursor.execute('SELECT * FROM users WHERE username=:un', {'un': username})
    user = cursor.fetchone()
    encrypt_password = user[1]
    if pbkdf2_sha256.verify(password, encrypt_password):
        return True
    else:
        return False


def register(username, password):
    # encrypt password
    # insert username and encrypted password into table users
    # enter login log
    # return True
    encrypted_password_hash = encrypt_password(password)
    cursor.execute('INSERT INTO users VALUES (:un, :pw)', {
                   'un': username, 'pw': encrypted_password_hash})
    connection.commit()
    now = datetime.now()
    time = now.strftime("%d/%b/%Y %H:%M:%S")
    cursor.execute('INSERT INTO user_login_logs VALUES (:un, :lt, :s, :a)',
                   {'un': username, 'lt': time, 's': 'Success', 'a': 'Register'})
    connection.commit()
    return True


def login(username, password):
    # verify password
    # if correct, enter login log and return True
    # if incorrect, return False
    success = verify_password(username, password)
    if success:
        now = datetime.now()
        time = now.strftime("%d/%b/%Y %H:%M:%S")
        cursor.execute('INSERT INTO user_login_logs VALUES (:un, :lt, :s, :a)',
                       {'un': username, 'lt': time, 's': 'Success', 'a': 'Login'})
        connection.commit()
        return True
    else:
        now = datetime.now()
        time = now.strftime("%d/%b/%Y %H:%M:%S")
        cursor.execute('INSERT INTO user_login_logs VALUES (:un, :lt, :s, :a)',
                       {'un': username, 'lt': time, 's': 'failure', 'a': 'Login'})
        connection.commit()
        return False




def close():
    connection.close()
