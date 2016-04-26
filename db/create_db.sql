CREATE DATABASE finance
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci;

CREATE USER 'jimbob'@'localhost' IDENTIFIED BY 'finance';
GRANT ALL ON finance.* TO 'jimbob'@'localhost';
