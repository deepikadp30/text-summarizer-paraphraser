import mysql.connector

def create_schema():
    # Connect to MySQL (without specifying database first)
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pass123"
    )
    cursor = conn.cursor()

    # Create database if not exists
    cursor.execute("CREATE DATABASE IF NOT EXISTS summarizer")
    cursor.execute("USE summarizer")

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Schema created successfully!")

if __name__ == "__main__":
    create_schema()
