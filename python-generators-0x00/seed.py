import mysql.connector
import csv
import uuid
from mysql.connector import Error

def connect_db():
    """Connect to MySQL server (no DB selected yet)"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='andy ochieng',
            password='18Andy@2004'
        )
        return connection
    except Error as e:
        print(f"Connection Error: {e}")
        return None

def create_database(connection):
    """Create database ALX_prodev if not exists"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created or already exists")
        cursor.close()
    except Error as e:
        print(f"Database Error: {e}")

def connect_to_prodev():
    """Connect directly to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='andy ochieng',
            password='18Andy@2004',
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Connection Error: {e}")
        return None

def create_table(connection):
    """Create user_data table"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            )
        """)
        print("Table user_data created successfully")
        cursor.close()
    except Error as e:
        print(f"Table Error: {e}")

def insert_data(connection, csv_file):
    """Insert unique rows from CSV into user_data table"""
    try:
        cursor = connection.cursor()
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']
                cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, name, email, age))
        connection.commit()
        print("Data inserted successfully")
        cursor.close()
    except Error as e:
        print(f"Insertion Error: {e}")
    except FileNotFoundError:
        print("CSV file not found")

def stream_user_data(connection):
    """Generator that streams user data rows one by one"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
        cursor.close()
    except Error as e:
        print(f"Streaming Error: {e}")

# Entry point for testing
if __name__ == "__main__":
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()
        print("Connection successful")

        connection = connect_to_prodev()
        if connection:
            create_table(connection)
            insert_data(connection, 'user_data.csv')
            print("Streaming first 5 rows:")
            for i, row in enumerate(stream_user_data(connection)):
                print(row)
                if i == 4:
                    break
