from flask import Blueprint, jsonify
from db import get_connection

get_authorization_blueprint = Blueprint('authorization', __name__)

@get_authorization_blueprint.route('/api/v1/authorization', methods=['GET'])
def get_authorization():
    global cur, conn
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute('SELECT client_id, login, password FROM client')

        clients = cur.fetchall()

        clients_json = []
        for client in clients:
            clients_json.append(
                {
                    'id': client[0],
                    'login': client[1],
                    'password': client[2]
                }
            )

        return jsonify(clients_json)
    except:
        return {
            "status": "error",
            "code": 500,
            "message": "Internal server error. Please try again later."
        }
    finally:
        cur.close()
        conn.close()
