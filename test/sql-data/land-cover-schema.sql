--
-- PostgreSQL database dump
--

-- Dumped from database version 12.11 (Ubuntu 12.11-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.11 (Ubuntu 12.11-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: data_catalonia_land_cover; Type: TABLE; Schema: public; Owner: gisfireuser
--

CREATE TABLE public.data_catalonia_land_cover (
    fid integer NOT NULL,
    id bigint,
    nivell_2 integer,
    geom public.geometry(Polygon,25831)
);


ALTER TABLE public.data_catalonia_land_cover OWNER TO gisfireuser;

--
-- Name: data_catalonia_land_cover_fid_seq; Type: SEQUENCE; Schema: public; Owner: gisfireuser
--

CREATE SEQUENCE public.data_catalonia_land_cover_fid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_catalonia_land_cover_fid_seq OWNER TO gisfireuser;

--
-- Name: data_catalonia_land_cover_fid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gisfireuser
--

ALTER SEQUENCE public.data_catalonia_land_cover_fid_seq OWNED BY public.data_catalonia_land_cover.fid;


--
-- Name: data_catalonia_land_cover fid; Type: DEFAULT; Schema: public; Owner: gisfireuser
--

ALTER TABLE ONLY public.data_catalonia_land_cover ALTER COLUMN fid SET DEFAULT nextval('public.data_catalonia_land_cover_fid_seq'::regclass);


--
-- Name: data_catalonia_land_cover data_catalonia_land_cover_pkey; Type: CONSTRAINT; Schema: public; Owner: gisfireuser
--

ALTER TABLE ONLY public.data_catalonia_land_cover
    ADD CONSTRAINT data_catalonia_land_cover_pkey PRIMARY KEY (fid);


--
-- Name: data_catalonia_land_cover_geom_geom_idx; Type: INDEX; Schema: public; Owner: gisfireuser
--

CREATE INDEX data_catalonia_land_cover_geom_geom_idx ON public.data_catalonia_land_cover USING gist (geom);


--
-- PostgreSQL database dump complete
--

