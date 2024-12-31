from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt
import jwt
import datetime

app = Flask(__name__)
CORS(app)

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
