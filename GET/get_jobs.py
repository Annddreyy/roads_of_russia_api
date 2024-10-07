from flask import Blueprint, jsonify

from db import get_connection

get_jobs_blueprint = Blueprint('jobs', __name__)

@get_jobs_blueprint.route('/api/v1/jobs', methods=['GET'])
def get_jobs():
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM job_title')

        jobs = cur.fetchall()

        jobs_json = []
        for job in jobs:
            jobs_json.append(
                {
                    'id': job[0],
                    'title': job[1]
                }
            )

        return jsonify(jobs_json)
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }
    finally:
        cur.close()
        conn.close()

@get_jobs_blueprint.route('/api/v1/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM job_title WHERE job_title_id={job_id}')

        job = cur.fetchone()

        if job:
            job_json = {
                'id': job[0],
                'title': job[1]
            }

            return jsonify(job_json)
        else:
            return {
                "status": "error",
                "code": 404,
                "message": f"Object with ID {job_id} not found"
            }
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }
    finally:
        cur.close()
        conn.close()
