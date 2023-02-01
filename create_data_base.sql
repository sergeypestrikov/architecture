pragma foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS student;
CREATE TABLE student (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32));
INSERT INTO person (idperson, lastname, firstname) VALUES (1, 'Sergey', 'Pestrikov')

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;