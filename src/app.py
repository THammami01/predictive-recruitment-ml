import os
import uuid
from pathlib import Path

import pymongo
from dotenv import load_dotenv
from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
from marshmallow import ValidationError

from funcs import classification, regression
from schemas import application, job

load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

mongo_client = pymongo.MongoClient(os.getenv("mongodb_conn_url"))
db = mongo_client["recruitment-project"]

Path("./src/figures").mkdir(exist_ok=True)

# sample_data = [
#     {"salary": 1000, "years_of_experience": 0, "has_diploma": False},
#     {"salary": 1500, "years_of_experience": 1, "has_diploma": False},
#     {"salary": 1700, "years_of_experience": 1, "has_diploma": True},
#     {"salary": 1200, "years_of_experience": 0, "has_diploma": False},
#     {"salary": 1150, "years_of_experience": 0, "has_diploma": False},
#     {"salary": 1800, "years_of_experience": 3, "has_diploma": True},
#     {"salary": 1550, "years_of_experience": 1, "has_diploma": False},
#     {"salary": 1750, "years_of_experience": 2, "has_diploma": False},
#     {"salary": 2200, "years_of_experience": 4, "has_diploma": True},
#     {"salary": 2050, "years_of_experience": 5, "has_diploma": True},
#     {"salary": 3000, "years_of_experience": 5, "has_diploma": True},
#     {"salary": 4000, "years_of_experience": 10, "has_diploma": True},
#     {"salary": 3500, "years_of_experience": 8, "has_diploma": True},
#     {"salary": 4500, "years_of_experience": 10, "has_diploma": True},
#     {"salary": 4200, "years_of_experience": 12, "has_diploma": True},
# ]


@app.route("/jobs", methods=["GET"])
@cross_origin()
def get_jobs():
    """
    Retrieves a list of jobs from the database.

    Returns:
        A list of jobs.
    """

    return list(db["jobs"].find({}, {"_id": 0}))


@app.route("/jobs", methods=["POST"])
@cross_origin()
def create_job():
    """
    Creates a new job.

    Returns:
        dict: A dictionary containing the job ID.
    """

    try:
        job_data = job.schema.load(request.get_json())

        job_data["id"] = str(uuid.uuid4())
        db["jobs"].insert_one(job_data)

        return {"job_id": job_data["id"]}, 201
    except ValidationError as e:
        return {"error": str(e)}, 400


@app.route("/jobs/<job_id>/apply", methods=["POST"])
@cross_origin()
def apply_for_job(job_id):
    """
    Creates a job application.

    Args:
        job_id (str): The ID of the job to apply for.

    Returns:
        dict: A dictionary containing the application ID.
    """

    try:
        application_data = application.schema.load(request.get_json())

        job = db["jobs"].find_one({"id": job_id}, {"_id": 0})
        if not job:
            return {"error": "Job not found"}, 404

        application_data["id"] = str(uuid.uuid4())
        application_data["job_id"] = job_id
        db["applications"].insert_one(application_data)

        return {"application_id": application_data["id"]}, 201
    except ValidationError as e:
        return {"error": str(e)}, 400


@app.route("/jobs/<job_id>/stats", methods=["GET"])
@cross_origin()
def get_job_stats(job_id):
    """
    Retrieves job statistics based on the provided job ID.

    Args:
        job_id (str): The ID of the job.

    Returns:
        dict: A dictionary containing the jobs, their applications, and regression/classification figures.
    """

    job = db["jobs"].find_one({"id": job_id}, {"_id": 0})
    if not job:
        return {"error": "Job not found"}, 404

    applications = list(db["applications"].find({"job_id": job_id}, {"_id": 0}))

    figures = [
        regression.generate_decision_tree(
            applications,
            feature_name="years_of_experience",
            feature_label="Years of Experience",
            target_name="salary",
        ),
        # regression.generate_decision_tree(
        #     applications,
        #     feature_name="salary",
        #     feature_label="Salary",
        #     target_name="years_of_experience",
        # ),
        # regression.generate_decision_tree(
        #     applications,
        #     feature_name="has_diploma",
        #     feature_label="Has Diploma",
        #     target_name="years_of_experience",
        # ),
        # regression.generate_decision_tree(
        #     applications,
        #     feature_name="has_diploma",
        #     feature_label="Has Diploma",
        #     target_name="salary",
        # ),
        # classification.generate_decision_tree(
        #     applications,
        #     feature_name="years_of_experience",
        #     feature_label="Years of Experience",
        #     target_name="has_diploma",
        # ),
        # classification.generate_decision_tree(
        #     applications,
        #     feature_name="salary",
        #     feature_label="Salary",
        #     target_name="has_diploma",
        # ),
        # regression.generate_linear_regression(
        #     applications,
        #     feature_name="years_of_experience",
        #     feature_label="Years of Experience",
        #     target_name="salary",
        #     target_label="Salary",
        #     prediction_range=(0, 20, 2),
        # ),
        # regression.generate_linear_regression(
        #     applications,
        #     feature_name="salary",
        #     feature_label="Salary",
        #     target_name="years_of_experience",
        #     target_label="Years of Experience",
        #     prediction_range=(1000, 5000, 100),
        # ),
    ]

    return {"job": job, "applications": applications, "figures": figures}


@app.route("/figures/<id>", methods=["GET"])
def get_figure_image(id):
    """
    Retrieves the image file for a given figure ID.

    Args:
        id (str): The ID of the figure.

    Returns:
        The file as a response with the appropriate MIME type.
    """

    try:
        return send_file(f"./src/figures/{id}.png", mimetype="image/png")
    except FileNotFoundError:
        return {"error": "Figure not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)
