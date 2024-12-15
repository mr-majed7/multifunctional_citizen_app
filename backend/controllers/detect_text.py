from flask import Flask, request, jsonify
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

def detect_text_in_image(image_bytes):
    rekognition = boto3.client(
        "rekognition",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    response = rekognition.detect_text(Image={"Bytes": image_bytes})

    text_detections = response["TextDetections"]

    name = None
    dob = None
    id_no = None

    for i in range(len(text_detections)):
        detected_text = text_detections[i]["DetectedText"]

        if "Name:" in detected_text:
            if i + 1 < len(text_detections):
                name = text_detections[i + 1][
                    "DetectedText"
                ] 
            break

    for i in range(len(text_detections)):
        detected_text = text_detections[i]["DetectedText"]

        if "date of birth" in detected_text.lower():
            dob = detected_text.split(":")[-1].strip() 
        elif "id no" in detected_text.lower():
            id_no = detected_text.split(":")[-1].strip()

    return {"Name": name, "Date of Birth": dob, "ID NO": id_no}



def detect_text():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files["image"]
    image_bytes = image_file.read()

    result = detect_text_in_image(image_bytes)
    
    return jsonify(result)
