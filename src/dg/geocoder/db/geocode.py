import logging

import psycopg2
import psycopg2.extras

from dg.geocoder.db.db import open, close
from dg.geocoder.db.iati_mapper import get_location_class_from_fcl, EXACTNESS_EXACT, LOCATION_REACH_ACTIVITY, \
    GAZETTEER_AGENCY_GEO_NAMES, LOCATION_PRECISION_EXACT

logger = logging.getLogger()

AUTO_CODED_STATUS = 0


def get_iati_code(code, iati_type):
    try:
        conn = open()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        sql = "select * from iati_codes where type=%s and code=%s"
        cur.execute(sql, (iati_type, str(code)))
        data = cur.fetchone()
        if data is None:
            data = {}
        return data
    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)


def save_narrative(text, lang, conn=None):
    should_close = False
    try:
        if conn is None:
            conn = open()
            should_close = True
        cur = conn.cursor()
        sql = "insert into narrative (id,description,lang) values (NEXTVAL('hibernate_sequence'),%s,%s) " \
              " RETURNING id"
        cur.execute(sql, (text, lang))

        if should_close:
            conn.commit()

        return cur.fetchone()[0]
    except Exception as error:
        logger.info(error)
        raise
    finally:
        if should_close:
            close(conn)


def save_location(location_status, lng, lat, activity_id, job_id, exactness_id, features_designation_id,
                  gazetteer_agency_id, location_class_id, location_reach_id, precision_id, conn=None):
    should_close = False
    try:
        if conn is None:
            conn = open()
            should_close = True
        cur = conn.cursor()

        sql = "INSERT INTO location(id,  location_status, point, activity_id,queue_id, exactness_id, " \
              "features_designation_id, gazetteer_agency_id, location_class_id, location_reach_id, " \
              "precision_id) VALUES (NEXTVAL('hibernate_sequence'),%s,ST_MakePoint(%s, %s), %s, %s,%s, %s, %s, %s, %s, %s) RETURNING id"

        cur.execute(sql,
                    (location_status, lng, lat, activity_id, job_id, exactness_id, features_designation_id,
                     gazetteer_agency_id, location_class_id, location_reach_id, precision_id))

        if should_close:
            conn.commit()

        return cur.fetchone()[0]
    except Exception as error:
        logger.info(error)
        raise
    finally:
        if should_close:
            close(conn)


def save_loc_name(location_id, name_id, conn=None):
    should_close = False
    try:
        if conn is None:
            conn = open()
            should_close = True
        cur = conn.cursor()

        sql = "INSERT INTO location_names(location_id, names_id) VALUES (%s, %s)"
        cur.execute(sql, (location_id, name_id))

        if should_close:
            conn.commit()

    except Exception as error:
        logger.info(error)
        raise
    finally:
        if should_close:
            close(conn)


def save_loc_administrative(location_id, name, code, level, conn=None):
    should_close = False
    try:
        if conn is None:
            conn = open()
            should_close = True
        cur = conn.cursor()

        sql = "INSERT INTO administrative(id, code, level,name,location_id, vocabulary_id) " \
              "VALUES (NEXTVAL('hibernate_sequence'), %s,%s,%s,%s, " \
              "(select id from iati_codes where code ='G1' and type='LOCATION_VOCABULARY'))"
        cur.execute(sql, (code, level, name, location_id))

        if should_close:
            conn.commit()

    except Exception as error:
        logger.info(error)
        raise
    finally:
        if should_close:
            close(conn)


def save_loc_identifier(location_id, code, conn=None):
    should_close = False
    try:
        if conn is None:
            conn = open()
            should_close = True
        cur = conn.cursor()

        sql = "INSERT INTO location_identifier(id, code, location_id, vocabulary_id) " \
              "VALUES (NEXTVAL('hibernate_sequence'), %s,%s, (select id from iati_codes where code ='G1' and type='LOCATION_VOCABULARY'))"
        cur.execute(sql, (code, location_id))

        if should_close:
            conn.commit()

    except Exception as error:
        logger.info(error)
        raise
    finally:
        if should_close:
            close(conn)


