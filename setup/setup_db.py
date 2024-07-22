import mysql.connector
from mysql.connector import errorcode

# Database connection configuration
config = {
    'user': 'root',  # Replace with your MySQL username
    'password': '1234',  # Replace with your MySQL password
    'host': '127.0.0.1',
    'raise_on_warnings': True
}

# The name of the database to be created
database_name = 'society_management'

# SQL commands to create tables
TABLES = {}
TABLES['facilities'] = (
    "CREATE TABLE `facilities` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(255) DEFAULT NULL,"
    "  `available` tinyint(1) DEFAULT NULL,"
    "  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,"
    "  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci")

TABLES['members'] = (
    "CREATE TABLE `members` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(255) DEFAULT NULL,"
    "  `email` varchar(255) DEFAULT NULL,"
    "  `phone` varchar(20) DEFAULT NULL,"
    "  `address` varchar(255) DEFAULT NULL,"
    "  `is_admin` tinyint(1) DEFAULT '0',"
    "  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,"
    "  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci")

TABLES['users'] = (
    "CREATE TABLE `users` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(255) DEFAULT NULL,"
    "  `email` varchar(255) DEFAULT NULL,"
    "  `phone` varchar(20) DEFAULT NULL,"
    "  `password` varchar(255) DEFAULT NULL,"
    "  `member_id` int DEFAULT NULL,"
    "  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,"
    "  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`member_id`) REFERENCES `members` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci")

TABLES['admins'] = (
    "CREATE TABLE `admins` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(255) DEFAULT NULL,"
    "  `email` varchar(255) DEFAULT NULL,"
    "  `phone` varchar(20) DEFAULT NULL,"
    "  `password` varchar(255) DEFAULT NULL,"
    "  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,"
    "  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci")

TABLES['complaints'] = (
    "CREATE TABLE `complaints` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `member_id` int DEFAULT NULL,"
    "  `description` text,"
    "  `status` varchar(50) DEFAULT 'Pending',"
    "  `reason` text DEFAULT NULL,"
    "  `response_reason` varchar(255) DEFAULT NULL,"
    "  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,"
    "  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`member_id`) REFERENCES `members` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci")

TABLES['bookings'] = (
    "CREATE TABLE `bookings` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `member_id` int DEFAULT NULL,"
    "  `facility_id` int DEFAULT NULL,"
    "  `date` date DEFAULT NULL,"
    "  `status` varchar(50) DEFAULT 'Pending',"
    "  `reason` text DEFAULT NULL,"
    "  `response_reason` varchar(255) DEFAULT NULL,"
    "  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,"
    "  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`member_id`) REFERENCES `members` (`id`) ON DELETE CASCADE,"
    "  FOREIGN KEY (`facility_id`) REFERENCES `facilities` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci")

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} DEFAULT CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci'")
        print(f"Database {database_name} created successfully.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

def create_tables(cursor):
    try:
        cursor.execute(f"USE {database_name}")
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print(f"Creating table {table_name}: ", end='')
                cursor.execute(table_description)
                print("OK")
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
    except mysql.connector.Error as err:
        print(err)

try:
    # Connect to MySQL server
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    # Create database and tables
    create_database(cursor)
    create_tables(cursor)
    
    # Commit changes
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
