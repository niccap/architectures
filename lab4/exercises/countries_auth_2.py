# countries.py
from flask import Flask, request, jsonify
from waitress import serve
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
auth = HTTPTokenAuth(scheme="API-Key") # Define the authentication type

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

@auth.verify_token
def verify_api_key(api_key):
    if api_key in auth_db:
        return auth_db[api_key]  # Returns the associated name
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



