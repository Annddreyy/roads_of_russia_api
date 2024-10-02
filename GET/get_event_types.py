from flask import Blueprint, jsonify
from db import get_connection

get_event_types_blueprint = Blueprint('event_types', __name__)

@get_event_types_blueprint.route('/api/v1/event_types', methods=['GET'])
def get_event_types():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM event_type')

        event_types = cur.fetchall()

        event_types_json = []
        for event_type in event_types:
            event_types_json.append(
                {
                    'id': event_type[0],
                    'title': event_type[1],
                    'description': event_type[2]
                }
            )

        return jsonify(event_types_json)
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }