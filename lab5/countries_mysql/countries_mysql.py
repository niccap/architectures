#countries_mysql.py
# LAB 5 - EXERCISE 1
# Modify the countries the Web Service to use the containerized DB
# Extend the API with the following endpoints:
#
# HTTP method  API endpoint     Description
# GET          /countries/<id>  Get the info of a single country
# PUT          /countries/<id>  Modify country data
# DELETE       /countries/<id>  Delete a country

from flask import Flask, request, jsonify
from waitress import serve
import pymysql

# Helper function to create a database connection
def get_connection():
    try:
        return pymysql.connect(
            host='mysql',              # MySQL service name defined in compose.yaml
            user='root',               # user name
            password='mypwd',          # password
            database='countries_db',   # database name
            cursorclass=pymysql.cursors.DictCursor, # returns rows as a dictionary
        )
    except pymysql.Error as err:
        print(f"Database error: {err}")
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
        return jsonify(result)
    else:
        return {"error": "Database error"}, 500

@app.get("/countries/<int:id>")
def get_county(id):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM countries WHERE id = %s", id)
        result = cursor.fetchall()
        connection.close()
        if result: 
            return jsonify(result)
        else:
            return {"error": "The requested id was not found"}, 404
    else:
        return {"error": "Database error"}, 500

@app.post("/countries")
def add_country():
    if request.is_json:
        country = request.get_json()
        connection = get_connection()
        if connection and "name" in country and "capital" in country and "area" in country:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO countries (name, capital, area) VALUES (%s, %s, %s)",
                           (country["name"], country["capital"], country["area"]))
            connection.commit() # apply last modifications
            country["id"] = cursor.lastrowid # retrieves the last generated id
            connection.close()
            return country, 201
        else:
            return {"error": "Database error"}, 500
    return {"error": "Request must be JSON"}, 415

@app.put("/countries/<int:id>")
def modify_country(id):
    if not request.is_json:
        return {"error": "Request must be JSON"}, 415
    country = request.get_json()
    if set(country.keys()) != {'name', 'capital', 'area'}:
        return {"error": "Request has invalid or missing data"}, 422
    country["id"] = id
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM countries WHERE id = %s", id)
        result = cursor.fetchall()
        if result: 
            cursor.execute("UPDATE countries SET name = %s, capital = %s, area = %s WHERE id = %s", 
                           (country["name"], country["capital"], country["area"], id))
            connection.commit()
            connection.close()
            return country
        else:
            connection.close()
            return {"error": "The requested id was not found"}, 404
    else:
        return {"error": "Database error"}, 500

@app.delete("/countries/<int:id>")
def delete_country(id):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM countries WHERE id = %s", id)
        result = cursor.fetchall()
        if result: 
            cursor.execute("DELETE FROM countries WHERE id = %s", id)
            connection.commit()
            connection.close()
            return "", 204
        else:
            connection.close()
            return {"error": "The requested id was not found"}, 404
    else:
        return {"error": "Database error"}, 500

serve(app, listen='*:8080')