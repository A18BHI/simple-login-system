# Simple Login System - Python + MySQL
# Cybersecurity related: we hash passwords so they are not stored in plain text

import mysql.connector
import bcrypt
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def register():
    username = input("Choose a username: ")
    password = input("Choose a password: ")

    # Hash the password (important for security)
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed)
        )
        conn.commit()
        print("User registered successfully!")
    except:
        print("Username already exists.")

    cursor.close()
    conn.close()


def login():
    username = input("Username: ")
    password = input("Password: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username = %s",
        (username,)
    )
    result = cursor.fetchone()

    if result:
        stored_hash = result[0]
        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            print("Login successful! Welcome", username)
        else:
            print("Wrong password.")
    else:
        print("User not found.")

    cursor.close()
    conn.close()


while True:
    print("\n1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Choose: ")

    if choice == "1":
        register()
    elif choice == "2":
        login()
    elif choice == "3":
        print("Bye!")
        break
    else:
        print("Invalid choice.")