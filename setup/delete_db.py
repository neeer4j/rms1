import mysql.connector
from mysql.connector import errorcode

# Database connection configuration
config = {
    'user': 'root',  # Replace with your MySQL username
    'password': '1234',  # Replace with your MySQL password
    'host': '127.0.0.1',
    'raise_on_warnings': True
}

# The name of the database to be deleted
database_name = 'society_management'

def delete_database(cursor, database_name):
    try:
        cursor.execute(f"DROP DATABASE IF EXISTS {database_name}")
        print(f"Database '{database_name}' deleted successfully.")
    except mysql.connector.Error as err:
        print(f"Failed deleting database: {err}")

try:
    # Connect to MySQL server
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    # Delete the specified database
    delete_database(cursor, database_name)
    
    # Commit changes (not strictly necessary for DROP DATABASE, but good practice)
    cnx.commit()
    
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
