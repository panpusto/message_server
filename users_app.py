import argparse

from psycopg2.errors import UniqueViolation, OperationalError
from psycopg2 import connect

from models import User
from crypto import check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")

args = parser.parse_args()


def create_user(cur, username, password):
    """This function create new user and save to database."""
    if len(password) < 8:
        print("Password is too short. It should have at least 8 characters")
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db(cur)
            print("User created successfully")
        except UniqueViolation as e:
            print("User with this username already exists", e)


def edit_user_password(cur, username, password, new_pass):
    """
    This function change user's password if user exist in db
    and enter correct password.
    """
    user = User.load_user_by_username(cur, username)
    if not user:
        print("User doesn't exist")
    elif check_password(password, user.hashed_password):
        if len(new_pass) < 8:
            print("Password is too short. It should have at least 8 characters")
        else:
            user.hashed_password = new_pass
            user.save_to_db(cur)
            print("Password changed successfully")
    else:
        print("Incorrect password")


def delete_user(cur, username, password):
    """This function delete user from database if correct password is entered."""
    user = User.load_user_by_username(cur, username)
    if not user:
        print("User doesn't exist")
    elif check_password(password, user.hashed_password):
        user.delete(cur)
        print("User deleted successfully")
    else:
        print("Incorrect password")


def list_users(cur):
    """This function print list of all users in database."""
    users = User.load_all_users(cur)
    for user in users:
        print(user.username)


if __name__ == '__main__':
    try:
        conn = connect(database="message_server",
                       user="postgres",
                       password="password",
                       host="127.0.0.1")
        conn.autocommit = True
        cursor = conn.cursor()
        # order depends on number of args -> descending
        if args.username and args.password and args.edit and args.new_pass:
            edit_user_password(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        elif args.list:
            list_users(cursor)
        else:
            parser.print_help()
        conn.close()
    except OperationalError as err:
        print("Connection error: ", err)

