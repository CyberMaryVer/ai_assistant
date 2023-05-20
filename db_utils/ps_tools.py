import psycopg2

# connect to the database
conn = psycopg2.connect(host='localhost',
                        # dbname='db_glosses',
                        user='postgres',
                        password='431279',
                        port='5432')
# create a cursor object
# cursor object is used to interact with the database
cur = conn.cursor()

cur.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname = 'glosses'")
# cur.execute("SET AUTOCOMMIT = ON")
exists = cur.fetchone()
if not exists:
    print("Database will be created")
    cur.execute('CREATE DATABASE glosses')

# create table with same headers as csv file
cur.execute("CREATE TABLE IF NOT EXISTS test(**** text, **** float, **** float, **** text)")

# open the csv file using python standard file I/O
# copy file into the table just created
with open('all_checked.csv', 'r') as f:
    next(f)  # Skip the header row.
    # f , <database name>, Comma-Seperated
    cur.copy_from(f, 'all_checked.csv', sep=',')
    # Commit Changes
    conn.commit()
    # Close connection
    conn.close()

f.close()
