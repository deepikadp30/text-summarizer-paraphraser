import mysql.connector
import bcrypt

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",           # your MySQL username
        password="pass123",  # your MySQL password
        database="summarizer"     # your database name
    )

def create_user(name, email, username, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO users (name, email, username, password_hash) VALUES (%s, %s, %s, %s)",
            (name, email, username, hashed_pw.decode('utf-8'))
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        conn.close()

def validate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        return user
    return None
