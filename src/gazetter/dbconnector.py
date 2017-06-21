import psycopg2
__author__ = 'sebas'

def open_db_connection():
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect('dbname=gazetteer user=postgres password=admin')
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def close_db_connection(conn=None):
    if conn is not None:
        conn.close()



