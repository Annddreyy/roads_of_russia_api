from flask import Blueprint, jsonify

from db import get_connection

get_supervisor_blueprint = Blueprint('supervisor', __name__)

@get_supervisor_blueprint.route('/api/v1/supervisor/<int:department_id>')
def get_supervisor(department_id):
    global cur, conn
    try:
        conn = get_connection()
        cur =  conn.cursor()

        cur.execute('SELECT supervisor_id FROM department_supervisor '
                    f'WHERE department_id={department_id}')

        supervisor_data = cur.fetchone()

        if supervisor_data:
            supervisor_id = supervisor_data[0]

            cur.execute('SELECT surname, name, patronymic '
                        'FROM client '
                        f'WHERE client_id={supervisor_id}')

            supervisor = cur.fetchone()

            cur.execute(f'SELECT title FROM department WHERE department_id={department_id}')

            department = cur.fetchone()[0]

            supervisor_json = {
                'id': supervisor_id,
                'department': department,
                'supervisor': f'{supervisor[0]} {supervisor[1][0]}. {supervisor[2][0]}.'
            }

            return jsonify(supervisor_json)
        else:
            return {
                "status": "error",
                "code": 404,
                "message": f"Object with ID {department_id} not found"
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