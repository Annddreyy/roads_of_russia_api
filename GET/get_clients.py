from flask import Blueprint, jsonify
from db import get_connection

get_clients_blueprint = Blueprint('clients', __name__)

@get_clients_blueprint.route('/api/v1/clients', methods=['GET'])
def get_clients():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM client')

        clients = cur.fetchall()

        clients_json = []
        for client in clients:
            department_id = client[13]
            cur.execute(f'SELECT title FROM department WHERE department_id={department_id}')
            department = cur.fetchone()[0]

            job_id = client[14]
            cur.execute(f'SELECT title FROM job_title WHERE job_title_id={job_id}')
            job = cur.fetchone()[0]

            role_id = client[15]
            cur.execute(f'SELECT title FROM system_role WHERE system_role_id={role_id}')
            role = cur.fetchone()[0]

            clients_json.append(
                {
                    'id': client[0],
                    'FIO': f'{client[1]} {client[2][0]}. {client[3][0]}.',
                    'photo': client[6],
                    'adress': client[7],
                    'phone': client[8],
                    'email': client[9],
                    'birthday_date': str(client[10]),
                    'cabinet': client[11],
                    'dop_information': client[12],
                    'department': department,
                    'job': job,
                    'role': role
                }
            )

        cur.close()
        conn.close()

        return jsonify(clients_json)
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }

@get_clients_blueprint.route('/api/v1/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(f'SELECT * FROM client WHERE client_id={client_id}')

        client = cur.fetchone()

        if client:
            client_json = []

            department_id = client[13]
            cur.execute(f'SELECT title FROM department WHERE department_id={department_id}')
            department = cur.fetchone()[0]

            job_id = client[14]
            cur.execute(f'SELECT title FROM job_title WHERE job_title_id={job_id}')
            job = cur.fetchone()[0]

            role_id = client[15]
            cur.execute(f'SELECT title FROM system_role WHERE system_role_id={role_id}')
            role = cur.fetchone()[0]

            client_json.append(
                {
                    'id': client[0],
                    'FIO': f'{client[1]} {client[2][0]}. {client[3][0]}.',
                    'photo': client[6],
                    'adress': client[7],
                    'phone': client[8],
                    'email': client[9],
                    'birthday_date': str(client[10]),
                    'cabinet': client[11],
                    'dop_information': client[12],
                    'department': department,
                    'job': job,
                    'role': role
                }
            )

            cur.close()
            conn.close()

            return jsonify(client_json)
        else:
            return {
                "status": "error",
                "code": 404,
                "message": f"Object with ID {client_id} not found"
            }
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }