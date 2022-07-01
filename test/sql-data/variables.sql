--
-- PostgreSQL database dump
--

-- Dumped from database version 12.11 (Ubuntu 12.11-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.11 (Ubuntu 12.11-0ubuntu0.20.04.1)

-- Started on 2022-07-01 18:07:10 CEST

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
-- TOC entry 3924 (class 0 OID 17509)
-- Dependencies: 220
-- Data for Name: meteocat_variable; Type: TABLE DATA; Schema: public; Owner: gisfireuser
--

INSERT INTO public.meteocat_variable VALUES (55, 1, 'Pressió atmosfèrica màxima', 'hPa', 'Px', 'DAT', 1, '2022-07-01 15:54:01.084387+02');
INSERT INTO public.meteocat_variable VALUES (56, 2, 'Pressió atmosfèrica mínima', 'hPa', 'Pn', 'DAT', 1, '2022-07-01 15:54:02.181442+02');
INSERT INTO public.meteocat_variable VALUES (57, 3, 'Humitat relativa màxima', '%', 'HRx', 'DAT', 0, '2022-07-01 15:54:02.189259+02');
INSERT INTO public.meteocat_variable VALUES (58, 30, 'Velocitat del vent a 10 m (esc.)', 'm/s', 'VV10', 'DAT', 1, '2022-07-01 15:54:02.194876+02');
INSERT INTO public.meteocat_variable VALUES (59, 31, 'Direcció de vent 10 m (m. 1) ', '°', 'DV10', 'DAT', 0, '2022-07-01 15:54:02.200185+02');
INSERT INTO public.meteocat_variable VALUES (60, 32, 'Temperatura', '°C', 'T', 'DAT', 1, '2022-07-01 15:54:02.206367+02');
INSERT INTO public.meteocat_variable VALUES (61, 33, 'Humitat relativa', '%', 'HR', 'DAT', 0, '2022-07-01 15:54:02.212132+02');
INSERT INTO public.meteocat_variable VALUES (62, 34, 'Pressió atmosfèrica', 'hPa', 'P', 'DAT', 1, '2022-07-01 15:54:02.217315+02');
INSERT INTO public.meteocat_variable VALUES (63, 35, 'Precipitació', 'mm', 'PPT', 'DAT', 1, '2022-07-01 15:54:02.222787+02');
INSERT INTO public.meteocat_variable VALUES (64, 36, 'Irradiància solar global', 'W/m²', 'RS', 'DAT', 0, '2022-07-01 15:54:02.228226+02');
INSERT INTO public.meteocat_variable VALUES (65, 40, 'Temperatura màxima', '°C', 'Tx', 'DAT', 1, '2022-07-01 15:54:02.23301+02');
INSERT INTO public.meteocat_variable VALUES (66, 42, 'Temperatura mínima', '°C', 'Tn', 'DAT', 1, '2022-07-01 15:54:02.238264+02');
INSERT INTO public.meteocat_variable VALUES (67, 44, 'Humitat relativa mínima', '%', 'HRn', 'DAT', 0, '2022-07-01 15:54:02.243222+02');
INSERT INTO public.meteocat_variable VALUES (68, 50, 'Ratxa màxima del vent a 10 m', 'm/s', 'VVx10', 'DAT', 1, '2022-07-01 15:54:02.248514+02');
INSERT INTO public.meteocat_variable VALUES (69, 51, 'Direcció de la ratxa màxima del vent a 10 m', '°', 'DVVx10', 'DAT', 0, '2022-07-01 15:54:02.253552+02');
INSERT INTO public.meteocat_variable VALUES (70, 72, 'Precipitació màxima en 1 minut', 'mm', 'PPTx1min', 'DAT', 1, '2022-07-01 15:54:02.258825+02');
INSERT INTO public.meteocat_variable VALUES (71, 6006, 'Evapotranspiració de referència', 'mm', 'ETo', 'CMV', 2, '2022-07-01 15:54:02.263524+02');
INSERT INTO public.meteocat_variable VALUES (72, 20, 'Velocitat del vent a 10 m (vec.)', 'm/s', 'VV10vec', 'DAT', 1, '2022-07-01 15:54:03.2091+02');
INSERT INTO public.meteocat_variable VALUES (73, 21, 'Direcció del vent a 10 m (m. u) ', '°', 'DV10u', 'DAT', 0, '2022-07-01 15:54:03.213623+02');
INSERT INTO public.meteocat_variable VALUES (74, 22, 'Desviació est. de la direcció del vent a 10 m', '°', 'DVdest10', 'DAT', 1, '2022-07-01 15:54:03.219644+02');
INSERT INTO public.meteocat_variable VALUES (75, 37, 'Desviació est. de la irradiància solar global', 'W/m²', 'RSdest', 'DAT', 0, '2022-07-01 15:54:03.259689+02');
INSERT INTO public.meteocat_variable VALUES (76, 71, 'Bateria', 'V', 'BAT', 'DAT', 1, '2022-07-01 15:54:03.288756+02');
INSERT INTO public.meteocat_variable VALUES (77, 900, 'Precipitació acumulada en 10 min', 'mm', 'PPT10min', 'AUX', 1, '2022-07-01 15:54:03.297559+02');
INSERT INTO public.meteocat_variable VALUES (78, 901, 'Precipitació acumulada en 1 min', 'mm', 'PPT1min', 'AUX', 1, '2022-07-01 15:54:03.302101+02');
INSERT INTO public.meteocat_variable VALUES (79, 38, 'Gruix de neu a terra', 'cm', 'GNEU', 'DAT', 0, '2022-07-01 15:54:12.578522+02');
INSERT INTO public.meteocat_variable VALUES (80, 39, 'Radiació UV', 'MED/h', 'RUV', 'DAT', 2, '2022-07-01 15:54:12.583508+02');
INSERT INTO public.meteocat_variable VALUES (81, 88, 'Quality number', '%(1)', 'QN', 'DAT', 0, '2022-07-01 15:54:12.623344+02');
INSERT INTO public.meteocat_variable VALUES (82, 64, 'Humectació moll', '%(1)', 'HMOLL', 'DAT', 2, '2022-07-01 15:54:24.359781+02');
INSERT INTO public.meteocat_variable VALUES (83, 65, 'Humectació sec', '%(1)', 'HSEC', 'DAT', 2, '2022-07-01 15:54:24.365905+02');
INSERT INTO public.meteocat_variable VALUES (84, 66, 'Humectació res', 'Ohms', 'HRES', 'DAT', 0, '2022-07-01 15:54:24.372632+02');
INSERT INTO public.meteocat_variable VALUES (85, 4, 'Temperatura màxima de subsòl a 5 cm', '°C', 'TSUBx5', 'DAT', 1, '2022-07-01 15:55:06.021358+02');
INSERT INTO public.meteocat_variable VALUES (86, 5, 'Temperatura mínima de subsòl a 5 cm', '°C', 'TSUBn5', 'DAT', 1, '2022-07-01 15:55:06.027443+02');
INSERT INTO public.meteocat_variable VALUES (87, 8, 'Desviació estàndard de la irradiància neta', 'W/m²', 'RNdest', 'DAT', 0, '2022-07-01 15:55:06.032705+02');
INSERT INTO public.meteocat_variable VALUES (88, 26, 'Velocitat del vent a 2 m (vec.)', 'm/s', 'VV2vec', 'DAT', 1, '2022-07-01 15:55:06.037537+02');
INSERT INTO public.meteocat_variable VALUES (89, 27, 'Direcció del vent a 2 m (m. u)', '°', 'DV2u', 'DAT', 0, '2022-07-01 15:55:06.041974+02');
INSERT INTO public.meteocat_variable VALUES (90, 28, 'Desviació est. de la direcció del vent a 2 m', '°', 'DVdest2', 'DAT', 1, '2022-07-01 15:55:06.046574+02');
INSERT INTO public.meteocat_variable VALUES (91, 46, 'Velocitat del vent a 2 m (esc.) ', 'm/s', 'VV2', 'DAT', 1, '2022-07-01 15:55:06.093159+02');
INSERT INTO public.meteocat_variable VALUES (92, 47, 'Direcció del vent a 2 m (m. 1) ', '°', 'DV2', 'DAT', 0, '2022-07-01 15:55:06.099384+02');
INSERT INTO public.meteocat_variable VALUES (93, 56, 'Ratxa màxima del vent a 2 m', 'm/s', 'VVx2', 'DAT', 1, '2022-07-01 15:55:06.104757+02');
INSERT INTO public.meteocat_variable VALUES (94, 57, 'Direcció de la ratxa màxima del vent a 2 m', '°', 'DVVx2', 'DAT', 0, '2022-07-01 15:55:06.110119+02');
INSERT INTO public.meteocat_variable VALUES (95, 59, 'Irradiància neta', 'W/m²', 'RN', 'DAT', 0, '2022-07-01 15:55:06.115449+02');
INSERT INTO public.meteocat_variable VALUES (96, 60, 'Temperatura de subsòl a 5 cm', '°C', 'TSUB5', 'DAT', 1, '2022-07-01 15:55:06.120244+02');
INSERT INTO public.meteocat_variable VALUES (97, 61, 'Temperatura de subsòl a 50 cm', '°C', 'TSUB50', 'DAT', 1, '2022-07-01 15:55:06.125427+02');
INSERT INTO public.meteocat_variable VALUES (98, 74, 'Humitat del combustible forestal 1', 'mV', 'HCF1', 'DAT', 0, '2022-07-01 15:55:06.14167+02');
INSERT INTO public.meteocat_variable VALUES (99, 75, 'Temperatura del combustible forestal  1', 'mV', 'TCF1', 'DAT', 1, '2022-07-01 15:55:06.147862+02');
INSERT INTO public.meteocat_variable VALUES (100, 76, 'Humitat del combustible forestal 2', 'mV', 'HCF2', 'DAT', 0, '2022-07-01 15:55:06.154003+02');
INSERT INTO public.meteocat_variable VALUES (101, 77, 'Temperatura del combustible forestal 2', 'mV', 'TCF2', 'DAT', 1, '2022-07-01 15:55:06.159117+02');
INSERT INTO public.meteocat_variable VALUES (102, 6, 'TDR màxima a 10 cm', '%(1)', 'TDRx10', 'DAT', 2, '2022-07-01 15:55:08.526618+02');
INSERT INTO public.meteocat_variable VALUES (103, 7, 'TDR mínima a 10 cm', '%(1)', 'TDRn10', 'DAT', 2, '2022-07-01 15:55:08.532044+02');
INSERT INTO public.meteocat_variable VALUES (104, 24, 'Direcció del vent a 6 m (m. u) ', '°', 'DV6u', 'DAT', 0, '2022-07-01 15:55:08.556111+02');
INSERT INTO public.meteocat_variable VALUES (105, 48, 'Velocitat del vent a 6 m (esc.)', 'm/s', 'VV6', 'DAT', 1, '2022-07-01 15:55:08.639586+02');
INSERT INTO public.meteocat_variable VALUES (106, 53, 'Ratxa màxima del vent a 6 m', 'm/s', 'VVx6', 'DAT', 1, '2022-07-01 15:55:08.654144+02');
INSERT INTO public.meteocat_variable VALUES (107, 62, 'TDR a 10 cm', '%(1)', 'TDR10', 'DAT', 2, '2022-07-01 15:55:08.683681+02');
INSERT INTO public.meteocat_variable VALUES (108, 63, 'TDR a 35 cm', '%(1)', 'TDR35', 'DAT', 2, '2022-07-01 15:55:08.689473+02');
INSERT INTO public.meteocat_variable VALUES (109, 23, 'Velocitat del vent a 6 m (vec.)', 'm/s', 'VV6vec', 'DAT', 1, '2022-07-01 15:55:19.715072+02');
INSERT INTO public.meteocat_variable VALUES (110, 25, 'Desviació est. de la direcció de vent a 6 m', '°', 'DVdest6', 'DAT', 1, '2022-07-01 15:55:19.725003+02');
INSERT INTO public.meteocat_variable VALUES (111, 49, 'Direcció del vent a 6 m (m. 1)', '°', 'DV6', 'DAT', 0, '2022-07-01 15:55:19.803255+02');
INSERT INTO public.meteocat_variable VALUES (112, 54, 'Direcció de la ratxa màxima del vent a 6 m', '°', 'DVVx6', 'DAT', 0, '2022-07-01 15:55:19.812792+02');
INSERT INTO public.meteocat_variable VALUES (113, 78, 'Humitat del combustible forestal 3', '%', 'HCF3', 'DAT', 0, '2022-07-01 15:55:19.866446+02');
INSERT INTO public.meteocat_variable VALUES (114, 79, 'Temperatura del combustible forestal 3', '°C', 'TCF3', 'DAT', 1, '2022-07-01 15:55:19.87347+02');
INSERT INTO public.meteocat_variable VALUES (115, 67, 'Humectació moll 2', '%(1)', 'HMOLL2', 'DAT', 2, '2022-07-01 15:55:41.030448+02');
INSERT INTO public.meteocat_variable VALUES (116, 68, 'Humectació sec 2', '%(1)', 'HSEC2', 'DAT', 2, '2022-07-01 15:55:41.036026+02');
INSERT INTO public.meteocat_variable VALUES (117, 69, 'Humectació res 2', 'Ohms', 'HRES2', 'DAT', 1, '2022-07-01 15:55:41.041334+02');
INSERT INTO public.meteocat_variable VALUES (118, 9, 'Irradiància reflectida', 'W/m²', 'Ir', 'DAT', 0, '2022-07-01 15:55:59.018573+02');
INSERT INTO public.meteocat_variable VALUES (119, 10, 'Irradiància fotosintèticament activa (PAR)', 'W/m²', 'PAR', 'DAT', 0, '2022-07-01 15:55:59.023205+02');
INSERT INTO public.meteocat_variable VALUES (120, 70, 'Precipitació acumulada', 'mm', 'PPTacu', 'DAT', 1, '2022-07-01 15:55:59.117458+02');
INSERT INTO public.meteocat_variable VALUES (121, 11, 'Temperatura de supefície', 'ºC', 'TSUP', 'DAT', 1, '2022-07-01 15:57:08.736328+02');
INSERT INTO public.meteocat_variable VALUES (122, 12, 'Temperatura màxima de superfície', 'ºC', 'TSUPx', 'DAT', 1, '2022-07-01 15:57:08.744716+02');
INSERT INTO public.meteocat_variable VALUES (123, 13, 'Temperatura mínima de superfície', 'ºC', 'TSUPn', 'DAT', 1, '2022-07-01 15:57:08.751349+02');
INSERT INTO public.meteocat_variable VALUES (124, 14, 'Temperatura de subsòl a 40 cm', 'ºC', 'TSUB40', 'DAT', 1, '2022-07-01 15:57:08.757712+02');
INSERT INTO public.meteocat_variable VALUES (125, 80, 'Temperatura de la neu 1', '°C', 'TNEU1', 'DAT', 1, '2022-07-01 15:57:23.981481+02');
INSERT INTO public.meteocat_variable VALUES (126, 81, 'Temperatura de la neu 2', '°C', 'TNEU2', 'DAT', 1, '2022-07-01 15:57:23.991718+02');
INSERT INTO public.meteocat_variable VALUES (127, 82, 'Temperatura de la neu 3', '°C', 'TNEU3', 'DAT', 1, '2022-07-01 15:57:24.002536+02');
INSERT INTO public.meteocat_variable VALUES (128, 83, 'Temperatura de la neu 4', '°C', 'TNEU4', 'DAT', 1, '2022-07-01 15:57:24.014333+02');
INSERT INTO public.meteocat_variable VALUES (129, 84, 'Temperatura de la neu 5', '°C', 'TNEU5', 'DAT', 1, '2022-07-01 15:57:24.040993+02');
INSERT INTO public.meteocat_variable VALUES (130, 85, 'Temperatura de la neu 6', '°C', 'TNEU6', 'DAT', 1, '2022-07-01 15:57:24.053949+02');
INSERT INTO public.meteocat_variable VALUES (131, 86, 'Temperatura de la neu 7', '°C', 'TNEU7', 'DAT', 1, '2022-07-01 15:57:24.065091+02');
INSERT INTO public.meteocat_variable VALUES (132, 87, 'Temperatura de la neu 8', '°C', 'TNEU8', 'DAT', 1, '2022-07-01 15:57:24.076192+02');
INSERT INTO public.meteocat_variable VALUES (133, 89, 'Temperatura del datalogger', '°C', 'TDLOG', 'DAT', 1, '2022-07-01 15:57:24.088199+02');


--
-- TOC entry 3932 (class 0 OID 0)
-- Dependencies: 219
-- Name: meteocat_variable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gisfireuser
--

SELECT pg_catalog.setval('public.meteocat_variable_id_seq', 133, true);


-- Completed on 2022-07-01 18:07:10 CEST

--
-- PostgreSQL database dump complete
--

