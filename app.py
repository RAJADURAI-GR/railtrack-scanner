from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
# Allow CORS for all domains, crucial for local development
CORS(app)

# Load data from the simple JSON database
try:
    with open('data.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: data.json not found. Creating a new one...")
    data = {
        "users": [
            {
                "username": "admin",
                "password": "Admin123", # For a real app, this should be a hashed password
                "role": "admin"
            },
            {
                "username": "inspector",
                "password": "User123",
                "role": "team_member"
            }
        ],
        "fittings": {
            "TRK-001": {
                "vendorName": "Global Rail Solutions Inc.",
                "manufactureDate": "2023-05-15",
                "inspectionHistory": [
                    "2023-06-01: Initial inspection",
                    "2023-12-10: Routine maintenance check",
                    "2024-03-22: Post-weather anomaly inspection"
                ],
                "warrantyPeriod": "5 years"
            },
            "TRK-002": {
                "vendorName": "Innovate Rail Solutions",
                "manufactureDate": "2024-01-20",
                "inspectionHistory": [
                    "2024-02-15: Initial installation and inspection"
                ],
                "warrantyPeriod": "10 years"
            },
            "TRK-003": {
                "vendorName": "TrackSafe Global",
                "manufactureDate": "2022-11-05",
                "inspectionHistory": [
                    "2022-12-01: Initial inspection",
                    "2023-10-15: Routine checkup"
                ],
                "warrantyPeriod": "3 years"
            }
        }
    }
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/login', methods=['POST'])
def login():
    """
    Handles user login authentication.
    Validates username and password against the data.json file.
    """
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        
        user = next((u for u in data['users'] if u['username'] == username and u['password'] == password), None)
        
        if user:
            return jsonify({"message": "Login successful", "role": user['role']}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/fitting/<fitting_id>', methods=['GET'])
def get_fitting_details(fitting_id):
    """
    Retrieves details for a specific track fitting based on its ID.
    """
    try:
        fitting_details = data['fittings'].get(fitting_id)
        if fitting_details:
            return jsonify(fitting_details), 200
        else:
            return jsonify({"error": "Fitting ID not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Using 0.0.0.0 for development to be accessible on the network
    # For production, consider using a WSGI server like Gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)
