from flask import Blueprint, jsonify
from db import get_connection

get_resume_blueprint = Blueprint('resume', __name__)

@get_resume_blueprint.route('/api/v1/resume', methods=['GET'])
def get_resume():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM resume')

        resumes = cur.fetchall()

        resumes_json = []
        for resume in resumes:
            job_id = resume[5]
            cur.execute(f'SELECT title FROM job_title WHERE job_title_id={job_id}')
            job = cur.fetchone()

            resumes_json.append(
                {
                    'id': resume[0],
                    'author': f'{resume[1]} {resume[2][0]}. {resume[3][0]}.',
                    'file_path': resume[4],
                    'job_title': job[0]
                }
            )

        cur.close()
        conn.close()

        return jsonify(resumes_json)
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }

@get_resume_blueprint.route('/api/v1/resume/<int:resume_id>', methods=['GET'])
def get_one_resume(resume_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM resume WHERE resume_id={resume_id}')

        resume = cur.fetchone()

        if resume:
            resume_json = []

            job_id = resume[5]
            cur.execute(f'SELECT title FROM job_title WHERE job_title_id={job_id}')
            job = cur.fetchone()

            resume_json.append(
                {
                    'id': resume[0],
                    'author': f'{resume[1]} {resume[2][0]}. {resume[3][0]}.',
                    'file_path': resume[4],
                    'job_title': job[0]
                }
            )

            cur.close()
            conn.close()

            return jsonify(resume_json)
        else:
            return {
                "status": "error",
                "code": 404,
                "message": f"Object with ID {resume_id} not found"
            }
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }