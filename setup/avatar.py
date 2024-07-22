import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='society_management'
)
cursor = conn.cursor()

# Add the new column 'avatar' to the 'users' table
alter_table_query = "ALTER TABLE users ADD avatar VARCHAR(255);"

try:
    cursor.execute(alter_table_query)
    conn.commit()
    print("Column added successfully.")
except mysql.connector.Error as e:
    print(f"An error occurred: {e}")

# Close the connection
conn.close()
