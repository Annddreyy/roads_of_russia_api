import pyodbc
from flask import Flask, jsonify

app = Flask(__name__)

def get_connection():
    SERVER = 'localhost'
    DATABASE = 'roads_of_russia'
    USERNAME = 'sa'
    PASSWORD = '1234'
    connectionString = (f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                        f'SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};'
                        f'Trusted_Connection=yes')

    conn = pyodbc.connect(connectionString)

    return conn

@app.route('/api/v1/news', methods=['GET'])
def get_news():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM news')

    news = cur.fetchall()

    news_json = []
    for one_news in news:
        author_id = one_news[4]
        cur.execute(f'SELECT surname, name, patronymic FROM client WHERE client_id={author_id}')
        author = cur.fetchone()

        news_json.append(
            {
                'id': one_news[0],
                'title': one_news[1],
                'description': one_news[2],
                'date': str(one_news[3]),
                'author': f'{author[0]}.{author[1][0]}.{author[2][0]}',
                'image_path': one_news[5]
            }
        )

    cur.close()
    conn.close()

    return jsonify(news_json)

@app.route('/api/v1/news/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f'SELECT * FROM news WHERE news_id={news_id}')

    news = cur.fetchall()

    news_json = []
    for one_news in news:
        author_id = one_news[4]
        cur.execute(f'SELECT surname, name, patronymic FROM client WHERE client_id={author_id}')
        author = cur.fetchone()

        news_json.append(
            {
                'id': one_news[0],
                'title': one_news[1],
                'description': one_news[2],
                'date': str(one_news[3]),
                'author': f'{author[0]}.{author[1][0]}.{author[2][0]}'
            }
        )

    cur.close()
    conn.close()

    return jsonify(news_json)

@app.route('/api/v1/resume', methods=['GET'])
def get_resume():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM resume')

    resumes = cur.fetchall()

    resumes_json = []
    for resume in resumes:
        job_id = resume[5]
        cur.execute(f'SELECT title FROM job_title WHERE job_title_id={job_id}')
        job = cur.fetchone()
        resumes_json.append(
            {
                'id': resume[0],
                'author': f'{resume[1]} {resume[2][0]}. {resume[3][0]}.',
                'file_path': resume[4].split('/')[-1],
                'job_title': job[0]
            }
        )

    cur.close()
    conn.close()

    return jsonify(resumes_json)

@app.route('/api/v1/resume/<int:resume_id>', methods=['GET'])
def get_one_resume(resume_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f'SELECT * FROM resume WHERE resume_id={resume_id}')

    resumes = cur.fetchall()

    resumes_json = []
    for resume in resumes:
        job_id = resume[5]
        cur.execute(f'SELECT title FROM job_title WHERE job_title_id={job_id}')
        job = cur.fetchone()
        resumes_json.append(
            {
                'id': resume[0],
                'author': f'{resume[1]} {resume[2][0]}. {resume[3][0]}.',
                'file_path': resume[4].split('/')[-1],
                'job_title': job[0]
            }
        )

    cur.close()
    conn.close()

    return jsonify(resumes_json)

@app.route('/api/v1/clients', methods=['GET'])
def get_clients():
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
                'photo': client[6].split('/')[-1],
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

@app.route('/api/v1/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f'SELECT * FROM client WHERE client_id={client_id}')

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
                'photo': client[6].split('/')[-1],
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

if __name__ == '__main__':
    app.run(port=2345)
