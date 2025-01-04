from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy.orm import relationship
from decouple import config
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from controllers.detect_text import detect_text
from controllers.utility_bills import fetch_bills, update_bill_status
from controllers.payments import add_payment_details
from controllers.service_req import submit_request
import os
import mysql.connector
import bcrypt
import jwt
import datetime

app = Flask(__name__)
#CORS(app)
CORS(app,"origins": "*")
#app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
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

#users = {
 #   "user1": "password1",
  #  "user2": "password2"
#}

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
        {"service": "Fire", "phone_number": "102"},
        {"service": "Medical", "phone_number": "16263"},
    ]
    for contact in contacts:
        exists = PredefinedContact.query.filter_by(service=contact["service"]).first()
        if not exists:
            new_contact = PredefinedContact(service=contact["service"], phone_number=contact["phone_number"])
            db.session.add(new_contact)
    db.session.commit()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
class Complaint(db.Model):
    __tablename__ = 'complaint'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)
    user = relationship("User", backref="complaints")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

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


#@app.route('/login', methods=['POST'])
#def login():
 #   data = request.json
  #  username = data.get('username')
   # password = data.get('password')

    #if username in users and users[username] == password:
     #   return jsonify({"loggedIn": True, "message": "Login successful!"}), 200
    #else:
    #    return jsonify({"loggedIn": False, "message": "Invalid credentials!"}), 401

@app.route('/candidates', methods=['GET'])
def get_candidates():
    return jsonify(candidates)

@app.route('/vote', methods=['POST'])
def submit_vote():
    data = request.json
    #username = data.get('username')
    candidate_id = data.get('candidate_id')
    client_ip = request.remote_addr  
    if client_ip in votes:
        return jsonify({"message": "You have already voted!"}), 400
    votes[client_ip] = candidate_id
    return jsonify({"message": "Your vote has been submitted!"}), 200

  #  if username not in users:
   #     return jsonify({"message": "User not authenticated!"}), 401

   # votes[username] = candidate_id
    #return jsonify({"message": "Your vote has been submitted!"}), 200


@app.route('/emergency/personal', methods=['POST'])
def add_personal_contact():
    try:
        data = request.get_json()
        phone_number_pattern = re.compile(r'^\d{11}$')  
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

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500

@app.route('/complaints', methods=['POST'])
def create_complaint():
    data = request.get_json()
    if not all(key in data for key in ('user_id', 'title', 'description')):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        new_complaint = Complaint(
            user_id=data['user_id'],
            title=data['title'],
            description=data['description']
        )
        db.session.add(new_complaint)
        db.session.commit()
        return jsonify({"message": "Complaint submitted successfully!", "complaint": new_complaint.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/complaints', methods=['GET'])
def get_complaints():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    complaints = Complaint.query.filter_by(deleted=False).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "total": complaints.total,
        "pages": complaints.pages,
        "current_page": complaints.page,
        "complaints": [complaint.to_dict() for complaint in complaints.items]
    }), 200

    #complaints = Complaint.query.all()
    #return jsonify([complaint.to_dict() for complaint in complaints]), 200

@app.route('/complaints/<int:user_id>', methods=['GET'])
def get_user_complaints(user_id):
    complaints = Complaint.query.filter_by(user_id=user_id, deleted=False).all()
    return jsonify([complaint.to_dict() for complaint in complaints]), 200

