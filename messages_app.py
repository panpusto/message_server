import argparse

from psycopg2 import connect
from psycopg2.errors import OperationalError

from crypto import check_password
from models import Message, User

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-l", "--list", help="list of all messages", action="store_true")
parser.add_argument("-t", "--to", help="to")
parser.add_argument("-s", "--send", help="text message to send")

args = parser.parse_args()


def list_of_all_messages(cur, user):
    """This function print a list of all messages received by the user."""
    messages = Message.load_all_messages(cur, user.id)
    if messages:
        for message in messages:
            from_ = User.load_user_by_id(cur, message.from_id)
            print(20 * "-")
            print(f"from: {from_.username}")
            print(f"data: {message.creation_date}")
            print(message.text)
            print(20 * "-")
    else:
        print("You don't have any messages")


def send_message(cur, from_id, receiver_name, text):
    """This function save user's messages to database."""
    if len(text) > 255:
        print("Message is too long")
    to = User.load_user_by_username(cur, receiver_name)
    if to:
        message = Message(from_id, to.id, text=text)
        message.save_to_db(cur)
        print("Message sent successfully")
    else:
        print("Recipient doesn't exist")


if __name__ == '__main__':
    try:
        conn = connect(database='message_server',
                       user='postgres',
                       password='password',
                       host='127.0.0.1')
        conn.autocommit = True
        cursor = conn.cursor()
        if args.username and args.password:
            user = User.load_user_by_username(cursor, args.username)
            if check_password(args.password, user.hashed_password):
                if args.list:
                    list_of_all_messages(cursor, user)
                elif args.to and args.send:
                    send_message(cursor, user.id, args.to, args.send)
                else:
                    parser.print_help()
            else:
                print("Incorrect password or user doesn't exist")
        else:
            print("username and password are required")
            parser.print_help()
        conn.close()
    except OperationalError as e:
        print("Connection error: ", e)
