from flask import Blueprint, request

from db import get_connection

patch_client_blueprint = Blueprint('patch_client', __name__)

@patch_client_blueprint.route('/api/v1/clients/<int:client_id>', methods=['PATCH'])
def patch_client(client_id):
    print(1)
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f'SELECT surname, name, patronymic, adress, phone, email, photo '
                f'FROM client WHERE client_id={client_id}')

    user_info = cur.fetchone()


    new_data = request.get_json()

    if 'surname' in new_data:
        user_info[0] = new_data['surname']
    if 'name' in new_data:
        user_info[1] = new_data['name']
    if 'patronymic' in new_data:
        user_info[2] = new_data['patronymic']
    if 'adress' in new_data:
        user_info[3] = new_data['adress']
    if 'phone' in new_data:
        user_info[4] = new_data['phone']
    if 'email' in new_data:
        user_info[5] = new_data['email']
    if 'image_path' in new_data:
        user_info[6] = new_data['image_path']

    cur.execute('UPDATE client '
                f"SET surname='{user_info[0]}', name='{user_info[1]}', patronymic='{user_info[2]}', "
                f"adress='{user_info[3]}', phone='{user_info[4]}', email='{user_info[5]}', "
                f"photo='{user_info[6]}' "
                f"WHERE client_id={client_id}")

    cur.commit()

    cur.close()
    conn.close()

    return {'message': 'Data updated successfully!'}
