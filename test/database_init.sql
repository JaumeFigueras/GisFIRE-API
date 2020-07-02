SET TIMEZONE='utc';
INSERT INTO tokens (username, token, admin, valid_until) VALUES('user', 'user', FALSE, '2200-12-31 00:00:00');
INSERT INTO tokens (username, token, admin, valid_until) VALUES('user_old', 'user', FALSE, '2000-12-31 00:00:00');
INSERT INTO tokens (username, token, admin, valid_until) VALUES('admin', 'admin', TRUE, '2200-12-31 00:00:00');
INSERT INTO tokens (username, token, admin, valid_until) VALUES('admin_old', 'admin', TRUE, '2200-12-31 00:00:00');
