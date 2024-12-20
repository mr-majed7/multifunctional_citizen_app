from flask import Flask, request, jsonify
from flask_cors import CORS 
from controllers.detect_text import detect_text
from controllers.utility_bills import fetch_bills, update_bill_status

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

@app.route('/update_bill_status/<bill_id>', methods=['POST'])
def update_status(bill_id):
    message, status_code = update_bill_status(bill_id, status)

    return jsonify({"message": message}), status_code

if __name__ == "__main__":
    app.run(debug=True)
