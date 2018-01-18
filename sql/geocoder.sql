

CREATE SEQUENCE corpora_id_seq
    START WITH 1012266
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- Table: public.corpora

-- DROP TABLE public.corpora;

CREATE TABLE public.corpora
(
  id bigint NOT NULL,
  sentence text,
  category character varying(100),
  file character varying(500),
  CONSTRAINT corpora_pk PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.corpora
  OWNER TO postgres;
