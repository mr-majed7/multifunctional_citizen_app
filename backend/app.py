from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

profile = {
    "first_name": "Samiha",
    "last_name": "Tasnim",
    "email": "samihatasnim@gmail.com",
    "contact_number": "123-555-998-02",
    "address": "House 123, Dhaka",
    "city": "Dhaka",
    "state": "Dhaka",
    "zip_code": "1207",
    "country": "Bangladesh",
    "password": "12345678",
    "profile_photo": None,
}

users = {
    "user1": "password1",
    "user2": "password2"
}

candidates = [
    {"id": 1, "logoUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Dhaner_Shish.png/1200px-Dhaner_Shish.png"},
    {"id": 2, "logoUrl": "https://upload.wikimedia.org/wikipedia/commons/9/97/%E0%A6%B2%E0%A6%BE%E0%A6%99%E0%A7%8D%E0%A6%97%E0%A6%B2.jpg"},
    {"id": 3, "logoUrl": "https://www.thedailystar.net/sites/default/files/styles/big_202/public/images/city-election-2020/haatpakha_islami-andolan_0.jpg"}
]

votes = {}


@app.route("/api/profile", methods=["GET"])
def get_profile():
    return jsonify(profile)

@app.route("/api/profile", methods=["POST"])
def update_profile():
    data = request.json
    expected_fields = ["first_name", "last_name", "email", "contact_number", "address", "city", "state", "zip_code", "country"]

    for field in expected_fields:
        if field not in data:
            return jsonify({"success": False, "message": f"Missing field: {field}"}), 400

    profile.update(data)
    return jsonify({"success": True, "message": "Profile updated successfully!"})

@app.route("/api/profile/photo", methods=["POST"])
def upload_profile_photo():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "message": "No selected file"}), 400

    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    profile["profile_photo"] = filename
    return jsonify({"success": True, "message": "Photo uploaded successfully!", "photo": filename})

@app.route("/uploads/<filename>", methods=["GET"])
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        return jsonify({"loggedIn": True, "message": "Login successful!"}), 200
    else:
        return jsonify({"loggedIn": False, "message": "Invalid credentials!"}), 401

@app.route('/candidates', methods=['GET'])
def get_candidates():
    return jsonify(candidates)

@app.route('/vote', methods=['POST'])
def submit_vote():
    data = request.json
    username = data.get('username')
    candidate_id = data.get('candidate_id')

    if username not in users:
        return jsonify({"message": "User not authenticated!"}), 401

    votes[username] = candidate_id
    return jsonify({"message": "Your vote has been submitted!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
