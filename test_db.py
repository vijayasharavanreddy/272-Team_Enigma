import mysql.connector

db_config = {
    "user": "vijay",
    "password": "vijayasharavan@",
    "host": "localhost",
    "database": "hrdata",
}

try:
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected():
        print("Database connection successful!")
    conn.close()
except mysql.connector.Error as e:
    print("Error connecting to database:", e)
