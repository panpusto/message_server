from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

CREATE_DB = "CREATE DATABASE message_server;"

CREATE_USERS_TABLE = """CREATE TABLE users (
    id serial PRIMARY KEY,
    username varchar(255) UNIQUE,
    hashed_password varchar(80))"""

CREATE_MESSAGES_TABLE = """CREATE TABLE messages (
    id serial PRIMARY KEY,
    from_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    to_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    text varchar(255),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""

DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "127.0.0.1"

# create database
try:
    conn = connect(user=DB_USER,
                   password=DB_PASSWORD,
                   host=DB_HOST)
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(CREATE_DB)
        print("Database created successfully")
    except DuplicateDatabase as e:
        print("Database already exists", e)
    conn.close()
except OperationalError as e:
    print("Connection error: ", e)


# create tables
try:
    conn = connect(database="message_server",
                   user=DB_USER,
                   password=DB_PASSWORD,
                   host=DB_HOST)
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(CREATE_USERS_TABLE)
        print("Users table created successfully")
    except DuplicateTable as e:
        print("Users table already exists", e)

    try:
        cursor.execute(CREATE_MESSAGES_TABLE)
        print("Messages table created successfully")
    except DuplicateTable as e:
        print("Messages table already exists", e)
    conn.close()
except OperationalError as e:
    print("Connection error: ", e)

