import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('society_management.db')

# Execute a query
query = "SELECT * FROM your_table"
df = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

# Save the data to a CSV file
df.to_csv('output_file.csv', index=False)

print("Data has been exported to output_file.csv")
