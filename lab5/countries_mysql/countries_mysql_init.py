# countries_mysql_init.py
import pymysql

query = """
DROP DATABASE IF EXISTS countries_db;
CREATE DATABASE countries_db;
USE countries_db;
DROP TABLE IF EXISTS countries;
CREATE TABLE countries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    capital VARCHAR(255),
    area INT
);
INSERT INTO countries (name, capital, area)
VALUES
    ('Thailand', 'Bangkok', 513120),
    ('Australia', 'Canberra', 7617930),
    ('Egypt', 'Cairo', 1010408);
"""

# Create a connection to the MySQL database
connection = pymysql.connect(
    host='localhost',          # MySQL server address
    user='root',               # user name
    password='mypwd',          # password
    
    # multiple statements in one query
    client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS 
)

connection.cursor().execute(query) # executes the query
connection.commit()                # commits changes
connection.close()                 # closes the connection




