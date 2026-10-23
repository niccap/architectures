# countries_sqlite_init.py
import sqlite3, os

query = """
DROP TABLE IF EXISTS countries;
CREATE TABLE countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255),
    capital VARCHAR(255),
    area INTEGER
);
INSERT INTO countries (name, capital, area)
VALUES
    ('Thailand', 'Bangkok', 513120),
    ('Australia', 'Canberra', 7617930),
    ('Egypt', 'Cairo', 1010408);
"""

os.makedirs("data", exist_ok = True)              # creates a new folder
connection = sqlite3.connect("data/countries.db") # creates and connects to the database
connection.cursor().executescript(query)          # executes the query
connection.commit()                               # commits changes
connection.close()                                # closes the connection

