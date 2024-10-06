from flask import Blueprint, jsonify
from db import get_connection

get_events_blueprint = Blueprint('events', __name__)

@get_events_blueprint.route('/api/v1/events', methods=['GET'])
def get_events():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM event')

        events = cur.fetchall()

        events_json = []
        for event in events:
            event_type_id = event[3]
            cur.execute(f'SELECT title FROM event_type WHERE event_type_id={event_type_id}')
            event_type = cur.fetchone()[0]

            author_id = event[4]
            cur.execute(f'SELECT surname, name, patronymic, photo '
                        f'FROM client WHERE client_id={author_id}')
            author = cur.fetchone()

            events_json.append(
                {
                    'id': event[0],
                    'title': event[1],
                    'description': event[2],
                    'event_type': event_type,
                    'author': f'{author[0]} {author[1][0]}. {author[2][0]}.',
                    'photo': author[3],
                    'image_path': event[5],
                    'date_start': str(event[6]),
                    'date_end': str(event[7])
                }
            )

        return jsonify(events_json)
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }

@get_events_blueprint.route('/api/v1/events/<int:event_id>', methods=['GET'])
def get_one_event(event_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM event WHERE event_id={event_id}')

        event = cur.fetchone()

        if event:
            event_type_id = event[3]
            cur.execute(f'SELECT title FROM event_type WHERE event_type_id={event_type_id}')
            event_type = cur.fetchone()[0]

            author_id = event[4]
            cur.execute(f'SELECT surname, name, patronymic, photo '
                        f'FROM client WHERE client_id={author_id}')
            author = cur.fetchone()

            event_json = {
                'id': event[0],
                'title': event[1],
                'description': event[2],
                'event_type': event_type,
                'author': f'{author[0]} {author[1][0]}. {author[2][0]}.',
                'image_path': event[5],
                'date_start': str(event[6]),
                'date_end': str(event[7])
            }

            return jsonify(event_json)
        else:
            return {
                "status": "error",
                "code": 404,
                "message": f"Object with ID {event_id} not found"
            }
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }