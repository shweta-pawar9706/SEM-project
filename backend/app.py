from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import resume_parser
import scorer
import ats
import skillgap
import matcher

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return jsonify({"message": "Resume Analyzer API is running!"})


@app.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    parsed_data = resume_parser.parse_resume(filepath)
    score_data  = scorer.score_resume(parsed_data)
    return jsonify({
        "message": "Resume uploaded successfully",
        "data":    parsed_data,
        "score":   score_data
    })


@app.route("/ats", methods=["POST"])
def ats_check():
    data   = request.json
    result = ats.check_ats(data)
    return jsonify(result)


@app.route("/skillgap", methods=["POST"])
def skill_gap():
    data   = request.json
    result = skillgap.analyze_skill_gap(data)
    return jsonify(result)


@app.route("/match", methods=["POST"])
def match_roles():
    data   = request.json
    result = matcher.match_job_roles(data)
    return jsonify(result)


@app.route("/courses", methods=["GET"])
def get_courses():
    with open("data/courses.json", "r") as f:
        courses = json.load(f)
    return jsonify(courses)


if __name__ == "__main__":
    app.run(debug=True, port=5000)