@app.route('/complaints/<int:complaint_id>', methods=['DELETE'])
def delete_complaint(complaint_id):
    complaint = Complaint.query.get(complaint_id)
    if not complaint or complaint.deleted:
        return jsonify({"error": "Complaint not found"}), 404
    try:
        complaint.deleted = True
        #db.session.delete(complaint)
        db.session.commit()
        return jsonify({"message": "Complaint deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/detect-text", methods=["POST"])
def handle_detect_text():
    return detect_text()


@app.route('/get_bills/<nid_no>', methods=['GET'])
def get_bills(nid_no):
    bills, error = fetch_bills(nid_no)

    if error:
        return jsonify({"error": error}), 404

    return jsonify(bills), 200

@app.route('/update_bill_status/<bill_id>', methods=['PUT'])
def update_status(bill_id):
    message, status_code = update_bill_status(bill_id, 1)

    return jsonify({"message": message}), status_code

@app.route('/add_payment', methods=['POST'])
def add_payment():
    payment_details = request.json
    response, status_code = add_payment_details(payment_details)

    return response, status_code

@app.route('/service_req/<user_id>/<req_type>', methods=['POST'])
def handle_submit_request(user_id, req_type):
    data = request.json
    ticket_no = data.get('ticket_no')
    form_data = data.get('form_data')
    document_type = data.get('document_type')
    document_number = data.get('document_number')

    if not ticket_no or not form_data:
        return jsonify({"error": "Missing required fields: 'ticket_no' or 'form_data'"}), 400

    response, status_code = submit_request(user_id, req_type, ticket_no,document_type,document_number, form_data)

    return jsonify(response), status_code

app.config['SECRET_KEY'] = '39039'


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="39039",
        database="multifunctional_citizen_app"
    )


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json

    name = data.get('name')
    address = data.get('address')
    city = data.get('city')
    nid = data.get('nid')
    dob = data.get('dob')
    phone = data.get('phone')
    religion = data.get('religion')
    gender = data.get('gender')
    email = data.get('email')
    password = data.get('password')

    if not all([name, address, city, nid, dob, phone, religion, gender, email, password]):
        return jsonify({"error": "All fields are required"}), 400

    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        conn = get_db_connection()
        cursor = conn.cursor()

        print("Attempting to register user with email:", email)

        cursor.execute("""
            INSERT INTO users (name, address, city, nid, dob, phone, religion, gender, email, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, address, city, nid, dob, phone, religion, gender, email, hashed_password))

        conn.commit()
        print("User registered successfully with email:", email)

        cursor.close()
        conn.close()

        return jsonify({"message": "User registered successfully"}), 201

    except mysql.connector.IntegrityError as e:
        print("Database Integrity Error:", str(e))
        return jsonify({"error": "Email or NID already exists"}), 409
    except Exception as e:
        print("Error occurred during signup:", str(e))
        return jsonify({"error": "An error occurred"}), 500
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

@app.route('/', methods=['POST'])
def signin():
    data = request.json

    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"error": "Email and password are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        print("Attempting to sign in user with email:", email)

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))  
        user = cursor.fetchone()

        if not user:
            print("No user found with this email:", email)
            return jsonify({"error": "Invalid email or password"}), 401

        print("Fetched user:", user) 

        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            print("Password matched for user ID:", user['id'])  

            token = jwt.encode(
                {'user_id': user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )

            print("JWT generated successfully for user ID:", user['id'])  

            return jsonify({
                "message": "Login successful",
                "token": token,
                "user_id": user['id'],
                "nid": user['nid']
            }), 200
        else:
            print("Password did not match for email:", email)  
            return jsonify({"error": "Invalid email or password"}), 401

    except Exception as e:
        print("Error occurred during signin:", str(e))
        return jsonify({"error": "An error occurred"}), 500

    finally:
        cursor.close()
        conn.close()

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    print("Received feedback data:", data)

    required_fields = ['name', 'email', 'experience', 'usability', 'recommendation', 'feedback_text']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    name = data['name']
    email = data['email']
    experience = data['experience']
    usability = data['usability']
    recommendation = data['recommendation']
    feedback_text = data['feedback_text']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO feedback (name, email, experience, usability, recommendation, feedback_text)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, experience, usability, recommendation, feedback_text))
        conn.commit()

        return jsonify({'message': 'Feedback submitted successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/trafficfine', methods=['GET'])
def get_fines():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT users.name, users.nid, traffic_fine.case_number, traffic_fine.cause, traffic_fine.due_payment, traffic_fine.status
            FROM traffic_fine
            JOIN users ON traffic_fine.nid = users.nid
        """
        cursor.execute(query)
        fines = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(fines), 200
    except Exception as e:
        print("Error fetching fines:", e)
        return jsonify({"error": "Failed to fetch fines."}), 500


if __name__ == "__main__":
    app.run(debug=True)
