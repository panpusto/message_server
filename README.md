## Message-server (terminal app in Python)

App is connected to the database(**PostgreSQL**) and uses 
**argparse** library.

### Functionalities:
- users_app:
  - create new users and save user to database
  - edit user's password 
  - delete user from database
  - print list of all users

- messages_app:
  - send message to another user
  - print a list of all messages received by the user

    
### Run the app:
1. Clone this repository and save on your computer.
2. Run the terminal and go to the directory where you save this repository.
3. Create virtual environment `python -m venv .venv`
4. Activate virtualenv `source .venv/bin/activate`
5. Install require packages `pip install -r requirements.txt`
6. Now you can run app and create user account: 
`python users_app.py -u <username> -p <password>`
7. See all available commands: `python users_app.py -h`
8. If you want to send a message type:
`python messages_app.py -u <username> -p <password> -t <receiver username> -s <text message to send>`
9. Enjoy!