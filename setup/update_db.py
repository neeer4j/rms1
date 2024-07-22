import mysql.connector
from mysql.connector import errorcode

# Database connection configuration
config = {
    'user': 'root',  # Replace with your MySQL username
    'password': '1234',  # Replace with your MySQL password
    'host': '127.0.0.1',
    'raise_on_warnings': True
}

# SQL commands to create the database and tables
sql_commands = [
    "CREATE DATABASE IF NOT EXISTS society_management DEFAULT CHARACTER SET 'utf8'",
    "USE society_management",
    """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        phone VARCHAR(20),
        password VARCHAR(255) NOT NULL,
        member_id VARCHAR(255) UNIQUE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS members (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        phone VARCHAR(20),
        password VARCHAR(255) NOT NULL,
        member_id VARCHAR(255) UNIQUE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS complaints (
        id INT AUTO_INCREMENT PRIMARY KEY,
        member_id INT,
        description TEXT,
        status VARCHAR(255),
        FOREIGN KEY (member_id) REFERENCES members(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS facilities (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        available BOOLEAN
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS bookings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        member_id INT,
        facility_id INT,
        date DATE,
        status VARCHAR(255),
        FOREIGN KEY (member_id) REFERENCES members(id),
        FOREIGN KEY (facility_id) REFERENCES facilities(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS admins (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """
]

def execute_sql_commands(cursor, commands):
    for command in commands:
        if command.strip():
            try:
                cursor.execute(command)
            except mysql.connector.Error as err:
                print(f"Failed executing command: {command}\nError: {err}")

try:
    # Connect to MySQL server
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    # Execute SQL commands
    execute_sql_commands(cursor, sql_commands)
    
    # Commit changes
    cnx.commit()
    print("Database created and SQL commands executed successfully.")
    
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    cursor.close()
    cnx.close()
