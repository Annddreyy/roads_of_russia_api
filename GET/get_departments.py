from flask import Blueprint, jsonify

from db import get_connection

get_departments_bluprint = Blueprint('departments', __name__)

@get_departments_bluprint.route('/api/v1/departments', methods=['GET'])
def get_departments():
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT department_id, title FROM department')

        departments = cur.fetchall()

        departments_json = []

        for department in departments:
            departments_json.append(
                {
                    'id': department[0],
                    'title': department[1]
                }
            )

        return jsonify(departments_json)
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }
    finally:
        cur.close()
        conn.close()
