import psycopg2

__author__ = 'sebas'

def connect():
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect('dbname=gazetteer user=postgres password=admin')
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def close(conn=None):
    if conn is not None:
        conn.close()

def find_country(country):
    conn=connect()
    curs = conn.cursor()
    params=('%s%s' % (country,'%'),)
    curs.execute("select iso_alpha2,name from countryinfo where lower(name) like lower(%s) limit 1", params)
    country=curs.fetchone();
    return country;