def save_geocoding(geocoding, job_id, activity_id, conn=None):
    should_close = False

    try:
        if conn is None:
            conn = open()
            should_close = True

        geonameId = geocoding.get('geonameId')
        toponymName = geocoding.get('toponymName')
        name = geocoding.get('name')
        lat = geocoding.get('lat')
        lng = geocoding.get('lng')
        countryCode = geocoding.get('countryCode')
        countryName = geocoding.get('countryName')
        fcl = geocoding.get('fcl')
        fcode = geocoding.get('fcode')
        fclName = geocoding.get('fclName')
        fcodeName = geocoding.get('fcodeName')
        population = geocoding.get('population')
        continentCode = geocoding.get('continentCode')

        adminCode0 = geocoding.get('adminCode0')
        adminName0 = geocoding.get('adminName0')

        adminCode1 = geocoding.get('adminCode1')
        adminName1 = geocoding.get('adminName1')

        adminCode2 = geocoding.get('adminCode2')
        adminName2 = geocoding.get('adminName2')

        adminCode3 = geocoding.get('adminCode3')
        adminName3 = geocoding.get('adminName3')

        adminCode4 = geocoding.get('adminCode4')
        adminName4 = geocoding.get('adminName4')

        # geocoding
        geocoding_sql = """INSERT INTO GEOCODING 
              (id, geoname_id, toponym_name, name, lat, lng, country_code, country_name, fcl, fcode, fclname, 
              fcodename, population, continentcode, admin_code1, admin_name1, admin_code2, admin_name2,
               admin_code3, admin_name3, admin_code4, admin_name4,  queue_id, activity_id) 
              VALUES (NEXTVAL('hibernate_sequence'),%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
              %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s) RETURNING id"""
        cur = conn.cursor()
        geocoding_data = (
            geonameId, toponymName, name, lat, lng, countryCode, countryName, fcl, fcode, fclName, fcodeName,
            population,
            continentCode, adminCode1, adminName1, adminCode2, adminName2, adminCode3, adminName3, adminCode4,
            adminName4,
            job_id, activity_id)
        cur.execute(geocoding_sql, geocoding_data)

        geocoding_id = cur.fetchone()[0]

        name_id = save_narrative(toponymName, 'en', conn=conn)  # sending connection to keep same transaction
        location_class = get_location_class_from_fcl(fcl)
        location_class_id = get_iati_code(location_class.get('code'), location_class.get('type')).get('id')
        exactness_id = get_iati_code(EXACTNESS_EXACT.get('code'), EXACTNESS_EXACT.get('type')).get('id')
        features_designation_id = get_iati_code(fcode, 'FEATURE_DESIGNATION').get('id')
        location_reach_id = get_iati_code(LOCATION_REACH_ACTIVITY.get('code'), LOCATION_REACH_ACTIVITY.get('type')).get(
            'id')
        gazetteer_agency_id = get_iati_code(GAZETTEER_AGENCY_GEO_NAMES.get('code'),
                                            GAZETTEER_AGENCY_GEO_NAMES.get('type')).get('id')
        precision_id = get_iati_code(LOCATION_PRECISION_EXACT.get('code'), LOCATION_PRECISION_EXACT.get('type')).get(
            'id')

        # save location
        location_id = save_location(AUTO_CODED_STATUS,
                                    lng, lat,
                                    activity_id,
                                    job_id,
                                    exactness_id,
                                    features_designation_id,
                                    gazetteer_agency_id,
                                    location_class_id,
                                    location_reach_id,
                                    precision_id, conn=conn)

        save_loc_identifier(location_id, geonameId, conn=conn)

        save_loc_name(location_id, name_id, conn=conn)

        if adminCode0:
            save_loc_administrative(location_id, adminName0, adminCode0, 0, conn=conn)
        if adminCode1:
            save_loc_administrative(location_id, adminName1, adminCode1, 1, conn=conn)
        if adminCode2:
            save_loc_administrative(location_id, adminName2, adminCode2, 2, conn=conn)
        if adminCode3:
            save_loc_administrative(location_id, adminName3, adminCode3, 3, conn=conn)
        if adminCode4:
            save_loc_administrative(location_id, adminName4, adminCode4, 4, conn=conn)

        if should_close:
            conn.commit()

        return (location_id, geocoding_id)
    except Exception as error:
        logger.info(error)
        raise
    finally:
        if should_close:
            close(conn)


