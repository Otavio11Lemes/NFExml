import psycopg2

# Replace these with your actual database credentials
dbname = 'mercadomoviments'
user = 'postgres'
password = '70207811'
host = 'localhost'  # or your host address if different

try:
    # Establish a connection to the database
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)

    # Create a cursor object using the cursor() method
    cursor = conn.cursor()

    # Execute a SQL query
    cursor.execute("SELECT version();")

    # Fetch result
    db_version = cursor.fetchone()
    print("PostgreSQL database version:", db_version)

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    # Closing database connection.
    if conn:
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")
