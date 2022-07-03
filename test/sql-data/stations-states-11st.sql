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

--
-- Data for Name: meteocat_weather_station_state; Type: TABLE DATA; Schema: public; Owner: gisfireuser
--

INSERT INTO public.meteocat_weather_station_state VALUES (47, 'ACTIVE', '1996-02-15 20:30:00+01', NULL, 33, '2022-07-01 15:41:54.395512+02');
INSERT INTO public.meteocat_weather_station_state VALUES (65, 'ACTIVE', '1998-05-15 11:30:00+02', NULL, 47, '2022-07-01 15:41:54.417685+02');
INSERT INTO public.meteocat_weather_station_state VALUES (69, 'ACTIVE', '1999-10-11 17:30:00+02', NULL, 50, '2022-07-01 15:41:54.422439+02');
INSERT INTO public.meteocat_weather_station_state VALUES (102, 'ACTIVE', '1994-12-31 23:00:00+01', NULL, 76, '2022-07-01 15:41:54.465398+02');
INSERT INTO public.meteocat_weather_station_state VALUES (126, 'ACTIVE', '1990-01-10 00:00:00+01', '2005-05-04 12:30:00+02', 96, '2022-07-01 15:41:54.497893+02');
INSERT INTO public.meteocat_weather_station_state VALUES (127, 'DISMANTLED', '2005-05-04 12:30:00+02', NULL, 96, '2022-07-01 15:41:54.497893+02');
INSERT INTO public.meteocat_weather_station_state VALUES (154, 'ACTIVE', '1997-09-17 16:00:00+02', '2013-07-31 12:00:00+02', 117, '2022-07-01 15:41:54.538194+02');
INSERT INTO public.meteocat_weather_station_state VALUES (155, 'DISMANTLED', '2013-07-31 12:00:00+02', NULL, 117, '2022-07-01 15:41:54.538194+02');
INSERT INTO public.meteocat_weather_station_state VALUES (191, 'ACTIVE', '2000-06-22 13:00:00+02', NULL, 141, '2022-07-01 15:41:54.584286+02');
INSERT INTO public.meteocat_weather_station_state VALUES (197, 'ACTIVE', '1999-06-21 13:00:00+02', NULL, 146, '2022-07-01 15:41:54.594285+02');
INSERT INTO public.meteocat_weather_station_state VALUES (221, 'ACTIVE', '2005-05-04 15:00:00+02', NULL, 164, '2022-07-01 15:41:54.630295+02');
INSERT INTO public.meteocat_weather_station_state VALUES (260, 'ACTIVE', '2013-07-24 13:00:00+02', '2018-10-17 12:30:00+02', 202, '2022-07-01 15:41:54.702169+02');
INSERT INTO public.meteocat_weather_station_state VALUES (261, 'DISMANTLED', '2018-10-17 12:30:00+02', NULL, 202, '2022-07-01 15:41:54.702169+02');
INSERT INTO public.meteocat_weather_station_state VALUES (292, 'ACTIVE', '2002-03-01 18:00:00+01', NULL, 232, '2022-07-01 15:41:54.760439+02');


--
-- Name: meteocat_weather_station_state_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gisfireuser
--

SELECT pg_catalog.setval('public.meteocat_weather_station_state_id_seq', 297, true);


--
-- PostgreSQL database dump complete
--

