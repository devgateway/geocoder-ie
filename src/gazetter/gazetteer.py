from dbconnector import open_db_connection

__author__ = 'sebas'

def find(name,country_code):
    conn=open_db_connection()
    curs = conn.cursor()
    params=('%s%s' % (name,'%'),)
    curs.execute("select * from geoname where  name ilike %s limit 10", params)

    return curs;


def find_country(country):
    conn=open_db_connection()
    curs = conn.cursor()
    params=('%s%s' % (country,'%'),)
    curs.execute("select * from countryinfo where name ilike %s limit 1", params)
    country=curs.fetchone();
    return country;



print(find_country('guinea'))

cursor=find('Cordoba')
for row in cursor:
    print(row)

