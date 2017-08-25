from dg.geocoder.db.db import open, close


def save_geocoding(geocoding, doc_id, activity_id):
    conn = None
    try:
        conn = open()
        sql = """INSERT INTO GEOCODING 
              (id, geoname_id, toponym_name, name, lat, lng, country_code, country_name, fcl, fcode, fclname, fcodename, population, continentcode, admin_code_1, admin_name_1, admin_code_2, admin_name_2, admin_code_3, admin_name_3, admin_code_4, admin_name_4, document_id, activity_id) 
              VALUES (NEXTVAL('GLOBAL_ID_SEQ'), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"""
        cur = conn.cursor()
        data = (geocoding.get('geonameId'),
                geocoding.get('toponymName'),
                geocoding.get('name'),
                geocoding.get('lat'),
                geocoding.get('lng'),
                geocoding.get('countryCode'),
                geocoding.get('countryName'),
                geocoding.get('fcl'),
                geocoding.get('fcode'),
                geocoding.get('fclName'),
                geocoding.get('fcodeName'),
                geocoding.get('population'),
                geocoding.get('continentCode'),
                geocoding.get('adminCode1'),
                geocoding.get('adminName1'),
                geocoding.get('adminCode2'),
                geocoding.get('adminName2'),
                geocoding.get('adminCode3'),
                geocoding.get('adminName3'),
                geocoding.get('adminCode4'),
                geocoding.get('adminName4'),
                doc_id,
                activity_id
                )
        cur.execute(sql, data)
        result_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return result_id
    except Exception as error:
        print(error)
        raise
    finally:
        close(conn)


def save_extract_text(text, geocoding_id, entities=''):
    conn = None
    try:
        conn = open()
        sql = """INSERT INTO extract 
              (id, text, entities, geocoding_id) 
              VALUES (NEXTVAL('GLOBAL_ID_SEQ'), %s, %s, %s) RETURNING id"""
        cur = conn.cursor()
        data = (text, entities, geocoding_id)
        cur.execute(sql, data)
        result_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return result_id
    except Exception as error:
        print(error)
        raise
    finally:
        close(conn)


def save_activity(identifier, title, description, country, doc_id):
    conn = None
    try:
        conn = open()
        sql = """INSERT INTO ACTIVITY (ID, IDENTIFIER, TITLE, DESCRIPTION, COUNTRY_ISO, DOC_ID) 
              VALUES (NEXTVAL('GLOBAL_ID_SEQ'), %s, %s, %s, %s, %s) RETURNING id"""
        cur = conn.cursor()
        data = (identifier, title, description, country, doc_id,)
        cur.execute(sql, data)
        result_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return result_id
    except Exception as error:
        print(error)
        raise
    finally:
        close(conn)


def get_geocoding_list(activity_id=None, document_id=None):
    conn = None
    try:
        conn = open()
        cur = conn.cursor()
        sql_select = """SELECT * FROM GEOCODING WHERE 1=1 """
        data = ()

        if activity_id is not None:
            sql_select = sql_select + """AND ACTIVITY_ID = %s """
            data = data + (activity_id,)

        if document_id is not None:
            sql_select = sql_select + """AND DOCUMENT_ID = %s """
            data = data + (document_id,)

        sql_select = sql_select + " ORDER BY ID"
        cur.execute(sql_select, data)
        results = [(c) for c in cur]
        cur.close()
        return results
    except Exception as error:
        print(error)
        raise
    finally:
        close(conn)


def get_extracted_list(geocoding_id=None):
    conn = None
    try:
        conn = open()
        cur = conn.cursor()
        sql_select = """SELECT * FROM EXTRACT WHERE 1=1 """
        data = ()

        if geocoding_id is not None:
            sql_select = sql_select + """AND GEOCODING_ID = %s """
            data = data + (geocoding_id,)

        sql_select = sql_select + " ORDER BY ID"
        cur.execute(sql_select, data)
        results = [(c) for c in cur]
        cur.close()
        return results
    except Exception as error:
        print(error)
        raise
    finally:
        close(conn)


def get_activity_list(document_id=None):
    conn = None
    try:
        conn = open()
        cur = conn.cursor()
        sql_select = """SELECT * FROM ACTIVITY WHERE 1=1 """
        data = ()

        if document_id is not None:
            sql_select = sql_select + """AND DOC_ID = %s """
            data = data + (document_id,)

        sql_select = sql_select + " ORDER BY ID"
        cur.execute(sql_select, data)
        results = [(c) for c in cur]
        cur.close()
        return results
    except Exception as error:
        print(error)
        raise
    finally:
        close(conn)

