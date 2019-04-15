ALTER USER 'user' IDENTIFIED WITH mysql_native_password BY 'supersecret';

CREATE DATABASE IF NOT EXISTS pleasedoit;
USE pleasedoit;
CREATE TABLE Feature (
    ID int NOT NULL AUTO_INCREMENT,
    title VARCHAR(255),
    description VARCHAR(255),
    PRIMARY KEY (ID)
);
