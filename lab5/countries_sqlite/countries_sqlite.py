# countries_sqlite.py

from flask import Flask, request, jsonify
from waitress import serve
import sqlite3 # new

# Helper function to create a database connection
def get_connection():
    try:
        connection = sqlite3.connect("data/countries.db")
        connection.row_factory = sqlite3.Row # returns rows as a Row objects (support access by key)
        return connection
    except sqlite3.Error as e:
        print("Database error:", e)
        return None

app = Flask(__name__)

@app.get("/countries")
def get_countries():
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM countries")
        result = cursor.fetchall()
        connection.close()
        return jsonify([dict(row) for row in result])
    else:
        return {"error": "Database error"}, 500

@app.post("/countries")
def add_country():
    if request.is_json:
        country = request.get_json()
        connection = get_connection()
        if connection and "name" in country and "capital" in country and "area" in country:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO countries (name, capital, area) VALUES (?, ?, ?)",
                           (country["name"], country["capital"], country["area"]))
            connection.commit() # apply last modifications
            country["id"] = cursor.lastrowid # retrieves the last generated id
            connection.close()
            return country, 201
        else:
            return {"error": "Database error"}, 500
    return {"error": "Request must be JSON"}, 415

serve(app, listen='*:8080')



