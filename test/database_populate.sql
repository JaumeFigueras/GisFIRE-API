INSERT INTO user_token (username, token, is_admin, valid_until)
    VALUES ('john.doe', 'qwertyuiop123456789', TRUE, '2099-12-31T23:59:59Z');
INSERT INTO user_token (username, token, is_admin, valid_until)
    VALUES ('john.expired', 'qwertyuiop123456789', TRUE, '2020-12-31T23:59:59Z');
INSERT INTO user_token (username, token, is_admin, valid_until)
    VALUES ('jack.skellington', '0123456789asdfghjkl', FALSE, '2099-12-31T23:59:59Z');
INSERT INTO user_token (username, token, is_admin, valid_until)
    VALUES ('jack.expired', '12345zxcvbnm67890', FALSE, '2020-12-31T23:59:59Z');

INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 00:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 01:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 02:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 03:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 04:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 05:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 06:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 07:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 08:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 09:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 10:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 11:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 12:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 13:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 14:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 15:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 16:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 17:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 18:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 19:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 20:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 21:00:00Z', 200, 0);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 22:00:00Z', 200, 1);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-01 23:00:00Z', 200, 2);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-02 00:00:00Z', 200, 2);
INSERT INTO meteocat_xdde_request (request_date, http_status_code, number_of_lightnings)
    VALUES ('2021-11-02 01:00:00Z', 200, 250);
INSERT INTO meteocat_xdde_request (request_date, http_status_code)
    VALUES ('2021-11-02 02:00:00Z', 404);

INSERT INTO meteocat_lightning (_id, _data, _corrent_pic, _chi2, _ellipse_eix_major, _ellipse_eix_menor, _ellipse_angle,
                                _num_sensors, _nuvol_terra, _id_municipi, _coordenades_latitud, _coordenades_longitud,
                                geom)
    VALUES(123456780, '2021-11-01 22:05:37Z', 12.45, 0.57, 1500, 300, 0.27, 3, TRUE, 8007, 41.71408, 2.33371,
           ST_GeomFromText('POINT(2.33371 41.71408)', 4258));
INSERT INTO meteocat_lightning (_id, _data, _corrent_pic, _chi2, _ellipse_eix_major, _ellipse_eix_menor, _ellipse_angle,
                                _num_sensors, _nuvol_terra, _id_municipi, _coordenades_latitud, _coordenades_longitud,
                                geom)
    VALUES(123456781, '2021-11-01 23:05:37Z', 12.45, 0.57, 1500, 300, 0.27, 3, TRUE, 8007, 41.71408, 2.33371,
           ST_GeomFromText('POINT(2.33371 41.71408)', 4258));
INSERT INTO meteocat_lightning (_id, _data, _corrent_pic, _chi2, _ellipse_eix_major, _ellipse_eix_menor, _ellipse_angle,
                                _num_sensors, _nuvol_terra, _id_municipi, _coordenades_latitud, _coordenades_longitud,
                                geom)
    VALUES(123456782, '2021-11-01 23:10:37Z', 12.45, 0.57, 1500, 300, 0.27, 3, TRUE, 8007, 41.71408, 2.33371,
           ST_GeomFromText('POINT(2.33371 41.71408)', 4258));
INSERT INTO meteocat_lightning (_id, _data, _corrent_pic, _chi2, _ellipse_eix_major, _ellipse_eix_menor, _ellipse_angle,
                                _num_sensors, _nuvol_terra, _id_municipi, _coordenades_latitud, _coordenades_longitud,
                                geom)
    VALUES(123456789, '2021-11-02 00:05:37Z', 12.45, 0.57, 1500, 300, 0.27, 3, TRUE, 8007, 41.71408, 2.33371,
           ST_GeomFromText('POINT(2.33371 41.71408)', 4258));
INSERT INTO meteocat_lightning (_id, _data, _corrent_pic, _chi2, _ellipse_eix_major, _ellipse_eix_menor, _ellipse_angle,
                                _num_sensors, _nuvol_terra, _id_municipi, _coordenades_latitud, _coordenades_longitud,
                                geom)
    VALUES(123456790, '2021-11-02 00:06:37Z', -12.45, 0.57, 1500, 300, 1.27, 3, FALSE, 8009, 41.71308, 2.31371,
           ST_GeomFromText('POINT(2.31371 41.71308)', 4258));
INSERT INTO meteocat_lightning (_id, _data, _corrent_pic, _chi2, _ellipse_eix_major, _ellipse_eix_menor, _ellipse_angle,
                                _num_sensors, _nuvol_terra, _id_municipi, _coordenades_latitud, _coordenades_longitud,
                                geom)
    VALUES(123456791, '2021-11-02 00:06:37Z', -12.45, 0.57, 1500, 300, 1.27, 3, FALSE, 8009, 41.71308, 2.31371,
           ST_GeomFromText('POINT(2.31371 41.71308)', 4258));
INSERT INTO meteocat_lightning (_id, _data, _corrent_pic, _chi2, _ellipse_eix_major, _ellipse_eix_menor, _ellipse_angle,
                                _num_sensors, _nuvol_terra, _id_municipi, _coordenades_latitud, _coordenades_longitud,
                                geom)
    VALUES(123456792, '2021-11-02 01:06:37Z', -12.45, 0.57, 1500, 300, 1.27, 3, FALSE, 8009, 41.71308, 2.31371,
           ST_GeomFromText('POINT(2.31371 41.71308)', 4258));
INSERT INTO meteocat_lightning (_id, _data, _corrent_pic, _chi2, _ellipse_eix_major, _ellipse_eix_menor, _ellipse_angle,
                                _num_sensors, _nuvol_terra, _id_municipi, _coordenades_latitud, _coordenades_longitud,
                                geom)
    VALUES(123456793, '2021-11-02 01:06:37Z', -12.45, 0.57, 1500, 300, 1.27, 3, FALSE, 8009, 41.71308, 2.31371,
           ST_GeomFromText('POINT(2.31371 41.71308)', 4258));


