import psycopg2


def open():
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect('dbname=geocoder user=postgres password=admin')
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print("Wasn't able to connect")
        raise


def close(conn):
    if conn is not None:
        try:
            conn.close()
        except (Exception, psycopg2.Error) as error:
            print('error when closing connection')


