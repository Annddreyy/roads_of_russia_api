from flask import Blueprint, jsonify, request
from db import get_connection

post_event_blueprint = Blueprint('post_event', __name__)

@post_event_blueprint.route('/api/v1/events', methods=['POST'])
def add_event():
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        event = request.get_json()

        title = event['title']
        text = event['text']
        date_start = event['date_start']
        date_end = event['date_end']
        event_type_id = event['event_type']
        author = event['author']
        image_path = event['image_path']

        cur.execute('INSERT INTO event'
                    '(title, description, event_type_id, author_id, '
                    'image_path, date_start, date_end) '
                    f"VALUES('{title}', '{text}', {int(event_type_id)}, "
                    f"{author}, '{image_path}', '{date_start}', '{date_end}')")

        conn.commit()

        return jsonify({'message': 'Event was been upload!'}), 200
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }
    finally:
        cur.close()
        conn.close()