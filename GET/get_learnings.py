from flask import Blueprint, jsonify
from db import get_connection

get_learnings_blueprint = Blueprint('learnings', __name__)

@get_learnings_blueprint.route('/api/v1/learnings', methods=['GET'])
def get_learnings():
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT event_id, title, description, author_id, image_path, date_start, date_end '
                    'FROM event WHERE event_type_id=1')
        learnings = cur.fetchall()

        learnings_json = []
        for learning in learnings:
            author_id = learning[3]
            cur.execute(f'SELECT surname, name, patronymic, photo '
                        f'FROM client WHERE client_id={author_id}')
            author = cur.fetchone()

            learnings_json.append(
                {
                    'id': learning[0],
                    'title': learning[1],
                    'description': learning[2],
                    'author': f'{author[0]} {author[1][0]}. {author[2][0]}.',
                    'photo': author[3],
                    'image_path': learning[4],
                    'date_start': str(learning[5]),
                    'date_end': str(learning[6])
                }
            )

        return jsonify(learnings_json)
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }
    finally:
        cur.close()
        conn.close()

@get_learnings_blueprint.route('/api/v1/learnings/<int:learning_id>', methods=['GET'])
def get_one_learning(learning_id):
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT event_id, title, description, author_id, image_path, date_start, date_end '
                    f'FROM event WHERE event_type_id=1 AND event_id={learning_id}')

        learning = cur.fetchone()

        if learning:
            cur.execute(f'SELECT surname, name, patronymic '
                        f'FROM client WHERE client_id={learning[3]}')
            author = cur.fetchone()

            learning_json = {
                'id': learning[0],
                'title': learning[1],
                'description': learning[2],
                'author': f'{author[0]} {author[1][0]}. {author[2][0]}',
                'image_path': learning[4],
                'date_start': str(learning[5]),
                'date_end': str(learning[6])
            }

            return jsonify(learning_json)
        else:
            return {
                "status": "error",
                "code": 404,
                "message": f"Object with ID {learning_id} not found"
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