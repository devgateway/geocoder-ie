--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.3

-- Started on 2017-09-04 18:16:17

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12387)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2159 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 185 (class 1259 OID 59391)
-- Name: activity; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE activity (
    id bigint NOT NULL,
    title text,
    description text,
    country_iso character varying(250),
    document_id bigint,
    identifier character varying(250)
);


ALTER TABLE activity OWNER TO postgres;

--
-- TOC entry 186 (class 1259 OID 59397)
-- Name: corpora; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE corpora (
    id bigint NOT NULL,
    sentence text,
    category character varying(100),
    file character varying(500)
);


ALTER TABLE corpora OWNER TO postgres;

--
-- TOC entry 187 (class 1259 OID 59405)
-- Name: doc_queue; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE doc_queue (
    id bigint NOT NULL,
    file_name character varying(500),
    type character varying(50),
    state character varying(50),
    create_date timestamp without time zone,
    processed_date timestamp without time zone,
    country_iso character varying(50),
    message character varying(300)
);


ALTER TABLE doc_queue OWNER TO postgres;

--
-- TOC entry 188 (class 1259 OID 59411)
-- Name: extract; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE "extract" (
    id bigint NOT NULL,
    text text,
    entities character varying(250),
    geocoding_id bigint
);


ALTER TABLE "extract" OWNER TO postgres;

--
-- TOC entry 189 (class 1259 OID 59417)
-- Name: geocoding; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE geocoding (
    id bigint NOT NULL,
    geoname_id bigint NOT NULL,
    toponym_name character varying(250),
    name character varying(250),
    lat character varying(250),
    lng character varying(250),
    country_code character varying(250),
    country_name character varying(250),
    fcl character varying(250),
    fcode character varying(250),
    fclname character varying(250),
    fcodename character varying(250),
    population character varying(250),
    continentcode character varying(250),
    admin_code_1 character varying(250),
    admin_name_1 character varying(250),
    admin_code_2 character varying(250),
    admin_name_2 character varying(250),
    admin_code_3 character varying(250),
    admin_name_3 character varying(250),
    admin_code_4 character varying(250),
    admin_name_4 character varying(250),
    document_id bigint,
    activity_id bigint
);


ALTER TABLE geocoding OWNER TO postgres;

--
-- TOC entry 190 (class 1259 OID 59423)
-- Name: global_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE global_id_seq
    START WITH 1012266
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE global_id_seq OWNER TO postgres;

--
-- TOC entry 2023 (class 2606 OID 59490)
-- Name: activity activity_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY activity
    ADD CONSTRAINT activity_pk PRIMARY KEY (id);


--
-- TOC entry 2025 (class 2606 OID 59492)
-- Name: corpora corpora_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY corpora
    ADD CONSTRAINT corpora_pk PRIMARY KEY (id);


--
-- TOC entry 2027 (class 2606 OID 59494)
-- Name: doc_queue doc_queue_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY doc_queue
    ADD CONSTRAINT doc_queue_pk PRIMARY KEY (id);


--
-- TOC entry 2029 (class 2606 OID 59496)
-- Name: extract extract_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "extract"
    ADD CONSTRAINT extract_pk PRIMARY KEY (id);


--
-- TOC entry 2031 (class 2606 OID 59498)
-- Name: geocoding geocoding_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY geocoding
    ADD CONSTRAINT geocoding_pk PRIMARY KEY (id);


--
-- TOC entry 2032 (class 2606 OID 59499)
-- Name: activity fk_doc_queue_activity_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY activity
    ADD CONSTRAINT fk_doc_queue_activity_id FOREIGN KEY (document_id) REFERENCES doc_queue(id);


--
-- TOC entry 2033 (class 2606 OID 59504)
-- Name: extract fk_extract_geocoding; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "extract"
    ADD CONSTRAINT fk_extract_geocoding FOREIGN KEY (geocoding_id) REFERENCES geocoding(id);


--
-- TOC entry 2034 (class 2606 OID 59509)
-- Name: geocoding fk_geocoding_activity; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY geocoding
    ADD CONSTRAINT fk_geocoding_activity FOREIGN KEY (activity_id) REFERENCES activity(id);


--
-- TOC entry 2035 (class 2606 OID 59514)
-- Name: geocoding fk_geocoding_document; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY geocoding
    ADD CONSTRAINT fk_geocoding_document FOREIGN KEY (document_id) REFERENCES doc_queue(id);


-- Completed on 2017-09-04 18:16:17

--
-- PostgreSQL database dump complete
--

