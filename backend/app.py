from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
import re


app = Flask(__name__)
#CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sammy@localhost/multifunctional_citizen_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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


class PredefinedContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(50), nullable=False)  
    phone_number = db.Column(db.String(15), nullable=False)

class PersonalContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


with app.app_context():
    db.create_all()
    contacts = [
        {"service": "Police", "phone_number": "999"},
        {"service": "Fire", "phone_number": "998"},
        {"service": "Medical", "phone_number": "997"},
    ]
    for contact in contacts:
        exists = PredefinedContact.query.filter_by(service=contact["service"]).first()
        if not exists:
            new_contact = PredefinedContact(service=contact["service"], phone_number=contact["phone_number"])
            db.session.add(new_contact)
    db.session.commit()


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


@app.route('/emergency/personal', methods=['POST'])
def add_personal_contact():
    try:
        data = request.get_json()
        phone_number_pattern = re.compile(r'^\d{11}$')  # Example: strict validation
        if not phone_number_pattern.match(data.get('phone_number', '')):
            return jsonify({"message": "Invalid phone number format"}), 400
        if not data.get('name') or not data.get('user_id'):
            return jsonify({"message": "Name and user_id are required"}), 400
        
        new_contact = PersonalContact(
            user_id=data['user_id'],
            name=data['name'],
            phone_number=data['phone_number'],
            relationship=data.get('relationship', '')
        )
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({"message": "Personal contact added successfully!"}), 201
    except Exception as e:
        print(f"Error: {e}") 
        return jsonify({"message": "Failed to add contact", "error": str(e)}), 500

@app.route('/emergency/predefined', methods=['GET'])
def get_predefined_contacts():
    contacts = PredefinedContact.query.all()
    result = [{"id": c.id, "service": c.service, "phone_number": c.phone_number} for c in contacts]
    return jsonify(result)

@app.route('/emergency/personal/<int:user_id>', methods=['GET'])
def get_personal_contacts(user_id):
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        contacts = PersonalContact.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)
        result = [{"id": c.id, "name": c.name, "phone_number": c.phone_number, "relationship": c.relationship} for c in contacts.items]
        return jsonify({"contacts": result, "total": contacts.total, "pages": contacts.pages})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to retrieve personal contacts", "error": str(e)}), 500


@app.route('/emergency/personal/<int:user_id>/<int:contact_id>', methods=['DELETE'])
def delete_personal_contact(user_id, contact_id):
    contact = PersonalContact.query.filter_by(user_id=user_id, id=contact_id).first()
    if not contact:
        return jsonify({"message": "Contact not found"}), 404
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": "Contact deleted successfully!"})


#if __name__ == '__main__':
  #  app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
