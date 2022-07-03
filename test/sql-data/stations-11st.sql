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
-- Data for Name: meteocat_weather_station; Type: TABLE DATA; Schema: public; Owner: gisfireuser
--

INSERT INTO public.meteocat_weather_station VALUES (33, 'D2', 'Vacarisses', 'AUTO', 41.59252, 1.915, 'Planta potabilitzadora', 343, 82917, 'Vacarisses', 40, 'Vallès Occidental', 8, 'Barcelona', 1, 'XEMA', '2022-07-01 15:41:54.395512+02', '0101000020A2100000A4703D0AD7A3FE3FEB1C03B2D7CB4440');
INSERT INTO public.meteocat_weather_station VALUES (47, 'DG', 'Núria (1.971 m)', 'AUTO', 42.39848, 2.15517, 'Santuari de Núria', 1971.4, 170433, 'Queralbs', 31, 'Ripollès', 17, 'Girona', 1, 'XEMA', '2022-07-01 15:41:54.417685+02', '0101000020A21000000490DAC4C93D0140170E846401334540');
INSERT INTO public.meteocat_weather_station VALUES (50, 'DJ', 'Banyoles', 'AUTO', 42.11653, 2.78969, 'Abocador comarcal de Puigpalter', 176, 170157, 'Banyoles', 28, 'Pla de l''Estany', 17, 'Girona', 1, 'XEMA', '2022-07-01 15:41:54.422439+02', '0101000020A21000006FD39FFD485106405E807D74EA0E4540');
INSERT INTO public.meteocat_weather_station VALUES (76, 'U7', 'Aldover', 'AUTO', 40.85936, 0.50525, 'Granges de Fabra', 52, 430069, 'Aldover', 9, 'Baix Ebre', 43, 'Tarragona', 1, 'XEMA', '2022-07-01 15:41:54.465398+02', '0101000020A21000005EBA490C022BE03FCBBE2B82FF6D4440');
INSERT INTO public.meteocat_weather_station VALUES (96, 'UR', 'Malgrat de Mar - Cooperativa', 'AUTO', 41.64908, 2.75209, 'Cooperativa Garbí, camí del Pla, s/n. Apt. correus 80', 2, 81108, 'Malgrat de Mar', 21, 'Maresme', 8, 'Barcelona', 1, 'XEMA', '2022-07-01 15:41:54.497893+02', '0101000020A21000006A300DC3470406406C3EAE0D15D34440');
INSERT INTO public.meteocat_weather_station VALUES (117, 'VF', 'Alcarràs - Torrent d''Alcarràs', 'AUTO', 41.56482, 0.54999, 'Partida Graminella', 122, 250117, 'Alcarràs', 33, 'Segrià', 25, 'Lleida', 1, 'XEMA', '2022-07-01 15:41:54.538194+02', '0101000020A2100000B610E4A08499E13F381092054CC84440');
INSERT INTO public.meteocat_weather_station VALUES (141, 'W5', 'Oliana', 'AUTO', 42.07683, 1.31489, 'Partida Esclotes', 490, 251497, 'Oliana', 4, 'Alt Urgell', 25, 'Lleida', 1, 'XEMA', '2022-07-01 15:41:54.584286+02', '0101000020A21000002766BD18CA09F53F04ADC090D5094540');
INSERT INTO public.meteocat_weather_station VALUES (146, 'WB', 'Albesa', 'AUTO', 41.76036, 0.67022, 'Partida l''Eral, camí del Torricó', 267, 250083, 'Albesa', 23, 'Noguera', 25, 'Lleida', 1, 'XEMA', '2022-07-01 15:41:54.594285+02', '0101000020A2100000FC00A4367172E53FE197FA7953E14440');
INSERT INTO public.meteocat_weather_station VALUES (164, 'WT', 'Malgrat de Mar', 'AUTO', 41.64707, 2.75658, 'Camí de la Pomereda', 2, 81108, 'Malgrat de Mar', 21, 'Maresme', 8, 'Barcelona', 1, 'XEMA', '2022-07-01 15:41:54.630295+02', '0101000020A21000002176A6D0790D0640821C9430D3D24440');
INSERT INTO public.meteocat_weather_station VALUES (202, 'XW', 'Lleida - la Bordeta', 'AUTO', 41.59822, 0.64855, 'Torre de Vallverdú', 165, 251207, 'Lleida', 33, 'Segrià', 25, 'Lleida', 1, 'XEMA', '2022-07-01 15:41:54.702169+02', '0101000020A2100000FE43FAEDEBC0E43F14E8137992CC4440');
INSERT INTO public.meteocat_weather_station VALUES (232, 'Z7', 'Espot (2.519 m)', 'AUTO', 42.53412, 1.05476, 'Espot', 2519, 250827, 'Espot', 26, 'Pallars Sobirà', 25, 'Lleida', 1, 'XEMA', '2022-07-01 15:41:54.760439+02', '0101000020A2100000381092054CE0F03FDC114E0B5E444540');


--
-- Name: meteocat_weather_station_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gisfireuser
--

SELECT pg_catalog.setval('public.meteocat_weather_station_id_seq', 237, true);


--
-- PostgreSQL database dump complete
--

