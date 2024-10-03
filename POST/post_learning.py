from flask import Blueprint, jsonify, request
from db import get_connection

post_learning_blueprint = Blueprint('post_learning', __name__)

@post_learning_blueprint.route('/api/v1/learnings', methods=['POST'])
def add_learning():
    try:
        conn = get_connection()
        cur = conn.cursor()

        learning = request.get_json()

        title = learning['title']
        text = learning['text']
        date_start = learning['date_start']
        date_end = learning['date_end']
        author = learning['author']
        image_path = learning['image_path']

        cur.execute('INSERT INTO event'
                    '(title, description, event_type_id, author_id, '
                    'image_path, date_start, date_end) '
                    f"VALUES('{title}', '{text}', 1, "
                    f"{author}, '{image_path}', '{date_start}', '{date_end}')")

        cur.commit()

        cur.close()
        conn.close()

        return jsonify({'message': 'Event was been upload!'}), 200
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }