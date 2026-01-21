

USE parking_db;

CREATE TABLE parking_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plate_number VARCHAR(20) NOT NULL,
    parking_slot VARCHAR(5) NOT NULL,
    entry_time DATETIME NOT NULL,
    exit_time DATETIME DEFAULT NULL,
    fee DECIMAL(10,2) DEFAULT NULL
);