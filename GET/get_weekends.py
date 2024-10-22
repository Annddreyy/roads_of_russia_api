from flask import Blueprint, jsonify

from db import get_connection

get_weekends_blueprint = Blueprint('weekends', __name__)

@get_weekends_blueprint.route('/api/v1/weekends')
def get_weekends():
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM weekends')

        weekends = cur.fetchall()

        weekends_json = []
        for weekend in weekends:
            weekends_json.append(
                {
                    'id': weekend[0],
                    'date_start': str(weekend[1]),
                    'date_end': str(weekend[2]),
                    'client': weekend[3]
                }
            )

        return jsonify(weekends_json)
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }
    finally:
        cur.close()
        conn.close()

@get_weekends_blueprint.route('/api/v1/weekends/<int:weekend_id>')
def get_weekend(weekend_id):
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM weekends WHERE weekends_id={weekend_id}')

        weekend = cur.fetchone()

        if weekend:
            weekends_json = {
                'id': weekend[0],
                'date_start': str(weekend[1]),
                'date_end': str(weekend[2]),
                'client': weekend[3]
            }

            return jsonify(weekends_json)
        else:
            return {
                "status": "error",
                "code": 404,
                "message": f"Object with ID {weekend_id} not found"
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