import mysql.connector
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
import random

app = Flask(__name__)
CORS(app, origins="*")

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db_config = {
    'host': 'localhost',  
    'user': 'root',        
    'password': '12345',  
    'database': 'multifunctional_citizen_app'
}
def get_db_connection():
    return mysql.connector.connect(**db_config)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

applications = {}
application_id_counter = 10000000000
receipt_folder = "receipts"  

if not os.path.exists(receipt_folder):
    os.makedirs(receipt_folder)

@app.route('/submit_application', methods=['POST'])
def submit_application():
    form_data = request.json

    if not form_data:
        return jsonify({"error": "No data provided"}), 400

    try:
        
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

       
        sql = """
        INSERT INTO applications (
            passport_type, passport_pages, years_validity, nid, mobile_number,
            country_code, gender, marital_status, full_name, given_name,
            surname, profession, religion, email, password,
            permanent_country, permanent_district, permanent_city,
            permanent_post_office, present_country, present_district,
            present_city, present_post_office, father_name, father_profession,
            father_nid, mother_name, mother_profession, mother_nid, receipt_path
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (
            form_data.get('passport_type'), form_data.get('passport_pages'), form_data.get('years_validity'),
            form_data.get('nid'), form_data.get('mobile_number'), form_data.get('country_code'),
            form_data.get('gender'), form_data.get('marital_status'), form_data.get('full_name'),
            form_data.get('given_name'), form_data.get('surname'), form_data.get('profession'),
            form_data.get('religion'), form_data.get('email'), form_data.get('password'),
            form_data.get('permanent_country'), form_data.get('permanent_district'),
            form_data.get('permanent_city'), form_data.get('permanent_post_office'),
            form_data.get('present_country'), form_data.get('present_district'),
            form_data.get('present_city'), form_data.get('present_post_office'),
            form_data.get('father_name'), form_data.get('father_profession'),
            form_data.get('father_nid'), form_data.get('mother_name'),
            form_data.get('mother_profession'), form_data.get('mother_nid'),
            None  
        )
        cursor.execute(sql, data)
        application_id = cursor.lastrowid

       
        receipt_path = os.path.join(receipt_folder, f"receipt_{application_id}.txt")
        with open(receipt_path, "w") as f:
            f.write(f"Application ID: {application_id}\n")
            f.write(f"Full Name: {form_data.get('full_name', 'N/A')}\n")
            f.write(f"Passport Type: {form_data.get('passport_type', 'N/A')}\n")
            f.write(f"Mobile Number: {form_data.get('country_code', '')} {form_data.get('mobile_number', '')}\n")
            f.write(f"Email: {form_data.get('email', 'N/A')}\n")

        
        cursor.execute("UPDATE applications SET receipt_path = %s WHERE id = %s", (receipt_path, application_id))
        connection.commit()

        return jsonify({"message": "Application submitted successfully", "id": application_id, "receipt_path": receipt_path}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/download-receipt', methods=['GET'])
def download_receipt():
    try:
        receipt_path = request.args.get('path')
        if not receipt_path or not os.path.exists(receipt_path):
            return jsonify({"error": "Invalid receipt path"}), 400
        return send_file(receipt_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/property-tax', methods=['POST'])
def property_tax():
    try:
        
        property_type = request.form.get('propertyType')
        section_id = request.form.get('sectionId')
        peth_id = request.form.get('pethId')
        account_no = request.form.get('accountNo')
        name = request.form.get('name')
        address = request.form.get('address')
        property_description = request.form.get('propertyDescription')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        year = request.form.get('year')
        amount = request.form.get('amount')
        
     
        document = request.files.get('documents')
        document_path = None
        if document:
            document_path = os.path.join(tempfile.gettempdir(), document.filename)
            document.save(document_path)
      
        
        connection = get_db_connection()
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO property_tax_records (
                property_type, section_id, peth_id, account_no, name,
                address, property_description, mobile, email, year,
                amount, document_path
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            property_type, section_id, peth_id, account_no, name,
            address, property_description, mobile, email, year,
            amount, document_path
        ))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Form submitted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/records', methods=['GET'])
def get_records():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM property_tax_records")
        records = cursor.fetchall()
        cursor.close()
        connection.close()

        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
    
@app.route('/api/tin/register', methods=['POST'])
def register_tin():
    try:
       
        name = request.form.get('name')
        national_id = request.form.get('nationalID')
        address = request.form.get('address')
        phone = request.form.get('phone')
        file = request.files.get('documents')

       
        if not all([name, national_id, address, phone]):
            return jsonify({'error': 'All fields are required.'}), 400

       
        file_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        elif file:
            return jsonify({'error': 'Invalid document file type.'}), 400

     
        tin_number = f"TIN{random.randint(100000, 999999)}"

        
        db = get_db_connection()
        cursor = db.cursor()
        query = """
            INSERT INTO tin_applications (name, national_id, address, phone, tin_number, document_path)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, national_id, address, phone, tin_number, file_path))
        db.commit()

        cursor.close()
        db.close()

       
        print(f"SMS to {phone}: Your TIN number is {tin_number}")

        return jsonify({'status': 'Application submitted', 'tinNumber': tin_number}), 200

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
       

if __name__ == "__main__":
    app.run(debug=True, port=5000)


