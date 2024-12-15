from flask import Flask, request, jsonify
from flask_cors import CORS 
from controllers.detect_text import detect_text

app = Flask(__name__)
CORS(app)

@app.route("/detect-text", methods=["POST"])
def handle_detect_text():
    return detect_text()

if __name__ == "__main__":
    app.run(debug=True)