def save_extract_text(text, geocoding_id, location_id, queue_id, entities='', conn=None):
    should_close = False
    try:
        if conn is None:
            conn = open()
            should_close = True

        sql = """INSERT INTO extract 
              (id, text, entities, geocoding_id,location_id,queue_id,file_name) 
              VALUES (NEXTVAL('hibernate_sequence'), %s, %s,%s, %s,%s,%s) RETURNING id"""
        cur = conn.cursor()
        data = (text.get('text'), entities, geocoding_id, location_id, queue_id, text.get('file'))
        cur.execute(sql, data)
        result_id = cur.fetchone()[0]
        if should_close:
            conn.commit()

        return result_id
    except Exception as error:
        conn.cancel()
        logger.info(error)
        raise
    finally:
        if should_close:
            close(conn)


def save_activity(identifier, title, description, country, doc_id):
    conn = None
    try:
        conn = open()
        sql = """INSERT INTO ACTIVITY (ID, IDENTIFIER, TITLE, DESCRIPTION, COUNTRY_ISO, DOCUMENT_ID) 
              VALUES (NEXTVAL('hibernate_sequence'), %s, %s, %s, %s, %s) RETURNING id"""
        cur = conn.cursor()
        data = (identifier, title, description, country, doc_id,)
        cur.execute(sql, data)
        result_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return result_id
    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)


def get_geocoding_list(activity_id=None, queue_id=None, document_id=None):
    conn = None
    try:
        conn = open()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        sql_select = """SELECT * FROM GEOCODING WHERE 1=1 """
        data = ()

        if activity_id is not None:
            sql_select = sql_select + """AND ACTIVITY_ID = %s """
            data = data + (activity_id,)

        if document_id is not None:
            sql_select = sql_select + """AND DOCUMENT_ID = %s """
            data = data + (document_id,)

        if queue_id is not None:
            sql_select = sql_select + """AND QUEUE_ID = %s """
            data = data + (queue_id,)

        sql_select = sql_select + " ORDER BY ID"
        cur.execute(sql_select, data)
        results = cur.fetchall()
        cur.close()
        return results
    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)


def get_extracted_list(geocoding_id=None):
    conn = None
    try:
        conn = open()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        sql_select = """SELECT * FROM EXTRACT WHERE 1=1 """
        data = ()

        if geocoding_id is not None:
            sql_select = sql_select + """AND GEOCODING_ID = %s """
            data = data + (geocoding_id,)

        sql_select = sql_select + " ORDER BY ID"
        cur.execute(sql_select, data)
        results = cur.fetchall()
        cur.close()
        return results
    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)


def get_activity_list(document_id=None):
    conn = None
    try:
        conn = open()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        sql_select = """SELECT * FROM ACTIVITY WHERE 1=1 """
        data = ()

        if document_id is not None:
            sql_select = sql_select + """AND DOCUMENT_ID = %s """
            data = data + (document_id,)

        sql_select = sql_select + " ORDER BY ID"
        cur.execute(sql_select, data)
        results = [c for c in cur]
        cur.close()
        return results
    except Exception as error:
        logger.info(error)
        raise
    finally:
        close(conn)
