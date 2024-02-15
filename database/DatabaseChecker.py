import mysql.connector

# Connect to MySQL server
cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', port='3306')
cursor = cnx.cursor()

# Execute SQL query to check if database exists
cursor.execute("SHOW DATABASES")
databases = cursor.fetchall()

# Check if the database exists
database_exists = False
for db in databases:
    if db[0] == 'sustainabilitygame':
        database_exists = True
        break

if database_exists:
    print("Database exists.")
else:
    print("Database does not exist.")

# Close cursor and connection
cursor.close()
cnx.close()
