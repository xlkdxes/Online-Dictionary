CREATE DATABASE DictProject;

USE DictProject;

CREATE TABLE users (
	user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50)
);

CREATE TABLE words (
	word_id INT PRIMARY KEY AUTO_INCREMENT,
    word VARCHAR(100) UNIQUE,
    explaination VARCHAR(500)
);

CREATE TABLE queryhistory (
	user_id INT,
    word_id INT,
    query_time DATETIME DEFAULT NOW(),
    
    PRIMARY KEY (user_id, word_id, query_time),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (word_id) REFERENCES words(word_id)
);
