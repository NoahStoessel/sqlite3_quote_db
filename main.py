import sqlite3
import getpass
import hashlib
def encode(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
def username_taken(username, cur):
    all_users = get_all_users(cur)
    if all_users == []:
        return False
    for user in all_users:
        if user[0] == username:
            return True
    return False
def login(username, password, users):
    actual_user = ()
    if users is None:
        assert False, "USERS IS NONE!!"
    user_exists = False
    for user in users:
        if (username, password) == (user[0], user[1]):
            user_exists = True
            actual_user = user
    return user_exists, actual_user
def get_all_users(cur):
    users = []
    all_users = cur.execute('''SELECT * FROM users ORDER BY username''')
    for user in all_users:
        users.append(user)
    return users
def get_user_data(cur):
    username  = str(input("Enter your desired username: "))
    while username_taken(username, cur):
        print("Username taken")
        username = str(input("Enter your desired username: "))
    password = str(getpass.getpass("Enter your desired password: "))
    quote = str(input("Enter your desired quote: "))
    
    return (username, encode(password), quote)
def insert_user(conn, cur, user):
    cur.execute('''INSERT INTO users (username, password, quote) VALUES (?, ?, ?)''', user)
    conn.commit()
conn = sqlite3.connect("./test.db")

cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users
            (username TEXT, password BLOB, quote TEXT)''')
conn.commit()
while True:
    print("1) Register")
    print("2) Login")
    print("3) Quit")
    user_option = str(input("Choose an option: "))
    if user_option == "1":
        insert_user(conn, cur, get_user_data(cur))
    elif user_option == "2":
        user_temp = input("Input your username: ")
        pass_temp = getpass.getpass("Input your password: ")
        exists, actual_user = login(user_temp, encode(pass_temp), get_all_users(cur))
        if exists:
            print(f'Your quote is: {actual_user[2]}')
        else:
            print("Username or Password is incorrect!")
    elif user_option == "3":
        break


cur.close()
conn.close()
