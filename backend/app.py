from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from controllers.detect_text import detect_text
from controllers.utility_bills import fetch_bills, update_bill_status
from controllers.payments import add_payment_details
from controllers.service_req import submit_request
import os

app = Flask(__name__)
CORS(app)  

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


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/multifunctional_citizen'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    religion = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(
        name=data['name'],
        address=data['address'],
        city=data['city'],
        country=data['country'],
        phone=data['phone'],
        religion=data['religion'],
        gender=data['gender'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/signin', methods=['POST'])
def signin():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
