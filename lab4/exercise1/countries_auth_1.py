# LAB 4 - EXERCISE
# Modify the server to support API-key authentication

from flask import Flask, request, jsonify
from waitress import serve

app = Flask(__name__)

countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]

auth_db = {
    '2RQs4LkXj6eQ73c?-YKtPYXg5ce0ERvmVIg4IUMc1q2?DAH/R1IZkxv7sWHNawWb': 'user1', 
    'sNrfAdL0c-93ZQV9xE!W5WCqYKDdXkE7Djc5kXh8jO!ruYWnPqCOu1hI---0ovX?': 'user2'
    }

def _find_next_id():
    return max(country["id"] for country in countries) + 1

@app.before_request
def before_request():
    api_key = request.headers.get('API-Key')
    if not api_key or not api_key in auth_db:
        return {'error': 'Unauthorized'}, 401

@app.get("/countries")
def get_countries():
    return jsonify(countries) # generates JSON from a Python list

@app.post("/countries")
def add_country():
    if request.is_json:
        country = request.get_json() # generates a Python dictionary from a JSON
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415

serve(app, listen='*:8080')



