from flask import Blueprint, jsonify

from db import get_connection

get_jobs_blueprint = Blueprint('jobs', __name__)

@get_jobs_blueprint.route('/api/v1/jobs', methods=['GET'])
def get_jobs():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM job_title')

    jobs = cur.fetchall()

    jobs_json = []
    for job in jobs:
        jobs_json.append(
            {
                'id': job[0],
                'title': job[1]
            }
        )

    cur.close()
    conn.close()

    return jsonify(jobs_json)

@get_jobs_blueprint.route('/api/v1/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f'SELECT * FROM job_title WHERE job_title_id={job_id}')

    job = cur.one()

    job_json = {
        'id': job[0],
        'title': job[1]
    }

    cur.close()
    conn.close()

    return jsonify(job_json)
