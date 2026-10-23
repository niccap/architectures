# LAB 4 - EXERCISE 1
# Improve the country Web service to enforce:
# - API-key authentication
# - HTTPS-based secure connection
# - CORS support
# Containerize your Web service and deploy it on Azure

# countries_auth.py

# To start the HTTP server:
# hypercorn countries_auth:app --bind :8080

# To start the HTTPS server:
# hypercorn countries_auth:app --bind :443 --certfile=cert.pem --keyfile=key.pem 

from flask import Flask, request, jsonify

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

@app.get("/countries", provide_automatic_options=False)
def get_countries():
    return jsonify(countries) 

@app.post("/countries", provide_automatic_options=False)
def add_country():
    if request.is_json:
        country = request.get_json() 
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415

# Check API-key before any request (except for the OPTIONS method)
@app.before_request
def before_request():
    if request.method != 'OPTIONS': # skip the OPTIONS method to enable CORS
        api_key = request.headers.get('API-Key')
        if not api_key or not api_key in auth_db:
            return {'error': 'Unauthorized'}, 401

# Enable CORS to allow requests from web browsers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response

# To enable CORS the OPTIONS method must respond with the OK status
@app.route('/countries', methods=['OPTIONS'])
def handle_options():
    return '', 200 # No content, just a successful response
