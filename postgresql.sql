CREATE DATABASE "myDB"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Below code is just for reference. 
-- Python will automatically create a table
-- Table: public.itunes_subscription

-- DROP TABLE public.itunes_subscription;

CREATE TABLE public.itunes_subscription
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    transactions json[],
    trial_start_date timestamp with time zone,
    sub_start_date timestamp with time zone,
    expiration_date timestamp with time zone NOT NULL,
    current_status text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE public.itunes_subscription
    OWNER to postgres;