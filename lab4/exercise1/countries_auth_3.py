# LAB 4 - EXERCISE
# Modify the server to support HTTP Basic Authentication

from flask import Flask, request, jsonify
from waitress import serve
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth() # Define the authentication type

countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]

users = {
    'user1': 'password123',
    'user2': 'securepass456'
}

def _find_next_id():
    return max(country["id"] for country in countries) + 1

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username  # Returns the associated name
    return None # Access denied

@app.get("/countries")
@auth.login_required # Protect the route with the authentication
def get_countries():
    return jsonify(countries) # generates JSON from a Python list

@app.post("/countries")
@auth.login_required # Protect the route with the authentication
def add_country():
    if request.is_json:
        country = request.get_json() # generates a Python dictionary from a JSON
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415

serve(app, listen='*:8080')



